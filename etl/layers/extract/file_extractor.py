from pathlib import Path
from typing import Any

import pandas as pd

from etl.layers.extract.base import BaseExtractor


class FileExtractor(BaseExtractor):
    def __init__(self, path: Path) -> None:
        self.path = path

    def extract(self) -> list[dict[str, Any]]:
        df = pd.read_csv(self.path)
        return df.to_dict(orient="records")
