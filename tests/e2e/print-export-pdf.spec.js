/**
 * Print / Export PDF Action — ST-01 (EPIC-01, v7.6, BLG-FE-119)
 *
 * Design source: docs/design/2026-07-20__release-v7.6/print-pdf-export/ux_spec.md
 * Spec refs: docs/specs/frontend/pages/weekly_digest.md#4. Print / Export PDF
 *            docs/specs/frontend/pages/trade_plan.md#7c. Print / Export PDF
 *
 * Covers observable AC:
 *   SC-PRINT-01  WeeklyDigest: Print button present and clickable once data loads
 *   SC-PRINT-02  WeeklyDigest: Print button hidden while loading / on error
 *   SC-PRINT-03  WeeklyDigest: print-media emulation hides nav/sidebar/actions,
 *                keeps table content
 *   SC-PRINT-04  TradePlan: Print button present and clickable in detail view
 *   SC-PRINT-05  TradePlan: Print button absent on the creation form (no editId)
 *   SC-PRINT-06  TradePlan: print-media emulation hides nav/sidebar/actions,
 *                keeps detail-view content
 *
 * Infrastructure: Playwright page.route() network interception. No live backend
 * required. App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const PLAN_ID = '00000000-0000-0000-0000-000000000099';

const DIGEST_SEED = {
  status: 'ok',
  data: {
    realised_pnl_7d: 166.10,
    unrealised_pnl_delta_7d: -42.80,
    alerts_fired_7d: 5,
    alerts_dismissed_7d: 3,
    compliance_score_current: 80.0,
    compliance_score_7d_ago: 75.0,
    staleness_hours: 18.5,
    as_of_utc: '2026-04-01T10:30:00+00:00',
  },
};

const EXISTING_PLAN_DETAIL = {
  status: 'ok',
  data: {
    id: PLAN_ID,
    ticker: 'AAPL',
    market: 'US',
    status: 'draft',
    setup_thesis: 'Breakout above 50d MA on volume',
    entry_rationale: 'Confirmed with signal',
    regime_context_at_entry: 'risk_on',
    r_target: 2.0,
    early_exit_conditions: 'Close below 50d MA',
    confirmation_criteria: 'Volume > 1.5x avg',
    checklist_items: [
      { id: 'signal_confirmed', label: 'Strategy signal confirmed', checked: true },
    ],
  },
};

/** Stub window.print() so it never opens a real dialog; tracks call count. */
async function stubPrint(page) {
  await page.addInitScript(() => {
    window.__printCalls = 0;
    window.print = () => {
      window.__printCalls += 1;
    };
  });
}

async function mockLayoutFallbacks(page) {
  await page.route('**/alerts/history', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/portfolio/positions**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { positions: [] } }) })
  );
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

// ---------------------------------------------------------------------------
// WeeklyDigest
// ---------------------------------------------------------------------------

test.describe('WeeklyDigest — Print / Export PDF', () => {
  test.beforeEach(async ({ page }) => {
    await stubPrint(page);
    await mockLayoutFallbacks(page);
  });

  test('SC-PRINT-01: Print button present and clickable once digest data loads', async ({ page }) => {
    await page.route('**/digest/weekly', (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(DIGEST_SEED) })
    );
    await page.goto('/#/WeeklyDigest');

    const printBtn = page.getByTestId('print-export-pdf-btn');
    await expect(printBtn).toBeVisible({ timeout: 8000 });
    await printBtn.click();
    await expect.poll(() => page.evaluate(() => window.__printCalls)).toBe(1);
  });

  test('SC-PRINT-02: Print button hidden on error state', async ({ page }) => {
    await page.route('**/digest/weekly', (route) =>
      route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error' }) })
    );
    await page.goto('/#/WeeklyDigest');

    await expect(page.getByRole('button', { name: /try again/i })).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('print-export-pdf-btn')).toHaveCount(0);
  });

  test('SC-PRINT-03: print-media emulation hides nav/sidebar/actions, keeps table content', async ({ page }) => {
    await page.route('**/digest/weekly', (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(DIGEST_SEED) })
    );
    await page.goto('/#/WeeklyDigest');
    await expect(page.getByTestId('print-export-pdf-btn')).toBeVisible({ timeout: 8000 });

    // Desktop sidebar visible in screen mode
    await expect(page.locator('aside').first()).toBeVisible();

    await page.emulateMedia({ media: 'print' });

    await expect(page.locator('aside').first()).not.toBeVisible();
    await expect(page.getByTestId('print-export-pdf-btn')).not.toBeVisible();
    // Table content remains
    await expect(page.getByText('Realised P&L (7d)')).toBeVisible();
    await expect(page.locator('td').filter({ hasText: /^£166\.10$/ }).first()).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// TradePlan
// ---------------------------------------------------------------------------

test.describe('TradePlan — Print / Export PDF', () => {
  test.beforeEach(async ({ page }) => {
    await stubPrint(page);
    await mockLayoutFallbacks(page);
    await page.route(`${API}/market/status`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { regime: 'risk_on' } }) })
    );
  });

  test('SC-PRINT-04: Print button present and clickable in detail view', async ({ page }) => {
    await page.route(new RegExp(`${API}/trade-plans/${PLAN_ID}$`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EXISTING_PLAN_DETAIL) })
    );
    const qs = new URLSearchParams({ edit: PLAN_ID, ticker: 'AAPL', market: 'US' }).toString();
    await page.goto(`/#/TradePlan?${qs}`);

    const printBtn = page.getByTestId('print-export-pdf-btn');
    await expect(printBtn).toBeVisible({ timeout: 10000 });
    await printBtn.click();
    await expect.poll(() => page.evaluate(() => window.__printCalls)).toBe(1);
  });

  test('SC-PRINT-05: Print button absent on the creation form', async ({ page }) => {
    await page.goto('/#/TradePlan?ticker=AAPL&market=US');
    await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('print-export-pdf-btn')).toHaveCount(0);
  });

  test('SC-PRINT-06: print-media emulation hides nav/sidebar/actions, keeps detail content', async ({ page }) => {
    await page.route(new RegExp(`${API}/trade-plans/${PLAN_ID}$`), (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EXISTING_PLAN_DETAIL) })
    );
    const qs = new URLSearchParams({ edit: PLAN_ID, ticker: 'AAPL', market: 'US' }).toString();
    await page.goto(`/#/TradePlan?${qs}`);
    await expect(page.getByTestId('print-export-pdf-btn')).toBeVisible({ timeout: 10000 });

    await expect(page.locator('aside').first()).toBeVisible();

    await page.emulateMedia({ media: 'print' });

    await expect(page.locator('aside').first()).not.toBeVisible();
    await expect(page.getByTestId('print-export-pdf-btn')).not.toBeVisible();
    // Detail-view content remains (setup thesis textarea content)
    await expect(page.getByPlaceholder(/describe the setup/i)).toHaveValue('Breakout above 50d MA on volume');
  });
});
