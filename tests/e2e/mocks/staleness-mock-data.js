/**
 * Staleness Indicator Mock Data — SC-STALE-01 through SC-STALE-05
 * ST-02 (BLG-FEAT-09, v2.3): Metrics Staleness Indicator
 *
 * Spec: docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md
 *       docs/specs/frontend/pages/analytics.md §Metrics Staleness Indicator
 */

'use strict';

// ---------------------------------------------------------------------------
// Timestamps
// ---------------------------------------------------------------------------

/** 10 minutes ago — well within the 4h freshness threshold. */
const FRESH_SYNC_AT = new Date(Date.now() - 10 * 60 * 1000).toISOString();

/** 5 hours ago — beyond the 4h stale threshold. */
const STALE_SYNC_AT = new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString();

/** Fixed timestamp for tooltip assertion tests. */
const FIXED_SYNC_AT = '2026-03-29T09:41:00.000000+00:00';

// ---------------------------------------------------------------------------
// Minimal GET /analytics/metrics responses
// Only last_sync_at matters for staleness tests; other fields are stubs.
// ---------------------------------------------------------------------------

function makeAnalyticsMetrics(lastSyncAt) {
  return {
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
      last_sync_at: lastSyncAt,
    },
  };
}

/** Fresh data response (last_sync_at = 10 mins ago). */
const ANALYTICS_FRESH = makeAnalyticsMetrics(FRESH_SYNC_AT);

/** Stale data response (last_sync_at = 5 hours ago). */
const ANALYTICS_STALE = makeAnalyticsMetrics(STALE_SYNC_AT);

/** Response with last_sync_at absent — indicator should be hidden. */
const ANALYTICS_NO_SYNC_AT = makeAnalyticsMetrics(null);

/** Fixed timestamp response — for tooltip text assertion. */
const ANALYTICS_FIXED_TS = makeAnalyticsMetrics(FIXED_SYNC_AT);

// ---------------------------------------------------------------------------
// GET /trades — 10 closed trades, enough to pass min_trades_for_analytics
// Used by PerformanceAnalytics to render the main content path.
// Minimal fields; values need not be financially meaningful.
// ---------------------------------------------------------------------------

function makeTrade(n) {
  const exitDate = new Date(Date.now() - n * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
  const entryDate = new Date(Date.now() - (n + 5) * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
  return {
    id: `trade-${n}`,
    ticker: 'AAPL',
    market: 'US',
    entry_date: entryDate,
    exit_date: exitDate,
    entry_price: 100,
    exit_price: n % 2 === 0 ? 110 : 95,
    shares: 10,
    pnl: n % 2 === 0 ? 100 : -50,
    pnl_pct: n % 2 === 0 ? 10 : -5,
    pnl_percent: n % 2 === 0 ? 10 : -5,
    exit_reason: 'manual',
    holding_days: 5,
    tags: [],
  };
}

const TEN_TRADES = { trades: Array.from({ length: 10 }, (_, i) => makeTrade(i + 1)) };

// ---------------------------------------------------------------------------
// GET /settings — minimal to satisfy PerformanceAnalytics default
// ---------------------------------------------------------------------------

const SETTINGS_DEFAULT = [{ min_trades_for_analytics: 10 }];

// ---------------------------------------------------------------------------
// Stub responses for analytics sub-endpoints
// (CohortAnalysis, RMultipleDistribution, DisciplineComplianceSection)
// Empty but structurally valid — prevents console errors without affecting test assertions.
// ---------------------------------------------------------------------------

const COHORT_EMPTY = { status: 'ok', data: { cohorts: [], has_enough_data: false } };
const R_MULTIPLE_EMPTY = { status: 'ok', data: { buckets: [], summary: {}, has_enough_data: false } };
const COMPLIANCE_EMPTY = { status: 'ok', data: {} };

// ---------------------------------------------------------------------------
// GET /positions — empty list for Positions page tests
// ---------------------------------------------------------------------------

const POSITIONS_EMPTY = [];

module.exports = {
  FRESH_SYNC_AT,
  STALE_SYNC_AT,
  FIXED_SYNC_AT,
  ANALYTICS_FRESH,
  ANALYTICS_STALE,
  ANALYTICS_NO_SYNC_AT,
  ANALYTICS_FIXED_TS,
  TEN_TRADES,
  SETTINGS_DEFAULT,
  COHORT_EMPTY,
  R_MULTIPLE_EMPTY,
  COMPLIANCE_EMPTY,
  POSITIONS_EMPTY,
};
