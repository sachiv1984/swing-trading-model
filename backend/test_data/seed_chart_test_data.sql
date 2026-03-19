-- seed_chart_test_data.sql
-- Seeds 12 closed trades for ST-11 chart interactivity DoQ sign-off.
-- Satisfies all preconditions in docs/testing/chart_interactivity_scenarios.md
--
-- Usage (Render PostgreSQL):
--   psql "$DATABASE_URL" -f backend/test_data/seed_chart_test_data.sql
--
-- Or paste into Render dashboard → PostgreSQL → Query tab.
--
-- What is created:
--   Settings record (if none exists)
--   Jan 2026: AZN (+2R), SHEL (-1.5R), ULVR (+2R), BP. (-1R)        = 4 trades
--   Feb 2026: HSBA (+1.5R), VOD (-0.5R), GSK (+3R), RIO (-1R),
--             LGEN (+0.5R), BT.A (-2.5R)                             = 6 trades
--   Mar 2026: MKS (+2R), BATS (-3R)                                  = 2 trades
--   Apr 2026: 0 trades  ← zero-tile for SC-CHART-IX-01c
--   All 7 R-multiple histogram buckets populated.

DO $$
DECLARE
    v_portfolio_id  UUID;
    v_position_id   UUID;
BEGIN

    -- ── Portfolio ID ─────────────────────────────────────────────────────
    SELECT id INTO v_portfolio_id FROM portfolios LIMIT 1;
    IF v_portfolio_id IS NULL THEN
        RAISE EXCEPTION 'No portfolio found. Set up the app first.';
    END IF;

    -- ── Settings (create if missing) ──────────────────────────────────────
    IF NOT EXISTS (SELECT 1 FROM settings) THEN
        INSERT INTO settings (
            min_hold_days, atr_multiplier_initial, atr_multiplier_trailing,
            atr_period, default_currency, uk_commission, us_commission,
            stamp_duty_rate, fx_fee_rate, min_trades_for_analytics, default_risk_percent
        ) VALUES (
            5, 2.0, 3.0, 14, 'GBP', 11.95, 0.0, 0.5, 0.5, 10, 1.0
        );
        RAISE NOTICE 'Settings created.';
    END IF;

    -- ────────────────────────────────────────────────────────────────────
    -- Helper macro: insert position → return id, then insert trade_history
    -- Prices are in pence (UK stocks). PnL = shares*(exit-entry)/100 GBP (excl. fees).
    -- ────────────────────────────────────────────────────────────────────

    -- [01] AZN  Jan  +2.0R  bucket: 2R to 3R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'AZN', 'UK', '2026-01-06', 11500, 11000, 10, 1150.00, 100.00, 8.70, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'AZN', 'UK', '2026-01-06', '2026-01-20', 10, 11500, 12500, 1150.00, 100.00, 8.70, 14, 'target', '[SEED]');

    -- [02] SHEL  Jan  -1.5R  bucket: -2R to -1R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'SHEL', 'UK', '2026-01-07', 2600, 2400, 10, 260.00, -30.00, -11.54, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'SHEL', 'UK', '2026-01-07', '2026-01-21', 10, 2600, 2300, 260.00, -30.00, -11.54, 14, 'stop_hit', '[SEED]');

    -- [03] ULVR  Jan  +2.0R  bucket: 2R to 3R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'ULVR', 'UK', '2026-01-08', 4200, 4000, 25, 1050.00, 100.00, 9.52, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'ULVR', 'UK', '2026-01-08', '2026-01-22', 25, 4200, 4600, 1050.00, 100.00, 9.52, 14, 'target', '[SEED]');

    -- [04] BP.   Jan  -1.0R  bucket: -1R to 0R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'BP.', 'UK', '2026-01-09', 430, 400, 100, 430.00, -30.00, -6.98, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'BP.', 'UK', '2026-01-09', '2026-01-23', 100, 430, 400, 430.00, -30.00, -6.98, 14, 'stop_hit', '[SEED]');

    -- [05] HSBA  Feb  +1.5R  bucket: 1R to 2R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'HSBA', 'UK', '2026-02-03', 700, 650, 200, 1400.00, 150.00, 10.71, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'HSBA', 'UK', '2026-02-03', '2026-02-17', 200, 700, 775, 1400.00, 150.00, 10.71, 14, 'manual', '[SEED]');

    -- [06] VOD   Feb  -0.5R  bucket: -1R to 0R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'VOD', 'UK', '2026-02-04', 75, 65, 500, 375.00, -25.00, -6.67, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'VOD', 'UK', '2026-02-04', '2026-02-18', 500, 75, 70, 375.00, -25.00, -6.67, 14, 'manual', '[SEED]');

    -- [07] GSK   Feb  +3.0R  bucket: 3R+
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'GSK', 'UK', '2026-02-05', 1700, 1600, 50, 850.00, 150.00, 17.65, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'GSK', 'UK', '2026-02-05', '2026-02-19', 50, 1700, 2000, 850.00, 150.00, 17.65, 14, 'target', '[SEED]');

    -- [08] RIO   Feb  -1.0R  bucket: -1R to 0R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'RIO', 'UK', '2026-02-06', 5200, 4900, 10, 520.00, -30.00, -5.77, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'RIO', 'UK', '2026-02-06', '2026-02-20', 10, 5200, 4900, 520.00, -30.00, -5.77, 14, 'stop_hit', '[SEED]');

    -- [09] LGEN  Feb  +0.5R  bucket: 0R to 1R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'LGEN', 'UK', '2026-02-07', 240, 220, 500, 1200.00, 50.00, 4.17, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'LGEN', 'UK', '2026-02-07', '2026-02-21', 500, 240, 250, 1200.00, 50.00, 4.17, 14, 'manual', '[SEED]');

    -- [10] BT.A  Feb  -2.5R  bucket: -3R+
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'BT.A', 'UK', '2026-02-10', 140, 120, 200, 280.00, -100.00, -35.71, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'BT.A', 'UK', '2026-02-10', '2026-02-24', 200, 140, 90, 280.00, -100.00, -35.71, 14, 'stop_hit', '[SEED]');

    -- [11] MKS   Mar  +2.0R  bucket: 2R to 3R
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'MKS', 'UK', '2026-03-03', 380, 340, 125, 475.00, 100.00, 21.05, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'MKS', 'UK', '2026-03-03', '2026-03-17', 125, 380, 460, 475.00, 100.00, 21.05, 14, 'target', '[SEED]');

    -- [12] BATS  Mar  -3.0R  bucket: -3R+
    INSERT INTO positions (portfolio_id, ticker, market, entry_date, entry_price, initial_stop, shares, total_cost, pnl, pnl_pct, status, holding_days, entry_note)
    VALUES (v_portfolio_id, 'BATS', 'UK', '2026-03-04', 2700, 2600, 40, 1080.00, -120.00, -11.11, 'closed', 14, '[SEED] ST-11')
    RETURNING id INTO v_position_id;
    INSERT INTO trade_history (portfolio_id, position_id, ticker, market, entry_date, exit_date, shares, entry_price, exit_price, total_cost, pnl, pnl_pct, holding_days, exit_reason, exit_note)
    VALUES (v_portfolio_id, v_position_id, 'BATS', 'UK', '2026-03-04', '2026-03-18', 40, 2700, 2400, 1080.00, -120.00, -11.11, 14, 'stop_hit', '[SEED]');

    RAISE NOTICE 'Seeded 12 trades (Jan×4 / Feb×6 / Mar×2). All 7 R-multiple buckets populated.';

END $$;
