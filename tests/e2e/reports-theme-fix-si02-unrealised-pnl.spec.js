/**
 * SI-02 Gate Status Section + Unrealised P&L Card — Light/Dark Theme Fix
 * (ST-04, BLG-FE-151, EPIC-01, v8.7) / (ST-05, BLG-FE-152, EPIC-01, v8.7)
 *
 * Both sections previously hardcoded dark-only structural classes
 * (bg-slate-800/50, bg-slate-800/30, text-white, text-slate-300 with no
 * light-theme pair). Converted to explicit light+dark pairs — same defect
 * class and fix pattern as BLG-FE-87/88/95, verified the same way as
 * heading-light-theme-contrast.spec.js.
 *
 * Covers observable AC:
 *   SC-TF-01  SI-02 Gate Status heading — dark theme: white (unchanged)
 *   SC-TF-02  SI-02 Gate Status heading — light theme: slate-900 (fixed)
 *   SC-TF-03  SI-02 Gate Status container — dark theme: slate-800/50 (unchanged)
 *   SC-TF-04  SI-02 Gate Status container — light theme: slate-100, not slate-800 (fixed)
 *   SC-TF-05  Unrealised P&L card (Tax Year tab) — dark theme: slate-800/30 container (unchanged)
 *   SC-TF-06  Unrealised P&L card (Tax Year tab) — light theme: white container, not slate-800 (fixed)
 *
 * Infrastructure: Playwright page.route() network interception, reusing the
 * mock helpers established in reports-si02-gate-status.spec.js. Theme toggle
 * via page.addInitScript setting localStorage["theme"], same pattern as
 * heading-light-theme-contrast.spec.js.
 *
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'),
 * then click the "Tax Year P&L" tab (default tab is "Performance").
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const WHITE_RGB = 'rgb(255, 255, 255)';
const SLATE_900_RGB = 'rgb(15, 23, 42)';

const TAX_YEAR_REPORT_WITH_UNREALISED = {
  status: 'ok',
  data: {
    tax_year_label: '2026/27',
    summary: {
      total_realised_pnl: 500,
      total_gross_profit: 800,
      total_gross_loss: -300,
      win_rate: 0.6,
      total_closed_trades: 5,
    },
    trades: [],
    estimated_unrealised_pnl: 250,
    unrealised_note: 'Based on current open positions at last close.',
  },
};

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTaxYearReport(page) {
  await page.route(new RegExp(`${API}/reports/tax-year`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TAX_YEAR_REPORT_WITH_UNREALISED) })
  );
}

async function mockTrades(page, totalTrades) {
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { total_trades: totalTrades, win_rate: 0, total_pnl: 0, trades: [] } }),
    })
  );
}

async function mockTradePlans(page, plans) {
  await page.route(`${API}/trade-plans`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plans }) })
  );
}

async function mockArc5Compliance(page, tradePlanAdherenceRate) {
  await page.route(new RegExp(`${API}/analytics/arc5-compliance`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          period: '7d',
          validation_pass_rate_by_rule: {},
          events_per_week: 0,
          override_rate: null,
          top_rule_breach: null,
          trade_plan_adherence_rate: tradePlanAdherenceRate,
        },
      }),
    })
  );
}

async function gotoTaxYearTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /tax year p&l/i }).click();
  await expect(page.getByTestId('si02-gate-status-section')).toBeVisible({ timeout: 10000 });
}

async function mockAll(page, theme) {
  if (theme === 'light') {
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
  }
  await mockFallback(page);
  await mockTaxYearReport(page);
  await mockTrades(page, 5);
  await mockTradePlans(page, []);
  await mockArc5Compliance(page, 0);
}

test.describe('SI-02 Gate Status theme fix (SC-TF-01..04)', () => {
  test('SC-TF-01/03: dark theme — heading white, container slate-800/50 (unchanged)', async ({ page }) => {
    await mockAll(page, 'dark');
    await gotoTaxYearTab(page);

    const heading = page.getByRole('heading', { name: 'SI-02 Gate Status' });
    await expect(heading).toBeVisible();
    expect(await heading.evaluate((el) => getComputedStyle(el).color)).toBe(WHITE_RGB);

    const container = page.getByTestId('si02-gate-status-section');
    const bg = await container.evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(bg).toMatch(/^rgba\(30, 41, 59/);
  });

  test('SC-TF-02/04: light theme — heading slate-900, container not slate-800 (fixed)', async ({ page }) => {
    await mockAll(page, 'light');
    await gotoTaxYearTab(page);

    const heading = page.getByRole('heading', { name: 'SI-02 Gate Status' });
    await expect(heading).toBeVisible();
    const color = await heading.evaluate((el) => getComputedStyle(el).color);
    expect(color).toBe(SLATE_900_RGB);
    expect(color).not.toBe(WHITE_RGB);

    const container = page.getByTestId('si02-gate-status-section');
    const bg = await container.evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(bg).not.toMatch(/^rgba\(30, 41, 59/);
  });
});

test.describe('Unrealised P&L card theme fix (SC-TF-05/06)', () => {
  test('SC-TF-05: dark theme — card container slate-800/30 (unchanged)', async ({ page }) => {
    await mockAll(page, 'dark');
    await gotoTaxYearTab(page);

    const heading = page.getByText('Indicative Unrealised P&L (current positions)');
    await expect(heading).toBeVisible();
    const card = page.locator('div', { has: heading }).last();
    const bg = await card.evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(bg).toMatch(/^rgba\(30, 41, 59/);
  });

  test('SC-TF-06: light theme — card container white, not slate-800 (fixed)', async ({ page }) => {
    await mockAll(page, 'light');
    await gotoTaxYearTab(page);

    const heading = page.getByText('Indicative Unrealised P&L (current positions)');
    await expect(heading).toBeVisible();
    const card = page.locator('div', { has: heading }).last();
    const bg = await card.evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(bg).toBe(WHITE_RGB);
    expect(bg).not.toMatch(/^rgba\(30, 41, 59/);
  });
});
