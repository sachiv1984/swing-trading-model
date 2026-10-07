"""
ST-07 (BLG-FE-197, EPIC-02, v9.10): pin add_position()'s stop handling.

Trade Entry no longer offers a Stop Price input because the backend never
used one: add_position() stores initial_stop = current_stop =
entry − INITIAL_ATR_MULTIPLIER × ATR (strategy_rules.md §5), with the
multiplier taken from the fixed §11 source (backend/strategy_parameters.py,
ST-01 ruling (a)), and ignores any submitted stop_price. These tests fail if
a submitted stop ever starts to reach the stored row, or if the stored stop
stops matching the formula the Trade Entry panel displays.

The real calculations module is loaded from its file, for the same
suite-order reason as tests/test_live_exit_decision.py.
"""
import importlib.util
import sys
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

BACKEND = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(BACKEND))

_spec = importlib.util.spec_from_file_location(
    "_real_calculations_st07", BACKEND / "utils" / "calculations.py"
)
real_calcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(real_calcs)

import services.position_service as position_service  # noqa: E402
from strategy_parameters import INITIAL_ATR_MULTIPLIER  # noqa: E402


def _settings():
    # A settings row that disagrees with §11, to prove it is not read.
    return [{
        "uk_commission": 9.95,
        "us_commission": 0,
        "stamp_duty_rate": 0.005,
        "fx_fee_rate": 0.0015,
        "atr_multiplier_initial": 2,
        "atr_multiplier_trailing": 1,
    }]


class TestAddPositionStopHandling:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()

    def _add(self, *, market="UK", ticker="VOD.L", entry_price=100.0, atr_value=None,
             fetched_atr=None, stop_price=None, fx_rate=None):
        for name in ("calculate_initial_stop", "calculate_uk_entry_fees", "calculate_us_entry_fees"):
            self._patch(name, new=getattr(real_calcs, name))
        self._patch("get_portfolio", return_value={"id": "portfolio-1", "cash": 1_000_000.0})
        self._patch("get_settings", return_value=_settings())
        mock_create = self._patch("create_position", return_value={"id": "new-position-id"})
        self._patch("update_portfolio_cash")
        self._patch("calculate_atr", return_value=fetched_atr)
        self._patch("get_live_fx_rate", return_value=1.25)
        self._patch("get_unlinked_trade_plan_for_entry", return_value=None)
        self._patch("get_current_strategy_version", return_value="1.4")
        response = position_service.add_position(
            ticker=ticker, market=market, entry_date=str(date.today()),
            shares=10, entry_price=entry_price, atr_value=atr_value,
            stop_price=stop_price, fx_rate=fx_rate,
        )
        return mock_create.call_args.args[1], response

    def test_multiplier_is_the_fixed_section_11_value(self):
        assert INITIAL_ATR_MULTIPLIER == 5.0

    def test_stored_stop_is_entry_minus_5x_atr(self):
        data, response = self._add(entry_price=100.0, atr_value=2.0)
        assert data["initial_stop"] == pytest.approx(90.0)
        assert data["current_stop"] == pytest.approx(90.0)
        assert response["initial_stop"] == pytest.approx(90.0)

    def test_submitted_stop_price_is_ignored(self):
        data, response = self._add(entry_price=100.0, atr_value=2.0, stop_price=97.5)
        assert data["initial_stop"] == pytest.approx(90.0)
        assert data["current_stop"] == pytest.approx(90.0)
        assert "stop_price" not in data
        assert response["initial_stop"] == pytest.approx(90.0)

    def test_blank_atr_is_fetched_and_drives_the_stop(self):
        data, response = self._add(entry_price=100.0, atr_value=None, fetched_atr=4.0, stop_price=99.0)
        assert data["atr_source"] == "fetched"
        assert data["initial_stop"] == pytest.approx(80.0)  # 100 − 5 × 4
        assert response["initial_stop"] == pytest.approx(80.0)

    def test_us_stop_is_in_native_currency(self):
        data, response = self._add(market="US", ticker="AAPL", entry_price=200.0, atr_value=3.0,
                                   stop_price=150.0, fx_rate=1.25)
        assert data["initial_stop"] == pytest.approx(185.0)  # 200 − 5 × 3, USD, not GBP-converted
        assert response["initial_stop"] == pytest.approx(185.0)
