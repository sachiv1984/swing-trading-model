"""
Tests for ST-08 (External API Health) and ST-09 (AI Journal Health).

All tests mock DB and external calls — no live connections required.
"""

import math
from unittest.mock import MagicMock, patch
import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


# ---------------------------------------------------------------------------
# ST-08 — External API Health
# ---------------------------------------------------------------------------

class TestExternalApiHealth:

    def setup_method(self):
        from services.health_service import _ext_api_state
        # Reset state between tests
        _ext_api_state["alpaca"]["calls"].clear()
        _ext_api_state["alpaca"]["last_successful_call"] = None
        _ext_api_state["yahoo_finance"]["calls"].clear()
        _ext_api_state["yahoo_finance"]["last_successful_call"] = None

    def test_empty_state_returns_zero_error_rate(self):
        from services.health_service import get_external_api_health
        result = get_external_api_health()
        assert result["alpaca"]["error_rate"] == 0.0
        assert result["yahoo_finance"]["error_rate"] == 0.0
        assert result["alpaca"]["last_successful_call"] is None
        assert result["alpaca"]["p95_latency_ms"] is None

    def test_record_successful_call_updates_last_successful(self):
        from services.health_service import record_external_api_call, get_external_api_health
        record_external_api_call("alpaca", True, 150.0)
        result = get_external_api_health()
        assert result["alpaca"]["last_successful_call"] is not None
        assert result["alpaca"]["error_rate"] == 0.0

    def test_record_failed_call_sets_error_rate(self):
        from services.health_service import record_external_api_call, get_external_api_health
        record_external_api_call("alpaca", False, 50.0)
        record_external_api_call("alpaca", False, 50.0)
        record_external_api_call("alpaca", True, 100.0)
        result = get_external_api_health()
        assert result["alpaca"]["last_successful_call"] is not None
        assert result["alpaca"]["error_rate"] == pytest.approx(2 / 3, abs=0.001)

    def test_p95_latency_computed_from_successful_calls(self):
        from services.health_service import record_external_api_call, get_external_api_health
        latencies = [100.0 * i for i in range(1, 21)]  # 100..2000 ms
        for lat in latencies:
            record_external_api_call("yahoo_finance", True, lat)
        result = get_external_api_health()
        p95 = result["yahoo_finance"]["p95_latency_ms"]
        assert p95 is not None
        # p95 of 20 values: index ceil(0.95*20)-1 = 18 → sorted[18] = 1900
        assert p95 == 1900

    def test_unknown_api_name_ignored(self):
        from services.health_service import record_external_api_call
        record_external_api_call("nonexistent_api", True, 100.0)  # no exception

    def test_degraded_response_structure(self):
        from services.health_service import record_external_api_call, get_external_api_health
        record_external_api_call("alpaca", False, 5000.0)
        result = get_external_api_health()
        assert "last_successful_call" in result["alpaca"]
        assert "error_rate" in result["alpaca"]
        assert "p95_latency_ms" in result["alpaca"]


# ---------------------------------------------------------------------------
# ST-08 — GET /health includes external_apis and ai_journal sections
# ---------------------------------------------------------------------------

class TestOperationalHealthIncludes:

    def test_health_response_includes_external_apis(self):
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p:
            mock_p.return_value = {}
            result = get_operational_health()
        assert "external_apis" in result
        assert "alpaca" in result["external_apis"]
        assert "yahoo_finance" in result["external_apis"]

    def test_health_response_includes_ai_journal(self):
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p, \
             patch('services.health_service.get_ai_journal_health') as mock_ai:
            mock_p.return_value = {}
            mock_ai.return_value = {"status": "unavailable"}
            result = get_operational_health()
        assert "ai_journal" in result


# ---------------------------------------------------------------------------
# ST-09 — AI Journal Health
# ---------------------------------------------------------------------------

class TestAiJournalHealth:

    def _make_db_mock(self, count_7d=0, total_24h=0, failed_24h=0, durations=None):
        conn = MagicMock()
        cur = MagicMock()
        ctx = MagicMock()
        ctx.__enter__ = MagicMock(return_value=cur)
        ctx.__exit__ = MagicMock(return_value=False)
        conn.cursor.return_value = ctx
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)

        dur_rows = [(d,) for d in sorted(durations or [])]

        call_count = [0]
        def fetchone_side():
            call_count[0] += 1
            if call_count[0] == 1:
                return (count_7d,)
            if call_count[0] == 2:
                return (total_24h, failed_24h)
            return None

        def fetchall_side():
            return dur_rows

        cur.fetchone.side_effect = fetchone_side
        cur.fetchall.side_effect = fetchall_side
        return conn

    def test_unavailable_when_no_data(self):
        from services.health_service import get_ai_journal_health
        conn = self._make_db_mock(count_7d=0, total_24h=0, failed_24h=0)
        with patch('database.get_db', return_value=conn):
            result = get_ai_journal_health()
        assert result == {"status": "unavailable"}

    def test_populated_metrics(self):
        from services.health_service import get_ai_journal_health
        conn = self._make_db_mock(
            count_7d=14, total_24h=4, failed_24h=1, durations=[500, 600, 700, 800]
        )
        with patch('database.get_db', return_value=conn):
            result = get_ai_journal_health()
        assert result["usage_rate"] == pytest.approx(2.0, abs=0.01)
        assert result["error_rate"] == pytest.approx(0.25, abs=0.001)
        assert result["p95_latency_ms"] is not None

    def test_error_rate_zero_when_all_success(self):
        from services.health_service import get_ai_journal_health
        conn = self._make_db_mock(count_7d=7, total_24h=3, failed_24h=0)
        with patch('database.get_db', return_value=conn):
            result = get_ai_journal_health()
        assert result["error_rate"] == 0.0

    def test_exception_returns_unavailable(self):
        from services.health_service import get_ai_journal_health
        with patch('database.get_db', side_effect=Exception("DB down")):
            result = get_ai_journal_health()
        assert result == {"status": "unavailable"}

    def test_empty_audit_table_graceful(self):
        from services.health_service import get_ai_journal_health
        conn = self._make_db_mock(count_7d=0, total_24h=0, failed_24h=0, durations=[])
        with patch('database.get_db', return_value=conn):
            result = get_ai_journal_health()
        assert result == {"status": "unavailable"}
