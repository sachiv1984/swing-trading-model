#!/usr/bin/env python3
"""Pre-commit check: a staged .claude_current_state.json must not point at a
missing execution_state.json (BLG-GOV-430 lesson, 2026-11-19).

tests/test_state_execution_path_consistency.py already guards this, but only in
CI. At v9.18 (and v9.17) the sprint-start commit set status Executing on main
while execution_state.json existed only on the EPIC branch, so every PR cut
from main failed CI until the EPIC merged. This runs the same two checks
against the git INDEX (what is being committed), only when the state file is
staged:

  1. execution_state_path == claude/cycles/<active_cycle>/execution_state.json
  2. from Sprint Execution on (status not in PRE_EXECUTION_STATUSES), that file
     is in the index — committed already or staged in this commit.

Exit 1 with the reason on a mismatch; exit 0 otherwise (including when the state
file is not staged). Usage: python3 scripts/check_staged_state_path.py
"""

import json
import subprocess
import sys

STATE = ".claude_current_state.json"
# Same list as tests/test_state_execution_path_consistency.py.
PRE_EXECUTION_STATUSES = {"Release_Planning_Complete", "Design_Gate_Passed", "Sprint_Planning_Complete"}


def _git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def check(state: dict, in_index) -> list:
    """Return problems; in_index(path) -> bool says whether path is in the index."""
    problems = []
    expected = f"claude/cycles/{state.get('active_cycle')}/execution_state.json"
    path = state.get("execution_state_path")
    if path != expected:
        problems.append(f"execution_state_path is {path!r}; active_cycle expects {expected!r}")
    if state.get("status") not in PRE_EXECUTION_STATUSES and path and not in_index(path):
        problems.append(
            f"status is {state.get('status')!r} but {path} is not in this commit or the branch: "
            "commit execution_state.json together with the status change (BLG-GOV-430)"
        )
    return problems


def main() -> int:
    staged = _git("diff", "--cached", "--name-only").stdout.split()
    if STATE not in staged:
        return 0
    shown = _git("show", f":{STATE}")
    if shown.returncode != 0:
        return 0  # deleted from the index; nothing to check
    problems = check(json.loads(shown.stdout), lambda p: _git("cat-file", "-e", f":{p}").returncode == 0)
    for p in problems:
        print(f"[state-path check] {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
