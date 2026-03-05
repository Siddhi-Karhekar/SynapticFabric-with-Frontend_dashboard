# ==========================================
# SYNAPTICFABRIC — FASTAPI BACKEND
# ==========================================

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import asyncio
import json

from digital_twin.simulator import run_digital_twin, MACHINE_MEMORY
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer
from backend_fastapi.ai_engine.context_store import LATEST_PLANT_CONTEXT
from rag_assistant.rag_chain import generate_answer


app = FastAPI(title="SynapticFabric API")


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
# REST ENDPOINTS
# ==========================================

@app.get("/")
def root():
    return {"status": "SynapticFabric backend running"}


@app.get("/twin-status")
def twin_status():

    machines = run_digital_twin()
    analyzed = machine_analyzer.analyze_machines(machines)

    valid = [
        m for m in analyzed
        if isinstance(m, dict) and "machine_id" in m
    ]

    return json_safe(valid)


@app.get("/plant-context")
def plant_context():
    return json_safe(LATEST_PLANT_CONTEXT)


# ==========================================
# MAINTENANCE ENDPOINT
# ==========================================

@app.post("/maintenance/{machine_id}")
def perform_maintenance(machine_id: str):

    if machine_id in MACHINE_MEMORY:

        MACHINE_MEMORY[machine_id]["tool_wear"] *= 0.3
        MACHINE_MEMORY[machine_id]["vibration_index"] *= 0.4
        MACHINE_MEMORY[machine_id]["anomaly_score"] *= 0.2

        return {"status": f"{machine_id} maintenance complete"}

    return {"error": "machine not found"}


# ==========================================
# WEBSOCKET STREAM
# ==========================================

@app.websocket("/ws/machines")
async def machine_stream(ws: WebSocket):

    await ws.accept()
    print("✅ WebSocket connected")

    try:
        while True:

            machines = run_digital_twin()
            analyzed = machine_analyzer.analyze_machines(machines)

            valid = [
                m for m in analyzed
                if isinstance(m, dict) and m.get("machine_id")
            ]

            await ws.send_json(json_safe(valid))

            await asyncio.sleep(1)

    except Exception as e:
        print("🚨 WEBSOCKET CRASH:", e)


# ==========================================
# STREAMING CHAT
# ==========================================

@app.post("/chat-stream")
async def chat_stream(query: str):

    async def stream():

        answer = generate_answer(query)

        for word in answer.split():
            yield word + " "
            await asyncio.sleep(0.02)

    return StreamingResponse(stream(), media_type="text/plain")