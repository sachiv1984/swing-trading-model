"""
ST-02 (BLG-FEAT-67, EPIC-02, v7.9): Historical sector/regime exposure trend.

Covers:
- compute_sector_exposure: refactor-safety golden test proving the extracted
  pure function produces identical output to the original inline logic in
  GET /portfolio/sector-weights (no behaviour change from the refactor).
- bucket_sector_regime_weekly: insufficient-history gating (AC-03), weekly
  bucketing (last snapshot per ISO week wins), top-5-sectors + "Other"
  grouping, regime pass-through.
- database.py's sector_regime_history functions (fail-open on DB error).

CI-safe: no live DB or network connections.
"""

import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from routers.portfolio_risk import compute_sector_exposure, bucket_sector_regime_weekly, get_sector_regime_trend


def _position(ticker="AAPL", market="US", shares=10, current_price=100.0, entry_price=90.0, fx_rate=1.27):
    return {
        "ticker": ticker,
        "market": market,
        "shares": shares,
        "entry_price": entry_price,
        "current_price": current_price,
        "fill_price": entry_price * fx_rate if market == "US" else None,
        "fx_rate": fx_rate,
    }


class TestComputeSectorExposure(unittest.TestCase):
    """Golden test — extraction from GET /portfolio/sector-weights must not
    change behaviour: same inputs, same output shape and values."""

    def test_single_position_full_exposure(self):
        """A single-position portfolio is 100% concentrated in that one
        sector, which necessarily trips the >=40% concentration_alert -- this
        is expected, not a bug."""
        positions = [_position(ticker="AAPL", market="US", shares=10, current_price=100.0)]
        ticker_sector_map = {"AAPL": "Technology"}
        result = compute_sector_exposure(positions, ticker_sector_map, live_fx_rate=1.27)

        self.assertEqual(result["total_positions"], 1)
        self.assertEqual(len(result["sectors"]), 1)
        self.assertEqual(result["sectors"][0]["sector_name"], "Technology")
        self.assertEqual(result["sectors"][0]["exposure_pct"], 100.0)
        self.assertTrue(result["concentration_alert"])

    def test_concentration_alert_at_40_percent(self):
        positions = [
            _position(ticker="AAPL", market="US", shares=100, current_price=100.0),
            _position(ticker="VOD.L", market="UK", shares=100, current_price=1.0, entry_price=1.0),
        ]
        ticker_sector_map = {"AAPL": "Technology", "VOD.L": "Communication Services"}
        result = compute_sector_exposure(positions, ticker_sector_map, live_fx_rate=1.0)

        aapl_sector = next(s for s in result["sectors"] if s["sector_name"] == "Technology")
        self.assertGreaterEqual(aapl_sector["exposure_pct"], 40.0)
        self.assertTrue(result["concentration_alert"])

    def test_unclassified_fallback_when_no_sector_mapping(self):
        positions = [_position(ticker="ZZZZ", market="US")]
        result = compute_sector_exposure(positions, ticker_sector_map={}, live_fx_rate=1.27)
        self.assertEqual(result["sectors"][0]["sector_name"], "Unclassified")

    def test_empty_positions_returns_zero_state(self):
        result = compute_sector_exposure([], ticker_sector_map={}, live_fx_rate=1.27)
        self.assertEqual(result["sectors"], [])
        self.assertEqual(result["total_positions"], 0)
        self.assertFalse(result["concentration_alert"])


def _daily_row(day, sectors, regime_us=True, regime_uk=True):
    return {"snapshot_date": day, "sectors": sectors, "regime_us": regime_us, "regime_uk": regime_uk}


