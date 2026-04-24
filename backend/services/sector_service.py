"""
Sector & Industry Classification Service (DS-03)

Fetches sector and industry classification for tickers via Yahoo Finance.
Used for screener results enrichment and position sector display.

Scope: US and UK tickers. UK tickers use the .L suffix for Yahoo Finance.
Data source: yfinance Ticker.info ('sector', 'industry' fields).
"""
import yfinance as yf
from typing import Optional, Tuple


def get_sector_and_industry(ticker: str, market: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Fetch sector and industry for a ticker via Yahoo Finance.

    Returns (sector, industry). Both may be None if Yahoo Finance
    does not carry classification for this ticker (common for some UK stocks).
    """
    try:
        yf_ticker = ticker if not ticker.endswith(".L") else ticker
        if market == "UK" and not ticker.endswith(".L"):
            yf_ticker = ticker + ".L"

        info = yf.Ticker(yf_ticker).info
        sector = info.get("sector") or None
        industry = info.get("industry") or None
        return sector, industry
    except Exception:
        return None, None


def enrich_positions_with_sector(positions: list) -> list:
    """
    Add sector and industry fields to each position dict.

    Fetches classification for every position. Positions that cannot be
    enriched receive sector=None, industry=None.
    """
    enriched = []
    for pos in positions:
        sector, industry = get_sector_and_industry(pos["ticker"], pos["market"])
        enriched.append({**pos, "sector": sector, "industry": industry})
    return enriched
