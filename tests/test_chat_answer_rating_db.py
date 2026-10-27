"""
ST-22 (BLG-FE-208), EPIC-03, v9.13 — chat answer ratings (DS-35) and the
Response Acceptance Rate against a real Postgres.

Runs against a real Postgres (CI Phase B's service; skipped where none is
reachable, e.g. Phase A's stub DATABASE_URL). Each test uses a scratch schema,
dropped afterwards, and points database.get_db at it.

- A rating persists against its claude_audit_log row; a second rating for the
  same answer is not stored and the first is returned (AC 1, "once").
- Only a successful POST /ai/chat row can be rated.
- get_response_acceptance_rate() returns useful / rated, and None when nothing
  is rated (AC 3).
"""
import os
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

psycopg2 = pytest.importorskip("psycopg2")
from psycopg2.extras import RealDictCursor  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

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


def _real_database_module():
    """tests/conftest.py replaces `database` with stubs; load the real file."""
    import importlib.util
    path = Path(__file__).parent.parent / "backend" / "database.py"
    spec = importlib.util.spec_from_file_location("database_real_st22", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def scratch_db():
    name = f"st22_{uuid.uuid4().hex[:8]}"
    conn = _connect()
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA {name}")

    @contextmanager
    def get_db():
        c = _connect()
        try:
            with c.cursor() as cur:
                cur.execute(f"SET search_path TO {name}, public")
            yield c
            c.commit()
        except Exception:
            c.rollback()
            raise
        finally:
            c.close()

    database = _real_database_module()
    with patch.object(database, "get_db", get_db):
        yield database
    with conn.cursor() as cur:
        cur.execute(f"DROP SCHEMA {name} CASCADE")
    conn.close()


def _answer(database, endpoint="POST /ai/chat", result="pass", at=None):
    answer_id = database.create_claude_audit_entry(
        endpoint=endpoint, model_id="m", prompt_version="v1.2", compliance_check_result=result)
    assert answer_id is not None
    if at is not None:
        with database.get_db() as c:
            with c.cursor() as cur:
                cur.execute("UPDATE claude_audit_log SET generated_at = %s WHERE id = %s", (at, answer_id))
    return answer_id


def test_audit_entry_returns_its_row_id(scratch_db):
    answer_id = _answer(scratch_db)
    uuid.UUID(answer_id)


def test_rating_persists_once(scratch_db):
    answer_id = _answer(scratch_db)
    first = scratch_db.create_chat_answer_rating(answer_id, "useful")
    assert first["created"] is True and first["rating"] == "useful" and first["answer_id"] == answer_id

    second = scratch_db.create_chat_answer_rating(answer_id, "not_useful")
    assert second["created"] is False
    assert second["rating"] == "useful"  # the first rating is kept, not overwritten
    assert second["rated_at"] == first["rated_at"]

    with scratch_db.get_db() as c:
        with c.cursor() as cur:
            cur.execute("SELECT answer_id, rating FROM chat_answer_ratings")
            rows = cur.fetchall()
    assert [(str(r["answer_id"]), r["rating"]) for r in rows] == [(answer_id, "useful")]


@pytest.mark.parametrize("endpoint, result", [
    ("POST /ai/daily-briefing", "pass"),
    ("POST /ai/chat", "model_call_failed"),
])
def test_only_successful_chat_answers_can_be_rated(scratch_db, endpoint, result):
    answer_id = _answer(scratch_db, endpoint=endpoint, result=result)
    assert scratch_db.create_chat_answer_rating(answer_id, "useful") is None


def test_unknown_answer_is_none(scratch_db):
    scratch_db.ensure_claude_audit_log_compliance_check_column()
    assert scratch_db.create_chat_answer_rating(str(uuid.uuid4()), "useful") is None


def test_check_constraint_rejects_other_values(scratch_db):
    answer_id = _answer(scratch_db)
    with pytest.raises(psycopg2.errors.CheckViolation):
        scratch_db.create_chat_answer_rating(answer_id, "great")


def test_acceptance_rate_null_when_nothing_rated(scratch_db):
    _answer(scratch_db)
    assert scratch_db.get_response_acceptance_rate() == {"rated": 0, "useful": 0, "rate": None}


def test_acceptance_rate_from_stored_ratings(scratch_db):
    for rating in ("useful", "useful", "not_useful"):
        scratch_db.create_chat_answer_rating(_answer(scratch_db), rating)
    _answer(scratch_db)  # unrated: excluded
    assert scratch_db.get_response_acceptance_rate() == {"rated": 3, "useful": 2, "rate": pytest.approx(2 / 3)}


def test_acceptance_rate_window_uses_answer_time(scratch_db):
    old = _answer(scratch_db, at=datetime(2026, 9, 1, tzinfo=timezone.utc))
    new = _answer(scratch_db, at=datetime(2026, 10, 20, tzinfo=timezone.utc))
    scratch_db.create_chat_answer_rating(old, "not_useful")
    scratch_db.create_chat_answer_rating(new, "useful")
    oct_ = scratch_db.get_response_acceptance_rate(datetime(2026, 10, 1, tzinfo=timezone.utc),
                                                   datetime(2026, 11, 1, tzinfo=timezone.utc))
    assert oct_ == {"rated": 1, "useful": 1, "rate": 1.0}
