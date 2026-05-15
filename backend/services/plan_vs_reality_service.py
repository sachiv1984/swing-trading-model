"""
Plan vs Reality Calculation Service — PO-01

Compares trade plan predictions against actual trade outcomes for closed positions.
Spec: docs/specs/api_contracts/trades_endpoints.md#GET /trades/{id}/plan-vs-reality
ST-05, EPIC-02, v3.5
"""

from typing import Dict, Optional
from database import (
    get_trade_by_id,
    get_position_by_id,
    get_trade_plans_by_position,
    ensure_plan_vs_reality_columns,
)
from utils.formatting import decimal_to_float


def _to_float(val) -> Optional[float]:
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _compute_r_achieved(entry_price: float, exit_price: float, initial_stop: Optional[float]) -> Optional[float]:
    if initial_stop is None or entry_price is None or exit_price is None:
        return None
    risk = entry_price - initial_stop
    if risk == 0:
        return None
    return round((exit_price - entry_price) / risk, 2)


def _compute_entry_delta_pct(actual_entry: float, planned_entry: Optional[float]) -> Optional[float]:
    if planned_entry is None or actual_entry is None or planned_entry == 0:
        return None
    return round((actual_entry - planned_entry) / planned_entry * 100, 2)


def _compute_stop_discipline(actual_stop: Optional[float], planned_stop: Optional[float]) -> str:
    if planned_stop is None:
        return "not_captured"
    if actual_stop is None:
        return "not_captured"
    diff_pct = abs(actual_stop - planned_stop) / planned_stop * 100
    if diff_pct <= 1.0:
        return "on_plan"
    elif diff_pct <= 5.0:
        return "minor_deviation"
    return "deviation"


def _compute_plan_adherence_flag(
    entry_delta_pct: Optional[float],
    stop_discipline: str,
    exit_reason: Optional[str],
    early_exit_conditions: Optional[str],
) -> str:
    if entry_delta_pct is not None and abs(entry_delta_pct) > 2.0:
        return "entry_deviation"
    if stop_discipline in ("deviation",):
        return "stop_deviation"
    if exit_reason and early_exit_conditions:
        # Heuristic: if exit_reason contains keywords suggesting early exit
        early_keywords = ("stop", "loss", "cut", "early", "trailing")
        if any(k in exit_reason.lower() for k in early_keywords):
            plan_lower = early_exit_conditions.lower()
            if any(k in plan_lower for k in early_keywords):
                return "on_plan"
        return "early_exit" if exit_reason.lower() not in ("target", "target hit") else "on_plan"
    return "on_plan"


def compute_plan_vs_reality(trade: Dict, position: Optional[Dict], trade_plan: Dict) -> Dict:
    """Produce the plan_vs_reality comparison record."""
    entry_price = _to_float(trade.get("entry_price"))
    exit_price = _to_float(trade.get("exit_price"))
    initial_stop = _to_float(position.get("initial_stop")) if position else None

    r_achieved = _compute_r_achieved(entry_price, exit_price, initial_stop)
    r_target = _to_float(trade_plan.get("r_target"))
    r_delta = round(r_achieved - r_target, 2) if (r_achieved is not None and r_target is not None) else None

    planned_stop = _to_float(trade_plan.get("planned_stop_price"))
    stop_discipline = _compute_stop_discipline(initial_stop, planned_stop)

    # planned_entry_price: use signal entry_price if available via position — not yet snapshotted to trade_plans
    # Per arc4_data_requirements.md §3.1: planned_entry_price linkage may break if signal is updated.
    # Flag as not_captured until the snapshot field is added in a future sprint.
    entry_delta_pct = None

    exit_reason = trade.get("exit_reason")
    early_exit_conditions = trade_plan.get("early_exit_conditions")
    plan_adherence_flag = _compute_plan_adherence_flag(
        entry_delta_pct, stop_discipline, exit_reason, early_exit_conditions
    )

    lifecycle_state = position.get("position_state") if position else None

    return {
        "plan_linked": True,
        "trade_plan_id": str(trade_plan.get("id")) if trade_plan.get("id") else None,
        "r_achieved": r_achieved,
        "r_target": r_target,
        "r_delta": r_delta,
        "entry_delta_pct": entry_delta_pct,
        "stop_discipline": stop_discipline,
        "exit_reason_actual": exit_reason,
        "exit_reason_planned": early_exit_conditions,
        "lifecycle_state_at_exit": lifecycle_state,
        "plan_adherence_flag": plan_adherence_flag,
        "deviation_note": None,
    }


def get_plan_vs_reality_for_trade(trade_id: str) -> Dict:
    """
    Retrieve or compute the plan vs reality comparison for a trade.

    Returns:
        dict with key "status": "trade_open" if position is still open.
        dict with key "status": "no_plan" if no trade plan found (raises ValueError instead per API contract).
        dict with the full comparison record if trade is closed and has a plan.

    Raises:
        ValueError: if trade_id not found, or no trade plan linked.
    """
    ensure_plan_vs_reality_columns()

    trade = get_trade_by_id(trade_id)
    if trade is None:
        raise ValueError(f"Trade '{trade_id}' not found")

    trade = decimal_to_float(dict(trade))

    # Check if position is still open (trade_history record would not exist for open positions,
    # but guard against edge cases where position_id can be used to check position status)
    position_id = trade.get("position_id")
    position = get_position_by_id(str(position_id)) if position_id else None
    if position and position.get("status") == "open":
        return {"status": "trade_open"}

    # Look up trade plan via position_id
    if not position_id:
        raise ValueError("No trade plan found for this trade")

    portfolio_id = trade.get("portfolio_id")
    if not portfolio_id:
        raise ValueError("No trade plan found for this trade")

    plans = get_trade_plans_by_position(str(position_id), str(portfolio_id))
    if not plans:
        raise ValueError("No trade plan found for this trade")

    # Use the most recent active or completed plan
    active_plans = [p for p in plans if p.get("status") in ("active", "completed", "draft")]
    trade_plan = decimal_to_float(dict(active_plans[0])) if active_plans else decimal_to_float(dict(plans[0]))

    result = compute_plan_vs_reality(trade, position, trade_plan)
    return result
