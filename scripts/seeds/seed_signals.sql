-- scripts/seeds/seed_signals.sql
-- Seed data for the signals table.
--
-- Inserts 4 representative signals against the staging portfolio:
--   2 active signals (new)    — will render on the Signals page
--   1 dismissed signal        — won't render by default but confirms dismissal state
--   1 entered signal          — signal acted on (position opened)
--
-- Signal data is representative of real momentum signals but uses
-- fixed values so QA tests are deterministic.
--
-- Signal date: 2026-04-10 (one day before the seed baseline date 2026-04-11)
--
-- Prerequisites: seed_portfolio_trades.sql must have run first so a portfolio row exists.

BEGIN;

INSERT INTO signals (
    portfolio_id,
    ticker,
    market,
    signal_date,
    rank,
    momentum_percent,
    current_price,
    price_gbp,
    atr_value,
    volatility,
    initial_stop,
    suggested_shares,
    allocation_gbp,
    total_cost,
    status
)
SELECT
    p.id,
    sig.ticker,
    sig.market,
    sig.signal_date::date,
    sig.rank,
    sig.momentum_percent,
    sig.current_price,
    sig.price_gbp,
    sig.atr_value,
    sig.volatility,
    sig.initial_stop,
    sig.suggested_shares,
    sig.allocation_gbp,
    sig.total_cost,
    sig.status
FROM (SELECT id FROM portfolios LIMIT 1) p
CROSS JOIN (VALUES
    -- Active signals (visible on Signals page)
    ('LGEN',   'UK', '2026-04-10', 1, 8.42,  230.50,  230.50, 4.20, 0.82, 210.00, 217, 500.00,  500.19,  'new'),
    ('BARC',   'UK', '2026-04-10', 2, 7.15,  152.30,  152.30, 3.10, 0.74, 138.00, 163, 248.00,  248.25,  'new'),
    -- Dismissed signal (excluded from active view)
    ('HSBA',   'UK', '2026-04-10', 3, 6.80,  624.10,  624.10, 8.90, 0.66, 595.00,  40, 249.60,  249.64,  'dismissed'),
    -- Entered signal — position opened from this signal (excluded from active view)
    ('TSCO',   'UK', '2026-04-10', 4, 5.90,  310.20,  310.20, 5.40, 0.71, 290.00,  80, 248.16,  248.16,  'entered')
) AS sig(ticker, market, signal_date, rank, momentum_percent, current_price, price_gbp,
         atr_value, volatility, initial_stop, suggested_shares, allocation_gbp, total_cost, status)
ON CONFLICT (portfolio_id, ticker, signal_date) DO UPDATE SET
    rank               = EXCLUDED.rank,
    momentum_percent   = EXCLUDED.momentum_percent,
    current_price      = EXCLUDED.current_price,
    price_gbp          = EXCLUDED.price_gbp,
    atr_value          = EXCLUDED.atr_value,
    volatility         = EXCLUDED.volatility,
    initial_stop       = EXCLUDED.initial_stop,
    suggested_shares   = EXCLUDED.suggested_shares,
    allocation_gbp     = EXCLUDED.allocation_gbp,
    total_cost         = EXCLUDED.total_cost,
    status             = EXCLUDED.status,
    updated_at         = NOW();

COMMIT;
