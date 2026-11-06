"""
ST-31 (EPIC-05, v9.15, BLG-OPS-191; Product Owner ruling ESC-EXEC-20261105-05):
governance-only and docs-only pushes skip the five code-test suites, except
that CI Pytest Phase A runs the docs-coupled tests.

Covers the classifier (scripts/ci_code_changes.py), the docs-coupled selector
(tests/docs_coupled.py) and the wiring of the five workflows. The live check,
a governance-only PR on main reporting every required check without running
the suites, is post-merge (BLG-OPS-211).
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
WORKFLOWS = ROOT / ".github" / "workflows"

_spec = importlib.util.spec_from_file_location("ci_code_changes", ROOT / "scripts" / "ci_code_changes.py")
ci_code_changes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ci_code_changes)

from tests.docs_coupled import is_docs_coupled  # noqa: E402

# Workflow file -> the suite job(s) that skip on a governance-only change.
SUITES = {
    "ci-tests.yml": ["pytest-phase-b"],
    "smoke-tests.yml": ["smoke"],
    "service-coverage.yml": ["service-coverage"],
    "golden-outputs.yml": ["golden-outputs"],
    "integration-tests.yml": ["portfolio-integration"],
}


# --- classifier -------------------------------------------------------------

@pytest.mark.parametrize("paths", [
    ["claude/backlog/backlog.md"],
    ["claude/cycles/x/execution_state.json", "docs/specs/data_model.md"],
    ["docs/ops/runbook.md", "", "  "],
])
def test_governance_or_docs_only_changes_skip_the_suites(paths):
    assert ci_code_changes.needs_code_suites(paths) is False


@pytest.mark.parametrize("paths", [
    ["backend/main.py"],
    ["docs/specs/data_model.md", "backend/database.py"],
    ["claude/system/execution_prompt.md", ".github/workflows/ci-tests.yml"],
    ["tests/conftest.py"],
    ["CLAUDE.md"],              # repo-root file, not under claude/
    ["claudefile.txt"],         # prefix match is on the directory, not the word
    ["src/pages/Positions.js"],
])
def test_any_path_outside_claude_and_docs_runs_the_suites(paths):
    assert ci_code_changes.needs_code_suites(paths) is True


def test_an_empty_file_list_fails_safe_and_runs_the_suites():
    assert ci_code_changes.needs_code_suites([]) is True


def test_script_prints_true_or_false_from_stdin():
    script = str(ROOT / "scripts" / "ci_code_changes.py")
    run = lambda text: subprocess.run([sys.executable, script], input=text, capture_output=True, text=True).stdout.strip()
    assert run("claude/a.md\ndocs/b.md\n") == "false"
    assert run("claude/a.md\nbackend/c.py\n") == "true"
    assert run("") == "true"


# --- workflow wiring ----------------------------------------------------------

def _load(name):
    return yaml.safe_load((WORKFLOWS / name).read_text())


@pytest.mark.parametrize("name", sorted(SUITES))
def test_workflow_still_triggers_on_every_push_and_pr(name):
    """No workflow-level path filter: a filtered-out workflow never reports its
    checks, which leaves a required check pending (backlog_archive.md:2167)."""
    on = _load(name).get(True) or _load(name).get("on")
    for event in ("push", "pull_request"):
        assert event in on
        assert "paths" not in (on[event] or {}) and "paths-ignore" not in (on[event] or {})


@pytest.mark.parametrize("name", sorted(SUITES))
def test_workflow_has_a_changes_job_using_the_detector(name):
    jobs = _load(name)["jobs"]
    changes = jobs["changes"]
    assert changes["outputs"]["code"] == "${{ steps.detect.outputs.code }}"
    uses = [step.get("uses") for step in changes["steps"]]
    assert "./.github/actions/detect-code-changes" in uses
    sparse = changes["steps"][0]["with"]["sparse-checkout"]
    assert "scripts/ci_code_changes.py" in sparse


@pytest.mark.parametrize("name,job", [(n, j) for n, js in SUITES.items() for j in js])
def test_suite_job_skips_only_on_an_explicit_false(name, job):
    """A skipped job reports success, so required checks still report. The
    condition skips only on "false": if detection fails, the suite runs."""
    spec = _load(name)["jobs"][job]
    assert spec["needs"] == "changes"
    assert spec["if"] == "${{ !cancelled() && needs.changes.outputs.code != 'false' }}"


def test_phase_a_always_runs_and_switches_to_the_docs_coupled_subset():
    """Pytest Phase A is a required check: it is never skipped. On a
    governance-only change it runs the docs-coupled tests instead of its list."""
    job = _load("ci-tests.yml")["jobs"]["pytest-phase-a"]
    assert job["needs"] == "changes"
    assert job["if"] == "${{ !cancelled() }}"
    steps = {s.get("name"): s for s in job["steps"]}
    subset = steps["Run docs-coupled tests (governance-only or docs-only change, ST-31)"]
    assert subset["if"] == "needs.changes.outputs.code == 'false'"
    assert "--docs-coupled-only" in subset["run"]
    assert steps["Run Phase A clean tests"]["if"] == "needs.changes.outputs.code != 'false'"
    assert steps["Run mock harness smoke tests (BLG-QA-08)"]["if"] == "needs.changes.outputs.code != 'false'"


def test_detector_action_fails_safe():
    action = (ROOT / ".github" / "actions" / "detect-code-changes" / "action.yml").read_text()
    assert "code=true" in action                     # unavailable list -> run everything
    assert '[ "$count" -lt 300 ]' in action          # truncated compare -> run everything
    assert "0000000000000000000000000000000000000000" in action  # new branch -> run everything


# --- docs-coupled selector ----------------------------------------------------

@pytest.mark.parametrize("module", [
    "test_strategy_version_registry.py",
    "test_exit_reason_values.py",
    "test_scan_backlog_gate_conditions_gating_item_shipped.py",
    "test_check_backlog_item_integrity.py",
    "test_ci_code_changes.py",
])
def test_known_docs_reading_tests_are_selected(module):
    assert is_docs_coupled(ROOT / "tests" / module)


@pytest.mark.parametrize("module", [
    "test_stop_reconciliation.py",
    "test_watchlist_service.py",
])
def test_pure_code_tests_are_not_selected(module):
    assert not is_docs_coupled(ROOT / "tests" / module)


@pytest.mark.parametrize("source,expected", [
    ('p = ROOT / "claude" / "backlog" / "backlog.md"', True),
    ("open('docs/specs/data_model.md')", True),
    ('read("strategy_rules.md")', True),
    ('subprocess.run(["python3", "scripts/check_x.py"])', True),
    ("from backend.services import x  # no document read", False),
    ("assert claude_cost == 3", False),
])
def test_selection_rule(tmp_path, source, expected):
    f = tmp_path / "test_sample.py"
    f.write_text(source)
    assert is_docs_coupled(f) is expected
