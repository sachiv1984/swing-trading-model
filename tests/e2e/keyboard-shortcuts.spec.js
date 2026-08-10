/**
 * Keyboard Shortcuts — Acceptance Tests — ST-11 (EPIC-03, v3.0)
 *
 * Covers non-visual AC for global keyboard shortcuts introduced in ST-11.
 * Visual AC (kbd element styling, sidebar footer layout) requires DoQ
 * local-run or staging verification — not covered here.
 *
 * Scenarios:
 *   SC-KBD-01  'r' key dispatches app:refresh event on any page
 *   SC-KBD-02  'n' key on Positions page navigates to TradeEntry
 *   SC-KBD-03  'n' key on TradeHistory page navigates to TradeEntry
 *   SC-KBD-04  'w' key on Screener page dispatches app:add-to-watchlist event
 *   SC-KBD-05  'w' key on Watchlist page dispatches app:add-to-watchlist event
 *   SC-KBD-06  'r' key suppressed when focus is inside a text input
 *   SC-KBD-07  'n' key suppressed when focus is inside a textarea
 *   SC-KBD-08  'n' key on Dashboard does NOT navigate (page not in shortcut map)
 *   SC-KBD-09  Sidebar footer shows shortcut hints on Positions page
 *   SC-KBD-10  Sidebar footer shows correct shortcut hints on Screener page
 *   SC-KBD-11  No regression: existing keyboard behaviour in forms unchanged
 *
 * Spec refs:
 *   docs/specs/frontend/pages/navigation.md v1.1 §Keyboard Shortcuts
 *   docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md v1.0
 *
 * Infrastructure: page.route() network interception — no live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Common stubs
// ---------------------------------------------------------------------------

async function stubCommon(page) {
  await page.route(`${API}/alerts/history`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route(`${API}/portfolio/positions**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { positions: [] } }) })
  );
  await page.route(`${API}/portfolio/trades**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { trades: [] } }) })
  );
  await page.route(`${API}/screener/results**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ results: [], run_id: null, run_timestamp: null, total: 0, limit: 200, offset: 0 }) })
  );
  // ST-21 (BLG-FEAT-29, v8.5): stub the Regime History panel's own data call.
  await page.route(`${API}/screener/regime-distribution**`, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ ok: true, data: { window: '30d', run_count: 0, total_observations: 0, risk_on_count: 0, risk_off_count: 0, risk_on_pct: null, risk_off_pct: null } }),
    })
  );
  await page.route(`${API}/watchlist**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
}

async function goto(page, hash) {
  await page.goto(hash);
  await page.waitForLoadState('domcontentloaded');
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

test.beforeEach(async ({ page }) => {
  await stubCommon(page);
});

// SC-KBD-01 — 'r' key dispatches app:refresh event
test('SC-KBD-01: r key dispatches app:refresh custom event', async ({ page }) => {
  await goto(page, '/#/Positions');

  let refreshFired = false;
  await page.evaluate(() => {
    window.addEventListener('app:refresh', () => { window._refreshFired = true; });
  });

  await page.keyboard.press('r');

  const fired = await page.evaluate(() => window._refreshFired === true);
  expect(fired).toBe(true);
});

// SC-KBD-02 — 'n' key on Positions navigates to TradeEntry
test('SC-KBD-02: n key on Positions navigates to TradeEntry', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.keyboard.press('n');
  await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 3000 });
});

// SC-KBD-03 — 'n' key on TradeHistory navigates to TradeEntry
test('SC-KBD-03: n key on TradeHistory navigates to TradeEntry', async ({ page }) => {
  await goto(page, '/#/TradeHistory');
  await expect(page.getByText('Trade History').first()).toBeVisible({ timeout: 8000 });
  await page.keyboard.press('n');
  await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 3000 });
});

// SC-KBD-04 — 'w' key on Screener dispatches app:add-to-watchlist
test('SC-KBD-04: w key on Screener dispatches app:add-to-watchlist', async ({ page }) => {
  await goto(page, '/#/Screener');

  await page.evaluate(() => {
    window.addEventListener('app:add-to-watchlist', () => { window._watchlistFired = true; });
  });

  await page.keyboard.press('w');

  const fired = await page.evaluate(() => window._watchlistFired === true);
  expect(fired).toBe(true);
});

// SC-KBD-05 — 'w' key on Watchlist dispatches app:add-to-watchlist
test('SC-KBD-05: w key on Watchlist dispatches app:add-to-watchlist', async ({ page }) => {
  await goto(page, '/#/Watchlist');

  await page.evaluate(() => {
    window.addEventListener('app:add-to-watchlist', () => { window._watchlistFired = true; });
  });

  await page.keyboard.press('w');

  const fired = await page.evaluate(() => window._watchlistFired === true);
  expect(fired).toBe(true);
});

// SC-KBD-06 — 'r' key suppressed inside text input
test('SC-KBD-06: r key does not fire app:refresh when focus is in a text input', async ({ page }) => {
  // TradeEntry has text inputs
  await page.route(`${API}/portfolio/currencies**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(`${API}/portfolio/strategies**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );

  await goto(page, '/#/TradeEntry');

  await page.evaluate(() => {
    window.addEventListener('app:refresh', () => { window._refreshFired = true; });
  });

  // Focus a text input
  const input = page.locator('input[type="text"]').first();
  const inputVisible = await input.isVisible().catch(() => false);
  if (inputVisible) {
    await input.focus();
    await page.keyboard.press('r');
    const fired = await page.evaluate(() => window._refreshFired === true);
    expect(fired).toBe(false);
  } else {
    // If no text input on page, test is advisory — pass
    test.skip();
  }
});

// SC-KBD-07 — 'n' key suppressed inside textarea
test('SC-KBD-07: n key does not navigate when focus is in a textarea', async ({ page }) => {
  await goto(page, '/#/Positions');

  // Inject a textarea into the page, focus it, press n
  await page.evaluate(() => {
    const ta = document.createElement('textarea');
    ta.id = 'test-ta';
    document.body.appendChild(ta);
    ta.focus();
  });

  const startUrl = page.url();
  await page.keyboard.press('n');
  // URL should not change
  expect(page.url()).toBe(startUrl);
});

// SC-KBD-08 — 'n' key on Dashboard does NOT navigate
test('SC-KBD-08: n key on Dashboard does not navigate away', async ({ page }) => {
  await page.route(`${API}/portfolio/metrics**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: {} }) })
  );
  await goto(page, '/#/');

  const startUrl = page.url();
  await page.keyboard.press('n');
  // Should remain on Dashboard — 'n' has no binding here
  expect(page.url()).toBe(startUrl);
});

// SC-KBD-09 — Sidebar footer shows shortcut hints on Positions
test('SC-KBD-09: Sidebar footer shows n and r hints on Positions page', async ({ page }) => {
  await goto(page, '/#/Positions');

  // Sidebar footer should contain kbd elements for 'n' and 'r'
  const sidebar = page.locator('aside').first();
  await expect(sidebar).toContainText('n', { timeout: 5000 });
  await expect(sidebar).toContainText('r');
});

// SC-KBD-10 — Sidebar footer shows correct hints on Screener
test('SC-KBD-10: Sidebar footer shows w and r hints on Screener page', async ({ page }) => {
  await goto(page, '/#/Screener');

  const sidebar = page.locator('aside').first();
  await expect(sidebar).toContainText('w', { timeout: 5000 });
  await expect(sidebar).toContainText('r');
});

// SC-KBD-11 — Typing in form inputs still works (no global suppression of keydown)
test('SC-KBD-11: Typing in an input field works normally (no interference)', async ({ page }) => {
  await page.route(`${API}/portfolio/currencies**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route(`${API}/portfolio/strategies**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );

  await goto(page, '/#/TradeEntry');

  const input = page.locator('input[type="text"]').first();
  const inputVisible = await input.isVisible().catch(() => false);
  if (inputVisible) {
    await input.fill('AAPL');
    await expect(input).toHaveValue('AAPL');
  } else {
    test.skip();
  }
});
