"""
ST-13: Service Layer Test Coverage — Tier 1 Pure-Math Services

Tests for service-layer functions that contain calculations derived from
canonical specifications and have no database dependencies.

Tier 1 scope (v1.9):
    - services/grace_service.py
    - services/drawdown_service.py

Coverage standard: ≥80% line coverage on Tier 1 modules.
Measured by: pytest-cov with module-scoped --cov flags (see golden-outputs.yml).

Spec refs:
    - grace_service:    position_endpoints.md v1.8.3 (grace_days_remaining formula)
    - drawdown_service: metrics_definitions.md v1.5.8 §Current Drawdown

All tests are CI-safe: no database calls, no HTTP calls.
DB calls in drawdown_service are patched via unittest.mock.
"""

import sys
import unittest
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Path setup: allow importing from backend/services directly
# ---------------------------------------------------------------------------

import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.grace_service import compute_grace_days_remaining
from services.drawdown_service import get_drawdown_fields


# ---------------------------------------------------------------------------
# grace_service — compute_grace_days_remaining
# Canonical spec: position_endpoints.md v1.8.3
#
# Rules:
#   grace_period=True  → max(0, 10 − holding_days)
#   grace_period=False → None
# CRITICAL: day 10 = post-grace (grace_period=False) → None, NOT 0
# ---------------------------------------------------------------------------

class TestGraceService(unittest.TestCase):

    def test_grace_day_0_returns_10(self):
        """Position entered today (holding_days=0) has 10 days remaining."""
        self.assertEqual(compute_grace_days_remaining(True, 0), 10)

    def test_grace_day_1_returns_9(self):
        self.assertEqual(compute_grace_days_remaining(True, 1), 9)

    def test_grace_day_5_returns_5(self):
        """Midpoint: 5 days held, 5 remaining."""
        self.assertEqual(compute_grace_days_remaining(True, 5), 5)

    def test_grace_day_9_returns_1(self):
        """Last day of grace window."""
        self.assertEqual(compute_grace_days_remaining(True, 9), 1)

    def test_grace_day_10_in_grace_returns_0(self):
        """
        Edge case: grace_period=True with holding_days=10.
        Formula: max(0, 10-10) = 0.
        Note: in production, grace_period is False by day 10 (A-QA-05).
        This tests the mathematical branch only.
        """
        self.assertEqual(compute_grace_days_remaining(True, 10), 0)

    def test_grace_day_15_clamps_to_0(self):
        """Formula clamps at 0 — no negative values returned."""
        self.assertEqual(compute_grace_days_remaining(True, 15), 0)

    def test_not_in_grace_returns_none(self):
        """grace_period=False always returns None regardless of holding_days."""
        self.assertIsNone(compute_grace_days_remaining(False, 0))
        self.assertIsNone(compute_grace_days_remaining(False, 5))
        self.assertIsNone(compute_grace_days_remaining(False, 10))
        self.assertIsNone(compute_grace_days_remaining(False, 100))

    def test_return_type_is_int_when_in_grace(self):
        """Return type is int (not float) when grace_period=True."""
        result = compute_grace_days_remaining(True, 3)
        self.assertIsInstance(result, int)

    def test_return_type_is_none_when_not_in_grace(self):
        result = compute_grace_days_remaining(False, 3)
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# drawdown_service — get_drawdown_fields
# Canonical spec: metrics_definitions.md v1.5.8 §Current Drawdown
#
# Formula:
#   current_drawdown_percent = (current_total_value − peak) / peak × 100
#   peak = MAX(portfolio_history.total_value) [all-time]
#
# Contract:
#   - current_drawdown_percent is always ≤ 0.0
#   - Both fields default to 0.0 when no portfolio_history exists (peak=0.0)
# ---------------------------------------------------------------------------

PORTFOLIO_ID = "test-portfolio-1"


class TestDrawdownService(unittest.TestCase):

    def test_no_history_returns_zero_fields(self):
        """When no portfolio_history exists (peak=0.0), both fields return 0.0."""
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=0.0):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=10000.0)
        self.assertEqual(result['current_drawdown_percent'], 0.0)
        self.assertEqual(result['peak_portfolio_value'], 0.0)

    def test_at_peak_returns_zero_drawdown(self):
        """Portfolio at its all-time high: drawdown = 0.0%."""
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=10000.0):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=10000.0)
        self.assertEqual(result['current_drawdown_percent'], 0.0)
        self.assertEqual(result['peak_portfolio_value'], 10000.0)

    def test_10pct_drawdown(self):
        """£9,000 current vs £10,000 peak → -10.0%."""
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=10000.0):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=9000.0)
        self.assertEqual(result['current_drawdown_percent'], -10.0)
        self.assertEqual(result['peak_portfolio_value'], 10000.0)

    def test_50pct_drawdown(self):
        """£5,000 current vs £10,000 peak → -50.0%."""
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=10000.0):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=5000.0)
        self.assertEqual(result['current_drawdown_percent'], -50.0)

    def test_drawdown_is_never_positive(self):
        """
        Guard: if current_total_value > peak (snapshot timing edge case),
        result is clamped to 0.0 — never positive.
        """
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=9900.0):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=10000.0)
        self.assertLessEqual(result['current_drawdown_percent'], 0.0)

    def test_result_fields_always_present(self):
        """Both fields must always be present in the returned dict."""
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=10000.0):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=8000.0)
        self.assertIn('current_drawdown_percent', result)
        self.assertIn('peak_portfolio_value', result)

    def test_drawdown_rounding_4dp(self):
        """current_drawdown_percent rounded to 4 decimal places per spec."""
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=10000.0):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=9999.0)
        # -0.01% = -0.0100. Check at most 4 dp.
        val = result['current_drawdown_percent']
        self.assertEqual(round(val, 4), val)

    def test_peak_rounded_2dp(self):
        """peak_portfolio_value rounded to 2 decimal places."""
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=10000.123456):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=10000.0)
        self.assertEqual(result['peak_portfolio_value'], round(10000.123456, 2))

    def test_boundary_fractional_drawdown(self):
        """Fractional drawdown: £9,990 vs £10,000 peak → -0.1%."""
        with patch('services.drawdown_service.get_peak_portfolio_value', return_value=10000.0):
            result = get_drawdown_fields(PORTFOLIO_ID, current_total_value=9990.0)
        self.assertAlmostEqual(result['current_drawdown_percent'], -0.1, places=3)


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
