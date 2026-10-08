"""
ST-14 (BLG-BE-147, EPIC-02, v9.11) — GET /positions/grace-period-alerts selects
on calendar days since entry (grace_days_remaining <= 2), not days_in_state.

Design: docs/design/2026-10-08__release-v9.11/grace-alert-calendar-days/decision_record.md
"""
import sys
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))
import main  # noqa: E402

CLIENT = TestClient(main.app, raise_server_exceptions=False)


def _row(ticker, days_since_entry, state_entered_at):
    return {
        "id": f"pos-{ticker}", "ticker": ticker, "market": "US", "position_state": "GRACE",
        "state_entered_at": state_entered_at,
        "entry_date": date.today() - timedelta(days=days_since_entry),
        "entry_price": 100.0, "atr": 2.0, "initial_stop": 90.0,
        "trade_plan_id": None, "setup_thesis": None, "entry_rationale": None, "stop_level": None, "r_target": None,
    }


def _alerts(rows):
    cur = MagicMock()
    cur.fetchall.return_value = rows

    @contextmanager
    def fake_db():
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        yield conn

    with patch.object(main, "get_portfolio", return_value={"id": "pf-1"}), \
         patch("database.get_db", fake_db):
        resp = CLIENT.get("/positions/grace-period-alerts")
    assert resp.status_code == 200, resp.text
    return {a["ticker"]: a for a in resp.json()["data"]}


def test_day_eight_with_state_entered_today_is_included():
    now = datetime.now(timezone.utc)
    alerts = _alerts([_row("MU", 8, now)])
    assert "MU" in alerts
    assert alerts["MU"]["grace_days_remaining"] == 2
    assert alerts["MU"]["days_in_state"] == 0


def test_day_seven_is_excluded_even_with_a_long_days_in_state():
    long_ago = datetime.now(timezone.utc) - timedelta(days=9)
    assert _alerts([_row("WDC", 7, long_ago)]) == {}


def test_day_nine_and_ended_grace_are_included():
    now = datetime.now(timezone.utc)
    alerts = _alerts([_row("A", 9, now), _row("B", 10, now)])
    assert alerts["A"]["grace_days_remaining"] == 1
    assert alerts["B"]["grace_days_remaining"] == 0
