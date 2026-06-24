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

from database import get_portfolio, get_latest_snapshot, get_settings
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
    # Fee estimation — uses settings for commission/rate values
    # ------------------------------------------------------------------
    settings_list = get_settings()
    settings = settings_list[0] if settings_list else {}

    gross_cost_native = suggested_shares * entry_price

    if market == "US":
        fee_breakdown = calculate_us_entry_fees(gross_cost_native, settings)
    else:
        fee_breakdown = calculate_uk_entry_fees(gross_cost_native, settings)

    estimated_fees_native = fee_breakdown["total"]

    # ------------------------------------------------------------------
    # Estimated cost in GBP
    # ------------------------------------------------------------------
    if market == "US":
        estimated_cost = (gross_cost_native + estimated_fees_native) / fx_rate_used
        estimated_fees = round(estimated_fees_native / fx_rate_used, 2)
    else:
        estimated_cost = gross_cost_native + estimated_fees_native
        estimated_fees = round(estimated_fees_native, 2)

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
        # Conservative: deduct estimated fee rate from available cash before dividing
        if market == "US":
            fx_fee_rate = float(settings.get("fx_fee_rate", 0.0015))
            effective_price_gbp = entry_price * (1 + fx_fee_rate) / fx_rate_used
        else:
            stamp_duty_rate = float(settings.get("stamp_duty_rate", 0.005))
            commission = float(settings.get("uk_commission", 9.95))
            # Back out commission from available cash first, then apply stamp duty
            spendable = max(0.0, available_cash - commission)
            effective_price_gbp = entry_price * (1 + stamp_duty_rate)

        if market == "US":
            max_raw = available_cash / effective_price_gbp
        else:
            max_raw = spendable / effective_price_gbp

        result["max_affordable_shares"] = _floor_4dp(max_raw)

    return result


# ---------------------------------------------------------------------------
# ST-04 (BLG-FEAT-48) — Inverse-volatility batch sizing
# ---------------------------------------------------------------------------
# Production strategy parameters (must match production_strategy.py OPTIMAL_PARAMS):
_INV_VOL_MIN_WEIGHT = 0.05   # 5% of available cash minimum allocation
_INV_VOL_MAX_WEIGHT = 0.20   # 20% of available cash maximum allocation


def size_batch_inv_vol(signals: list, available_cash: float, fx_rate: float = 1.0) -> list:
    """
    Compute inverse-volatility position sizes for a batch of momentum signals.

    Algorithm (production_strategy.py OPTIMAL_PARAMS):
      1. weight_i = (1 / ATR_i) / sum(1 / ATR_j)   for all signals with ATR > 0
      2. Cap each weight to [_INV_VOL_MIN_WEIGHT, _INV_VOL_MAX_WEIGHT]
      3. Re-normalise capped weights so they sum to 1.0
      4. allocation_gbp_i = available_cash * normalised_weight_i
      5. suggested_shares_i = floor(allocation_gbp_i / price_gbp_i)  (whole shares)

    Args:
        signals:        List of signal dicts, each with 'atr_value', 'price_gbp',
                        'current_price', and 'market' fields (from generate_momentum_signals).
        available_cash: Portfolio cash available for allocation (GBP).
        fx_rate:        Live GBP/USD rate; used only for fee estimation on US stocks.

    Returns:
        Same list of signals with 'suggested_shares', 'allocation_gbp', 'total_cost'
        and 'inv_vol_weight' populated in-place. Signals with atr_value == 0 get 0 shares.

    AC-04 / RISK-03: This function is only called for signal-driven batch entries.
    Manual sizing (size_position()) is untouched.
    """
    # Step 1 — inverse-ATR weights
    inv_atrs = []
    for sig in signals:
        atr = sig.get('atr_value', 0) or 0
        inv_atrs.append(1.0 / atr if atr > 0 else 0.0)

    total_inv_atr = sum(inv_atrs)
    if total_inv_atr == 0:
        for sig in signals:
            sig['suggested_shares'] = 0
            sig['allocation_gbp'] = 0
            sig['total_cost'] = 0
            sig['inv_vol_weight'] = 0
            sig['reason'] = 'Inv-vol sizing: no valid ATR values'
        return signals

    raw_weights = [v / total_inv_atr for v in inv_atrs]

    # Step 2 — cap to [min, max]
    capped = [max(_INV_VOL_MIN_WEIGHT, min(_INV_VOL_MAX_WEIGHT, w)) for w in raw_weights]

    # Step 3 — re-normalise so sum == 1.0
    cap_total = sum(capped)
    normalised = [w / cap_total for w in capped]

    # Step 4 & 5 — allocate and compute shares
    settings_list = get_settings()
    settings = settings_list[0] if settings_list else {}

    for sig, weight in zip(signals, normalised):
        allocation_gbp = available_cash * weight
        price_gbp = sig.get('price_gbp', 0) or 0

        if price_gbp <= 0:
            sig['suggested_shares'] = 0
            sig['allocation_gbp'] = 0
            sig['total_cost'] = 0
            sig['inv_vol_weight'] = round(weight, 6)
            sig['reason'] = 'Inv-vol sizing: price_gbp unavailable'
            continue

        # Whole shares only (consistent with signal_endpoints.md data model note)
        raw_shares = allocation_gbp / price_gbp
        whole_shares = int(math.floor(raw_shares))

        # Fee estimation
        gross_cost = whole_shares * (sig.get('current_price', price_gbp))
        if sig.get('market') == 'US':
            fee = calculate_us_entry_fees(gross_cost, settings).get('total_fee', 0)
        else:
            fee = calculate_uk_entry_fees(gross_cost, settings).get('total_fee', 0)

        total_cost = round(gross_cost + fee, 2) if whole_shares > 0 else 0

        sig['suggested_shares'] = whole_shares
        sig['allocation_gbp'] = round(allocation_gbp, 2)
        sig['total_cost'] = total_cost
        sig['inv_vol_weight'] = round(weight, 6)
        sig['reason'] = (
            None if whole_shares > 0
            else 'Inv-vol sizing yielded 0 shares for this allocation'
        )

    return signals
