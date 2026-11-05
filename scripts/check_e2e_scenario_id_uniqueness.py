#!/usr/bin/env python3
"""
Playwright scenario-ID uniqueness check (ST-42, BLG-QA-224, EPIC-07, v9.15).

A scenario ID (the leading `SC-XX-NN` / `V-XX-NN` token of a `test(...)`
title) cited in evidence must name one scenario. `epic01-v34-lifecycle.spec.js`
(Trail Stop modal) and `epic01-v62-stops-alerts.spec.js` (trailing-stop
column) both used SC-TS-01..06 for different scenarios, so an evidence line
citing "SC-TS-04" was ambiguous; ST-42 renamed the second file's IDs SC-TSC-*.

This script fails when one scenario ID is used in more than one file under
tests/e2e. Repeats inside a single file are not checked.

KNOWN_DUPLICATES lists the pre-existing cross-file duplicates outside ST-42's
SC-TS scope, tracked by BLG-QA-250. It may only shrink: an entry that is no
longer duplicated fails the check, so a fix must also remove its entry.

Usage: python3 scripts/check_e2e_scenario_id_uniqueness.py [--root tests/e2e]
Exit 0 = unique (apart from KNOWN_DUPLICATES); 1 = a new duplicate or a stale
KNOWN_DUPLICATES entry, one line each; 2 = usage/IO error.
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

E2E_ROOT = Path("tests/e2e")
TEST_TITLE_ID_RE = re.compile(
    r"""\btest(?:\.only|\.skip|\.fixme|\.fail)?\(\s*['"`]([A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)+)(?=[:\s'"`])"""
)

# BLG-QA-250: rename one side of each and update its citations.
KNOWN_DUPLICATES = {
    **{f"SC-CSV-0{n}": ("screener-watchlist-csv-export.spec.js", "tax-year-csv-export.spec.js") for n in range(1, 6)},
    **{f"SC-GP-0{n}": ("epic01-v34-lifecycle.spec.js", "gate-progress.spec.js") for n in range(1, 5)},
    **{f"SC-LS-0{n}": ("epic01-v34-lifecycle.spec.js", "loading-states.spec.js") for n in range(1, 5)},
    **{f"SC-MRU-0{n}": ("market-regime-unknown.spec.js", "monthly-pnl-realized-unrealized.spec.js") for n in range(1, 3)},
    **{f"SC-TP-0{n}": ("theme-persistence.spec.js", "trade-plan.spec.js") for n in range(1, 5)},
}


def scenario_ids(root: Path) -> dict:
    """Scenario ID -> set of spec file paths (relative to root) whose test titles use it."""
    ids = defaultdict(set)
    for path in sorted(root.rglob("*.spec.[jt]s")):
        if not path.is_file():
            continue
        for m in TEST_TITLE_ID_RE.finditer(path.read_text(encoding="utf-8")):
            ids[m.group(1)].add(path.relative_to(root).as_posix())
    return ids


def check(ids: dict, known=KNOWN_DUPLICATES) -> list:
    problems = []
    for sid, files in sorted(ids.items()):
        if len(files) > 1 and tuple(sorted(files)) != tuple(sorted(known.get(sid, ()))):
            problems.append(f"{sid}: used in {len(files)} files: {', '.join(sorted(files))}")
    for sid, files in sorted(known.items()):
        if tuple(sorted(ids.get(sid, ()))) != tuple(sorted(files)):
            problems.append(f"{sid}: KNOWN_DUPLICATES entry {sorted(files)} no longer matches "
                            f"{sorted(ids.get(sid, ()))} -- remove or correct the entry")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(E2E_ROOT))
    args = parser.parse_args(argv)
    root = Path(args.root)
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    ids = scenario_ids(root)
    problems = check(ids)
    for p in problems:
        print(p)
    if problems:
        print(f"\n{len(problems)} scenario-ID problem(s) under {root}. Give one file a distinct prefix "
              "and update its citations (ST-42, BLG-QA-224).", file=sys.stderr)
        return 1
    print(f"OK: {len(ids)} scenario IDs under {root}; no new cross-file duplicates "
          f"({len(KNOWN_DUPLICATES)} known, BLG-QA-250)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
