"""
Nightly Computation CI Simulation Tests
ST-07 (BLG-QA-65, EPIC-02, v6.3)

Tests three nightly computation services:
  - calculate_trailing_stop()     — utils/calculations.py
  - _is_last_trading_day_of_month() / generate_rebalance_exit_signals()
                                  — services/signal_service.py
  - size_batch_inv_vol()          — services/sizing_service.py

Scenario coverage defined in docs/specs/qa/strategy_signal_regression_spec.md v1.0.
Fixture data: tests/fixtures/nightly_portfolio_state.json (spec_version: 1.0).
"""

import json
import math
import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Fixture loader
# ---------------------------------------------------------------------------

_FIXTURE_PATH = Path(__file__).parent / "fixtures" / "nightly_portfolio_state.json"


@pytest.fixture(scope="module")
def fixture_data():
    with open(_FIXTURE_PATH) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _approx(val, expected, rel_tol=1e-6):
    """Return True when val is within rel_tol of expected (handles zero)."""
    return math.isclose(val, expected, rel_tol=rel_tol, abs_tol=1e-9)


# ===========================================================================
# Trailing Stop Computation Tests (TS-01 … TS-07)
# ===========================================================================

from utils.calculations import calculate_trailing_stop


@pytest.fixture(scope="module")
def ts_settings(fixture_data):
    return fixture_data["settings"]


def test_TS01_profitable_stop_trails_up(fixture_data, ts_settings):
    """TS-01: Profitable position — stop ratchets upward when price moves up."""
    s = fixture_data["trailing_stop_scenarios"]["TS-01_profitable_stop_trails_up"]
    stop, reason, mult = calculate_trailing_stop(
        current_price=s["current_price"],
        atr=s["atr"],
        is_profitable=s["is_profitable"],
        current_stop=s["current_stop"],
        entry_price=s["entry_price"],
        settings=ts_settings,
    )
    assert _approx(stop, s["expected_stop"]), f"Expected {s['expected_stop']}, got {stop}"
    assert _approx(mult, s["expected_atr_mult"])
    assert stop >= s["current_stop"], "Stop must not decrease (ratchet invariant)"
    assert stop >= s["entry_price"], "Profitable stop must not go below entry"


def test_TS02_profitable_stop_does_not_decrease(fixture_data, ts_settings):
    """TS-02: Profitable — new computed stop below current_stop → stop unchanged."""
    s = fixture_data["trailing_stop_scenarios"]["TS-02_profitable_stop_unchanged"]
    stop, _, _ = calculate_trailing_stop(
        current_price=s["current_price"],
        atr=s["atr"],
        is_profitable=s["is_profitable"],
        current_stop=s["current_stop"],
        entry_price=s["entry_price"],
        settings=ts_settings,
    )
    assert _approx(stop, s["expected_stop"]), f"Expected {s['expected_stop']}, got {stop}"
    assert stop >= s["current_stop"], "Ratchet invariant violated"


def test_TS03_profitable_stop_floored_at_entry(fixture_data, ts_settings):
    """TS-03: Profitable — 2×ATR below entry → stop floored at entry_price."""
    s = fixture_data["trailing_stop_scenarios"]["TS-03_profitable_stop_floored_at_entry"]
    stop, _, _ = calculate_trailing_stop(
        current_price=s["current_price"],
        atr=s["atr"],
        is_profitable=s["is_profitable"],
        current_stop=s["current_stop"],
        entry_price=s["entry_price"],
        settings=ts_settings,
    )
    assert _approx(stop, s["expected_stop"]), f"Expected {s['expected_stop']}, got {stop}"
    assert stop >= s["entry_price"], "Profitable stop must never fall below entry"


