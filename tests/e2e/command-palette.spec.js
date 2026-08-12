/**
 * Global Command Palette — Acceptance Tests — ST-01 (EPIC-01, v7.5, BLG-FE-115)
 *
 * Covers the 3 acceptance criteria from stage4_backlog_slice.md#ST-01:
 *   AC-1  Cmd/Ctrl-K opens the palette from any page in the app
 *   AC-2  Typing a ticker surfaces matches across Watchlist/Positions/TradePlans
 *         and navigates to the selected result
 *   AC-3  Typing a page name navigates to that page
 *
 * Spec refs:
 *   docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md
 *   docs/specs/frontend/pages/navigation.md v1.3 §Global Command Palette
 *   docs/specs/blg_fe_115_pre_implementation_readiness_pass.md
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const MOCK_POSITIONS = [
  { id: 'pos-1', ticker: 'AAPL', shares: 10, entry_price: 150 },
];
const MOCK_WATCHLIST = [
  { id: 'wl-1', ticker: 'MSFT', signal_status: 'active' },
];
const MOCK_TRADE_PLANS = [
  { id: 'plan-1', ticker: 'TSLA', market: 'US', status: 'draft' },
];

/** Catch-all fallback registered first — specific routes registered after
 *  it take precedence (Playwright matches most-recently-registered first). */
