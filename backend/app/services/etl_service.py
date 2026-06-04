from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pipeline_run import PipelineRun
from app.schemas.etl import PipelineRunCreate, PipelineRunResponse


class ETLService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_runs(self) -> list[PipelineRunResponse]:
        result = await self.db.execute(
            select(PipelineRun).order_by(PipelineRun.started_at.desc()).limit(50)
        )
        runs = result.scalars().all()
        return [PipelineRunResponse.model_validate(r) for r in runs]

    async def create_run(self, payload: PipelineRunCreate) -> PipelineRunResponse:
        run = PipelineRun(pipeline_id=payload.pipeline_id, status="pending")
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        return PipelineRunResponse.model_validate(run)
