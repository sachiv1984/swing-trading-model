#!/usr/bin/env python3
"""Arc velocity report generator (ST-29, EPIC-07, v9.16, BLG-GOV-26).

Builds the data section of an arc velocity report for any release range,
from two sources:

* ``claude/cycles/velocity_metrics.md`` Velocity History table
  (Planned / Completed / Velocity per cycle), the canonical story counts.
* Each cycle's ``claude/cycles/<date>__release-vX.Y/execution_state.json``
  for EPIC counts and outcomes.

Usage (Arc 2 example):

    python3 scripts/arc_velocity_report.py --arc "Arc 2" --from v3.1 --to v6.1

Prints Markdown to stdout. With ``--out <file>``, replaces the text between
``<!-- arc-velocity:begin -->`` and ``<!-- arc-velocity:end -->`` in that
file instead, so the report's narrative sections are kept on re-run.

Metric definitions (also stated in the generated output):

* Stories/cycle: Planned and Completed from velocity_metrics.md.
* Velocity: Completed / Planned per cycle (velocity_metrics.md definition).
* Arc velocity: sum(Completed) / sum(Planned) over the arc (story-weighted).
* EPIC completion rate: EPICs with status ``merged`` or ``done`` divided by
  EPICs in sprint scope. EPICs with status ``deferred_at_planning`` were never
  in sprint scope and are excluded from the denominator.
* Rolling velocity: mean of the per-cycle velocity over the trailing
  ``--window`` cycles (default 6, matching velocity_metrics.md).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import statistics
import sys

BEGIN = "<!-- arc-velocity:begin -->"
END = "<!-- arc-velocity:end -->"
COMPLETED_EPIC = {"merged", "done"}
OUT_OF_SCOPE_EPIC = {"deferred_at_planning"}

_ROW = re.compile(
    r"^\|\s*(v\d+\.\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([0-9.]+)\s*\|"
)


def version_key(v: str) -> tuple[int, int]:
    major, minor = v.lstrip("v").split(".")
    return int(major), int(minor)


def parse_velocity_table(text: str) -> dict[str, dict]:
    """Return {version: {planned, completed, velocity}} from the history table."""
    rows: dict[str, dict] = {}
    for line in text.splitlines():
        m = _ROW.match(line)
        if m:
            v, planned, completed, vel = m.groups()
            rows[v] = {
                "planned": int(planned),
                "completed": int(completed),
                "velocity": float(vel),
            }
    return rows


def find_cycle_dirs(cycles_dir: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in glob.glob(os.path.join(cycles_dir, "*__release-v*")):
        m = re.search(r"__release-(v\d+\.\d+)$", path.rstrip("/"))
        if m and os.path.isdir(path):
            out[m.group(1)] = path
    return out


def epic_counts(execution_state: dict) -> dict:
    epics = execution_state.get("epics") or {}
    in_scope = completed = deferred = 0
    other: list[str] = []
    for epic_id, epic in epics.items():
        status = (epic or {}).get("status")
        if status in OUT_OF_SCOPE_EPIC:
            deferred += 1
            continue
        in_scope += 1
        if status in COMPLETED_EPIC:
            completed += 1
        else:
            other.append(f"{epic_id}: {status}")
    return {
        "in_scope": in_scope,
        "completed": completed,
        "deferred_at_planning": deferred,
        "not_completed": sorted(other),
    }


def select_range(versions, start: str, end: str) -> list[str]:
    lo, hi = version_key(start), version_key(end)
    return sorted((v for v in versions if lo <= version_key(v) <= hi), key=version_key)


def build_rows(velocity: dict, cycle_dirs: dict, start: str, end: str):
    rows = []
    missing = []
    for v in select_range(set(velocity) | set(cycle_dirs), start, end):
        vel = velocity.get(v)
        epics = None
        cdir = cycle_dirs.get(v)
        if cdir:
            es_path = os.path.join(cdir, "execution_state.json")
            if os.path.exists(es_path):
                with open(es_path, encoding="utf-8") as fh:
                    epics = epic_counts(json.load(fh))
        if vel is None or epics is None:
            missing.append(
                f"{v}: "
                + ", ".join(
                    x
                    for x, absent in (
                        ("no velocity_metrics.md row", vel is None),
                        ("no execution_state.json", epics is None),
                    )
                    if absent
                )
            )
            continue
        rows.append({"version": v, **vel, "epics": epics})
    return rows, missing


def summarise(rows: list[dict], window: int) -> dict:
    planned = sum(r["planned"] for r in rows)
    completed = sum(r["completed"] for r in rows)
    vels = [r["velocity"] for r in rows]
    ep_in = sum(r["epics"]["in_scope"] for r in rows)
    ep_done = sum(r["epics"]["completed"] for r in rows)
    rolling = []
    for i in range(len(rows)):
        if i + 1 >= window:
            win = vels[i + 1 - window : i + 1]
            rolling.append((rows[i]["version"], sum(win) / window))
    below = [r for r in rows if r["velocity"] < 1.0]
    return {
        "cycles": len(rows),
        "planned": planned,
        "completed": completed,
        "arc_velocity": (completed / planned) if planned else 0.0,
        "mean_cycle_velocity": statistics.mean(vels) if vels else 0.0,
        "stories_per_cycle_mean": (completed / len(rows)) if rows else 0.0,
        "stories_per_cycle_median": statistics.median(r["completed"] for r in rows) if rows else 0,
        "stories_per_cycle_min": min((r["completed"] for r in rows), default=0),
        "stories_per_cycle_max": max((r["completed"] for r in rows), default=0),
        "epics_in_scope": ep_in,
        "epics_completed": ep_done,
        "epic_completion_rate": (ep_done / ep_in) if ep_in else 0.0,
        "epics_deferred_at_planning": sum(r["epics"]["deferred_at_planning"] for r in rows),
        "rolling": rolling,
        "rolling_min": min(rolling, key=lambda x: x[1]) if rolling else None,
        "below_full": below,
        "window": window,
    }


def render(arc: str, start: str, end: str, rows, missing, s) -> str:
    L = []
    L.append(f"### {arc} summary ({start}–{end})")
    L.append("")
    L.append("| Measure | Value |")
    L.append("|---------|-------|")
    L.append(f"| Cycles | {s['cycles']} |")
    L.append(f"| Stories planned / completed | {s['planned']} / {s['completed']} |")
    L.append(f"| Arc velocity (story-weighted) | {s['arc_velocity']:.3f} |")
    L.append(f"| Mean per-cycle velocity | {s['mean_cycle_velocity']:.3f} |")
    L.append(
        f"| Stories completed per cycle | mean {s['stories_per_cycle_mean']:.1f}, "
        f"median {s['stories_per_cycle_median']:g}, range {s['stories_per_cycle_min']}–{s['stories_per_cycle_max']} |"
    )
    L.append(
        f"| EPIC completion rate | {s['epics_completed']} / {s['epics_in_scope']} = {s['epic_completion_rate']:.3f} |"
    )
    L.append(f"| EPICs deferred at planning (excluded) | {s['epics_deferred_at_planning']} |")
    L.append(f"| Cycles below velocity 1.00 | {len(s['below_full'])} of {s['cycles']} |")
    if s["rolling_min"]:
        v, val = s["rolling_min"]
        L.append(f"| Lowest {s['window']}-cycle rolling velocity | {val:.3f} (window ending {v}) |")
        L.append(f"| Rolling velocity at arc close | {s['rolling'][-1][1]:.3f} (window ending {s['rolling'][-1][0]}) |")
    L.append("")
    L.append(f"### {arc} per-cycle detail")
    L.append("")
    L.append(f"| Cycle | Planned | Completed | Velocity | {s['window']}-cycle rolling | EPICs completed / in scope | Not completed |")
    L.append("|-------|---------|-----------|----------|-------------|-----------------|---------------|")
    roll = dict(s["rolling"])
    for r in rows:
        e = r["epics"]
        rv = f"{roll[r['version']]:.3f}" if r["version"] in roll else "—"
        extra = "; ".join(e["not_completed"]) or "—"
        if e["deferred_at_planning"]:
            extra = (extra if extra != "—" else "") + (
                ("; " if extra != "—" else "") + f"{e['deferred_at_planning']} deferred at planning"
            )
        L.append(
            f"| {r['version']} | {r['planned']} | {r['completed']} | {r['velocity']:.2f} | {rv} | "
            f"{e['completed']} / {e['in_scope']} | {extra} |"
        )
    if missing:
        L.append("")
        L.append("**Cycles in range with missing inputs (excluded):** " + "; ".join(missing))
    return "\n".join(L) + "\n"


def write_between_markers(path: str, body: str) -> None:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise SystemExit(f"{path}: expected exactly one {BEGIN} and one {END} marker")
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + BEGIN + "\n" + body + END + tail)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--arc", required=True, help='Arc label, e.g. "Arc 2"')
    ap.add_argument("--from", dest="start", required=True, help="First release, e.g. v3.1")
    ap.add_argument("--to", dest="end", required=True, help="Last release, e.g. v6.1")
    ap.add_argument("--velocity-file", default="claude/cycles/velocity_metrics.md")
    ap.add_argument("--cycles-dir", default="claude/cycles")
    ap.add_argument("--window", type=int, default=6)
    ap.add_argument("--out", help="Report file to update between the arc-velocity markers")
    args = ap.parse_args(argv)

    with open(args.velocity_file, encoding="utf-8") as fh:
        velocity = parse_velocity_table(fh.read())
    rows, missing = build_rows(velocity, find_cycle_dirs(args.cycles_dir), args.start, args.end)
    if not rows:
        print(f"No cycles found in {args.start}–{args.end}", file=sys.stderr)
        return 1
    body = render(args.arc, args.start, args.end, rows, missing, summarise(rows, args.window))
    if args.out:
        write_between_markers(args.out, body)
    else:
        sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