async function stubCommon(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/alerts/history`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_POSITIONS) })
  );
  await page.route(`${API}/watchlist`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: MOCK_WATCHLIST }) })
  );
  await page.route(`${API}/trade-plans`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: MOCK_TRADE_PLANS }) })
  );
}

async function goto(page, hash) {
  await page.goto(hash);
  await page.waitForLoadState('domcontentloaded');
}

test.beforeEach(async ({ page }) => {
  await stubCommon(page);
});

// AC-1 — Cmd/Ctrl-K opens the palette from any page
test('SC-CP-01: Ctrl+K opens the palette from Positions page', async ({ page }) => {
  await goto(page, '/#/Positions');
  await expect(page.getByTestId('command-palette-input')).not.toBeVisible();
  await page.keyboard.press('Control+k');
  await expect(page.getByTestId('command-palette-input')).toBeVisible();
});

test('SC-CP-02: Ctrl+K opens the palette from a different page (Settings)', async ({ page }) => {
  await goto(page, '/#/Settings');
  await page.keyboard.press('Control+k');
  await expect(page.getByTestId('command-palette-input')).toBeVisible();
});

test('SC-CP-03: mouse fallback (desktop nav search affordance) opens the palette', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.getByTestId('command-palette-trigger-desktop').click();
  await expect(page.getByTestId('command-palette-input')).toBeVisible();
});

test('SC-CP-04: Escape closes the palette without navigating', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.keyboard.press('Control+k');
  await expect(page.getByTestId('command-palette-input')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.getByTestId('command-palette-input')).not.toBeVisible();
  await expect(page).toHaveURL(/#\/Positions/);
});

test('SC-CP-05: Ctrl+K is suppressed while focus is inside a text input', async ({ page }) => {
  await goto(page, '/#/Positions');
  // Force focus into a text input, then confirm the shortcut doesn't fire.
  await page.evaluate(() => {
    const input = document.createElement('input');
    input.type = 'text';
    input.id = 'test-focus-target';
    document.body.appendChild(input);
    input.focus();
  });
  await page.keyboard.press('Control+k');
  await expect(page.getByTestId('command-palette-input')).not.toBeVisible();
});

// AC-3 — Typing a page name navigates to that page
test('SC-CP-06: typing a page name and selecting it navigates to that page', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.keyboard.press('Control+k');
  await page.getByTestId('command-palette-input').fill('Screener');
  await page.getByTestId('command-palette-page-Screener').click();
  await expect(page).toHaveURL(/#\/Screener/);
  await expect(page.getByTestId('command-palette-input')).not.toBeVisible();
});

test('SC-CP-07: typing "Trade Plans" navigates to the Trade Plans list page', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.keyboard.press('Control+k');
  await page.getByTestId('command-palette-input').fill('Trade Plans');
  await page.getByTestId('command-palette-page-TradePlans').click();
  await expect(page).toHaveURL(/#\/TradePlans/);
});

// AC-2 — Typing a ticker surfaces matches across Watchlist/Positions/TradePlans
test('SC-CP-08: typing an open-position ticker surfaces it under "Your Data" and navigates to Positions', async ({ page }) => {
  await goto(page, '/#/Settings');
  await page.keyboard.press('Control+k');
  await page.getByTestId('command-palette-input').fill('AAPL');
  await expect(page.getByTestId('command-palette-position-AAPL')).toBeVisible();
  await page.getByTestId('command-palette-position-AAPL').click();
  await expect(page).toHaveURL(/#\/Positions/);
});

test('SC-CP-09: typing a watchlist ticker surfaces it under "Your Data" and navigates to Watchlist', async ({ page }) => {
  await goto(page, '/#/Settings');
  await page.keyboard.press('Control+k');
  await page.getByTestId('command-palette-input').fill('MSFT');
  await expect(page.getByTestId('command-palette-watchlist-MSFT')).toBeVisible();
  await page.getByTestId('command-palette-watchlist-MSFT').click();
  await expect(page).toHaveURL(/#\/Watchlist/);
});

test('SC-CP-10: typing a trade-plan ticker surfaces it under "Your Data" and navigates to that plan\'s detail view', async ({ page }) => {
  await goto(page, '/#/Settings');
  await page.keyboard.press('Control+k');
  await page.getByTestId('command-palette-input').fill('TSLA');
  await expect(page.getByTestId('command-palette-plan-plan-1')).toBeVisible();
  await page.getByTestId('command-palette-plan-plan-1').click();
  await expect(page).toHaveURL(/#\/TradePlan\?edit=plan-1/);
});

test('SC-CP-11: no matches shows the compact "No results" empty state', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.keyboard.press('Control+k');
  await page.getByTestId('command-palette-input').fill('zzzznotarealquery');
  await expect(page.getByTestId('command-palette-empty')).toHaveText("No results for 'zzzznotarealquery'.");
});

test('SC-CP-12: empty input shows a curated set of frequent pages, no "Your Data" group', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.keyboard.press('Control+k');
  await expect(page.getByTestId('command-palette-page-Watchlist')).toBeVisible();
  await expect(page.getByTestId('command-palette-position-AAPL')).not.toBeVisible();
});

// ST-06 (BLG-FE-145, EPIC-03, v8.5) — tailwind.config.js registered `muted`/
// `muted-foreground` so `-muted` utility classes now compile to real CSS
// instead of an empty rule. CommandGroup's "Pages" heading is styled via
// `[&_[cmdk-group-heading]]:text-muted-foreground` (src/components/ui/command.js)
// -- a confirmed-affected call site rendered by SC-CP-12 above. Before the
// fix this class produced no CSS rule at all, so the heading fell back to
// whatever `color` it inherited from its ancestors (the CommandGroup's own
// `text-foreground`, near-white in this app's dark theme -- NOT literal
// black; corrected here after an inaccurate `rgb(0, 0, 0)` claim was caught
// in agent-mediated DoQ review). After the fix it must resolve to the
// actual `--muted-foreground` HSL value for the active theme.
test('SC-CP-13: "Pages" command-group heading renders the real muted-foreground colour (ST-06, BLG-FE-145)', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.keyboard.press('Control+k');
  const heading = page.locator('[cmdk-group-heading]', { hasText: 'Pages' }).first();
  await expect(heading).toBeVisible();

  const color = await heading.evaluate((el) => getComputedStyle(el).color);
  // Dark theme (this app's default, set in Layout.js) --muted-foreground is
  // "0 0% 63.9%" (src/index.css .dark) == rgb(163, 163, 163).
  expect(color).toBe('rgb(163, 163, 163)');
});

// Second confirmed-affected call site, exercising the other CSS mechanism
// -muted-foreground drives: a `::placeholder` pseudo-element colour (via
// `placeholder:text-muted-foreground`, src/components/ui/command.js
// CommandInput) rather than a plain element `color` (SC-CP-13's group
// heading, above). This is the same class shadcn's generic `Input`
// primitive (src/components/ui/input.js) uses for its own placeholder --
// CommandInput and Input share the identical utility class, so this call
// site is representative of that family too, not just the command palette.
test('SC-CP-14: command palette search input placeholder renders the real muted-foreground colour (ST-06, BLG-FE-145)', async ({ page }) => {
  await goto(page, '/#/Positions');
  await page.keyboard.press('Control+k');
  const input = page.getByTestId('command-palette-input');
  await expect(input).toBeVisible();

  const placeholderColor = await input.evaluate((el) => getComputedStyle(el, '::placeholder').color);
  expect(placeholderColor).toBe('rgb(163, 163, 163)');
});

// ST-06 (EPIC-03, v8.6, BLG-FE-149): the desktop search-affordance trigger
// button and its ⌘K badge both used the pre-v6.7 failing text-slate-500
// shade on both isDark branches (dark AND light) instead of the canonical
// text-slate-600 dark:text-slate-400 pair. Dark theme is this app's default
// (Layout.js) -- Tailwind's slate-400 is rgb(148, 163, 184).
test('SC-CP-15: desktop search-affordance trigger renders the canonical secondary-text colour, not the failing slate-500 shade', async ({ page }) => {
  await goto(page, '/#/Positions');
  const trigger = page.getByTestId('command-palette-trigger-desktop');
  await expect(trigger).toBeVisible();

  const color = await trigger.evaluate((el) => getComputedStyle(el).color);
  expect(color).toBe('rgb(148, 163, 184)');
});

test('SC-CP-16: ⌘K badge renders the canonical secondary-text colour, not the failing slate-500 shade', async ({ page }) => {
  await goto(page, '/#/Positions');
  const badge = page.getByTestId('command-palette-trigger-desktop').locator('kbd');
  await expect(badge).toBeVisible();

  const color = await badge.evaluate((el) => getComputedStyle(el).color);
  expect(color).toBe('rgb(148, 163, 184)');
});
