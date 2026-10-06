"""
ST-04 (BLG-QA-207, EPIC-01, v9.10): unit tests for the live exit decision and
grace-period behaviour.

Covers strategy_rules.md clauses that the traceability matrix
(docs/testing/strategy_rule_test_traceability_matrix.md) recorded as None or
Partial because no CI test called the live code path:

  - C8-00 / C8.1-01 / C8.2 / C6.3-01: backend/utils/calculations.py::
    should_exit_position is called directly (never stubbed) for the grace
    boundary (day 9 vs day 10), price at/below/above stop, risk-off
    overriding both grace and stop, and the closed set of exit reasons.
  - C5-02: add_position() persists an initial stop (initial_stop and
    current_stop) on the entry write.
  - C6.3-02: analyze_positions() still writes a stop for an in-grace position
    (the stored stop is carried, never zeroed or dropped).
  - C8.1-02: analyze_positions() recommends EXIT but never closes the
    position itself — the exit needs a separate, user-confirmed call.
  - C6.3-03 / C8.3: exit_position() accepts a manual exit inside the grace
    period.
  - C7.1-02: analyze_positions() recomputes the stop on load, and the nightly
    job freshly recomputes ATR.

Some other test modules replace attributes of sys.modules["utils.calculations"]
with MagicMocks and do not restore them. To stay hermetic regardless of suite
order, the real calculations module is loaded from its file under a private
name, and position_service's bindings are patched back to the real functions
where a test depends on them.
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
    "_real_calculations_st04", BACKEND / "utils" / "calculations.py"
)
real_calcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(real_calcs)

import services.position_service as position_service  # noqa: E402

should_exit_position = real_calcs.should_exit_position

# §8: a position may exit under exactly these conditions. Manual exit is
# user-initiated and is never returned by the automated decision.
AUTOMATED_EXIT_REASONS = {"Stop Loss Hit", "Risk-Off Signal"}


# ---------------------------------------------------------------------------
# should_exit_position — called directly, not stubbed
# ---------------------------------------------------------------------------

class TestGraceBoundary:
    """C6.3-01 / C8.1-01: the stop is inactive until day 10."""

    def test_day_9_below_stop_holds(self):
        assert should_exit_position(90.0, 100.0, holding_days=9, market_risk_on=True) == (False, None)

    def test_day_10_below_stop_exits(self):
        assert should_exit_position(90.0, 100.0, holding_days=10, market_risk_on=True) == (True, "Stop Loss Hit")

    def test_day_0_below_stop_holds(self):
        assert should_exit_position(1.0, 100.0, holding_days=0, market_risk_on=True) == (False, None)

    def test_grace_length_is_a_parameter(self):
        # The boundary follows grace_period_days, not a hidden constant.
        assert should_exit_position(90.0, 100.0, 11, True, grace_period_days=12) == (False, None)
        assert should_exit_position(90.0, 100.0, 12, True, grace_period_days=12) == (True, "Stop Loss Hit")


class TestPriceVersusStop:
    """C8.1-01: after grace, exit fires when price is at or below the stop."""

    def test_price_below_stop_exits(self):
        assert should_exit_position(99.99, 100.0, 15, True) == (True, "Stop Loss Hit")

    def test_price_at_stop_exits(self):
        assert should_exit_position(100.0, 100.0, 15, True) == (True, "Stop Loss Hit")

    def test_price_above_stop_holds(self):
        assert should_exit_position(100.01, 100.0, 15, True) == (False, None)


class TestRiskOffOverrides:
    """C8.2: risk-off exits regardless of grace and stop."""

    def test_risk_off_inside_grace_exits(self):
        assert should_exit_position(150.0, 100.0, 2, market_risk_on=False) == (True, "Risk-Off Signal")

    def test_risk_off_above_stop_exits(self):
        assert should_exit_position(150.0, 100.0, 30, market_risk_on=False) == (True, "Risk-Off Signal")

    def test_risk_off_takes_precedence_over_stop_breach(self):
        assert should_exit_position(90.0, 100.0, 30, market_risk_on=False) == (True, "Risk-Off Signal")


class TestClosedSetOfExitReasons:
    """C8-00: the automated decision returns only the §8 reasons, or holds."""

    @pytest.mark.parametrize("price", [50.0, 100.0, 150.0])
    @pytest.mark.parametrize("stop", [0.0, 100.0])
    @pytest.mark.parametrize("days", [0, 9, 10, 400])
    @pytest.mark.parametrize("risk_on", [True, False])
    def test_reason_is_in_closed_set(self, price, stop, days, risk_on):
        should_exit, reason = should_exit_position(price, stop, days, risk_on)
        if should_exit:
            assert reason in AUTOMATED_EXIT_REASONS
        else:
            assert reason is None


# ---------------------------------------------------------------------------
# Service write paths
# ---------------------------------------------------------------------------

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
        "current_stop": 90.0,
        "initial_stop": 85.0,
        "atr": 5.0,
        "total_cost": 1000.0,
        "fees_paid": 10.0,
        "status": "open",
        "entry_note": None,
        "tags": [],
        "risk_off_exit": False,
        "user_fill_price": None,
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


class TestEntryPersistsInitialStop(_Patcher):
    """C5-02: the stop exists and is stored from day one."""

    def test_add_position_writes_initial_and_current_stop(self):
        self._use_real_calcs("calculate_initial_stop", "calculate_uk_entry_fees")
        self._patch("get_portfolio", return_value={"id": "portfolio-1", "cash": 100000.0})
        self._patch("get_settings", return_value=_settings())
        mock_create = self._patch("create_position", return_value={"id": "new-position-id"})
        self._patch("update_portfolio_cash")
        self._patch("calculate_atr", return_value=4.0)
        self._patch("get_unlinked_trade_plan_for_entry", return_value=None)
        self._patch("get_current_strategy_version", return_value="1.4")

        position_service.add_position(
            ticker="VOD.L", market="UK", entry_date=str(date.today()),
            shares=10, entry_price=100.0,
        )

        position_data = mock_create.call_args.args[1]
        # §5: initial stop = entry − 5 × ATR = 100 − 20
        assert position_data["initial_stop"] == pytest.approx(80.0)
        assert position_data["current_stop"] == pytest.approx(80.0)
        assert position_data["atr"] == pytest.approx(4.0)


class _AnalyzeRun(_Patcher):
    def _run_analyze(self, position, price, risk_on=True):
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
        mock_update = self._patch("update_position")
        mock_trade = self._patch("create_trade_history")
        result = position_service.analyze_positions()
        return result, mock_update, mock_trade


class TestGracePeriodStillStoresStop(_AnalyzeRun):
    """C6.3-02 / C6.3-01: during grace the stop is still stored, and no stop exit is recommended."""

    def test_in_grace_write_keeps_the_stored_stop(self):
        position = _open_position(entry_date=date.today() - timedelta(days=3), current_stop=80.0)
        result, mock_update, _ = self._run_analyze(position, price=75.0)  # below stop

        updates = mock_update.call_args.args[1]
        assert updates["current_stop"] == pytest.approx(80.0)
        action = result["actions"][0]
        assert action["action"] == "HOLD"
        assert action["grace_period"] is True


class TestStopExitNeedsManualConfirmation(_AnalyzeRun):
    """C8.1-02: analyze recommends EXIT; it never closes the position itself."""

    def test_post_grace_breach_recommends_exit_without_closing(self):
        position = _open_position(entry_date=date.today() - timedelta(days=30), current_stop=90.0)
        result, mock_update, mock_trade = self._run_analyze(position, price=85.0)

        action = result["actions"][0]
        assert action["action"] == "EXIT"
        assert action["exit_reason"] == "Stop Loss Hit"
        mock_trade.assert_not_called()
        for call in mock_update.call_args_list:
            assert "status" not in call.args[1]

    def test_risk_off_recommends_exit_inside_grace(self):
        position = _open_position(entry_date=date.today() - timedelta(days=2))
        result, _, mock_trade = self._run_analyze(position, price=120.0, risk_on=False)

        assert result["actions"][0]["action"] == "EXIT"
        assert result["actions"][0]["exit_reason"] == "Risk-Off Signal"
        mock_trade.assert_not_called()


class TestOnLoadRecompute(_AnalyzeRun):
    """C7.1-02 (on-load half): each analyze call recomputes and stamps the stop."""

    def test_post_grace_load_recomputes_stop(self):
        position = _open_position(entry_date=date.today() - timedelta(days=30), current_stop=90.0, atr=5.0)
        _, mock_update, _ = self._run_analyze(position, price=120.0)

        updates = mock_update.call_args.args[1]
        # Profitable: 120 − 2 × 5 = 110, above the stored 90
        assert updates["current_stop"] == pytest.approx(110.0)
        assert "stop_calculated_at" in updates
        assert updates["active_atr_multiplier"] == pytest.approx(2.0)


class TestNightlyRecomputesAtr(_Patcher):
    """C7.1-02 (nightly half): the nightly job fetches a fresh ATR every run."""

    def test_nightly_calls_calculate_atr_and_stores_it(self):
        self._use_real_calcs("calculate_trailing_stop", "calculate_holding_days")
        self._patch("get_portfolio", return_value={"id": "portfolio-1"})
        self._patch("get_positions", return_value=[_open_position(atr=3.0)])
        self._patch("get_live_fx_rate", return_value=1.0)
        self._patch("get_current_price", return_value=120.0)
        mock_atr = self._patch("calculate_atr", return_value=6.0)
        mock_update = self._patch("update_position")

        position_service.run_nightly_trailing_stop_update()

        mock_atr.assert_called_once()
        assert mock_update.call_args.args[1]["atr"] == pytest.approx(6.0)


class TestManualExitInsideGrace(_Patcher):
    """C6.3-03 / C8.3: manual exit is accepted at any time, including day 0-9."""

    @pytest.mark.parametrize("days_held", [0, 3, 9])
    def test_exit_position_accepts_in_grace_manual_exit(self, days_held):
        self._use_real_calcs("calculate_holding_days")
        entry = date.today() - timedelta(days=days_held)
        self._patch("get_portfolio", return_value={"id": "portfolio-1", "cash": 1000.0})
        self._patch("get_positions", return_value=[_open_position(entry_date=entry)])
        self._patch("get_settings", return_value=_settings())
        self._patch("calculate_exit_proceeds", return_value={
            "gross_proceeds_gbp": 950.0, "exit_fees_gbp": 9.95, "net_proceeds_gbp": 940.05,
            "net_proceeds_native": 940.05,
            "fee_breakdown": {"commission": 9.95, "stamp_duty": 0, "fx_fee": 0},
        })
        self._patch("calculate_realized_pnl", return_value=(-59.95, -5.995))
        self._patch("ensure_planned_entry_price_column")
        self._patch("get_trade_plans_by_position", return_value=[])
        mock_trade = self._patch("create_trade_history")
        mock_update = self._patch("update_position")
        self._patch("update_portfolio_cash")

        position_service.exit_position(position_id="pos-1", exit_price=95.0)

        trade = mock_trade.call_args.args[1]
        assert trade["exit_reason"] == "Manual Exit"
        assert trade["holding_days"] == days_held
        assert mock_update.call_args.args[1]["status"] == "closed"
