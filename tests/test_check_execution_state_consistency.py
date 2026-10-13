"""
ST-41 (BLG-GOV-363, EPIC-06, v9.12) — scripts/check_execution_state_consistency.py
passes on a consistent execution_state.json and fails, naming the field, for
each of execution_prompt.md §9.2's four equality breaks.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("ckstate", ROOT / "scripts" / "check_execution_state_consistency.py")
ckstate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ckstate)

CONSISTENT = {
    "completed_items": ["ST-01", "ST-02"],
    "blocked_items": ["ST-03"],
    "delegated_items": ["ST-04"],
    "merge_gate": {"epics_merged": ["EPIC-01"], "epics_pending": ["EPIC-02"], "all_merged": False},
    "epics": {
        "EPIC-01": {"status": "merged", "pr_status": "merged", "qa_signed_off": True, "stories": {
            "ST-01": {"status": "merged", "commit_sha": "a1", "completed_utc": "2026-10-13T00:00:00Z"},
        }},
        "EPIC-02": {"status": "in_progress", "pr_status": "none", "qa_signed_off": False, "stories": {
            "ST-02": {"status": "done", "commit_sha": "b2", "completed_utc": "2026-10-13T01:00:00Z"},
            "ST-03": {"status": "blocked_decision", "commit_sha": None, "completed_utc": None},
            "ST-04": {"status": "blocked_backend", "commit_sha": None, "completed_utc": None},
            "ST-05": {"status": "not_started", "commit_sha": None, "completed_utc": None},
        }},
    },
}


def _break(fn):
    state = copy.deepcopy(CONSISTENT)
    fn(state)
    return ckstate.check_state(state)


def test_consistent_state_passes():
    assert ckstate.check_state(CONSISTENT) == []


@pytest.mark.parametrize("mutate, field", [
    # equality 1: completed_items vs done/merged stories
    (lambda s: s["completed_items"].remove("ST-02"), "completed_items"),
    (lambda s: s["epics"]["EPIC-02"]["stories"]["ST-05"].update(status="done", commit_sha="c", completed_utc="t"), "completed_items"),
    # equality 2: blocked_items ∪ delegated_items vs blocked_* stories
    (lambda s: s["delegated_items"].clear(), "blocked_items/delegated_items"),
    (lambda s: s["blocked_items"].append("ST-05"), "blocked_items/delegated_items"),
    # equality 3: merge_gate.epics_merged / epics_pending vs pr_status
    (lambda s: s["epics"]["EPIC-02"].update(pr_status="merged"), "merge_gate.epics_merged"),
    (lambda s: s["merge_gate"].update(epics_pending=[]), "merge_gate.epics_pending"),
    # equality 4: all_merged vs epics_pending empty
    (lambda s: s["merge_gate"].update(all_merged=True), "merge_gate.all_merged"),
])
def test_each_equality_break_names_its_field(mutate, field):
    problems = _break(mutate)
    assert problems and any(p.startswith(field + ":") for p in problems), problems


def test_done_story_without_commit_sha_or_completed_utc_fails():
    problems = _break(lambda s: s["epics"]["EPIC-02"]["stories"]["ST-02"].update(commit_sha=None, completed_utc=""))
    assert "ST-02.commit_sha: empty on a story with status done" in problems
    assert "ST-02.completed_utc: empty on a story with status done" in problems


def test_qa_signed_off_epic_must_be_done():
    problems = _break(lambda s: s["epics"]["EPIC-02"].update(qa_signed_off=True))
    assert any(p.startswith("EPIC-02.status:") for p in problems)


def test_cli_exit_codes(tmp_path, capsys):
    good = tmp_path / "good.json"
    good.write_text(json.dumps(CONSISTENT))
    assert ckstate.main([str(good)]) == 0
    bad_state = copy.deepcopy(CONSISTENT)
    bad_state["merge_gate"]["all_merged"] = True
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(bad_state))
    assert ckstate.main([str(bad)]) == 1
    assert "merge_gate.all_merged" in capsys.readouterr().out
    assert ckstate.main([]) == 2
