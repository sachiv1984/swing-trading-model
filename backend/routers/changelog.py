"""
Changelog Router (ST-01, EPIC-01, v7.8, BLG-FE-128)

GET /changelog/latest — most recent release's changelog summary, for the
in-app "What's New" panel (docs/specs/frontend/pages/dashboard.md §6A).

Contract: docs/specs/api_contracts/changelog_endpoints.md
"""

from fastapi import APIRouter

from services.changelog_service import get_latest_changelog_entry

router = APIRouter(prefix="/changelog", tags=["Changelog"])


@router.get("/latest")
def get_latest():
    """
    Return the most recent release's version label and changes-shipped
    descriptions, parsed server-side from docs/product/changelog.md.
    Returns `data: null` if no parseable version section exists (frontend
    renders the DataState empty branch).
    """
    entry = get_latest_changelog_entry()
    return {"status": "ok", "data": entry}
