"""
Screener Router (DS-01 / ST-04)
Contract: docs/specs/api_contracts/screener_api_contract.md
"""
import logging
import uuid
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from services.screener_batch_service import run_screener, get_screener_results, is_run_in_progress, get_regime_distribution
from services.health_service import record_nightly_job

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/screener", tags=["Screener"])


class RunScreenerRequest(BaseModel):
    ticker_universe: Optional[List[str]] = None


@router.get("/results")
def screener_results(
    limit: int = 50,
    offset: int = 0,
    market: Optional[str] = None,
    run_id: Optional[str] = None,
):
    """
    GET /screener/results

    Returns screener result records from the latest completed run.
    Contract: screener_api_contract.md
    """
    if limit > 200:
        return JSONResponse(status_code=400, content={"status": "error", "message": "INVALID_PARAMS: limit must be ≤ 200"})
    if market and market not in ("US", "UK", "all"):
        return JSONResponse(status_code=400, content={"status": "error", "message": "INVALID_PARAMS: market must be US, UK, or all"})
    try:
        data = get_screener_results(market=market, run_id=run_id, limit=limit, offset=offset)
        return {"ok": True, "data": data}
    except ValueError:
        # If a run is currently in progress and the caller supplied a run_id,
        # return 202 so the frontend keeps polling instead of treating it as a
        # hard failure.
        if run_id and is_run_in_progress():
            return JSONResponse(
                status_code=202,
                content={"ok": True, "data": {"status": "running", "run_id": run_id}},
            )
        return JSONResponse(status_code=404, content={"status": "error", "message": "NO_RESULTS"})


@router.get("/regime-distribution")
def screener_regime_distribution(window: str = "30d"):
    """
    GET /screener/regime-distribution

    Returns the aggregate market regime (risk-on/risk-off) distribution
    over screener run history for the requested rolling window.
    Contract: screener_api_contract.md. ST-21 (BLG-FEAT-29, EPIC-06, v8.5).
    """
    if window not in ("30d", "60d", "all"):
        return JSONResponse(status_code=400, content={"status": "error", "message": "INVALID_PARAMS: window must be 30d, 60d, or all"})
    data = get_regime_distribution(window=window)
    return {"ok": True, "data": data}


@router.post("/run", status_code=202)
def trigger_screener_run(
    background_tasks: BackgroundTasks,
    request: RunScreenerRequest = RunScreenerRequest(),
):
    """
    POST /screener/run

    Triggers a screener run asynchronously. Returns 202 immediately with a run_id.
    The frontend polls GET /screener/results?run_id=<id> until results appear.
    Returns 409 if a run is already in progress.
    Contract: screener_api_contract.md

    ST-01 (BLG-OPS-144, EPIC-01, v8.8): background run outcome is now recorded in the
    GET /health/scheduler job registry (job name "screener_refresh") so a missed or
    failed nightly refresh is visible — this endpoint previously had no scheduled
    trigger at all (root cause of screener results going 24 days stale).
    """
    if request.ticker_universe is not None:
        for t in request.ticker_universe:
            if not t or not t.strip():
                return JSONResponse(status_code=400, content={"status": "error", "message": "INVALID_TICKER"})

    if is_run_in_progress():
        return JSONResponse(status_code=409, content={"status": "error", "message": "RUN_IN_PROGRESS"})

    pending_run_id = str(uuid.uuid4())

    def _run_in_background():
        try:
            result = run_screener(request.ticker_universe, run_id=pending_run_id)
            from routers.research import invalidate_research_cache
            invalidate_research_cache()
            record_nightly_job("screener_refresh", "ok", detail={"run_id": pending_run_id, "result": result})
        except RuntimeError as exc:
            logger.warning("Background screener run failed: %s", exc)
            record_nightly_job("screener_refresh", "error", error=str(exc))
        except Exception as exc:
            logger.error("Background screener run error: %s", exc, exc_info=True)
            record_nightly_job("screener_refresh", "error", error=str(exc))

    background_tasks.add_task(_run_in_background)

    return {"ok": True, "data": {
        "run_id": pending_run_id,
        "status": "accepted",
    }}
