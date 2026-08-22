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
    initial_count = len(df)

    # Safety checks
    df = df.drop_duplicates(subset=['udi'])
    df = df.dropna(subset=['udi', 'started_at', 'ended_at'])
    df = df[df['duration_min'] > 0]
    df = df[df['ended_at'] > df['started_at']]

    dropped = initial_count - len(df)
    if dropped > 0:
        context.log.warning(f"Dropped {dropped} invalid/duplicate rows")

    if df.empty:
        context.log.warning("No data received from bronze_downtime_logs!")

    df['duration_min'] = df['duration_min'].round(2)

    engine = postgres.get_engine()
    df.to_sql("downtime_logs", engine, schema="silver", if_exists="replace", index=False)

    context.log.info(f"Silver downtime logs written: {len(df)} rows")

    return Output(
        value=df,
        metadata={"num_records": len(df), "columns": list(df.columns)}
    )