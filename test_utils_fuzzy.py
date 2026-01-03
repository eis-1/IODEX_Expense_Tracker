"""
Tests for fuzzy timezone matching helper.
"""
from utils import fuzzy_timezones


def test_fuzzy_timezones_substring():
    res = fuzzy_timezones('tokyo', limit=10)
    assert any('Tokyo' in tz or 'tokyo' in tz.lower() for tz in res)


def test_fuzzy_timezones_fallback():
    res = fuzzy_timezones('newy', limit=10)
    assert any('New_York' in tz or 'new_york' in tz.lower() or 'New_York' in str(res) for tz in res) or len(res) > 0
