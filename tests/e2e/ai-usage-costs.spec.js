/**
 * Claude API Usage & Costs (Settings §6) — Acceptance Tests — ST-07 (EPIC-07, v7.6, BLG-FEAT-77)
 * + AI Spend Trend Chart (Settings §6a) — ST-06 (EPIC-06, v7.8, BLG-FEAT-82)
 *
 * Covers the acceptance criteria from stage4_backlog_slice.md#ST-07, as
 * reframed by ESC-EXEC-20260720-01 (v1.1 addendum to
 * docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md):
 *   - Settings §6 renders the current month's Claude API spend (single figure)
 *   - Loading and error states behave per spec, independent of the rest of the page
 *
 * SC-AIC-06..09 cover §6a's spend trend chart (v7.8, ST-06, BLG-FEAT-82):
 * renders below the current-month figure; loading/error states are
 * independent of the current-month figure's own query; renders whatever
 * history exists (no zero-padding).
 *
 * Spec refs:
 *   docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md v1.1 §7
 *   docs/design/2026-07-24__release-v7.8/ai-spend-trend-chart/ux_spec.md
 *   docs/specs/frontend/pages/settings.md §6/§6a
 *   docs/specs/api_contracts/ai_endpoints.md §GET /ai/monthly-cost, §GET /ai/spend-trend
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');
const { apiOk } = require('./fixtures/api-mocks');

const API = 'http://localhost:8000';

const MOCK_SETTINGS = {
  id: 'settings-1',
  min_hold_days: 5,
  atr_multiplier_initial: 2,
  atr_multiplier_trailing: 3,
  atr_period: 14,
  default_risk_percent: 1.0,
  default_currency: 'GBP',
  theme: 'dark',
  uk_commission: 9.95,
  us_commission: 0,
  stamp_duty_rate: 0.005,
  fx_fee_rate: 0.0015,
  min_trades_for_analytics: 10,
  concentration_position_threshold_pct: 15,
  concentration_sector_threshold_pct: 30,
};

async function mockCommonFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockSettings(page) {
  await page.route(`${API}/settings`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk([MOCK_SETTINGS])) });
    } else {
      route.continue();
    }
  });
}

async function gotoSettings(page) {
  await page.goto('/#/Settings');
  await page.waitForLoadState('domcontentloaded');
}

// ---------------------------------------------------------------------------
// SC-AIC-01 — Loaded state
// ---------------------------------------------------------------------------

test('SC-AIC-01: renders "Claude API Usage & Costs" with the current month total', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk({ total_cost_usd: 7.42, request_count: 12 })) })
  );

  await gotoSettings(page);

  await expect(page.getByText('Claude API Usage & Costs')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Claude API spend for the current calendar month')).toBeVisible();
  await expect(page.getByText('$7.42')).toBeVisible({ timeout: 5000 });
});

test('SC-AIC-02: no "Gemini" row and no "Combined Total" row are rendered', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk({ total_cost_usd: 7.42, request_count: 12 })) })
  );

  await gotoSettings(page);
  await expect(page.getByText('Claude API Usage & Costs')).toBeVisible({ timeout: 5000 });

  await expect(page.getByText(/gemini/i)).toHaveCount(0);
  await expect(page.getByText(/combined total/i)).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-AIC-03 — Zero-spend month
// ---------------------------------------------------------------------------

test('SC-AIC-03: zero-spend month renders "$0.00", not a blank or dash', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk({ total_cost_usd: 0.0, request_count: 0 })) })
  );

  await gotoSettings(page);
  await expect(page.getByText('$0.00')).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-AIC-04 — Error state
// ---------------------------------------------------------------------------

test('SC-AIC-04: fetch failure shows "AI cost data unavailable", not a numeric fallback', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'Internal failure' }) })
  );

  await gotoSettings(page);

  await expect(page.getByText('AI cost data unavailable')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('$0.00')).toHaveCount(0);
});

test('SC-AIC-05: monthly-cost failure does not block the rest of the Settings page', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'Internal failure' }) })
  );

  await gotoSettings(page);

  await expect(page.getByText('AI cost data unavailable')).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('heading', { name: 'Strategy Parameters' })).toBeVisible();
  await expect(page.getByRole('button', { name: /save settings/i })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-AIC-06..09 — AI Spend Trend Chart (§6a, ST-06, EPIC-06, v7.8, BLG-FEAT-82)
// ---------------------------------------------------------------------------

const SPEND_TREND_DATA = [
  { version: 'v7.3', spend_usd: 4.12 },
  { version: 'v7.4', spend_usd: 2.87 },
  { version: 'v7.5', spend_usd: 5.03 },
  { version: 'v7.6', spend_usd: 3.91 },
  { version: 'v7.7', spend_usd: 6.20 },
  { version: 'v7.8', spend_usd: 1.45 },
];

test('SC-AIC-06: spend trend chart renders below the current-month figure', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk({ total_cost_usd: 7.42, request_count: 12 })) })
  );
  await page.route(`${API}/ai/spend-trend`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk(SPEND_TREND_DATA)) })
  );

  await gotoSettings(page);

  await expect(page.getByText('$7.42')).toBeVisible({ timeout: 5000 });
  const chart = page.locator('[data-testid="ai-spend-trend-chart"]');
  await expect(chart).toBeVisible({ timeout: 5000 });
  await expect(chart.getByText('Spend by release cycle')).toBeVisible();
});

test('SC-AIC-07: spend trend loading state shows an independent skeleton', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk({ total_cost_usd: 7.42, request_count: 12 })) })
  );
  await page.route(`${API}/ai/spend-trend`, async (route) => {
    await new Promise((r) => setTimeout(r, 800));
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk(SPEND_TREND_DATA)) });
  });

  await gotoSettings(page);

  // Current-month figure resolves independently of the (slower) trend fetch.
  await expect(page.getByText('$7.42')).toBeVisible({ timeout: 5000 });
  await expect(page.locator('[data-testid="ai-spend-trend-loading"]')).toBeVisible({ timeout: 2000 });
  await expect(page.locator('[data-testid="ai-spend-trend-chart"]')).toBeVisible({ timeout: 5000 });
});

test('SC-AIC-08: spend trend failure shows "AI spend trend unavailable", independent of the current-month figure', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk({ total_cost_usd: 7.42, request_count: 12 })) })
  );
  await page.route(`${API}/ai/spend-trend`, (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'Internal failure' }) })
  );

  await gotoSettings(page);

  await expect(page.getByText('$7.42')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('AI spend trend unavailable')).toBeVisible({ timeout: 5000 });
  await expect(page.locator('[data-testid="ai-spend-trend-chart"]')).toHaveCount(0);
});

test('SC-AIC-09: fewer than 6 cycles of history renders whatever exists, no crash', async ({ page }) => {
  await mockCommonFallback(page);
  await mockSettings(page);
  await page.route(`${API}/ai/monthly-cost`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk({ total_cost_usd: 7.42, request_count: 12 })) })
  );
  await page.route(`${API}/ai/spend-trend`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(apiOk([{ version: 'v7.8', spend_usd: 1.45 }])) })
  );

  await gotoSettings(page);

  await expect(page.getByText('$7.42')).toBeVisible({ timeout: 5000 });
  const chart = page.locator('[data-testid="ai-spend-trend-chart"]');
  await expect(chart).toBeVisible({ timeout: 5000 });
});
