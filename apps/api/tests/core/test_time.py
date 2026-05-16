"""Tests for the time utilities."""

from datetime import UTC, datetime

from workbench.core.time import utcnow


def test_utcnow_returns_aware_datetime() -> None:
    """utcnow() returns a timezone-aware datetime."""
    dt = utcnow()
    assert isinstance(dt, datetime)
    assert dt.tzinfo is not None
    assert dt.tzinfo == UTC


def test_utcnow_is_recent() -> None:
    """utcnow() returns a time close to now."""
    before = datetime.now(UTC)
    dt = utcnow()
    after = datetime.now(UTC)
    
    assert before <= dt <= after
