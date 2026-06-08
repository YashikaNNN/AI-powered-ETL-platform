from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from etl.models.pipeline_run import PipelineRunRecord
from etl.pipelines.sample_pipeline import SamplePipeline
from etl.services.metadata_service import MetadataService
from etl.utils.logging import get_logger

logger = get_logger(__name__)

ETL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ETL_ROOT / "data" / "raw" / "sample.csv"


@dataclass
class PipelineExecutionResult:
    run_id: int
    pipeline_id: str
    status: str
    started_at: datetime
    finished_at: datetime
    row_count: int | None = None
    error_message: str | None = None


def execute_sample_pipeline(
    source_path: Path | None = None,
) -> PipelineExecutionResult:
    """Run SamplePipeline with MetadataService lifecycle tracking."""
    metadata = MetadataService()
    source = source_path or DEFAULT_SOURCE
    pipeline = SamplePipeline(source_path=source)
    started_at = datetime.now(timezone.utc)
    run_id = metadata.record_start(pipeline.pipeline_id)

    logger.info("Pipeline run %s started for %s", run_id, pipeline.pipeline_id)

    try:
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source}")

        row_count = pipeline.run()
        finished_at = datetime.now(timezone.utc)
        metadata.record_finish(
            run_id,
            PipelineRunRecord(
                pipeline_id=pipeline.pipeline_id,
                status="success",
                started_at=started_at,
                run_id=run_id,
                finished_at=finished_at,
                row_count=row_count,
            ),
        )
        logger.info(
            "Pipeline run %s completed: %s rows loaded",
            run_id,
            row_count,
        )
        return PipelineExecutionResult(
            run_id=run_id,
            pipeline_id=pipeline.pipeline_id,
            status="success",
            started_at=started_at,
            finished_at=finished_at,
            row_count=row_count,
        )
    except Exception as exc:
        finished_at = datetime.now(timezone.utc)
        metadata.record_finish(
            run_id,
            PipelineRunRecord(
                pipeline_id=pipeline.pipeline_id,
                status="failed",
                started_at=started_at,
                run_id=run_id,
                finished_at=finished_at,
                error_message=str(exc),
            ),
        )
        logger.exception("Pipeline run %s failed", run_id)
        return PipelineExecutionResult(
            run_id=run_id,
            pipeline_id=pipeline.pipeline_id,
            status="failed",
            started_at=started_at,
            finished_at=finished_at,
            error_message=str(exc),
        )
