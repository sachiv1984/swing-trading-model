"""
News Router (DS-06)

Exposes Alpaca news headlines for US tickers.
Display-only per BLG-GOV-16 §13 review.
"""
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from services.news_service import get_news_headlines

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/{ticker}")
def get_ticker_news(
    ticker: str,
    market: str = Query(default="US", description="US or UK"),
    limit: int = Query(default=10, ge=1, le=10),
):
    """
    Fetch up to 10 recent news headlines for a ticker.

    UK tickers return an empty headlines list (no Alpaca news data).
    Display-only — no sentiment scoring.
    """
    try:
        headlines = get_news_headlines(ticker.upper(), market.upper(), limit=limit)
        return {
            "ok": True,
            "data": {
                "ticker": ticker.upper(),
                "market": market.upper(),
                "headlines": headlines,
                "count": len(headlines),
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
