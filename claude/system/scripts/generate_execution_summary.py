#!/usr/bin/env python3
"""Regenerate claude/cycles/<cycle_id>/execution_state.json as a computed summary
from claude/cycles/<cycle_id>/execution_state/EPIC-*.json (per-EPIC mechanism, ST-19).

This file is never hand-edited. A git conflict on the generated execution_state.json
is resolved by re-running this script on the merged main branch, not by manual merge.

Usage:
    python3 claude/system/scripts/generate_execution_summary.py <cycle_id>

Reads:
    claude/cycles/<cycle_id>/execution_state/_cycle_meta.json   (cycle-level fields)
    claude/cycles/<cycle_id>/execution_state/EPIC-*.json        (one per EPIC)

Writes:
    claude/cycles/<cycle_id>/execution_state.json                (regenerated summary)
"""
import json
import sys
import glob
import os
from datetime import datetime, timezone


def main():
    if len(sys.argv) != 2:
        print("Usage: generate_execution_summary.py <cycle_id>", file=sys.stderr)
        sys.exit(1)

    cycle_id = sys.argv[1]
    repo_root = os.getcwd()
    cycle_dir = os.path.join(repo_root, "claude", "cycles", cycle_id)
    state_dir = os.path.join(cycle_dir, "execution_state")
    meta_path = os.path.join(state_dir, "_cycle_meta.json")
    out_path = os.path.join(cycle_dir, "execution_state.json")

    if not os.path.isdir(state_dir):
        print(f"No per-EPIC execution_state directory at {state_dir}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path) as f:
        meta = json.load(f)

    epic_files = sorted(glob.glob(os.path.join(state_dir, "EPIC-*.json")))
    if not epic_files:
        print(f"No EPIC-*.json files found in {state_dir}", file=sys.stderr)
        sys.exit(1)

    epics = {}
    blocked_items = []
    delegated_items = []
    completed_items = []
    epics_merged = []
    epics_pending = []

    for path in epic_files:
        with open(path) as f:
            epic = json.load(f)
        epic_id = epic["epic_id"]

        epics[epic_id] = {
            "status": epic["status"],
            "branch": epic["branch"],
            "pr_number": epic.get("pr_number"),
            "pr_status": epic.get("pr_status", "none"),
            "qa_signed_off": epic.get("qa_signed_off", False),
            "qa_evidence_log": epic.get("qa_evidence_log"),
            "test_scenarios": epic.get("test_scenarios", []),
            "stories": epic.get("stories", {}),
        }

        if epic["status"] == "merged":
            epics_merged.append(epic_id)
        else:
            epics_pending.append(epic_id)

        for st_id, story in epic.get("stories", {}).items():
            full_id = f"{epic_id}/{st_id}"
            status = story.get("status", "not_started")
            if status.startswith("blocked_"):
                blocked_items.append(full_id)
            if story.get("classification", "").startswith("delegated"):
                delegated_items.append(full_id)
            if status in ("done", "merged"):
                completed_items.append(full_id)

    summary = {
        "cycle_id": meta["cycle_id"],
        "sprint_goal": meta.get("sprint_goal", ""),
        "backlog_slice_source": meta.get("backlog_slice_source", ""),
        "invoked_utc": meta.get("invoked_utc"),
        "mode": meta.get("mode", "standard"),
        "status": meta.get("status", "Running"),
        "last_updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "epics": epics,
        "blocked_items": sorted(blocked_items),
        "delegated_items": sorted(delegated_items),
        "completed_items": sorted(completed_items),
        "open_escalations": meta.get("open_escalations", []),
        "merge_gate": {
            "epics_merged": sorted(epics_merged),
            "epics_pending": sorted(epics_pending),
            "all_merged": len(epics_pending) == 0,
        },
        "process_notes": meta.get("process_notes", []),
        "sealed": meta.get("sealed", False),
        "sealed_utc": meta.get("sealed_utc"),
        "_generated_by": "claude/system/scripts/generate_execution_summary.py — do not hand-edit",
    }

    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")

    print(f"Regenerated {out_path} from {len(epic_files)} EPIC file(s): "
          f"{len(epics_merged)} merged, {len(epics_pending)} pending.")


if __name__ == "__main__":
    main()
