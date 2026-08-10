/**
 * Trade Plan Acceptance Tests — ST-03 (EPIC-01, v3.1) + ST-09 (EPIC-03, v3.5)
 *
 * Covers observable AC for the Trade Plan creation/edit form:
 *   SC-TP-01  Form renders with all required fields
 *   SC-TP-02  Ticker/market pre-populated from query params
 *   SC-TP-03  Regime context auto-populated from GET /market/status
 *   SC-TP-04  Save button disabled when ticker is empty
 *   SC-TP-05  Existing plan banner shown when position already has a plan
 *   SC-TP-06  Success banner shown after saving
 *   SC-TP-07  No regression — Positions and Watchlist pages still render
 *   SC-TP-08  Edit mode: form pre-populated from GET /trade-plans/{id} (RQ v5 useEffect fix)
 *   SC-TP-29  Native form fields use the shared focus-visible:ring pattern (ST-04, EPIC-01, v8.2, BLG-FE-138)
 *
 * Spec refs: GitHub Issue #311 (ST-03 AC), GitHub Issue #394 (ST-09 AC)
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const PLAN_ID = '00000000-0000-0000-0000-000000000001';
const POSITION_ID = '00000000-0000-0000-0000-000000000002';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

const MARKET_STATUS_OK = {
  status: 'ok',
  data: { regime_status: 'risk_on' },
};

const TRADE_PLAN_SAVED = {
  status: 'ok',
  data: {
    id: PLAN_ID,
    ticker: 'AAPL',
    market: 'US',
    status: 'draft',
    setup_thesis: 'Test thesis',
    entry_rationale: 'Test rationale',
    regime_context_at_entry: 'risk_on',
    r_target: 2.5,
    early_exit_conditions: null,
    confirmation_criteria: null,
    checklist_completed: false,
    checklist_items: [],
  },
};

const PRE_ENTRY_VALIDATION_WARN = {
  status: 'ok',
  data: {
    ticker: 'AAPL',
    market: 'US',
    quantity: 10,
    advisory_status: 'warn',
    override_required: true,
    checks: [
      { rule: 'regime_gate', status: 'pass', detail: 'US market is Risk-On', severity: 'fail' },
      { rule: 'cash_constraint', status: 'pass', detail: 'Within available cash', severity: 'fail' },
      { rule: 'sector_concentration', status: 'warn', detail: 'Technology 32% > 30% limit', severity: 'warn' },
      { rule: 'earnings_proximity', status: 'pass', detail: 'Earnings 71 days away', severity: 'warn' },
      { rule: 'sizing_validity', status: 'pass', detail: 'Position sizing valid', severity: 'warn' },
    ],
  },
};

const PRE_ENTRY_VALIDATION_PASS = {
  status: 'ok',
  data: {
    ticker: 'AAPL',
    market: 'US',
    quantity: 10,
    advisory_status: 'pass',
    override_required: false,
    checks: [
      { rule: 'regime_gate', status: 'pass', detail: 'US market is Risk-On', severity: 'fail' },
      { rule: 'cash_constraint', status: 'pass', detail: 'Within available cash', severity: 'fail' },
      { rule: 'sector_concentration', status: 'pass', detail: 'Sector allocation within limits', severity: 'warn' },
      { rule: 'earnings_proximity', status: 'pass', detail: 'Earnings 71 days away', severity: 'warn' },
      { rule: 'sizing_validity', status: 'pass', detail: 'Position sizing valid', severity: 'warn' },
    ],
  },
};

const EXISTING_PLAN_FOR_POSITION = {
  status: 'ok',
  data: [
    {
      id: PLAN_ID,
      ticker: 'AAPL',
      market: 'US',
      position_id: POSITION_ID,
      status: 'active',
    },
  ],
};

const NO_PLAN_FOR_POSITION = { status: 'ok', data: null };

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMarketStatus(page, payload = MARKET_STATUS_OK) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockTradePlansPost(page, payload = TRADE_PLAN_SAVED) {
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(payload) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
  });
}

async function mockByPosition(page, payload) {
  await page.route(new RegExp(`${API}/trade-plans/by-position/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

/** Navigate to the TradePlan page with optional query params. */
async function gotoTradePlan(page, params = {}) {
  const qs = new URLSearchParams(params).toString();
  const hash = qs ? `/#/TradePlan?${qs}` : '/#/TradePlan';
  await page.goto(hash);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-TP-01 — Form renders with all required fields
// ---------------------------------------------------------------------------

test('SC-TP-01: Trade Plan form renders all required fields', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  // Text areas for reasoning fields
  await expect(page.getByPlaceholder(/describe the setup/i)).toBeVisible({ timeout: 5000 });
  await expect(page.getByPlaceholder(/why enter now/i)).toBeVisible();
  await expect(page.getByPlaceholder(/what must be true/i)).toBeVisible();
  await expect(page.getByPlaceholder(/under what conditions/i)).toBeVisible();

  // Numeric and select fields
  await expect(page.getByPlaceholder(/e\.g\. 2\.5/i)).toBeVisible();
  await expect(page.locator('select').filter({ has: page.locator('option[value="US"]') })).toBeVisible();

  // Pre-entry checklist (replaced single checkbox with structured checklist in ST-05)
  await expect(page.getByText('Strategy signal confirmed')).toBeVisible();
  await expect(page.getByText('Stop level defined')).toBeVisible();

  // Save button present
  await expect(page.getByRole('button', { name: /save plan/i })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-TP-29 — Native form fields use the shared focus-visible ring pattern
// (ST-04, EPIC-01, v8.2, BLG-FE-138)
// ---------------------------------------------------------------------------

test('SC-TP-29: Native form fields use the shared focus-visible:ring pattern, not the old focus:border-cyan-500', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  const setupThesis = page.getByPlaceholder(/describe the setup/i);
  await expect(setupThesis).toHaveClass(/focus-visible:ring-1/);
  await expect(setupThesis).toHaveClass(/focus-visible:ring-ring/);
  await expect(setupThesis).not.toHaveClass(/focus:border-cyan-500/);

  const marketSelect = page.locator('select').filter({ has: page.locator('option[value="US"]') });
  await expect(marketSelect).toHaveClass(/focus-visible:ring-1/);
  await expect(marketSelect).not.toHaveClass(/focus:border-cyan-500/);
});

// ---------------------------------------------------------------------------
// SC-TP-02 — Ticker and market pre-populated from query params
// ---------------------------------------------------------------------------

test('SC-TP-02: Ticker and market pre-populated from query params', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await gotoTradePlan(page, { ticker: 'TSLA', market: 'US' });

  await expect(page.locator('input[placeholder*="AAPL"]')).toHaveValue('TSLA', { timeout: 5000 });

  // Market select shows the passed value
  const marketSelect = page.locator('select').filter({ has: page.locator('option[value="US"]') }).first();
  await expect(marketSelect).toHaveValue('US');
});

// ---------------------------------------------------------------------------
// SC-TP-03 — Regime context auto-populated from GET /market/status
// ---------------------------------------------------------------------------

test('SC-TP-03: Regime context input auto-populated from market status API', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page, { status: 'ok', data: { regime_status: 'risk_off' } });
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  // Regime at Entry is now a read-only display div (not an input) — auto-populated
  // from the market status API and not editable by the user to prevent bypass.
  const regimeField = page.locator('label').filter({ hasText: /regime at entry/i }).locator('xpath=../div');
  await expect(regimeField).toContainText('risk_off', { timeout: 5000 });
});

