"""
Trades Export Router

GET /trades/export/csv — Export full closed trade history as a
downloadable CSV attachment.

Contract: docs/specs/api_contracts/trade_endpoints.md v1.8.4
"""

import traceback

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response

from database import get_all_closed_trades_for_csv_export
from services.trade_csv_service import build_trade_history_csv

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.get("/trades/export/csv")
def export_trade_history_csv(request: Request):
    """
    Export the full closed trade history as a downloadable CSV file.

    Returns all closed trades ordered by exit_date descending.
    No date filter or pagination in v1.6.1 — full history always returned.

    On success: HTTP 200, Content-Type text/csv, attachment disposition.
    On error:   HTTP 500, JSON error envelope (not a CSV body).

    Spec: trade_endpoints.md v1.8.4 §GET /trades/export/csv
    """
    try:
        # Retrieve portfolio_id via the existing request.state pattern.
        # Adjust if the codebase resolves portfolio_id differently
        # (e.g. from a dependency, header, or JWT claim).
        portfolio_id = request.state.portfolio_id

        trades = get_all_closed_trades_for_csv_export(portfolio_id)
        csv_content = build_trade_history_csv(trades)

        # On empty trade history: build_trade_history_csv returns the
        # header row only. Response is still HTTP 200 — not 204. (B-12)
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="trade_history.csv"',
            },
        )

    except Exception as e:
        # All errors: print traceback for log visibility, return HTTP 500
        # as JSON (not CSV) per trade_endpoints.md v1.8.4 §errors. (B-13)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
