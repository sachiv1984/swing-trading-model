"""Unit tests for the cost-monitoring instrumentation and reporting added in
ST-11/ST-12/ST-14 (EPIC-03, v9.3, BLG-OPS-17/BLG-OPS-20/BLG-OPS-96):
  - database.py: ensure_api_call_log_table, log_api_call, get_api_call_report,
    get_api_session_report, get_monthly_claude_cost_by_feature
  - routers/cost_monitoring.py: GET /ops/alpaca-call-report,
    GET /ops/research-session-report
  - routers/ai.py: GET /ai/monthly-cost-by-feature
  - services/alpaca_service.py: call-count logging on get_ohlcv_bars()

See tests/test_monthly_ai_cost.py for the mock-cursor pattern this file follows.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# conftest.py's database stub lacks the real implementations under test here —
# same rationale as test_monthly_ai_cost.py / test_signal_write_sanitization.py.
sys.modules.pop("database", None)
import database  # noqa: E402


def _mock_conn(fetchone_row=None, fetchall_rows=None):
    mock_cursor = MagicMock()
    if fetchone_row is not None:
        mock_cursor.fetchone.return_value = fetchone_row
    if fetchall_rows is not None:
        mock_cursor.fetchall.return_value = fetchall_rows
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


# ---------------------------------------------------------------------------
# log_api_call
# ---------------------------------------------------------------------------

def test_log_api_call_inserts_row_with_all_fields():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_api_call_log_table"):
            database.log_api_call("alpaca", "GET /v2/stocks/{symbol}/bars", session_id="sess-1", success=True)

    executed_sql, params = mock_cursor.execute.call_args[0]
    assert "api_call_log" in executed_sql
    assert params == ("alpaca", "GET /v2/stocks/{symbol}/bars", "sess-1", True)


def test_log_api_call_swallows_db_failure():
    """Fail-safe convention (matches create_claude_audit_entry) — instrumentation
    must never break the caller's actual request."""
    with patch.object(database, "get_db", side_effect=Exception("connection refused")):
        # Must not raise.
        database.log_api_call("alpaca", "GET /v2/stocks/{symbol}/bars", success=False)


# ---------------------------------------------------------------------------
# get_api_call_report (ST-11)
# ---------------------------------------------------------------------------

def test_get_api_call_report_daily_returns_counts():
    mock_conn, mock_cursor = _mock_conn(fetchone_row={"total_calls": 10, "success_count": 8, "failure_count": 2})
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_api_call_log_table"):
            result = database.get_api_call_report("alpaca", window="daily")
    assert result == {
        "service": "alpaca", "window": "daily",
        "total_calls": 10, "success_count": 8, "failure_count": 2,
    }


def test_get_api_call_report_weekly_uses_7_day_window():
    mock_conn, mock_cursor = _mock_conn(fetchone_row={"total_calls": 1, "success_count": 1, "failure_count": 0})
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_api_call_log_table"):
            database.get_api_call_report("alpaca", window="weekly")
    executed_sql = mock_cursor.execute.call_args[0][0]
    assert "INTERVAL '7 days'" in executed_sql


def test_get_api_call_report_db_failure_returns_zero_defaults():
    with patch.object(database, "get_db", side_effect=Exception("connection refused")):
        result = database.get_api_call_report("alpaca", window="daily")
    assert result == {
        "service": "alpaca", "window": "daily",
        "total_calls": 0, "success_count": 0, "failure_count": 0,
    }


# ---------------------------------------------------------------------------
# get_api_session_report (ST-12)
# ---------------------------------------------------------------------------

