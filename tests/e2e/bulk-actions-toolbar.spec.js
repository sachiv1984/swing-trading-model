/**
 * Bulk Actions Toolbar — Acceptance Tests — ST-03 (EPIC-03, v7.5, BLG-FE-117)
 *
 * Covers the 3 acceptance criteria from stage4_backlog_slice.md#ST-03:
 *   - Rows in Watchlist and TradePlans tables are multi-selectable
 *   - A bulk-action toolbar appears once one or more rows are selected
 *   - Bulk tag/archive/remove operations apply to all selected rows in a single action
 *
 * Spec refs:
 *   docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md
 *   docs/specs/frontend/pages/watchlist.md v0.4 §Bulk Actions
 *   docs/specs/frontend/pages/trade_plan.md v1.1 §11 Bulk Actions
 *   docs/specs/blg_fe_117_pre_implementation_readiness_pass.md (AC-04 scenario list)
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const MOCK_WATCHLIST = [
  { id: 'wl-1', ticker: 'AAPL', market: 'US', company_name: 'Apple Inc.', signal_status: 'active', tags: [], target_entry_price: null, initial_stop_price: null, current_stop_price: null, created_at: '2026-07-17T10:00:00Z' },
  { id: 'wl-2', ticker: 'MSFT', market: 'US', company_name: 'Microsoft', signal_status: 'no_signal', tags: [], target_entry_price: null, initial_stop_price: null, current_stop_price: null, created_at: '2026-07-16T10:00:00Z' },
];

const MOCK_PLANS = [
  { id: 'tp-1', ticker: 'AAPL', market: 'US', status: 'draft', r_target: 2, setup_thesis: 'breakout', updated_at: '2026-07-17T10:00:00Z' },
  { id: 'tp-2', ticker: 'TSLA', market: 'US', status: 'active', r_target: 3, setup_thesis: 'momentum', updated_at: '2026-07-16T10:00:00Z' },
];

async function mockCommonFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockWatchlist(page, { onBulkTag, onBulkDelete } = {}) {
  await page.route(`${API}/watchlist/tags`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: ['momentum'] }) })
  );
  await page.route(`${API}/watchlist/bulk-tag`, (route) => {
    const body = route.request().postDataJSON();
    onBulkTag?.(body);
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { succeeded: body.ids, failed: [] } }) });
  });
  await page.route(`${API}/watchlist/bulk`, (route) => {
    const body = route.request().postDataJSON();
    onBulkDelete?.(body);
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { succeeded: body.ids, failed: [] } }) });
  });
  await page.route(`${API}/watchlist`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: MOCK_WATCHLIST }) });
    } else {
      route.continue();
    }
  });
}

async function mockTradePlans(page, { onBulkTag, onBulkArchive, onBulkDelete } = {}) {
  await page.route(`${API}/trade-plans/tags`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: ['momentum'] }) })
  );
  await page.route(`${API}/trade-plans/bulk-tag`, (route) => {
    const body = route.request().postDataJSON();
    onBulkTag?.(body);
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { succeeded: body.ids, failed: [] } }) });
  });
  await page.route(`${API}/trade-plans/bulk-archive`, (route) => {
    const body = route.request().postDataJSON();
    onBulkArchive?.(body);
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { succeeded: body.ids, failed: [] } }) });
  });
  await page.route(`${API}/trade-plans/bulk`, (route) => {
    const body = route.request().postDataJSON();
    onBulkDelete?.(body);
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { succeeded: body.ids, failed: [] } }) });
  });
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: MOCK_PLANS }) });
    } else {
      route.continue();
    }
  });
}

test.beforeEach(async ({ page }) => {
  await mockCommonFallback(page);
});

// ---------------------------------------------------------------------------
// Watchlist
// ---------------------------------------------------------------------------

test('SC-BAT-01: Watchlist rows are multi-selectable via checkboxes', async ({ page }) => {
  await mockWatchlist(page);
  await page.goto('/#/Watchlist');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await expect(page.getByRole('checkbox').first()).toBeVisible();
});

test('SC-BAT-02: Watchlist toolbar absent at zero-selected, appears on 1+ selected', async ({ page }) => {
  await mockWatchlist(page);
  await page.goto('/#/Watchlist');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await expect(page.getByText(/selected$/)).toHaveCount(0);

  const checkboxes = page.getByRole('checkbox');
  await checkboxes.nth(1).click(); // first row checkbox (0 = header select-all)

  await expect(page.getByText('1 selected')).toBeVisible({ timeout: 2000 });
  await expect(page.getByRole('button', { name: 'Bulk Tag' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Bulk Remove' })).toBeVisible();
});

test('SC-BAT-03: Watchlist Clear button deselects all rows', async ({ page }) => {
  await mockWatchlist(page);
  await page.goto('/#/Watchlist');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').nth(1).click();
  await expect(page.getByText('1 selected')).toBeVisible({ timeout: 2000 });

  await page.getByRole('button', { name: 'Clear' }).click();
  await expect(page.getByText(/selected$/)).toHaveCount(0);
});

test('SC-BAT-04: Watchlist select-all header checkbox selects all visible rows', async ({ page }) => {
  await mockWatchlist(page);
  await page.goto('/#/Watchlist');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').first().click();
  await expect(page.getByText('2 selected')).toBeVisible({ timeout: 2000 });
});

test('SC-BAT-05: Watchlist Bulk Tag applies tags to all selected rows via POST /watchlist/bulk-tag', async ({ page }) => {
  let postBody = null;
  await mockWatchlist(page, { onBulkTag: (body) => { postBody = body; } });
  await page.goto('/#/Watchlist');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').first().click(); // select all
  await expect(page.getByText('2 selected')).toBeVisible({ timeout: 2000 });

  await page.getByRole('button', { name: 'Bulk Tag' }).click();
  await page.getByPlaceholder('Add a tag and press Enter').fill('momentum');
  await page.getByPlaceholder('Add a tag and press Enter').press('Enter');
  await page.getByRole('button', { name: 'Apply Tags' }).click();

  await expect.poll(() => postBody, { timeout: 3000 }).not.toBeNull();
  expect(postBody.ids.sort()).toEqual(['wl-1', 'wl-2']);
  expect(postBody.tags).toEqual(['momentum']);

  await expect(page.getByText('2 entries updated.')).toBeVisible({ timeout: 3000 });
  // Selection cleared, toolbar gone
  await expect(page.getByText(/selected$/)).toHaveCount(0);
});

test('SC-BAT-06: Watchlist Bulk Remove requires confirmation before firing DELETE /watchlist/bulk', async ({ page }) => {
  let deleteFired = false;
  await mockWatchlist(page, { onBulkDelete: () => { deleteFired = true; } });
  await page.goto('/#/Watchlist');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').nth(1).click();
  await page.getByRole('button', { name: 'Bulk Remove' }).click();

  await expect(page.getByText('Remove 1 selected watchlist entries?')).toBeVisible({ timeout: 2000 });
  expect(deleteFired).toBe(false);

  await page.getByRole('button', { name: 'Bulk Remove', exact: true }).last().click();

  await expect.poll(() => deleteFired, { timeout: 3000 }).toBe(true);
});

test('SC-BAT-07: Watchlist Bulk Remove Cancel dismisses without deleting', async ({ page }) => {
  let deleteFired = false;
  await mockWatchlist(page, { onBulkDelete: () => { deleteFired = true; } });
  await page.goto('/#/Watchlist');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').nth(1).click();
  await page.getByRole('button', { name: 'Bulk Remove' }).click();
  await expect(page.getByText('Remove 1 selected watchlist entries?')).toBeVisible({ timeout: 2000 });

  await page.getByRole('button', { name: 'Cancel' }).click();
  await expect(page.getByText('Remove 1 selected watchlist entries?')).toHaveCount(0);
  expect(deleteFired).toBe(false);
  // Selection retained after cancel
  await expect(page.getByText('1 selected')).toBeVisible();
});

// ---------------------------------------------------------------------------
// Trade Plans
// ---------------------------------------------------------------------------

test('SC-BAT-08: Trade Plans rows are multi-selectable and toolbar shows Bulk Archive/Delete', async ({ page }) => {
  await mockTradePlans(page);
  await page.goto('/#/TradePlans');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').nth(1).click();
  await expect(page.getByText('1 selected')).toBeVisible({ timeout: 2000 });
  await expect(page.getByRole('button', { name: 'Bulk Tag' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Bulk Archive' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Bulk Delete' })).toBeVisible();
});

test('SC-BAT-09: Trade Plans shows excluded-count note when an active plan is selected', async ({ page }) => {
  await mockTradePlans(page);
  await page.goto('/#/TradePlans');
  await expect(page.getByText('TSLA').first()).toBeVisible({ timeout: 8000 });

  // Select all (row 1 = draft AAPL, row 2 = active TSLA)
  await page.getByRole('checkbox').first().click();
  await expect(page.getByText('2 selected')).toBeVisible({ timeout: 2000 });
  await expect(page.getByText('1 active plan(s) excluded — cannot be archived.')).toBeVisible();
});

test('SC-BAT-10: Trade Plans Bulk Delete confirmation fires DELETE /trade-plans/bulk with correct ids', async ({ page }) => {
  let deleteBody = null;
  await mockTradePlans(page, { onBulkDelete: (body) => { deleteBody = body; } });
  await page.goto('/#/TradePlans');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').nth(1).click();
  await page.getByRole('button', { name: 'Bulk Delete' }).click();
  await expect(page.getByText('Delete 1 selected trade plan(s)?')).toBeVisible({ timeout: 2000 });

  await page.getByRole('button', { name: 'Bulk Delete', exact: true }).last().click();

  await expect.poll(() => deleteBody, { timeout: 3000 }).not.toBeNull();
  expect(deleteBody.ids).toEqual(['tp-1']);
  await expect(page.getByText('1 plans updated.')).toBeVisible({ timeout: 3000 });
});

test('SC-BAT-11: Trade Plans Bulk Tag applies tags via POST /trade-plans/bulk-tag', async ({ page }) => {
  let postBody = null;
  await mockTradePlans(page, { onBulkTag: (body) => { postBody = body; } });
  await page.goto('/#/TradePlans');
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').nth(1).click();
  await page.getByRole('button', { name: 'Bulk Tag' }).click();
  await page.getByPlaceholder('Add a tag and press Enter').fill('breakout');
  await page.getByPlaceholder('Add a tag and press Enter').press('Enter');
  await page.getByRole('button', { name: 'Apply Tags' }).click();

  await expect.poll(() => postBody, { timeout: 3000 }).not.toBeNull();
  expect(postBody.ids).toEqual(['tp-1']);
  expect(postBody.tags).toEqual(['breakout']);
});

test('SC-BAT-12: partial-failure shows per-row detail, not a single opaque message', async ({ page }) => {
  await mockTradePlans(page);
  // Override bulk-archive to return a partial failure
  await page.route(`${API}/trade-plans/bulk-archive`, (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { succeeded: ['tp-1'], failed: [{ id: 'tp-2', reason: 'active_status_excluded' }] } }),
    });
  });

  await page.goto('/#/TradePlans');
  await expect(page.getByText('TSLA').first()).toBeVisible({ timeout: 8000 });

  await page.getByRole('checkbox').first().click(); // select all
  await page.getByRole('button', { name: 'Bulk Archive' }).click();
  await expect(page.getByText('Archive 2 selected trade plan(s)?')).toBeVisible({ timeout: 2000 });
  await page.getByRole('button', { name: 'Bulk Archive', exact: true }).last().click();

  await expect(page.getByText('1 succeeded, 1 failed.')).toBeVisible({ timeout: 3000 });
  await page.getByRole('button', { name: /Details/i }).click();
  await expect(page.getByText('tp-2: active_status_excluded')).toBeVisible();

  // Failed row remains selected
  await expect(page.getByText('1 selected')).toBeVisible();
});