def test_TS04_losing_wide_stop_applied(fixture_data, ts_settings):
    """TS-04: Losing position — 5×ATR multiplier applied; stop may be below entry."""
    s = fixture_data["trailing_stop_scenarios"]["TS-04_losing_wide_stop"]
    stop, _, mult = calculate_trailing_stop(
        current_price=s["current_price"],
        atr=s["atr"],
        is_profitable=s["is_profitable"],
        current_stop=s["current_stop"],
        entry_price=s["entry_price"],
        settings=ts_settings,
    )
    assert _approx(stop, s["expected_stop"]), f"Expected {s['expected_stop']}, got {stop}"
    assert _approx(mult, s["expected_atr_mult"]), f"Expected 5x multiplier, got {mult}"
    # Stop may be below entry for losing positions — no floor enforcement
    assert stop >= s["current_stop"], "Ratchet invariant violated for losing position"


def test_TS05_losing_stop_ratchet_holds(fixture_data, ts_settings):
    """TS-05: Losing — computed stop below current_stop → ratchet holds."""
    s = fixture_data["trailing_stop_scenarios"]["TS-05_losing_stop_unchanged"]
    stop, _, _ = calculate_trailing_stop(
        current_price=s["current_price"],
        atr=s["atr"],
        is_profitable=s["is_profitable"],
        current_stop=s["current_stop"],
        entry_price=s["entry_price"],
        settings=ts_settings,
    )
    assert _approx(stop, s["expected_stop"]), f"Expected {s['expected_stop']}, got {stop}"
    assert stop >= s["current_stop"], "Ratchet invariant violated"


def test_TS06_zero_atr_no_division_error(fixture_data, ts_settings):
    """TS-06: ATR = 0 — no division by zero; stop is at most current_price."""
    s = fixture_data["trailing_stop_scenarios"]["TS-06_zero_atr"]
    stop, reason, _ = calculate_trailing_stop(
        current_price=s["current_price"],
        atr=s["atr"],
        is_profitable=s["is_profitable"],
        current_stop=s["current_stop"],
        entry_price=s["entry_price"],
        settings=ts_settings,
    )
    assert isinstance(stop, float), "Should return a float even with ATR=0"
    assert stop >= s["current_stop"], "Ratchet invariant violated"
    assert _approx(stop, s["expected_stop"]), f"Expected {s['expected_stop']}, got {stop}"


def test_TS07_mixed_portfolio_independent(ts_settings):
    """TS-07: Mixed portfolio — profitable and losing positions computed independently."""
    profitable_stop, _, p_mult = calculate_trailing_stop(
        current_price=120.0, atr=5.0, is_profitable=True,
        current_stop=100.0, entry_price=100.0, settings=ts_settings,
    )
    losing_stop, _, l_mult = calculate_trailing_stop(
        current_price=90.0, atr=5.0, is_profitable=False,
        current_stop=60.0, entry_price=100.0, settings=ts_settings,
    )
    assert _approx(profitable_stop, 110.0), "Profitable stop should be 110"
    assert _approx(p_mult, 2.0)
    assert _approx(losing_stop, 65.0), "Losing stop should be 65"
    assert _approx(l_mult, 5.0)


# ===========================================================================
# Rebalance Exit Detection Tests (RX-01 … RX-05)
# ===========================================================================

from services.signal_service import _is_last_trading_day_of_month, generate_rebalance_exit_signals


def test_RX01_non_rebalance_day_no_signals():
    """RX-01: Mid-month weekday → _is_last_trading_day returns False; no signals generated."""
    mid_month = datetime(2026, 6, 15)  # Monday, 15 June 2026
    assert not _is_last_trading_day_of_month(mid_month)


def test_RX_last_trading_day_detection_end_of_june():
    """RX-aux: 30 June 2026 is a Tuesday (next weekday is 1 July → different month)."""
    end_of_june = datetime(2026, 6, 30)
    assert _is_last_trading_day_of_month(end_of_june)


