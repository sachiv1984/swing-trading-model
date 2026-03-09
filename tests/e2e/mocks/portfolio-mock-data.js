/**
 * Portfolio Mock Data — Risk Dashboard Acceptance Tests
 * ST-11: Canonical Test Scenario Library Phase 1
 *
 * Each constant corresponds to a test dataset defined in:
 * docs/testing/risk_dashboard_scenarios.md §4 (TD-01 through TD-10)
 *
 * These objects match the GET /portfolio response shape produced by
 * backend/services/portfolio_service.py. All monetary values in GBP.
 * Portfolio value = £10,000 in all datasets unless stated.
 *
 * Usage: import in Playwright tests, pass to page.route() mock handler.
 */

'use strict';

// ---------------------------------------------------------------------------
// Shared defaults
// ---------------------------------------------------------------------------

const DEFAULT_PORTFOLIO = {
  current_drawdown_percent: 0.0,
  peak_portfolio_value: 10000.00,
  days_underwater: 0,
};

// ---------------------------------------------------------------------------
// TD-01 — Zero heat, no open positions
// Scenarios: SC-RD-01, SC-RD-13, SC-RD-15, SC-RD-25
// ---------------------------------------------------------------------------

const TD_01 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 0.0,
  position_risks: [],
  positions: [],
};

// ---------------------------------------------------------------------------
// TD-02 — Heat 9.9% (just below 10% boundary — Low band)
// Scenarios: SC-RD-02
// ---------------------------------------------------------------------------

const TD_02 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 9.9,
  position_risks: [{ ticker: 'ALPHA', position_risk_gbp: 990.00 }],
  positions: [
    {
      id: 'p-alpha',
      ticker: 'ALPHA',
      market: 'UK',
      status: 'open',
      entry_price: 99.00,
      current_price: 95.00,
      current_stop: 89.10,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'LOSING',
      holding_days: 15,
      entry_date: '2026-02-23',
    },
  ],
};

// ---------------------------------------------------------------------------
// TD-03 — Heat exactly 10.0% (Moderate boundary)
// Derivation: (100.00 − 90.00) × 100 / 10000 × 100 = 10.0%
// Scenarios: SC-RD-03
// ---------------------------------------------------------------------------

const TD_03 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 10.0,
  position_risks: [{ ticker: 'BRAVO', position_risk_gbp: 1000.00 }],
  positions: [
    {
      id: 'p-bravo',
      ticker: 'BRAVO',
      market: 'UK',
      status: 'open',
      entry_price: 100.00,
      current_price: 95.00,
      current_stop: 90.00,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'LOSING',
      holding_days: 10,
      entry_date: '2026-02-28',
    },
  ],
};

// ---------------------------------------------------------------------------
// TD-04 — Heat exactly 20.0% (High boundary)
// Derivation: (100.00 − 80.00) × 100 / 10000 × 100 = 20.0%
// Scenarios: SC-RD-04
// ---------------------------------------------------------------------------

const TD_04 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 20.0,
  position_risks: [{ ticker: 'CHARLIE', position_risk_gbp: 2000.00 }],
  positions: [
    {
      id: 'p-charlie',
      ticker: 'CHARLIE',
      market: 'UK',
      status: 'open',
      entry_price: 100.00,
      current_price: 88.00,
      current_stop: 80.00,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'LOSING',
      holding_days: 7,
      entry_date: '2026-03-01',
    },
  ],
};

// ---------------------------------------------------------------------------
// TD-05 — Heat exactly 30.0% (Extreme boundary)
// Derivation: (100.00 − 70.00) × 100 / 10000 × 100 = 30.0%
// Scenarios: SC-RD-05
// ---------------------------------------------------------------------------

