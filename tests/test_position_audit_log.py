"""
BLG-BE-73 regression tests (ST-06, EPIC-06, v7.9).

Audit trail for manual position overrides — the three genuinely
user-initiated, manual PATCH endpoints that sit outside the automated
trade lifecycle (note, tags, mark-reviewed) each write a
position_audit_log entry recording the before/after value. Core
trade/financial fields (entry_price, shares, stop) have no manual-override
endpoint in this product (confirmed via Financial Reporting & Records
Owner scope decision, recorded in execution_state.json for this story) and
are out of scope.
"""
import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

import services.position_service as position_service  # noqa: E402

# conftest.py replaces sys.modules["database"] (session-wide, process-global)
# with an auto-derived stub whose function bodies are bare MagicMocks — see
# tests/conftest.py and tests/test_claude_audit_log_filters.py's identical
# convention. Loading a private, independent copy of the real module via
# importlib means TestPositionAuditLogDatabaseFunctions below never touches
# sys.modules["database"] and exercises the real create_position_audit_log_entry
# logic rather than a MagicMock stand-in.
_db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'database.py')
_spec = importlib.util.spec_from_file_location('database_real_for_position_audit_log_test', _db_path)
_real_database = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real_database)


class _PatchHelper:
    def setup_method(self):
        self._patches = []

    def teardown_method(self):
        for p in self._patches:
            p.stop()

    def _patch(self, name, **kwargs):
        p = patch.object(position_service, name, **kwargs)
        self._patches.append(p)
        return p.start()


class TestUpdateNoteAuditLog(_PatchHelper):
    def test_update_note_writes_audit_entry_with_before_after(self):
        self._patch("get_position", return_value={"id": "pos-1", "entry_note": "old note"})
        self._patch("update_position_note", return_value={"id": "pos-1", "entry_note": "new note"})
        audit_mock = self._patch("create_position_audit_log_entry")

        position_service.update_note("pos-1", "new note")

        audit_mock.assert_called_once_with("pos-1", "note", "entry_note", "old note", "new note")

    def test_update_note_raises_before_writing_audit_entry_if_position_missing(self):
        self._patch("get_position", return_value=None)
        audit_mock = self._patch("create_position_audit_log_entry")

        try:
            position_service.update_note("missing-pos", "new note")
            assert False, "expected ValueError"
        except ValueError:
            pass

        audit_mock.assert_not_called()


class TestUpdateTagsAuditLog(_PatchHelper):
    def test_update_tags_writes_audit_entry_with_before_after(self):
        self._patch("get_position", return_value={"id": "pos-1", "tags": ["old-tag"]})
        self._patch("update_position_tags", return_value={"id": "pos-1", "tags": ["new-tag"]})
        audit_mock = self._patch("create_position_audit_log_entry")

        position_service.update_tags("pos-1", ["new-tag"])

        audit_mock.assert_called_once_with("pos-1", "tags", "tags", ["old-tag"], ["new-tag"])


class TestMarkPositionReviewedAuditLog(_PatchHelper):
    def test_mark_reviewed_writes_audit_entry_with_before_after(self):
        self._patch("get_position", return_value={"id": "pos-1", "last_reviewed_at": None})
        self._patch("db_mark_position_reviewed", return_value={"id": "pos-1", "last_reviewed_at": "2026-07-27T12:00:00"})
        audit_mock = self._patch("create_position_audit_log_entry")

        position_service.mark_position_reviewed("pos-1")

        audit_mock.assert_called_once_with(
            "pos-1", "mark-reviewed", "last_reviewed_at", None, "2026-07-27T12:00:00"
        )

    def test_mark_reviewed_raises_before_writing_audit_entry_if_position_missing(self):
        self._patch("get_position", return_value=None)
        audit_mock = self._patch("create_position_audit_log_entry")

        try:
            position_service.mark_position_reviewed("missing-pos")
            assert False, "expected ValueError"
        except ValueError:
            pass

        audit_mock.assert_not_called()


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


class TestPositionAuditLogDatabaseFunctions:
    """Exercises the real database.py position_audit_log functions (loaded
    independently of the process-global stub — see module docstring above)."""

    def test_create_position_audit_log_entry_writes_expected_row(self):
        conn, cur = _make_conn_cur()
        with patch.object(_real_database, "get_db", return_value=conn):
            _real_database.create_position_audit_log_entry(
                "pos-1", "note", "entry_note", "old note", "new note"
            )

        insert_call = [c for c in cur.execute.call_args_list if "INSERT INTO position_audit_log" in c.args[0]]
        assert len(insert_call) == 1
        params = insert_call[0].args[1]
        assert params == ("pos-1", "note", "entry_note", "old note", "new note")

    def test_create_position_audit_log_entry_does_not_raise_on_db_failure(self):
        with patch.object(_real_database, "get_db", side_effect=Exception("db unavailable")):
            # Fail-open: must not raise, matching create_claude_audit_entry's convention.
            _real_database.create_position_audit_log_entry("pos-1", "note", "entry_note", "old", "new")
