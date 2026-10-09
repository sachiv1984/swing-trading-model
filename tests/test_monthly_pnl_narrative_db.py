"""
ST-25/ST-26 (EPIC-04, v9.11, BLG-FEAT-59 / BLG-SPEC-174) — the monthly P&L
narrative's database layer against a real Postgres.

Runs against a real Postgres (CI Phase B's service; skipped where none is
reachable, e.g. Phase A's stub DATABASE_URL). Each test uses a scratch schema,
dropped afterwards, and points database.get_db at it.

- DS-30: monthly_pnl_narratives is created by its ensure-function; a stored
  summary is returned only for a matching input hash; a regeneration
  overwrites the row for that tax year.
- ST-26: count_monthly_pnl_narrative_generations() counts generations, not
  model calls: one terminal row per completed request.
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
ENDPOINT = "POST /reports/monthly-pnl/narrative"


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
    spec = importlib.util.spec_from_file_location("database_real_st25", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def scratch_db():
    name = f"st25_{uuid.uuid4().hex[:8]}"
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
        yield database, get_db
    with conn.cursor() as cur:
        cur.execute(f"DROP SCHEMA {name} CASCADE")
    conn.close()


def _audit_row(get_db, endpoint, result, at):
    with get_db() as c:
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO claude_audit_log (endpoint, model_id, prompt_version, compliance_check_result, generated_at) "
                "VALUES (%s, 'm', 'v1.0', %s, %s)",
                (endpoint, result, at),
            )


def test_ds30_storage_round_trip(scratch_db):
    database, _ = scratch_db
    pid = str(uuid.uuid4())
    row = {"input_hash": "a" * 64, "narrative_text": "first", "source": "ai",
           "compliance_check_result": "pass", "model_version": "m", "prompt_version": "v1.0"}
    database.upsert_monthly_pnl_narrative(pid, 2025, row)
    assert database.get_monthly_pnl_narrative(pid, 2025, "a" * 64)["narrative_text"] == "first"
    assert database.get_monthly_pnl_narrative(pid, 2025, "b" * 64) is None  # figures changed

    database.upsert_monthly_pnl_narrative(pid, 2025, {**row, "input_hash": "b" * 64, "narrative_text": "second",
                                                      "source": "fallback"})
    assert database.get_monthly_pnl_narrative(pid, 2025, "a" * 64) is None  # overwritten, one row per year
    got = database.get_monthly_pnl_narrative(pid, 2025, "b" * 64)
    assert (got["narrative_text"], got["source"]) == ("second", "fallback")


def test_ds30_source_check_constraint(scratch_db):
    database, _ = scratch_db
    with pytest.raises(psycopg2.errors.CheckViolation):
        database.upsert_monthly_pnl_narrative(str(uuid.uuid4()), 2025, {
            "input_hash": "c" * 64, "narrative_text": "x", "source": "other",
            "model_version": "m", "prompt_version": "v1.0"})


def test_st26_counts_generations_not_model_calls(scratch_db):
    database, get_db = scratch_db
    database.ensure_claude_audit_log_table()
    database.ensure_claude_audit_log_compliance_check_column()
    oct = datetime(2026, 10, 10, tzinfo=timezone.utc)
    rows = [
        (ENDPOINT, "pass"),                                        # generation 1 (ai, first attempt)
        (ENDPOINT, "fail_regenerate:prescriptive_language"),       # intermediate: not counted
        (ENDPOINT, "pass_on_regenerate"),                          # generation 2 (ai, after one retry)
        (ENDPOINT, "fail_regenerate:direction_check_failed"),      # intermediate
        (ENDPOINT, "fail_fallback:direction_check_failed"),        # generation 3 (fallback)
        (ENDPOINT, "model_call_failed"),                           # nothing stored: not counted
        ("POST /ai/chat", "pass"),                                 # another feature
        ("POST /trades/{trade_id}/debrief", "fail_fallback:x"),    # another feature
    ]
    for endpoint, result in rows:
        _audit_row(get_db, endpoint, result, oct)
    _audit_row(get_db, ENDPOINT, "pass", datetime(2026, 9, 1, tzinfo=timezone.utc))  # before the window

    assert database.count_monthly_pnl_narrative_generations() == {"generations": 4, "ai": 3, "fallback": 1}
    assert database.count_monthly_pnl_narrative_generations(
        date_from=datetime(2026, 10, 5, tzinfo=timezone.utc)) == {"generations": 3, "ai": 2, "fallback": 1}
    assert database.count_monthly_pnl_narrative_generations(
        date_to=datetime(2026, 10, 5, tzinfo=timezone.utc)) == {"generations": 1, "ai": 1, "fallback": 0}


def test_st26_count_matches_the_python_rule(scratch_db):
    """The SQL and monthly_pnl_narrative_service.is_generation_row() agree row by row."""
    from services.monthly_pnl_narrative_service import is_generation_row
    database, get_db = scratch_db
    database.ensure_claude_audit_log_table()
    database.ensure_claude_audit_log_compliance_check_column()
    at = datetime(2026, 10, 10, tzinfo=timezone.utc)
    cases = [(ENDPOINT, r) for r in ("pass", "pass_on_regenerate", "fail_fallback:a+b", "fail_regenerate:a",
                                     "model_call_failed", "failXfallback:a", None)]
    expected = sum(1 for e, r in cases if is_generation_row(e, r))
    for e, r in cases:
        _audit_row(get_db, e, r, at)
    assert database.count_monthly_pnl_narrative_generations()["generations"] == expected == 3
