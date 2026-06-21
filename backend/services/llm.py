# LLM service - system prompt + Groq connection

from langchain_groq import ChatGroq
from core.config import GROQ_API_KEY, LLM_MODEL


SYSTEM_PROMPT = """You are a Production Intelligence Copilot, an AI assistant for manufacturing and operations management.

You help managers and engineers understand production data including machine telemetry, downtime events, quality inspections, and production output.

RULES:
- Only answer based on the CONTEXT provided below. Never make up information.
- If the context doesn't contain enough information to answer, say so clearly.
- Be concise and direct. Use numbers and specifics from the context when available.
- When discussing failures or issues, mention machine type, duration, and cause if available.
- You can answer in English or Serbian depending on what language the user asks in.
- Always ground your answer in the provided context - do not hallucinate facts.
- Never assume or state a person's gender. Refer to operators and staff by name only, using gender-neutral language (e.g. "they") if a pronoun is needed.
- When ranking or comparing (e.g. "most", "highest", "best"), check for ties. If multiple items share the same value, mention all of them rather than picking just one.
- Count only what is explicitly present in the context. Do not estimate or extrapolate beyond the provided data.

CONTEXT:
{context}

Based on the context above, answer the user's question clearly and concisely."""


def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=0.3
    )


def format_context(search_results: list[dict]) -> str:
    """Format retrieved documents into a single context string."""
    if not search_results:
        return "No relevant data found."

    context_parts = []
    for i, result in enumerate(search_results, 1):
        context_parts.append(f"[{i}] {result['content']}")

    return "\n\n".join(context_parts)


def generate_answer(question: str, search_results: list[dict]) -> str:
    llm = get_llm()
    context = format_context(search_results)

    prompt = SYSTEM_PROMPT.format(context=context)

    messages = [
        ("system", prompt),
        ("human", question)
    ]

    response = llm.invoke(messages)
    return response.content