// ---------------------------------------------------------------------------
// SC-TP-04 — Save button disabled when ticker is empty
// ---------------------------------------------------------------------------

test('SC-TP-04: Save Plan button is disabled when ticker field is empty', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await gotoTradePlan(page);

  // No ticker passed — button should be disabled
  const saveBtn = page.getByRole('button', { name: /save plan/i });
  await expect(saveBtn).toBeDisabled({ timeout: 5000 });

  // Entering a ticker enables the button
  await page.locator('input[placeholder*="AAPL"]').fill('MSFT');
  await expect(saveBtn).toBeEnabled({ timeout: 3000 });
});

// ---------------------------------------------------------------------------
// SC-TP-05 — Existing plan banner when position already has a plan
// ---------------------------------------------------------------------------

test('SC-TP-05: Amber banner shown when position already has an existing trade plan', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockByPosition(page, EXISTING_PLAN_FOR_POSITION);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US', position_id: POSITION_ID });

  // Amber banner with "edit it instead" link
  await expect(page.locator('[class*="amber"]').filter({ hasText: /existing trade plan/i })).toBeVisible({ timeout: 5000 });
  await expect(page.getByRole('button', { name: /edit it instead/i })).toBeVisible();
});

// ---------------------------------------------------------------------------
// SC-TP-06 — Success banner shown after saving
// ---------------------------------------------------------------------------

