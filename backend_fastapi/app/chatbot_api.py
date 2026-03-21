from fastapi import APIRouter, Body
import ollama

from digital_twin.simulator import MACHINE_MEMORY
from backend_fastapi.ai_engine.machine_analyzer import machine_analyzer  # ✅ FIX

router = APIRouter()


@router.post("/chat")
async def chat(payload: dict = Body(...)):

    query = payload.get("query", "")
    print("📩 QUERY:", query)

    # ==========================================
    # 🔍 MACHINE ANALYSIS
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
            "health_status": "Unknown",
            "rul_cycles": 0,
            "rul_time": "unknown",
            "root_cause": []
        }

    # ==========================================
    # 🔍 ROOT CAUSE
    # ==========================================

    root_causes = highest.get("root_cause", [])

    if root_causes:
        root_cause_text = "\n".join([
            f"- {c.get('issue')} ({round(c.get('confidence', 0)*100)}%)"
            for c in root_causes if c.get("confidence", 0) > 0.3
        ])
    else:
        root_cause_text = "No significant issues detected."

    # ==========================================
    # 🧠 CONTEXT
    # ==========================================

    context = f"""
Machine ID: {highest.get('machine_id')}

Health: {highest.get('health_status')}
Failure Risk: {round(highest.get('prediction', 0) * 100)}%

RUL:
- Cycles: {highest.get('rul_cycles')}
- Time: {highest.get('rul_time')}

Sensors:
- Temp: {round(highest.get('temperature', 0), 2)} °C
- Vibration: {round(highest.get('vibration_index', 0), 3)}
- Wear: {round(highest.get('tool_wear', 0)*100,1)}%
- Torque: {round(highest.get('torque', 0), 2)}

Root Causes:
{root_cause_text}
"""

    # ==========================================
    # 🤖 LLM
    # ==========================================

    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "system",
                    "content": "Industrial AI assistant. Answer briefly and explain root cause."
                },
                {
                    "role": "user",
                    "content": f"{context}\n\nQuestion: {query}"
                }
            ],
            options={"temperature": 0.3}
        )

        answer = response.get("message", {}).get("content")

    except Exception as e:
        print("❌ OLLAMA ERROR:", e)
        answer = None

    # ==========================================
    # 🛡 FALLBACK
    # ==========================================

    if not answer:
        issue = root_causes[0]["issue"] if root_causes else "unknown issue"

        answer = (
            f"{highest['machine_id']} has highest risk ({round(highest['prediction']*100)}%) "
            f"due to {issue}. RUL: {highest.get('rul_cycles')} cycles."
        )

    print("✅ ANSWER:", answer)

    return {"answer": answer}