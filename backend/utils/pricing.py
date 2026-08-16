"""
Pricing and Market Data Utilities

This module handles all external data fetching for prices, FX rates, and market regime.
Isolated from FastAPI for testability and reusability.

Functions:
    - get_current_price(): Fetch live stock price from Yahoo Finance
    - get_live_fx_rate(): Fetch GBP/USD exchange rate
    - check_market_regime(): Check SPY/FTSE vs 200-day MA for risk on/off
    - calculate_atr(): Calculate Average True Range for a ticker
"""

import time
import logging
import requests
from datetime import datetime
from typing import Optional, Dict

from utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)

DEFAULT_FX_RATE = 1.27

# TTL cache for GBP/USD rate — refreshed every 5 minutes to avoid a live HTTP
# call on every portfolio endpoint request (root cause of concentration-status
# and drawdown-status high latency: BLG-OPS-62).
_fx_cache: Dict = {"rate": None, "expires_at": 0.0}
_FX_CACHE_TTL_SECONDS = 300


def _is_us_ticker(ticker: str) -> bool:
    return not ticker.endswith(".L")


@retry_with_backoff(
    max_attempts=3,
    base_delay=0.5,
    retryable_exceptions=(requests.exceptions.RequestException,),
)
def _yahoo_fetch_price(ticker: str) -> float:
    """
    Fetch current price from Yahoo Finance (internal, not market-routed).
    Raises on any transient/network failure (retried by the decorator) or a
    `ValueError` when the response is well-formed but carries no usable price
    (not retried — retrying won't produce data that isn't there).
    """
    time.sleep(0.3)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {"interval": "1d", "range": "1d"}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    response = requests.get(url, params=params, headers=headers, timeout=10)
    data = response.json()
    if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
        result = data["chart"]["result"][0]
        if "meta" in result and "regularMarketPrice" in result["meta"]:
            price = float(result["meta"]["regularMarketPrice"])
            if price > 0:
                return price
    raise ValueError(f"No valid price in Yahoo Finance response for {ticker}")


def _yahoo_get_current_price(ticker: str) -> Optional[float]:
    """Fetch current price from Yahoo Finance, retrying transient failures (ST-09, ~3 attempts)."""
    try:
        return _yahoo_fetch_price(ticker)
    except Exception as exc:
        logger.warning("Yahoo Finance price fetch failed for %s: %s", ticker, exc)
        return None


def get_current_price(ticker: str) -> Optional[float]:
    """
    Fetch current price for a ticker.

    Routing (DS-05 / BLG-SPEC-22):
    - US tickers: Alpaca Data API v2 first; Yahoo Finance fallback on failure.
    - UK tickers (.L suffix): Yahoo Finance only (Alpaca does not support UK tickers).
    Fallback is always logged per BLG-SPEC-22 contract.

    Returns price in native currency (USD for US, pence for UK).
    UK stocks need pence→pounds conversion by caller.
    """
    if _is_us_ticker(ticker):
        # US: try Alpaca first (DS-05)
        try:
            from services.alpaca_service import get_latest_close
            alpaca_price = get_latest_close(ticker)
            if alpaca_price is not None and alpaca_price > 0:
                print(f"✓ {ticker}: ${alpaca_price:.2f} (Alpaca)")
                return alpaca_price
            logger.warning("Alpaca unavailable for %s — falling back to Yahoo Finance", ticker)
        except Exception as exc:
            logger.warning("Alpaca import/fetch error for %s: %s — falling back to Yahoo Finance", ticker, exc)

    # UK tickers, or US fallback
    price = _yahoo_get_current_price(ticker)
    if price is not None and price > 0:
        source = "Yahoo Finance fallback" if _is_us_ticker(ticker) else "Yahoo Finance"
        print(f"✓ {ticker}: {price:.2f} ({source})")
        return price

    print(f"⚠️  {ticker}: No price available")
    return None


