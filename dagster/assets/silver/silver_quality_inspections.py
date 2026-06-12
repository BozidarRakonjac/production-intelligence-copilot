import pandas as pd
from dagster import Output, asset, AssetExecutionContext, AssetIn
from resources.postgres import PostgresResource


@asset(
    ins={"bronze_quality_inspections": AssetIn(key_prefix="bronze")},
    group_name="silver",
    key_prefix=["silver"],
    compute_kind="python",
    description="Cleans and transforms bronze quality inspections into silver, adds defect_rate"
)
def silver_quality_inspections(context: AssetExecutionContext, postgres: PostgresResource, bronze_quality_inspections: pd.DataFrame) -> Output:

    df = bronze_quality_inspections.copy()

    df['defect_rate'] = (df['defect_count'] / df['sample_size'] * 100).round(2)

    engine = postgres.get_engine()
    df.to_sql("quality_inspections", engine, schema="silver", if_exists="replace", index=False)

    context.log.info(f"Silver quality inspections written: {len(df)} rows")

    return Output(
        value=df,
        metadata={"num_records": len(df), "columns": list(df.columns)}
    )