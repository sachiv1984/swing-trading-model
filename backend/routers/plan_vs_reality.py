"""
Plan vs Reality Router — PO-01

GET /trades/{trade_id}/plan-vs-reality
Spec: docs/specs/api_contracts/trades_endpoints.md#GET /trades/{id}/plan-vs-reality
ST-05, EPIC-02, v3.5
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.plan_vs_reality_service import get_plan_vs_reality_for_trade

router = APIRouter(tags=["Trades"])


@router.get("/trades/{trade_id}/plan-vs-reality")
def get_plan_vs_reality(trade_id: str):
    """
    GET /trades/{trade_id}/plan-vs-reality

    Returns the plan vs reality comparison for a closed trade that has a linked trade plan.
    - 200 {"status": "trade_open"} if position is still open.
    - 404 if trade not found or no trade plan linked.
    """
    try:
        result = get_plan_vs_reality_for_trade(trade_id)
        return {"status": "ok", "data": result}
    except ValueError as exc:
        msg = str(exc)
        if "No trade plan found" in msg:
            return JSONResponse(status_code=404, content={"status": "error", "message": "No trade plan found for this trade"})
        return JSONResponse(status_code=404, content={"status": "error", "message": msg})
    except Exception as exc:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(exc)})
