from etl.layers.extract.base import BaseExtractor
from etl.layers.load.base import BaseLoader
from etl.layers.transform.base import BaseTransformer
from etl.utils.logging import get_logger

logger = get_logger(__name__)


class BasePipeline:
    pipeline_id: str = "base"

    def __init__(
        self,
        extractor: BaseExtractor,
        transformer: BaseTransformer,
        loader: BaseLoader,
    ) -> None:
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self) -> int:
        logger.info("Starting pipeline %s", self.pipeline_id)
        raw = self.extractor.extract()
        transformed = self.transformer.transform(raw)
        row_count = self.loader.load(transformed)
        logger.info("Pipeline %s finished: %s rows", self.pipeline_id, row_count)
        return row_count
