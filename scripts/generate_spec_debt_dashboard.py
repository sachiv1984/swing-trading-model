#!/usr/bin/env python3
"""
Spec Debt Dashboard Generator — ST-16 (BLG-SPEC-69, EPIC-04, v9.3)

Scans claude/backlog/backlog.md for all open BLG-SPEC-* items, extracts a
best-effort filing date from each item's own **Source:** line (a YYYY-MM-DD
date, preferring one immediately preceded by "cycle "/"session"/"—" wording
over other dates that may appear incidentally in the same line), computes
age in days since that date against today, and writes a single-page summary
to docs/specs/spec_debt_dashboard.md.

"Refreshable at future groom backlog runs" (AC): re-run this script any time
after backlog.md changes to regenerate the dashboard with current data — it
has no side effects on backlog.md itself (read-only) and always overwrites
its own output file in full.

Usage: backend/.venv/bin/python3 scripts/generate_spec_debt_dashboard.py
       (or system python3 — this script has no backend/service dependencies)
"""
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BACKLOG_PATH = REPO_ROOT / "claude" / "backlog" / "backlog.md"
OUTPUT_PATH = REPO_ROOT / "docs" / "specs" / "spec_debt_dashboard.md"

ITEM_HEADING_RE = re.compile(r"^### (BLG-SPEC-\d+) — (.+)$")
# Field lines are normally one-per-line ("**Priority:** P3 (Low)"), but at
# least one legacy item (BLG-SPEC-81) packs multiple fields onto one line
# separated by " | " ("**Priority:** P3 | **Type:** ... | **Source:** ...").
# Splitting every line on " | " before matching handles both uniformly —
# a normal line just yields one segment.
FIELD_RE = re.compile(r"^\*\*([A-Za-z ]+):\*\*\s*(.*)$")
# No trailing \b: a date is frequently followed by "__" (e.g. "2026-05-22__scheduled")
# and \b does not count as a boundary between a digit and an underscore (both
# are "word" characters) -- use a negative lookahead for a further digit instead,
# so "2026-05-223" doesn't falsely match "2026-05-22" as a prefix.
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})(?!\d)")


def parse_backlog_items(text: str) -> list[dict]:
    """Parse backlog.md into a list of {id, title, priority, source, ...}
    dicts for every BLG-SPEC-* item found. A new item starts at each
    matching '### BLG-SPEC-N — Title' heading and its fields continue until
    the next '### ' heading or end of file."""
    lines = text.splitlines()
    items = []
    current = None
    for line in lines:
        heading = ITEM_HEADING_RE.match(line)
        if heading:
            if current:
                items.append(current)
            current = {"id": heading.group(1), "title": heading.group(2), "priority": None, "source": None}
            continue
        if line.startswith("### ") and current:
            items.append(current)
            current = None
            continue
        if current is not None:
            for segment in line.split(" | "):
                field = FIELD_RE.match(segment.strip())
                if field:
                    name, value = field.group(1).strip(), field.group(2).strip()
                    if name == "Priority" and current["priority"] is None:
                        current["priority"] = value
                    elif name == "Source" and current["source"] is None:
                        current["source"] = value
    if current:
        items.append(current)
    return items


def extract_filing_date(source_field: str | None) -> date | None:
    """Best-effort: return the last YYYY-MM-DD date found in the Source
    field (backlog.md's convention consistently places the filing/promotion
    date at or near the end of this field, e.g. '... cycle 2026-05-22__scheduled'
    or '... — 2026-09-08')."""
    if not source_field:
        return None
    matches = DATE_RE.findall(source_field)
    if not matches:
        return None
    try:
        return datetime.strptime(matches[-1], "%Y-%m-%d").date()
    except ValueError:
        return None


def priority_sort_key(priority: str | None) -> int:
    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    for p, rank in order.items():
        if priority and priority.startswith(p):
            return rank
    return 99


def main() -> int:
    if not BACKLOG_PATH.exists():
        print(f"ERROR: {BACKLOG_PATH} not found", file=sys.stderr)
        return 1

    text = BACKLOG_PATH.read_text()
    items = parse_backlog_items(text)
    today = date.today()

    rows = []
    undated = []
    for item in items:
        filed = extract_filing_date(item["source"])
        age_days = (today - filed).days if filed else None
        rows.append({**item, "filed": filed, "age_days": age_days})
        if filed is None:
            undated.append(item["id"])

    rows.sort(key=lambda r: (priority_sort_key(r["priority"]), -(r["age_days"] or -1)))

    lines = []
    lines.append("**Owner:** Head of Specs Team")
    lines.append("**Class:** Operational Record (Class 3)")
    lines.append("**Status:** Active")
    lines.append(f"**Last Updated:** {today.isoformat()} (generated by scripts/generate_spec_debt_dashboard.py — ST-16, BLG-SPEC-69, EPIC-04, v9.3)")
    lines.append("**Source:** ST-16 (BLG-SPEC-69, EPIC-04, v9.3 sprint execution)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("# Spec Debt Dashboard")
    lines.append("")
    lines.append("Single-page summary of all open `BLG-SPEC-*` items in `claude/backlog/backlog.md`, with age since filing. Regenerate by re-running `scripts/generate_spec_debt_dashboard.py` (read-only against backlog.md; always overwrites this file in full) — refreshable at any future `groom backlog` run or on demand.")
    lines.append("")
    lines.append(f"**Generated:** {today.isoformat()}")
    lines.append(f"**Total open BLG-SPEC-* items:** {len(rows)}")
    if undated:
        lines.append(f"**Items with no parseable filing date in their Source field:** {len(undated)} ({', '.join(undated)}) — age shown as N/A below; their Source field should be reviewed for a missing or non-standard date.")
    lines.append("")
    lines.append("| ID | Priority | Title | Filed | Age (days) |")
    lines.append("|----|----------|-------|-------|------------|")
    for r in rows:
        filed_str = r["filed"].isoformat() if r["filed"] else "N/A"
        age_str = str(r["age_days"]) if r["age_days"] is not None else "N/A"
        priority_str = r["priority"] or "N/A"
        lines.append(f"| {r['id']} | {priority_str} | {r['title']} | {filed_str} | {age_str} |")
    lines.append("")

    dated_ages = [r["age_days"] for r in rows if r["age_days"] is not None]
    if dated_ages:
        lines.append("## Summary Statistics")
        lines.append("")
        lines.append(f"- Oldest open item: {max(dated_ages)} days")
        lines.append(f"- Median age: {sorted(dated_ages)[len(dated_ages) // 2]} days")
        lines.append(f"- Items open > 90 days: {sum(1 for a in dated_ages if a > 90)}")
        lines.append(f"- Items open > 180 days: {sum(1 for a in dated_ages if a > 180)}")
        lines.append("")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUTPUT_PATH} — {len(rows)} open BLG-SPEC-* items ({len(undated)} undated).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
