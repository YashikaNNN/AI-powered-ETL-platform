from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.etl import PipelineRunCreate, PipelineRunResponse
from app.services.etl_service import ETLService

router = APIRouter(prefix="/etl", tags=["etl"])


@router.get("/runs", response_model=list[PipelineRunResponse])
async def list_pipeline_runs(
    db: AsyncSession = Depends(get_db),
) -> list[PipelineRunResponse]:
    service = ETLService(db)
    return await service.list_runs()


@router.post("/runs", response_model=PipelineRunResponse, status_code=201)
async def trigger_pipeline_run(
    payload: PipelineRunCreate,
    db: AsyncSession = Depends(get_db),
) -> PipelineRunResponse:
    service = ETLService(db)
    return await service.execute_run(payload)
