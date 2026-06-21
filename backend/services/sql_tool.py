# SQL aggregation tool - safe predefined queries for counting/ranking questions

from sqlalchemy import create_engine, text
from core.config import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL)


def operator_shift_stats() -> str:
    """Count shifts per operator broken down by efficiency category."""
    engine = get_engine()
    sql = text("""
        SELECT 
            operator,
            COUNT(*) as total_shifts,
            COUNT(*) FILTER (WHERE efficiency < 60) as critical_shifts,
            ROUND(AVG(efficiency)::numeric, 2) as avg_efficiency
        FROM silver.production_events
        GROUP BY operator
        ORDER BY critical_shifts DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()

    lines = ["Operator shift statistics:"]
    for row in rows:
        lines.append(
            f"- {row[0]}: {row[1]} total shifts, {row[2]} critical shifts, "
            f"{row[3]}% avg efficiency"
        )
    return "\n".join(lines)


def machine_failure_stats() -> str:
    """Count failures and downtime per machine type."""
    engine = get_engine()
    sql = text("""
        SELECT 
            machine_type,
            COUNT(*) as total_failures,
            ROUND(AVG(duration_min)::numeric, 2) as avg_downtime,
            SUM(duration_min) as total_downtime
        FROM silver.downtime_logs
        GROUP BY machine_type
        ORDER BY total_failures DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()

    lines = ["Machine failure statistics:"]
    for row in rows:
        lines.append(
            f"- Machine {row[0]}: {row[1]} failures, "
            f"{row[2]} min avg downtime, {row[3]} min total downtime"
        )
    return "\n".join(lines)


def quality_defect_stats() -> str:
    """Defect statistics grouped by defect type."""
    engine = get_engine()
    sql = text("""
        SELECT 
            defect_type,
            COUNT(*) as occurrences,
            ROUND(AVG(defect_rate)::numeric, 2) as avg_defect_rate
        FROM silver.quality_inspections
        WHERE defect_count > 0
        GROUP BY defect_type
        ORDER BY occurrences DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()

    lines = ["Quality defect statistics:"]
    for row in rows:
        lines.append(
            f"- {row[0]}: occurred {row[1]} times, {row[2]}% avg defect rate"
        )
    return "\n".join(lines)


def shift_performance_stats() -> str:
    """Performance statistics grouped by shift (morning/evening/night)."""
    engine = get_engine()
    sql = text("""
        SELECT 
            shift,
            COUNT(*) as total_shifts,
            ROUND(AVG(efficiency)::numeric, 2) as avg_efficiency,
            SUM(actual_qty) as total_produced,
            SUM(planned_qty) as total_planned
        FROM silver.production_events
        GROUP BY shift
        ORDER BY avg_efficiency DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()

    lines = ["Shift performance statistics:"]
    for row in rows:
        lines.append(
            f"- {row[0].capitalize()} shift: {row[1]} shifts, "
            f"{row[2]}% avg efficiency, {row[3]}/{row[4]} units produced"
        )
    return "\n".join(lines)


def machine_quality_stats() -> str:
    """Defect rate statistics grouped by machine type."""
    engine = get_engine()
    sql = text("""
        SELECT 
            machine_type,
            COUNT(*) as total_inspections,
            ROUND(AVG(defect_rate)::numeric, 2) as avg_defect_rate,
            SUM(defect_count) as total_defects
        FROM silver.quality_inspections
        GROUP BY machine_type
        ORDER BY avg_defect_rate DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()

    lines = ["Machine quality statistics:"]
    for row in rows:
        lines.append(
            f"- Machine {row[0]}: {row[1]} inspections, "
            f"{row[2]}% avg defect rate, {row[3]} total defects"
        )
    return "\n".join(lines)


def overall_summary_stats() -> str:
    """High level summary across all data."""
    engine = get_engine()
    sql = text("""
        SELECT
            (SELECT COUNT(*) FROM silver.downtime_logs) as total_downtime_events,
            (SELECT ROUND(AVG(duration_min)::numeric, 2) FROM silver.downtime_logs) as avg_downtime,
            (SELECT ROUND(AVG(defect_rate)::numeric, 2) FROM silver.quality_inspections) as avg_defect_rate,
            (SELECT ROUND(AVG(efficiency)::numeric, 2) FROM silver.production_events) as avg_efficiency
    """)
    with engine.connect() as conn:
        row = conn.execute(sql).fetchone()

    return (
        f"Overall summary: {row[0]} total downtime events, "
        f"{row[1]} min avg downtime, {row[2]}% avg defect rate, "
        f"{row[3]}% avg production efficiency"
    )