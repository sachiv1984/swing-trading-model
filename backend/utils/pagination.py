"""
Cursor-based pagination pattern for list endpoints (ST-17, EPIC-06,
v8.1, BLG-BE-47).

Additive, opt-in only: an endpoint using this helper without a caller-supplied
`cursor`/`limit` continues to behave as before — see the migrated reference
implementation (`GET /trade-plans`) for the exact opt-in shape.

Pattern documented in
docs/specs/api_contracts/backend_engineering_patterns.md (Cursor-based
pagination pattern section).

Keyset (not offset) pagination, ordered by `(created_at DESC, id DESC)`.
Postgres supports row-value comparison directly, so the WHERE fragment
this module builds (`(created_at, id) < (%s, %s)`) is a single indexable
comparison, not an OFFSET scan — this is what makes keyset pagination
scale where OFFSET-based pagination degrades on large tables.
"""
import base64
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


def encode_cursor(created_at: datetime, row_id: str) -> str:
    """Opaque cursor encoding the last row of the current page."""
    raw = f"{created_at.isoformat()}|{row_id}"
    return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("ascii")


def decode_cursor(cursor: str) -> Tuple[datetime, str]:
    """Inverse of encode_cursor. Raises ValueError on a malformed cursor —
    callers should catch this and return a 400, not propagate a 500."""
    raw = base64.urlsafe_b64decode(cursor.encode("ascii")).decode("utf-8")
    created_at_str, row_id = raw.split("|", 1)
    return datetime.fromisoformat(created_at_str), row_id


def cursor_where_clause(
    cursor: Optional[str], created_field: str = "created_at", id_field: str = "id"
) -> Tuple[str, List[Any]]:
    """Returns (sql_fragment, params) to AND onto an existing WHERE clause,
    for keyset pagination ordered by (created_field DESC, id_field DESC).
    Returns ("", []) if cursor is None — the caller's existing query is
    unaffected, preserving the additive/opt-in guarantee."""
    if not cursor:
        return "", []
    created_at, row_id = decode_cursor(cursor)
    return f"({created_field}, {id_field}) < (%s, %s)", [created_at, row_id]


def paginate_results(
    rows: List[Dict[str, Any]],
    limit: int,
    created_field: str = "created_at",
    id_field: str = "id",
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Trims an over-fetched row list (caller must query `limit + 1` rows,
    ordered by (created_field DESC, id_field DESC), applying
    cursor_where_clause's fragment) down to `limit` and computes the
    next-page cursor. Returns (page, next_cursor); next_cursor is None
    when the fetched rows fit within `limit` (no further page)."""
    has_more = len(rows) > limit
    page = rows[:limit]
    next_cursor = None
    if has_more and page:
        last = page[-1]
        next_cursor = encode_cursor(last[created_field], last[id_field])
    return page, next_cursor