def test_RX_last_trading_day_detection_skips_weekend():
    """RX-aux: When month ends on Sunday (May 31 2026), the function marks
    both Friday May 29 and Saturday May 30 as 'last trading day' because
    it only checks that the next non-weekend calendar day is in the next month.
    The function does NOT validate that check_date itself is a weekday — it
    is called from a scheduled job that only runs on weekdays in production.
    Thursday May 28 must NOT be detected as last trading day (May 29 is a
    non-weekend day in the same month).
    """
    thursday = datetime(2026, 5, 28)    # Thursday — next weekday = Friday May 29 (same month)
    friday_before = datetime(2026, 5, 29)  # Friday — next weekday = June 1 (next month)
    assert not _is_last_trading_day_of_month(thursday)
    assert _is_last_trading_day_of_month(friday_before)


def test_RX01_generate_returns_early_on_non_rebalance_day(database_stub):
    """RX-01: generate_rebalance_exit_signals() returns early on non-rebalance day."""
    mid_month = datetime(2026, 6, 15)
    with patch("services.signal_service.datetime") as mock_dt:
        mock_dt.now.return_value = mid_month
        result = generate_rebalance_exit_signals()
    assert result["is_last_trading_day"] is False
    assert result["signals_created"] == 0


def test_RX02_position_not_in_top5_gets_signal(database_stub):
    """RX-02: Rebalance day; position not in top-5 → 1 exit_rebalance signal created."""
    rebalance_day = datetime(2026, 6, 30)

    database_stub.get_portfolio.return_value = {"id": "portfolio-001"}
    database_stub.get_signals.return_value = [
        {"ticker": "AAPL", "signal_date": "2026-06-30", "status": "new"},
        {"ticker": "MSFT", "signal_date": "2026-06-30", "status": "new"},
    ]
    database_stub.get_positions.return_value = [
        {
            "ticker": "TSLA",  # NOT in top-5
            "market": "US",
            "current_price": 250.0,
            "current_stop": 200.0,
        }
    ]
    created_signal = {"id": "sig-001", "ticker": "TSLA", "signal_type": "exit_rebalance"}
    database_stub.create_rebalance_exit_signal.return_value = created_signal

    with patch("services.signal_service.datetime") as mock_dt, \
         patch("services.signal_service.get_live_fx_rate", return_value=1.27), \
         patch("services.signal_service.decimal_to_float", side_effect=lambda x: x):
        mock_dt.now.return_value = rebalance_day
        result = generate_rebalance_exit_signals()

    assert result["is_last_trading_day"] is True
    assert result["signals_created"] == 1
    database_stub.create_rebalance_exit_signal.assert_called_once()


def test_RX03_position_in_top5_no_signal(database_stub):
    """RX-03: Rebalance day; position IS in top-5 → no signal generated."""
    rebalance_day = datetime(2026, 6, 30)

    database_stub.get_portfolio.return_value = {"id": "portfolio-001"}
    database_stub.get_signals.return_value = [
        {"ticker": "AAPL", "signal_date": "2026-06-30", "status": "new"},
    ]
    database_stub.get_positions.return_value = [
        {
            "ticker": "AAPL",  # IS in top-5
            "market": "US",
            "current_price": 200.0,
            "current_stop": 180.0,
        }
    ]
    database_stub.create_rebalance_exit_signal.reset_mock()

    with patch("services.signal_service.datetime") as mock_dt, \
         patch("services.signal_service.get_live_fx_rate", return_value=1.27), \
         patch("services.signal_service.decimal_to_float", side_effect=lambda x: x):
        mock_dt.now.return_value = rebalance_day
        result = generate_rebalance_exit_signals()

    assert result["is_last_trading_day"] is True
    assert result["signals_created"] == 0
    database_stub.create_rebalance_exit_signal.assert_not_called()


