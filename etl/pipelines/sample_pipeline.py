from pathlib import Path

from etl.layers.extract.file_extractor import FileExtractor
from etl.layers.load.postgres_loader import PostgresLoader
from etl.layers.transform.ai_enricher import AIEnricher
from etl.pipelines.base_pipeline import BasePipeline


class SamplePipeline(BasePipeline):
    pipeline_id = "sample_csv_to_postgres"

    def __init__(self, source_path: Path) -> None:
        super().__init__(
            extractor=FileExtractor(source_path),
            transformer=AIEnricher(),
            loader=PostgresLoader(table="sample_events"),
        )
