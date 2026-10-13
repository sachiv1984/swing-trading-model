"""
US (NYSE) trading-session calendar — ST-14 (BLG-BE-148, EPIC-02, v9.12)

Used by the Gap Risk Flag (gap_risk_service.py) to find "that position's next
trading session" (strategy_rules.md §13.3). Strategy Rules & System Intent Owner
ruling ESC-EXEC-20261013-07, recorded as the v9.12 addendum ("Revised Ruling 3")
in docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md.

Deterministic and offline (Binding Condition 1 of that ruling): every date is
computed in code from fixed rules plus the dated one-off closure list below. No
network, file, database or price-history call is made, and sessions are never
inferred from OHLCV data. Rule-based, so any year is covered.

A session is any weekday that is not an NYSE full-closure holiday and not a
listed one-off closure. Early-close days (e.g. the day after Thanksgiving) are
sessions: a manual exit (§8.3) is possible on them.

Full-closure holidays (NYSE observance rules):
  New Year's Day   1 Jan; Sunday -> Monday 2 Jan; Saturday -> not observed
                   (the NYSE does not close on the Friday before, 31 Dec)
  MLK Day          3rd Monday of January
  Presidents' Day  3rd Monday of February
  Good Friday      Friday before Easter Sunday
  Memorial Day     last Monday of May
  Juneteenth       19 Jun, from 2022; Saturday -> Friday, Sunday -> Monday
  Independence Day 4 Jul; Saturday -> Friday, Sunday -> Monday
  Labor Day        1st Monday of September
  Thanksgiving     4th Thursday of November
  Christmas        25 Dec; Saturday -> Friday, Sunday -> Monday

Unannounced closures are not anticipated. A new one-off closure, or a holiday
rule change (as Juneteenth was in 2022), is added here by a code change. An
unlisted closure can only make the gap-risk window shorter than it should be
(under-flagging); it can never flag every position or flag after a gap.

Last checked against the NYSE's published holiday schedule (2026 and 2027): 2026-10-13.
"""
from datetime import date, datetime, timedelta
from functools import lru_cache
from typing import FrozenSet, Optional
from zoneinfo import ZoneInfo

from dateutil.easter import easter

US_MARKET_TZ = "America/New_York"

# One-off full-day NYSE closures (dated; extend by code change).
ONE_OFF_CLOSURES: FrozenSet[date] = frozenset({
    date(2012, 10, 29),  # Hurricane Sandy
    date(2012, 10, 30),  # Hurricane Sandy
    date(2018, 12, 5),   # National Day of Mourning, President George H. W. Bush
    date(2025, 1, 9),    # National Day of Mourning, President Jimmy Carter
})


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """The n-th given weekday (Monday=0) of a month."""
    first = date(year, month, 1)
    return first + timedelta(days=(weekday - first.weekday()) % 7 + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> date:
    nxt = date(year + (month == 12), month % 12 + 1, 1)
    last = nxt - timedelta(days=1)
    return last - timedelta(days=(last.weekday() - weekday) % 7)


def _observed(d: date) -> date:
    """Saturday -> Friday, Sunday -> Monday."""
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


@lru_cache(maxsize=64)
def nyse_holidays(year: int) -> FrozenSet[date]:
    """NYSE full-closure holidays observed in a calendar year (one-off closures excluded)."""
    holidays = set()
    new_year = date(year, 1, 1)
    if new_year.weekday() == 6:
        holidays.add(new_year + timedelta(days=1))
    elif new_year.weekday() != 5:
        holidays.add(new_year)
    holidays.add(_nth_weekday(year, 1, 0, 3))   # MLK Day
    holidays.add(_nth_weekday(year, 2, 0, 3))   # Presidents' Day
    holidays.add(easter(year) - timedelta(days=2))  # Good Friday
    holidays.add(_last_weekday(year, 5, 0))     # Memorial Day
    if year >= 2022:
        holidays.add(_observed(date(year, 6, 19)))  # Juneteenth
    holidays.add(_observed(date(year, 7, 4)))   # Independence Day
    holidays.add(_nth_weekday(year, 9, 0, 1))   # Labor Day
    holidays.add(_nth_weekday(year, 11, 3, 4))  # Thanksgiving
    holidays.add(_observed(date(year, 12, 25)))  # Christmas
    return frozenset(holidays)


def is_nyse_session(d: date) -> bool:
    return d.weekday() < 5 and d not in nyse_holidays(d.year) and d not in ONE_OFF_CLOSURES


def next_nyse_session(d: date) -> date:
    """The first NYSE session strictly after d."""
    nxt = d + timedelta(days=1)
    while not is_nyse_session(nxt):
        nxt += timedelta(days=1)
    return nxt


def days_to_next_nyse_session(d: date) -> int:
    """Calendar days from d to the first NYSE session after it."""
    return (next_nyse_session(d) - d).days


def us_market_date(now: Optional[datetime] = None) -> date:
    """Today's date in America/New_York. A 02:00 UTC view is still the previous US day.

    `now` must be timezone-aware when given. Uses the zone database; if it cannot
    be loaded this raises rather than falling back to the server or UTC date
    (ruling ESC-EXEC-20261013-07, Binding Condition 2).
    """
    tz = ZoneInfo(US_MARKET_TZ)
    if now is None:
        return datetime.now(tz).date()
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    return now.astimezone(tz).date()