def test_RX04_position_at_stop_no_signal(database_stub):
    """RX-04: Rebalance day; position at trailing stop → skipped (deduplication)."""
    rebalance_day = datetime(2026, 6, 30)

    database_stub.get_portfolio.return_value = {"id": "portfolio-001"}
    database_stub.get_signals.return_value = [
        {"ticker": "GOOGL", "signal_date": "2026-06-30", "status": "new"},
    ]
    database_stub.get_positions.return_value = [
        {
            "ticker": "TSLA",
            "market": "US",
            "current_price": 195.0,  # price <= stop → at stop breach
            "current_stop": 200.0,
        }
    ]
    database_stub.create_rebalance_exit_signal.reset_mock()

    with patch("services.signal_service.datetime") as mock_dt, \
         patch("services.signal_service.get_live_fx_rate", return_value=1.27), \
         patch("services.signal_service.decimal_to_float", side_effect=lambda x: x):
        mock_dt.now.return_value = rebalance_day
        result = generate_rebalance_exit_signals()

    assert result["signals_created"] == 0, "Position at stop should be skipped"
    database_stub.create_rebalance_exit_signal.assert_not_called()


def test_RX05_mixed_portfolio_one_exit_one_retain(database_stub):
    """RX-05: Mixed portfolio — 1 exit signal for non-top-5; top-5 position retained."""
    rebalance_day = datetime(2026, 6, 30)

    database_stub.get_portfolio.return_value = {"id": "portfolio-001"}
    database_stub.get_signals.return_value = [
        {"ticker": "AAPL", "signal_date": "2026-06-30", "status": "new"},
    ]
    database_stub.get_positions.return_value = [
        {"ticker": "AAPL", "market": "US", "current_price": 200.0, "current_stop": 180.0},  # top-5
        {"ticker": "TSLA", "market": "US", "current_price": 250.0, "current_stop": 200.0},  # not top-5
    ]
    database_stub.create_rebalance_exit_signal.reset_mock()
    database_stub.create_rebalance_exit_signal.return_value = {
        "id": "sig-002", "ticker": "TSLA"
    }

    with patch("services.signal_service.datetime") as mock_dt, \
         patch("services.signal_service.get_live_fx_rate", return_value=1.27), \
         patch("services.signal_service.decimal_to_float", side_effect=lambda x: x):
        mock_dt.now.return_value = rebalance_day
        result = generate_rebalance_exit_signals()

    assert result["signals_created"] == 1
    call_args = database_stub.create_rebalance_exit_signal.call_args
    assert call_args.kwargs.get("ticker") == "TSLA"


# ===========================================================================
# Inverse-Volatility Sizing Tests (IV-01 … IV-07)
# ===========================================================================

from services.sizing_service import size_batch_inv_vol

_IV_MIN = 0.05
_IV_MAX = 0.20


def _make_signal(ticker, atr, price_gbp):
    return {
        "ticker": ticker,
        "market": "US",
        "atr_value": atr,
        "current_price": price_gbp * 1.27,
        "price_gbp": price_gbp,
    }


@pytest.fixture(autouse=True)
def stub_settings(database_stub):
    """Ensure get_settings() returns a valid settings dict for sizing tests."""
    database_stub.get_settings.return_value = [
        {"atr_multiplier_trailing": 2.0, "atr_multiplier_initial": 5.0}
    ]


def test_IV01_single_signal_full_allocation():
    """IV-01: Single signal — weight=1.0, full cash allocation."""
    signals = [_make_signal("AAPL", atr=5.0, price_gbp=157.48)]
    result = size_batch_inv_vol(signals, available_cash=10000.0, fx_rate=1.27)
    assert len(result) == 1
    assert _approx(result[0]["inv_vol_weight"], 1.0)
    assert _approx(result[0]["allocation_gbp"], 10000.0)
    assert result[0]["suggested_shares"] == math.floor(10000.0 / 157.48)


