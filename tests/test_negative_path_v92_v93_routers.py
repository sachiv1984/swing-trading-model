"""
ST-17 (BLG-QA-176, EPIC-04, v9.7): Backfill negative-path tests for the 3
newest v9.2/v9.3 routers.

Identification (per this story's AC "3 routers identified"): the 3 newest
individual routes added during the v9.2 (2026-09-07__release-v9.2) / v9.3
(2026-09-09__release-v9.3) cycles, by commit date --

  1. POST /ai/check-endpoint-anomalies   (952ac326, 2026-09-14, v9.3 ST-09/BLG-OPS-151)
  2. POST /ops/purge-audit-logs           (a588d67f, 2026-09-10, v9.3 ST-13/BLG-OPS-94)
  3. GET  /ops/research-session-report    (a588d67f, 2026-09-10, v9.3 ST-12/BLG-OPS-20)

(Only one brand-new *router file* was added in this window, cost_monitoring.py
on 2026-09-10 -- "3 newest routers" in the AC's own wording is read here as
the 3 newest individual routes, since a single new file cannot itself supply
3 distinct "routers shipped". The 4th route added in the same commit as #2/#3,
GET /ops/monthly-cost-by-feature, and GET /alerts/history (e6845cbe,
2026-09-09) were considered and are not among the 3 selected -- #2 and #3
were prioritised over the omitted #4 for having the most negative-path-
relevant behaviour: #2 is destructive (delete) and #3 has real
divide-by-zero/empty-data edge cases in its own report computation.)

Each already has positive-path coverage in tests/test_cost_monitoring.py.
This file adds the negative paths that were missing: missing/invalid
X-API-Key auth (all three), and method-not-allowed for the wrong HTTP verb.
"""
from fastapi.testclient import TestClient

from main import app

CLIENT = TestClient(app, raise_server_exceptions=False)


class TestCheckEndpointAnomaliesNegativePaths:
    def test_missing_api_key_returns_401(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "real-key")
        try:
            r = CLIENT.post("/ai/check-endpoint-anomalies")
            assert r.status_code == 401
        finally:
            monkeypatch.delenv("API_KEY", raising=False)

    def test_wrong_api_key_returns_401(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "real-key")
        try:
            r = CLIENT.post("/ai/check-endpoint-anomalies", headers={"X-API-Key": "wrong-key"})
            assert r.status_code == 401
        finally:
            monkeypatch.delenv("API_KEY", raising=False)

    def test_get_method_not_allowed(self):
        """This endpoint is POST-only -- GET must be rejected, not silently accepted
        or routed elsewhere."""
        r = CLIENT.get("/ai/check-endpoint-anomalies")
        assert r.status_code == 405


class TestPurgeAuditLogsNegativePaths:
    def test_missing_api_key_returns_401(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "real-key")
        try:
            r = CLIENT.post("/ops/purge-audit-logs")
            assert r.status_code == 401
        finally:
            monkeypatch.delenv("API_KEY", raising=False)

    def test_wrong_api_key_returns_401(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "real-key")
        try:
            r = CLIENT.post("/ops/purge-audit-logs", headers={"X-API-Key": "wrong-key"})
            assert r.status_code == 401
        finally:
            monkeypatch.delenv("API_KEY", raising=False)

    def test_get_method_not_allowed(self):
        """This endpoint is POST-only (a destructive delete) -- GET must be
        rejected, not silently accepted."""
        r = CLIENT.get("/ops/purge-audit-logs")
        assert r.status_code == 405


class TestResearchSessionReportNegativePaths:
    def test_missing_api_key_returns_401(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "real-key")
        try:
            r = CLIENT.get("/ops/research-session-report")
            assert r.status_code == 401
        finally:
            monkeypatch.delenv("API_KEY", raising=False)

    def test_wrong_api_key_returns_401(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "real-key")
        try:
            r = CLIENT.get("/ops/research-session-report", headers={"X-API-Key": "wrong-key"})
            assert r.status_code == 401
        finally:
            monkeypatch.delenv("API_KEY", raising=False)

    def test_post_method_not_allowed(self):
        """This endpoint is GET-only (read-only report) -- POST must be rejected."""
        r = CLIENT.post("/ops/research-session-report")
        assert r.status_code == 405