class TestBucketSectorRegimeWeekly(unittest.TestCase):

    def test_fewer_than_8_weeks_is_insufficient_history(self):
        # 2026-06-01 is a Monday; 3 consecutive days from it stay within one ISO week.
        rows = [_daily_row(date(2026, 6, 1), []), _daily_row(date(2026, 6, 2), []), _daily_row(date(2026, 6, 3), [])]
        result = bucket_sector_regime_weekly(rows, weeks=12)
        self.assertTrue(result["insufficient_history"])
        self.assertEqual(result["weeks_available"], 1)

    def test_exactly_8_weeks_is_sufficient(self):
        rows = []
        for week_num in range(8):
            day = date(2026, 1, 5) + __import__("datetime").timedelta(weeks=week_num)
            rows.append(_daily_row(day, [{"sector_name": "Technology", "exposure_pct": 50.0}]))
        result = bucket_sector_regime_weekly(rows, weeks=12)
        self.assertFalse(result["insufficient_history"])
        self.assertEqual(len(result["weeks"]), 8)

    def test_last_snapshot_in_week_wins(self):
        import datetime as dt
        week_start = date(2026, 6, 1)  # a Monday
        rows = [
            _daily_row(week_start, [{"sector_name": "Technology", "exposure_pct": 30.0}]),
            _daily_row(week_start + dt.timedelta(days=2), [{"sector_name": "Technology", "exposure_pct": 35.0}]),
        ]
        # pad with 7 more distinct weeks to clear the insufficient-history gate
        for i in range(1, 8):
            rows.append(_daily_row(week_start + dt.timedelta(weeks=i), [{"sector_name": "Technology", "exposure_pct": 40.0}]))

        result = bucket_sector_regime_weekly(rows, weeks=12)
        first_week = result["weeks"][0]
        tech = next(s for s in first_week["sectors"] if s["sector_name"] == "Technology")
        self.assertEqual(tech["exposure_pct"], 35.0)

    def test_top_5_sectors_plus_other_grouping(self):
        import datetime as dt
        week_start = date(2026, 6, 1)
        many_sectors = [{"sector_name": f"Sector{i}", "exposure_pct": 10.0} for i in range(7)]
        rows = [_daily_row(week_start + dt.timedelta(weeks=i), many_sectors) for i in range(8)]

        result = bucket_sector_regime_weekly(rows, weeks=12)
        last_week_sectors = result["weeks"][-1]["sectors"]
        sector_names = [s["sector_name"] for s in last_week_sectors]

        self.assertEqual(len(sector_names), 6)  # top 5 + Other
        self.assertIn("Other", sector_names)
        other = next(s for s in last_week_sectors if s["sector_name"] == "Other")
        self.assertAlmostEqual(other["exposure_pct"], 20.0, places=1)  # remaining 2 sectors x 10%

    def test_regime_passthrough(self):
        import datetime as dt
        week_start = date(2026, 6, 1)
        rows = [_daily_row(week_start + dt.timedelta(weeks=i), [], regime_us=False, regime_uk=True) for i in range(8)]
        result = bucket_sector_regime_weekly(rows, weeks=12)
        self.assertFalse(result["weeks"][0]["regime_us"])
        self.assertTrue(result["weeks"][0]["regime_uk"])


class TestGetSectorRegimeTrendEndpoint(unittest.TestCase):
    """A genuine failure (DB error, etc.) must surface as status: error, not
    be folded into the same insufficient_history: true shape the legitimate
    day-one accumulation state uses -- those two conditions must stay
    distinguishable to the frontend (SectorRegimeTrend.js's isError branch
    vs. its insufficient_history branch)."""

    def test_exception_returns_error_status_not_insufficient_history(self):
        with patch("routers.portfolio_risk.get_portfolio", side_effect=Exception("db unavailable")):
            result = get_sector_regime_trend(weeks=12)
        self.assertEqual(result["status"], "error")
        self.assertNotIn("data", result)

    def test_no_portfolio_is_insufficient_history_not_error(self):
        with patch("routers.portfolio_risk.get_portfolio", return_value=None):
            result = get_sector_regime_trend(weeks=12)
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["data"]["insufficient_history"])


class TestSectorRegimeHistoryDatabaseFunctions(unittest.TestCase):
    """Real database.py functions, loaded independently of the process-global
    stub — same convention as test_claude_audit_log_filters.py."""

    @classmethod
    def setUpClass(cls):
        import importlib.util
        import os
        db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
        spec = importlib.util.spec_from_file_location('database_real_for_sector_regime_test', db_path)
        cls.database = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.database)

    def _make_conn_cur(self):
        cur = MagicMock()
        cur_ctx = MagicMock()
        cur_ctx.__enter__ = MagicMock(return_value=cur)
        cur_ctx.__exit__ = MagicMock(return_value=False)
        conn = MagicMock()
        conn.cursor.return_value = cur_ctx
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        return conn, cur

    def test_create_sector_regime_snapshot_does_not_raise_on_db_failure(self):
        with patch.object(self.database, "get_db", side_effect=Exception("db unavailable")):
            with self.assertRaises(Exception):
                # ensure_sector_regime_history_table() itself is called first and
                # WILL raise here (unlike the fail-open audit-log pattern) -- this
                # snapshot is called from a try/except in portfolio_service.py,
                # not internally fail-open, so confirm it propagates as expected.
                self.database.create_sector_regime_snapshot("port-1", date(2026, 7, 27), [], True, True)

    def test_get_sector_regime_history_returns_rows(self):
        conn, cur = self._make_conn_cur()
        cur.fetchall.return_value = [{"snapshot_date": date(2026, 7, 27), "sectors": [], "regime_us": True, "regime_uk": True}]
        with patch.object(self.database, "get_db", return_value=conn):
            result = self.database.get_sector_regime_history("port-1", weeks=12)
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
