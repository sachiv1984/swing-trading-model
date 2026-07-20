/**
 * Custom Price Alerts — Acceptance Tests — ST-02 (EPIC-02, v7.5, BLG-FE-116)
 *
 * Covers the CRUD acceptance criteria from stage4_backlog_slice.md#ST-02:
 *   - User can create a ticker/condition/threshold alert from the UI
 *   - User can view, edit, and delete active alerts
 * (The "alert fires via delivery channel" AC is staging-only — see
 *  qa_evidence_EPIC-02.md / backlog for the deferred-staging tracking item.)
 *
 * Spec refs:
 *   docs/design/2026-07-17__release-v7.5/custom-price-alerts/ux_spec.md
 *   docs/specs/frontend/pages/notifications.md v0.4 §Section 3
 *   docs/specs/blg_fe_116_pre_implementation_readiness_pass.md (AC-07 mock-payload strategy)
 *
 * Infrastructure: page.route() network interception — no live backend, no live
 * get_current_price/yfinance calls (per readiness pass AC-07).
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');
// Shared OpenAPI-derived mock fixture library — ST-05 (EPIC-05, v7.6, BLG-QA-114).
// Working example per that item's Quality AC: consumes the shared factories
// instead of hand-rolled inline JSON for the /price-alerts fixtures below.
const { priceAlertsListOk, priceAlert } = require('./fixtures/api-mocks');

const EMPTY_FEED = { status: 'ok', data: { notifications: [], has_more: false } };
const EMPTY_PREFS = {
  status: 'ok',
  data: {
    preferences: [
      { alert_type: 'stop_loss_approach', email_enabled: true },
      { alert_type: 'grace_period_warning', email_enabled: true },
      { alert_type: 'market_regime_change', email_enabled: true },
      { alert_type: 'daily_portfolio_summary', email_enabled: true },
    ],
  },
};
const EMPTY_RULES = { status: 'ok', data: [] };
const EMPTY_PRICE_ALERTS = priceAlertsListOk();

// Fixture rows spanning both active=true/false and both condition values (AC-07).
const POPULATED_PRICE_ALERTS = priceAlertsListOk([
  priceAlert({
    id: 'pa-1', ticker: 'AAPL', condition: 'above', threshold_price: 150.0,
    active: true, triggered_at: null,
    created_at: '2026-07-17T12:00:00Z', updated_at: '2026-07-17T12:00:00Z',
  }),
  priceAlert({
    id: 'pa-2', ticker: 'VOD.L', condition: 'below', threshold_price: 42.1,
    active: false, triggered_at: '2026-07-16T09:00:00Z',
    created_at: '2026-07-16T08:00:00Z', updated_at: '2026-07-16T09:00:00Z',
  }),
]);

async function mockCommon(page) {
  await page.route(/\/notifications\?page=/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_FEED) })
  );
  await page.route(/\/notifications\/preferences/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_PREFS) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) });
    }
  });
  await page.route(/\/alerts\/rules$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_RULES) });
    } else {
      route.continue();
    }
  });
}

async function gotoPreferences(page) {
  await page.goto('/#/notifications/preferences');
  await page.waitForLoadState('domcontentloaded');
}

// ---------------------------------------------------------------------------
// SC-CPA-01/02 — Empty state
// ---------------------------------------------------------------------------

test('SC-CPA-01: empty state shows heading, body, and CTA', async ({ page }) => {
  await mockCommon(page);
  await page.route(/\/price-alerts$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_PRICE_ALERTS) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);

  await expect(page.getByText('No custom price alerts.')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Create an alert to be notified when a ticker crosses a price you choose.')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Add price alert' })).toBeVisible();
});

test('SC-CPA-02: clicking "Add price alert" opens create form with all fields', async ({ page }) => {
  await mockCommon(page);
  await page.route(/\/price-alerts$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_PRICE_ALERTS) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add price alert' }).click();

  await expect(page.getByPlaceholder('e.g. AAPL')).toBeVisible({ timeout: 2000 });
  await expect(page.getByRole('button', { name: 'above', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'below', exact: true })).toBeVisible();
  await expect(page.getByPlaceholder('0.00')).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-CPA-03 — Ticker validation
// ---------------------------------------------------------------------------

test('SC-CPA-03: ticker validation rejects invalid format', async ({ page }) => {
  await mockCommon(page);
  await page.route(/\/price-alerts$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_PRICE_ALERTS) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add price alert' }).click();
  await page.getByPlaceholder('e.g. AAPL').fill('TOOLONGTICKER!');

  await expect(page.getByText('Invalid format. Use 1–10 alphanumeric characters.')).toBeVisible({ timeout: 2000 });
});

// ---------------------------------------------------------------------------
// SC-CPA-04 — Threshold validation
// ---------------------------------------------------------------------------

test('SC-CPA-04: threshold validation rejects non-positive value', async ({ page }) => {
  await mockCommon(page);
  await page.route(/\/price-alerts$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_PRICE_ALERTS) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add price alert' }).click();
  await page.getByPlaceholder('0.00').fill('0');

  await expect(page.getByText('Threshold must be a positive number.')).toBeVisible({ timeout: 2000 });
});

// ---------------------------------------------------------------------------
// SC-CPA-05 — Successful create
// ---------------------------------------------------------------------------

test('SC-CPA-05: save fires POST /price-alerts with correct body and refreshes list', async ({ page }) => {
  await mockCommon(page);

  let postFired = false;
  let postBody = null;
  await page.route(/\/price-alerts$/, (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      const payload = postFired ? POPULATED_PRICE_ALERTS : EMPTY_PRICE_ALERTS;
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) });
    } else if (method === 'POST') {
      postBody = route.request().postDataJSON();
      postFired = true;
      route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: POPULATED_PRICE_ALERTS.data[0] }),
      });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add price alert' }).click();

  await page.getByPlaceholder('e.g. AAPL').fill('aapl');
  await page.getByRole('button', { name: 'above', exact: true }).click();
  await page.getByPlaceholder('0.00').fill('150');

  await page.getByRole('button', { name: 'Save' }).click();

  await expect.poll(() => postBody, { timeout: 3000 }).not.toBeNull();
  expect(postBody.ticker).toBe('AAPL');
  expect(postBody.condition).toBe('above');
  expect(postBody.threshold_price).toBe(150);

  // Form closes, list refreshes with new row
  await expect(page.getByRole('button', { name: 'Save' })).toHaveCount(0, { timeout: 3000 });
  await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CPA-06 — Create error handling
// ---------------------------------------------------------------------------

test('SC-CPA-06: generic POST failure shows "Failed to create price alert" error', async ({ page }) => {
  await mockCommon(page);
  await page.route(/\/price-alerts$/, (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_PRICE_ALERTS) });
    } else if (method === 'POST') {
      route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ detail: 'Internal server error' }) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add price alert' }).click();
  await page.getByPlaceholder('e.g. AAPL').fill('AAPL');
  await page.getByPlaceholder('0.00').fill('150');
  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText('Failed to create price alert. Please try again.')).toBeVisible({ timeout: 5000 });
});

test('SC-CPA-07: cap-exceeded (400) shows the specific max-alerts message', async ({ page }) => {
  await mockCommon(page);
  await page.route(/\/price-alerts$/, (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_PRICE_ALERTS) });
    } else if (method === 'POST') {
      route.fulfill({
        status: 400, contentType: 'application/json',
        body: JSON.stringify({ detail: "You've reached the maximum number of active price alerts." }),
      });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add price alert' }).click();
  await page.getByPlaceholder('e.g. AAPL').fill('AAPL');
  await page.getByPlaceholder('0.00').fill('150');
  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText("You've reached the maximum number of active price alerts.")).toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-CPA-08 — Cancel
// ---------------------------------------------------------------------------

test('SC-CPA-08: Cancel closes create form and re-shows CTA', async ({ page }) => {
  await mockCommon(page);
  await page.route(/\/price-alerts$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EMPTY_PRICE_ALERTS) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await page.getByRole('button', { name: 'Add price alert' }).click();
  await expect(page.getByRole('button', { name: 'Save' })).toBeVisible({ timeout: 2000 });

  await page.getByRole('button', { name: 'Cancel' }).click();

  await expect(page.getByRole('button', { name: 'Save' })).toHaveCount(0, { timeout: 2000 });
  await expect(page.getByRole('button', { name: 'Add price alert' })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-CPA-09 — Populated list formatting (Active + Triggered, above/below, currency)
// ---------------------------------------------------------------------------

test('SC-CPA-09: populated list shows ticker, condition/threshold, and status correctly', async ({ page }) => {
  await mockCommon(page);
  await page.route(/\/price-alerts$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(POPULATED_PRICE_ALERTS) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);

  await expect(page.getByText('AAPL')).toBeVisible({ timeout: 5000 });
  await expect(page.getByText('Above $150.00')).toBeVisible();
  await expect(page.getByText('Active', { exact: true })).toBeVisible();

  await expect(page.getByText('VOD.L')).toBeVisible();
  await expect(page.getByText('Below £42.10')).toBeVisible();
  await expect(page.getByText('Triggered', { exact: true })).toBeVisible();

  // CTA moves to header row (not empty-state) once populated
  await expect(page.getByRole('button', { name: 'Add price alert' })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-CPA-10 — Delete flow
// ---------------------------------------------------------------------------

test('SC-CPA-10: delete icon shows inline confirmation, Delete removes the row', async ({ page }) => {
  await mockCommon(page);

  let deleteFired = false;
  await page.route(/\/price-alerts/, (route) => {
    const method = route.request().method();
    const url = route.request().url();
    if (method === 'GET' && /\/price-alerts$/.test(url)) {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(POPULATED_PRICE_ALERTS) });
    } else if (method === 'DELETE') {
      deleteFired = true;
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { deleted: true, id: 'pa-1' } }) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await expect(page.getByText('AAPL')).toBeVisible({ timeout: 5000 });

  // Click the trash icon in the AAPL row (first data row)
  const row = page.locator('div.flex.items-center.justify-between').filter({ hasText: 'AAPL' });
  await row.getByRole('button').last().click();

  await expect(page.getByText('Delete price alert for AAPL?')).toBeVisible({ timeout: 2000 });

  await page.getByRole('button', { name: 'Delete', exact: true }).click();

  await expect.poll(() => deleteFired, { timeout: 3000 }).toBe(true);
  await expect(page.getByText('Delete price alert for AAPL?')).toHaveCount(0, { timeout: 3000 });
});

test('SC-CPA-11: delete confirmation Cancel dismisses without deleting', async ({ page }) => {
  await mockCommon(page);
  let deleteFired = false;
  await page.route(/\/price-alerts/, (route) => {
    const method = route.request().method();
    const url = route.request().url();
    if (method === 'GET' && /\/price-alerts$/.test(url)) {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(POPULATED_PRICE_ALERTS) });
    } else if (method === 'DELETE') {
      deleteFired = true;
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { deleted: true, id: 'pa-1' } }) });
    } else {
      route.continue();
    }
  });

  await gotoPreferences(page);
  await expect(page.getByText('AAPL')).toBeVisible({ timeout: 5000 });

  const row = page.locator('div.flex.items-center.justify-between').filter({ hasText: 'AAPL' });
  await row.getByRole('button').last().click();
  await expect(page.getByText('Delete price alert for AAPL?')).toBeVisible({ timeout: 2000 });

  await page.getByRole('button', { name: 'Cancel', exact: true }).click();

  await expect(page.getByText('Delete price alert for AAPL?')).toHaveCount(0, { timeout: 2000 });
  expect(deleteFired).toBe(false);
  // Row still present
  await expect(page.getByText('AAPL')).toBeVisible();
});
