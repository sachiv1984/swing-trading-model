"""
ST-04 (BLG-FEAT-98, EPIC-01, v9.6): Reflection reminder — backend unit tests

Design: docs/design/2026-09-21__release-v9.6/reflection-reminder/decision_record.md
Contract: docs/specs/api_contracts/alerts_endpoints.md (reflection_reminder alert type)

No database or network calls — all I/O is mocked. NOTE: the SQL text is asserted structurally
(parameters, required clauses) but is not executed against a real Postgres in this suite
(no live database in the sandbox — SBX-NO-LIVE-DB); see qa_evidence_EPIC-01.md.

Coverage:
  - _evaluate_reflection_reminders: 48h delay + look-back parameters, no-reflection and
    at-most-one-reminder-per-trade filters, feed row always created, delivery governed by
    the preference (default OFF), concurrent-run ON CONFLICT no-op, failure isolation.
  - preference model: reflection_reminder is a preference type only (not a rule type),
    default OFF, seeded for already-seeded portfolios, accepted by update_preferences.
  - database.upsert_trade_reflection: auto-marks the trade's reminder read, isolated by a
    SAVEPOINT so it cannot fail the reflection save.
"""

import importlib.util as _ilu
import json
import sys
import types
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Database stub is registered by tests/conftest.py (BLG-QA-20). config/utils stubs are scoped to
# the single exec_module call via patch.dict (same pattern as tests/test_price_alerts_service.py).
_config_stub = types.ModuleType("config")
_config_stub.DEFAULT_MIN_HOLD_DAYS = 10
_config_stub.TELEGRAM_BOT_TOKEN = ""
_config_stub.TELEGRAM_CHAT_ID = ""
_pricing_stub = types.ModuleType("utils.pricing")
_pricing_stub.check_market_regime = MagicMock()
_pricing_stub.get_current_price = MagicMock()
_utils_stub = types.ModuleType("utils")
_utils_stub.pricing = _pricing_stub

_spec = _ilu.spec_from_file_location(
    "alerts_service_st04",
    Path(__file__).parent.parent / "backend" / "services" / "alerts_service.py",
)
alerts_service = _ilu.module_from_spec(_spec)
with patch.dict(sys.modules, {"config": _config_stub, "utils": _utils_stub, "utils.pricing": _pricing_stub}):
    _spec.loader.exec_module(alerts_service)

_evaluate = alerts_service._evaluate_reflection_reminders

# Private, isolated copy of the real backend/database.py (shared_standards.md §18): never
# touches sys.modules["database"].
_db_spec = _ilu.spec_from_file_location(
    "database_st04_private",
    Path(__file__).parent.parent / "backend" / "database.py",
)
real_database = _ilu.module_from_spec(_db_spec)
with patch.dict("os.environ", {"DATABASE_URL": "postgresql://user:pw@localhost:5432/dummy"}):
    _db_spec.loader.exec_module(real_database)

PORTFOLIO = "pf-1"
TRADE_A = "11111111-1111-1111-1111-111111111111"
TRADE_B = "22222222-2222-2222-2222-222222222222"


def _cur(candidates, insert_results=None):
    """MagicMock cursor: SELECT candidates -> fetchall; each INSERT ... RETURNING -> fetchone."""
    cur = MagicMock()
    cur.fetchall.return_value = candidates
    results = list(insert_results if insert_results is not None else [{"id": f"notif-{i}"} for i in range(len(candidates))])
    cur.fetchone.side_effect = results
    return cur


def _sql_calls(cur):
    return [(c.args[0], c.args[1] if len(c.args) > 1 else None) for c in cur.execute.call_args_list]


