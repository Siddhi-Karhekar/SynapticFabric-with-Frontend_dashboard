# ==========================================
# SYNAPTICFABRIC — FASTAPI BACKEND (FINAL FIX)
# ==========================================

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import asyncio
import json
import math

# ------------------------------------------
# INTERNAL MODULE IMPORTS
# ------------------------------------------

from digital_twin.simulator import run_digital_twin
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer
from backend_fastapi.ai_engine.context_store import LATEST_PLANT_CONTEXT
from rag_assistant.rag_chain import generate_answer


# ==========================================
# APP INIT
# ==========================================

app = FastAPI(title="SynapticFabric API")


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
# ✅ WEBSOCKET — FINAL STABLE VERSION
# ==========================================

@app.websocket("/ws/machines")
async def machine_stream(ws: WebSocket):
    await ws.accept()

    print("✅ WebSocket connected")

    try:
        while True:

            # 1️⃣ Generate twin
            machines = run_digital_twin()

            # 2️⃣ Run AI analyzer
            analyzed_machines = machine_analyzer.analyze_machines(machines)

            # ✅ 3️⃣ HARD FILTER (CRITICAL FIX)
            valid = [
                m for m in analyzed_machines
                if isinstance(m, dict)
                and m.get("machine_id") is not None
            ]

            print("Sending machines:", valid)

            # 4️⃣ Send ONLY valid machines
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