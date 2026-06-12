import pandas as pd
from dagster import Output, asset, AssetExecutionContext, AssetIn
from resources.postgres import PostgresResource


@asset(
    ins={"bronze_machine_telemetry": AssetIn(key_prefix="bronze")},
    group_name="silver",
    key_prefix=["silver"],
    compute_kind="python",
    description="Cleans and transforms bronze telemetry into silver"
)
def silver_machine_telemetry(context: AssetExecutionContext, postgres: PostgresResource, bronze_machine_telemetry: pd.DataFrame) -> Output:

    df = bronze_machine_telemetry.copy()
    initial_count = len(df)

    # Safety checks
    df = df.drop_duplicates(subset=['udi'])
    df = df.dropna(subset=['udi', 'inserted_at'])
    df = df[df['air_temp'] > 0]
    df = df[df['process_temp'] > 0]
    df = df[df['rpm'] > 0]

    dropped = initial_count - len(df)
    if dropped > 0:
        context.log.warning(f"Dropped {dropped} invalid/duplicate rows")

    if df.empty:
        context.log.warning("No data received from bronze_machine_telemetry!")


    df['air_temp_celsius'] = df['air_temp'] - 273.15
    df['process_temp_celsius'] = df['process_temp'] - 273.15

    engine = postgres.get_engine()
    df.to_sql("machine_telemetry", engine, schema="silver", if_exists="replace", index=False)

    context.log.info(f"Silver machine telemetry written: {len(df)} rows")

    return Output(
        value=df,
        metadata={"num_records": len(df), "columns": list(df.columns)}
    )