"""
ST-09 (BLG-BE-205, EPIC-04, v9.17; data_model.md DS-40): the nightly job records
when it last moved each position's stop, and the stop before that move.

Acceptance criteria (stage4_backlog_slice.md ST-09):
  - After a nightly run that raises a stop, stop_last_moved_date is that run's
    date and previous_stop is the stop before the move.
  - A run that leaves the stop unchanged leaves both fields unchanged.
  - GET /positions returns both, read-only.

The real stop arithmetic (calculate_trailing_stop, calculate_holding_days) is
loaded from its file, as in tests/test_atr_provenance.py.
"""
import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

BACKEND = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(BACKEND))

_spec = importlib.util.spec_from_file_location(
    "_real_calculations_st09_v917", BACKEND / "utils" / "calculations.py"
)
real_calcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(real_calcs)

import services.position_service as position_service  # noqa: E402


def _open_position(**overrides):
    base = {
        "id": "pos-1",
        "portfolio_id": "portfolio-1",
        "ticker": "VOD.L",
        "market": "UK",
        "entry_date": date.today() - timedelta(days=30),
        "entry_price": 100.0,
        "fill_price": None,
        "fx_rate": 1.0,
        "shares": 10.0,
        "current_stop": 80.0,
        "initial_stop": 75.0,
        "atr": 5.0,
        "atr_source": "fetched",
        "total_cost": 1000.0,
        "status": "open",
        "entry_note": None,
        "exit_note": None,
        "tags": [],
        "last_reviewed_at": None,
        "risk_off_exit": False,
        "position_state": None,
        "state_history": [],
        "state_entered_at": None,
        "stop_calculated_at": None,
        "atr_calculated_at": None,
        "active_atr_multiplier": None,
        "stop_last_moved_date": None,
        "previous_stop": None,
    }
    base.update(overrides)
    return base


class _Patcher:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()


class TestNightlyStopLastMoved(_Patcher):

    def _run(self, position, price, atr=5.0):
        for name in ("calculate_trailing_stop", "calculate_holding_days"):
            self._patch(name, new=getattr(real_calcs, name))
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[position])
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=price)
        self._patch("calculate_atr", return_value=atr)
        mock_update = self._patch("update_position")
        result = position_service.run_nightly_trailing_stop_update()
        return result, mock_update

    def test_raised_stop_records_run_date_and_previous_stop(self):
        # Profitable at 120: max(120 - 2 x 5 = 110, entry 100) = 110 > stored 80.
        result, mock_update = self._run(_open_position(), price=120.0)
        written = mock_update.call_args.args[1]
        assert written["current_stop"] == pytest.approx(110.0)
        assert written["stop_last_moved_date"] == result["run_date"]
        assert written["previous_stop"] == pytest.approx(80.0)
        assert result["results"][0]["stop_moved"] is True

    def test_second_move_overwrites_with_the_newer_run(self):
        pos = _open_position(current_stop=105.0, stop_last_moved_date=date(2026, 1, 5), previous_stop=95.0)
        result, mock_update = self._run(pos, price=120.0)
        written = mock_update.call_args.args[1]
        assert written["stop_last_moved_date"] == result["run_date"]
        assert written["previous_stop"] == pytest.approx(105.0)

    def test_unchanged_stop_leaves_both_fields_unchanged(self):
        # Losing at 90: 90 - 5 x 5 = 65 < stored 80, so the ratchet keeps 80.
        pos = _open_position(stop_last_moved_date=date(2026, 1, 5), previous_stop=78.0)
        result, mock_update = self._run(pos, price=90.0)
        written = mock_update.call_args.args[1]
        assert written["current_stop"] == pytest.approx(80.0)
        assert "stop_last_moved_date" not in written
        assert "previous_stop" not in written
        assert result["results"][0]["stop_moved"] is False

    def test_sub_rounding_rise_is_not_a_move(self):
        # Raw new stop 90.00498 - 2 x 5 = 80.00498 is above the stored 80.0049,
        # but rounds to 80.00, so stop_to_store keeps 80.0049 and nothing moved.
        pos = _open_position(current_stop=80.0049, entry_price=60.0)
        result, mock_update = self._run(pos, price=90.00498, atr=5.0)
        assert result["results"][0]["new_stop"] == pytest.approx(80.0, abs=0.01)
        written = mock_update.call_args.args[1]
        assert written["current_stop"] == pytest.approx(80.0049)
        assert "stop_last_moved_date" not in written
        assert "previous_stop" not in written

    def test_second_raise_same_day_keeps_the_days_first_previous_stop(self):
        today = position_service.datetime.now(position_service.timezone.utc).strftime("%Y-%m-%d")
        pos = _open_position(current_stop=83.0, stop_last_moved_date=date.fromisoformat(today), previous_stop=80.0)
        _, mock_update = self._run(pos, price=120.0)
        written = mock_update.call_args.args[1]
        assert written["current_stop"] == pytest.approx(110.0)
        assert written["stop_last_moved_date"] == today
        assert "previous_stop" not in written  # stays 80, the stop before the day's first move

    def test_rise_hidden_at_2dp_is_not_a_move(self):
        # Stored 84.996; the ratchet writes 85.00. Both show as 85.00, so no move.
        pos = _open_position(current_stop=84.996, entry_price=60.0)
        _, mock_update = self._run(pos, price=95.0, atr=5.0)
        written = mock_update.call_args.args[1]
        assert written["current_stop"] == pytest.approx(85.0)
        assert "stop_last_moved_date" not in written

    def test_null_stored_stop_is_not_a_move(self):
        # A NULL current_stop reads as 0 in the job; its first write is not a move "from 0".
        _, mock_update = self._run(_open_position(current_stop=None), price=120.0)
        written = mock_update.call_args.args[1]
        assert "stop_last_moved_date" not in written
        assert "previous_stop" not in written

    def test_missing_columns_still_ratchet_without_recording(self):
        self._patch("ensure_stop_last_moved_columns", side_effect=RuntimeError("column lock timeout"))
        result, mock_update = self._run(_open_position(), price=120.0)
        written = mock_update.call_args.args[1]
        assert written["current_stop"] == pytest.approx(110.0)
        assert "stop_last_moved_date" not in written
        assert result["updated"] == 1

    def test_in_grace_writes_neither_field(self):
        pos = _open_position(entry_date=date.today() - timedelta(days=3))
        _, mock_update = self._run(pos, price=120.0)
        written = mock_update.call_args.args[1]
        assert "stop_last_moved_date" not in written
        assert "previous_stop" not in written

    def test_no_atr_skip_writes_neither_field(self):
        _, mock_update = self._run(_open_position(atr=None), price=120.0, atr=None)
        mock_update.assert_called_once_with("pos-1", {"stop_frozen_reason": "atr_unavailable"})


