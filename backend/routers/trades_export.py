"""
Trade Export Router

GET /trades/export/csv — export full closed trade history as CSV attachment.

Contract: docs/specs/api_contracts/trade_endpoints.md v1.8.4
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, JSONResponse
from database import get_portfolio
from services.trade_service import build_trade_history_csv

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.get("/export/csv")
def export_trades_csv():
    """
    Export full closed trade history as a downloadable CSV file.
    Returns text/csv with Content-Disposition: attachment.
    Contract: trade_endpoints.md v1.8.4
    """
    try:
        portfolio = get_portfolio()
        if not portfolio:
            raise HTTPException(status_code=500, detail="Portfolio not found")

        portfolio_id = portfolio["id"]
        csv_content = build_trade_history_csv(portfolio_id)

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="trade_history.csv"'
            },
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"status": "error", "message": e.detail if isinstance(e.detail, str) else str(e.detail)},
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )
