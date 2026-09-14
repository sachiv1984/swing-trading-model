/**
 * Settings heading-order and TradePlan/Settings aria-labelledby pinned
 * regression tests — ST-08 (EPIC-02, v9.4, BLG-QA-164).
 *
 * Pins two accessibility fixes shipped at v9.1/v9.2 so a future refactor
 * cannot silently reintroduce either regression:
 *
 *   1. Settings heading order (BLG-FE-170, ST-02 EPIC-02 v9.2): each
 *      SectionCard heading on the Settings page must render as <h2>, not
 *      <h3> — the page's PageHeader renders the sole <h1>; a SectionCard
 *      <h3> skips a level and re-triggers the axe-core heading-order
 *      finding this story fixed.
 *   2. aria-labelledby association on 5 controls (BLG-FE-171/BLG-FE-166,
 *      ST-03 EPIC-02 v9.2 + ST-02 EPIC-01 v9.1): 2 Settings <Select>
 *      triggers (Default Currency, Theme) and 3 TradePlan native <select>
 *      elements (Market, Status, Setup Type) must each carry an
 *      aria-labelledby attribute whose value resolves to an element that
 *      actually exists in the DOM.
 *
 * Spec refs: src/pages/Settings.js (SectionCard, ST-02/ST-03 EPIC-02 v9.2
 * comments), src/pages/TradePlan.js (Field labelId prop, ST-02 EPIC-01 v9.1)
 *
 * Infrastructure: Playwright page.route() network interception. No live
 * backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function gotoSettings(page) {
  await mockFallback(page);
  await page.goto('/#/Settings');
  await expect(page.getByRole('heading', { name: 'Settings', level: 1 })).toBeVisible({ timeout: 10000 });
}

async function gotoTradePlan(page) {
  await mockFallback(page);
  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// Settings heading order (BLG-FE-170)
// ---------------------------------------------------------------------------

test.describe('SC-SET-HDR-01 — Settings heading order regression', () => {
  test('SC-SET-HDR-01a: page has exactly one <h1> ("Settings")', async ({ page }) => {
    await gotoSettings(page);

    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('h1')).toHaveText('Settings');
  });

  test('SC-SET-HDR-01b: every SectionCard heading renders as <h2>, not <h3> (no h1->h3 skip)', async ({ page }) => {
    await gotoSettings(page);

    // SectionCard renders one heading per settings section (Strategy
    // Parameters, Currency & Fees, Appearance, Risk Concentration, etc.) —
    // there must be at least one, and every one of them must be an <h2>.
    const h2s = page.locator('h2');
    await expect(h2s.first()).toBeVisible({ timeout: 5000 });
    const h2Count = await h2s.count();
    expect(h2Count).toBeGreaterThan(0);

    // The regression this pins: SectionCard's heading regressing from h2
    // back to h3 would skip a level under the page's single h1 — assert
    // zero h3 elements exist on the page (Settings has no legitimate h3
    // usage today).
    await expect(page.locator('h3')).toHaveCount(0);
  });
});

// ---------------------------------------------------------------------------
// aria-labelledby association — Settings selects (BLG-FE-171)
// ---------------------------------------------------------------------------

test.describe('SC-SET-ARIA-01 — Settings Select aria-labelledby regression', () => {
  test('SC-SET-ARIA-01: Default Currency and Theme triggers reference an existing label element', async ({ page }) => {
    await gotoSettings(page);

    for (const labelId of ['settings-default-currency-label', 'settings-theme-label']) {
      const trigger = page.locator(`[aria-labelledby="${labelId}"]`);
      await expect(trigger).toBeVisible({ timeout: 5000 });
      // The referenced id must resolve to a real element — a broken
      // aria-labelledby (label removed but attribute left dangling) is as
      // much a regression as the attribute being removed outright.
      await expect(page.locator(`#${labelId}`)).toHaveCount(1);
    }
  });
});

// ---------------------------------------------------------------------------
// aria-labelledby association — TradePlan selects (BLG-FE-166)
// ---------------------------------------------------------------------------

test.describe('SC-TP-ARIA-01 — TradePlan select aria-labelledby regression', () => {
  test('SC-TP-ARIA-01: Market, Status, and Setup Type selects reference an existing label element', async ({ page }) => {
    await gotoTradePlan(page);

    for (const labelId of ['trade-plan-market-label', 'trade-plan-status-label', 'trade-plan-setup-type-label']) {
      const control = page.locator(`[aria-labelledby="${labelId}"]`);
      await expect(control).toBeVisible({ timeout: 5000 });
      await expect(page.locator(`#${labelId}`)).toHaveCount(1);
    }
  });
});
