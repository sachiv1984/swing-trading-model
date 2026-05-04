"""
Earnings Calendar Router (DS-04)

Provides next earnings date for tickers sourced from Yahoo Finance.
Spec: earnings_endpoints.md v0.1
"""
from fastapi import APIRouter, Query
from services.earnings_service import get_earnings

router = APIRouter(prefix="/earnings", tags=["Earnings"])


@router.get("/{ticker}")
def get_ticker_earnings(
    ticker: str,
    market: str = Query(default="US", description="US or UK"),
):
    """GET /earnings/{ticker} — next earnings date for a ticker."""
    return get_earnings(ticker, market)
