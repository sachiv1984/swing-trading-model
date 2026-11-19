#!/usr/bin/env python3
"""Report gzipped JS bundle sizes against performance_budget.md §3.3.

ST-06 (BLG-QA-271, EPIC-01, v9.18). Reads every *.js file in <build>/static/js
(the CRA output; *.map and *.LICENSE.txt are not .js and are skipped), gzips each
at level 9 in memory, and compares against the §3.3 budget:

  main bundle (main.*.js)          <= 200 KB
  each other chunk (*.chunk.js)    <= 80 KB
  total of all JS                  <= 500 KB      (1 KB = 1024 bytes)

Report only by default (exit 0), per §3.5: the current single bundle is over
budget until the Phase 4 stage 4 speed work (BLG-FE-315/316/317). Pass --enforce
to exit 1 on any over-budget line. Exits 2 if no JS is found, so a broken build
path never reports an empty, passing table.

Limits: measures gzip, not brotli (GitHub Pages serves gzip); does not see CSS,
images or fonts; a file named main.*.js is the main bundle, anything else is a chunk.

Usage: python3 scripts/perf/check_bundle_size.py [build_dir] [--summary FILE] [--json FILE] [--enforce]
"""

import argparse
import gzip
import json
import sys
from pathlib import Path

KB = 1024
LIMITS = {"main": 200 * KB, "chunk": 80 * KB, "total": 500 * KB}


def measure(build_dir: Path):
    js_dir = build_dir / "static" / "js"
    files = sorted(p for p in js_dir.glob("*.js")) if js_dir.is_dir() else []
    rows = []
    for p in files:
        raw = p.read_bytes()
        kind = "main" if p.name.startswith("main.") else "chunk"
        rows.append({"file": p.name, "kind": kind, "raw": len(raw), "gzip": len(gzip.compress(raw, compresslevel=9))})
    return rows


def evaluate(rows):
    """Return (rows with an 'over' flag, total gzip, list of over-budget messages)."""
    over = []
    for r in rows:
        limit = LIMITS[r["kind"]]
        r["limit"] = limit
        r["over"] = r["gzip"] > limit
        if r["over"]:
            over.append(f"{r['file']}: {r['gzip'] / KB:.1f} KB gzip > {limit / KB:.0f} KB ({r['kind']} budget)")
    total = sum(r["gzip"] for r in rows)
    if total > LIMITS["total"]:
        over.append(f"total JS: {total / KB:.1f} KB gzip > {LIMITS['total'] / KB:.0f} KB")
    return rows, total, over


def markdown(rows, total, over):
    mark = lambda bad: "⚠️ over" if bad else "✅"  # noqa: E731
    lines = [
        "### JS bundle size (gzip -9; performance_budget.md §3.3, report only)",
        "",
        "| File | Kind | Raw KB | Gzip KB | Budget KB | |",
        "|------|------|--------|---------|-----------|---|",
    ]
    for r in rows:
        lines.append(f"| {r['file']} | {r['kind']} | {r['raw'] / KB:.1f} | {r['gzip'] / KB:.1f} | {r['limit'] / KB:.0f} | {mark(r['over'])} |")
    lines.append(f"| **Total** | | | **{total / KB:.1f}** | {LIMITS['total'] / KB:.0f} | {mark(total > LIMITS['total'])} |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("build_dir", nargs="?", default="build")
    ap.add_argument("--summary")
    ap.add_argument("--json")
    ap.add_argument("--enforce", action="store_true")
    a = ap.parse_args(argv)

    rows = measure(Path(a.build_dir))
    if not rows:
        print(f"ERROR: no .js files under {a.build_dir}/static/js — build missing or path wrong", file=sys.stderr)
        return 2
    rows, total, over = evaluate(rows)
    md = markdown(rows, total, over)
    print(md)
    if a.summary:
        with open(a.summary, "a", encoding="utf-8") as fh:
            fh.write(md + "\n")
    if a.json:
        Path(a.json).write_text(json.dumps({"files": rows, "total_gzip": total, "over_budget": over}, indent=2))
    for msg in over:
        # GitHub annotation; visible on the PR without failing the job.
        print(f"::warning title=Bundle over budget::{msg}")
    return 1 if (a.enforce and over) else 0


if __name__ == "__main__":
    sys.exit(main())
