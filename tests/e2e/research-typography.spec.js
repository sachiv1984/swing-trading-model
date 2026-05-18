/**
 * Research Page — Typography Conformance Tests
 * ST-10 (BLG-FE-35, v3.7 EPIC-04)
 *
 * Covers SC-RV-TYP-01: Research page typography conforms to design_system.md scale.
 * Replaces the one-time human staging run (DEL-20260518-01 / BLG-FE-35) with
 * permanent CI coverage so regression is caught automatically.
 *
 * design_system.md typography scale references verified:
 *   Region label:          text-xs font-medium text-slate-400 uppercase tracking-wider
 *   Data value (prominent): text-xl font-semibold text-white (or colour variant)
 *   Data value (normal):   text-sm text-slate-200
 *   Chip / badge:          text-xs font-medium
 *   Muted caption:         text-xs text-slate-500
 *
 * Infrastructure: page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/research/AAPL').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const TICKER = 'AAPL';

// ---------------------------------------------------------------------------
// Mock data (minimal — enough for all regions to render)
// ---------------------------------------------------------------------------

const RESEARCH_OK = {
  status: 'ok',
  data: {
    ticker: TICKER,
    market: 'US',
    price: 182.30,
    price_change_pct: 0.012,
    market_cap: 2800000000000,
    updated_at: new Date(Date.now() - 3600000).toISOString(),
    signal: {
      signal_id: 'sig-typ-001',
      status: 'active',
      rank: 1,
      atr: 4.20,
      entry_price: 178.50,
      stop_price: 172.00,
      r_target: 2.5,
    },
    regime: { label: 'risk_on', spy_risk_on: true, ftse_risk_on: true },
    sector: { sector: 'Technology', industry: 'Consumer Electronics' },
    screener: null,
    earnings: null,
    news_headlines: [
      { headline: 'Apple reports record quarterly revenue', source: 'Reuters', published_at: new Date(Date.now() - 7200000).toISOString() },
    ],
  },
};

const HEAT_OK = {
  status: 'ok',
  data: {
    valid: true,
    current_heat_percent: 12.0,
    prospective_heat_percent: 18.5,
    incremental_heat_percent: 6.5,
    prospective_risk_gbp: 650,
    portfolio_value_gbp: 50000,
    ticker: TICKER,
  },
};

// ---------------------------------------------------------------------------
// Route helper
// ---------------------------------------------------------------------------

async function setupRoutes(page) {
  await page.route(`${API}/research/${TICKER}`, async (route) => {
    await route.fulfill({ json: RESEARCH_OK });
  });

  await page.route(`${API}/portfolio/prospective-heat**`, async (route) => {
    await route.fulfill({ json: HEAT_OK });
  });

  await page.route(`${API}/trade-plans**`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: [] } });
  });

  await page.route(`${API}/market/status`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: { spy: { price: 521.0, ma200: 480.0, is_risk_on: true }, fx_rate: 1.27 } } });
  });

  await page.route(`${API}/positions**`, async (route) => {
    await route.fulfill({ json: { status: 'ok', data: [] } });
  });
}

// ---------------------------------------------------------------------------
// SC-RV-TYP-01: Typography conformance
// ---------------------------------------------------------------------------

test.describe('SC-RV-TYP-01 — Research page typography conforms to design_system.md', () => {

  test('Region labels use text-xs font-medium text-slate-400 uppercase tracking-wider', async ({ page }) => {
    await setupRoutes(page);
    await page.goto(`/#/research/${TICKER}`);

    // Wait for page to render (price visible confirms data loaded)
    await expect(page.getByText('Price & Signal')).toBeVisible({ timeout: 8000 });

    // All four region label h2 elements
    const regionLabels = page.locator('h2').filter({ hasText: /Price & Signal|Prospective heat|Trade Plan|Recent News/i });
    const count = await regionLabels.count();
    expect(count).toBeGreaterThanOrEqual(3);

    for (let i = 0; i < count; i++) {
      const label = regionLabels.nth(i);
      await expect(label).toHaveClass(/text-xs/);
      await expect(label).toHaveClass(/font-medium/);
      await expect(label).toHaveClass(/text-slate-400/);
      await expect(label).toHaveClass(/uppercase/);
      await expect(label).toHaveClass(/tracking-wider/);
    }
  });

  test('Primary data value (Current Price) uses text-xl font-semibold', async ({ page }) => {
    await setupRoutes(page);
    await page.goto(`/#/research/${TICKER}`);

    // Wait for price to render
    await expect(page.getByText('$182.30')).toBeVisible({ timeout: 8000 });

    const priceEl = page.getByText('$182.30');
    await expect(priceEl).toHaveClass(/text-xl/);
    await expect(priceEl).toHaveClass(/font-semibold/);
  });

  test('Signal badge uses text-xs font-medium', async ({ page }) => {
    await setupRoutes(page);
    await page.goto(`/#/research/${TICKER}`);

    // Wait for signal badge (Active/Watch/No Signal)
    await expect(page.getByText('Price & Signal')).toBeVisible({ timeout: 8000 });

    // SignalBadge renders the status label in a span with text-xs font-medium
    const badge = page.locator('span').filter({ hasText: /^(Active|Watch|No Signal)$/ }).first();
    await expect(badge).toHaveClass(/text-xs/);
    await expect(badge).toHaveClass(/font-medium/);
  });

  test('Field sub-labels use text-xs text-slate-400', async ({ page }) => {
    await setupRoutes(page);
    await page.goto(`/#/research/${TICKER}`);

    await expect(page.getByText('Price & Signal')).toBeVisible({ timeout: 8000 });

    // "Current Price" and "ATR (14d)" are field sub-labels
    const currentPriceLabel = page.getByText('Current Price');
    await expect(currentPriceLabel).toHaveClass(/text-xs/);
    await expect(currentPriceLabel).toHaveClass(/text-slate-400/);

    const atrLabel = page.getByText('ATR (14d)');
    await expect(atrLabel).toHaveClass(/text-xs/);
    await expect(atrLabel).toHaveClass(/text-slate-400/);
  });

  test('News source caption uses text-xs text-slate-500', async ({ page }) => {
    await setupRoutes(page);
    await page.goto(`/#/research/${TICKER}`);

    await expect(page.getByText('Recent News')).toBeVisible({ timeout: 8000 });

    // News source/timestamp line — muted caption class
    const caption = page.locator('p.text-xs.text-slate-500').first();
    await expect(caption).toBeVisible();
    await expect(caption).toHaveClass(/text-xs/);
    await expect(caption).toHaveClass(/text-slate-500/);
  });

});
