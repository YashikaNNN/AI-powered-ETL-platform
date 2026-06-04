from abc import ABC, abstractmethod
from typing import Any


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> list[dict[str, Any]]:
        """Pull raw records from a source system."""
