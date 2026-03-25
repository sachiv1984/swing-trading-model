-- scripts/reset_staging_db.sql
-- Resets the staging database to a known baseline state.
--
-- Idempotent: safe to run multiple times.
-- Uses TRUNCATE ... CASCADE to clear all data in FK-dependency order.
-- Re-inserts: one portfolio (£20,000 cash) + default settings.
--
-- Tables cleared via CASCADE from portfolios:
--   positions, trade_history, trade_reflections, cash_transactions,
--   portfolio_history, signals, watchlist,
--   alert_rules, alert_evaluations, notifications, notification_preferences
-- Also cleared separately: settings
-- Tables NOT cleared: tickers (static lookup data, not test state)
--
-- Usage (Render / Supabase PostgreSQL):
--   psql "$STAGING_DATABASE_URL" -f scripts/reset_staging_db.sql
--
-- Or paste into the Supabase SQL Editor for the staging project.
--
-- See scripts/reset_staging_db.sh for the shell wrapper that guards
-- against accidentally targeting a non-staging database.

BEGIN;

-- ── Step 1: Clear all application data ───────────────────────────────────
-- TRUNCATE portfolios CASCADE clears every table that has a FK chain to
-- portfolios in a single pass. settings has no FK to portfolios and is
-- truncated separately.

DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'portfolios'
    ) THEN
        TRUNCATE TABLE portfolios CASCADE;
        RAISE NOTICE 'portfolios + all dependent tables truncated.';
    ELSE
        RAISE NOTICE 'portfolios table not found — skipping truncate.';
    END IF;

    IF EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = 'settings'
    ) THEN
        TRUNCATE TABLE settings;
        RAISE NOTICE 'settings truncated.';
    ELSE
        RAISE NOTICE 'settings table not found — skipping truncate.';
    END IF;
END $$;

-- ── Step 2: Re-insert baseline portfolio (£20,000 cash) ──────────────────
INSERT INTO portfolios (cash, last_updated)
VALUES (20000.00, NOW());

-- ── Step 3: Re-insert default settings ───────────────────────────────────
INSERT INTO settings (
    min_hold_days,
    atr_multiplier_initial,
    atr_multiplier_trailing,
    atr_period,
    default_currency,
    uk_commission,
    us_commission,
    stamp_duty_rate,
    fx_fee_rate,
    min_trades_for_analytics,
    default_risk_percent
) VALUES (
    5,       -- min_hold_days
    2.0,     -- atr_multiplier_initial
    3.0,     -- atr_multiplier_trailing
    14,      -- atr_period
    'GBP',   -- default_currency
    11.95,   -- uk_commission (£)
    0.0,     -- us_commission
    0.5,     -- stamp_duty_rate (%)
    0.5,     -- fx_fee_rate (%)
    10,      -- min_trades_for_analytics
    1.0      -- default_risk_percent
);

COMMIT;

\echo ''
\echo 'Staging DB reset complete.'
\echo 'Baseline: 1 portfolio (cash=£20,000) + default settings.'
\echo 'All positions, trades, watchlist, alerts, signals, notifications cleared.'
