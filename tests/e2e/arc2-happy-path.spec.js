/**
 * Arc 2 (Pre-Trade Research & Planning) — arc-level happy path (ST-24, BLG-QA-21, EPIC-06, v9.16)
 *
 * Protocol: docs/qa/arc2_e2e_qa_protocol.md §4 (stages A1–A5).
 * The journey continues where tests/e2e/trade-plan-lifecycle.spec.js (ST-26) takes over: exit and
 * Plan vs Reality are asserted there, not repeated here.
 *
 *   SC-ARC2-01  Screener row → "Research" opens the Research View for the ticker (PT-02), with the
 *               Setup Quality Score (PT-04) and prospective heat (PT-03); no plan exists yet
 *   SC-ARC2-02  Research View → "Create Trade Plan" → Trade Plan for the ticker; the quality score is
 *               shown; with entry and stop the shares pre-fill with the §4.1 suggestion
 *   SC-ARC2-03  The pre-trade entry checklist (PT-05) is completed and saved on the plan with the
 *               thesis and R target (PT-01); the plan is a `draft`
 *   SC-ARC2-04  The Research View now shows the plan (Draft badge, "View full plan")
 *   SC-ARC2-05  Trade Plans → "Start Trade" → Create Position links the plan; it becomes `active`
 *
 * Mock backend: tests/e2e/mocks/trade-plan-lifecycle-backend.js (shared with ST-26).
 * Infrastructure: page.route() network interception — no live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const { mockBackend } = require('./mocks/trade-plan-lifecycle-backend');

const CHECKLIST_IDS = ['signal_confirmed', 'heat_limit_checked', 'stop_defined', 'research_reviewed'];
const THESIS = 'Momentum leader breaking out above its 50-day range with the regime risk-on.';

test('SC-ARC2-01..05: Screener → Research → Trade Plan (quality score, checklist) → linked position', async ({ page }) => {
  test.setTimeout(120000);
  const db = await mockBackend(page);

  // ── SC-ARC2-01: Screener → Research View ──
  await page.goto('/#/Screener');
  const row = page.locator('tr', { hasText: 'AAPL' }).first();
  await expect(row).toBeVisible({ timeout: 10000 });
  await row.getByRole('button', { name: /^Research$/ }).click();
  await expect(page).toHaveURL(/#\/research\/AAPL/, { timeout: 8000 });
  await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82', { timeout: 10000 });
  await expect(page.getByText(/prospective/i).first()).toBeVisible();
  await expect(page.getByText('No trade plan for AAPL.')).toBeVisible();

  // ── SC-ARC2-02: Research View → Create Trade Plan ──
  await page.getByRole('button', { name: 'Create Trade Plan' }).click();
  await expect(page).toHaveURL(/#\/TradePlan\?ticker=AAPL/, { timeout: 8000 });
  await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82', { timeout: 8000 });
  await page.getByTestId('planned-entry-price-input').fill('182.3');
  await page.getByTestId('planned-stop-price-input').fill('165.05');
  await expect(page.getByTestId('plan-suggested-size')).toHaveText('Suggested size: 10 shares (§4.1, 1% risk)', { timeout: 5000 });
  await expect(page.getByTestId('planned-quantity-input')).toHaveValue('10');

  // ── SC-ARC2-03: thesis, R target and the completed checklist are saved on a draft plan ──
  await page.getByTestId('setup-thesis-textarea').fill(THESIS);
  await page.getByPlaceholder('e.g. 2.5').fill('2');
  for (const id of CHECKLIST_IDS) {
    const item = page.getByTestId(`entry-checklist-item-${id}`);
    if ((await item.getAttribute('aria-checked')) !== 'true') await item.click();
    await expect(item).toHaveAttribute('aria-checked', 'true');
  }
  await page.getByRole('button', { name: /save plan/i }).click();
  await expect(page.getByText('Trade plan saved successfully.')).toBeVisible({ timeout: 8000 });

  expect(db.plans).toHaveLength(1);
  const saved = db.plans[0];
  expect(saved).toMatchObject({
    ticker: 'AAPL', market: 'US', status: 'draft', setup_thesis: THESIS, r_target: 2,
    planned_entry_price: 182.3, planned_stop_price: 165.05, planned_quantity: 10, checklist_completed: true,
  });
  expect(saved.checklist_items.map((i) => [i.id, i.checked])).toEqual(CHECKLIST_IDS.map((id) => [id, true]));

  // ── SC-ARC2-04: the Research View shows the new plan ──
  await page.goto('/#/research/AAPL');
  await expect(page.getByText('View full plan')).toBeVisible({ timeout: 10000 });
  await expect(page.getByText('Draft', { exact: true })).toBeVisible();

  // ── SC-ARC2-05: start the trade from the plan; the plan links and becomes active ──
  await page.goto('/#/TradePlans');
  await page.getByTestId('start-trade-from-plan-plan-tpl-0001').click();
  await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });
  await expect(page.getByPlaceholder('0', { exact: true })).toHaveValue('10', { timeout: 8000 });
  await page.getByPlaceholder('Fetched automatically if blank').fill('3.45');
  await page.getByRole('button', { name: /create position/i }).click();
  await expect(page.getByText('Linked to trade plan for AAPL.', { exact: false })).toBeVisible({ timeout: 8000 });
  expect(db.lastEntry).toMatchObject({ trade_plan_id: 'plan-tpl-0001', entry_price: 182.3, shares: 10 });
  expect(db.plans[0]).toMatchObject({ status: 'active', position_id: 'pos-tpl-0001' });
});
