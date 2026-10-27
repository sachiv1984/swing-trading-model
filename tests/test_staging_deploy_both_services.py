"""
ST-29 (BLG-OPS-189, EPIC-05, v9.13) — staging-deploy.yml deploys both
staging services and waits on each.

- AC 1: the workflow calls RENDER_STAGING_BACKEND_DEPLOY_HOOK and
  RENDER_STAGING_FRONTEND_DEPLOY_HOOK (RENDER_STAGING_DEPLOY_HOOK retired),
  and a hook's deploy ID must belong to the expected service.
- AC 3: a test fails if the workflow calls only one hook or waits on a
  service it did not deploy (check_workflow_wiring, run here against the
  real workflow and against broken variants of it).
- AC 4 (automated half): the smoke test fails when the host behind
  STAGING_API_URL is not srv-d6rtdg94tr6s73ce2j6g.

AC 2 (a live run on main with both services on the run's commit) is
staging-only.
"""
import json
import sys
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import staging_smoke_test as smoke  # noqa: E402
import trigger_staging_deploy as trig  # noqa: E402
import wait_for_staging_deploy_live as waiter  # noqa: E402

BACKEND = "trading-assistant-api-staging"
FRONTEND = "trading-assistant-staging"
BACKEND_ID = "srv-d6rtdg94tr6s73ce2j6g"
FRONTEND_ID = "srv-d6rtdg94tr6s73ce2j60"


def _workflow():
    return yaml.safe_load(trig.WORKFLOW.read_text())


def _steps(wf):
    return wf["jobs"]["deploy-staging"]["steps"]


def _resp(status, body):
    r = MagicMock()
    r.status = status
    r.read.return_value = json.dumps(body).encode() if not isinstance(body, bytes) else body
    r.__enter__ = lambda self: r
    r.__exit__ = lambda self, *a: False
    return r


def _http_error(code):
    return HTTPError("https://api.render.com", code, "err", {}, BytesIO(b""))


class TestWorkflowWiring:
    def test_real_workflow_deploys_and_waits_on_both_services(self):
        assert trig.check_workflow_wiring(_workflow()) == []

    def test_retired_single_hook_secret_is_gone(self):
        assert "secrets.RENDER_STAGING_DEPLOY_HOOK" not in trig.WORKFLOW.read_text()

    def test_fails_when_only_the_backend_hook_is_called(self):
        wf = _workflow()
        steps = _steps(wf)
        steps[:] = [s for s in steps if s.get("id") != "frontend_hook"]
        errors = trig.check_workflow_wiring(wf)
        assert any(f"no step calls {FRONTEND}'s deploy hook" in e for e in errors)
        assert any(f"waits on {FRONTEND}, which this workflow does not deploy" in e for e in errors)

    def test_fails_when_only_the_frontend_hook_is_called(self):
        wf = _workflow()
        steps = _steps(wf)
        steps[:] = [s for s in steps if s.get("id") != "backend_hook"]
        errors = trig.check_workflow_wiring(wf)
        assert any(f"no step calls {BACKEND}'s deploy hook" in e for e in errors)
        assert any(f"waits on {BACKEND}, which this workflow does not deploy" in e for e in errors)

    def test_fails_when_the_old_single_hook_shape_returns(self):
        """The pre-v9.13 shape: one curl to RENDER_STAGING_DEPLOY_HOOK, one
        wait on the (default) backend."""
        wf = {"jobs": {"deploy-staging": {"steps": [
            {"name": "Trigger Render deploy hook",
             "run": 'curl -X POST "$RENDER_STAGING_DEPLOY_HOOK"',
             "env": {"RENDER_STAGING_DEPLOY_HOOK": "${{ secrets.RENDER_STAGING_DEPLOY_HOOK }}"}},
            {"name": "Wait", "run": 'python3 scripts/wait_for_staging_deploy_live.py "$GITHUB_SHA"'},
        ]}}}
        errors = trig.check_workflow_wiring(wf)
        assert any("retired RENDER_STAGING_DEPLOY_HOOK" in e for e in errors)
        assert any(f"waits on {BACKEND}, which this workflow does not deploy" in e for e in errors)

    def test_fails_when_a_wait_step_is_missing(self):
        wf = _workflow()
        steps = _steps(wf)
        steps[:] = [s for s in steps if not ("wait_for_staging_deploy_live" in (s.get("run") or "")
                                             and FRONTEND in s["run"])]
        assert any(f"no step waits on {FRONTEND}" in e for e in trig.check_workflow_wiring(wf))

    def test_fails_when_a_hook_reads_the_other_services_secret(self):
        wf = _workflow()
        step = next(s for s in _steps(wf) if s.get("id") == "frontend_hook")
        step["env"] = {"RENDER_STAGING_BACKEND_DEPLOY_HOOK": "${{ secrets.RENDER_STAGING_BACKEND_DEPLOY_HOOK }}"}
        errors = trig.check_workflow_wiring(wf)
        assert any("RENDER_STAGING_FRONTEND_DEPLOY_HOOK" in e for e in errors)

    def test_each_wait_follows_its_own_hooks_deploy_id(self):
        runs = {s.get("name"): s.get("run") for s in _steps(_workflow())}
        assert "steps.backend_hook.outputs.deploy_id" in runs["Wait for staging backend deploy to go live"]
        assert "steps.frontend_hook.outputs.deploy_id" in runs["Wait for staging frontend deploy to go live"]


