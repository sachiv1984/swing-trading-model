"""
Alerts Service

Business logic for alert rules, evaluation engine, and notification management.

Alert types:
  - stop_loss_approach: fires when stop is within threshold_percent of current price
  - grace_period_warning: fires on last 2 days of grace period (days 8+9 with default 10-day hold)
  - market_regime_change: fires on transition to risk_off (state change, not sustained state)
  - daily_portfolio_summary: fires once per portfolio per UTC calendar day

Delivery: FastAPI BackgroundTasks per ADR-003. Email delivery is a post-response background task.
Re-delivery: on each evaluate call, notifications with delivered=false and delivery_attempts<3
are re-enqueued.

Contract: docs/specs/api_contracts/alerts_endpoints.md v0.1
"""

import logging
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from config import DEFAULT_MIN_HOLD_DAYS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from database import get_db, get_portfolio, get_positions, get_settings
from utils.pricing import check_market_regime, get_current_price

logger = logging.getLogger(__name__)

ALERT_TYPES = [
    "stop_loss_approach",
    "grace_period_warning",
    "market_regime_change",
    "daily_portfolio_summary",
]

# Custom price alerts (ST-02, BLG-FE-116, EPIC-02, v7.5) — separate, many-rows-per-portfolio
# table, distinct from the singleton-per-type alert_rules above. See
# docs/specs/blg_fe_116_pre_implementation_readiness_pass.md AC-01/AC-03.
PRICE_ALERT_TICKER_RE = re.compile(r'^[A-Z0-9.]{1,10}$')
PRICE_ALERT_CAP = 50

DEFAULT_RULES = [
    {"type": "stop_loss_approach",      "enabled": True,  "threshold_percent": 5.0},
    {"type": "grace_period_warning",    "enabled": True,  "threshold_percent": None},
    {"type": "market_regime_change",    "enabled": True,  "threshold_percent": None},
    {"type": "daily_portfolio_summary", "enabled": True,  "threshold_percent": None},
]

# Module-level last-known regime tracker keyed by portfolio_id.
# Persists across requests within a process lifetime.
_last_known_regime: Dict[str, bool] = {}


# ---------------------------------------------------------------------------
# Table bootstrap
# ---------------------------------------------------------------------------

def ensure_alerts_tables():
    """Create alert tables if they do not yet exist (idempotent)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS alert_rules (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
                    type VARCHAR(50) NOT NULL
                        CHECK (type IN (
                            'stop_loss_approach', 'grace_period_warning',
                            'market_regime_change', 'daily_portfolio_summary'
                        )),
                    enabled BOOLEAN NOT NULL DEFAULT TRUE,
                    threshold_percent DECIMAL(5,2),
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    CONSTRAINT uq_alert_rules_portfolio_type UNIQUE (portfolio_id, type)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_alert_rules_portfolio
                    ON alert_rules(portfolio_id)
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
                    alert_type VARCHAR(50) NOT NULL
                        CHECK (alert_type IN (
                            'stop_loss_approach', 'grace_period_warning',
                            'market_regime_change', 'daily_portfolio_summary'
                        )),
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    context JSONB,
                    read BOOLEAN NOT NULL DEFAULT FALSE,
                    delivered BOOLEAN NOT NULL DEFAULT FALSE,
                    delivery_attempted_at TIMESTAMPTZ,
                    delivery_attempts INTEGER NOT NULL DEFAULT 0,
                    delivery_error TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_notifications_portfolio
                    ON notifications(portfolio_id)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_notifications_created
                    ON notifications(created_at DESC)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_notifications_read
                    ON notifications(portfolio_id, read)
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS notification_preferences (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
                    alert_type VARCHAR(50) NOT NULL
                        CHECK (alert_type IN (
                            'stop_loss_approach', 'grace_period_warning',
                            'market_regime_change', 'daily_portfolio_summary'
                        )),
                    email_enabled BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    CONSTRAINT uq_notification_preferences_portfolio_type
                        UNIQUE (portfolio_id, alert_type)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_notification_preferences_portfolio
                    ON notification_preferences(portfolio_id)
            """)

            # Custom price alerts (ST-02, BLG-FE-116, EPIC-02, v7.5)
            # Down migration: DROP TABLE IF EXISTS price_alerts;
            cur.execute("""
                CREATE TABLE IF NOT EXISTS price_alerts (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
                    ticker VARCHAR(10) NOT NULL,
                    condition VARCHAR(10) NOT NULL CHECK (condition IN ('above', 'below')),
                    threshold_price NUMERIC(10, 4) NOT NULL CHECK (threshold_price > 0),
                    active BOOLEAN NOT NULL DEFAULT TRUE,
                    triggered_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_price_alerts_portfolio_active
                    ON price_alerts(portfolio_id, active)
            """)

            # Extend notifications.alert_type CHECK to permit 'custom_price_alert'
            # (idempotent — only alters if not already extended; data_model.md v2.12->v2.13).
            cur.execute("""
                SELECT pg_get_constraintdef(oid) AS def
                FROM pg_constraint
                WHERE conrelid = 'notifications'::regclass
                  AND contype = 'c'
                  AND conname = 'notifications_alert_type_check'
            """)
            existing_check = cur.fetchone()
            if existing_check is None or 'custom_price_alert' not in existing_check["def"]:
                cur.execute("ALTER TABLE notifications DROP CONSTRAINT IF EXISTS notifications_alert_type_check")
                cur.execute("""
                    ALTER TABLE notifications ADD CONSTRAINT notifications_alert_type_check CHECK (alert_type IN (
                        'stop_loss_approach', 'grace_period_warning',
                        'market_regime_change', 'daily_portfolio_summary',
                        'custom_price_alert'
                    ))
                """)

            # Down migration: DROP TABLE IF EXISTS alert_evaluations;
            cur.execute("""
                CREATE TABLE IF NOT EXISTS alert_evaluations (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
                    evaluation_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    rule_type VARCHAR(50) NOT NULL
                        CHECK (rule_type IN (
                            'stop_loss_approach', 'grace_period_warning',
                            'market_regime_change', 'daily_portfolio_summary'
                        )),
                    symbol VARCHAR(20),
                    triggered BOOLEAN NOT NULL,
                    notification_sent BOOLEAN NOT NULL,
                    values_compared JSONB NOT NULL DEFAULT '{}'
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_alert_evaluations_portfolio_time
                    ON alert_evaluations(portfolio_id, evaluation_timestamp DESC)
            """)


