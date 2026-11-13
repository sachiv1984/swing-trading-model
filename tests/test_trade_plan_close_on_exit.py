"""
ST-11 (BLG-BE-211, EPIC-05, v9.17): a linked trade plan moves `active` ->
`closed` when its position closes (data_model.md §Trade Plan Lifecycle, DS-41).

Two parts:

- exit_position(): a full exit closes the position's `active` linked plan; a
  partial exit leaves it `active`; no plan and a failed plan write do not
  affect the exit. Runs the real exit_position() with the DB layer mocked
  (same pattern as tests/test_exit_null_fill_price.py).
- backfill_closed_position_trade_plans(): closes `active` plans whose linked
  position is already `closed`, leaves every other row alone, writes one audit
  row per plan, and a second run changes nothing. Runs against a real Postgres
  in a scratch schema (CI Phase B; skipped where none is reachable).
"""
import os
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent))

import services.position_service as position_service  # noqa: E402


# ---------------------------------------------------------------------------
# exit_position(): full exit, partial exit, no plan
# ---------------------------------------------------------------------------

def _uk_position(**overrides):
    position = {
        "id": "pos-1",
        "ticker": "VOD.L",
        "market": "UK",
        "status": "open",
        "shares": 10,
        "total_cost": 12.0,
        "fees_paid": 0.0,
        "entry_price": 1.20,
        "fx_rate": None,
        "fill_price": None,
        "entry_date": "2026-10-01",
        "atr": None,
        "active_atr_multiplier": None,
    }
    position.update(overrides)
    return position


def _exit(plans, shares=None, update_side_effect=None):
    plan_writes = []

    def _update(plan_id, portfolio_id, data, audit_source=None):
        if update_side_effect and plan_id in update_side_effect[0]:
            raise update_side_effect[1]
        plan_writes.append((plan_id, portfolio_id, data, audit_source))
        return {"id": plan_id, **data}

    with patch.object(position_service, "get_portfolio", return_value={"id": "portfolio-1", "cash": 0.0}), \
         patch.object(position_service, "get_positions", return_value=[_uk_position()]), \
         patch.object(position_service, "get_settings", return_value=[{"uk_commission": 0, "stamp_duty_rate": 0}]), \
         patch.object(position_service, "update_portfolio_cash"), \
         patch.object(position_service, "create_trade_history"), \
         patch.object(position_service, "update_position") as update_position, \
         patch.object(position_service, "get_signals", return_value=[]), \
         patch.object(position_service, "get_trade_plans_by_position", return_value=plans), \
         patch.object(position_service, "update_trade_plan", side_effect=_update), \
         patch.object(position_service, "ensure_planned_entry_price_column", return_value=None):
        result = position_service.exit_position(
            position_id="pos-1", exit_price=1.30, shares=shares, exit_date="2026-11-13",
        )
    return result, plan_writes, update_position


def test_full_exit_closes_the_linked_active_plan():
    result, writes, _ = _exit([{"id": "plan-1", "status": "active", "position_id": "pos-1"}])
    assert result["is_partial_exit"] is False
    assert writes == [("plan-1", "portfolio-1", {"status": "closed"}, "position-exit")]


def test_partial_exit_leaves_the_plan_active():
    result, writes, _ = _exit([{"id": "plan-1", "status": "active", "position_id": "pos-1"}], shares=4)
    assert result["is_partial_exit"] is True
    assert writes == []


def test_full_exit_with_no_linked_plan_writes_nothing():
    result, writes, update_position = _exit([])
    assert writes == []
    # The position itself still closes.
    assert update_position.call_args.args[1]["status"] == "closed"
    assert result["remaining_shares"] == 0


def test_full_exit_leaves_terminal_and_hand_set_statuses_alone():
    plans = [
        {"id": "plan-a", "status": "abandoned", "position_id": "pos-1"},
        {"id": "plan-c", "status": "closed", "position_id": "pos-1"},
        {"id": "plan-d", "status": "draft", "position_id": "pos-1"},
    ]
    _, writes, _ = _exit(plans)
    assert writes == []


def test_a_failed_plan_write_does_not_fail_the_exit_or_the_other_plans():
    result, writes, update_position = _exit(
        [{"id": "plan-1", "status": "active", "position_id": "pos-1"},
         {"id": "plan-2", "status": "active", "position_id": "pos-1"}],
        update_side_effect=({"plan-1"}, RuntimeError("db down")),
    )
    assert [w[0] for w in writes] == ["plan-2"]
    assert result["is_partial_exit"] is False
    assert update_position.call_args.args[1]["status"] == "closed"


# ---------------------------------------------------------------------------
# backfill_closed_position_trade_plans(): real Postgres, scratch schema
# ---------------------------------------------------------------------------

DB_URL = os.environ.get("DATABASE_URL", "")


def _connect():
    import psycopg2
    from psycopg2.extras import RealDictCursor
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor, connect_timeout=3)


def _db_available():
    if not DB_URL or "stub" in DB_URL:
        return False
    try:
        _connect().close()
        return True
    except Exception:
        return False


