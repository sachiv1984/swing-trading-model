"""
Job-registration wiring regression coverage for screener_refresh and
risk_off_alerts (ST-12, BLG-QA-149, EPIC-04, v8.9).

ST-01/ST-02 (v8.8) added `record_nightly_job("screener_refresh", ...)` (in
`backend/routers/screener.py`'s background run task) and
`record_nightly_job("risk_off_alerts", ...)` (in
`backend/main.py::risk_off_alerts_endpoint`), each on both the success and
error paths -- but nothing asserted these calls actually fire with the
correct job name and status. A future accidental removal, renaming, or
status-value typo in either call site would pass the rest of the suite
undetected. This file closes that gap.

CI-safe: no live DB or network connections -- TestClient(app) with the
session-scoped database stub; `run_screener`/`run_nightly_risk_off_alerts`
and `record_nightly_job` are mocked directly at their call sites.

POST /screener/run's job-recording happens inside a BackgroundTasks task
(`_run_in_background`, a closure). Starlette's TestClient runs background
tasks synchronously as part of the request/response cycle before returning
the response object, so `record_nightly_job` has already been called by
the time `CLIENT.post(...)` returns -- no additional wait/poll needed.
"""

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.modules.pop("database", None)

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402

CLIENT = TestClient(app, raise_server_exceptions=False)


class TestScreenerRefreshJobRegistration:
    def test_success_path_records_screener_refresh_ok(self):
        with patch("routers.screener.run_screener", return_value={"tickers_scanned": 20}), \
             patch("routers.screener.is_run_in_progress", return_value=False), \
             patch("routers.research.invalidate_research_cache"), \
             patch("routers.screener.record_nightly_job") as mock_record:
            resp = CLIENT.post("/screener/run", json={})

        assert resp.status_code == 202
        mock_record.assert_called_once()
        args = mock_record.call_args.args
        assert args[0] == "screener_refresh"
        assert args[1] == "ok"

    def test_error_path_records_screener_refresh_error(self):
        with patch("routers.screener.run_screener", side_effect=RuntimeError("data source unavailable")), \
             patch("routers.screener.is_run_in_progress", return_value=False), \
             patch("routers.screener.record_nightly_job") as mock_record:
            resp = CLIENT.post("/screener/run", json={})

        assert resp.status_code == 202  # 202 is returned before the background task runs
        mock_record.assert_called_once()
        args = mock_record.call_args.args
        assert args[0] == "screener_refresh"
        assert args[1] == "error"
        assert mock_record.call_args.kwargs.get("error") is not None


class TestRiskOffAlertsJobRegistration:
    def test_success_path_records_risk_off_alerts_ok(self):
        with patch("main.run_nightly_risk_off_alerts", return_value={"flagged": 2}), \
             patch("main.record_nightly_job") as mock_record:
            resp = CLIENT.post("/positions/risk-off-alerts")

        assert resp.status_code == 200
        mock_record.assert_called_once()
        args = mock_record.call_args.args
        assert args[0] == "risk_off_alerts"
        assert args[1] == "ok"

    def test_error_path_records_risk_off_alerts_error(self):
        with patch("main.run_nightly_risk_off_alerts", side_effect=RuntimeError("regime lookup failed")), \
             patch("main.record_nightly_job") as mock_record:
            resp = CLIENT.post("/positions/risk-off-alerts")

        assert resp.status_code == 500
        mock_record.assert_called_once()
        args = mock_record.call_args.args
        assert args[0] == "risk_off_alerts"
        assert args[1] == "error"
        assert mock_record.call_args.kwargs.get("error") is not None
