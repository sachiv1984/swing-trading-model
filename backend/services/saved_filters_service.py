"""
Saved Filters Service

Business logic for named, server-side Trade History filter presets
(ST-04, BLG-FE-118, EPIC-04, v7.5).

Distinct from the page's ephemeral, device-local active-filter state
(BLG-FE-40 localStorage-envelope pattern) — these rows persist across
devices/sessions until explicitly deleted.

Contract: docs/specs/api_contracts/saved_filters_endpoints.md
Data model: docs/specs/data_model.md (saved_filters table, migration v2.12->v2.13)
"""

import logging
from typing import Dict, List

from database import get_db

logger = logging.getLogger(__name__)

_NAME_MAX_LENGTH = 100


def ensure_saved_filters_table() -> None:
    """Create the saved_filters table if it does not yet exist (idempotent)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS saved_filters (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
                    name VARCHAR(100) NOT NULL,
                    filter_state JSONB NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    CONSTRAINT uq_saved_filters_portfolio_name UNIQUE (portfolio_id, name)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_saved_filters_portfolio
                    ON saved_filters(portfolio_id)
            """)


def get_saved_filters(portfolio_id: str) -> List[Dict]:
    """Return all saved filter presets for the portfolio, most recently created first."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM saved_filters
                WHERE portfolio_id = %s
                ORDER BY created_at DESC
            """, (portfolio_id,))
            return [_row(r) for r in cur.fetchall()]


def create_saved_filter(portfolio_id: str, data: Dict) -> Dict:
    """
    Create a named filter preset. Raises ValueError (-> 400) on invalid input
    or a duplicate name for this portfolio (UNIQUE (portfolio_id, name)).
    """
    name = (data.get("name") or "").strip()
    filter_state = data.get("filter_state")

    if not name:
        raise ValueError("name is required")
    if len(name) > _NAME_MAX_LENGTH:
        raise ValueError(f"name must be {_NAME_MAX_LENGTH} characters or fewer")
    if not isinstance(filter_state, dict):
        raise ValueError("filter_state is required and must be an object")

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM saved_filters WHERE portfolio_id = %s AND name = %s",
                (portfolio_id, name)
            )
            if cur.fetchone():
                raise ValueError(f"A preset named '{name}' already exists.")

            import json
            cur.execute("""
                INSERT INTO saved_filters (portfolio_id, name, filter_state)
                VALUES (%s, %s, %s::jsonb)
                RETURNING *
            """, (portfolio_id, name, json.dumps(filter_state)))
            return _row(cur.fetchone())


def delete_saved_filter(portfolio_id: str, filter_id: str) -> Dict:
    """Delete a saved filter preset."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM saved_filters WHERE id = %s AND portfolio_id = %s RETURNING id",
                (filter_id, portfolio_id)
            )
            row = cur.fetchone()
            if not row:
                raise LookupError(f"Saved filter {filter_id} not found")
            return {"deleted": True, "id": str(row["id"])}


def _row(r) -> Dict:
    return {
        "id": str(r["id"]),
        "name": r["name"],
        "filter_state": r["filter_state"] if isinstance(r["filter_state"], dict) else {},
        "created_at": r["created_at"].isoformat() if hasattr(r["created_at"], "isoformat") else str(r["created_at"]),
        "updated_at": r["updated_at"].isoformat() if hasattr(r["updated_at"], "isoformat") else str(r["updated_at"]),
    }
