"""
ST-17 (BLG-BE-146, EPIC-03, v9.12) — GET /market/atr/{ticker}?market=UK|US is
Trade Entry's read-only ATR preview. The stop Trade Entry shows before save
(entry − INITIAL_ATR_MULTIPLIER × the previewed ATR, position_form.md v1.9
§Initial Stop) must equal the initial_stop that POST /portfolio/position
stores for the same inputs (AC 2). Both paths must therefore fetch the ATR
for the same normalised symbol through calculate_atr().

The real calculations module is loaded from its file, for the same
suite-order reason as tests/test_add_position_stop_handling.py.
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
    "_real_calculations_st17", BACKEND / "utils" / "calculations.py"
)
real_calcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(real_calcs)

import services.position_service as position_service  # noqa: E402
from strategy_parameters import INITIAL_ATR_MULTIPLIER  # noqa: E402


def _client():
    from tests._real_database import real_database_imports
    with real_database_imports():
        from fastapi.testclient import TestClient
        import main
    return TestClient(main.app, raise_server_exceptions=False), main


def _preview(ticker, market, atr):
    client, main = _client()
    with patch.object(main, "calculate_atr", return_value=atr) as mock_atr:
        response = client.get(f"/market/atr/{ticker}", params={"market": market})
    return response, mock_atr


def _save(*, ticker, market, entry_price, fetched_atr):
    """add_position() with ATR blank, so it fetches the ATR itself."""
    patches = [
        patch.object(position_service, name, new=getattr(real_calcs, name))
        for name in ("calculate_initial_stop", "calculate_uk_entry_fees", "calculate_us_entry_fees")
    ]
    patches += [
        patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 1_000_000.0}),
        patch.object(position_service, "get_settings", return_value=[{
            "uk_commission": 9.95, "us_commission": 0, "stamp_duty_rate": 0.005, "fx_fee_rate": 0.0015,
        }]),
        patch.object(position_service, "create_position", return_value={"id": "new-position-id"}),
        patch.object(position_service, "update_portfolio_cash"),
        patch.object(position_service, "get_live_fx_rate", return_value=1.25),
        patch.object(position_service, "get_unlinked_trade_plan_for_entry", return_value=None),
        patch.object(position_service, "get_current_strategy_version", return_value="1.4"),
    ]
    atr_patch = patch.object(position_service, "calculate_atr", return_value=fetched_atr)
    for p in patches:
        p.start()
    mock_atr = atr_patch.start()
    try:
        response = position_service.add_position(
            ticker=ticker, market=market, entry_date=str(date.today()),
            shares=10, entry_price=entry_price, atr_value=None,
        )
    finally:
        atr_patch.stop()
        for p in patches:
            p.stop()
    return response, mock_atr


class TestPreviewResponse:
    def test_returns_native_atr_with_period_and_as_of(self):
        response, mock_atr = _preview("AAPL", "US", 3.1372)
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["ticker"] == "AAPL"
        assert data["market"] == "US"
        assert data["atr"] == pytest.approx(3.1372)
        assert data["atr_period"] == 14
        assert data["as_of"]
        mock_atr.assert_called_once_with("AAPL")

    def test_uk_ticker_is_fetched_with_the_l_suffix(self):
        response, mock_atr = _preview("vod", "UK", 1.5)
        assert response.status_code == 200
        assert response.json()["data"]["ticker"] == "VOD"
        mock_atr.assert_called_once_with("VOD.L")

    def test_unavailable_atr_is_null_not_an_error(self):
        response, _ = _preview("LGEN", "UK", None)
        assert response.status_code == 200
        assert response.json()["data"]["atr"] is None

    def test_invalid_market_is_400(self):
        response, mock_atr = _preview("AAPL", "EU", 3.0)
        assert response.status_code == 400
        mock_atr.assert_not_called()

    def test_writes_nothing(self):
        client, main = _client()
        with patch.object(main, "calculate_atr", return_value=2.0), \
             patch("database.update_position") as update, \
             patch("database.create_position") as create:
            client.get("/market/atr/AAPL", params={"market": "US"})
        update.assert_not_called()
        create.assert_not_called()


class TestPreviewStopMatchesSavedStop:
    """AC 2: the stop shown before save equals POST /portfolio/position's initial_stop."""

    @pytest.mark.parametrize("ticker,market,entry_price,atr", [
        ("AAPL", "US", 187.43, 3.1372),
        ("VOD", "UK", 72.18, 1.0449),
        ("LGEN.L", "UK", 250.0, 4.0),
    ])
    def test_preview_stop_equals_saved_initial_stop(self, ticker, market, entry_price, atr):
        preview, preview_atr_call = _preview(ticker, market, atr)
        previewed_atr = preview.json()["data"]["atr"]
        shown_stop = round(entry_price - INITIAL_ATR_MULTIPLIER * previewed_atr, 2)

        saved, save_atr_call = _save(ticker=ticker, market=market, entry_price=entry_price, fetched_atr=atr)

        assert saved["initial_stop"] == shown_stop
        # Both paths fetch the ATR for the same symbol.
        assert preview_atr_call.call_args.args[0] == save_atr_call.call_args.args[0]
