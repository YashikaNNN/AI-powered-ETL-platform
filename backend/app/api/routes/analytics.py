from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.analytics import (
    AnalyticsSummaryResponse,
    InsightRequest,
    InsightResponse,
    PaginatedEventsResponse,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/events", response_model=PaginatedEventsResponse)
async def list_events(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
) -> PaginatedEventsResponse:
    service = AnalyticsService(db)
    return await service.list_events(page=page, page_size=page_size)


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    db: AsyncSession = Depends(get_db),
) -> AnalyticsSummaryResponse:
    service = AnalyticsService(db)
    return await service.get_summary()


@router.post("/insights", response_model=InsightResponse)
async def generate_insights(
    payload: InsightRequest,
    db: AsyncSession = Depends(get_db),
) -> InsightResponse:
    service = AnalyticsService(db)
    return await service.generate_insight(payload)
