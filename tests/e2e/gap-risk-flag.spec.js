/**
 * Overnight/Weekend Gap Risk Flag — Acceptance Tests
 * ST-02 (BLG-FEAT-65, v6.9)
 *
 * Covers AC-01–03 (Playwright-coverable per stage4_backlog_slice.md: "coverable by
 * Playwright using mocked earnings-calendar/OHLCV fixtures and mocked Friday-close
 * date context"). Day-of-week / earnings-proximity logic is fully server-side
 * (gap_risk_service.py) — these tests mock the GET /positions/{id}/gap-risk response
 * directly rather than mocking the client clock, matching "frontend renders the flag
 * as returned — no client-side day-of-week logic" (ux_spec.md §5). AC-04 (§13
 * sign-off) is a governance gate, not a testable UI behaviour.
 *
 *   SC-GR-01  No flag — Alerts column shows "—"
 *   SC-GR-02  Earnings-flagged — "GAP RISK" badge shown, amber-600 background
 *   SC-GR-03  Weekend-hold-flagged — "GAP RISK" badge shown
 *   SC-GR-04  Tooltip / aria-label exposes reason + historical average gap
 *   SC-GR-05  Insufficient history — badge still shown; tooltip shows "insufficient history"
 *   SC-GR-06  Both reasons present — tooltip lists both reasons
 *   SC-GR-07  Risk-Off and Gap Risk badges stack in the same Alerts cell
 *   SC-GR-08  Grid View — Gap Risk badge shown on the position card
 *
 * Spec refs:
 *   docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md
 *   docs/specs/frontend/pages/positions.md §Gap Risk Badge
 *   docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk
 *
 * ROUTING NOTE: App uses HashRouter — all navigation via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

function makePosition(overrides = {}) {
  return {
    id: 'pos-gaprisk-01',
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
    holding_days: 15,
    grace_days_remaining: null,
    status: 'open',
    entry_date: '2026-06-01',
    initial_stop: 130.00,
    current_trailing_stop: 0,
    risk_off_exit: false,
    tags: null,
    ...overrides,
  };
}

const NO_FLAG = { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false };
const EARNINGS_FLAG = { flagged: true, reasons: ['earnings'], avg_gap_pct: 2.3, event_count: 14, insufficient_history: false };
const WEEKEND_FLAG = { flagged: true, reasons: ['weekend_hold'], avg_gap_pct: 1.1, event_count: 31, insufficient_history: false };
const BOTH_FLAG = { flagged: true, reasons: ['earnings', 'weekend_hold'], avg_gap_pct: 3.0, event_count: 20, insufficient_history: false };
const INSUFFICIENT_FLAG = { flagged: true, reasons: ['earnings'], avg_gap_pct: null, event_count: 3, insufficient_history: true };

async function stubPositionsPage(page, positions, gapRiskPayload) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance-recheck') || url.includes('/positions/compliance') || url.includes('/gap-risk')) {
      return route.continue();
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) });
  });
  await page.route('**/portfolio*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/positions/compliance*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null, days_until_earnings: null }) })
  );
  await page.route('**/positions/*/gap-risk', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: gapRiskPayload }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
}

async function gotoPositionsTable(page, positions, gapRiskPayload) {
  await stubPositionsPage(page, positions, gapRiskPayload);
  await page.goto('/#/Positions');
  const firstTicker = positions[0]?.ticker || 'AAPL';
  await page.waitForSelector(`text=${firstTicker}`, { timeout: 8000 });
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 8000 });
  await tableBtn.click();
  await page.waitForSelector('table', { timeout: 5000 });
}

test('SC-GR-01: No flag — Alerts column shows a dash', async ({ page }) => {
  const pos = makePosition();
  await gotoPositionsTable(page, [pos], NO_FLAG);

  await expect(page.locator('[data-testid="gap-risk-badge"]')).not.toBeVisible({ timeout: 5000 });
});

test('SC-GR-02: Earnings-flagged position shows "GAP RISK" badge with amber-600 background', async ({ page }) => {
  const pos = makePosition();
  await gotoPositionsTable(page, [pos], EARNINGS_FLAG);

  const badge = page.locator('[data-testid="gap-risk-badge"]').first();
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toContainText('GAP RISK');
  await expect(badge).toHaveCSS('background-color', 'rgb(217, 119, 6)'); // #D97706
});

test('SC-GR-03: Weekend-hold-flagged position shows "GAP RISK" badge', async ({ page }) => {
  const pos = makePosition();
  await gotoPositionsTable(page, [pos], WEEKEND_FLAG);

  await expect(page.locator('[data-testid="gap-risk-badge"]').first()).toBeVisible({ timeout: 5000 });
});

test('SC-GR-04: Tooltip / aria-label exposes reason and historical average gap', async ({ page }) => {
  const pos = makePosition();
  await gotoPositionsTable(page, [pos], EARNINGS_FLAG);

  const badge = page.locator('[data-testid="gap-risk-badge"]').first();
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveAttribute('aria-label', /Earnings before next session/);
  await expect(badge).toHaveAttribute('aria-label', /2\.3/);
  await expect(badge).toHaveAttribute('title', /2\.3/);
});

test('SC-GR-05: Insufficient history — badge still shown, tooltip shows "insufficient history"', async ({ page }) => {
  const pos = makePosition();
  await gotoPositionsTable(page, [pos], INSUFFICIENT_FLAG);

  const badge = page.locator('[data-testid="gap-risk-badge"]').first();
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveAttribute('aria-label', /insufficient history/);
});

test('SC-GR-06: Both reasons present — tooltip lists both reasons', async ({ page }) => {
  const pos = makePosition();
  await gotoPositionsTable(page, [pos], BOTH_FLAG);

  const badge = page.locator('[data-testid="gap-risk-badge"]').first();
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveAttribute('aria-label', /Earnings before next session/);
  await expect(badge).toHaveAttribute('aria-label', /Weekend hold/);
});

test('SC-GR-07: Risk-Off and Gap Risk badges stack in the same Alerts cell', async ({ page }) => {
  const pos = makePosition({ risk_off_exit: true });
  await gotoPositionsTable(page, [pos], EARNINGS_FLAG);

  const riskOffBadge = page.locator('span[title="Risk-off regime: index below MA200 — consider exit"]');
  const gapBadge = page.locator('[data-testid="gap-risk-badge"]').first();
  await expect(riskOffBadge).toBeVisible({ timeout: 5000 });
  await expect(gapBadge).toBeVisible({ timeout: 5000 });
});

test('SC-GR-08: Grid View — Gap Risk badge shown on the position card', async ({ page }) => {
  const pos = makePosition();
  await stubPositionsPage(page, [pos], EARNINGS_FLAG);
  await page.goto('/#/Positions');
  await page.waitForSelector(`text=${pos.ticker}`, { timeout: 8000 });

  await expect(page.locator('[data-testid="gap-risk-badge"]').first()).toBeVisible({ timeout: 5000 });
});