def get_live_fx_rate() -> float:  # noqa: C901
    """
    Fetch live GBP/USD exchange rate from Yahoo Finance
    
    Returns:
        GBP/USD rate as float (e.g., 1.3684)
        Falls back to 1.27 if fetch fails
        
    Notes:
        - Cached for 5 minutes (BLG-OPS-62 fix); falls back to DEFAULT_FX_RATE on error
        - Used for converting USD positions to GBP
    """
    now = time.monotonic()
    if _fx_cache["rate"] is not None and now < _fx_cache["expires_at"]:
        return _fx_cache["rate"]

    try:
        
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GBPUSD=X"
        params = {
            "interval": "1d",
            "range": "1d"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
            result = data["chart"]["result"][0]
            
            # Try meta.regularMarketPrice first
            if "meta" in result and "regularMarketPrice" in result["meta"]:
                fx_rate = float(result["meta"]["regularMarketPrice"])
                if fx_rate > 0:
                    print(f"✓ Live FX rate (GBP/USD): {fx_rate:.4f}")
                    _fx_cache["rate"] = fx_rate
                    _fx_cache["expires_at"] = time.monotonic() + _FX_CACHE_TTL_SECONDS
                    return fx_rate

            # Try latest close price
            if "indicators" in result and "quote" in result["indicators"]:
                quotes = result["indicators"]["quote"]
                if len(quotes) > 0 and "close" in quotes[0]:
                    closes = [c for c in quotes[0]["close"] if c is not None]
                    if closes:
                        fx_rate = float(closes[-1])
                        if fx_rate > 0:
                            print(f"✓ Live FX rate (GBP/USD): {fx_rate:.4f}")
                            _fx_cache["rate"] = fx_rate
                            _fx_cache["expires_at"] = time.monotonic() + _FX_CACHE_TTL_SECONDS
                            return fx_rate
        
        print(f"⚠️  Could not fetch live FX rate, using default {DEFAULT_FX_RATE}")
        return DEFAULT_FX_RATE
        
    except Exception as e:
        print(f"⚠️  FX rate fetch error: {e}, using default {DEFAULT_FX_RATE}")
        return DEFAULT_FX_RATE


@retry_with_backoff(
    max_attempts=3,
    base_delay=0.5,
    retryable_exceptions=(requests.exceptions.RequestException,),
)
def _yahoo_fetch_ma200_pair(ticker: str):
    """
    Fetch current price and 200-day MA for a ticker from Yahoo Finance (internal).
    Raises on any transient/network failure (retried by the decorator, ST-09) or a
    `ValueError` when the response is well-formed but carries no usable chart data
    (not retried — retrying won't produce data that isn't there).
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    params = {
        "interval": "1d",
        "range": "1y"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }

    response = requests.get(url, params=params, headers=headers, timeout=15)
    data = response.json()

    if not ("chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0):
        raise ValueError(f"No chart result in Yahoo Finance response for {ticker}")

    result = data["chart"]["result"][0]

    # Get current price
    current = None
    if "meta" in result and "regularMarketPrice" in result["meta"]:
        current = float(result["meta"]["regularMarketPrice"])

    # Get historical closes for MA200
    ma200 = None
    if "indicators" in result and "quote" in result["indicators"]:
        quotes = result["indicators"]["quote"]
        if len(quotes) > 0 and "close" in quotes[0]:
            closes = [c for c in quotes[0]["close"] if c is not None]
            if len(closes) >= 200:
                # Calculate 200-day moving average
                ma200 = sum(closes[-200:]) / 200
            elif len(closes) > 0:
                # Use available data if less than 200 days
                ma200 = sum(closes) / len(closes)

    return current, ma200


_market_regime_cache: dict = {}
_MARKET_REGIME_TTL_SECONDS = 300  # 5-minute shared cache (BLG-BE-25, v5.0 ST-07; consolidated here BLG-BE-97, v8.8 ST-07)


def check_market_regime() -> Dict[str, any]:
    """
    Check SPY and FTSE for risk on/off using 200-day moving average

    Single canonical implementation (BLG-BE-97, v8.8 ST-07 — consolidates the
    former duplicate in `position_manager.py`, which used a separate
    `yfinance` data path with no retry logic). All call sites (dashboard,
    pre-entry validation, signal generation, position analysis, `/market/status`)
    now share this one implementation and its 5-minute result cache, so they
    also share one Yahoo Finance round-trip per cache window.

    Returns:
        Dictionary with:
            - spy_risk_on: bool (SPY > 200-day MA)
            - ftse_risk_on: bool (FTSE > 200-day MA)
            - spy_price: float
            - spy_ma200: float
            - ftse_price: float
            - ftse_ma200: float
            - date: datetime (as-of time this result was computed)

    Notes:
        - Results are cached for 5 minutes (BLG-BE-25) — a cache hit returns
          immediately with no network call.
        - Defaults to risk-on if data unavailable
        - Includes 300ms delay to avoid rate limiting
        - Retries transient network failures before falling back (ST-09, ~3 attempts)
        - Used to determine if positions should be exited
    """
    now = datetime.now()
    cached = _market_regime_cache.get("result")
    cached_at = _market_regime_cache.get("cached_at")
    if cached is not None and cached_at is not None:
        age = (now - cached_at).total_seconds()
        if age < _MARKET_REGIME_TTL_SECONDS:
            return cached

    try:
        time.sleep(0.3)

        def get_ma200(ticker: str):
            """Get current price and 200-day MA for a ticker, retrying transient failures."""
            try:
                return _yahoo_fetch_ma200_pair(ticker)
            except Exception as e:
                print(f"Error getting MA200 for {ticker}: {e}")
                return None, None

        # Get SPY data
        spy_price, spy_ma200 = get_ma200("SPY")
        
        # Get FTSE data
        ftse_price, ftse_ma200 = get_ma200("^FTSE")
        
        # Default to risk-on if we can't fetch data
        if spy_price is None or spy_ma200 is None:
            print("⚠️  Could not fetch SPY data, defaulting to risk-on")
            spy_risk_on = True
            spy_price = 0
            spy_ma200 = 0
        else:
            spy_risk_on = spy_price > spy_ma200
        
        if ftse_price is None or ftse_ma200 is None:
            print("⚠️  Could not fetch FTSE data, defaulting to risk-on")
            ftse_risk_on = True
            ftse_price = 0
            ftse_ma200 = 0
        else:
            ftse_risk_on = ftse_price > ftse_ma200
        
        result = {
            'spy_risk_on': spy_risk_on,
            'ftse_risk_on': ftse_risk_on,
            'spy_price': spy_price or 0,
            'spy_ma200': spy_ma200 or 0,
            'ftse_price': ftse_price or 0,
            'ftse_ma200': ftse_ma200 or 0,
            'date': now
        }
        _market_regime_cache["result"] = result
        _market_regime_cache["cached_at"] = now
        return result
    except Exception as e:
        print(f"❌ Market regime check failed: {e}")
        # Not cached — an unexpected outer-level failure (as opposed to the
        # per-index fetch fallback above, which is a normal, cached result)
        # should retry fresh on the next call rather than pin a synthetic
        # result for the full TTL window.
        return {
            'spy_risk_on': True,
            'ftse_risk_on': True,
            'spy_price': 0,
            'spy_ma200': 0,
            'ftse_price': 0,
            'ftse_ma200': 0,
            'date': now
        }


def _compute_atr_from_bars(highs, lows, closes, period, ticker):
    """Shared ATR computation from OHLC arrays."""
    if len(highs) >= period and len(lows) >= period and len(closes) >= period:
        true_ranges = []
        for i in range(1, len(closes)):
            tr = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
            true_ranges.append(tr)
        if len(true_ranges) >= period:
            atr = sum(true_ranges[-period:]) / period
            if ticker.endswith('.L'):
                atr = atr / 100
                print(f"   📊 ATR for {ticker}: {atr:.2f} (converted from pence)")
            else:
                print(f"   📊 ATR for {ticker}: {atr:.2f}")
            return atr
    return None


def _alpaca_calculate_atr(ticker: str, period: int) -> Optional[float]:
    """Fetch ATR for a US ticker via Alpaca bars (DS-05)."""
    try:
        from services.alpaca_service import get_historical_bars
        bars = get_historical_bars(ticker, limit=max(period + 5, 30))
        if not bars or len(bars) < period:
            return None
        highs = [b["h"] for b in bars]
        lows = [b["l"] for b in bars]
        closes = [b["c"] for b in bars]
        return _compute_atr_from_bars(highs, lows, closes, period, ticker)
    except Exception as exc:
        logger.warning("Alpaca ATR fetch failed for %s: %s", ticker, exc)
        return None


def calculate_atr(ticker: str, period: int = 14) -> Optional[float]:
    """
    Calculate Average True Range (ATR) for a ticker.

    Routing (DS-05): US tickers use Alpaca first, Yahoo Finance fallback.
    UK tickers use Yahoo Finance. ATR returned in native currency (GBP for UK).
    """
    if _is_us_ticker(ticker):
        atr = _alpaca_calculate_atr(ticker, period)
        if atr is not None:
            return atr
        logger.warning("Alpaca ATR unavailable for %s — falling back to Yahoo Finance", ticker)

    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "1mo"  # Need enough data for ATR calculation
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
            result = data["chart"]["result"][0]
            if "indicators" in result and "quote" in result["indicators"]:
                quote = result["indicators"]["quote"][0]
                highs = [h for h in quote.get("high", []) if h is not None]
                lows = [l for l in quote.get("low", []) if l is not None]
                closes = [c for c in quote.get("close", []) if c is not None]
                atr = _compute_atr_from_bars(highs, lows, closes, period, ticker)
                if atr is not None:
                    return atr

        print(f"   ⚠️  Could not calculate ATR for {ticker}")
        return None

    except Exception as e:
        print(f"   ❌ ATR calculation error for {ticker}: {e}")
        return None
