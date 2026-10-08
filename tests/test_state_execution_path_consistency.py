"""
ST-27, EPIC-04, v9.9, BLG-GOV-354: .claude_current_state.json's
execution_state_path field must match active_cycle's own execution_state.json.

Root cause (documented in claude/schemas/state_field_owners.json): the field
was previously attributed to sprint_planning_prompt.md ("Phase 2, seal
step"), but that prompt's own STEP 7 write block never actually wrote it --
execution_state.json doesn't exist yet at planning time. A grep across
claude/system/*.md, scripts/*.py, and backend/ found zero readers of this
field anywhere; every engine derives the path directly from active_cycle
instead. Nothing updated the stale pointer at cycle transition because
nothing was ever responsible for updating it.

This test is the "fixed so it can't drift again" mechanism the AC asks
for, since no real code reader exists to serve that role -- it fails on
the next cycle transition that forgets to correct this field, independent
of whether a human or an engine makes that commit.
"""
import json

import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
STATE_FILE = REPO_ROOT / ".claude_current_state.json"


def test_execution_state_path_matches_active_cycle():
    state = json.loads(STATE_FILE.read_text())
    active_cycle = state["active_cycle"]
    expected = f"claude/cycles/{active_cycle}/execution_state.json"
    assert state["execution_state_path"] == expected, (
        f"execution_state_path ({state['execution_state_path']!r}) does not match "
        f"active_cycle ({active_cycle!r}) -- expected {expected!r}. "
        "See claude/schemas/state_field_owners.json's execution_state_path entry "
        "for why this drifts silently (no engine STEP currently writes it)."
    )


# execution_state.json is first written when Sprint Execution starts. Between
# Release Planning and that point the path is correct for the new cycle but the
# file does not exist yet, so the existence check only applies from Executing on.
PRE_EXECUTION_STATUSES = {
    "Release_Planning_Complete",
    "Design_Gate_Passed",
    "Sprint_Planning_Complete",
}


def test_execution_state_path_file_exists():
    state = json.loads(STATE_FILE.read_text())
    if state["status"] in PRE_EXECUTION_STATUSES:
        pytest.skip(f"status {state['status']!r} precedes Sprint Execution; execution_state.json not created yet")
    path = REPO_ROOT / state["execution_state_path"]
    assert path.exists(), f"execution_state_path points to a non-existent file: {path}"
