"""
SC-HEALTH-01 — GET /health and GET /health/database response schema validation.

Closes TSG-v22-02 (docs/specs/Specs_Index.md §10.2, identified 2026-03-24,
open ~24 cycles): "Automated test for GET /health and GET /health/database
response schemas not yet in CI."

Acceptance criteria derived directly from the canonical contract
(docs/specs/api_contracts/health_endpoints.md):
- GET /health returns status, db, last_market_status_check,
  last_alert_evaluation, external_apis, ai_journal with the documented
  types and nested shapes.
- GET /health/database returns size_bytes, size_mb, limit_bytes, limit_mb,
  used_percent, threshold_percent, status with the documented types.

All tests mock DB and external calls — no live connections required
(per SBX-NO-LIVE-DB, shared_standards.md §16.16).
"""

from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


class TestGetHealthResponseSchema:
    """SC-HEALTH-01a — GET /health response matches health_endpoints.md's documented schema."""

    def setup_method(self):
        from services.health_service import _ext_api_state
        _ext_api_state["alpaca"]["calls"].clear()
        _ext_api_state["alpaca"]["last_successful_call"] = None
        _ext_api_state["yahoo_finance"]["calls"].clear()
        _ext_api_state["yahoo_finance"]["last_successful_call"] = None

    def test_top_level_keys_present(self):
        """Every top-level field documented in health_endpoints.md's GET /health response is present."""
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p:
            mock_p.return_value = {}
            result = get_operational_health()

        expected_keys = {
            "status", "db", "last_market_status_check", "last_alert_evaluation",
            "external_apis", "ai_journal",
        }
        assert expected_keys.issubset(result.keys()), (
            f"Missing keys: {expected_keys - result.keys()}"
        )

    def test_status_and_db_are_documented_enum_values(self):
        """`status` and `db` are restricted to the two values health_endpoints.md documents."""
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p:
            mock_p.return_value = {}
            result = get_operational_health()
        assert result["status"] in ("ok", "error")
        assert result["db"] in ("connected", "error")

    def test_healthy_db_reports_ok_status_and_connected_db(self):
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p:
            mock_p.return_value = {}
            result = get_operational_health()
        assert result["status"] == "ok"
        assert result["db"] == "connected"

    def test_db_failure_reports_error_status_and_error_db(self):
        """A DB call failure surfaces as status=error, db=error — not silently masked."""
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio', side_effect=RuntimeError("connection refused")):
            result = get_operational_health()
        assert result["status"] == "error"
        assert result["db"] == "error"

    def test_timestamp_fields_are_string_or_null(self):
        """last_market_status_check / last_alert_evaluation are ISO-8601 strings or null (cold-start case)."""
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p:
            mock_p.return_value = {}
            result = get_operational_health()
        assert result["last_market_status_check"] is None or isinstance(result["last_market_status_check"], str)
        assert result["last_alert_evaluation"] is None or isinstance(result["last_alert_evaluation"], str)

    def test_external_apis_has_documented_shape_for_each_provider(self):
        """external_apis is keyed by provider name; each entry has the 3 documented fields."""
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p:
            mock_p.return_value = {}
            result = get_operational_health()

        assert set(result["external_apis"].keys()) >= {"alpaca", "yahoo_finance"}
        for provider, entry in result["external_apis"].items():
            assert set(entry.keys()) == {"last_successful_call", "error_rate", "p95_latency_ms"}, (
                f"{provider} entry has unexpected shape: {entry}"
            )
            assert isinstance(entry["error_rate"], (int, float))
            assert 0.0 <= entry["error_rate"] <= 1.0
            assert entry["last_successful_call"] is None or isinstance(entry["last_successful_call"], str)
            assert entry["p95_latency_ms"] is None or isinstance(entry["p95_latency_ms"], (int, float))

    def test_ai_journal_unavailable_shape_when_no_activity(self):
        """With no AI journal activity, ai_journal collapses to {"status": "unavailable"} per spec."""
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p, \
             patch('services.health_service.get_ai_journal_health') as mock_ai:
            mock_p.return_value = {}
            mock_ai.return_value = {"status": "unavailable"}
            result = get_operational_health()
        assert result["ai_journal"] == {"status": "unavailable"}

    def test_ai_journal_active_shape_has_three_documented_fields(self):
        """With activity, ai_journal reports the 3 documented metric fields, not the unavailable shape."""
        from services.health_service import get_operational_health
        with patch('services.health_service.get_portfolio') as mock_p, \
             patch('services.health_service.get_ai_journal_health') as mock_ai:
            mock_p.return_value = {}
            mock_ai.return_value = {"usage_rate": 3.5714, "error_rate": 0.0, "p95_latency_ms": 1820}
            result = get_operational_health()
        assert set(result["ai_journal"].keys()) == {"usage_rate", "error_rate", "p95_latency_ms"}
        assert isinstance(result["ai_journal"]["usage_rate"], (int, float))
        assert isinstance(result["ai_journal"]["error_rate"], (int, float))


