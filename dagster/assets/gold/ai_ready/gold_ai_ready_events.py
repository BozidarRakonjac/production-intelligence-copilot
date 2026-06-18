import json
import pandas as pd
from dagster import Output, asset, AssetExecutionContext, AssetIn
from resources.postgres import PostgresResource
from resources.embeddings import EmbeddingResource
from utils.text_builders import build_downtime_text, build_quality_text, build_production_text
from utils.metadata_builders import build_downtime_metadata, build_quality_metadata, build_production_metadata


@asset(
    ins={
        "silver_downtime_logs": AssetIn(key_prefix="silver"),
        "silver_quality_inspections": AssetIn(key_prefix="silver"),
        "silver_production_events": AssetIn(key_prefix="silver"),
    },
    group_name="gold",
    key_prefix=["gold"],
    compute_kind="python",
    description="Builds AI-ready events table with embeddings from silver tables"
)
def gold_ai_ready_events(
    context: AssetExecutionContext,
    postgres: PostgresResource,
    embedding: EmbeddingResource,
    silver_downtime_logs: pd.DataFrame,
    silver_quality_inspections: pd.DataFrame,
    silver_production_events: pd.DataFrame,
) -> Output:

    records = []

    # Process downtime rows
    for _, row in silver_downtime_logs.iterrows():
        records.append({
            "content": build_downtime_text(row),
            "metadata": json.dumps(build_downtime_metadata(row))
        })

    # Process quality rows
    for _, row in silver_quality_inspections.iterrows():
        records.append({
            "content": build_quality_text(row),
            "metadata": json.dumps(build_quality_metadata(row))
        })

    # Process production rows
    for _, row in silver_production_events.iterrows():
        records.append({
            "content": build_production_text(row),
            "metadata": json.dumps(build_production_metadata(row))
        })

    df = pd.DataFrame(records)
    context.log.info(f"Total AI-ready records built: {len(df)}")

    # Generate embeddings for content column
    context.log.info("Generating embeddings with nomic-embed-text...")
    embeddings_model = embedding.get_embeddings()
    embeddings = embeddings_model.embed_documents(df['content'].tolist())
    df['embedding'] = embeddings
    context.log.info(f"Embeddings generated: {len(embeddings)} vectors")

    # Write to gold table
    engine = postgres.get_engine()
    df.to_sql("ai_ready_events", engine, schema="gold", if_exists="replace", index=True, index_label="id")

    context.log.info(f"Gold AI-ready events written: {len(df)} rows")

    return Output(
        value=df,
        metadata={
            "num_records": len(df),
            "num_embeddings": len(embeddings),
            "columns": list(df.columns)
        }
    )