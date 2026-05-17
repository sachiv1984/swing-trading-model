"""
ST-07: Fee Drag Backend Unit Tests — trade_service.get_trade_history_with_stats()

Covers SC-FEE-05 and SC-FEE-06 from docs/testing/fee-drag-scenarios.md v1.0.

SC-FEE-05: fee_drag_pct formula: exit_fees / gross_proceeds * 100 (or None when inputs invalid)
SC-FEE-06: avg_fee_drag_pct aggregation (mean of non-null values, or None)

All DB calls are stubbed at import time — no live database required.
Uses the same sys.modules contamination-safe stub pattern as test_alerts_service.py.
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch

import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# ---------------------------------------------------------------------------
# Minimal sys.modules stubs — must be registered before any backend import.
# Mirrors the pattern in test_alerts_service.py to avoid collection cascades.
# ---------------------------------------------------------------------------

if "database" not in sys.modules:
    _db_stub = types.ModuleType("database")
    sys.modules["database"] = _db_stub
else:
    _db_stub = sys.modules["database"]

for _fn in (
    "get_db", "get_portfolio", "get_positions", "update_position",
    "create_position", "update_portfolio_cash", "get_settings",
    "create_trade_history", "update_position_note", "update_position_tags",
    "get_all_tags", "search_positions_by_tags", "get_trade_history",
    "get_trade_history_by_tax_year", "create_cash_transaction",
    "get_cash_transactions", "get_total_deposits_withdrawals",
    "create_portfolio_snapshot", "get_portfolio_snapshots",
    "get_latest_snapshot", "create_signal", "get_signals",
    "update_signal", "delete_signal", "get_all_tickers",
    "get_peak_portfolio_value", "get_all_closed_trades_for_csv_export",
    "get_trade_reflection", "upsert_trade_reflection",
    "get_database_size_bytes", "delete_position",
    "download_ticker_data", "compute_atr_simple", "create_settings", "update_settings",
    "get_trade_plans_by_position", "ensure_planned_entry_price_column",
):
    if not hasattr(_db_stub, _fn):
        setattr(_db_stub, _fn, MagicMock())

if "utils.pricing" not in sys.modules:
    _pricing_stub = types.ModuleType("utils.pricing")
    sys.modules["utils.pricing"] = _pricing_stub
for _fn in ("check_market_regime", "get_current_price", "get_live_fx_rate", "calculate_atr"):
    if not hasattr(sys.modules["utils.pricing"], _fn):
        setattr(sys.modules["utils.pricing"], _fn, MagicMock())

if "utils.calculations" not in sys.modules:
    _calcs_stub = types.ModuleType("utils.calculations")
    sys.modules["utils.calculations"] = _calcs_stub
for _fn in (
    "calculate_initial_stop", "calculate_trailing_stop", "calculate_position_pnl",
    "calculate_holding_days", "calculate_uk_entry_fees", "calculate_us_entry_fees",
    "calculate_uk_exit_fees", "calculate_us_exit_fees", "calculate_position_size",
    "calculate_realized_pnl", "should_exit_position", "calculate_exit_proceeds",
    "calculate_portfolio_pnl",
):
    if not hasattr(sys.modules["utils.calculations"], _fn):
        setattr(sys.modules["utils.calculations"], _fn, MagicMock())

if "utils.formatting" not in sys.modules:
    _fmt_stub = types.ModuleType("utils.formatting")
    sys.modules["utils.formatting"] = _fmt_stub
if not hasattr(sys.modules["utils.formatting"], "decimal_to_float"):
    sys.modules["utils.formatting"].decimal_to_float = MagicMock(side_effect=lambda x: x)

# Register utils as a package with submodule attributes
if "utils" not in sys.modules:
    sys.modules["utils"] = types.ModuleType("utils")
sys.modules["utils"].pricing = sys.modules["utils.pricing"]
sys.modules["utils"].calculations = sys.modules["utils.calculations"]
sys.modules["utils"].formatting = sys.modules["utils.formatting"]

# ---------------------------------------------------------------------------
# Import the module under test
# ---------------------------------------------------------------------------

from services.trade_service import get_trade_history_with_stats  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PORTFOLIO = {"id": "port-1"}


def _make_trade(**kwargs):
    """Return a minimal raw trade dict. Keyword args override defaults."""
    base = {
        "id": "t1",
        "ticker": "LGEN",
        "market": "UK",
        "entry_date": "2026-03-01",
        "exit_date": "2026-03-15",
        "shares": 100,
        "entry_price": 200.00,
        "exit_price": 220.00,
        "pnl": 1990.05,
        "pnl_pct": 9.95,
        "holding_days": 14,
        "exit_reason": "Target Reached",
        "entry_note": None,
        "exit_note": None,
        "tags": [],
        "fill_price": None,
        "exit_fees": None,
        "gross_proceeds": None,
    }
    base.update(kwargs)
    return base


# ---------------------------------------------------------------------------
# SC-FEE-05 — fee_drag_pct formula correctness
# ---------------------------------------------------------------------------

class TestFeeDragFormula(unittest.TestCase):
    """SC-FEE-05: fee_drag_pct = round(exit_fees / gross_proceeds * 100, 2)"""

    def _get_fee_drag(self, exit_fees, gross_proceeds):
        """Call get_trade_history_with_stats with one trade and return its fee_drag_pct."""
        trade = _make_trade(exit_fees=exit_fees, gross_proceeds=gross_proceeds)
        with (
            patch('services.trade_service.get_portfolio', return_value=PORTFOLIO),
            patch('services.trade_service.get_trade_history', return_value=[trade]),
        ):
            result = get_trade_history_with_stats()
        return result["trades"][0]["fee_drag_pct"]

    def test_standard_case(self):
        """exit_fees=9.95, gross_proceeds=2200.00 → fee_drag_pct = 0.45"""
        val = self._get_fee_drag(exit_fees=9.95, gross_proceeds=2200.00)
        self.assertEqual(val, 0.45)

    def test_zero_exit_fees(self):
        """exit_fees=0, gross_proceeds=1000 → fee_drag_pct = 0.0"""
        val = self._get_fee_drag(exit_fees=0, gross_proceeds=1000.00)
        self.assertEqual(val, 0.0)

    def test_exit_fees_none(self):
        """exit_fees=None → fee_drag_pct = None"""
        val = self._get_fee_drag(exit_fees=None, gross_proceeds=1000.00)
        self.assertIsNone(val)

    def test_gross_proceeds_none(self):
        """gross_proceeds=None → fee_drag_pct = None"""
        val = self._get_fee_drag(exit_fees=9.95, gross_proceeds=None)
        self.assertIsNone(val)

    def test_gross_proceeds_zero(self):
        """gross_proceeds=0 → fee_drag_pct = None (division guard)"""
        val = self._get_fee_drag(exit_fees=9.95, gross_proceeds=0)
        self.assertIsNone(val)

    def test_both_none(self):
        """Both None → fee_drag_pct = None"""
        val = self._get_fee_drag(exit_fees=None, gross_proceeds=None)
        self.assertIsNone(val)

    def test_rounding_to_2dp(self):
        """Result is rounded to exactly 2 decimal places."""
        # exit_fees=1.00, gross_proceeds=300.00 → 0.3333... → rounds to 0.33
        val = self._get_fee_drag(exit_fees=1.00, gross_proceeds=300.00)
        self.assertEqual(val, round(val, 2))
        self.assertAlmostEqual(val, 0.33, places=2)

    def test_return_type_float_when_calculable(self):
        """fee_drag_pct is float (not Decimal/str) when calculable."""
        val = self._get_fee_drag(exit_fees=9.95, gross_proceeds=2200.00)
        self.assertIsInstance(val, float)

    def test_return_type_none_when_not_calculable(self):
        """fee_drag_pct is exactly None when inputs are missing."""
        val = self._get_fee_drag(exit_fees=None, gross_proceeds=None)
        self.assertIsNone(val)


# ---------------------------------------------------------------------------
# SC-FEE-06 — avg_fee_drag_pct aggregation
# ---------------------------------------------------------------------------

class TestAvgFeeDragAggregation(unittest.TestCase):
    """SC-FEE-06: avg_fee_drag_pct = round(mean of non-null fee_drag_pct values, 2)"""

    def _run(self, trades_raw):
        with (
            patch('services.trade_service.get_portfolio', return_value=PORTFOLIO),
            patch('services.trade_service.get_trade_history', return_value=trades_raw),
        ):
            return get_trade_history_with_stats()

    def test_two_trades_with_fee_drag(self):
        """avg of 0.45 and 0.25 = 0.35"""
        trades = [
            _make_trade(id="t1", ticker="LGEN", exit_fees=9.95, gross_proceeds=2200.00),
            _make_trade(id="t2", ticker="VOD",  exit_fees=4.25, gross_proceeds=1700.00),
        ]
        result = self._run(trades)
        # 9.95/2200*100 = 0.45; 4.25/1700*100 = 0.25; avg = 0.35
        self.assertEqual(result["avg_fee_drag_pct"], 0.35)

    def test_all_null_fee_drag(self):
        """All trades have null fee_drag_pct → avg_fee_drag_pct = None"""
        trades = [
            _make_trade(id="t1", exit_fees=None, gross_proceeds=None),
            _make_trade(id="t2", exit_fees=None, gross_proceeds=None),
        ]
        result = self._run(trades)
        self.assertIsNone(result["avg_fee_drag_pct"])

    def test_empty_trade_list(self):
        """No trades at all → avg_fee_drag_pct = None"""
        with (
            patch('services.trade_service.get_portfolio', return_value=PORTFOLIO),
            patch('services.trade_service.get_trade_history', return_value=[]),
        ):
            result = get_trade_history_with_stats()
        self.assertIsNone(result["avg_fee_drag_pct"])

    def test_mixed_null_and_non_null(self):
        """Only non-null values contribute to the average."""
        trades = [
            _make_trade(id="t1", ticker="LGEN", exit_fees=9.95, gross_proceeds=2200.00),  # 0.45
            _make_trade(id="t2", ticker="BARC", exit_fees=None, gross_proceeds=None),      # null
        ]
        result = self._run(trades)
        # avg is 0.45 only (BARC excluded)
        self.assertEqual(result["avg_fee_drag_pct"], 0.45)

    def test_single_trade_non_null(self):
        """Single trade with valid fee drag → avg equals that trade's value."""
        trades = [_make_trade(exit_fees=9.95, gross_proceeds=2200.00)]
        result = self._run(trades)
        self.assertEqual(result["avg_fee_drag_pct"], 0.45)

    def test_avg_rounded_to_2dp(self):
        """avg_fee_drag_pct is rounded to 2 decimal places."""
        trades = [
            _make_trade(id="t1", exit_fees=1.00, gross_proceeds=300.00),   # 0.3333...
            _make_trade(id="t2", exit_fees=2.00, gross_proceeds=300.00),   # 0.6666...
        ]
        result = self._run(trades)
        val = result["avg_fee_drag_pct"]
        self.assertIsNotNone(val)
        self.assertEqual(round(val, 2), val)

    def test_avg_field_always_present_in_result(self):
        """avg_fee_drag_pct key is always present in the return dict."""
        trades = [_make_trade(exit_fees=9.95, gross_proceeds=2200.00)]
        result = self._run(trades)
        self.assertIn("avg_fee_drag_pct", result)

    def test_avg_field_present_when_null(self):
        """avg_fee_drag_pct key present (value None) even when no fee data."""
        trades = [_make_trade(exit_fees=None, gross_proceeds=None)]
        result = self._run(trades)
        self.assertIn("avg_fee_drag_pct", result)
        self.assertIsNone(result["avg_fee_drag_pct"])


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
