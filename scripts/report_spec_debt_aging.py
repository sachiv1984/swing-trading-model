#!/usr/bin/env python3
"""
Spec debt aging report (ST-54, BLG-GOV-191, EPIC-07, v9.14).

Lists every open `BLG-SPEC-*` item in claude/backlog/backlog.md by the number
of release cycles it has been available to Release Planning without being
given a story, the measure release_planning_prompt.md §1.1 (Backlog Age
Advisory) warns on at 2 or more.

Per-item ready-pool membership is not recorded anywhere, so "available" is
read as: a release cycle (a claude/cycles/<date>__release-v<x.y> folder)
whose date is on or after the item's filing date. A cycle counts as
"seated" when its stage4_backlog_slice.md (or an amended slice) has a story
whose **Source:** line names the item. The age is the number of such cycles
since the most recent seated one (or since filing, if never seated).

  - Filing date: the last YYYY-MM-DD on the item's **Source:** line. An item
    with no date there is listed as undated and not aged (§1.1: "skip
    silently" when an item cannot be dated reliably).
  - An item with a **Gate criteria:** other than "None" is flagged gated: it
    was probably not in the ready pool, so its age overstates §1.1's measure.
  - An item bannered "✅ COMPLETE" is not open and is skipped.

Usage: python3 scripts/report_spec_debt_aging.py [--threshold N]
Prints a Markdown table, oldest first. Always exits 0 (a report, not a gate).
"""
import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BACKLOG = REPO / "claude" / "backlog" / "backlog.md"
CYCLES = REPO / "claude" / "cycles"

ITEM_HEADING = re.compile(r"^### (BLG-[A-Z]+-\d+)\b(.*)$", re.MULTILINE)
CYCLE_DIR = re.compile(r"^(\d{4}-\d{2}-\d{2})__release-(v\d+\.\d+)$")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def open_spec_items(backlog_text: str) -> list:
    """[{id, title, filed, gated}] for each open BLG-SPEC item, in file order."""
    headings = list(ITEM_HEADING.finditer(backlog_text))
    items = []
    for i, h in enumerate(headings):
        item_id = h.group(1)
        if not item_id.startswith("BLG-SPEC-"):
            continue
        body = backlog_text[h.end():headings[i + 1].start() if i + 1 < len(headings) else len(backlog_text)]
        title = h.group(2).strip().lstrip("—").strip()
        if "✅ COMPLETE" in title or "✅ COMPLETE" in body.split("\n**Problem**")[0]:
            continue
        source = re.search(r"^\*\*Source:\*\*(.*)$", body, re.MULTILINE)
        dates = DATE.findall(source.group(1)) if source else []
        gate = re.search(r"^\*\*Gate criteria:\*\*\s*(.*)$", body, re.MULTILINE)
        gated = bool(gate) and not gate.group(1).strip().lower().startswith("none")
        items.append({"id": item_id, "title": title, "filed": dates[-1] if dates else None, "gated": gated})
    return items


def release_cycles(cycles_dir: Path) -> list:
    """[{date, version, sources}] for each release cycle folder, oldest first."""
    cycles = []
    for d in sorted(cycles_dir.iterdir()):
        m = CYCLE_DIR.match(d.name)
        if not m or not d.is_dir():
            continue
        slices = [d / "stage4_backlog_slice.md"] + sorted(d.glob("amendments/*/amended_backlog_slice.md"))
        text = "\n".join(p.read_text(encoding="utf-8") for p in slices if p.exists())
        sources = set(re.findall(r"BLG-SPEC-\d+\b", "\n".join(re.findall(r"^\*\*Source:\*\*.*$", text, re.MULTILINE))))
        cycles.append({"date": m.group(1), "version": m.group(2), "sources": sources})
    return cycles


def age_items(items: list, cycles: list) -> list:
    """Add cycles_unseated and last_seated to each dated item."""
    for item in items:
        item["cycles_unseated"], item["last_seated"] = None, None
        if not item["filed"]:
            continue
        age = 0
        for cycle in cycles:
            if cycle["date"] < item["filed"]:
                continue
            if item["id"] in cycle["sources"]:
                age, item["last_seated"] = 0, cycle["version"]
            else:
                age += 1
        item["cycles_unseated"] = age
    return items


def render(items: list, threshold: int) -> str:
    dated = sorted((i for i in items if i["cycles_unseated"] is not None),
                   key=lambda i: (-i["cycles_unseated"], i["id"]))
    undated = [i for i in items if i["cycles_unseated"] is None]
    flagged = [i for i in dated if i["cycles_unseated"] >= threshold and not i["gated"]]
    lines = [
        f"# Spec debt aging — {len(items)} open BLG-SPEC item(s)",
        "",
        f"§1.1 advisory threshold: {threshold}+ release cycles without a story. "
        f"Ungated items at or over it: {len(flagged)}.",
        "",
        "| Item | Cycles without a story | Filed | Last seated | Gated | Title |",
        "|------|-----------------------:|-------|-------------|-------|-------|",
    ]
    for i in dated:
        mark = " ⚠" if i in flagged else ""
        lines.append(f"| {i['id']} | {i['cycles_unseated']}{mark} | {i['filed']} | {i['last_seated'] or '—'} | "
                     f"{'yes' if i['gated'] else 'no'} | {i['title']} |")
    if undated:
        lines += ["", "Undated (no date on the **Source:** line, not aged): "
                  + ", ".join(i["id"] for i in undated)]
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--threshold", type=int, default=2)
    args = parser.parse_args(argv)
    items = age_items(open_spec_items(BACKLOG.read_text(encoding="utf-8")), release_cycles(CYCLES))
    print(render(items, args.threshold))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
