from abc import ABC, abstractmethod
from typing import Any


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Clean, enrich, or reshape raw records."""
