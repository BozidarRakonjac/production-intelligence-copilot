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

    df['air_temp_celsius'] = df['air_temp'] - 273.15
    df['process_temp_celsius'] = df['process_temp'] - 273.15

    engine = postgres.get_engine()
    df.to_sql("machine_telemetry", engine, schema="silver", if_exists="replace", index=False)

    context.log.info(f"Silver machine telemetry written: {len(df)} rows")

    return Output(
        value=df,
        metadata={"num_records": len(df), "columns": list(df.columns)}
    )