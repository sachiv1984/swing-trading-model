"""
Screener Data Service (DS-01 / ST-02)

Fetches OHLCV data for screener engine consumption.
  - US tickers: Alpaca Data API v2 (primary), Yahoo Finance crumb-based (fallback)
  - UK tickers: Yahoo Finance simple/no-crumb (sequential, 0.3s spacing in batch service)

Returns normalised daily OHLCV records:
  [{"date": "YYYY-MM-DD", "open": float, "high": float, "low": float,
    "close": float, "volume": int}]

Pence-denominated UK tickers (currency=GBp) are divided by 100 → GBP.
Returns None when data is unavailable from all sources.
"""
import logging
import os
import random
import threading
import requests
import time as _time
from datetime import datetime, timezone
from typing import Optional, List, Dict

from services.alpaca_service import get_ohlcv_bars
from services.health_service import record_external_api_call

logger = logging.getLogger(__name__)

_YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
_YAHOO_CRUMB_URL = "https://query1.finance.yahoo.com/v1/test/getcrumb"
_YAHOO_CONSENT_URL = "https://finance.yahoo.com/"

_STOOQ_URL = "https://stooq.com/q/d/l/"
_STOOQ_HEADERS = {"User-Agent": "Mozilla/5.0"}

_TWELVE_DATA_URL = "https://api.twelvedata.com/time_series"
_TWELVE_DATA_API_KEY = os.environ.get("TWELVE_DATA_API_KEY", "")
_TWELVE_DATA_RATE_LIMIT = 8        # max requests per 60s (free tier)
_twelve_data_req_lock = threading.Lock()
_twelve_data_req_times: List[float] = []  # monotonic timestamps of recent requests
_YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
}

_crumb_lock = threading.Lock()
_yahoo_session: Optional[requests.Session] = None
_yahoo_crumb: Optional[str] = None
_yahoo_cooldown_until: float = 0.0  # monotonic; 0 = no cooldown active
_YAHOO_COOLDOWN_SECS = 120  # back off 2 minutes after a 429 on the crumb endpoint
_YAHOO_401_COOLDOWN_SECS = 60   # back off 1 minute after 3 consecutive 401s
_crumb_consecutive_401s: int = 0

