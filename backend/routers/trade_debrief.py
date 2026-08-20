"""
Trade Debrief Router — ST-06 (EPIC-02, v8.9, BLG-FEAT-90)

GET  /trades/{trade_id}/debrief
POST /trades/{trade_id}/debrief

Spec: docs/specs/api_contracts/trade_endpoints.md#GET /trades/{trade_id}/debrief
§13 review: docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.debrief_service import generate_trade_debrief, get_existing_debrief

router = APIRouter(tags=["Trades"])


@router.get("/trades/{trade_id}/debrief")
def get_trade_debrief(trade_id: str):
    """
    GET /trades/{trade_id}/debrief

    Returns the existing AI-generated post-trade debrief for a closed trade,
    if one has already been generated. 404 if none exists yet -- the frontend
    offers an on-demand "Generate Debrief" action (POST, below) in that case.
    """
    try:
        result = get_existing_debrief(trade_id)
        if result is None:
            return JSONResponse(status_code=404, content={"status": "error", "message": "No debrief generated yet for this trade"})
        return {"status": "ok", "data": result}
    except Exception as exc:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(exc)})


@router.post("/trades/{trade_id}/debrief")
def post_trade_debrief(trade_id: str):
    """
    POST /trades/{trade_id}/debrief

    Generate (or regenerate) the AI post-trade debrief for a closed trade,
    on demand. Regeneration overwrites the prior debrief. Always returns 200
    with a debrief (the deterministic plan-vs-reality summary is never
    unavailable); `generation_status` in the response indicates whether the
    AI-generated focus area is present, omitted per §13 Condition 9's
    compliance-check fallback, or unavailable (no ANTHROPIC_API_KEY).
    """
    try:
        result = generate_trade_debrief(trade_id)
        return {"status": "ok", "data": result}
    except ValueError as exc:
        return JSONResponse(status_code=404, content={"status": "error", "message": str(exc)})
    except Exception as exc:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(exc)})
