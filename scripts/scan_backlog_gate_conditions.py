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

Already-resolved-banner detection (Release Planning lessons_learnt.md
Friction Item 1, `2026-09-23__release-v9.7`; widens `BLG-GOV-345`/ST-27's
date-lapsed fix, which covered only the gate-language half of the same
underlying problem). An item can be functionally already-done — carrying
its own `**Resolution (...):**` or `**Resolved (...):**` block recording
a same-session or prior fix — without the `✅ COMPLETE` banner the first
version of this scan's sibling check (`v9.6` Friction Item 1) looked for.
`BLG-FE-189` slipped through this way at `v9.7`: fixed and Playwright-
covered same-session, but with no `✅ COMPLETE` banner, so a banner-only
scan would still have missed it. Any item body containing `**Resolution
(` or `**Resolved (` (either capitalisation, either heading or bold-field
form) is reported in a separate "already-resolved — verify before
seating" list, independent of gated/ungated status — a candidate is not
truly a fresh selection opportunity if it already carries this marker.

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

# ST-23 (BLG-GOV-347, EPIC-04, v9.9): a date immediately preceded by one of
# these governing keywords is preferred over a bare first-match when a
# gate_condition embeds more than one date — see _lapsed_date()'s docstring.
GOVERNING_KEYWORD_DATE_RE = re.compile(
    r"(?:no earlier than|clears?|due|completes?|by)\s*~?(\d{4}-\d{2}-\d{2})",
    re.IGNORECASE,
)

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

