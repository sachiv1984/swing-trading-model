"""
ST-20 (BLG-OPS-175, EPIC-03, v9.11) — a genuinely concurrent double-submit of
the same price alert is absorbed at the database layer.

Runs against a real Postgres (CI Phase B's service; skipped where none is
reachable, e.g. Phase A's stub DATABASE_URL). It creates a scratch schema with
the price_alerts columns, applies DS-28's Up Migration read from
docs/specs/data_model.md, then races create_price_alert() against another
transaction that has inserted the same alert and not yet committed:

  1. transaction A inserts the alert and holds it uncommitted;
  2. create_price_alert() (B) runs its de-dup SELECT, sees nothing (A is
     uncommitted), and INSERTs, which blocks on the partial unique index;
  3. A commits; B's INSERT raises a unique violation, which the service
     absorbs by returning A's alert.

Exactly one active row results. Without the index, B would insert a second.
"""
import os
import re
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest

psycopg2 = pytest.importorskip("psycopg2")
from psycopg2.extras import RealDictCursor  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
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


def _ds28_up_migration() -> str:
    text = (ROOT / "docs" / "specs" / "data_model.md").read_text()
    section = text[text.index("## DS-28 "):]
    return re.search(r"### Up Migration.*?```sql\n(.*?)```", section, re.S).group(1)


@pytest.fixture
def schema():
    name = f"st20_{uuid.uuid4().hex[:8]}"
    conn = _connect()
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA {name}")
        cur.execute(f"SET search_path TO {name}")
        cur.execute("""
            CREATE TABLE price_alerts (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                portfolio_id UUID NOT NULL,
                ticker VARCHAR(10) NOT NULL,
                condition VARCHAR(10) NOT NULL CHECK (condition IN ('above', 'below')),
                threshold_price NUMERIC(10, 4) NOT NULL CHECK (threshold_price > 0),
                active BOOLEAN NOT NULL DEFAULT TRUE,
                triggered_at TIMESTAMPTZ,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
    conn.autocommit = False
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {name}")
        cur.execute(_ds28_up_migration())
    conn.commit()
    yield name
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP SCHEMA {name} CASCADE")
    conn.close()


def _service_get_db(schema_name):
    @contextmanager
    def get_db():
        conn = _connect()
        try:
            with conn.cursor() as cur:
                cur.execute(f"SET search_path TO {schema_name}")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    return get_db


def test_migration_creates_the_partial_unique_index(schema):
    conn = _connect()
    with conn.cursor() as cur:
        cur.execute("SELECT indexdef FROM pg_indexes WHERE schemaname = %s AND indexname = 'idx_price_alerts_active_unique'", (schema,))
        row = cur.fetchone()
    conn.close()
    assert row and "UNIQUE" in row["indexdef"] and "WHERE (active = true)" in row["indexdef"]


def test_concurrent_double_submit_is_absorbed_at_the_db_layer(schema):
    from services import alerts_service

    portfolio = str(uuid.uuid4())
    a = _connect()
    with a.cursor() as cur:
        cur.execute(f"SET search_path TO {schema}")
        cur.execute(
            "INSERT INTO price_alerts (portfolio_id, ticker, condition, threshold_price) VALUES (%s, 'AAPL', 'above', 200) RETURNING id",
            (portfolio,),
        )
        a_id = str(cur.fetchone()["id"])  # A holds this row uncommitted

    result = {}

    def submit_b():
        with patch.object(alerts_service, "get_db", _service_get_db(schema)):
            result["b"] = alerts_service.create_price_alert(
                portfolio, {"ticker": "AAPL", "condition": "above", "threshold_price": 200}
            )

    b = threading.Thread(target=submit_b)
    b.start()
    time.sleep(1.0)               # B has passed its SELECT and is blocked on the index
    assert b.is_alive(), "B should be waiting on A's uncommitted row"
    a.commit()
    b.join(timeout=10)
    a.close()

    assert str(result["b"]["id"]) == a_id
    check = _connect()
    with check.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) AS n FROM {schema}.price_alerts WHERE active = TRUE")
        assert cur.fetchone()["n"] == 1
    check.close()


def test_a_triggered_alert_does_not_block_a_new_active_one(schema):
    portfolio = str(uuid.uuid4())
    conn = _connect()
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {schema}")
        cur.execute("INSERT INTO price_alerts (portfolio_id, ticker, condition, threshold_price, active) VALUES (%s, 'MSFT', 'below', 300, FALSE)", (portfolio,))
        cur.execute("INSERT INTO price_alerts (portfolio_id, ticker, condition, threshold_price) VALUES (%s, 'MSFT', 'below', 300)", (portfolio,))
    conn.commit()
    conn.close()
