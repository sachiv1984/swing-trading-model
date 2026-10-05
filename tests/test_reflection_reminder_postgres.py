"""
ST-13 (BLG-QA-189, EPIC-03, v9.9): real-Postgres integration test for the
reflection-reminder evaluation step (ST-04, BLG-FEAT-98, v9.6).

tests/test_reflection_reminder.py asserts the SQL text and parameters but never
executes them. This test runs them for real: it builds a pre-v9.6 alerts schema,
lets ensure_alerts_tables() migrate it, seeds closed trades on either side of
every eligibility boundary, and drives the real evaluate_alerts() entry point.
Asserted:
  - eligibility: 48h delay (47h no / 49h yes), 30-day look-back (29d yes / 31d no),
    reflected trades excluded, back-dated exit_date does not make a fresh closure
    eligible (created_at wins), NULL created_at falls back to exit_date, other
    portfolios' trades excluded
  - idempotence: a second run creates nothing, and the partial unique index
    uq_notifications_reflection_reminder_trade (the ON CONFLICT target) rejects a
    second reminder row for the same trade
  - rows created with the preference OFF are settled and are not re-delivered
    once the preference is later turned ON; a reminder created while it is ON is
    delivered

Phase B only: skipped when DATABASE_URL contains 'stub' (Phase A stays fully
mocked), matching tests/test_schema.py. Runs inside a dedicated schema that is
dropped before and after, so it never touches other tests' tables.
"""
import importlib.util as _ilu
import os
import sys
import types
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

psycopg2 = pytest.importorskip("psycopg2")
from psycopg2.extras import RealDictCursor  # noqa: E402

_DATABASE_URL = os.getenv("DATABASE_URL", "")
pytestmark = pytest.mark.skipif(
    "stub" in _DATABASE_URL.lower() or not _DATABASE_URL,
    reason="Phase A — DATABASE_URL is a stub; reflection-reminder integration test requires real Postgres (Phase B)",
)

SCHEMA = "st13_reflection_reminder_it"
PORTFOLIO = "11111111-1111-1111-1111-111111111111"
OTHER_PORTFOLIO = "22222222-2222-2222-2222-222222222222"

# Load a private copy of alerts_service.py (never touches sys.modules["database"] --
# shared_standards.md §18). config/utils stubs are scoped to the exec_module call, same
# as tests/test_reflection_reminder.py.
_config_stub = types.ModuleType("config")
_config_stub.DEFAULT_MIN_HOLD_DAYS = 10
_config_stub.TELEGRAM_BOT_TOKEN = ""
_config_stub.TELEGRAM_CHAT_ID = ""
_pricing_stub = types.ModuleType("utils.pricing")
_pricing_stub.check_market_regime = MagicMock()
_pricing_stub.get_current_price = MagicMock()
_utils_stub = types.ModuleType("utils")
_utils_stub.pricing = _pricing_stub
_database_stub = types.ModuleType("database")
for _name in ("get_db", "get_portfolio", "get_positions", "get_settings"):
    setattr(_database_stub, _name, MagicMock())

_spec = _ilu.spec_from_file_location(
    "alerts_service_st13_it", Path(__file__).parent.parent / "backend" / "services" / "alerts_service.py"
)
alerts_service = _ilu.module_from_spec(_spec)
with patch.dict(sys.modules, {
    "config": _config_stub, "utils": _utils_stub, "utils.pricing": _pricing_stub, "database": _database_stub,
}):
    _spec.loader.exec_module(alerts_service)


def _connect():
    conn = psycopg2.connect(_DATABASE_URL, cursor_factory=RealDictCursor)
    with conn.cursor() as cur:
        cur.execute(f"SET search_path TO {SCHEMA}")
    return conn


