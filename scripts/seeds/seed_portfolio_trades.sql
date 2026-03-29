-- scripts/seeds/seed_portfolio_trades.sql
-- Seeds positions, trade_history, and cash_transactions for the
-- portfolio/trades domain QA scenarios.
--
-- Domains seeded: positions (open), trade_history (closed), cash_transactions
--
-- Prerequisites:
--   - reset_staging_db.sql (or reset_staging_db.sh) must have been run to
--     ensure a clean portfolio baseline exists before seeding.
--
-- Usage:
--   psql "$STAGING_DATABASE_URL" -f scripts/seeds/seed_portfolio_trades.sql
--
-- Idempotent:
--   - Clears domain tables for this portfolio before inserting.
--   - Safe to re-run after reset_staging_db; produces identical state each run.
--
-- After this seed:
--   - 1 cash_transaction: initial £20,000 deposit
--   - 2 open positions: LGEN (UK) and BARC (UK)
--   - 2 closed trade_history entries: ULVR (profit) and VOD (small loss)
--   - portfolio.cash updated to reflect open position costs
--
-- ST-05 smoke paths satisfied:
--   "add trade"       — portfolio + settings baseline exists (from reset)
--   "view portfolio"  — 2 open positions visible on Portfolio page

BEGIN;

-- ── Clear domain tables for this portfolio ────────────────────────────────
-- Deletion order respects FK constraints:
--   trade_reflections → trade_history; then positions; then cash_transactions.
--
-- NOTE: TRUNCATE ... CASCADE in reset_staging_db.sql already clears these.
-- These DELETEs guard against re-running the seed without an intervening reset.

DELETE FROM trade_reflections
WHERE trade_id IN (
    SELECT id FROM trade_history
    WHERE portfolio_id = (SELECT id FROM portfolios LIMIT 1)
);

DELETE FROM trade_history
WHERE portfolio_id = (SELECT id FROM portfolios LIMIT 1);

DELETE FROM positions
WHERE portfolio_id = (SELECT id FROM portfolios LIMIT 1);

DELETE FROM cash_transactions
WHERE portfolio_id = (SELECT id FROM portfolios LIMIT 1);

-- ── cash_transactions: initial deposit ───────────────────────────────────
WITH portfolio AS (SELECT id FROM portfolios LIMIT 1)
INSERT INTO cash_transactions (portfolio_id, type, amount, date, note)
SELECT id, 'deposit', 20000.00, '2026-01-02', 'Initial capital deposit'
FROM portfolio;

-- ── positions: 2 open UK positions ───────────────────────────────────────
-- LGEN: Legal & General, 1000 shares @ 245p, entered 2026-03-01
-- BARC: Barclays, 1200 shares @ 210p, entered 2026-03-10
--
-- total_cost = (shares × entry_price) + fees_paid (all in GBP)
--   LGEN: (1000 × 2.45) + 11.95 = 2461.95
--   BARC: (1200 × 2.10) + 11.95 = 2531.95
--   Total invested: 4993.90 — deducted from portfolio cash below.

WITH portfolio AS (SELECT id FROM portfolios LIMIT 1)
INSERT INTO positions (
    portfolio_id, ticker, market,
    entry_date, entry_price, shares,
    total_cost, fees_paid, fee_type,
    initial_stop, current_stop, current_price,
    atr, holding_days,
    pnl, pnl_pct, status
)
SELECT
    p.id,
    pos.ticker,
    pos.market,
    pos.entry_date::date,
    pos.entry_price,
    pos.shares,
    pos.total_cost,
    pos.fees_paid,
    pos.fee_type,
    pos.initial_stop,
    pos.current_stop,
    pos.current_price,
    pos.atr,
    pos.holding_days,
    pos.pnl,
    pos.pnl_pct,
    'open'
