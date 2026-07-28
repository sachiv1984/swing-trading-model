/**
 * "Why Is My Stop Moving" Explainer Tooltip
 * ST-05 (BLG-FEAT-87, EPIC-05, v7.9)
 *
 * Design source: docs/design/2026-07-27__release-v7.9/trailing-stop-explainer-tooltip/ux_spec.md
 * Frontend spec: docs/specs/frontend/pages/positions.md §Trailing Stop Column
 *
 * Coverage (non-visual AC only — colour/spacing itself is DoQ manual/visual review):
 *   SC-TSE-01  Table View — info icon present next to the Stop column header
 *   SC-TSE-02  Table View — hovering the icon reveals the explainer tooltip text
 *   SC-TSE-03  Grid View — info icon present in the Trail Stop tile
 *   SC-TSE-04  Keyboard focus reveals the tooltip (accessibility requirement, ux_spec.md §4)
 *   SC-TSE-05  Icon has the specified aria-label
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Positions'). Grid View
 * is the default; Table View requires clicking [aria-label="Table view"].
 */

'use strict';

const { test, expect } = require('@playwright/test');

function makePosition(overrides = {}) {
  return {
    id: 'pos-tse-01',
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
    entry_date: new Date().toISOString(),
    initial_stop: 130.00,
    current_trailing_stop: 135.00,
    risk_off_exit: false,
    lifecycle_state: 'PROFITABLE',
    position_state: 'PROFITABLE',
    days_in_state: 20,
    tags: null,
    last_reviewed_at: new Date().toISOString(),
    ...overrides,
  };
}

async function stubPositionsPage(page, positions) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance') || url.includes('/grace-period-alerts') || url.includes('/gap-risk')) {
      return route.continue();
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
  await page.route('**/portfolio/drawdown-status', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { threshold_breached: false } }) })
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

async function gotoPositionsTable(page, positions) {
  await stubPositionsPage(page, positions);
  await page.goto('/#/Positions');
  const firstTicker = positions[0]?.ticker || 'AAPL';
  await page.waitForSelector(`text=${firstTicker}`, { timeout: 8000 });
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 8000 });
  await tableBtn.click();
  await page.waitForSelector('table', { timeout: 5000 });
}

test('SC-TSE-01: Table View shows the explainer icon next to the Stop column header', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition()]);

  const icon = page.getByRole('button', { name: /why is my stop moving/i });
  await expect(icon).toBeVisible({ timeout: 8000 });
});

test('SC-TSE-02: Hovering the icon reveals the explainer tooltip text', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition()]);

  const icon = page.getByRole('button', { name: /why is my stop moving/i });
  await icon.hover();

  await expect(page.getByText(/tightens as a position becomes profitable/i)).toBeVisible({ timeout: 5000 });
  await expect(page.getByText(/atr is recalculated daily/i)).toBeVisible();
  await expect(page.getByText(/once tightened, a stop never loosens/i)).toBeVisible();
});

test('SC-TSE-03: Grid View shows the explainer icon in the Trail Stop tile', async ({ page }) => {
  await stubPositionsPage(page, [makePosition()]);
  await page.goto('/#/Positions');
  await page.waitForSelector('text=AAPL', { timeout: 8000 });

  const icon = page.getByRole('button', { name: /why is my stop moving/i });
  await expect(icon).toBeVisible({ timeout: 8000 });
});

test('SC-TSE-04: Keyboard focus reveals the tooltip', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition()]);

  const icon = page.getByRole('button', { name: /why is my stop moving/i });
  await icon.focus();

  await expect(page.getByText(/tightens as a position becomes profitable/i)).toBeVisible({ timeout: 5000 });
});

test('SC-TSE-05: Icon has the specified aria-label', async ({ page }) => {
  await gotoPositionsTable(page, [makePosition()]);

  const icon = page.locator('[aria-label="Why is my stop moving? Explanation of trailing stop behaviour."]');
  await expect(icon).toBeVisible({ timeout: 8000 });
});
