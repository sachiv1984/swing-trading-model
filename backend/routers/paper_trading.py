from fastapi import APIRouter, HTTPException
from services.alpaca_paper_sync_service import get_paper_positions

router = APIRouter(tags=["Portfolio"])


@router.get("/portfolio/paper-positions")
def get_paper_positions_endpoint():
    """
    Returns current Alpaca paper account positions with P&L.
    Returns {"paper_tracking_enabled": false} when ALPACA_PAPER_API_KEY is absent.
    §13: display-only; no automated order execution.
    """
    try:
        result = get_paper_positions()
        if not result.get("paper_tracking_enabled"):
            return result
        return {"status": "ok", **result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