# ---------------------------------------------------------------------------
# Alert Rules
# ---------------------------------------------------------------------------

def _seed_alert_rules(portfolio_id: str, cur) -> None:
    """Insert default rules for all four types (skips types that already exist)."""
    for rule in DEFAULT_RULES:
        cur.execute("""
            INSERT INTO alert_rules (portfolio_id, type, enabled, threshold_percent)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (portfolio_id, type) DO NOTHING
        """, (portfolio_id, rule["type"], rule["enabled"], rule["threshold_percent"]))


def get_alert_rules(portfolio_id: str) -> List[Dict]:
    """Return all alert rules, seeding defaults on first use."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM alert_rules WHERE portfolio_id = %s",
                (portfolio_id,)
            )
            if cur.fetchone()["cnt"] == 0:
                _seed_alert_rules(portfolio_id, cur)

            cur.execute(
                "SELECT * FROM alert_rules WHERE portfolio_id = %s ORDER BY type",
                (portfolio_id,)
            )
            return [_rule_row(r) for r in cur.fetchall()]


def create_alert_rule(portfolio_id: str, data: Dict) -> Dict:
    """
    Create an alert rule. Returns 400 if the type already exists.
    Primarily used to restore a deleted rule.
    """
    rule_type = data["type"]
    enabled = data.get("enabled", True)
    threshold_percent = data.get("threshold_percent")

    if rule_type not in ALERT_TYPES:
        raise ValueError(f"Invalid alert type: {rule_type}")
    if rule_type == "stop_loss_approach":
        if threshold_percent is None:
            raise ValueError("threshold_percent is required for stop_loss_approach")
        if not (0 < threshold_percent <= 100):
            raise ValueError("threshold_percent must be > 0 and <= 100")

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM alert_rules WHERE portfolio_id = %s AND type = %s",
                (portfolio_id, rule_type)
            )
            if cur.fetchone():
                raise ValueError(f"Rule for type '{rule_type}' already exists")

            cur.execute("""
                INSERT INTO alert_rules (portfolio_id, type, enabled, threshold_percent)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """, (portfolio_id, rule_type, enabled, threshold_percent))
            return _rule_row(cur.fetchone())


def update_alert_rule(portfolio_id: str, rule_id: str, data: Dict) -> Dict:
    """Partial update of an alert rule."""
    allowed = {"enabled", "threshold_percent"}
    updates = {k: v for k, v in data.items() if k in allowed and v is not None}
    if not updates:
        raise ValueError("No updatable fields provided")

    if "threshold_percent" in updates:
        tp = updates["threshold_percent"]
        if not (0 < tp <= 100):
            raise ValueError("threshold_percent must be > 0 and <= 100")

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM alert_rules WHERE id = %s AND portfolio_id = %s",
                (rule_id, portfolio_id)
            )
            row = cur.fetchone()
            if not row:
                raise LookupError(f"Rule {rule_id} not found")

            set_parts = ", ".join(f"{k} = %s" for k in updates)
            values = list(updates.values()) + [rule_id]
            cur.execute(
                f"UPDATE alert_rules SET {set_parts}, updated_at = NOW() WHERE id = %s RETURNING *",
                values
            )
            return _rule_row(cur.fetchone())


def delete_alert_rule(portfolio_id: str, rule_id: str) -> Dict:
    """Delete an alert rule."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM alert_rules WHERE id = %s AND portfolio_id = %s RETURNING id",
                (rule_id, portfolio_id)
            )
            row = cur.fetchone()
            if not row:
                raise LookupError(f"Rule {rule_id} not found")
            return {"deleted": True, "id": str(row["id"])}


# ---------------------------------------------------------------------------
# Custom Price Alerts (ST-02, BLG-FE-116, EPIC-02, v7.5)
# ---------------------------------------------------------------------------

