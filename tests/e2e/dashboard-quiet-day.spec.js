/**
 * Quiet-day Dashboard — Playwright tests
 * ST-09 (EPIC-02, v9.18, BLG-UX-11). Spec: docs/specs/frontend/pages/dashboard.md v4.4 §3A;
 * design record docs/design/2026-11-18__release-v9.18/dashboard-quiet-day/decision_record.md §2.
 *
 * Covers:
 *   SC-QD-01a/b  QD-01  Quiet-day fixture: below "Due today" only the "Nothing to show" line, listing all
 *                       11 names in table order; no briefing panel, no card rows, no empty-state card (light, dark)
 *   SC-QD-02     QD-02  One open position: Cards 1 and 2 keep their v4.0 positions in Row 1, Card 3 folds,
 *                       the line lists the other folded names
 *   SC-QD-03     QD-03  Each link entry has its target; "AI briefing" reveals the AI Daily Briefing card
 *                       with Regenerate and sets aria-expanded="true"; "What's new" does the same
 *   SC-QD-03b           The revealed "AI briefing" entry stays in the line while Regenerate runs (review fix)
 *   SC-QD-04     QD-04  A failing element shows its error in place and is not in the line
 *                       (the Screener Hits card reads GET /signals, so that request fails)
 *   SC-QD-04b    QD-04  A failed earnings lookup (data_status unavailable) shows the Earnings error, not a fold
 *   SC-QD-05            An element still loading shows its skeleton and joins the line once loaded
 *   SC-QD-06            axe on the quiet-day page (light, dark): no serious or critical violation
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

const ALL_NAMES = [
  'Screener hits', 'Positions to watch', 'Red flags', 'Earnings', 'Compliance', 'AI briefing',
  'Open positions', 'Portfolio heat', 'In grace', 'Recent activity', "What's new",
];

// Quiet day: every source loads and is empty.
async function mockQuietDay(page) {
  await page.route(new RegExp(`${API}/`), (route) => {
    const url = route.request().url();
    if (url.includes('/market/status')) {
      return route.fulfill(json({ status: 'ok', data: { spy: { is_risk_on: true }, ftse: { is_risk_on: true } } }));
    }
    if (/\/positions(\?|$)/.test(url)) return route.fulfill(json([]));
    return route.fulfill(json({ status: 'ok', data: [] }));
  });
}

const line = (page) => page.getByTestId('dashboard-nothing-to-show');

async function gotoDashboard(page) {
  await page.goto('/#/');
  await expect(page.getByRole('heading', { level: 1, name: 'Dashboard', exact: true })).toBeVisible({ timeout: 15000 });
}

for (const theme of ['light', 'dark']) {
  test(`SC-QD-01${theme === 'light' ? 'a' : 'b'}: quiet day folds every element into one line (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await mockQuietDay(page);
    await gotoDashboard(page);

    await expect(line(page)).toHaveText(`Nothing to show: ${ALL_NAMES.join(' · ')}`, { timeout: 15000 });
    const entries = line(page).locator('a, button');
    await expect(entries).toHaveText(ALL_NAMES);

    // Nothing else below "Due today" is an empty-state element.
    await expect(page.getByTestId('dashboard-briefing-panel')).toBeHidden();
    await expect(page.getByTestId('dashboard-status-row')).toBeHidden();
    await expect(page.getByTestId('ai-daily-briefing-card')).toHaveCount(0);
    await expect(page.getByTestId('whats-new-card')).toHaveCount(0);
    for (const heading of ['No open positions', 'No positions in grace', 'No recent activity', 'No portfolio heat data',
      'No new signals', 'No positions to watch', 'No red flags this week', 'No earnings in 7 days', 'No compliance data yet',
      'No briefing for today']) {
      await expect(page.getByText(heading, { exact: true })).toHaveCount(0);
    }
    // The line sits directly below the Today list.
    const todayBox = await page.getByTestId('today-list').boundingBox();
    const lineBox = await line(page).boundingBox();
    expect(lineBox.y).toBeGreaterThanOrEqual(todayBox.y + todayBox.height);
  });
}

test('SC-QD-02: a card with data keeps its v4.0 position; Card 3 folds', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await mockQuietDay(page);
  await page.route(/localhost:8000\/positions(\?|$)/, (r) => r.fulfill(json([
    { id: 'p1', ticker: 'AAPL', market: 'US', status: 'open', pnl: 12.5, grace_period: false, grace_days_remaining: null, current_price: 190, current_trailing_stop: 170 },
  ])));
  await page.route(/localhost:8000\/portfolio(\?|$)/, (r) => r.fulfill(json({ status: 'ok', data: { portfolio_heat_percent: 0.8, positions: [] } })));
  await gotoDashboard(page);

  const row = page.getByTestId('dashboard-status-row');
  await expect(row).toBeVisible({ timeout: 15000 });
  const titles = row.locator('p.uppercase');
  await expect(titles).toHaveText(['Open Positions', 'Portfolio Heat']);
  // Two cards share Row 1 left to right with no gap: Card 1 first.
  const [b1, b2] = await Promise.all([titles.nth(0).boundingBox(), titles.nth(1).boundingBox()]);
  expect(Math.abs(b1.y - b2.y)).toBeLessThan(2);
  expect(b1.x).toBeLessThan(b2.x);
  await expect(row).toHaveClass(/md:grid-cols-2/);

  await expect(line(page).locator('a, button')).toHaveText(
    ALL_NAMES.filter((n) => n !== 'Open positions' && n !== 'Portfolio heat')
  );
});

test('SC-QD-03: line entries go to their targets; the disclosure entries reveal their cards', async ({ page }) => {
  await mockQuietDay(page);
  await gotoDashboard(page);
  await expect(line(page)).toBeVisible({ timeout: 15000 });

  const targets = {
    'screener-hits': '#/Screener',
    'positions-to-watch': '#/Positions?grace=open',
    'red-flags': '#/Journal?section=red-flags',
    earnings: '#/Positions',
    compliance: '#/Performance?section=compliance',
    'open-positions': '#/Positions',
    'portfolio-heat': '#/RiskDashboard',
    'in-grace': '#/Positions?grace=open',
    'recent-activity': '#/TradeHistory',
  };
  for (const [key, href] of Object.entries(targets)) {
    await expect(page.getByTestId(`nothing-to-show-${key}`)).toHaveAttribute('href', href);
  }

  const ai = page.getByTestId('nothing-to-show-ai-briefing');
  await expect(ai).toHaveAttribute('aria-expanded', 'false');
  await ai.click();
  await expect(ai).toHaveAttribute('aria-expanded', 'true');
  await expect(ai).toBeFocused();
  await expect(page.getByTestId('dashboard-briefing-panel')).toBeVisible();
  await expect(page.getByTestId('ai-daily-briefing-card')).toBeVisible();
  await expect(page.getByTestId('regenerate-briefing-btn')).toBeVisible();
  // Its name stays in the line, now expanded.
  await expect(line(page).locator('a, button')).toHaveText(ALL_NAMES);

  const wn = page.getByTestId('nothing-to-show-whats-new');
  await wn.click();
  await expect(wn).toHaveAttribute('aria-expanded', 'true');
  await expect(page.getByTestId('whats-new-card')).toBeVisible();

  await page.getByTestId('nothing-to-show-red-flags').click();
  await expect(page).toHaveURL(/#\/Journal\?section=red-flags$/);
});

test('SC-QD-04: a failing element shows its error in place and is not in the line', async ({ page }) => {
  await mockQuietDay(page);
  await page.route(/localhost:8000\/signals(\?|$)/, (r) => r.fulfill(json({ status: 'error', message: 'boom' }, 500)));
  await gotoDashboard(page);

  await expect(line(page)).toBeVisible({ timeout: 15000 });
  const briefing = page.getByTestId('morning-briefing');
  await expect(briefing).toBeVisible({ timeout: 15000 });
  await expect(briefing.getByText('Screener Hits', { exact: true })).toBeVisible();
  await expect(briefing.getByText('Unable to load')).toBeVisible({ timeout: 15000 });
  await expect(page.getByTestId('nothing-to-show-screener-hits')).toHaveCount(0);
  await expect(line(page).locator('a, button')).toHaveText(ALL_NAMES.filter((n) => n !== 'Screener hits'));
});

test('SC-QD-04b: a failed earnings lookup is an error, not "nothing to show"', async ({ page }) => {
  await mockQuietDay(page);
  await page.route(/localhost:8000\/positions(\?|$)/, (r) => r.fulfill(json([
    { id: 'p1', ticker: 'AAPL', market: 'US', status: 'open', pnl: 12.5, grace_period: false, grace_days_remaining: null },
  ])));
  await page.route(/localhost:8000\/earnings\//, (r) => r.fulfill(json({ ticker: 'AAPL', days_until_earnings: null, data_status: 'unavailable' })));
  await gotoDashboard(page);

  const briefing = page.getByTestId('morning-briefing');
  await expect(briefing.getByText('Earnings', { exact: true })).toBeVisible({ timeout: 15000 });
  await expect(briefing.getByText('Unable to load')).toBeVisible();
  await expect(page.getByTestId('nothing-to-show-earnings')).toHaveCount(0);
});

test('SC-QD-03b: the revealed "AI briefing" entry stays in the line while Regenerate runs', async ({ page }) => {
  await mockQuietDay(page);
  await page.route(/localhost:8000\/ai\/daily-briefing/, async (r) => {
    await new Promise((resolve) => setTimeout(resolve, 1500));
    await r.fulfill(json({ status: 'error', message: 'no key' }, 503));
  });
  await gotoDashboard(page);
  const ai = page.getByTestId('nothing-to-show-ai-briefing');
  await ai.click({ timeout: 15000 });
  await expect(ai).toHaveAttribute('aria-controls', 'dashboard-ai-briefing');
  await page.getByTestId('regenerate-briefing-btn').click();
  await expect(page.getByTestId('briefing-loading')).toBeVisible();
  await expect(ai).toBeVisible();
  await expect(ai).toHaveAttribute('aria-expanded', 'true');
});

test('SC-QD-05: an element still loading shows its skeleton and joins the line once loaded', async ({ page }) => {
  await mockQuietDay(page);
  let release;
  const gate = new Promise((resolve) => { release = resolve; });
  await page.route(/localhost:8000\/trades(\?|$)/, async (r) => {
    await gate;
    await r.fulfill(json({ status: 'ok', data: { trades: [] } }));
  });
  await gotoDashboard(page);

  await expect(page.getByTestId('nothing-to-show-open-positions')).toBeVisible({ timeout: 15000 });
  await expect(page.getByTestId('nothing-to-show-recent-activity')).toHaveCount(0);
  await expect(page.getByText('Recent Activity', { exact: true })).toBeVisible();
  release();
  await expect(page.getByTestId('nothing-to-show-recent-activity')).toBeVisible({ timeout: 15000 });
  await expect(page.getByText('Recent Activity', { exact: true })).toHaveCount(0);
});

for (const theme of ['light', 'dark']) {
  test(`SC-QD-06: axe finds no serious or critical violation on the quiet day (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => {
      window.localStorage.setItem('theme', t);
      window.localStorage.setItem('command-palette-tooltip-seen', 'true');
    }, theme);
    await mockQuietDay(page);
    await gotoDashboard(page);
    await expect(line(page)).toBeVisible({ timeout: 15000 });
    const results = await new AxeBuilder({ page }).include('main').analyze();
    const blocking = results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
    expect(blocking.map((v) => v.id)).toEqual([]);
    // The line itself: every contrast check decided.
    const lineResults = await new AxeBuilder({ page }).include('[data-testid="dashboard-nothing-to-show"]').withRules(['color-contrast']).analyze();
    expect(lineResults.violations).toEqual([]);
    expect(lineResults.incomplete).toEqual([]);
  });
}
