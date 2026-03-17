"""
Prospective Heat Router

Implements GET /portfolio/prospective-heat — calculates portfolio heat
if a prospective new position were added.

Contract: docs/specs/api_contracts/portfolio_endpoints.md §GET /portfolio/prospective-heat
Calculation rules: docs/specs/metrics_definitions.md §Portfolio Heat

Read-only. Does not mutate any state.
"""

from fastapi import APIRouter
from typing import Optional
from services.portfolio_service import get_portfolio_summary
from utils.pricing import get_live_fx_rate

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
    # --- Input validation ---
    if stop_price >= entry_price:
        return {"status": "ok", "data": {"valid": False, "error": "stop_price must be less than entry_price"}}
    if shares <= 0:
        return {"status": "ok", "data": {"valid": False, "error": "shares must be greater than 0"}}
    if entry_price <= 0 or stop_price <= 0:
        return {"status": "ok", "data": {"valid": False, "error": "entry_price and stop_price must be greater than 0"}}

    # --- FX rate ---
    market = (market or "UK").upper()
    if market == "US":
        fx_rate_used = float(fx_rate) if fx_rate else get_live_fx_rate()
    else:
        fx_rate_used = 1.0

    # --- Current portfolio state ---
    portfolio = get_portfolio_summary()
    portfolio_value_gbp = portfolio.get("total_value", 0.0)

    if portfolio_value_gbp <= 0:
        return {"status": "ok", "data": {"valid": False, "error": "portfolio value is zero; cannot calculate heat"}}

    position_risks = portfolio.get("position_risks", [])
    current_risk_gbp = sum(r.get("position_risk_gbp", 0.0) for r in position_risks)

    # --- Prospective position risk (metrics_definitions.md §Portfolio Heat) ---
    prospective_risk_gbp = round((entry_price - stop_price) * shares / fx_rate_used, 2)

    # --- Heat calculations ---
    current_heat_percent = round(current_risk_gbp / portfolio_value_gbp * 100, 2)
    total_risk_gbp = current_risk_gbp + prospective_risk_gbp
    prospective_heat_percent = round(total_risk_gbp / portfolio_value_gbp * 100, 2)
    incremental_heat_percent = round(prospective_heat_percent - current_heat_percent, 2)

    return {
        "status": "ok",
        "data": {
            "valid": True,
            "current_heat_percent": current_heat_percent,
            "prospective_heat_percent": prospective_heat_percent,
            "incremental_heat_percent": incremental_heat_percent,
            "prospective_risk_gbp": prospective_risk_gbp,
            "portfolio_value_gbp": round(portfolio_value_gbp, 2),
            "ticker": ticker,
        },
    }
