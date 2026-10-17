"""
Stop freshness (ST-10, EPIC-02, v9.13, BLG-SPEC-188).

How long ago each open position's stop was last recalculated, from
positions.stop_calculated_at (DS-22). Definition: metrics_definitions.md
§Stop Freshness. Shown on System Status (system_status.md v1.3 §Stop
Freshness Panel); the figures are computed here so the page and a manual SQL
check read the same source (design record §5).

Display only (§13): reading the age changes no stop.
"""
from datetime import datetime, timezone
from statistics import median
from typing import Dict, Optional

from database import get_portfolio, get_positions


def _as_utc(value: datetime) -> datetime:
    """stop_calculated_at is TIMESTAMPTZ; treat a naive value as UTC."""
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def get_stop_freshness(now: Optional[datetime] = None) -> Dict:
    """
    Median and maximum age, in hours, of stop_calculated_at across open positions.

    Positions with a NULL stop_calculated_at are excluded from the median and
    the maximum and counted in never_recalculated. Ages are rounded to 2dp;
    the median of an even count is the mean of the two middle ages.

    Returns:
        {
          "as_of": ISO-8601 UTC,
          "open_positions": n,
          "recalculated_positions": k (positions with a stop_calculated_at),
          "never_recalculated": m (= n - k),
          "median_age_hours": float | None (None when k = 0),
          "max_age_hours": float | None,
          "oldest_ticker": str | None,
          "oldest_stop_calculated_at": ISO-8601 | None,
        }
    """
    as_of = _as_utc(now) if now else datetime.now(timezone.utc)
    portfolio = get_portfolio()
    positions = get_positions(str(portfolio["id"]), status="open") if portfolio else []

    stamped = [
        (p["ticker"], _as_utc(p["stop_calculated_at"]))
        for p in positions
        if p.get("stop_calculated_at") is not None
    ]
    result = {
        "as_of": as_of.isoformat(),
        "open_positions": len(positions),
        "recalculated_positions": len(stamped),
        "never_recalculated": len(positions) - len(stamped),
        "median_age_hours": None,
        "max_age_hours": None,
        "oldest_ticker": None,
        "oldest_stop_calculated_at": None,
    }
    if not stamped:
        return result

    ages = [(as_of - ts).total_seconds() / 3600 for _, ts in stamped]
    oldest_ticker, oldest_ts = min(stamped, key=lambda s: s[1])
    result.update({
        "median_age_hours": round(median(ages), 2),
        "max_age_hours": round(max(ages), 2),
        "oldest_ticker": oldest_ticker,
        "oldest_stop_calculated_at": oldest_ts.isoformat(),
    })
    return result
