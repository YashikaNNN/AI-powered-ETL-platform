from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.gemini.client import GeminiClient
from app.schemas.analytics import InsightRequest, InsightResponse


class AnalyticsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.gemini = GeminiClient()

    async def generate_insight(self, payload: InsightRequest) -> InsightResponse:
        summary = await self.gemini.generate_text(
            prompt=f"Analyze the following analytics request: {payload.query}"
        )
        return InsightResponse(summary=summary, model=self.gemini.model_name)
