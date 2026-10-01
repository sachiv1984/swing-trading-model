"""
ST-01, EPIC-01, v9.9, BLG-BE-135: stop/ATR recalculation timestamp + active
multiplier persistence (DS-22) and GET /positions exposure.

Covers:
  - get_positions_with_prices() correctly passes stop_calculated_at /
    atr_calculated_at / active_atr_multiplier through to the API response
    shape (None when absent, ISO string when present).
  - analyze_positions() writes stop_calculated_at + active_atr_multiplier
    to update_position() only when a real (non-grace-period) recompute
    happened, and atr_calculated_at only when ATR was freshly computed.
  - run_nightly_trailing_stop_update() always writes all 3 fields together
    (it always freshly recomputes both ATR and the stop in one pass).

Does not re-test the pre-existing business logic of these functions
(P&L, FX conversion, stop ratcheting, etc.) -- only the new fields this
story adds.
"""
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.position_service as position_service


def _base_position(**overrides):
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
        "current_stop": 90.0,
        "initial_stop": 85.0,
        "atr": 5.0,
        "total_cost": 1000.0,
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
    }
    base.update(overrides)
    return base


class TestGetPositionsWithPricesExposesNewFields:

    def _run(self, position):
        with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(position_service, "get_positions", return_value=[position]), \
             patch.object(position_service, "get_live_fx_rate", return_value=1.0), \
             patch.object(position_service, "get_current_price", return_value=110.0), \
             patch.object(position_service, "get_sector_and_industry", return_value=(None, None)):
            return position_service.get_positions_with_prices()

    def test_fields_null_when_never_recomputed(self):
        result = self._run(_base_position())
        pos = result[0]
        assert pos["atr_calculated_at"] is None
        assert pos["stop_calculated_at"] is None
        assert pos["active_atr_multiplier"] is None

    def test_fields_populated_when_present(self):
        ts = datetime(2026, 10, 1, 6, 0, 0, tzinfo=timezone.utc)
        result = self._run(_base_position(
            stop_calculated_at=ts, atr_calculated_at=ts, active_atr_multiplier=2.0,
        ))
        pos = result[0]
        assert pos["atr_calculated_at"] == ts.isoformat()
        assert pos["stop_calculated_at"] == ts.isoformat()
        assert pos["active_atr_multiplier"] == 2.0


class TestAnalyzePositionsWritesTimestamps:

    def _run(self, position):
        with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(position_service, "get_positions", return_value=[position]), \
             patch.object(position_service, "get_live_fx_rate", return_value=1.0), \
             patch.object(position_service, "get_current_price", return_value=110.0), \
             patch.object(position_service, "check_market_regime",
                           return_value={"spy_risk_on": True, "ftse_risk_on": True}), \
             patch.object(position_service, "update_position") as mock_update:
            position_service.analyze_positions()
            return mock_update

    def test_post_grace_write_includes_stop_calculated_at_and_multiplier(self):
        mock_update = self._run(_base_position(
            entry_date=date.today() - timedelta(days=30),  # well past the 10-day grace period
        ))
        assert mock_update.called
        updates = mock_update.call_args.args[1]
        assert "stop_calculated_at" in updates
        assert "active_atr_multiplier" in updates
        assert updates["active_atr_multiplier"] > 0  # a real multiplier, not the grace-period sentinel 0

    def test_grace_period_write_omits_stop_calculated_at(self):
        mock_update = self._run(_base_position(
            entry_date=date.today() - timedelta(days=2),  # inside the 10-day grace period
        ))
        assert mock_update.called
        updates = mock_update.call_args.args[1]
        assert "stop_calculated_at" not in updates
        assert "active_atr_multiplier" not in updates

    def test_atr_calculated_at_written_when_atr_missing_from_db(self):
        with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(position_service, "get_positions", return_value=[_base_position(atr=None, entry_date=date.today() - timedelta(days=30))]), \
             patch.object(position_service, "get_live_fx_rate", return_value=1.0), \
             patch.object(position_service, "get_current_price", return_value=110.0), \
             patch.object(position_service, "check_market_regime",
                           return_value={"spy_risk_on": True, "ftse_risk_on": True}), \
             patch.object(position_service, "calculate_atr", return_value=5.0), \
             patch.object(position_service, "update_position") as mock_update:
            position_service.analyze_positions()

        # First call stores the freshly-computed ATR with its timestamp
        first_call_updates = mock_update.call_args_list[0].args[1]
        assert "atr_calculated_at" in first_call_updates
        assert first_call_updates["atr"] == 5.0


class TestNightlyTrailingStopUpdateWritesAllThreeFields:

    def test_writes_stop_atr_timestamps_and_multiplier_together(self):
        position = _base_position(entry_date=date.today() - timedelta(days=30))
        with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1"}), \
             patch.object(position_service, "get_positions", return_value=[position]), \
             patch.object(position_service, "get_live_fx_rate", return_value=1.0), \
             patch.object(position_service, "get_current_price", return_value=110.0), \
             patch.object(position_service, "calculate_atr", return_value=5.0), \
             patch.object(position_service, "update_position") as mock_update:
            position_service.run_nightly_trailing_stop_update()

        assert mock_update.called
        updates = mock_update.call_args.args[1]
        assert "stop_calculated_at" in updates
        assert "atr_calculated_at" in updates
        assert "active_atr_multiplier" in updates
        # Both timestamps come from the same now_utc capture in this single pass
        assert updates["stop_calculated_at"] == updates["atr_calculated_at"]
