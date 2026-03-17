"""Tests for wdadaptivepy's model for Adaptive's Level."""

from datetime import datetime, timezone

from wdadaptivepy.models.time import Period


def test_missing_timezone() -> None:
    """Test that a timezone is added."""
    period = Period(start="2025-01-01")  # pyright: ignore[reportArgumentType]
    assert period.start == datetime(2025, 1, 1, tzinfo=timezone.utc)


def test_specific_timezone() -> None:
    """Test that an RFC 3339 datetime string keeps timezone."""
    period = Period(start="2025-01-01T00:00:00Z")  # pyright: ignore[reportArgumentType]
    assert period.start == datetime(2025, 1, 1, tzinfo=timezone.utc)
