/**
 * Morning Briefing — Playwright Acceptance Tests
 * ST-02 (EPIC-02, v6.0) — BLG-FEAT-46 AC-09
 *
 * Covers observable ACs for the MorningBriefing section on DashboardHome:
 *
 *   SC-MB-01  Morning Briefing section renders on DashboardHome page load (AC-01)
 *   SC-MB-02  All 5 card types show data or empty state without error (AC-07)
 *   SC-MB-03  Screener Hits card renders and links to /Screener (AC-02)
 *   SC-MB-04  Positions to Watch card renders and links to /Positions (AC-03)
 *   SC-MB-05  Red Flags card renders and links to /RedFlagJournal (AC-04)
 *   SC-MB-06  Earnings card renders and links to /Positions (AC-05)
 *   SC-MB-07  Compliance card renders and links to /PerformanceAnalytics (AC-06)
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * ROUTING NOTE: App uses HashRouter. Navigation uses page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Mock payloads
// ---------------------------------------------------------------------------

const SIGNALS_EMPTY = [];
const SIGNALS_WITH_NEW = [
  { id: 'sig-1', ticker: 'AAPL', status: 'new', momentum_percent: 12.3, signal_date: '2026-06-19' },
  { id: 'sig-2', ticker: 'MSFT', status: 'new', momentum_percent: 8.5, signal_date: '2026-06-19' },
  { id: 'sig-3', ticker: 'TSLA', status: 'entered', momentum_percent: 5.0, signal_date: '2026-06-18' },
];

const POSITIONS_EMPTY = [];
const POSITIONS_WITH_GRACE = [
  {
    id: 'pos-1', ticker: 'NVDA', market: 'US', grace_period: true,
    grace_days_remaining: 3, display_status: 'GRACE', entry_date: '2026-06-16',
  },
  {
    id: 'pos-2', ticker: 'BA', market: 'US', grace_period: false,
    grace_days_remaining: null, display_status: 'PROFITABLE', entry_date: '2026-05-01',
  },
];

const GRACE_ALERTS_EMPTY = { status: 'ok', data: [] };
const GRACE_ALERTS_WITH_ALERT = {
  status: 'ok',
  data: [{ position_id: 'pos-exit', ticker: 'AAPL', market: 'US', days_in_state: 9 }],
};

const RED_FLAG_JOURNAL_EMPTY = {
  status: 'ok',
  data: { total: 0, page: 1, page_size: 1, items: [] },
};
const RED_FLAG_JOURNAL_WITH_EVENTS = {
  status: 'ok',
  data: { total: 3, page: 1, page_size: 1, items: [
    { id: 'rfj-1', event_type: 'pre_entry_override', ticker: 'TSLA', created_at: '2026-06-19T10:00:00Z' },
  ]},
};

const EARNINGS_NO_DATE = { ticker: 'NVDA', next_earnings_date: null, days_until_earnings: null };
const EARNINGS_WITHIN_7D = { ticker: 'BA', next_earnings_date: '2026-06-24', days_until_earnings: 5 };

const ARC5_7D = {
  status: 'ok',
  data: {
    period: '7d',
    validation_pass_rate_by_rule: { regime_gate: { pass_rate: 0.85, pass_count: 17, fail_count: 3 } },
    events_per_week: 1.4,
    override_rate: 0.1,
    top_rule_breach: 'regime_gate',
    trade_plan_adherence_rate: 0.80,
  },
};
const ARC5_30D = {
  status: 'ok',
  data: {
    period: '30d',
    validation_pass_rate_by_rule: { regime_gate: { pass_rate: 0.78, pass_count: 60, fail_count: 17 } },
    events_per_week: 1.6,
    override_rate: 0.12,
    top_rule_breach: 'regime_gate',
    trade_plan_adherence_rate: 0.75,
  },
};

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
}

async function mockAllMorningBriefingEndpoints(page, {
  signals = SIGNALS_EMPTY,
  positions = POSITIONS_EMPTY,
  graceAlerts = GRACE_ALERTS_EMPTY,
  redFlags = RED_FLAG_JOURNAL_EMPTY,
  arc5_7d = ARC5_7D,
  arc5_30d = ARC5_30D,
} = {}) {
  await page.route(`${API}/signals`, route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(signals) })
  );
  await page.route(`${API}/positions`, route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) })
  );
  await page.route(`${API}/positions/grace-period-alerts`, route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(graceAlerts) })
  );
  await page.route(new RegExp(`${API}/portfolio/red-flag-journal`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(redFlags) })
  );
  await page.route(new RegExp(`${API}/earnings/`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EARNINGS_NO_DATE) })
  );
  await page.route(new RegExp(`${API}/analytics/arc5-compliance\\?period=7d`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(arc5_7d) })
  );
  await page.route(new RegExp(`${API}/analytics/arc5-compliance\\?period=30d`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(arc5_30d) })
  );
}

async function gotoDashboard(page) {
  await page.goto('/#/DashboardHome');
  await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-MB-01 — Morning Briefing section renders on page load (AC-01)
// ---------------------------------------------------------------------------

test.describe('SC-MB-01 — Morning Briefing section renders', () => {
  test('SC-MB-01: Morning Briefing heading visible on DashboardHome page load', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('[data-testid="morning-briefing"]')).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-MB-02 — All 5 card types show data or empty state (AC-07)
// ---------------------------------------------------------------------------

test.describe('SC-MB-02 — All 5 cards render without error', () => {
  test('SC-MB-02: All 5 card titles visible in empty state', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Screener Hits')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Positions to Watch')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Red Flags')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Earnings')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Arc 5 Compliance')).toBeVisible({ timeout: 5000 });
  });

  test('SC-MB-02b: Empty state text renders for all cards with no data', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('No new signals')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('No positions to watch')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('No red flags this week')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('No earnings in 7 days')).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-MB-03 — Screener Hits card with data (AC-02)
// ---------------------------------------------------------------------------

test.describe('SC-MB-03 — Screener Hits card (AC-02)', () => {
  test('SC-MB-03: Screener hits count shows new signals count', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page, { signals: SIGNALS_WITH_NEW });
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    // 2 signals have status=new in SIGNALS_WITH_NEW
    await expect(page.getByText('2')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/new signals today/)).toBeVisible({ timeout: 5000 });
  });

  test('SC-MB-03b: Screener Hits card links to /Screener', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Screener Hits')).toBeVisible({ timeout: 5000 });
    const screenerLink = page.locator('[data-testid="morning-briefing"] a[href*="Screener"]');
    await expect(screenerLink.first()).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-MB-04 — Positions to Watch card (AC-03)
// ---------------------------------------------------------------------------

test.describe('SC-MB-04 — Positions to Watch card (AC-03)', () => {
  test('SC-MB-04: Positions with grace period shown in Positions to Watch', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page, {
      positions: POSITIONS_WITH_GRACE,
      graceAlerts: GRACE_ALERTS_EMPTY,
    });
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    // 1 position has grace_period=true
    await expect(page.getByText(/in grace/)).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-MB-05 — Red Flags card (AC-04)
// ---------------------------------------------------------------------------

test.describe('SC-MB-05 — Red Flags card (AC-04)', () => {
  test('SC-MB-05: Red flags count shows events from last 7 days', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page, { redFlags: RED_FLAG_JOURNAL_WITH_EVENTS });
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    // total=3 events
    await expect(page.getByText('3')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/events in last 7 days/)).toBeVisible({ timeout: 5000 });
  });

  test('SC-MB-05b: Red Flags card links to /RedFlagJournal', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    const link = page.locator('a[href*="RedFlagJournal"]');
    await expect(link.first()).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-MB-06 — Earnings card (AC-05)
// ---------------------------------------------------------------------------

test.describe('SC-MB-06 — Earnings card (AC-05)', () => {
  test('SC-MB-06: Earnings card links to /Positions', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Earnings')).toBeVisible({ timeout: 5000 });
    const link = page.locator('a[href*="Positions"]');
    await expect(link.first()).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// SC-MB-07 — Compliance card (AC-06)
// ---------------------------------------------------------------------------

test.describe('SC-MB-07 — Compliance card (AC-06)', () => {
  test('SC-MB-07: Compliance score and trend visible', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Arc 5 Compliance')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('7-day compliance score')).toBeVisible({ timeout: 5000 });
  });

  test('SC-MB-07b: Compliance card links to /PerformanceAnalytics', async ({ page }) => {
    await mockFallback(page);
    await mockAllMorningBriefingEndpoints(page);
    await gotoDashboard(page);

    await expect(page.getByText('Morning Briefing')).toBeVisible({ timeout: 10000 });
    const link = page.locator('a[href*="PerformanceAnalytics"]');
    await expect(link.first()).toBeVisible({ timeout: 5000 });
  });
});
