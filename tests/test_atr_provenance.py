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
        # DS-22 meaning: atr_calculated_at moves only on a fresh fetch (PR review fix).
        assert "atr_calculated_at" not in mock_update.call_args.args[1]
        assert "stop_calculated_at" in mock_update.call_args.args[1]

    def test_fresh_fetch_stamps_atr_calculated_at(self):
        _, mock_update = self._run(_open_position(), fetched_atr=6.0)
        assert "atr_calculated_at" in mock_update.call_args.args[1]

    def test_no_atr_at_all_skips_and_writes_only_the_frozen_reason(self):
        # ST-15 (BLG-FE-202, v9.12): the skip keeps the stop and now records why.
        # Nothing else is written: no stop, ATR or timestamp.
        result, mock_update = self._run(_open_position(atr=None), fetched_atr=None)
        mock_update.assert_called_once_with("pos-1", {"stop_frozen_reason": "atr_unavailable"})
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


class TestUsPositionWithNullFillPrice(_Patcher):
    """ST-12 (BLG-BE-145, EPIC-02, v9.12): a US row with a NULL fill_price recomputes
    without error on both paths and on GET /positions. positions.entry_price is GBP,
    so the native entry is entry_price × fx_rate: $100 here. The §7.2 breakeven floor
    must use $100, not the GBP £80."""

    def _us(self, **overrides):
        base = dict(ticker="AAPL", market="US", entry_price=80.0, fill_price=None, fx_rate=1.25,
                    current_stop=85.0, initial_stop=75.0, atr=5.0, total_cost=800.0)
        base.update(overrides)
        return _open_position(**base)

    def test_on_load_recompute_uses_native_entry_floor(self):
        _, mock_update = _AnalyzeRun._run(self, self._us(), price=104.0)
        # Profitable: max(stored 85, 104 − 2 × 5 = 94, native entry 100) = 100
        assert mock_update.call_args.args[1]["current_stop"] == pytest.approx(100.0)

    def test_nightly_recompute_uses_native_entry_floor(self):
        self._use_real_calcs("calculate_trailing_stop", "calculate_holding_days")
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[self._us()])
        self._patch("get_live_fx_rate", return_value=1.30)
        self._patch("get_current_price", return_value=104.0)
        self._patch("calculate_atr", return_value=5.0)
        mock_update = self._patch("update_position")
        position_service.run_nightly_trailing_stop_update()
        assert mock_update.call_args.args[1]["current_stop"] == pytest.approx(100.0)

    def test_null_fx_rate_falls_back_to_live_rate(self):
        _, mock_update = _AnalyzeRun._run(self, self._us(fx_rate=None), price=104.0)
        # live rate patched to 1.0 by _AnalyzeRun: native entry 80 × 1.0 = 80, so no floor binds
        assert mock_update.call_args.args[1]["current_stop"] == pytest.approx(94.0)

    def test_get_positions_computes_pnl(self):
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[self._us()])
        self._patch("get_live_fx_rate", return_value=1.25)
        self._patch("get_current_price", return_value=110.0)
        self._patch("get_sector_and_industry", return_value=(None, None))
        self._use_real_calcs("calculate_position_pnl")
        result = position_service.get_positions_with_prices()
        assert result[0]["pnl"] is not None


class TestStopFrozenReason(_Patcher):
    """ST-15 (BLG-FE-202, EPIC-02, v9.12, DS-32): both recompute paths record a stop
    kept for lack of ATR as stop_frozen_reason = 'atr_unavailable', clear it on the
    next recompute with an ATR, and GET /positions returns it."""

    def _nightly(self, position, fetched_atr):
        return TestNightlyProvenance._run(self, position, fetched_atr)

    def test_nightly_skip_sets_it(self):
        _, mock_update = self._nightly(_open_position(atr=None), fetched_atr=None)
        assert mock_update.call_args.args[1] == {"stop_frozen_reason": "atr_unavailable"}

    def test_nightly_recompute_with_atr_clears_it(self):
        _, mock_update = self._nightly(_open_position(stop_frozen_reason="atr_unavailable"), fetched_atr=6.0)
        assert mock_update.call_args.args[1]["stop_frozen_reason"] is None

    def test_nightly_skip_in_grace_does_not_set_it(self):
        pos = _open_position(atr=None, entry_date=date.today() - timedelta(days=3))
        _, mock_update = self._nightly(pos, fetched_atr=None)
        mock_update.assert_not_called()

    def test_on_load_without_atr_sets_it(self):
        _, mock_update = _AnalyzeRun._run(self, _open_position(atr=None), price=110.0, fetched_atr=None)
        assert mock_update.call_args.args[1]["stop_frozen_reason"] == "atr_unavailable"

    def test_on_load_with_atr_clears_it(self):
        pos = _open_position(stop_frozen_reason="atr_unavailable")
        _, mock_update = _AnalyzeRun._run(self, pos, price=110.0, fetched_atr=None)
        assert mock_update.call_args.args[1]["stop_frozen_reason"] is None

    def test_on_load_in_grace_leaves_it_alone(self):
        pos = _open_position(atr=None, entry_date=date.today() - timedelta(days=3))
        _, mock_update = _AnalyzeRun._run(self, pos, price=110.0, fetched_atr=None)
        assert "stop_frozen_reason" not in mock_update.call_args.args[1]

    @pytest.mark.parametrize("reason", ["atr_unavailable", None])
    def test_get_positions_returns_it(self, reason):
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[_open_position(stop_frozen_reason=reason)])
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=110.0)
        self._patch("get_sector_and_industry", return_value=(None, None))
        assert position_service.get_positions_with_prices()[0]["stop_frozen_reason"] == reason