class TestGetHealthDatabaseResponseSchema:
    """SC-HEALTH-01b — GET /health/database response matches health_endpoints.md's documented schema."""

    def test_top_level_keys_present_on_success(self):
        from services.health_service import get_db_size_info
        with patch('services.health_service.get_database_size_bytes', return_value=52_428_800):
            result = get_db_size_info()

        expected_keys = {
            "size_bytes", "size_mb", "limit_bytes", "limit_mb",
            "used_percent", "threshold_percent", "status",
        }
        assert set(result.keys()) == expected_keys, (
            f"Unexpected keys: {set(result.keys()) ^ expected_keys}"
        )

    def test_field_types_match_spec_on_success(self):
        from services.health_service import get_db_size_info
        with patch('services.health_service.get_database_size_bytes', return_value=52_428_800):
            result = get_db_size_info()

        assert isinstance(result["size_bytes"], int)
        assert isinstance(result["size_mb"], float)
        assert isinstance(result["limit_bytes"], int)
        assert isinstance(result["limit_mb"], float)
        assert isinstance(result["used_percent"], float)
        assert isinstance(result["threshold_percent"], float)
        assert result["status"] in ("ok", "warning", "error")

    def test_limit_bytes_matches_render_free_tier_256mb(self):
        """limit_bytes is the fixed 256 MB Render free-tier constant documented in the spec."""
        from services.health_service import get_db_size_info
        with patch('services.health_service.get_database_size_bytes', return_value=1_000_000):
            result = get_db_size_info()
        assert result["limit_bytes"] == 268_435_456
        assert result["limit_mb"] == 256.0

    def test_status_ok_below_threshold(self):
        from services.health_service import get_db_size_info
        # ~10% of 256MB — well below the default 80% threshold
        with patch('services.health_service.get_database_size_bytes', return_value=26_843_546):
            result = get_db_size_info()
        assert result["status"] == "ok"

    def test_status_warning_at_or_above_threshold(self):
        from services.health_service import get_db_size_info
        # ~85% of 256MB — above the default 80% threshold
        with patch('services.health_service.get_database_size_bytes', return_value=228_170_137):
            result = get_db_size_info()
        assert result["status"] == "warning"

    def test_query_failure_returns_error_status_not_exception(self):
        """A size-query failure surfaces as status=error in the response, not an unhandled exception."""
        from services.health_service import get_db_size_info
        with patch('services.health_service.get_database_size_bytes', side_effect=RuntimeError("db unreachable")):
            result = get_db_size_info()
        assert result["status"] == "error"
        assert result["size_bytes"] is None
        assert result["size_mb"] is None
        assert result["used_percent"] is None
        # limit_bytes/limit_mb/threshold_percent remain populated even on failure (fixed constants)
        assert result["limit_bytes"] == 268_435_456
