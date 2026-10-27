"""
ST-28 (BLG-OPS-187, EPIC-05, v9.13) — the daily AI cost alert fails loudly.

get_daily_ai_cost() swallowed any query error and returned a $0 total, so a
broken cost query looked like "no spend today": the endpoint answered 200,
the workflow step passed and no alert could ever fire.

- AC 1: a simulated cost-query failure is logged, reported as an error
  status (503, status "error") and fails the workflow step (curl
  --fail-with-body on a non-2xx).
- AC 2 (automated half): ai-daily-cost-check.yml sends a Telegram message
  when any step fails. The real failed-run receipt is a staging-only check.
"""
import logging
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    import database as real_database  # noqa: E402
    from fastapi.testclient import TestClient  # noqa: E402

    import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)
WORKFLOW = Path(__file__).parent.parent / ".github" / "workflows" / "ai-daily-cost-check.yml"


def _failing_db():
    cur = MagicMock()
    cur.execute.side_effect = RuntimeError("relation claude_audit_log does not exist")
    cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
    conn = MagicMock(__exit__=MagicMock(return_value=False))
    conn.__enter__ = MagicMock(return_value=conn)
    conn.cursor.return_value = cur_ctx
    return conn


class TestQueryFailure:
    def test_real_query_raises_instead_of_returning_zero(self):
        with patch.object(real_database, "get_db", side_effect=_failing_db), \
             patch.object(real_database, "ensure_claude_audit_log_table"):
            with pytest.raises(RuntimeError):
                real_database.get_daily_ai_cost()

    def test_service_logs_and_returns_error_status(self, caplog):
        from services.gemini_service import check_and_alert_daily_cost
        with patch("database.get_daily_ai_cost", side_effect=RuntimeError("db down")), \
             patch("urllib.request.urlopen") as urlopen, \
             caplog.at_level(logging.ERROR):
            result = check_and_alert_daily_cost(threshold_usd=1.00)
        assert result["status"] == "error"
        assert result["error"] == "cost_query_failed"
        assert "total_cost_usd" not in result and "request_count" not in result
        assert not urlopen.called
        assert any("Daily AI cost query failed" in r.getMessage() and r.exc_info for r in caplog.records)

    def test_endpoint_returns_503_on_query_failure(self):
        with patch("database.get_daily_ai_cost", side_effect=RuntimeError("db down")):
            resp = CLIENT.post("/ai/check-daily-cost")
        assert resp.status_code == 503
        body = resp.json()
        assert body["status"] == "error" and body["error"] == "cost_query_failed"

    def test_endpoint_200_with_ok_status_on_success(self):
        with patch("database.get_daily_ai_cost", return_value={"total_cost_usd": 0.10, "request_count": 2}):
            resp = CLIENT.post("/ai/check-daily-cost")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok" and body["total_cost_usd"] == 0.10


class TestWorkflowFailsLoudly:
    def _steps(self):
        wf = yaml.safe_load(WORKFLOW.read_text())
        return wf["jobs"]["check-daily-cost"]["steps"]

    def test_trigger_step_fails_on_non_2xx(self):
        trigger = self._steps()[0]["run"]
        assert "curl --fail-with-body" in trigger
        assert '"${API_URL}/ai/check-daily-cost"' in trigger

    def test_trigger_step_fails_when_secrets_missing(self):
        trigger = self._steps()[0]["run"]
        assert '[ -z "$API_URL" ] || [ -z "$API_KEY" ]' in trigger
        assert "exit 1" in trigger

    def test_failure_step_sends_telegram(self):
        alert = self._steps()[-1]
        assert alert["if"] == "failure()"
        assert alert["env"]["TELEGRAM_BOT_TOKEN"] == "${{ secrets.TELEGRAM_BOT_TOKEN }}"
        assert alert["env"]["TELEGRAM_CHAT_ID"] == "${{ secrets.TELEGRAM_CHAT_ID }}"
        assert "api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" in alert["run"]
