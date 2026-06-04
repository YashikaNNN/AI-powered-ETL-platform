from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.analytics import InsightRequest, InsightResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/insights", response_model=InsightResponse)
async def generate_insights(
    payload: InsightRequest,
    db: AsyncSession = Depends(get_db),
) -> InsightResponse:
    service = AnalyticsService(db)
    return await service.generate_insight(payload)
