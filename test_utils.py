"""
Tests for timestamp parsing/formatting utilities.
"""
from datetime import datetime, timezone
import utils


def test_parse_iso_to_local_dt_roundtrip():
    # Use an explicit UTC timestamp
    iso = "2026-01-03T12:00:00+00:00"
    dt_local = utils.parse_iso_to_local_dt(iso)
    assert dt_local is not None
    assert dt_local.tzinfo is not None

    # Converting back to UTC should match original UTC time
    back_to_utc = dt_local.astimezone(timezone.utc).replace(tzinfo=None)
    assert back_to_utc == datetime(2026, 1, 3, 12, 0, 0)


def test_format_iso_to_local_non_empty():
    iso = "2026-01-03T12:00:00+00:00"
    s = utils.format_iso_to_local(iso)
    assert isinstance(s, str) and len(s) > 0


def test_format_iso_to_local_handles_empty():
    assert utils.format_iso_to_local("") == ""
    assert utils.parse_iso_to_local_dt("") is None