test('SC-TP-06: Success banner shown after trade plan is saved', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockByPosition(page, NO_PLAN_FOR_POSITION);
  await mockTradePlansPost(page);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  await page.getByRole('button', { name: /save plan/i }).click();

  await expect(page.locator('[class*="emerald"]').filter({ hasText: /saved successfully/i })).toBeVisible({ timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-TP-07 — No regression to Positions and Watchlist pages
// ---------------------------------------------------------------------------

test('SC-TP-07a: Positions page still renders after Trade Plan routes are registered', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );

  await page.goto('/#/Positions');

  // No crash — page heading is always present (h1 alone avoids strict-mode
  // violation when both the heading and empty-state text are simultaneously visible)
  await expect(page.locator('h1').filter({ hasText: /positions/i })).toBeVisible({ timeout: 8000 });
});

test('SC-TP-07b: Watchlist page still renders after Trade Plan routes are registered', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/watchlist`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );

  await page.goto('/#/Watchlist');

  await expect(page.locator('h1').filter({ hasText: /watchlist/i })).toBeVisible({ timeout: 8000 });
});

// ---------------------------------------------------------------------------
// SC-TP-08 — Edit mode: form pre-populated from existing plan (RQ v5 fix)
// ---------------------------------------------------------------------------

const EXISTING_PLAN_DETAIL = {
  status: 'ok',
  data: {
    id: PLAN_ID,
    ticker: 'AAPL',
    market: 'US',
    status: 'draft',
    setup_thesis: 'Breakout above 50d MA on volume',
    entry_rationale: 'Confirmed with signal',
    regime_context_at_entry: 'risk_on',
    r_target: 2.0,
    early_exit_conditions: 'Close below 50d MA',
    confirmation_criteria: 'Volume > 1.5x avg',
    checklist_items: [
      { id: 'signal_confirmed', label: 'Strategy signal confirmed', checked: true },
      { id: 'stop_defined', label: 'Stop level defined', checked: false },
    ],
  },
};

test('SC-TP-08: Edit mode pre-populates form fields from GET /trade-plans/{id}', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(new RegExp(`${API}/trade-plans/${PLAN_ID}$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EXISTING_PLAN_DETAIL) })
  );

  const qs = new URLSearchParams({ edit: PLAN_ID, ticker: 'AAPL', market: 'US' }).toString();
  await page.goto(`/#/TradePlan?${qs}`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });

  // Form fields should be pre-populated from the fetched plan
  await expect(page.getByPlaceholder(/describe the setup/i)).toHaveValue('Breakout above 50d MA on volume', { timeout: 5000 });
  await expect(page.getByPlaceholder(/why enter now/i)).toHaveValue('Confirmed with signal');
  await expect(page.getByPlaceholder(/e\.g\. 2\.5/i)).toHaveValue('2');
});

// ---------------------------------------------------------------------------
// SC-TP-09 through SC-TP-14 — ST-06, ST-07, ST-08 (v3.8 EPIC-03)
// ---------------------------------------------------------------------------

// ST-06 — Setup Type Classification Field

test('SC-TP-09: Setup type dropdown is present on the trade plan form', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('setup-type-select')).toBeVisible({ timeout: 8000 });
});

test('SC-TP-10: Setup type dropdown contains all six options', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.getByTestId('setup-type-select')).toBeVisible({ timeout: 8000 });

  const options = await page.getByTestId('setup-type-select').locator('option').allTextContents();
  const expected = ['Breakout', 'Pullback to MA', 'Momentum Continuation', 'Mean Reversion', 'Catalyst-driven', 'Other'];
  for (const opt of expected) {
    expect(options).toContain(opt);
  }
});

