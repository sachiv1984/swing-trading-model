"""
ST-03 (BLG-FEAT-79, EPIC-03, v7.6): P&L Export <-> Trade Plan Closure
Reconciliation — Unit Tests

Tests reconcile_pnl_vs_trade_plans in isolation (pure function, plain
dict rows in, no database or network calls).

Spec: docs/specs/pnl_export_reconciliation.md §3 (Reconciliation Rules)
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Database stub is registered by tests/conftest.py (BLG-QA-20 / retired
# BLG-QA-73 auto-scan) — pnl_reconciliation_service imports from
# `database`, so it resolves against that stub at import time.
from services.pnl_reconciliation_service import reconcile_pnl_vs_trade_plans


def _trade(position_id, trade_id="th-1", ticker="AAPL"):
    return {"id": trade_id, "position_id": position_id, "ticker": ticker, "pnl": 100.0}


def _plan(position_id, status, plan_id="tp-1", ticker="AAPL"):
    return {"id": plan_id, "position_id": position_id, "status": status, "ticker": ticker}


class TestReconcilePnlVsTradePlans(unittest.TestCase):
    def test_no_mismatch_when_closed_plan_has_matching_trade_history(self):
        result = reconcile_pnl_vs_trade_plans(
            trade_history=[_trade("pos-1")],
            trade_plans=[_plan("pos-1", "closed")],
        )
        self.assertEqual(result["mismatches"], [])
        self.assertEqual(result["trade_history_count"], 1)
        self.assertEqual(result["trade_plans_closed_count"], 1)

    def test_no_mismatch_when_trade_history_has_no_linked_plan(self):
        result = reconcile_pnl_vs_trade_plans(
            trade_history=[_trade("pos-1")],
            trade_plans=[],
        )
        self.assertEqual(result["mismatches"], [])

    def test_flags_closed_plan_with_no_trade_history(self):
        result = reconcile_pnl_vs_trade_plans(
            trade_history=[],
            trade_plans=[_plan("pos-1", "closed", plan_id="tp-9")],
        )
        self.assertEqual(len(result["mismatches"]), 1)
        mismatch = result["mismatches"][0]
        self.assertEqual(mismatch["type"], "closed_plan_no_trade_history")
        self.assertEqual(mismatch["position_id"], "pos-1")
        self.assertEqual(mismatch["trade_plan_id"], "tp-9")

    def test_flags_trade_history_with_plan_not_closed(self):
        result = reconcile_pnl_vs_trade_plans(
            trade_history=[_trade("pos-1", trade_id="th-5")],
            trade_plans=[_plan("pos-1", "active", plan_id="tp-3")],
        )
        self.assertEqual(len(result["mismatches"]), 1)
        mismatch = result["mismatches"][0]
        self.assertEqual(mismatch["type"], "trade_history_plan_not_closed")
        self.assertEqual(mismatch["position_id"], "pos-1")
        self.assertEqual(mismatch["trade_history_id"], "th-5")
        self.assertEqual(mismatch["trade_plan_id"], "tp-3")
        self.assertEqual(mismatch["plan_status"], "active")

    def test_draft_plan_also_flagged_as_not_closed(self):
        result = reconcile_pnl_vs_trade_plans(
            trade_history=[_trade("pos-1")],
            trade_plans=[_plan("pos-1", "draft")],
        )
        self.assertEqual(len(result["mismatches"]), 1)
        self.assertEqual(result["mismatches"][0]["plan_status"], "draft")

    def test_trade_history_rows_without_position_id_are_ignored(self):
        result = reconcile_pnl_vs_trade_plans(
            trade_history=[_trade(None)],
            trade_plans=[],
        )
        self.assertEqual(result["mismatches"], [])
        self.assertEqual(result["trade_history_count"], 1)

    def test_plans_without_position_id_excluded_from_closed_count_and_checks(self):
        result = reconcile_pnl_vs_trade_plans(
            trade_history=[],
            trade_plans=[_plan(None, "closed")],
        )
        self.assertEqual(result["mismatches"], [])
        self.assertEqual(result["trade_plans_closed_count"], 0)

    def test_multiple_positions_mixed_outcomes(self):
        result = reconcile_pnl_vs_trade_plans(
            trade_history=[_trade("pos-1", trade_id="th-1"), _trade("pos-2", trade_id="th-2")],
            trade_plans=[
                _plan("pos-1", "closed", plan_id="tp-1"),
                _plan("pos-2", "active", plan_id="tp-2"),
                _plan("pos-3", "closed", plan_id="tp-3"),
            ],
        )
        types_found = sorted(m["type"] for m in result["mismatches"])
        self.assertEqual(types_found, ["closed_plan_no_trade_history", "trade_history_plan_not_closed"])
        self.assertEqual(result["trade_plans_closed_count"], 2)


if __name__ == "__main__":
    unittest.main()
