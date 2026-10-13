"""
ST-06 (BLG-OPS-183, EPIC-01, v9.12) — the daily AI cost alert counts Claude
calls.

get_daily_ai_cost() summed gemini_audit_log, which only plan and thesis
generation write, so every other Claude feature (briefing, chat, journal
summary, debrief, monthly P&L narrative) was invisible to the $1.00/day
alert. It now sums claude_audit_log only: every Claude call writes it, and
plan/thesis generation writes both tables, so reading both would count
those calls twice.

The real get_daily_ai_cost() runs against two in-memory audit tables; the
real gemini_service._log_audit() fills both for a plan-generation call.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from tests._real_database import real_database_imports  # noqa: E402

with real_database_imports():
    import database as real_database  # noqa: E402


class _FakeAuditDb:
    """Two audit tables; answers get_daily_ai_cost()'s SUM/COUNT query for
    whichever table it names, counting today's rows only."""

    COST_COLUMN = {"claude_audit_log": "cost_usd", "gemini_audit_log": "estimated_cost_usd"}

    def __init__(self):
        self.tables = {"claude_audit_log": [], "gemini_audit_log": []}
        self.queried = []

    def add(self, table, cost, generated_at=None):
        self.tables[table].append({self.COST_COLUMN[table]: cost,
                                   "generated_at": generated_at or datetime.now(timezone.utc)})

    def get_db(self):
        db = self
        cur = MagicMock()

        def execute(sql, params=None):
            table = next(t for t in db.tables if f"FROM {t}" in sql)
            db.queried.append(table)
            today = datetime.now(timezone.utc).date()
            rows = [r for r in db.tables[table] if r["generated_at"].date() >= today]
            cur.fetchone.return_value = {
                "total_cost": sum(r[db.COST_COLUMN[table]] or 0 for r in rows),
                "request_count": len(rows),
            }

        cur.execute.side_effect = execute
        cur_ctx = MagicMock(__enter__=MagicMock(return_value=cur), __exit__=MagicMock(return_value=False))
        conn = MagicMock(__exit__=MagicMock(return_value=False))
        conn.__enter__ = MagicMock(return_value=conn)
        conn.cursor.return_value = cur_ctx
        return conn


def _daily_cost(db):
    with patch.object(real_database, "get_db", side_effect=db.get_db), \
         patch.object(real_database, "ensure_claude_audit_log_table"):
        return real_database.get_daily_ai_cost()


def test_claude_audit_log_row_is_counted_in_the_daily_total():
    db = _FakeAuditDb()
    db.add("claude_audit_log", 0.0123)   # e.g. a daily briefing
    db.add("claude_audit_log", 0.0300, generated_at=datetime(2020, 1, 1, tzinfo=timezone.utc))  # not today
    result = _daily_cost(db)
    assert db.queried == ["claude_audit_log"]
    assert result == {"total_cost_usd": 0.0123, "request_count": 1}


def test_plan_generation_call_is_counted_once():
    db = _FakeAuditDb()

    def create_gemini_audit_entry(**kw):
        db.add("gemini_audit_log", kw["estimated_cost_usd"])

    def create_claude_audit_entry(**kw):
        db.add("claude_audit_log", kw["cost_usd"])

    from services import gemini_service
    stub = sys.modules["database"]
    with patch.object(stub, "create_gemini_audit_entry", side_effect=create_gemini_audit_entry), \
         patch.object(stub, "create_claude_audit_entry", side_effect=create_claude_audit_entry):
        gemini_service._log_audit("plan-1", "in", "out", SimpleNamespace(input_tokens=1000, output_tokens=500),
                                  endpoint="POST /trade-plans/generate-plan")

    # The call is in both tables, as before...
    assert len(db.tables["gemini_audit_log"]) == 1 and len(db.tables["claude_audit_log"]) == 1
    one_call_cost = db.tables["claude_audit_log"][0]["cost_usd"]
    assert one_call_cost > 0
    # ...but the daily total counts it once.
    assert _daily_cost(db) == {"total_cost_usd": one_call_cost, "request_count": 1}


def test_alert_fires_when_claude_spend_passes_the_threshold(monkeypatch):
    db = _FakeAuditDb()
    for _ in range(3):
        db.add("claude_audit_log", 0.40)   # $1.20 of Claude spend, none in gemini_audit_log

    from services.gemini_service import check_and_alert_daily_cost
    stub = sys.modules["database"]
    monkeypatch.setattr(stub, "get_daily_ai_cost", lambda: _daily_cost(db))
    monkeypatch.setattr(stub, "ensure_scheduled_alert_dedup_table", lambda: None)
    monkeypatch.setattr(stub, "get_last_alert_fingerprint", lambda key: None)
    monkeypatch.setattr(stub, "record_alert_fingerprint", lambda key, fp: None)
    with patch("config.TELEGRAM_BOT_TOKEN", "test_token"), patch("config.TELEGRAM_CHAT_ID", "123"), \
         patch("urllib.request.urlopen") as urlopen:
        result = check_and_alert_daily_cost(threshold_usd=1.00)

    assert round(result["total_cost_usd"], 6) == 1.2 and result["request_count"] == 3
    assert result["threshold_exceeded"] is True and result["alert_sent"] is True
    assert urlopen.called


def test_scheduler_workflow_calls_the_endpoint():
    wf = (Path(__file__).parent.parent / ".github" / "workflows" / "ai-daily-cost-check.yml").read_text()
    assert "schedule:" in wf and "workflow_dispatch:" in wf
    assert '"${API_URL}/ai/check-daily-cost"' in wf
