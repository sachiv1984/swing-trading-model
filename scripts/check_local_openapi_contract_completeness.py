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

Usage (pre-commit hook — runs against the full current working tree, same
as the CI gate; not staged-diff-scoped, since the underlying scripts already
scan the complete docs/specs/api_contracts/ + openapi.yaml + backend/routers/
tree and that full-tree check is what "mirrors the existing CI gate's logic"
means here):
    python3 scripts/check_local_openapi_contract_completeness.py

Exit code 0: no drift found by either check.
Exit code 1: at least one check found drift — commit is blocked.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CHECKS = [
    REPO_ROOT / "scripts" / "lint_api_contract_headings.py",
    REPO_ROOT / "scripts" / "openapi_3way_drift_sweep.py",
]


def run_checks(checks=None, python=None) -> int:
    """Run each check script in order; return 0 if all pass, 1 if any fail.
    Runs all checks even if an earlier one fails, so a single hook run
    surfaces every issue at once rather than stopping at the first."""
    checks = checks if checks is not None else CHECKS
    python = python or sys.executable
    overall_rc = 0
    for check in checks:
        result = subprocess.run([python, str(check)], capture_output=False)
        if result.returncode != 0:
            overall_rc = 1
    return overall_rc


def main() -> int:
    rc = run_checks()
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
