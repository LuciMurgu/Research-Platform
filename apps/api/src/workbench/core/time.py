"""Timezone-aware datetime utilities."""

from datetime import UTC, datetime


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime.

    Returns:
        datetime: Current time with tzinfo=UTC
    """
    return datetime.now(UTC)
