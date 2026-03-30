/**
 * Analytics Mock Data — Chart Interactivity Acceptance Tests
 * ST-06: BLG-QA-01 — Playwright E2E for Chart Interactivity
 *
 * Covers scenarios SC-CHART-IX-01 through SC-CHART-IX-06 (16 sub-scenarios).
 * Spec: docs/testing/chart_interactivity_scenarios.md
 *
 * Data contract: GET /trades → { trades: [...] }, GET /settings → [{ ... }]
 *
 * Dataset design:
 *   - 15 closed trades across Jan-Mar 2026, all with stop/entry/exit prices
 *   - JAN_2026_TRADES: 3 known trades with deterministic P&L (data integrity)
 *   - 5+ data points required for UnderwaterChart zoom (MIN_POINTS=4 guard)
 *   - 10+ trades with stop prices for RMultipleAnalysis threshold
 *   - ZERO_TRADES_MONTH: monthlyData entry injected to test non-clickable tile
 */

'use strict';

// ---------------------------------------------------------------------------
// Individual trades
// ---------------------------------------------------------------------------

// Jan 2026 — 3 trades with known P&L: +£150, -£80, +£200 → total +£270
const JAN_T1 = {
  id: 't-jan-1',
  ticker: 'AAAA',
  market: 'UK',
  entry_date: '2026-01-05',
  exit_date: '2026-01-12',
  entry_price: 100.00,
  exit_price: 115.00,
  stop_price: 90.00,
  shares: 10,
  pnl: 150.00,
  pnl_percent: 15.0,
  exit_reason: 'target',
  tags: ['momentum'],
};

const JAN_T2 = {
  id: 't-jan-2',
  ticker: 'BBBB',
  market: 'UK',
  entry_date: '2026-01-10',
  exit_date: '2026-01-20',
  entry_price: 50.00,
  exit_price: 42.00,
  stop_price: 44.00,
  shares: 10,
  pnl: -80.00,
  pnl_percent: -16.0,
  exit_reason: 'stop_hit',
  tags: ['breakout'],
};

const JAN_T3 = {
  id: 't-jan-3',
  ticker: 'CCCC',
  market: 'UK',
  entry_date: '2026-01-15',
  exit_date: '2026-01-28',
  entry_price: 80.00,
  exit_price: 105.00,
  stop_price: 72.00,
  shares: 8,
  pnl: 200.00,
  pnl_percent: 31.25,
  exit_reason: 'target',
  tags: ['momentum'],
};

// Feb 2026 — 5 trades
const FEB_T1 = {
  id: 't-feb-1',
  ticker: 'DDDD',
  market: 'UK',
  entry_date: '2026-02-02',
  exit_date: '2026-02-10',
  entry_price: 60.00,
  exit_price: 72.00,
  stop_price: 54.00,
  shares: 10,
  pnl: 120.00,
  pnl_percent: 20.0,
  exit_reason: 'target',
  tags: ['breakout'],
};

const FEB_T2 = {
  id: 't-feb-2',
  ticker: 'EEEE',
  market: 'US',
  entry_date: '2026-02-05',
  exit_date: '2026-02-12',
  entry_price: 40.00,
  exit_price: 35.00,
  stop_price: 36.00,
  shares: 20,
  pnl: -100.00,
  pnl_percent: -12.5,
  exit_reason: 'stop_hit',
  tags: [],
};

const FEB_T3 = {
  id: 't-feb-3',
  ticker: 'FFFF',
  market: 'UK',
  entry_date: '2026-02-08',
  exit_date: '2026-02-15',
  entry_price: 90.00,
  exit_price: 99.00,
  stop_price: 81.00,
  shares: 10,
  pnl: 90.00,
  pnl_percent: 10.0,
  exit_reason: 'manual',
  tags: ['momentum'],
};

const FEB_T4 = {
  id: 't-feb-4',
  ticker: 'GGGG',
  market: 'UK',
  entry_date: '2026-02-14',
  exit_date: '2026-02-20',
  entry_price: 120.00,
  exit_price: 108.00,
  stop_price: 108.00,
  shares: 5,
  pnl: -60.00,
  pnl_percent: -10.0,
  exit_reason: 'stop_hit',
  tags: [],
};

