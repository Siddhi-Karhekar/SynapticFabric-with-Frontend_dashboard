from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time

from digital_twin.simulator import run_digital_twin, MACHINE_MEMORY
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer

# ==========================================
# INIT
# ==========================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# GLOBAL STATE
# ==========================================

MAINTENANCE_COOLDOWN = {}
COOLDOWN_TIME = 20  # seconds

# ==========================================
# WEBSOCKET STREAM
# ==========================================

@app.websocket("/ws/machines")
async def stream(ws: WebSocket):
    await ws.accept()
    print("✅ WebSocket connected")

    while True:

        # 🔥 STEP 1: GET DIGITAL TWIN DATA
        machines = run_digital_twin()

        # 🔧 STEP 2: APPLY MAINTENANCE COOLDOWN
        for m in machines:
            mid = m["machine_id"]

            if mid in MAINTENANCE_COOLDOWN:
                elapsed = time.time() - MAINTENANCE_COOLDOWN[mid]

                if elapsed < COOLDOWN_TIME:
                    # 🔒 Freeze machine in healthy state
                    m["tool_wear"] = 0.05
                    m["vibration_index"] = 0.25
                    m["temperature"] = 295
                    m["torque"] = 40
                else:
                    # ✅ cooldown finished
                    del MAINTENANCE_COOLDOWN[mid]

        # 🤖 STEP 3: ANALYZE MACHINES
        analyzed = machine_analyzer.analyze_machines(machines)

        # 📊 STEP 4: FACTORY ANALYTICS
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

        # 📡 STEP 5: SEND TO FRONTEND
        await ws.send_json({
            "machines": analyzed,
            "factory_analytics": analytics
        })

        await asyncio.sleep(1)


# ==========================================
# 🔧 MAINTENANCE ENDPOINT
# ==========================================

@app.post("/maintenance/{machine_id}")
def maintain(machine_id: str):

    if machine_id not in MACHINE_MEMORY:
        return {
            "status": "error",
            "message": "machine not found"
        }

    # ✅ HARD RESET MACHINE STATE
    MACHINE_MEMORY[machine_id]["tool_wear"] = 0.05
    MACHINE_MEMORY[machine_id]["vibration_index"] = 0.25
    MACHINE_MEMORY[machine_id]["temperature"] = 295
    MACHINE_MEMORY[machine_id]["torque"] = 40

    # ✅ START COOLDOWN TIMER
    MAINTENANCE_COOLDOWN[machine_id] = time.time()

    return {
        "status": "success",
        "machine": machine_id
    }