OHLCVRecord = Dict[str, object]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _refresh_yahoo_crumb() -> Optional[str]:
    """Establish a new Yahoo Finance session and fetch a fresh crumb token."""
    global _yahoo_session, _yahoo_crumb, _yahoo_cooldown_until, _crumb_consecutive_401s
    with _crumb_lock:
        # Skip the network call entirely while in cooldown
        if _time.monotonic() < _yahoo_cooldown_until:
            return None
        # If another thread already refreshed the crumb while we waited for the
        # lock, reuse it rather than firing another HTTP request (thundering herd).
        if _yahoo_crumb is not None:
            return _yahoo_crumb
        sess = requests.Session()
        try:
            sess.get(_YAHOO_CONSENT_URL, headers=_YAHOO_HEADERS, timeout=10)
            resp = sess.get(_YAHOO_CRUMB_URL, headers=_YAHOO_HEADERS, timeout=10)
            if resp.status_code == 200 and resp.text.strip():
                _yahoo_session = sess
                _yahoo_crumb = resp.text.strip()
                _yahoo_cooldown_until = 0.0
                _crumb_consecutive_401s = 0
                logger.info("Yahoo Finance crumb refreshed successfully")
                return _yahoo_crumb
            if resp.status_code == 429:
                _crumb_consecutive_401s = 0
                _yahoo_cooldown_until = _time.monotonic() + _YAHOO_COOLDOWN_SECS
                logger.warning(
                    "Yahoo Finance crumb fetch returned HTTP 429 — entering %ds cooldown",
                    _YAHOO_COOLDOWN_SECS,
                )
            elif resp.status_code == 401:
                _crumb_consecutive_401s += 1
                logger.warning(
                    "Yahoo Finance crumb fetch returned HTTP 401 (consecutive: %d)",
                    _crumb_consecutive_401s,
                )
                if _crumb_consecutive_401s >= 3:
                    _yahoo_cooldown_until = _time.monotonic() + _YAHOO_401_COOLDOWN_SECS
                    logger.warning(
                        "Yahoo Finance crumb returned 401 %d times — entering %ds cooldown",
                        _crumb_consecutive_401s, _YAHOO_401_COOLDOWN_SECS,
                    )
            else:
                logger.warning("Yahoo Finance crumb fetch returned HTTP %d", resp.status_code)
        except requests.RequestException as exc:
            logger.warning("Yahoo Finance crumb refresh failed: %s", exc)
        return None


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
    global _yahoo_session, _yahoo_crumb

    # Fast-fail during cooldown — avoids hammering the crumb endpoint on sustained 429s
    if _time.monotonic() < _yahoo_cooldown_until:
        return None

    range_param = f"{max(days, 30)}d"
    url = _YAHOO_CHART_URL.format(ticker=ticker)

    # Ensure we have a session and crumb; refresh lazily if missing
    if _yahoo_crumb is None:
        _refresh_yahoo_crumb()

    def _do_request(crumb: Optional[str]) -> requests.Response:
        sess = _yahoo_session or requests
        params: Dict = {"interval": "1d", "range": range_param}
        if crumb:
            params["crumb"] = crumb
        return sess.get(url, params=params, headers=_YAHOO_HEADERS, timeout=15)

    t0 = _time.monotonic()
    try:
        resp = _do_request(_yahoo_crumb)

        # On 401 (Invalid Crumb) or 429 (rate limit): refresh crumb and retry once with backoff
        if resp.status_code in (401, 429):
            consecutive_failures = getattr(_yahoo_fetch_ohlcv, "_consecutive_401", 0) + 1
            _yahoo_fetch_ohlcv._consecutive_401 = consecutive_failures
            logger.warning(
                "Yahoo Finance HTTP %d for %s — refreshing crumb (consecutive failures: %d)",
                resp.status_code, ticker, consecutive_failures,
            )
            new_crumb = _refresh_yahoo_crumb()
            # Exponential backoff with jitter: base 1s * 2^(min(failures-1,3)) + uniform jitter
            backoff = min(1.0 * (2 ** min(consecutive_failures - 1, 3)), 8.0)
            jitter = random.uniform(0, backoff * 0.3)
            _time.sleep(backoff + jitter)
            if new_crumb:
                resp = _do_request(new_crumb)
            else:
                latency = (_time.monotonic() - t0) * 1000
                record_external_api_call("yahoo_finance", False, latency)
                logger.warning("Yahoo Finance crumb refresh failed for %s — marking as failed", ticker)
                return None
        else:
            _yahoo_fetch_ohlcv._consecutive_401 = 0

        latency = (_time.monotonic() - t0) * 1000
        if resp.status_code != 200:
            record_external_api_call("yahoo_finance", False, latency)
            logger.warning("Yahoo Finance HTTP %d for %s (range=%sd)", resp.status_code, ticker, max(days, 30))
            return None
        record_external_api_call("yahoo_finance", True, latency)
        data = resp.json()
    except requests.RequestException as exc:
        latency = (_time.monotonic() - t0) * 1000
        record_external_api_call("yahoo_finance", False, latency)
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
# Twelve Data (UK primary data source)
# ---------------------------------------------------------------------------

def _twelve_data_rate_wait() -> None:
    """Block until the Twelve Data sliding-window rate limit allows another request.

    Free tier: 8 requests per 60 seconds. All worker threads share this limiter.
    """
    with _twelve_data_req_lock:
        now = _time.monotonic()
        # Drop timestamps older than the 60s window
        while _twelve_data_req_times and _twelve_data_req_times[0] < now - 60.0:
            _twelve_data_req_times.pop(0)
        if len(_twelve_data_req_times) >= _TWELVE_DATA_RATE_LIMIT:
            wait = _twelve_data_req_times[0] + 60.0 - _time.monotonic()
            if wait > 0:
                logger.debug("Twelve Data rate limiter sleeping %.1fs", wait)
                _time.sleep(wait)
            # Re-clean after sleep
            cutoff = _time.monotonic() - 60.0
            while _twelve_data_req_times and _twelve_data_req_times[0] < cutoff:
                _twelve_data_req_times.pop(0)
        _twelve_data_req_times.append(_time.monotonic())