const FEB_T5 = {
  id: 't-feb-5',
  ticker: 'HHHH',
  market: 'US',
  entry_date: '2026-02-18',
  exit_date: '2026-02-25',
  entry_price: 200.00,
  exit_price: 230.00,
  stop_price: 180.00,
  shares: 5,
  pnl: 150.00,
  pnl_percent: 15.0,
  exit_reason: 'target',
  tags: ['breakout'],
};

// Mar 2026 — 7 trades (within last_month window from 2026-03-25)
const MAR_T1 = {
  id: 't-mar-1',
  ticker: 'IIII',
  market: 'UK',
  entry_date: '2026-03-01',
  exit_date: '2026-03-05',
  entry_price: 50.00,
  exit_price: 62.00,
  stop_price: 45.00,
  shares: 10,
  pnl: 120.00,
  pnl_percent: 24.0,
  exit_reason: 'target',
  tags: ['momentum'],
};

const MAR_T2 = {
  id: 't-mar-2',
  ticker: 'JJJJ',
  market: 'UK',
  entry_date: '2026-03-03',
  exit_date: '2026-03-07',
  entry_price: 75.00,
  exit_price: 67.50,
  stop_price: 67.50,
  shares: 10,
  pnl: -75.00,
  pnl_percent: -10.0,
  exit_reason: 'stop_hit',
  tags: [],
};

const MAR_T3 = {
  id: 't-mar-3',
  ticker: 'KKKK',
  market: 'US',
  entry_date: '2026-03-06',
  exit_date: '2026-03-10',
  entry_price: 300.00,
  exit_price: 336.00,
  stop_price: 270.00,
  shares: 5,
  pnl: 180.00,
  pnl_percent: 12.0,
  exit_reason: 'target',
  tags: ['breakout', 'momentum'],
};

const MAR_T4 = {
  id: 't-mar-4',
  ticker: 'LLLL',
  market: 'UK',
  entry_date: '2026-03-10',
  exit_date: '2026-03-14',
  entry_price: 40.00,
  exit_price: 36.00,
  stop_price: 36.00,
  shares: 15,
  pnl: -60.00,
  pnl_percent: -10.0,
  exit_reason: 'stop_hit',
  tags: [],
};

const MAR_T5 = {
  id: 't-mar-5',
  ticker: 'MMMM',
  market: 'UK',
  entry_date: '2026-03-12',
  exit_date: '2026-03-17',
  entry_price: 110.00,
  exit_price: 132.00,
  stop_price: 99.00,
  shares: 5,
  pnl: 110.00,
  pnl_percent: 20.0,
  exit_reason: 'target',
  tags: ['momentum'],
};

const MAR_T6 = {
  id: 't-mar-6',
  ticker: 'NNNN',
  market: 'US',
  entry_date: '2026-03-15',
  exit_date: '2026-03-19',
  entry_price: 80.00,
  exit_price: 72.00,
  stop_price: 72.00,
  shares: 10,
  pnl: -80.00,
  pnl_percent: -10.0,
  exit_reason: 'stop_hit',
  tags: [],
};

const MAR_T7 = {
  id: 't-mar-7',
  ticker: 'OOOO',
  market: 'UK',
  entry_date: '2026-03-18',
  exit_date: '2026-03-22',
  entry_price: 55.00,
  exit_price: 66.00,
  stop_price: 49.50,
  shares: 10,
  pnl: 110.00,
  pnl_percent: 20.0,
  exit_reason: 'target',
  tags: ['breakout'],
};

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

/** Full dataset — 15 trades across 3 months */
const ALL_TRADES = {
  trades: [
    JAN_T1, JAN_T2, JAN_T3,
    FEB_T1, FEB_T2, FEB_T3, FEB_T4, FEB_T5,
    MAR_T1, MAR_T2, MAR_T3, MAR_T4, MAR_T5, MAR_T6, MAR_T7,
  ],
};

/**
 * Jan 2026 known values (for SC-CHART-IX-01d / SC-CHART-IX-06a):
 *   count = 3
 *   totalPnl = +£150 + (−£80) + £200 = +£270.00
 */
const JAN_2026_EXPECTED = {
  monthKey: '2026-01',
  tradeCount: 3,
  totalPnl: 270.00,
};

/**
 * Settings mock — sets min_trades_for_analytics=1 so analytics render with
 * any non-empty dataset. Returned as array (matches settingsRaw[0] branch).
 */
const ANALYTICS_SETTINGS = [{ min_trades_for_analytics: 1 }];

module.exports = {
  ALL_TRADES,
  JAN_2026_EXPECTED,
  ANALYTICS_SETTINGS,
};