def test_get_api_session_report_computes_baseline_and_flags_anomalies():
    # 3 sessions: counts 1, 1, 10 -> mean = 4.0, threshold = 8.0 -> only the 10 is anomalous
    rows = [
        {"session_id": "s3", "call_count": 10},
        {"session_id": "s1", "call_count": 1},
        {"session_id": "s2", "call_count": 1},
    ]
    mock_conn, mock_cursor = _mock_conn(fetchall_rows=rows)
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_api_call_log_table"):
            result = database.get_api_session_report("research", anomaly_multiplier=2.0)

    assert result["session_count"] == 3
    assert result["baseline_calls_per_session"] == 4.0
    assert result["anomaly_multiplier"] == 2.0
    by_id = {s["session_id"]: s for s in result["sessions"]}
    assert by_id["s3"]["anomalous"] is True
    assert by_id["s1"]["anomalous"] is False
    assert by_id["s2"]["anomalous"] is False


def test_get_api_session_report_zero_sessions_no_anomalies_no_division_error():
    mock_conn, mock_cursor = _mock_conn(fetchall_rows=[])
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_api_call_log_table"):
            result = database.get_api_session_report("research")
    assert result["session_count"] == 0
    assert result["baseline_calls_per_session"] == 0.0
    assert result["sessions"] == []


def test_get_api_session_report_db_failure_returns_empty_defaults():
    with patch.object(database, "get_db", side_effect=Exception("connection refused")):
        result = database.get_api_session_report("research")
    assert result["session_count"] == 0
    assert result["sessions"] == []


# ---------------------------------------------------------------------------
# get_monthly_claude_cost_by_feature (ST-14)
# ---------------------------------------------------------------------------

def test_get_monthly_claude_cost_by_feature_groups_by_endpoint():
    rows = [
        {"endpoint": "POST /ai/daily-briefing", "total_cost": 0.0041, "request_count": 4},
        {"endpoint": "POST /trade-plans/{plan_id}/generate-thesis", "total_cost": 0.0022, "request_count": 2},
    ]
    mock_conn, mock_cursor = _mock_conn(fetchall_rows=rows)
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_claude_audit_log_table"):
            result = database.get_monthly_claude_cost_by_feature()

    assert result == [
        {"endpoint": "POST /ai/daily-briefing", "total_cost_usd": 0.0041, "request_count": 4},
        {"endpoint": "POST /trade-plans/{plan_id}/generate-thesis", "total_cost_usd": 0.0022, "request_count": 2},
    ]
    executed_sql = mock_cursor.execute.call_args[0][0]
    assert "GROUP BY endpoint" in executed_sql
    assert "date_trunc('month', NOW())" in executed_sql


def test_get_monthly_claude_cost_by_feature_no_calls_returns_empty_list():
    mock_conn, mock_cursor = _mock_conn(fetchall_rows=[])
    with patch.object(database, "get_db", return_value=mock_conn):
        with patch.object(database, "ensure_claude_audit_log_table"):
            result = database.get_monthly_claude_cost_by_feature()
    assert result == []


def test_get_monthly_claude_cost_by_feature_db_failure_returns_empty_list():
    with patch.object(database, "get_db", side_effect=Exception("connection refused")):
        result = database.get_monthly_claude_cost_by_feature()
    assert result == []


# ---------------------------------------------------------------------------
# alpaca_service.py instrumentation (ST-11)
# ---------------------------------------------------------------------------

def test_get_ohlcv_bars_logs_success_on_200():
    from services import alpaca_service

    mock_resp = MagicMock(status_code=200)
    mock_resp.json.return_value = {"bars": [{"t": "2026-01-01", "o": 1, "h": 2, "l": 0.5, "c": 1.5, "v": 100}]}

    with patch.object(alpaca_service, "_credentials_configured", return_value=True):
        with patch.object(alpaca_service.requests, "get", return_value=mock_resp):
            with patch.object(alpaca_service, "_log_alpaca_call") as mock_log:
                bars = alpaca_service.get_ohlcv_bars("AAPL")

    assert bars is not None
    mock_log.assert_called_once_with(success=True)


def test_get_ohlcv_bars_logs_failure_on_403():
    from services import alpaca_service

    mock_resp = MagicMock(status_code=403)

    with patch.object(alpaca_service, "_credentials_configured", return_value=True):
        with patch.object(alpaca_service.requests, "get", return_value=mock_resp):
            with patch.object(alpaca_service, "_log_alpaca_call") as mock_log:
                bars = alpaca_service.get_ohlcv_bars("AAPL")

    assert bars is None
    mock_log.assert_called_once_with(success=False)


