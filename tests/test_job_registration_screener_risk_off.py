"""
Job-registration wiring regression coverage for screener_refresh,
risk_off_alerts (ST-12, BLG-QA-149, EPIC-04, v8.9), and trailing_stop /
rebalance_exit / inv_vol_sizing (ST-05, BLG-OPS-160, EPIC-02, v9.5).

ST-01/ST-02 (v8.8) added `record_nightly_job("screener_refresh", ...)` (in
`backend/routers/screener.py`'s background run task) and
`record_nightly_job("risk_off_alerts", ...)` (in
`backend/main.py::risk_off_alerts_endpoint`), each on both the success and
error paths -- but nothing asserted these calls actually fire with the
correct job name and status. A future accidental removal, renaming, or
status-value typo in either call site would pass the rest of the suite
undetected. This file closes that gap.

ST-05 (BLG-OPS-160, v9.5) found `POST /positions/nightly-stop-update` and
`POST /signals/rebalance-exit` had the same job-registration wiring but no
scheduled trigger at all (fixed via new `nightly-stop-update.yml`/
`rebalance-exit.yml` GitHub Actions workflows) -- and, like screener_refresh/
risk_off_alerts originally, no test coverage of the wiring itself. Extended
this file's existing pattern to close that gap too, rather than leaving the
newly-scheduled jobs as the one pair in this registry without regression
coverage.

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


class TestNightlyStopUpdateJobRegistration:
    def test_success_path_records_trailing_stop_ok(self):
        with patch("main.run_nightly_trailing_stop_update", return_value={"updated": 3}), \
             patch("main.record_nightly_job") as mock_record:
            resp = CLIENT.post("/positions/nightly-stop-update")

        assert resp.status_code == 200
        mock_record.assert_called_once()
        args = mock_record.call_args.args
        assert args[0] == "trailing_stop"
        assert args[1] == "ok"

    def test_error_path_records_trailing_stop_error(self):
        with patch("main.run_nightly_trailing_stop_update", side_effect=RuntimeError("ATR lookup failed")), \
             patch("main.record_nightly_job") as mock_record:
            resp = CLIENT.post("/positions/nightly-stop-update")

        assert resp.status_code == 500
        mock_record.assert_called_once()
        args = mock_record.call_args.args
        assert args[0] == "trailing_stop"
        assert args[1] == "error"
        assert mock_record.call_args.kwargs.get("error") is not None


class TestRebalanceExitJobRegistration:
    def test_success_path_records_rebalance_exit_and_inv_vol_sizing_ok(self):
        """generate_rebalance_exit_signals() co-invokes inv_vol_sizing on
        the same success path (backend/main.py's own comment: "inv_vol_sizing
        runs inside generate_rebalance_exit_signals for sized signals") --
        both job names must be recorded, not just rebalance_exit."""
        with patch("main.generate_rebalance_exit_signals", return_value={"signals_created": 1}), \
             patch("main.record_nightly_job") as mock_record:
            resp = CLIENT.post("/signals/rebalance-exit")

        assert resp.status_code == 200
        assert mock_record.call_count == 2
        recorded_jobs = {call.args[0]: call.args[1] for call in mock_record.call_args_list}
        assert recorded_jobs == {"rebalance_exit": "ok", "inv_vol_sizing": "ok"}

    def test_error_path_records_rebalance_exit_error_only(self):
        """On failure, inv_vol_sizing must NOT also be recorded as ok --
        it is only co-invoked on the success path."""
        with patch("main.generate_rebalance_exit_signals", side_effect=RuntimeError("signal generation failed")), \
             patch("main.record_nightly_job") as mock_record:
            resp = CLIENT.post("/signals/rebalance-exit")

        assert resp.status_code == 500
        mock_record.assert_called_once()
        args = mock_record.call_args.args
        assert args[0] == "rebalance_exit"
        assert args[1] == "error"
        assert mock_record.call_args.kwargs.get("error") is not None
