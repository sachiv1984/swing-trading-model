"""
Regression tests for scripts/staging_smoke_test.py (ST-13, BLG-OPS-25,
EPIC-03, v9.0).

Mocked-network unit tests for the matching/failure-detection logic. The
AC's "deliberate local test... confirms the new step actually catches
the regression" was additionally verified in-session against a real,
locally-running instance of backend/main.py backed by a real local
PostgreSQL server (not just these mocks) — see the ST-13 commit message
for the concrete failure sequence observed (missing tables/columns each
correctly surfaced as a smoke-test failure) and the eventual pass once
the schema was completed. These tests cover the script's logic in
isolation, CI-safe with no live network or DB.
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import urllib.error

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import staging_smoke_test as smoke  # noqa: E402


def _mock_response(status, body_dict):
    import json as _json
    mock_resp = MagicMock()
    mock_resp.status = status
    mock_resp.read.return_value = _json.dumps(body_dict).encode()
    mock_resp.__enter__ = lambda self: mock_resp
    mock_resp.__exit__ = lambda self, *a: None
    return mock_resp


class TestRunChecks:
    def test_all_healthy_endpoints_produce_no_failures(self):
        with patch("staging_smoke_test.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = _mock_response(200, {"status": "ok"})
            failures = smoke.run_checks("http://fake", "test-key")
        assert failures == []

    def test_http_500_is_a_failure(self):
        import io

        def _side_effect(req, timeout=None):
            raise urllib.error.HTTPError(req.full_url, 500, "Internal Server Error", {}, io.BytesIO(b'{"detail": "boom"}'))

        with patch("staging_smoke_test.urllib.request.urlopen", side_effect=_side_effect):
            failures = smoke.run_checks("http://fake", "test-key")
        assert len(failures) == len(smoke.CHECKS)
        assert all("HTTP 500" in f for f in failures)

    def test_connection_refused_is_a_failure(self):
        with patch("staging_smoke_test.urllib.request.urlopen", side_effect=OSError("Connection refused")):
            failures = smoke.run_checks("http://fake", "test-key")
        assert len(failures) == len(smoke.CHECKS)
        assert all("request failed" in f for f in failures)

    def test_non_200_status_is_a_failure(self):
        with patch("staging_smoke_test.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = _mock_response(503, {"status": "ok"})
            failures = smoke.run_checks("http://fake", "test-key")
        assert len(failures) == len(smoke.CHECKS)
        assert all("expected HTTP 200, got 503" in f for f in failures)

    def test_error_envelope_with_200_is_a_failure(self):
        """Real dry-run finding: /health can return HTTP 200 with its own
        {"status": "error", "db": "error", ...} summary when a subsystem
        (e.g. the DB) is genuinely broken — this must count as a failure,
        not a pass, even though the HTTP layer succeeded."""
        with patch("staging_smoke_test.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = _mock_response(200, {"status": "error", "db": "error"})
            failures = smoke.run_checks("http://fake", "test-key")
        assert len(failures) == len(smoke.CHECKS)
        assert all("status=error" in f for f in failures)

    def test_invalid_json_is_a_failure(self):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b"not json"
        mock_resp.__enter__ = lambda self: mock_resp
        mock_resp.__exit__ = lambda self, *a: None
        with patch("staging_smoke_test.urllib.request.urlopen", return_value=mock_resp):
            failures = smoke.run_checks("http://fake", "test-key")
        assert len(failures) == len(smoke.CHECKS)
        assert all("not valid JSON" in f for f in failures)

    def test_unauthenticated_check_does_not_send_api_key_header(self):
        """/health requires no auth (requires_auth: False) — confirms the
        request is built without an X-API-Key header for that check."""
        captured_requests = []

        def _capture(req, timeout=None):
            captured_requests.append(req)
            return _mock_response(200, {"status": "ok"})

        with patch("staging_smoke_test.urllib.request.urlopen", side_effect=_capture):
            smoke.run_checks("http://fake", "test-key")

        health_reqs = [r for r in captured_requests if r.full_url.endswith("/health")]
        assert len(health_reqs) == 1
        assert "X-api-key" not in health_reqs[0].headers  # urllib title-cases header keys

    def test_authenticated_checks_send_api_key_header(self):
        captured_requests = []

        def _capture(req, timeout=None):
            captured_requests.append(req)
            return _mock_response(200, {"status": "ok"})

        with patch("staging_smoke_test.urllib.request.urlopen", side_effect=_capture):
            smoke.run_checks("http://fake", "test-key-123")

        positions_reqs = [r for r in captured_requests if r.full_url.endswith("/positions")]
        assert len(positions_reqs) == 1
        assert positions_reqs[0].headers.get("X-api-key") == "test-key-123"


class TestMain:
    def test_missing_staging_api_url_env_var_fails(self, monkeypatch):
        monkeypatch.delenv("STAGING_API_URL", raising=False)
        assert smoke.main() == 1

    def test_all_checks_pass_returns_zero(self, monkeypatch):
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        with patch("staging_smoke_test._wake_up", return_value=True):
            with patch("staging_smoke_test.run_checks", return_value=[]):
                assert smoke.main() == 0

    def test_any_check_failure_returns_one(self, monkeypatch):
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        with patch("staging_smoke_test._wake_up", return_value=True):
            with patch("staging_smoke_test.run_checks", return_value=["GET /positions: HTTP 500"]):
                assert smoke.main() == 1

    def test_wake_up_failure_does_not_itself_fail_the_run(self, monkeypatch):
        """A failed wake-up ping is a warning, not a hard failure — the
        real checks (with their own timeout/retry-equivalent handling)
        still run and determine the outcome."""
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        with patch("staging_smoke_test._wake_up", return_value=False):
            with patch("staging_smoke_test.run_checks", return_value=[]):
                assert smoke.main() == 0
