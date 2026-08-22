import pandas as pd
from dagster import asset
from resources.postgres import PostgresResource

@asset(
    key_prefix=["bronze"],
    group_name="bronze",
    compute_kind="python",
    description="Reads raw machine telemetry from bronze schema"
)

def bronze_machine_telemetry(postgres: PostgresResource):
    engine = postgres.get_engine()
    df = pd.read_sql("SELECT * FROM bronze.machine_telemetry", engine)
    print(f"Bronze telemetry loaded: {len(df)} rows")
    return df