from typing import Any

import google.generativeai as genai

from etl.config import settings
from etl.layers.transform.base import BaseTransformer


class AIEnricher(BaseTransformer):
    """Use Gemini to add derived fields or classifications to records."""

    def __init__(self) -> None:
        genai.configure(api_key=settings.gemini_api_key)
        self._model = genai.GenerativeModel(settings.gemini_model)

    def transform(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        # Starter: pass-through; implement batch enrichment per record
        return records
