#!/usr/bin/env python3
"""
Tally each ST item's `**Owner:**` field per role from a cycle's
sprint_backlog.md (ST-33, EPIC-06, v9.8, BLG-GOV-341).

Extracted from roadmap_prompt.md STEP 7.2's own manual method so the same
parsing logic backfills claude/roadmap/role_share_history.md and can be
re-run at each future rebalance, instead of STEP 7.2 re-deriving the tally
by hand from raw sprint_backlog.md text each time.

Usage: python3 scripts/compute_role_share_history.py <sprint_backlog.md path> [...]
Prints, for each file, a per-role story count and the file's total story
count. With --json, prints a single JSON object keyed by cycle folder name.

Attribution check (ST-45, BLG-QA-212, EPIC-06, v9.12): a `#### ST-` block
with no `**Owner:**` line, or an ST heading at any other level, is reported
rather than silently dropped. Each file's `st_headings` count is compared
with its attributed `total`, and any difference is printed as a WARNING to
stderr and listed under `unattributed` / `other_level_headings` in --json.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Matches "#### ST-xx — <title>" followed (within the same story block, before
# the next "#### ST-" or "---") by "**Owner:** <role>".
STORY_RE = re.compile(r"^####\s+(ST-\d+[a-z]?)\b.*$", re.M)
OWNER_RE = re.compile(r"^\*\*Owner:\*\*\s*(.+?)\s*$", re.M)
ANY_ST_HEADING_RE = re.compile(r"^#{1,6}\s+(ST-\d+[a-z]?)\b.*$", re.M)


def analyse(text: str) -> dict:
    """Raw tally plus attribution diagnostics for one sprint_backlog.md."""
    story_matches = list(STORY_RE.finditer(text))
    counts = Counter()
    unattributed = []
    for i, m in enumerate(story_matches):
        start = m.end()
        end = story_matches[i + 1].start() if i + 1 < len(story_matches) else len(text)
        owner_m = OWNER_RE.search(text[start:end])
        if owner_m:
            counts[owner_m.group(1).strip()] += 1
        else:
            unattributed.append(m.group(1))
    level4 = {m.start() for m in story_matches}
    other_level = [m.group(1) for m in ANY_ST_HEADING_RE.finditer(text) if m.start() not in level4]
    return {
        "counts": counts,
        "st_headings": len(story_matches) + len(other_level),
        "unattributed": unattributed,
        "other_level_headings": other_level,
    }


def tally(path: Path) -> Counter:
    return analyse(path.read_text())["counts"]


def main() -> int:
    args = sys.argv[1:]
    as_json = "--json" in args
    paths = [Path(a) for a in args if a != "--json"]
    if not paths:
        print("Usage: python3 scripts/compute_role_share_history.py <sprint_backlog.md path> [...] [--json]", file=sys.stderr)
        return 1

    results = {}
    for p in paths:
        if not p.exists():
            print(f"Not found: {p}", file=sys.stderr)
            return 1
        a = analyse(p.read_text())
        counts = a["counts"]
        total = sum(counts.values())
        cycle = p.parent.name
        results[cycle] = {"total": total, "by_role": dict(counts.most_common()),
                          "st_headings": a["st_headings"], "unattributed": a["unattributed"],
                          "other_level_headings": a["other_level_headings"]}
        if total != a["st_headings"]:
            print(f"WARNING: {cycle}: {a['st_headings']} ST headings but {total} attributed stories "
                  f"(difference {a['st_headings'] - total}); no Owner line: {a['unattributed'] or 'none'}; "
                  f"non-#### ST headings: {a['other_level_headings'] or 'none'}", file=sys.stderr)

    if as_json:
        print(json.dumps(results, indent=2))
    else:
        for cycle, data in results.items():
            print(f"=== {cycle} (total {data['total']} stories) ===")
            for role, count in data["by_role"].items():
                pct = 100 * count / data["total"] if data["total"] else 0
                print(f"  {role}: {count} ({pct:.1f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