def _twelve_data_fetch_ohlcv(ticker: str, days: int) -> Optional[List[OHLCVRecord]]:
    """Fetch OHLCV from Twelve Data for UK (LSE) tickers.

    Converts LSE ticker format: AZN.L → symbol=AZN, mic_code=XLON
    Handles pence-denominated tickers (currency GBp/GBX → divide by 100).
    Returns None when API key is absent or on any failure.
    """
    if not _TWELVE_DATA_API_KEY:
        logger.warning("TWELVE_DATA_API_KEY not configured — skipping Twelve Data for %s", ticker)
        return None

    # Twelve Data uses ISO 10383 MIC code for exchange disambiguation.
    # LSE tickers use mic_code=XLON (not exchange=LSE which causes 404).
    if ticker.upper().endswith(".L"):
        symbol = ticker[:-2].upper()
        mic_code = "XLON"
    else:
        symbol = ticker.upper()
        mic_code = None

    _twelve_data_rate_wait()
    t0 = _time.monotonic()
    try:
        params: Dict = {
            "symbol": symbol,
            "interval": "1day",
            "outputsize": max(days, 30),
            "apikey": _TWELVE_DATA_API_KEY,
        }
        if mic_code:
            params["mic_code"] = mic_code

        resp = requests.get(_TWELVE_DATA_URL, params=params, timeout=15)
        latency = (_time.monotonic() - t0) * 1000

        if resp.status_code == 429:
            record_external_api_call("twelve_data", False, latency)
            logger.warning("Twelve Data rate limit hit for %s", ticker)
            return None

        if resp.status_code != 200:
            record_external_api_call("twelve_data", False, latency)
            try:
                body = resp.json()
                logger.warning(
                    "Twelve Data HTTP %d for %s — code=%s msg=%s",
                    resp.status_code, ticker,
                    body.get("code", "?"), body.get("message", resp.text[:200]),
                )
            except Exception:
                logger.warning("Twelve Data HTTP %d for %s — %s", resp.status_code, ticker, resp.text[:200])
            return None

        data = resp.json()

        if data.get("status") == "error" or "values" not in data:
            record_external_api_call("twelve_data", False, latency)
            logger.warning("Twelve Data error for %s: %s", ticker, data.get("message", "no values"))
            return None

        # Pence conversion: LSE prices come back in pence (GBp/GBX)
        currency = data.get("meta", {}).get("currency", "")
        scale = 100.0 if currency in ("GBp", "GBX") else 1.0

        records = []
        for v in data["values"]:
            try:
                records.append({
                    "date": v["datetime"][:10],
                    "open": float(v["open"]) / scale,
                    "high": float(v["high"]) / scale,
                    "low": float(v["low"]) / scale,
                    "close": float(v["close"]) / scale,
                    "volume": int(float(v.get("volume", 0) or 0)),
                })
            except (KeyError, ValueError, TypeError):
                continue

        if not records:
            record_external_api_call("twelve_data", False, latency)
            return None

        records = records[-days:] if len(records) > days else records
        record_external_api_call("twelve_data", True, latency)
        logger.info("OHLCV OK via Twelve Data for %s (%d bars)", ticker, len(records))
        return records

    except requests.RequestException as exc:
        latency = (_time.monotonic() - t0) * 1000
        record_external_api_call("twelve_data", False, latency)
        logger.warning("Twelve Data request error for %s: %s", ticker, exc)
        return None


# ---------------------------------------------------------------------------
# Stooq (UK secondary data source — fallback when Twelve Data unavailable)
# ---------------------------------------------------------------------------

def _stooq_fetch_ohlcv(ticker: str, days: int) -> Optional[List[OHLCVRecord]]:
    """Fetch OHLCV from Stooq CSV endpoint for UK tickers.

    Converts LSE ticker format: AZN.L → AZN.UK
    Stooq prices are in GBP (not pence) — no scaling required.
    Returns None on any failure.
    """
    # Convert Yahoo .L suffix to Stooq .UK suffix
    if ticker.upper().endswith(".L"):
        stooq_symbol = ticker[:-2].upper() + ".UK"
    else:
        stooq_symbol = ticker.upper()

    t0 = _time.monotonic()
    try:
        resp = requests.get(
            _STOOQ_URL,
            params={"s": stooq_symbol, "i": "d"},
            headers=_STOOQ_HEADERS,
            timeout=5,
        )
        latency = (_time.monotonic() - t0) * 1000

        if resp.status_code != 200:
            record_external_api_call("stooq", False, latency)
            logger.warning("Stooq HTTP %d for %s", resp.status_code, ticker)
            return None

        lines = resp.text.strip().splitlines()
        if len(lines) < 2:
            record_external_api_call("stooq", False, latency)
            logger.warning("Stooq empty response for %s", ticker)
            return None

        # Stooq sometimes returns "No data" as the body
        if "no data" in resp.text.lower():
            record_external_api_call("stooq", False, latency)
            logger.warning("Stooq no data for %s", ticker)
            return None

        records = []
        for line in lines[1:]:  # skip header: Date,Open,High,Low,Close,Volume
            parts = line.split(",")
            if len(parts) < 5:
                continue
            try:
                records.append({
                    "date": parts[0].strip(),
                    "open": float(parts[1]),
                    "high": float(parts[2]),
                    "low": float(parts[3]),
                    "close": float(parts[4]),
                    "volume": int(float(parts[5])) if len(parts) > 5 and parts[5].strip() else 0,
                })
            except (ValueError, IndexError):
                continue

        if not records:
            record_external_api_call("stooq", False, latency)
            return None

        records = sorted(records, key=lambda r: r["date"])
        # Return only the most recent `days` records
        records = records[-days:] if len(records) > days else records
        record_external_api_call("stooq", True, latency)
        logger.info("OHLCV OK via Stooq for %s (%d bars)", ticker, len(records))
        return records

    except requests.RequestException as exc:
        latency = (_time.monotonic() - t0) * 1000
        record_external_api_call("stooq", False, latency)
        logger.warning("Stooq request error for %s: %s", ticker, exc)
        return None


