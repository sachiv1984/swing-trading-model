"""
Screener Data Service (DS-01 / ST-02)

Fetches OHLCV data for screener engine consumption.
  - US tickers: Alpaca Data API v2 (primary), Yahoo Finance (fallback)
  - UK tickers: Yahoo Finance (always)

Returns normalised daily OHLCV records:
  [{"date": "YYYY-MM-DD", "open": float, "high": float, "low": float,
    "close": float, "volume": int}]

Pence-denominated UK tickers (currency=GBp) are divided by 100 → GBP.
Returns None when data is unavailable from all sources.
"""
import logging
import requests
from datetime import datetime, timezone
from typing import Optional, List, Dict

from services.alpaca_service import get_ohlcv_bars

logger = logging.getLogger(__name__)

_YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
_YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

OHLCVRecord = Dict[str, object]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _alpaca_bars_to_ohlcv(bars: List[Dict]) -> List[OHLCVRecord]:
    result = []
    for b in bars:
        try:
            date_str = b["t"][:10]  # ISO timestamp → YYYY-MM-DD
            result.append({
                "date": date_str,
                "open": float(b["o"]),
                "high": float(b["h"]),
                "low": float(b["l"]),
                "close": float(b["c"]),
                "volume": int(b["v"]),
            })
        except (KeyError, ValueError, TypeError):
            continue
    return sorted(result, key=lambda r: r["date"])


def _yahoo_fetch_ohlcv(ticker: str, days: int) -> Optional[List[OHLCVRecord]]:
    range_param = f"{max(days, 30)}d"
    url = _YAHOO_CHART_URL.format(ticker=ticker)
    try:
        resp = requests.get(
            url,
            params={"interval": "1d", "range": range_param},
            headers=_YAHOO_HEADERS,
            timeout=15,
        )
        if resp.status_code != 200:
            logger.warning("Yahoo Finance HTTP %d for %s", resp.status_code, ticker)
            return None
        data = resp.json()
    except requests.RequestException as exc:
        logger.warning("Yahoo Finance request error for %s: %s", ticker, exc)
        return None

    try:
        result_block = data["chart"]["result"]
        if not result_block:
            return None
        r = result_block[0]
        timestamps = r.get("timestamp", [])
        quote = r["indicators"]["quote"][0]
        opens = quote.get("open", [])
        highs = quote.get("high", [])
        lows = quote.get("low", [])
        closes = quote.get("close", [])
        volumes = quote.get("volume", [])

        currency = r.get("meta", {}).get("currency", "")
        pence = currency == "GBp"
        scale = 100.0 if pence else 1.0

        records = []
        for i, ts in enumerate(timestamps):
            try:
                date_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
                records.append({
                    "date": date_str,
                    "open": float(opens[i]) / scale if opens[i] is not None else None,
                    "high": float(highs[i]) / scale if highs[i] is not None else None,
                    "low": float(lows[i]) / scale if lows[i] is not None else None,
                    "close": float(closes[i]) / scale if closes[i] is not None else None,
                    "volume": int(volumes[i]) if i < len(volumes) and volumes[i] is not None else 0,
                })
            except (IndexError, TypeError, ValueError):
                continue

        # Drop records with missing close (unusable for screener)
        records = [rec for rec in records if rec["close"] is not None]
        return sorted(records, key=lambda r: r["date"]) or None
    except (KeyError, IndexError, TypeError) as exc:
        logger.warning("Yahoo Finance parse error for %s: %s", ticker, exc)
        return None


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def fetch_ohlcv(ticker: str, market: str, days: int = 30) -> Optional[List[OHLCVRecord]]:
    """
    Fetch normalised OHLCV data for a ticker.

    market='US' → Alpaca primary, Yahoo Finance fallback.
    market='UK' → Yahoo Finance only.

    Returns a list of OHLCVRecord dicts ordered by date ascending,
    or None if no data could be obtained.
    """
    ticker = ticker.strip().upper()

    if market == "US":
        bars = get_ohlcv_bars(ticker, limit=days)
        if bars:
            ohlcv = _alpaca_bars_to_ohlcv(bars)
            if ohlcv:
                return ohlcv
        logger.info("Alpaca unavailable for %s — falling back to Yahoo Finance", ticker)

    # UK tickers always use Yahoo Finance; US falls through here on Alpaca failure
    return _yahoo_fetch_ohlcv(ticker, days)
