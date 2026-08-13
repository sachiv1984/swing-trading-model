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
_TABLE_ROW_RE = re.compile(r"^\|\s*(EPIC-\d+)\s*\|\s*(.+?)\s*\|.*\|$", re.MULTILINE)


def get_latest_changelog_entry() -> Optional[dict]:
    """
    Return the most recent version's changelog summary, or None if
    docs/product/changelog.md is missing, has no parseable version
    heading, or has no "### Changes shipped" table for that version.

    Returns {"version": "vX.Y", "changes": [<description>, ...]}. `version`
    is the bare version number only (per the UX spec's "What's New — v{X.Y}"
    title format -- the title/date portion of the changelog heading is not
    surfaced). `changes` contains only the Description column (not EPIC ID
    or spec sections) per the UX spec -- those are internal governance
    references, not user-facing copy.
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

    descriptions = []
    for m in _TABLE_ROW_RE.finditer(changes_match.group(1)):
        epic_id, desc = m.group(1), m.group(2)
        if set(epic_id) <= {"-"} or set(desc) <= {"-"}:
            continue  # markdown separator row
        descriptions.append(desc)

    if not descriptions:
        return None

    return {"version": latest.group(1), "changes": descriptions}
