"""
ST-41 (BLG-OPS-186, EPIC-06, v9.14) — the daily AI cost check covers the last
hours of the day.

ai-daily-cost-check.yml runs at 00:15, 06:15, 12:15 and 18:15 UTC, and the
check summed today's spend only, so spend after the day's last run was never
compared with that day's threshold: the 00:15 run had already started a new
day. Every call now also checks the previous UTC day's final total.

- AC 1: spend between the last run and midnight is checked against its own
  day's threshold (and the alert names that day).
- AC 2: the day-boundary case — the real get_daily_ai_cost() query bounds,
  run against an in-memory claude_audit_log with rows either side of midnight.
"""
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    import database as real_database  # noqa: E402

TODAY = date(2026, 10, 30)
YESTERDAY = date(2026, 10, 29)
NOW = datetime(2026, 10, 30, 0, 15, tzinfo=timezone.utc)  # the first run of the day


class _FakeAuditLog:
    """claude_audit_log rows; answers get_daily_ai_cost()'s query using the
    [day, day + 1) bounds it passes, as Postgres would for a UTC day."""

    def __init__(self, rows):
        self.rows = rows  # (generated_at, cost_usd)
        self.sql = []

    def get_db(self):
        log = self
        cur = MagicMock()

        def execute(sql, params=None):
            log.sql.append(sql)
            start = datetime.fromisoformat(params[0]).replace(tzinfo=timezone.utc)
            end = start + timedelta(days=1)
            hits = [c for ts, c in log.rows if start <= ts < end]
            cur.fetchone.return_value = {"total_cost": sum(hits), "request_count": len(hits)}

        cur.execute.side_effect = execute
        cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
        conn = MagicMock(__exit__=MagicMock(return_value=False))
        conn.__enter__ = MagicMock(return_value=conn)
        conn.cursor.return_value = cur_ctx
        return conn


def _utc(day, hh, mm):
    return datetime(day.year, day.month, day.day, hh, mm, tzinfo=timezone.utc)


# Yesterday: $0.40 by the 18:15 run (under $1.00), then $0.80 more after it.
ROWS = [
    (_utc(YESTERDAY, 9, 0), 0.40),
    (_utc(YESTERDAY, 20, 30), 0.50),
    (_utc(YESTERDAY, 23, 59), 0.30),
    (_utc(TODAY, 0, 1), 0.05),
]


class _FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return NOW if tz else NOW.replace(tzinfo=None)


def _run_check(rows, last_fingerprint=None, fail_first_send=False):
    """Run check_and_alert_daily_cost() at NOW against the real query and
    an in-memory audit log. Returns (result, alert messages, fingerprints)."""
    import database as stub
    from services.gemini_service import check_and_alert_daily_cost

    log = _FakeAuditLog(rows)
    sent, recorded = [], []
    state = {"fp": last_fingerprint}

    def real_query(day=None):
        with patch.object(real_database, "get_db", side_effect=log.get_db), \
             patch.object(real_database, "ensure_claude_audit_log_table"):
            return real_database.get_daily_ai_cost(day)

    def record(key, fp):
        recorded.append((key, fp))
        state["fp"] = fp

    calls = {"n": 0}

    def urlopen(url, timeout=None):
        calls["n"] += 1
        if fail_first_send and calls["n"] == 1:
            raise OSError("telegram unreachable")
        sent.append(parse_qs(urlparse(url).query)["text"][0])
        return MagicMock()

    with patch.object(stub, "get_daily_ai_cost", side_effect=real_query), \
         patch.object(stub, "ensure_scheduled_alert_dedup_table"), \
         patch.object(stub, "get_last_alert_fingerprint", side_effect=lambda key: state["fp"]), \
         patch.object(stub, "record_alert_fingerprint", side_effect=record), \
         patch("datetime.datetime", _FrozenDatetime), \
         patch("config.TELEGRAM_BOT_TOKEN", "tok"), patch("config.TELEGRAM_CHAT_ID", "123"), \
         patch("urllib.request.urlopen", side_effect=urlopen):
        result = check_and_alert_daily_cost(threshold_usd=1.00)
    return result, sent, recorded, log


class TestQueryBounds:
    def test_a_day_sums_its_own_rows_only(self):
        log = _FakeAuditLog(ROWS)
        with patch.object(real_database, "get_db", side_effect=log.get_db), \
             patch.object(real_database, "ensure_claude_audit_log_table"):
            y = real_database.get_daily_ai_cost(YESTERDAY.isoformat())
            t = real_database.get_daily_ai_cost(TODAY.isoformat())
        assert round(y["total_cost_usd"], 6) == 1.2 and y["request_count"] == 3
        assert round(t["total_cost_usd"], 6) == 0.05 and t["request_count"] == 1

    def test_query_has_an_upper_bound_and_is_utc(self):
        log = _FakeAuditLog([])
        with patch.object(real_database, "get_db", side_effect=log.get_db), \
             patch.object(real_database, "ensure_claude_audit_log_table"):
            real_database.get_daily_ai_cost(TODAY.isoformat())
        sql = log.sql[0]
        assert "generated_at <" in sql and "AT TIME ZONE 'UTC'" in sql
        assert "CURRENT_DATE" not in sql


