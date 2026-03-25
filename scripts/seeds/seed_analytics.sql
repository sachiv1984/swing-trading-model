-- scripts/seeds/seed_analytics.sql
-- Seeds closed trade_history records for Performance Analytics QA scenarios.
--
-- Purpose:
--   Provides enough closed trades (12) to cross the min_trades_for_analytics
--   threshold (default: 10) so the analytics page renders charts instead of
--   the "Not Enough Data" empty state.
--
--   Trade data matches the Playwright mock in tests/e2e/mocks/analytics-mock-data.js
--   exactly — same tickers, dates, and P&L values. This keeps staging visual
--   checks and automated test assertions comparable.
--
-- Domains seeded: trade_history (closed trades only)
--
-- Prerequisites:
--   - reset_staging_db.sql must have been run to establish the portfolio baseline.
--
-- Usage:
--   psql "$STAGING_DATABASE_URL" -f scripts/seeds/seed_analytics.sql
--
-- Idempotent:
--   Deletes these tickers from trade_history before inserting.
--   Safe to re-run after reset; produces identical state each time.
--
-- Known constraint:
--   trade_history has no stop_price column. The /trades endpoint therefore
--   does not return stop_price. RMultipleAnalysis and the heatmap modal
--   R-multiple column will not render on staging until stop_price is added
--   to the API response (see backlog item filed during ST-06 delivery).
--   Visual checks V-CHART-05a/b/c in staging_visual_test_script_ST-06.md
--   are marked as staging-blocked for this reason.
--
-- After this seed:
--   - 12 closed trades: 3 in Jan 2026, 5 in Feb 2026, 4 in Mar 2026
--   - Jan 2026 P&L: AAAA +£150, BBBB -£80, CCCC +£200 → total +£270
--   - Feb 2026 P&L: DDDD +£120, EEEE -£100, FFFF +£90, GGGG -£60, HHHH +£150 → total +£200
--   - Mar 2026 P&L: IIII +£120, JJJJ -£75, KKKK +£180, LLLL -£60 → total +£165
--
-- ST-06 visual checks satisfied (staging):
--   V-CHART-01* (heatmap modal, cursor, colour coding)   — covered
--   V-CHART-02* (zoom, grab cursor)                      — covered
--   V-CHART-03* (tooltip content + flip)                 — covered
--   V-CHART-05* (R-multiple bar tooltip)                 — BLOCKED: no stop_price

BEGIN;

-- ── Idempotency: clear this seed's tickers from trade_history ─────────────
DELETE FROM trade_reflections
WHERE trade_id IN (
    SELECT id FROM trade_history
    WHERE portfolio_id = (SELECT id FROM portfolios LIMIT 1)
      AND ticker IN ('AAAA','BBBB','CCCC','DDDD','EEEE','FFFF',
                     'GGGG','HHHH','IIII','JJJJ','KKKK','LLLL')
);

DELETE FROM trade_history
WHERE portfolio_id = (SELECT id FROM portfolios LIMIT 1)
  AND ticker IN ('AAAA','BBBB','CCCC','DDDD','EEEE','FFFF',
                 'GGGG','HHHH','IIII','JJJJ','KKKK','LLLL');

-- ── Insert 12 closed trades ───────────────────────────────────────────────
-- Columns: portfolio_id, position_id, ticker, market, entry_date, exit_date,
--          shares, entry_price, exit_price, total_cost, gross_proceeds,
--          net_proceeds, entry_fees, exit_fees, pnl, pnl_pct, holding_days,
--          exit_reason, tags
--
-- No stop_price column exists in trade_history — see constraint note above.
-- Fees are 0 for simplicity: total_cost = shares × entry_price,
--                            gross_proceeds = net_proceeds = shares × exit_price.

WITH portfolio AS (SELECT id FROM portfolios LIMIT 1)
INSERT INTO trade_history (
    portfolio_id, position_id,
    ticker, market,
    entry_date, exit_date,
    shares, entry_price, exit_price,
    total_cost, gross_proceeds, net_proceeds,
    entry_fees, exit_fees,
    pnl, pnl_pct, holding_days,
    exit_reason, tags
)
SELECT
    p.id,
    NULL,
    t.ticker, t.market,
    t.entry_date::date, t.exit_date::date,
    t.shares, t.entry_price, t.exit_price,
    t.total_cost, t.gross_proceeds, t.net_proceeds,
    0.00, 0.00,
    t.pnl, t.pnl_pct, t.holding_days,
    t.exit_reason, t.tags::text[]
