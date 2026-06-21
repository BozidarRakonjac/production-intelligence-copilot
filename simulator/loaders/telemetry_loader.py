# Read Kaggle CSV and load into bronze.machine_telemetry
from templates.descriptions import get_machine_id
import pandas as pd
import os
import random
from datetime import datetime, timedelta

def get_failure_type(row):
    if row['TWF'] == 1:
        return 'TOOL_WEAR_FAILURE'
    elif row['HDF'] == 1:
        return 'HEAT_FAILURE'
    elif row['PWF'] == 1:
        return 'POWER_FAILURE'
    elif row['OSF'] == 1:
        return 'OVERSTRAIN_FAILURE'
    elif row['RNF'] == 1:
        return 'RANDOM_FAILURE'
    else:
        return 'NONE'


def get_random_timestamp(days_back: int = 90) -> datetime:
    """Generate a random timestamp within the last N days, business hours weighted."""
    now = datetime.now()
    random_days = random.uniform(0, days_back)
    timestamp = now - timedelta(days=random_days)
    # randomize hour/minute for realism within that day
    timestamp = timestamp.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )
    return timestamp


def load_telemetry(conn):
    cursor = conn.cursor()

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ai4i2020.csv')
    df = pd.read_csv(csv_path)

    inserted = 0
    skipped = 0
    type_counters = {"L": 0, "M": 0, "H": 0}

    for _, row in df.iterrows():
        failure_type = get_failure_type(row)
        machine_type = row['Type']

        machine_id = get_machine_id(machine_type, type_counters[machine_type])
        type_counters[machine_type] += 1

        timestamp = get_random_timestamp(days_back=90)

        try:
            cursor.execute("""
                INSERT INTO bronze.machine_telemetry 
                    (udi, product_id, type, machine_id, air_temp, process_temp, 
                     rpm, torque, tool_wear, machine_failure, failure_type, inserted_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (udi) DO NOTHING
            """, (
                row['UDI'], row['Product ID'], row['Type'], machine_id,
                row['Air temperature [K]'], row['Process temperature [K]'],
                row['Rotational speed [rpm]'], row['Torque [Nm]'],
                row['Tool wear [min]'], row['Machine failure'], failure_type,
                timestamp
            ))
            inserted += 1
        except Exception as e:
            print(f"Skipping row {row['UDI']}: {e}")
            skipped += 1

    conn.commit()
    cursor.close()
    print(f"Telemetry loaded: {inserted} inserted, {skipped} skipped")