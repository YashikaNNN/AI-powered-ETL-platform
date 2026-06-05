from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from etl.layers.transform.base import BaseTransformer
from etl.utils.logging import get_logger

logger = get_logger(__name__)

REQUIRED_FIELDS = ("event_id", "user_id", "event_type", "event_timestamp")


class StandardCleaner(BaseTransformer):
    """Validate, normalize, and type-coerce raw event records."""

    def transform(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        cleaned: list[dict[str, Any]] = []
        skipped = 0

        for record in records:
            normalized = self._normalize_record(record)
            if normalized is None:
                skipped += 1
                continue
            cleaned.append(normalized)

        if skipped:
            logger.warning("Skipped %s invalid record(s) during transform", skipped)

        return cleaned

    def _normalize_record(self, record: dict[str, Any]) -> dict[str, Any] | None:
        row = {str(k).strip().lower(): v for k, v in record.items()}

        if any(not row.get(field) for field in REQUIRED_FIELDS):
            return None

        event_timestamp = self._parse_timestamp(row["event_timestamp"])
        if event_timestamp is None:
            return None

        amount = self._parse_amount(row.get("amount", 0))

        return {
            "event_id": str(row["event_id"]).strip(),
            "user_id": str(row["user_id"]).strip(),
            "event_type": str(row["event_type"]).strip().lower(),
            "event_timestamp": event_timestamp,
            "amount": amount,
        }

    @staticmethod
    def _parse_timestamp(value: Any) -> datetime | None:
        if isinstance(value, datetime):
            return value if value.tzinfo else value.replace(tzinfo=timezone.utc)

        text = str(value).strip()
        if not text:
            return None

        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None

        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)

    @staticmethod
    def _parse_amount(value: Any) -> Decimal:
        try:
            return Decimal(str(value)).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            return Decimal("0.00")
