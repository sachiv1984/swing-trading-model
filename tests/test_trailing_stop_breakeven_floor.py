"""
BLG-BE-102 regression tests (ST-01, EPIC-01, v8.9).

Nightly trailing-stop ratchet must apply a breakeven floor for profitable
positions: a profitable position's stop must never sit below its own
entry_price. This is enforced by backend/utils/calculations.py's
calculate_trailing_stop() (`trailing_stop = max(current_stop, new_stop,
entry_price)` when profitable) — the single canonical calculation path used
by both live production entry points:
  - services/position_service.py::get_positions_with_prices() -> analyze_positions()
    (invoked nightly via GET /positions/analyze, see .github/workflows/daily-snapshot.yml)
  - services/position_service.py::run_nightly_trailing_stop_update()
    (invoked via POST /positions/nightly-stop-update)

backend/position_manager.py has its own, deliberately simpler inline
formula (`max(current_stop, new_stop)`, no entry_price floor) — confirmed
by code-path audit (v8.9 ST-01) to be a backtest-tool-only path, never
imported or invoked by any live-serving endpoint (its only cross-module
export used in production, check_market_regime, is unrelated to stop
calculation). It is intentionally reconciled against the base ratchet
formula — without the floor — by tests/test_stop_reconciliation.py, which
exists to catch backtest/live divergence on the *shared* base formula, not
to require the live-only floor enhancement in the backtest tool.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from utils.calculations import calculate_trailing_stop  # noqa: E402


class TestBreakevenFloorProfitablePosition:
    """Profitable positions must never have a stop below entry_price."""

    def test_wdc_worked_example_from_BLG_BE_102(self):
        """
        Exact figures from the BLG-BE-102 investigation (WDC, entry
        2026-08-07, native entry price $434.30, current_price $508.80,
        ATR $54.1986, current_stop stuck at initial_stop $163.31,
        profitable, grace period over).

        Expected: max(163.31, 508.80 - 2*54.1986, 434.30) = 434.30
        (breakeven floor governs — the unfloored ATR trail (400.40) is
        still below entry_price).
        """
        new_stop, reason, atr_mult = calculate_trailing_stop(
            current_price=508.80,
            atr=54.1986,
            is_profitable=True,
            current_stop=163.31,
            entry_price=434.30,
            settings={"atr_multiplier_trailing": 2.0, "atr_multiplier_initial": 5.0},
        )
        assert new_stop == 434.30, (
            f"breakeven floor not applied: expected 434.30, got {new_stop}"
        )
        assert atr_mult == 2.0

    def test_profitable_stop_never_below_entry_price(self):
        """General case: even when the ATR trail and prior stop are both
        below entry, the floor must win."""
        new_stop, _, _ = calculate_trailing_stop(
            current_price=105.0,
            atr=20.0,   # ATR trail = 105 - 2*20 = 65, well below entry
            is_profitable=True,
            current_stop=50.0,
            entry_price=100.0,
            settings={},
        )
        assert new_stop >= 100.0, (
            "profitable position's stop fell below its own entry_price"
        )
        assert new_stop == 100.0

    def test_profitable_stop_uses_atr_trail_when_above_entry(self):
        """Floor is a lower bound only — a genuinely higher ATR trail
        stop must still win when the position has moved well into profit."""
        new_stop, _, _ = calculate_trailing_stop(
            current_price=200.0,
            atr=10.0,   # ATR trail = 200 - 2*10 = 180, above entry
            is_profitable=True,
            current_stop=150.0,
            entry_price=100.0,
            settings={},
        )
        assert new_stop == 180.0

    def test_losing_position_not_floored_at_entry(self):
        """Losing positions intentionally retain the wide stop and may sit
        below entry_price — the floor is profit-only (§ calculate_trailing_stop
        docstring: 'Losing: Allow wide stop, can be below entry')."""
        new_stop, _, _ = calculate_trailing_stop(
            current_price=90.0,
            atr=10.0,
            is_profitable=False,
            current_stop=60.0,
            entry_price=100.0,
            settings={},
        )
        assert new_stop < 100.0
        assert new_stop == 60.0  # new_stop = 90 - 5*10 = 40; max(current_stop=60, 40) = 60

    def test_stop_only_ever_ratchets_up_never_down(self):
        """§7.3 ratchet invariant, still enforced when the floor is applied."""
        new_stop, _, _ = calculate_trailing_stop(
            current_price=100.0,
            atr=50.0,   # ATR trail = 100 - 2*50 = 0, well below current_stop
            is_profitable=True,
            current_stop=90.0,
            entry_price=80.0,
            settings={},
        )
        assert new_stop >= 90.0


class TestPositionManagerNotOnLiveStopPath:
    """Confirms BLG-BE-102 scope item 1: only one calculation path is used
    in production. position_manager.py's inline formula is never invoked by
    a live-serving endpoint."""

    def test_position_service_does_not_import_position_manager(self):
        import services.position_service as position_service_module

        src_path = Path(position_service_module.__file__)
        source = src_path.read_text()
        assert "import position_manager" not in source
        assert "from position_manager" not in source

    def test_live_endpoints_call_calculate_trailing_stop(self):
        """Both live stop-writing paths (analyze_positions via
        get_positions_with_prices, and run_nightly_trailing_stop_update)
        must go through the shared, floored calculate_trailing_stop()."""
        import services.position_service as position_service_module

        source = Path(position_service_module.__file__).read_text()
        # Two live call sites: get_positions_with_prices() and
        # run_nightly_trailing_stop_update(). The import line reads
        # "calculate_trailing_stop," (no trailing paren) and does not
        # match this substring, so 2 is the exact expected count.
        assert source.count("calculate_trailing_stop(") >= 2
