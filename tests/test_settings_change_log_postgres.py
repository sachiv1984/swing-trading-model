"""
ST-38 (BLG-QA-226, EPIC-06, v9.18): the settings change-log SQL against a real
Postgres.

tests/test_settings_change_log.py drives create_settings(), update_settings()
and get_last_settings_change() through a fake connection that records the SQL,
so a wrong column or table name in that SQL passes it. This file runs the same
real backend/database.py functions against real tables:

- `settings` and `settings_change_log` are created from the canonical SQL in
  docs/specs/data_model.md (§6 Settings Table and the DS-33 Up Migration), not
  from a copy, so the test follows the spec.
- Two saves (create, then update) each write one log row per changed field,
  with the field, old value, new value and request source, and one batch_id
  per save; the update logs only the fields whose value changed.
- get_last_settings_change() returns the second save as last_change.
- The same insert with a deliberately broken column name fails against real
  Postgres (the AC 2 negative case, run on every Phase B run).

Phase B only: skipped when DATABASE_URL is a stub or unreachable (Phase A),
like tests/test_chat_answer_rating_db.py. Each test uses its own schema, dropped
afterwards. Never point this at a shared database: it creates and drops schemas.
"""
import os
import re
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

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


def _spec_sql():
    """The settings DDL and the DS-33 Up Migration, read from data_model.md."""
    text = (ROOT / "docs" / "specs" / "data_model.md").read_text()
    blocks = re.findall(r"```sql\n(.*?)```", text, re.S)
    settings = [b for b in blocks if b.lstrip().startswith("CREATE TABLE settings (")]
    change_log = [b for b in blocks if "CREATE TABLE IF NOT EXISTS settings_change_log" in b]
    assert len(settings) == 1, "data_model.md §6 must hold exactly one CREATE TABLE settings block"
    assert len(change_log) == 1, "data_model.md DS-33 must hold exactly one settings_change_log Up Migration"
    return settings[0], change_log[0]


@pytest.fixture
def scratch_db():
    """The real database module with get_db pointed at a fresh schema holding the spec tables."""
    name = f"st38_{uuid.uuid4().hex[:8]}"
    settings_sql, change_log_sql = _spec_sql()
    admin = _connect()
    admin.autocommit = True
    with admin.cursor() as cur:
        cur.execute(f"CREATE SCHEMA {name}")
        cur.execute(f"SET search_path TO {name}")
        cur.execute(settings_sql)
        cur.execute(change_log_sql)

    @contextmanager
    def get_db():
        c = _connect()
        try:
            with c.cursor() as cur:
                cur.execute(f"SET search_path TO {name}")
            yield c
            c.commit()
        except Exception:
            c.rollback()
            raise
        finally:
            c.close()

    database = load_real_database(f"database_real_{name}")
    try:
        with patch.object(database, "get_db", get_db):
            yield database
    finally:
        with admin.cursor() as cur:
            cur.execute(f"DROP SCHEMA {name} CASCADE")
        admin.close()


def _log_rows(database):
    with database.get_db() as c:
        with c.cursor() as cur:
            cur.execute(
                "SELECT settings_id, batch_id, field, old_value, new_value, request_source, changed_at "
                "FROM settings_change_log ORDER BY id"
            )
            return [dict(r) for r in cur.fetchall()]


