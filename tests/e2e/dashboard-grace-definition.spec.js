/**
 * One grace definition across the Dashboard — Playwright tests
 * ST-10 (EPIC-02, v9.18, BLG-FE-308). Spec: docs/specs/frontend/pages/dashboard.md v4.4 §4B,
 * §1A Cards table (Positions to Watch) and §4 Card 1 / Card 3; design record
 * docs/design/2026-11-18__release-v9.18/dashboard-quiet-day/decision_record.md §3.
 *
 * Covers:
 *   SC-GD-01  GD-01  With the §4B rows A–E plus a row whose grace_period and grace_days_remaining
 *                    disagree, Card 1, Card 3 and Positions to Watch all count 3; Card 3 reads
 *                    "Ends today"; Positions to Watch reads "3 in grace · 2 ending within 2 days"
 *                    with no "exit zone"; the Today list's Grace ends today lists B only
 *   SC-GD-01b GD-01  The same with a row that has no status field: every count is 4
 *   SC-GD-02  GD-02  Positions to Watch opens /Positions?grace=open when its count is above 0
 *   SC-GD-03         Card 3 with in-grace positions but no day count shows no "next ends" line
 *                    (the old "No expiry date set" text is gone)
 *
 * Fixture shape follows backend/services/position_service.py: GET /positions sends
 * status "open" for every open position, the lifecycle state in position_state,
 * grace_period, and grace_days_remaining (null when not in grace).
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

const row = (ticker, grace_period, grace_days_remaining, position_state, holding_days) => ({
  id: `pos-${ticker}`, ticker, market: 'US', status: 'open', position_state, holding_days,
  grace_period, grace_days_remaining, pnl: 10, current_price: 110, current_trailing_stop: 90,
  entry_date: '2026-11-10',
});

// dashboard.md §4B worked rows, plus G: flags that disagree (grace_period false
// with a day count). G is not in grace by the one definition.
const ROWS = [
  row('AAAA', true, 10, 'GRACE', 0),
  row('BBBB', true, 1, 'GRACE', 9),
  row('CCCC', false, null, 'GRACE', 10), // stale lifecycle state
  row('DDDD', true, 2, 'OPEN', 8), // lagging lifecycle state
  row('EEEE', false, null, 'PROFITABLE', 30),
  row('GGGG', false, 3, 'GRACE', 7), // disagreeing flags
];
// Review fix: a row with no status field, in grace with 5 days left. Every
// count includes it, so with it every grace count is 4 (Card 1 used to filter
// on status first and would count 3).
const NO_STATUS = { ...row('JJJJ', true, 5, 'GRACE', 5), status: undefined };

async function mockDashboard(page, positions) {
  await page.route(new RegExp(`${API}/`), (route) => {
    const url = route.request().url();
    if (url.includes('/market/status')) {
      return route.fulfill(json({ status: 'ok', data: { spy: { is_risk_on: true }, ftse: { is_risk_on: true } } }));
    }
    if (/\/positions(\?|$)/.test(url)) return route.fulfill(json(positions));
    return route.fulfill(json({ status: 'ok', data: [] }));
  });
}

const cardByTitle = (page, title) =>
  page.locator('a', { has: page.getByText(title, { exact: true }) }).first();

async function gotoDashboard(page) {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto('/#/');
  await expect(page.getByRole('heading', { level: 1, name: 'Dashboard', exact: true })).toBeVisible({ timeout: 15000 });
}

test('SC-GD-01: every Dashboard grace count uses the one definition', async ({ page }) => {
  await mockDashboard(page, ROWS);
  await gotoDashboard(page);

  const card1 = cardByTitle(page, 'Open Positions');
  await expect(card1).toContainText('3 in grace', { timeout: 15000 });

  const card3 = cardByTitle(page, 'In Grace Today');
  await expect(card3.locator('p.text-4xl')).toHaveText('3');
  await expect(card3.getByTestId('dashboard-grace-next-ends')).toHaveText('Ends today');

  const watch = cardByTitle(page, 'Positions to Watch');
  await expect(watch.locator('p.text-4xl')).toHaveText('3');
  await expect(watch.getByTestId('positions-to-watch-subtext')).toHaveText('3 in grace · 2 ending within 2 days');
  await expect(watch).not.toContainText('exit zone');

  const graceGroup = page.getByTestId('today-group-grace');
  await expect(graceGroup).toContainText('BBBB');
  for (const other of ['AAAA', 'CCCC', 'DDDD', 'EEEE', 'GGGG']) await expect(graceGroup).not.toContainText(other);
});

test('SC-GD-01b: a row with no status still counts the same on every card', async ({ page }) => {
  await mockDashboard(page, [...ROWS, NO_STATUS]);
  await gotoDashboard(page);
  await expect(cardByTitle(page, 'Open Positions')).toContainText('4 in grace', { timeout: 15000 });
  await expect(cardByTitle(page, 'In Grace Today').locator('p.text-4xl')).toHaveText('4');
  await expect(cardByTitle(page, 'Positions to Watch').getByTestId('positions-to-watch-subtext')).toHaveText('4 in grace · 2 ending within 2 days');
});

test('SC-GD-02: Positions to Watch opens the Positions grace view when its count is above 0', async ({ page }) => {
  await mockDashboard(page, ROWS);
  await gotoDashboard(page);

  const watch = cardByTitle(page, 'Positions to Watch');
  await expect(watch).toHaveAttribute('href', '#/Positions?grace=open', { timeout: 15000 });
  await watch.click();
  await expect(page).toHaveURL(/#\/Positions\?grace=open$/);
});

test('SC-GD-03: in-grace positions with no day count show the count and no "next ends" line', async ({ page }) => {
  await mockDashboard(page, [row('HHHH', true, null, 'GRACE', 3)]);
  await gotoDashboard(page);

  const card3 = cardByTitle(page, 'In Grace Today');
  await expect(card3.locator('p.text-4xl')).toHaveText('1', { timeout: 15000 });
  await expect(card3.getByTestId('dashboard-grace-next-ends')).toHaveCount(0);
  await expect(card3).not.toContainText('No expiry date set');
  await expect(cardByTitle(page, 'Positions to Watch').getByTestId('positions-to-watch-subtext')).toHaveText('1 in grace');
});
