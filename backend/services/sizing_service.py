"""
Sizing Service

Implements the Position Sizing Calculator per strategy_rules.md §4.1.

All calculation rules, validity conditions, rounding, and FX handling are
defined canonically in strategy_rules.md §4.1. This service is the authoritative
backend implementation of those rules. The frontend must not recalculate or
derive any value returned by this service.

Calculation summary:
    RiskAmount      = PortfolioValue × RiskPercent
    StopDistance    = EntryPrice − StopPrice
    RawShares       = RiskAmount / StopDistance
    SuggestedShares = floor(RawShares, 4dp)
    EstimatedCost   = (SuggestedShares × EntryPrice) + EstimatedFees

PortfolioValue is the latest portfolio_history.total_value snapshot.
Available cash (portfolios.cash) is the feasibility gate only — not the risk basis.
"""

import math
from typing import Dict, Optional

from database import get_portfolio, get_latest_snapshot
from utils.pricing import get_live_fx_rate
from utils.calculations import calculate_uk_entry_fees, calculate_us_entry_fees


# ---------------------------------------------------------------------------
# Reason codes — per portfolio_endpoints.md
# ---------------------------------------------------------------------------

INVALID_RISK_PERCENT = "INVALID_RISK_PERCENT"
INVALID_ENTRY_PRICE = "INVALID_ENTRY_PRICE"
INVALID_STOP_PRICE = "INVALID_STOP_PRICE"
INVALID_STOP_DISTANCE = "INVALID_STOP_DISTANCE"
NO_PORTFOLIO_VALUE_SNAPSHOT = "NO_PORTFOLIO_VALUE_SNAPSHOT"

REASON_DETAILS = {
    INVALID_RISK_PERCENT: "risk_percent must be greater than 0",
    INVALID_ENTRY_PRICE: "entry_price must be greater than 0",
    INVALID_STOP_PRICE: "stop_price must be greater than 0",
    INVALID_STOP_DISTANCE: "Stop price must be below entry price",
    NO_PORTFOLIO_VALUE_SNAPSHOT: "No portfolio value snapshot found — run POST /portfolio/snapshot first",
}


def _invalid_response(reason: str) -> Dict:
    """Build a valid: false response with reason code and detail."""
    return {
        "valid": False,
        "reason": reason,
        "reason_detail": REASON_DETAILS[reason],
    }


def _floor_4dp(value: float) -> float:
    """Floor a value to 4 decimal places (conservative rounding per §4.1.3)."""
    return math.floor(value * 10000) / 10000


def size_position(
    entry_price: float,
    stop_price: float,
    risk_percent: float,
    market: str = "UK",
    fx_rate: Optional[float] = None,
) -> Dict:
    """
    Calculate suggested position size per strategy_rules.md §4.1.

    Args:
        entry_price:  Prospective entry price in native currency (USD for US, GBP for UK)
        stop_price:   Intended initial stop price in native currency
        risk_percent: Percentage of portfolio value to risk, e.g. 1.00 for 1%
        market:       "US" or "UK" (default "UK")
        fx_rate:      User-provided FX override for US positions. If None, uses live rate.

    Returns:
        Dict conforming to the PositionSizeResponse schema in portfolio_endpoints.md.
        Always returns HTTP 200 — business rule failures are expressed via valid: false.
    """

    # ------------------------------------------------------------------
    # §4.1.4 Validity rules — check inputs before any calculation
    # ------------------------------------------------------------------
    if risk_percent <= 0:
        return _invalid_response(INVALID_RISK_PERCENT)

    if entry_price <= 0:
        return _invalid_response(INVALID_ENTRY_PRICE)

    if stop_price <= 0:
        return _invalid_response(INVALID_STOP_PRICE)

    if stop_price >= entry_price:
        return _invalid_response(INVALID_STOP_DISTANCE)

    # ------------------------------------------------------------------
    # Fetch portfolio data
    # ------------------------------------------------------------------
    portfolio = get_portfolio()
    if not portfolio:
        return _invalid_response(NO_PORTFOLIO_VALUE_SNAPSHOT)

    portfolio_id = str(portfolio["id"])
    available_cash = float(portfolio["cash"])

    # §4.1.1 PortfolioValue = latest portfolio_history.total_value
    snapshot = get_latest_snapshot(portfolio_id)
    if not snapshot:
        return _invalid_response(NO_PORTFOLIO_VALUE_SNAPSHOT)

    portfolio_value = float(snapshot["total_value"])

    if portfolio_value <= 0:
        return _invalid_response(NO_PORTFOLIO_VALUE_SNAPSHOT)

    # ------------------------------------------------------------------
    # §4.1.5 FX handling
    # ------------------------------------------------------------------
    if market == "US":
        if fx_rate is not None:
            fx_rate_used = float(fx_rate)
        else:
            fx_rate_used = get_live_fx_rate()
    else:
        fx_rate_used = 1.0

    # ------------------------------------------------------------------
    # §4.1.2 Risk basis
    # ------------------------------------------------------------------
    risk_amount = portfolio_value * (risk_percent / 100)

    # ------------------------------------------------------------------
    # §4.1.1 Stop distance (native currency)
    # ------------------------------------------------------------------
    stop_distance = entry_price - stop_price

    # ------------------------------------------------------------------
    # §4.1.3 Share calculation — floor to 4dp (conservative)
    # ------------------------------------------------------------------
    raw_shares = risk_amount / (stop_distance * fx_rate_used)
    suggested_shares = _floor_4dp(raw_shares)

    # ------------------------------------------------------------------
    # Fee estimation
    # ------------------------------------------------------------------
    if market == "US":
        estimated_fees = calculate_us_entry_fees(
            entry_price, suggested_shares, fx_rate_used
        )
    else:
        estimated_fees = calculate_uk_entry_fees(entry_price, suggested_shares)

    # ------------------------------------------------------------------
    # Estimated cost in GBP
    # ------------------------------------------------------------------
    if market == "US":
        estimated_cost = (suggested_shares * entry_price / fx_rate_used) + estimated_fees
    else:
        estimated_cost = (suggested_shares * entry_price) + estimated_fees

    estimated_cost = round(estimated_cost, 2)
    estimated_fees = round(estimated_fees, 2)

    # ------------------------------------------------------------------
    # §4.1.6 Cash constraint (execution feasibility gate)
    # ------------------------------------------------------------------
    cash_sufficient = estimated_cost <= available_cash

    result = {
        "valid": True,
        "suggested_shares": suggested_shares,
        "risk_amount": round(risk_amount, 2),
        "stop_distance": round(stop_distance, 4),
        "estimated_cost": estimated_cost,
        "estimated_fees": estimated_fees,
        "fx_rate_used": round(fx_rate_used, 4),
        "cash_sufficient": cash_sufficient,
        "available_cash": round(available_cash, 2),
    }

    if not cash_sufficient:
        # §4.1.6 — include max_affordable_shares when insufficient cash
        if market == "US":
            # Approximate: net of fees, back-calculate max shares
            max_cost_for_shares = available_cash * 0.995  # conservative: leave ~0.5% for fees
            max_raw = max_cost_for_shares * fx_rate_used / entry_price
        else:
            max_raw = available_cash / entry_price
        result["max_affordable_shares"] = _floor_4dp(max_raw)

    return result