@contextmanager
def _schema_get_db():
    """Same contract as database.get_db (commit on success, rollback on error),
    pinned to this test's private schema."""
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# Pre-v9.6 shape: notifications/notification_preferences exist with the old alert_type
# CHECKs (no 'reflection_reminder') and without the partial unique index.
_PRE_V96_DDL = f"""
CREATE SCHEMA {SCHEMA};
SET search_path TO {SCHEMA};
CREATE TABLE portfolios (id UUID PRIMARY KEY, name TEXT);
CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), portfolio_id UUID, ticker TEXT,
    holding_days INTEGER, current_stop NUMERIC, current_price NUMERIC, entry_date DATE, status TEXT
);
CREATE TABLE trade_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    ticker TEXT NOT NULL, exit_date DATE NOT NULL, created_at TIMESTAMP
);
CREATE TABLE trade_reflections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trade_id UUID NOT NULL UNIQUE REFERENCES trade_history(id) ON DELETE CASCADE
);
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    alert_type VARCHAR(50) NOT NULL,
    title TEXT NOT NULL, message TEXT NOT NULL, context JSONB,
    read BOOLEAN NOT NULL DEFAULT FALSE, delivered BOOLEAN NOT NULL DEFAULT FALSE,
    delivery_attempted_at TIMESTAMPTZ, delivery_attempts INTEGER NOT NULL DEFAULT 0,
    delivery_error TEXT, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT notifications_alert_type_check CHECK (alert_type IN (
        'stop_loss_approach', 'grace_period_warning', 'market_regime_change',
        'daily_portfolio_summary', 'custom_price_alert'))
);
CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN (
        'stop_loss_approach', 'grace_period_warning', 'market_regime_change', 'daily_portfolio_summary')),
    email_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_notification_preferences_portfolio_type UNIQUE (portfolio_id, alert_type)
);
"""

# label -> (portfolio, created_at offset SQL or None, exit_date offset SQL, reflected)
TRADES = {
    "closed_47h":        (PORTFOLIO, "NOW() - INTERVAL '47 hours'", "CURRENT_DATE - 2", False),
    "closed_49h":        (PORTFOLIO, "NOW() - INTERVAL '49 hours'", "CURRENT_DATE - 2", False),
    "closed_72h":        (PORTFOLIO, "NOW() - INTERVAL '72 hours'", "CURRENT_DATE - 3", False),
    "closed_29d":        (PORTFOLIO, "NOW() - INTERVAL '29 days'", "CURRENT_DATE - 29", False),
    "closed_31d":        (PORTFOLIO, "NOW() - INTERVAL '31 days'", "CURRENT_DATE - 31", False),
    "reflected_72h":     (PORTFOLIO, "NOW() - INTERVAL '72 hours'", "CURRENT_DATE - 3", True),
    # Recorded an hour ago, but the user back-dated the exit: created_at wins -> not yet due.
    "backdated_exit":    (PORTFOLIO, "NOW() - INTERVAL '1 hour'", "CURRENT_DATE - 10", False),
    # Legacy row with no created_at: falls back to exit_date.
    "null_created_5d":   (PORTFOLIO, None, "CURRENT_DATE - 5", False),
    "other_portfolio":   (OTHER_PORTFOLIO, "NOW() - INTERVAL '72 hours'", "CURRENT_DATE - 3", False),
}
EXPECTED_FIRST_RUN = {"closed_49h", "closed_72h", "closed_29d", "null_created_5d"}


def _seed(cur):
    cur.execute("INSERT INTO portfolios (id, name) VALUES (%s, 'main'), (%s, 'other')", (PORTFOLIO, OTHER_PORTFOLIO))
    ids = {}
    for label, (portfolio, created_sql, exit_sql, reflected) in TRADES.items():
        cur.execute(
            f"INSERT INTO trade_history (portfolio_id, ticker, exit_date, created_at) "
            f"VALUES (%s, %s, {exit_sql}, {created_sql or 'NULL'}) RETURNING id",
            (portfolio, label.upper()[:10]),
        )
        ids[label] = str(cur.fetchone()["id"])
        if reflected:
            cur.execute("INSERT INTO trade_reflections (trade_id) VALUES (%s)", (ids[label],))
    return ids


def _disable_all_rules(cur):
    """Seed every rule type disabled, so evaluate_alerts() runs only the price-alert,
    reflection-reminder and re-delivery steps (no positions/market-data paths)."""
    for rule in alerts_service.DEFAULT_RULES:
        cur.execute(
            "INSERT INTO alert_rules (portfolio_id, type, enabled) VALUES (%s, %s, FALSE)",
            (PORTFOLIO, rule["type"]),
        )


def _reminders(cur):
    cur.execute(
        "SELECT id, context->>'trade_id' AS trade_id, delivered, delivery_error FROM notifications "
        "WHERE alert_type = 'reflection_reminder' ORDER BY created_at"
    )
    return cur.fetchall()


