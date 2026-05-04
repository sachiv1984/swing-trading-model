"""
Earnings Calendar Service (DS-04)

Fetches next earnings date for tickers via Yahoo Finance (yfinance).
Returns structured earnings data including days until earnings and fiscal quarter.

Data freshness: Yahoo Finance earnings dates are generally reliable 2-4 weeks out.
Dates further in the future may shift. Null returned if date unavailable.
"""
import yfinance as yf
from datetime import date, datetime
from typing import Optional, Dict, Any


def _yf_ticker_symbol(ticker: str, market: str) -> str:
    if market == "UK" and not ticker.endswith(".L"):
        return ticker + ".L"
    return ticker


def get_earnings(ticker: str, market: str = "US") -> Dict[str, Any]:
    """
    Fetch next earnings date for a ticker.

    Returns dict with: ticker, next_earnings_date (ISO string or null),
    days_until_earnings (int or null), fiscal_quarter (str or null),
    data_source.
    """
    yf_symbol = _yf_ticker_symbol(ticker, market)
    try:
        t = yf.Ticker(yf_symbol)
        info = t.info
        earnings_date = info.get("earningsDate") or info.get("earningsTimestamp")

        if isinstance(earnings_date, list):
            earnings_date = earnings_date[0] if earnings_date else None

        if isinstance(earnings_date, (int, float)):
            earnings_date = datetime.utcfromtimestamp(earnings_date).date()
        elif isinstance(earnings_date, datetime):
            earnings_date = earnings_date.date()

        if earnings_date is None:
            cal = getattr(t, "calendar", None)
            if cal is not None and hasattr(cal, "columns"):
                if "Earnings Date" in cal.columns:
                    val = cal["Earnings Date"].iloc[0] if len(cal) > 0 else None
                    if val is not None:
                        earnings_date = val.date() if hasattr(val, "date") else None

        if earnings_date is None:
            return {
                "ticker": ticker,
                "next_earnings_date": None,
                "days_until_earnings": None,
                "fiscal_quarter": None,
                "data_source": "yahoo_finance",
            }

        today = date.today()
        days_until = (earnings_date - today).days
        fiscal_quarter = info.get("earningsQuarterlyGrowth") and None  # not reliable from info
        try:
            fiscal_quarter = info.get("mostRecentQuarter")
            if fiscal_quarter:
                fiscal_quarter = str(fiscal_quarter)
        except Exception:
            fiscal_quarter = None

        return {
            "ticker": ticker,
            "next_earnings_date": earnings_date.isoformat(),
            "days_until_earnings": days_until,
            "fiscal_quarter": fiscal_quarter,
            "data_source": "yahoo_finance",
        }
    except Exception:
        return {
            "ticker": ticker,
            "next_earnings_date": None,
            "days_until_earnings": None,
            "fiscal_quarter": None,
            "data_source": "yahoo_finance",
        }
