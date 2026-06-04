from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PipelineRunCreate(BaseModel):
    pipeline_id: str


class PipelineRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pipeline_id: str
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    row_count: int | None = None
    error_message: str | None = None