def get_price_alerts(portfolio_id: str) -> List[Dict]:
    """Return all price alerts for the portfolio, most recently created first."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM price_alerts
                WHERE portfolio_id = %s
                ORDER BY created_at DESC
            """, (portfolio_id,))
            return [_price_alert_row(r) for r in cur.fetchall()]


def create_price_alert(portfolio_id: str, data: Dict) -> Dict:
    """
    Create a price alert. Raises ValueError (-> 400) on invalid input or when the
    per-portfolio active-alert cap is exceeded (readiness pass AC-03).
    """
    ticker = (data.get("ticker") or "").strip().upper()
    condition = data.get("condition")
    threshold_price = data.get("threshold_price")

    if not ticker or not PRICE_ALERT_TICKER_RE.match(ticker):
        raise ValueError("ticker must be 1-10 alphanumeric characters")
    if condition not in ("above", "below"):
        raise ValueError("condition must be 'above' or 'below'")
    if threshold_price is None or float(threshold_price) <= 0:
        raise ValueError("threshold_price must be a positive number")

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM price_alerts WHERE portfolio_id = %s AND active = TRUE",
                (portfolio_id,)
            )
            if cur.fetchone()["cnt"] >= PRICE_ALERT_CAP:
                raise ValueError("You've reached the maximum number of active price alerts.")

            cur.execute("""
                INSERT INTO price_alerts (portfolio_id, ticker, condition, threshold_price)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """, (portfolio_id, ticker, condition, float(threshold_price)))
            return _price_alert_row(cur.fetchone())