class TestTrigger:
    HOOK = "https://api.render.com/deploy/srv-d6rtdg94tr6s73ce2j6g?key=abc"

    def test_hook_is_called_with_the_commit_as_ref(self):
        url = trig.hook_url_with_ref(self.HOOK, "deadbeef")
        assert url.startswith("https://api.render.com/deploy/srv-d6rtdg94tr6s73ce2j6g?")
        assert "key=abc" in url and "ref=deadbeef" in url

    @pytest.mark.parametrize("body,expected", [
        ({"deploy": {"id": "dep-1"}}, "dep-1"),
        ({"id": "dep-2"}, "dep-2"),
        ({}, ""),
        (b"not json", ""),
    ])
    def test_parse_deploy_id(self, body, expected):
        raw = json.dumps(body).encode() if isinstance(body, dict) else body
        assert trig.parse_deploy_id(raw) == expected

    def test_deploy_on_the_expected_service_passes(self):
        calls = []

        def fake_urlopen(req, timeout=None):
            calls.append(req.full_url)
            if "/deploy/" in req.full_url:
                return _resp(200, {"deploy": {"id": "dep-ok"}})
            return _resp(200, {"id": "dep-ok"})

        with patch("trigger_staging_deploy.urlopen", side_effect=fake_urlopen):
            assert trig.trigger(BACKEND, "sha1", self.HOOK, "k") == "dep-ok"
        assert calls[1] == f"https://api.render.com/v1/services/{BACKEND_ID}/deploys/dep-ok"

    def test_mis_pasted_hook_fails_loudly(self):
        """The frontend secret holds the backend's hook: the returned deploy
        is not found under the frontend service."""
        def fake_urlopen(req, timeout=None):
            if "/deploy/" in req.full_url:
                return _resp(200, {"deploy": {"id": "dep-backend"}})
            raise _http_error(404)

        with patch("trigger_staging_deploy.urlopen", side_effect=fake_urlopen):
            with pytest.raises(RuntimeError, match="RENDER_STAGING_FRONTEND_DEPLOY_HOOK holds another service's hook"):
                trig.trigger(FRONTEND, "sha1", self.HOOK, "k")

    def test_hook_http_error_fails(self):
        with patch("trigger_staging_deploy.urlopen", side_effect=_http_error(401)):
            with pytest.raises(RuntimeError, match="HTTP 401"):
                trig.trigger(BACKEND, "sha1", self.HOOK, "k")

    def test_missing_hook_secret_fails(self, monkeypatch, capsys):
        monkeypatch.delenv("RENDER_STAGING_FRONTEND_DEPLOY_HOOK", raising=False)
        monkeypatch.setattr(sys, "argv", ["trigger_staging_deploy.py", FRONTEND, "sha1"])
        assert trig.main() == 1
        assert "RENDER_STAGING_FRONTEND_DEPLOY_HOOK is not set" in capsys.readouterr().out

    def test_main_writes_deploy_id_output(self, monkeypatch, tmp_path):
        out = tmp_path / "out"
        monkeypatch.setenv("RENDER_STAGING_BACKEND_DEPLOY_HOOK", self.HOOK)
        monkeypatch.setenv("RENDER_PLATFORM_API_KEY", "k")
        monkeypatch.setenv("GITHUB_OUTPUT", str(out))
        monkeypatch.setattr(sys, "argv", ["trigger_staging_deploy.py", BACKEND, "sha1"])
        with patch("trigger_staging_deploy.trigger", return_value="dep-9"):
            assert trig.main() == 0
        assert out.read_text() == "deploy_id=dep-9\n"


