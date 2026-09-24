/**
 * Clone as New Plan — Trade Plans list + form (ST-01, EPIC-01, v9.6, BLG-FEAT-96)
 *
 * Design source: docs/design/2026-09-21__release-v9.6/trade-plan-clone/decision_record.md §5
 * Spec: docs/specs/frontend/pages/trade_plan.md v1.16 §4.5
 *
 * Covers observable AC (ST-01 AC-01, AC-02, AC-03):
 *   SC-TPC-01  Clone link is present on every list row regardless of status (incl. abandoned/closed)
 *   SC-TPC-02  Clicking Clone opens a new, unsaved plan pre-populated from the source, with the banner
 *   SC-TPC-03  Copy/reset table: price levels, position link and checklist completion are NOT carried over
 *   SC-TPC-04  Nothing is persisted until Save; the saved payload is a fresh `draft` with no id/position_id
 *   SC-TPC-05  Detail view (edit mode) header shows Clone, including for an abandoned plan
 *   SC-TPC-06  Source load failure opens a blank form and shows the warning toast
 *
 * v9.7 ST-02 (EPIC-02, BLG-FE-186) — Setup Type is Copied (trade_plan.md v1.16 §4.5); a copied
 * value always wins over the watchlisted-signal auto-fill default:
 *   SC-TPC-07  Clone of a plan with a Setup Type keeps it when the ticker also has a watchlisted signal
 *   SC-TPC-08  Clone of a plan with no Setup Type still gets the watchlisted-signal auto-fill (nothing to protect)
 *   SC-TPC-09  Clone keeps the source Setup Type when the ticker has no watchlisted signal
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 * Route note: the app's page-name route is /TradePlan?clone_from={id}; the spec's
 * /trade-plans/new?clone_from={id} is the same destination under the spec's idealised route names.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const SRC_ID = '11111111-1111-1111-1111-111111111111';
const POSITION_ID = '22222222-2222-2222-2222-222222222222';

const SOURCE_PLAN = {
  id: SRC_ID,
  ticker: 'NVDA',
  market: 'US',
  status: 'active',
  position_id: POSITION_ID,
  setup_type: 'Breakout',
  setup_thesis: 'Base breakout on rising volume',
  entry_rationale: 'Close above pivot',
  invalidation_condition: 'Close back below the base low',
  r_target: 3,
  planned_quantity: 40,
  planned_entry_price: 121.5,
  planned_stop_price: 115.25,
  trade_tags: ['breakout', 'momentum'],
  checklist_completed: true,
  checklist_items: [
    { id: 'signal_confirmed', label: 'Strategy signal confirmed', checked: true },
    { id: 'heat_limit_checked', label: 'Position size within heat limits', checked: true },
    { id: 'stop_defined', label: 'Stop level defined', checked: true },
    { id: 'research_reviewed', label: 'Pre-trade research reviewed', checked: true },
  ],
  created_at: '2026-08-03T09:00:00Z',
  updated_at: '2026-09-15T09:00:00Z',
};

const json = (data) => ({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data }) });

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json([])));
}

/** Registers the source-plan detail read and records any POST to /trade-plans. */
async function mockApi(page, { plans = [SOURCE_PLAN], detail = SOURCE_PLAN } = {}) {
  const posts = [];
  await page.route(`${API}/market/status`, (route) => route.fulfill(json({ regime_status: 'risk_on' })));
  await page.route(`${API}/trade-plans/tags`, (route) => route.fulfill(json(['breakout', 'momentum'])));
  await page.route(`${API}/trade-plans`, (route) => {
    if (route.request().method() === 'POST') {
      posts.push(JSON.parse(route.request().postData() || '{}'));
      return route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { id: 'new-id' } }) });
    }
    return route.fulfill(json(plans));
  });
  await page.route(new RegExp(`${API}/trade-plans/${SRC_ID}$`), (route) => {
    if (detail === null) return route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ status: 'error', error: { code: 'NOT_FOUND' } }) });
    return route.fulfill(json(detail));
  });
  return posts;
}

