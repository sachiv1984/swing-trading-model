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

Gating-item-shipped detection (ST-40, EPIC-06, v9.12, BLG-GOV-386): a gate
whose condition is "`BLG-X` shipped/complete" stays gated after `BLG-X`
ships, because nothing re-reads it. v9.11 Release Planning found 26 such
items by hand (`BLG-OPS-179` genuinely ready, `BLG-FE-195` already
delivered). A gated item whose `gate_condition` names one or more `BLG-*`
IDs (other than its own), every one of which is either absent from the
active backlog.md (archived) or bannered `✅ COMPLETE`, is reported in a
separate "gating item shipped — verify" list. As with the date-lapsed list,
this never clears the gate: a shipped dependency means the condition needs
re-reading, since some gates also name a soak period or a non-BLG
condition. An item whose gate names at least one still-active item is not
listed. Consumed by `release_planning_prompt.md` §1.3a alongside the
date-lapsed list.

Explicitly-ungated values (ST-35, EPIC-06, v9.13, BLG-GOV-390): a gate
field whose whole value is `None`, `N/A`, `-` or `—` (case-insensitive,
trimmed, optional trailing period) says the item has no gate. The field
regexes capture any non-empty value, so these used to be reported as gated:
17 items on 2026-10-15, silently left out of every Release Planning ready
pool. They are now treated as ungated and counted separately as
"explicitly ungated", so the change stays visible in the scan output.

Known non-gate dates (ST-36, EPIC-06, v9.13, BLG-GOV-373): some gate
conditions embed a date that does not govern the gate, such as a counting
start or a provenance note. BLG-OPS-53 (the v4.0 ship date, 2026-05-22) and
BLG-FEAT-92 (a 2026-09-03 decision date) were reported as date-lapsed at
every rebalance from 2026-09-28 to 2026-10-06 and excluded by hand each
time. KNOWN_NON_GATE_DATES lists those items, each with a reason and a
review date. An entry with a `date` ignores only that date when deciding
whether the gate has lapsed, so any other date in the same condition
(BLG-OPS-53's `clears 2026-11-22`) still counts. An entry with `date: None`
ignores every date in the item's gate, for a gate that has no date of its
own (BLG-FEAT-92 inherits BLG-FEAT-30's gate, and its provenance notes
carried three different dates). The entries are reported in their own
"known non-gate dates" section, which also says when an entry is past its
review date or its date is no longer in the item's gate.

Usage:
    python3 scripts/scan_backlog_gate_conditions.py [--json] [--as-of YYYY-MM-DD] [--backlog PATH]

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
# ST-35 (BLG-GOV-390): a gate field value that says "no gate".
EXPLICITLY_UNGATED_RE = re.compile(r"(?:none|n/a|-|—)\.?", re.IGNORECASE)

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
GATE_BLG_REF_RE = re.compile(r"\bBLG-[A-Z]+-\d+\b")
COMPLETE_BANNER = "✅ COMPLETE"

ALREADY_RESOLVED_RE = re.compile(
    r"\*\*(Resolutions?|Resolved)\s*\(.*?\):\*\*",
    re.IGNORECASE,
)


# ST-36 (BLG-GOV-373): items whose embedded gate date(s) do not govern the
# gate. Each needs a reason and a review date. "date": None ignores every
# date in that item's gate; review the entry by its review_by date.
KNOWN_NON_GATE_DATES = [
    {
        "id": "BLG-OPS-53",
        "date": "2026-05-22",
        "reason": "v4.0 ship date: the start of the 6-month claude_audit_log age count, not the gate date",
        "review_by": "2026-11-22",
    },
    {
        "id": "BLG-FEAT-92",
        "date": None,
        "reason": "provenance notes (Product Owner reconciliation decision 2026-09-03 and later); the gate is inherited from BLG-FEAT-30 and carries no date of its own",
        "review_by": "2027-01-16",
    },
]


def _ignored_dates(item_id, allow_list):
    """Dates to ignore for item_id, or None when every date is ignored."""
    entries = [e for e in allow_list if e["id"] == item_id]
    if any(e["date"] is None for e in entries):
        return None
    return {datetime.date.fromisoformat(e["date"]) for e in entries}


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


def _lapsed_date(gate_condition, as_of, ignored=frozenset()):
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
    for kw in GOVERNING_KEYWORD_DATE_RE.finditer(gate_condition):
        try:
            governing = datetime.date.fromisoformat(kw.group(1))
        except ValueError:
            continue  # fall through to the no-keyword-match path below
        if governing in ignored:
            continue
        return (governing if governing <= as_of else None), False

    found_dates = []
    for raw in EMBEDDED_DATE_RE.findall(gate_condition):
        try:
            found = datetime.date.fromisoformat(raw)
        except ValueError:
            continue
        if found not in ignored:
            found_dates.append(found)

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


def classify_item(item_id, title, body, as_of, allow_list=KNOWN_NON_GATE_DATES):
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
        "explicitly_ungated": None,
    }

    ar = ALREADY_RESOLVED_RE.search(body)
    if ar:
        result["already_resolved"] = ar.group(0)

    for source, regex in (("Gate criteria", GATE_CRITERIA_RE), ("Gate", GATE_SHORT_RE), ("Gate date", GATE_DATE_RE)):
        m = regex.search(body)
        if not m:
            continue
        condition = m.group(1).strip()
        if EXPLICITLY_UNGATED_RE.fullmatch(condition):
            # ST-35 (BLG-GOV-390): "None"/"N/A" means no gate; keep looking
            # at the other gate fields rather than reporting it as gated.
            result["explicitly_ungated"] = f"{source}: {condition}"
            continue
        result["gated"] = True
        result["gate_source"] = source
        result["gate_condition"] = condition
        ignored = _ignored_dates(item_id, allow_list)
        if ignored is not None:
            result["date_lapsed"], result["date_ambiguous"] = _lapsed_date(condition, as_of, ignored)
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


