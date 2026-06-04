from typing import Any

from sqlalchemy import create_engine, text

from etl.config import settings
from etl.layers.load.base import BaseLoader


class PostgresLoader(BaseLoader):
    def __init__(self, table: str, schema: str = "analytics") -> None:
        self.table = table
        self.schema = schema
        self.engine = create_engine(settings.database_url)

    def load(self, records: list[dict[str, Any]]) -> int:
        if not records:
            return 0
        # Starter: implement bulk insert via COPY or executemany
        return len(records)
