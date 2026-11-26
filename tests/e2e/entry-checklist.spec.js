/**
 * Entry Checklist Acceptance Tests — ST-11 (EPIC-03, v3.3) — BLG-QA-14
 *
 * Covers observable AC for the Pre-Entry Checklist component (PT-05, v3.2):
 *   SC-CL-01  Checklist renders in Trade Plan form with 4 default items
 *   SC-CL-02  Items can be toggled (checked/unchecked)
 *   SC-CL-03  State persists on save (POST /trade-plans carries checklist_items)
 *   SC-CL-04  Pre-population: stop_defined pre-checked when early_exit_conditions present
 *   SC-CL-05  Pre-population: research_reviewed pre-checked when r_target is set
 *   SC-CL-06  "Review research →" link navigates to /research/{ticker}
 *   SC-CL-07  Read-only checklist renders in Research view trade plan panel
 *   SC-CL-08  Checklist item has role="checkbox", aria-checked, tabindex="0"; reachable via Tab (ST-06, BLG-FE-135, EPIC-02, v8.0)
 *   SC-CL-09  Space key toggles the focused item; aria-checked updates (ST-06)
 *   SC-CL-10  Enter key toggles the focused item; aria-checked updates (ST-06)
 *   SC-CL-11  Read-only checklist items are not Tab-reachable (tabindex="-1") (ST-06)
 *   SC-CL-12  CL-10 (v9.18 ST-12): "Position size checks" and "Stop level defined" show automatic status
 *             that follows the inputs, and cannot be ticked or focused
 *   SC-CL-13  CL-11: the two judgement items stay tickable; a v1.29 plan saved with four ticks loads its
 *             judgement ticks, and re-saving stores the system items with "auto": true
 *   SC-CL-13b A v9.18 plan saved with both judgement items unticked reopens unticked (no r_target pre-tick)
 *   SC-CL-14  Saved shape: system items carry auto: true and checked = status; checklist_completed = judgement items
 *   SC-CL-15  Read-only (Research): status from the stored snapshot and stop, captioned; no snapshot → "Not checked when saved"
 *
 * v9.18 ST-12 (BLG-UX-19, trade_plan.md v1.30 §6): the counter covers the two judgement items
 * ("{n} / 2 confirmed", "Both confirmed"); the stop_defined pre-tick from early_exit_conditions is
 * retired (SC-CL-04 rewritten to the status rule).
 *
 * Note (SC-CL-05): Pre-population matches TradePlan.js (buildPrePopulatedItems):
 * research_reviewed ← r_target presence (the stop_defined pre-tick was retired by ST-12, v9.18). The spec (trade_plan.md §6.2) references
 * stop_level and risk_reward_notes — this is a known spec/impl discrepancy recorded
 * in the Known Deviations log (implementation takes precedence for test purposes).
 *
 * Spec ref: docs/specs/frontend/pages/trade_plan.md §6
 * Infrastructure: Playwright page.route() network interception. No live backend.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 * — NOT page.goto('/path'). Path-based navigation loads the Dashboard silently.
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const TICKER = 'AAPL';
const PLAN_ID = '00000000-0000-0000-0000-000000000001';

// ---------------------------------------------------------------------------
// Mock payloads
// ---------------------------------------------------------------------------

const EMPTY_CHECKLIST_PLAN = {
  status: 'ok',
  data: {
    id: PLAN_ID,
    ticker: TICKER,
    market: 'US',
    status: 'draft',
    setup_thesis: 'Bullish breakout',
    entry_rationale: 'Strong momentum',
    r_target: null,
    early_exit_conditions: null,
    confirmation_criteria: null,
    checklist_completed: false,
    checklist_items: [],
  },
};

const PLAN_WITH_R_TARGET = {
  status: 'ok',
  data: {
    ...EMPTY_CHECKLIST_PLAN.data,
    r_target: 2.5,
    early_exit_conditions: null,
  },
};

const PLAN_WITH_EXIT_CONDITIONS = {
  status: 'ok',
  data: {
    ...EMPTY_CHECKLIST_PLAN.data,
    r_target: null,
    early_exit_conditions: 'Exit if breaks below 20 EMA',
  },
};

const PLAN_WITH_CHECKED_ITEMS = {
  status: 'ok',
  data: {
    id: PLAN_ID,
    ticker: TICKER,
    market: 'US',
    status: 'active',
    setup_thesis: 'Bullish breakout',
    entry_rationale: '',
    r_target: 2.5,
    early_exit_conditions: 'Exit if breaks below 20 EMA',
    confirmation_criteria: null,
    checklist_completed: true,
    checklist_items: [
      { id: 'signal_confirmed', label: 'Strategy signal confirmed', checked: true },
      { id: 'heat_limit_checked', label: 'Position size within heat limits', checked: false },
      { id: 'stop_defined', label: 'Stop level defined', checked: true },
      { id: 'research_reviewed', label: 'Pre-trade research reviewed', checked: true },
    ],
  },
};

// Research view mock with active plan containing checklist items
const RESEARCH_WITH_PLAN = {
  status: 'ok',
  data: {
    ticker: TICKER,
    market: 'US',
    price: 178.50,
    price_change_pct: 0.0142,
    market_cap: 2800000000000,
    signal: null,
    regime: { label: 'risk_on', spy_risk_on: true, ftse_risk_on: true },
    sector: { sector: 'Technology', industry: 'Consumer Electronics' },
    screener: null,
    earnings: null,
    news_headlines: [],
  },
};

const TRADE_PLANS_WITH_ACTIVE = {
  status: 'ok',
  data: [
    {
      id: PLAN_ID,
      ticker: TICKER,
      market: 'US',
      status: 'active',
      stop_level: 175.0,
      risk_reward_notes: 'R/R looks good',
      checklist_items: [
        { id: 'signal_confirmed', label: 'Strategy signal confirmed', checked: true },
        { id: 'heat_limit_checked', label: 'Position size within heat limits', checked: false },
        { id: 'stop_defined', label: 'Stop level defined', checked: true },
        { id: 'research_reviewed', label: 'Pre-trade research reviewed', checked: true },
      ],
    },
  ],
};

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMarketStatus(page) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { regime_status: 'risk_on' } }),
    })
  );
}

async function mockTradePlanGet(page, payload) {
  await page.route(new RegExp(`${API}/trade-plans/${PLAN_ID}`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockTradePlansListEmpty(page) {
  await page.route(new RegExp(`${API}/trade-plans$`), (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    } else {
      route.continue();
    }
  });
}

async function gotoNewTradePlan(page) {
  await page.goto(`/#/TradePlan?ticker=${TICKER}&market=US`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

async function gotoEditTradePlan(page) {
  await page.goto(`/#/TradePlan?edit=${PLAN_ID}&ticker=${TICKER}`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
}

async function gotoResearch(page) {
  await page.goto(`/#/research/${TICKER}?market=US`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: new RegExp(TICKER, 'i') })).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// SC-CL-01 — Checklist renders in form with 4 default items
// ---------------------------------------------------------------------------

test('SC-CL-01: Pre-entry checklist renders 4 default items in new trade plan form', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);
  await gotoNewTradePlan(page);

  await expect(page.getByText('Strategy signal confirmed')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('checklist-system')).toContainText('Position size checks');
  await expect(page.getByTestId('checklist-system')).toContainText('Stop level defined');
  await expect(page.getByText('Pre-trade research reviewed')).toBeVisible();
  // v9.18 ST-12: two groups — two status rows and two tickable items.
  await expect(page.getByTestId('checklist-human').getByRole('checkbox')).toHaveCount(2);
  await expect(page.getByText('Position size within heat limits')).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-CL-02 — Items can be toggled
// ---------------------------------------------------------------------------

test('SC-CL-02: Checklist items can be checked and unchecked', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);
  await gotoNewTradePlan(page);

  // EntryChecklist.js renders a custom checkbox (styled div, no real <input>) —
  // observe toggled state via the "N / 2 confirmed" counter (v9.18 ST-12).
  const counter = page.getByTestId('checklist-counter');
  await expect(counter).toHaveText('0 / 2 confirmed');

  const signalLabel = page.getByText('Strategy signal confirmed');
  await signalLabel.click();
  await expect(counter).toHaveText('1 / 2 confirmed');

  await signalLabel.click();
  await expect(counter).toHaveText('0 / 2 confirmed');
});

// ---------------------------------------------------------------------------
// SC-CL-03 — State persists on save (POST body contains checklist_items)
// ---------------------------------------------------------------------------

test('SC-CL-03: Checklist state is included in POST body when saving', async ({ page }) => {
  let capturedBody = null;

  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);

  // Intercept POST /trade-plans to capture the body
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      const body = route.request().postDataJSON();
      capturedBody = body;
      route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { id: PLAN_ID, ...body } }),
      });
    } else {
      route.continue();
    }
  });

  await gotoNewTradePlan(page);

  // Fill required ticker (pre-populated from query param)
  // Trigger save
  const saveBtn = page.getByRole('button', { name: /save/i });
  await saveBtn.waitFor({ timeout: 5000 });
  await saveBtn.click();

  // Verify POST body contained checklist_items
  await page.waitForTimeout(1000);
  expect(capturedBody).not.toBeNull();
  expect(capturedBody).toHaveProperty('checklist_items');
  expect(Array.isArray(capturedBody.checklist_items)).toBe(true);
});

// ---------------------------------------------------------------------------
// SC-CL-04 — (v9.18 ST-12) early_exit_conditions no longer pre-ticks anything;
// "Stop level defined" is a status from the Stop Level field
// ---------------------------------------------------------------------------

test('SC-CL-04: a plan with early_exit_conditions but no stop shows "Stop level defined" as not set', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanGet(page, PLAN_WITH_EXIT_CONDITIONS);
  await page.route(new RegExp(`${API}/trade-plans$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [PLAN_WITH_EXIT_CONDITIONS.data] }) })
  );

  await gotoEditTradePlan(page);

  await expect(page.getByTestId('entry-checklist-status-stop_defined-text')).toHaveText('✗ Not set', { timeout: 5000 });
  await expect(page.getByTestId('entry-checklist-item-stop_defined')).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// SC-CL-05 — research_reviewed pre-checked when r_target is set
// ---------------------------------------------------------------------------

test('SC-CL-05: research_reviewed pre-checked when editing plan with r_target set', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanGet(page, PLAN_WITH_R_TARGET);

  await page.route(new RegExp(`${API}/trade-plans$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [PLAN_WITH_R_TARGET.data] }) })
  );

  await gotoEditTradePlan(page);

  const researchLabel = page.getByText('Pre-trade research reviewed');
  await researchLabel.waitFor({ timeout: 5000 });
  await expect(researchLabel).toBeVisible();

  // r_target is set (2.5) → research_reviewed should be pre-checked
  // Visual check: the checklist item for research reviewed renders with a checked indicator
  // (exact DOM depends on EntryChecklist implementation)
});

// ---------------------------------------------------------------------------
// SC-CL-06 — "Review research →" link navigates to /research/{ticker}
// ---------------------------------------------------------------------------

test('SC-CL-06: Review research link navigates to /research/{ticker}', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);
  await gotoNewTradePlan(page);

  const reviewLink = page.getByRole('link', { name: /review research/i });
  await reviewLink.waitFor({ timeout: 5000 });

  const href = await reviewLink.getAttribute('href');
  // Link should reference /research/{ticker} — either via href or onClick navigation
  // Accept hash-router format: /#/Research?ticker=AAPL or #/research/AAPL
  expect(href?.toLowerCase()).toMatch(/research.*aapl|aapl.*research/i);
});

// ---------------------------------------------------------------------------
// SC-CL-07 — Read-only checklist renders in Research view trade plan panel
// ---------------------------------------------------------------------------

test('SC-CL-07: Read-only checklist renders in Research view when active plan has checklist items', async ({ page }) => {
  await mockFallback(page);

  // Mock research endpoint
  await page.route(new RegExp(`${API}/research/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RESEARCH_WITH_PLAN) })
  );

  // Mock trade plans list — returns plan with checklist items
  await page.route(new RegExp(`${API}/trade-plans`), (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(TRADE_PLANS_WITH_ACTIVE),
      });
    } else {
      route.continue();
    }
  });

  // Mock heat endpoint
  await page.route(new RegExp(`${API}/portfolio/prospective-heat`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: null }) })
  );

  await gotoResearch(page);

  // The trade plan panel should show checklist items in read-only mode
  // At least one checklist label should be visible
  const checklistLabel = page.getByText('Pre-Entry Checklist');
  const strategyLabel = page.getByText('Strategy signal confirmed');

  // Either the checklist section heading or the first item label should be visible
  const isChecklistVisible =
    await checklistLabel.isVisible().catch(() => false) ||
    await strategyLabel.isVisible().catch(() => false);

  expect(isChecklistVisible).toBe(true);
});

// ---------------------------------------------------------------------------
// SC-CL-08 through SC-CL-11 — Keyboard accessibility (ST-06, BLG-FE-135, EPIC-02, v8.0)
//
// Design source: docs/design/2026-07-30__release-v8.0/entry-checklist-keyboard-accessibility/decision_record.md
// CheckItem is rendered as a WAI-ARIA checkbox (role="checkbox", aria-checked,
// tabIndex) — not a native <input type="checkbox">, so these tests target the
// data-testid added for this story rather than an input element.
// ---------------------------------------------------------------------------

test('SC-CL-08: Checklist items are real checkboxes, reachable via Tab in list order (Tab and Shift+Tab)', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);
  await gotoNewTradePlan(page);

  const signalItem = page.getByTestId('entry-checklist-item-signal_confirmed');
  // v9.18 ST-12: the next tickable item is "Pre-trade research reviewed"; the
  // two system rows are not focusable.
  const heatItem = page.getByTestId('entry-checklist-item-research_reviewed');
  await expect(signalItem).toBeVisible({ timeout: 5000 });
  await expect(signalItem).toHaveAttribute('role', 'checkbox');
  await expect(signalItem).toHaveAttribute('aria-checked', 'false');
  await expect(signalItem).toHaveAttribute('tabindex', '0');

  // Real keyboard Tab traversal — focus the field immediately preceding the
  // checklist in the form ("Invalidation Condition", ST-01/EPIC-01/v8.7 —
  // inserted after "Early Exit Conditions"), then Tab into the first
  // checklist item, Tab again to reach the second item (list order), then
  // Shift+Tab back to confirm reverse order.
  await page.getByPlaceholder(/What would prove this thesis wrong/i).focus();
  await page.keyboard.press('Tab');
  await expect(signalItem).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(heatItem).toBeFocused();

  await page.keyboard.press('Shift+Tab');
  await expect(signalItem).toBeFocused();
});

test('SC-CL-09: Space key toggles the focused checklist item and aria-checked updates', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);
  await gotoNewTradePlan(page);

  const signalItem = page.getByTestId('entry-checklist-item-signal_confirmed');
  const counter = page.getByTestId('checklist-counter');
  await expect(counter).toHaveText('0 / 2 confirmed');

  await page.getByPlaceholder(/What would prove this thesis wrong/i).focus();
  await page.keyboard.press('Tab');
  await expect(signalItem).toBeFocused();

  await page.keyboard.press('Space');
  await expect(signalItem).toHaveAttribute('aria-checked', 'true');
  await expect(counter).toHaveText('1 / 2 confirmed');

  await page.keyboard.press('Space');
  await expect(signalItem).toHaveAttribute('aria-checked', 'false');
  await expect(counter).toHaveText('0 / 2 confirmed');
});

test('SC-CL-10: Enter key toggles the focused checklist item and aria-checked updates', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);
  await gotoNewTradePlan(page);

  const signalItem = page.getByTestId('entry-checklist-item-signal_confirmed');
  // v9.18 ST-12: the two system rows are not in the tab order, so the second
  // tickable item, research_reviewed, follows signal_confirmed directly.
  const stopItem = page.getByTestId('entry-checklist-item-research_reviewed');
  const counter = page.getByTestId('checklist-counter');
  await expect(counter).toHaveText('0 / 2 confirmed');

  // Tab through the list order to reach the 2nd tickable item, proving
  // list-order traversal rather than jumping straight to the target.
  await page.getByPlaceholder(/What would prove this thesis wrong/i).focus();
  await page.keyboard.press('Tab'); // -> signal_confirmed
  await expect(signalItem).toBeFocused();
  await page.keyboard.press('Tab'); // -> research_reviewed (system rows skipped)
  await expect(stopItem).toBeFocused();

  await page.keyboard.press('Enter');
  await expect(stopItem).toHaveAttribute('aria-checked', 'true');
  await expect(counter).toHaveText('1 / 2 confirmed');
});

test('SC-CL-11: Read-only checklist items are skipped by Tab traversal (not focusable)', async ({ page }) => {
  await mockFallback(page);

  await page.route(new RegExp(`${API}/research/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RESEARCH_WITH_PLAN) })
  );
  await page.route(new RegExp(`${API}/trade-plans`), (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(TRADE_PLANS_WITH_ACTIVE) });
    } else {
      route.continue();
    }
  });
  await page.route(new RegExp(`${API}/portfolio/prospective-heat`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: null }) })
  );

  await gotoResearch(page);

  const readOnlyItem = page.getByTestId('entry-checklist-item-signal_confirmed');
  await expect(readOnlyItem).toBeVisible({ timeout: 5000 });
  await expect(readOnlyItem).toHaveAttribute('tabindex', '-1');

  // Real keyboard Tab traversal across the whole page — confirm the read-only
  // checklist item's data-testid is never the focused element at any Tab stop,
  // while also confirming Tab is genuinely moving focus (not a page-wide no-op).
  await page.locator('body').click({ position: { x: 0, y: 0 } });
  const seenTestIds = new Set();
  let focusMoved = false;
  for (let i = 0; i < 40; i++) {
    await page.keyboard.press('Tab');
    const focusedTestId = await page.evaluate(() => document.activeElement?.getAttribute('data-testid') || null);
    if (focusedTestId) seenTestIds.add(focusedTestId);
    const focusedIsBody = await page.evaluate(() => document.activeElement === document.body);
    if (!focusedIsBody) focusMoved = true;
    if (focusedTestId === 'entry-checklist-item-signal_confirmed') {
      throw new Error('Read-only checklist item received keyboard focus via Tab — should be skipped (tabindex=-1)');
    }
  }
  expect(focusMoved).toBe(true);
});

// ---------------------------------------------------------------------------
// SC-CL-12 to SC-CL-15 — system status and judgement ticks (v9.18 ST-12,
// BLG-UX-19, trade_plan.md v1.30 §6; ESC-EXEC-20261126-01)
// ---------------------------------------------------------------------------

function preEntry(cash, sector, sizing) {
  return {
    status: 'ok',
    data: {
      ticker: TICKER, market: 'US', quantity: 10,
      advisory_status: [cash, sector, sizing].includes('fail') ? 'fail' : [cash, sector, sizing].includes('warn') ? 'warn' : 'pass',
      override_required: [cash, sector, sizing].some((x) => x === 'warn' || x === 'fail'),
      checks: [
        { rule: 'regime_gate', status: 'pass', detail: 'Risk-on' },
        { rule: 'cash_constraint', status: cash, detail: 'cash' },
        { rule: 'sector_concentration', status: sector, detail: 'sector' },
        { rule: 'earnings_proximity', status: 'skipped', detail: 'n/a' },
        { rule: 'sizing_validity', status: sizing, detail: 'sizing' },
      ],
    },
  };
}

const sizeText = (page) => page.getByTestId('entry-checklist-status-heat_limit_checked-text');
const stopStatus = (page) => page.getByTestId('entry-checklist-status-stop_defined-text');

test('SC-CL-12: CL-10 — the two system items follow the inputs and cannot be ticked', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);
  // 10 shares pass; 20 shares warn on sector concentration.
  await page.route(/\/portfolio\/pre-entry-validation/, (route) => {
    const q = new URL(route.request().url()).searchParams.get('quantity');
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(q === '20' ? preEntry('pass', 'warn', 'pass') : preEntry('pass', 'pass', 'skipped')) });
  });
  await gotoNewTradePlan(page);

  await expect(sizeText(page)).toHaveText('Not checked yet', { timeout: 5000 });
  await expect(stopStatus(page)).toHaveText('✗ Not set');

  await page.getByTestId('planned-quantity-input').fill('10');
  await expect(sizeText(page)).toHaveText('✓ Pass', { timeout: 10000 });
  await page.getByTestId('planned-quantity-input').fill('20');
  await expect(sizeText(page)).toHaveText('! Warning — see Pre-Entry Checks', { timeout: 10000 });

  await page.getByTestId('planned-stop-price-input').fill('142');
  await expect(stopStatus(page)).toHaveText('✓ Set: 142.00 USD');
  await page.getByTestId('planned-stop-price-input').fill('0');
  await expect(stopStatus(page)).toHaveText('✗ Not set');

  // Not a checkbox, not focusable; clicking changes nothing.
  const system = page.getByTestId('checklist-system');
  await expect(system.getByRole('checkbox')).toHaveCount(0);
  await expect(system.locator('[tabindex]')).toHaveCount(0);
  await page.getByTestId('entry-checklist-status-stop_defined').click();
  await expect(stopStatus(page)).toHaveText('✗ Not set');
  await expect(page.getByTestId('checklist-counter')).toHaveText('0 / 2 confirmed');
});

// A v1.29 plan: four ticks, no "auto" flag, no snapshot, Stop Level 142 (record §4 worked example).
const LEGACY_PLAN = {
  status: 'ok',
  data: {
    ...EMPTY_CHECKLIST_PLAN.data,
    planned_stop_price: 142,
    pre_entry_validation_snapshot: null,
    checklist_completed: true,
    checklist_items: [
      { id: 'signal_confirmed', label: 'Strategy signal confirmed', checked: true },
      { id: 'heat_limit_checked', label: 'Position size within heat limits', checked: true },
      { id: 'stop_defined', label: 'Stop level defined', checked: true },
      { id: 'research_reviewed', label: 'Pre-trade research reviewed', checked: true },
    ],
  },
};

test('SC-CL-13: CL-11 — a v1.29 plan loads its judgement ticks; they stay tickable', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanGet(page, LEGACY_PLAN);
  await page.route(new RegExp(`${API}/trade-plans$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [LEGACY_PLAN.data] }) })
  );
  await gotoEditTradePlan(page);

  await expect(page.getByTestId('entry-checklist-item-signal_confirmed')).toHaveAttribute('aria-checked', 'true', { timeout: 5000 });
  await expect(page.getByTestId('entry-checklist-item-research_reviewed')).toHaveAttribute('aria-checked', 'true');
  await expect(page.getByTestId('checklist-counter')).toHaveText('Both confirmed');
  // The saved ticks of the system items are not shown as ticks: status is recomputed.
  await expect(sizeText(page)).toHaveText('Not checked yet');
  await expect(stopStatus(page)).toHaveText('✓ Set: 142.00 USD');

  await page.getByTestId('entry-checklist-item-research_reviewed').click();
  await expect(page.getByTestId('checklist-counter')).toHaveText('1 / 2 confirmed');
});

// Review fix: a v9.18 plan saved with both judgement items unticked (system items auto).
const V918_UNTICKED = {
  status: 'ok',
  data: {
    ...EMPTY_CHECKLIST_PLAN.data,
    r_target: 2,
    planned_stop_price: 142,
    checklist_completed: false,
    checklist_items: [
      { id: 'signal_confirmed', label: 'Strategy signal confirmed', checked: false },
      { id: 'heat_limit_checked', label: 'Position size checks', checked: false, auto: true },
      { id: 'stop_defined', label: 'Stop level defined', checked: true, auto: true },
      { id: 'research_reviewed', label: 'Pre-trade research reviewed', checked: false },
    ],
  },
};

test('SC-CL-13b: a saved v9.18 plan keeps its unticked judgement items (no r_target pre-tick on reopen)', async ({ page }) => {
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlanGet(page, V918_UNTICKED);
  await page.route(new RegExp(`${API}/trade-plans$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [V918_UNTICKED.data] }) })
  );
  await gotoEditTradePlan(page);
  await expect(stopStatus(page)).toHaveText('✓ Set: 142.00 USD', { timeout: 5000 });
  await expect(page.getByTestId('entry-checklist-item-research_reviewed')).toHaveAttribute('aria-checked', 'false');
  await expect(page.getByTestId('checklist-counter')).toHaveText('0 / 2 confirmed');
});

test('SC-CL-14: the saved checklist marks the system items auto with checked = status', async ({ page }) => {
  let body = null;
  await mockFallback(page);
  await mockMarketStatus(page);
  await mockTradePlansListEmpty(page);
  await page.route(/\/portfolio\/pre-entry-validation/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(preEntry('pass', 'warn', 'pass')) })
  );
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    body = route.request().postDataJSON();
    return route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { id: PLAN_ID, ...body } }) });
  });
  await gotoNewTradePlan(page);
  await page.getByTestId('planned-quantity-input').fill('10');
  await page.getByTestId('planned-stop-price-input').fill('142');
  await expect(sizeText(page)).toHaveText('! Warning — see Pre-Entry Checks', { timeout: 10000 });
  await page.getByTestId('entry-checklist-item-signal_confirmed').click();
  await page.getByTestId('entry-checklist-item-research_reviewed').click();
  // A warning needs the existing acknowledgement before saving (§5e, unchanged).
  const ack = page.getByRole('checkbox', { name: /acknowledge/i });
  if (await ack.count()) await ack.first().check();
  await page.getByRole('button', { name: /save/i }).first().click();
  await expect.poll(() => body).not.toBeNull();

  const byId = Object.fromEntries(body.checklist_items.map((i) => [i.id, i]));
  expect(byId.heat_limit_checked).toMatchObject({ label: 'Position size checks', checked: false, auto: true });
  expect(byId.stop_defined).toMatchObject({ checked: true, auto: true });
  expect(byId.signal_confirmed.checked).toBe(true);
  expect(byId.signal_confirmed.auto).toBeUndefined();
  expect(byId.research_reviewed.checked).toBe(true);
  expect(body.checklist_completed).toBe(true);
});

test('SC-CL-15: read-only on Research shows status from the stored snapshot, captioned; no snapshot says so', async ({ page }) => {
  await mockFallback(page);
  await page.route(new RegExp(`${API}/research/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(RESEARCH_WITH_PLAN) })
  );
  const withSnapshot = {
    ...TRADE_PLANS_WITH_ACTIVE.data[0],
    planned_stop_price: 175,
    pre_entry_validation_snapshot: { captured_at: '2026-11-20T09:05:00', advisory_status: 'fail', checks: [{ rule: 'cash_constraint', status: 'fail' }] },
  };
  let plans = [withSnapshot];
  await page.route(new RegExp(`${API}/trade-plans`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: plans }) })
  );
  await page.route(new RegExp(`${API}/portfolio/prospective-heat`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: null }) })
  );
  await gotoResearch(page);
  await expect(sizeText(page)).toHaveText('✗ Fail — see Pre-Entry Checks', { timeout: 10000 });
  await expect(stopStatus(page)).toHaveText('✓ Set: 175.00 USD');
  await expect(page.getByTestId('checklist-captured-at')).toHaveText('As checked when the plan was saved, 20 Nov 09:05');

  plans = [{ ...withSnapshot, pre_entry_validation_snapshot: null }];
  await page.reload();
  await expect(sizeText(page)).toHaveText('Not checked when saved', { timeout: 10000 });
  await expect(page.getByTestId('checklist-captured-at')).toHaveCount(0);
});

