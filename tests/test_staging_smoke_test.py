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
        monkeypatch.delenv("EXPECTED_COMMIT_SHA", raising=False)
        with patch("staging_smoke_test._wake_up", return_value=True):
            with patch("staging_smoke_test.run_checks", return_value=[]):
                assert smoke.main() == 0

    def test_any_check_failure_returns_one(self, monkeypatch):
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        monkeypatch.delenv("EXPECTED_COMMIT_SHA", raising=False)
        with patch("staging_smoke_test._wake_up", return_value=True):
            with patch("staging_smoke_test.run_checks", return_value=["GET /positions: HTTP 500"]):
                assert smoke.main() == 1

    def test_wake_up_failure_does_not_itself_fail_the_run(self, monkeypatch):
        """A failed wake-up ping is a warning, not a hard failure — the
        real checks (with their own timeout/retry-equivalent handling)
        still run and determine the outcome."""
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        monkeypatch.delenv("EXPECTED_COMMIT_SHA", raising=False)
        with patch("staging_smoke_test._wake_up", return_value=False):
            with patch("staging_smoke_test.run_checks", return_value=[]):
                assert smoke.main() == 0

    def test_expected_commit_sha_unset_skips_deploy_check_entirely(self, monkeypatch):
        """No EXPECTED_COMMIT_SHA (e.g. a manual workflow_dispatch run with no
        commit context) -- the stale-deploy check must not run at all, and
        must not affect the exit code."""
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        monkeypatch.delenv("EXPECTED_COMMIT_SHA", raising=False)
        with patch("staging_smoke_test._wake_up", return_value=True):
            with patch("staging_smoke_test.run_checks", return_value=[]):
                with patch("staging_smoke_test.check_deployed_commit") as mock_check:
                    assert smoke.main() == 0
        mock_check.assert_not_called()

    def test_expected_commit_sha_set_and_matching_returns_zero(self, monkeypatch):
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        monkeypatch.setenv("EXPECTED_COMMIT_SHA", "abc123")
        with patch("staging_smoke_test._wake_up", return_value=True):
            with patch("staging_smoke_test.run_checks", return_value=[]):
                with patch("staging_smoke_test.check_deployed_commit", return_value="") as mock_check:
                    assert smoke.main() == 0
        mock_check.assert_called_once_with("http://fake", "test-key", "abc123")

    def test_stale_deploy_fails_the_run_even_when_smoke_checks_pass(self, monkeypatch):
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        monkeypatch.setenv("EXPECTED_COMMIT_SHA", "abc123")
        with patch("staging_smoke_test._wake_up", return_value=True):
            with patch("staging_smoke_test.run_checks", return_value=[]):
                with patch(
                    "staging_smoke_test.check_deployed_commit",
                    return_value="STALE STAGING DEPLOY: staging is running commit 'def456' but the latest merged commit on main is 'abc123'",
                ):
                    assert smoke.main() == 1

    def test_known_limit_message_does_not_fail_the_run(self, monkeypatch):
        """A missing deployed_commit_sha (e.g. an older staging deploy predating
        this field) is a documented known limit, not a stale-deploy failure."""
        monkeypatch.setenv("STAGING_API_URL", "http://fake")
        monkeypatch.setenv("STAGING_API_KEY", "test-key")
        monkeypatch.setenv("EXPECTED_COMMIT_SHA", "abc123")
        with patch("staging_smoke_test._wake_up", return_value=True):
            with patch("staging_smoke_test.run_checks", return_value=[]):
                with patch(
                    "staging_smoke_test.check_deployed_commit",
                    return_value="known limit: GET /health/detailed did not report a deployed_commit_sha",
                ):
                    assert smoke.main() == 0


class TestCheckDeployedCommit:
    def test_matching_commit_returns_empty_string(self):
        with patch("staging_smoke_test.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = _mock_response(200, {"deployed_commit_sha": "abc123"})
            result = smoke.check_deployed_commit("http://fake", "test-key", "abc123")
        assert result == ""

    def test_mismatched_commit_is_flagged_as_stale(self):
        with patch("staging_smoke_test.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = _mock_response(200, {"deployed_commit_sha": "old-sha"})
            result = smoke.check_deployed_commit("http://fake", "test-key", "new-sha")
        assert "STALE STAGING DEPLOY" in result
        assert "old-sha" in result
        assert "new-sha" in result

    def test_null_deployed_commit_sha_is_a_known_limit_not_a_failure(self):
        with patch("staging_smoke_test.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = _mock_response(200, {"deployed_commit_sha": None})
            result = smoke.check_deployed_commit("http://fake", "test-key", "abc123")
        assert result.startswith("known limit:")

    def test_missing_deployed_commit_sha_key_is_a_known_limit_not_a_failure(self):
        """Older staging deploy predating this field -- key absent entirely."""
        with patch("staging_smoke_test.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = _mock_response(200, {"status": "healthy"})
            result = smoke.check_deployed_commit("http://fake", "test-key", "abc123")
        assert result.startswith("known limit:")

    def test_request_failure_is_reported_not_raised(self):
        with patch("staging_smoke_test.urllib.request.urlopen", side_effect=OSError("Connection refused")):
            result = smoke.check_deployed_commit("http://fake", "test-key", "abc123")
        assert "could not check deployed commit" in result

    def test_non_200_status_is_reported(self):
        with patch("staging_smoke_test.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = _mock_response(503, {})
            result = smoke.check_deployed_commit("http://fake", "test-key", "abc123")
        assert "503" in result

    def test_invalid_json_is_reported(self):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = b"not json"
        mock_resp.__enter__ = lambda self: mock_resp
        mock_resp.__exit__ = lambda self, *a: None
        with patch("staging_smoke_test.urllib.request.urlopen", return_value=mock_resp):
            result = smoke.check_deployed_commit("http://fake", "test-key", "abc123")
        assert "not valid JSON" in result