test('SC-TP-11: Setup type value is persisted in saved plan payload', async ({ page }) => {
  const posts = [];
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      posts.push(JSON.parse(route.request().postData()));
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { id: PLAN_ID } }) });
    } else { route.continue(); }
  });

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.getByTestId('setup-type-select')).toBeVisible({ timeout: 8000 });
  await page.getByTestId('setup-type-select').selectOption('Breakout');
  await page.getByRole('button', { name: /save plan/i }).click();
  await page.waitForTimeout(500);

  expect(posts.length).toBeGreaterThan(0);
  expect(posts[0].setup_type).toBe('Breakout');
});

// ST-07 — News Context Panel

test('SC-TP-12: News context panel renders for US ticker when news is available', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(`${API}/news/AAPL`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [
        { title: 'Apple beats earnings', source: 'Reuters', created_at: new Date().toISOString() },
        { title: 'iPhone demand strong', source: 'Bloomberg', created_at: new Date().toISOString() },
      ]}),
    })
  );
  await page.route(new RegExp(`${API}/news/AAPL\\?limit=5`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [
        { title: 'Apple beats earnings', source: 'Reuters', created_at: new Date().toISOString() },
        { title: 'iPhone demand strong', source: 'Bloomberg', created_at: new Date().toISOString() },
      ]}),
    })
  );

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('news-context-panel')).toBeVisible({ timeout: 8000 });
});

test('SC-TP-13: News panel is collapsible', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(new RegExp(`${API}/news/AAPL`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [
        { title: 'Apple beats earnings', source: 'Reuters', created_at: new Date().toISOString() },
      ]}),
    })
  );

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.getByTestId('news-context-panel')).toBeVisible({ timeout: 8000 });
  // Toggle should be clickable
  await page.getByTestId('news-panel-toggle').click();
  // Headline list should be hidden after collapse
  await expect(page.getByTestId('news-headline-list')).not.toBeVisible({ timeout: 3000 });
});

// ST-08 — AI-Assisted Thesis Generation

test('SC-TP-14: Generate thesis button is present on the trade plan form', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('generate-thesis-btn')).toBeVisible({ timeout: 8000 });
});

test('SC-TP-15: Clicking generate thesis populates the setup thesis textarea', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.getByTestId('generate-thesis-btn')).toBeVisible({ timeout: 8000 });

  // Select a setup type first
  await page.getByTestId('setup-type-select').selectOption('Breakout');
  await page.getByTestId('generate-thesis-btn').click();

  const textarea = page.getByTestId('setup-thesis-textarea');
  const value = await textarea.inputValue();
  expect(value.length).toBeGreaterThan(10);
});

test('SC-TP-16: AI draft badge appears after generating thesis and clears on user edit', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.getByTestId('generate-thesis-btn')).toBeVisible({ timeout: 8000 });

  await page.getByTestId('generate-thesis-btn').click();
  await expect(page.getByTestId('ai-draft-badge')).toBeVisible({ timeout: 3000 });

  // Editing the textarea should clear the badge
  await page.getByTestId('setup-thesis-textarea').click();
  await page.keyboard.press('End');
  await page.keyboard.type(' edited');
  await expect(page.getByTestId('ai-draft-badge')).not.toBeVisible({ timeout: 3000 });
});

// ST-03 — Pre-Entry Validation Panel (SI-01)

test('SC-TP-17: Pre-entry checks panel renders when ticker and quantity are set', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(`${API}/portfolio/pre-entry-validation*`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PRE_ENTRY_VALIDATION_PASS) })
  );
  await page.route(new RegExp(`${API}/news/AAPL`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });

  // Panel should not be visible before quantity is set
  await expect(page.getByTestId('pre-entry-checks-panel')).not.toBeVisible({ timeout: 3000 });

  // Fill quantity
  await page.getByPlaceholder(/e\.g\. 50/i).fill('10');

  // Panel should now appear
  await expect(page.getByTestId('pre-entry-checks-panel')).toBeVisible({ timeout: 5000 });
});

