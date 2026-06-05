from dagster import Definitions
from resources.postgres import PostgresResource
import os

defs = Definitions(
    assets=[],
    resources={
        "postgres": PostgresResource(
            connection_string=f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
    }
)