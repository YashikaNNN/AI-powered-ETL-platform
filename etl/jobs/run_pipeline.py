"""CLI entrypoint: python -m etl.jobs.run_pipeline"""

from etl.services.pipeline_runner import execute_sample_pipeline


def main() -> None:
    result = execute_sample_pipeline()
    if result.status == "failed":
        raise RuntimeError(result.error_message or "Pipeline execution failed")


if __name__ == "__main__":
    main()
