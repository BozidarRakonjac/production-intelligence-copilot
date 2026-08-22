# LangChain agent - decides between semantic search and SQL aggregation tools

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from core.config import GROQ_API_KEY, LLM_MODEL
from services.retrieval import hybrid_search
from services.sql_tool import (
    overall_summary_stats,
    downtime_breakdown,
    quality_breakdown,
    production_breakdown,
    machine_full_report,
)


@tool
def search_events(query: str) -> str:
    """Search for EXAMPLE descriptions of specific incidents to understand 
    WHAT happened, the cause, and resolution details. Returns only a few 
    example matches - NEVER use this for counting or 'how many' questions."""
    results = hybrid_search(query, {})
    if not results:
        return "No relevant events found."
    return "\n\n".join([r["content"] for r in results])


@tool
def get_kpi_summary(time_range: str = "all_time") -> str:
    """Get overall KPI summary: downtime, MTTR, defect rate, quality rate, 
    performance, estimated OEE. time_range options: 'today', 'yesterday', 
    'this_week', 'this_month', 'last_30_days', 'last_90_days', 'all_time'."""
    return overall_summary_stats(time_range)


@tool
def get_downtime_breakdown(group_by: str = "machine_id", time_range: str = "all_time") -> str:
    """Get downtime counts and durations grouped by a dimension. 
    group_by options: 'machine_id' (specific machine like L-01), 
    'machine_type' (L/M/H category), 'reason_code' (failure type), 
    'resolved_by' (technician). time_range options: 'today', 'yesterday', 
    'this_week', 'this_month', 'last_30_days', 'last_90_days', 'all_time'."""
    return downtime_breakdown(group_by, time_range)


@tool
def get_quality_breakdown(group_by: str = "machine_id", time_range: str = "all_time") -> str:
    """Get quality/defect statistics grouped by a dimension. 
    group_by options: 'machine_id', 'machine_type', 'defect_type'. 
    time_range options: 'today', 'yesterday', 'this_week', 'this_month', 
    'last_30_days', 'last_90_days', 'all_time'."""
    return quality_breakdown(group_by, time_range)


@tool
def get_production_breakdown(group_by: str = "machine_id", time_range: str = "all_time") -> str:
    """Get production/efficiency statistics grouped by a dimension. 
    group_by options: 'machine_id', 'machine_type', 'shift', 'operator'. 
    time_range options: 'today', 'yesterday', 'this_week', 'this_month', 
    'last_30_days', 'last_90_days', 'all_time'."""
    return production_breakdown(group_by, time_range)


@tool
def get_machine_report(machine_id: str) -> str:
    """Get a complete report for one specific machine by its ID 
    (e.g. 'L-01', 'M-02', 'H-01'): failures, repair time, defect rate, 
    efficiency. Use this for 'what happened on machine X' or 
    'compare machine A vs B' questions (call once per machine)."""
    return machine_full_report(machine_id)


SYSTEM_PROMPT = """You are a Production Intelligence Copilot, an AI assistant for manufacturing and operations management.

You help managers and engineers monitor KPIs, investigate issues, and compare performance using real production data covering machine telemetry, downtime, quality, and production output across 10 machines (L-01 to L-05, M-01 to M-03, H-01 to H-02) over the last 90 days.

RULES:
- ALWAYS use a statistics tool for counts, frequency, "how many", "most/least", rankings, or comparisons. NEVER use search_events for these.
- Use search_events ONLY to find details/descriptions of specific incidents.
- Use get_machine_report for "what happened on machine X" or comparing specific machines.
- Use get_downtime_breakdown / get_quality_breakdown / get_production_breakdown with the right group_by for ranking/comparison questions (by machine, type, shift, operator, technician, defect type, or reason).
- Use get_kpi_summary for overview/executive summary questions, with time_range matching what was asked.
- Never make up information. Only answer based on tool results.
- Never assume or state a person's gender. Use gender-neutral language.
- When ranking or comparing, check for ties. If multiple items share the same value, mention all of them.
- This system reflects real historical operational data over the last 90 days. It does not perform predictive simulations or what-if analysis.
- For executive summaries, call get_kpi_summary plus the relevant breakdown tools and synthesize into a clear report.
- You can answer in English or Serbian depending on what language the user asks in.
- You can answer in Serbian ONLY if the user's question is written in Serbian. If the question is in English, you MUST respond in English. Match the user's input language exactly, do not switch languages on your own.
"""


def get_agent():
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=0.3
    )

    tools = [
        search_events,
        get_kpi_summary,
        get_downtime_breakdown,
        get_quality_breakdown,
        get_production_breakdown,
        get_machine_report,
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