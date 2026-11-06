"""
ST-41 (BLG-GOV-363, EPIC-06, v9.12) — scripts/check_execution_state_consistency.py
passes on a consistent execution_state.json and fails, naming the field, for
each of execution_prompt.md §9.2's four equality breaks.

ST-44 (BLG-GOV-397, EPIC-07, v9.14) adds two checks: a done/merged story must
have deviations_filed true, and every `## ESC-EXEC-*` heading in the sibling
execution_escalations.md must have a key in open_escalations.

ST-38 (BLG-QA-240, EPIC-07, v9.15): the expected epics_pending set is the
sprint's full EPIC list (initialised epics ∪ merge_order ∪ the sibling
sprint_backlog_index.json), so an EPIC not yet initialised counts as pending.
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
    "open_escalations": {"ESC-EXEC-20261013-01": {"item": "ST-03", "disposition": "Open"}},
    "merge_gate": {"epics_merged": ["EPIC-01"], "epics_pending": ["EPIC-02"], "all_merged": False},
    "epics": {
        "EPIC-01": {"status": "merged", "pr_status": "merged", "qa_signed_off": True, "stories": {
            "ST-01": {"status": "merged", "commit_sha": "a1", "completed_utc": "2026-10-13T00:00:00Z", "deviations_filed": True},
        }},
        "EPIC-02": {"status": "in_progress", "pr_status": "none", "qa_signed_off": False, "stories": {
            "ST-02": {"status": "done", "commit_sha": "b2", "completed_utc": "2026-10-13T01:00:00Z", "deviations_filed": True},
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
    (lambda s: s["epics"]["EPIC-02"]["stories"]["ST-05"].update(status="done", commit_sha="c", completed_utc="t", deviations_filed=True), "completed_items"),
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


ESCALATIONS_MD = """# Execution Escalations

## ESC-EXEC-20261013-01

- **ST/EPIC item:** ST-03 / EPIC-02
"""


def test_consistent_state_with_escalations_passes():
    assert ckstate.check_state(CONSISTENT, ESCALATIONS_MD) == []


@pytest.mark.parametrize("status", ["done", "merged"])
def test_done_story_with_deviations_filed_false_fails_naming_the_story(status):
    problems = _break(lambda s: s["epics"]["EPIC-02"]["stories"]["ST-02"].update(status=status, deviations_filed=False))
    assert f"ST-02.deviations_filed: is False on a story with status {status} (expected true)" in problems


def test_done_story_without_deviations_filed_fails():
    problems = _break(lambda s: s["epics"]["EPIC-02"]["stories"]["ST-02"].pop("deviations_filed"))
    assert any(p.startswith("ST-02.deviations_filed:") for p in problems), problems


def test_not_started_story_with_deviations_filed_false_passes():
    assert _break(lambda s: s["epics"]["EPIC-02"]["stories"]["ST-05"].update(deviations_filed=False)) == []


def test_escalation_heading_without_open_escalations_key_fails_naming_the_id():
    md = ESCALATIONS_MD + "\n## ESC-EXEC-20261014-02\n\n- **ST/EPIC item:** ST-04 / EPIC-02\n"
    problems = ckstate.check_state(CONSISTENT, md)
    assert problems == ["open_escalations.ESC-EXEC-20261014-02: heading in execution_escalations.md has no key"]


def test_escalation_check_ignores_non_heading_mentions():
    md = ESCALATIONS_MD + "\nSee ESC-EXEC-20261099-09 and ### ESC-EXEC-20261099-08 in prose.\n"
    assert ckstate.check_state(CONSISTENT, md) == []


def test_cli_reads_sibling_escalations_file(tmp_path, capsys):
    (tmp_path / "execution_state.json").write_text(json.dumps(CONSISTENT))
    (tmp_path / "execution_escalations.md").write_text(ESCALATIONS_MD)
    assert ckstate.main([str(tmp_path / "execution_state.json")]) == 0
    (tmp_path / "execution_escalations.md").write_text(ESCALATIONS_MD + "\n## ESC-EXEC-20261014-02\n")
    assert ckstate.main([str(tmp_path / "execution_state.json")]) == 1
    assert "open_escalations.ESC-EXEC-20261014-02" in capsys.readouterr().out


SEVEN = ["EPIC-01", "EPIC-02", "EPIC-03", "EPIC-04", "EPIC-05", "EPIC-06", "EPIC-07"]


def _partial(pending, all_merged):
    """Two EPICs merged and initialised; five listed in merge_order only."""
    return {
        "merge_order": SEVEN,
        "completed_items": ["ST-01", "ST-02"],
        "blocked_items": [], "delegated_items": [],
        "merge_gate": {"epics_merged": ["EPIC-01", "EPIC-02"], "epics_pending": pending, "all_merged": all_merged},
        "epics": {
            "EPIC-01": {"status": "merged", "pr_status": "merged", "qa_signed_off": True, "stories": {
                "ST-01": {"status": "merged", "commit_sha": "a1", "completed_utc": "t", "deviations_filed": True}}},
            "EPIC-02": {"status": "merged", "pr_status": "merged", "qa_signed_off": True, "stories": {
                "ST-02": {"status": "merged", "commit_sha": "b2", "completed_utc": "t", "deviations_filed": True}}},
        },
    }


def test_partially_initialised_sprint_passes_with_uninitialised_epics_pending():
    assert ckstate.check_state(_partial(SEVEN[2:], False)) == []


def test_empty_pending_fails_when_merge_order_lists_an_unmerged_epic():
    problems = ckstate.check_state(_partial([], True))
    assert any(p.startswith("merge_gate.epics_pending:") and "EPIC-05" in p for p in problems), problems


def test_index_epics_count_as_pending_without_merge_order():
    state = _partial(SEVEN[2:], False)
    del state["merge_order"]
    assert any(p.startswith("merge_gate.epics_pending:") for p in ckstate.check_state(state))
    assert ckstate.check_state(state, index_epics=SEVEN) == []


def test_cli_reads_sibling_sprint_backlog_index(tmp_path, capsys):
    state = _partial(SEVEN[2:], False)
    del state["merge_order"]
    (tmp_path / "execution_state.json").write_text(json.dumps(state))
    assert ckstate.main([str(tmp_path / "execution_state.json")]) == 1
    capsys.readouterr()
    (tmp_path / "sprint_backlog_index.json").write_text(json.dumps({"epics": {e: {} for e in SEVEN}}))
    assert ckstate.main([str(tmp_path / "execution_state.json")]) == 0
