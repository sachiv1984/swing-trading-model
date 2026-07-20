"""
Watchlist Router

Endpoints for pre-position ticker monitoring.

Contract: docs/specs/api_contracts/watchlist_endpoints.md v0.1
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from typing import List
from database import get_portfolio
from services.watchlist_service import (
    get_watchlist,
    create_watchlist_entry,
    update_watchlist_entry,
    delete_watchlist_entry,
    get_all_watchlist_tags,
    bulk_tag_watchlist,
    bulk_delete_watchlist,
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


class BulkTagRequest(BaseModel):
    ids: List[str]
    tags: List[str]


class BulkIdsRequest(BaseModel):
    ids: List[str]


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


@router.get("/watchlist/tags")
def get_watchlist_tags_endpoint():
    """
    GET /watchlist/tags — unique tags across all watchlist entries, for autocomplete.
    Contract: watchlist_endpoints.md §GET /watchlist/tags
    ST-03 (BLG-FE-117, EPIC-03, v7.5).
    """
    try:
        portfolio_id = _get_portfolio_id()
        tags = get_all_watchlist_tags(portfolio_id)
        return {"status": "ok", "data": tags}
    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# IMPORTANT — router ordering: bulk-tag/bulk MUST be declared before
# PATCH/DELETE /watchlist/{entry_id} below, or FastAPI routes them to the
# wildcard handler with entry_id="bulk-tag"/"bulk" (same constraint as
# alerts.py's /notifications/mark-all-read note).
@router.post("/watchlist/bulk-tag")
def bulk_tag_watchlist_endpoint(request: BulkTagRequest):
    """
    POST /watchlist/bulk-tag — add tags to each selected watchlist entry (union, not replace).
    Contract: watchlist_endpoints.md §POST /watchlist/bulk-tag
    ST-03 (BLG-FE-117, EPIC-03, v7.5).
    """
    try:
        portfolio_id = _get_portfolio_id()
        result = bulk_tag_watchlist(portfolio_id, request.ids, request.tags)
        return {"status": "ok", "data": result}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/watchlist/bulk")
def bulk_delete_watchlist_endpoint(request: BulkIdsRequest):
    """
    DELETE /watchlist/bulk — remove each selected watchlist entry.
    Contract: watchlist_endpoints.md §DELETE /watchlist/bulk
    ST-03 (BLG-FE-117, EPIC-03, v7.5).
    """
    try:
        portfolio_id = _get_portfolio_id()
        result = bulk_delete_watchlist(portfolio_id, request.ids)
        return {"status": "ok", "data": result}
    except HTTPException:
        raise
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
