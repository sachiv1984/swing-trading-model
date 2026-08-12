/**
 * Saved Filter Presets & Calendar View — Acceptance Tests — ST-04 (EPIC-04, v7.5, BLG-FE-118)
 *
 * Covers the 2 acceptance criteria from stage4_backlog_slice.md#ST-04:
 *   - User can save a filter combination by name and reapply it in a later session
 *   - A calendar view renders trade plan dates and key dates, navigable by month
 *
 * Spec refs:
 *   docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md
 *   docs/specs/frontend/pages/trade_history.md §Saved Filter Presets & Calendar View
 *   docs/specs/blg_fe_118_pre_implementation_readiness_pass.md
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const MOCK_TRADES = [
  {
    id: 't-1', ticker: 'AAPL', market: 'US',
    entry_date: '2026-06-20', exit_date: '2026-07-03',
    entry_price: 150.0, exit_price: 160.0, fill_price: 150.0,
    shares: 10, pnl: 100.0, pnl_pct: 6.67, slippage_pct: 0,
    exit_reason: 'Target Reached', tags: [],
  },
  {
    id: 't-2', ticker: 'TSLA', market: 'US',
    entry_date: '2026-07-10', exit_date: '2026-07-17',
    entry_price: 250.0, exit_price: 240.0, fill_price: 250.0,
    shares: 5, pnl: -50.0, pnl_pct: -4.0, slippage_pct: 0,
    exit_reason: 'Stop Loss Hit', tags: [],
  },
];

async function mockCommonFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockTradeHistory(page, { trades = MOCK_TRADES, presets = [], onSavePreset, onDeletePreset, dailyPnl } = {}) {
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ trades }) })
  );
  await page.route(`${API}/saved-filters`, (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: presets }) });
    } else if (method === 'POST') {
      const body = route.request().postDataJSON();
      onSavePreset?.(body);
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { id: 'sf-new', ...body } }) });
    } else {
      route.continue();
    }
  });
  await page.route(new RegExp(`${API}/saved-filters/.*`), (route) => {
    if (route.request().method() === 'DELETE') {
      onDeletePreset?.();
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { deleted: true, id: 'sf-1' } }) });
    } else {
      route.continue();
    }
  });
  await page.route(new RegExp(`${API}/reports/daily-pnl.*`), (route) => {
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: dailyPnl ?? [{ day: 3, realised_pnl_gbp: 100, trade_count: 1 }, { day: 17, realised_pnl_gbp: -50, trade_count: 1 }],
        estimated_unrealised_pnl: 340.5,
        unrealised_note: 'Indicative only — not a tax liability.',
      }),
    });
  });
}

async function gotoTradeHistory(page) {
  await page.goto('/#/TradeHistory');
  await page.waitForLoadState('domcontentloaded');
}

test.beforeEach(async ({ page }) => {
  await mockCommonFallback(page);
});

// ---------------------------------------------------------------------------
// Saved Filter Presets
// ---------------------------------------------------------------------------

test('SC-SFC-01: "Save current filters as…" hidden when no filters active', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await expect(page.getByText('Save current filters as…')).toHaveCount(0);
});

test('SC-SFC-02: "Save current filters as…" appears once a filter is active', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.locator('button[role="combobox"]').first().click();
  await page.getByRole('option', { name: 'UK' }).click();

  await expect(page.getByText('Save current filters as…')).toBeVisible({ timeout: 2000 });
});

test('SC-SFC-03: saving a preset fires POST /saved-filters with name and filter_state', async ({ page }) => {
  let saveBody = null;
  await mockTradeHistory(page, { onSavePreset: (body) => { saveBody = body; } });
  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.locator('button[role="combobox"]').first().click();
  await page.getByRole('option', { name: 'UK' }).click();
  await page.getByText('Save current filters as…').click();
  await page.getByPlaceholder('Preset name').fill('My UK Trades');
  await page.getByRole('button', { name: 'Save', exact: true }).click();

  await expect.poll(() => saveBody, { timeout: 3000 }).not.toBeNull();
  expect(saveBody.name).toBe('My UK Trades');
  expect(saveBody.filter_state.market).toBe('UK');
});

test('SC-SFC-04: applying a saved preset overwrites the active filter selection', async ({ page }) => {
  await mockTradeHistory(page, {
    presets: [{ id: 'sf-1', name: 'UK Only', filter_state: { market: 'UK', result: 'all', dateFrom: '', dateTo: '', tags: [] }, created_at: '2026-07-20T10:00:00Z', updated_at: '2026-07-20T10:00:00Z' }],
  });
  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  const savedFiltersDropdown = page.locator('button[role="combobox"]').nth(2);
  await savedFiltersDropdown.click();
  await page.getByRole('option', { name: 'UK Only' }).click();

  await expect(page.getByText('Save current filters as…')).toBeVisible({ timeout: 2000 });
});

// ---------------------------------------------------------------------------
// Calendar View
// ---------------------------------------------------------------------------

test('SC-SFC-05: Calendar toggle switches view and Table remains default', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await expect(page.getByRole('button', { name: 'Table' })).toBeVisible();
  await page.getByRole('button', { name: 'Calendar' }).click();

  await expect(page.getByText(/Unrealised P&L \(as of today\)/)).toBeVisible({ timeout: 3000 });
});

test('SC-SFC-06: calendar day with exits shows a coloured indicator with tooltip', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });
  await page.getByRole('button', { name: 'Calendar' }).click();
  await expect(page.getByText(/Unrealised P&L/)).toBeVisible({ timeout: 3000 });

  const day3Button = page.locator('button[title*="trade"]').first();
  await expect(day3Button).toBeVisible({ timeout: 3000 });
  const title = await day3Button.getAttribute('title');
  expect(title).toMatch(/£/);
});

test('SC-SFC-07: clicking a day with exits switches to Table view with date filter set', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });
  await page.getByRole('button', { name: 'Calendar' }).click();
  await expect(page.getByText(/Unrealised P&L/)).toBeVisible({ timeout: 3000 });

  const dayButton = page.locator('button[title*="trade"]').first();
  await dayButton.click();

  // Back to Table view
  await expect(page.getByText(/Unrealised P&L/)).toHaveCount(0, { timeout: 2000 });
  await expect(page.locator('input[type="date"]').first()).not.toHaveValue('', { timeout: 2000 });
});

test('SC-SFC-08: month navigation fires a new GET /reports/daily-pnl request', async ({ page }) => {
  const monthsRequested = [];
  await mockTradeHistory(page);
  await page.route(new RegExp(`${API}/reports/daily-pnl.*`), (route) => {
    const url = new URL(route.request().url());
    monthsRequested.push(url.searchParams.get('month'));
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [], estimated_unrealised_pnl: 0, unrealised_note: 'x' }),
    });
  });

  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });
  await page.getByRole('button', { name: 'Calendar' }).click();
  await expect(page.getByText(/Unrealised P&L/)).toBeVisible({ timeout: 3000 });

  await expect.poll(() => monthsRequested.length, { timeout: 3000 }).toBeGreaterThanOrEqual(1);
  const initialCount = monthsRequested.length;

  await page.locator('button svg').last().locator('..').click();

  await expect.poll(() => monthsRequested.length, { timeout: 3000 }).toBeGreaterThan(initialCount);
});

test('SC-SFC-10: saved-filters preset dropdown renders the real placeholder colour (ST-05, EPIC-03, v8.6, BLG-FE-148)', async ({ page }) => {
  // Found by agent-mediated DoQ review of EPIC-03 (2026-08-11): ST-05's own
  // investigation had wrongly concluded Select's `data-[placeholder]:
  // text-muted-foreground` styling (src/components/ui/select.js:19) had no
  // live call site app-wide, since every OTHER Select in the codebase
  // pre-populates a `value`. This one doesn't -- SavedFiltersControl.js's
  // preset picker passes no `value` prop, so it renders uncontrolled and
  // shows its placeholder ("No saved filters" / "Saved filters") on every
  // visit to Trade History until a preset is picked. Dark theme (this app's
  // default) --muted-foreground is "0 0% 63.9%" == rgb(163, 163, 163),
  // matching command-palette.spec.js SC-CP-13/14's already-established value
  // for the same token.
  await mockTradeHistory(page);
  await gotoTradeHistory(page);
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  const presetTrigger = page.locator('button[role="combobox"]').filter({ hasText: 'No saved filters' });
  await expect(presetTrigger).toBeVisible({ timeout: 5000 });

  // data-[placeholder]:text-muted-foreground lives on the trigger button
  // itself (src/components/ui/select.js SelectTrigger); the inner span
  // inherits it via CSS inheritance.
  const color = await presetTrigger.evaluate((el) => getComputedStyle(el).color);
  expect(color).toBe('rgb(163, 163, 163)');
});

test('SC-SFC-09: no closed trades at all shows the full-page empty state', async ({ page }) => {
  await mockTradeHistory(page, { trades: [] });
  await gotoTradeHistory(page);
  await page.getByRole('button', { name: 'Calendar' }).click();

  // ST-10 (BLG-FE-92, EPIC-04, v8.5): heading dropped its trailing period
  // per the empty-state microcopy pattern decision (headings are labels,
  // not sentences).
  await expect(page.getByText('No closed trades yet', { exact: true })).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Your trading calendar will populate as you close trades.')).toBeVisible();
});