test('SC-TP-18: Pre-entry checks panel hidden when quantity is empty', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(new RegExp(`${API}/news/AAPL`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('pre-entry-checks-panel')).not.toBeVisible({ timeout: 3000 });
});

test('SC-TP-19: Override acknowledgement checkbox visible when advisory warning present', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(`${API}/portfolio/pre-entry-validation*`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PRE_ENTRY_VALIDATION_WARN) })
  );
  await page.route(new RegExp(`${API}/news/AAPL`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
  await page.getByPlaceholder(/e\.g\. 50/i).fill('10');
  await expect(page.getByTestId('pre-entry-checks-panel')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('override-acknowledgement-checkbox')).toBeVisible({ timeout: 5000 });
});

test('SC-TP-20: Plan saves with pre_entry_override_acknowledged in payload when override checked', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(`${API}/portfolio/pre-entry-validation*`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PRE_ENTRY_VALIDATION_WARN) })
  );
  await page.route(new RegExp(`${API}/news/AAPL`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  let capturedBody = null;
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      capturedBody = JSON.parse(route.request().postData() || '{}');
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(TRADE_PLAN_SAVED) });
    } else {
      route.continue();
    }
  });

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
  await page.getByPlaceholder(/e\.g\. 50/i).fill('10');
  await expect(page.getByTestId('override-acknowledgement-checkbox')).toBeVisible({ timeout: 5000 });
  await page.getByTestId('override-acknowledgement-checkbox').check();

  // Save the plan
  await page.getByRole('button', { name: /Save Plan/i }).click();
  await expect(page.locator('text=/saved|success/i')).toBeVisible({ timeout: 5000 });

  expect(capturedBody).not.toBeNull();
  expect(capturedBody.pre_entry_override_acknowledged).toBe(true);
});

// ST-16 — entry_price / stop_price parameters in pre-entry validation API call

test('SC-TP-21: Pre-entry validation request includes entry_price and stop_price when both are provided', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(new RegExp(`${API}/news/AAPL`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  let capturedUrl = null;
  await page.route(`${API}/portfolio/pre-entry-validation*`, (route) => {
    capturedUrl = route.request().url();
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PRE_ENTRY_VALIDATION_PASS) });
  });

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });

  // Fill quantity to trigger the validation panel
  await page.getByPlaceholder(/e\.g\. 50/i).fill('10');
  // Fill entry and stop prices
  await page.getByTestId('planned-entry-price-input').fill('150');
  await page.getByTestId('planned-stop-price-input').fill('142');

  // Wait for the panel to load
  await expect(page.getByTestId('pre-entry-checks-panel')).toBeVisible({ timeout: 5000 });

  // Verify the API request URL includes both price params
  expect(capturedUrl).not.toBeNull();
  expect(capturedUrl).toContain('entry_price=150');
  expect(capturedUrl).toContain('stop_price=142');
});

// ST-17 — No "Gemini" text in AI thesis generation UI

test('SC-TP-22: AI thesis generation UI contains no Gemini references', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await page.route(new RegExp(`${API}/news/AAPL`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });

  // Check entire page text for Gemini references
  const pageContent = await page.locator('body').innerText();
  expect(pageContent.toLowerCase()).not.toContain('gemini');
});

// ---------------------------------------------------------------------------
// SC-TP-23 — Claude thesis feedback mechanism (ST-07, BLG-FE-46, v6.5)
// docs/design/2026-07-02__release-v6.5/thesis-feedback-mechanism/ux_spec.md
// ---------------------------------------------------------------------------

const GENERATE_PLAN_RESPONSE = {
  status: 'ok',
  data: {
    available: true,
    fields: {
      setup_thesis: 'Claude-generated thesis: AAPL breaking out above 200 EMA on rising volume.',
      entry_rationale: 'Momentum confirmed by relative strength vs SPY.',
      confirmation_criteria: 'Close above prior resistance on 2x avg volume.',
    },
    // ST-07 (BLG-FE-143, EPIC-03, v8.5): real shape returned by
    // generate_full_plan() (backend/services/gemini_service.py) alongside
    // `fields` -- previously omitted from this fixture since nothing
    // consumed it yet.
    model_version: 'claude-haiku-4-5',
    prompt_version: 'v3.0',
  },
};

