"""
Compliance Recheck Service — ST-01 (BLG-FEAT-64, v6.9)

Re-applies the 5 existing SI-01 pre-entry deterministic rule checks against an
open position's *current* state (current regime, current signal conditions,
current heat/sizing) rather than its entry-time snapshot. This is a manual,
on-demand, single-position check — it does not replace or duplicate SI-02
(drift detection), which remains a separate gated capability.

Reuses the check functions already implemented for GET /portfolio/pre-entry-validation
(routers/pre_entry_validation.py) — pure re-application of the existing deterministic
rule set, no new statistical model or scoring (per stage4_backlog_slice.md ST-01).

Sector concentration adaptation: the original _check_sector_concentration is designed
to assess a *prospective new* position (adds its value on top of all currently open
positions). Reusing it verbatim for an *already-open* position would double-count that
position's value — once via its stored entry-time value in the open-positions loop,
once via the live-priced "new position" contribution — systematically overstating
concentration for every rechecked position. _check_sector_concentration_recheck below
excludes the position being rechecked from the baseline sum and adds back its own
live-priced value, so the same deterministic formula is applied without double-counting.

§13 compliance: display-only re-application of existing deterministic rules; no new
automation/prediction surface (AC-04, Strategy Rules & System Intent Owner sign-off).
Spec: docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/compliance-recheck
      docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md
"""
from typing import Dict, List, Optional

from utils.formatting import decimal_to_float
from routers.pre_entry_validation import (
    _check_regime,
    _check_cash_constraint,
    _check_earnings_proximity,
    _check_sizing_validity,
    _get_ticker_sector,
    _SECTOR_CONCENTRATION_PCT,
)


def _check_sector_concentration_recheck(position_id: str, ticker: str, market: str, quantity: float) -> Dict:
    """Sector concentration recheck per strategy_rules.md §4.2.2 — see module docstring
    for why this excludes the rechecked position from the baseline sum.

    Imports database/pricing helpers locally (matching the pattern already used by
    routers/pre_entry_validation.py's own _check_* functions) so callers can patch
    them at their canonical module path rather than this module's import site.
    """
    from database import get_portfolio, get_positions
    from utils.pricing import get_current_price, get_live_fx_rate

    try:
        sector = _get_ticker_sector(ticker)
        if not sector:
            return {
                "rule": "sector_concentration",
                "status": "skipped",
                "detail": "Sector data unavailable for this ticker",
                "severity": "warn",
            }

        portfolio = get_portfolio()
        if not portfolio:
            return {"rule": "sector_concentration", "status": "skipped", "detail": "Portfolio not found", "severity": "warn"}

        cash = float(portfolio["cash"])
        positions = get_positions(str(portfolio["id"]), status="open")
        live_fx_rate = get_live_fx_rate()
        fx = float(live_fx_rate) if live_fx_rate and live_fx_rate > 0 else 1.27

        total_pos_value = 0.0
        current_sector_value = 0.0

        for pos in positions:
            pos = decimal_to_float(dict(pos))
            if str(pos.get("id")) == str(position_id):
                continue  # exclude self — added back below at live price
            shares = float(pos.get("shares", 0))
            price = float(pos.get("current_price") or pos.get("entry_price") or 0)
            pos_market = pos.get("market", "UK")
            value_gbp = price * shares / fx if pos_market == "US" else price * shares
            total_pos_value += value_gbp
            if pos.get("sector") and pos["sector"].lower() == sector.lower():
                current_sector_value += value_gbp

        live_price = get_current_price(ticker)
        if live_price is None:
            return {
                "rule": "sector_concentration",
                "status": "skipped",
                "detail": "Live price unavailable for concentration estimate",
                "severity": "warn",
            }

        self_value_gbp = quantity * live_price / fx if market.upper() == "US" else quantity * live_price
        total_pos_value += self_value_gbp
        total_portfolio_value = cash + total_pos_value
        if total_portfolio_value <= 0:
            return {"rule": "sector_concentration", "status": "skipped", "detail": "Portfolio value is zero", "severity": "warn"}

        current_pct = round((current_sector_value + self_value_gbp) / total_portfolio_value * 100, 2)
        within_limit = current_pct < _SECTOR_CONCENTRATION_PCT

        return {
            "rule": "sector_concentration",
            "status": "pass" if within_limit else "warn",
            "detail": (
                f"Current {sector} sector allocation {current_pct}% within {_SECTOR_CONCENTRATION_PCT}% advisory limit"
                if within_limit
                else f"Current {sector} sector allocation {current_pct}% exceeds {_SECTOR_CONCENTRATION_PCT}% advisory limit"
            ),
            "severity": "warn",
            "sector": sector,
            "projected_sector_pct": current_pct,
            "threshold_pct": _SECTOR_CONCENTRATION_PCT,
        }
    except Exception as exc:
        return {"rule": "sector_concentration", "status": "skipped", "detail": f"Sector check error: {exc}", "severity": "warn"}


def _aggregate_overall_status(checks: List[Dict]) -> str:
    """fail > warn > pass. Skipped checks excluded — mirrors pre-entry aggregation."""
    active = [c for c in checks if c["status"] != "skipped"]
    if any(c["status"] == "fail" for c in active):
        return "fail"
    if any(c["status"] == "warn" for c in active):
        return "warn"
    return "pass"


def get_compliance_recheck(position_id: str) -> Optional[Dict]:
    """
    Re-run the 5 SI-01 checks against an open position's current state.

    Returns None if the position does not exist or is not open (caller maps to 404).

    Response shape (docs/specs/api_contracts/position_endpoints.md):
      { "overall_status": "pass"|"warn"|"fail", "checks": [{ "rule_key", "status", "detail" }] }
    """
    from database import get_position_by_id

    raw = get_position_by_id(position_id)
    if not raw:
        return None
    pos = decimal_to_float(dict(raw))
    if pos.get("status") != "open":
        return None

    ticker = pos["ticker"]
    market = pos["market"]
    quantity = float(pos.get("shares") or 0)
    entry_price = float(pos.get("entry_price") or 0) or None
    # Current effective stop (trailing stop if set, else the entry-time initial stop) —
    # reflects the position's current risk state rather than the entry-time snapshot (AC-01).
    current_stop = pos.get("current_stop") or pos.get("initial_stop")
    stop_price = float(current_stop) if current_stop else None

    raw_checks = [
        _check_regime(market),
        _check_cash_constraint(ticker, market, quantity),
        _check_sector_concentration_recheck(position_id, ticker, market, quantity),
        _check_earnings_proximity(ticker, market),
        _check_sizing_validity(entry_price, stop_price),
    ]

    checks = [
        {"rule_key": c["rule"], "status": c["status"], "detail": c["detail"]}
        for c in raw_checks
    ]

    return {
        "overall_status": _aggregate_overall_status(raw_checks),
        "checks": checks,
    }
