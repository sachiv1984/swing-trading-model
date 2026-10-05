#!/usr/bin/env python3
"""
Reproduce roadmap_prompt.md STEP 2.4 (Product Value Ratio Diagnostic) and
STEP 7.1 (Skill-Silo Alert "Governance story %") from docs/product/changelog.md's
own inline [U|G|D|P] tags (ST-25, EPIC-04, v9.9, BLG-GOV-352).

Each released version's "### Tech backlog items shipped" section carries one
bullet per shipped story, e.g.:

    - [ST-01] [U] Formatting-helper migration completed across all 70 ...

This script walks the changelog's "## vX.Y" sections newest-first, reads the
[U|G|D|P] tag off each bullet, and reproduces:

- STEP 2.4: user_value_ratio = U stories / total stories, over the last
  --pvr-window (default 5) cycles.
- STEP 7.1: governance_pct = (G + D + P) / total * 100, over the last
  --silo-window (default 3) cycles.

STEP 7.2 (Cross-Role Workload Balance) is a *different* input (sprint_backlog.md
`**Owner:**` fields, not changelog tags) and is already covered by
`scripts/compute_role_share_history.py` — this script does not duplicate it.

This is an optional acceleration, not a hard dependency: roadmap_prompt.md's
own STEP 2.4/7.1 text remains the authoritative procedure if this script and
the changelog ever disagree (e.g. a cycle shipped before the [U|G|D|P] tagging
convention existed, pre-v6.6 — those cycles are silently skipped since they
have no tagged bullets to read).

Usage:
    python3 scripts/compute_rebalance_diagnostics.py docs/product/changelog.md
    python3 scripts/compute_rebalance_diagnostics.py docs/product/changelog.md --json
    python3 scripts/compute_rebalance_diagnostics.py docs/product/changelog.md \\
        --pvr-window 5 --silo-window 3
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

VERSION_HEADER_RE = re.compile(r"^##\s+v[\w.]+.*$", re.M)
CYCLE_RE = re.compile(r"^Cycle:\s*(.+?)\s*$", re.M)
TAGGED_BULLET_RE = re.compile(r"^- \[ST-\d+[a-z]?\]\s*\[([UGDP])\]", re.M)


def parse_cycles(text: str):
    """Return a list of {cycle, tags: Counter} dicts, newest cycle first."""
    headers = list(VERSION_HEADER_RE.finditer(text))
    cycles = []
    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]
        cycle_m = CYCLE_RE.search(block)
        cycle_id = cycle_m.group(1) if cycle_m else m.group(0).strip()
        tags = Counter(TAGGED_BULLET_RE.findall(block))
        if sum(tags.values()) > 0:
            cycles.append({"cycle": cycle_id, "tags": tags})
    return cycles


def window_totals(cycles, window: int):
    selected = cycles[:window]
    total = Counter()
    for c in selected:
        total.update(c["tags"])
    return selected, total


def pvr_diagnostic(cycles, window: int):
    selected, total = window_totals(cycles, window)
    n = sum(total.values())
    ratio = round(total["U"] / n, 3) if n else None
    if ratio is not None:
        tier = "Healthy" if ratio >= 0.50 else ("Advisory" if ratio >= 0.30 else "Product Value Alert")
    else:
        tier = None
    return {
        "window_cycles": [c["cycle"] for c in selected],
        "U": total["U"], "G": total["G"], "D": total["D"], "P": total["P"],
        "total": n,
        "user_value_ratio": ratio,
        "tier": tier,
    }


def skill_silo_diagnostic(cycles, window: int):
    selected, total = window_totals(cycles, window)
    n = sum(total.values())
    governance = total["G"] + total["D"] + total["P"]
    pct = round(100 * governance / n, 1) if n else None
    alert = pct is not None and pct > 40
    return {
        "window_cycles": [c["cycle"] for c in selected],
        "U": total["U"], "G": total["G"], "D": total["D"], "P": total["P"],
        "total": n,
        "governance_pct": pct,
        "skill_silo_alert": alert,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("changelog", type=Path, help="Path to docs/product/changelog.md")
    parser.add_argument("--pvr-window", type=int, default=5, help="Cycles for STEP 2.4 (default 5)")
    parser.add_argument("--silo-window", type=int, default=3, help="Cycles for STEP 7.1 (default 3)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.changelog.exists():
        print(f"Not found: {args.changelog}", file=sys.stderr)
        return 1

    cycles = parse_cycles(args.changelog.read_text())
    pvr = pvr_diagnostic(cycles, args.pvr_window)
    silo = skill_silo_diagnostic(cycles, args.silo_window)

    if args.json:
        print(json.dumps({"step_2_4_product_value_ratio": pvr, "step_7_1_skill_silo": silo}, indent=2))
    else:
        print(f"=== STEP 2.4 — Product Value Ratio (last {args.pvr_window} cycles) ===")
        print(f"  Window: {', '.join(pvr['window_cycles'])}")
        print(f"  U={pvr['U']} G={pvr['G']} D={pvr['D']} P={pvr['P']} total={pvr['total']}")
        print(f"  user_value_ratio = {pvr['user_value_ratio']} ({pvr['tier']})")
        print()
        print(f"=== STEP 7.1 — Skill-Silo Governance % (last {args.silo_window} cycles) ===")
        print(f"  Window: {', '.join(silo['window_cycles'])}")
        print(f"  U={silo['U']} G={silo['G']} D={silo['D']} P={silo['P']} total={silo['total']}")
        print(f"  governance_pct = {silo['governance_pct']}%" + (" — Skill-Silo Alert (>40%)" if silo['skill_silo_alert'] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
