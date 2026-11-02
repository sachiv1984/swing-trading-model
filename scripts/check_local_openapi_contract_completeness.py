#!/usr/bin/env python3
"""
check_local_openapi_contract_completeness.py — ST-23 (BLG-GOV-179, EPIC-05, v9.3)

Local pre-commit mirror of the CI-level OpenAPI Drift Detection gate
(.github/workflows/openapi-drift.yml), so a new `## METHOD /path` heading
added to docs/specs/api_contracts/*.md without a matching
docs/reference/openapi.yaml entry (or vice versa) is caught before the
commit ever leaves the local machine, not just at CI push-time — the same
"catch it locally first" principle already established by the sibling
check_router_test_registration.py hook (ST-10, EPIC-10, v7.9, BLG-QA-125).

Runs the 2 checks the CI gate itself runs, in the same order:
  1. scripts/lint_api_contract_headings.py — catches the "###-level
     silent-fail" case (a miscoded heading depth invisible to the `##`-only
     drift regex).
  2. scripts/openapi_3way_drift_sweep.py — catches contract-vs-openapi.yaml
     drift (the CI gate's own core check) AND additionally router-decorator
     drift (a broader check than the CI gate's 2-way comparison, still
     satisfying "at least the same class of omission" since it's a strict
     superset).

Usage:
    python3 scripts/check_local_openapi_contract_completeness.py           # manual run: working tree
    python3 scripts/check_local_openapi_contract_completeness.py --staged  # pre-commit hook: index

Both modes check the full tree the CI gate checks (every contract file,
openapi.yaml and backend/routers/), not just the changed files.

--staged (ST-31, BLG-QA-238, EPIC-05, v9.14): the hook passes this flag.
The staged version of every input file, and of the 2 check scripts, is
exported from the index (`git checkout-index`) into a temporary directory
and the checks run there. A route still undocumented in another story's
unstaged work therefore no longer blocks an unrelated, complete commit
(found at v9.13 EPIC-02, ST-13; LL-v9.13-P3-01). An undocumented route in
staged content still fails. Without the flag, a manual run checks the
working tree as before.

Exit code 0: no drift found by either check.
Exit code 1: at least one check found drift — commit is blocked.
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CHECK_SCRIPTS = [
    "scripts/lint_api_contract_headings.py",
    "scripts/openapi_3way_drift_sweep.py",
]
CHECKS = [REPO_ROOT / check for check in CHECK_SCRIPTS]

# Everything the 2 checks read, relative to the repo root. --staged exports
# the index version of these (and of CHECK_SCRIPTS) before running.
STAGED_INPUTS = [
    "docs/specs/api_contracts",
    "docs/reference/openapi.yaml",
    "backend/routers",
    "backend/main.py",
]


def run_checks(checks=None, python=None, cwd=None) -> int:
    """Run each check script in order; return 0 if all pass, 1 if any fail.
    Runs all checks even if an earlier one fails, so a single hook run
    surfaces every issue at once rather than stopping at the first.
    lint_api_contract_headings.py resolves its default directory from the
    current directory, so cwd must be the root of the tree being checked."""
    checks = checks if checks is not None else CHECKS
    python = python or sys.executable
    cwd = cwd or REPO_ROOT
    overall_rc = 0
    for check in checks:
        result = subprocess.run([python, str(check)], capture_output=False, cwd=cwd)
        if result.returncode != 0:
            overall_rc = 1
    return overall_rc


def export_index(repo_root: Path, dest: Path) -> None:
    """Write the staged (index) version of the check scripts and their inputs
    under dest, keeping repo-relative paths."""
    paths = CHECK_SCRIPTS + STAGED_INPUTS
    files = subprocess.run(
        ["git", "ls-files", "-z", "--", *paths],
        cwd=repo_root, capture_output=True, check=True,
    ).stdout
    subprocess.run(
        ["git", "checkout-index", "-z", "--stdin", f"--prefix={dest}/"],
        cwd=repo_root, input=files, check=True,
    )


def run_staged_checks(repo_root: Path = REPO_ROOT, python=None) -> int:
    with tempfile.TemporaryDirectory(prefix="openapi-staged-") as tmp:
        tree = Path(tmp)
        export_index(repo_root, tree)
        return run_checks(checks=[tree / check for check in CHECK_SCRIPTS], python=python, cwd=tree)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "--staged", action="store_true",
        help="check the staged (index) content instead of the working tree (used by .githooks/pre-commit)",
    )
    args = parser.parse_args(argv)
    rc = run_staged_checks() if args.staged else run_checks()
    if rc != 0:
        print(
            "\nMERGE BLOCKED locally: OpenAPI contract completeness check failed "
            "(mirrors .github/workflows/openapi-drift.yml). Resolve the drift "
            "listed above before committing.",
            file=sys.stderr,
        )
    return rc


if __name__ == "__main__":
    sys.exit(main())
