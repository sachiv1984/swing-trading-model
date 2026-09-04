"""
Pre-Entry Validation Router (SI-01 / ST-02)

Implements GET /portfolio/pre-entry-validation — non-blocking advisory pre-entry rule check.

§13 compliance note: All checks are advisory. No result blocks or prevents trade plan submission.
This panel is decision support only, consistent with strategy_rules.md §3 and §4.1.7.
Decision record: docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md
Spec: docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/pre-entry-validation
"""

from typing import Optional
from fastapi import APIRouter, Query
from database import log_pre_entry_validation_results
from services.concentration_service import get_ticker_sector as _get_ticker_sector

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

_EARNINGS_PROXIMITY_DAYS = 5        # strategy_rules.md §4.2.3
_SECTOR_CONCENTRATION_PCT = 30.0    # strategy_rules.md §4.2.2


def _check_regime(market: str) -> dict:
    """Regime gate per strategy_rules.md §4.2.1 and §8.2."""
    try:
        from position_manager import check_market_regime
        regime = check_market_regime()
        if market.upper() == "UK":
            risk_on = bool(regime.get("ftse_risk_on", False))
            label = "FTSE 100"
        else:
            risk_on = bool(regime.get("spy_risk_on", False))
            label = "SPY"
        direction = "above" if risk_on else "below"
        regime_label = "Risk-On" if risk_on else "Risk-Off"
        return {
            "rule": "regime_gate",
            "status": "pass" if risk_on else "fail",
            "detail": f"{market.upper()} market is {regime_label} ({label} {direction} 200-day MA)",
            "severity": "fail",
        }
    except Exception as exc:
        return {
            "rule": "regime_gate",
            "status": "skipped",
            "detail": f"Regime data unavailable: {exc}",
            "severity": "fail",
        }


def _check_cash_constraint(ticker: str, market: str, quantity: float) -> dict:
    """Cash constraint per strategy_rules.md §4.2.4 and §4.1.6."""
    try:
        from database import get_portfolio
        from utils.pricing import get_current_price, get_live_fx_rate

        portfolio = get_portfolio()
        if not portfolio:
            return {"rule": "cash_constraint", "status": "skipped", "detail": "Portfolio not found", "severity": "fail"}

        available_cash_gbp = float(portfolio["cash"])
        live_price = get_current_price(ticker)
        if live_price is None:
            return {"rule": "cash_constraint", "status": "skipped", "detail": "Live price unavailable", "severity": "fail"}

        if market.upper() == "US":
            fx = get_live_fx_rate()
            price_gbp = live_price / fx if fx and fx > 0 else live_price
        else:
            fx = 1.0
            price_gbp = live_price

        estimated_cost_gbp = round(quantity * price_gbp, 2)
        sufficient = estimated_cost_gbp <= available_cash_gbp

        return {
            "rule": "cash_constraint",
            "status": "pass" if sufficient else "fail",
            "detail": (
                f"Estimated cost £{estimated_cost_gbp:,.2f} within available cash £{available_cash_gbp:,.2f}"
                if sufficient
                else f"Estimated cost £{estimated_cost_gbp:,.2f} exceeds available cash £{available_cash_gbp:,.2f}"
            ),
            "severity": "fail",
            "estimated_cost_gbp": estimated_cost_gbp,
            "available_cash_gbp": available_cash_gbp,
            # ST-03 (EPIC-01, v8.0): §4.1.5 requires the FX rate used be
            # returned for auditability wherever a GBP amount is FX-derived.
            "fx_rate_used": round(fx, 4),
        }
    except Exception as exc:
        return {"rule": "cash_constraint", "status": "skipped", "detail": f"Cash check error: {exc}", "severity": "fail"}


def _check_sector_concentration(ticker: str, market: str, quantity: float) -> dict:
    """Sector concentration per strategy_rules.md §4.2.2."""
    try:
        sector = _get_ticker_sector(ticker)
        if not sector:
            return {
                "rule": "sector_concentration",
                "status": "skipped",
                "detail": "Sector data unavailable for this ticker",
                "severity": "warn",
            }

        from database import get_portfolio, get_positions
        from utils.pricing import get_current_price, get_live_fx_rate
        from utils.formatting import decimal_to_float

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

        new_value_gbp = quantity * live_price / fx if market.upper() == "US" else quantity * live_price
        total_portfolio_value = cash + total_pos_value
        if total_portfolio_value <= 0:
            return {"rule": "sector_concentration", "status": "skipped", "detail": "Portfolio value is zero", "severity": "warn"}

        projected_pct = round((current_sector_value + new_value_gbp) / total_portfolio_value * 100, 2)
        within_limit = projected_pct < _SECTOR_CONCENTRATION_PCT

        return {
            "rule": "sector_concentration",
            "status": "pass" if within_limit else "warn",
            "detail": (
                f"Projected {sector} sector allocation {projected_pct}% within {_SECTOR_CONCENTRATION_PCT}% advisory limit"
                if within_limit
                else f"Projected {sector} sector allocation {projected_pct}% would exceed {_SECTOR_CONCENTRATION_PCT}% advisory limit"
            ),
            "severity": "warn",
            "sector": sector,
            "projected_sector_pct": projected_pct,
            "threshold_pct": _SECTOR_CONCENTRATION_PCT,
        }
    except Exception as exc:
        return {"rule": "sector_concentration", "status": "skipped", "detail": f"Sector check error: {exc}", "severity": "warn"}