def delete_price_alert(portfolio_id: str, alert_id: str) -> Dict:
    """Delete a price alert."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM price_alerts WHERE id = %s AND portfolio_id = %s RETURNING id",
                (alert_id, portfolio_id)
            )
            row = cur.fetchone()
            if not row:
                raise LookupError(f"Price alert {alert_id} not found")
            return {"deleted": True, "id": str(row["id"])}


def _evaluate_price_alerts(cur, portfolio_id: str, enqueue_delivery) -> Dict:
    """
    Evaluate all active custom price alerts for the portfolio (readiness pass AC-02).
    Runs as a step inside evaluate_alerts() — reuses the already-scheduled
    POST /alerts/evaluate cron trigger rather than a second scheduler.
    """
    cur.execute("""
        SELECT id, ticker, condition, threshold_price
        FROM price_alerts
        WHERE portfolio_id = %s AND active = TRUE
    """, (portfolio_id,))
    rows = cur.fetchall()

    triggered_count = 0
    error_count = 0
    notifications_created = 0
    delivery_tasks_enqueued = 0

    for pa in rows:
        ticker = pa["ticker"]
        try:
            current_price = get_current_price(ticker)
        except Exception as e:
            logger.warning("custom_price_alert: price fetch failed for %s: %s", ticker, e)
            error_count += 1
            continue
        if current_price is None:
            error_count += 1
            continue

        threshold = float(pa["threshold_price"])
        condition = pa["condition"]
        condition_met = (
            (condition == "above" and current_price > threshold) or
            (condition == "below" and current_price < threshold)
        )
        if not condition_met:
            continue

        title = f"Price Alert — {ticker} {condition} {threshold:.2f}"
        message = (
            f"{ticker} crossed {condition} your threshold of {threshold:.2f} "
            f"(current: {current_price:.2f})."
        )
        context = {
            "ticker": ticker,
            "condition": condition,
            "threshold_price": threshold,
            "current_price": current_price,
        }
        context["price_alert_id"] = str(pa["id"])  # ST-09 (BLG-BE-84, EPIC-02, v8.8) — alert-to-trade provenance
        notif_id = _insert_notification(cur, portfolio_id, "custom_price_alert", title, message, context)
        notifications_created += 1
        enqueue_delivery(str(notif_id))
        delivery_tasks_enqueued += 1

        cur.execute("""
            UPDATE price_alerts SET active = FALSE, triggered_at = NOW(), updated_at = NOW()
            WHERE id = %s
        """, (pa["id"],))
        triggered_count += 1

    from services.health_service import record_nightly_job
    record_nightly_job(
        "custom_price_alerts",
        "ok" if error_count == 0 else "degraded",
        detail={"evaluated": len(rows), "triggered": triggered_count, "errors": error_count},
    )

    return {
        "evaluated": len(rows),
        "triggered": triggered_count,
        "errors": error_count,
        "notifications_created": notifications_created,
        "delivery_tasks_enqueued": delivery_tasks_enqueued,
    }


def _price_alert_row(r) -> Dict:
    return {
        "id": str(r["id"]),
        "ticker": r["ticker"],
        "condition": r["condition"],
        "threshold_price": float(r["threshold_price"]),
        "active": r["active"],
        "triggered_at": r["triggered_at"].isoformat() if hasattr(r["triggered_at"], "isoformat") else r["triggered_at"],
        "created_at": r["created_at"].isoformat() if hasattr(r["created_at"], "isoformat") else str(r["created_at"]),
        "updated_at": r["updated_at"].isoformat() if hasattr(r["updated_at"], "isoformat") else str(r["updated_at"]),
    }


# ---------------------------------------------------------------------------
# Alert Evaluation Engine
# ---------------------------------------------------------------------------

def evaluate_alerts(portfolio_id: str, enqueue_delivery) -> Dict:
    """
    Evaluate all enabled alert rules against current portfolio state.

    For each triggered rule, a notification is written and email delivery is
    enqueued via the provided enqueue_delivery callback (FastAPI BackgroundTasks).

    Also re-enqueues delivery for prior notifications where
    delivered=false and delivery_attempts<3.

    Args:
        portfolio_id: Portfolio to evaluate.
        enqueue_delivery: Callable(notification_id) that schedules background delivery.

    Returns:
        Summary dict per spec.
    """
    # Ensure all tables exist (idempotent — safe on cold production DB).
    ensure_alerts_tables()

    with get_db() as conn:
        with conn.cursor() as cur:
            # Seed default rules on first evaluate call if none exist yet
            # (mirrors get_alert_rules seeding — evaluate may be called before
            # the preferences page is ever visited).
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM alert_rules WHERE portfolio_id = %s",
                (portfolio_id,)
            )
            if cur.fetchone()["cnt"] == 0:
                _seed_alert_rules(portfolio_id, cur)

            # Load enabled rules
            cur.execute(
                "SELECT * FROM alert_rules WHERE portfolio_id = %s AND enabled = TRUE",
                (portfolio_id,)
            )
            rules = {r["type"]: r for r in cur.fetchall()}

            # Load open positions with current_stop and current_price
            cur.execute("""
                SELECT id, ticker, holding_days, current_stop, current_price,
                       entry_date, status
                FROM positions
                WHERE portfolio_id = %s AND status = 'open'
            """, (portfolio_id,))
            positions = cur.fetchall()

            # Load settings for min_hold_days
            settings_list = get_settings()
            settings_row = settings_list[0] if settings_list else None
            min_hold_days = (
                int(settings_row["min_hold_days"])
                if settings_row and settings_row.get("min_hold_days")
                else DEFAULT_MIN_HOLD_DAYS
            )

            # Load notification preferences
            cur.execute(
                "SELECT alert_type, email_enabled FROM notification_preferences WHERE portfolio_id = %s",
                (portfolio_id,)
            )
            pref_rows = cur.fetchall()
            prefs = {r["alert_type"]: r["email_enabled"] for r in pref_rows}
            # Default to email enabled if no preference row yet
            for t in ALERT_TYPES:
                prefs.setdefault(t, True)

            notifications_created = 0
            delivery_tasks_enqueued = 0

            evaluations_persisted = 0

            # --- stop_loss_approach ---
            if "stop_loss_approach" in rules:
                threshold = float(rules["stop_loss_approach"]["threshold_percent"] or 5.0)
                for pos in positions:
                    if pos["current_stop"] is None or pos["current_price"] is None:
                        continue
                    current_price = float(pos["current_price"])
                    current_stop = float(pos["current_stop"])
                    if current_price <= 0:
                        continue
                    ticker = pos["ticker"]
                    proximity_pct = (current_price - current_stop) / current_price * 100
                    condition_met = proximity_pct <= threshold
                    triggered = False
                    notification_sent = False
                    values = {
                        "stop_price": round(current_stop, 2),
                        "current_price": round(current_price, 2),
                        "gap_pct": round(proximity_pct, 2),
                        "threshold_pct": threshold,
                    }
                    if condition_met and _notif_exists_today_for_ticker(
                            cur, portfolio_id, "stop_loss_approach", ticker):
                        logger.info(
                            "Dedup: stop_loss_approach for %s already dispatched today — skipping",
                            ticker,
                        )
                    elif condition_met:
                        title = f"Stop Loss Approach — {ticker}"
                        message = (
                            f"{ticker} stop ({current_stop:.2f}) is within "
                            f"{proximity_pct:.1f}% of current price ({current_price:.2f}). "
                            f"Consider reviewing your stop."
                        )
                        context = {
                            "ticker": ticker,
                            "stop_price": current_stop,
                            "current_price": current_price,
                            "proximity_percent": round(proximity_pct, 2),
                        }
                        notif_id = _insert_notification(
                            cur, portfolio_id, "stop_loss_approach", title, message, context
                        )
                        notifications_created += 1
                        triggered = True
                        if prefs.get("stop_loss_approach"):
                            enqueue_delivery(str(notif_id))
                            delivery_tasks_enqueued += 1
                            notification_sent = True
                    _insert_evaluation(cur, portfolio_id, "stop_loss_approach",
                                       ticker, triggered, notification_sent, values)
                    evaluations_persisted += 1

            # --- grace_period_warning ---
            if "grace_period_warning" in rules:
                for pos in positions:
                    holding_days = pos["holding_days"] or 0
                    ticker = pos["ticker"]
                    condition_met = (holding_days >= min_hold_days - 2) and (holding_days < min_hold_days)
                    triggered = False
                    notification_sent = False
                    values = {
                        "holding_days": holding_days,
                        "min_hold_days": min_hold_days,
                        "days_remaining": min_hold_days - holding_days,
                    }
                    if condition_met and _notif_exists_today_for_ticker(
                            cur, portfolio_id, "grace_period_warning", ticker):
                        logger.info(
                            "Dedup: grace_period_warning for %s already dispatched today — skipping",
                            ticker,
                        )
                    elif condition_met:
                        days_remaining = min_hold_days - holding_days
                        title = f"Grace Period Warning — {ticker}"
                        message = (
                            f"{ticker} has {days_remaining} day(s) remaining in the "
                            f"{min_hold_days}-day grace period (day {holding_days} of {min_hold_days})."
                        )
                        context = {
                            "ticker": ticker,
                            "holding_days": holding_days,
                            "min_hold_days": min_hold_days,
                            "days_remaining": days_remaining,
                        }
                        notif_id = _insert_notification(
                            cur, portfolio_id, "grace_period_warning", title, message, context
                        )
                        notifications_created += 1
                        triggered = True
                        if prefs.get("grace_period_warning"):
                            enqueue_delivery(str(notif_id))
                            delivery_tasks_enqueued += 1
                            notification_sent = True
                    _insert_evaluation(cur, portfolio_id, "grace_period_warning",
                                       ticker, triggered, notification_sent, values)
                    evaluations_persisted += 1

            # --- market_regime_change ---
            if "market_regime_change" in rules:
                regime_notif = _check_regime_change(portfolio_id)
                triggered = regime_notif is not None
                notification_sent = False
                regime_values = regime_notif["context"] if regime_notif else {}
                if triggered:
                    notif_id = _insert_notification(
                        cur, portfolio_id,
                        "market_regime_change",
                        regime_notif["title"],
                        regime_notif["message"],
                        regime_notif["context"],
                    )
                    notifications_created += 1
                    if prefs.get("market_regime_change"):
                        enqueue_delivery(str(notif_id))
                        delivery_tasks_enqueued += 1
                        notification_sent = True
                _insert_evaluation(cur, portfolio_id, "market_regime_change",
                                   None, triggered, notification_sent, regime_values)
                evaluations_persisted += 1

            # --- daily_portfolio_summary ---
            if "daily_portfolio_summary" in rules:
                already_done = _daily_summary_exists_today(cur, portfolio_id)
                triggered = False
                notification_sent = False
                open_count = len(positions)
                summary_values = {"open_positions": open_count}
                if not already_done:
                    title = "Daily Portfolio Summary"
                    message = f"Daily summary: {open_count} open position(s) as of today."
                    notif_id = _insert_notification(
                        cur, portfolio_id,
                        "daily_portfolio_summary", title, message, summary_values
                    )
                    notifications_created += 1
                    triggered = True
                    if prefs.get("daily_portfolio_summary"):
                        enqueue_delivery(str(notif_id))
                        delivery_tasks_enqueued += 1
                        notification_sent = True
                _insert_evaluation(cur, portfolio_id, "daily_portfolio_summary",
                                   None, triggered, notification_sent, summary_values)
                evaluations_persisted += 1

            # --- custom_price_alerts (ST-02, BLG-FE-116, EPIC-02, v7.5) ---
            price_alert_summary = _evaluate_price_alerts(cur, portfolio_id, enqueue_delivery)
            notifications_created += price_alert_summary["notifications_created"]
            delivery_tasks_enqueued += price_alert_summary["delivery_tasks_enqueued"]

            # --- Re-delivery for failed prior notifications ---
            redelivery_tasks_enqueued = 0
            cur.execute("""
                SELECT id, alert_type FROM notifications
                WHERE portfolio_id = %s
                  AND delivered = FALSE
                  AND delivery_attempts < 3
                  AND created_at < NOW() - INTERVAL '10 seconds'
            """, (portfolio_id,))
            stale = cur.fetchall()
            for row in stale:
                if prefs.get(row["alert_type"], True):
                    enqueue_delivery(str(row["id"]))
                    redelivery_tasks_enqueued += 1

            return {
                "rules_evaluated": len(rules),
                "notifications_created": notifications_created,
                "delivery_tasks_enqueued": delivery_tasks_enqueued,
                "redelivery_tasks_enqueued": redelivery_tasks_enqueued,
                "evaluations_persisted": evaluations_persisted,
                "custom_price_alerts": price_alert_summary,
            }


def _check_regime_change(portfolio_id: str) -> Optional[Dict]:
    """
    Return a notification payload if the market regime has transitioned to risk_off
    since last check. Updates _last_known_regime in-place.
    Overall regime: risk_on only when BOTH SPY and FTSE are risk_on.
    """
    try:
        regime = check_market_regime()
    except Exception as e:
        logger.warning("Could not fetch market regime for change detection: %s", e)
        return None

    currently_risk_on = bool(regime.get("spy_risk_on")) and bool(regime.get("ftse_risk_on"))
    prev_risk_on = _last_known_regime.get(portfolio_id)
    _last_known_regime[portfolio_id] = currently_risk_on

    if prev_risk_on is None:
        # First call after startup — record current state, do not fire.
        # This satisfies ST-03 pre-condition #3: cold start must not trigger a spurious
        # market_regime_change alert. On restart, the first evaluate call re-establishes
        # the baseline; any genuine transition fires on the following call.
        return None

    if prev_risk_on and not currently_risk_on:
        # Transition: risk_on → risk_off
        return {
            "title": "Market Regime Change — Risk Off",
            "message": (
                "The market regime has transitioned to risk-off. "
                "SPY and/or FTSE 100 is now below its 200-day moving average."
            ),
            "context": {
                "spy_risk_on": regime.get("spy_risk_on"),
                "ftse_risk_on": regime.get("ftse_risk_on"),
            },
        }
    return None


def _daily_summary_exists_today(cur, portfolio_id: str) -> bool:
    """Return True if a daily_portfolio_summary notification already exists for today (UTC)."""
    cur.execute("""
        SELECT 1 FROM notifications
        WHERE portfolio_id = %s
          AND alert_type = 'daily_portfolio_summary'
          AND created_at::date = CURRENT_DATE
        LIMIT 1
    """, (portfolio_id,))
    return cur.fetchone() is not None


def _notif_exists_today_for_ticker(cur, portfolio_id: str, alert_type: str, ticker: str) -> bool:
    """Return True if a notification for this (portfolio, type, ticker) already exists today (UTC).
    Used for calendar-day deduplication on position-specific alert types per ST-03 Decision B.
    """
    cur.execute("""
        SELECT 1 FROM notifications
        WHERE portfolio_id = %s
          AND alert_type = %s
          AND context->>'ticker' = %s
          AND created_at::date = CURRENT_DATE
        LIMIT 1
    """, (portfolio_id, alert_type, ticker))
    return cur.fetchone() is not None


def _insert_evaluation(cur, portfolio_id: str, rule_type: str, symbol: Optional[str],
                       triggered: bool, notification_sent: bool, values_compared: Dict) -> None:
    """Persist one alert_evaluations row per rule/position evaluated."""
    import json
    cur.execute("""
        INSERT INTO alert_evaluations
            (portfolio_id, rule_type, symbol, triggered, notification_sent, values_compared)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (portfolio_id, rule_type, symbol, triggered, notification_sent,
          json.dumps(values_compared)))