test('SC-TPC-01: Clone link is present on every row, including abandoned and closed plans', async ({ page }) => {
  await mockFallback(page);
  const plans = ['draft', 'active', 'closed', 'abandoned'].map((status, i) => ({
    ...SOURCE_PLAN, id: `plan-${status}`, ticker: `T${i}`, status, position_id: null,
  }));
  await mockApi(page, { plans });
  await page.goto('/#/TradePlans');
  for (const [i, status] of ['draft', 'active', 'closed', 'abandoned'].entries()) {
    const clone = page.getByTestId(`clone-plan-plan-${status}`);
    await expect(clone).toBeVisible({ timeout: 10000 });
    await expect(clone).toHaveAttribute('aria-label', `Clone T${i} plan`);
  }
});

test('SC-TPC-02: Clicking Clone opens a new unsaved plan pre-populated from the source, with the banner', async ({ page }) => {
  await mockFallback(page);
  await mockApi(page);
  await page.goto('/#/TradePlans');
  await page.getByTestId(`clone-plan-${SRC_ID}`).click();

  await expect(page).toHaveURL(new RegExp(`#/TradePlan\\?clone_from=${SRC_ID}`));
  await expect(page.getByPlaceholder(/describe the setup/i)).toHaveValue('Base breakout on rising volume', { timeout: 10000 });
  await expect(page.getByPlaceholder(/what would prove this thesis wrong/i)).toHaveValue('Close back below the base low');
  await expect(page.getByPlaceholder(/e\.g\. 2\.5/i)).toHaveValue('3');
  await expect(page.getByPlaceholder(/e\.g\. AAPL/i)).toHaveValue('NVDA');
  await expect(page.getByText('breakout', { exact: true })).toBeVisible();
  await expect(page.getByText('momentum', { exact: true })).toBeVisible();

  const banner = page.getByTestId('clone-banner');
  await expect(banner).toBeVisible();
  await expect(banner).toContainText('Cloned from NVDA plan (3 Aug 2026)');
  await expect(banner).toContainText('Nothing is saved until you click Save Plan.');
  // Non-dismissible per the design record
  await expect(banner.getByTestId('standing-alert-dismiss')).toHaveCount(0);
});

test('SC-TPC-03: Price levels, position link and checklist completion are not carried over', async ({ page }) => {
  await mockFallback(page);
  await mockApi(page);
  await page.goto(`/#/TradePlan?clone_from=${SRC_ID}`);
  await expect(page.getByTestId('clone-banner')).toBeVisible({ timeout: 10000 });

  await expect(page.getByPlaceholder(/e\.g\. 150\.00/i)).toHaveValue('');
  await expect(page.getByPlaceholder(/e\.g\. 142\.00/i)).toHaveValue('');
  await expect(page.getByPlaceholder(/e\.g\. 50/i)).toHaveValue('');
  // Checklist template kept, completion reset
  for (const id of ['signal_confirmed', 'heat_limit_checked', 'stop_defined', 'research_reviewed']) {
    await expect(page.getByTestId(`entry-checklist-item-${id}`)).toHaveAttribute('aria-checked', 'false');
  }
  // Status starts as Draft (there is no "planned" status)
  await expect(page.getByText('Draft', { exact: true }).first()).toBeVisible();
});

test('SC-TPC-04: Nothing is persisted until Save; the saved clone is a fresh draft with no id or position_id', async ({ page }) => {
  await mockFallback(page);
  const posts = await mockApi(page);
  await page.goto(`/#/TradePlan?clone_from=${SRC_ID}`);
  await expect(page.getByTestId('clone-banner')).toBeVisible({ timeout: 10000 });
  expect(posts).toHaveLength(0); // opening the clone persists nothing

  await page.getByRole('button', { name: /save plan/i }).click();
  await expect.poll(() => posts.length, { timeout: 10000 }).toBe(1);

  const body = posts[0];
  expect(body.ticker).toBe('NVDA');
  expect(body.status).toBe('draft');
  expect(body.position_id).toBeNull();
  expect(body.id).toBeUndefined();
  expect(body.created_at).toBeUndefined();
  expect(body.updated_at).toBeUndefined();
  expect(body.planned_entry_price).toBeNull();
  expect(body.planned_stop_price).toBeNull();
  expect(body.setup_thesis).toBe('Base breakout on rising volume');
  expect(body.r_target).toBe(3);
  expect(body.checklist_items.every((i) => i.checked === false)).toBe(true);
  expect(body.checklist_completed).toBe(false);
});