needs_pg = pytest.mark.skipif(not _db_available(), reason="needs a reachable Postgres (CI Phase B)")


def _real_database_module():
    """tests/conftest.py replaces `database` with stubs; load the real file."""
    import importlib.util
    path = Path(__file__).parent.parent / "backend" / "database.py"
    spec = importlib.util.spec_from_file_location("database_real_st11", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def scratch_db():
    name = f"st11_{uuid.uuid4().hex[:8]}"
    conn = _connect()
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA {name}")
        cur.execute(f"SET search_path TO {name}")
        # Only the columns the backfill reads or writes.
        cur.execute("""
            CREATE TABLE positions (
                id UUID PRIMARY KEY,
                portfolio_id UUID NOT NULL,
                status VARCHAR(20) NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE trade_plans (
                id UUID PRIMARY KEY,
                portfolio_id UUID NOT NULL,
                position_id UUID,
                status VARCHAR(20) NOT NULL,
                updated_at TIMESTAMPTZ
            )
        """)

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


def _seed(get_db):
    portfolio = str(uuid.uuid4())
    other_portfolio = str(uuid.uuid4())
    ids = {k: str(uuid.uuid4()) for k in (
        "pos_closed", "pos_open", "pos_other_portfolio",
        "plan_to_close", "plan_open_position", "plan_abandoned", "plan_draft_unlinked",
        "plan_portfolio_mismatch",
    )}
    with get_db() as c, c.cursor() as cur:
        cur.execute("INSERT INTO positions VALUES (%s, %s, 'closed'), (%s, %s, 'open'), (%s, %s, 'closed')",
                    (ids["pos_closed"], portfolio, ids["pos_open"], portfolio,
                     ids["pos_other_portfolio"], other_portfolio))
        rows = [
            (ids["plan_to_close"], portfolio, ids["pos_closed"], "active"),
            (ids["plan_open_position"], portfolio, ids["pos_open"], "active"),
            (ids["plan_abandoned"], portfolio, ids["pos_closed"], "abandoned"),
            (ids["plan_draft_unlinked"], portfolio, None, "draft"),
            # Linked to a closed position in another portfolio: not this plan's position.
            (ids["plan_portfolio_mismatch"], portfolio, ids["pos_other_portfolio"], "active"),
        ]
        for row in rows:
            cur.execute("INSERT INTO trade_plans (id, portfolio_id, position_id, status) VALUES (%s, %s, %s, %s)", row)
    return ids


def _statuses(get_db):
    with get_db() as c, c.cursor() as cur:
        cur.execute("SELECT id, status FROM trade_plans")
        return {str(r["id"]): r["status"] for r in cur.fetchall()}


@needs_pg
def test_backfill_closes_only_active_plans_whose_position_is_closed(scratch_db):
    database, get_db = scratch_db
    ids = _seed(get_db)

    closed = database.backfill_closed_position_trade_plans()

    assert closed == [ids["plan_to_close"]]
    statuses = _statuses(get_db)
    assert statuses[ids["plan_to_close"]] == "closed"
    assert statuses[ids["plan_open_position"]] == "active"
    assert statuses[ids["plan_abandoned"]] == "abandoned"
    assert statuses[ids["plan_draft_unlinked"]] == "draft"
    assert statuses[ids["plan_portfolio_mismatch"]] == "active"

    with get_db() as c, c.cursor() as cur:
        cur.execute("SELECT trade_plan_id, source, field, before_value, after_value FROM trade_plan_audit_log")
        audit = [dict(r) for r in cur.fetchall()]
    assert len(audit) == 1
    assert str(audit[0]["trade_plan_id"]) == ids["plan_to_close"]
    assert (audit[0]["source"], audit[0]["field"], audit[0]["before_value"], audit[0]["after_value"]) == (
        "backfill-st11", "status", "active", "closed")


@needs_pg
def test_backfill_is_idempotent(scratch_db):
    database, get_db = scratch_db
    _seed(get_db)
    assert len(database.backfill_closed_position_trade_plans()) == 1
    before = _statuses(get_db)

    assert database.backfill_closed_position_trade_plans() == []
    assert _statuses(get_db) == before


@needs_pg
def test_down_migration_reopens_backfilled_plans_and_backfill_reapplies(scratch_db):
    """data_model.md DS-41 Down Migration, then the Up Migration again."""
    database, get_db = scratch_db
    ids = _seed(get_db)
    database.backfill_closed_position_trade_plans()

    with get_db() as c, c.cursor() as cur:
        cur.execute("""
            UPDATE trade_plans
            SET status = 'active', updated_at = NOW()
            WHERE id IN (
              SELECT trade_plan_id FROM trade_plan_audit_log
              WHERE source = 'backfill-st11' AND field = 'status'
            )
        """)
    statuses = _statuses(get_db)
    assert statuses[ids["plan_to_close"]] == "active"
    # Rows the backfill never touched are not reopened.
    assert statuses[ids["plan_abandoned"]] == "abandoned"

    assert database.backfill_closed_position_trade_plans() == [ids["plan_to_close"]]
    assert _statuses(get_db)[ids["plan_to_close"]] == "closed"
