"""
ST-12 (BLG-QA-186, EPIC-03, v9.9): property-based tests for two universal
strategy invariants. The existing example-based tests only cover hand-picked
cases.

1. strategy_rules.md §7.3 (hard constraint): stops never move downwards --
   `UpdatedStop = max(CurrentStop, NewlyCalculatedStop)`. Checked against
   utils.calculations.calculate_trailing_stop, the function both the live
   per-position stop update and the nightly update call
   (services/position_service.py). Checked for a single step and over a
   generated multi-day price/ATR path.

2. strategy_rules.md §4.1.4 (validity rules): checked against
   services.sizing_service.size_position, the canonical §4.1 implementation.
   - Any input breaching a §4.1.4 rule returns valid: false with the
     deterministic reason code, and never reaches the portfolio lookup.
   - Any input satisfying them (with a positive portfolio-value snapshot)
     returns valid: true, with non-negative 4dp-floored shares that never
     risk more than RiskAmount (§4.1.3 conservative rounding).

A deliberately broken ratchet (no max() against the current stop) is run
through the same property and must be falsified -- proving the property
can actually catch a regression, not just pass.
"""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from utils.calculations import calculate_trailing_stop  # noqa: E402
from services import sizing_service  # noqa: E402

PROPERTY_SETTINGS = settings(max_examples=300, deadline=None, suppress_health_check=[HealthCheck.too_slow])

prices = st.floats(min_value=0.01, max_value=100_000, allow_nan=False, allow_infinity=False)
atrs = st.floats(min_value=0.0, max_value=10_000, allow_nan=False, allow_infinity=False)
multipliers = st.floats(min_value=0.5, max_value=10, allow_nan=False, allow_infinity=False)


def _settings(trailing, initial):
    return {"atr_multiplier_trailing": trailing, "atr_multiplier_initial": initial}


# ---------------------------------------------------------------------------
# §7.3 -- stops never decrease
# ---------------------------------------------------------------------------

def _broken_trailing_stop(current_price, atr, is_profitable, current_stop, entry_price, settings_):
    """Regression stand-in: recomputes the stop from scratch with no ratchet
    against the current stop -- exactly the §7.3 breach the property guards."""
    key = "atr_multiplier_trailing" if is_profitable else "atr_multiplier_initial"
    mult = float(settings_[key])
    return current_price - mult * atr, "broken", mult


def _single_step_ratchet_property(fn):
    @PROPERTY_SETTINGS
    @given(
        current_price=prices, atr=atrs, is_profitable=st.booleans(), current_stop=prices,
        entry_price=prices, trailing=multipliers, initial=multipliers,
    )
    def check(current_price, atr, is_profitable, current_stop, entry_price, trailing, initial):
        new_stop, _, _ = fn(current_price, atr, is_profitable, current_stop, entry_price, _settings(trailing, initial))
        assert new_stop >= current_stop, (
            f"§7.3 breached: stop moved down from {current_stop} to {new_stop}"
        )

    return check


def test_stop_never_decreases_single_step():
    _single_step_ratchet_property(calculate_trailing_stop)()


@PROPERTY_SETTINGS
@given(
    entry_price=prices,
    initial_stop_fraction=st.floats(min_value=0.01, max_value=0.99),
    path=st.lists(st.tuples(prices, atrs), min_size=1, max_size=40),
    trailing=multipliers,
    initial=multipliers,
)
def test_stop_is_monotonic_over_a_price_path(entry_price, initial_stop_fraction, path, trailing, initial):
    """Feed each day's output back in as the next day's current stop, the way
    the nightly update does: the stop series must be non-decreasing."""
    stop = entry_price * initial_stop_fraction
    history = [stop]
    for price, atr in path:
        stop, _, _ = calculate_trailing_stop(price, atr, price > entry_price, stop, entry_price, _settings(trailing, initial))
        history.append(stop)
    assert all(b >= a for a, b in zip(history, history[1:])), f"stop series decreased: {history}"


@PROPERTY_SETTINGS
@given(current_price=prices, atr=atrs, current_stop=prices, entry_price=prices, trailing=multipliers, initial=multipliers)
def test_profitable_stop_never_below_entry(current_price, atr, current_stop, entry_price, trailing, initial):
    """Companion invariant in the same function: a profitable position's stop
    is floored at entry (protect gains)."""
    new_stop, _, _ = calculate_trailing_stop(current_price, atr, True, current_stop, entry_price, _settings(trailing, initial))
    assert new_stop >= entry_price


def test_deliberately_broken_ratchet_is_falsified():
    """AC-02: the same property must reject an implementation without the
    max(current_stop, ...) ratchet."""
    with pytest.raises(AssertionError, match="§7.3 breached"):
        _single_step_ratchet_property(_broken_trailing_stop)()


