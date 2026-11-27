"""ST-13 (BLG-FE-320, EPIC-02, v9.18): get_rules_followed_evidence on real Postgres.
Revised definition: ESC-EXEC-20261126-02 (plan-time events join through the plan).

metrics_definitions.md §Rules Followed. Runs against a real Postgres (CI
Phase B's service; skipped where none is reachable, e.g. Phase A's stub
DATABASE_URL). Each test uses a scratch schema, dropped afterwards.
"""
import os
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest

psycopg2 = pytest.importorskip("psycopg2")
from psycopg2.extras import RealDictCursor, Json  # noqa: E402

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
    spec = importlib.util.spec_from_file_location("database_real_st13", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# search_path is the scratch schema only (no `public`): a dropped scratch
# table must not fall through to a public.trade_plans another Phase B test made.
# gen_random_uuid lives in pg_catalog, so it still resolves.
@pytest.fixture
def scratch_db():
    name = f"st13_{uuid.uuid4().hex[:8]}"
    conn = _connect()
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA {name}")
        cur.execute(f"SET search_path TO {name}")
        cur.execute(
            """CREATE TABLE red_flag_events (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(), event_type TEXT NOT NULL,
                ticker TEXT NOT NULL, position_id UUID, context JSONB,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())"""
        )
        cur.execute(
            """CREATE TABLE trade_plans (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(), portfolio_id UUID NOT NULL,
                position_id UUID, ticker TEXT, pre_entry_override_acknowledged BOOLEAN,
                pre_entry_validation_snapshot JSONB, checklist_items JSONB NOT NULL DEFAULT '[]'::JSONB)"""
        )

    @contextmanager
    def get_db():
        # search_path as a connection option, not a SET: the code under test
        # rolls back after a missing table, and a rollback would undo a SET made
        # in the transaction, sending later queries to public.
        c = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor, connect_timeout=3,
                             options=f"-c search_path={name}")
        try:
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


PORT = str(uuid.uuid4())
OTHER_PORT = str(uuid.uuid4())
P_EVENTS, P_PLAN_OVERRIDE, P_PLAN_SNAPSHOT, P_OTHER_PORT, P_PLAN_SKIP = (str(uuid.uuid4()) for _ in range(5))
PLAN_SKIP_ID = str(uuid.uuid4())
ALL = [P_EVENTS, P_PLAN_OVERRIDE, P_PLAN_SNAPSHOT, P_OTHER_PORT, P_PLAN_SKIP]


def _seed(get_db):
    with get_db() as c:
        with c.cursor() as cur:
            for et, pid in [("pre_entry_override", P_EVENTS), ("checklist_skipped", P_EVENTS),
                            ("checklist_skipped", P_EVENTS), ("pre_entry_override", None)]:
                cur.execute("INSERT INTO red_flag_events (event_type, ticker, position_id) VALUES (%s, 'AAPL', %s)", (et, pid))
            plans = [
                (PORT, P_PLAN_OVERRIDE, True, None),
                (PORT, P_PLAN_OVERRIDE, None, None),          # a second plan for the same position
                (PORT, P_PLAN_SNAPSHOT, False, Json({"captured_at": "2026-11-20T09:00:00Z", "checks": []})),
                (PORT, None, True, None),                     # unlinked plan: never joined
                (OTHER_PORT, P_OTHER_PORT, True, None),       # another portfolio
            ]
            for port, pid, ack, snap in plans:
                cur.execute(
                    """INSERT INTO trade_plans (portfolio_id, position_id, ticker, pre_entry_override_acknowledged,
                       pre_entry_validation_snapshot) VALUES (%s, %s, 'AAPL', %s, %s)""",
                    (port, pid, ack, snap),
                )
            # A plan whose last saved checklist still has an unticked judgement item
            # (ESC-EXEC-20261126-03), linked to P_PLAN_SKIP; its draft-time event
            # (position_id null, naming the plan) is not read.
            cur.execute(
                """INSERT INTO trade_plans (id, portfolio_id, position_id, ticker, checklist_items)
                   VALUES (%s, %s, %s, 'AAPL', %s)""",
                (PLAN_SKIP_ID, PORT, P_PLAN_SKIP, Json([
                    {"id": "signal_confirmed", "checked": True},
                    {"id": "heat_limit_checked", "checked": False, "auto": True},
                    {"id": "research_reviewed", "checked": False},
                ])),
            )
            cur.execute(
                "INSERT INTO red_flag_events (event_type, ticker, position_id, context) VALUES ('checklist_skipped', 'AAPL', NULL, %s)",
                (Json({"source": "trade_plan", "plan_id": PLAN_SKIP_ID, "unchecked_items": 1, "total_items": 2}),),
            )