const TD_05 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 30.0,
  position_risks: [{ ticker: 'DELTA', position_risk_gbp: 3000.00 }],
  positions: [
    {
      id: 'p-delta',
      ticker: 'DELTA',
      market: 'UK',
      status: 'open',
      entry_price: 100.00,
      current_price: 78.00,
      current_stop: 70.00,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'LOSING',
      holding_days: 5,
      entry_date: '2026-03-03',
    },
  ],
};

// ---------------------------------------------------------------------------
// TD-06 — Heat 35.0% (above 30% — deep Extreme)
// Derivation: (100.00 − 65.00) × 100 / 10000 × 100 = 35.0%
// Scenarios: SC-RD-06
// ---------------------------------------------------------------------------

const TD_06 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 35.0,
  position_risks: [{ ticker: 'ECHO', position_risk_gbp: 3500.00 }],
  positions: [
    {
      id: 'p-echo',
      ticker: 'ECHO',
      market: 'UK',
      status: 'open',
      entry_price: 100.00,
      current_price: 72.00,
      current_stop: 65.00,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'LOSING',
      holding_days: 3,
      entry_date: '2026-03-05',
    },
  ],
};

// ---------------------------------------------------------------------------
// TD-07 — Grace period colour coding (3 grace + 1 non-grace)
// Sort: ascending by grace_days_remaining (FOXT 1 < GOLF 4 < HOTL 5)
// Scenarios: SC-RD-07, SC-RD-08, SC-RD-09, SC-RD-10, SC-RD-11
// ---------------------------------------------------------------------------

const TD_07 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 8.0,
  position_risks: [],
  positions: [
    {
      id: 'p-foxt',
      ticker: 'FOXT',
      market: 'UK',
      status: 'open',
      entry_price: 50.00,
      current_price: 48.00,
      current_stop: 45.00,
      shares: 100,
      grace_period: true,
      grace_days_remaining: 1,
      display_status: 'GRACE',
      holding_days: 9,
      entry_date: '2026-02-28',
    },
    {
      id: 'p-golf',
      ticker: 'GOLF',
      market: 'UK',
      status: 'open',
      entry_price: 60.00,
      current_price: 58.00,
      current_stop: 54.00,
      shares: 100,
      grace_period: true,
      grace_days_remaining: 4,
      display_status: 'GRACE',
      holding_days: 6,
      entry_date: '2026-03-03',
    },
    {
      id: 'p-hotl',
      ticker: 'HOTL',
      market: 'UK',
      status: 'open',
      entry_price: 70.00,
      current_price: 68.00,
      current_stop: 63.00,
      shares: 100,
      grace_period: true,
      grace_days_remaining: 5,
      display_status: 'GRACE',
      holding_days: 5,
      entry_date: '2026-03-04',
    },
    {
      id: 'p-indi',
      ticker: 'INDI',
      market: 'UK',
      status: 'open',
      entry_price: 80.00,
      current_price: 82.00,
      current_stop: 72.00,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'PROFITABLE',
      holding_days: 20,
      entry_date: '2026-02-18',
    },
  ],
};

// ---------------------------------------------------------------------------
// TD-08 — Grace period at day 10 (within grace) and expired excluded
// Scenarios: SC-RD-12
// ---------------------------------------------------------------------------

const TD_08 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 3.0,
  position_risks: [],
  positions: [
    {
      id: 'p-juliet',
      ticker: 'JULIET',
      market: 'UK',
      status: 'open',
      entry_price: 40.00,
      current_price: 38.00,
      current_stop: 36.00,
      shares: 150,
      grace_period: true,
      grace_days_remaining: 10,
      display_status: 'GRACE',
      holding_days: 1,
      entry_date: '2026-03-08',
    },
    {
      id: 'p-kilo',
      ticker: 'KILO',
      market: 'UK',
      status: 'open',
      entry_price: 50.00,
      current_price: 48.00,
      current_stop: 44.00,
      shares: 50,
      grace_period: false,
      grace_days_remaining: 0,
      display_status: 'LOSING',
      holding_days: 12,
      entry_date: '2026-02-26',
    },
  ],
};

