"""
Unit tests for plan_vs_reality_service — ST-01 (EPIC-01, v3.6).

Covers:
  AC-02: planned_entry_price snapshot captured via exit_position() (integration path
         tested via compute_plan_vs_reality with explicit field present)
  AC-03: entry_delta_pct = (actual - planned) / planned * 100 when planned_entry_price set
  AC-04: compute_plan_vs_reality returns entry_delta_pct (float) when field populated
  AC-05: existing trades without planned_entry_price → entry_delta_pct: null, no error

No database calls — CI-safe. Stubs sys.modules before importing backend code.
"""

import sys
import types
import unittest
from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Minimal sys.modules stubs — must be registered before any backend import.
# ---------------------------------------------------------------------------

def _make_db_stub():
    stub = types.ModuleType("database")
    stub.get_trade_by_id = MagicMock(return_value=None)
    stub.get_position_by_id = MagicMock(return_value=None)
    stub.get_trade_plans_by_position = MagicMock(return_value=[])
    stub.ensure_plan_vs_reality_columns = MagicMock()
    stub.ensure_planned_entry_price_column = MagicMock()
    return stub


if "database" not in sys.modules:
    sys.modules["database"] = _make_db_stub()

if "utils.formatting" not in sys.modules:
    _fmt_stub = types.ModuleType("utils.formatting")
    _fmt_stub.decimal_to_float = lambda x: x
    # Guard against clobbering an already-loaded real "utils" package (same
    # pattern as test_trade_service.py) — unconditionally overwriting
    # sys.modules["utils"] here silently split module state (e.g.
    # utils.pricing._market_regime_cache, BLG-BE-97 v8.8 ST-07) across two
    # live module instances whenever this file was collected after other
    # test files had already triggered a real `import utils.pricing`.
    if "utils" not in sys.modules:
        sys.modules["utils"] = types.ModuleType("utils")
    sys.modules["utils.formatting"] = _fmt_stub

import os
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend", "services"))

# Import the module directly, bypassing services/__init__.py
_pvr = importlib.import_module("plan_vs_reality_service")
_compute_entry_delta_pct = _pvr._compute_entry_delta_pct
compute_plan_vs_reality = _pvr.compute_plan_vs_reality


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _trade(entry_price=100.0, exit_price=110.0, planned_entry_price=None, exit_reason="target"):
    return {
        "entry_price": entry_price,
        "exit_price": exit_price,
        "planned_entry_price": planned_entry_price,
        "exit_reason": exit_reason,
        "position_id": "pos-1",
        "portfolio_id": "port-1",
    }


def _position(initial_stop=95.0, status="closed", position_state="exit_zone"):
    return {
        "initial_stop": initial_stop,
        "status": status,
        "position_state": position_state,
    }


def _plan(r_target=2.0, planned_stop_price=95.0, early_exit_conditions=None):
    return {
        "id": "plan-1",
        "r_target": r_target,
        "planned_stop_price": planned_stop_price,
        "early_exit_conditions": early_exit_conditions,
        "status": "active",
    }


# ---------------------------------------------------------------------------
# AC-03: _compute_entry_delta_pct unit tests
# ---------------------------------------------------------------------------

class TestComputeEntryDeltaPct(unittest.TestCase):

    def test_positive_delta_when_entry_above_planned(self):
        # bought at 102 vs planned 100 → +2.00%
        result = _compute_entry_delta_pct(102.0, 100.0)
        self.assertEqual(result, 2.0)

    def test_negative_delta_when_entry_below_planned(self):
        # bought at 98 vs planned 100 → -2.00%
        result = _compute_entry_delta_pct(98.0, 100.0)
        self.assertEqual(result, -2.0)

    def test_zero_delta_exact_match(self):
        result = _compute_entry_delta_pct(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_returns_none_when_planned_is_none(self):
        result = _compute_entry_delta_pct(102.0, None)
        self.assertIsNone(result)

    def test_returns_none_when_actual_is_none(self):
        result = _compute_entry_delta_pct(None, 100.0)
        self.assertIsNone(result)

    def test_returns_none_when_planned_is_zero(self):
        result = _compute_entry_delta_pct(100.0, 0.0)
        self.assertIsNone(result)

    def test_fractional_rounding_to_2dp(self):
        # 101.005 / 100.0 * 100 = 1.005 → rounds to 1.0 or 1.01
        result = _compute_entry_delta_pct(101.005, 100.0)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, float)
        # just verify it's rounded to 2 decimal places
        self.assertEqual(result, round(result, 2))


# ---------------------------------------------------------------------------
# AC-04: compute_plan_vs_reality returns entry_delta_pct (float) when populated
# ---------------------------------------------------------------------------

