"""
ST-07 (BLG-FE-197, EPIC-02, v9.10): pin add_position()'s stop handling.

Trade Entry no longer offers a Stop Price input because the backend never
used one: add_position() stores initial_stop = current_stop =
entry − INITIAL_ATR_MULTIPLIER × ATR (strategy_rules.md §5), with the
multiplier taken from the fixed §11 source (backend/strategy_parameters.py,
ST-01 ruling (a)). These tests fail if the stored stop stops matching the
formula the Trade Entry panel displays.

ST-10 (BLG-BE-159, EPIC-02, v9.12): a supplied stop_price is no longer silently
ignored. POST /portfolio/position rejects it with a 400 (Strategy Rules &
System Intent Owner ruling ESC-EXEC-20261013-06), and add_position() no longer
takes a stop_price argument at all.

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
             fetched_atr=None, fx_rate=None):
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
            fx_rate=fx_rate,
        )
        return mock_create.call_args.args[1], response

    def _add_with_cleanup(self, **kwargs):
        self.setup_method()
        try:
            return self._add(**kwargs)
        finally:
            self.teardown_method()

    def test_multiplier_is_the_fixed_section_11_value(self):
        assert INITIAL_ATR_MULTIPLIER == 5.0

    def test_stored_stop_is_entry_minus_5x_atr(self):
        data, response = self._add(entry_price=100.0, atr_value=2.0)
        assert data["initial_stop"] == pytest.approx(90.0)
        assert data["current_stop"] == pytest.approx(90.0)
        assert response["initial_stop"] == pytest.approx(90.0)

    def test_add_position_takes_no_stop_price(self):
        with pytest.raises(TypeError):
            position_service.add_position(
                ticker="VOD.L", market="UK", entry_date=str(date.today()),
                shares=10, entry_price=100.0, atr_value=2.0, stop_price=97.5,
            )

    def test_blank_atr_is_fetched_and_drives_the_stop(self):
        data, response = self._add(entry_price=100.0, atr_value=None, fetched_atr=4.0)
        assert data["atr_source"] == "fetched"
        assert data["initial_stop"] == pytest.approx(80.0)  # 100 − 5 × 4
        assert response["initial_stop"] == pytest.approx(80.0)

    def test_us_stop_is_in_native_currency(self):
        data, response = self._add(market="US", ticker="AAPL", entry_price=200.0, atr_value=3.0,
                                   fx_rate=1.25)
        assert data["initial_stop"] == pytest.approx(185.0)  # 200 − 5 × 3, USD, not GBP-converted
        assert response["initial_stop"] == pytest.approx(185.0)


class TestSuppliedEntryStopRejected:
    """ST-10 AC 3: a supplied entry stop is rejected with a clear error, never silently ignored."""

    @staticmethod
    def _client():
        from tests._real_database import real_database_imports
        with real_database_imports():
            from fastapi.testclient import TestClient
            import main
        return TestClient(main.app, raise_server_exceptions=False), main

    _BODY = {"ticker": "VOD.L", "market": "UK", "entry_date": "2026-10-13", "shares": 10, "entry_price": 100.0}

    def test_supplied_stop_price_returns_400_with_message(self):
        client, main = self._client()
        with patch.object(main, "add_position") as mock_add:
            response = client.post("/portfolio/position", json={**self._BODY, "stop_price": 97.5})
        assert response.status_code == 400
        assert "stop_price is not accepted" in response.text
        assert "entry price − 5 × ATR (strategy_rules.md §5, §11)" in response.text
        mock_add.assert_not_called()

    def test_message_multiplier_comes_from_section_11_constant(self):
        _, main = self._client()
        assert f"− {INITIAL_ATR_MULTIPLIER:g} × ATR" in main.STOP_PRICE_NOT_ACCEPTED

    def test_null_stop_price_is_accepted(self):
        client, main = self._client()
        with patch.object(main, "add_position", return_value={"position_id": "p-1"}) as mock_add:
            response = client.post("/portfolio/position", json={**self._BODY, "stop_price": None})
        assert response.status_code == 200
        mock_add.assert_called_once()
        assert "stop_price" not in mock_add.call_args.kwargs


class TestImplausibleTypedAtrRejected:
    """ST-18 (BLG-FE-203, EPIC-03, v9.12) AC 2: a typed ATR whose 5× multiple meets
    or exceeds the entry price is rejected with a 400 and an explanatory message."""

    _BODY = {"ticker": "VOD.L", "market": "UK", "entry_date": "2026-10-13", "shares": 10, "entry_price": 10.0}

    @staticmethod
    def _client():
        return TestSuppliedEntryStopRejected._client()

    @pytest.mark.parametrize("atr_value", [2.0, 2.5, 150.0])  # 5 × ATR == 10, > 10, pence-scale
    def test_endpoint_returns_400_with_message(self, atr_value):
        client, main = self._client()
        with patch("services.position_service.create_position") as mock_create, \
             patch("services.position_service.get_portfolio", return_value={"id": "portfolio-1", "cash": 1_000_000.0}):
            response = client.post("/portfolio/position", json={**self._BODY, "atr_value": atr_value})
        assert response.status_code == 400
        detail = response.json()["detail"]
        assert "puts the initial stop at or below zero" in detail
        assert f"{INITIAL_ATR_MULTIPLIER:g} × ATR must be less than the entry price" in detail
        assert "ATR is in £, not pence or cents." in detail
        mock_create.assert_not_called()

    def test_us_message_names_dollars(self):
        with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 1_000_000.0}):
            with pytest.raises(ValueError, match=r"ATR is in \$, not pence or cents\."):
                position_service.add_position(
                    ticker="AAPL", market="US", entry_date=str(date.today()),
                    shares=10, entry_price=10.0, atr_value=2.0,
                )

    def test_plausible_typed_atr_is_stored(self):
        data, response = TestAddPositionStopHandling()._add_with_cleanup(entry_price=10.0, atr_value=1.5)
        assert data["atr_source"] == "user"
        assert response["initial_stop"] == pytest.approx(2.5)  # 10 − 5 × 1.5

    def test_blank_atr_is_not_checked_against_entry(self):
        # A fetched ATR is never rejected here: the check applies to typed input only.
        data, _ = TestAddPositionStopHandling()._add_with_cleanup(entry_price=10.0, atr_value=None, fetched_atr=3.0)
        assert data["atr_source"] == "fetched"
