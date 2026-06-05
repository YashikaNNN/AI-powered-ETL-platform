"""CLI entrypoint: python -m etl.jobs.run_pipeline"""

from datetime import datetime, timezone
from pathlib import Path

from etl.models.pipeline_run import PipelineRunRecord
from etl.pipelines.sample_pipeline import SamplePipeline
from etl.services.metadata_service import MetadataService
from etl.utils.logging import get_logger

logger = get_logger(__name__)

ETL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ETL_ROOT / "data" / "raw" / "sample.csv"


def main() -> None:
    metadata = MetadataService()
    pipeline = SamplePipeline(source_path=DEFAULT_SOURCE)
    started_at = datetime.now(timezone.utc)
    run_id = metadata.record_start(pipeline.pipeline_id)

    try:
        if not DEFAULT_SOURCE.exists():
            raise FileNotFoundError(f"Source file not found: {DEFAULT_SOURCE}")

        row_count = pipeline.run()
        metadata.record_finish(
            run_id,
            PipelineRunRecord(
                pipeline_id=pipeline.pipeline_id,
                status="success",
                started_at=started_at,
                run_id=run_id,
                finished_at=datetime.now(timezone.utc),
                row_count=row_count,
            ),
        )
        logger.info("Pipeline run %s completed: %s rows loaded", run_id, row_count)
    except Exception as exc:
        metadata.record_finish(
            run_id,
            PipelineRunRecord(
                pipeline_id=pipeline.pipeline_id,
                status="failed",
                started_at=started_at,
                run_id=run_id,
                finished_at=datetime.now(timezone.utc),
                error_message=str(exc),
            ),
        )
        logger.exception("Pipeline run %s failed", run_id)
        raise


if __name__ == "__main__":
    main()