# ---------------------------------------------------------------------------
# §4.1.4 -- sizing validity rules
# ---------------------------------------------------------------------------

nonpositive = st.one_of(st.just(0.0), st.floats(max_value=0, allow_nan=False, allow_infinity=False))
positive_price = st.floats(min_value=0.01, max_value=100_000, allow_nan=False, allow_infinity=False)
positive_risk = st.floats(min_value=0.01, max_value=100, allow_nan=False, allow_infinity=False)


def _expected_reason(risk_percent, entry_price, stop_price):
    """§4.1.4's rules, in size_position's documented check order."""
    if risk_percent <= 0:
        return sizing_service.INVALID_RISK_PERCENT
    if entry_price <= 0:
        return sizing_service.INVALID_ENTRY_PRICE
    if stop_price <= 0:
        return sizing_service.INVALID_STOP_PRICE
    if stop_price >= entry_price:
        return sizing_service.INVALID_STOP_DISTANCE
    return None


@PROPERTY_SETTINGS
@given(
    risk_percent=st.one_of(nonpositive, positive_risk),
    entry_price=st.one_of(nonpositive, positive_price),
    stop_price=st.one_of(nonpositive, positive_price),
)
def test_invalid_inputs_always_rejected_with_deterministic_reason(risk_percent, entry_price, stop_price):
    expected = _expected_reason(risk_percent, entry_price, stop_price)
    assume(expected is not None)
    with patch.object(sizing_service, "get_portfolio") as get_portfolio:
        result = sizing_service.size_position(entry_price=entry_price, stop_price=stop_price, risk_percent=risk_percent)
        # Rejected before any portfolio lookup -- suggested shares never computed.
        get_portfolio.assert_not_called()
    assert result["valid"] is False
    assert result["reason"] == expected
    assert result["reason_detail"] == sizing_service.REASON_DETAILS[expected]
    assert "suggested_shares" not in result


@PROPERTY_SETTINGS
@given(
    entry_price=positive_price,
    stop_fraction=st.floats(min_value=0.01, max_value=0.999),
    risk_percent=positive_risk,
    portfolio_value=st.floats(min_value=1, max_value=10_000_000, allow_nan=False, allow_infinity=False),
    market=st.sampled_from(["UK", "US"]),
    fx_rate=st.floats(min_value=0.5, max_value=2.0),
)
def test_valid_inputs_produce_valid_conservative_size(entry_price, stop_fraction, risk_percent, portfolio_value, market, fx_rate):
    stop_price = entry_price * stop_fraction
    assume(0 < stop_price < entry_price)
    with patch.object(sizing_service, "get_portfolio", return_value={"id": "p1", "cash": 1_000_000.0}), \
         patch.object(sizing_service, "get_latest_snapshot", return_value={"total_value": portfolio_value}), \
         patch.object(sizing_service, "get_settings", return_value=[{}]), \
         patch.object(sizing_service, "_calculate_heat_impact", return_value=None):
        result = sizing_service.size_position(
            entry_price=entry_price, stop_price=stop_price, risk_percent=risk_percent,
            market=market, fx_rate=fx_rate if market == "US" else None,
        )
    assert result["valid"] is True
    shares = result["suggested_shares"]
    assert shares >= 0
    # At most 4 decimal places. round() is exact here: floor-to-4dp yields the
    # float nearest k/10000, which round(.., 4) maps back to itself
    # (a `* 10000` comparison is not -- 0.0006 * 10000 == 5.999...).
    assert round(shares, 4) == shares, f"shares {shares} has more than 4dp"
    fx_used = fx_rate if market == "US" else 1.0
    risk_amount = portfolio_value * risk_percent / 100
    risked = shares * (entry_price - stop_price) * fx_used
    assert risked <= risk_amount * (1 + 1e-9), f"risks {risked} > RiskAmount {risk_amount}"


@PROPERTY_SETTINGS
@given(snapshot_value=st.one_of(st.none(), nonpositive))
def test_missing_or_nonpositive_portfolio_value_is_invalid(snapshot_value):
    snapshot = None if snapshot_value is None else {"total_value": snapshot_value}
    with patch.object(sizing_service, "get_portfolio", return_value={"id": "p1", "cash": 1000.0}), \
         patch.object(sizing_service, "get_latest_snapshot", return_value=snapshot):
        result = sizing_service.size_position(entry_price=100.0, stop_price=90.0, risk_percent=1.0)
    assert result["valid"] is False
    assert result["reason"] == sizing_service.NO_PORTFOLIO_VALUE_SNAPSHOT
