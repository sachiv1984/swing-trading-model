"""
Unit tests for PositionLifecycleService (EPIC-01, ST-02).

Tests all 5 state transition paths:
  EXIT ZONE  — price >= entry + 2R
  PROFITABLE — price > entry + 0.5 ATR
  LOSING     — price < entry - 0.5 ATR
  GRACE      — fewer than 10 calendar days since entry, whatever the price
               (ST-12, BLG-FE-196, v9.10: grace precedence, calendar days)
  UNKNOWN    — missing data or post-grace neutral zone, with lifecycle_reason

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
    compute_lifecycle_reason,
    compute_days_in_state,
    _count_calendar_days,
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


class TestCountCalendarDays(unittest.TestCase):

    def test_zero_for_today(self):
        entry = date.today().isoformat()
        self.assertEqual(_count_calendar_days(entry), 0)

    def test_counts_calendar_days_including_weekends(self):
        entry = (date.today() - timedelta(days=7)).isoformat()
        self.assertEqual(_count_calendar_days(entry), 7)

    def test_future_date_returns_zero(self):
        future = (date.today() + timedelta(days=5)).isoformat()
        self.assertEqual(_count_calendar_days(future), 0)

    def test_unparseable_returns_none(self):
        self.assertIsNone(_count_calendar_days(None))
        self.assertIsNone(_count_calendar_days("not-a-date"))


class TestComputePositionState(unittest.TestCase):

    # --- GRACE ---

    def test_grace_fresh_position(self):
        """Position opened today, price at entry → GRACE."""
        pos = _pos(100.0, 100.0, 2.0, days_ago=0)
        self.assertEqual(compute_position_state(pos), "GRACE")

    def test_grace_day_5_neutral(self):
        """Day 5, price within ±0.5 ATR → GRACE."""
        pos = _pos(100.0, 100.5, 2.0, days_ago=5)
        self.assertEqual(compute_position_state(pos), "GRACE")

    # --- PROFITABLE ---

    def test_profitable_beyond_0_5_atr(self):
        """Post-grace, price above entry + 0.5 ATR → PROFITABLE."""
        pos = _pos(100.0, 102.0, 2.0, days_ago=10)  # 2.0 > 0.5×2.0=1.0
        self.assertEqual(compute_position_state(pos), "PROFITABLE")

    def test_profitable_after_grace_window(self):
        """Price above threshold, opened 20 days ago → PROFITABLE."""
        pos = _pos(100.0, 102.0, 2.0, days_ago=20)
        self.assertEqual(compute_position_state(pos), "PROFITABLE")

    # --- LOSING ---

    def test_losing_below_0_5_atr(self):
        """Post-grace (day 10), price below entry - 0.5 ATR → LOSING."""
        pos = _pos(100.0, 98.0, 2.0, days_ago=10)  # 98 < 100 - 1.0 = 99
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
        """Post-grace, no ATR → UNKNOWN."""
        pos = _pos(100.0, 100.0, None, days_ago=12)
        self.assertEqual(compute_position_state(pos), "UNKNOWN")

    def test_unknown_missing_price(self):
        """No current price → UNKNOWN."""
        entry_date = (date.today() - timedelta(days=12)).isoformat()
        pos = {
            "entry_price": 100.0,
            "current_price_native": None,
            "atr": 2.0,
            "entry_date": entry_date,
        }
        self.assertEqual(compute_position_state(pos), "UNKNOWN")

    def test_unknown_post_grace_neutral_zone(self):
        """After grace (day 10+), price within ±0.5 ATR → UNKNOWN."""
        pos = _pos(100.0, 100.3, 2.0, days_ago=20)  # within ±1.0 ATR band
        self.assertEqual(compute_position_state(pos), "UNKNOWN")

    # --- Priority: GRACE > EXIT ZONE > PROFITABLE > LOSING ---

    def test_exit_zone_beats_profitable(self):
        """EXIT ZONE takes priority over PROFITABLE."""
        # R=5, price=115 (>PROFITABLE threshold of 101, also >=EXIT ZONE 110)
        pos = _pos(100.0, 115.0, 2.0, days_ago=20, initial_stop=95.0)
        self.assertEqual(compute_position_state(pos), "EXIT ZONE")

    def test_grace_overrides_losing(self):
        """ST-12: in grace, a position > 0.5 ATR below entry is still GRACE."""
        pos = _pos(100.0, 97.0, 2.0, days_ago=3)
        self.assertEqual(compute_position_state(pos), "GRACE")

    def test_grace_overrides_profitable_and_exit_zone(self):
        """ST-12: in grace, a position at 2R is still GRACE."""
        pos = _pos(100.0, 115.0, 2.0, days_ago=3, initial_stop=95.0)
        self.assertEqual(compute_position_state(pos), "GRACE")

    def test_grace_boundary_day_9_vs_day_10(self):
        """ST-12: matches GET /positions' grace_period (holding_days < 10)."""
        self.assertEqual(compute_position_state(_pos(100.0, 97.0, 2.0, days_ago=9)), "GRACE")
        self.assertEqual(compute_position_state(_pos(100.0, 97.0, 2.0, days_ago=10)), "LOSING")

    def test_grace_without_atr_is_grace(self):
        """ST-12: missing ATR does not override grace."""
        self.assertEqual(compute_position_state(_pos(100.0, 100.0, None, days_ago=2)), "GRACE")


class TestLifecycleReason(unittest.TestCase):
    """ST-12: the reason an UNKNOWN badge is UNKNOWN."""

    def test_missing_atr_after_grace(self):
        self.assertEqual(compute_lifecycle_reason(_pos(100.0, 100.0, None, days_ago=12)), "missing_data")

    def test_missing_entry_date(self):
        pos = _pos(100.0, 100.0, 2.0)
        pos["entry_date"] = None
        self.assertEqual(compute_lifecycle_reason(pos), "missing_data")

    def test_flat_after_grace(self):
        self.assertEqual(compute_lifecycle_reason(_pos(100.0, 100.3, 2.0, days_ago=20)), "flat_after_grace")

    def test_null_for_known_states(self):
        self.assertIsNone(compute_lifecycle_reason(_pos(100.0, 97.0, 2.0, days_ago=3)))
        self.assertIsNone(compute_lifecycle_reason(_pos(100.0, 97.0, 2.0, days_ago=20)))


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
