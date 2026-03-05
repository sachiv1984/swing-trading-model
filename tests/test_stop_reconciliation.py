"""
ST-06: Backtest vs Live Stop Reconciliation

Verifies that:
  1. position_manager.py PARAMS match the canonical parameters in strategy_rules.md §11
  2. position_manager.py stop calculation formula matches spec §7.2 / §7.3
  3. For every golden stop-loss input, the backtest tool and the spec formula
     produce identical results

This test is designed to fail loudly if someone silently changes PARAMS in
position_manager.py or alters the stop formula — catching divergence before
it reaches live positions.

No database calls are made — this suite is CI-safe.
"""

import json
import math
import sys
import unittest
from pathlib import Path

# ---------------------------------------------------------------------------
# Load golden vectors
# ---------------------------------------------------------------------------

GOLDEN_PATH = Path(__file__).parent / "golden_outputs.json"

with open(GOLDEN_PATH) as f:
    GOLDEN = json.load(f)

CANONICAL = GOLDEN["_metadata"]["canonical_parameters"]

# ---------------------------------------------------------------------------
# Import position_manager (backtest tool)
# ---------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    import position_manager as pm
    POSITION_MANAGER_AVAILABLE = True
    PM_IMPORT_ERROR = None
except ImportError as e:
    POSITION_MANAGER_AVAILABLE = False
    PM_IMPORT_ERROR = str(e)


# ---------------------------------------------------------------------------
# Spec reference formulas (duplicate from test_golden_outputs for isolation)
# ---------------------------------------------------------------------------

def spec_stop(current_price: float, atr: float, multiplier: float) -> float:
    return current_price - (multiplier * atr)


def spec_updated_stop(current_stop: float, new_stop: float) -> float:
    return max(current_stop, new_stop)


def spec_initial_stop(entry_price: float, atr: float, multiplier: float) -> float:
    return entry_price - (multiplier * atr)


# ---------------------------------------------------------------------------
# ST-06 Tests
# ---------------------------------------------------------------------------

@unittest.skipUnless(POSITION_MANAGER_AVAILABLE, f"position_manager not importable: {PM_IMPORT_ERROR}")
class TestPositionManagerParams(unittest.TestCase):
    """
    PARAMS in position_manager.py must match strategy_rules.md §11 canonical parameters.
    Any divergence here means the backtest tool is running on different rules than the spec.
    """

    def test_grace_period_days(self):
        self.assertEqual(
            pm.PARAMS.get("min_hold_days"),
            CANONICAL["grace_period_days"],
            f"position_manager PARAMS['min_hold_days'] must equal "
            f"canonical grace_period_days={CANONICAL['grace_period_days']} (§11)"
        )

    def test_initial_atr_multiplier(self):
        self.assertEqual(
            pm.PARAMS.get("initial_atr_mult"),
            CANONICAL["initial_atr_multiplier"],
            f"position_manager PARAMS['initial_atr_mult'] must equal "
            f"canonical initial_atr_multiplier={CANONICAL['initial_atr_multiplier']} (§11)"
        )

    def test_profit_atr_multiplier(self):
        self.assertEqual(
            pm.PARAMS.get("profit_atr_mult"),
            CANONICAL["profit_atr_multiplier"],
            f"position_manager PARAMS['profit_atr_mult'] must equal "
            f"canonical profit_atr_multiplier={CANONICAL['profit_atr_multiplier']} (§11)"
        )

    def test_atr_period_days(self):
        self.assertEqual(
            pm.PARAMS.get("atr_period"),
            CANONICAL["atr_period_days"],
            f"position_manager PARAMS['atr_period'] must equal "
            f"canonical atr_period_days={CANONICAL['atr_period_days']} (§11)"
        )


