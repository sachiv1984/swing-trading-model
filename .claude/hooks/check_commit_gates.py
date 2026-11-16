#!/usr/bin/env python3
# PreToolUse hook logic — warns (never blocks) when a `git commit` is about to
# land without satisfying one of two purely mechanical CLAUDE.md hard gates:
#   - OpenAPI Drift Detection (CLAUDE.md §2 / commit-check Check 3)
#   - Backend route four-way sync (CLAUDE.md §2 / commit-check Check 10)
# plus one process nudge (2026-11-16, user direction):
#   - First-time-right record: a story commit on an exec/** branch that stages
#     non-test src/ or backend/ code, for a story whose execution_state.json
#     notes have no "First-time-right:" line (/first-time-right skill, Step 4)
# These are file-membership checks with no judgment call involved, unlike the
# other commit-check checks (E2E N/A exceptions, governance §6 version-match)
# which stay in the /commit-check skill where an LLM can weigh ambiguous cases.
# Mirrors check_commit_format.py's warn-only posture: diff parsing is heuristic,
# so on any ambiguity this stays silent rather than risk a false block.
import sys
import json
import re
import subprocess

PROJECT_ROOT = "/root/swing-trading-model"


def approve(reason=None):
    out = {"decision": "approve"}
    if reason:
        out["reason"] = reason
    print(json.dumps(out))
    sys.exit(0)


def run(args):
    try:
        return subprocess.run(
            args, cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10
        ).stdout
    except Exception:
        return ""



FTR_MARKER = "first-time-right:"
STORY_ID = re.compile(r"\[(ST-\d+)\]")


def is_code_file(path):
    """Non-test application code: src/** or backend/** (tests and specs excluded)."""
    if not (path.startswith("src/") or path.startswith("backend/")):
        return False
    lowered = path.lower()
    return not ("/tests/" in lowered or lowered.startswith("backend/tests/")
                or ".test." in lowered or ".spec." in lowered
                or "/test_" in lowered or path == "backend/routers/test.py")


def first_time_right_warning(command, branch, staged_files, execution_state):
    """Return a warning string, or None. Pure: no I/O, so it can be unit-tested."""
    if not branch.startswith("exec/"):
        return None
    if not any(is_code_file(f) for f in staged_files):
        return None
    stories = STORY_ID.findall(command or "")
    if not stories or not isinstance(execution_state, dict):
        return None
    missing = []
    for epic in (execution_state.get("epics") or {}).values():
        for story_id, story in (epic.get("stories") or {}).items():
            if story_id in stories:
                notes = str((story or {}).get("notes") or "").lower()
                if FTR_MARKER not in notes:
                    missing.append(story_id)
    if not missing:
        return None
    return (
        "First-time-right record missing for " + ", ".join(sorted(set(missing))) +
        ": this commit stages application code, but the story's execution_state.json "
        "notes have no 'First-time-right:' line. Run /first-time-right (pass A before "
        "building, pass B before review) and record it, or say why it does not apply."
    )


def load_execution_state():
    try:
        with open(f"{PROJECT_ROOT}/.claude_current_state.json") as fh:
            path = json.load(fh).get("execution_state_path")
        if not path:
            return None
        with open(f"{PROJECT_ROOT}/{path}") as fh:
            return json.load(fh)
    except Exception:
        return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        approve()

    command = data.get("tool_input", {}).get("command", "") or ""

    if "git commit" not in command:
        approve()

    staged_files = [f for f in run(["git", "diff", "--cached", "--name-only"]).splitlines() if f]
    if not staged_files:
        approve()

    warnings = []

    # --- Check 3: OpenAPI drift detection ---------------------------------
    api_contract_files = [
        f for f in staged_files
        if f.startswith("docs/specs/api_contracts/") and f.endswith(".md")
    ]
    heading_pattern = re.compile(r'^\+##\s+(GET|POST|PUT|DELETE|PATCH)\s+/\S+')

    new_endpoints = []
    for f in api_contract_files:
        diff = run(["git", "diff", "--cached", "--", f])
        for line in diff.splitlines():
            if line.startswith("+++"):
                continue
            m = heading_pattern.match(line)
            if m:
                new_endpoints.append((f, line[1:].strip()))

    if new_endpoints and "docs/reference/openapi.yaml" not in staged_files:
        lines = "\n".join(f"  {f}: {heading}" for f, heading in new_endpoints)
        warnings.append(
            "OpenAPI Drift Detection — new API contract heading(s) staged without "
            "docs/reference/openapi.yaml:\n" + lines +
            "\n\nCLAUDE.md §2: every new API endpoint must be added to openapi.yaml "
            "in the same commit as the contract. This fails the OpenAPI Drift "
            "Detection CI gate and blocks the PR."
        )

    # --- Check 10: Backend route four-way sync -----------------------------
    router_files = [
        f for f in staged_files
        if f.startswith("backend/routers/") and f.endswith(".py") and f != "backend/routers/test.py"
    ]
    decorator_pattern = re.compile(r'^\+\s*@router\.(get|post|put|delete)\(')

    new_routes = []
    for f in router_files:
        diff = run(["git", "diff", "--cached", "--", f])
        for line in diff.splitlines():
            if line.startswith("+++"):
                continue
            if decorator_pattern.match(line):
                new_routes.append((f, line[1:].strip()))

    if new_routes:
        required = [
            "backend/routers/test.py",
            "src/pages/SystemStatus.js",
            "tests/e2e/system-status.spec.js",
        ]
        missing = [r for r in required if r not in staged_files]
        if missing:
            lines = "\n".join(f"  {f}: {decorator}" for f, decorator in new_routes)
            warnings.append(
                "Backend route four-way sync — new route decorator(s) staged without "
                "all required companion files:\n" + lines +
                "\n\nMissing from staged set: " + ", ".join(missing) +
                "\n\nCLAUDE.md §2: a new route requires (1) a test.py entry, "
                "(2) the SystemStatus.js fallback count bumped, and "
                "(3) SC-SS-01b updated in system-status.spec.js — all in the same commit."
            )

    # --- First-time-right record (process nudge) --------------------------
    ftr = first_time_right_warning(
        command,
        run(["git", "branch", "--show-current"]).strip(),
        staged_files,
        load_execution_state(),
    )
    if ftr:
        warnings.append(ftr)

    if not warnings:
        approve()

    approve("\n\n".join(warnings))


if __name__ == "__main__":
    main()