// ---------------------------------------------------------------------------
// TD-09 — All three position states simultaneously (for sort order tests)
// Canonical sort: GRACE asc stop-dist, LOSING asc stop-dist, PROFITABLE
// Scenarios: SC-RD-14 (canonical sort verification)
// ---------------------------------------------------------------------------

const TD_09 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 5.0,
  position_risks: [],
  positions: [
    {
      id: 'p-lima',
      ticker: 'LIMA',
      market: 'UK',
      status: 'open',
      entry_price: 6.00,
      current_price: 5.00,
      current_stop: 4.80,
      shares: 500,
      grace_period: true,
      grace_days_remaining: 5,
      display_status: 'GRACE',
      holding_days: 5,
      entry_date: '2026-03-04',
    },
    {
      id: 'p-mike',
      ticker: 'MIKE',
      market: 'UK',
      status: 'open',
      entry_price: 9.00,
      current_price: 8.00,
      current_stop: 7.50,
      shares: 200,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'LOSING',
      holding_days: 12,
      entry_date: '2026-02-26',
    },
    {
      id: 'p-novem',
      ticker: 'NOVEM',
      market: 'UK',
      status: 'open',
      entry_price: 9.00,
      current_price: 8.00,
      current_stop: 7.00,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'LOSING',
      holding_days: 8,
      entry_date: '2026-03-01',
    },
    {
      id: 'p-oscar',
      ticker: 'OSCAR',
      market: 'UK',
      status: 'open',
      entry_price: 12.00,
      current_price: 15.00,
      current_stop: 12.00,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'PROFITABLE',
      holding_days: 30,
      entry_date: '2026-02-08',
    },
  ],
};

// ---------------------------------------------------------------------------
// TD-10 — Prospective heat: current state for SC-RD-16
// Current portfolio_heat_percent = 15.0%; risk = £1,500
// Scenarios: SC-RD-16
// ---------------------------------------------------------------------------

const TD_10 = {
  ...DEFAULT_PORTFOLIO,
  portfolio_heat_percent: 15.0,
  position_risks: [{ ticker: 'EXISTING', position_risk_gbp: 1500.00 }],
  positions: [
    {
      id: 'p-existing',
      ticker: 'EXISTING',
      market: 'UK',
      status: 'open',
      entry_price: 100.00,
      current_price: 96.00,
      current_stop: 85.00,
      shares: 100,
      grace_period: false,
      grace_days_remaining: null,
      display_status: 'LOSING',
      holding_days: 8,
      entry_date: '2026-03-01',
    },
  ],
};

// ---------------------------------------------------------------------------
// Prospective heat API responses (GET /portfolio/prospective-heat)
// ---------------------------------------------------------------------------

// SC-RD-16: PAPA at entry=20, stop=14, shares=100 → 21.0% projected
const PROSPECTIVE_HEAT_TD10_ABOVE_20 = {
  projected_heat_percent: 21.0,
  added_risk_gbp: 600.0,
};

// SC-RD-18: Any valid inputs with current heat 9.0% → 12.0% projected
const PROSPECTIVE_HEAT_GENERIC = {
  projected_heat_percent: 12.0,
  added_risk_gbp: 300.0,
};

// ---------------------------------------------------------------------------
// Empty positions endpoint response (used for entity fallback suppression in
// error-state scenarios — prevents entity fallback from hiding the error card)
// ---------------------------------------------------------------------------

const EMPTY_POSITIONS = [];

module.exports = {
  TD_01,
  TD_02,
  TD_03,
  TD_04,
  TD_05,
  TD_06,
  TD_07,
  TD_08,
  TD_09,
  TD_10,
  PROSPECTIVE_HEAT_TD10_ABOVE_20,
  PROSPECTIVE_HEAT_GENERIC,
  EMPTY_POSITIONS,
};
