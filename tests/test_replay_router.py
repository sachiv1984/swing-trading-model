"""
tests/test_replay_router.py — ST-01b (EPIC-01, v9.7, BLG-FEAT-74)

HTTP-level tests for POST /replay/run: the manual body-parsing/validation surface
(D2) and the error-code mapping (D5). Service-level behaviour (the simulation itself)
is covered by tests/test_replay_service.py; this file only exercises the router
boundary. CI-safe: TestClient(app) with `services.replay_service.run_replay` and
`database.get_portfolio` mocked -- no real DB connection, no network call.
"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402
from services.replay_service import ReplayPriceDataUnavailableError, ReplayScopeTooLargeError  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)


def _assert_canonical_error(resp, status_code, code=None):
    assert resp.status_code == status_code
    body = resp.json()
    assert body.get("status") == "error"
    assert isinstance(body.get("message"), str) and body["message"]
    assert "detail" not in body
    if code is not None:
        assert body.get("code") == code


# ── Structural validation (D2) -- every rejection uses the canonical envelope ────────

def test_missing_body_is_400_validation_error():
    resp = CLIENT.post("/replay/run")
    _assert_canonical_error(resp, 400, "validation_error")


def test_malformed_json_body_is_400_validation_error():
    resp = CLIENT.post("/replay/run", content=b"{not valid json", headers={"content-type": "application/json"})
    _assert_canonical_error(resp, 400, "validation_error")


def test_non_object_body_is_400_validation_error():
    for payload in ([1, 2, 3], "a string", 42, None):
        resp = CLIENT.post("/replay/run", json=payload)
        _assert_canonical_error(resp, 400, "validation_error")


def test_both_trade_ids_and_date_range_is_400():
    resp = CLIENT.post("/replay/run", json={"trade_ids": ["00000000-0000-0000-0000-000000000000"], "date_from": "2026-01-01", "date_to": "2026-01-02"})
    _assert_canonical_error(resp, 400, "validation_error")


def test_neither_trade_ids_nor_date_range_is_400():
    resp = CLIENT.post("/replay/run", json={})
    _assert_canonical_error(resp, 400, "validation_error")


def test_extra_field_is_400():
    resp = CLIENT.post("/replay/run", json={"trade_ids": ["00000000-0000-0000-0000-000000000000"], "extra_field": 1})
    _assert_canonical_error(resp, 400, "validation_error")
    resp2 = CLIENT.post("/replay/run", json={"date_from": "2026-01-01", "date_to": "2026-01-02", "rule_override": "x"})
    _assert_canonical_error(resp2, 400, "validation_error")


def test_empty_trade_ids_list_is_400():
    resp = CLIENT.post("/replay/run", json={"trade_ids": []})
    _assert_canonical_error(resp, 400, "validation_error")


def test_non_uuid_trade_id_is_400():
    resp = CLIENT.post("/replay/run", json={"trade_ids": ["not-a-uuid"]})
    _assert_canonical_error(resp, 400, "validation_error")


def test_trade_ids_not_a_list_is_400():
    resp = CLIENT.post("/replay/run", json={"trade_ids": "00000000-0000-0000-0000-000000000000"})
    _assert_canonical_error(resp, 400, "validation_error")


def test_date_range_missing_one_bound_is_400():
    resp = CLIENT.post("/replay/run", json={"date_from": "2026-01-01"})
    _assert_canonical_error(resp, 400, "validation_error")


def test_date_from_after_date_to_is_400():
    resp = CLIENT.post("/replay/run", json={"date_from": "2026-06-01", "date_to": "2026-01-01"})
    _assert_canonical_error(resp, 400, "validation_error")


def test_date_to_in_the_future_is_400():
    resp = CLIENT.post("/replay/run", json={"date_from": "2026-01-01", "date_to": "2099-01-01"})
    _assert_canonical_error(resp, 400, "validation_error")


def test_non_string_date_is_400():
    resp = CLIENT.post("/replay/run", json={"date_from": 20260101, "date_to": "2026-01-02"})
    _assert_canonical_error(resp, 400, "validation_error")


def test_malformed_date_string_is_400():
    resp = CLIENT.post("/replay/run", json={"date_from": "01/01/2026", "date_to": "2026-01-02"})
    _assert_canonical_error(resp, 400, "validation_error")


# ── Error-code mapping from the service layer (D5) ──────────────────────────────────

def test_scope_too_large_maps_to_400():
    with patch("routers.replay.run_replay", side_effect=ReplayScopeTooLargeError("too many trades")):
        resp = CLIENT.post("/replay/run", json={"trade_ids": ["00000000-0000-0000-0000-000000000000"]})
    _assert_canonical_error(resp, 400, "replay_scope_too_large")


def test_price_data_unavailable_maps_to_500():
    with patch("routers.replay.run_replay", side_effect=ReplayPriceDataUnavailableError("no data")):
        resp = CLIENT.post("/replay/run", json={"trade_ids": ["00000000-0000-0000-0000-000000000000"]})
    _assert_canonical_error(resp, 500, "price_data_unavailable")


def test_unexpected_error_maps_to_500_replay_failed():
    with patch("routers.replay.run_replay", side_effect=RuntimeError("boom")):
        resp = CLIENT.post("/replay/run", json={"trade_ids": ["00000000-0000-0000-0000-000000000000"]})
    _assert_canonical_error(resp, 500, "replay_failed")


def test_valid_request_reaches_the_service_and_returns_ok_envelope():
    fake_data = {"retrospective_notice": "x", "run": {}, "summary": {}, "trades": []}
    with patch("routers.replay.run_replay", return_value=fake_data) as mock_run:
        resp = CLIENT.post("/replay/run", json={"trade_ids": ["00000000-0000-0000-0000-000000000000"]})
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "data": fake_data}
    mock_run.assert_called_once()
    _, kwargs = mock_run.call_args
    assert kwargs["mode"] == "trade_set"
    assert kwargs["trade_ids"] == ["00000000-0000-0000-0000-000000000000"]


def test_valid_date_range_request_passes_parsed_dates_to_the_service():
    fake_data = {"retrospective_notice": "x", "run": {}, "summary": {}, "trades": []}
    with patch("routers.replay.run_replay", return_value=fake_data) as mock_run:
        resp = CLIENT.post("/replay/run", json={"date_from": "2023-01-01", "date_to": "2023-06-01"})
    assert resp.status_code == 200
    _, kwargs = mock_run.call_args
    assert kwargs["mode"] == "date_range"
    assert kwargs["date_from"].isoformat() == "2023-01-01"
    assert kwargs["date_to"].isoformat() == "2023-06-01"
