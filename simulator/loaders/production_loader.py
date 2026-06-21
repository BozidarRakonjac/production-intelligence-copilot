# Inserts production event every 200 telemetry rows

import random
from datetime import timedelta
from templates.descriptions import SHIFT_NAMES, OPERATOR_NAMES, OPERATOR_NOTES

def load_production(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT udi, type, machine_id, machine_failure, inserted_at
        FROM bronze.machine_telemetry
        ORDER BY inserted_at
    """)
    rows = cursor.fetchall()

    inserted = 0
    skipped = 0
    shift_number = 0
    fault_count_in_shift = 0
    shift_index = 0
    machine_id_in_shift = None

    for i, row in enumerate(rows):
        udi, machine_type, machine_id, machine_failure, inserted_at = row
        machine_id_in_shift = machine_id

        if machine_failure == 1:
            fault_count_in_shift += 1

        if (i + 1) % 200 == 0:
            shift_number += 1
            shift_name = SHIFT_NAMES[shift_index % len(SHIFT_NAMES)]
            shift_index += 1

            end_time = inserted_at
            start_time = end_time - timedelta(hours=8)
            planned_qty = 500

            if fault_count_in_shift == 0:
                actual_qty = random.randint(470, 500)
                note = random.choice(OPERATOR_NOTES["normal"])
            elif fault_count_in_shift <= 2:
                actual_qty = random.randint(400, 469)
                note = random.choice(OPERATOR_NOTES["minor"])
            elif fault_count_in_shift <= 5:
                actual_qty = random.randint(300, 399)
                note = random.choice(OPERATOR_NOTES["serious"])
            else:
                actual_qty = random.randint(150, 299)
                note = random.choice(OPERATOR_NOTES["critical"])

            try:
                cursor.execute("""
                    INSERT INTO bronze.production_events
                        (shift_id, machine_type, machine_id, shift, planned_qty,
                         actual_qty, start_time, end_time, operator, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (shift_id) DO NOTHING
                """, (
                    shift_number, machine_type, machine_id_in_shift, shift_name,
                    planned_qty, actual_qty, start_time, end_time,
                    random.choice(OPERATOR_NAMES), note
                ))
                inserted += 1
            except Exception as e:
                print(f"Skipping production row {shift_number}: {e}")
                skipped += 1

            fault_count_in_shift = 0

    conn.commit()
    cursor.close()
    print(f"Production events loaded: {inserted} inserted, {skipped} skipped")