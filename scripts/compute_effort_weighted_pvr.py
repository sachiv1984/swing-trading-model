#!/usr/bin/env python3
"""
Compute effort-weighted PVR (Product Value Ratio) for the last 5 rolling
shipped-release windows, cross-validated against product_value_ratio_history.md's
already-recorded story-count U/G/D/P breakdown (ST-31, EPIC-06, v9.8, BLG-GOV-339).

Cross-references each shipped story's docs/product/changelog.md U/G/D/P tag
against its own cycle's sprint_backlog.md **Estimated effort:** field, then
sums effort-days per tag per window instead of raw story counts. See
docs/specs/metrics_definitions.md Appendix F, "PVR Measurement Package", for
the full methodology, weight-normalisation table, and disclosed coverage gaps.

Run from the repo root: python3 scripts/compute_effort_weighted_pvr.py
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

REPO = Path(__file__).resolve().parent.parent
CHANGELOG = REPO / "docs/product/changelog.md"

VERSION_TO_FOLDER = {
    "v7.5": "2026-07-17__release-v7.5", "v7.6": "2026-07-20__release-v7.6",
    "v7.7": "2026-07-21__release-v7.7", "v7.8": "2026-07-24__release-v7.8",
    "v7.9": "2026-07-27__release-v7.9",
    "v8.1": "2026-08-03__release-v8.1", "v8.2": "2026-08-04__release-v8.2",
    "v8.3": "2026-08-05__release-v8.3", "v8.4": "2026-08-07__release-v8.4",
    "v8.5": "2026-08-08__release-v8.5", "v8.6": "2026-08-11__release-v8.6",
    "v8.7": "2026-08-12__release-v8.7", "v8.8": "2026-08-14__release-v8.8",
    "v8.9": "2026-08-17__release-v8.9", "v9.0": "2026-08-21__release-v9.0",
    "v9.1": "2026-09-03__release-v9.1", "v9.2": "2026-09-07__release-v9.2",
    "v9.3": "2026-09-09__release-v9.3", "v9.4": "2026-09-14__release-v9.4",
    "v9.5": "2026-09-15__release-v9.5", "v9.6": "2026-09-21__release-v9.6",
    "v9.7": "2026-09-23__release-v9.7",
}

WINDOWS = {
    "v7.5-v7.9": ["v7.5", "v7.6", "v7.7", "v7.8", "v7.9"],
    "v8.1-v8.5": ["v8.1", "v8.2", "v8.3", "v8.4", "v8.5"],
    "v8.9-v9.3": ["v8.9", "v9.0", "v9.1", "v9.2", "v9.3"],
    "v9.1-v9.5": ["v9.1", "v9.2", "v9.3", "v9.4", "v9.5"],
    "v9.3-v9.7": ["v9.3", "v9.4", "v9.5", "v9.6", "v9.7"],
}
RECORDED = {
    "v8.1-v8.5": {"U": 14, "G": 30, "D": 80, "P": 3, "total": 127},
    "v8.9-v9.3": {"U": 16, "G": 48, "D": 110, "P": 0, "total": 174},
    "v9.1-v9.5": {"U": 9, "G": 60, "D": 122, "P": 4, "total": 195},
    "v9.3-v9.7": {"U": 14, "G": 36, "D": 104, "P": 4, "total": 158},
}

BAND_MIDPOINT = {
    "XS": 0.4, "S": 0.75, "M": 1.75, "L": 3.5, "VL": 3.5, "VH": 12.0,
}


def parse_changelog_tags(version: str):
    """Return {ST-ID: tag} for the given version's 'Tech backlog items shipped' list."""
    text = CHANGELOG.read_text()
    heading_re = re.compile(rf"^## {re.escape(version)}\b.*$", re.M)
    m = heading_re.search(text)
    if not m:
        return {}
    next_m = re.search(r"^## v", text[m.end():], re.M)
    end = m.end() + next_m.start() if next_m else len(text)
    section = text[m.end():end]
    tag_re = re.compile(r"^-\s*\[(ST-\d+[a-z]?)\]\s*\[([UGDP])\]", re.M)
    return {sid: tag for sid, tag in tag_re.findall(section)}


