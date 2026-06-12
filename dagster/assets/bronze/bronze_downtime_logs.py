import pandas as pd
from dagster import asset
from resources.postgres import PostgresResource

@asset(
    key_prefix=["bronze"],
    group_name="bronze",
    compute_kind="python",
    description="Reads raw downtime logs from bronze schema"
)

def bronze_downtime_logs(postgres: PostgresResource):
    engine = postgres.get_engine()
    df = pd.read_sql("SELECT * FROM bronze.downtime_logs", engine)
    print(f"Bronze downtime logs loaded: {len(df)} rows")
    return df