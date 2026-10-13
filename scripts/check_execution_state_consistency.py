#!/usr/bin/env python3
"""
Mechanical form of the execution_state.json read-back in execution_prompt.md
§9.2 (ST-41, BLG-GOV-363, EPIC-06, v9.12).

§9.2 makes the top-level summary fields projections of per-story `status`
and per-EPIC `pr_status`, and requires a read-back from disk after every
state write. Done by hand, that read-back is the same memory-dependent step
the ESC-CLOSE-20260930-02 ruling exists to remove. This script checks:

  1. completed_items   == the set of stories with status done/merged
  2. blocked_items ∪ delegated_items == the set of stories with a blocked_* status
  3. merge_gate.epics_merged == EPICs with pr_status merged, and
     merge_gate.epics_pending == the remaining EPICs
  4. merge_gate.all_merged is true exactly when epics_pending is empty

plus the per-record rules §9.2 names alongside them:
  - a story with status done/merged has commit_sha and completed_utc set
  - an EPIC with qa_signed_off true has status done/merged (§9.2 item 5)

Usage: python3 scripts/check_execution_state_consistency.py <execution_state.json>
Exit 0 = consistent; 1 = mismatches (one per line, naming the field); 2 = usage/IO error.
"""
import json
import sys
from pathlib import Path

DONE = {"done", "merged"}


def _ids(values):
    return sorted(set(values or []), key=lambda s: (len(s), s))


def check_state(state: dict) -> list:
    epics = state.get("epics", {})
    stories = {sid: rec for epic in epics.values() for sid, rec in epic.get("stories", {}).items()}
    problems = []

    done = {sid for sid, rec in stories.items() if rec.get("status") in DONE}
    recorded = set(state.get("completed_items") or [])
    if recorded != done:
        problems.append(f"completed_items: missing {_ids(done - recorded)}, unexpected {_ids(recorded - done)}")

    blocked = {sid for sid, rec in stories.items() if str(rec.get("status", "")).startswith("blocked_")}
    listed = set(state.get("blocked_items") or []) | set(state.get("delegated_items") or [])
    if listed != blocked:
        problems.append(f"blocked_items/delegated_items: blocked_* stories not listed {_ids(blocked - listed)}, "
                        f"listed but not blocked_* {_ids(listed - blocked)}")

    gate = state.get("merge_gate") or {}
    merged = {eid for eid, epic in epics.items() if epic.get("pr_status") == "merged"}
    if set(gate.get("epics_merged") or []) != merged:
        problems.append(f"merge_gate.epics_merged: expected {_ids(merged)}, found {_ids(gate.get('epics_merged'))}")
    pending = set(epics) - merged
    if set(gate.get("epics_pending") or []) != pending:
        problems.append(f"merge_gate.epics_pending: expected {_ids(pending)}, found {_ids(gate.get('epics_pending'))}")
    if bool(gate.get("all_merged")) != (not gate.get("epics_pending")):
        problems.append(f"merge_gate.all_merged: is {gate.get('all_merged')!r} but epics_pending is "
                        f"{_ids(gate.get('epics_pending'))}")

    for sid in sorted(done, key=lambda s: (len(s), s)):
        for field in ("commit_sha", "completed_utc"):
            if not stories[sid].get(field):
                problems.append(f"{sid}.{field}: empty on a story with status {stories[sid]['status']}")
    for eid, epic in sorted(epics.items()):
        if epic.get("qa_signed_off") is True and epic.get("status") not in DONE:
            problems.append(f"{eid}.status: is {epic.get('status')!r} but qa_signed_off is true (expected done/merged)")
    return problems


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.strip().splitlines()[-2], file=sys.stderr)
        return 2
    path = Path(argv[0])
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        return 2
    problems = check_state(state)
    for p in problems:
        print(p)
    if problems:
        print(f"\n{len(problems)} inconsistency(ies) in {path}. Correct and re-run before advancing "
              "(execution_prompt.md §9.2).", file=sys.stderr)
        return 1
    print(f"OK: {path} summary fields match per-story and per-EPIC records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
