/**
 * Trade plan lifecycle, end to end (ST-26, BLG-QA-23, EPIC-06, v9.16)
 *
 * One journey through the app as built after EPIC-02 (ST-07 "Plan this", ST-08 suggested size):
 *
 *   SC-TPL-01  Signals "Plan this" → Trade Plan pre-filled; the Setup Quality Score is visible;
 *              entering the stop pre-fills Planned Shares with the §4.1 suggestion; Save Plan
 *              creates a `draft` plan carrying the suggested size
 *   SC-TPL-02  Reopening the saved plan shows the same quality score (it is recomputed per
 *              ticker, not stored on the plan, so "persistence" means it survives a reload)
 *   SC-TPL-03  Trade Plans → "Start Trade" → Trade Entry pre-filled from the plan; Create Position
 *              sends trade_plan_id; the plan moves `draft` → `active` and gains position_id
 *   SC-TPL-04  Positions → Exit → Confirm Exit closes the position and writes a trade
 *   SC-TPL-05  Trade History → expand the trade → Plan vs Reality shows the values the backend
 *              formulas give for the plan and fills entered above (R achieved, R target, R delta,
 *              entry delta, adherence badge, state at exit)
 *
 * The scenarios run as one test because each step depends on state the previous one wrote.
 *
 * Mock backend: tests/e2e/mocks/trade-plan-lifecycle-backend.js — page.route() over an in-memory store (`db`). The write handlers copy the
 * backend's own rules so the journey's state is the state production would hold:
 *   - POST /portfolio/position: initial stop = entry − 5×ATR (calculations.py::calculate_initial_stop);
 *     an explicit trade_plan_id links the plan and sets status `active` (position_service.py::add_position)
 *   - POST /positions/{id}/exit: planned_entry_price is snapshotted from the ticker's signal
 *     current_price (position_service.py, Arc 4 PO-01); the plan's status is left unchanged — see
 *     the known gap below
 *   - GET /trades/{id}/plan-vs-reality: a port of plan_vs_reality_service.py::compute_plan_vs_reality.
 *     The formulas themselves are unit-tested in tests/test_plan_vs_reality.py; this test checks that
 *     the numbers entered through the UI reach that comparison and are displayed correctly. The
 *     expected values below are worked by hand, not read back from the port.
 *
 * Known gap (BLG-BE-211, filed by this story): data_model.md §Trade Plan Lifecycle says `active` →
 * `closed` happens when the linked position closes, but no backend code path writes `closed`. This
 * test therefore does not assert the plan's status after the exit; when BLG-BE-211 ships, add that
 * assertion (Trade Plans badge "Closed") and make the exit handler below set it.
 *
 * Known gap (BLG-BE-212, filed by ST-24): the exit snapshots planned_entry_price from the signal's
 * price at exit, not from the plan, so the entry delta below is the formula as built. When BLG-BE-212
 * ships, change the mock's exit handler and the worked entry delta.
 *
 * Infrastructure: page.route() network interception — no live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const { EXIT_PRICE, mockBackend } = require('./mocks/trade-plan-lifecycle-backend');

// Values the user enters along the journey.
const PLAN_STOP = '165.05';
const PLAN_R_TARGET = '2';
const PLAN_EARLY_EXIT = 'Close below the 50-day MA';
const ACTUAL_ENTRY = '184';
const ACTUAL_ATR = '3.45';

const planStatusBadge = (page, label) =>
  page.locator('tr', { hasText: 'AAPL' }).getByText(label, { exact: true });

test('SC-TPL-01..05: a plan goes from "Plan this" to a closed trade and its Plan vs Reality', async ({ page }) => {
  test.setTimeout(120000);
  const db = await mockBackend(page);

  // ── SC-TPL-01: create the plan from a signal, with the quality score visible ──
  await page.goto('/#/Signals');
  await page.getByTestId('signal-plan-this-AAPL').click();
  await expect(page).toHaveURL(/#\/TradePlan\?/, { timeout: 8000 });
  await expect(page.getByTestId('planned-entry-price-input')).toHaveValue('182.3', { timeout: 8000 });
  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('setup-quality-score-panel')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82');

  await page.getByTestId('planned-stop-price-input').fill(PLAN_STOP);
  await expect(page.getByTestId('plan-suggested-size')).toHaveText('Suggested size: 10 shares (§4.1, 1% risk)', { timeout: 5000 });
  await expect(page.getByTestId('planned-quantity-input')).toHaveValue('10');
  await page.getByPlaceholder('e.g. 2.5').fill(PLAN_R_TARGET);
  await page.getByPlaceholder('Under what conditions would you exit before the stop is hit?').fill(PLAN_EARLY_EXIT);
  await page.getByRole('button', { name: /save plan/i }).click();
  await expect(page.getByText('Trade plan saved successfully.')).toBeVisible({ timeout: 8000 });

  expect(db.plans).toHaveLength(1);
  expect(db.plans[0]).toMatchObject({
    ticker: 'AAPL', market: 'US', status: 'draft', position_id: null,
    planned_entry_price: 182.3, planned_stop_price: 165.05, planned_quantity: 10, r_target: 2,
    early_exit_conditions: PLAN_EARLY_EXIT,
  });

  // ── SC-TPL-02: the quality score is still shown when the saved plan is reopened ──
  await page.goto('/#/TradePlan?edit=plan-tpl-0001');
  await expect(page.getByTestId('planned-stop-price-input')).toHaveValue('165.05', { timeout: 10000 });
  await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82', { timeout: 8000 });

  // ── SC-TPL-03: start the trade from the plan; the plan links and becomes active ──
  await page.goto('/#/TradePlans');
  await expect(planStatusBadge(page, 'Draft')).toBeVisible({ timeout: 10000 });
  await page.getByTestId('start-trade-from-plan-plan-tpl-0001').click();
  await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });
  await expect(page.getByPlaceholder('e.g., AAPL or VOD.L')).toHaveValue('AAPL', { timeout: 8000 });
  await expect(page.getByPlaceholder('0', { exact: true })).toHaveValue('10');
  await expect(page.getByPlaceholder('0.00').first()).toHaveValue('182.3');
  await page.getByPlaceholder('0.00').first().fill(ACTUAL_ENTRY);
  await page.getByPlaceholder('Fetched automatically if blank').fill(ACTUAL_ATR);
  await page.getByRole('button', { name: /create position/i }).click();
  await expect(page.getByText('Linked to trade plan for AAPL.', { exact: false })).toBeVisible({ timeout: 8000 });
  await expect(page).toHaveURL(/#\/Positions/, { timeout: 8000 });

  expect(db.lastEntry).toMatchObject({ ticker: 'AAPL', trade_plan_id: 'plan-tpl-0001', entry_price: 184, shares: 10, atr_value: 3.45 });
  expect(db.plans[0]).toMatchObject({ status: 'active', position_id: 'pos-tpl-0001' });
  expect(db.log).toEqual([['plan', 'draft'], ['plan', 'active']]);

  await page.goto('/#/TradePlans');
  await expect(planStatusBadge(page, 'Active')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('start-trade-from-plan-plan-tpl-0001')).toHaveCount(0);

  // ── SC-TPL-04: close the position ──
  await page.goto('/#/Positions');
  await page.waitForSelector('text=AAPL', { timeout: 8000 });
  await page.locator('[aria-label="Table view"]').click();
  await page.getByRole('button', { name: 'Exit AAPL' }).click();
  const modal = page.getByRole('dialog', { name: 'Exit Position' });
  await expect(modal).toBeVisible({ timeout: 5000 });
  await modal.getByRole('button', { name: 'Confirm Exit' }).click();
  await expect(modal).toBeHidden({ timeout: 5000 });

  expect(db.lastExit).toMatchObject({ shares: 10, exit_price: EXIT_PRICE });
  expect(db.positions[0].status).toBe('closed');
  expect(db.trades).toHaveLength(1);

  // ── SC-TPL-05: Plan vs Reality for the closed trade ──
  // Worked by hand from the values entered above:
  //   initial stop   = 184 − 5 × 3.45                  = 166.75
  //   R achieved     = (210 − 184) / (184 − 166.75)     = 1.507 → +1.51R
  //   R delta        = 1.51 − 2                         = −0.49R
  //   entry delta    = (184 − 182.30) / 182.30 × 100    = +0.93%   (planned entry snapshotted from the signal)
  //   stop vs plan   = |166.75 − 165.05| / 165.05       = 1.03% → minor_deviation (not a stop deviation)
  //   adherence      = exit reason is not a target and the plan has early-exit conditions → Early Exit
  await page.goto('/#/TradeHistory');
  await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });
  await page.getByText('AAPL').first().click();
  const pvr = page.getByTestId('plan-vs-reality-section');
  await expect(pvr).toBeVisible({ timeout: 8000 });
  await expect(pvr).toContainText('+1.51R');
  await expect(pvr).toContainText('Target: 2R');
  await expect(pvr).toContainText('−0.49R vs target');
  await expect(pvr).toContainText('+0.93%');
  await expect(pvr).toContainText(`Planned: ${PLAN_EARLY_EXIT}`);
  await expect(pvr).toContainText('PROFITABLE');
  await expect(pvr).toContainText('Early Exit');
});