class TestComputePlanVsRealityWithPlannedEntry(unittest.TestCase):

    def test_entry_delta_pct_populated_when_planned_entry_set(self):
        trade = _trade(entry_price=102.0, planned_entry_price=100.0)
        position = _position(initial_stop=95.0)
        plan = _plan(r_target=2.0, planned_stop_price=95.0)

        result = compute_plan_vs_reality(trade, position, plan)

        self.assertIn("entry_delta_pct", result)
        self.assertAlmostEqual(result["entry_delta_pct"], 2.0)

    def test_r_achieved_and_r_delta_computed(self):
        # entry=100, exit=110, stop=95 → risk=5, gain=10 → R=2.0; target=2.0 → delta=0
        trade = _trade(entry_price=100.0, exit_price=110.0, planned_entry_price=100.0)
        position = _position(initial_stop=95.0)
        plan = _plan(r_target=2.0)

        result = compute_plan_vs_reality(trade, position, plan)

        self.assertEqual(result["r_achieved"], 2.0)
        self.assertEqual(result["r_delta"], 0.0)
        self.assertEqual(result["entry_delta_pct"], 0.0)

    def test_plan_linked_true(self):
        trade = _trade(entry_price=100.0, planned_entry_price=100.0)
        result = compute_plan_vs_reality(trade, _position(), _plan())
        self.assertTrue(result["plan_linked"])
        self.assertEqual(result["trade_plan_id"], "plan-1")

    def test_entry_deviation_flag_when_delta_exceeds_two_pct(self):
        # planned=100, actual=103 → delta=3% → should flag entry_deviation
        trade = _trade(entry_price=103.0, planned_entry_price=100.0)
        result = compute_plan_vs_reality(trade, _position(), _plan())
        self.assertEqual(result["plan_adherence_flag"], "entry_deviation")


# ---------------------------------------------------------------------------
# AC-05: existing trades without planned_entry_price → entry_delta_pct: null
# ---------------------------------------------------------------------------

class TestComputePlanVsRealityWithoutPlannedEntry(unittest.TestCase):

    def test_entry_delta_pct_is_none_when_planned_entry_absent(self):
        trade = _trade(entry_price=100.0, planned_entry_price=None)
        result = compute_plan_vs_reality(trade, _position(), _plan())
        self.assertIsNone(result["entry_delta_pct"])

    def test_no_error_when_planned_entry_absent(self):
        trade = _trade(entry_price=100.0, planned_entry_price=None)
        # should not raise
        try:
            result = compute_plan_vs_reality(trade, _position(), _plan())
        except Exception as e:
            self.fail(f"compute_plan_vs_reality raised unexpectedly: {e}")

    def test_other_fields_still_computed_without_planned_entry(self):
        # r_achieved and r_delta should still work when planned_entry absent
        trade = _trade(entry_price=100.0, exit_price=110.0, planned_entry_price=None)
        result = compute_plan_vs_reality(trade, _position(initial_stop=95.0), _plan(r_target=2.0))
        self.assertEqual(result["r_achieved"], 2.0)
        self.assertEqual(result["r_delta"], 0.0)
        self.assertIsNone(result["entry_delta_pct"])

    def test_entry_delta_pct_none_when_no_position(self):
        trade = _trade(entry_price=100.0, planned_entry_price=None)
        result = compute_plan_vs_reality(trade, None, _plan())
        self.assertIsNone(result["entry_delta_pct"])


# ---------------------------------------------------------------------------
# AC-02: planned_entry_price field present in compute_plan_vs_reality input
#         (verifies the service reads from trade dict, not a hardcoded None)
# ---------------------------------------------------------------------------

class TestPlannedEntryPriceReadFromTradeDict(unittest.TestCase):

    def test_reads_planned_entry_price_from_trade_dict(self):
        # Confirms compute_plan_vs_reality uses trade['planned_entry_price']
        trade = {
            "entry_price": 50.0,
            "exit_price": 55.0,
            "planned_entry_price": 48.0,
            "exit_reason": "target",
            "position_id": "pos-x",
            "portfolio_id": "port-x",
        }
        result = compute_plan_vs_reality(trade, _position(initial_stop=45.0), _plan(r_target=1.0))
        # delta = (50 - 48) / 48 * 100 = 4.17%
        expected = round((50.0 - 48.0) / 48.0 * 100, 2)
        self.assertEqual(result["entry_delta_pct"], expected)

    def test_planned_entry_from_dict_string_coerced_to_float(self):
        # Simulate Decimal/string value from DB row
        trade = _trade(entry_price="102.50", planned_entry_price="100.00")
        result = compute_plan_vs_reality(trade, _position(), _plan())
        self.assertAlmostEqual(result["entry_delta_pct"], 2.5)


if __name__ == "__main__":
    unittest.main()
