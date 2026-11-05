"""
ST-40 (BLG-QA-221, EPIC-07, v9.15): real-Postgres tests for the ai_audit_log
UUID[] path (DS-31, ST-01/BLG-BE-162, v9.12) and the claude_audit_log daily
cost sum (get_daily_ai_cost, ST-06/BLG-OPS-183 and ST-41/BLG-OPS-186).

Until now this SQL was checked only through mocks: the DS-31
`ALTER ... TYPE UUID[] USING NULL`, the `%s::uuid[]` audit insert, the
history filter's `%s::uuid = ANY(trade_ids)`, and
`SUM(cost_usd) FROM claude_audit_log` over a UTC day. Here it runs for real:
  - DS-31: an INTEGER[] trade_ids column is converted to UUID[], its integer
    values cleared, and a second run is a no-op
  - an insert with trade_history UUIDs, then the history filter by one of
    them (match, no match, and no filter)
  - the daily cost sum over rows either side of both UTC day boundaries, with
    the session time zone set away from UTC so a timestamp/timestamptz or
    table-name mistake changes the total

Phase B only: skipped when DATABASE_URL contains 'stub' (Phase A stays fully
mocked), as in tests/test_reflection_reminder_postgres.py. Runs in a dedicated
schema (search_path set through PGOPTIONS for every connection the code under
test opens), dropped before and after.
"""
import importlib.util as _ilu
import os
import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pytest

psycopg2 = pytest.importorskip("psycopg2")
from psycopg2.extras import RealDictCursor  # noqa: E402

_DATABASE_URL = os.getenv("DATABASE_URL", "")
pytestmark = pytest.mark.skipif(
    "stub" in _DATABASE_URL.lower() or not _DATABASE_URL,
    reason="Phase A — DATABASE_URL is a stub; ai_audit_log/claude_audit_log integration tests require real Postgres (Phase B)",
)

SCHEMA = "st40_ai_audit_it"
# A session time zone well away from UTC, so a UTC-day boundary error moves rows.
PGOPTIONS = f"-c search_path={SCHEMA} -c timezone=America/New_York"

from tests._real_database import load_real_database  # noqa: E402
from tests._scoped_utils_stubs import scoped_stub_modules  # noqa: E402

database = load_real_database("database_real_for_st40_ai_audit")

_spec = _ilu.spec_from_file_location(
    "ai_audit_service_st40_it", Path(__file__).parent.parent / "backend" / "services" / "ai_audit_service.py"
)
ai_audit_service = _ilu.module_from_spec(_spec)
with scoped_stub_modules({"database": database}):
    _spec.loader.exec_module(ai_audit_service)


def _connect():
    return psycopg2.connect(database._clean_db_url(_DATABASE_URL), cursor_factory=RealDictCursor,
                            options=PGOPTIONS)


def _drop_schema():
    conn = psycopg2.connect(database._clean_db_url(_DATABASE_URL))
    try:
        with conn.cursor() as cur:
            cur.execute(f"DROP SCHEMA IF EXISTS {SCHEMA} CASCADE")
        conn.commit()
    finally:
        conn.close()


@pytest.fixture
def schema(monkeypatch):
    _drop_schema()
    conn = psycopg2.connect(database._clean_db_url(_DATABASE_URL))
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA {SCHEMA}")
    conn.commit()
    conn.close()
    # libpq reads PGOPTIONS on every connect, so get_db() lands in SCHEMA too.
    monkeypatch.setenv("PGOPTIONS", PGOPTIONS)
    # ensure_* functions run once per process; each test starts from an empty schema.
    database.reset_ensure_once()
    yield
    database.reset_ensure_once()
    _drop_schema()


def _column_type(cur, table, column):
    cur.execute(
        "SELECT udt_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s AND column_name = %s",
        (SCHEMA, table, column),
    )
    return cur.fetchone()["udt_name"]


# ---------------------------------------------------------------------------
# DS-31: INTEGER[] -> UUID[]
# ---------------------------------------------------------------------------

