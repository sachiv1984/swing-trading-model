"""
Ticker Universe Router (DS-01 / ST-01)
Contract: docs/specs/api_contracts/ticker_universe_api_contract.md
"""
import concurrent.futures
import os

import yfinance as yf
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from services.ticker_universe_service import get_all_tickers, add_ticker, soft_delete_ticker

router = APIRouter(prefix="/ticker-universe", tags=["Screener"])


def _validate_ticker_yfinance(ticker: str) -> str | None:
    """
    Validate ticker via Yahoo Finance with a 5-second timeout.

    Returns None when the ticker is recognised and tradeable.
    Returns an error detail string when invalid, unknown, or the lookup times out.

    Bypass entirely by setting env var SKIP_TICKER_VALIDATION=true (CI / integration tests).
    """
    def _fetch() -> bool:
        info = yf.Ticker(ticker).info
        return bool(info.get("quoteType"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_fetch)
        try:
            valid = future.result(timeout=5.0)
        except concurrent.futures.TimeoutError:
            return "Ticker validation timed out — check symbol and retry"
        except Exception:
            return f"Ticker '{ticker}' not found or not tradeable"

    if not valid:
        return f"Ticker '{ticker}' not found or not tradeable"
    return None


class AddTickerRequest(BaseModel):
    ticker: str
    market: str
    sector: Optional[str] = None
    industry: Optional[str] = None


@router.get("")
def list_tickers(market: Optional[str] = None, active_only: bool = True):
    """
    GET /ticker-universe

    Returns the list of tickers eligible for screener runs.
    Filtered by market (UK|US) and/or active status.
    """
    if market is not None and market not in ("UK", "US"):
        return JSONResponse(status_code=400, content={"status": "error", "message": "market must be UK or US"})
    tickers = get_all_tickers(market=market, active_only=active_only)
    return {"status": "ok", "data": tickers}


@router.post("", status_code=201)
def create_ticker(request: AddTickerRequest):
    """
    POST /ticker-universe

    Add a ticker to the screener universe.
    Re-activates soft-deleted tickers on conflict.
    Returns 400 if market is not UK or US, or ticker is blank.
    Returns 422 if the ticker symbol is not recognised by Yahoo Finance.
    Set SKIP_TICKER_VALIDATION=true to bypass the Yahoo Finance lookup (CI / tests).
    """
    try:
        ticker_upper = request.ticker.strip().upper()
        if not os.getenv("SKIP_TICKER_VALIDATION", "").lower() == "true":
            error = _validate_ticker_yfinance(ticker_upper)
            if error:
                raise HTTPException(status_code=422, detail=error)
        row = add_ticker(
            ticker=request.ticker,
            market=request.market,
            sector=request.sector,
            industry=request.industry,
        )
        return {"status": "ok", "data": row}
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)},
        )


@router.delete("/{ticker}")
def delete_ticker(ticker: str):
    """
    DELETE /ticker-universe/{ticker}

    Soft-deletes a ticker (sets active=FALSE).
    Returns 404 if ticker not found or already inactive.
    """
    removed = soft_delete_ticker(ticker)
    if not removed:
        return JSONResponse(status_code=404, content={"status": "error", "message": f"Ticker '{ticker.upper()}' not found or already inactive"})
    return {"status": "ok"}
