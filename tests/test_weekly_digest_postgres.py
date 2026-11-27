"""
ST-14 (EPIC-03, v9.18, BLG-SPEC-204): the Weekly Digest's journal completion
rate is the same figure as GET /analytics/compliance-metrics, against a real
Postgres.

- Runs the real `_fetch_weekly_digest_data` and `get_compliance_core_counts`
  over the same `trade_history` rows (notes empty, NULL, whitespace-free text,
  entry-only, exit-only; trades either side of the 7-day cutoff) and asserts
  the digest's rate and count equal the analytics rate and trade_count.
- ST-16: `red_flags_7d` counts `red_flag_events` inside the rolling 7 × 24h
  window (rows either side of the boundary).
- ST-17: the five loop counts for the current ISO week against real rows
  either side of Monday 00:00 UTC (DATE, TIMESTAMP and TIMESTAMPTZ columns),
  with distinct (ticker, market) signals and distinct-day reviews; the
  `loop_events` CHECK rejects any other event type.
- A failed earlier query (a missing `portfolio_history` table) no longer
  aborts the transaction for the later ones: the journal fields still answer.

Phase B only: skipped when DATABASE_URL is a stub or unreachable (Phase A),
like tests/test_settings_change_log_postgres.py. Each test uses its own
schema, dropped afterwards. Never point this at a shared database.
"""
import os
import sys
import uuid
from datetime import date, timedelta
from pathlib import Path

import pytest

psycopg2 = pytest.importorskip("psycopg2")
from psycopg2.extras import RealDictCursor  # noqa: E402

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))
from tests._real_database import load_real_database  # noqa: E402

DB_URL = os.environ.get("DATABASE_URL", "")


def _connect():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor, connect_timeout=3)


def _db_available():
    if not DB_URL or "stub" in DB_URL:
        return False
    try:
        _connect().close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _db_available(), reason="needs a reachable Postgres (CI Phase B)")

# Only the columns the two queries read; types per data_model.md trade_history.
TABLES = """
CREATE TABLE trade_history (
    id SERIAL PRIMARY KEY,
    exit_date DATE NOT NULL,
    pnl DECIMAL(10, 2),
    exit_reason VARCHAR(50),
    entry_note TEXT,
    exit_note TEXT
);
CREATE TABLE red_flag_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL DEFAULT 'override',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
CREATE TABLE signals (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    market VARCHAR(5) NOT NULL,
    signal_date DATE NOT NULL
);
CREATE TABLE trade_plans (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE trade_reflections (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    read BOOLEAN NOT NULL DEFAULT FALSE
);
"""

TODAY = date.today()
OLD = TODAY - timedelta(days=30)  # before the cutoff
NEW = TODAY - timedelta(days=1)   # inside the window
ROWS = [
    # (exit_date, entry_note, exit_note) → journalled?
    (OLD, "thesis", None),   # yes
    (OLD, None, "lesson"),   # yes
    (OLD, "", ""),           # no: empty strings
    (OLD, None, None),       # no
    (NEW, "", "done"),       # yes
    (NEW, None, None),       # no
    (NEW, "a", "b"),         # yes
]


@pytest.fixture
def scratch():
    name = f"st14_{uuid.uuid4().hex[:8]}"
    admin = _connect()
    admin.autocommit = True
    with admin.cursor() as cur:
        cur.execute(f"CREATE SCHEMA {name}")
        cur.execute(f"SET search_path TO {name}")
        cur.execute(TABLES)
        cur.executemany(
            "INSERT INTO trade_history (exit_date, pnl, exit_reason, entry_note, exit_note) "
            "VALUES (%s, 10, 'Manual Exit', %s, %s)",
            ROWS,
        )
        cur.executemany(
            "INSERT INTO red_flag_events (created_at) VALUES (NOW() - %s::interval)",
            [("1 hour",), ("6 days 23 hours",), ("7 days 1 hour",), ("30 days",)],
        )
    conn = _connect()
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {name}")
    conn.commit()
    database = load_real_database(f"database_real_{name}")
    try:
        yield database, conn
    finally:
        conn.close()
        with admin.cursor() as cur:
            cur.execute(f"DROP SCHEMA {name} CASCADE")
        admin.close()


