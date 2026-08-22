# Inserts quality inspection every 30 telemetry rows
# Defect type is based on failure type for realism
# Failed batches can have multiple defect types

import random
from templates.descriptions import DEFECT_TYPES, QUALITY_DESCRIPTIONS, FAILURE_TO_DEFECT_MAP

def load_quality(conn):
    cursor = conn.cursor()

    # Read all telemetry rows ordered by udi
    cursor.execute("""
        SELECT udi, type, machine_failure, failure_type, inserted_at
        FROM bronze.machine_telemetry
        ORDER BY udi
    """)
    rows = cursor.fetchall()

    inserted = 0
    skipped = 0
    batch_number = 0
    fault_in_batch = False
    failure_types_in_batch = []

    for i, row in enumerate(rows):
        udi, machine_type, machine_failure, failure_type, inserted_at = row

        # Track failures in current batch
        if machine_failure == 1:
            fault_in_batch = True
            failure_types_in_batch.append(failure_type)

        # Every 30 rows create quality inspection
        if (i + 1) % 30 == 0:
            batch_number += 1

            if fault_in_batch:
                # Pick defects based on actual failure types that happened
                possible_defects = []
                for ft in failure_types_in_batch:
                    possible_defects.extend(FAILURE_TO_DEFECT_MAP.get(ft, DEFECT_TYPES))
                
                # Remove duplicates
                possible_defects = list(set(possible_defects))
                
                # Pick 1-3 defect types realistically
                num_defects = random.randint(1, min(3, len(possible_defects)))
                selected_defects = random.sample(possible_defects, k=num_defects)
                
                defect_count = random.randint(5, 15)
                pass_fail = "FAIL"
            else:
                # Normal batch - random minor defect or none
                selected_defects = random.sample(DEFECT_TYPES, k=1)
                defect_count = random.randint(0, 3)
                pass_fail = "PASS"

            # Use first defect type as primary, combine descriptions
            primary_defect = selected_defects[0]
            description = " | ".join([
                QUALITY_DESCRIPTIONS.get(d, "") for d in selected_defects
            ])

            try:
                cursor.execute("""
                    INSERT INTO bronze.quality_inspections
                        (batch_id, machine_type, inspected_at, sample_size,
                         defect_count, defect_type, description, pass_fail)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (batch_id) DO NOTHING
                """, (
                    batch_number,
                    machine_type,
                    inserted_at,
                    50,
                    defect_count,
                    primary_defect,
                    description,
                    pass_fail
                ))
                inserted += 1
            except Exception as e:
                print(f"Skipping quality row {batch_number}: {e}")
                skipped += 1

            # Reset for next batch
            fault_in_batch = False
            failure_types_in_batch = []

    conn.commit()
    cursor.close()
    print(f"Quality inspections loaded: {inserted} inserted, {skipped} skipped")