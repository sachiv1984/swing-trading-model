#!/usr/bin/env python3
"""
Structural integrity check for claude/backlog/backlog.md items (ST-39,
BLG-GOV-385, EPIC-06, v9.12).

A clean `git merge` can splice two backlog items together when both end with
the same metadata lines: at `3237cb5e` (CLAUDE.md §8 merge into v9.11 EPIC-05)
BLG-SPEC-190 kept only its first 5 metadata lines and its Problem/Scope/AC
landed inside BLG-BE-157, which then carried two bodies. git reported no
conflict, so nothing caught it. This script checks every `### BLG-…` item:

  - no item ID appears twice
  - each required metadata field (Priority, Type, Owner, Source, Effort,
    Provisional-Target) appears exactly once, either on its own line or in
    the legacy compact `**A:** x | **B:** y` form
  - exactly one Problem block (`**Problem**` or legacy `**Problem:** …`)
  - at most one Scope block and at most one Acceptance Criteria block
  - either Scope + Acceptance Criteria, or a single legacy
    `**Proposed solution**` block in their place

CLAUDE.md §8 runs it after every merge resolution that touches backlog.md;
.github/workflows/backlog-item-integrity.yml runs it on every PR that does.

Usage: python3 scripts/check_backlog_item_integrity.py [backlog.md ...]
Exit 0 = all items intact; 1 = violations (one per line); 2 = usage/IO error.
"""
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "claude" / "backlog" / "backlog.md"

ITEM_RE = re.compile(r"^### (BLG-[A-Z]+-\d+)\b")
HEADING_RE = re.compile(r"^#{1,3} ")
REQUIRED_FIELDS = ("Priority", "Type", "Owner", "Source", "Effort", "Provisional-Target")
# A field opens a line, or follows a `|` separator in the compact one-line form.
FIELD_RES = {f: re.compile(r"(?:^|\|\s*)\*\*" + re.escape(f) + r":\*\*") for f in REQUIRED_FIELDS}
SECTION_RES = {
    "Problem": re.compile(r"^\*\*Problem(?:\*\*\s*$|:\*\*)"),
    "Scope": re.compile(r"^\*\*Scope(?:\*\*\s*$|:\*\*)"),
    "Acceptance Criteria": re.compile(r"^\*\*Acceptance Criteria(?:\*\*\s*$|:\*\*)"),
    "Proposed solution": re.compile(r"^\*\*Proposed solution(?:\*\*\s*$|:\*\*)"),
}


def parse_items(text: str) -> list:
    """Return [{id, line, body}] for every `### BLG-…` item. An item ends at
    the next heading of level 1-3."""
    items, current = [], None
    for lineno, line in enumerate(text.splitlines(), start=1):
        if HEADING_RE.match(line):
            m = ITEM_RE.match(line)
            current = {"id": m.group(1), "line": lineno, "body": []} if m else None
            if current:
                items.append(current)
            continue
        if current is not None:
            current["body"].append(line)
    return items


def check_text(text: str, label: str = "backlog.md") -> list:
    items = parse_items(text)
    violations = []

    counts = Counter(it["id"] for it in items)
    for item_id, n in sorted(counts.items()):
        if n > 1:
            lines = ", ".join(str(it["line"]) for it in items if it["id"] == item_id)
            violations.append(f"{label}: {item_id} appears {n} times (lines {lines})")

    for it in items:
        where = f"{label}:{it['line']}: {it['id']}"
        body = it["body"]
        for field, rx in FIELD_RES.items():
            n = sum(len(rx.findall(line)) for line in body)
            if n != 1:
                violations.append(f"{where}: **{field}:** found {n} times, expected 1")
        sec = {name: sum(1 for line in body if rx.match(line)) for name, rx in SECTION_RES.items()}
        if sec["Problem"] != 1:
            violations.append(f"{where}: Problem block found {sec['Problem']} times, expected 1")
        for name in ("Scope", "Acceptance Criteria", "Proposed solution"):
            if sec[name] > 1:
                violations.append(f"{where}: {name} block found {sec[name]} times, expected at most 1")
        if sec["Proposed solution"] == 0:
            for name in ("Scope", "Acceptance Criteria"):
                if sec[name] == 0:
                    violations.append(f"{where}: no {name} block (and no legacy Proposed solution block)")
    return violations


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    paths = [Path(a) for a in argv] or [DEFAULT_PATH]
    violations = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read {path}: {exc}", file=sys.stderr)
            return 2
        violations += check_text(text, label=str(path))
    for v in violations:
        print(v)
    if violations:
        print(f"\n{len(violations)} backlog item integrity violation(s). If this follows a merge, "
              "diff each named item against both merge parents and restore it (CLAUDE.md §8).",
              file=sys.stderr)
        return 1
    print(f"OK: backlog item integrity check passed ({', '.join(str(p) for p in paths)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