test('SC-TPC-05: Detail (edit) header shows Clone, including for an abandoned plan', async ({ page }) => {
  await mockFallback(page);
  await mockApi(page, { detail: { ...SOURCE_PLAN, status: 'abandoned', abandonment_reason: 'Setup failed before entry' } });
  await page.goto(`/#/TradePlan?edit=${SRC_ID}&ticker=NVDA&market=US`);
  const btn = page.getByTestId('clone-plan-btn');
  await expect(btn).toBeVisible({ timeout: 10000 });
  await expect(btn).toHaveAttribute('aria-label', 'Clone NVDA plan');
  await btn.click();
  await expect(page).toHaveURL(new RegExp(`#/TradePlan\\?clone_from=${SRC_ID}`));
  await expect(page.getByTestId('clone-banner')).toBeVisible({ timeout: 10000 });
});

test('SC-TPC-06: A source that cannot be loaded opens a blank form with a warning toast', async ({ page }) => {
  await mockFallback(page);
  await mockApi(page, { detail: null });
  await page.goto(`/#/TradePlan?clone_from=${SRC_ID}`);
  await expect(page.getByText("Couldn't load that plan to clone. Starting a blank plan.")).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('clone-banner')).toHaveCount(0);
  await expect(page.getByPlaceholder(/describe the setup/i)).toHaveValue('');
  await expect(page.getByPlaceholder(/e\.g\. AAPL/i)).toHaveValue('');
});

// ---------------------------------------------------------------------------
// v9.7 ST-02 (BLG-FE-186) — Setup Type on clone
// Design source: docs/design/2026-09-23__release-v9.7/trade-plan-clone-setup-type/decision_record.md §5
// ---------------------------------------------------------------------------

const WATCHLISTED_NVDA_SIGNAL = {
  ticker: 'NVDA',
  market: 'US',
  rank: 3,
  regime: 'on',
  momentum_percent: 12.5,
  price_vs_50d_ma: 4.2,
  current_price: 120,
  atr_value: 2,
  initial_stop: 110,
};

/** Registers the watchlisted-signals read the form's auto-fill (linkedSignal) depends on. */
async function mockWatchlistedSignals(page, signals) {
  await page.route(/\/signals\?status=watchlisted/, (route) => route.fulfill(json(signals)));
}

test('SC-TPC-07: Clone keeps the source Setup Type when the ticker also has a watchlisted signal', async ({ page }) => {
  await mockFallback(page);
  await mockApi(page, { detail: { ...SOURCE_PLAN, setup_type: 'Breakout' } });
  await mockWatchlistedSignals(page, [WATCHLISTED_NVDA_SIGNAL]);
  await page.goto(`/#/TradePlan?clone_from=${SRC_ID}`);
  await expect(page.getByTestId('clone-banner')).toBeVisible({ timeout: 10000 });
  await expect(page.getByPlaceholder(/e\.g\. AAPL/i)).toHaveValue('NVDA');
  // Wait until the auto-fill has demonstrably run: it fills the empty Entry Rationale-derived
  // signal context panel for the linked ticker. Then assert the copied value was not overwritten.
  await expect(page.getByTestId('setup-type-select')).toHaveValue('Breakout');
  // Guard against a late overwrite (the auto-fill effect fires after the watchlist read resolves).
  await page.waitForTimeout(1000);
  await expect(page.getByTestId('setup-type-select')).toHaveValue('Breakout');
});

test('SC-TPC-08: Clone of a plan with no Setup Type still gets the watchlisted-signal auto-fill', async ({ page }) => {
  await mockFallback(page);
  await mockApi(page, { detail: { ...SOURCE_PLAN, setup_type: null } });
  await mockWatchlistedSignals(page, [WATCHLISTED_NVDA_SIGNAL]);
  await page.goto(`/#/TradePlan?clone_from=${SRC_ID}`);
  await expect(page.getByTestId('clone-banner')).toBeVisible({ timeout: 10000 });
  // No copied value to protect, so the existing auto-fill default applies (decision record §5, second case).
  await expect(page.getByTestId('setup-type-select')).toHaveValue('Momentum Continuation', { timeout: 10000 });
});

test('SC-TPC-09: Clone keeps the source Setup Type when the ticker has no watchlisted signal', async ({ page }) => {
  await mockFallback(page);
  await mockApi(page, { detail: { ...SOURCE_PLAN, setup_type: 'Pullback to MA' } });
  await mockWatchlistedSignals(page, []);
  await page.goto(`/#/TradePlan?clone_from=${SRC_ID}`);
  await expect(page.getByTestId('clone-banner')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('setup-type-select')).toHaveValue('Pullback to MA');
});