def test_get_ohlcv_bars_no_credentials_does_not_log():
    """No call was actually attempted — nothing to log."""
    from services import alpaca_service

    with patch.object(alpaca_service, "_credentials_configured", return_value=False):
        with patch.object(alpaca_service, "_log_alpaca_call") as mock_log:
            bars = alpaca_service.get_ohlcv_bars("AAPL")

    assert bars is None
    mock_log.assert_not_called()


def test_log_alpaca_call_swallows_import_failure():
    """_log_alpaca_call itself must never raise, even if database import fails."""
    from services import alpaca_service

    with patch("builtins.__import__", side_effect=ImportError("boom")):
        # Must not raise.
        alpaca_service._log_alpaca_call(success=True)


# ---------------------------------------------------------------------------
# routers/cost_monitoring.py (ST-11/ST-12)
# ---------------------------------------------------------------------------

def test_alpaca_call_report_endpoint_returns_ok():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app, raise_server_exceptions=False)
    with patch("database.get_api_call_report", return_value={
        "service": "alpaca", "window": "daily", "total_calls": 5, "success_count": 5, "failure_count": 0,
    }):
        r = client.get("/ops/alpaca-call-report")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["data"]["total_calls"] == 5


def test_alpaca_call_report_endpoint_rejects_invalid_window():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app, raise_server_exceptions=False)
    r = client.get("/ops/alpaca-call-report?window=monthly")
    assert r.status_code == 422


def test_research_session_report_endpoint_returns_ok():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app, raise_server_exceptions=False)
    with patch("database.get_api_session_report", return_value={
        "service": "research", "period_days": 7, "session_count": 0,
        "baseline_calls_per_session": 0.0, "anomaly_multiplier": 2.0, "sessions": [],
    }):
        r = client.get("/ops/research-session-report")
    assert r.status_code == 200
    assert r.json()["data"]["service"] == "research"


# ---------------------------------------------------------------------------
# routers/ai.py — GET /ai/monthly-cost-by-feature (ST-14)
# ---------------------------------------------------------------------------

def test_monthly_cost_by_feature_endpoint_returns_ok():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app, raise_server_exceptions=False)
    with patch("database.get_monthly_claude_cost_by_feature", return_value=[
        {"endpoint": "POST /ai/chat", "total_cost_usd": 0.01, "request_count": 3},
    ]):
        r = client.get("/ai/monthly-cost-by-feature")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["data"]["features"][0]["endpoint"] == "POST /ai/chat"


def test_monthly_cost_by_feature_endpoint_empty_month_returns_empty_list():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app, raise_server_exceptions=False)
    with patch("database.get_monthly_claude_cost_by_feature", return_value=[]):
        r = client.get("/ai/monthly-cost-by-feature")
    assert r.status_code == 200
    assert r.json()["data"]["features"] == []


# ---------------------------------------------------------------------------
# routers/research.py session logging (ST-12)
# ---------------------------------------------------------------------------

def test_get_research_logs_4_external_calls_with_one_shared_session_id():
    """A cache-miss GET /research/{ticker} request logs exactly 4 external
    calls (_get_price_data, _get_earnings, _get_market_cap, _get_news) — not
    the 4 internal/DB-backed helpers (_get_regime, _get_signal, _get_sector,
    _get_screener) — all tagged with the same session_id."""
    import routers.research as research

    research._research_cache.clear()

    with patch.object(research, "get_portfolio", return_value=None), \
         patch.object(research, "_get_price_data", return_value={"price": 100.0, "price_change_pct": 1.0}), \
         patch.object(research, "_get_regime", return_value=None), \
         patch.object(research, "_get_sector", return_value={"sector": None, "industry": None}), \
         patch.object(research, "_get_screener", return_value=None), \
         patch.object(research, "_get_earnings", return_value=None), \
         patch.object(research, "_get_market_cap", return_value=None), \
         patch.object(research, "_get_news", return_value=[]), \
         patch.object(research, "_log_research_call") as mock_log:
        research.get_research("NEWTICKER", market="US")

    assert mock_log.call_count == 4
    session_ids = {call.args[0] for call in mock_log.call_args_list}
    assert len(session_ids) == 1, "all 4 calls must share one session_id"
    logged_endpoints = {call.args[1] for call in mock_log.call_args_list}
    assert logged_endpoints == {"_get_price_data", "_get_earnings", "_get_market_cap", "_get_news"}


