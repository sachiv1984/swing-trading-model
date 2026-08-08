#!/usr/bin/env python3
"""
Backlog Gate-Condition Scan (ST-29, EPIC-07, v8.4; BLG-GOV-286).

Canonical, scripted (not ad hoc) procedure for detecting whether a backlog
candidate in claude/backlog/backlog.md is gate-blocked. Used by
release_planning_prompt.md STEP 1 (§1.4a Perennial-Return Check and the
gate-detection step that precedes it) instead of manually reading each
candidate's fields.

Why this exists as a script and not prose guidance: the ad hoc reading
practice produced 3 self-caught scan misses across 3 consecutive Release
Planning cycles (v8.0, v8.1, v8.2 — see BLG-GOV-286's Problem statement)
plus a 4th failure mode self-caught scanning for this very story (v8.4):
a missing `---` separator between two adjacent backlog entries lets one
item's body text bleed into the next item's field scan. The same class of
prose-advisory-failed-twice pattern that justified elevating the API
performance baseline check to a script (see
check_api_performance_baseline_drift.py's own docstring) applies here.

Item boundaries are always determined by the next `### BLG-` (or
`### TEST-GAP-`) heading — never by the `---` separator, which this repo's
live backlog.md is not 100% consistent about (20 of 293 gaps currently
lack it; see this story's qa evidence for the count). This structurally
eliminates failure mode 4 rather than just detecting it.

Gate-field variants covered (failure modes 1-3):
    **Gate criteria:**   — canonical field, most items
    **Gate:**             — short-form variant
    **Gate date:**        — date-only variant
    **Provisional-Target:** containing gate-like free text with no formal
        Gate field present — flagged as a data-quality warning (the
        BLG-OPS-48 pattern that caused 2 of the 3 original misses; the
        canonical fix is for the item to carry a proper Gate field, so
        this scan flags rather than silently treats it as ungated)

Usage:
    python3 scripts/scan_backlog_gate_conditions.py [--json]

Exit code is always 0 — this is a scan/report tool consumed by Release
Planning's STEP 1, not a hard CI gate (backlog items are allowed to be
gated; the goal is visibility, not blocking).
"""
import argparse
import json
import re
import sys
from pathlib import Path

BACKLOG_PATH = Path("claude/backlog/backlog.md")

HEADING_RE = re.compile(r"^### (BLG-[A-Z]+-[A-Za-z0-9]+|TEST-GAP-[A-Za-z0-9-]+) — (.+)$")
GATE_CRITERIA_RE = re.compile(r"^\*\*Gate criteria:\*\*\s*(.+)$", re.MULTILINE)
GATE_SHORT_RE = re.compile(r"^\*\*Gate:\*\*\s*(.+)$", re.MULTILINE)
GATE_DATE_RE = re.compile(r"^\*\*Gate date:\*\*\s*(.+)$", re.MULTILINE)
PROVISIONAL_TARGET_RE = re.compile(r"^\*\*Provisional-Target:\*\*\s*(.+)$", re.MULTILINE)

# Free-text signals inside Provisional-Target that suggest an embedded gate
# condition masquerading as a plain target (the BLG-OPS-48 pattern before
# its duplicate-field defect was fixed — kept here as a defensive check in
# case the pattern recurs on a different item).
EMBEDDED_GATE_SIGNAL_RE = re.compile(
    r"\(.*(gate|gated|no earlier than|conditional|pending).*\)", re.IGNORECASE
)


def parse_items(text: str):
    """Split backlog.md into (item_id, title, body) blocks using heading
    boundaries only — never the `---` separator (failure mode 4 fix)."""
    lines = text.split("\n")
    heading_idx = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m:
            heading_idx.append((i, m.group(1), m.group(2)))

    items = []
    for n, (start, item_id, title) in enumerate(heading_idx):
        end = heading_idx[n + 1][0] if n + 1 < len(heading_idx) else len(lines)
        body = "\n".join(lines[start:end])
        items.append((item_id, title, body))
    return items


def classify_item(item_id, title, body):
    result = {
        "id": item_id,
        "title": title,
        "gated": False,
        "gate_source": None,
        "gate_condition": None,
        "data_quality_warning": None,
    }

    m = GATE_CRITERIA_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate criteria"
        result["gate_condition"] = m.group(1).strip()
        return result

    m = GATE_SHORT_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate"
        result["gate_condition"] = m.group(1).strip()
        return result

    m = GATE_DATE_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate date"
        result["gate_condition"] = m.group(1).strip()
        return result

    # No formal gate field found — check for an embedded-gate signal inside
    # Provisional-Target as a data-quality warning (does not mark the item
    # gated; the canonical fix is adding a proper Gate field).
    pt = PROVISIONAL_TARGET_RE.search(body)
    if pt and EMBEDDED_GATE_SIGNAL_RE.search(pt.group(1)):
        result["data_quality_warning"] = (
            f"Provisional-Target contains gate-like free text with no formal "
            f"Gate field: {pt.group(1).strip()!r}"
        )

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a text report")
    args = parser.parse_args()

    if not BACKLOG_PATH.exists():
        print(f"ERROR: {BACKLOG_PATH} not found", file=sys.stderr)
        sys.exit(0)

    text = BACKLOG_PATH.read_text()
    items = parse_items(text)
    results = [classify_item(item_id, title, body) for item_id, title, body in items]

    gated = [r for r in results if r["gated"]]
    warnings = [r for r in results if r["data_quality_warning"]]

    if args.json:
        print(json.dumps({"gated": gated, "data_quality_warnings": warnings, "total_items": len(results)}, indent=2))
        sys.exit(0)

    print(f"Scanned {len(results)} backlog items ({BACKLOG_PATH}).")
    print(f"\n{len(gated)} gated/conditional item(s):")
    for r in gated:
        print(f"  {r['id']} — [{r['gate_source']}] {r['gate_condition']}")

    if warnings:
        print(f"\n{len(warnings)} data-quality warning(s) (embedded gate language, no formal Gate field):")
        for r in warnings:
            print(f"  {r['id']} — {r['data_quality_warning']}")

    print("\nExit code 0 (scan/report tool — not a hard CI gate).")
    sys.exit(0)


if __name__ == "__main__":
    main()
