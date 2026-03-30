-- scripts/seeds/seed_alerts.sql
-- Seeds alert rules, notification preferences, and sample notifications
-- for the alerts domain QA scenarios.
--
-- Domains seeded: alert_rules, notification_preferences, notifications
--
-- Prerequisites:
--   - reset_staging_db.sql (or reset_staging_db.sh) must have been run to
--     ensure a clean portfolio baseline exists before seeding.
--
-- Usage:
--   psql "$STAGING_DATABASE_URL" -f scripts/seeds/seed_alerts.sql
--
-- Idempotent:
--   - alert_rules and notification_preferences: ON CONFLICT DO UPDATE
--   - notifications: DELETE + INSERT (predictable count for smoke tests)
--
-- After this seed:
--   - 4 alert rules (one per type, all enabled; stop_loss threshold = 5%)
--   - 4 notification preferences (all types, email enabled)
--   - 2 unread notifications (stop_loss_approach + daily_portfolio_summary)
--
-- ST-05 smoke path satisfied: "view alerts" path finds unread notifications.

BEGIN;

-- ── alert_rules ───────────────────────────────────────────────────────────
WITH portfolio AS (
    SELECT id FROM portfolios LIMIT 1
)
INSERT INTO alert_rules (portfolio_id, type, enabled, threshold_percent)
SELECT
    p.id,
    r.type,
    r.enabled,
    r.threshold_percent
FROM portfolio p
CROSS JOIN (VALUES
    ('stop_loss_approach',       TRUE, 5.00),
    ('grace_period_warning',     TRUE, NULL),
    ('market_regime_change',     TRUE, NULL),
    ('daily_portfolio_summary',  TRUE, NULL)
) AS r(type, enabled, threshold_percent)
ON CONFLICT (portfolio_id, type) DO UPDATE
    SET enabled           = EXCLUDED.enabled,
        threshold_percent = EXCLUDED.threshold_percent,
        updated_at        = NOW();

-- ── notification_preferences ──────────────────────────────────────────────
WITH portfolio AS (
    SELECT id FROM portfolios LIMIT 1
)
INSERT INTO notification_preferences (portfolio_id, alert_type, email_enabled)
SELECT
    p.id,
    pref.alert_type,
    pref.email_enabled
FROM portfolio p
CROSS JOIN (VALUES
    ('stop_loss_approach',       TRUE),
    ('grace_period_warning',     TRUE),
    ('market_regime_change',     TRUE),
    ('daily_portfolio_summary',  TRUE)
) AS pref(alert_type, email_enabled)
ON CONFLICT (portfolio_id, alert_type) DO UPDATE
    SET email_enabled = EXCLUDED.email_enabled,
        updated_at    = NOW();

-- ── notifications ─────────────────────────────────────────────────────────
-- Clear and re-insert for deterministic count (2 unread notifications).
DELETE FROM notifications
WHERE portfolio_id = (SELECT id FROM portfolios LIMIT 1);

WITH portfolio AS (
    SELECT id FROM portfolios LIMIT 1
)
INSERT INTO notifications (
    portfolio_id, alert_type, title, message, context,
    read, delivered, delivery_attempts
)
SELECT
    p.id,
    n.alert_type,
    n.title,
    n.message,
    n.context::jsonb,
    FALSE,   -- unread
    TRUE,    -- delivered
    1        -- one delivery attempt recorded
FROM portfolio p
CROSS JOIN (VALUES
    (
        'stop_loss_approach',
        'Stop Loss Approaching: LGEN',
        'LGEN is within 5% of your stop loss (220p). Current price: 225p.',
        '{"ticker":"LGEN","stop_price":2.20,"current_price":2.25,"proximity_percent":2.22}'
    ),
    (
        'daily_portfolio_summary',
        'Daily Portfolio Summary',
        'Portfolio value: £20,560.00. 2 open positions. Unrealised P&L: +£560.00.',
        '{"portfolio_value_gbp":20560.00,"open_position_count":2,"unrealised_pnl_gbp":560.00}'
    )
) AS n(alert_type, title, message, context);

COMMIT;

\echo ''
\echo 'Alerts seed complete.'
\echo '  alert_rules: 4 rules seeded (all types, all enabled; stop_loss threshold=5%)'
\echo '  notification_preferences: 4 preferences seeded (all types, email enabled)'
\echo '  notifications: 2 unread notifications inserted'
