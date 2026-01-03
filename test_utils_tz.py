"""
Tests for timezone handling in utils.format_iso_timestamp
"""
from utils import format_iso_timestamp


def test_format_with_explicit_timezone():
    iso = '2026-01-03T12:00:00+00:00'
    s = format_iso_timestamp(iso, mode='local', custom_fmt='%Y-%m-%d %H:%M:%S %Z', show_relative=False, tz_name='Asia/Tokyo')
    # Tokyo is UTC+9, so hour should be 21
    assert '21:00:00' in s or '21:00' in s


def test_format_system_and_utc():
    iso = '2026-01-03T12:00:00+00:00'
    s_utc = format_iso_timestamp(iso, mode='utc', show_relative=False)
    assert '12:00:00' in s_utc
    s_sys = format_iso_timestamp(iso, mode='local', show_relative=False)
    assert isinstance(s_sys, str) and len(s_sys) > 0
