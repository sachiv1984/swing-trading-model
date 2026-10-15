"""
ST-26 (BLG-SEC-41, EPIC-04, v9.12): every settings write produces a
settings_change_log row (field, old value, new value, timestamp, request source),
and GET /settings returns the most recent save as last_change.

The write paths run through the real backend/database.py create_settings() and
update_settings() with a fake connection that records the SQL, as in
tests/test_settings_create_and_plan_snapshot.py. No database or network is touched.
"""
import re
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import load_real_database, real_database_imports  # noqa: E402

with real_database_imports():
    from fastapi.testclient import TestClient  # noqa: E402
    import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)
REAL_DB = load_real_database("database_real_for_test_settings_change_log")
ROOT = Path(__file__).parent.parent

STORED_ROW = {
    "id": "settings-1", "min_hold_days": 10, "atr_period": 14,
    "atr_multiplier_initial": Decimal("5.00"), "atr_multiplier_trailing": Decimal("2.00"),
    "default_currency": "GBP", "theme": "dark", "uk_commission": Decimal("9.95"),
    "us_commission": Decimal("0.00"), "stamp_duty_rate": Decimal("0.00500"),
    "fx_fee_rate": Decimal("0.00150"), "min_trades_for_analytics": 10,
    "default_risk_percent": Decimal("1.00"),
    "created_at": datetime(2026, 1, 1), "updated_at": datetime(2026, 1, 1),
}
LOG_INSERT = "INSERT INTO settings_change_log"


class _RecordingDb:
    """Fake get_db(): records every statement; SELECT/UPDATE/INSERT ... RETURNING return `row`."""

    def __init__(self, row, log_rows=()):
        self.executed = []
        self.row = row
        self.log_rows = list(log_rows)

    @contextmanager
    def __call__(self):
        conn = MagicMock()
        cur = MagicMock()
        cur.execute.side_effect = lambda sql, params=None: self.executed.append((sql, params))
        cur.fetchone.side_effect = lambda: dict(self.row) if self.row is not None else None
        cur.fetchall.return_value = self.log_rows
        conn.cursor.return_value.__enter__.return_value = cur
        yield conn

    def log_inserts(self):
        return [params for sql, params in self.executed if sql.startswith(LOG_INSERT)]


def _patch(body, headers=None, row=STORED_ROW):
    db = _RecordingDb(row)
    with patch.object(main, "update_settings", REAL_DB.update_settings), patch.object(REAL_DB, "get_db", db):
        response = CLIENT.patch("/settings/settings-1", json=body, headers=headers or {})
    return response, db


def _post(body, headers=None, returned_row=STORED_ROW):
    db = _RecordingDb(returned_row)
    with patch.object(main, "create_settings", REAL_DB.create_settings), patch.object(REAL_DB, "get_db", db):
        response = CLIENT.post("/settings", json=body, headers=headers or {})
    return response, db


class TestUpdateWritesLogRows:

    def test_each_changed_field_gets_a_row_with_old_new_and_source(self):
        response, db = _patch({"default_risk_percent": 1.5, "uk_commission": 7.5},
                              headers={"X-Request-Source": "settings_page"})
        assert response.status_code == 200
        rows = db.log_inserts()
        assert sorted((r[2], r[3], r[4], r[5]) for r in rows) == [
            ("default_risk_percent", "1", "1.5", "settings_page"),
            ("uk_commission", "9.95", "7.5", "settings_page"),
        ]
        assert all(r[0] == "settings-1" for r in rows)

    def test_one_save_shares_one_batch_id(self):
        _, db = _patch({"default_risk_percent": 1.5, "theme": "light"})
        batch_ids = {r[1] for r in db.log_inserts()}
        assert len(batch_ids) == 1 and re.fullmatch(r"[0-9a-f-]{36}", batch_ids.pop())

    def test_unchanged_fields_are_not_logged(self):
        # The Settings page sends every field on each save; only real changes are logged.
        _, db = _patch({"default_risk_percent": 1.0, "stamp_duty_rate": 0.005, "theme": "dark", "fx_fee_rate": 0.002})
        assert [r[2] for r in db.log_inserts()] == ["fx_fee_rate"]

    def test_no_header_is_logged_as_api(self):
        _, db = _patch({"theme": "light"})
        assert db.log_inserts()[0][5] == "api"

    def test_unknown_header_value_is_logged_as_api(self):
        _, db = _patch({"theme": "light"}, headers={"X-Request-Source": "'; DROP TABLE settings; --"})
        assert db.log_inserts()[0][5] == "api"

    def test_log_rows_are_written_in_the_same_transaction_after_the_update(self):
        _, db = _patch({"theme": "light"})
        statements = [sql.split(" ")[0] for sql, _ in db.executed]
        assert statements == ["SELECT", "UPDATE", "INSERT"]
        assert db.executed[0][0].endswith("FOR UPDATE")

    def test_missing_row_logs_nothing(self):
        response, db = _patch({"theme": "light"}, row=None)
        assert response.status_code == 500
        assert db.log_inserts() == []


