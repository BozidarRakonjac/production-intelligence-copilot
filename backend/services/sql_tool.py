# SQL aggregation tools - covers standard manufacturing KPIs
# Supports filtering by machine_id and time range

from sqlalchemy import create_engine, text
from core.config import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL)


def _date_filter_clause(time_range: str) -> str:
    """Returns a SQL WHERE clause fragment for the given time range."""
    ranges = {
        "today": "CURRENT_DATE",
        "yesterday": "CURRENT_DATE - INTERVAL '1 day'",
        "this_week": "CURRENT_DATE - INTERVAL '7 days'",
        "this_month": "CURRENT_DATE - INTERVAL '30 days'",
        "last_30_days": "CURRENT_DATE - INTERVAL '30 days'",
        "last_90_days": "CURRENT_DATE - INTERVAL '90 days'",
        "all_time": None,
    }
    if time_range not in ranges or ranges[time_range] is None:
        return "1=1"
    if time_range == "today":
        return "date_col = CURRENT_DATE"
    if time_range == "yesterday":
        return "date_col = CURRENT_DATE - INTERVAL '1 day'"
    return f"date_col >= {ranges[time_range]}"


def overall_summary_stats(time_range: str = "all_time") -> str:
    """High level KPI summary: downtime, MTTR, defect rate, quality rate, performance, OEE estimate."""
    engine = get_engine()
    downtime_filter = _date_filter_clause(time_range).replace("date_col", "started_at::date")
    quality_filter = _date_filter_clause(time_range).replace("date_col", "inspected_at::date")
    production_filter = _date_filter_clause(time_range).replace("date_col", "start_time::date")

    sql = text(f"""
        SELECT
            (SELECT COUNT(*) FROM silver.downtime_logs WHERE {downtime_filter}) as total_downtime_events,
            (SELECT ROUND(AVG(duration_min)::numeric, 2) FROM silver.downtime_logs WHERE {downtime_filter}) as avg_repair_time,
            (SELECT ROUND(SUM(duration_min)::numeric, 2) FROM silver.downtime_logs WHERE {downtime_filter}) as total_downtime_min,
            (SELECT ROUND(AVG(defect_rate)::numeric, 2) FROM silver.quality_inspections WHERE {quality_filter}) as avg_defect_rate,
            (SELECT ROUND(AVG(efficiency)::numeric, 2) FROM silver.production_events WHERE {production_filter}) as avg_performance,
            (SELECT SUM(actual_qty) FROM silver.production_events WHERE {production_filter}) as total_produced,
            (SELECT SUM(planned_qty) FROM silver.production_events WHERE {production_filter}) as total_planned
    """)
    with engine.connect() as conn:
        row = conn.execute(sql).fetchone()

    if row[0] is None and row[5] is None:
        return f"No data found for time range: {time_range}"

    quality_rate = round(100 - row[3], 2) if row[3] is not None else None
    oee_estimate = round((row[4] / 100) * (quality_rate / 100) * 100, 2) if row[4] and quality_rate else None

    return (
        f"KPI summary ({time_range}):\n"
        f"- Total downtime events: {row[0]}\n"
        f"- Average repair time (MTTR): {row[1]} min\n"
        f"- Total downtime: {row[2]} min\n"
        f"- Average defect rate: {row[3]}%\n"
        f"- Quality rate (good units): {quality_rate}%\n"
        f"- Average performance/efficiency: {row[4]}%\n"
        f"- Total produced: {row[5]} / {row[6]} planned units\n"
        f"- Estimated OEE: {oee_estimate}%"
    )


