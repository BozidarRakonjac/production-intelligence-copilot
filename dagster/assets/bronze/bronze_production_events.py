import pandas as pd
from dagster import asset
from resources.postgres import PostgresResource

@asset(
    key_prefix=["bronze"],
    group_name="bronze",
    compute_kind="python",
    description="Reads raw production events from bronze schema"
)
def bronze_production_events(postgres: PostgresResource):
    engine = postgres.get_engine()
    df = pd.read_sql("SELECT * FROM bronze.production_events", engine)
    print(f"Bronze production events loaded: {len(df)} rows")
    return df