class TestCreateWritesLogRows:

    def test_create_logs_every_non_null_column_with_null_old_value(self):
        response, db = _post({"theme": "dark"}, headers={"X-Request-Source": "settings_page"})
        assert response.status_code == 200
        rows = db.log_inserts()
        logged = {r[2]: (r[3], r[4], r[5]) for r in rows}
        assert "id" not in logged and "created_at" not in logged and "updated_at" not in logged
        assert logged["theme"] == (None, "dark", "settings_page")
        assert logged["stamp_duty_rate"] == (None, "0.005", "settings_page")
        assert logged["min_hold_days"] == (None, "10", "settings_page")
        assert len({r[1] for r in rows}) == 1

    def test_empty_create_still_logs_the_defaulted_row(self):
        _, db = _post({})
        assert db.executed[0][0] == "INSERT INTO settings DEFAULT VALUES RETURNING *"
        assert len(db.log_inserts()) == 12


class TestValueText:

    def test_numbers_drop_trailing_zeros_and_strings_pass_through(self):
        text = REAL_DB._settings_value_text
        assert text(Decimal("0.00500")) == "0.005"
        assert text(Decimal("10")) == "10"
        assert text(Decimal("0.00")) == "0"
        assert text(9.95) == "9.95"
        assert text(15) == "15"
        assert text("GBP") == "GBP"
        assert text(None) is None


class TestLastChange:

    def test_returns_the_latest_batch_with_all_its_changes(self):
        at = datetime(2026, 10, 15, 8, 30, tzinfo=timezone.utc)
        db = _RecordingDb(None, log_rows=[
            {"field": "default_risk_percent", "old_value": "1", "new_value": "1.5", "changed_at": at, "request_source": "settings_page"},
            {"field": "theme", "old_value": "dark", "new_value": "light", "changed_at": at, "request_source": "settings_page"},
        ])
        with patch.object(REAL_DB, "get_db", db):
            last = REAL_DB.get_last_settings_change()
        assert last == {
            "field": "default_risk_percent", "old_value": "1", "new_value": "1.5",
            "changed_at": "2026-10-15T08:30:00+00:00", "request_source": "settings_page",
            "changes": [
                {"field": "default_risk_percent", "old_value": "1", "new_value": "1.5"},
                {"field": "theme", "old_value": "dark", "new_value": "light"},
            ],
        }
        sql = db.executed[0][0]
        assert "ORDER BY changed_at DESC, id DESC LIMIT 1" in sql and sql.endswith("ORDER BY id")

    def test_none_when_nothing_is_logged(self):
        with patch.object(REAL_DB, "get_db", _RecordingDb(None)):
            assert REAL_DB.get_last_settings_change() is None

    def test_get_settings_returns_last_change_on_the_settings_object(self):
        last = {"field": "theme", "old_value": "dark", "new_value": "light", "changed_at": "2026-10-15T08:30:00+00:00",
                "request_source": "api", "changes": [{"field": "theme", "old_value": "dark", "new_value": "light"}]}
        with patch.object(main, "get_settings", return_value=[{"id": "settings-1", "theme": "light"}]), \
             patch.object(main, "get_last_settings_change", return_value=last):
            body = CLIENT.get("/settings").json()
        assert body["data"][0]["last_change"] == last

    def test_get_settings_last_change_null_when_nothing_logged(self):
        with patch.object(main, "get_settings", return_value=[{"id": "settings-1"}]), \
             patch.object(main, "get_last_settings_change", return_value=None):
            body = CLIENT.get("/settings").json()
        assert body["data"][0]["last_change"] is None


class TestMigrationRecorded:

    def test_ds33_is_in_data_model_with_the_audit_columns(self):
        doc = (ROOT / "docs" / "specs" / "data_model.md").read_text()
        section = doc[doc.index("## DS-33"):]
        for column in ("settings_id", "batch_id", "field", "old_value", "new_value",
                       "changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()", "request_source"):
            assert column in section
