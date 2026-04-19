/**
 * Smoke Test Mock Data — ST-05 (BLG-QA-05)
 * Critical-Path Smoke Tests: add trade, view portfolio, view alerts
 *
 * Spec ref: docs/testing/ (ST-05 critical paths)
 * Seeded state ref: scripts/seeds/ (seed data is compatible with these shapes)
 *
 * Response shapes match:
 *   GET  /settings               → {status, data: [...]}
 *   GET  /positions              → {status, data: [...]}
 *   GET  /portfolio              → {status, data: {...}}
 *   POST /portfolio/size         → {status, data: {...}}
 *   POST /portfolio/position     → {status, data: {...}}
 *   GET  /notifications?page=N  → {status, data: {notifications, has_more}}
 *
 * Usage: import in Playwright tests, pass to page.route() mock handler.
 */

'use strict';

// ---------------------------------------------------------------------------
// GET /settings  (used by TradeEntry on mount)
// ---------------------------------------------------------------------------
const SMOKE_SETTINGS = {
  status: 'ok',
  data: [
    {
      id: 'settings-smoke-1',
      min_hold_days: 5,
      atr_multiplier_initial: 2.0,
      atr_multiplier_trailing: 3.0,
      atr_period: 14,
      default_currency: 'GBP',
      uk_commission: 11.95,
      us_commission: 0.0,
      stamp_duty_rate: 0.5,
      fx_fee_rate: 0.5,
      min_trades_for_analytics: 10,
      default_risk_percent: 1.0,
    },
  ],
};

// ---------------------------------------------------------------------------
// GET /positions  (used by Positions page + TradeEntry position-tags query)
//
// NOTE: /positions returns a raw array (no {status,data} envelope).
// base44Client uses doFetch('/positions', { raw: true }) — raw:true bypasses
// envelope unwrapping and returns the JSON as-is. Mock must match this shape.
// ---------------------------------------------------------------------------
const SMOKE_POSITIONS = [
  {
    id: 'smoke-pos-lgen',
    portfolio_id: 'smoke-portfolio-1',
    ticker: 'LGEN',
    market: 'UK',
    entry_date: '2026-03-01',
    entry_price: 2.45,
    current_price: 2.52,
    current_stop: 2.20,
    shares: 1000,
    total_cost: 2461.95,
    fees_paid: 11.95,
    pnl: 70.05,
    pnl_pct: 2.85,
    status: 'open',
    holding_days: 24,
    grace_period: false,
    grace_days_remaining: null,
    tags: ['momentum'],
  },
  {
    id: 'smoke-pos-barc',
    portfolio_id: 'smoke-portfolio-1',
    ticker: 'BARC',
    market: 'UK',
    entry_date: '2026-03-10',
    entry_price: 2.10,
    current_price: 2.18,
    current_stop: 1.90,
    shares: 1200,
    total_cost: 2531.95,
    fees_paid: 11.95,
    pnl: 96.05,
    pnl_pct: 3.79,
    status: 'open',
    holding_days: 15,
    grace_period: false,
    grace_days_remaining: null,
    tags: ['breakout'],
  },
];

// ---------------------------------------------------------------------------
// GET /portfolio  (used by Positions page and PositionSizingWidget)
// ---------------------------------------------------------------------------
const SMOKE_PORTFOLIO = {
  status: 'ok',
  data: {
    id: 'smoke-portfolio-1',
    cash: 15006.10,
    initial_cash: 20000.00,
    portfolio_heat_percent: 5.24,
    peak_portfolio_value: 20000.00,
    current_drawdown_percent: 0.0,
    days_underwater: 0,
    position_risks: [
      { ticker: 'LGEN', position_risk_gbp: 300.00 },
      { ticker: 'BARC', position_risk_gbp: 240.00 },
    ],
    positions: SMOKE_POSITIONS,
  },
};

// ---------------------------------------------------------------------------
// POST /portfolio/size  (PositionSizingWidget — auto-fills shares)
// Returns suggested_shares=100 so TradeEntry isFormValid becomes true.
// ---------------------------------------------------------------------------
const SMOKE_SIZE_RESULT = {
  status: 'ok',
  data: {
    valid: true,
    cash_sufficient: true,
    suggested_shares: 100,
    position_size_gbp: 245.00,
    risk_amount_gbp: 30.00,
    risk_percent: 1.0,
    max_affordable_shares: null,
    portfolio_cash: 15006.10,
  },
};

// ---------------------------------------------------------------------------
// POST /portfolio/position  (created position response)
// ---------------------------------------------------------------------------
const SMOKE_POSITION_CREATED = {
  status: 'ok',
  data: {
    id: 'smoke-created-pos-1',
    portfolio_id: 'smoke-portfolio-1',
    ticker: 'LGEN',
    market: 'UK',
    entry_date: '2026-03-25',
    entry_price: 2.45,
    shares: 100,
    total_cost: 256.95,
    fees_paid: 11.95,
    status: 'open',
    holding_days: 0,
    pnl: 0.0,
    pnl_pct: 0.0,
  },
};

// ---------------------------------------------------------------------------
// GET /notifications?page=1  (view alerts path — 1 unread, 1 read)
// ---------------------------------------------------------------------------
const SMOKE_NOTIFICATIONS = {
  status: 'ok',
  data: {
    notifications: [
      {
        id: 'smoke-notif-1',
        alert_type: 'stop_loss_approach',
        title: 'Stop Loss Approaching: LGEN',
        message: 'LGEN is within 5% of your stop loss (220p). Current price: 225p.',
        read: false,
        created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        portfolio_id: 'smoke-portfolio-1',
      },
      {
        id: 'smoke-notif-2',
        alert_type: 'daily_portfolio_summary',
        title: 'Daily Portfolio Summary',
        message: 'Portfolio value: £20,560.00. 2 open positions. Unrealised P&L: +£560.00.',
        read: true,
        created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        portfolio_id: 'smoke-portfolio-1',
      },
    ],
    has_more: false,
  },
};

module.exports = {
  SMOKE_SETTINGS,
  SMOKE_POSITIONS,
  SMOKE_PORTFOLIO,
  SMOKE_SIZE_RESULT,
  SMOKE_POSITION_CREATED,
  SMOKE_NOTIFICATIONS,
};
