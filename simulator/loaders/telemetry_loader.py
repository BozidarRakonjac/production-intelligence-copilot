# Read Kaggle CSV and load into bronze.machine_telemetry

import pandas as pd
import os

def get_failure_type(row):
    # Combine 5 failure columns into one clean failure_type
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

def load_telemetry(conn):
    cursor = conn.cursor()
    
    # Read CSV from data folder
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ai4i2020.csv')
    df = pd.read_csv(csv_path)
    
    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        failure_type = get_failure_type(row)
        
        try:
            cursor.execute("""
                INSERT INTO bronze.machine_telemetry 
                    (udi, product_id, type, air_temp, process_temp, 
                     rpm, torque, tool_wear, machine_failure, failure_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (udi) DO NOTHING
            """, (
                row['UDI'],
                row['Product ID'],
                row['Type'],
                row['Air temperature [K]'],
                row['Process temperature [K]'],
                row['Rotational speed [rpm]'],
                row['Torque [Nm]'],
                row['Tool wear [min]'],
                row['Machine failure'],
                failure_type
            ))
            inserted += 1
        except Exception as e:
            print(f"Skipping row {row['UDI']}: {e}")
            skipped += 1

    conn.commit()
    cursor.close()
    print(f"Telemetry loaded: {inserted} inserted, {skipped} skipped")