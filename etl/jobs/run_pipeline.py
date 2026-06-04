"""CLI entrypoint: python -m jobs.run_pipeline"""

from pathlib import Path

from etl.pipelines.sample_pipeline import SamplePipeline
from etl.services.metadata_service import MetadataService


def main() -> None:
    metadata = MetadataService()
    pipeline = SamplePipeline(source_path=Path("data/raw/sample.csv"))
    metadata.record_start(pipeline.pipeline_id)
    pipeline.run()


if __name__ == "__main__":
    main()