def test_digest_rate_equals_compliance_metrics_rate(scratch):
    database, conn = scratch
    # portfolio_history is absent: its queries fail first, and the journal
    # queries after them must still run (the transaction is rolled back).
    digest = database.get_weekly_digest_data(conn=conn)
    core = database.get_compliance_core_counts(conn=conn)
    analytics_rate = round(int(core["trades_with_notes"]) / int(core["total_trades"]) * 100, 1)

    assert digest["closed_trades_total"] == int(core["total_trades"]) == 7
    assert digest["journal_completion_rate_current"] == analytics_rate == 57.1  # 4 of 7
    assert digest["closed_trades_total_7d_ago"] == 4
    assert digest["journal_completion_rate_7d_ago"] == 50.0  # 2 of the 4 old trades
    assert digest["unrealised_pnl_delta_7d"] is None
    assert digest["staleness_hours"] is None
    # ST-16: two of the four red flags are inside the rolling 7 × 24h window.
    assert digest["red_flags_7d"] == 2


def test_loop_counts_against_real_rows(scratch):
    from datetime import datetime, timedelta, timezone

    database, conn = scratch
    now = datetime.now(timezone.utc)
    week_start = database.iso_week_start_utc(now)
    if now - week_start < timedelta(minutes=5):
        pytest.skip("too close to Monday 00:00 UTC for an in-week row")
    inside = week_start + (now - week_start) / 2      # in the window
    before = week_start - timedelta(seconds=1)        # Sunday 23:59:59 UTC
    inside_n, before_n = inside.replace(tzinfo=None), before.replace(tzinfo=None)

    database.ensure_loop_events_table(conn=conn)
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO signals (ticker, market, signal_date) VALUES (%s, %s, %s)",
            [
                ("VOD.L", "UK", week_start.date()),                       # in
                ("VOD.L", "UK", inside.date()),                           # same pair again
                ("GSK", "US", week_start.date()),                         # in
                ("GSK.L", "UK", week_start.date()),                       # in: other market
                ("AAPL", "US", (week_start - timedelta(days=1)).date()),  # Sunday: out
            ],
        )
        cur.executemany("INSERT INTO trade_plans (created_at) VALUES (%s)", [(inside,), (before,)])
        cur.executemany("INSERT INTO positions (created_at) VALUES (%s)", [(inside_n,), (inside_n,), (before_n,)])
        cur.executemany("INSERT INTO trade_reflections (created_at) VALUES (%s)", [(before_n,)])
        cur.executemany(
            "INSERT INTO loop_events (event_type, created_at) VALUES (%s, %s)",
            [
                ("weekly_digest_opened", week_start),                     # day 1
                ("weekly_digest_opened", week_start + timedelta(hours=3)),  # day 1 again
                ("weekly_digest_opened", before),                         # last week
                ("due_today_action", inside),                             # not a review
            ],
        )
    conn.commit()

    loop = database.get_weekly_digest_data(conn=conn)["loop"]
    assert loop == {
        "week_start": week_start.date().isoformat(),
        "signals": 3,
        "plans": 1,
        "entries": 2,
        "reflections": 0,
        "reviews": 1,
    }


def test_loop_events_check_rejects_other_types(scratch):
    database, conn = scratch
    database.ensure_loop_events_table(conn=conn)
    database.record_loop_event("due_today_action", conn=conn)
    with conn.cursor() as cur:
        with pytest.raises(psycopg2.errors.CheckViolation):
            cur.execute("INSERT INTO loop_events (event_type) VALUES ('page_view')")
    conn.rollback()
    with conn.cursor() as cur:
        cur.execute("SELECT event_type FROM loop_events")
        assert [r["event_type"] for r in cur.fetchall()] == ["due_today_action"]