class TestEvaluateReflectionReminders(unittest.TestCase):

    def test_no_candidates_creates_nothing_and_releases_savepoint(self):
        cur = _cur([])
        enqueue = MagicMock()
        out = _evaluate(cur, PORTFOLIO, {"reflection_reminder": True}, enqueue)
        self.assertEqual(out["candidates"], 0)
        self.assertEqual(out["notifications_created"], 0)
        enqueue.assert_not_called()
        statements = [s for s, _ in _sql_calls(cur)]
        self.assertEqual(statements[0], "SAVEPOINT reflection_reminders")
        self.assertEqual(statements[-1], "RELEASE SAVEPOINT reflection_reminders")
        self.assertFalse(any("INSERT INTO notifications" in s for s in statements))

    def test_query_parameters_encode_48h_delay_and_bounded_lookback(self):
        cur = _cur([])
        _evaluate(cur, PORTFOLIO, {}, MagicMock())
        select_sql, params = _sql_calls(cur)[1]
        self.assertEqual(params, (PORTFOLIO, 48, 30))
        self.assertIn("<= NOW() - (%s * INTERVAL '1 hour')", select_sql)
        self.assertIn(">= NOW() - (%s * INTERVAL '1 day')", select_sql)
        self.assertEqual(alerts_service.REFLECTION_REMINDER_DELAY_HOURS, 48)

    def test_query_excludes_trades_with_a_reflection_or_an_existing_reminder(self):
        cur = _cur([])
        _evaluate(cur, PORTFOLIO, {}, MagicMock())
        select_sql, _ = _sql_calls(cur)[1]
        self.assertIn("NOT EXISTS", select_sql)
        self.assertIn("FROM trade_reflections tr WHERE tr.trade_id = th.id", select_sql)
        # any existing reminder (read or unread) suppresses a new one — "at most one, ever"
        self.assertIn("n.alert_type = 'reflection_reminder'", select_sql)
        self.assertIn("n.context->>'trade_id' = th.id::text", select_sql)
        # close timestamp = when the closure was recorded, not the (back-datable) exit_date
        self.assertIn("COALESCE(th.created_at, th.exit_date::timestamp)", select_sql)

    def test_feed_row_created_but_delivery_not_enqueued_when_preference_off(self):
        cur = _cur([{"id": TRADE_A, "ticker": "NVDA", "exit_date": date(2026, 9, 17)}])
        enqueue = MagicMock()
        out = _evaluate(cur, PORTFOLIO, {"reflection_reminder": False}, enqueue)
        self.assertEqual(out["notifications_created"], 1)
        self.assertEqual(out["delivery_tasks_enqueued"], 0)
        enqueue.assert_not_called()

    def test_default_preference_is_off_when_key_missing(self):
        cur = _cur([{"id": TRADE_A, "ticker": "NVDA", "exit_date": date(2026, 9, 17)}])
        enqueue = MagicMock()
        _evaluate(cur, PORTFOLIO, {}, enqueue)
        enqueue.assert_not_called()
        self.assertFalse(alerts_service.PREFERENCE_DEFAULTS["reflection_reminder"])

    def test_delivery_enqueued_only_when_preference_on(self):
        cur = _cur([{"id": TRADE_A, "ticker": "NVDA", "exit_date": date(2026, 9, 17)}], [{"id": "notif-9"}])
        enqueue = MagicMock()
        out = _evaluate(cur, PORTFOLIO, {"reflection_reminder": True}, enqueue)
        enqueue.assert_called_once_with("notif-9")
        self.assertEqual(out["delivery_tasks_enqueued"], 1)

    def test_notification_content_matches_the_design_record(self):
        cur = _cur([{"id": TRADE_A, "ticker": "NVDA", "exit_date": date(2026, 9, 17)}])
        _evaluate(cur, PORTFOLIO, {}, MagicMock())
        insert_sql, params = [c for c in _sql_calls(cur) if "INSERT INTO notifications" in c[0]][0]
        portfolio, title, message, context_json = params
        self.assertEqual(portfolio, PORTFOLIO)
        self.assertEqual(title, "Reflection Reminder — NVDA")
        self.assertEqual(message, "NVDA closed on 2026-09-17. Take a few minutes to record what you learned.")
        self.assertEqual(json.loads(context_json), {"trade_id": TRADE_A, "ticker": "NVDA", "exit_date": "2026-09-17"})
        self.assertIn("ON CONFLICT ((context->>'trade_id')) WHERE alert_type = 'reflection_reminder'", insert_sql)
        self.assertIn("DO NOTHING", insert_sql)

    def test_one_reminder_per_candidate_trade(self):
        cur = _cur([
            {"id": TRADE_A, "ticker": "NVDA", "exit_date": date(2026, 9, 17)},
            {"id": TRADE_B, "ticker": "AAPL", "exit_date": date(2026, 9, 18)},
        ])
        out = _evaluate(cur, PORTFOLIO, {}, MagicMock())
        inserts = [c for c in _sql_calls(cur) if "INSERT INTO notifications" in c[0]]
        self.assertEqual(len(inserts), 2)
        self.assertEqual(out["notifications_created"], 2)
        self.assertEqual({json.loads(p[3])["trade_id"] for _, p in inserts}, {TRADE_A, TRADE_B})

    def test_concurrent_run_conflict_is_a_silent_no_op(self):
        # ON CONFLICT DO NOTHING ... RETURNING yields no row -> not counted, nothing enqueued
        cur = _cur([{"id": TRADE_A, "ticker": "NVDA", "exit_date": date(2026, 9, 17)}], [None])
        enqueue = MagicMock()
        out = _evaluate(cur, PORTFOLIO, {"reflection_reminder": True}, enqueue)
        self.assertEqual(out["notifications_created"], 0)
        enqueue.assert_not_called()

    def test_failure_is_isolated_and_rolls_back_to_the_savepoint(self):
        cur = MagicMock()
        state = {"n": 0}

        def execute(sql, params=None):
            state["n"] += 1
            if sql.strip().startswith("SELECT th.id"):
                raise RuntimeError("relation trade_reflections does not exist")

        cur.execute.side_effect = execute
        out = _evaluate(cur, PORTFOLIO, {}, MagicMock())  # must not raise
        self.assertIn("trade_reflections", out["error"])
        self.assertEqual(out["notifications_created"], 0)
        statements = [c.args[0] for c in cur.execute.call_args_list]
        self.assertIn("ROLLBACK TO SAVEPOINT reflection_reminders", statements)


