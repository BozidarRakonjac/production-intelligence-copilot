# Builds structured metadata dict for AI filtering per silver table row

def build_downtime_metadata(row) -> dict:
    return {
        "source_table": "downtime",
        "event_date": str(row['started_at'].date()),
        "machine_type": row['machine_type'],
        "reason_code": row['reason_code'],
        "duration_min": float(row['duration_min']),
        "duration_category": _duration_category(row['duration_min']),
        "resolved_by": row['resolved_by']
    }


def build_quality_metadata(row) -> dict:
    return {
        "source_table": "quality",
        "event_date": str(row['inspected_at'].date()),
        "machine_type": row['machine_type'],
        "defect_type": row['defect_type'],
        "defect_count": int(row['defect_count']),
        "defect_rate": float(row['defect_rate']),
        "defect_category": _defect_category(row['defect_rate']),
        "pass_fail": row['pass_fail']
    }


def build_production_metadata(row) -> dict:
    efficiency = float(row['efficiency'])
    return {
        "source_table": "production",
        "event_date": str(row['start_time'].date()),
        "machine_type": row['machine_type'],
        "shift": row['shift'],
        "planned_qty": int(row['planned_qty']),
        "actual_qty": int(row['actual_qty']),
        "efficiency": efficiency,
        "efficiency_category": _efficiency_category(efficiency),
        "operator": row['operator']
    }


# Private helper functions

def _efficiency_category(efficiency: float) -> str:
    if efficiency < 60:
        return "low"
    elif efficiency < 80:
        return "medium"
    else:
        return "high"


def _defect_category(defect_rate: float) -> str:
    if defect_rate == 0:
        return "none"
    elif defect_rate < 10:
        return "low"
    elif defect_rate < 20:
        return "medium"
    else:
        return "high"


def _duration_category(duration_min: float) -> str:
    if duration_min < 30:
        return "short"
    elif duration_min < 90:
        return "medium"
    else:
        return "long"