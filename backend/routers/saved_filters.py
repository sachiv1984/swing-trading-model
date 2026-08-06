"""
Saved Filters Router

Endpoints for named, server-side Trade History filter presets
(ST-04, BLG-FE-118, EPIC-04, v7.5).

Contract: docs/specs/api_contracts/saved_filters_endpoints.md v1.0
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict

from database import get_portfolio
from services.saved_filters_service import (
    get_saved_filters,
    create_saved_filter,
    delete_saved_filter,
)

router = APIRouter(tags=["Saved Filters"])


def _get_portfolio_id() -> str:
    portfolio = get_portfolio()
    if not portfolio:
        raise HTTPException(status_code=500, detail="Portfolio not found")
    return str(portfolio["id"])


class CreateSavedFilterRequest(BaseModel):
    name: str
    filter_state: Dict[str, Any]


@router.get("/saved-filters")
def get_saved_filters_endpoint():
    """
    Return all saved filter presets for the portfolio.
    Contract: saved_filters_endpoints.md §GET /saved-filters
    """
    try:
        portfolio_id = _get_portfolio_id()
        data = get_saved_filters(portfolio_id)
        return {"status": "ok", "data": data}
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )
    except Exception as e:
        import traceback; traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )


@router.post("/saved-filters")
def create_saved_filter_endpoint(request: CreateSavedFilterRequest):
    """
    Create a named filter preset. Returns 400 for a duplicate name.
    Contract: saved_filters_endpoints.md §POST /saved-filters
    """
    try:
        portfolio_id = _get_portfolio_id()
        preset = create_saved_filter(portfolio_id, request.model_dump())
        return {"status": "ok", "data": preset}
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
    except Exception as e:
        import traceback; traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )


@router.delete("/saved-filters/{filter_id}")
def delete_saved_filter_endpoint(filter_id: str):
    """
    Delete a saved filter preset.
    Contract: saved_filters_endpoints.md §DELETE /saved-filters/{id}
    """
    try:
        portfolio_id = _get_portfolio_id()
        result = delete_saved_filter(portfolio_id, filter_id)
        return {"status": "ok", "data": result}
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )
    except LookupError as e:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": str(e)},
        )
    except Exception as e:
        import traceback; traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )
