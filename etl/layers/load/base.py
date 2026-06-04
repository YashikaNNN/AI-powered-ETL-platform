from abc import ABC, abstractmethod
from typing import Any


class BaseLoader(ABC):
    @abstractmethod
    def load(self, records: list[dict[str, Any]]) -> int:
        """Persist records; returns rows written."""
