/**
 * Risk Dashboard Grace Period panel → Positions deep link
 * ST-22 (BLG-FE-207, EPIC-03, v9.12)
 *
 * Design source: docs/design/2026-10-12__release-v9.12/grace-panel-position-link/decision_record.md
 * Specs: docs/specs/frontend/pages/risk_dashboard.md §5.2; docs/specs/frontend/pages/positions.md §Position Deep Link
 *
 * Coverage:
 *   SC-GPL-01  Clicking a grace row opens Positions with that position visible and highlighted
 *              (data-highlighted="true", ring), the ?position= parameter stripped (AC 1)
 *   SC-GPL-02  The highlight is removed after 2000 ms
 *   SC-GPL-03  Table view: the matching row is highlighted
 *   SC-GPL-04  An id not in the open list is ignored and the parameter stripped
 *   SC-GPL-05  Heading, badge, entry date format and row link attributes match §5.2 (AC 2)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const { TD_07 } = require('./mocks/portfolio-mock-data');

const API = 'http://localhost:8000';

function makePosition(overrides = {}) {
  return {
    id: 'p-x', ticker: 'XXXX', market: 'UK', status: 'open',
    entry_price: 50, current_price: 48, current_price_native: 48,
    current_trailing_stop: 45, current_trailing_stop_native: 45,
    stop_price: 45, stop_price_native: 45, shares: 100, fx_rate: 1, live_fx_rate: 1,
    holding_days: 6, grace_period: true, grace_days_remaining: 4,
    risk_off_exit: false, entry_date: '2026-02-28', pnl: -200, pnl_percent: -4,
    position_state: 'GRACE', days_in_state: 6,
    ...overrides,
  };
}

// The Positions list: the three grace positions from TD_07 plus filler rows, so the target needs a scroll.
const POSITIONS = [
  ...Array.from({ length: 9 }, (_, i) => makePosition({ id: `p-fill-${i}`, ticker: `FIL${i}`, grace_period: false, position_state: 'PROFITABLE' })),
  makePosition({ id: 'p-foxt', ticker: 'FOXT', grace_days_remaining: 1, holding_days: 9 }),
  makePosition({ id: 'p-golf', ticker: 'GOLF' }),
];

async function stub(page) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { spy: { price: 500, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7600, is_risk_on: true }, fx_rate: 1.27 } }) })
  );
  await page.route(`${API}/positions**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(POSITIONS) })
  );
  await page.route(`${API}/portfolio`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TD_07) })
  );
}

async function gotoRiskDashboard(page) {
  await page.goto('/#/RiskDashboard');
  await expect(page.locator('[data-testid="grace-period-row"]').first()).toBeVisible({ timeout: 15000 });
}

test('SC-GPL-01: clicking a grace row opens Positions with that position highlighted', async ({ page }) => {
  await stub(page);
  await gotoRiskDashboard(page);

  await page.getByRole('link', { name: 'Open FOXT on Positions' }).click();

  const card = page.locator('[data-position-id="p-foxt"]');
  await expect(card).toBeVisible({ timeout: 10000 });
  await expect(card).toHaveAttribute('data-highlighted', 'true');
  await expect(card).toHaveClass(/ring-cyan-500/);
  await expect(card).toBeInViewport();
  await expect(page).toHaveURL(/#\/Positions$/); // ?position= stripped
  // Only the target is highlighted.
  await expect(page.locator('[data-highlighted="true"]')).toHaveCount(1);
});

test('SC-GPL-02: the highlight is removed after 2000 ms', async ({ page }) => {
  await stub(page);
  await page.clock.install();
  await page.goto('/#/Positions');
  const card = page.locator('[data-position-id="p-golf"]');
  await expect(card).toBeVisible({ timeout: 10000 });
  // Pause the clock once loaded, then follow the deep link client-side, so the
  // 2000 ms hold only advances through runFor().
  await page.clock.pauseAt(Date.now() + 1000);
  await page.evaluate(() => { window.location.hash = '#/Positions?position=p-golf'; });
  await expect(card).toHaveAttribute('data-highlighted', 'true', { timeout: 10000 });

  await page.clock.runFor(1900);
  await expect(card).toHaveAttribute('data-highlighted', 'true');
  await page.clock.runFor(200);
  await expect(card).not.toHaveAttribute('data-highlighted', 'true');
  await expect(card).not.toHaveClass(/ring-cyan-500/);
});

test('SC-GPL-03: in Table view the matching row is highlighted', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Positions');
  await page.getByRole('button', { name: 'Table view' }).click();
  await expect(page.locator('tr[data-position-id="p-foxt"]')).toBeVisible({ timeout: 10000 });

  await page.goto('/#/Positions?position=p-foxt');
  const row = page.locator('tr[data-position-id="p-foxt"]');
  await expect(row).toHaveAttribute('data-highlighted', 'true');
  await expect(row).toHaveClass(/ring-cyan-500/);
});

test('SC-GPL-04: an unknown id is ignored and the parameter stripped', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Positions?position=does-not-exist');
  await expect(page.locator('[data-position-id="p-foxt"]')).toBeVisible({ timeout: 10000 });
  await expect(page).toHaveURL(/#\/Positions$/);
  await expect(page.locator('[data-highlighted="true"]')).toHaveCount(0);
});

test('SC-GPL-05: heading, badge, date format and row link match risk_dashboard.md §5.2', async ({ page }) => {
  await stub(page);
  await gotoRiskDashboard(page);

  await expect(page.getByRole('heading', { name: 'Grace Period Positions', exact: true })).toBeVisible();
  await expect(page.getByText('3 positions in grace period', { exact: true })).toBeVisible();
  const foxt = page.getByRole('link', { name: 'Open FOXT on Positions' });
  await expect(foxt).toContainText('28 Feb 2026');
  await expect(foxt).toHaveAttribute('href', /#\/Positions\?position=p-foxt$/);
  await expect(foxt.locator('svg.lucide-chevron-right')).toHaveAttribute('aria-hidden', 'true');
});
