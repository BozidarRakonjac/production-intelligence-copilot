import pandas as pd
from dagster import Output, asset, AssetExecutionContext, AssetIn
from resources.postgres import PostgresResource


@asset(
    ins={"bronze_downtime_logs": AssetIn(key_prefix="bronze")},
    group_name="silver",
    key_prefix=["silver"],
    compute_kind="python",
    description="Cleans and transforms bronze downtime logs into silver"
)

def silver_downtime_logs(context: AssetExecutionContext, postgres: PostgresResource, bronze_downtime_logs: pd.DataFrame) -> Output:

    df = bronze_downtime_logs.copy()

    df['duration_min'] = df['duration_min'].round(2)

    engine = postgres.get_engine()
    df.to_sql("downtime_logs", engine, schema="silver", if_exists="replace", index=False)

    context.log.info(f"Silver downtime logs written: {len(df)} rows")

    return Output(
        value=df,
        metadata={"num_records": len(df), "columns": list(df.columns)}
    )