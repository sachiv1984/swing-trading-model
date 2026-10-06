"""
Single source of the strategy_rules.md §11 stop parameters (ST-01, BLG-BE-138,
EPIC-01, v9.10).

Parameter-authority ruling, 2026-10-06 (ESC-EXEC-20261006-01, outcome (a)):
these values are fixed by the strategy rules. They are not read from the
editable `settings` row. Changing one is a §12.3 strategy change, made here,
in strategy_rules.md §11 and in the frontend display mirror
src/lib/strategyParameters.js (tests/test_strategy_parameter_parity.py fails
if the two drift).

Every live stop path imports from here: analyze_positions,
run_nightly_trailing_stop_update, add_position, get_positions_with_prices,
should_exit_position (callers), grace_service, compliance_service and
alerts_service. The backtest/replay engines (strategy_engine.py,
replay_service.py, position_manager.py) carry their own parameter sets by
design and are not on the live path.
"""
from typing import Dict, Final

GRACE_PERIOD_DAYS: Final[int] = 10          # §6.2 / §11: days 0-9 are grace
INITIAL_ATR_MULTIPLIER: Final[float] = 5.0  # §5 / §7.2: initial and losing stop
PROFIT_ATR_MULTIPLIER: Final[float] = 2.0   # §7.2: profitable stop
ATR_PERIOD_DAYS: Final[int] = 14            # §7.1


def stop_multiplier_settings() -> Dict[str, float]:
    """The settings-shaped dict calculate_trailing_stop() expects."""
    return {
        "atr_multiplier_initial": INITIAL_ATR_MULTIPLIER,
        "atr_multiplier_trailing": PROFIT_ATR_MULTIPLIER,
    }
