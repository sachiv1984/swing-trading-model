"""
Compliance Service — ST-01 (BLG-FEAT-11, v2.3)

Computes per-position ATR-based strategy compliance flags for open positions.

Rules:
  Stop Compliance:  stop_distance / atr <= ATR_STOP_THRESHOLD (2.5)
                    Grace-period positions have no active stop — not assessed.
  Stop Age:         Days since stop was last set. Approximated as holding_days
                    because the positions table has no stop_updated_at column.
  Size Compliance:  Actual risk-amount (stop_distance × shares, in GBP) <=
                    (portfolio_value × risk_percent / 100) × SIZE_TOLERANCE

Spec: docs/specs/frontend/pages/positions.md §Strategy Compliance Panel
      docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md
Constraint §13.3: Display-only. No automated notification, alert, or action.
"""

from typing import Dict, List, Optional

from database import get_portfolio, get_positions, get_settings, get_latest_snapshot
from utils.formatting import decimal_to_float

# ---------------------------------------------------------------------------
# Compliance thresholds
# ---------------------------------------------------------------------------
# Maximum stop-distance / ATR ratio for a stop to be considered compliant.
# A stop set at 2 ATR from entry is the canonical strategy rule.
# 2.5 allows reasonable trailing without flagging every trailed stop.
ATR_STOP_THRESHOLD = 2.5

# Tolerance multiplier for size compliance.
# A position is compliant if actual_risk_gbp <= recommended_risk_gbp × 1.10.
SIZE_TOLERANCE = 1.10

# Default risk percent if settings row is absent or field is null.
DEFAULT_RISK_PERCENT = 1.0

# Grace period length in days (must match grace_service.py / strategy rules).
GRACE_PERIOD_DAYS = 10


def _compute_stop_compliance(
    entry_price: float,
    current_stop: float,
    initial_stop: float,
    atr: float,
    in_grace: bool,
) -> Optional[bool]:
    """
    Returns True (compliant), False (non-compliant), or None (cannot assess).

    During grace period the stop is not active — returns None rather than
    flagging the position as non-compliant before a stop is required.
    """
    if in_grace:
        return None

    effective_stop = current_stop if current_stop and current_stop > 0 else initial_stop
    if not effective_stop or effective_stop <= 0:
        return False  # No stop set after grace period → non-compliant

    if not atr or atr <= 0:
        return None  # ATR not available — cannot assess

    stop_distance = entry_price - effective_stop
    if stop_distance <= 0:
        return False  # Stop above entry price — invalid

    return (stop_distance / atr) <= ATR_STOP_THRESHOLD


def _compute_stop_age(holding_days: int, in_grace: bool) -> Optional[int]:
    """
    Returns the approximate age of the stop in days, or None if in grace period.

    Approximation: we use holding_days as the conservative (worst-case) estimate
    because the positions table does not record a stop_updated_at timestamp.
    """
    if in_grace:
        return None
    return holding_days


