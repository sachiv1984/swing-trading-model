"""
Real-Postgres validation of `get_claude_endpoint_cost_windows()` — ST-18
(EPIC-04, v9.7, BLG-QA-177).

No test in the repo previously executed this function's actual SQL: it uses
Postgres-only constructs (`FILTER (WHERE ...)`, `(%(param)s || ' hours')::interval`,
`NOW()`) that cannot be reproduced against SQLite, so a synthetic-dialect proxy
(the pattern used elsewhere for e.g. `test_positions_open_ticker_entry_date_unique_migration.py`)
is not viable here — it would test a reimplementation, not the real query.

Phase B only: skipped when DATABASE_URL contains 'stub' (Phase A CI where all
DB calls are mocked). Runs against real Postgres in Phase B CI (see
`.github/workflows/ci-tests.yml`'s `pytest-phase-b` job) and can also be run
locally against any real Postgres instance.
"""
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psycopg2
import pytest
from psycopg2.extras import RealDictCursor

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

_DATABASE_URL = os.getenv("DATABASE_URL", "")
_SKIP_PHASE_A = "stub" in _DATABASE_URL.lower()
_SKIP_REASON = "Phase A — DATABASE_URL is a stub; requires real Postgres (Phase B)"

_TEST_ENDPOINT = "__st18_test_endpoint__"


def _get_conn():
    return psycopg2.connect(_DATABASE_URL, cursor_factory=RealDictCursor)


def _clean(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM claude_audit_log WHERE endpoint = %s", (_TEST_ENDPOINT,))
    conn.commit()


def _insert_row(conn, generated_at, cost_usd):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO claude_audit_log
                (endpoint, model_id, prompt_version, input_tokens, output_tokens, cost_usd, generated_at)
            VALUES (%s, 'test-model', 'v1', 10, 10, %s, %s)
            """,
            (_TEST_ENDPOINT, cost_usd, generated_at),
        )
    conn.commit()


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
def test_get_claude_endpoint_cost_windows_boundaries():
    """Real (non-stubbed) get_claude_endpoint_cost_windows() correctly separates
    recent (last 24h) from baseline (the 7 days immediately preceding, excluding
    recent) and excludes rows entirely outside both windows."""
    sys.modules.pop("database", None)
    from database import ensure_claude_audit_log_table, get_claude_endpoint_cost_windows

    conn = _get_conn()
    try:
        ensure_claude_audit_log_table()
        _clean(conn)

        now = datetime.now(timezone.utc)

        # Recent window (< 24h ago): 2 rows, costs 1.00 and 3.00 -> avg 2.00
        _insert_row(conn, now - timedelta(hours=1), 1.00)
        _insert_row(conn, now - timedelta(hours=2), 3.00)

        # Baseline window (>= 24h ago and < 24h + 7d ago): 2 rows, costs 0.50 and 1.50 -> avg 1.00
        _insert_row(conn, now - timedelta(hours=25), 0.50)
        _insert_row(conn, now - timedelta(days=5), 1.50)

        # Outside both windows entirely (> 24h + 7d ago): must not appear in either bucket
        _insert_row(conn, now - timedelta(days=10), 999.00)

        results = get_claude_endpoint_cost_windows(recent_hours=24, baseline_days=7)
    finally:
        _clean(conn)
        conn.close()

    matches = [r for r in results if r["endpoint"] == _TEST_ENDPOINT]
    assert len(matches) == 1, (
        f"Expected exactly one row for {_TEST_ENDPOINT!r}, got {matches!r} "
        f"(get_claude_endpoint_cost_windows returned {results!r} — an empty/missing "
        f"result here likely means the function's bare `except Exception: return []` "
        f"swallowed a real error; check the query executes against this schema)"
    )
    row = matches[0]

    assert row["recent_count"] == 2, row
    assert row["recent_avg_cost_usd"] == pytest.approx(2.00), row

    assert row["baseline_count"] == 2, row
    assert row["baseline_avg_cost_usd"] == pytest.approx(1.00), row


@pytest.mark.skipif(_SKIP_PHASE_A, reason=_SKIP_REASON)
def test_get_claude_endpoint_cost_windows_empty_when_no_rows():
    """No rows for an endpoint -> COALESCE defaults apply (0.0 avg, 0 count),
    not an exception or a missing row."""
    sys.modules.pop("database", None)
    from database import ensure_claude_audit_log_table, get_claude_endpoint_cost_windows

    conn = _get_conn()
    try:
        ensure_claude_audit_log_table()
        _clean(conn)
        results = get_claude_endpoint_cost_windows(recent_hours=24, baseline_days=7)
    finally:
        conn.close()

    assert all(r["endpoint"] != _TEST_ENDPOINT for r in results)
