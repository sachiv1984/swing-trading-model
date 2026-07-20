"""
P&L Export <-> Trade Plan Closure Reconciliation Service

Spec: docs/specs/pnl_export_reconciliation.md
ST-03, EPIC-03, v7.6, BLG-FEAT-79

Structural closure-state check between trade_history (source of the tax-year
P&L export) and trade_plans.status. Does not compare P&L figures -
trade_plans stores no financial columns; see spec §4.
"""

from typing import Dict, List, Optional

from database import get_trade_history, get_trade_plans


def reconcile_pnl_vs_trade_plans(trade_history: List[Dict], trade_plans: List[Dict]) -> Dict:
    """Pure reconciliation logic - no DB coupling, takes already-fetched rows.

    Spec: docs/specs/pnl_export_reconciliation.md §3 (Reconciliation Rules)
    """
    history_by_position: Dict[str, Dict] = {}
    for row in trade_history:
        position_id = row.get("position_id")
        if position_id is not None:
            history_by_position[str(position_id)] = row

    plans_by_position: Dict[str, Dict] = {}
    for row in trade_plans:
        position_id = row.get("position_id")
        if position_id is not None:
            plans_by_position[str(position_id)] = row

    mismatches = []

    closed_plans = [p for p in trade_plans if p.get("status") == "closed" and p.get("position_id") is not None]
    for plan in closed_plans:
        position_id = str(plan.get("position_id"))
        if position_id not in history_by_position:
            mismatches.append({
                "type": "closed_plan_no_trade_history",
                "position_id": position_id,
                "trade_plan_id": str(plan.get("id")),
                "ticker": plan.get("ticker"),
            })

    for trade in trade_history:
        position_id = trade.get("position_id")
        if position_id is None:
            continue
        position_id = str(position_id)
        plan = plans_by_position.get(position_id)
        if plan is not None and plan.get("status") != "closed":
            mismatches.append({
                "type": "trade_history_plan_not_closed",
                "position_id": position_id,
                "trade_history_id": str(trade.get("id")),
                "trade_plan_id": str(plan.get("id")),
                "ticker": trade.get("ticker"),
                "plan_status": plan.get("status"),
            })

    return {
        "trade_history_count": len(trade_history),
        "trade_plans_closed_count": len(closed_plans),
        "mismatches": mismatches,
    }


def run_reconciliation(portfolio_id: str) -> Dict:
    """Fetch live rows and run the reconciliation. Read-only - no writes."""
    trade_history = get_trade_history(portfolio_id)
    trade_plans = get_trade_plans(portfolio_id)
    return reconcile_pnl_vs_trade_plans(trade_history, trade_plans)