class TestWaitForDeploy:
    def _run(self, statuses):
        it = iter(statuses)
        with patch("wait_for_staging_deploy_live.get_deploy", side_effect=lambda *a: next(it)), \
             patch("wait_for_staging_deploy_live.time.sleep"):
            return waiter.wait_for_deploy("sha1", "k", FRONTEND_ID, "dep-1", timeout_s=60, poll_interval_s=1)

    def test_live_on_target_commit(self):
        assert self._run([("build_in_progress", "sha1"), ("live", "sha1")]) is True

    def test_failed_build_stops_at_once(self):
        assert self._run([("build_in_progress", "sha1"), ("build_failed", "sha1")]) is False

    def test_live_on_another_commit_fails(self):
        assert self._run([("live", "other")]) is False

    def test_main_waits_on_the_named_service_and_deploy(self, monkeypatch):
        monkeypatch.setenv("RENDER_PLATFORM_API_KEY", "k")
        monkeypatch.setattr(sys, "argv", ["w", "sha1", "--service", FRONTEND, "--deploy-id", "dep-7"])
        with patch("wait_for_staging_deploy_live.wait_for_deploy", return_value=True) as w:
            assert waiter.main() == 0
        w.assert_called_once_with("sha1", "k", FRONTEND_ID, "dep-7")

    def test_main_rejects_an_unknown_service(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["w", "sha1", "--service", "prod-api"])
        assert waiter.main() == 2


class TestSmokeHostCheck:
    def _check(self, body, status=200):
        with patch("staging_smoke_test._request", return_value=(status, json.dumps(body).encode())):
            return smoke.check_host_is_staging_backend("http://staging", "k")

    def test_staging_backend_passes(self):
        assert self._check({"render_service_id": BACKEND_ID}) == ""

    def test_other_host_fails_loudly(self):
        result = self._check({"render_service_id": "srv-somewhere-else"})
        assert result.startswith("WRONG STAGING HOST") and BACKEND_ID in result

    def test_frontend_service_fails(self):
        assert self._check({"render_service_id": FRONTEND_ID}).startswith("WRONG STAGING HOST")

    def test_missing_field_is_a_known_limit_warning(self):
        assert self._check({"deployed_commit_sha": "abc"}).startswith("known limit:")

    def test_main_fails_on_wrong_host(self, monkeypatch):
        monkeypatch.setenv("STAGING_API_URL", "http://staging")
        monkeypatch.delenv("EXPECTED_COMMIT_SHA", raising=False)
        with patch("staging_smoke_test._wake_up", return_value=True), \
             patch("staging_smoke_test.run_checks", return_value=[]), \
             patch("staging_smoke_test.check_host_is_staging_backend", return_value="WRONG STAGING HOST: x"):
            assert smoke.main() == 1

    def test_health_detailed_reports_render_service_id(self, monkeypatch):
        sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
        from services.health_service import get_render_service_id
        monkeypatch.setenv("RENDER_SERVICE_ID", BACKEND_ID)
        assert get_render_service_id() == BACKEND_ID
        monkeypatch.delenv("RENDER_SERVICE_ID")
        assert get_render_service_id() is None