@pytest.fixture
def seeded_schema():
    admin = psycopg2.connect(_DATABASE_URL, cursor_factory=RealDictCursor)
    admin.autocommit = True
    with admin.cursor() as cur:
        cur.execute(f"DROP SCHEMA IF EXISTS {SCHEMA} CASCADE")
        cur.execute(_PRE_V96_DDL)
    with patch.object(alerts_service, "get_db", _schema_get_db), \
         patch.object(alerts_service, "get_settings", return_value=[]):
        alerts_service.ensure_alerts_tables()  # migrate from the pre-v9.6 shape
        with _schema_get_db() as conn, conn.cursor() as cur:
            ids = _seed(cur)
            _disable_all_rules(cur)
        try:
            yield ids
        finally:
            with admin.cursor() as cur:
                cur.execute(f"DROP SCHEMA IF EXISTS {SCHEMA} CASCADE")
            admin.close()


def test_migration_adds_reflection_reminder_type_and_partial_unique_index(seeded_schema):
    with _schema_get_db() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT indexdef FROM pg_indexes WHERE schemaname = %s AND indexname = 'uq_notifications_reflection_reminder_trade'",
            (SCHEMA,),
        )
        row = cur.fetchone()
        assert row is not None, "partial unique index missing after ensure_alerts_tables()"
        assert "UNIQUE" in row["indexdef"] and "reflection_reminder" in row["indexdef"]
        cur.execute(
            "INSERT INTO notification_preferences (portfolio_id, alert_type, email_enabled) "
            "VALUES (%s, 'reflection_reminder', FALSE)",
            (PORTFOLIO,),
        )


def test_eligibility_idempotence_and_preference_off_rows_never_redelivered(seeded_schema):
    ids = seeded_schema
    by_trade = {v: k for k, v in ids.items()}
    enqueue = MagicMock()

    # Run 1 -- preference OFF (default): exactly the eligible trades get a settled feed row.
    summary = alerts_service.evaluate_alerts(PORTFOLIO, enqueue)
    reflection = summary["reflection_reminders"]
    assert reflection["error"] is None, reflection["error"]
    with _schema_get_db() as conn, conn.cursor() as cur:
        rows = _reminders(cur)
    assert {by_trade[r["trade_id"]] for r in rows} == EXPECTED_FIRST_RUN
    assert reflection["notifications_created"] == len(EXPECTED_FIRST_RUN)
    assert all(r["delivered"] is True and r["delivery_error"] == "email disabled" for r in rows)
    enqueue.assert_not_called()

    # Run 2 -- nothing new: at most one reminder per trade.
    summary = alerts_service.evaluate_alerts(PORTFOLIO, enqueue)
    assert summary["reflection_reminders"]["notifications_created"] == 0
    assert summary["reflection_reminders"]["error"] is None

    # The ON CONFLICT target itself: a second reminder row for the same trade is rejected.
    with pytest.raises(psycopg2.errors.UniqueViolation):
        with _schema_get_db() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notifications (portfolio_id, alert_type, title, message, context) "
                "VALUES (%s, 'reflection_reminder', 't', 'm', jsonb_build_object('trade_id', %s::text))",
                (PORTFOLIO, ids["closed_72h"]),
            )

    # Turn the preference ON later, and age the existing rows past the re-delivery
    # loop's 10-second floor so they would be picked up if left unsettled.
    with _schema_get_db() as conn, conn.cursor() as cur:
        cur.execute("UPDATE notifications SET created_at = NOW() - INTERVAL '1 hour'")
        cur.execute(
            "INSERT INTO notification_preferences (portfolio_id, alert_type, email_enabled) "
            "VALUES (%s, 'reflection_reminder', TRUE)",
            (PORTFOLIO,),
        )
        # A fresh closure that becomes due while the preference is ON (control case).
        cur.execute(
            "INSERT INTO trade_history (portfolio_id, ticker, exit_date, created_at) "
            "VALUES (%s, 'NEWLYDUE', CURRENT_DATE - 3, NOW() - INTERVAL '50 hours') RETURNING id",
            (PORTFOLIO,),
        )
        newly_due = str(cur.fetchone()["id"])

    enqueue.reset_mock()
    summary = alerts_service.evaluate_alerts(PORTFOLIO, enqueue)
    assert summary["redelivery_tasks_enqueued"] == 0, "preference-OFF reminders were re-delivered"
    assert summary["reflection_reminders"]["notifications_created"] == 1
    with _schema_get_db() as conn, conn.cursor() as cur:
        rows = {r["trade_id"]: r for r in _reminders(cur)}
    assert rows[newly_due]["delivered"] is False and rows[newly_due]["delivery_error"] is None
    enqueue.assert_called_once_with(str(rows[newly_due]["id"]))
