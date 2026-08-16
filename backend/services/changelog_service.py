"""
Changelog Service (ST-01, EPIC-01, v7.8, BLG-FE-128)

Parses docs/product/changelog.md to serve the most recent release's
"### Changes shipped" entries for the in-app "What's New" panel
(docs/specs/frontend/pages/dashboard.md §6A). Parsed server-side on each
request -- no hardcoded copy in the frontend build, so a new release is
picked up automatically with no manual wiring.
"""

import re
from pathlib import Path
from typing import Optional

CHANGELOG_PATH = Path(__file__).resolve().parent.parent.parent / "docs" / "product" / "changelog.md"
# ST-16 (BLG-OPS-140, EPIC-06, v8.7): if you're changing what file this
# service reads at runtime (or adding a similar runtime-read of a
# non-code file elsewhere), check docs/ops/render_build_deploy_path_filter_audit.md
# first -- Render's deploy path filters (one repo-visible, one
# dashboard-only) can silently skip a redeploy for a file outside their
# watch paths, with no signal visible anywhere in this repo.

_VERSION_HEADING_RE = re.compile(r"^## (v\S+) — (.+)$", re.MULTILINE)
_CHANGES_SHIPPED_RE = re.compile(r"^### Changes shipped\s*\n(.*?)(?=\n##|\Z)", re.MULTILINE | re.DOTALL)
# ST-13 (BLG-FE-161, EPIC-03, v8.8): the table now carries a 4th column,
# `User Impact` (3rd cell), inserted between `Description` and `Spec
# sections updated` -- see docs/design/2026-08-14__release-v8.8/
# whats-new-user-benefit-copy/decision_record.md. This regex requires all
# 4 cells to be present, so a pre-v8.8 3-column table row (no `User
# Impact` column at all) simply does not match -- it degrades to "no
# changes" for that release rather than raising, consistent with the
# decision record treating the column as additive/forward-only, not
# retrofitted onto every historical row.
_TABLE_ROW_RE = re.compile(r"^\|\s*(EPIC-\d+)\s*\|\s*.+?\s*\|\s*(.+?)\s*\|.*\|$", re.MULTILINE)
_EMPTY_CELL_VALUES = {"", "-", "—"}


def get_latest_changelog_entry() -> Optional[dict]:
    """
    Return the most recent version's changelog summary, or None if
    docs/product/changelog.md is missing, has no parseable version
    heading, has no "### Changes shipped" table for that version, or
    that table has no row with a populated `User Impact` cell.

    Returns {"version": "vX.Y", "changes": [<user impact copy>, ...]}.
    `version` is the bare version number only (per the UX spec's "What's
    New — v{X.Y}" title format -- the title/date portion of the
    changelog heading is not surfaced). `changes` contains only the
    `User Impact` column (not `Description`, EPIC ID, or spec sections)
    per the UX spec (dashboard.md §6A v3.3) -- `Description` remains the
    engineering record and is never surfaced here. A row with an empty
    or `—` `User Impact` cell is excluded entirely: this is the
    mechanism behind "an EPIC with no user-facing change does not appear
    in the What's New feed."
    """
    if not CHANGELOG_PATH.exists():
        return None

    text = CHANGELOG_PATH.read_text()
    headings = list(_VERSION_HEADING_RE.finditer(text))
    if not headings:
        return None

    latest = headings[0]
    start = latest.end()
    end = headings[1].start() if len(headings) > 1 else len(text)
    section_text = text[start:end]

    changes_match = _CHANGES_SHIPPED_RE.search(section_text)
    if not changes_match:
        return None

    user_impacts = []
    for m in _TABLE_ROW_RE.finditer(changes_match.group(1)):
        epic_id, user_impact = m.group(1), m.group(2)
        if set(epic_id) <= {"-"} or user_impact.strip() in _EMPTY_CELL_VALUES:
            continue  # markdown separator row, or no user-facing change for this EPIC
        user_impacts.append(user_impact)

    if not user_impacts:
        return None

    return {"version": latest.group(1), "changes": user_impacts}