def _insert_notification(cur, portfolio_id: str, alert_type: str,
                         title: str, message: str, context: Dict) -> str:
    """Insert a notification row and return its id."""
    import json
    cur.execute("""
        INSERT INTO notifications
            (portfolio_id, alert_type, title, message, context)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (portfolio_id, alert_type, title, message, json.dumps(context)))
    return cur.fetchone()["id"]


# ---------------------------------------------------------------------------
# Notification delivery background task
# ---------------------------------------------------------------------------

def deliver_notification(notification_id: str) -> None:
    """
    Background task: deliver notification via Telegram Bot API.

    Runs after the API response is returned (FastAPI BackgroundTasks, per ADR-003).
    Increments delivery_attempts on every call. Sets delivered=True on success,
    records delivery_error on failure. evaluate_alerts will re-enqueue if
    delivered=False and delivery_attempts < 3.

    Required env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
    If any are unset, the notification is logged and marked delivered to avoid
    infinite retry loops on misconfigured deployments.
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM notifications WHERE id = %s",
                    (notification_id,)
                )
                notif = cur.fetchone()
                if not notif:
                    logger.warning("deliver_notification: notification %s not found", notification_id)
                    return

                if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
                    logger.warning(
                        "deliver_notification: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — "
                        "marking delivered without sending. notification_id=%s", notification_id
                    )
                    cur.execute("""
                        UPDATE notifications
                        SET delivered = TRUE,
                            delivery_attempted_at = NOW(),
                            delivery_attempts = delivery_attempts + 1,
                            delivery_error = 'email not configured'
                        WHERE id = %s
                    """, (notification_id,))
                    return

                _send_via_telegram(notif)

                cur.execute("""
                    UPDATE notifications
                    SET delivered = TRUE,
                        delivery_attempted_at = NOW(),
                        delivery_attempts = delivery_attempts + 1,
                        delivery_error = NULL
                    WHERE id = %s
                """, (notification_id,))
                logger.info(
                    "deliver_notification: sent type=%s notification_id=%s",
                    notif["alert_type"], notification_id
                )

    except Exception as e:
        logger.error("deliver_notification failed for %s: %s", notification_id, e)
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE notifications
                        SET delivery_attempted_at = NOW(),
                            delivery_attempts = delivery_attempts + 1,
                            delivery_error = %s
                        WHERE id = %s
                    """, (str(e)[:500], notification_id))
        except Exception:
            pass


def _send_via_telegram(notif: dict) -> None:
    """Send an alert via Telegram Bot API (port 443 — Render-free-tier compatible)."""
    import urllib.request
    import urllib.parse
    import json

    text = f"*{notif['title']}*\n{notif['message']}"
    params = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    })
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?{params}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
        if not body.get("ok"):
            raise RuntimeError(f"Telegram API error: {body}")


def _build_email(notif) -> tuple:
    """
    Build (subject, html_body) for a notification row.
    Returns a clear subject and user-readable HTML body per ST-04 AC.
    """
    alert_type = notif["alert_type"]
    title = notif["title"]
    message = notif["message"]
    created_at = notif["created_at"]
    if hasattr(created_at, "strftime"):
        created_str = created_at.strftime("%Y-%m-%d %H:%M UTC")
    else:
        created_str = str(created_at)

    subject = f"[Trading Alert] {title}"

    type_labels = {
        "stop_loss_approach":      "Stop Loss Approach",
        "grace_period_warning":    "Grace Period Warning",
        "market_regime_change":    "Market Regime Change",
        "daily_portfolio_summary": "Daily Portfolio Summary",
    }
    type_label = type_labels.get(alert_type, alert_type)

    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">
  <div style="border-left: 4px solid #e85d04; padding-left: 16px; margin-bottom: 24px;">
    <h2 style="margin: 0 0 8px 0; color: #e85d04;">{title}</h2>
    <p style="margin: 0; font-size: 13px; color: #888;">{type_label} &mdash; {created_str}</p>
  </div>
  <p style="font-size: 16px; line-height: 1.6;">{message}</p>
  <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
  <p style="font-size: 12px; color: #aaa;">
    Swing Trading Model &mdash; automated alert.<br>
    Manage your notification preferences in the app.
  </p>
</body>
</html>
"""
    return subject, html_body


