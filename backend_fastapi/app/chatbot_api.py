from fastapi import APIRouter
from rag_assistant.rag_chain import generate_answer
from vectordb.retrieve_context import get_machine_context
from vectordb.semantic_retriever import retrieve_similar_context
from digital_twin.twin_state import get_digital_twin_state
from explainable_ai.explainer import generate_feature_explanation
from edge_ai.rul_predictor import predict_rul

router = APIRouter()

@router.post("/chat")
def chat(query: str):

    live_context = get_machine_context()
    historical_context = retrieve_similar_context(query)
    twin_context = get_digital_twin_state()
    explanation_context = generate_feature_explanation()

    # example extraction (simple demo)
    tool_wear = 100
    anomaly_score = 0.6

    rul_context = predict_rul(tool_wear, anomaly_score)

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

    return {"answer": answer}