async function mockImproveWithAi(page, payload = GENERATE_PLAN_RESPONSE) {
  await page.route(`${API}/trade-plans/generate-plan`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

// mockFallback registers a catch-all `${API}/` route; Playwright resolves
// overlapping routes in most-recently-registered-first order, so any
// specific mock (e.g. mockImproveWithAi) must be (re-)registered AFTER
// mockFallback runs inside this helper, not before it's called — otherwise
// the catch-all silently wins and the specific mock is never reached.
async function gotoTradePlanForAi(page, { improveWithAi } = {}) {
  await mockFallback(page);
  if (improveWithAi) await mockImproveWithAi(page, improveWithAi === true ? undefined : improveWithAi);
  await mockMarketStatus(page);
  await page.route(new RegExp(`${API}/news/AAPL`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.goto('/#/TradePlan?ticker=AAPL&market=US');
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

test('SC-TP-23a: feedback control is not shown for template-only "Generate thesis" (not a Claude draft)', async ({ page }) => {
  await gotoTradePlanForAi(page);
  await expect(page.getByTestId('generate-thesis-btn')).toBeVisible({ timeout: 8000 });

  await page.getByTestId('generate-thesis-btn').click();
  await expect(page.getByTestId('ai-draft-badge')).toBeVisible({ timeout: 3000 });

  // Template-only draft sets isAiDraft but must never set isClaudeDraft — the
  // feedback control must not render (ux_spec.md "Trigger Condition" note).
  await expect(page.getByTestId('thesis-feedback-control')).toHaveCount(0);
});

test('SC-TP-23b: feedback control appears after "Improve with AI" (Claude draft) and not before', async ({ page }) => {
  await gotoTradePlanForAi(page, { improveWithAi: true });

  const improveBtn = page.getByTestId('improve-with-ai-btn');
  await expect(improveBtn).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('thesis-feedback-control')).toHaveCount(0);

  await improveBtn.click();
  await expect(page.getByTestId('thesis-feedback-control')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('thesis-feedback-useful')).toBeVisible();
  await expect(page.getByTestId('thesis-feedback-not-useful')).toBeVisible();
});

test('SC-TP-23c: selecting "Useful" highlights it, disables both options, and shows the confirmation', async ({ page }) => {
  await gotoTradePlanForAi(page, { improveWithAi: true });

  await page.getByTestId('improve-with-ai-btn').click();
  await expect(page.getByTestId('thesis-feedback-useful')).toBeVisible({ timeout: 5000 });

  await page.getByTestId('thesis-feedback-useful').click();

  await expect(page.getByTestId('thesis-feedback-confirmation')).toBeVisible({ timeout: 1000 });
  await expect(page.getByTestId('thesis-feedback-confirmation')).toHaveText('Thanks — feedback recorded.');

  // After the confirmation fades (~2s), both options remain visible but disabled,
  // with the selected option highlighted (ux_spec.md "Post-selection").
  await expect(page.getByTestId('thesis-feedback-useful')).toBeVisible({ timeout: 3000 });
  await expect(page.getByTestId('thesis-feedback-useful')).toBeDisabled();
  await expect(page.getByTestId('thesis-feedback-useful')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByTestId('thesis-feedback-not-useful')).toBeDisabled();
});

test('SC-TP-23d: selecting "Not useful" highlights it and disables both options (single-shot per draft)', async ({ page }) => {
  await gotoTradePlanForAi(page, { improveWithAi: true });

  await page.getByTestId('improve-with-ai-btn').click();
  await expect(page.getByTestId('thesis-feedback-not-useful')).toBeVisible({ timeout: 5000 });

  await page.getByTestId('thesis-feedback-not-useful').click();
  await expect(page.getByTestId('thesis-feedback-confirmation')).toBeVisible({ timeout: 1000 });

  await expect(page.getByTestId('thesis-feedback-not-useful')).toBeVisible({ timeout: 3000 });
  await expect(page.getByTestId('thesis-feedback-not-useful')).toBeDisabled();
  await expect(page.getByTestId('thesis-feedback-not-useful')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByTestId('thesis-feedback-useful')).toBeDisabled();
});

test('SC-TP-23e: editing the thesis textarea after feedback hides the control entirely', async ({ page }) => {
  await gotoTradePlanForAi(page, { improveWithAi: true });

  await page.getByTestId('improve-with-ai-btn').click();
  await expect(page.getByTestId('thesis-feedback-useful')).toBeVisible({ timeout: 5000 });
  await page.getByTestId('thesis-feedback-useful').click();
  await expect(page.getByTestId('thesis-feedback-confirmation')).toBeVisible({ timeout: 1000 });

  await page.getByTestId('setup-thesis-textarea').click();
  await page.keyboard.press('End');
  await page.keyboard.type(' edited by trader');

  await expect(page.getByTestId('thesis-feedback-control')).toHaveCount(0);
  await expect(page.getByTestId('ai-draft-badge')).not.toBeVisible();
});

test('SC-TP-23f: thesis_feedback is included in the save payload once feedback is given', async ({ page }) => {
  await gotoTradePlanForAi(page, { improveWithAi: true });

  let savedPayload = null;
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      savedPayload = route.request().postDataJSON();
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(TRADE_PLAN_SAVED) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
  });

  await page.getByTestId('improve-with-ai-btn').click();
  await expect(page.getByTestId('thesis-feedback-useful')).toBeVisible({ timeout: 5000 });
  await page.getByTestId('thesis-feedback-useful').click();
  await expect(page.getByTestId('thesis-feedback-confirmation')).toBeVisible({ timeout: 1000 });

  await page.getByRole('button', { name: /save plan/i }).click();
  await expect(page.locator('[class*="emerald"]').filter({ hasText: /saved successfully/i })).toBeVisible({ timeout: 8000 });

  expect(savedPayload.thesis_feedback).toBe('useful');
});

// ST-07 (BLG-FE-143, EPIC-03, v8.5) — thesis_model_version/thesis_prompt_version
// AC-01: AI-generated content (Improve with AI, the real Claude path) has both
// fields populated in the save payload. AC-02: manually-typed or user-edited
// content leaves both fields null -- covers the client-side-template path
// (never AI) and the edit-after-AI path (no longer purely AI-generated).

test('SC-TP-24a: "Improve with AI" (Claude) populates thesis_model_version/thesis_prompt_version in the save payload', async ({ page }) => {
  await gotoTradePlanForAi(page, { improveWithAi: true });

  let savedPayload = null;
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      savedPayload = route.request().postDataJSON();
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(TRADE_PLAN_SAVED) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
  });

  await page.getByTestId('improve-with-ai-btn').click();
  await expect(page.getByTestId('thesis-feedback-control')).toBeVisible({ timeout: 5000 });

  await page.getByRole('button', { name: /save plan/i }).click();
  await expect(page.locator('[class*="emerald"]').filter({ hasText: /saved successfully/i })).toBeVisible({ timeout: 8000 });

  expect(savedPayload.thesis_model_version).toBe('claude-haiku-4-5');
  expect(savedPayload.thesis_prompt_version).toBe('v3.0');
});