# Already-resolved-banner detection (Release Planning lessons_learnt.md
# Friction Item 1, v9.7) — a `**Resolution (...):**` or `**Resolved (...):**`
# block anywhere in the item body, independent of the `✅ COMPLETE` banner
# convention the original v9.6 sibling check looked for.
ALREADY_RESOLVED_RE = re.compile(
    r"\*\*(Resolutions?|Resolved)\s*\(.*?\):\*\*",
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
    """Return (lapsed_date_or_None, ambiguous) for the embedded ISO date(s)
    in gate_condition.

    ST-23 (BLG-GOV-347, EPIC-04, v9.9): previously used re.search to take
    only the FIRST embedded date, undisambiguated — a gate_condition
    mentioning an earlier, still-future date before a later, already-past
    clears-date was silently reported as NOT lapsed (a false negative that
    could hide a genuinely-clearable item from the ready pool indefinitely,
    since this script drives release_planning_prompt.md §1.3a).

    Fix, in priority order:
      1. If a date is immediately preceded by a governing keyword ("no
         earlier than", "clears", "due", "completes", "by" —
         GOVERNING_KEYWORD_DATE_RE), that date is authoritative regardless
         of any other embedded date. This is the common case in practice
         (e.g. "No earlier than 2026-11-01 (~6 months after ... 2026-05-28)"
         — the keyword date is clearly the one that governs; a bare
         multi-date heuristic would otherwise misflag this as ambiguous).
      2. Otherwise, examine ALL embedded dates:
         - 0 dates: (None, False)
         - All dates agree on lapsed status (all <= as_of, or all > as_of):
           (earliest lapsed date or None, False) — no ambiguity.
         - Dates disagree (at least one <= as_of and at least one > as_of):
           report as LAPSED (the conservative choice — matches this scan's
           existing bias toward surfacing a possibly-clearable item for
           human verification rather than silently hiding it) AND flag
           ambiguous=True, so the report/JSON output distinguishes "lapsed,
           unambiguous" from "lapsed, but multiple dates disagree — verify
           which one actually governs." This satisfies both of the AC's
           accepted resolutions (correctly flagged as lapsed, AND
           explicitly flagged for manual disambiguation) rather than
           choosing only one.
    """
    kw = GOVERNING_KEYWORD_DATE_RE.search(gate_condition)
    if kw:
        try:
            governing = datetime.date.fromisoformat(kw.group(1))
            return (governing if governing <= as_of else None), False
        except ValueError:
            pass  # fall through to the no-keyword-match path below

    found_dates = []
    for raw in EMBEDDED_DATE_RE.findall(gate_condition):
        try:
            found_dates.append(datetime.date.fromisoformat(raw))
        except ValueError:
            continue

    if not found_dates:
        return None, False

    lapsed_dates = [d for d in found_dates if d <= as_of]
    future_dates = [d for d in found_dates if d > as_of]

    if lapsed_dates and future_dates:
        # Disagreement: report lapsed (earliest lapsed date) + ambiguous.
        return min(lapsed_dates), True

    if lapsed_dates:
        return min(lapsed_dates), False

    return None, False


def classify_item(item_id, title, body, as_of):
    result = {
        "id": item_id,
        "title": title,
        "gated": False,
        "gate_source": None,
        "gate_condition": None,
        "data_quality_warning": None,
        "date_lapsed": None,
        "date_ambiguous": False,
        "already_resolved": None,
    }

    ar = ALREADY_RESOLVED_RE.search(body)
    if ar:
        result["already_resolved"] = ar.group(0)

    m = GATE_CRITERIA_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate criteria"
        result["gate_condition"] = m.group(1).strip()
        result["date_lapsed"], result["date_ambiguous"] = _lapsed_date(result["gate_condition"], as_of)
        return result

    m = GATE_SHORT_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate"
        result["gate_condition"] = m.group(1).strip()
        result["date_lapsed"], result["date_ambiguous"] = _lapsed_date(result["gate_condition"], as_of)
        return result

    m = GATE_DATE_RE.search(body)
    if m:
        result["gated"] = True
        result["gate_source"] = "Gate date"
        result["gate_condition"] = m.group(1).strip()
        result["date_lapsed"], result["date_ambiguous"] = _lapsed_date(result["gate_condition"], as_of)
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
    already_resolved = [r for r in results if r["already_resolved"]]

    if args.json:
        print(json.dumps({
            "as_of": as_of.isoformat(),
            "gated": gated,
            "date_lapsed": [{**r, "date_lapsed": r["date_lapsed"].isoformat()} for r in date_lapsed],
            "data_quality_warnings": warnings,
            "already_resolved": already_resolved,
            "total_items": len(results),
        }, indent=2, default=str))
        sys.exit(0)

    print(f"Scanned {len(results)} backlog items ({BACKLOG_PATH}), as of {as_of.isoformat()}.")
    print(f"\n{len(gated)} gated/conditional item(s):")
    for r in gated:
        if r["date_lapsed"]:
            ambiguous_suffix = " — AMBIGUOUS: multiple dates disagree, verify which one governs" if r["date_ambiguous"] else ""
            lapsed_note = f"  [DATE-LAPSED {r['date_lapsed'].isoformat()} — verify{ambiguous_suffix}]"
        else:
            lapsed_note = ""
        print(f"  {r['id']} — [{r['gate_source']}] {r['gate_condition']}{lapsed_note}")

    if date_lapsed:
        print(f"\n{len(date_lapsed)} item(s) with a lapsed gate date — verify before treating as still gated (do not auto-clear):")
        for r in date_lapsed:
            ambiguous_note = " [AMBIGUOUS — multiple embedded dates disagree on lapsed status; manually confirm which date actually governs this gate]" if r["date_ambiguous"] else ""
            print(f"  {r['id']} — gate date {r['date_lapsed'].isoformat()} — {r['gate_condition']}{ambiguous_note}")

    if warnings:
        print(f"\n{len(warnings)} data-quality warning(s) (embedded gate language, no formal Gate field):")
        for r in warnings:
            print(f"  {r['id']} — {r['data_quality_warning']}")

    if already_resolved:
        print(f"\n{len(already_resolved)} item(s) with an already-resolved banner — verify before seating as a fresh selection:")
        for r in already_resolved:
            print(f"  {r['id']} — {r['already_resolved']}")

    print("\nExit code 0 (scan/report tool — not a hard CI gate).")
    sys.exit(0)


if __name__ == "__main__":
    main()
