"""
ST-08 (EPIC-02, v9.13, BLG-API-07): POST /settings and PATCH /settings/{settings_id}
reject a write that sets any of the four strategy parameters fixed by
strategy_rules.md §11 (min_hold_days, atr_period, atr_multiplier_initial,
atr_multiplier_trailing) with a 400, instead of storing a value no stop path
reads. API Contracts & Documentation Owner ruling (A), ESC-EXEC-20261017-04.

A field counts only when the request sets it to a non-null value: an absent
field or an explicit null is a no-op and the write proceeds.

CI-safe: create_settings / update_settings are patched; no live DB.
"""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    from fastapi.testclient import TestClient  # noqa: E402

    import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)

FIXED = ["min_hold_days", "atr_period", "atr_multiplier_initial", "atr_multiplier_trailing"]
VALUES = {"min_hold_days": 5, "atr_period": 20, "atr_multiplier_initial": 3.0, "atr_multiplier_trailing": 1.5}

# What the Settings page sends (it strips FIXED_STRATEGY_FIELDS, src/pages/Settings.js).
SETTINGS_PAGE_BODY = {
    "default_currency": "GBP", "theme": "dark", "uk_commission": 9.95, "us_commission": 0,
    "stamp_duty_rate": 0.005, "fx_fee_rate": 0.0015, "default_risk_percent": 1.0,
}


def _post(body):
    with patch.object(main, "create_settings", return_value={"id": "s-1"}) as mock_write:
        return CLIENT.post("/settings", json=body), mock_write


def _patch(body):
    with patch.object(main, "update_settings", return_value={"id": "s-1"}) as mock_write:
        return CLIENT.patch("/settings/s-1", json=body), mock_write


@pytest.mark.parametrize("send", [_post, _patch], ids=["POST", "PATCH"])
@pytest.mark.parametrize("field", FIXED)
def test_each_fixed_field_is_rejected_and_nothing_written(send, field):
    response, mock_write = send({**SETTINGS_PAGE_BODY, field: VALUES[field]})
    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "error"
    assert "strategy_rules.md §11" in body["message"]
    assert field in body["message"]
    assert "§12.3" in body["message"]
    mock_write.assert_not_called()


@pytest.mark.parametrize("send", [_post, _patch], ids=["POST", "PATCH"])
def test_several_fixed_fields_are_all_listed_in_order(send):
    response, _ = send({"atr_multiplier_trailing": 1.5, "min_hold_days": 5, "theme": "light"})
    assert response.status_code == 400
    assert response.json()["message"].startswith("min_hold_days, atr_multiplier_trailing cannot be set")


@pytest.mark.parametrize("send", [_post, _patch], ids=["POST", "PATCH"])
def test_explicit_null_is_a_no_op(send):
    response, mock_write = send({**SETTINGS_PAGE_BODY, **{f: None for f in FIXED}})
    assert response.status_code == 200
    mock_write.assert_called_once()


@pytest.mark.parametrize("send", [_post, _patch], ids=["POST", "PATCH"])
def test_settings_page_body_is_accepted(send):
    response, mock_write = send(SETTINGS_PAGE_BODY)
    assert response.status_code == 200
    mock_write.assert_called_once()


def test_message_values_come_from_the_section_11_constants():
    response, _ = _post({"atr_period": 20})
    message = response.json()["message"]
    assert f"grace period {main.GRACE_PERIOD_DAYS} days" in message
    assert f"ATR period {main.ATR_PERIOD_DAYS}" in message
    assert f"initial multiplier {main.INITIAL_ATR_MULTIPLIER:g}×" in message
    assert f"trailing multiplier {main.PROFIT_ATR_MULTIPLIER:g}×" in message
