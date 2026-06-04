from datetime import datetime, timezone

from sqlalchemy import create_engine, text

from etl.config import settings
from etl.models.pipeline_run import PipelineRunRecord


class MetadataService:
    """Track pipeline runs in etl_metadata.pipeline_runs."""

    def __init__(self) -> None:
        self.engine = create_engine(settings.database_url)

    def record_start(self, pipeline_id: str) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """
                    INSERT INTO etl_metadata.pipeline_runs (pipeline_id, status, started_at)
                    VALUES (:pipeline_id, 'running', :started_at)
                    """
                ),
                {"pipeline_id": pipeline_id, "started_at": datetime.now(timezone.utc)},
            )

    def record_finish(self, record: PipelineRunRecord) -> None:
        pass  # Implement update by pipeline_id + started_at
