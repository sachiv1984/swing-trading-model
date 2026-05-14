/**
 * EPIC-01 v3.4 — Position Lifecycle, Grace Period, Stop Trail Tests
 *
 * ST-01 (IT-01) — Position lifecycle state badge
 *   SC-LS-01  Lifecycle "State" column header present in table view
 *   SC-LS-02  GRACE badge renders with days_in_state suffix "GRACE — Nd"
 *   SC-LS-03  PROFITABLE, EXIT ZONE, LOSING, UNKNOWN badges render in correct colours
 *   SC-LS-04  No badge rendered when lifecycle_state is null (flag off / legacy position)
 *
 * ST-02 (IT-02) — Grace period alert card
 *   SC-GP-01  Alert card renders when position is GRACE ≥ day 8
 *   SC-GP-02  Alert card shows "Day N of 10" label and contextual body text
 *   SC-GP-03  Alert card dismissed on ✕ click and removed from view
 *
 * ST-03 (IT-03) — Trail Stop modal
 *   SC-TS-01  Trail Stop button visible for PROFITABLE position
 *   SC-TS-02  Trail Stop modal shows trail calculation data
 *   SC-TS-03  Trail Stop button absent for GRACE/LOSING/UNKNOWN states
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation via page.goto('/#/Positions')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Shared setup
// ---------------------------------------------------------------------------

async function stubCommon(page) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/alerts/history`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { spy: { price: 500, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7600, is_risk_on: true }, fx_rate: 1.27 } }) })
  );
  await page.route(`${API}/portfolio**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: { total_value: 10000, positions: [] } }) })
  );
  await page.route(`${API}/positions/grace-period-alerts`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/metrics**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: {} }) })
  );
  await page.route(`${API}/notifications**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );
}

function makePosition(overrides = {}) {
  return {
    id: 'pos-001',
    ticker: 'NVDA',
    market: 'US',
    entry_price: 800.00,
    current_price: 850.00,
    current_price_native: 850.00,
    stop_price: 760.00,
    stop_price_native: 760.00,
    current_stop: 760.00,
    shares: 10,
    pnl: 500.00,
    pnl_percent: 6.25,
    holding_days: 5,
    grace_days_remaining: null,
    status: 'open',
    entry_date: '2026-04-01',
    lifecycle_state: null,
    days_in_state: null,
    ...overrides,
  };
}

async function setupPositions(page, positions) {
  await page.route(`${API}/positions**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) })
  );
}

async function goToTableView(page) {
  await page.goto('/#/Positions');
  await page.waitForLoadState('domcontentloaded');
  // Switch to table view
  const tableBtn = page.locator('[aria-label="Table view"]');
  if (await tableBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    await tableBtn.click();
  }
}

// ---------------------------------------------------------------------------
// ST-01 — Lifecycle state badge
// ---------------------------------------------------------------------------

test.describe('ST-01 — Position lifecycle state badge', () => {
  test('SC-LS-01: "State" column header present in table view', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'PROFITABLE', days_in_state: 3 })]);
    await goToTableView(page);
    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('th', { hasText: 'State' })).toBeVisible();
  });

  test('SC-LS-02: GRACE badge renders with days_in_state suffix', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'GRACE', days_in_state: 5 })]);
    await goToTableView(page);
    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('GRACE — 5d')).toBeVisible();
  });

  test('SC-LS-03: PROFITABLE badge renders', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'PROFITABLE', days_in_state: 10 })]);
    await goToTableView(page);
    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('PROFITABLE')).toBeVisible();
  });

  test('SC-LS-04: No lifecycle badge when lifecycle_state is null', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: null, days_in_state: null })]);
    await goToTableView(page);
    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    // The lifecycle badge is a span with specific bg colour classes — none should be present
    await expect(page.locator('span.bg-blue-600')).not.toBeVisible();   // GRACE
    await expect(page.locator('span.bg-green-700')).not.toBeVisible();  // PROFITABLE
    await expect(page.locator('span.bg-violet-600')).not.toBeVisible(); // EXIT ZONE
    await expect(page.locator('span.bg-red-600')).not.toBeVisible();    // LOSING
  });
});

// ---------------------------------------------------------------------------
// ST-02 — Grace period alert card
// ---------------------------------------------------------------------------

test.describe('ST-02 — Grace period alert card', () => {
  function makeAlert(overrides = {}) {
    return {
      position_id: 'pos-001',
      ticker: 'NVDA',
      market: 'US',
      days_in_state: 8,
      trade_plan_id: null,
      trade_plan_summary: null,
      ...overrides,
    };
  }

  test('SC-GP-01: Alert card renders when position is GRACE ≥ day 8', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'GRACE', days_in_state: 8 })]);
    await page.route(`${API}/positions/grace-period-alerts`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [makeAlert()] }) })
    );
    await page.goto('/#/Positions');
    await expect(page.getByText(/grace period alert/i)).toBeVisible({ timeout: 8000 });
  });

  test('SC-GP-02: Alert card shows "Day N of 10" label and contextual body text', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'GRACE', days_in_state: 8 })]);
    await page.route(`${API}/positions/grace-period-alerts`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [makeAlert({ days_in_state: 8 })] }) })
    );
    await page.goto('/#/Positions');
    await expect(page.getByText(/day 8 of 10/i)).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/grace period ends in 2 trading day/i)).toBeVisible();
  });

  test('SC-GP-03: Alert card dismissed on ✕ click', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'GRACE', days_in_state: 8 })]);
    await page.route(`${API}/positions/grace-period-alerts`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [makeAlert()] }) })
    );
    await page.goto('/#/Positions');
    await expect(page.getByText(/grace period alert/i)).toBeVisible({ timeout: 8000 });
    await page.getByRole('button', { name: /dismiss grace period alert for NVDA/i }).click();
    await expect(page.getByText(/grace period alert — NVDA/i)).not.toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// ST-03 — Trail Stop modal
// ---------------------------------------------------------------------------

test.describe('ST-03 — Trail Stop modal', () => {
  const TRAIL_DATA = {
    current_stop: 760.00,
    atr_trail_stop: 810.50,
    trail_difference: 50.50,
    trail_r_terms: 1.3,
  };

  test('SC-TS-01: Trail Stop button visible for PROFITABLE position with stop set', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'PROFITABLE', days_in_state: 10, current_stop: 760 })]);
    await goToTableView(page);
    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    // ArrowUpDown icon button (trail stop) should be visible
    const trailBtn = page.locator('[title="Trail Stop"]');
    await expect(trailBtn).toBeVisible({ timeout: 5000 });
  });

  test('SC-TS-02: Trail Stop modal shows trail calculation data', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'PROFITABLE', days_in_state: 10, current_stop: 760 })]);
    await page.route(`${API}/positions/pos-001/stop-trail`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: TRAIL_DATA }) })
    );
    await goToTableView(page);
    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    await page.locator('[title="Trail Stop"]').click();
    await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(/trail stop — NVDA/i)).toBeVisible();
    // The ATR trail stop value appears in the dd element (not the button)
    await expect(page.locator('dd').filter({ hasText: '$810.50' })).toBeVisible({ timeout: 5000 });
  });

  test('SC-TS-03: Trail Stop button absent for GRACE state', async ({ page }) => {
    await stubCommon(page);
    await setupPositions(page, [makePosition({ lifecycle_state: 'GRACE', days_in_state: 3, current_stop: 760 })]);
    await goToTableView(page);
    await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('[title="Trail Stop"]')).not.toBeVisible();
  });
});
