from langchain_community.llms import Ollama

from backend_fastapi.ai_engine.context_store import LATEST_PLANT_CONTEXT
# Faster deterministic responses
llm = Ollama(
    model="llama3",
    temperature=0.1,
)


def generate_answer(user_query: str) -> str:
    """
    Ultra-fast AI response using cached plant context.
    """

    context = LATEST_PLANT_CONTEXT

    prompt = f"""
You are an Industrial AI Maintenance Engineer.

LIVE PLANT STATUS:
{context}

USER QUESTION:
{user_query}

Provide concise engineering reasoning and actions.
"""

    response = llm.invoke(prompt)

    return response