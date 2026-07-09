"""
Trade Plans Router (DS-04 / ST-02)

CRUD endpoints for pre-trade reasoning documents.
Spec: docs/specs/api_contracts/trade_plan_endpoints.md v0.1
"""
import re
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
    get_trade_history,
    get_all_trade_plan_tags,
)

# Tag Rules — journal_components.md §3/§4 (reused for trade_tags, ST-05 BLG-FEAT-52)
_TAG_MAX_LENGTH = 20
_TAG_MAX_COUNT = 10
_TAG_PATTERN = re.compile(r"^[a-z0-9-]+$")


def _validate_trade_tags(tags: Optional[List[str]]) -> List[str]:
    """Lowercase, alphanumeric+hyphen, max 20 chars, max 10 tags, deduped."""
    if not tags:
        return []
    validated: List[str] = []
    for tag in tags:
        clean = (tag or "").strip().lower()
        if clean and len(clean) <= _TAG_MAX_LENGTH and _TAG_PATTERN.match(clean) and clean not in validated:
            validated.append(clean)
    return validated[:_TAG_MAX_COUNT]

_SETUP_QUALITY_MIN_TRADES = 20

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
    thesis_feedback: Optional[str] = None
    # Pre-entry check inputs — persisted so they survive save/reload
    planned_quantity: Optional[int] = None
    planned_entry_price: Optional[float] = None
    planned_stop_price: Optional[float] = None
    # SI-02 DS-07 fields (frontend-passed)
    signal_id: Optional[str] = None
    risk_percent_used: Optional[float] = None
    pre_entry_validation_snapshot: Optional[Any] = None
    trade_tags: Optional[List[str]] = None


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
    thesis_feedback: Optional[str] = None
    planned_quantity: Optional[int] = None
    planned_entry_price: Optional[float] = None
    planned_stop_price: Optional[float] = None
    trade_tags: Optional[List[str]] = None


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
        plan_data["trade_tags"] = _validate_trade_tags(plan_data.get("trade_tags"))

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


# ST-08, EPIC-04, v6.1
@router.get("/setup-quality-score")
def get_setup_quality_score(ticker: str = Query(..., description="Ticker symbol")):
    """
    GET /trade-plans/setup-quality-score?ticker={ticker}

    Return a 0–100 setup quality score derived from closed trade history.
    Gate: returns gate_not_met when fewer than 20 closed trades exist.

    Score factors:
      - win_rate: % of closed trades where pnl > 0
      - average_pnl_pct: average pnl_pct across all closed trades
      - score: clamp(round(win_rate * 0.6 + max(average_pnl_pct, 0) * 0.4), 0, 100)

    Spec: stage4_backlog_slice.md#ST-08
    """
    try:
        portfolio = get_portfolio()
        if not portfolio:
            return {"status": "ok", "data": {"gate_not_met": True, "min_trades_required": _SETUP_QUALITY_MIN_TRADES, "current_trades": 0}}

        trades = get_trade_history(str(portfolio["id"]))
        closed = [t for t in trades if t.get("pnl") is not None]
        total = len(closed)

        if total < _SETUP_QUALITY_MIN_TRADES:
            return {
                "status": "ok",
                "data": {
                    "gate_not_met": True,
                    "min_trades_required": _SETUP_QUALITY_MIN_TRADES,
                    "current_trades": total,
                },
            }

        winning = [t for t in closed if float(t["pnl"]) > 0]
        win_rate = round(len(winning) / total * 100, 1)
        avg_pnl = round(sum(float(t.get("pnl_pct") or 0) for t in closed) / total, 2)

        raw_score = win_rate * 0.6 + max(avg_pnl, 0) * 0.4
        score = max(0, min(100, round(raw_score)))

        return {
            "status": "ok",
            "data": {
                "gate_not_met": False,
                "ticker": ticker.upper(),
                "score": score,
                "matching_trades": total,
                "win_rate": win_rate,
                "average_pnl_pct": avg_pnl,
                "score_explanation": (
                    f"Based on {total} closed trades: {win_rate}% win rate, "
                    f"{avg_pnl}% average return. "
                    f"Score = win_rate×0.6 + max(avg_return,0)×0.4."
                ),
            },
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.get("/tags")
def get_trade_plan_tags_endpoint():
    """GET /trade-plans/tags — unique trade-plan tags for autocomplete (ST-05 BLG-FEAT-52).

    Mirrors GET /positions/tags. Reads trade_plans.trade_tags only — data-independent
    from the existing position/journal tags (journal_components.md).
    Spec: docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md
    """
    try:
        ensure_trade_plans_table()
        portfolio_id = _get_portfolio_id()
        tags = get_all_trade_plan_tags(portfolio_id)
        return {"status": "ok", "data": tags}
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
        if "trade_tags" in data:
            data["trade_tags"] = _validate_trade_tags(data["trade_tags"])

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
    planned_entry_price: Optional[float] = None
    planned_stop_price: Optional[float] = None
    planned_quantity: Optional[int] = None
    r_target: Optional[float] = None


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
            planned_entry_price=body.planned_entry_price,
            planned_stop_price=body.planned_stop_price,
            planned_quantity=body.planned_quantity,
            r_target=body.r_target,
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
