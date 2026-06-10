from dagster import Definitions
from resources.postgres import PostgresResource
import os
from assets.bronze.machine_telemetry import bronze_machine_telemetry
from assets.bronze.downtime_logs import bronze_downtime_logs
from assets.bronze.quality_inspections import bronze_quality_inspections
from assets.bronze.production_events import bronze_production_events

defs = Definitions(
    assets=[
        bronze_machine_telemetry,
        bronze_downtime_logs,
        bronze_quality_inspections,
        bronze_production_events
    ],
    resources={
        "postgres": PostgresResource(
            connection_string=f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
    }
)