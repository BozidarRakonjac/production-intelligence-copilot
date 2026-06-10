import pandas as pd
from dagster import asset
from resources.postgres import PostgresResource

@asset
def bronze_quality_inspections(postgres: PostgresResource):
    engine = postgres.get_engine()
    df = pd.read_sql("SELECT * FROM bronze.quality_inspections", engine)
    print(f"Bronze quality inspections loaded: {len(df)} rows")
    return df