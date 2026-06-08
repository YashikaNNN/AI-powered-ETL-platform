from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InsightRequest(BaseModel):
    query: str = ""
    dataset_id: str | None = None


class InsightResponse(BaseModel):
    summary: str
    model: str


class SampleEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: str
    user_id: str
    event_type: str
    event_timestamp: datetime
    amount: Decimal
    loaded_at: datetime


class PaginatedEventsResponse(BaseModel):
    items: list[SampleEventResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class EventTypeCount(BaseModel):
    event_type: str
    count: int


class AnalyticsSummaryResponse(BaseModel):
    total_events: int
    total_revenue: Decimal = Field(description="Sum of amount across all events")
    by_event_type: list[EventTypeCount]
