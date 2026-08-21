"""
Regression tests for scripts/wait_for_staging_deploy_live.py (ST-13,
BLG-OPS-25, EPIC-03, v9.0).

This module exists specifically because an earlier version of
staging-deploy.yml used a fixed `sleep 120` instead of an actual deploy-
status poll, based on an incorrect assumption that no Render platform API
access existed in this repo — caught by agent-mediated Infrastructure &
Operations Owner review, which found scripts/check_staging_deploy_drift.py
already provides exactly this capability. These tests cover the polling
logic in isolation (mocked, no live Render API calls).
"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import wait_for_staging_deploy_live as waiter  # noqa: E402


class TestWaitForLive:
    def test_returns_true_immediately_when_already_live(self):
        with patch("wait_for_staging_deploy_live.get_latest_live_commit", return_value=("target-sha", "2026-08-21T00:00:00Z")):
            with patch("wait_for_staging_deploy_live.time.sleep"):
                result = waiter.wait_for_live("target-sha", "fake-api-key", timeout_s=60, poll_interval_s=1)
        assert result is True

    def test_polls_until_target_sha_appears(self):
        responses = iter([
            ("old-sha", "2026-08-21T00:00:00Z"),
            ("old-sha", "2026-08-21T00:00:00Z"),
            ("target-sha", "2026-08-21T00:05:00Z"),
        ])
        with patch("wait_for_staging_deploy_live.get_latest_live_commit", side_effect=lambda *a: next(responses)):
            with patch("wait_for_staging_deploy_live.time.sleep") as mock_sleep:
                result = waiter.wait_for_live("target-sha", "fake-api-key", timeout_s=60, poll_interval_s=1)
        assert result is True
        assert mock_sleep.call_count == 2  # slept between the 2 non-matching polls

    def test_times_out_returns_false_not_true(self):
        """A timeout must be a hard failure (False), never silently treated
        as success — see module docstring on why this differs from a
        soft warn-and-proceed design."""
        with patch("wait_for_staging_deploy_live.get_latest_live_commit", return_value=("stale-sha", "2026-08-21T00:00:00Z")):
            with patch("wait_for_staging_deploy_live.time.sleep"):
                # timeout_s smaller than poll_interval_s -> loop body runs at
                # most once before the deadline check fails it out.
                result = waiter.wait_for_live("target-sha", "fake-api-key", timeout_s=0, poll_interval_s=1)
        assert result is False

    def test_transient_api_error_is_retried_not_fatal(self):
        """A single Render API hiccup must not abort the whole wait --
        only a full timeout should give up."""
        call_count = {"n": 0}

        def _side_effect(*a):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise RuntimeError("Render API error for service srv-xxx: HTTP 503")
            return ("target-sha", "2026-08-21T00:00:00Z")

        with patch("wait_for_staging_deploy_live.get_latest_live_commit", side_effect=_side_effect):
            with patch("wait_for_staging_deploy_live.time.sleep"):
                result = waiter.wait_for_live("target-sha", "fake-api-key", timeout_s=60, poll_interval_s=1)
        assert result is True
        assert call_count["n"] == 2


class TestMain:
    def test_missing_target_sha_arg_returns_usage_error(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["wait_for_staging_deploy_live.py"])
        assert waiter.main() == 2

    def test_success_path_returns_zero(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["wait_for_staging_deploy_live.py", "target-sha"])
        monkeypatch.setenv("RENDER_PLATFORM_API_KEY", "fake-key")
        with patch("wait_for_staging_deploy_live.wait_for_live", return_value=True):
            assert waiter.main() == 0

    def test_timeout_path_returns_one(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["wait_for_staging_deploy_live.py", "target-sha"])
        monkeypatch.setenv("RENDER_PLATFORM_API_KEY", "fake-key")
        with patch("wait_for_staging_deploy_live.wait_for_live", return_value=False):
            assert waiter.main() == 1
