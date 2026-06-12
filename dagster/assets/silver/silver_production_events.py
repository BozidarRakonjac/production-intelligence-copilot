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

    df['efficiency'] = (df['actual_qty'] / df['planned_qty'] * 100).round(2)

    engine = postgres.get_engine()
    df.to_sql("production_events", engine, schema="silver", if_exists="replace", index=False)

    context.log.info(f"Silver production events written: {len(df)} rows")

    return Output(
        value=df,
        metadata={"num_records": len(df), "columns": list(df.columns)}
    )