class TestPreferenceModel(unittest.TestCase):

    def test_reflection_reminder_is_a_preference_type_not_a_rule_type(self):
        # POST /alerts/rules validates against ALERT_TYPES — the reminder has no rule.
        self.assertNotIn("reflection_reminder", alerts_service.ALERT_TYPES)
        self.assertIn("reflection_reminder", alerts_service.PREFERENCE_TYPES)
        self.assertEqual(len(alerts_service.PREFERENCE_TYPES), len(alerts_service.ALERT_TYPES) + 1)

    def test_defaults_existing_types_on_new_type_off(self):
        d = alerts_service.PREFERENCE_DEFAULTS
        for t in alerts_service.ALERT_TYPES:
            self.assertTrue(d[t], t)
        self.assertFalse(d["reflection_reminder"])

    def test_seed_inserts_every_preference_type_with_its_default_and_never_overwrites(self):
        cur = MagicMock()
        alerts_service._seed_preferences(PORTFOLIO, cur)
        calls = [(c.args[1][1], c.args[1][2]) for c in cur.execute.call_args_list]
        self.assertEqual(dict(calls)["reflection_reminder"], False)
        self.assertEqual(dict(calls)["stop_loss_approach"], True)
        self.assertEqual(len(calls), len(alerts_service.PREFERENCE_TYPES))
        for c in cur.execute.call_args_list:
            self.assertIn("ON CONFLICT (portfolio_id, alert_type) DO NOTHING", c.args[0])

    def _run_get_preferences(self, existing_count):
        cur = MagicMock()
        cur.fetchone.return_value = {"cnt": existing_count}
        cur.fetchall.return_value = [{"alert_type": "reflection_reminder", "email_enabled": False}]
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        ctx = MagicMock()
        ctx.__enter__.return_value = conn
        with patch.object(alerts_service, "get_db", return_value=ctx), \
             patch.object(alerts_service, "_seed_preferences") as seed:
            out = alerts_service.get_preferences(PORTFOLIO)
        return out, seed

    def test_get_preferences_backfills_the_new_row_for_an_already_seeded_portfolio(self):
        out, seed = self._run_get_preferences(existing_count=4)  # pre-v9.6 portfolio: 4 rows
        seed.assert_called_once()
        self.assertEqual(out["preferences"], [{"alert_type": "reflection_reminder", "email_enabled": False}])

    def test_get_preferences_does_not_reseed_when_complete(self):
        _, seed = self._run_get_preferences(existing_count=len(alerts_service.PREFERENCE_TYPES))
        seed.assert_not_called()

    def test_update_preferences_accepts_reflection_reminder_and_rejects_unknown(self):
        cur = MagicMock()
        cur.fetchall.return_value = []
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        ctx = MagicMock()
        ctx.__enter__.return_value = conn
        with patch.object(alerts_service, "get_db", return_value=ctx):
            alerts_service.update_preferences(PORTFOLIO, {"reflection_reminder": {"email_enabled": True}})
        self.assertTrue(any(c.args[1] == (PORTFOLIO, "reflection_reminder", True)
                            for c in cur.execute.call_args_list if len(c.args) > 1))
        with self.assertRaises(ValueError):
            alerts_service.update_preferences(PORTFOLIO, {"not_a_type": {"email_enabled": True}})

    def test_email_label_exists_for_the_new_type(self):
        notif = {"alert_type": "reflection_reminder", "title": "Reflection Reminder — NVDA",
                 "message": "m", "created_at": "2026-09-19"}
        _, html = alerts_service._build_email(notif)
        self.assertIn("Reflection Reminder", html)


