/**
 * Position Review Cadence Nudge — ST-15 (BLG-FEAT-68, EPIC-03, v7.0)
 *
 * Design source: docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md
 * Spec: docs/specs/frontend/pages/positions.md §Last Reviewed Column
 *
 * Coverage:
 *   SC-RCN-01  Table View — "Reviewed {N}d ago" shown for a position with last_reviewed_at set
 *   SC-RCN-02  Table View — "Not yet reviewed" shown when last_reviewed_at is null
 *   SC-RCN-03  Table View — flagged (amber text + clock icon) when days_since_review >= 14
 *   SC-RCN-04  Table View — flag suppressed when GRACE state with days_in_state >= 8 (AC-04)
 *   SC-RCN-05  Table View — flag suppressed when portfolio drawdown threshold is breached (AC-04)
 *   SC-RCN-06  Table View — clicking "Mark Reviewed" fires PATCH /positions/{id}/mark-reviewed
 *   SC-RCN-07  Grid View — Last Reviewed row shown in card footer with the same text/flag logic
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Positions'). Grid View
 * is the default; Table View requires clicking [aria-label="Table view"].
 */

'use strict';

const { test, expect } = require('@playwright/test');

function makePosition(overrides = {}) {
  const daysAgo = (n) => {
    const d = new Date();
    d.setDate(d.getDate() - n);
    return d.toISOString();
  };
  return {
    id: 'pos-rcn-01',
    ticker: 'AAPL',
    market: 'US',
    entry_price: 150.00,
    current_price: 155.00,
    current_price_native: 160.00,
    stop_price: 140.00,
    stop_price_native: 145.00,
    shares: 10,
    pnl: 50.00,
    pnl_percent: 3.3,
    holding_days: 30,
    grace_days_remaining: null,
    status: 'open',
    entry_date: daysAgo(30),
    initial_stop: 130.00,
    current_trailing_stop: 0,
    risk_off_exit: false,
    lifecycle_state: 'PROFITABLE',
    position_state: 'PROFITABLE',
    days_in_state: 20,
    tags: null,
    last_reviewed_at: null,
    ...overrides,
  };
}

const NO_DRAWDOWN = { threshold_breached: false };
const DRAWDOWN_ACTIVE = { threshold_breached: true, current_drawdown_pct: 12.0, threshold_pct: 10.0 };

async function stubPositionsPage(page, positions, { drawdown = NO_DRAWDOWN } = {}) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance') || url.includes('/grace-period-alerts') || url.includes('/gap-risk')) {
      return route.continue();
    }
    const method = route.request().method();
    if (method === 'PATCH' && url.includes('/mark-reviewed')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { id: 'pos-rcn-01', last_reviewed_at: new Date().toISOString() } }),
      });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) });
  });
  await page.route('**/positions/*/gap-risk', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false } }) })
  );
  await page.route('**/positions/compliance*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/positions/grace-period-alerts', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );
  // Playwright's "*" does not cross "/" — a **/portfolio* glob would never
  // match sub-paths like /portfolio/drawdown-status, so each is registered
  // as its own exact-path route (same convention as epic02-v34-risk-prompts.spec.js).
  await page.route('**/portfolio/drawdown-status', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: drawdown }) })
  );
  await page.route('**/portfolio/concentration-status', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { any_breach: false } }) })
  );
  await page.route('**/portfolio*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null, days_until_earnings: null }) })
  );
}

async function gotoPositionsTable(page, positions, opts) {
  await stubPositionsPage(page, positions, opts);
  await page.goto('/#/Positions');
  const firstTicker = positions[0]?.ticker || 'AAPL';
  await page.waitForSelector(`text=${firstTicker}`, { timeout: 8000 });
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 8000 });
  await tableBtn.click();
  await page.waitForSelector('table', { timeout: 5000 });
}

test('SC-RCN-01: Table View shows "Reviewed {N}d ago" for a reviewed position', async ({ page }) => {
  const fiveDaysAgo = new Date();
  fiveDaysAgo.setDate(fiveDaysAgo.getDate() - 5);
  const pos = makePosition({ last_reviewed_at: fiveDaysAgo.toISOString() });
  await gotoPositionsTable(page, [pos]);

  const cell = page.locator('[data-testid="last-reviewed-cell"]');
  await expect(cell).toBeVisible({ timeout: 5000 });
  await expect(cell).toContainText('Reviewed 5d ago');
});

test('SC-RCN-02: Table View shows "Not yet reviewed" when last_reviewed_at is null', async ({ page }) => {
  const pos = makePosition({ last_reviewed_at: null });
  await gotoPositionsTable(page, [pos]);

  const cell = page.locator('[data-testid="last-reviewed-cell"]');
  await expect(cell).toBeVisible({ timeout: 5000 });
  await expect(cell).toContainText('Not yet reviewed');
});

test('SC-RCN-03: Table View flags (amber + clock icon) when days_since_review >= 14', async ({ page }) => {
  const twentyDaysAgo = new Date();
  twentyDaysAgo.setDate(twentyDaysAgo.getDate() - 20);
  const pos = makePosition({ last_reviewed_at: twentyDaysAgo.toISOString(), position_state: 'PROFITABLE', days_in_state: 20 });
  await gotoPositionsTable(page, [pos]);

  const cell = page.locator('[data-testid="last-reviewed-cell"]');
  const text = cell.locator('span');
  await expect(text).toHaveClass(/text-amber-600/);
  await expect(cell.locator('svg.lucide-clock')).toBeVisible();
});