# ---------------------------------------------------------------------------
# Notification feed
# ---------------------------------------------------------------------------

def get_notifications(
    portfolio_id: str,
    page: int = 1,
    since_days: Optional[int] = None,
    read: Optional[bool] = None,
) -> Dict:
    """Return paginated notification feed, newest first.

    Optional filters (v0.6, ST-02/EPIC-02/v7.7): `since_days` restricts to
    notifications created within the last N days; `read` restricts to
    read-only (True) or unread-only (False) items. Both applied before
    pagination. Absent params preserve the prior unfiltered behaviour.
    """
    per_page = 50
    offset = (page - 1) * per_page
    where_clauses = ["portfolio_id = %s"]
    params = [portfolio_id]
    if since_days is not None:
        where_clauses.append("created_at >= NOW() - (%s * INTERVAL '1 day')")
        params.append(since_days)
    if read is not None:
        where_clauses.append("read = %s")
        params.append(read)
    where_sql = " AND ".join(where_clauses)

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT COUNT(*) AS cnt FROM notifications WHERE {where_sql}",
                tuple(params)
            )
            total = cur.fetchone()["cnt"]

            cur.execute(f"""
                SELECT id, alert_type, title, message, read, created_at, context
                FROM notifications
                WHERE {where_sql}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """, tuple(params) + (per_page, offset))
            rows = cur.fetchall()

    notifications = [_notif_row(r) for r in rows]
    return {
        "notifications": notifications,
        "total": total,
        "page": page,
        "per_page": per_page,
        "has_more": (offset + per_page) < total,
    }