class TestEnsureTablesMigration(unittest.TestCase):
    """ensure_alerts_tables(): CHECK extension for the two alert_type constraints + unique index."""

    NOTIF_OK = {"def": "CHECK (alert_type IN ('custom_price_alert', 'reflection_reminder'))"}

    def _run(self, pref_checks):
        cur = MagicMock()
        cur.fetchone.return_value = self.NOTIF_OK
        cur.fetchall.return_value = pref_checks
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        ctx = MagicMock()
        ctx.__enter__.return_value = conn
        with patch.object(alerts_service, "get_db", return_value=ctx):
            alerts_service.ensure_alerts_tables()
        return [c.args[0] for c in cur.execute.call_args_list]

    def test_old_four_type_preferences_check_is_replaced_even_if_named_differently(self):
        old = {"conname": "notification_preferences_type_chk", "def": "CHECK (alert_type IN ('stop_loss_approach'))"}
        sql = self._run([old])
        self.assertTrue(any('DROP CONSTRAINT IF EXISTS "notification_preferences_type_chk"' in q for q in sql))
        add = [q for q in sql if "ADD CONSTRAINT notification_preferences_alert_type_check" in q]
        self.assertEqual(len(add), 1)
        self.assertIn("'reflection_reminder'", add[0])

    def test_already_extended_preferences_check_is_left_alone(self):
        ok = {"conname": "notification_preferences_alert_type_check", "def": "CHECK (alert_type IN ('reflection_reminder'))"}
        sql = self._run([ok])
        self.assertFalse(any("notification_preferences DROP CONSTRAINT" in q or
                             "ADD CONSTRAINT notification_preferences_alert_type_check" in q for q in sql))

    def test_partial_unique_index_enforces_one_reminder_per_trade(self):
        sql = self._run([])
        idx = [q for q in sql if "uq_notifications_reflection_reminder_trade" in q]
        self.assertEqual(len(idx), 1)
        self.assertIn("CREATE UNIQUE INDEX IF NOT EXISTS", idx[0])
        self.assertIn("((context->>'trade_id'))", idx[0])
        self.assertIn("WHERE alert_type = 'reflection_reminder'", idx[0])

    def test_notifications_check_not_touched_when_already_extended(self):
        sql = self._run([])
        self.assertFalse(any("notifications DROP CONSTRAINT" in q for q in sql))


class TestUpsertReflectionAutoReadsReminder(unittest.TestCase):

    def _run(self, execute_side_effect=None):
        cur = MagicMock()
        cur.fetchone.side_effect = [{"id": TRADE_A}, {"id": "refl-1", "trade_id": TRADE_A}]
        if execute_side_effect:
            cur.execute.side_effect = execute_side_effect
        conn = MagicMock()
        conn.cursor.return_value.__enter__.return_value = cur
        ctx = MagicMock()
        ctx.__enter__.return_value = conn
        with patch.object(real_database, "get_db", return_value=ctx):
            row = real_database.upsert_trade_reflection(TRADE_A, {"key_takeaway": "x"})
        return row, cur

    def test_marks_only_this_trades_unread_reminder_read(self):
        row, cur = self._run()
        self.assertEqual(row["id"], "refl-1")
        updates = [c for c in cur.execute.call_args_list if "UPDATE notifications" in c.args[0]]
        self.assertEqual(len(updates), 1)
        sql, params = updates[0].args
        self.assertIn("alert_type = 'reflection_reminder'", sql)
        self.assertIn("context->>'trade_id' = %s", sql)
        self.assertIn("read = FALSE", sql)
        self.assertEqual(params, (TRADE_A,))

    def test_reminder_update_failure_never_fails_the_reflection_save(self):
        def boom(sql, params=None):
            if "UPDATE notifications" in sql:
                raise RuntimeError('relation "notifications" does not exist')
        row, cur = self._run(execute_side_effect=boom)
        self.assertEqual(row["id"], "refl-1")  # the reflection itself was still returned
        self.assertIn("ROLLBACK TO SAVEPOINT reflection_reminder_read",
                      [c.args[0] for c in cur.execute.call_args_list])


if __name__ == "__main__":
    unittest.main()
