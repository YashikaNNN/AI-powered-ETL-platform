import asyncio
import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.integrations.etl.bootstrap import configure_etl_database, ensure_etl_importable
from app.models.pipeline_run import PipelineRun
from app.schemas.etl import PipelineRunCreate, PipelineRunResponse

logger = logging.getLogger(__name__)


class ETLService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_runs(self) -> list[PipelineRunResponse]:
        result = await self.db.execute(
            select(PipelineRun).order_by(PipelineRun.started_at.desc()).limit(50)
        )
        runs = result.scalars().all()
        return [PipelineRunResponse.model_validate(r) for r in runs]

    async def execute_run(self, payload: PipelineRunCreate) -> PipelineRunResponse:
        ensure_etl_importable()
        configure_etl_database(settings.database_url_sync)

        from etl.pipelines.sample_pipeline import SamplePipeline
        from etl.services.pipeline_runner import execute_sample_pipeline

        if payload.pipeline_id != SamplePipeline.pipeline_id:
            logger.warning("Unsupported pipeline requested: %s", payload.pipeline_id)
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported pipeline: {payload.pipeline_id}. "
                    f"Supported pipeline: {SamplePipeline.pipeline_id}"
                ),
            )

        logger.info("Executing pipeline %s via API", payload.pipeline_id)

        result = await asyncio.to_thread(execute_sample_pipeline)

        logger.info(
            "Pipeline run %s finished with status=%s row_count=%s",
            result.run_id,
            result.status,
            result.row_count,
        )

        run = await self.db.get(PipelineRun, result.run_id)
        if run is not None:
            return PipelineRunResponse.model_validate(run)

        return PipelineRunResponse(
            id=result.run_id,
            pipeline_id=result.pipeline_id,
            status=result.status,
            started_at=result.started_at,
            finished_at=result.finished_at,
            row_count=result.row_count,
            error_message=result.error_message,
        )