def mark_notification_read(portfolio_id: str, notification_id: str) -> Dict:
    """Mark a single notification as read. Idempotent."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE notifications
                SET read = TRUE
                WHERE id = %s AND portfolio_id = %s
                RETURNING id, alert_type, title, message, read, created_at, context
            """, (notification_id, portfolio_id))
            row = cur.fetchone()
            if not row:
                raise LookupError(f"Notification {notification_id} not found")
            return _notif_row(row)


def mark_all_notifications_read(portfolio_id: str) -> Dict:
    """Mark all unread notifications as read."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE notifications
                SET read = TRUE
                WHERE portfolio_id = %s AND read = FALSE
            """, (portfolio_id,))
            return {"marked_read_count": cur.rowcount}


# ---------------------------------------------------------------------------
# Notification Preferences
# ---------------------------------------------------------------------------

def _seed_preferences(portfolio_id: str, cur) -> None:
    """Insert default preferences (all email enabled) for all four types."""
    for alert_type in ALERT_TYPES:
        cur.execute("""
            INSERT INTO notification_preferences (portfolio_id, alert_type, email_enabled)
            VALUES (%s, %s, TRUE)
            ON CONFLICT (portfolio_id, alert_type) DO NOTHING
        """, (portfolio_id, alert_type))


def get_preferences(portfolio_id: str) -> Dict:
    """Return notification preferences, seeding defaults on first use."""
    # ensure_alerts_tables() is called at application startup (main.py on_startup).
    # Calling it here on every request wastes a full DB connection (~1.5s on Supabase
    # free tier). Tables are guaranteed to exist after startup. ST-06 fix.
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM notification_preferences WHERE portfolio_id = %s",
                (portfolio_id,)
            )
            if cur.fetchone()["cnt"] == 0:
                _seed_preferences(portfolio_id, cur)

            cur.execute(
                "SELECT alert_type, email_enabled FROM notification_preferences WHERE portfolio_id = %s ORDER BY alert_type",
                (portfolio_id,)
            )
            rows = cur.fetchall()
            return {"preferences": [{"alert_type": r["alert_type"], "email_enabled": r["email_enabled"]} for r in rows]}


