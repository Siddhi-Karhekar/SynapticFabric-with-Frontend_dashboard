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

    while True:
        machines = run_digital_twin()

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

        analyzed = machine_analyzer.analyze_machines(machines)

        avg_risk = sum(m["prediction"] for m in analyzed) / len(analyzed)
        unstable = max(analyzed, key=lambda x: x["prediction"])

        analytics = {
            "plant_health_score": round((1 - avg_risk) * 100, 1),
            "most_unstable_machine": unstable["machine_id"],
            "total_machines": len(analyzed),
            "machines_needing_attention": [
                m["machine_id"]
                for m in analyzed
                if m["health_status"] != "Healthy"
            ]
        }

        await ws.send_json({
            "machines": analyzed,
            "factory_analytics": analytics
        })

        await asyncio.sleep(1)


@app.post("/maintenance/{machine_id}")
def maintain(machine_id: str):

    if machine_id not in MACHINE_MEMORY:
        return {"status": "error", "message": "machine not found"}

    MACHINE_MEMORY[machine_id]["tool_wear"] = 0.02
    MACHINE_MEMORY[machine_id]["vibration_index"] = 0.15
    MACHINE_MEMORY[machine_id]["temperature"] = 293
    MACHINE_MEMORY[machine_id]["torque"] = 38

    MAINTENANCE_COOLDOWN[machine_id] = time.time()

    return {"status": "success", "machine": machine_id}