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


def tally(path: Path) -> Counter:
    text = path.read_text()
    story_matches = list(STORY_RE.finditer(text))
    counts = Counter()
    for i, m in enumerate(story_matches):
        start = m.end()
        end = story_matches[i + 1].start() if i + 1 < len(story_matches) else len(text)
        block = text[start:end]
        owner_m = OWNER_RE.search(block)
        if owner_m:
            counts[owner_m.group(1).strip()] += 1
    return counts


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
        counts = tally(p)
        total = sum(counts.values())
        cycle = p.parent.name
        results[cycle] = {"total": total, "by_role": dict(counts.most_common())}

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
