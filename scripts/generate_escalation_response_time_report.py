#!/usr/bin/env python3
"""Cross-role escalation response-time tracker (ST-18, EPIC-05, v9.4, BLG-GOV-301).

Scans every escalations.md-family file across all cycles
(execution_escalations.md, escalations.md, verification_escalations.md,
closure_escalations.md), extracts each entry's Raised at / Owning
authority / Disposition fields per shared_standards.md §4's format, and
aggregates response outcomes by role.

This is a manually-run reporting script, not a scheduled job — re-run it
and refresh docs/governance/escalation_response_time_tracker.md's table
whenever an up-to-date view is needed (e.g. before a PMO Lead workload
review). See that document's Methodology section for the known data-
quality limitations this script works around and cannot fully resolve
(pre-shared_standards.md-era files use inconsistent field names; most
resolution dates are date-only, not full timestamps, so sub-day response
times cannot be measured precisely).
"""
import re
import glob
import sys
from collections import defaultdict
from datetime import datetime, timezone

FILE_GLOBS = [
    "claude/cycles/*/execution_escalations.md",
    "claude/cycles/*/escalations.md",
    "claude/cycles/*/verification_escalations.md",
    "claude/cycles/*/closure_escalations.md",
]

DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def split_authorities(text):
    """Split an 'Owning authority' field on ';' or ' and ' -- but only at
    paren-depth 0, so a parenthetical qualifier's own prose (which may
    itself contain 'and'/';', e.g. "Product Owner (co-consulted: X, per
    Y's dual ownership and Z's note)") is never torn into fake extra
    "roles". Trailing parenthetical qualifiers are then stripped from
    each resulting piece."""
    parts = []
    depth = 0
    buf = ""
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "(":
            depth += 1
            buf += ch
        elif ch == ")":
            depth = max(0, depth - 1)
            buf += ch
        elif depth == 0 and ch == ";":
            parts.append(buf)
            buf = ""
        elif depth == 0 and text[i:i + 5] == " and ":
            parts.append(buf)
            buf = ""
            i += 4  # skip the matched " and " (minus the char consumed by the loop's own increment)
        else:
            buf += ch
        i += 1
    parts.append(buf)
    # [^)]* (not .*?) so this only ever strips ONE self-contained trailing
    # parenthetical, never backtracks across an intervening ")...(" to eat
    # a second, unrelated paren group (and whatever un-parenthesised text,
    # e.g. a second role name, sits between them) along with it.
    return [re.sub(r"\s*\([^)]*\)\s*$", "", p).strip().rstrip(".") for p in parts if p.strip()]


def extract_rows(files):
    rows = []
    for path in files:
        text = open(path, encoding="utf-8").read()
        blocks = re.split(r"^## (ESC-[A-Za-z0-9-]+)", text, flags=re.M)
        for i in range(1, len(blocks), 2):
            esc_id = blocks[i]
            content = blocks[i + 1]
            raised_m = re.search(r"Raised at:\**\s*([0-9T:Z\-]+)", content)
            auth_m = re.search(r"Owning authority:\**\s*(.+)", content)
            disp_m = re.search(r"Disposition:\**\s*(\S+)", content)
            if not raised_m or not auth_m or not disp_m:
                continue  # pre-shared_standards.md-era entry, or non-conforming field names
            try:
                raised_dt = datetime.fromisoformat(raised_m.group(1).replace("Z", "+00:00"))
            except ValueError:
                continue
            disposition = disp_m.group(1)
            after_disp = content[disp_m.end():]
            res_section = re.search(r"Resolution(?: summary)?:\**\s*(.*)", after_disp)
            search_text = res_section.group(1) if res_section else after_disp
            d = DATE_RE.search(search_text[:400])
            resolved_date = d.group(1) if (disposition == "Resolved" and d) else None
            authorities = split_authorities(auth_m.group(1))
            rows.append({
                "file": path, "id": esc_id, "raised": raised_dt,
                "authorities": authorities, "disposition": disposition,
                "resolved_date": resolved_date,
            })
    return rows


def aggregate(rows):
    by_role = defaultdict(lambda: {"total": 0, "resolved_dated": 0, "same_day": 0,
                                    "multi_day": [], "open": 0})
    for r in rows:
        for role in r["authorities"]:
            b = by_role[role]
            b["total"] += 1
            if r["disposition"] == "Open":
                b["open"] += 1
            if r["resolved_date"]:
                resolved_dt = datetime.fromisoformat(r["resolved_date"] + "T00:00:00+00:00")
                delta_days = (resolved_dt - r["raised"].astimezone(timezone.utc)).total_seconds() / 86400
                if 0 <= delta_days <= 400:  # guard against parse noise / clearly-wrong dates
                    b["resolved_dated"] += 1
                    if delta_days < 1:
                        b["same_day"] += 1
                    else:
                        b["multi_day"].append(round(delta_days, 1))
    return by_role


def render_markdown(files, rows, by_role):
    total_resolved_dated = sum(1 for r in rows if r["resolved_date"])
    lines = []
    lines.append(f"_Scanned {len(files)} files, {len(rows)} structured entries parsed, "
                  f"{total_resolved_dated} with an extractable resolution date "
                  f"({round(100 * total_resolved_dated / len(rows)) if rows else 0}% coverage)._")
    lines.append("")
    lines.append("| Role | Total | Resolved (dated) | Same-day | Multi-day avg | Still open |")
    lines.append("|------|------:|------------------:|---------:|---------------:|-----------:|")
    for role, d in sorted(by_role.items(), key=lambda kv: -kv[1]["total"]):
        md = round(sum(d["multi_day"]) / len(d["multi_day"]), 1) if d["multi_day"] else "—"
        lines.append(f"| {role} | {d['total']} | {d['resolved_dated']} | {d['same_day']} | {md} | {d['open']} |")
    return "\n".join(lines)


if __name__ == "__main__":
    files = sorted(sum((glob.glob(g) for g in FILE_GLOBS), []))
    rows = extract_rows(files)
    by_role = aggregate(rows)
    print(render_markdown(files, rows, by_role))
