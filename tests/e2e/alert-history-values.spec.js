/**
 * Alert History compact values (ST-04, BLG-FE-228, EPIC-01, v9.18)
 *
 * Spec: docs/specs/frontend/pages/notifications.md v0.14 §Alert History Values;
 * design: docs/design/2026-11-18__release-v9.18/alert-delivery-truth/decision_record.md §4.
 *
 *   SC-AHV-01  Each of the 4 alert types shows its intended compact text (AC)
 *   SC-AHV-02  UK rows (symbol ends .L) show prices in pounds; US rows in dollars
 *   SC-AHV-03  An untriggered regime row ({}) shows "—"
 *   SC-AHV-04  The expanded row uses the spec labels and the row's currency
 *
 * Fixtures follow the writer, not the contract summary: values_compared keys are the
 * ones alerts_service.evaluate_alerts passes to _insert_evaluation; symbol is the
 * position's ticker (UK keeps .L, data_model.md positions.ticker); prices are native
 * (UK pounds). gap_pct is the writer's round(proximity, 2), so the 1-dp display rounds.
 *
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const routed = require('./fixtures/routed-pages-populated');

const ev = (id, minutesAgo, rule_type, symbol, triggered, values_compared) => ({
  id,
  evaluation_timestamp: new Date(Date.UTC(2026, 10, 18, 9, 0) - minutesAgo * 60000).toISOString(),
  rule_type,
  symbol,
  triggered,
  notification_sent: triggered,
  values_compared,
});

const EVALUATIONS = [
  ev('e-stop-uk', 0, 'stop_loss_approach', 'BARC.L', true,
    { stop_price: 180.0, current_price: 182.5, gap_pct: 1.37, threshold_pct: 5.0 }),
  ev('e-stop-us', 1, 'stop_loss_approach', 'AAPL', false,
    { stop_price: 210.0, current_price: 238.75, gap_pct: 12.04, threshold_pct: 5.0 }),
  ev('e-grace', 2, 'grace_period_warning', 'VOD.L', true,
    { holding_days: 8, min_hold_days: 10, days_remaining: 2 }),
  ev('e-regime', 3, 'market_regime_change', null, true,
    { spy_risk_on: true, ftse_risk_on: false }),
  ev('e-regime-none', 4, 'market_regime_change', null, false, {}),
  ev('e-summary', 5, 'daily_portfolio_summary', null, true, { open_positions: 3 }),
];

async function mockHistory(page) {
  await routed.catchAll(page);
  await page.route(/\/alerts\/history/, (route) => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ status: 'ok', data: { total: EVALUATIONS.length, evaluations: EVALUATIONS } }),
  }));
}

// Rows are newest first, the same order as EVALUATIONS; the Values cell is the 6th.
const valuesCell = (page, index) =>
  page.locator('main tbody tr').filter({ has: page.getByTestId('alert-history-expand') }).nth(index).locator('td').nth(5);

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => window.localStorage.setItem('command-palette-tooltip-seen', 'true'));
  await mockHistory(page);
  await page.goto('/#/notifications/history');
  await expect(page.getByTestId('alert-history-expand').first()).toBeVisible({ timeout: 10000 });
});

test('SC-AHV-01: each of the 4 alert types shows its intended compact text', async ({ page }) => {
  await expect(valuesCell(page, 0)).toHaveText('Price £182.50 · Stop £180.00 · Gap 1.4%');
  await expect(valuesCell(page, 2)).toHaveText('Day 8 of 10 · 2 day(s) left');
  await expect(valuesCell(page, 3)).toHaveText('US RISK-ON · UK RISK-OFF');
  await expect(valuesCell(page, 5)).toHaveText('3 open position(s)');
});

test('SC-AHV-02: UK prices are in pounds and US prices in dollars', async ({ page }) => {
  await expect(valuesCell(page, 0)).toContainText('£182.50');
  await expect(valuesCell(page, 0)).not.toContainText('$');
  await expect(valuesCell(page, 1)).toHaveText('Price $238.75 · Stop $210.00 · Gap 12.0%');
});

test('SC-AHV-03: an untriggered regime row with no values shows a dash', async ({ page }) => {
  await expect(valuesCell(page, 4)).toHaveText('—');
});

test('SC-AHV-04: the expanded row uses the spec labels and the row currency', async ({ page }) => {
  await page.getByTestId('alert-history-expand').first().click();
  const detail = page.locator('#alert-history-detail-e-stop-uk');
  await expect(detail).toBeVisible();
  for (const [label, value] of [
    ['Stop price', '£180.00'],
    ['Current price', '£182.50'],
    ['Gap to stop', '1.4%'],
    ['Threshold', '5.0%'],
  ]) {
    const line = detail.locator('div.flex').filter({ hasText: label });
    await expect(line).toHaveCount(1);
    await expect(line).toContainText(value);
  }

  await page.getByTestId('alert-history-expand').nth(2).click();
  const grace = page.locator('#alert-history-detail-e-grace');
  for (const label of ['Days held', 'Grace period (days)', 'Days left']) {
    await expect(grace.getByText(label, { exact: false })).toBeVisible();
  }
});
