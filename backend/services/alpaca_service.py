"""
Alpaca Markets Data Service (DS-05)

Fetches OHLCV bar data for US tickers from Alpaca Data API v2.
Per BLG-SPEC-22 (alpaca_integration_contract.md):
  - Base URL: https://data.alpaca.markets
  - Auth: APCA-API-KEY-ID + APCA-API-SECRET-KEY headers (env vars)
  - Endpoint: GET /v2/stocks/{symbol}/bars
  - US tickers only — UK tickers always use Yahoo Finance
  - Fallback: Yahoo Finance OHLCV when Alpaca fails (always logged)
  - API version pinned: v2 / v1beta1

Rate limits: 200 req/min (Free tier). Retry on 429 with exponential backoff (max 5).
"""
import os
import time
import logging
import requests
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

ALPACA_BASE_URL = "https://data.alpaca.markets"
ALPACA_API_KEY = os.environ.get("APCA_API_KEY_ID", "")
ALPACA_API_SECRET = os.environ.get("APCA_API_SECRET_KEY", "")

# API version is pinned per BLG-SPEC-22
_BARS_PATH = "/v2/stocks/{symbol}/bars"


def _alpaca_headers() -> Dict[str, str]:
    return {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_API_SECRET,
        "Accept": "application/json",
    }


def _credentials_configured() -> bool:
    return bool(ALPACA_API_KEY and ALPACA_API_SECRET)


def get_ohlcv_bars(symbol: str, limit: int = 30, timeframe: str = "1Day") -> Optional[List[Dict]]:
    """
    Fetch OHLCV bars for a US ticker from Alpaca Data API v2.

    Returns a list of bar dicts with keys: t (timestamp), o, h, l, c, v.
    Returns None on any failure (caller must invoke fallback).

    Retry: 429 → exponential backoff, up to 5 attempts.
            5xx → up to 3 attempts.
            403 → no retry (credential issue).
    """
    if not _credentials_configured():
        logger.warning("Alpaca credentials not configured — skipping Alpaca fetch for %s", symbol)
        return None

    url = ALPACA_BASE_URL + _BARS_PATH.format(symbol=symbol)
    params = {"timeframe": timeframe, "limit": limit, "feed": "iex"}
    headers = _alpaca_headers()

    max_attempts = 5
    delay = 1.0

    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                bars = data.get("bars") or []
                logger.info("Alpaca bars fetched for %s: %d bars", symbol, len(bars))
                return bars or None
            elif resp.status_code == 429:
                if attempt < max_attempts:
                    time.sleep(delay)
                    delay = min(delay * 2, 30)
                    continue
                logger.warning("Alpaca rate limit exceeded for %s after %d attempts", symbol, attempt)
                return None
            elif resp.status_code == 403:
                logger.error("Alpaca 403 Forbidden for %s — check credentials", symbol)
                return None
            elif resp.status_code >= 500 and attempt <= 3:
                time.sleep(delay)
                delay = min(delay * 2, 10)
                continue
            else:
                logger.warning("Alpaca unexpected status %d for %s", resp.status_code, symbol)
                return None
        except requests.RequestException as exc:
            logger.warning("Alpaca request error for %s (attempt %d): %s", symbol, attempt, exc)
            if attempt >= 3:
                return None
            time.sleep(delay)

    return None


def get_latest_close(symbol: str) -> Optional[float]:
    """
    Fetch the latest close price for a US ticker from Alpaca.
    Returns None if Alpaca is unavailable (caller uses Yahoo Finance fallback).
    """
    bars = get_ohlcv_bars(symbol, limit=2)
    if bars:
        return float(bars[-1]["c"])
    return None


def get_historical_bars(symbol: str, limit: int = 30) -> Optional[List[Dict]]:
    """
    Fetch recent daily OHLCV bars for ATR and signal calculation.
    Returns None on failure.
    """
    return get_ohlcv_bars(symbol, limit=limit)
