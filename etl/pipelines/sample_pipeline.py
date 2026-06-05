from pathlib import Path

from etl.layers.extract.file_extractor import FileExtractor
from etl.layers.load.postgres_loader import PostgresLoader
from etl.layers.transform.standard_cleaner import StandardCleaner
from etl.pipelines.base_pipeline import BasePipeline

EVENT_COLUMNS = ["event_id", "user_id", "event_type", "event_timestamp", "amount"]


class SamplePipeline(BasePipeline):
    pipeline_id = "sample_csv_to_postgres"

    def __init__(self, source_path: Path) -> None:
        super().__init__(
            extractor=FileExtractor(source_path),
            transformer=StandardCleaner(),
            loader=PostgresLoader(
                table="sample_events",
                columns=EVENT_COLUMNS,
                on_conflict_column="event_id",
            ),
        )