def test_IV05_zero_atr_signal_gets_minimum_floor_not_zero():
    """IV-05: ATR=0 for one signal — the min-weight floor (0.05) is applied to
    the zero-inv-ATR signal before normalisation, so it receives a small non-zero
    allocation. Full-zero allocation only occurs when ALL signals have ATR=0 (IV-06).
    The valid-ATR signal receives a higher weight than the zero-ATR signal.
    """
    signals = [
        _make_signal("AAPL", atr=0.0, price_gbp=118.11),
        _make_signal("GOOGL", atr=10.0, price_gbp=118.11),
    ]
    result = size_batch_inv_vol(signals, available_cash=10000.0, fx_rate=1.27)
    aapl = next(s for s in result if s["ticker"] == "AAPL")
    googl = next(s for s in result if s["ticker"] == "GOOGL")
    # Zero-ATR signal gets the minimum-floor allocation, not zero
    assert aapl["inv_vol_weight"] >= _IV_MIN - 1e-9, \
        "Zero-ATR signal should receive the minimum-floor weight"
    # Valid-ATR signal gets a strictly higher weight than zero-ATR signal
    assert googl["inv_vol_weight"] > aapl["inv_vol_weight"], \
        "Valid-ATR signal should receive higher weight than zero-ATR signal"
    # Weights sum to 1.0
    total = aapl["inv_vol_weight"] + googl["inv_vol_weight"]
    assert _approx(total, 1.0, rel_tol=1e-4)


def test_IV06_all_zero_atr_returns_zero_shares():
    """IV-06: All signals have ATR=0 → all get 0 shares; no ZeroDivisionError."""
    signals = [
        _make_signal("AAPL", atr=0.0, price_gbp=118.11),
        _make_signal("GOOGL", atr=0.0, price_gbp=118.11),
    ]
    result = size_batch_inv_vol(signals, available_cash=10000.0, fx_rate=1.27)
    for sig in result:
        assert sig["suggested_shares"] == 0
        assert sig["allocation_gbp"] == 0


def test_IV03_max_weight_cap_reduces_dominance():
    """IV-03: Signal with very low ATR (high inv-vol weight) is capped at _INV_VOL_MAX_WEIGHT
    BEFORE normalisation. After renormalisation, the final weight may exceed _IV_MAX but
    is strictly less than the uncapped raw weight (capping reduces concentration).
    Total normalised weights sum to 1.0.

    With ATR=[0.1, 5, 5, 5, 5]:
      raw_weights ≈ [0.926, 0.0185×4]
      capped = [0.20, 0.05×4] = [0.20, 0.20 total for others]
      normalised = [0.50, 0.125×4]   (post-cap normalisation)
    Signal A's final weight (0.5) is reduced from raw (0.926) by the cap.
    """
    signals = [
        _make_signal("A", atr=0.1, price_gbp=100.0),
        _make_signal("B", atr=5.0, price_gbp=100.0),
        _make_signal("C", atr=5.0, price_gbp=100.0),
        _make_signal("D", atr=5.0, price_gbp=100.0),
        _make_signal("E", atr=5.0, price_gbp=100.0),
    ]
    result = size_batch_inv_vol(signals, available_cash=10000.0, fx_rate=1.27)
    a = next(s for s in result if s["ticker"] == "A")
    # Cap reduced dominance: final weight should be 0.5, not 0.926 (raw uncapped)
    # Note: post-normalisation weight can exceed _IV_MAX; that is expected behaviour
    assert a["inv_vol_weight"] < 0.926 - 1e-6, \
        f"Cap did not reduce A's dominance (weight={a['inv_vol_weight']})"
    assert _approx(a["inv_vol_weight"], 0.5, rel_tol=1e-4), \
        f"Expected post-cap weight ~0.5, got {a['inv_vol_weight']}"
    # All same-ATR signals get equal weight
    b = next(s for s in result if s["ticker"] == "B")
    assert _approx(b["inv_vol_weight"], 0.125, rel_tol=1e-4)
    # Total weight = 1.0
    total_weight = sum(s["inv_vol_weight"] for s in result)
    assert _approx(total_weight, 1.0, rel_tol=1e-4), f"Weights sum {total_weight} != 1.0"


