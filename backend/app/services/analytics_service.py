import logging
import math
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.integrations.openrouter_client import OpenRouterClient
from app.models.sample_event import SampleEvent
from app.schemas.analytics import (
    AnalyticsSummaryResponse,
    EventTypeCount,
    InsightRequest,
    InsightResponse,
    PaginatedEventsResponse,
    SampleEventResponse,
)

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.gemini = OpenRouterClient()

    async def list_events(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedEventsResponse:
        offset = (page - 1) * page_size

        try:
            total_result = await self.db.execute(
                select(func.count()).select_from(SampleEvent)
            )
            total = total_result.scalar_one()

            result = await self.db.execute(
                select(SampleEvent)
                .order_by(SampleEvent.event_timestamp.desc())
                .offset(offset)
                .limit(page_size)
            )
            events = result.scalars().all()

            total_pages = math.ceil(total / page_size) if total > 0 else 0

            logger.info(
                "Listed events page=%s page_size=%s total=%s returned=%s",
                page,
                page_size,
                total,
                len(events),
            )

            return PaginatedEventsResponse(
                items=[SampleEventResponse.model_validate(e) for e in events],
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
            )

        except SQLAlchemyError as exc:
            logger.exception("Database error while listing events")
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch events",
            ) from exc

    async def get_summary(self) -> AnalyticsSummaryResponse:
        try:
            totals_result = await self.db.execute(
                select(
                    func.count(SampleEvent.id),
                    func.coalesce(func.sum(SampleEvent.amount), 0),
                )
            )
            total_events, total_revenue = totals_result.one()

            breakdown_result = await self.db.execute(
                select(SampleEvent.event_type, func.count(SampleEvent.id))
                .group_by(SampleEvent.event_type)
                .order_by(SampleEvent.event_type)
            )

            by_event_type = [
                EventTypeCount(event_type=row[0], count=row[1])
                for row in breakdown_result.all()
            ]

            logger.info(
                "Analytics summary total_events=%s total_revenue=%s types=%s",
                total_events,
                total_revenue,
                len(by_event_type),
            )

            return AnalyticsSummaryResponse(
                total_events=total_events,
                total_revenue=Decimal(str(total_revenue)),
                by_event_type=by_event_type,
            )

        except SQLAlchemyError as exc:
            logger.exception("Database error while building analytics summary")
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch analytics summary",
            ) from exc

    async def generate_insight(self, payload: InsightRequest) -> InsightResponse:
        if not settings.openrouter_api_key:
            logger.error("OpenRouter API key is not configured")
            raise HTTPException(
                status_code=503,
                detail="OpenRouter API key is not configured",
            )

        try:
            analytics_summary = await self.get_summary()
            prompt = self._build_insight_prompt(
                analytics_summary,
                payload.query,
            )

            logger.info(
                "Generating AI insights for %s events",
                analytics_summary.total_events,
            )

            insight_text = await self.gemini.generate_text(prompt)

            return InsightResponse(
                summary=insight_text,
                model=self.gemini.model_name,
            )

        except HTTPException:
            raise

        except SQLAlchemyError as exc:
            logger.exception("Database error while generating insights")
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch analytics data for insights",
            ) from exc

        except Exception as exc:
            logger.exception("Failed to generate AI insights")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate AI insights",
            ) from exc

    @staticmethod
    def _build_insight_prompt(
        analytics_summary: AnalyticsSummaryResponse,
        user_query: str,
    ) -> str:
        breakdown_lines = [
            f"  - {item.event_type}: {item.count}"
            for item in analytics_summary.by_event_type
        ]

        breakdown = (
            "\n".join(breakdown_lines)
            if breakdown_lines
            else "  - No events recorded"
        )

        question = user_query.strip() or (
            "Provide actionable business insights based on the analytics data below."
        )

        return f"""You are a senior data analyst reviewing ecommerce event analytics.

Analytics Summary (from PostgreSQL):
- Total Events: {analytics_summary.total_events}
- Total Revenue: ${analytics_summary.total_revenue}
- Events by Type:
{breakdown}

User Request: {question}

Write structured business insights using exactly these markdown sections:

## Key Findings
Summarize the most important patterns in 2-4 bullet points.

## Revenue Analysis
Interpret total revenue and which event types likely drive it.

## Event Trends
Comment on event type distribution and user behavior signals.

## Recommendations
Provide 2-3 concrete, actionable recommendations.

Keep the response concise, data-driven, and professional."""