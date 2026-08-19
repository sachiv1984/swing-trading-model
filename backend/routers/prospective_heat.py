"""
Prospective Heat Router

Implements GET /portfolio/prospective-heat — calculates portfolio heat
if a prospective new position were added.

Contract: docs/specs/api_contracts/portfolio_endpoints.md §GET /portfolio/prospective-heat
Calculation rules: docs/specs/metrics_definitions.md §Portfolio Heat

Read-only. Does not mutate any state.

Calculation logic extracted to services/portfolio_service.py::calculate_prospective_heat
(ST-05, BLG-FEAT-91) — shared with POST /portfolio/size's heat_impact_percent
field (services/sizing_service.py). This router is now a thin wrapper.
"""

from fastapi import APIRouter
from typing import Optional
from services.portfolio_service import calculate_prospective_heat

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/prospective-heat")
def prospective_heat_endpoint(
    ticker: str,
    shares: float,
    entry_price: float,
    stop_price: float,
    market: Optional[str] = "UK",
    fx_rate: Optional[float] = None,
):
    """
    Calculate portfolio heat percentage if a prospective position were added.

    Read-only. Does not create a position or mutate any state.
    Safe to call repeatedly on debounced keystrokes.

    Returns HTTP 200 for all outcomes (valid or invalid inputs).
    Returns HTTP 500 for unexpected server errors.
    """
    result = calculate_prospective_heat(
        entry_price=entry_price,
        stop_price=stop_price,
        shares=shares,
        market=market,
        fx_rate=fx_rate,
    )

    if not result.get("valid"):
        return {"status": "ok", "data": result}

    return {
        "status": "ok",
        "data": {
            **result,
            "ticker": ticker,
        },
    }
