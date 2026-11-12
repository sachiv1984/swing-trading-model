/**
 * Single grace view — ST-04 (BLG-FE-257, EPIC-01, v9.17)
 *
 * Specs: docs/specs/frontend/pages/positions.md v2.26 §Grace Period View;
 *        dashboard.md v4.2 Card 3; risk_dashboard.md v0.1.16 §5.2
 * Design: docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md §5, §10
 *
 * AC (stage4_backlog_slice.md#ST-04): grace detail renders in one component on
 * one page; the other surfaces link to it.
 *
 *   SC-POSGV-01  GracePeriodView lists every in-grace position (not only ≤ 2 days left),
 *                plus an alert whose grace has just ended (0 days), ordered by
 *                grace_days_remaining then ticker, with the day label, body sentence,
 *                trade plan block or "No trade plan linked." and View Trade Plan. A row
 *                with no alert (more than 2 days left) shows no plan line
 *                (Known Deviation DEV-EPIC01-ST04-01)
 *   SC-POSGV-02  Rows with ≤ 2 days left keep the amber accent; others are neutral
 *   SC-POSGV-03  No dismiss control; a leftover grace_alert_dismissed_* key hides nothing
 *   SC-POSGV-04  A row's ticker links to /Positions?position={id}
 *   SC-POSGV-05  Dashboard Card 3 links to /Positions?grace=open, which opens the grace view
 *   SC-POSGV-06  The Risk Dashboard panel links to /Positions?grace=open and lists no rows
 *   SC-POSGV-07  Visiting Dashboard, Risk Dashboard and Positions, per-position
 *                "Day n of 10" text appears only inside grace-period-view
 *   SC-POSGV-08  axe colour contrast of the Risk Dashboard grace panel, light and dark
 *
 * Mock layer: page.route(). HashRouter: navigate with '/#/…'.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;
const { makePosition, openPositionsWarning } = require('./fixtures/positions-table');
const { TD_07 } = require('./mocks/portfolio-mock-data');

const API = 'http://localhost:8000';
const json = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });

const inGrace = (id, ticker, days) => makePosition({
  id, ticker, grace_period: true, grace_days_remaining: days, holding_days: 10 - days,
  lifecycle_state: 'GRACE', position_state: 'GRACE',
});
// Expected order: EEEE (0, alert only: grace has just ended), BBBB (1), CCCC (1),
// DDDD (2), AAAA (6); OTHR is not in grace.
const POSITIONS = [
  inGrace('pos-a', 'AAAA', 6),
  inGrace('pos-c', 'CCCC', 1),
  makePosition({ id: 'pos-oth', ticker: 'OTHR' }),
  inGrace('pos-b', 'BBBB', 1),
  inGrace('pos-d', 'DDDD', 2),
];
const ALERTS = [
  {
    position_id: 'pos-b', ticker: 'BBBB', market: 'US', days_in_state: 9, grace_days_remaining: 1,
    trade_plan_id: 'tp-9', trade_plan_summary: { setup_thesis: 'Breakout over the 50-day high', stop_level: 95, r_target: 3 },
  },
  { position_id: 'pos-c', ticker: 'CCCC', market: 'US', days_in_state: 9, grace_days_remaining: 1, trade_plan_id: null, trade_plan_summary: null },
  { position_id: 'pos-d', ticker: 'DDDD', market: 'US', days_in_state: 8, grace_days_remaining: 2, trade_plan_id: null, trade_plan_summary: null },
  { position_id: 'pos-e', ticker: 'EEEE', market: 'US', days_in_state: 10, grace_days_remaining: 0, trade_plan_id: null, trade_plan_summary: null },
];
const PORTFOLIO = {
  ...TD_07,
  positions: POSITIONS.map((p) => ({ ...p, display_status: p.grace_period ? 'GRACE' : 'PROFITABLE' })),
};

async function stubAll(page) {
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(json({ data: { spy: { price: 500, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7600, is_risk_on: true }, fx_rate: 1.27 } })));
  await page.route(`${API}/positions`, (r) => r.fulfill(json(POSITIONS)));
  await page.route(`${API}/positions?*`, (r) => r.fulfill(json(POSITIONS)));
  await page.route(`${API}/positions/grace-period-alerts`, (r) => r.fulfill(json({ status: 'ok', data: ALERTS })));
  await page.route(`${API}/portfolio`, (r) => r.fulfill(json(PORTFOLIO)));
  await page.route(`${API}/portfolio/drawdown-status`, (r) => r.fulfill(json({ status: 'ok', data: { threshold_breached: false } })));
  await page.route(`${API}/portfolio/concentration-status`, (r) => r.fulfill(json({ status: 'ok', data: { any_breach: false } })));
  await page.route(`${API}/analytics/metrics*`, (r) => r.fulfill(json({ status: 'ok', data: { last_sync_at: null } })));
}

async function gotoGraceView(page) {
  await stubAll(page);
  await page.goto('/#/Positions?grace=open');
  const view = page.getByTestId('grace-period-view');
  await expect(view).toBeVisible({ timeout: 10000 });
  return view;
}

test.describe('Single grace view (ST-04, BLG-FE-257)', () => {
  test('SC-POSGV-01 — lists every in-grace position in order, with the existing copy', async ({ page }) => {
    const view = await gotoGraceView(page);
    const tickers = await view.locator('[data-testid^="grace-row-"]').evaluateAll(
      (els) => els.filter((el) => el.tagName === 'LI').map((el) => el.getAttribute('data-testid').replace('grace-row-', '')));
    expect(tickers).toEqual(['EEEE', 'BBBB', 'CCCC', 'DDDD', 'AAAA']);

    const e = view.getByTestId('grace-row-EEEE');
    await expect(e.getByTestId('grace-alert-day-label')).toHaveText('Day 10 of 10');
    await expect(e).toContainText('Grace period has ended. Your position will transition to LOSING or PROFITABLE on next refresh.');

    const b = view.getByTestId('grace-row-BBBB');
    await expect(b.getByTestId('grace-alert-day-label')).toHaveText('Day 10 of 10');
    await expect(b).toContainText('Your grace period ends in 1 day. Review your original thesis before the window closes.');
    await expect(b.getByTestId('grace-row-plan')).toContainText('Breakout over the 50-day high');
    await expect(b.getByTestId('grace-row-plan')).toContainText('R-target: 3R');
    await expect(b.getByRole('link', { name: /View Trade Plan/ })).toHaveAttribute('href', '#/TradePlan?edit=tp-9&ticker=BBBB');

    await expect(view.getByTestId('grace-row-DDDD')).toContainText('No trade plan linked.');

    // No alert row (more than 2 days left): the plan is unknown, so no plan line.
    const a = view.getByTestId('grace-row-AAAA');
    await expect(a.getByTestId('grace-alert-day-label')).toHaveText('Day 5 of 10');
    await expect(a).not.toContainText('No trade plan linked.');
    await expect(a.getByTestId('grace-row-plan')).toHaveCount(0);
    await expect(a.getByRole('link', { name: /View Trade Plan/ })).toHaveCount(0);
    await expect(view.getByTestId('grace-row-OTHR')).toHaveCount(0);

    // The strip summary counts the same four rows.
    await expect(page.getByTestId('warning-entry-grace').getByTestId('warning-summary')).toHaveText(/^5 positions in grace · next ends /);
  });

  test('SC-POSGV-02 — ≤ 2 days left keeps the amber accent; more is neutral', async ({ page }) => {
    const view = await gotoGraceView(page);
    for (const t of ['BBBB', 'CCCC', 'DDDD']) {
      await expect(view.getByTestId(`grace-row-${t}`)).toHaveClass(/border-l-amber-500/);
      await expect(view.getByTestId(`grace-row-${t}`).getByTestId('grace-alert-day-label')).toHaveClass(/text-app-warning/);
    }
    await expect(view.getByTestId('grace-row-AAAA')).not.toHaveClass(/border-l-amber-500/);
    await expect(view.getByTestId('grace-row-AAAA').getByTestId('grace-alert-day-label')).toHaveClass(/text-app-muted/);
  });

  test('SC-POSGV-03 — no dismiss; an old dismiss key hides nothing', async ({ page }) => {
    await page.addInitScript(() => window.sessionStorage.setItem('grace_alert_dismissed_pos-b', '1'));
    const view = await gotoGraceView(page);
    await expect(view.getByTestId('grace-row-BBBB')).toBeVisible();
    await expect(view.getByRole('button')).toHaveCount(0);
  });

  test('SC-POSGV-04 — a row\'s ticker links to the position', async ({ page }) => {
    const view = await gotoGraceView(page);
    const link = view.getByRole('link', { name: 'Open DDDD on Positions' });
    await expect(link).toHaveAttribute('href', '#/Positions?position=pos-d');
    await link.click();
    await expect(page.locator('[data-position-id="pos-d"]')).toHaveAttribute('data-highlighted', 'true', { timeout: 8000 });
  });

  test('SC-POSGV-05 — Dashboard Card 3 opens the grace view', async ({ page }) => {
    await stubAll(page);
    await page.goto('/#/DashboardHome');
    const card = page.locator('a', { has: page.getByText('In Grace Today', { exact: true }) }).first();
    await expect(card).toHaveAttribute('href', '#/Positions?grace=open', { timeout: 15000 });
    await card.click();
    await expect(page.getByTestId('grace-period-view')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('warning-entry-grace')).toBeInViewport();
  });

  test('SC-POSGV-06 — the Risk Dashboard panel links to the grace view and lists no rows', async ({ page }) => {
    await stubAll(page);
    await page.goto('/#/RiskDashboard');
    const link = page.getByTestId('grace-panel-link');
    await expect(link).toBeVisible({ timeout: 15000 });
    await expect(page.getByText('4 positions in grace period', { exact: true })).toBeVisible();
    await expect(page.getByTestId('grace-panel-next-ends')).toHaveText('Ends today');
    await expect(page.getByRole('link', { name: /^Open .* on Positions$/ })).toHaveCount(0);
    await link.click();
    await expect(page.getByTestId('grace-period-view')).toBeVisible({ timeout: 10000 });
  });

  test('SC-POSGV-07 — "Day n of 10" appears only inside the grace view', async ({ page }) => {
    await stubAll(page);
    const DAY = /Day \d+ of 10/;
    await page.goto('/#/DashboardHome');
    await expect(page.locator('a', { has: page.getByText('In Grace Today', { exact: true }) }).first()).toBeVisible({ timeout: 15000 });
    await expect(page.getByText(DAY)).toHaveCount(0);

    await page.goto('/#/RiskDashboard');
    await expect(page.getByTestId('grace-panel-link')).toBeVisible({ timeout: 15000 });
    await expect(page.getByText(DAY)).toHaveCount(0);

    await page.goto('/#/Positions?grace=open');
    const view = page.getByTestId('grace-period-view');
    await expect(view).toBeVisible({ timeout: 10000 });
    const inView = await view.getByText(DAY).count();
    expect(inView).toBe(5);
    await expect(page.getByText(DAY)).toHaveCount(inView);
    // Table view, rows collapsed: still only the grace view.
    await page.getByRole('button', { name: 'Table view' }).click();
    await expect(page.getByTestId('position-row').first()).toBeVisible();
    await expect(page.getByText(DAY)).toHaveCount(inView);
  });

  for (const theme of ['light', 'dark']) {
    test(`SC-POSGV-08 — Risk Dashboard grace panel colour contrast (${theme})`, async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await stubAll(page);
      await page.goto('/#/RiskDashboard');
      await expect(page.getByTestId('grace-panel-link')).toBeVisible({ timeout: 15000 });
      const panel = page.locator('div.rounded-2xl', { has: page.getByTestId('grace-panel-link') });
      await expect(panel).toHaveCount(1);
      const results = await new AxeBuilder({ page })
        .include('[data-testid="grace-panel-link"]')
        .include('[data-testid="grace-panel-next-ends"]')
        .withRules(['color-contrast']).analyze();
      expect(results.violations).toEqual([]);
    });
  }
});
