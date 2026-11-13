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


def _empty(ticker: str) -> Dict[str, Any]:
    return {
        "ticker": ticker,
        "next_earnings_date": None,
        "days_until_earnings": None,
        "fiscal_quarter": None,
        "data_source": "yahoo_finance",
    }


# ST-15 (BLG-OPS-217, v9.17): symbol -> (next earnings date or None,
# fiscal_quarter), kept RESULT_TTL_SECONDS and only after a usable Yahoo answer.
# A page that shows one badge per row then costs Yahoo nothing on a reload.
RESULT_TTL_SECONDS = yahoo_info.INFO_TTL_SECONDS
_result_cache = yahoo_info.TTLCache()


def _lookup(yf_symbol: str, today: date):
    """(next earnings date or None, fiscal_quarter, usable) from Yahoo."""
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

    if earnings_date is None and not candidates and not no_earnings_type:
        cal = yahoo_info.call_with_slot(lambda: getattr(t, "calendar", None))
        if cal is not None and hasattr(cal, "columns"):
            if "Earnings Date" in cal.columns:
                val = cal["Earnings Date"].iloc[0] if len(cal) > 0 else None
                if val is not None:
                    earnings_date = val.date() if hasattr(val, "date") else None
        if earnings_date is not None and earnings_date < today:
            earnings_date = None

    fiscal_quarter = None
    try:
        fiscal_quarter = info.get("mostRecentQuarter")
        if fiscal_quarter:
            fiscal_quarter = str(fiscal_quarter)
    except Exception:
        fiscal_quarter = None

    return earnings_date, fiscal_quarter, yahoo_info.is_usable_info(info)


def get_earnings(ticker: str, market: str = "US") -> Dict[str, Any]:
    """
    Fetch next earnings date for a ticker.

    Returns dict with: ticker, next_earnings_date (ISO string or null),
    days_until_earnings (int or null), fiscal_quarter (str or null),
    data_source.

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
            earnings_date, fiscal_quarter, usable = _lookup(yf_symbol, today)
            if usable:
                _result_cache.set(key, (earnings_date, fiscal_quarter), RESULT_TTL_SECONDS)
            else:
                _result_cache.delete(key)

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
        }
    except Exception:
        return _empty(ticker)
