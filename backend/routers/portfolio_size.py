"""
Portfolio Size Router

Implements POST /portfolio/size — position sizing calculator endpoint.

Contract: docs/specs/api_contracts/portfolio_endpoints.md
Calculation rules: docs/specs/strategy_rules.md §4.1

This router is thin. All business logic lives in sizing_service.py.
HTTP 400 is returned for malformed requests (missing required fields,
invalid market, invalid fx_rate). Business rule failures (invalid stop
distance, missing snapshot, etc.) return HTTP 200 with valid: false — this
is intentional per the API contract.
"""

from fastapi import APIRouter, HTTPException
from models.requests import SizePositionRequest
from services.sizing_service import size_position

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.post("/size")
def size_position_endpoint(request: SizePositionRequest):
    """
    Calculate suggested position size based on portfolio risk parameters.

    Read-only. Does not create a position or mutate any state.
    Safe to call repeatedly on debounced keystrokes.

    Returns HTTP 200 for all business rule outcomes (valid or invalid).
    Returns HTTP 400 for malformed requests (missing fields, bad market value).
    Returns HTTP 500 for unexpected server errors.
    """
    try:
        result = size_position(
            entry_price=request.entry_price,
            stop_price=request.stop_price,
            risk_percent=request.risk_percent,
            market=request.market or "UK",
            fx_rate=request.fx_rate,
        )
        return {"status": "ok", "data": result}

    except ValueError as e:
        # Pydantic validators raise ValueError for bad market/fx_rate values
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Sizing calculation failed: {str(e)}")
