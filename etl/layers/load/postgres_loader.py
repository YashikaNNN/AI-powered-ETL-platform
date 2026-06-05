from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from etl.config import settings
from etl.layers.load.base import BaseLoader
from etl.utils.logging import get_logger

logger = get_logger(__name__)


class PostgresLoader(BaseLoader):
    def __init__(
        self,
        table: str,
        schema: str = "analytics",
        columns: list[str] | None = None,
        on_conflict_column: str | None = None,
        engine: Engine | None = None,
    ) -> None:
        self.table = table
        self.schema = schema
        self.columns = columns or []
        self.on_conflict_column = on_conflict_column
        self.engine = engine or create_engine(settings.database_url)

    def load(self, records: list[dict[str, Any]]) -> int:
        if not records:
            return 0

        columns = self.columns or list(records[0].keys())
        col_list = ", ".join(columns)
        param_list = ", ".join(f":{col}" for col in columns)
        conflict_clause = (
            f" ON CONFLICT ({self.on_conflict_column}) DO NOTHING"
            if self.on_conflict_column
            else ""
        )
        stmt = text(
            f"""
            INSERT INTO {self.schema}.{self.table} ({col_list})
            VALUES ({param_list}){conflict_clause}
            """
        )

        payload = [{col: record[col] for col in columns} for record in records]

        with self.engine.begin() as conn:
            result = conn.execute(stmt, payload)
            inserted = result.rowcount if result.rowcount >= 0 else len(payload)

        logger.info("Loaded %s row(s) into %s.%s", inserted, self.schema, self.table)
        return inserted