def parse_effort_weight(effort_text: str):
    """Convert an **Estimated effort:** value to a numeric day weight."""
    effort_text = effort_text.strip()
    # Direct numeric: "8.00d", "4.0 days", "9.0 days (S+S+S+M+M+M+S)"
    m = re.match(r"^(\d+(?:\.\d+)?)\s*d(?:ays)?\b", effort_text)
    if m:
        return float(m.group(1))
    # Numeric-first, band as a parenthetical annotation: "0.5 (XS)", "4.0 (L)",
    # "9.0 (S+S+S+M+M+M+S)" (a consolidated multi-story batch) — the number
    # itself IS the day estimate here, already unit-less days.
    m2 = re.match(r"^(\d+(?:\.\d+)?)\s*\([^)]*\)\s*$", effort_text)
    if m2:
        return float(m2.group(1))
    # Bare number, no unit, no band annotation: "0.1", "0.75", "0.5"
    m3 = re.match(r"^(\d+(?:\.\d+)?)\s*$", effort_text)
    if m3:
        return float(m3.group(1))
    # Band with parenthetical range: "S (~0.5-1d)" / "M (~1-2d)" / "XS (<1h)"
    band_m = re.match(r"^(XS|VS|S|M|L|VL|VH)\b\s*\(([^)]*)\)", effort_text)
    if band_m:
        band, paren = band_m.group(1), band_m.group(2)
        nums = re.findall(r"(\d+(?:\.\d+)?)", paren)
        if len(nums) >= 2:
            return (float(nums[0]) + float(nums[1])) / 2
        if len(nums) == 1:
            if "<" in paren or "h)" in paren or paren.strip().endswith("h"):
                return 0.15  # sub-day, hour-scale
            return float(nums[0])
        return BAND_MIDPOINT.get(band)
    # Bare band, no parenthetical
    band_m2 = re.match(r"^(XS|VS|S|M|L|VL|VH)\b\s*$", effort_text)
    if band_m2:
        return BAND_MIDPOINT.get(band_m2.group(1))
    return None


def parse_sprint_backlog_efforts(folder: str):
    """Return {ST-ID: weight} for every #### ST-xx block's first Estimated effort line."""
    path = REPO / "claude/cycles" / folder / "sprint_backlog.md"
    if not path.exists():
        return {}, []
    text = path.read_text()
    header_re = re.compile(r"^####\s+(ST-\d+[a-z]?)\b", re.M)
    headers = list(header_re.finditer(text))
    effort_re = re.compile(r"^\*\*Estimated effort:\*\*\s*(.+?)\s*$", re.M)
    results = {}
    unparsed = []
    for i, h in enumerate(headers):
        sid = h.group(1)
        start = h.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]
        em = effort_re.search(block)
        if not em:
            continue
        weight = parse_effort_weight(em.group(1))
        if weight is None:
            unparsed.append((sid, em.group(1)))
        else:
            results[sid] = weight
    return results, unparsed


def main():
    for window_name, versions in WINDOWS.items():
        weighted = defaultdict(float)
        counted = defaultdict(int)
        missing_effort = []
        for v in versions:
            folder = VERSION_TO_FOLDER[v]
            tags = parse_changelog_tags(v)
            efforts, unparsed = parse_sprint_backlog_efforts(folder)
            for sid, tag in tags.items():
                counted[tag] += 1
                counted["total"] += 1
                w = efforts.get(sid)
                if w is None:
                    missing_effort.append((v, sid, tag))
                    continue
                weighted[tag] += w
                weighted["total"] += w

        recorded = RECORDED.get(window_name)
        story_pvr = counted["U"] / counted["total"] if counted["total"] else 0
        weighted_pvr = weighted["U"] / weighted["total"] if weighted["total"] else 0

        print(f"=== {window_name} ===")
        if recorded:
            match = "MATCH" if counted["total"] == recorded["total"] and counted["U"] == recorded["U"] else "MISMATCH"
            print(f"  Reconstructed: U={counted['U']} G={counted['G']} D={counted['D']} P={counted['P']} total={counted['total']}  vs recorded U={recorded['U']} G={recorded['G']} D={recorded['D']} P={recorded['P']} total={recorded['total']}  [{match}]")
        else:
            print(f"  Reconstructed (no recorded breakdown to cross-validate against): U={counted['U']} G={counted['G']} D={counted['D']} P={counted['P']} total={counted['total']}")
        print(f"  Story-count PVR (reconstructed): {story_pvr:.3f}")
        print(f"  Effort-weighted: U={weighted['U']:.2f}d G={weighted['G']:.2f}d D={weighted['D']:.2f}d P={weighted['P']:.2f}d total={weighted['total']:.2f}d")
        print(f"  Effort-weighted PVR: {weighted_pvr:.3f}")
        print(f"  Missing effort lookups: {len(missing_effort)} of {counted['total']}")
        for v, sid, tag in missing_effort[:10]:
            print(f"    {v} {sid} [{tag}]")
        print()


if __name__ == "__main__":
    sys.exit(main())