test('SC-RCN-04: Table View suppresses flag when GRACE state with days_in_state >= 8 (AC-04)', async ({ page }) => {
  const twentyDaysAgo = new Date();
  twentyDaysAgo.setDate(twentyDaysAgo.getDate() - 20);
  const pos = makePosition({
    last_reviewed_at: twentyDaysAgo.toISOString(),
    lifecycle_state: 'GRACE',
    position_state: 'GRACE',
    days_in_state: 8,
  });
  await gotoPositionsTable(page, [pos]);

  const cell = page.locator('[data-testid="last-reviewed-cell"]');
  const text = cell.locator('span');
  // Text still renders (informational), but not flagged amber
  await expect(cell).toContainText('Reviewed 20d ago');
  await expect(text).not.toHaveClass(/text-amber-600/);
  // ST-06 (EPIC-03, v8.6, BLG-FE-149): non-flagged state must use the
  // canonical secondary-text token (text-slate-600 dark:text-slate-400),
  // not the failing text-slate-500 shade this story corrected.
  await expect(text).toHaveClass(/text-slate-600/);
  await expect(text).toHaveClass(/dark:text-slate-400/);
});

test('SC-RCN-05: Table View suppresses flag when portfolio drawdown is active (AC-04)', async ({ page }) => {
  const twentyDaysAgo = new Date();
  twentyDaysAgo.setDate(twentyDaysAgo.getDate() - 20);
  const pos = makePosition({ last_reviewed_at: twentyDaysAgo.toISOString(), position_state: 'PROFITABLE', days_in_state: 20 });
  await gotoPositionsTable(page, [pos], { drawdown: DRAWDOWN_ACTIVE });

  const cell = page.locator('[data-testid="last-reviewed-cell"]');
  const text = cell.locator('span');
  await expect(cell).toContainText('Reviewed 20d ago');
  // Suppression depends on the (independent, async) drawdown-status query
  // resolving — poll rather than a single immediate check.
  await expect(text).not.toHaveClass(/text-amber-600/, { timeout: 8000 });
});

test('SC-RCN-06: Clicking "Mark Reviewed" fires PATCH /positions/{id}/mark-reviewed', async ({ page }) => {
  const pos = makePosition({ last_reviewed_at: null });
  await gotoPositionsTable(page, [pos]);

  const [request] = await Promise.all([
    page.waitForRequest((req) => req.url().includes('/mark-reviewed') && req.method() === 'PATCH'),
    page.locator('[data-testid="mark-reviewed-button"]').click(),
  ]);

  expect(request.url()).toContain(`/positions/${pos.id}/mark-reviewed`);
});

test('SC-RCN-07: Grid View shows Last Reviewed row in card footer', async ({ page }) => {
  // makePosition()'s default entry_date is 30 days ago (>= the 14-day
  // REVIEW_STALE_THRESHOLD_DAYS in PositionCard.js), so with
  // last_reviewed_at null this is correctly the FLAGGED (amber) "Not yet
  // reviewed" state -- confirmed against real Playwright CI. (A prior
  // revision of this test incorrectly asserted the non-flagged slate
  // classes here and failed in real CI; SC-RCN-08 below tests the
  // genuinely non-flagged variant instead.)
  const pos = makePosition({ last_reviewed_at: null });
  await stubPositionsPage(page, [pos]);
  await page.goto('/#/Positions');
  await page.waitForSelector(`text=${pos.ticker}`, { timeout: 8000 });

  const row = page.locator('[data-testid="last-reviewed-row"]');
  await expect(row).toBeVisible({ timeout: 5000 });
  await expect(row).toContainText('Not yet reviewed');
  await expect(row.locator('[data-testid="mark-reviewed-button"]')).toBeVisible();
});

test('SC-RCN-08: Grid View non-flagged "Not yet reviewed" state resolves the canonical secondary-text token (ST-06, EPIC-03, v8.6, BLG-FE-149)', async ({ page }) => {
  // A position with last_reviewed_at null AND a recent entry_date (within
  // the 14-day REVIEW_STALE_THRESHOLD_DAYS) is "Not yet reviewed" but NOT
  // flagged -- PositionCard.js's LastReviewedRow renders this via the same
  // ternary ST-06 fixed (text-amber-* when flagged, else the canonical
  // text-slate-600 dark:text-slate-400 pair, not the pre-fix
  // text-slate-500 shade).
  const recentEntryDate = new Date();
  recentEntryDate.setDate(recentEntryDate.getDate() - 3);
  const pos = makePosition({ last_reviewed_at: null, entry_date: recentEntryDate.toISOString() });
  await stubPositionsPage(page, [pos]);
  await page.goto('/#/Positions');
  await page.waitForSelector(`text=${pos.ticker}`, { timeout: 8000 });

  const row = page.locator('[data-testid="last-reviewed-row"]');
  await expect(row).toBeVisible({ timeout: 5000 });
  await expect(row).toContainText('Not yet reviewed');

  const text = row.locator('span').filter({ hasText: 'Not yet reviewed' });
  await expect(text).not.toHaveClass(/text-amber-600/);
  await expect(text).toHaveClass(/text-slate-600/);
  await expect(text).toHaveClass(/dark:text-slate-400/);
});
