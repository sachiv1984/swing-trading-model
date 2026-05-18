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
import requests
import time
from database import get_portfolio
from services.signal_service import get_signals
from services.sector_service import get_sector_and_industry
from services.screener_batch_service import get_screener_results

router = APIRouter(prefix="/research", tags=["Research"])

_YF_UNAVAILABLE = "yf_unavailable"
_TICKER_NOT_FOUND = "ticker_not_found"

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
        signals = get_signals()
        ticker_upper = ticker.upper()
        matches = [s for s in signals if (s.get("ticker") or "").upper() == ticker_upper]
        if not matches:
            return None
        s = matches[0]
        return {
            "signal_id": str(s.get("id", "")),
            "direction": s.get("direction"),
            "signal_date": s.get("signal_date").isoformat() if hasattr(s.get("signal_date"), "isoformat") else s.get("signal_date"),
            "status": s.get("status"),
            "rank": s.get("rank"),
            "atr": float(s["atr"]) if s.get("atr") is not None else None,
            "entry_price": float(s["entry_price"]) if s.get("entry_price") is not None else None,
            "stop_price": float(s["stop_price"]) if s.get("stop_price") is not None else None,
            "r_target": float(s["r_target"]) if s.get("r_target") is not None else None,
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
    try:
        if not market:
            market = "UK" if ticker.upper().endswith(".L") else "US"
        else:
            market = market.upper()

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

        return {
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
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