FROM portfolio p
CROSS JOIN (VALUES
    -- ── Jan 2026 (3 trades, total P&L = +£270) ─────────────────────────────
    -- ticker  mkt   entry_date    exit_date     shares entry_p exit_p  total_c  gross    net      pnl    pnl_pct hdays exit_reason  tags
    ('AAAA', 'UK', '2026-01-05', '2026-01-12', 10.0,  100.00, 115.00, 1000.00, 1150.00, 1150.00,  150.00, 15.00,  7, 'target',   '{momentum}'),
    ('BBBB', 'UK', '2026-01-10', '2026-01-20', 10.0,   50.00,  42.00,  500.00,  420.00,  420.00,  -80.00,-16.00, 10, 'stop_hit', '{breakout}'),
    ('CCCC', 'UK', '2026-01-15', '2026-01-28',  8.0,   80.00, 105.00,  640.00,  840.00,  840.00,  200.00, 31.25, 13, 'target',   '{momentum}'),
    -- ── Feb 2026 (5 trades, total P&L = +£200) ─────────────────────────────
    ('DDDD', 'UK', '2026-02-02', '2026-02-10', 10.0,   60.00,  72.00,  600.00,  720.00,  720.00,  120.00, 20.00,  8, 'target',   '{breakout}'),
    ('EEEE', 'US', '2026-02-05', '2026-02-12', 20.0,   40.00,  35.00,  800.00,  700.00,  700.00, -100.00,-12.50,  7, 'stop_hit', '{}'),
    ('FFFF', 'UK', '2026-02-08', '2026-02-15', 10.0,   90.00,  99.00,  900.00,  990.00,  990.00,   90.00, 10.00,  7, 'manual',   '{momentum}'),
    ('GGGG', 'UK', '2026-02-14', '2026-02-20',  5.0,  120.00, 108.00,  600.00,  540.00,  540.00,  -60.00,-10.00,  6, 'stop_hit', '{}'),
    ('HHHH', 'US', '2026-02-18', '2026-02-25',  5.0,  200.00, 230.00, 1000.00, 1150.00, 1150.00,  150.00, 15.00,  7, 'target',   '{breakout}'),
    -- ── Mar 2026 (4 trades, total P&L = +£165) ─────────────────────────────
    ('IIII', 'UK', '2026-03-01', '2026-03-05', 10.0,   50.00,  62.00,  500.00,  620.00,  620.00,  120.00, 24.00,  4, 'target',   '{momentum}'),
    ('JJJJ', 'UK', '2026-03-03', '2026-03-07', 10.0,   75.00,  67.50,  750.00,  675.00,  675.00,  -75.00,-10.00,  4, 'stop_hit', '{}'),
    ('KKKK', 'US', '2026-03-06', '2026-03-10',  5.0,  300.00, 336.00, 1500.00, 1680.00, 1680.00,  180.00, 12.00,  4, 'target',   '{breakout,momentum}'),
    ('LLLL', 'UK', '2026-03-10', '2026-03-14', 15.0,   40.00,  36.00,  600.00,  540.00,  540.00,  -60.00,-10.00,  4, 'stop_hit', '{}')
) AS t(
    ticker, market, entry_date, exit_date,
    shares, entry_price, exit_price,
    total_cost, gross_proceeds, net_proceeds,
    pnl, pnl_pct, holding_days,
    exit_reason, tags
);

COMMIT;

\echo ''
\echo 'Analytics seed complete.'
\echo '  trade_history: 12 closed trades'
\echo '    Jan 2026 — 3 trades (AAAA +£150, BBBB -£80, CCCC +£200) → total +£270'
\echo '    Feb 2026 — 5 trades (DDDD +£120, EEEE -£100, FFFF +£90, GGGG -£60, HHHH +£150) → total +£200'
\echo '    Mar 2026 — 4 trades (IIII +£120, JJJJ -£75, KKKK +£180, LLLL -£60) → total +£165'
\echo ''
\echo 'Note: R-Multiple chart will not render — stop_price not in trade_history.'
\echo 'Visual checks V-CHART-05a/b/c are staging-blocked until the API gap is resolved.'
