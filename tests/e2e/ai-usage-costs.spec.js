/**
 * Claude API Usage & Costs (Settings §6) — Acceptance Tests — ST-07 (EPIC-07, v7.6, BLG-FEAT-77)
 *
 * Covers the acceptance criteria from stage4_backlog_slice.md#ST-07, as
 * reframed by ESC-EXEC-20260720-01 (v1.1 addendum to
 * docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md):
 *   - Settings §6 renders the current month's Claude API spend (single figure)
 *   - Loading and error states behave per spec, independent of the rest of the page
 *
 * Spec refs:
 *   docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md v1.1 §7
 *   docs/specs/frontend/pages/settings.md v1.5 §6
 *   docs/specs/api_contracts/ai_endpoints.md v1.7 §GET /ai/monthly-cost
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
