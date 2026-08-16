"""
Pre-Trade Research Router (ST-05 / EPIC-02)

Aggregation endpoint: GET /research/{ticker}
Spec: docs/specs/api_contracts/research_endpoint.md v1.2

Sub-source failures return null fields (200). Critical failure modes:
  - Yahoo Finance entirely unavailable → 503
  - Ticker not found in any source → 404
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Optional
import logging
import requests
import time

logger = logging.getLogger(__name__)
from database import get_portfolio
from services.signal_service import get_signals_for_ticker
from services.sector_service import get_sector_and_industry
from services.screener_batch_service import get_screener_results

router = APIRouter(prefix="/research", tags=["Research"])

_YF_UNAVAILABLE = "yf_unavailable"
_TICKER_NOT_FOUND = "ticker_not_found"

# Per-ticker TTL cache — avoids sequential external API calls on every page load.
# Gate cleared 2026-06-11: p95=4,601ms > 3,000ms threshold (BLG-OPS-22).
# TTL: 15 minutes per ticker. Invalidated on screener run (see invalidate_research_cache).
_RESEARCH_CACHE_TTL_SECONDS = 900
_research_cache: dict = {}  # key: (ticker_upper, market) → {"data": ..., "expires_at": float}
_cache_hits = 0
_cache_misses = 0


def invalidate_research_cache(tickers: list = None) -> None:
    """Invalidate cached research entries. Called after screener run completes.

    Args:
        tickers: list of ticker strings to invalidate (upper-case). None = invalidate all.
    """
    global _cache_hits, _cache_misses
    if tickers is None:
        _research_cache.clear()
        logger.info("[research_cache] Full cache invalidated (screener run)")
    else:
        for ticker in tickers:
            for market in ("US", "UK"):
                _research_cache.pop((ticker.upper(), market), None)
        logger.info("[research_cache] Partial invalidation for %d tickers", len(tickers))

_YF_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


def _get_price_data(ticker: str, market: str):
    """Fetch current price and 1-day change % from Yahoo Finance.

    Returns a data dict on success or partial-null, _YF_UNAVAILABLE sentinel
    when Yahoo Finance cannot be reached, or _TICKER_NOT_FOUND sentinel when
    the ticker is unknown to Yahoo Finance.
    """
    try:
        time.sleep(0.3)
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        resp = requests.get(url, params={"interval": "1d", "range": "1d"}, headers=_YF_HEADERS, timeout=10)
        if not resp.ok:
            return _YF_UNAVAILABLE
        chart = resp.json().get("chart", {})
        result = chart.get("result")
        if not result:
            return _TICKER_NOT_FOUND
        meta = result[0]["meta"]
        price = meta.get("regularMarketPrice")
        change_pct = meta.get("regularMarketChangePercent")
        if change_pct is None:
            prev_close = meta.get("chartPreviousClose")
            if price and prev_close:
                change_pct = (price - prev_close) / prev_close * 100
        if price and market == "UK":
            price = price / 100  # pence → pounds
        return {
            "price": float(price) if price else None,
            "price_change_pct": float(change_pct) / 100 if change_pct is not None else None,
        }
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return _YF_UNAVAILABLE
    except Exception:
        return {"price": None, "price_change_pct": None}


def _get_market_cap(ticker: str) -> Optional[float]:
    try:
        import yfinance as yf
        info = yf.Ticker(ticker).info
        return info.get("marketCap")
    except Exception:
        return None


def _get_news(ticker: str, market: str) -> list:
    try:
        from services.news_service import get_news_headlines
        return get_news_headlines(ticker, market)
    except Exception:
        return []


def _regime_label(spy_risk_on: bool, ftse_risk_on: bool) -> str:
    if spy_risk_on and ftse_risk_on:
        return "risk_on"
    if not spy_risk_on and not ftse_risk_on:
        return "risk_off"
    return "mixed"


def _get_regime() -> Optional[dict]:
    try:
        from utils.pricing import check_market_regime
        r = check_market_regime()
        return {
            "label": _regime_label(r.get("spy_risk_on", False), r.get("ftse_risk_on", False)),
            "spy_risk_on": r.get("spy_risk_on"),
            "ftse_risk_on": r.get("ftse_risk_on"),
        }
    except Exception:
        return None


def _get_signal(ticker: str, portfolio_id: str) -> Optional[dict]:
    try:
        # ST-12 (BLG-BE-94, EPIC-02, v8.8): query the ticker directly rather
        # than fetching every signal ever generated for the portfolio and
        # filtering in Python — that scan's cost grows unbounded with the
        # signals table's history, unlike the rest of this endpoint's
        # sources. Same selection semantics below, just less I/O.
        signals = get_signals_for_ticker(ticker)
        ticker_upper = ticker.upper()
        matches = [s for s in signals if (s.get("ticker") or "").upper() == ticker_upper]
        if not matches:
            return None
        # Prefer most recent signal by date; within same date prefer 'new' over other statuses
        matches.sort(key=lambda x: (
            str(x.get("signal_date") or ""),
            0 if x.get("status") == "new" else 1
        ), reverse=True)
        s = matches[0]
        entry_price = float(s["current_price"]) if s.get("current_price") is not None else None
        stop_price = float(s["initial_stop"]) if s.get("initial_stop") is not None else None
        r_target = 3.0 if (entry_price is not None and stop_price is not None) else None
        return {
            "signal_id": str(s.get("id", "")),
            "direction": s.get("direction"),
            "signal_date": s.get("signal_date").isoformat() if hasattr(s.get("signal_date"), "isoformat") else s.get("signal_date"),
            "status": s.get("status"),
            "rank": s.get("rank"),
            "atr": float(s["atr_value"]) if s.get("atr_value") is not None else None,
            "entry_price": entry_price,
            "stop_price": stop_price,
            "r_target": r_target,
        }
    except Exception:
        return None


def _get_sector(ticker: str, market: str) -> dict:
    try:
        sector, industry = get_sector_and_industry(ticker, market)
        return {"sector": sector, "industry": industry}
    except Exception:
        return {"sector": None, "industry": None}


def _get_screener(ticker: str) -> Optional[dict]:
    try:
        results = get_screener_results(limit=500)
        rows = results.get("results", [])
        ticker_upper = ticker.upper()
        match = next((r for r in rows if (r.get("ticker") or "").upper() == ticker_upper), None)
        if not match:
            return None
        return {
            "in_latest_results": True,
            "latest_run_timestamp": match.get("run_timestamp"),
            "score": float(match["score"]) if match.get("score") is not None else None,
            "atr_pct": float(match["atr_pct"]) if match.get("atr_pct") is not None else None,
        }
    except Exception:
        return None


def _get_earnings(ticker: str, market: str) -> Optional[dict]:
    try:
        from services.earnings_service import get_earnings
        data = get_earnings(ticker, market)
        if not data:
            return None
        return {
            "next_earnings_date": data.get("next_earnings_date"),
            "days_until_earnings": data.get("days_until_earnings"),
            "fiscal_quarter": data.get("fiscal_quarter"),
            "data_source": data.get("data_source"),
        }
    except Exception:
        return None


@router.get("/{ticker}")
def get_research(ticker: str, market: Optional[str] = None):
    """GET /research/{ticker} — aggregated pre-trade research snapshot."""
    global _cache_hits, _cache_misses
    try:
        if not market:
            market = "UK" if ticker.upper().endswith(".L") else "US"
        else:
            market = market.upper()

        cache_key = (ticker.upper(), market)
        now = time.monotonic()
        cached = _research_cache.get(cache_key)
        if cached and now < cached["expires_at"]:
            _cache_hits += 1
            logger.info(
                "[research_cache] HIT %s (hits=%d misses=%d)", ticker.upper(), _cache_hits, _cache_misses
            )
            return cached["data"]
        _cache_misses += 1
        logger.info(
            "[research_cache] MISS %s (hits=%d misses=%d)", ticker.upper(), _cache_hits, _cache_misses
        )

        portfolio = get_portfolio()
        portfolio_id = str(portfolio["id"]) if portfolio else None

        price_data = _get_price_data(ticker, market)

        if price_data is _YF_UNAVAILABLE:
            return JSONResponse(
                status_code=503,
                content={"status": "error", "message": "Market data service is currently unavailable. Please try again later."},
            )
        if price_data is _TICKER_NOT_FOUND:
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": f"Ticker '{ticker.upper()}' not found."},
            )

        signal = _get_signal(ticker, portfolio_id) if portfolio_id else None
        regime = _get_regime()
        sector = _get_sector(ticker, market)
        screener = _get_screener(ticker)
        earnings = _get_earnings(ticker, market)
        market_cap = _get_market_cap(ticker)
        news_headlines = _get_news(ticker, market)

        response = {
            "status": "ok",
            "data": {
                "ticker": ticker.upper(),
                "market": market,
                "price": price_data["price"],
                "price_change_pct": price_data["price_change_pct"],
                "market_cap": market_cap,
                "signal": signal,
                "regime": regime,
                "sector": sector,
                "screener": screener,
                "earnings": earnings,
                "news_headlines": news_headlines,
            },
        }
        _research_cache[cache_key] = {"data": response, "expires_at": time.monotonic() + _RESEARCH_CACHE_TTL_SECONDS}
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
