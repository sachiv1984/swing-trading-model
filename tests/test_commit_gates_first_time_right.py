"""
.claude/hooks/check_commit_gates.py — first-time-right record nudge (2026-11-16, user direction).

A story commit on an exec/** branch that stages non-test src/ or backend/ code warns (never
blocks) when that story's execution_state.json notes have no "First-time-right:" line
(/first-time-right skill, Step 4). The check is the pure first_time_right_warning(); the
module's hook entry point runs only under __main__, so importing it reads no stdin.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / ".claude" / "hooks" / "check_commit_gates.py"

_spec = importlib.util.spec_from_file_location("check_commit_gates_under_test", HOOK)
gates = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gates)

BRANCH = "exec/2026-11-11__release-v9.17/EPIC-05"
CMD = 'git commit -m "[EPIC-05][ST-14] Fix the stop"'


def _state(notes):
    return {"epics": {"EPIC-05": {"stories": {"ST-14": {"notes": notes}, "ST-12": {"notes": ""}}}}}


def test_warns_when_story_has_no_record():
    warning = gates.first_time_right_warning(CMD, BRANCH, ["src/pages/TradePlan.js"], _state("Commit abc."))
    assert warning and "ST-14" in warning and "/first-time-right" in warning


def test_silent_when_record_present_case_insensitive():
    notes = "first-time-right: 2026-11-16 pass A — 1 done"
    assert gates.first_time_right_warning(CMD, BRANCH, ["src/pages/TradePlan.js"], _state(notes)) is None


def test_silent_for_tests_specs_and_docs_only():
    staged = ["tests/e2e/trade-plan-stop-prefill.spec.js", "docs/specs/frontend/pages/trade_plan.md",
              "backend/routers/test.py", "src/lib/foo.test.js"]
    assert gates.first_time_right_warning(CMD, BRANCH, staged, _state("")) is None


def test_silent_off_exec_branches_and_for_governance_commits():
    assert gates.first_time_right_warning(CMD, "main", ["src/pages/TradePlan.js"], _state("")) is None
    gov = 'git commit -m "[GOVERNANCE] Persist state"'
    assert gates.first_time_right_warning(gov, BRANCH, ["src/pages/TradePlan.js"], _state("")) is None


def test_names_every_story_in_a_multi_story_commit_that_lacks_a_record():
    cmd = 'git commit -m "[EPIC-05][ST-12][ST-14] Both"'
    warning = gates.first_time_right_warning(cmd, BRANCH, ["backend/database.py"], _state("First-time-right: ok"))
    assert warning and "missing for ST-12:" in warning


def test_heredoc_commit_message_in_the_command_is_read():
    cmd = "git commit -q -F - <<'EOF'\n[EPIC-05][ST-14] Fix\n\nBody\nEOF"
    assert gates.first_time_right_warning(cmd, BRANCH, ["src/pages/TradePlan.js"], _state("")) is not None


def test_unknown_story_or_missing_state_is_silent():
    assert gates.first_time_right_warning(CMD, BRANCH, ["src/a.js"], None) is None
    other = 'git commit -m "[EPIC-02][ST-05] Not in state"'
    assert gates.first_time_right_warning(other, BRANCH, ["src/a.js"], _state("")) is None


def test_hook_entry_point_still_approves_non_commit_commands():
    out = subprocess.run([sys.executable, str(HOOK)], input=json.dumps({"tool_input": {"command": "ls"}}),
                         capture_output=True, text=True, timeout=20)
    assert json.loads(out.stdout) == {"decision": "approve"}
