#!/usr/bin/env python3
"""
Backend test coverage report generator (ST-22, BLG-QA-84, EPIC-04, v9.0).

Renders a Markdown coverage summary from one or two `coverage.py` JSON
reports (produced by `pytest --cov-report=json:<path>`), for posting as a
PR comment. Matches the update-or-create PR-comment pattern already used
by `.github/workflows/endpoint-coverage.yml` (a different, endpoint-mapping
kind of coverage — this one is pytest-cov line coverage of `backend/`).

Usage:
    python3 scripts/generate_backend_coverage_report.py --head coverage_head.json [--base coverage_base.json]
"""
import argparse
import json
import sys
from pathlib import Path

MARKER = "Backend Test Coverage Report"


def _load(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _module_rows(data: dict) -> list:
    """One row per top-level backend/ subpackage (services/routers/utils/
    models/database.py/main.py), aggregated from the per-file totals —
    a full per-file table would be too long for a PR comment."""
    groups = {}
    for file_path, info in data.get("files", {}).items():
        parts = Path(file_path).parts
        # file_path is relative to repo root, e.g. "backend/services/foo.py"
        if len(parts) >= 3 and parts[0] == "backend" and parts[1] in ("services", "routers", "utils", "models"):
            group = parts[1]
        elif len(parts) >= 2 and parts[0] == "backend":
            group = parts[1]  # e.g. "database.py", "main.py" as their own group
        else:
            group = "other"
        s = info["summary"]
        g = groups.setdefault(group, {"covered": 0, "statements": 0})
        g["covered"] += s["covered_lines"]
        g["statements"] += s["num_statements"]

    rows = []
    for group, g in sorted(groups.items()):
        pct = round(g["covered"] / g["statements"] * 100, 1) if g["statements"] else 0.0
        rows.append((group, g["covered"], g["statements"], pct))
    return rows


def generate_report(head_data: dict, base_data: dict = None) -> str:
    head_totals = head_data["totals"]
    head_pct = round(head_totals["percent_covered"], 1)

    lines = [
        f"## {MARKER}",
        "",
        f"**Total coverage:** {head_pct}% ({head_totals['covered_lines']}/{head_totals['num_statements']} statements)",
    ]

    if base_data is not None:
        base_totals = base_data["totals"]
        base_pct = round(base_totals["percent_covered"], 1)
        delta = round(head_pct - base_pct, 1)
        arrow = "📈" if delta > 0 else ("📉" if delta < 0 else "➡️")
        sign = "+" if delta > 0 else ""
        lines.append(f"**Delta vs base branch:** {sign}{delta}pp {arrow} (base: {base_pct}%)")
    else:
        lines.append("**Delta vs base branch:** not available this run (base coverage could not be computed)")

    lines += [
        "",
        "| Package | Covered | Statements | Coverage |",
        "|---------|---------|------------|----------|",
    ]
    for group, covered, statements, pct in _module_rows(head_data):
        lines.append(f"| `backend/{group}` | {covered} | {statements} | {pct}% |")

    lines += [
        "",
        "> **Advisory only** — this report never blocks merge, same convention as "
        "`endpoint-coverage.yml`'s Endpoint Coverage Report. Generated from "
        "`pytest --cov` against `tests/` (excluding `tests/e2e/`).",
    ]

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--head", required=True, help="Path to the PR head's coverage.json")
    parser.add_argument("--base", default=None, help="Path to the base branch's coverage.json (optional)")
    parser.add_argument("--out", default="coverage_report.md", help="Output Markdown file path")
    args = parser.parse_args()

    head_data = _load(args.head)
    base_data = _load(args.base) if args.base and Path(args.base).exists() else None

    report = generate_report(head_data, base_data)
    print(report)
    Path(args.out).write_text(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
