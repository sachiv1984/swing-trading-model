"""
Alpaca News Service (DS-06)

Fetches news headlines for US tickers via Alpaca Data API v1beta1.
Display-only per BLG-GOV-16 §13 review — no sentiment scoring, no
automated advisory generated.

UK tickers: no Alpaca news data; returns empty list.
"""
import os
import time
import logging
import requests
from typing import List, Dict

logger = logging.getLogger(__name__)

ALPACA_BASE_URL = "https://data.alpaca.markets"
ALPACA_API_KEY = os.environ.get("APCA_API_KEY_ID", "")
ALPACA_API_SECRET = os.environ.get("APCA_API_SECRET_KEY", "")

_NEWS_PATH = "/v1beta1/news"
MAX_HEADLINES = 10


def _alpaca_headers() -> Dict[str, str]:
    return {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_API_SECRET,
        "Accept": "application/json",
    }


def _credentials_configured() -> bool:
    return bool(ALPACA_API_KEY and ALPACA_API_SECRET)


def get_news_headlines(ticker: str, market: str, limit: int = MAX_HEADLINES) -> List[Dict]:
    """
    Fetch recent news headlines for a ticker from Alpaca News API.

    UK tickers always return [] (Alpaca does not carry UK news).
    Returns list of dicts with keys: headline, published_at, source (may be None).
    Returns [] on any error — callers should display empty state.

    Display-only: no sentiment fields returned. Per §13 review (BLG-GOV-16).
    """
    if market == "UK":
        return []

    if not _credentials_configured():
        logger.warning("Alpaca credentials not configured — no news for %s", ticker)
        return []

    url = ALPACA_BASE_URL + _NEWS_PATH
    params = {"symbols": ticker, "limit": min(limit, MAX_HEADLINES)}
    headers = _alpaca_headers()

    max_attempts = 3
    delay = 1.0

    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                articles = data.get("news", [])
                return [
                    {
                        "headline": a.get("headline", ""),
                        "published_at": a.get("created_at") or a.get("updated_at"),
                        "source": a.get("source") or None,
                    }
                    for a in articles
                    if a.get("headline")
                ]
            elif resp.status_code == 429:
                if attempt < max_attempts:
                    time.sleep(delay)
                    delay = min(delay * 2, 30)
                    continue
                logger.warning("Alpaca news rate limit for %s", ticker)
                return []
            elif resp.status_code == 403:
                logger.error("Alpaca news 403 Forbidden for %s", ticker)
                return []
            else:
                logger.warning("Alpaca news unexpected status %d for %s", resp.status_code, ticker)
                return []
        except requests.RequestException as exc:
            logger.warning("Alpaca news fetch error for %s (attempt %d): %s", ticker, attempt, exc)
            if attempt >= max_attempts:
                return []
            time.sleep(delay)

    return []