test('SC-TP-24b: template-only "Generate thesis" (not Claude) leaves thesis_model_version/thesis_prompt_version null', async ({ page }) => {
  await gotoTradePlanForAi(page);

  let savedPayload = null;
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      savedPayload = route.request().postDataJSON();
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(TRADE_PLAN_SAVED) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
  });

  await page.getByTestId('generate-thesis-btn').click();
  await expect(page.getByTestId('ai-draft-badge')).toBeVisible({ timeout: 3000 });

  await page.getByRole('button', { name: /save plan/i }).click();
  await expect(page.locator('[class*="emerald"]').filter({ hasText: /saved successfully/i })).toBeVisible({ timeout: 8000 });

  expect(savedPayload.thesis_model_version).toBeNull();
  expect(savedPayload.thesis_prompt_version).toBeNull();
});

test('SC-TP-24c: editing a narrative field after "Improve with AI" clears thesis_model_version/thesis_prompt_version before save', async ({ page }) => {
  await gotoTradePlanForAi(page, { improveWithAi: true });

  let savedPayload = null;
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      savedPayload = route.request().postDataJSON();
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(TRADE_PLAN_SAVED) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
  });

  await page.getByTestId('improve-with-ai-btn').click();
  await expect(page.getByTestId('thesis-feedback-control')).toBeVisible({ timeout: 5000 });

  // Manual edit to a narrative field -- content is no longer purely AI-generated.
  await page.getByTestId('setup-thesis-textarea').click();
  await page.keyboard.press('End');
  await page.keyboard.type(' edited by trader');
  await expect(page.getByTestId('ai-draft-badge')).not.toBeVisible();

  await page.getByRole('button', { name: /save plan/i }).click();
  await expect(page.locator('[class*="emerald"]').filter({ hasText: /saved successfully/i })).toBeVisible({ timeout: 8000 });

  expect(savedPayload.thesis_model_version).toBeNull();
  expect(savedPayload.thesis_prompt_version).toBeNull();
});