def test_get_research_cache_hit_logs_nothing():
    """A cache hit makes no external calls — nothing should be logged."""
    import routers.research as research
    import time as time_module

    research._research_cache.clear()
    research._research_cache[("CACHEDTICKER", "US")] = {
        "data": {"status": "ok", "data": {"ticker": "CACHEDTICKER"}},
        "expires_at": time_module.monotonic() + 900,
    }

    with patch.object(research, "_log_research_call") as mock_log:
        research.get_research("CACHEDTICKER", market="US")

    mock_log.assert_not_called()
    research._research_cache.clear()


def test_get_research_yf_unavailable_still_logs_price_data_call_as_failure():
    import routers.research as research

    research._research_cache.clear()

    with patch.object(research, "get_portfolio", return_value=None), \
         patch.object(research, "_get_price_data", return_value=research._YF_UNAVAILABLE), \
         patch.object(research, "_log_research_call") as mock_log:
        research.get_research("UNAVAILTICKER", market="US")

    mock_log.assert_called_once()
    call = mock_log.call_args
    assert call.args[1] == "_get_price_data"
    assert call.kwargs["success"] is False


def test_log_research_call_swallows_import_failure():
    import routers.research as research

    with patch("builtins.__import__", side_effect=ImportError("boom")):
        # Must not raise.
        research._log_research_call("sess-1", "_get_news", success=True)


# ---------------------------------------------------------------------------
# purge_claude_audit_log_older_than_730_days (ST-13)
# ---------------------------------------------------------------------------

def test_purge_claude_audit_log_returns_deleted_count():
    mock_conn, mock_cursor = _mock_conn()
    mock_cursor.rowcount = 7
    with patch.object(database, "get_db", return_value=mock_conn):
        result = database.purge_claude_audit_log_older_than_730_days()
    assert result == 7
    executed_sql = mock_cursor.execute.call_args[0][0]
    assert "claude_audit_log" in executed_sql
    assert "INTERVAL '730 days'" in executed_sql


def test_purge_claude_audit_log_db_failure_returns_zero_not_exception():
    with patch.object(database, "get_db", side_effect=Exception("connection refused")):
        result = database.purge_claude_audit_log_older_than_730_days()
    assert result == 0


# ---------------------------------------------------------------------------
# routers/cost_monitoring.py — POST /ops/purge-audit-logs (ST-13)
# ---------------------------------------------------------------------------

def test_purge_audit_logs_endpoint_returns_both_counts():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app, raise_server_exceptions=False)
    with patch("database.purge_gemini_audit_log_older_than_90_days", return_value=3), \
         patch("database.purge_claude_audit_log_older_than_730_days", return_value=5):
        r = client.post("/ops/purge-audit-logs")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["data"] == {
        "gemini_audit_log_rows_deleted": 3,
        "claude_audit_log_rows_deleted": 5,
    }


def test_purge_audit_logs_endpoint_calls_both_purge_functions_even_when_idempotent():
    """Both tables are always attempted, regardless of how many rows qualify."""
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app, raise_server_exceptions=False)
    with patch("database.purge_gemini_audit_log_older_than_90_days", return_value=0) as mock_gemini, \
         patch("database.purge_claude_audit_log_older_than_730_days", return_value=0) as mock_claude:
        r = client.post("/ops/purge-audit-logs")
    assert r.status_code == 200
    mock_gemini.assert_called_once()
    mock_claude.assert_called_once()
