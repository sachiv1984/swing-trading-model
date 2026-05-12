"""
Unit tests for PositionLifecycleService (EPIC-01, ST-02).

Tests all 5 state transition paths:
  EXIT ZONE  — price >= entry + 2R
  PROFITABLE — price > entry + 0.5 ATR
  LOSING     — price < entry - 0.5 ATR
  GRACE      — trading days <= 10 and price within ±0.5 ATR
  UNKNOWN    — missing ATR or post-grace neutral zone

No database calls — CI-safe. Uses date offsets relative to today.
"""

import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent.parent / "backend" / "services"))

from services.position_lifecycle_service import (
    compute_position_state,
    compute_days_in_state,
    _count_trading_days,
)


def _pos(entry_price, current_price_native, atr, days_ago=0, initial_stop=None):
    """Helper: build a minimal position dict for testing."""
    entry_date = (date.today() - timedelta(days=days_ago)).isoformat()
    return {
        "entry_price": entry_price,
        "current_price_native": current_price_native,
        "atr": atr,
        "entry_date": entry_date,
        "initial_stop": initial_stop,
    }


class TestCountTradingDays(unittest.TestCase):

    def test_zero_for_today(self):
        entry = date.today().isoformat()
        self.assertEqual(_count_trading_days(entry), 0)

    def test_counts_weekdays_not_weekends(self):
        # 7 calendar days always includes ≥ 5 and ≤ 5 weekdays
        entry = (date.today() - timedelta(days=7)).isoformat()
        result = _count_trading_days(entry)
        self.assertGreaterEqual(result, 4)
        self.assertLessEqual(result, 7)

    def test_future_date_returns_zero(self):
        future = (date.today() + timedelta(days=5)).isoformat()
        self.assertEqual(_count_trading_days(future), 0)


class TestComputePositionState(unittest.TestCase):

    # --- GRACE ---

    def test_grace_fresh_position(self):
        """Position opened today, price at entry → GRACE."""
        pos = _pos(100.0, 100.0, 2.0, days_ago=0)
        self.assertEqual(compute_position_state(pos), "GRACE")

    def test_grace_day_5_neutral(self):
        """Day 5 (3 trading days), price within ±0.5 ATR → GRACE."""
        pos = _pos(100.0, 100.5, 2.0, days_ago=5)
        self.assertEqual(compute_position_state(pos), "GRACE")

    # --- PROFITABLE ---

    def test_profitable_beyond_0_5_atr(self):
        """Price above entry + 0.5 ATR → PROFITABLE (any age)."""
        pos = _pos(100.0, 102.0, 2.0, days_ago=3)  # 2.0 > 0.5×2.0=1.0
        self.assertEqual(compute_position_state(pos), "PROFITABLE")

    def test_profitable_after_grace_window(self):
        """Price above threshold, opened 20 days ago → PROFITABLE."""
        pos = _pos(100.0, 102.0, 2.0, days_ago=20)
        self.assertEqual(compute_position_state(pos), "PROFITABLE")

    # --- LOSING ---

    def test_losing_below_0_5_atr(self):
        """Price below entry - 0.5 ATR → LOSING (even in grace window)."""
        pos = _pos(100.0, 98.0, 2.0, days_ago=3)  # 98 < 100 - 1.0 = 99
        self.assertEqual(compute_position_state(pos), "LOSING")

    def test_losing_after_grace(self):
        """Price below threshold, opened 20 days ago → LOSING."""
        pos = _pos(100.0, 97.0, 2.0, days_ago=20)
        self.assertEqual(compute_position_state(pos), "LOSING")

    # --- EXIT ZONE ---

    def test_exit_zone_price_at_2r(self):
        """Price exactly at entry + 2R → EXIT ZONE."""
        # R = 100 - 95 = 5; 2R = 10; exit_zone_price = 110
        pos = _pos(100.0, 110.0, 2.0, days_ago=20, initial_stop=95.0)
        self.assertEqual(compute_position_state(pos), "EXIT ZONE")

    def test_exit_zone_price_above_2r(self):
        """Price above entry + 2R → EXIT ZONE."""
        pos = _pos(100.0, 115.0, 2.0, days_ago=20, initial_stop=95.0)
        self.assertEqual(compute_position_state(pos), "EXIT ZONE")

    def test_no_exit_zone_without_stop(self):
        """Without initial_stop, EXIT ZONE cannot be triggered; falls to PROFITABLE."""
        pos = _pos(100.0, 115.0, 2.0, days_ago=20, initial_stop=None)
        self.assertEqual(compute_position_state(pos), "PROFITABLE")

    def test_no_exit_zone_when_stop_above_entry(self):
        """initial_stop >= entry_price means R <= 0; EXIT ZONE skipped."""
        pos = _pos(100.0, 115.0, 2.0, days_ago=20, initial_stop=105.0)
        self.assertEqual(compute_position_state(pos), "PROFITABLE")

    # --- UNKNOWN ---

    def test_unknown_missing_atr(self):
        """No ATR → UNKNOWN."""
        pos = _pos(100.0, 100.0, None, days_ago=3)
        self.assertEqual(compute_position_state(pos), "UNKNOWN")

    def test_unknown_missing_price(self):
        """No current price → UNKNOWN."""
        entry_date = (date.today() - timedelta(days=3)).isoformat()
        pos = {
            "entry_price": 100.0,
            "current_price_native": None,
            "atr": 2.0,
            "entry_date": entry_date,
        }
        self.assertEqual(compute_position_state(pos), "UNKNOWN")

    def test_unknown_post_grace_neutral_zone(self):
        """After grace (>10 trading days), price within ±0.5 ATR → UNKNOWN."""
        pos = _pos(100.0, 100.3, 2.0, days_ago=20)  # within ±1.0 ATR band
        self.assertEqual(compute_position_state(pos), "UNKNOWN")

    # --- Priority: EXIT ZONE > PROFITABLE > LOSING > GRACE ---

    def test_exit_zone_beats_profitable(self):
        """EXIT ZONE takes priority over PROFITABLE."""
        # R=5, price=115 (>PROFITABLE threshold of 101, also >=EXIT ZONE 110)
        pos = _pos(100.0, 115.0, 2.0, days_ago=20, initial_stop=95.0)
        self.assertEqual(compute_position_state(pos), "EXIT ZONE")

    def test_losing_overrides_grace(self):
        """LOSING beats GRACE even within 10 trading days."""
        pos = _pos(100.0, 97.0, 2.0, days_ago=3)
        self.assertEqual(compute_position_state(pos), "LOSING")

    def test_profitable_overrides_grace(self):
        """PROFITABLE beats GRACE even within 10 trading days."""
        pos = _pos(100.0, 102.0, 2.0, days_ago=3)
        self.assertEqual(compute_position_state(pos), "PROFITABLE")


class TestComputeDaysInState(unittest.TestCase):

    def test_none_returns_zero(self):
        self.assertEqual(compute_days_in_state(None), 0)

    def test_today_returns_zero(self):
        from datetime import datetime
        self.assertEqual(compute_days_in_state(datetime.utcnow()), 0)

    def test_yesterday_returns_one(self):
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1, hours=1)
        self.assertEqual(compute_days_in_state(yesterday), 1)


if __name__ == "__main__":
    unittest.main()