def _check_earnings_proximity(ticker: str, market: str) -> dict:
    """Earnings proximity per strategy_rules.md §4.2.3. US tickers only."""
    if market.upper() != "US":
        return {
            "rule": "earnings_proximity",
            "status": "skipped",
            "detail": "Earnings proximity check applies to US tickers only",
            "severity": "warn",
        }
    try:
        from services.earnings_service import get_earnings
        result = get_earnings(ticker, market)
        days_until = result.get("days_until_earnings")
        earnings_date = result.get("next_earnings_date")

        if days_until is None or earnings_date is None:
            return {"rule": "earnings_proximity", "status": "skipped", "detail": "Earnings date not available", "severity": "warn"}

        within_window = 0 <= days_until <= _EARNINGS_PROXIMITY_DAYS
        return {
            "rule": "earnings_proximity",
            "status": "warn" if within_window else "pass",
            "detail": (
                f"Earnings in {days_until} day(s) ({earnings_date}) — elevated gap risk within {_EARNINGS_PROXIMITY_DAYS}-day window"
                if within_window
                else f"Next earnings {earnings_date} ({days_until} days) — outside {_EARNINGS_PROXIMITY_DAYS}-day proximity window"
            ),
            "severity": "warn",
            "earnings_date": earnings_date,
            "days_until_earnings": days_until,
        }
    except Exception as exc:
        return {"rule": "earnings_proximity", "status": "skipped", "detail": f"Earnings data error: {exc}", "severity": "warn"}


def _check_sizing_validity(entry_price: Optional[float], stop_price: Optional[float]) -> dict:
    """Position sizing validity per strategy_rules.md §4.2.5 and §4.1.4."""
    if entry_price is None or stop_price is None:
        return {
            "rule": "sizing_validity",
            "status": "skipped",
            "detail": "Provide entry_price and stop_price query params for sizing validity check",
            "severity": "fail",
        }
    if entry_price <= 0 or stop_price <= 0:
        return {
            "rule": "sizing_validity",
            "status": "fail",
            "detail": "Entry price and stop price must each be greater than zero (strategy_rules.md §4.1.4)",
            "severity": "fail",
        }
    stop_distance = round(entry_price - stop_price, 6)
    if stop_distance <= 0:
        return {
            "rule": "sizing_validity",
            "status": "fail",
            "detail": f"Stop distance ≤ 0 — stop {stop_price} ≥ entry {entry_price} is invalid (§4.1.4)",
            "severity": "fail",
            "stop_distance": stop_distance,
        }
    return {
        "rule": "sizing_validity",
        "status": "pass",
        "detail": f"Stop distance {stop_distance} is valid (entry {entry_price}, stop {stop_price})",
        "severity": "fail",
        "stop_distance": stop_distance,
    }


def _aggregate_advisory_status(checks: list) -> str:
    """Aggregate check results: fail > warn > pass. Skipped checks are excluded."""
    active = [c for c in checks if c["status"] != "skipped"]
    if any(c["status"] == "fail" for c in active):
        return "fail"
    if any(c["status"] == "warn" for c in active):
        return "warn"
    return "pass"


@router.get("/pre-entry-validation")
def get_pre_entry_validation(
    ticker: str = Query(..., description="Ticker symbol"),
    quantity: float = Query(..., description="Proposed number of shares"),
    market: str = Query(default="US", description="Market: US or UK"),
    entry_price: Optional[float] = Query(default=None, description="Optional entry price — enables sizing validity check (§4.1.4)"),
    stop_price: Optional[float] = Query(default=None, description="Optional stop price — enables sizing validity check (§4.1.4)"),
):
    """
    GET /portfolio/pre-entry-validation — advisory pre-entry rule check (SI-01).

    Returns per-rule advisory results for 5 strategy checks. Non-blocking:
    no result prevents trade plan submission. Override acknowledgement is
    metadata only and has no effect on any calculation.

    §13 compliance: decision support only — not a submission gate.
    strategy_rules.md §4.2 | decision record: SI-01-section13-review.md
    """
    checks = [
        _check_regime(market),
        _check_cash_constraint(ticker, market, quantity),
        _check_sector_concentration(ticker, market, quantity),
        _check_earnings_proximity(ticker, market),
        _check_sizing_validity(entry_price, stop_price),
    ]

    advisory_status = _aggregate_advisory_status(checks)

    log_pre_entry_validation_results(ticker, market, checks)

    return {
        "status": "ok",
        "data": {
            "ticker": ticker,
            "market": market.upper(),
            "quantity": quantity,
            "advisory_status": advisory_status,
            "override_required": advisory_status in ("fail", "warn"),
            "checks": checks,
        },
    }
