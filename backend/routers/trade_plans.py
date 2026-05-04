"""
Trade Plans Router (DS-04 / ST-02)

CRUD endpoints for pre-trade reasoning documents.
Spec: docs/specs/api_contracts/trade_plan_endpoints.md v0.1
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from database import (
    get_portfolio,
    create_trade_plan,
    get_trade_plans,
    get_trade_plan_by_id,
    update_trade_plan,
    delete_trade_plan,
    get_trade_plans_by_position,
    ensure_trade_plans_table,
)

router = APIRouter(prefix="/trade-plans", tags=["Trade Plans"])


class TradePlanCreate(BaseModel):
    ticker: str
    market: str
    position_id: Optional[str] = None
    setup_thesis: Optional[str] = None
    entry_rationale: Optional[str] = None
    regime_context_at_entry: Optional[str] = None
    r_target: Optional[float] = None
    early_exit_conditions: Optional[str] = None
    confirmation_criteria: Optional[str] = None
    checklist_completed: bool = False
    checklist_items: list = []
    status: str = "draft"


class TradePlanUpdate(BaseModel):
    position_id: Optional[str] = None
    setup_thesis: Optional[str] = None
    entry_rationale: Optional[str] = None
    regime_context_at_entry: Optional[str] = None
    r_target: Optional[float] = None
    early_exit_conditions: Optional[str] = None
    confirmation_criteria: Optional[str] = None
    checklist_completed: Optional[bool] = None
    checklist_items: Optional[list] = None
    status: Optional[str] = None


def _get_portfolio_id():
    portfolio = get_portfolio()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return str(portfolio["id"])


def _serialize(plan: dict) -> dict:
    out = dict(plan)
    for k, v in out.items():
        if hasattr(v, "isoformat"):
            out[k] = v.isoformat()
    if "checklist_items" in out and not isinstance(out["checklist_items"], list):
        import json
        try:
            out["checklist_items"] = json.loads(out["checklist_items"])
        except Exception:
            out["checklist_items"] = []
    if "r_target" in out and out["r_target"] is not None:
        out["r_target"] = float(out["r_target"])
    return out


@router.post("", status_code=201)
def create_plan(body: TradePlanCreate):
    """POST /trade-plans — create a new trade plan."""
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        plan = create_trade_plan(portfolio_id, body.dict())
        return {"status": "ok", "data": _serialize(plan)}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.get("")
def list_plans(status: Optional[str] = Query(default=None)):
    """GET /trade-plans — list all trade plans, optionally filtered by status."""
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        plans = get_trade_plans(portfolio_id, status)
        return {"status": "ok", "data": [_serialize(p) for p in plans]}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.get("/by-position/{position_id}")
def list_plans_by_position(position_id: str):
    """GET /trade-plans/by-position/{position_id} — plans linked to a position."""
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        plans = get_trade_plans_by_position(position_id, portfolio_id)
        return {"status": "ok", "data": [_serialize(p) for p in plans]}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.get("/{plan_id}")
def get_plan(plan_id: str):
    """GET /trade-plans/{id} — retrieve a single trade plan."""
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        plan = get_trade_plan_by_id(plan_id, portfolio_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Trade plan not found")
        return {"status": "ok", "data": _serialize(plan)}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.put("/{plan_id}")
def update_plan(plan_id: str, body: TradePlanUpdate):
    """PUT /trade-plans/{id} — update a trade plan."""
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        data = {k: v for k, v in body.dict().items() if v is not None}
        plan = update_trade_plan(plan_id, portfolio_id, data)
        if not plan:
            raise HTTPException(status_code=404, detail="Trade plan not found")
        return {"status": "ok", "data": _serialize(plan)}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.delete("/{plan_id}")
def delete_plan(plan_id: str):
    """DELETE /trade-plans/{id} — delete a trade plan."""
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        deleted = delete_trade_plan(plan_id, portfolio_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Trade plan not found")
        return {"status": "ok", "message": "Trade plan deleted"}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
