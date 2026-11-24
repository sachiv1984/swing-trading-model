"""
Earnings Calendar Service (DS-04)

Fetches next earnings date for tickers via Yahoo Finance (yfinance).
Returns structured earnings data including days until earnings and fiscal quarter.

Data freshness: Yahoo Finance earnings dates are generally reliable 2-4 weeks out.
Dates further in the future may shift. Null returned if date unavailable.
"""
import yfinance as yf
from datetime import date, datetime, timezone
from typing import Optional, Dict, Any

from services.us_market_calendar import US_MARKET_TZ, us_market_date
from utils import yahoo_info
from zoneinfo import ZoneInfo


# Yahoo quoteType values that never carry earnings (ST-15, BLG-OPS-217, v9.17).
_NO_EARNINGS_QUOTE_TYPES = frozenset({"ETF", "MUTUALFUND", "INDEX", "CURRENCY", "CRYPTOCURRENCY", "FUTURE"})


def _et_date(dt: datetime) -> date:
    """The America/New_York date of an aware datetime (ST-22, BLG-BE-174).

    A naive value carries no zone and is usually a bare date at midnight, so its
    own date is kept, as before ST-22. Epoch timestamps are made UTC-aware first.
    """
    if dt.tzinfo is None:
        return dt.date()
    return dt.astimezone(ZoneInfo(US_MARKET_TZ)).date()


