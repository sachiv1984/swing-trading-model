"""
ST-42 (BLG-OPS-188, EPIC-06, v9.14) — ci-usage-report.yml's monthly commit.

The workflow's only scheduled run (2026-10-01, run 36861580190) failed at
"Commit report": it pushed straight to main, and main's branch protection
requires a pull request with an approving review, which a GITHUB_TOKEN push
cannot bypass. The report now goes to its own branch and an artifact, and
the workflow opens a [GOVERNANCE] PR for a human to merge.

The confirming run on main (AC 1, and AC 2's 2026-09.md) is post-merge,
tracked by BLG-OPS-202. These tests pin the workflow's shape.
"""
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).parent.parent / ".github" / "workflows" / "ci-usage-report.yml"


def _steps():
    wf = yaml.safe_load(WORKFLOW.read_text())
    return {s["name"]: s for s in wf["jobs"]["generate-report"]["steps"]}, wf


def test_report_is_not_pushed_to_main():
    steps, _ = _steps()
    commit = steps["Commit report to its branch and open a PR"]["run"]
    assert 'BRANCH="ci-usage-report/${YM}"' in commit
    assert 'git push --force origin "$BRANCH"' in commit
    for line in commit.splitlines():
        if "git push" in line:
            assert '"$BRANCH"' in line, line
    assert "Commit report" not in steps  # the old step that pushed to main


def test_a_pr_to_main_is_opened_with_a_governance_title():
    steps, wf = _steps()
    commit = steps["Commit report to its branch and open a PR"]["run"]
    assert 'TITLE="[GOVERNANCE] Add monthly CI usage report ${YM}"' in commit
    assert 'gh pr create --base main --head "$BRANCH"' in commit
    assert wf["permissions"] == {"contents": "write", "pull-requests": "write"}


def test_a_refused_pr_does_not_fail_the_run_and_prints_the_compare_link():
    steps, _ = _steps()
    commit = steps["Commit report to its branch and open a PR"]["run"]
    assert 'if PR_URL="$(gh pr create' in commit and '2>pr_error.txt' in commit
    assert "::warning::" in commit and "${COMPARE}" in commit
    # Only GitHub's "not permitted" refusal takes the warning path.
    assert 'grep -qi "not permitted to create or approve pull requests" pr_error.txt' in commit


def test_any_other_pr_failure_fails_the_run():
    steps, _ = _steps()
    commit = steps["Commit report to its branch and open a PR"]["run"]
    tail = commit.split('grep -qi "not permitted', 1)[1]
    assert "else" in tail and "::error::gh pr create failed" in tail and "exit 1" in tail
    assert 'COMPARE="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/compare/main...${BRANCH}"' in commit


def test_report_is_kept_as_an_artifact():
    steps, _ = _steps()
    upload = steps["Upload report artifact"]
    assert upload["uses"].startswith("actions/upload-artifact@")
    assert upload["with"]["path"] == "docs/ops/ci_usage_reports/${{ steps.generate.outputs.year_month }}.md"


def test_year_month_input_is_validated_not_interpolated_into_the_shell():
    steps, _ = _steps()
    gen = steps["Generate report"]
    assert gen["env"]["INPUT_YEAR_MONTH"] == "${{ inputs.year_month }}"
    assert "${{ inputs" not in gen["run"]
    assert "^[0-9]{4}-(0[1-9]|1[0-2])$" in gen["run"]
    assert 'echo "year_month=$YM" >> "$GITHUB_OUTPUT"' in gen["run"]