def _compute_size_compliance(
    entry_price: float,
    stop_price: float,
    shares: float,
    market: str,
    fx_rate: float,
    portfolio_value_gbp: Optional[float],
    risk_percent: float,
) -> Optional[bool]:
    """
    Returns True (compliant), False (non-compliant), or None (cannot assess).

    Assesses whether the position's initial risk amount is within the
    strategy's allowed risk per trade.
    """
    if portfolio_value_gbp is None or portfolio_value_gbp <= 0:
        return None

    effective_stop = stop_price if stop_price and stop_price > 0 else None
    if effective_stop is None:
        return None

    stop_distance_native = entry_price - effective_stop
    if stop_distance_native <= 0:
        return None

    # Convert risk amount to GBP
    if market == "US":
        fx = fx_rate if fx_rate and fx_rate > 0 else 1.27
        actual_risk_gbp = (stop_distance_native * shares) / fx
    else:
        actual_risk_gbp = stop_distance_native * shares

    recommended_risk_gbp = portfolio_value_gbp * (risk_percent / 100.0)
    return actual_risk_gbp <= recommended_risk_gbp * SIZE_TOLERANCE


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_position_compliance() -> Dict:
    """
    Compute strategy compliance flags for all open positions.

    Returns a dict conforming to GET /positions/compliance response schema:
    {
      "overall_status": "Compliant" | "Needs Attention" | "Review Required",
      "compliant_count": int,
      "total_count": int,
      "positions": [
        {
          "position_id": str,
          "ticker": str,
          "market": str,
          "stop_compliant": bool | null,
          "stop_age_days": int | null,
          "size_compliant": bool | null
        }
      ]
    }
    """
    portfolio = get_portfolio()
    if not portfolio:
        raise ValueError("Portfolio not found")

    portfolio_id = str(portfolio["id"])
    raw_positions = get_positions(portfolio_id, status="open")

    if not raw_positions:
        return {
            "overall_status": "Compliant",
            "compliant_count": 0,
            "total_count": 0,
            "positions": [],
        }

    # Fetch portfolio value for size compliance
    snapshot = get_latest_snapshot(portfolio_id)
    portfolio_value_gbp: Optional[float] = None
    if snapshot:
        snap = decimal_to_float(snapshot)
        portfolio_value_gbp = snap.get("total_value")

    # Fetch risk_percent from settings
    risk_percent = DEFAULT_RISK_PERCENT
    settings_rows = get_settings()
    if settings_rows:
        s = decimal_to_float(dict(settings_rows[0]))
        rp = s.get("default_risk_percent")
        if rp and rp > 0:
            risk_percent = float(rp)

    results: List[Dict] = []
    for pos in raw_positions:
        pos = decimal_to_float(pos)

        holding_days = int(pos.get("holding_days") or 0)
        in_grace = holding_days < GRACE_PERIOD_DAYS

        entry_price = float(pos.get("entry_price") or 0)
        current_stop = float(pos.get("current_stop") or 0)
        initial_stop = float(pos.get("initial_stop") or 0)
        atr = float(pos.get("atr") or 0)
        shares = float(pos.get("shares") or 0)
        market = pos.get("market", "UK")
        fx_rate = float(pos.get("fx_rate") or 1.27)

        ticker_raw = pos.get("ticker", "")
        display_ticker = ticker_raw.replace(".L", "") if market == "UK" else ticker_raw

        stop_compliant = _compute_stop_compliance(
            entry_price=entry_price,
            current_stop=current_stop,
            initial_stop=initial_stop,
            atr=atr,
            in_grace=in_grace,
        )
        stop_age_days = _compute_stop_age(holding_days, in_grace)

        # Use initial_stop for size compliance (entry-time risk assessment)
        effective_entry_stop = initial_stop if initial_stop > 0 else current_stop
        size_compliant = _compute_size_compliance(
            entry_price=entry_price,
            stop_price=effective_entry_stop,
            shares=shares,
            market=market,
            fx_rate=fx_rate,
            portfolio_value_gbp=portfolio_value_gbp,
            risk_percent=risk_percent,
        )

        results.append({
            "position_id": str(pos.get("id", "")),
            "ticker": display_ticker,
            "market": market,
            "stop_compliant": stop_compliant,
            "stop_age_days": stop_age_days,
            "size_compliant": size_compliant,
        })

    # Tally compliance
    total = len(results)
    # A position is "fully compliant" if all assessable flags are True
    def is_fully_compliant(p: Dict) -> bool:
        flags = [p["stop_compliant"], p["size_compliant"]]
        assessable = [f for f in flags if f is not None]
        return all(assessable) if assessable else True

    compliant_count = sum(1 for p in results if is_fully_compliant(p))
    non_compliant_count = total - compliant_count

    if non_compliant_count == 0:
        overall_status = "Compliant"
    elif non_compliant_count / total < 0.5:
        overall_status = "Needs Attention"
    else:
        overall_status = "Review Required"

    return {
        "overall_status": overall_status,
        "compliant_count": compliant_count,
        "total_count": total,
        "positions": results,
    }