def downtime_breakdown(group_by: str = "machine_id", time_range: str = "all_time") -> str:
    """Downtime event counts and durations grouped by a dimension.
    group_by options: 'machine_id', 'machine_type', 'reason_code', 'resolved_by'"""
    valid_columns = {"machine_id", "machine_type", "reason_code", "resolved_by"}
    if group_by not in valid_columns:
        return f"Invalid group_by '{group_by}'. Valid options: {valid_columns}"

    engine = get_engine()
    date_filter = _date_filter_clause(time_range).replace("date_col", "started_at::date")

    sql = text(f"""
        SELECT 
            {group_by},
            COUNT(*) as occurrences,
            ROUND(AVG(duration_min)::numeric, 2) as avg_duration,
            ROUND(SUM(duration_min)::numeric, 2) as total_duration
        FROM silver.downtime_logs
        WHERE {date_filter}
        GROUP BY {group_by}
        ORDER BY occurrences DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()

    if not rows:
        return f"No downtime data found for time range: {time_range}"

    lines = [f"Downtime breakdown by {group_by} ({time_range}):"]
    for row in rows:
        lines.append(
            f"- {row[0]}: {row[1]} occurrences, {row[2]} min avg duration, {row[3]} min total"
        )
    return "\n".join(lines)


def quality_breakdown(group_by: str = "machine_id", time_range: str = "all_time") -> str:
    """Quality/defect statistics grouped by a dimension.
    group_by options: 'machine_id', 'machine_type', 'defect_type'"""
    valid_columns = {"machine_id", "machine_type", "defect_type"}
    if group_by not in valid_columns:
        return f"Invalid group_by '{group_by}'. Valid options: {valid_columns}"

    engine = get_engine()
    date_filter = _date_filter_clause(time_range).replace("date_col", "inspected_at::date")

    sql = text(f"""
        SELECT 
            {group_by},
            COUNT(*) as total_inspections,
            ROUND(AVG(defect_rate)::numeric, 2) as avg_defect_rate,
            SUM(defect_count) as total_defects,
            COUNT(*) FILTER (WHERE pass_fail = 'FAIL') as failed_inspections
        FROM silver.quality_inspections
        WHERE {date_filter}
        GROUP BY {group_by}
        ORDER BY avg_defect_rate DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()

    if not rows:
        return f"No quality data found for time range: {time_range}"

    lines = [f"Quality breakdown by {group_by} ({time_range}):"]
    for row in rows:
        lines.append(
            f"- {row[0]}: {row[1]} inspections, {row[2]}% avg defect rate, "
            f"{row[3]} total defects, {row[4]} failed inspections"
        )
    return "\n".join(lines)


def production_breakdown(group_by: str = "machine_id", time_range: str = "all_time") -> str:
    """Production/efficiency statistics grouped by a dimension.
    group_by options: 'machine_id', 'machine_type', 'shift', 'operator'"""
    valid_columns = {"machine_id", "machine_type", "shift", "operator"}
    if group_by not in valid_columns:
        return f"Invalid group_by '{group_by}'. Valid options: {valid_columns}"

    engine = get_engine()
    date_filter = _date_filter_clause(time_range).replace("date_col", "start_time::date")

    sql = text(f"""
        SELECT 
            {group_by},
            COUNT(*) as total_shifts,
            ROUND(AVG(efficiency)::numeric, 2) as avg_efficiency,
            SUM(actual_qty) as total_produced,
            SUM(planned_qty) as total_planned,
            COUNT(*) FILTER (WHERE efficiency < 60) as critical_shifts
        FROM silver.production_events
        WHERE {date_filter}
        GROUP BY {group_by}
        ORDER BY avg_efficiency DESC
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).fetchall()

    if not rows:
        return f"No production data found for time range: {time_range}"

    lines = [f"Production breakdown by {group_by} ({time_range}):"]
    for row in rows:
        lines.append(
            f"- {row[0]}: {row[1]} shifts, {row[2]}% avg efficiency, "
            f"{row[3]}/{row[4]} units produced, {row[5]} critical shifts"
        )
    return "\n".join(lines)


def machine_full_report(machine_id: str) -> str:
    """Complete report for a single specific machine: downtime, quality, and production stats."""
    engine = get_engine()

    sql = text("""
        SELECT 
            (SELECT COUNT(*) FROM silver.downtime_logs WHERE machine_id = :mid) as failures,
            (SELECT ROUND(AVG(duration_min)::numeric, 2) FROM silver.downtime_logs WHERE machine_id = :mid) as avg_repair,
            (SELECT ROUND(AVG(defect_rate)::numeric, 2) FROM silver.quality_inspections WHERE machine_id = :mid) as defect_rate,
            (SELECT ROUND(AVG(efficiency)::numeric, 2) FROM silver.production_events WHERE machine_id = :mid) as efficiency
    """)
    with engine.connect() as conn:
        row = conn.execute(sql, {"mid": machine_id}).fetchone()

    if row[0] is None and row[2] is None and row[3] is None:
        return f"No data found for machine {machine_id}. Check the machine_id is correct (e.g. L-01, M-02, H-01)."

    return (
        f"Report for machine {machine_id}:\n"
        f"- Total failures: {row[0]}\n"
        f"- Average repair time: {row[1]} min\n"
        f"- Average defect rate: {row[2]}%\n"
        f"- Average efficiency: {row[3]}%"
    )