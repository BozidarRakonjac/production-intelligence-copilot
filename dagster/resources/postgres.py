from dagster import ConfigurableResource
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

class PostgresResource(ConfigurableResource):
    connection_string: str

    def get_engine(self) -> Engine:
        return create_engine(self.connection_string)