# ---------------------------------------------------------------------------
# Yahoo Finance — simple no-crumb fetch (UK screener path)
# ---------------------------------------------------------------------------

_YAHOO_SIMPLE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

def _yahoo_fetch_ohlcv_simple(ticker: str, days: int) -> Optional[List[OHLCVRecord]]:
    """Cookie-free Yahoo Finance fetch — mirrors the signal service approach.

    No crumb, no session, no shared cooldown state. Safe to call sequentially
    from the screener without interfering with the crumb-based path used by
    the US fallback and earnings service.
    """
    url = _YAHOO_CHART_URL.format(ticker=ticker)
    # Use timestamp range (same as signal service) rather than range=Nd
    # so we get a predictable window even near market open.
    from datetime import timedelta
    end_dt = datetime.now(tz=timezone.utc)
    start_dt = end_dt - timedelta(days=max(days, 30) + 10)  # small buffer for weekends
    params = {
        "interval": "1d",
        "period1": int(start_dt.timestamp()),
        "period2": int(end_dt.timestamp()),
    }
    t0 = _time.monotonic()
    try:
        resp = requests.get(url, params=params, headers=_YAHOO_SIMPLE_HEADERS, timeout=15)
        latency = (_time.monotonic() - t0) * 1000

        if resp.status_code != 200:
            record_external_api_call("yahoo_finance", False, latency)
            logger.warning("Yahoo Finance (simple) HTTP %d for %s", resp.status_code, ticker)
            return None

        data = resp.json()
        result_block = data.get("chart", {}).get("result")
        if not result_block:
            record_external_api_call("yahoo_finance", False, latency)
            return None

        r = result_block[0]
        timestamps = r.get("timestamp", [])
        quote = r["indicators"]["quote"][0]
        currency = r.get("meta", {}).get("currency", "")
        scale = 100.0 if currency == "GBp" else 1.0

        records = []
        for i, ts in enumerate(timestamps):
            try:
                c = quote["close"][i]
                if c is None:
                    continue
                records.append({
                    "date": datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d"),
                    "open": (quote["open"][i] or c) / scale,
                    "high": (quote["high"][i] or c) / scale,
                    "low": (quote["low"][i] or c) / scale,
                    "close": c / scale,
                    "volume": int(quote.get("volume", [0] * (i + 1))[i] or 0),
                })
            except (KeyError, IndexError, TypeError):
                continue

        if not records:
            record_external_api_call("yahoo_finance", False, latency)
            return None

        records = records[-days:] if len(records) > days else records
        record_external_api_call("yahoo_finance", True, latency)
        logger.info("OHLCV OK via Yahoo Finance for %s (%d bars)", ticker, len(records))
        return records

    except requests.RequestException as exc:
        latency = (_time.monotonic() - t0) * 1000
        record_external_api_call("yahoo_finance", False, latency)
        logger.warning("Yahoo Finance (simple) request error for %s: %s", ticker, exc)
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
        t0 = _time.monotonic()
        alpaca_symbol = ticker.replace("-", ".")
        bars = get_ohlcv_bars(alpaca_symbol, limit=days)
        latency = (_time.monotonic() - t0) * 1000
        if bars:
            record_external_api_call("alpaca", True, latency)
            ohlcv = _alpaca_bars_to_ohlcv(bars)
            if ohlcv:
                logger.info("OHLCV OK via Alpaca for %s (%d bars)", ticker, len(ohlcv))
                return ohlcv
        else:
            record_external_api_call("alpaca", False, latency)
        logger.info("Alpaca unavailable for %s — falling back to Yahoo Finance", ticker)
        result = _yahoo_fetch_ohlcv(ticker, days)
        if result:
            return result
        logger.warning("OHLCV FAILED for %s (market=%s) — no data from any source", ticker, market)
        return None

    # UK tickers: simple no-crumb Yahoo Finance fetch.
    # Twelve Data requires a paid plan for LSE symbols.
    # Stooq consistently times out from Render's IP range.
    # The crumb-based _yahoo_fetch_ohlcv shares cooldown state with the earnings
    # service and gets 429'd before the screener even starts; the simple path
    # uses no session/crumb and doesn't interfere with that state.
    result = _yahoo_fetch_ohlcv_simple(ticker, days)
    if result:
        return result
    logger.warning("OHLCV FAILED for %s (market=%s) — no data from any source", ticker, market)
    return None
