#!/usr/bin/env python3
"""
check_doq_signoff_staleness.py — ST-18 (EPIC-04, v8.3, BLG-QA-98)

Pre-merge lint: fails if any claude/cycles/*/qa_evidence_EPIC-*.md file
still carries a "Pending DoQ" or "Awaiting QA" placeholder in its
acceptance-criteria table (per claude/system/templates/qa_evidence_template.md's
own documented convention: these two strings are pre-signing placeholders
only and must be updated to "Pass"/"Fail" before the sign-off block is
completed).

Problem this catches (BLG-QA-98): a per-EPIC PR's own QA evidence check
(quality_gate.yml's "Verify QA Evidence" step) only reads the ONE
qa_evidence file matching that PR's own EPIC ID. A cross-EPIC merge
conflict resolution (CLAUDE.md §8) can combine or touch qa_evidence
content from a DIFFERENT EPIC without that EPIC's own PR re-running the
per-EPIC check — a residual "Pending" row can then reach main unflagged.
This script scans every qa_evidence file in the ACTIVE cycle, not just
the current PR's own EPIC, closing that gap.

Scope (important): only the ACTIVE cycle's qa_evidence files are scanned
(cycle_id read from .claude_current_state.json, same source the existing
"Verify QA Evidence" quality_gate.yml step already uses) — NOT every
qa_evidence file in repo history. Historical cycles are closed, sealed
Class 4 planning documents (document_lifecycle_guide.md) that legitimately
retain old "Pending"/"Awaiting QA" text from before their own sign-off was
completed at the time; a repo-wide scan would find dozens of such
pre-existing, immutable, already-shipped occurrences and permanently block
every future PR. Confirmed empirically: an unscoped first draft of this
script found 6 such occurrences across 4 already-closed cycles (v1.10,
v2.0, v2.9, v3.7) dating back to 2026-03/04 — none of them are this
story's concern, and none are fixable without violating the sealed-
artefact rule (CLAUDE.md §2).

Usage:
    python3 scripts/check_doq_signoff_staleness.py [cycle_id]

If cycle_id is omitted, it is read from .claude_current_state.json's
active_cycle field.

Exit code 0: no stale placeholders found in any qa_evidence file in scope.
Exit code 1: at least one file in scope has a residual Pending/Awaiting-QA row.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CYCLES_DIR = REPO_ROOT / "claude" / "cycles"
STATE_PATH = REPO_ROOT / ".claude_current_state.json"

# Case-sensitive, matching the exact placeholder strings documented in
# qa_evidence_template.md's own authoring note. Anchored to `| ... |` so it
# only matches a placeholder occupying its own table cell (the template's
# actual documented usage: a standalone Result-column value) — not any
# occurrence of the phrase, which false-positives on prose that quotes the
# placeholder strings by name (e.g. this very script's own ST-18 row in
# qa_evidence_EPIC-04.md, which describes what the check catches).
STALE_PLACEHOLDER_RE = re.compile(r"\|\s*(?:Pending DoQ|Awaiting QA)\s*\|")


def find_stale_placeholders(text):
    """Return a list of (line_number, line_text) for every line containing
    a stale sign-off placeholder. Pure function — no filesystem access —
    so it can be unit-tested directly against a synthetic string."""
    findings = []
    for i, line in enumerate(text.splitlines(), start=1):
        if STALE_PLACEHOLDER_RE.search(line):
            findings.append((i, line.strip()))
    return findings


def find_qa_evidence_files(cycle_id):
    cycle_dir = CYCLES_DIR / cycle_id
    if not cycle_dir.is_dir():
        return []
    return sorted(cycle_dir.glob("qa_evidence_EPIC-*.md"))


def get_active_cycle():
    if not STATE_PATH.exists():
        return None
    state = json.loads(STATE_PATH.read_text())
    return state.get("active_cycle")


def main():
    cycle_id = sys.argv[1] if len(sys.argv) > 1 else get_active_cycle()
    if not cycle_id:
        print("Error: no cycle_id given and active_cycle not set in .claude_current_state.json.")
        return 1

    files = find_qa_evidence_files(cycle_id)
    if not files:
        print(f"No qa_evidence_EPIC-*.md files found for cycle {cycle_id} — nothing to check.")
        return 0

    total_findings = 0
    for path in files:
        text = path.read_text()
        findings = find_stale_placeholders(text)
        if findings:
            total_findings += len(findings)
            rel = path.relative_to(REPO_ROOT)
            print(f"STALE SIGN-OFF: {rel}")
            for line_no, line_text in findings:
                print(f"  line {line_no}: {line_text}")

    if total_findings == 0:
        print(f"Checked {len(files)} qa_evidence file(s) in cycle {cycle_id} — no stale sign-off placeholders found.")
        return 0

    print(f"\n{total_findings} stale sign-off placeholder(s) found across {len(files)} file(s) checked.")
    print("Update the Result column from 'Pending DoQ'/'Awaiting QA' to 'Pass'/'Pass with notes'/'Fail' "
          "before this PR can merge (qa_evidence_template.md's own authoring note).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
