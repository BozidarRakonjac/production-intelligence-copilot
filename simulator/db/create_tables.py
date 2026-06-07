# Create bronze schema, enable pgvector extension and 4 tables

import psycopg2

def create_tables(conn):
    cursor = conn.cursor()
    
    # Enable pgvector extension
    cursor.execute("""
        CREATE EXTENSION IF NOT EXISTS vector;
    """)

    # Create bronze schema
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS bronze;
    """)

    # Table 1 - raw sensor data from Kaggle CSV
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bronze.machine_telemetry (
            id              SERIAL PRIMARY KEY,
            udi             INTEGER UNIQUE,
            product_id      VARCHAR(20),
            type            VARCHAR(5),
            air_temp        FLOAT,
            process_temp    FLOAT,
            rpm             INTEGER,
            torque          FLOAT,
            tool_wear       INTEGER,
            machine_failure INTEGER,
            failure_type    VARCHAR(50),
            inserted_at     TIMESTAMP DEFAULT NOW()
        );
    """)

    # Table 2 - logged whenever fault detected in telemetry
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bronze.downtime_logs (
            id              SERIAL PRIMARY KEY,
            udi             INTEGER UNIQUE,
            machine_type    VARCHAR(5),
            reason_code     VARCHAR(50),
            description     TEXT,
            resolved_by     VARCHAR(50),
            started_at      TIMESTAMP,
            ended_at        TIMESTAMP,
            duration_min    FLOAT
        );
    """)

    # Table 3 - logged every 30 rows of telemetry
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bronze.quality_inspections (
            id              SERIAL PRIMARY KEY,
            batch_id        INTEGER UNIQUE,
            machine_type    VARCHAR(5),
            inspected_at    TIMESTAMP,
            sample_size     INTEGER,
            defect_count    INTEGER,
            defect_type     VARCHAR(50),
            description     TEXT,
            pass_fail       VARCHAR(10)
        );
    """)

    # Table 4 - logged every 200 rows of telemetry
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bronze.production_events (
            id              SERIAL PRIMARY KEY,
            shift_id        INTEGER UNIQUE,
            machine_type    VARCHAR(5),
            shift           VARCHAR(20),
            planned_qty     INTEGER,
            actual_qty      INTEGER,
            start_time      TIMESTAMP,
            end_time        TIMESTAMP,
            operator        VARCHAR(50),
            notes           TEXT
        );
    """)

    conn.commit()
    cursor.close()
    print("Bronze schema, pgvector extension and tables created successfully")