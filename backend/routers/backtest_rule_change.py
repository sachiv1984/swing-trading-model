"""
Backtest Rule Change Router (ST-07, BLG-FEAT-89, EPIC-02, v8.9)

Implements the "Backtest Rule Change" tab's endpoints on the Strategy
Benchmark page — run a candidate strategy_rules.md parameter change against
a bounded historical window from inside the app, with no external script
step, and persist each run for later audit.

Contract: docs/specs/api_contracts/strategy_benchmark_endpoints.md
Design source: docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md

§13 compliance note: see services/backtest_rule_service.py module docstring.
This endpoint is read/compute-only relative to strategy_rules.md — it never
writes to the canonical strategy document or any live rule configuration.
"""

from typing import Dict, Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import get_backtest_rule_runs, get_backtest_rule_run_by_id
from services.backtest_rule_service import run_candidate_backtest, BacktestRuleChangeError

router = APIRouter(prefix="/strategy/backtest-rule-change", tags=["Strategy Benchmark"])


class BacktestRuleChangeRequest(BaseModel):
    # All fields optional — any omitted field falls back to the live
    # strategy_rules.md value (services.backtest_rule_service.LIVE_PARAMS).
    lookback: Optional[int] = None
    top_n: Optional[int] = None
    atr_mult: Optional[float] = None
    rebalance_freq: Optional[str] = None
    min_position_pct: Optional[float] = None
    max_position_pct: Optional[float] = None
    min_hold_days: Optional[int] = None
    risk_off_mode: Optional[str] = None
    stop_loss_mode: Optional[str] = None
    initial_atr_mult: Optional[float] = None
    profit_atr_mult: Optional[float] = None
    initiated_by: Optional[str] = None


@router.post("/run")
def run_backtest_rule_change(request: BacktestRuleChangeRequest):
    """
    Run a candidate rule-change backtest against a bounded historical window
    and compare it to the live rule set over the identical universe/window.

    Synchronous — backtests over the bounded universe/window typically
    complete in single-digit seconds; the frontend shows an inline spinner
    for the duration (ux_spec.md §2.1).

    Returns HTTP 200 with the comparison result and the persisted run's id.
    Returns HTTP 400 for an unknown candidate parameter field.
    Returns HTTP 500 for unexpected server errors.
    """
    overrides = request.dict(exclude={"initiated_by"}, exclude_none=True)
    try:
        result = run_candidate_backtest(overrides, initiated_by=request.initiated_by)
        return {"status": "ok", "data": result}
    except BacktestRuleChangeError as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Backtest run failed: {str(e)}"},
        )


@router.get("/runs")
def list_backtest_rule_runs(limit: int = 20):
    """Run History — most recent first (AC-03). Summary fields only."""
    try:
        runs = get_backtest_rule_runs(limit=limit)
        for r in runs:
            r["id"] = str(r["id"])
            r["created_at"] = r["created_at"].isoformat()
            r["universe_start_date"] = r["universe_start_date"].isoformat()
            r["universe_end_date"] = r["universe_end_date"].isoformat()
        return {"status": "ok", "data": runs}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.get("/runs/{run_id}")
def get_backtest_rule_run(run_id: str):
    """Re-view a prior run's stored output without re-running (AC-03)."""
    try:
        run = get_backtest_rule_run_by_id(run_id)
        if not run:
            return JSONResponse(status_code=404, content={"status": "error", "message": "Run not found"})
        run["id"] = str(run["id"])
        run["created_at"] = run["created_at"].isoformat()
        run["universe_start_date"] = run["universe_start_date"].isoformat()
        run["universe_end_date"] = run["universe_end_date"].isoformat()
        return {"status": "ok", "data": run}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