// ---------------------------------------------------------------------------
// SC-TP-24–27 — Trade Plan Tags (ST-05, BLG-FEAT-52, EPIC-02, v6.8)
// Design source: docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md
// ---------------------------------------------------------------------------

async function mockTradePlanTags(page, tags = []) {
  await page.route(`${API}/trade-plans/tags`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: tags }) })
  );
}

test('SC-TP-24: Tags section renders with "No tags" placeholder when plan has no tags', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanTags(page, ['momentum', 'breakout']);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  await expect(page.getByTestId('trade-plan-tags')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('trade-plan-tags')).toContainText(/no tags/i);
  await expect(page.getByTestId('trade-plan-tag-input')).toBeVisible();
});

test('SC-TP-25: Typing a tag and pressing Enter adds it as a pill', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanTags(page);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  await page.getByTestId('trade-plan-tag-input').fill('Breakout Setup');
  await page.getByTestId('trade-plan-tag-input').press('Enter');

  // Normalised: lowercase, spaces -> hyphens
  await expect(page.getByTestId('trade-plan-tags')).toContainText('breakout-setup');
  await expect(page.getByTestId('trade-plan-tag-remove-breakout-setup')).toBeVisible();
});

test('SC-TP-26: Clicking the X on a tag pill removes it', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanTags(page);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  await page.getByTestId('trade-plan-tag-input').fill('momentum');
  await page.getByTestId('trade-plan-tag-input').press('Enter');
  await expect(page.getByTestId('trade-plan-tag-remove-momentum')).toBeVisible();

  await page.getByTestId('trade-plan-tag-remove-momentum').click();

  await expect(page.getByTestId('trade-plan-tag-remove-momentum')).toHaveCount(0);
  await expect(page.getByTestId('trade-plan-tags')).toContainText(/no tags/i);
});

test('SC-TP-27: trade_tags is included in the save payload', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanTags(page);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  let savedPayload = null;
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      savedPayload = route.request().postDataJSON();
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(TRADE_PLAN_SAVED) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
  });

  await page.getByTestId('trade-plan-tag-input').fill('earnings-play');
  await page.getByTestId('trade-plan-tag-input').press('Enter');

  await page.getByRole('button', { name: /save plan/i }).click();
  await expect(page.locator('[class*="emerald"]').filter({ hasText: /saved successfully/i })).toBeVisible({ timeout: 8000 });

  expect(savedPayload.trade_tags).toEqual(['earnings-play']);
});

test('SC-TP-28: Tag suggestion is selectable via keyboard (Tab + Enter), not just mouse (EPIC-01, ST-01)', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanTags(page, ['momentum', 'breakout']);
  await gotoTradePlan(page, { ticker: 'AAPL', market: 'US' });

  const tagInput = page.getByTestId('trade-plan-tag-input');
  await tagInput.fill('mom');

  const suggestion = page.getByRole('button', { name: 'momentum', exact: true });
  await expect(suggestion).toBeVisible();

  await suggestion.focus();
  await page.keyboard.press('Enter');

  await expect(page.getByTestId('trade-plan-tags')).toContainText('momentum');
  await expect(page.getByTestId('trade-plan-tag-remove-momentum')).toBeVisible();
});
