# LangChain agent - decides between semantic search and SQL aggregation tools

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from core.config import GROQ_API_KEY, LLM_MODEL
from services.retrieval import hybrid_search
from services.sql_tool import (
    operator_shift_stats,
    machine_failure_stats,
    quality_defect_stats,
    shift_performance_stats,
    overall_summary_stats,
    machine_quality_stats
)


@tool
def search_events(query: str) -> str:
    """Search for specific events, incidents, or descriptions about machine 
    failures, quality issues, or production notes. Use this for 'why' or 
    'what happened' questions about specific incidents."""
    results = hybrid_search(query, {})
    if not results:
        return "No relevant events found."
    return "\n\n".join([r["content"] for r in results])


@tool
def get_operator_statistics() -> str:
    """Get statistics about operators including total shifts, critical 
    shifts count, and average efficiency per operator. Use this for 
    questions about which operator performs best/worst or has most issues."""
    return operator_shift_stats()


@tool
def get_machine_failure_statistics() -> str:
    """Get failure counts and downtime statistics grouped by machine type 
    (L, M, H). Use this for questions about which machine fails most or 
    has most downtime."""
    return machine_failure_stats()


@tool
def get_quality_statistics() -> str:
    """Get defect statistics grouped by defect type. Use this for questions 
    about most common defects or quality issue patterns."""
    return quality_defect_stats()

@tool
def get_machine_quality_statistics() -> str:
    """Get defect rate statistics grouped by machine type (L, M, H). Use 
    this for questions comparing quality/defects across different machines, 
    or combining machine downtime with machine quality issues."""
    return machine_quality_stats()



@tool
def get_shift_statistics() -> str:
    """Get performance statistics grouped by shift (morning/evening/night). 
    Use this for questions comparing shift performance."""
    return shift_performance_stats()


@tool
def get_overall_summary() -> str:
    """Get high level summary statistics across all production data. Use 
    this for general overview questions."""
    return overall_summary_stats()


SYSTEM_PROMPT = """You are a Production Intelligence Copilot, an AI assistant for manufacturing and operations management.

You help managers and engineers understand production data including machine telemetry, downtime events, quality inspections, and production output.

RULES:
    - Use the available tools to answer questions accurately. Choose the right tool based on the question type:
    - For "why" or "what happened" questions about specific incidents -> use search_events
    - For counting, ranking, or "which X has most/least Y" questions -> use the relevant statistics tool
    - For general overview questions -> use get_overall_summary
    - Never make up information. Only answer based on tool results.
    - Be concise and direct. Use exact numbers from tool results.
    - Never assume or state a person's gender. Use gender-neutral language.
    - When ranking or comparing, check for ties. If multiple items share the same value, mention all of them.
    - This system reflects a snapshot of current operational data. It does not perform predictive simulations, forecasts, or what-if analysis.
    - If a question requires data dimensions not available in any tool (e.g. defect rate by shift, when shift only exists in production data), clearly state what data is available instead of guessing or inventing calculations.
    - If asked a hypothetical or predictive question (e.g. "what if we reduced X"), explain that this system shows current real data, not simulations, and offer the closest real statistic instead.
    - You can answer in English or Serbian depending on what language the user asks in.
"""


def get_agent():
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=0.3
    )

    tools = [
        search_events,
        get_operator_statistics,
        get_machine_failure_statistics,
        get_quality_statistics,
        get_shift_statistics,
        get_overall_summary,
    ]

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )


def generate_agent_answer(question: str) -> dict:
    agent = get_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    
    # Extract final answer from last message
    final_message = result["messages"][-1]
    answer = final_message.content
    
    return {"output": answer}