def test_IV04_min_weight_floor_raises_near_zero_weight():
    """IV-04: Signal with very high ATR (near-zero inv-vol weight) is floored at
    _INV_VOL_MIN_WEIGHT BEFORE normalisation. After renormalisation, its final weight
    is strictly greater than the uncapped raw weight.

    With ATR=[0.1, 1000]:
      inv_atrs = [10, 0.001]; total ≈ 10.001
      raw_weights ≈ [0.9999, 0.0001]
      capped = [min(0.20, 0.9999)=0.20, max(0.05, 0.0001)=0.05]
      normalised = [0.20/0.25, 0.05/0.25] = [0.80, 0.20]
    Signal B's final weight (0.20) is raised from raw (0.0001) by the floor.
    """
    signals = [
        _make_signal("A", atr=0.1, price_gbp=100.0),
        _make_signal("B", atr=1000.0, price_gbp=100.0),
    ]
    result = size_batch_inv_vol(signals, available_cash=10000.0, fx_rate=1.27)
    b = next(s for s in result if s["ticker"] == "B")
    # Floor raised B's weight: raw was ~0.0001; post-floor+normalise is 0.20
    assert b["inv_vol_weight"] > 0.001, \
        f"Min-weight floor did not raise B's weight (weight={b['inv_vol_weight']})"
    assert _approx(b["inv_vol_weight"], 0.20, rel_tol=1e-4), \
        f"Expected post-floor weight ~0.20, got {b['inv_vol_weight']}"
    total_weight = sum(s["inv_vol_weight"] for s in result)
    assert _approx(total_weight, 1.0, rel_tol=1e-4)


def test_IV07_mixed_volatility_three_signals():
    """IV-07: Mixed ATR portfolio — inverse-volatility ordering is preserved.

    With ATR=[5, 10, 20]:
      inv_atrs = [0.2, 0.1, 0.05]; total = 0.35
      raw_weights = [0.571, 0.286, 0.143]
      capped = [0.20, 0.20, 0.143]   (0.571 > _IV_MAX → capped; 0.143 > _IV_MIN → unchanged)
      normalised = [0.368, 0.368, 0.263]

    After normalisation LOW_VOL and MID_VOL have equal weight (both hit the cap);
    both are strictly higher than HIGH_VOL. Weights sum to 1.0.
    Note: post-normalisation weights may exceed _IV_MAX (0.20); this is expected.
    """
    signals = [
        _make_signal("LOW_VOL", atr=5.0, price_gbp=100.0),
        _make_signal("MID_VOL", atr=10.0, price_gbp=100.0),
        _make_signal("HIGH_VOL", atr=20.0, price_gbp=100.0),
    ]
    result = size_batch_inv_vol(signals, available_cash=10000.0, fx_rate=1.27)
    low = next(s for s in result if s["ticker"] == "LOW_VOL")
    mid = next(s for s in result if s["ticker"] == "MID_VOL")
    high = next(s for s in result if s["ticker"] == "HIGH_VOL")
    # Lower-volatility signals get equal or higher weight than higher-volatility
    assert low["inv_vol_weight"] >= high["inv_vol_weight"], \
        "LOW_VOL should have weight >= HIGH_VOL"
    assert mid["inv_vol_weight"] >= high["inv_vol_weight"], \
        "MID_VOL should have weight >= HIGH_VOL"
    # Expected normalised weights
    assert _approx(low["inv_vol_weight"], 0.368421, rel_tol=1e-4)
    assert _approx(high["inv_vol_weight"], 0.263158, rel_tol=1e-4)
    total_weight = sum(s["inv_vol_weight"] for s in result)
    assert _approx(total_weight, 1.0, rel_tol=1e-4), f"Weights sum {total_weight} != 1.0"
