"""
AI Spend Trend Service (ST-06, EPIC-06, v7.8, BLG-FEAT-82)

Buckets claude_audit_log.cost_usd by release-cycle date window for the
Settings page's AI spend trend chart (settings.md §6, extends the existing
current-month spend card).

Cycle-boundary source: docs/product/changelog.md's release version headings
(## vX.Y — <title> — <date>) -- NOT claude/cycles/*/state.json as the UX
spec's first-choice suggestion named. That governance-tracking directory is
an internal engineering-process artefact, not guaranteed to be present in
the deployed runtime environment, and coupling a user-facing endpoint to it
would be fragile. The UX spec explicitly allows "an equivalent cycle-boundary
source" -- changelog.md is product-facing, already deployed, and already
carries exactly what's needed: a version label plus a ship date per release.
"""

import re
from pathlib import Path
from typing import Optional

CHANGELOG_PATH = Path(__file__).resolve().parent.parent.parent / "docs" / "product" / "changelog.md"

_VERSION_HEADING_RE = re.compile(
    r"^## (v\S+) — .+ — (\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE
)

MAX_CYCLES = 6


def _parse_changelog_cycles(text: str) -> list[dict]:
    """
    Parse changelog.md for {version, date} pairs, sorted ascending by date
    (oldest first). Returns [] if no parseable version headings exist.

    Same-day releases (real case in this changelog -- e.g. v7.5 and v7.6
    both shipped 2026-07-20) can't be disambiguated by date alone (no
    time-of-day granularity). changelog.md's own convention is strictly
    newest-entry-at-top, so document order is itself a valid finer-grained
    ordering signal: reverse it (oldest-appearing-first) before the stable
    date sort, so a same-day tie resolves in the correct chronological
    order rather than an arbitrary one.
    """
    cycles = []
    for m in _VERSION_HEADING_RE.finditer(text):
        cycles.append({"version": m.group(1), "date": m.group(2)})
    cycles.reverse()
    cycles.sort(key=lambda c: c["date"])
    return cycles


def get_ai_spend_trend() -> list[dict]:
    """
    Return per-release-cycle Claude API spend for the last MAX_CYCLES
    (6) release cycles found in docs/product/changelog.md, oldest to
    newest (matches the chart's left-to-right X-axis ordering).

    Renders whatever cycles exist if fewer than 6 are available -- no
    padding with zero/empty bars (per ux_spec.md §5).

    Returns [] if changelog.md is missing or has no parseable cycles.
    """
    from database import get_claude_spend_between

    if not CHANGELOG_PATH.exists():
        return []

    cycles = _parse_changelog_cycles(CHANGELOG_PATH.read_text())
    if not cycles:
        return []

    recent = cycles[-MAX_CYCLES:]

    trend = []
    for i, cycle in enumerate(recent):
        window_start = cycle["date"]
        window_end: Optional[str] = recent[i + 1]["date"] if i + 1 < len(recent) else None
        spend = get_claude_spend_between(window_start, window_end)
        trend.append({"version": cycle["version"], "spend_usd": round(spend, 2)})

    return trend
