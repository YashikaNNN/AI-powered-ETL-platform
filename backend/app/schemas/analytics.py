from pydantic import BaseModel


class InsightRequest(BaseModel):
    query: str
    dataset_id: str | None = None


class InsightResponse(BaseModel):
    summary: str
    model: str
