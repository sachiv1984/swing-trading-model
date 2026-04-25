"""
Screener Router (DS-01 / ST-04)
Contract: docs/specs/api_contracts/screener_api_contract.md
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from services.screener_batch_service import run_screener, get_screener_results

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
        raise HTTPException(status_code=400, detail="INVALID_PARAMS: limit must be ≤ 200")
    if market and market not in ("US", "UK", "all"):
        raise HTTPException(status_code=400, detail="INVALID_PARAMS: market must be US, UK, or all")
    try:
        data = get_screener_results(market=market, run_id=run_id, limit=limit, offset=offset)
        return {"ok": True, "data": data}
    except ValueError:
        raise HTTPException(status_code=404, detail="NO_RESULTS")


@router.post("/run", status_code=202)
def trigger_screener_run(request: RunScreenerRequest = RunScreenerRequest()):
    """
    POST /screener/run

    Triggers a screener run. Runs synchronously; returns when complete.
    Returns 409 if a run is already in progress.
    Contract: screener_api_contract.md
    """
    if request.ticker_universe is not None:
        for t in request.ticker_universe:
            if not t or not t.strip():
                raise HTTPException(status_code=400, detail="INVALID_TICKER")
    try:
        result = run_screener(request.ticker_universe)
        return {"ok": True, "data": {"run_id": result["run_id"], "status": "accepted"}}
    except RuntimeError as e:
        if "RUN_IN_PROGRESS" in str(e):
            raise HTTPException(status_code=409, detail="RUN_IN_PROGRESS")
        raise HTTPException(status_code=500, detail=str(e))
