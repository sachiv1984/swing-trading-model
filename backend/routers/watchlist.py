"""
Watchlist Router

Endpoints for pre-position ticker monitoring.

Contract: docs/specs/api_contracts/watchlist_endpoints.md v0.1
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from database import get_portfolio
from services.watchlist_service import (
    get_watchlist,
    create_watchlist_entry,
    update_watchlist_entry,
    delete_watchlist_entry,
)

router = APIRouter(tags=["Watchlist"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_portfolio_id() -> str:
    portfolio = get_portfolio()
    if not portfolio:
        raise HTTPException(status_code=500, detail="Portfolio not found")
    return str(portfolio["id"])


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class CreateWatchlistRequest(BaseModel):
    ticker: str
    market: str
    target_entry_price: Optional[float] = None
    initial_stop_price: Optional[float] = None
    current_stop_price: Optional[float] = None


class UpdateWatchlistRequest(BaseModel):
    target_entry_price: Optional[float] = None
    initial_stop_price: Optional[float] = None
    current_stop_price: Optional[float] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/watchlist")
def get_watchlist_endpoint():
    """
    List all watchlist entries with computed signal_status.
    Contract: watchlist_endpoints.md §GET /watchlist
    """
    try:
        portfolio_id = _get_portfolio_id()
        entries = get_watchlist(portfolio_id)
        return {"status": "ok", "data": entries}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/watchlist", status_code=201)
def create_watchlist_endpoint(request: CreateWatchlistRequest):
    """
    Add a ticker to the watchlist.
    Returns 409 if ticker already exists for this portfolio.
    Contract: watchlist_endpoints.md §POST /watchlist
    """
    try:
        portfolio_id = _get_portfolio_id()
        entry = create_watchlist_entry(portfolio_id, request.model_dump())
        return {"status": "ok", "data": entry}
    except HTTPException:
        raise
    except LookupError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/watchlist/{entry_id}")
def update_watchlist_endpoint(entry_id: str, request: UpdateWatchlistRequest):
    """
    Update price fields on a watchlist entry. ticker and market are read-only.
    Contract: watchlist_endpoints.md §PATCH /watchlist/{id}
    """
    try:
        portfolio_id = _get_portfolio_id()
        entry = update_watchlist_entry(
            portfolio_id, entry_id,
            request.model_dump()  # includes None values so service can detect empties
        )
        return {"status": "ok", "data": entry}
    except HTTPException:
        raise
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/watchlist/{entry_id}")
def delete_watchlist_endpoint(entry_id: str):
    """
    Remove a ticker from the watchlist. Not idempotent — second call returns 404.
    Contract: watchlist_endpoints.md §DELETE /watchlist/{id}
    """
    try:
        portfolio_id = _get_portfolio_id()
        result = delete_watchlist_entry(portfolio_id, entry_id)
        return {"status": "ok", "data": result}
    except HTTPException:
        raise
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
