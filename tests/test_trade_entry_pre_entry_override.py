"""
ST-01 (BLG-FE-244, EPIC-01, v9.15): Trade Entry shows the pre-entry checks on
every route, and an entry saved with the acknowledgement ticked records the
override the same way the Trade Plan path does (position_form.md §Pre-Entry
Checks, decision record §2.4): one red_flag_events row with
event_type "pre_entry_override" and context.source "trade_entry". A failed
event write never fails the save.

ST-05 (BLG-FE-222): POST /portfolio/position normalises the ticker (trim,
upper-case) before add_position() sees it.
"""
import sys
from pathlib import Path
from unittest.mock import patch

BACKEND = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(BACKEND))

_BODY = {
    "ticker": "AAPL", "market": "US", "entry_date": "2026-11-04",
    "shares": 10, "entry_price": 100.0, "fx_rate": 1.3,
}
_RESULT = {"position_id": "pos-1", "ticker": "AAPL", "initial_stop": 90.0}


def _client():
    from tests._real_database import real_database_imports
    with real_database_imports():
        from fastapi.testclient import TestClient
        import main
    return TestClient(main.app, raise_server_exceptions=False), main


def _post(body, create_side_effect=None):
    client, main = _client()
    import database
    with patch.object(main, "add_position", return_value=_RESULT) as mock_add, \
         patch.object(database, "ensure_red_flag_events_table"), \
         patch.object(database, "create_red_flag_event", side_effect=create_side_effect) as mock_event, \
         patch("services.alpaca_paper_sync_service.sync_open_paper_position", create=True):
        response = client.post("/portfolio/position", json=body)
    return response, mock_add, mock_event


class TestTradeEntryOverrideEvent:
    def test_acknowledged_entry_writes_one_trade_entry_override_event(self):
        response, _, mock_event = _post({**_BODY, "pre_entry_override_acknowledged": True})
        assert response.status_code == 200
        mock_event.assert_called_once_with(
            event_type="pre_entry_override",
            ticker="AAPL",
            position_id="pos-1",
            context={"source": "trade_entry", "override_acknowledged": True},
        )

    def test_unacknowledged_entry_writes_no_event(self):
        for body in (_BODY, {**_BODY, "pre_entry_override_acknowledged": False}):
            response, _, mock_event = _post(body)
            assert response.status_code == 200
            mock_event.assert_not_called()

    def test_failed_event_write_does_not_fail_the_save(self):
        response, mock_add, _ = _post(
            {**_BODY, "pre_entry_override_acknowledged": True},
            create_side_effect=RuntimeError("db down"),
        )
        assert response.status_code == 200
        assert response.json()["data"]["position_id"] == "pos-1"
        mock_add.assert_called_once()

    def test_flag_is_not_passed_to_add_position(self):
        _, mock_add, _ = _post({**_BODY, "pre_entry_override_acknowledged": True})
        assert "pre_entry_override_acknowledged" not in mock_add.call_args.kwargs


class TestTickerNormalisedAtTheEndpoint:
    def test_untrimmed_lower_case_ticker_reaches_add_position_normalised(self):
        _, mock_add, _ = _post({**_BODY, "ticker": "  aapl "})
        assert mock_add.call_args.kwargs["ticker"] == "AAPL"