class TestOnLoadStopLastMoved(_Patcher):
    """Ruling 2026-11-13 (Head of Specs Team, Data Model & Domain Schema Owner):
    GET /positions/analyze records a move too, because the 16:00 UTC snapshot's
    on-load recompute usually raises a stop before the nightly run."""

    def _analyze(self, position, price):
        for name in ("should_exit_position", "calculate_trailing_stop",
                     "calculate_holding_days", "calculate_position_pnl"):
            self._patch(name, new=getattr(real_calcs, name))
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[position])
        self._patch("get_settings", return_value=[{
            "uk_commission": 9.95, "us_commission": 0, "stamp_duty_rate": 0.005,
            "fx_fee_rate": 0.0015, "atr_multiplier_initial": 5, "atr_multiplier_trailing": 2,
        }])
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=price)
        self._patch("check_market_regime", return_value={"spy_risk_on": True, "ftse_risk_on": True})
        self._patch("calculate_atr", return_value=None)  # reuse the stored ATR of 5
        mock_update = self._patch("update_position")
        position_service.analyze_positions()
        return mock_update.call_args.args[1]

    def test_on_load_raise_records_the_move(self):
        written = self._analyze(_open_position(), price=120.0)
        assert written["current_stop"] == pytest.approx(110.0)
        assert written["stop_last_moved_date"] == position_service.datetime.now(
            position_service.timezone.utc).strftime("%Y-%m-%d")
        assert written["previous_stop"] == pytest.approx(80.0)

    def test_on_load_unchanged_stop_records_nothing(self):
        written = self._analyze(_open_position(), price=90.0)
        assert written["current_stop"] == pytest.approx(80.0)
        assert "stop_last_moved_date" not in written
        assert "previous_stop" not in written


class TestGetPositionsReturnsStopLastMoved(_Patcher):

    def _get(self, position):
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[position])
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=110.0)
        self._patch("get_sector_and_industry", return_value=(None, None))
        return position_service.get_positions_with_prices()[0]

    def test_fields_returned_when_set(self):
        row = self._get(_open_position(stop_last_moved_date=date(2026, 11, 11), previous_stop=78.12345))
        assert row["stop_last_moved_date"] == "2026-11-11"
        assert row["previous_stop"] == pytest.approx(78.12)

    def test_fields_null_before_first_move(self):
        row = self._get(_open_position())
        assert row["stop_last_moved_date"] is None
        assert row["previous_stop"] is None


class TestEnsureStopLastMovedColumns:
    """The startup ensure-function adds both nullable columns idempotently and commits."""

    def test_adds_both_columns(self):
        from unittest.mock import MagicMock
        from tests._real_database import load_real_database
        database = load_real_database("database_real_for_test_stop_last_moved")
        cur = MagicMock()
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        get_db = MagicMock()
        get_db.return_value.__enter__.return_value = conn
        database.reset_ensure_once()
        with patch.object(database, "get_db", get_db):
            database.ensure_stop_last_moved_columns()
            database.ensure_stop_last_moved_columns()  # second call is a no-op (ensure_once)
        sql = [c.args[0] for c in cur.execute.call_args_list]
        assert sql == [
            "ALTER TABLE positions ADD COLUMN IF NOT EXISTS stop_last_moved_date DATE",
            "ALTER TABLE positions ADD COLUMN IF NOT EXISTS previous_stop DECIMAL(10, 4)",
        ]
        conn.commit.assert_called_once()
