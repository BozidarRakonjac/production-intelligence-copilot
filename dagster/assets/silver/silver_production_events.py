import pandas as pd
from dagster import Output, asset, AssetExecutionContext, AssetIn
from resources.postgres import PostgresResource


@asset(
    ins={"bronze_production_events": AssetIn(key_prefix="bronze")},
    group_name="silver",
    key_prefix=["silver"],
    compute_kind="python",
    description="Cleans and transforms bronze production events into silver, adds efficiency"
)
def silver_production_events(context: AssetExecutionContext, postgres: PostgresResource, bronze_production_events: pd.DataFrame) -> Output:

    df = bronze_production_events.copy()
    initial_count = len(df)

    # Safety checks
    df = df.drop_duplicates(subset=['shift_id'])
    df = df.dropna(subset=['shift_id', 'start_time', 'end_time'])
    df = df[df['actual_qty'] >= 0]
    df = df[df['actual_qty'] <= df['planned_qty']]

    dropped = initial_count - len(df)
    if dropped > 0:
        context.log.warning(f"Dropped {dropped} invalid/duplicate rows")

    if df.empty:
        context.log.warning("No data received from bronze_production_events!")

    df['efficiency'] = (df['actual_qty'] / df['planned_qty'] * 100).round(2)

    engine = postgres.get_engine()
    df.to_sql("production_events", engine, schema="silver", if_exists="replace", index=False)

    context.log.info(f"Silver production events written: {len(df)} rows")

    return Output(
        value=df,
        metadata={"num_records": len(df), "columns": list(df.columns)}
    )