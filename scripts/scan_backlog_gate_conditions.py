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
        this scan flags rather than silently treats it as ungated).
        Matched inside either parentheses (the original BLG-OPS-48 form)
        or square brackets (the BLG-FEAT-73 form, e.g.
        `[gate status unverified/unmet]` — a 5th distinct failure mode,
        BLG-GOV-292, self-caught during v8.5 release planning and fixed
        at v8.5 post-ship closure)

Date-lapsed detection (ST-27, EPIC-07, v9.6, BLG-GOV-345): a gated item's
`gate_condition` text is also scanned for an embedded ISO date
(`YYYY-MM-DD`, with or without a leading `~`). If found and that date is
on or before the scan's as-of date, the item is additionally reported in
a separate "date-lapsed — verify" list. This does NOT remove the item
from the main gated list or change `gated`/`gate_condition` in any way —
a lapsed date means the condition needs re-verification, not that it is
automatically cleared (silently auto-clearing a gate the scan cannot
itself verify would be worse than the permanently-gated bug this fixes).
Consumed by `release_planning_prompt.md` §1.3a, which requires this list
be read — and each item verified and either cleared or re-gated with a
new dated condition — before the ready pool is fixed.

Usage:
    python3 scripts/scan_backlog_gate_conditions.py [--json] [--as-of YYYY-MM-DD]

Exit code is always 0 — this is a scan/report tool consumed by Release
Planning's STEP 1, not a hard CI gate (backlog items are allowed to be
gated; the goal is visibility, not blocking).
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

BACKLOG_PATH = Path("claude/backlog/backlog.md")
EMBEDDED_DATE_RE = re.compile(r"~?(\d{4}-\d{2}-\d{2})")

HEADING_RE = re.compile(r"^### (BLG-[A-Z]+-[A-Za-z0-9]+|TEST-GAP-[A-Za-z0-9-]+) — (.+)$")
GATE_CRITERIA_RE = re.compile(r"^\*\*Gate criteria:\*\*\s*(.+)$", re.MULTILINE)
GATE_SHORT_RE = re.compile(r"^\*\*Gate:\*\*\s*(.+)$", re.MULTILINE)
GATE_DATE_RE = re.compile(r"^\*\*Gate date:\*\*\s*(.+)$", re.MULTILINE)
PROVISIONAL_TARGET_RE = re.compile(r"^\*\*Provisional-Target:\*\*\s*(.+)$", re.MULTILINE)

# Free-text signals inside Provisional-Target that suggest an embedded gate
# condition masquerading as a plain target (the BLG-OPS-48 pattern before
# its duplicate-field defect was fixed — kept here as a defensive check in
# case the pattern recurs on a different item).
#
# Two delimiter forms are covered (BLG-GOV-292, v8.5 post-ship closure):
# parentheses (the original BLG-OPS-48 pattern) and square brackets (the
# BLG-FEAT-73 pattern — `[gate status unverified/unmet]` — a 5th distinct
# failure mode in this same problem class, self-caught during v8.5 release
# planning). Matched as two alternatives rather than a single bracket-class
# pattern so each delimiter must open and close with its own kind (no
# cross-matching a stray `(` with a `]`).
EMBEDDED_GATE_SIGNAL_RE = re.compile(
    r"\(.*(gate|gated|no earlier than|conditional|pending).*\)"
    r"|"
    r"\[.*(gate|gated|no earlier than|conditional|pending|unmet|unverified).*\]",
    re.IGNORECASE,
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


def _lapsed_date(gate_condition, as_of):
    """Return the first embedded ISO date in gate_condition if it is on or
    before as_of, else None. Multiple dates (e.g. a 'due' date and an
    unrelated year reference) are not disambiguated — the first match is
    used, matching this scan's existing single-first-match convention for
    every other field."""
    m = EMBEDDED_DATE_RE.search(gate_condition)
    if not m:
        return None
    try:
        found = datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None
    return found if found <= as_of else None


def classify_item(item_id, title, body, as_of):
    result = {
        "id": item_id,
        "title": title,
        "gated": False,
        "gate_source": None,
        "gate_condition": None,
        "data_quality_warning": None,
        "date_lapsed": None,
    }

    m = GATE_CRITERIA_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate criteria"
        result["gate_condition"] = m.group(1).strip()
        result["date_lapsed"] = _lapsed_date(result["gate_condition"], as_of)
        return result

    m = GATE_SHORT_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate"
        result["gate_condition"] = m.group(1).strip()
        result["date_lapsed"] = _lapsed_date(result["gate_condition"], as_of)
        return result

    m = GATE_DATE_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate date"
        result["gate_condition"] = m.group(1).strip()
        result["date_lapsed"] = _lapsed_date(result["gate_condition"], as_of)
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
    parser.add_argument("--as-of", default=None, help="ISO date to evaluate lapsed gates against (default: today)")
    args = parser.parse_args()

    as_of = datetime.date.fromisoformat(args.as_of) if args.as_of else datetime.date.today()

    if not BACKLOG_PATH.exists():
        print(f"ERROR: {BACKLOG_PATH} not found", file=sys.stderr)
        sys.exit(0)

    text = BACKLOG_PATH.read_text()
    items = parse_items(text)
    results = [classify_item(item_id, title, body, as_of) for item_id, title, body in items]

    gated = [r for r in results if r["gated"]]
    warnings = [r for r in results if r["data_quality_warning"]]
    date_lapsed = [r for r in gated if r["date_lapsed"]]

    if args.json:
        print(json.dumps({
            "as_of": as_of.isoformat(),
            "gated": gated,
            "date_lapsed": [{**r, "date_lapsed": r["date_lapsed"].isoformat()} for r in date_lapsed],
            "data_quality_warnings": warnings,
            "total_items": len(results),
        }, indent=2, default=str))
        sys.exit(0)

    print(f"Scanned {len(results)} backlog items ({BACKLOG_PATH}), as of {as_of.isoformat()}.")
    print(f"\n{len(gated)} gated/conditional item(s):")
    for r in gated:
        lapsed_note = f"  [DATE-LAPSED {r['date_lapsed'].isoformat()} — verify]" if r["date_lapsed"] else ""
        print(f"  {r['id']} — [{r['gate_source']}] {r['gate_condition']}{lapsed_note}")

    if date_lapsed:
        print(f"\n{len(date_lapsed)} item(s) with a lapsed gate date — verify before treating as still gated (do not auto-clear):")
        for r in date_lapsed:
            print(f"  {r['id']} — gate date {r['date_lapsed'].isoformat()} — {r['gate_condition']}")

    if warnings:
        print(f"\n{len(warnings)} data-quality warning(s) (embedded gate language, no formal Gate field):")
        for r in warnings:
            print(f"  {r['id']} — {r['data_quality_warning']}")

    print("\nExit code 0 (scan/report tool — not a hard CI gate).")
    sys.exit(0)


if __name__ == "__main__":
    main()
