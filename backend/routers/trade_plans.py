"""
Trade Plans Router (DS-04 / ST-02)

CRUD endpoints for pre-trade reasoning documents.
Spec: docs/specs/api_contracts/trade_plan_endpoints.md v0.1
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import timezone, datetime
from database import (
    get_portfolio,
    create_trade_plan,
    get_trade_plans,
    get_trade_plan_by_id,
    update_trade_plan,
    delete_trade_plan,
    get_trade_plans_by_position,
    ensure_trade_plans_table,
    ensure_si02_trade_plans_columns,
    create_red_flag_event,
    ensure_red_flag_events_table,
    get_latest_snapshot,
    get_settings,
)

router = APIRouter(prefix="/trade-plans", tags=["Trade Plans"])


SETUP_TYPE_OPTIONS = {
    "Breakout",
    "Pullback to MA",
    "Momentum Continuation",
    "Mean Reversion",
    "Catalyst-driven",
    "Other",
}


class TradePlanCreate(BaseModel):
    ticker: str
    market: str
    position_id: Optional[str] = None
    setup_type: Optional[str] = None
    setup_thesis: Optional[str] = None
    entry_rationale: Optional[str] = None
    regime_context_at_entry: Optional[str] = None
    r_target: Optional[float] = None
    early_exit_conditions: Optional[str] = None
    confirmation_criteria: Optional[str] = None
    checklist_completed: bool = False
    checklist_items: list = []
    status: str = "draft"
    pre_entry_override_acknowledged: Optional[bool] = None
    # SI-02 DS-07 fields (frontend-passed)
    signal_id: Optional[str] = None
    risk_percent_used: Optional[float] = None
    pre_entry_validation_snapshot: Optional[Any] = None


class TradePlanUpdate(BaseModel):
    position_id: Optional[str] = None
    setup_type: Optional[str] = None
    setup_thesis: Optional[str] = None
    entry_rationale: Optional[str] = None
    regime_context_at_entry: Optional[str] = None
    r_target: Optional[float] = None
    early_exit_conditions: Optional[str] = None
    confirmation_criteria: Optional[str] = None
    checklist_completed: Optional[bool] = None
    checklist_items: Optional[list] = None
    status: Optional[str] = None
    abandonment_reason: Optional[str] = None
    pre_entry_override_acknowledged: Optional[bool] = None


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


def _maybe_write_override_event(ticker: str, position_id=None) -> None:
    try:
        ensure_red_flag_events_table()
        create_red_flag_event(
            event_type="pre_entry_override",
            ticker=ticker,
            position_id=str(position_id) if position_id else None,
            context={"source": "trade_plan", "override_acknowledged": True},
        )
    except Exception:
        pass


@router.post("", status_code=201)
def create_plan(body: TradePlanCreate):
    """POST /trade-plans — create a new trade plan.

    SI-02 DS-07: backend captures portfolio_value_at_entry and effective_settings_snapshot
    at creation time. signal_id, risk_percent_used, and pre_entry_validation_snapshot are
    frontend-passed and persisted without validation (nullable — may be absent from body).
    Spec: docs/specs/data_model/si02_data_schema.md §7
    """
    try:
        ensure_trade_plans_table()
        ensure_si02_trade_plans_columns()
        portfolio_id = _get_portfolio_id()

        plan_data = body.dict()

        # Capture portfolio_value_at_entry from latest snapshot
        try:
            snapshot = get_latest_snapshot(portfolio_id)
            plan_data["portfolio_value_at_entry"] = float(snapshot["total_value"]) if snapshot and snapshot.get("total_value") is not None else None
        except Exception:
            plan_data["portfolio_value_at_entry"] = None

        # Capture effective_settings_snapshot from current settings
        try:
            settings_list = get_settings()
            if settings_list:
                s = settings_list[0]
                plan_data["effective_settings_snapshot"] = {
                    "default_risk_percent": float(s["default_risk_percent"]) if s.get("default_risk_percent") is not None else None,
                    "atr_multiplier_initial": float(s["atr_multiplier_initial"]) if s.get("atr_multiplier_initial") is not None else None,
                    "atr_multiplier_trailing": float(s["atr_multiplier_trailing"]) if s.get("atr_multiplier_trailing") is not None else None,
                    "min_hold_days": int(s["min_hold_days"]) if s.get("min_hold_days") is not None else None,
                    "captured_at": datetime.now(timezone.utc).isoformat(),
                }
            else:
                plan_data["effective_settings_snapshot"] = None
        except Exception:
            plan_data["effective_settings_snapshot"] = None

        plan = create_trade_plan(portfolio_id, plan_data)
        if body.pre_entry_override_acknowledged:
            _maybe_write_override_event(body.ticker, body.position_id)
        return {"status": "ok", "data": _serialize(plan)}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.get("")
def list_plans(status: Optional[str] = Query(default=None), ticker: Optional[str] = Query(default=None)):
    """GET /trade-plans — list all trade plans, optionally filtered by status and/or ticker."""
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        plans = get_trade_plans(portfolio_id, status, ticker)
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
    """PUT /trade-plans/{id} — update a trade plan.

    Abandonment rules (BLG-FEAT-21):
    - status='abandoned' requires abandonment_reason (400 if missing)
    - Cannot abandon a plan linked to an active (open) position (400)
    """
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        data = {k: v for k, v in body.dict().items() if v is not None}

        if data.get("status") == "abandoned":
            if not data.get("abandonment_reason"):
                raise HTTPException(status_code=400, detail="abandonment_reason is required when status is 'abandoned'")
            existing = get_trade_plan_by_id(plan_id, portfolio_id)
            if not existing:
                raise HTTPException(status_code=404, detail="Trade plan not found")
            if existing.get("position_id"):
                from database import get_positions
                linked_positions = get_positions(portfolio_id, status="open")
                linked_ids = {str(p["id"]) for p in linked_positions}
                if str(existing["position_id"]) in linked_ids:
                    raise HTTPException(
                        status_code=400,
                        detail="Cannot abandon a trade plan linked to an active open position",
                    )

        plan = update_trade_plan(plan_id, portfolio_id, data)
        if not plan:
            raise HTTPException(status_code=404, detail="Trade plan not found")
        if body.pre_entry_override_acknowledged:
            _maybe_write_override_event(plan.get("ticker", ""), plan.get("position_id"))
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


class GeneratePlanRequest(BaseModel):
    ticker: str
    market: str = "US"
    setup_type: Optional[str] = None
    signal_data: Optional[dict] = None


@router.post("/generate-plan")
def generate_plan(body: GeneratePlanRequest):
    """POST /trade-plans/generate-plan — generate all plan fields from ticker + signal.

    Does not require a saved plan. Accepts form data and signal data in the request body.
    Returns all fields: setup_thesis, entry_rationale, confirmation_criteria,
    early_exit_conditions, r_target.
    """
    try:
        from services.gemini_service import generate_full_plan
        result = generate_full_plan(
            ticker=body.ticker,
            market=body.market,
            setup_type=body.setup_type,
            signal_data=body.signal_data,
        )
        return {"status": "ok", "data": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.post("/{plan_id}/generate-thesis")
def generate_thesis(plan_id: str):
    """POST /trade-plans/{plan_id}/generate-thesis — generate thesis via Claude Haiku.

    Returns generated thesis when ANTHROPIC_API_KEY is set.
    Returns graceful error payload (HTTP 200) when key is absent or API call fails.
    Audit trail and cost tracking logged in ST-07/ST-08.
    """
    try:
        from services.gemini_service import generate_setup_thesis
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        plan = get_trade_plan_by_id(plan_id, portfolio_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Trade plan not found")

        result = generate_setup_thesis(
            ticker=plan.get("ticker", ""),
            market=plan.get("market", "US"),
            setup_type=plan.get("setup_type"),
            plan_data={
                "entry_rationale": plan.get("entry_rationale"),
                "confirmation_criteria": plan.get("confirmation_criteria"),
            },
            plan_id=plan_id,
        )
        return {"status": "ok", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
