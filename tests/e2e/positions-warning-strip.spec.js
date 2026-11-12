/**
 * Positions warning strip — ST-03 (BLG-FE-262, EPIC-01, v9.17)
 *
 * Spec: docs/specs/frontend/pages/positions.md v2.25 §Warning Strip
 * Design: docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md §6, §10
 *
 * AC (stage4_backlog_slice.md#ST-03): with all four conditions active, one strip
 * shows four entries and each expands.
 *
 *   SC-POSWS-01  All four warnings active: one strip, four entries in the fixed
 *                order (drawdown, concentration, grace, staleness), with their summary lines
 *   SC-POSWS-02  Each entry starts collapsed; "Show details" reveals its existing
 *                content and "Hide details" closes it (aria-expanded, aria-controls)
 *   SC-POSWS-03  No warning active: no strip renders
 *   SC-POSWS-04  The strip is one "Warnings" region; the old per-warning role="alert"
 *                live regions are gone
 *   SC-POSWS-05  ?grace=open opens the grace entry
 *   SC-POSWS-06  Dismissing the drawdown review removes its entry; a single fresh
 *                staleness entry reads "Data as of …" with the UTC time as its title
 *   SC-POSWS-08  With GET /positions returning no positions, a grace-period alert still
 *                shows the grace entry, and the "next ends" date counts day 1 as today
 *   SC-POSWS-07  axe colour contrast of the strip, collapsed and with every entry open,
 *                in light and dark themes
 *
 * Mock layer: page.route(). HashRouter: navigate with '/#/…'.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;
const { stubPositionsPage, DECISION_FIXTURES } = require('./fixtures/positions-table');

const { OTHER, GRACE_BREACH } = DECISION_FIXTURES;
const json = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });

const DRAWDOWN = {
  current_drawdown_pct: 12.4,
  threshold_pct: 10.0,
  threshold_breached: true,
  portfolio_heat_pct: 6.3,
  regime_status: 'Bearish',
  positions_by_state: { GRACE: 1, PROFITABLE: 1 },
};
const CONCENTRATION = {
  any_breach: true,
  position_threshold_pct: 15.0,
  sector_threshold_pct: 30.0,
  breaching_positions: [{ ticker: 'OTHR', heat_pct: 22.1, limit_pct: 15.0 }],
  breaching_sectors: [{ sector: 'Technology', concentration_pct: 41.2, limit_pct: 30.0 }],
};
const GRACE_ALERT = {
  position_id: GRACE_BREACH.id,
  ticker: GRACE_BREACH.ticker,
  market: 'US',
  days_in_state: 9,
  grace_days_remaining: 1,
  trade_plan_id: null,
  trade_plan_summary: null,
};
const FIXED_SYNC_AT = '2026-03-29T09:41:00.000000+00:00'; // stale; title "Updated: 2026-03-29 09:41 UTC"

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function daysFromToday(n) {
  const d = new Date();
  d.setDate(d.getDate() + n);
  return `${String(d.getDate()).padStart(2, '0')} ${MONTHS[d.getMonth()]}`;
}

/**
 * Stub the Positions page with the chosen warnings active. Later page.route()
 * registrations take precedence, so these override stubPositionsPage's quiet defaults.
 */
async function gotoWithWarnings(page, {
  drawdown = true, concentration = true, grace = true, syncAt = FIXED_SYNC_AT, hash = '/#/Positions',
} = {}) {
  await stubPositionsPage(page, grace ? [OTHER, GRACE_BREACH] : [OTHER]);
  await page.route('**/portfolio/drawdown-status', (r) =>
    r.fulfill(json({ status: 'ok', data: drawdown ? DRAWDOWN : { threshold_breached: false } })));
  await page.route('**/portfolio/concentration-status', (r) =>
    r.fulfill(json({ status: 'ok', data: concentration ? CONCENTRATION : { any_breach: false } })));
  await page.route('**/positions/grace-period-alerts', (r) =>
    r.fulfill(json({ status: 'ok', data: grace ? [GRACE_ALERT] : [] })));
  await page.route('**/analytics/metrics*', (r) =>
    r.fulfill(json({ status: 'ok', data: { last_sync_at: syncAt } })));
  await page.goto(hash);
  await page.getByRole('heading', { name: 'Positions', level: 1 }).waitFor({ timeout: 10000 });
}

