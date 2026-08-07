"""
trade_plan_audit_log regression tests (ST-13, BLG-BE-77, EPIC-03, v8.4).

Extends the position_audit_log pattern (BLG-BE-73, v7.9) to trade_plans:
update_trade_plan() now logs one audit row per genuinely-changed field when
the plan is "post-entry" (position_id set, either before or after the
edit) -- pre-entry edits to a still-draft plan are ordinary iterative
authoring and are not logged. Non-blocking: an audit-log write failure must
never break the underlying edit it is recording.

No live database required -- verifies behaviour via a mocked get_db()
connection, following the pattern already used by
test_trade_plans_ticker_index.py / test_trade_plan_thesis_provenance.py.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

sys.modules.pop("database", None)
import database  # noqa: E402


def _mock_conn():
    mock_cursor = MagicMock()
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


def test_ensure_trade_plan_audit_log_table_creates_table_and_index():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn):
        database.ensure_trade_plan_audit_log_table()

    sql_statements = [call.args[0] for call in mock_cursor.execute.call_args_list if call.args]
    assert any("CREATE TABLE IF NOT EXISTS trade_plan_audit_log" in s for s in sql_statements)
    assert any("idx_trade_plan_audit_log_trade_plan_id" in s for s in sql_statements)


def test_create_trade_plan_audit_log_entry_inserts_row():
    mock_conn, mock_cursor = _mock_conn()
    with patch.object(database, "get_db", return_value=mock_conn), \
         patch.object(database, "ensure_trade_plan_audit_log_table"):
        database.create_trade_plan_audit_log_entry("plan-1", "post-entry-edit", "status", "active", "closed")

    insert_calls = [c for c in mock_cursor.execute.call_args_list if c.args and "INSERT INTO trade_plan_audit_log" in c.args[0]]
    assert len(insert_calls) == 1
    params = insert_calls[0].args[1]
    assert params == ("plan-1", "post-entry-edit", "status", "active", "closed")


def test_create_trade_plan_audit_log_entry_never_raises_on_failure():
    """Fail-open: an audit-log write failure must never propagate to the caller."""
    with patch.object(database, "ensure_trade_plan_audit_log_table", side_effect=Exception("db down")):
        database.create_trade_plan_audit_log_entry("plan-1", "post-entry-edit", "status", "a", "b")  # must not raise


def test_update_trade_plan_logs_audit_entry_when_post_entry():
    """Plan is linked to a position (position_id set) -- edit must be logged."""
    before_row = {"id": "plan-1", "position_id": "pos-1", "status": "active", "r_target": 2.0}
    after_row = {"id": "plan-1", "position_id": "pos-1", "status": "closed", "r_target": 2.0}

    call_state = {"n": 0}

    def fake_fetchone():
        call_state["n"] += 1
        return after_row  # UPDATE ... RETURNING * result

    mock_conn, mock_cursor = _mock_conn()
    mock_cursor.fetchone.side_effect = fake_fetchone

    audit_calls = []

    def fake_get_trade_plan_by_id(trade_plan_id, portfolio_id):
        return before_row

    def fake_audit_entry(*args, **kwargs):
        audit_calls.append(args)

    with patch.object(database, "get_db", return_value=mock_conn), \
         patch.object(database, "get_trade_plan_by_id", side_effect=fake_get_trade_plan_by_id), \
         patch.object(database, "create_trade_plan_audit_log_entry", side_effect=fake_audit_entry):
        database.update_trade_plan("plan-1", "portfolio-1", {"status": "closed"})

    assert len(audit_calls) == 1
    assert audit_calls[0] == ("plan-1", "post-entry-edit", "status", "active", "closed")


def test_update_trade_plan_does_not_log_when_pre_entry_draft():
    """Plan has no position_id (still a draft) -- edit must NOT be logged."""
    before_row = {"id": "plan-2", "position_id": None, "status": "draft"}
    after_row = {"id": "plan-2", "position_id": None, "status": "active"}

    mock_conn, mock_cursor = _mock_conn()
    mock_cursor.fetchone.return_value = after_row

    audit_calls = []

    with patch.object(database, "get_db", return_value=mock_conn), \
         patch.object(database, "get_trade_plan_by_id", return_value=before_row), \
         patch.object(database, "create_trade_plan_audit_log_entry", side_effect=lambda *a: audit_calls.append(a)):
        database.update_trade_plan("plan-2", "portfolio-1", {"status": "active"})

    assert audit_calls == []


def test_update_trade_plan_does_not_log_unchanged_fields():
    """Only genuinely-changed fields produce an audit row."""
    before_row = {"id": "plan-1", "position_id": "pos-1", "status": "active", "r_target": 2.0}
    after_row = {"id": "plan-1", "position_id": "pos-1", "status": "active", "r_target": 2.5}

    mock_conn, mock_cursor = _mock_conn()
    mock_cursor.fetchone.return_value = after_row

    audit_calls = []

    with patch.object(database, "get_db", return_value=mock_conn), \
         patch.object(database, "get_trade_plan_by_id", return_value=before_row), \
         patch.object(database, "create_trade_plan_audit_log_entry", side_effect=lambda *a: audit_calls.append(a)):
        # status included in the update payload but its value is unchanged
        database.update_trade_plan("plan-1", "portfolio-1", {"status": "active", "r_target": 2.5})

    assert len(audit_calls) == 1
    assert audit_calls[0] == ("plan-1", "post-entry-edit", "r_target", 2.0, 2.5)
