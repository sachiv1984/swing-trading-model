"""
ST-15 (BLG-QA-191, EPIC-03, v9.9): I/O-boundary coverage for
scripts/check_nightly_stop_update_staleness.py and
scripts/generate_ci_usage_report.py.

test_nightly_stop_update_staleness.py / test_ci_usage_report.py already cover
both scripts' pure logic. This file covers the functions that talk to the
outside world -- get_scheduler_health() (requests.get), _gh_api() /
_gh_api_paginated() (subprocess.run against the `gh` CLI), the fetch_*
wrappers built on them, and check_nightly_stop_update_staleness.main()'s
GET /health/scheduler response-shape parsing. Every external call is mocked:
no live network or `gh` CLI dependency.
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import check_nightly_stop_update_staleness as staleness  # noqa: E402
import generate_ci_usage_report as ci_usage  # noqa: E402


# ---------------------------------------------------------------------------
# generate_ci_usage_report.py -- gh CLI boundary
# ---------------------------------------------------------------------------

def _completed(payload):
    return subprocess.CompletedProcess(args=[], returncode=0, stdout=json.dumps(payload), stderr="")


def _page_param(cmd):
    """Extract the `page=N` value from a captured `gh api` argv."""
    for i, arg in enumerate(cmd):
        if arg == "-f" and cmd[i + 1].startswith("page="):
            return int(cmd[i + 1].split("=", 1)[1])
    return None


def test_gh_api_forces_get_and_parses_stdout_json():
    with patch.object(ci_usage.subprocess, "run", return_value=_completed({"ok": 1})) as run:
        assert ci_usage._gh_api("repos/x/y", ["-f", "per_page=5"]) == {"ok": 1}
    cmd = run.call_args.args[0]
    # --method GET must be present: a parameterised `gh api` call defaults to POST otherwise.
    assert cmd[:5] == ["gh", "api", "repos/x/y", "--method", "GET"]
    assert cmd[5:] == ["-f", "per_page=5"]
    assert run.call_args.kwargs["check"] is True


def test_gh_api_propagates_cli_failure():
    err = subprocess.CalledProcessError(1, ["gh"], stderr="HTTP 404")
    with patch.object(ci_usage.subprocess, "run", side_effect=err):
        with pytest.raises(subprocess.CalledProcessError):
            ci_usage._gh_api("repos/x/missing")


def test_gh_api_paginated_walks_every_page_until_short_page():
    pages = {
        1: {"workflows": [{"id": i} for i in range(3)]},
        2: {"workflows": [{"id": i} for i in range(3, 6)]},
        3: {"workflows": [{"id": 6}]},  # short page -> stop
    }
    calls = []

    def fake_run(cmd, **_):
        page = _page_param(cmd)
        calls.append(page)
        return _completed(pages[page])

    with patch.object(ci_usage.subprocess, "run", side_effect=fake_run):
        items = ci_usage._gh_api_paginated("repos/x/actions/workflows", "workflows", per_page=3)

    assert [w["id"] for w in items] == list(range(7))
    assert calls == [1, 2, 3]


def test_gh_api_paginated_full_last_page_needs_one_empty_page_to_stop():
    pages = {1: {"artifacts": [{"n": 1}, {"n": 2}]}, 2: {"artifacts": []}}
    with patch.object(ci_usage.subprocess, "run", side_effect=lambda cmd, **_: _completed(pages[_page_param(cmd)])):
        assert ci_usage._gh_api_paginated("p", "artifacts", per_page=2) == [{"n": 1}, {"n": 2}]


def test_gh_api_paginated_missing_list_key_is_treated_as_empty():
    with patch.object(ci_usage.subprocess, "run", return_value=_completed({"message": "no key"})) as run:
        assert ci_usage._gh_api_paginated("p", "workflows") == []
    assert run.call_count == 1


def test_gh_api_paginated_forwards_extra_args_on_every_page():
    pages = {1: {"x": [1, 2]}, 2: {"x": [3]}}
    seen = []

    def fake_run(cmd, **_):
        seen.append(cmd)
        return _completed(pages[_page_param(cmd)])

    with patch.object(ci_usage.subprocess, "run", side_effect=fake_run):
        ci_usage._gh_api_paginated("p", "x", extra_args=["-f", "status=completed"], per_page=2)
    assert all("status=completed" in cmd for cmd in seen)
    assert all("per_page=2" in cmd for cmd in seen)


def test_fetch_workflows_projects_id_and_name():
    raw = [{"id": 1, "name": "CI", "path": ".github/workflows/ci.yml"}, {"id": 2, "name": "Deploy", "state": "active"}]
    with patch.object(ci_usage, "_gh_api_paginated", return_value=raw) as paginated:
        assert ci_usage.fetch_workflows() == [{"id": 1, "name": "CI"}, {"id": 2, "name": "Deploy"}]
    assert paginated.call_args.args[1] == "workflows"


def test_fetch_workflow_run_count_and_sample_parses_total_and_ids():
    data = {"total_count": 42, "workflow_runs": [{"id": 9}, {"id": 8}]}
    with patch.object(ci_usage, "_gh_api", return_value=data) as api:
        assert ci_usage.fetch_workflow_run_count_and_sample(7, "2026-08-01", "2026-08-31", sample_size=2) == (42, [9, 8])
    path, args = api.call_args.args
    assert path.endswith("/actions/workflows/7/runs")
    assert "created=2026-08-01..2026-08-31" in args
    assert "per_page=2" in args


def test_fetch_workflow_run_count_and_sample_defaults_on_empty_response():
    with patch.object(ci_usage, "_gh_api", return_value={}):
        assert ci_usage.fetch_workflow_run_count_and_sample(7, "a", "b") == (0, [])


def test_fetch_run_duration_ms_reads_run_duration_and_defaults_to_zero():
    with patch.object(ci_usage, "_gh_api", return_value={"run_duration_ms": 1234, "billable": {}}) as api:
        assert ci_usage.fetch_run_duration_ms(55) == 1234
    assert api.call_args.args[0].endswith("/actions/runs/55/timing")
    with patch.object(ci_usage, "_gh_api", return_value={"billable": {}}):
        assert ci_usage.fetch_run_duration_ms(55) == 0


def test_fetch_artifacts_in_window_filters_on_inclusive_utc_bounds():
    raw = [
        {"name": "before", "size_in_bytes": 1, "created_at": "2026-07-31T23:59:59Z"},
        {"name": "first-instant", "size_in_bytes": 2, "created_at": "2026-08-01T00:00:00Z"},
        {"name": "last-second", "size_in_bytes": 3, "created_at": "2026-08-31T23:59:59Z"},
        {"name": "after", "size_in_bytes": 4, "created_at": "2026-09-01T00:00:00Z"},
        {"name": "no-size", "created_at": "2026-08-15T12:00:00Z"},
    ]
    with patch.object(ci_usage, "_gh_api_paginated", return_value=raw):
        got = ci_usage.fetch_artifacts_in_window("2026-08-01", "2026-08-31")
    assert got == [
        {"name": "first-instant", "size_in_bytes": 2},
        {"name": "last-second", "size_in_bytes": 3},
        {"name": "no-size", "size_in_bytes": 0},
    ]


def test_fetch_artifacts_in_window_uses_paginated_helper_across_pages():
    """End-to-end through the real _gh_api_paginated: artifacts on page 2 are
    not dropped (regression guard for the pagination loop)."""
    pages = {
        1: {"artifacts": [{"name": f"a{i}", "size_in_bytes": i, "created_at": "2026-08-10T00:00:00Z"} for i in range(100)]},
        2: {"artifacts": [{"name": "page2", "size_in_bytes": 7, "created_at": "2026-08-20T00:00:00Z"}]},
    }
    with patch.object(ci_usage.subprocess, "run", side_effect=lambda cmd, **_: _completed(pages[_page_param(cmd)])):
        got = ci_usage.fetch_artifacts_in_window("2026-08-01", "2026-08-31")
    assert len(got) == 101
    assert got[-1] == {"name": "page2", "size_in_bytes": 7}


# ---------------------------------------------------------------------------
# check_nightly_stop_update_staleness.py -- HTTP boundary
# ---------------------------------------------------------------------------

def test_get_scheduler_health_calls_read_only_endpoint_with_api_key():
    resp = MagicMock()
    resp.json.return_value = {"jobs": {}}
    with patch.object(staleness.requests, "get", return_value=resp) as get:
        assert staleness.get_scheduler_health("https://api.example/", "k3y", timeout=5) == {"jobs": {}}
    get.assert_called_once_with("https://api.example/health/scheduler", headers={"X-API-Key": "k3y"}, timeout=5)
    resp.raise_for_status.assert_called_once()


def test_get_scheduler_health_raises_on_http_error():
    resp = MagicMock()
    resp.raise_for_status.side_effect = staleness.requests.HTTPError("503")
    with patch.object(staleness.requests, "get", return_value=resp):
        with pytest.raises(staleness.requests.HTTPError):
            staleness.get_scheduler_health("https://api.example", "k")


def _run_main(health, monkeypatch, capsys):
    monkeypatch.setenv("API_URL", "https://api.example")
    monkeypatch.setenv("API_KEY", "k")
    monkeypatch.setattr(sys, "argv", ["check_nightly_stop_update_staleness.py"])
    with patch.object(staleness, "get_scheduler_health", return_value=health):
        with pytest.raises(SystemExit) as exc:
            staleness.main()
    return exc.value.code, capsys.readouterr().out


def test_main_parses_recent_ok_run_as_not_overdue(monkeypatch, capsys):
    recent = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    code, out = _run_main({"jobs": {"trailing_stop": {"last_run_utc": recent, "last_status": "ok"}}}, monkeypatch, capsys)
    assert code == 0
    assert out.startswith("[OK]")


def test_main_parses_stale_run_as_overdue(monkeypatch, capsys):
    stale = (datetime.now(timezone.utc) - timedelta(hours=30)).isoformat()
    code, out = _run_main({"jobs": {"trailing_stop": {"last_run_utc": stale, "last_status": "ok"}}}, monkeypatch, capsys)
    assert code == 1
    assert out.startswith("[OVERDUE]")


@pytest.mark.parametrize("health", [{}, {"jobs": {}}, {"jobs": {"trailing_stop": {}}}])
def test_main_treats_missing_job_fields_as_never_run(health, monkeypatch, capsys):
    code, out = _run_main(health, monkeypatch, capsys)
    assert code == 1
    assert "no trailing_stop run has been recorded" in out


def test_main_requires_api_url_and_key(monkeypatch):
    monkeypatch.delenv("API_URL", raising=False)
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.setattr(sys, "argv", ["check_nightly_stop_update_staleness.py"])
    with patch.object(staleness, "get_scheduler_health") as fetch:
        with pytest.raises(SystemExit, match="API_URL and API_KEY must be set"):
            staleness.main()
    fetch.assert_not_called()