const strip = (page) => page.getByTestId('positions-warning-strip');
const entry = (page, kind) => page.getByTestId(`warning-entry-${kind}`);
const toggleOf = (page, kind) => entry(page, kind).getByRole('button', { name: /^(Show|Hide) details$/ });

test.describe('Positions warning strip (ST-03, BLG-FE-262)', () => {
  test('SC-POSWS-01 — all four warnings: one strip, four entries in order', async ({ page }) => {
    await gotoWithWarnings(page);
    await expect(strip(page)).toHaveCount(1);
    const kinds = await strip(page).locator('[data-testid^="warning-entry-"]').evaluateAll(
      (els) => els.map((el) => el.getAttribute('data-testid').replace('warning-entry-', '')));
    expect(kinds).toEqual(['drawdown', 'concentration', 'grace', 'staleness']);

    await expect(entry(page, 'drawdown').getByTestId('warning-summary'))
      .toHaveText('Drawdown review: 12.4% against a 10.0% threshold');
    await expect(entry(page, 'concentration').getByTestId('warning-summary'))
      .toHaveText('Concentration limit exceeded: 2 breaches');
    await expect(entry(page, 'grace').getByTestId('warning-summary'))
      // grace_days_remaining 1 is the last day of grace, so it ends today.
      .toHaveText(`1 position in grace · next ends ${daysFromToday(0)}`);
    await expect(entry(page, 'staleness').getByTestId('warning-summary'))
      .toHaveText(/^Data as of \d+ days ago — may be outdated$/);
  });

  test('SC-POSWS-02 — each entry starts collapsed and expands to its content', async ({ page }) => {
    await gotoWithWarnings(page);
    const expected = {
      drawdown: 'Portfolio Drawdown Review',
      concentration: 'Concentration Limits',
      grace: GRACE_BREACH.ticker,
      staleness: 'Updated: 2026-03-29 09:41 UTC',
    };
    for (const [kind, text] of Object.entries(expected)) {
      const btn = toggleOf(page, kind);
      await expect(btn).toHaveText('Show details');
      await expect(btn).toHaveAttribute('aria-expanded', 'false');
      // aria-controls names the detail only while it exists.
      await expect(btn).not.toHaveAttribute('aria-controls', /.*/);
      await expect(page.locator(`#warning-detail-${kind}`)).toHaveCount(0);
      await btn.click();
      await expect(btn).toHaveText('Hide details');
      await expect(btn).toHaveAttribute('aria-expanded', 'true');
      await expect(btn).toHaveAttribute('aria-controls', `warning-detail-${kind}`);
      await expect(page.locator(`#warning-detail-${kind}`)).toContainText(text);
    }
    // The existing content is unchanged inside the entries.
    await expect(page.locator('#warning-detail-concentration')).toContainText('Technology');
    await expect(page.locator('#warning-detail-concentration').getByRole('link', { name: /review.*settings/i })).toBeVisible();
    await expect(page.locator('#warning-detail-grace').getByTestId('grace-alert-day-label')).toHaveText('Day 10 of 10');
    await expect(page.locator('#warning-detail-drawdown')).toContainText('Bearish');
    // All four open at once; Hide details closes one.
    await expect(strip(page).locator('[id^="warning-detail-"]')).toHaveCount(4);
    await toggleOf(page, 'drawdown').click();
    await expect(page.locator('#warning-detail-drawdown')).toHaveCount(0);
  });

  test('SC-POSWS-03 — no warning active: no strip', async ({ page }) => {
    await gotoWithWarnings(page, { drawdown: false, concentration: false, grace: false, syncAt: null });
    await expect(page.getByRole('button', { name: 'Table view' })).toBeVisible();
    await expect(strip(page)).toHaveCount(0);
    await expect(page.getByText(/Data as of/)).toHaveCount(0);
  });

  test('SC-POSWS-04 — one "Warnings" region; no per-warning alert live regions', async ({ page }) => {
    await gotoWithWarnings(page);
    await expect(page.getByRole('region', { name: 'Warnings' })).toHaveCount(1);
    for (const kind of ['drawdown', 'concentration', 'grace', 'staleness']) await toggleOf(page, kind).click();
    await expect(strip(page).locator('[role="alert"]')).toHaveCount(0);
    await expect(strip(page).locator('[aria-live]')).toHaveCount(0);
  });

  test('SC-POSWS-05 — ?grace=open opens the grace entry', async ({ page }) => {
    await gotoWithWarnings(page, { hash: '/#/Positions?grace=open' });
    await expect(toggleOf(page, 'grace')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.locator('#warning-detail-grace').getByTestId(`grace-row-${GRACE_BREACH.ticker}`)).toBeVisible();
    await expect(entry(page, 'grace')).toBeInViewport();
    // The other entries stay collapsed.
    await expect(toggleOf(page, 'drawdown')).toHaveAttribute('aria-expanded', 'false');
  });

  test('SC-POSWS-06 — dismissing the drawdown review removes its entry; fresh staleness entry', async ({ page }) => {
    const fresh = new Date(Date.now() - 5 * 60 * 1000).toISOString();
    await gotoWithWarnings(page, { concentration: false, grace: false, syncAt: fresh });
    await expect(strip(page).locator('[data-testid^="warning-entry-"]')).toHaveCount(2);
    await toggleOf(page, 'drawdown').click();
    await page.getByRole('button', { name: /dismiss drawdown review prompt/i }).click();
    await expect(entry(page, 'drawdown')).toHaveCount(0);
    const summary = entry(page, 'staleness').getByTestId('warning-summary');
    await expect(summary).toHaveText(/^Data as of \d+ mins ago$/);
    await expect(summary.locator('[title^="Updated: "]')).toHaveCount(1);
  });

  test('SC-POSWS-08 — grace-period alerts alone show the grace entry', async ({ page }) => {
    await stubPositionsPage(page, []);
    await page.route('**/positions/grace-period-alerts', (r) =>
      r.fulfill(json({ status: 'ok', data: [{ ...GRACE_ALERT, grace_days_remaining: 2 }] })));
    await page.goto('/#/Positions');
    // Two days left: the last day is tomorrow.
    await expect(entry(page, 'grace').getByTestId('warning-summary'))
      .toHaveText(`1 position in grace · next ends ${daysFromToday(1)}`, { timeout: 8000 });
    await toggleOf(page, 'grace').click();
    await expect(page.locator('#warning-detail-grace').getByTestId('grace-alert-day-label')).toHaveText('Day 9 of 10');
  });

  for (const theme of ['light', 'dark']) {
    test(`SC-POSWS-07 — strip colour contrast (${theme})`, async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await gotoWithWarnings(page);
      await expect(strip(page)).toBeVisible();
      const collapsed = await new AxeBuilder({ page })
        .include('[data-testid="positions-warning-strip"]').withRules(['color-contrast']).analyze();
      expect(collapsed.violations).toEqual([]);
      // Every entry open, including the grace view (ST-04).
      for (const kind of ['drawdown', 'concentration', 'grace', 'staleness']) await toggleOf(page, kind).click();
      const open = await new AxeBuilder({ page })
        .include('[data-testid="positions-warning-strip"]')
        .withRules(['color-contrast']).analyze();
      expect(open.violations).toEqual([]);
    });
  }
});
