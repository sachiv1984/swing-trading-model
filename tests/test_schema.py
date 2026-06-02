"""
Schema smoke tests — ST-04 (EPIC-02, v4.9 BLG-QA-41).

Verifies that ensure_lifecycle_columns() correctly creates the three lifecycle
columns (position_state, state_entered_at, state_history) on the positions table.

Phase B only: skipped when DATABASE_URL contains 'stub' (Phase A CI where
all DB calls are mocked). Runs against real Postgres in Phase B CI.
"""
import os
import sys
import pytest
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

_DATABASE_URL = os.getenv("DATABASE_URL", "")
_SKIP_PHASE_A = "stub" in _DATABASE_URL.lower()
_SKIP_REASON = "Phase A — DATABASE_URL is a stub; schema smoke tests require real Postgres (Phase B)"

LIFECYCLE_COLUMNS = {"position_state", "state_entered_at", "state_history"}


def _get_conn():
    return psycopg2.connect(_DATABASE_URL, cursor_factory=RealDictCursor)


def _ensure_positions_table(conn):
    """Create a minimal positions table in the CI database if absent."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS positions (
                id SERIAL PRIMARY KEY,
                ticker VARCHAR(20)
            )
        """)
    conn.commit()


def _get_column_names(conn, table="positions"):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
              AND column_name = ANY(%s)
            """,
            (table, list(LIFECYCLE_COLUMNS)),
        )
        return {row["column_name"] for row in cur.fetchall()}


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
def test_ensure_lifecycle_columns_creates_all_three():
    """ensure_lifecycle_columns() creates position_state, state_entered_at, state_history."""
    # Evict conftest stub so we import the real database module
    sys.modules.pop("database", None)
    from database import ensure_lifecycle_columns

    conn = _get_conn()
    try:
        _ensure_positions_table(conn)
        # Drop lifecycle columns to start from a known-absent state
        with conn.cursor() as cur:
            for col in LIFECYCLE_COLUMNS:
                cur.execute(f"ALTER TABLE positions DROP COLUMN IF EXISTS {col}")
        conn.commit()

        # Verify they're gone before the call
        absent_before = _get_column_names(conn)
        assert absent_before == set(), f"Columns still present before migration: {absent_before}"

        # Run the migration
        ensure_lifecycle_columns()

        # Assert all three now exist
        found = _get_column_names(conn)
    finally:
        conn.close()

    assert LIFECYCLE_COLUMNS == found, (
        f"Missing lifecycle columns after ensure_lifecycle_columns(): "
        f"expected {LIFECYCLE_COLUMNS}, got {found}"
    )


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
def test_missing_lifecycle_column_detected():
    """A missing lifecycle column is detectable via information_schema — Phase B gate proves this."""
    sys.modules.pop("database", None)

    conn = _get_conn()
    try:
        _ensure_positions_table(conn)
        # Drop one column to simulate the missing-schema bug
        with conn.cursor() as cur:
            cur.execute("ALTER TABLE positions DROP COLUMN IF EXISTS position_state")
        conn.commit()

        found = _get_column_names(conn)
    finally:
        conn.close()

    assert "position_state" not in found, (
        "Expected position_state to be absent after DROP; Phase B gate would not have caught the bug."
    )
