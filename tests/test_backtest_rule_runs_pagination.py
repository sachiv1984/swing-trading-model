"""
GET /strategy/backtest-rule-change/runs pagination + validation tests
(ST-10, EPIC-03, v9.6, BLG-BE-118).

Covers:
  - A negative `limit` or `offset` returns HTTP 400 INVALID_PARAMS instead
    of an unguarded 500 (a negative LIMIT/OFFSET previously reached
    PostgreSQL unvalidated).
  - Existing (non-negative `limit`, default `offset`) behaviour is
    unchanged.
  - `offset` is passed through to database.get_backtest_rule_runs.

CI-safe: no live DB or network connections — TestClient(app) with the
router's imported `get_backtest_rule_runs` patched per test (same pattern
as test_router_error_envelope_conformance.py).
"""
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)

_SAMPLE_RUN = {
    "id": "3f1b2c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
    "initiated_by": "Product Owner",
    "rule_diff_summary": "min_hold_days: 10 -> 15",
    "universe_start_date": datetime(2022, 8, 18, tzinfo=timezone.utc),
    "universe_end_date": datetime(2026, 8, 18, tzinfo=timezone.utc),
    "universe_size": 20,
    "candidate_result": {"trade_count": 34},
    "live_result": {"trade_count": 31},
    "created_at": datetime(2026, 8, 18, 10, 0, 0, tzinfo=timezone.utc),
}


class TestNegativeParamsRejected:
    def test_negative_limit_returns_400_invalid_params(self):
        resp = CLIENT.get("/strategy/backtest-rule-change/runs?limit=-1")
        assert resp.status_code == 400
        body = resp.json()
        assert body["status"] == "error"
        assert "INVALID_PARAMS" in body["message"]

    def test_negative_offset_returns_400_invalid_params(self):
        resp = CLIENT.get("/strategy/backtest-rule-change/runs?offset=-5")
        assert resp.status_code == 400
        body = resp.json()
        assert body["status"] == "error"
        assert "INVALID_PARAMS" in body["message"]

    def test_both_negative_returns_400_invalid_params(self):
        resp = CLIENT.get("/strategy/backtest-rule-change/runs?limit=-1&offset=-1")
        assert resp.status_code == 400


class TestValidParamsUnchanged:
    @patch("routers.backtest_rule_change.get_backtest_rule_runs", return_value=[dict(_SAMPLE_RUN)])
    def test_default_params_still_200(self, mock_get):
        resp = CLIENT.get("/strategy/backtest-rule-change/runs")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
        mock_get.assert_called_once_with(limit=20, offset=0)

    @patch("routers.backtest_rule_change.get_backtest_rule_runs", return_value=[dict(_SAMPLE_RUN)])
    def test_explicit_limit_zero_is_valid_not_400(self, mock_get):
        # 0 is non-negative — must not be rejected by the new validation.
        resp = CLIENT.get("/strategy/backtest-rule-change/runs?limit=0")
        assert resp.status_code == 200
        mock_get.assert_called_once_with(limit=0, offset=0)


class TestOffsetPassthrough:
    @patch("routers.backtest_rule_change.get_backtest_rule_runs", return_value=[dict(_SAMPLE_RUN)])
    def test_offset_forwarded_to_database_call(self, mock_get):
        resp = CLIENT.get("/strategy/backtest-rule-change/runs?limit=10&offset=20")
        assert resp.status_code == 200
        mock_get.assert_called_once_with(limit=10, offset=20)
