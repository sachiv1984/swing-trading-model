"""
Ticker Universe Router (DS-01 / ST-01)
Contract: docs/specs/api_contracts/screener_api_contract.md
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.ticker_universe_service import get_all_tickers, add_ticker, soft_delete_ticker

router = APIRouter(prefix="/ticker-universe", tags=["Screener"])


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
        raise HTTPException(status_code=400, detail="market must be UK or US")
    tickers = get_all_tickers(market=market, active_only=active_only)
    return {"status": "ok", "data": tickers}


@router.post("", status_code=201)
def create_ticker(request: AddTickerRequest):
    """
    POST /ticker-universe

    Add a ticker to the screener universe.
    Re-activates soft-deleted tickers on conflict.
    Returns 400 if market is not UK or US, or ticker is blank.
    """
    try:
        row = add_ticker(
            ticker=request.ticker,
            market=request.market,
            sector=request.sector,
            industry=request.industry,
        )
        return {"status": "ok", "data": row}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{ticker}")
def delete_ticker(ticker: str):
    """
    DELETE /ticker-universe/{ticker}

    Soft-deletes a ticker (sets active=FALSE).
    Returns 404 if ticker not found or already inactive.
    """
    removed = soft_delete_ticker(ticker)
    if not removed:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker.upper()}' not found or already inactive")
    return {"status": "ok"}