FROM portfolio p
CROSS JOIN (VALUES
    -- ticker   mkt   entry_date    entry_p shares  total_cost fees    fee_type     init_stp curr_stp curr_p  atr   hdays pnl    pnl_pct
    ('LGEN', 'UK', '2026-03-01', 2.45,   1000.0, 2461.95,  11.95, 'commission', 2.15,    2.20,    2.52,   0.08, 24,   70.05, 2.85),
    ('BARC', 'UK', '2026-03-10', 2.10,   1200.0, 2531.95,  11.95, 'commission', 1.85,    1.90,    2.18,   0.06, 15,   96.05, 3.79)
) AS pos(
    ticker, market, entry_date, entry_price, shares,
    total_cost, fees_paid, fee_type,
    initial_stop, current_stop, current_price,
    atr, holding_days, pnl, pnl_pct
);

-- ── Update portfolio cash to reflect open position costs ──────────────────
-- Reset baseline = £20,000. Deduct total_cost of all open positions seeded above.
UPDATE portfolios
SET cash         = 20000.00 - (
                       SELECT COALESCE(SUM(total_cost), 0)
                       FROM positions
                       WHERE portfolio_id = portfolios.id
                         AND status = 'open'
                   ),
    last_updated = NOW();

-- ── trade_history: 2 closed trades ───────────────────────────────────────
-- ULVR: Unilever, profitable exit (trailing stop, +£296.10)
-- VOD:  Vodafone, small loss (stop loss hit, -£23.90)
--
-- position_id is NULL — these are historical records not linked to an
-- open position in this seed.

WITH portfolio AS (SELECT id FROM portfolios LIMIT 1)
INSERT INTO trade_history (
    portfolio_id, position_id,
    ticker, market,
    entry_date, exit_date,
    shares, entry_price, exit_price,
    total_cost, gross_proceeds, net_proceeds,
    entry_fees, exit_fees,
    pnl, pnl_pct, holding_days,
    exit_reason, entry_note, exit_note, tags
)
SELECT
    p.id,
    NULL,
    t.ticker,
    t.market,
    t.entry_date::date,
    t.exit_date::date,
    t.shares,
    t.entry_price,
    t.exit_price,
    t.total_cost,
    t.gross_proceeds,
    t.net_proceeds,
    t.entry_fees,
    t.exit_fees,
    t.pnl,
    t.pnl_pct,
    t.holding_days,
    t.exit_reason,
    t.entry_note,
    t.exit_note,
    t.tags::text[]
FROM portfolio p
CROSS JOIN (VALUES
    -- ticker  mkt   entry_date    exit_date     shares entry_p exit_p  total_cost gross_proc net_proc   entry_f exit_f  pnl     pnl_pct hdays exit_reason      entry_note                exit_note                    tags
    -- ULVR: gross=80×27.80=2224.00, exit_fee=11.95, net=2224.00-11.95=2212.05, pnl=2212.05-1915.95=296.10
    ('ULVR', 'UK', '2026-01-15', '2026-02-20', 80.0,  23.80,  27.80,  1915.95,   2224.00,   2212.05,   11.95,  11.95,  296.10, 15.45,  36,   'Trailing Stop', 'Breakout above 200 DMA', 'Trailing stop triggered.',  '{momentum}'),
    -- VOD:  gross=500×0.70=350.00, exit_fee=11.95, net=350.00-11.95=338.05, pnl=338.05-361.95=-23.90
    ('VOD',  'UK', '2026-02-01', '2026-03-05', 500.0,  0.70,   0.70,   361.95,    350.00,    338.05,    11.95,  11.95,  -23.90, -6.60,  32,   'Stop Loss Hit', 'Reversal attempt',       'Stop triggered on gap down.', '{mean_reversion}')
) AS t(
    ticker, market, entry_date, exit_date,
    shares, entry_price, exit_price,
    total_cost, gross_proceeds, net_proceeds,
    entry_fees, exit_fees,
    pnl, pnl_pct, holding_days,
    exit_reason, entry_note, exit_note, tags
);

COMMIT;

\echo ''
\echo 'Portfolio/trades seed complete.'
\echo '  cash_transactions: 1 deposit (£20,000 initial capital, 2026-01-02)'
\echo '  positions (open): 2 entries — LGEN (1000 shares @ 245p), BARC (1200 shares @ 210p)'
\echo '  trade_history: 2 closed trades — ULVR (+£296.10), VOD (-£23.90)'
\echo '  portfolio.cash: updated to reflect open position costs (£20,000 - £4,993.90)'
