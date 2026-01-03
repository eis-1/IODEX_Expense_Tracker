"""
Utility helpers for timestamp parsing and formatting.
"""
from datetime import datetime, timezone
from typing import Optional


def parse_iso_to_local_dt(iso_str: str) -> Optional[datetime]:
    """Parse an ISO-8601 timestamp (possibly timezone-aware) and convert it to local timezone.

    Returns a timezone-aware datetime in the local timezone, or None if iso_str is falsy.
    """
    if not iso_str:
        return None

    dt = datetime.fromisoformat(iso_str)
    if dt.tzinfo is None:
        # Treat naive timestamps as UTC
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone()


def format_iso_to_local(iso_str: str, fmt: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """Format an ISO-8601 timestamp into a localized string using the provided format.

    Returns an empty string when iso_str is falsy or cannot be parsed.
    """
    dt = parse_iso_to_local_dt(iso_str)
    if not dt:
        return ""
    return dt.strftime(fmt)


def humanize_relative(dt, now=None) -> str:
    """Return a short humanized relative time like '2d ago' or '3h ago'."""
    if dt is None:
        return ""
    if now is None:
        now = datetime.now(dt.tzinfo)
    delta = now - dt
    past = delta.total_seconds() >= 0
    secs = abs(int(delta.total_seconds()))
    if secs < 60:
        s = f"{secs}s"
    elif secs < 3600:
        s = f"{secs // 60}m"
    elif secs < 86400:
        s = f"{secs // 3600}h"
    else:
        s = f"{secs // 86400}d"
    return f"{s} {'ago' if past else 'from now'}"


def format_iso_timestamp(iso_str: str, mode: str = 'local', custom_fmt: str = '%Y-%m-%d %H:%M:%S %Z', show_relative: bool = True, tz_name: str = 'system') -> str:
    """Format an ISO timestamp according to mode and optionally append relative time.

    mode: 'local', 'utc', or 'custom'
    custom_fmt: strftime format used when mode == 'custom'
    show_relative: whether to append short relative time
    tz_name: 'system' or an IANA timezone name recognized by zoneinfo
    """
    if not iso_str:
        return ""

    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
    except Exception:
        return ""

    # Determine output datetime per requested mode and timezone
    if mode == 'utc':
        out_dt = dt.astimezone(timezone.utc)
        fmt = "%Y-%m-%d %H:%M:%S %Z"
    else:
        # Decide which tz to use: system, explicit tz_name, or local
        if tz_name and tz_name != 'system':
            try:
                from zoneinfo import ZoneInfo
                tzobj = ZoneInfo(tz_name)
                out_dt = dt.astimezone(tzobj)
            except Exception:
                out_dt = dt.astimezone()
        else:
            out_dt = dt.astimezone()

        if mode == 'custom':
            fmt = custom_fmt
        else:
            fmt = custom_fmt if custom_fmt else "%Y-%m-%d %H:%M:%S %Z"

    formatted = out_dt.strftime(fmt)
    if show_relative:
        rel = humanize_relative(out_dt)
        if rel:
            formatted = f"{formatted} ({rel})"
    return formatted


def sample_timezones(limit:int=10, include_system:bool=True) -> list:
    """Return a short list of popular IANA timezones for quick selection.

    If available, uses zoneinfo.available_timezones(), otherwise falls back to a curated list.
    """
    try:
        from zoneinfo import available_timezones
        tzs = sorted([tz for tz in available_timezones() if '/' in tz])
        popular = ["UTC", "Europe/London", "America/New_York", "Europe/Paris", "Asia/Tokyo", "Asia/Shanghai", "Australia/Sydney"]
        # merge ensuring order and uniqueness
        ordered = [t for t in popular if t in tzs]
        for t in tzs:
            if t not in ordered:
                ordered.append(t)
        result = ordered[:limit]
        if include_system:
            return (["system"] + result)
        return result
    except Exception:
        fallback = ["system", "UTC", "America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"]
        return fallback[:limit]


def fuzzy_timezones(query: str, limit: int = 50) -> list:
    """Return a list of timezones matching the query using fuzzy matching.

    Uses difflib.get_close_matches to rank similar timezone names when exact
    substring matches are not abundant.
    """
    import difflib
    q = (query or '').strip().lower()
    if not q:
        return sample_timezones(limit=limit, include_system=True)
    try:
        from zoneinfo import available_timezones
        all_tzs = sorted([tz for tz in available_timezones() if '/' in tz])
    except Exception:
        all_tzs = ["America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney"]

    # First prefer simple substring matches
    subs = [tz for tz in all_tzs if q in tz.lower()]
    if len(subs) >= min(10, limit):
        return ["system", "UTC"] + subs[:limit]

    # Otherwise use fuzzy matching
    scores = difflib.get_close_matches(q, all_tzs, n=limit, cutoff=0.1)
    return ["system", "UTC"] + scores