def update_preferences(portfolio_id: str, updates: Dict) -> Dict:
    """
    Partial update of notification preferences.
    updates: {alert_type: {"email_enabled": bool}, ...}
    """
    # ensure_alerts_tables() omitted — called at startup. ST-06 fix.
    invalid = [k for k in updates if k not in ALERT_TYPES]
    if invalid:
        raise ValueError(f"Unknown alert type key(s): {invalid}")
    if not updates:
        raise ValueError("No alert type keys provided")
    for key, val in updates.items():
        if not isinstance(val.get("email_enabled"), bool):
            raise ValueError(f"email_enabled must be a boolean for type '{key}'")

    with get_db() as conn:
        with conn.cursor() as cur:
            for alert_type, prefs in updates.items():
                cur.execute("""
                    INSERT INTO notification_preferences (portfolio_id, alert_type, email_enabled)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (portfolio_id, alert_type)
                    DO UPDATE SET email_enabled = EXCLUDED.email_enabled, updated_at = NOW()
                """, (portfolio_id, alert_type, prefs["email_enabled"]))

            cur.execute(
                "SELECT alert_type, email_enabled FROM notification_preferences WHERE portfolio_id = %s ORDER BY alert_type",
                (portfolio_id,)
            )
            rows = cur.fetchall()
            return {"preferences": [{"alert_type": r["alert_type"], "email_enabled": r["email_enabled"]} for r in rows]}


# ---------------------------------------------------------------------------
# Row serialisers
# ---------------------------------------------------------------------------

def _rule_row(r) -> Dict:
    return {
        "id": str(r["id"]),
        "type": r["type"],
        "enabled": r["enabled"],
        "threshold_percent": float(r["threshold_percent"]) if r["threshold_percent"] is not None else None,
        "created_at": r["created_at"].isoformat() if hasattr(r["created_at"], "isoformat") else str(r["created_at"]),
        "updated_at": r["updated_at"].isoformat() if hasattr(r["updated_at"], "isoformat") else str(r["updated_at"]),
    }


def _notif_row(r) -> Dict:
    return {
        "id": str(r["id"]),
        "alert_type": r["alert_type"],
        "title": r["title"],
        "message": r["message"],
        "read": r["read"],
        "created_at": r["created_at"].isoformat() if hasattr(r["created_at"], "isoformat") else str(r["created_at"]),
        # ST-09 (BLG-BE-84, EPIC-02, v8.8): exposed so the frontend can read
        # e.g. context.price_alert_id / context.ticker for the "create trade
        # plan from this alert" path. Was already stored (context JSONB) but
        # never selected/returned before this story.
        "context": r.get("context"),
    }


def _eval_row(r) -> Dict:
    return {
        "id": str(r["id"]),
        "evaluation_timestamp": r["evaluation_timestamp"].isoformat() if hasattr(r["evaluation_timestamp"], "isoformat") else str(r["evaluation_timestamp"]),
        "rule_type": r["rule_type"],
        "symbol": r["symbol"],
        "triggered": r["triggered"],
        "notification_sent": r["notification_sent"],
        "values_compared": r["values_compared"] if isinstance(r["values_compared"], dict) else {},
    }


# ---------------------------------------------------------------------------
# Alert History
# ---------------------------------------------------------------------------

def get_alert_history(portfolio_id: str, last_n_days: int = None, last_n_records: int = None) -> Dict:
    """
    Return alert evaluation history.
    - last_n_records takes precedence over last_n_days when both are supplied.
    - Default: last 30 days.
    Contract: docs/specs/api_contracts/alerts_endpoints.md v0.3 §GET /alerts/history
    """
    with get_db() as conn:
        with conn.cursor() as cur:
            if last_n_records:
                cur.execute("""
                    SELECT id, evaluation_timestamp, rule_type, symbol,
                           triggered, notification_sent, values_compared
                    FROM alert_evaluations
                    WHERE portfolio_id = %s
                    ORDER BY evaluation_timestamp DESC
                    LIMIT %s
                """, (portfolio_id, last_n_records))
                rows = cur.fetchall()
                cur.execute(
                    "SELECT COUNT(*) AS cnt FROM alert_evaluations WHERE portfolio_id = %s",
                    (portfolio_id,)
                )
            else:
                days = last_n_days or 30
                cur.execute("""
                    SELECT id, evaluation_timestamp, rule_type, symbol,
                           triggered, notification_sent, values_compared
                    FROM alert_evaluations
                    WHERE portfolio_id = %s
                      AND evaluation_timestamp >= NOW() - (%s * INTERVAL '1 day')
                    ORDER BY evaluation_timestamp DESC
                """, (portfolio_id, days))
                rows = cur.fetchall()
                cur.execute("""
                    SELECT COUNT(*) AS cnt FROM alert_evaluations
                    WHERE portfolio_id = %s
                      AND evaluation_timestamp >= NOW() - (%s * INTERVAL '1 day')
                """, (portfolio_id, days))
            total = cur.fetchone()["cnt"]

    return {
        "evaluations": [_eval_row(r) for r in rows],
        "total": total,
    }
