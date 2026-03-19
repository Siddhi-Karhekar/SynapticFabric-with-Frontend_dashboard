from fastapi import APIRouter, Body
import ollama

from digital_twin.simulator import MACHINE_MEMORY
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer

router = APIRouter()


# ==========================================
# 🤖 CHAT ENDPOINT (LLM + SAFE HYBRID)
# ==========================================

@router.post("/chat")
async def chat(payload: dict = Body(...)):

    query = payload.get("query", "")
    print("📩 QUERY:", query)

    # ==========================================
    # 🔍 MACHINE ANALYSIS (ALWAYS WORKS)
    # ==========================================

    try:
        machines = []

        for k, v in MACHINE_MEMORY.items():
            machines.append({
                "machine_id": k,
                "temperature": v.get("temperature", 295),
                "torque": v.get("torque", 40),
                "tool_wear": v.get("tool_wear", 0.1),
                "vibration_index": v.get("vibration_index", 0.2)
            })

        analyzed = machine_analyzer.analyze_machines(machines)

        highest = max(analyzed, key=lambda x: x["prediction"])

    except Exception as e:
        print("❌ ANALYSIS ERROR:", e)

        highest = {
            "machine_id": "M_1",
            "prediction": 0.5,
            "health_status": "Unknown"
        }

    # ==========================================
    # 🧠 CONTEXT FOR LLM
    # ==========================================

    context = f"""
Machine ID: {highest['machine_id']}
Failure Probability: {round(highest['prediction'] * 100)}%
Health Status: {highest['health_status']}
Temperature: {highest.get('temperature', 0)}
Vibration: {highest.get('vibration_index', 0)}
Tool Wear: {highest.get('tool_wear', 0)}
Torque: {highest.get('torque', 0)}
"""

    # ==========================================
    # 🤖 LLM CALL (SAFE)
    # ==========================================

    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an industrial AI assistant for CNC machines."
                },
                {
                    "role": "user",
                    "content": f"""
Answer briefly (1-2 sentences).

{context}

Question: {query}
"""
                }
            ],
            options={
                "temperature": 0.3
            }
        )

        answer = response.get("message", {}).get("content", None)

    except Exception as e:
        print("❌ OLLAMA ERROR:", e)
        answer = None

    # ==========================================
    # 🛡 FALLBACK (NEVER FAIL)
    # ==========================================

    if not answer:
        answer = (
            f"Machine {highest['machine_id']} has the highest failure risk "
            f"({round(highest['prediction'] * 100)}%) and is in "
            f"{highest['health_status']} state."
        )

    print("✅ FINAL ANSWER:", answer)

    return {"answer": answer}