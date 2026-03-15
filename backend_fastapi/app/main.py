# ==========================================
# SYNAPTICFABRIC — FASTAPI BACKEND
# ==========================================

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import asyncio
import json

# ==========================================
# INTERNAL MODULE IMPORTS
# ==========================================

from digital_twin.simulator import run_digital_twin
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer
from backend_fastapi.ai_engine.context_store import LATEST_PLANT_CONTEXT
from rag_assistant.rag_chain import generate_answer

# DATABASE
from backend_fastapi.database.database import engine, SessionLocal
from backend_fastapi.database.models import Base, MachineLog
from backend_fastapi.database.logger import log_machine_state

# ANALYTICS
from backend_fastapi.analytics.analytics_router import router as analytics_router
from backend_fastapi.analytics.realtime_analytics import compute_realtime_analytics


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(title="SynapticFabric API")

# include analytics router
app.include_router(analytics_router)

# Create database tables
Base.metadata.create_all(bind=engine)


# ==========================================
# SAFE JSON SERIALIZER
# ==========================================

def json_safe(data):
    return json.loads(json.dumps(data, default=str))


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {"status": "SynapticFabric backend running"}


# ==========================================
# DIGITAL TWIN SNAPSHOT
# ==========================================

@app.get("/twin-status")
def twin_status():

    machines = run_digital_twin()

    analyzed = machine_analyzer.analyze_machines(machines)

    # store data in DB
    for machine in analyzed:
        log_machine_state(machine)

    valid = [
        m for m in analyzed
        if isinstance(m, dict) and "machine_id" in m
    ]

    return json_safe(valid)


# ==========================================
# PLANT CONTEXT
# ==========================================

@app.get("/plant-context")
def plant_context():
    return json_safe(LATEST_PLANT_CONTEXT)


# ==========================================
# WEBSOCKET STREAM
# ==========================================

@app.websocket("/ws/machines")
async def machine_stream(ws: WebSocket):

    await ws.accept()

    print("✅ WebSocket connected")

    try:

        while True:

            # 1️⃣ DIGITAL TWIN
            machines = run_digital_twin()

            # 2️⃣ ANALYZE MACHINES
            analyzed_machines = machine_analyzer.analyze_machines(machines)

            # 3️⃣ STORE DATA IN DATABASE
            for machine in analyzed_machines:
                log_machine_state(machine)

            # 4️⃣ FILTER VALID MACHINES
            valid = [
                m for m in analyzed_machines
                if isinstance(m, dict)
                and m.get("machine_id") is not None
            ]

            # 5️⃣ COMPUTE REALTIME ANALYTICS
            analytics = compute_realtime_analytics(valid)

            # 6️⃣ CREATE PAYLOAD
            payload = {
                "machines": valid,
                "factory_analytics": analytics
            }

            # 7️⃣ SEND TO FRONTEND
            await ws.send_json(json_safe(payload))

            await asyncio.sleep(1)

    except Exception as e:
        print("🚨 WebSocket disconnected:", e)


# ==========================================
# MAINTENANCE ENDPOINT
# ==========================================

@app.post("/maintenance/{machine_id}")
def perform_maintenance(machine_id: str):

    from digital_twin.simulator import MACHINE_MEMORY

    if machine_id in MACHINE_MEMORY:

        MACHINE_MEMORY[machine_id]["tool_wear"] *= 0.3
        MACHINE_MEMORY[machine_id]["vibration_index"] *= 0.4
        MACHINE_MEMORY[machine_id]["anomaly_score"] *= 0.2

        return {"status": f"{machine_id} maintenance complete"}

    return {"error": "machine not found"}


# ==========================================
# STREAMING AI CHAT
# ==========================================

@app.post("/chat-stream")
async def chat_stream(query: str):

    async def stream():

        answer = generate_answer(query)

        for word in answer.split():
            yield word + " "
            await asyncio.sleep(0.02)

    return StreamingResponse(stream(), media_type="text/plain")


# ==========================================
# MACHINE HISTORY API
# ==========================================

@app.get("/machine-history/{machine_id}")
def machine_history(machine_id: str, limit: int = 100):

    db = SessionLocal()

    try:

        records = (
            db.query(MachineLog)
            .filter(MachineLog.machine_id == machine_id)
            .order_by(MachineLog.timestamp.desc())
            .limit(limit)
            .all()
        )

        history = []

        for r in records:

            history.append({
                "timestamp": r.timestamp,
                "machine_id": r.machine_id,
                "temperature": r.temperature,
                "torque": r.torque,
                "tool_wear": r.tool_wear,
                "vibration_index": r.vibration_index,
                "anomaly_score": r.anomaly_score,
                "health_status": r.health_status,
                "failure_probability": r.failure_probability
            })

        return history

    finally:
        db.close()