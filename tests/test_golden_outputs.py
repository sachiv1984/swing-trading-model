"""
ST-05: Golden Output Regression Tests

Loads tests/golden_outputs.json and verifies:
  1. Spec formulas produce the expected golden values (spec correctness)
  2. Implementation pure-math functions match the same golden values (impl correctness)

All expected values are derived from claude/strategy/strategy_rules.md §4.1 and §5/§7.
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


def load_golden() -> dict:
    with open(GOLDEN_PATH) as f:
        return json.load(f)


GOLDEN = load_golden()

# ---------------------------------------------------------------------------
# Spec formula implementations (authoritative, no implementation import)
# These mirror strategy_rules.md exactly and must NEVER be changed to match
# the implementation — the implementation must match these.
# ---------------------------------------------------------------------------

TOLERANCE = 1e-9  # floating-point equality tolerance for raw values
DP4_TOLERANCE = 0.0  # 4dp floored values must be exact


def spec_stop_distance(entry_price: float, stop_price: float) -> float:
    """§4.1.1: StopDistance = EntryPrice - StopPrice"""
    return entry_price - stop_price


def spec_risk_amount(portfolio_value: float, risk_percent: float) -> float:
    """§4.1.2: RiskAmount = PortfolioValue × (RiskPercent / 100)"""
    return portfolio_value * (risk_percent / 100)


def spec_raw_shares(risk_amount: float, stop_distance: float, fx_rate: float) -> float:
    """§4.1.3: RawShares = RiskAmount / (StopDistance × fx_rate)"""
    return risk_amount / (stop_distance * fx_rate)


def spec_suggested_shares(raw_shares: float) -> float:
    """§4.1.3: SuggestedShares = floor(RawShares × 10000) / 10000"""
    return math.floor(raw_shares * 10000) / 10000


def spec_initial_stop(entry_price: float, atr: float, multiplier: float) -> float:
    """§5: InitialStop = EntryPrice - (InitialATRMultiplier × ATR)"""
    return entry_price - (multiplier * atr)


def spec_trailing_stop(current_price: float, atr: float, multiplier: float) -> float:
    """§7.2: NewStop = CurrentPrice - (ATRMultiplier × ATR)"""
    return current_price - (multiplier * atr)


def spec_updated_stop(current_stop: float, new_calculated_stop: float) -> float:
    """§7.3: UpdatedStop = max(CurrentStop, NewlyCalculatedStop) — stops never decrease"""
    return max(current_stop, new_calculated_stop)


# ---------------------------------------------------------------------------
# Implementation imports (pure-math functions only — no DB required)
# ---------------------------------------------------------------------------

# Add backend to path for import
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    from services.sizing_service import _floor_4dp as impl_floor_4dp
    SIZING_AVAILABLE = True
except ImportError:
    SIZING_AVAILABLE = False

try:
    import position_manager as pm
    POSITION_MANAGER_AVAILABLE = True
except ImportError:
    POSITION_MANAGER_AVAILABLE = False


# ---------------------------------------------------------------------------
# Position Sizing Tests (ST-05 — §4.1)
# ---------------------------------------------------------------------------

class TestPositionSizingSpecFormulas(unittest.TestCase):
    """
    Verify spec formulas produce the expected golden values.
    These tests validate the specification itself is internally consistent.
    """

    def _run_case(self, case: dict):
        inp = case["inputs"]
        exp = case["expected"]
        cid = case["id"]

        entry = inp["entry_price"]
        stop = inp["stop_price"]
        risk_pct = inp["risk_percent"]
        portfolio = inp["portfolio_value"]
        fx = inp.get("fx_rate", 1.0)

        stop_dist = spec_stop_distance(entry, stop)
        risk_amt = spec_risk_amount(portfolio, risk_pct)
        raw = spec_raw_shares(risk_amt, stop_dist, fx)
        suggested = spec_suggested_shares(raw)

        self.assertAlmostEqual(
            stop_dist, exp["stop_distance"], places=4,
            msg=f"{cid}: stop_distance mismatch"
        )
        self.assertAlmostEqual(
            risk_amt, exp["risk_amount"], places=2,
            msg=f"{cid}: risk_amount mismatch"
        )
        self.assertAlmostEqual(
            raw, exp["raw_shares"], delta=TOLERANCE,
            msg=f"{cid}: raw_shares mismatch"
        )
        self.assertEqual(
            suggested, exp["suggested_shares"],
            msg=f"{cid}: suggested_shares mismatch (floor(4dp) rule)"
        )

    def test_PS01_uk_round(self):
        self._run_case(next(c for c in GOLDEN["position_sizing"] if c["id"] == "PS-01"))

    def test_PS02_uk_floor_required(self):
        self._run_case(next(c for c in GOLDEN["position_sizing"] if c["id"] == "PS-02"))

    def test_PS03_uk_small_risk(self):
        self._run_case(next(c for c in GOLDEN["position_sizing"] if c["id"] == "PS-03"))

    def test_PS04_us_fx_round(self):
        self._run_case(next(c for c in GOLDEN["position_sizing"] if c["id"] == "PS-04"))

    def test_PS05_us_fx_floor(self):
        self._run_case(next(c for c in GOLDEN["position_sizing"] if c["id"] == "PS-05"))


class TestPositionSizingImplementation(unittest.TestCase):
    """
    Verify implementation's pure-math functions match spec golden values.
    Skipped if sizing_service cannot be imported (DB-dependent imports fail in CI
    without a database — the _floor_4dp function itself has no DB dependency).
    """

    @unittest.skipUnless(SIZING_AVAILABLE, "sizing_service not importable")
    def test_floor_4dp_matches_spec_for_all_cases(self):
        """_floor_4dp must produce the same SuggestedShares as the spec formula."""
        for case in GOLDEN["position_sizing"]:
            inp = case["inputs"]
            exp = case["expected"]
            cid = case["id"]

            # Reproduce raw_shares via spec formula
            stop_dist = spec_stop_distance(inp["entry_price"], inp["stop_price"])
            risk_amt = spec_risk_amount(inp["portfolio_value"], inp["risk_percent"])
            fx = inp.get("fx_rate", 1.0)
            raw = spec_raw_shares(risk_amt, stop_dist, fx)

            impl_result = impl_floor_4dp(raw)
            spec_result = exp["suggested_shares"]

            self.assertEqual(
                impl_result, spec_result,
                msg=f"{cid}: _floor_4dp({raw}) = {impl_result}, expected {spec_result}"
            )


# ---------------------------------------------------------------------------
# Stop-Loss Tests (ST-05 — §5, §7)
# ---------------------------------------------------------------------------

class TestStopLossSpecFormulas(unittest.TestCase):
    """
    Verify stop-loss spec formulas produce the expected golden values.
    """

    def _get(self, sl_id: str) -> dict:
        return next(c for c in GOLDEN["stop_loss"] if c["id"] == sl_id)

    def test_SL01_initial_stop(self):
        case = self._get("SL-01")
        inp = case["inputs"]
        result = spec_initial_stop(inp["entry_price"], inp["atr"], inp["atr_multiplier"])
        self.assertAlmostEqual(result, case["expected"]["initial_stop"], places=2,
                               msg="SL-01: initial stop mismatch")

    def test_SL02_losing_trailing_stop(self):
        case = self._get("SL-02")
        inp = case["inputs"]
        result = spec_trailing_stop(inp["current_price"], inp["atr"], inp["atr_multiplier"])
        self.assertAlmostEqual(result, case["expected"]["new_stop"], places=2,
                               msg="SL-02: losing trailing stop mismatch")

    def test_SL03_profitable_trailing_stop(self):
        case = self._get("SL-03")
        inp = case["inputs"]
        result = spec_trailing_stop(inp["current_price"], inp["atr"], inp["atr_multiplier"])
        self.assertAlmostEqual(result, case["expected"]["new_stop"], places=2,
                               msg="SL-03: profitable trailing stop mismatch")

    def test_SL04_stop_moves_up(self):
        case = self._get("SL-04")
        inp = case["inputs"]
        result = spec_updated_stop(inp["current_stop"], inp["new_calculated_stop"])
        self.assertAlmostEqual(result, case["expected"]["trailing_stop"], places=2,
                               msg="SL-04: upward stop movement mismatch")

    def test_SL05_stop_blocked_downward(self):
        """CRITICAL — §7.3: stop must never decrease."""
        case = self._get("SL-05")
        inp = case["inputs"]
        result = spec_updated_stop(inp["current_stop"], inp["new_calculated_stop"])
        self.assertAlmostEqual(result, case["expected"]["trailing_stop"], places=2,
                               msg="SL-05: downward stop should be BLOCKED — §7.3 violation")
        # Explicit guard: result must equal current_stop (not decrease)
        self.assertGreaterEqual(result, inp["current_stop"],
                                msg="SL-05: stop decreased — §7.3 hard constraint violated")

    def test_SL06_stop_unchanged(self):
        case = self._get("SL-06")
        inp = case["inputs"]
        result = spec_updated_stop(inp["current_stop"], inp["new_calculated_stop"])
        self.assertAlmostEqual(result, case["expected"]["trailing_stop"], places=2,
                               msg="SL-06: equal stops should be unchanged")

    def test_SL07_stop_stays_high_after_state_transition(self):
        """§7.3: No exception for profitable-to-losing transition — stop cannot loosen."""
        case = self._get("SL-07")
        inp = case["inputs"]
        result = spec_updated_stop(inp["current_stop"], inp["new_calculated_stop"])
        self.assertAlmostEqual(result, case["expected"]["trailing_stop"], places=2,
                               msg="SL-07: stop loosened on state transition — §7.3 violation")
        self.assertGreaterEqual(result, inp["current_stop"],
                                msg="SL-07: stop decreased — §7.3 hard constraint violated")


# ---------------------------------------------------------------------------
# Metadata / sanity checks
# ---------------------------------------------------------------------------

class TestGoldenOutputsMetadata(unittest.TestCase):

    def test_golden_file_loads(self):
        self.assertIn("position_sizing", GOLDEN)
        self.assertIn("stop_loss", GOLDEN)

    def test_expected_case_counts(self):
        self.assertEqual(len(GOLDEN["position_sizing"]), 5, "Expected 5 position sizing cases")
        self.assertEqual(len(GOLDEN["stop_loss"]), 7, "Expected 7 stop-loss cases")

    def test_canonical_parameters_present(self):
        params = GOLDEN["_metadata"]["canonical_parameters"]
        self.assertEqual(params["grace_period_days"], 10)
        self.assertEqual(params["initial_atr_multiplier"], 5)
        self.assertEqual(params["profit_atr_multiplier"], 2)
        self.assertEqual(params["atr_period_days"], 14)

    def test_all_position_sizing_cases_have_expected(self):
        for case in GOLDEN["position_sizing"]:
            self.assertIn("expected", case, f"{case['id']} missing 'expected'")
            exp = case["expected"]
            for field in ("stop_distance", "risk_amount", "raw_shares", "suggested_shares"):
                self.assertIn(field, exp, f"{case['id']} missing expected.{field}")

    def test_all_stop_loss_cases_have_expected(self):
        for case in GOLDEN["stop_loss"]:
            self.assertIn("expected", case, f"{case['id']} missing 'expected'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