def test_evidence_by_position(scratch_db):
    database, get_db = scratch_db
    _seed(get_db)
    ev = database.get_rules_followed_evidence(PORT, ALL)

    # checklist_skipped events are not read; the plan's saved checklist decides.
    assert ev[P_EVENTS]["events"] == {"pre_entry_override"}
    assert ev[P_EVENTS]["override_acknowledged"] is False
    assert ev[P_EVENTS]["checklist_incomplete"] is True  # no linked plan: its position-linked event counts
    assert ev[P_PLAN_OVERRIDE] == {"events": set(), "override_acknowledged": True, "has_snapshot": False, "checklist_incomplete": False}
    assert ev[P_PLAN_SNAPSHOT] == {"events": set(), "override_acknowledged": False, "has_snapshot": True, "checklist_incomplete": False}
    assert ev[P_PLAN_SKIP]["events"] == set()
    assert ev[P_PLAN_SKIP]["checklist_incomplete"] is True
    # Another portfolio's plan is not read; null position_ids are never keys.
    assert P_OTHER_PORT not in ev
    assert "None" not in ev and None not in ev


def test_classification_end_to_end(scratch_db):
    database, get_db = scratch_db
    _seed(get_db)
    from services.rules_followed import classify_rules
    ev = database.get_rules_followed_evidence(PORT, ALL)
    assert classify_rules({"position_id": uuid.UUID(P_EVENTS), "entry_date": "2026-09-01"}, ev) == (False, ["checklist_skipped", "pre_entry_override"])
    assert classify_rules({"position_id": uuid.UUID(P_PLAN_OVERRIDE), "entry_date": "2026-09-01"}, ev) == (False, ["pre_entry_override"])
    assert classify_rules({"position_id": uuid.UUID(P_PLAN_SNAPSHOT), "entry_date": "2026-09-01"}, ev) == (True, [])


def test_only_the_asked_positions_are_returned(scratch_db):
    database, get_db = scratch_db
    _seed(get_db)
    assert set(database.get_rules_followed_evidence(PORT, [P_EVENTS])) == {P_EVENTS}
    assert database.get_rules_followed_evidence(PORT, []) == {}


def test_empty_tables_give_no_evidence(scratch_db):
    database, _ = scratch_db
    assert database.get_rules_followed_evidence(PORT, ALL) == {}


def test_missing_trade_plans_table_keeps_the_event_evidence(scratch_db):
    database, get_db = scratch_db
    _seed(get_db)
    with get_db() as c:
        with c.cursor() as cur:
            cur.execute("DROP TABLE trade_plans")
    ev = database.get_rules_followed_evidence(PORT, ALL)
    assert ev[P_EVENTS]["events"] == {"pre_entry_override"}
    assert P_PLAN_SKIP not in ev


def test_with_no_linked_plan_a_position_checklist_skipped_event_still_counts(scratch_db):
    database, get_db = scratch_db
    _seed(get_db)
    # P_EVENTS has a checklist_skipped event with its id and no linked plan.
    ev = database.get_rules_followed_evidence(PORT, ALL)
    assert ev[P_EVENTS]["checklist_incomplete"] is True
    # Once a complete plan is linked, the plan's saved checklist decides instead.
    with get_db() as c:
        with c.cursor() as cur:
            cur.execute(
                "INSERT INTO trade_plans (portfolio_id, position_id, ticker, checklist_items) VALUES (%s, %s, 'AAPL', %s)",
                (PORT, P_EVENTS, Json([{"id": "signal_confirmed", "checked": True}, {"id": "research_reviewed", "checked": True}])),
            )
    assert database.get_rules_followed_evidence(PORT, ALL)[P_EVENTS]["checklist_incomplete"] is False


def test_missing_red_flag_events_table_keeps_the_plan_evidence(scratch_db):
    database, get_db = scratch_db
    _seed(get_db)
    with get_db() as c:
        with c.cursor() as cur:
            cur.execute("DROP TABLE red_flag_events")
    ev = database.get_rules_followed_evidence(PORT, ALL)
    assert ev[P_PLAN_OVERRIDE]["override_acknowledged"] is True
    assert ev[P_PLAN_SKIP]["checklist_incomplete"] is True