def known_non_gate_dates(results, as_of, allow_list=KNOWN_NON_GATE_DATES):
    """ST-36 (BLG-GOV-373): one row per allow-list entry, with whether its
    date still appears in the item's gate and whether its review is due."""
    by_id = {r["id"]: r for r in results}
    rows = []
    for e in allow_list:
        r = by_id.get(e["id"])
        rows.append({
            **e,
            "present": bool(r and r["gated"] and (e["date"] is None or e["date"] in r["gate_condition"])),
            "review_due": datetime.date.fromisoformat(e["review_by"]) <= as_of,
        })
    return rows


def gating_item_shipped(results, items):
    """ST-40 (BLG-GOV-386): return [(result, shipped_ids)] for gated items
    whose gate names at least one BLG-* ID and all of those IDs are archived
    (absent from the active backlog) or bannered ✅ COMPLETE."""
    active_open = {item_id for item_id, title, body in items if COMPLETE_BANNER not in body}
    shipped = []
    for r in results:
        if not r["gated"]:
            continue
        refs = sorted(set(GATE_BLG_REF_RE.findall(r["gate_condition"])) - {r["id"]})
        if refs and not any(ref in active_open for ref in refs):
            shipped.append((r, refs))
    return shipped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a text report")
    parser.add_argument("--as-of", default=None, help="ISO date to evaluate lapsed gates against (default: today)")
    parser.add_argument("--backlog", default=str(BACKLOG_PATH), help="backlog file to scan (default: claude/backlog/backlog.md)")
    args = parser.parse_args()
    backlog_path = Path(args.backlog)

    as_of = datetime.date.fromisoformat(args.as_of) if args.as_of else datetime.date.today()

    if not backlog_path.exists():
        print(f"ERROR: {backlog_path} not found", file=sys.stderr)
        sys.exit(0)

    text = backlog_path.read_text()
    items = parse_items(text)
    results = [classify_item(item_id, title, body, as_of) for item_id, title, body in items]

    gated = [r for r in results if r["gated"]]
    warnings = [r for r in results if r["data_quality_warning"]]
    date_lapsed = [r for r in gated if r["date_lapsed"]]
    already_resolved = [r for r in results if r["already_resolved"]]
    explicitly_ungated = [r for r in results if r["explicitly_ungated"] and not r["gated"]]
    shipped = gating_item_shipped(results, items)
    non_gate_dates = known_non_gate_dates(results, as_of)

    if args.json:
        print(json.dumps({
            "as_of": as_of.isoformat(),
            "gated": gated,
            "date_lapsed": [{**r, "date_lapsed": r["date_lapsed"].isoformat()} for r in date_lapsed],
            "data_quality_warnings": warnings,
            "already_resolved": already_resolved,
            "explicitly_ungated": explicitly_ungated,
            "known_non_gate_dates": non_gate_dates,
            "gating_item_shipped": [{**r, "shipped_gating_items": refs} for r, refs in shipped],
            "total_items": len(results),
        }, indent=2, default=str))
        sys.exit(0)

    print(f"Scanned {len(results)} backlog items ({backlog_path}), as of {as_of.isoformat()}.")
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

    if non_gate_dates:
        print(f"\n{len(non_gate_dates)} known non-gate date(s) (allow-listed; ignored for date-lapse, other dates in the same gate still count):")
        for e in non_gate_dates:
            flags = "" if e["present"] else "  [not in the item's current gate — check whether the entry is still needed at review]"
            if e["review_due"]:
                flags += f"  [REVIEW DUE {e['review_by']}]"
            print(f"  {e['id']} — {e['date'] or 'all dates'} — {e['reason']} (review by {e['review_by']}){flags}")

    if shipped:
        print(f"\n{len(shipped)} item(s) whose gate names only shipped backlog items (gating item shipped — verify; re-read the gate, do not auto-clear):")
        for r, refs in shipped:
            print(f"  {r['id']} — gating item(s) {', '.join(refs)} archived or ✅ COMPLETE — {r['gate_condition']}")

    if explicitly_ungated:
        print(f"\n{len(explicitly_ungated)} explicitly ungated item(s) (gate field reads None/N/A — informational, not gated):")
        for r in explicitly_ungated:
            print(f"  {r['id']} — [{r['explicitly_ungated']}]")

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
