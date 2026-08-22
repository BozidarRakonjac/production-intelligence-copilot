# Builds human-readable content text for AI embedding per silver table row

def _clean_parts(parts: list) -> str:
    """Join parts filtering out empty, null, or unknown values."""
    return " | ".join([
        p for p in parts
        if p
        and not p.endswith(": ")
        and not p.endswith(": unknown")
        and not p.endswith(": nan")
        and not p.endswith(": None")
        and not p.endswith(": 0")
    ])


def build_downtime_text(row) -> str:
    parts = [
        f"Machine: {row.get('machine_id', '')} (type {row.get('machine_type', '')})",
        f"Date: {row.get('started_at', '')}",
        f"Failure: {row.get('reason_code', '')}",
        f"Description: {row.get('description', '')}",
        f"Duration: {row.get('duration_min', '')} minutes",
        f"Resolved by: {row.get('resolved_by', '')}",
    ]
    return _clean_parts(parts)


def build_quality_text(row) -> str:
    parts = [
        f"Machine: {row.get('machine_id', '')} (type {row.get('machine_type', '')})",
        f"Date: {row.get('inspected_at', '')}",
        f"Defect type: {row.get('defect_type', '')}",
        f"Defects found: {row.get('defect_count', '')} out of {row.get('sample_size', '')} samples",
        f"Defect rate: {row.get('defect_rate', '')}%",
        f"Description: {row.get('description', '')}",
        f"Result: {row.get('pass_fail', '')}",
    ]
    return _clean_parts(parts)


def build_production_text(row) -> str:
    parts = [
        f"Machine: {row.get('machine_id', '')} (type {row.get('machine_type', '')})",
        f"Date: {row.get('start_time', '')}",
        f"Shift: {row.get('shift', '')}",
        f"Output: {row.get('actual_qty', '')} out of {row.get('planned_qty', '')} planned units",
        f"Efficiency: {row.get('efficiency', '')}%",
        f"Operator: {row.get('operator', '')}",
        f"Notes: {row.get('notes', '')}",
    ]
    return _clean_parts(parts)