def _to_et_date(value) -> Optional[date]:
    """An earnings value from `Ticker.info` as an America/New_York date, or None.

    ST-22 (BLG-BE-174, v9.15): a timestamp is converted to its America/New_York
    date, so a 21:00 ET (after-close) release is that ET day, not the next UTC
    day. A naive datetime keeps its own date; a bare date is kept as it is.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return _et_date(datetime.fromtimestamp(value, timezone.utc))
    if isinstance(value, datetime):
        return _et_date(value)
    if isinstance(value, date):
        return value
    return None


def _yf_ticker_symbol(ticker: str, market: str) -> str:
    if market == "UK" and not ticker.endswith(".L"):
        return ticker + ".L"
    return ticker


# ST-33 (BLG-FE-294, v9.18): data_status tells a failed lookup from a
# successful one that found no upcoming date, which return the same null date.
#   "ok"          -- Yahoo answered (a usable `Ticker.info`, a cached answer, or a
#                    calendar date); next_earnings_date may still be null.
#   "unavailable" -- the lookup failed: an exception, no free lookup slot
#                    (YahooInfoBusy), or a throttled answer with no `quoteType`,
#                    no date at all and no calendar data. The frontend shows
#                    "unknown" and retries after 60 seconds.
DATA_STATUS_OK = "ok"
DATA_STATUS_UNAVAILABLE = "unavailable"


def _empty(ticker: str, data_status: str = DATA_STATUS_OK) -> Dict[str, Any]:
    return {
        "ticker": ticker,
        "next_earnings_date": None,
        "days_until_earnings": None,
        "fiscal_quarter": None,
        "data_source": "yahoo_finance",
        "data_status": data_status,
    }


# ST-15 (BLG-OPS-217, v9.17): symbol -> (next earnings date or None,
# fiscal_quarter), kept RESULT_TTL_SECONDS and only after a usable Yahoo answer.
# A page that shows one badge per row then costs Yahoo nothing on a reload.
RESULT_TTL_SECONDS = yahoo_info.INFO_TTL_SECONDS
# BLG-BE-235 (v9.18): an equity whose calendar fallback came back empty.
EMPTY_CALENDAR_TTL_SECONDS = 30 * 60
_result_cache = yahoo_info.TTLCache()


def _calendar_dates(cal):
    """(earnings dates, answered) from `Ticker.calendar`.

    ST-33 (BLG-FE-294, v9.18): yfinance 1.x returns a dict whose "Earnings
    Date" is a list of dates, and {} when its quoteSummary call fails; older
    versions returned a DataFrame. Until v9.18 only the DataFrame shape was
    read, so with the pinned yfinance 1.7.0 this fallback never found a date.
    `answered` is True when Yahoo returned calendar data (a non-empty dict, or
    a DataFrame), even if it holds only past dates or no earnings key.
    """
    if isinstance(cal, dict):
        values = cal.get("Earnings Date")
        values = values if isinstance(values, (list, tuple)) else [values]
        return [d for d in (_to_et_date(v) for v in values) if d is not None], bool(cal)
    if cal is not None and hasattr(cal, "columns"):
        dates = []
        if "Earnings Date" in cal.columns and len(cal) > 0:
            val = cal["Earnings Date"].iloc[0]
            if hasattr(val, "date"):
                dates.append(val.date())
        return dates, True
    return [], False


def _lookup(yf_symbol: str, today: date):
    """(next earnings date or None, fiscal_quarter, usable, answered, calendar_empty) from Yahoo.

    answered (ST-33): Yahoo gave at least one date, or calendar data, so the
    lookup did not fail even when `Ticker.info` lacked quoteType (throttled).
    """
    t = yf.Ticker(yf_symbol)
    info = yahoo_info.get_info(yf_symbol, lambda: t.info)

    # ST-15 (BLG-OPS-217, v9.17): after a company reports, Yahoo keeps the
    # past report in `earningsTimestamp` while `earningsTimestampStart`/`End`
    # already hold the next one (AAPL on 2026-11-13: 2026-11-02 and
    # 2027-01-28). Reading `earningsTimestamp` alone returned the past date,
    # a negative days_until_earnings that the frontend hides, so the badge
    # and the §4.2.3 pre-entry warning never showed for the next report.
    # The next date is the earliest candidate on or after today; when every
    # candidate is in the past, there is no known next date.
    candidates = []
    for key in ("earningsDate", "earningsTimestampStart", "earningsTimestampEnd", "earningsTimestamp"):
        value = info.get(key)
        for item in (value if isinstance(value, list) else [value]):
            parsed = _to_et_date(item)
            if parsed is not None:
                candidates.append(parsed)
    upcoming = [d for d in candidates if d >= today]
    earnings_date = min(upcoming) if upcoming else None

    # ST-15: funds and indices have no earnings. Their calendar lookup is a
    # quoteSummary call that Yahoo answers 404 ("No fundamentals data
    # found", twice with the crumb retry), counted as provider failures.
    no_earnings_type = info.get("quoteType") in _NO_EARNINGS_QUOTE_TYPES

    calendar_answered = False
    calendar_called = False
    if earnings_date is None and not candidates and not no_earnings_type:
        calendar_called = True
        cal = yahoo_info.call_with_slot(lambda: getattr(t, "calendar", None))
        cal_dates, calendar_answered = _calendar_dates(cal)
        upcoming = [d for d in cal_dates if d >= today]
        earnings_date = min(upcoming) if upcoming else None

    fiscal_quarter = None
    try:
        fiscal_quarter = info.get("mostRecentQuarter")
        if fiscal_quarter:
            fiscal_quarter = str(fiscal_quarter)
    except Exception:
        fiscal_quarter = None

    # ST-33: Yahoo answered when it gave any date (past ones included) or
    # calendar data, even if `Ticker.info` lacked quoteType.
    answered = bool(candidates) or calendar_answered
    # BLG-BE-235 (v9.18): yfinance returns {} both when its calendar call fails
    # and when there are no calendar events, so an empty answer cannot be told
    # apart from a failure. It reads as "no date" (ok), cached only briefly.
    calendar_empty = calendar_called and not calendar_answered
    return earnings_date, fiscal_quarter, yahoo_info.is_usable_info(info), answered, calendar_empty


def get_earnings(ticker: str, market: str = "US") -> Dict[str, Any]:
    """
    Fetch next earnings date for a ticker.

    Returns dict with: ticker, next_earnings_date (ISO string or null),
    days_until_earnings (int or null), fiscal_quarter (str or null),
    data_source, data_status ("ok" or "unavailable", ST-33).

    ST-15 (BLG-OPS-217, v9.17): results are cached per Yahoo symbol for
    RESULT_TTL_SECONDS after a usable answer, and Yahoo lookups share
    utils/yahoo_info's concurrency cap. days_until_earnings is counted on
    every call. A cached date that has passed is looked up again.
    """
    yf_symbol = _yf_ticker_symbol(ticker, market)
    try:
        # BLG-BE-204 (PR #2190 review, ST-22 follow-through): the US market date,
        # the same basis as next_earnings_date.
        today = us_market_date()

        key = yf_symbol.upper()
        cached = _result_cache.get(key)
        if cached is not None and (cached[0] is None or cached[0] >= today):
            earnings_date, fiscal_quarter = cached
        else:
            earnings_date, fiscal_quarter, usable, answered, calendar_empty = _lookup(yf_symbol, today)
            if usable:
                # BLG-BE-235: an empty calendar answer is kept 30 minutes, not
                # 12 hours, so a failed calendar call is retried within the
                # hour without every page load re-sending it.
                ttl = EMPTY_CALENDAR_TTL_SECONDS if calendar_empty else RESULT_TTL_SECONDS
                _result_cache.set(key, (earnings_date, fiscal_quarter), ttl)
            else:
                _result_cache.delete(key)
                if earnings_date is None and not answered:
                    # ST-33: a throttled answer with no date at all is a failed lookup.
                    return _empty(ticker, DATA_STATUS_UNAVAILABLE)

        if earnings_date is None:
            return _empty(ticker)

        # BLG-BE-204 (PR #2190 review, ST-22 follow-through): count from the US
        # market date, the same basis as next_earnings_date. With the server's
        # UTC date, a 21:00 ET release viewed at 00:30 UTC (19:30 ET, before it)
        # gave -1 days, and the §4.2.3 pre-entry check passed instead of warning.
        days_until = (earnings_date - today).days

        return {
            "ticker": ticker,
            "next_earnings_date": earnings_date.isoformat(),
            "days_until_earnings": days_until,
            "fiscal_quarter": fiscal_quarter,
            "data_source": "yahoo_finance",
            "data_status": DATA_STATUS_OK,
        }
    except Exception:
        # ST-33: includes YahooInfoBusy (no free lookup slot within the wait).
        return _empty(ticker, DATA_STATUS_UNAVAILABLE)
