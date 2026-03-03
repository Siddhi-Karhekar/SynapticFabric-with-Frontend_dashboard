from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import random

router = APIRouter()

MACHINES = ["M1", "M2", "M3", "M4"]

def generate_machine_state(machine_id):
    return {
        "machine_id": machine_id,
        "air_temp": round(random.uniform(295, 305), 2),
        "process_temp": round(random.uniform(300, 315), 2),
        "torque": round(random.uniform(35, 55), 2),
        "tool_wear": round(random.uniform(0, 100), 2),
        "vibration": round(random.uniform(0.2, 1.0), 2),
    }

@router.websocket("/ws/machines")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            for m in MACHINES:
                state = generate_machine_state(m)
                await websocket.send_text(json.dumps(state))

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("Client disconnected")