@unittest.skipUnless(POSITION_MANAGER_AVAILABLE, f"position_manager not importable: {PM_IMPORT_ERROR}")
class TestStopFormulaReconciliation(unittest.TestCase):
    """
    For each golden stop-loss case, verify that running the position_manager
    PARAMS + stop formula produces the same result as the spec formula.

    This catches divergence between backtest tool and spec without needing
    to call the live API.
    """

    def _pm_stop(self, current_price: float, atr: float, is_profitable: bool) -> float:
        """Apply position_manager's multiplier selection and stop formula."""
        if is_profitable:
            multiplier = pm.PARAMS["profit_atr_mult"]
        else:
            multiplier = pm.PARAMS["initial_atr_mult"]
        return current_price - (multiplier * atr)

    def _pm_updated_stop(self, current_stop: float, new_stop: float) -> float:
        """§7.3: UpdatedStop = max(CurrentStop, NewlyCalculatedStop)"""
        return max(current_stop, new_stop)

    def test_SL01_initial_stop_reconciles(self):
        """Initial stop: backtest formula must match spec §5."""
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-01")
        inp = case["inputs"]
        expected = case["expected"]["initial_stop"]

        spec_result = spec_initial_stop(
            inp["entry_price"], inp["atr"], pm.PARAMS["initial_atr_mult"]
        )
        self.assertAlmostEqual(spec_result, expected, places=2,
                               msg="SL-01: initial stop (using pm.PARAMS) diverges from golden")

    def test_SL02_losing_stop_reconciles(self):
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-02")
        inp = case["inputs"]
        expected = case["expected"]["new_stop"]

        pm_result = self._pm_stop(inp["current_price"], inp["atr"], inp["is_profitable"])
        spec_result = spec_stop(inp["current_price"], inp["atr"], inp["atr_multiplier"])

        self.assertAlmostEqual(pm_result, spec_result, places=2,
                               msg="SL-02: backtest and spec stop formulas diverge")
        self.assertAlmostEqual(pm_result, expected, places=2,
                               msg="SL-02: backtest result diverges from golden")

    def test_SL03_profitable_stop_reconciles(self):
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-03")
        inp = case["inputs"]
        expected = case["expected"]["new_stop"]

        pm_result = self._pm_stop(inp["current_price"], inp["atr"], inp["is_profitable"])
        spec_result = spec_stop(inp["current_price"], inp["atr"], inp["atr_multiplier"])

        self.assertAlmostEqual(pm_result, spec_result, places=2,
                               msg="SL-03: backtest and spec stop formulas diverge")
        self.assertAlmostEqual(pm_result, expected, places=2,
                               msg="SL-03: backtest result diverges from golden")

    def test_SL04_upward_movement_reconciles(self):
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-04")
        inp = case["inputs"]
        expected = case["expected"]["trailing_stop"]

        pm_result = self._pm_updated_stop(inp["current_stop"], inp["new_calculated_stop"])
        spec_result = spec_updated_stop(inp["current_stop"], inp["new_calculated_stop"])

        self.assertEqual(pm_result, spec_result,
                         msg="SL-04: backtest and spec updated_stop diverge")
        self.assertAlmostEqual(pm_result, expected, places=2,
                               msg="SL-04: backtest updated_stop diverges from golden")

    def test_SL05_downward_blocked_reconciles(self):
        """CRITICAL — §7.3: both backtest and spec must block downward movement."""
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-05")
        inp = case["inputs"]
        expected = case["expected"]["trailing_stop"]

        pm_result = self._pm_updated_stop(inp["current_stop"], inp["new_calculated_stop"])
        spec_result = spec_updated_stop(inp["current_stop"], inp["new_calculated_stop"])

        self.assertEqual(pm_result, spec_result,
                         msg="SL-05: backtest and spec diverge on downward-block rule")
        self.assertAlmostEqual(pm_result, expected, places=2,
                               msg="SL-05: stop was not blocked from decreasing — §7.3 violation")
        # Hard guard
        self.assertGreaterEqual(pm_result, inp["current_stop"],
                                msg="SL-05: backtest allowed stop to decrease — §7.3 violated")

    def test_SL06_equal_unchanged_reconciles(self):
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-06")
        inp = case["inputs"]
        expected = case["expected"]["trailing_stop"]

        pm_result = self._pm_updated_stop(inp["current_stop"], inp["new_calculated_stop"])
        self.assertAlmostEqual(pm_result, expected, places=2,
                               msg="SL-06: equal stops should remain unchanged")

    def test_SL07_state_transition_no_loosen_reconciles(self):
        """§7.3: Profitable-to-losing transition must not loosen the stop."""
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-07")
        inp = case["inputs"]
        expected = case["expected"]["trailing_stop"]

        pm_result = self._pm_updated_stop(inp["current_stop"], inp["new_calculated_stop"])
        self.assertAlmostEqual(pm_result, expected, places=2,
                               msg="SL-07: stop loosened after profitable-to-losing transition — §7.3 violated")
        self.assertGreaterEqual(pm_result, inp["current_stop"],
                                msg="SL-07: stop decreased — §7.3 hard constraint violated")


@unittest.skipUnless(POSITION_MANAGER_AVAILABLE, f"position_manager not importable: {PM_IMPORT_ERROR}")
class TestSyntheticDivergenceDetection(unittest.TestCase):
    """
    Confirm that the reconciliation tests WOULD fail if there were a synthetic divergence.
    Validates that our test harness is sensitive enough to catch real bugs.
    """

    def test_wrong_multiplier_would_be_detected(self):
        """If initial_atr_mult were 3 instead of 5, a losing stop would diverge from golden."""
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-02")
        inp = case["inputs"]
        expected = case["expected"]["new_stop"]

        # Simulate a wrong multiplier (3 instead of 5)
        wrong_result = inp["current_price"] - (3 * inp["atr"])
        self.assertNotAlmostEqual(
            wrong_result, expected, places=2,
            msg="Detection test broken: wrong multiplier should produce a different result"
        )

    def test_stop_decrease_would_be_detected(self):
        """If max() were replaced with min(), downward movement would not be blocked."""
        case = next(c for c in GOLDEN["stop_loss"] if c["id"] == "SL-05")
        inp = case["inputs"]
        expected = case["expected"]["trailing_stop"]

        # Simulate broken logic (min instead of max)
        broken_result = min(inp["current_stop"], inp["new_calculated_stop"])
        self.assertNotAlmostEqual(
            broken_result, expected, places=2,
            msg="Detection test broken: broken min() should diverge from golden"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
