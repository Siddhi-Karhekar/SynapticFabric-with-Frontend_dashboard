from fastapi import APIRouter, Body
import asyncio

from rag_assistant.rag_chain import generate_answer
from vectordb.retrieve_context import get_machine_context
from vectordb.semantic_retriever import retrieve_similar_context
from digital_twin.twin_state import get_digital_twin_state
from explainable_ai.explainer import generate_feature_explanation
from edge_ai.rul_predictor import predict_rul

# 🔍 NEW IMPORTS (safe addition)
from digital_twin.simulator import MACHINE_MEMORY
from backend_fastapi.ai_engine.root_cause import analyze_root_cause

router = APIRouter()


@router.post("/chat")
async def chat(payload: dict = Body(...)):

    query = payload.get("query", "")

    # ==========================================
    # ⚡ PARALLEL CONTEXT COLLECTION
    # ==========================================

    live_task = asyncio.to_thread(get_machine_context)
    rag_task = asyncio.to_thread(retrieve_similar_context, query)
    twin_task = asyncio.to_thread(get_digital_twin_state)
    explain_task = asyncio.to_thread(generate_feature_explanation)

    tool_wear = 100
    anomaly_score = 0.6
    rul_task = asyncio.to_thread(predict_rul, tool_wear, anomaly_score)

    (
        live_context,
        historical_context,
        twin_context,
        explanation_context,
        rul_context
    ) = await asyncio.gather(
        live_task,
        rag_task,
        twin_task,
        explain_task,
        rul_task
    )

    full_context = f"""
CURRENT MACHINE STATE:
{live_context}

DIGITAL TWIN PREDICTION:
{twin_context}

SIMILAR PAST CONDITIONS:
{historical_context}

EXPLAINABLE AI ANALYSIS:
{explanation_context}

RUL ESTIMATION:
{rul_context}
"""

    answer = generate_answer(full_context, query)

    return {
        "answer": answer
    }


# ==========================================================
# 🔍 NEW INSPECT ENDPOINT (SAFE ADDITION)
# ==========================================================
# ADD / REPLACE THIS PART




@router.post("/inspect")
def inspect_machine(payload: dict = Body(...)):

    machine_id = payload.get("machine_id")

    if not machine_id:
        return {"error": "machine_id is required"}

    if machine_id not in MACHINE_MEMORY:
        return {"error": "Machine not found"}

    machine = MACHINE_MEMORY[machine_id]

    diagnosis = analyze_root_cause(machine)

    return {
        "machine_id": machine_id,
        "diagnosis": diagnosis
    }