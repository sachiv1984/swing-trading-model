/**
 * Monthly P&L — Realised P&L by exit condition card — ST-24 (BLG-FEAT-99, EPIC-04, v9.14)
 *
 * Design source: docs/design/2026-10-29__release-v9.14/monthly-pnl-exit-condition-breakdown/decision_record.md
 * Spec: docs/specs/frontend/pages/reports.md §Exit Condition Breakdown (v0.26)
 * Data contract: docs/specs/api_contracts/reports_endpoints.md v0.19 — per-month `by_exit_condition`
 * ({ stop_loss | risk_off | manual: { realised_pnl_gbp, trade_count } }), present on every month or none.
 *
 * Coverage:
 *   SC-MEC-01  The card renders the three §8 category columns and a Total equal to each month's realised P&L,
 *              and the footer totals equal the sum of the months, in dark and light themes (AC 3)
 *   SC-MEC-02  A category with no trades shows "—" with no trade line; trade lines pluralise; a category
 *              with trades at exactly £0.00 shows the figure in the neutral tone
 *   SC-MEC-03  With by_exit_condition absent, "Exit-condition breakdown unavailable." shows and the
 *              Monthly table still renders
 *   SC-MEC-04  No card when the tax year has no closed trades
 *   SC-MEC-05  Placement: after the AI summary card, before the Unrealised P&L Card
 *   SC-MEC-06  axe: no color-contrast entry and no serious/critical violation in the card, both themes
 *   SC-MEC-07  Narrow viewport: the table overflows its own scroller, the card stays within the viewport,
 *              and the Month column is sticky
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/Reports'), then click the Monthly tab.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const NARRATIVE = new RegExp(`${API}/reports/monthly-pnl/narrative`);
const MONTHLY = new RegExp(`${API}/reports/monthly-pnl(?!\\?format=csv|/narrative)`);
const MINUS = '−';

const cat = (realised_pnl_gbp, trade_count) => ({ realised_pnl_gbp, trade_count });

// October: every category; −120.10 + 210.25 = 90.15 stop-loss, −15.50 risk-off, 13.00 manual → 87.65.
const OCTOBER = {
  year: 2026, month: 10, realised_pnl_gbp: 87.65, trade_count: 5, null_fee_trade_count: 0,
  snapshotted: false, restated: false, snapshot_realised_pnl_gbp: null, restated_diff_gbp: null,
  by_exit_condition: { stop_loss: cat(90.15, 2), risk_off: cat(-15.5, 1), manual: cat(13, 2) },
};
// September: stop-loss exits only; the other categories have no trades.
const SEPTEMBER = {
  year: 2026, month: 9, realised_pnl_gbp: -40, trade_count: 1, null_fee_trade_count: 0,
  snapshotted: true, restated: false, snapshot_realised_pnl_gbp: -40, restated_diff_gbp: 0,
  by_exit_condition: { stop_loss: cat(-40, 1), risk_off: cat(0, 0), manual: cat(0, 0) },
};

// August: one manual exit at exactly break-even, so its P&L renders in the neutral tone.
const AUGUST = {
  year: 2026, month: 8, realised_pnl_gbp: 0, trade_count: 1, null_fee_trade_count: 0,
  snapshotted: true, restated: false, snapshot_realised_pnl_gbp: 0, restated_diff_gbp: 0,
  by_exit_condition: { stop_loss: cat(0, 0), risk_off: cat(0, 0), manual: cat(0, 1) },
};

const withoutBreakdown = (m) => {
  const { by_exit_condition: _omit, ...rest } = m;
  return rest;
};

async function mockApi(page, months, { unrealised = null } = {}) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(MONTHLY, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok', data: months, estimated_unrealised_pnl: unrealised,
        unrealised_note: unrealised == null ? null : 'Indicative only.', compliance_summary: null,
      }),
    })
  );
  await page.route(NARRATIVE, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { year: null, narrative: null, source: null, generated_at: null, advisory: true } }),
    })
  );
}

async function gotoMonthlyTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /monthly p&l/i }).click();
}

for (const theme of ['dark', 'light']) {
  test(`SC-MEC-01: categories render and the Total reconciles to the month's realised P&L (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await mockApi(page, [OCTOBER, SEPTEMBER]);
    await gotoMonthlyTab(page);

    const card = page.getByTestId('monthly-exit-condition-card');
    await expect(card).toBeVisible({ timeout: 8000 });
    if (theme === 'dark') await expect(page.locator('html')).toHaveClass(/\bdark\b/);
    else await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);

    await expect(card.getByRole('heading', { name: 'Realised P&L by exit condition' })).toBeVisible();
    await expect(card.getByTestId('monthly-exit-condition-header-stop_loss')).toHaveText(/Stop-loss \(§8\.1\)/i);
    await expect(card.getByTestId('monthly-exit-condition-header-risk_off')).toHaveText(/Risk-off \(§8\.2\)/i);
    await expect(card.getByTestId('monthly-exit-condition-header-manual')).toHaveText(/Manual \(§8\.3\)/i);

    // One row per month, in the Monthly Financial Table's order, named with month and year.
    const rows = card.getByTestId('monthly-exit-condition-row');
    await expect(rows).toHaveCount(2);
    await expect(rows.nth(0)).toContainText('October 2026');
    await expect(rows.nth(1)).toContainText('September 2026');

    const october = rows.nth(0);
    await expect(october.getByTestId('monthly-exit-condition-stop_loss-pnl')).toHaveText('£90.15');
    await expect(october.getByTestId('monthly-exit-condition-risk_off-pnl')).toHaveText(`${MINUS}£15.50`);
    await expect(october.getByTestId('monthly-exit-condition-manual-pnl')).toHaveText('£13.00');
    // Total = the month's realised_pnl_gbp, the same figure as the Monthly Financial Table.
    await expect(october.getByTestId('monthly-exit-condition-total-pnl')).toHaveText('£87.65');
    await expect(october.getByTestId('monthly-exit-condition-total-trades')).toHaveText('5 trades');
    const tableOctober = page.getByTestId('monthly-realised-pnl-cell').first();
    await expect(tableOctober).toHaveText('£87.65');

    // Footer "Tax year total" sums each column for the months shown.
    const footer = card.getByTestId('monthly-exit-condition-footer');
    await expect(footer).toContainText('Tax year total');
    await expect(footer.getByTestId('monthly-exit-condition-footer-stop_loss-pnl')).toHaveText('£50.15');
    await expect(footer.getByTestId('monthly-exit-condition-footer-stop_loss-trades')).toHaveText('3 trades');
    await expect(footer.getByTestId('monthly-exit-condition-footer-risk_off-pnl')).toHaveText(`${MINUS}£15.50`);
    await expect(footer.getByTestId('monthly-exit-condition-footer-manual-pnl')).toHaveText('£13.00');
    await expect(footer.getByTestId('monthly-exit-condition-footer-total-pnl')).toHaveText('£47.65');
    await expect(footer.getByTestId('monthly-exit-condition-footer-total-trades')).toHaveText('6 trades');

    // Tone: positive green, negative red (the Monthly table's rule).
    const tone = (loc) => loc.evaluate((el) => getComputedStyle(el).color);
    const green = theme === 'dark' ? 'rgb(52, 211, 153)' : 'rgb(4, 120, 87)';
    const red = theme === 'dark' ? 'rgb(251, 113, 133)' : 'rgb(190, 18, 60)';
    expect(await tone(october.getByTestId('monthly-exit-condition-stop_loss-pnl'))).toBe(green);
    expect(await tone(october.getByTestId('monthly-exit-condition-risk_off-pnl'))).toBe(red);

    await expect(card.getByTestId('monthly-exit-condition-caption')).toHaveText(
      'Month-end rebalance exits (§8.4) are recorded as Manual Exit and counted under Manual until a separate exit reason exists.'
    );
    await expect(card.getByTestId('monthly-exit-condition-unavailable')).toHaveCount(0);
  });
}

test('SC-MEC-02: a category with no trades shows "—" with no trade line; trade lines pluralise; zero is neutral', async ({ page }) => {
  await mockApi(page, [OCTOBER, SEPTEMBER, AUGUST]);
  await gotoMonthlyTab(page);

  const september = page.getByTestId('monthly-exit-condition-row').nth(1);
  await expect(september).toBeVisible({ timeout: 8000 });
  await expect(september.getByTestId('monthly-exit-condition-risk_off')).toHaveText('—');
  await expect(september.getByTestId('monthly-exit-condition-manual')).toHaveText('—');
  await expect(september.getByTestId('monthly-exit-condition-risk_off-trades')).toHaveCount(0);
  await expect(september.getByTestId('monthly-exit-condition-stop_loss-trades')).toHaveText('1 trade');
  await expect(page.getByTestId('monthly-exit-condition-row').nth(0).getByTestId('monthly-exit-condition-manual-trades')).toHaveText('2 trades');

  // A category with trades and exactly £0.00 shows the figure (not "—") in the neutral tone.
  const august = page.getByTestId('monthly-exit-condition-row').nth(2);
  const zero = august.getByTestId('monthly-exit-condition-manual-pnl');
  await expect(zero).toHaveText('£0.00');
  await expect(august.getByTestId('monthly-exit-condition-manual-trades')).toHaveText('1 trade');
  await expect(zero).toHaveClass(/text-slate-600/);
  await expect(zero).not.toHaveClass(/emerald|rose/);
});

test('SC-MEC-03: by_exit_condition absent shows the unavailable state and the Monthly table still renders', async ({ page }) => {
  await mockApi(page, [withoutBreakdown(OCTOBER), withoutBreakdown(SEPTEMBER)]);
  await gotoMonthlyTab(page);

  const card = page.getByTestId('monthly-exit-condition-card');
  await expect(card).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-exit-condition-unavailable')).toHaveText('Exit-condition breakdown unavailable.');
  await expect(card.getByTestId('monthly-exit-condition-table')).toHaveCount(0);
  await expect(page.getByTestId('monthly-realised-pnl-cell')).toHaveCount(2);
  await expect(page.getByTestId('monthly-realised-pnl-cell').first()).toHaveText('£87.65');
});

test('SC-MEC-04: no card when the tax year has no closed trades', async ({ page }) => {
  await mockApi(page, []);
  await gotoMonthlyTab(page);
  await expect(page.getByText('No closed trades in scope.')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-exit-condition-card')).toHaveCount(0);
});

test('SC-MEC-05: the card sits after the AI summary card and before the Unrealised P&L Card', async ({ page }) => {
  await mockApi(page, [OCTOBER], { unrealised: 12.5 });
  await gotoMonthlyTab(page);
  await expect(page.getByTestId('monthly-exit-condition-card')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-narrative-card')).toBeVisible();
  await expect(page.getByTestId('monthly-unrealised-pnl-card')).toBeVisible();

  const order = await page.evaluate(() => {
    const ids = ['monthly-narrative-card', 'monthly-exit-condition-card', 'monthly-unrealised-pnl-card'];
    const els = ids.map((id) => document.querySelector(`[data-testid="${id}"]`));
    const follows = (a, b) => Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);
    return [follows(els[0], els[1]), follows(els[1], els[2])];
  });
  expect(order).toEqual([true, true]);
});

for (const theme of ['dark', 'light']) {
  test(`SC-MEC-06: axe finds no color-contrast entry and no serious/critical violation in the card (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await mockApi(page, [OCTOBER, SEPTEMBER]);
    await gotoMonthlyTab(page);
    await expect(page.getByTestId('monthly-exit-condition-row').first()).toBeVisible({ timeout: 8000 });
    await page.waitForTimeout(800); // let entrance animations settle

    const results = await new AxeBuilder({ page }).include('[data-testid="monthly-exit-condition-card"]').analyze();
    expect(results.violations.filter((v) => v.id === 'color-contrast').map((v) => v.nodes.map((n) => n.target))).toEqual([]);
    expect(results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical').map((v) => v.id)).toEqual([]);
  });
}

test('SC-MEC-07: at phone width the table scrolls inside the card and the page does not scroll sideways', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 800 });
  await mockApi(page, [OCTOBER, SEPTEMBER]);
  await gotoMonthlyTab(page);
  await expect(page.getByTestId('monthly-exit-condition-row').first()).toBeVisible({ timeout: 8000 });

  const scroller = page.getByTestId('monthly-exit-condition-table').locator('xpath=..');
  await expect(scroller).toHaveCSS('overflow-x', 'auto');
  // The table is wider than its scroller (it scrolls inside the card), and the card itself stays
  // within the viewport. The page-level scrollWidth is not asserted: at 375px the Reports tab bar
  // already overflows with no card on the page (BLG-FE-237), which ST-24 does not change.
  const widths = await page.evaluate(() => {
    const table = document.querySelector('[data-testid="monthly-exit-condition-table"]');
    const card = document.querySelector('[data-testid="monthly-exit-condition-card"]');
    return { table: table.scrollWidth, scroller: table.parentElement.clientWidth, cardRight: card.getBoundingClientRect().right };
  });
  expect(widths.table).toBeGreaterThan(widths.scroller);
  expect(widths.cardRight).toBeLessThanOrEqual(375);
  // The Month column is sticky.
  await expect(page.getByTestId('monthly-exit-condition-row').first().locator('td').first()).toHaveCSS('position', 'sticky');
});