def test_two_saves_write_log_rows_and_last_change(scratch_db):
    # Save 1: create with two explicit values; every other column takes its default.
    created = scratch_db.create_settings(
        {"default_risk_percent": 1.5, "theme": "light", "min_hold_days": None}, request_source="settings_page"
    )
    settings_id = str(created["id"])

    # Save 2: change two fields, re-send one unchanged value (not logged).
    scratch_db.update_settings(
        settings_id,
        {"default_risk_percent": 2.25, "uk_commission": 7.5, "theme": "light", "atr_period": None},
        request_source="api",
    )

    rows = _log_rows(scratch_db)
    batches = []
    for row in rows:
        if not batches or batches[-1][0] != row["batch_id"]:
            batches.append((row["batch_id"], []))
        batches[-1][1].append(row)
    assert len(batches) == 2, "each save must share one batch_id across its rows"
    (batch_1, save_1), (batch_2, save_2) = batches
    assert batch_1 != batch_2
    assert all(str(r["settings_id"]) == settings_id for r in rows)

    # Save 1 logs every non-null column of the new row, old_value NULL, as text
    # without trailing zeros (DECIMAL(4,2) 1.50 -> "1.5"; DECIMAL(6,5) 0.00500 -> "0.005").
    created_fields = {r["field"]: (r["old_value"], r["new_value"], r["request_source"]) for r in save_1}
    assert created_fields == {
        "min_hold_days": (None, "10", "settings_page"),
        "atr_multiplier_initial": (None, "5", "settings_page"),
        "atr_multiplier_trailing": (None, "2", "settings_page"),
        "atr_period": (None, "14", "settings_page"),
        "default_currency": (None, "GBP", "settings_page"),
        "theme": (None, "light", "settings_page"),
        "uk_commission": (None, "9.95", "settings_page"),
        "us_commission": (None, "0", "settings_page"),
        "stamp_duty_rate": (None, "0.005", "settings_page"),
        "fx_fee_rate": (None, "0.0015", "settings_page"),
        "min_trades_for_analytics": (None, "10", "settings_page"),
        "default_risk_percent": (None, "1.5", "settings_page"),
    }

    # Save 2 logs only the two fields whose value changed, in the order sent.
    assert [(r["field"], r["old_value"], r["new_value"], r["request_source"]) for r in save_2] == [
        ("default_risk_percent", "1.5", "2.25", "api"),
        ("uk_commission", "9.95", "7.5", "api"),
    ]

    # The stored row holds the new values.
    stored = scratch_db.get_settings()[0]
    assert str(stored["default_risk_percent"]) == "2.25" and str(stored["uk_commission"]) == "7.50"

    # last_change is the second save.
    last = scratch_db.get_last_settings_change()
    assert last["field"] == "default_risk_percent"
    assert (last["old_value"], last["new_value"], last["request_source"]) == ("1.5", "2.25", "api")
    assert last["changed_at"] == save_2[0]["changed_at"].isoformat()
    assert last["changes"] == [
        {"field": "default_risk_percent", "old_value": "1.5", "new_value": "2.25"},
        {"field": "uk_commission", "old_value": "9.95", "new_value": "7.5"},
    ]


def test_update_with_no_change_logs_nothing_and_last_change_is_kept(scratch_db):
    created = scratch_db.create_settings({"theme": "dark"})
    first_batch = {r["batch_id"] for r in _log_rows(scratch_db)}
    scratch_db.update_settings(str(created["id"]), {"theme": "dark", "uk_commission": 9.95})
    assert {r["batch_id"] for r in _log_rows(scratch_db)} == first_batch
    assert scratch_db.get_last_settings_change()["request_source"] == "api"


def test_no_log_rows_gives_no_last_change(scratch_db):
    assert scratch_db.get_last_settings_change() is None


def test_broken_insert_column_name_fails_against_real_postgres(scratch_db):
    """AC 2 negative case: the real insert, with one column name broken, fails here.

    The fake-connection tests in tests/test_settings_change_log.py pass this same
    broken SQL, which is why this file exists.
    """
    def broken_log(cur, settings_id, changes, request_source):
        for field, old_value, new_value in changes:
            cur.execute(
                "INSERT INTO settings_change_log "
                "(settings_id, batch_id, field_name, old_value, new_value, request_source) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (str(settings_id), str(uuid.uuid4()), field, old_value, new_value, request_source),
            )

    # The real insert names the column `field`; this test breaks only that name.
    source = (ROOT / "backend" / "database.py").read_text()
    assert "(settings_id, batch_id, field, old_value, new_value, request_source)" in source

    with patch.object(scratch_db, "_log_settings_changes", broken_log):
        with pytest.raises(psycopg2.errors.UndefinedColumn):
            scratch_db.create_settings({"theme": "light"})
    # The failed save rolled back with its settings row: nothing half-written.
    with scratch_db.get_db() as c:
        with c.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS n FROM settings")
            assert cur.fetchone()["n"] == 0