class TestDayBoundary:
    def test_spend_after_the_last_run_alerts_for_its_own_day(self):
        result, sent, recorded, _ = _run_check(ROWS)
        prev = result["previous_day"]
        assert prev["date"] == YESTERDAY.isoformat()
        assert round(prev["total_cost_usd"], 6) == 1.2 and prev["request_count"] == 3
        assert prev["threshold_exceeded"] is True and prev["alert_sent"] is True
        assert len(sent) == 1 and f"Date: {YESTERDAY.isoformat()}" in sent[0]
        assert recorded == [("daily_cost_alert", YESTERDAY.isoformat())]
        # Today's own figures are unaffected by yesterday's late spend.
        assert round(result["total_cost_usd"], 6) == 0.05
        assert result["threshold_exceeded"] is False and result["alert_sent"] is False

    def test_today_still_alerts_after_yesterdays_late_alert(self):
        rows = ROWS + [(_utc(TODAY, 0, 10), 1.00)]
        result, sent, recorded, _ = _run_check(rows)
        assert [m.split("\n")[1] for m in sent] == [f"Date: {YESTERDAY}", f"Date: {TODAY}"]
        assert recorded == [("daily_cost_alert", str(YESTERDAY)), ("daily_cost_alert", str(TODAY))]
        assert result["alert_sent"] is True and result["previous_day"]["alert_sent"] is True

    def test_yesterday_is_not_alerted_twice(self):
        # Yesterday's alert already went out (at its 18:15 run, or at an earlier
        # run today): no second message for it.
        result, sent, recorded, _ = _run_check(ROWS, last_fingerprint=YESTERDAY.isoformat())
        assert sent == [] and recorded == []
        assert result["previous_day"]["threshold_exceeded"] is True
        assert result["previous_day"]["alert_sent"] is False

    def test_an_alert_for_today_also_covers_yesterday(self):
        # The stored fingerprint is the latest alerted day; yesterday was
        # checked (oldest first) before today was alerted.
        _, sent, _, _ = _run_check(ROWS, last_fingerprint=TODAY.isoformat())
        assert sent == []

    def test_a_failed_previous_day_send_is_retried_not_superseded_by_today(self):
        # Both days are over the threshold and yesterday's message fails to
        # send. Today is not alerted on this run, so the fingerprint does not
        # move past yesterday; the next run sends yesterday, then today.
        rows = ROWS + [(_utc(TODAY, 0, 10), 1.00)]
        result, sent, recorded, _ = _run_check(rows, fail_first_send=True)
        assert sent == [] and recorded == []
        assert result["previous_day"]["alert_sent"] is False and result["alert_sent"] is False
        result, sent, recorded, _ = _run_check(rows)
        assert [m.split("\n")[1] for m in sent] == [f"Date: {YESTERDAY}", f"Date: {TODAY}"]

    def test_under_threshold_on_both_days_sends_nothing(self):
        rows = [(_utc(YESTERDAY, 23, 0), 0.40), (_utc(TODAY, 0, 5), 0.10)]
        result, sent, _, _ = _run_check(rows)
        assert sent == []
        assert result["previous_day"]["threshold_exceeded"] is False

    def test_a_failed_previous_day_query_is_an_error(self):
        from services.gemini_service import check_and_alert_daily_cost
        calls = []

        def failing(day=None):
            calls.append(day)
            raise RuntimeError("db down")

        with patch("database.get_daily_ai_cost", side_effect=failing):
            result = check_and_alert_daily_cost(threshold_usd=1.00)
        assert result["status"] == "error" and result["error"] == "cost_query_failed"
        assert len(calls) == 1


def test_router_returns_previous_day():
    with real_database_imports():
        from fastapi.testclient import TestClient
        import main
    client = TestClient(main.app, raise_server_exceptions=False)
    payload = {"status": "ok", "total_cost_usd": 0.0, "request_count": 0, "threshold_usd": 1.0,
               "threshold_exceeded": False, "alert_sent": False,
               "previous_day": {"date": "2026-10-29", "total_cost_usd": 1.2, "request_count": 3,
                                "threshold_exceeded": True, "alert_sent": True}}
    with patch("services.gemini_service.check_and_alert_daily_cost", return_value=payload):
        resp = client.post("/ai/check-daily-cost")
    if resp.status_code == 401:
        pytest.skip("API key auth active in this environment")
    assert resp.status_code == 200
    assert resp.json()["previous_day"]["alert_sent"] is True
