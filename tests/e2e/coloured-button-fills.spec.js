/**
 * E2E: Coloured Button fills render as authored — ST-25 (EPIC-04, v9.13, BLG-FE-221)
 *
 * cn() now merges classes with tailwind-merge, so a <Button>'s colour
 * className replaces the default variant's bg-primary instead of racing it in
 * CSS order. Each listed site renders its authored fill in both themes, and a
 * scoped axe color-contrast check passes on it.
 *
 * Scenarios (each runs in dark and light theme):
 *   SC-CBF-01  Screener "Add to Watchlist" confirm — emerald-700
 *   SC-CBF-02  Screener empty-state "Run Screener" — emerald-700
 *   SC-CBF-03  Trade Plans delete confirm — rose-600
 *   SC-CBF-04  Trade Plan "Abandon Plan" submit — amber-700
 *
 * Design source: docs/design/2026-10-16__release-v9.13/coloured-button-fills/decision_record.md §5
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation via page.goto('/#/<Page>')
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const EMERALD_700 = 'rgb(4, 120, 87)';
const ROSE_600 = 'rgb(225, 29, 72)';
const AMBER_700 = 'rgb(180, 83, 9)';

const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

async function stubCommon(page) {
  // Catch-all registered FIRST (LIFO — specific mocks registered after take precedence)
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/alerts/history`, (r) => r.fulfill(json({ data: { evaluations: [] } })));
  await page.route(`${API}/portfolio/**`, (r) => r.fulfill(json({ ok: true, data: {} })));
  await page.route(`${API}/notifications**`, (r) => r.fulfill(json({ data: [] })));
}

async function expectFillAndContrast(button, colour) {
  await expect(button).toBeVisible({ timeout: 8000 });
  await expect(button).toHaveCSS('background-color', colour);
  await expect(button).toHaveCSS('color', 'rgb(255, 255, 255)');
  const page = button.page();
  // Wait out finite animations (dialog open, colour transitions) so axe reads settled colours.
  await page.waitForFunction(() => document.getAnimations()
    .every((a) => a.playState !== 'running' || a.effect?.getTiming().iterations === Infinity));
  await page.waitForTimeout(200);
  await button.evaluate((el) => el.setAttribute('data-cbf-target', ''));
  const results = await new AxeBuilder({ page }).include('[data-cbf-target]').withRules(['color-contrast']).analyze();
  expect(results.violations).toEqual([]);
}

const SCREENER_ROW = {
  ticker: 'AAPL', market: 'US', price: 175.5, currency: 'USD', atr: 3.2, atr_pct: 1.83,
  regime_status: 'risk_on', signal_score: 0.82, sector: 'Technology',
  proximity_to_entry_zone: 'near_entry', news_headline_count: 0,
};
const PLANS = [
  { id: 'plan-1', ticker: 'AAPL', market: 'US', status: 'draft', r_target: 2.5, setup_thesis: 'Breakout above resistance', updated_at: new Date().toISOString() },
];

for (const theme of ['dark', 'light']) {
  test.describe(`Coloured Button fills (ST-25) — ${theme} theme`, () => {
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await stubCommon(page);
    });

    test(`SC-CBF-01 (${theme}): Screener "Add to Watchlist" renders emerald-700`, async ({ page }) => {
      await page.route(`${API}/screener/results**`, (r) =>
        r.fulfill(json({ results: [SCREENER_ROW], run_id: 'r1', run_timestamp: new Date().toISOString(), total: 1, limit: 200, offset: 0 })));
      await page.route(`${API}/watchlist`, (r) => r.fulfill(json({ items: [] })));
      await page.goto('/#/Screener');
      await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
      await page.getByRole('button', { name: /add.*watchlist|watchlist/i }).first().click();
      await expectFillAndContrast(page.getByRole('button', { name: 'Add to Watchlist', exact: true }).last(), EMERALD_700);
    });

    test(`SC-CBF-02 (${theme}): Screener empty-state "Run Screener" renders emerald-700`, async ({ page }) => {
      await page.route(`${API}/screener/results**`, (r) =>
        r.fulfill(json({ results: [], run_id: null, run_timestamp: null, total: 0, limit: 200, offset: 0 })));
      await page.goto('/#/Screener');
      await expectFillAndContrast(page.getByRole('button', { name: 'Run Screener', exact: true }).last(), EMERALD_700);
    });

    test(`SC-CBF-03 (${theme}): Trade Plans delete confirm renders rose-600`, async ({ page }) => {
      await page.route(`${API}/trade-plans`, (r) => r.fulfill(json({ data: PLANS })));
      await page.goto('/#/TradePlans');
      const row = page.locator('tr').filter({ hasText: 'AAPL' });
      await expect(row).toBeVisible({ timeout: 8000 });
      await row.getByRole('button').last().click();
      await expectFillAndContrast(page.getByRole('button', { name: 'Delete', exact: true }), ROSE_600);
    });

    test(`SC-CBF-04 (${theme}): Trade Plan "Abandon Plan" renders amber-700`, async ({ page }) => {
      await page.route(`${API}/trade-plans/plan-1`, (r) => r.fulfill(json({ data: PLANS[0] })));
      await page.route(`${API}/trade-plans/by-position/**`, (r) => r.fulfill(json({ data: [] })));
      await page.goto('/#/TradePlan?edit=plan-1&ticker=AAPL&market=US');
      await page.getByRole('button', { name: /abandon plan/i }).click();
      await page.getByPlaceholder(/min 10 characters/i).fill('Setup invalidated by market conditions shift');
      await expectFillAndContrast(page.getByRole('button', { name: /^abandon plan$/i }).last(), AMBER_700);
    });
  });
}
