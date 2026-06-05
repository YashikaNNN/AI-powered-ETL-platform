from dataclasses import dataclass
from datetime import datetime


@dataclass
class PipelineRunRecord:
    pipeline_id: str
    status: str
    started_at: datetime
    run_id: int | None = None
    finished_at: datetime | None = None
    row_count: int | None = None
    error_message: str | None = None
