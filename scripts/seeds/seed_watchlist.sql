-- scripts/seeds/seed_watchlist.sql
-- Seeds watchlist entries for the watchlist domain QA scenarios.
--
-- Domains seeded: watchlist
--
-- Prerequisites:
--   - reset_staging_db.sql (or reset_staging_db.sh) must have been run to
--     ensure a clean portfolio baseline exists before seeding.
--
-- Usage:
--   psql "$STAGING_DATABASE_URL" -f scripts/seeds/seed_watchlist.sql
--
-- Idempotent:
--   - ON CONFLICT (portfolio_id, ticker) DO UPDATE
--
-- After this seed:
--   - 4 watchlist entries: 2 US stocks, 2 UK stocks
--   - All entries have target_entry_price, initial_stop_price, current_stop_price

BEGIN;

-- ── watchlist ─────────────────────────────────────────────────────────────
WITH portfolio AS (
    SELECT id FROM portfolios LIMIT 1
)
INSERT INTO watchlist (
    portfolio_id, ticker, market,
    target_entry_price, initial_stop_price, current_stop_price
)
SELECT
    p.id,
    w.ticker,
    w.market,
    w.target_entry_price,
    w.initial_stop_price,
    w.current_stop_price
FROM portfolio p
CROSS JOIN (VALUES
    ('AAPL', 'US', 165.00, 148.50, 150.25),
    ('MSFT', 'US', 380.00, 342.00, 355.00),
    ('LGEN', 'UK',   2.45,   2.15,   2.20),
    ('BARC', 'UK',   2.10,   1.85,   1.90)
) AS w(ticker, market, target_entry_price, initial_stop_price, current_stop_price)
ON CONFLICT (portfolio_id, ticker) DO UPDATE
    SET market             = EXCLUDED.market,
        target_entry_price = EXCLUDED.target_entry_price,
        initial_stop_price = EXCLUDED.initial_stop_price,
        current_stop_price = EXCLUDED.current_stop_price,
        updated_at         = NOW();

COMMIT;

\echo ''
\echo 'Watchlist seed complete.'
\echo '  watchlist: 4 entries seeded (AAPL, MSFT [US]; LGEN, BARC [UK])'
