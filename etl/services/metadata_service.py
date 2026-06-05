from datetime import datetime, timezone

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from etl.config import settings
from etl.models.pipeline_run import PipelineRunRecord


class MetadataService:
    """Track pipeline runs in etl_metadata.pipeline_runs."""

    def __init__(self, engine: Engine | None = None) -> None:
        self.engine = engine or create_engine(settings.database_url)

    def record_start(self, pipeline_id: str) -> int:
        with self.engine.begin() as conn:
            result = conn.execute(
                text(
                    """
                    INSERT INTO etl_metadata.pipeline_runs (pipeline_id, status, started_at)
                    VALUES (:pipeline_id, 'running', :started_at)
                    RETURNING id
                    """
                ),
                {
                    "pipeline_id": pipeline_id,
                    "started_at": datetime.now(timezone.utc),
                },
            )
            run_id = result.scalar_one()
        return int(run_id)

    def record_finish(self, run_id: int, record: PipelineRunRecord) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """
                    UPDATE etl_metadata.pipeline_runs
                    SET status = :status,
                        finished_at = :finished_at,
                        row_count = :row_count,
                        error_message = :error_message
                    WHERE id = :run_id
                    """
                ),
                {
                    "run_id": run_id,
                    "status": record.status,
                    "finished_at": record.finished_at,
                    "row_count": record.row_count,
                    "error_message": record.error_message,
                },
            )
