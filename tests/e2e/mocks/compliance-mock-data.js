/**
 * Compliance Panel Mock Data — SC-COMP-01 through SC-COMP-07
 * ST-01 (BLG-FEAT-11, v2.3): Strategy Compliance Score (Display-Only)
 *
 * Spec: docs/specs/frontend/pages/positions.md §Strategy Compliance Panel
 *       docs/design/2026-03-24__release-v2.3/compliance-panel/ux_spec.md
 */

'use strict';

// ---------------------------------------------------------------------------
// GET /positions — two open positions for Table View rendering
// Fields mirror what get_positions_with_prices() returns. Only fields
// actually read by Positions.js table view render path are included.
// ---------------------------------------------------------------------------

const TWO_OPEN_POSITIONS = [
  {
    id: 'pos-1',
    ticker: 'AAPL',
    market: 'US',
    entry_date: '2026-03-01',
    entry_price: 180.00,
    current_price: 190.00,
    current_price_native: 190.00,
    stop_price: 170.00,
    stop_price_native: 170.00,
    shares: 10,
    pnl: 100.00,
    pnl_percent: 5.56,
    holding_days: 28,
    grace_days_remaining: null,
    grace_period: false,
    status: 'open',
    display_status: 'PROFITABLE',
    tags: [],
    entry_note: null,
    exit_note: null,
  },
  {
    id: 'pos-2',
    ticker: 'SHEL',
    market: 'UK',
    entry_date: '2026-03-17',
    entry_price: 2600.00,
    current_price: 2650.00,
    current_price_native: 2650.00,
    stop_price: 2450.00,
    stop_price_native: 2450.00,
    shares: 5,
    pnl: 25.00,
    pnl_percent: 1.92,
    holding_days: 12,
    grace_days_remaining: null,
    grace_period: false,
    status: 'open',
    display_status: 'PROFITABLE',
    tags: [],
    entry_note: null,
    exit_note: null,
  },
];

// ---------------------------------------------------------------------------
// GET /positions/compliance — response variants
// ---------------------------------------------------------------------------

/** All positions compliant — green badge, panel collapsed by default. */
const COMPLIANCE_ALL_COMPLIANT = {
  status: 'ok',
  data: {
    overall_status: 'Compliant',
    compliant_count: 2,
    total_count: 2,
    positions: [
      {
        position_id: 'pos-1',
        ticker: 'AAPL',
        market: 'US',
        stop_compliant: true,
        stop_age_days: 28,
        size_compliant: true,
      },
      {
        position_id: 'pos-2',
        ticker: 'SHEL',
        market: 'UK',
        stop_compliant: true,
        stop_age_days: 12,
        size_compliant: true,
      },
    ],
  },
};

/** One non-compliant stop — amber "Needs Attention" badge, expanded by default. */
const COMPLIANCE_NEEDS_ATTENTION = {
  status: 'ok',
  data: {
    overall_status: 'Needs Attention',
    compliant_count: 1,
    total_count: 2,
    positions: [
      {
        position_id: 'pos-1',
        ticker: 'AAPL',
        market: 'US',
        stop_compliant: false,    // non-compliant stop → ⚠️
        stop_age_days: 28,
        size_compliant: true,
      },
      {
        position_id: 'pos-2',
        ticker: 'SHEL',
        market: 'UK',
        stop_compliant: true,
        stop_age_days: 12,
        size_compliant: true,
      },
    ],
  },
};

/** All positions non-compliant (≥50%) — red "Review Required" badge, expanded. */
const COMPLIANCE_REVIEW_REQUIRED = {
  status: 'ok',
  data: {
    overall_status: 'Review Required',
    compliant_count: 0,
    total_count: 2,
    positions: [
      {
        position_id: 'pos-1',
        ticker: 'AAPL',
        market: 'US',
        stop_compliant: false,
        stop_age_days: 28,
        size_compliant: false,
      },
      {
        position_id: 'pos-2',
        ticker: 'SHEL',
        market: 'UK',
        stop_compliant: false,
        stop_age_days: 15,
        size_compliant: false,
      },
    ],
  },
};

/**
 * Grace-period position — null flags for pos-1 (still within first 10 days).
 * Verifies "Not set" stop age display and "—" for null compliance flags.
 */
const COMPLIANCE_WITH_GRACE = {
  status: 'ok',
  data: {
    overall_status: 'Compliant',
    compliant_count: 2,
    total_count: 2,
    positions: [
      {
        position_id: 'pos-1',
        ticker: 'AAPL',
        market: 'US',
        stop_compliant: null,   // grace period — not assessed
        stop_age_days: null,    // grace period — "Not set"
        size_compliant: null,
      },
      {
        position_id: 'pos-2',
        ticker: 'SHEL',
        market: 'UK',
        stop_compliant: true,
        stop_age_days: 12,
        size_compliant: true,
      },
    ],
  },
};

/** No open positions — panel must be hidden entirely. */
const COMPLIANCE_NO_POSITIONS = {
  status: 'ok',
  data: {
    overall_status: 'Compliant',
    compliant_count: 0,
    total_count: 0,
    positions: [],
  },
};

// ---------------------------------------------------------------------------
// GET /analytics/metrics — minimal stub so MetricsStalenessIndicator
// renders without console errors. Staleness is not under test here.
// ---------------------------------------------------------------------------

const ANALYTICS_STUB = {
  status: 'ok',
  data: {
    summary: { total_trades: 0, win_rate: 0, total_pnl: 0, has_enough_data: false, min_required: 10 },
    executive_metrics: {},
    advanced_metrics: {},
    market_comparison: {},
    exit_reasons: [],
    monthly_data: [],
    day_of_week: [],
    holding_periods: [],
    top_performers: { winners: [], losers: [] },
    consistency_metrics: {},
    trades_for_charts: [],
    last_sync_at: null,   // null → staleness indicator hidden, no interference
  },
};

module.exports = {
  TWO_OPEN_POSITIONS,
  COMPLIANCE_ALL_COMPLIANT,
  COMPLIANCE_NEEDS_ATTENTION,
  COMPLIANCE_REVIEW_REQUIRED,
  COMPLIANCE_WITH_GRACE,
  COMPLIANCE_NO_POSITIONS,
  ANALYTICS_STUB,
};
