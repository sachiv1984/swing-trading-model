"""
BLG-BE-58 regression tests (ST-08, EPIC-02, v8.8).

Append-only position_state_history table, logging lifecycle state
transitions alongside (not instead of) the existing state_history JSONB
column on positions (DS-05, v2.6). No behavioural change to
compute_position_state() or the rest of the state machine — this only adds
a second, normalized persistence path for genuine transitions.
"""
import importlib.util
import os
import sys
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.position_lifecycle_service as lifecycle_service  # noqa: E402

# conftest.py replaces sys.modules["database"] (session-wide, process-global)
# with an auto-derived stub whose function bodies are bare MagicMocks — see
# tests/test_position_audit_log.py's identical convention. Loading a private,
# independent copy of the real module via importlib means
# TestPositionStateHistoryDatabaseFunctions below never touches
# sys.modules["database"] and exercises the real
# create_position_state_history_entry logic rather than a MagicMock stand-in.
_db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
_spec = importlib.util.spec_from_file_location('database_real_for_position_state_history_test', _db_path)
_real_database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real_database)


def _raw_position_row(position_id="pos-1", position_state="LOSING", atr=2.0):
    """Tuned so compute_position_state() returns PROFITABLE — a transition
    away from the stored LOSING state, when position_state=LOSING (default)."""
    entry_date = (date.today() - timedelta(days=30)).isoformat()
    return {
        "id": position_id,
        "entry_price": 100.0,
        "current_price_native": 103.0,  # > entry + 0.5*atr(2.0)=101 -> PROFITABLE
        "atr": atr,
        "entry_date": entry_date,
        "initial_stop": 90.0,
        "position_state": position_state,
        "state_history": [{"state": position_state, "entered_at": "2026-01-01T00:00:00"}],
        "state_entered_at": "2026-01-01T00:00:00",
    }


class TestRefreshPositionLifecycleWritesStateHistory:
    def test_transition_writes_state_history_entry(self):
        row = _raw_position_row(position_state="LOSING")  # -> PROFITABLE = transition
        with patch.object(lifecycle_service, "update_position_lifecycle_state",
                           return_value={"position_state": "PROFITABLE"}) as mock_update, \
             patch.object(lifecycle_service, "create_position_state_history_entry") as mock_history:
            lifecycle_service.refresh_position_lifecycle("pos-1", prefetched_position=row)

        mock_update.assert_called_once()
        mock_history.assert_called_once()
        args = mock_history.call_args.args
        assert args[0] == "pos-1"
        assert args[1] == "LOSING"    # from_state
        assert args[2] == "PROFITABLE"  # to_state

    def test_no_transition_does_not_write_state_history_entry(self):
        row = _raw_position_row(position_state="PROFITABLE")  # already PROFITABLE -> no transition
        with patch.object(lifecycle_service, "update_position_lifecycle_state") as mock_update, \
             patch.object(lifecycle_service, "create_position_state_history_entry") as mock_history:
            lifecycle_service.refresh_position_lifecycle("pos-1", prefetched_position=row)

        mock_update.assert_not_called()
        mock_history.assert_not_called()

    def test_first_ever_state_has_null_from_state(self):
        row = _raw_position_row(position_state=None)  # no prior stored state
        with patch.object(lifecycle_service, "update_position_lifecycle_state",
                           return_value={"position_state": "PROFITABLE"}), \
             patch.object(lifecycle_service, "create_position_state_history_entry") as mock_history:
            lifecycle_service.refresh_position_lifecycle("pos-1", prefetched_position=row)

        mock_history.assert_called_once()
        args = mock_history.call_args.args
        assert args[1] is None  # from_state
        assert args[2] == "PROFITABLE"  # to_state

    def test_primary_write_runs_before_audit_write(self):
        """ST-10 (BLG-BE-100, EPIC-03, v8.9): the primary write
        (update_position_lifecycle_state) must be called before the audit
        write (create_position_state_history_entry), not after -- the two
        writes use separate DB connections/transactions, so call order is
        what prevents a phantom state_history row for a transition that
        never actually landed on `positions`."""
        row = _raw_position_row(position_state="LOSING")
        call_order = []
        with patch.object(lifecycle_service, "update_position_lifecycle_state",
                           side_effect=lambda *a, **kw: call_order.append("primary") or {"position_state": "PROFITABLE"}), \
             patch.object(lifecycle_service, "create_position_state_history_entry",
                           side_effect=lambda *a, **kw: call_order.append("audit")):
            lifecycle_service.refresh_position_lifecycle("pos-1", prefetched_position=row)

        assert call_order == ["primary", "audit"]

    def test_audit_write_not_reached_when_primary_write_raises(self):
        """AC-2: 'the audit row is not written when the primary write
        fails' -- if update_position_lifecycle_state raises, the function
        must propagate the exception and never reach the audit-write call
        (not swallow it and continue to log a phantom transition)."""
        row = _raw_position_row(position_state="LOSING")
        with patch.object(lifecycle_service, "update_position_lifecycle_state",
                           side_effect=RuntimeError("db unavailable")), \
             patch.object(lifecycle_service, "create_position_state_history_entry") as mock_history:
            with pytest.raises(RuntimeError):
                lifecycle_service.refresh_position_lifecycle("pos-1", prefetched_position=row)

        mock_history.assert_not_called()


def _make_conn_cur():
    cur = MagicMock()
    cur_ctx = MagicMock()
    cur_ctx.__enter__ = MagicMock(return_value=cur)
    cur_ctx.__exit__ = MagicMock(return_value=False)

    conn = MagicMock()
    conn.cursor.return_value = cur_ctx
    conn.__enter__ = MagicMock(return_value=conn)
    conn.__exit__ = MagicMock(return_value=False)
    return conn, cur


class TestPositionStateHistoryDatabaseFunctions:
    """Exercises the real database.py position_state_history functions
    (loaded independently of the process-global stub — see module docstring
    above)."""

    def test_create_position_state_history_entry_writes_expected_row(self):
        conn, cur = _make_conn_cur()
        with patch.object(_real_database, "get_db", return_value=conn), \
             patch.object(_real_database, "ensure_position_state_history_table"):
            _real_database.create_position_state_history_entry(
                "pos-1", "LOSING", "PROFITABLE", "2026-08-14T12:00:00"
            )

        insert_call = [c for c in cur.execute.call_args_list if "INSERT INTO position_state_history" in c.args[0]]
        assert len(insert_call) == 1
        params = insert_call[0].args[1]
        assert params == ("pos-1", "LOSING", "PROFITABLE", "2026-08-14T12:00:00")

    def test_create_position_state_history_entry_does_not_raise_on_db_failure(self):
        with patch.object(_real_database, "get_db", side_effect=Exception("db unavailable")), \
             patch.object(_real_database, "ensure_position_state_history_table"):
            # Fail-open: must not raise, matching create_position_audit_log_entry's convention.
            _real_database.create_position_state_history_entry("pos-1", "LOSING", "PROFITABLE", "2026-08-14T12:00:00")

    def test_ensure_position_state_history_table_creates_table_and_index(self):
        conn, cur = _make_conn_cur()
        with patch.object(_real_database, "get_db", return_value=conn):
            _real_database.ensure_position_state_history_table()

        statements = " ".join(c.args[0] for c in cur.execute.call_args_list)
        assert "CREATE TABLE IF NOT EXISTS position_state_history" in statements
        assert "CREATE INDEX IF NOT EXISTS idx_position_state_history_position_id" in statements