def test_ds31_converts_an_integer_array_table_to_uuid_array(schema):
    with _connect() as conn, conn.cursor() as cur:
        # The pre-DS-31 shape of the table, with an integer value that named no trade.
        cur.execute("""
            CREATE TABLE ai_audit_log (
                run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                invoked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                trade_ids INTEGER[],
                date_from DATE, date_to DATE,
                trade_count INTEGER NOT NULL DEFAULT 0,
                model_version VARCHAR(100), output_hash VARCHAR(64),
                summary_produced BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)
        cur.execute("INSERT INTO ai_audit_log (trade_ids, trade_count) VALUES ('{1,2}', 2)")
        assert _column_type(cur, "ai_audit_log", "trade_ids") == "_int4"

    ai_audit_service.ensure_ai_audit_table()
    ai_audit_service.ensure_ai_audit_table()  # idempotent: second run is a no-op

    with _connect() as conn, conn.cursor() as cur:
        assert _column_type(cur, "ai_audit_log", "trade_ids") == "_uuid"
        cur.execute("SELECT trade_ids, trade_count FROM ai_audit_log")
        rows = cur.fetchall()
    assert len(rows) == 1
    assert rows[0]["trade_ids"] is None  # cleared, not cast
    assert rows[0]["trade_count"] == 2


def test_fresh_table_is_created_with_uuid_array(schema):
    ai_audit_service.ensure_ai_audit_table()
    with _connect() as conn, conn.cursor() as cur:
        assert _column_type(cur, "ai_audit_log", "trade_ids") == "_uuid"


# ---------------------------------------------------------------------------
# UUID insert and history filter
# ---------------------------------------------------------------------------

def test_insert_and_history_filter_with_trade_uuids(schema):
    ai_audit_service.ensure_ai_audit_table()
    t1, t2, t3 = (str(uuid.uuid4()) for _ in range(3))

    run_a = ai_audit_service.log_ai_summary_run([t1, t2], None, None, 2, "model-x", "summary A", 120)
    run_b = ai_audit_service.log_ai_summary_run([t2], None, None, 1, "model-x", None)
    run_c = ai_audit_service.log_ai_summary_run(None, date(2026, 10, 1), date(2026, 10, 31), 5, "model-x", "C")

    with _connect() as conn, conn.cursor() as cur:
        # Read element-wise: psycopg2 has no uuid[] adapter registered, so the
        # column itself comes back as the text "{...}" (BLG-BE-206).
        cur.execute("SELECT unnest(trade_ids)::text AS t FROM ai_audit_log WHERE run_id = %s", (run_a,))
        stored = [r["t"] for r in cur.fetchall()]
    assert sorted(stored) == sorted([t1, t2])

    def ids(rows):
        return {str(r["run_id"]) for r in rows}

    assert ids(ai_audit_service.query_audit_log(trade_id=t1)) == {run_a}
    assert ids(ai_audit_service.query_audit_log(trade_id=t2)) == {run_a, run_b}
    assert ai_audit_service.query_audit_log(trade_id=t3) == []
    assert ids(ai_audit_service.query_audit_log()) == {run_a, run_b, run_c}
    # A uuid.UUID is accepted as well as its string form.
    assert ids(ai_audit_service.query_audit_log(trade_id=uuid.UUID(t1))) == {run_a}


# ---------------------------------------------------------------------------
# claude_audit_log daily cost sum across a UTC day boundary
# ---------------------------------------------------------------------------

def test_daily_cost_sum_counts_only_the_utc_day(schema):
    database.ensure_claude_audit_log_table()
    day = date(2026, 11, 4)
    start = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
    rows = [
        (start - timedelta(seconds=1), "0.50000000"),               # previous UTC day
        (start, "0.01000000"),                                       # first instant of the day
        (start + timedelta(hours=12), "0.02000000"),
        (start + timedelta(days=1) - timedelta(seconds=1), "0.03000000"),  # last second of the day
        (start + timedelta(days=1), "0.70000000"),                   # next UTC day
    ]
    with _connect() as conn, conn.cursor() as cur:
        for ts, cost in rows:
            cur.execute(
                "INSERT INTO claude_audit_log (endpoint, model_id, prompt_version, cost_usd, generated_at) "
                "VALUES ('POST /ai/daily-briefing', 'm', 'v1', %s, %s)",
                (Decimal(cost), ts),
            )
        # Rows outside claude_audit_log must not count (the pre-ST-06 table).
        cur.execute("CREATE TABLE gemini_audit_log (cost_usd NUMERIC(12, 8), generated_at TIMESTAMPTZ)")
        cur.execute("INSERT INTO gemini_audit_log VALUES (9.0, %s)", (start + timedelta(hours=1),))

    result = database.get_daily_ai_cost(day.isoformat())
    assert result == {"total_cost_usd": pytest.approx(0.06), "request_count": 3}
    assert database.get_daily_ai_cost((day - timedelta(days=1)).isoformat())["request_count"] == 1
    assert database.get_daily_ai_cost((day + timedelta(days=1)).isoformat())["total_cost_usd"] == pytest.approx(0.70)


def test_daily_cost_sum_is_zero_for_an_empty_day(schema):
    database.ensure_claude_audit_log_table()
    assert database.get_daily_ai_cost("2026-11-04") == {"total_cost_usd": 0.0, "request_count": 0}
