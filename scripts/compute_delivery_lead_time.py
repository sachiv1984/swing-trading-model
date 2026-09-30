#!/usr/bin/env python3
"""
Compute median filed->shipped lead time by priority band, per release cycle,
from claude/backlog/backlog_archive.md (ST-32, EPIC-06, v9.8, BLG-GOV-340).

Filed date: the trailing "- YYYY-MM-DD" citation on a retired item's
**Source:** line, or (when absent, typically for idea-intake-sourced items)
the roadmap-rebalance/promotion date embedded in that same line's own text.
See docs/specs/metrics_definitions.md Appendix F, "Delivery Lead Time by
Priority Band", for the full methodology and disclosed limitations.

Usage: python3 scripts/compute_delivery_lead_time.py
"""
import re
import sys
from collections import defaultdict
from datetime import date
from statistics import median

ARCHIVE = "claude/backlog/backlog_archive.md"

HEADER_RE = re.compile(r"^### (BLG-[A-Z]+-\d+) — (.+)$", re.M)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
SHIPPED_RE = re.compile(r"^\*\*Shipped in:\*\*\s*(v[\d.]+)", re.M)
RETIRED_RE = re.compile(r"^\*\*Retired:\*\*\s*(\d{4}-\d{2}-\d{2})", re.M)
PRIORITY_AT_RETIREMENT_RE = re.compile(r"^\*\*Priority at retirement:\*\*\s*(P\d)", re.M)
SOURCE_RE = re.compile(r"^\*\*Source:\*\*\s*(.+)$", re.M)

CYCLE_TO_VERSION = {
    "2026-09-09__release-v9.3": "v9.3",
    "2026-09-14__release-v9.4": "v9.4",
    "2026-09-15__release-v9.5": "v9.5",
    "2026-09-21__release-v9.6": "v9.6",
    "2026-09-23__release-v9.7": "v9.7",
}
TARGET_VERSIONS = set(CYCLE_TO_VERSION.values())


def filed_date_from_source(source_line: str):
    # Prefer a trailing "— YYYY-MM-DD" at the end of the line.
    trailing = re.search(r"—\s*(\d{4}-\d{2}-\d{2})\s*$", source_line)
    if trailing:
        return trailing.group(1)
    # Fallback: first date-shaped substring anywhere in the line.
    m = DATE_RE.search(source_line)
    if m:
        return m.group(1)
    return None


def main():
    text = open(ARCHIVE).read()
    headers = list(HEADER_RE.finditer(text))

    # Each BLG id appears twice consecutively: a short retirement-stamp block,
    # then the full original entry. Pair them up positionally.
    entries = []
    i = 0
    while i < len(headers):
        h = headers[i]
        blg_id = h.group(1)
        start = h.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]

        shipped_m = SHIPPED_RE.search(block)
        retired_m = RETIRED_RE.search(block)
        prio_m = PRIORITY_AT_RETIREMENT_RE.search(block)

        if shipped_m and retired_m and prio_m:
            # This is a short retirement-stamp block. Look ahead to the next
            # block (same BLG id, the full original entry) for its Source line.
            filed_date = None
            if i + 1 < len(headers) and headers[i + 1].group(1) == blg_id:
                next_start = headers[i + 1].end()
                next_end = headers[i + 2].start() if i + 2 < len(headers) else len(text)
                next_block = text[next_start:next_end]
                source_m = SOURCE_RE.search(next_block)
                if source_m:
                    filed_date = filed_date_from_source(source_m.group(1))
                i += 1  # consume the paired full-entry block too
            entries.append({
                "id": blg_id,
                "shipped_version": shipped_m.group(1),
                "retired_date": retired_m.group(1),
                "priority": prio_m.group(1),
                "filed_date": filed_date,
            })
        i += 1

    by_cycle_priority = defaultdict(list)
    skipped_no_filed = []
    for e in entries:
        if e["shipped_version"] not in TARGET_VERSIONS:
            continue
        if not e["filed_date"]:
            skipped_no_filed.append(e["id"])
            continue
        filed = date.fromisoformat(e["filed_date"])
        retired = date.fromisoformat(e["retired_date"])
        lead_days = (retired - filed).days
        if lead_days < 0:
            # Filed-date extraction picked up a later/unrelated date in the
            # Source line prose rather than the true filing date; exclude.
            skipped_no_filed.append(e["id"] + " (negative lead time, excluded)")
            continue
        by_cycle_priority[(e["shipped_version"], e["priority"])].append(lead_days)

    print("=== Median filed->shipped lead time (days) by priority band, per cycle ===")
    for version in ["v9.3", "v9.4", "v9.5", "v9.6", "v9.7"]:
        row = []
        for prio in ["P0", "P1", "P2", "P3", "P4"]:
            vals = by_cycle_priority.get((version, prio), [])
            if vals:
                row.append(f"{prio}: n={len(vals)} median={median(vals):.1f}d")
        total_n = sum(len(v) for k, v in by_cycle_priority.items() if k[0] == version)
        print(f"{version} (n={total_n}): " + " | ".join(row))

    print(f"\nSkipped (no usable filed date): {len(skipped_no_filed)}")
    for s in skipped_no_filed[:30]:
        print(f"  {s}")


if __name__ == "__main__":
    sys.exit(main())
