from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time

from digital_twin.simulator import run_digital_twin, MACHINE_MEMORY
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer

# ✅ CHAT ROUTER
from backend_fastapi.app.chatbot_api import router as chatbot_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ REGISTER CHAT ROUTES
app.include_router(chatbot_router)

MAINTENANCE_COOLDOWN = {}
COOLDOWN_TIME = 20


@app.websocket("/ws/machines")
async def stream(ws: WebSocket):

    await ws.accept()
    print("✅ WebSocket connected")

    try:
        while True:

            # ======================================
            # 🔥 DIGITAL TWIN
            # ======================================

            machines = run_digital_twin()

            # ======================================
            # 🔧 MAINTENANCE COOLDOWN
            # ======================================

            for m in machines:
                mid = m["machine_id"]

                if mid in MAINTENANCE_COOLDOWN:
                    elapsed = time.time() - MAINTENANCE_COOLDOWN[mid]

                    if elapsed < COOLDOWN_TIME:
                        m["tool_wear"] = 0.02
                        m["vibration_index"] = 0.15
                        m["temperature"] = 293
                        m["torque"] = 38
                    else:
                        del MAINTENANCE_COOLDOWN[mid]

            # ======================================
            # 🤖 AI ANALYSIS
            # ======================================

            analyzed = machine_analyzer.analyze_machines(machines)

            print("📡 Sending analyzed data:", analyzed)

            # ======================================
            # 🛡 SAFE ANALYTICS (NO CRASH)
            # ======================================

            safe_predictions = [
                m.get("prediction", m.get("anomaly_score", 0))
                for m in analyzed
            ]

            avg_risk = sum(safe_predictions) / len(safe_predictions)

            unstable = max(
                analyzed,
                key=lambda x: x.get("prediction", x.get("anomaly_score", 0))
            )

            analytics = {
                "plant_health_score": round((1 - avg_risk) * 100, 1),
                "most_unstable_machine": unstable.get("machine_id", "Unknown"),
                "total_machines": len(analyzed),
                "machines_needing_attention": [
                    m.get("machine_id")
                    for m in analyzed
                    if m.get("health_status") != "Healthy"
                ]
            }

            # ======================================
            # 📡 SEND DATA
            # ======================================

            await ws.send_json({
                "machines": analyzed,
                "factory_analytics": analytics
            })

            await asyncio.sleep(1)

    except Exception as e:
        print("❌ WebSocket runtime error:", e)

    finally:
        print("🔌 WebSocket connection closed")