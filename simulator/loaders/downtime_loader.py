# Reads faults from machine_telemetry and inserts into downtime_logs

import random
from datetime import timedelta
from templates.descriptions import OPERATOR_NAMES, DOWNTIME_DESCRIPTIONS, REASON_CODES

def load_downtime(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT udi, type, machine_id, failure_type, inserted_at 
        FROM bronze.machine_telemetry 
        WHERE machine_failure = 1
        ORDER BY inserted_at
    """)
    fault_rows = cursor.fetchall()

    inserted = 0
    skipped = 0

    for row in fault_rows:
        udi, machine_type, machine_id, failure_type, started_at = row

        ended_at = started_at + timedelta(minutes=random.randint(15, 180))
        duration_min = (ended_at - started_at).total_seconds() / 60

        try:
            cursor.execute("""
                INSERT INTO bronze.downtime_logs
                    (udi, machine_type, machine_id, reason_code, description, 
                     resolved_by, started_at, ended_at, duration_min)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (udi) DO NOTHING
            """, (
                udi, machine_type, machine_id,
                REASON_CODES.get(failure_type, "UNKNOWN"),
                DOWNTIME_DESCRIPTIONS.get(failure_type, "Failure detected."),
                random.choice(OPERATOR_NAMES),
                started_at, ended_at, duration_min
            ))
            inserted += 1
        except Exception as e:
            print(f"Skipping downtime row {udi}: {e}")
            skipped += 1

    conn.commit()
    cursor.close()
    print(f"Downtime logs loaded: {inserted} inserted, {skipped} skipped")