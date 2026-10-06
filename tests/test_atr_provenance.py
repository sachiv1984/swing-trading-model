"""
ST-02 (BLG-BE-139, EPIC-01, v9.10): remove silent ATR fallbacks and record
ATR provenance (positions.atr_source, data_model.md DS-25).

Covers both fallbacks named by the story:
  - Entry-time: add_position() still substitutes 2% of entry when no ATR can
    be fetched, but now records atr_source = 'fallback' instead of storing the
    invented value silently. A typed ATR is 'user'; a fetched one 'fetched'.
  - Recompute-time: analyze_positions() used to move the stop to entry when
    ATR was missing. For a losing position that put the stop above the
    current price and produced a stop-breach signal that §7.2's wide-stop
    rule would not. Now the stored stop is left unchanged and the action is
    flagged atr_unavailable.

Also checks the nightly job's provenance write and GET /positions exposure.
The real calculations module is loaded from its file, for the same
suite-order reason as tests/test_live_exit_decision.py.
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
    "_real_calculations_st02", BACKEND / "utils" / "calculations.py"
)
real_calcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(real_calcs)

import services.position_service as position_service  # noqa: E402


def _settings():
    return [{
        "uk_commission": 9.95,
        "us_commission": 0,
        "stamp_duty_rate": 0.005,
        "fx_fee_rate": 0.0015,
        "atr_multiplier_initial": 5,
        "atr_multiplier_trailing": 2,
    }]


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

    def _use_real_calcs(self, *names):
        for name in names:
            self._patch(name, new=getattr(real_calcs, name))


class TestEntryProvenance(_Patcher):
    """Entry-time fallback: 2% of entry is recorded as 'fallback', not silent."""

    def _add(self, atr_value=None, fetched_atr=None):
        self._use_real_calcs("calculate_initial_stop", "calculate_uk_entry_fees")
        self._patch("get_portfolio", return_value={"id": "portfolio-1", "cash": 100000.0})
        self._patch("get_settings", return_value=_settings())
        mock_create = self._patch("create_position", return_value={"id": "new-position-id"})
        self._patch("update_portfolio_cash")
        self._patch("calculate_atr", return_value=fetched_atr)
        self._patch("get_unlinked_trade_plan_for_entry", return_value=None)
        self._patch("get_current_strategy_version", return_value="1.4")
        position_service.add_position(
            ticker="VOD.L", market="UK", entry_date=str(date.today()),
            shares=10, entry_price=100.0, atr_value=atr_value,
        )
        return mock_create.call_args.args[1]

    def test_user_typed_atr_is_user(self):
        data = self._add(atr_value=3.0)
        assert data["atr_source"] == "user"
        assert data["atr"] == pytest.approx(3.0)

    def test_fetched_atr_is_fetched(self):
        data = self._add(fetched_atr=4.0)
        assert data["atr_source"] == "fetched"
        assert data["atr"] == pytest.approx(4.0)

    def test_unavailable_atr_is_recorded_as_fallback(self):
        data = self._add(fetched_atr=None)
        assert data["atr_source"] == "fallback"
        assert data["atr"] == pytest.approx(2.0)  # 2% of 100
        assert data["initial_stop"] == pytest.approx(90.0)  # 100 − 5 × 2


class _AnalyzeRun(_Patcher):
    def _run(self, position, price, fetched_atr=None, risk_on=True):
        self._use_real_calcs(
            "should_exit_position", "calculate_trailing_stop",
            "calculate_holding_days", "calculate_position_pnl",
        )
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[position])
        self._patch("get_settings", return_value=_settings())
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=price)
        self._patch("check_market_regime",
                    return_value={"spy_risk_on": risk_on, "ftse_risk_on": risk_on})
        self._patch("calculate_atr", return_value=fetched_atr)
        mock_update = self._patch("update_position")
        result = position_service.analyze_positions()
        return result, mock_update


class TestRecomputeWithoutAtr(_AnalyzeRun):
    """Recompute-time fallback: stop unchanged, position flagged, no breach created."""

    def test_losing_position_keeps_stop_and_holds(self):
        # Old behaviour: stop -> max(80, entry 100) = 100, above the 95 price,
        # so a post-grace EXIT "Stop Loss Hit" appeared from nowhere.
        position = _open_position(atr=None, current_stop=80.0)
        result, mock_update = self._run(position, price=95.0, fetched_atr=None)

        action = result["actions"][0]
        assert action["action"] == "HOLD"
        assert action["exit_reason"] is None
        assert action["atr_unavailable"] is True
        assert action["current_stop"] == pytest.approx(80.0)
        updates = mock_update.call_args.args[1]
        assert updates["current_stop"] == pytest.approx(80.0)
        assert "stop_calculated_at" not in updates
        assert "atr_source" not in updates

    def test_profitable_position_keeps_stop(self):
        position = _open_position(atr=0, current_stop=80.0)
        result, mock_update = self._run(position, price=130.0, fetched_atr=None)

        assert result["actions"][0]["current_stop"] == pytest.approx(80.0)
        assert mock_update.call_args.args[1]["current_stop"] == pytest.approx(80.0)

    def test_risk_off_still_exits_without_atr(self):
        position = _open_position(atr=None)
        result, _ = self._run(position, price=95.0, fetched_atr=None, risk_on=False)
        assert result["actions"][0]["exit_reason"] == "Risk-Off Signal"

    def test_freshly_fetched_atr_is_recorded_as_fetched(self):
        position = _open_position(atr=None, atr_source=None)
        result, mock_update = self._run(position, price=120.0, fetched_atr=5.0)

        first = mock_update.call_args_list[0].args[1]
        assert first["atr_source"] == "fetched"
        assert result["actions"][0]["atr_unavailable"] is False

    def test_stored_atr_flag_is_false(self):
        result, _ = self._run(_open_position(), price=120.0)
        assert result["actions"][0]["atr_unavailable"] is False


class TestNightlyProvenance(_Patcher):

    def _run(self, position, fetched_atr):
        self._use_real_calcs("calculate_trailing_stop", "calculate_holding_days")
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[position])
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=120.0)
        self._patch("calculate_atr", return_value=fetched_atr)
        mock_update = self._patch("update_position")
        result = position_service.run_nightly_trailing_stop_update()
        return result, mock_update

    def test_fresh_fetch_writes_fetched(self):
        _, mock_update = self._run(_open_position(atr_source="fallback"), fetched_atr=6.0)
        assert mock_update.call_args.args[1]["atr_source"] == "fetched"

    def test_reused_stored_atr_leaves_provenance_alone(self):
        _, mock_update = self._run(_open_position(atr=5.0, atr_source="user"), fetched_atr=None)
        assert "atr_source" not in mock_update.call_args.args[1]

    def test_no_atr_at_all_skips_and_writes_nothing(self):
        result, mock_update = self._run(_open_position(atr=None), fetched_atr=None)
        mock_update.assert_not_called()
        assert result["results"][0]["status"] == "skipped"


class TestGetPositionsExposesAtrSource(_Patcher):

    @pytest.mark.parametrize("source", ["fetched", "user", "fallback", None])
    def test_atr_source_passed_through(self, source):
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[_open_position(atr_source=source)])
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=110.0)
        self._patch("get_sector_and_industry", return_value=(None, None))
        result = position_service.get_positions_with_prices()
        assert result[0]["atr_source"] == source
