/**
 * In-page section index — Playwright tests
 * ST-07 (EPIC-02, v9.17, BLG-FE-263). Specs: trade_plan.md v1.28 §5g,
 * strategy_benchmark.md v0.11 §3a (both with their build notes); design source
 * docs/design/2026-11-11__release-v9.17/long-page-section-index/decision_record.md §2, §3, §7.
 *
 * Covers:
 *   SC-SIX-01  Trade Plan lists its sections in order; What-if sizing only while the stop is a positive number
 *   SC-SIX-02  Trade Plan: each link reaches its heading in one click, focuses it, sets ?section= (replace), keeps the other params
 *   SC-SIX-03  Trade Plan: ?section=rules opens at Rules; an unknown id does nothing
 *   SC-SIX-04  aria-current moves after scrolling to a later section (IntersectionObserver)
 *   SC-SIX-05  Trade Plan at 390 px: sticky pill row (44 px links), no page-level horizontal scroll
 *   SC-SIX-06  Strategy Benchmark: index on the Benchmark tab only, four sections, one-click reach,
 *              ?section=trade-log on load, ignored on the other tabs; Open positions left out when empty
 *   SC-SIX-07  Strategy Benchmark at 390 px: no page-level horizontal scroll
 *   SC-SIX-08  axe: the index has no violation and no unrated colour contrast (light and dark)
 *   SC-SIX-09  link hrefs are real hash-router URLs; the What-if panel keeps its inputs across a stop edit;
 *              a reachable jump does not pin aria-current; a tab switch drops ?section=
 *
 * "Reaches its heading": the heading is in the viewport, and in the top quarter
 * unless the page is already scrolled to its end (the last sections of a page
 * cannot scroll higher than the document allows).
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

const PLAN_IDS = ['basics', 'setup', 'entry', 'thesis', 'rules', 'sizing', 'checklist'];
const PLAN_LABELS = ['Basics', 'Signal and setup', 'Entry, stop and size', 'Thesis', 'Rules', 'What-if sizing', 'Checklist'];
const PLAN_URL = '/#/TradePlan?ticker=NVDA&market=US';

async function mockTradePlan(page) {
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(json({ status: 'ok', data: { spy: { price: 521, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7200, is_risk_on: true }, fx_rate: 1.27 } }))
  );
  await page.route(new RegExp(`${API}/portfolio/pre-entry-validation`), (r) =>
    r.fulfill(json({ status: 'ok', data: { advisory_status: 'pass', checks: [{ rule: 'regime_gate', status: 'pass', detail: 'US market is risk-on' }] } }))
  );
}

// Benchmark fixtures: enough rows that every panel, the trade log included,
// can scroll towards the top of the viewport.
const YEARS = [2019, 2020, 2021, 2022, 2023, 2024, 2025];
const SUMMARY = {
  filters: { year: null, market: 'ALL' },
  last_imported_at: '2026-06-30T10:15:00Z',
  available_years: YEARS,
  backtest_stats: { total_trades: 60, win_rate_pct: 61.7, avg_pnl_gbp: 205.25, total_pnl_gbp: 12315.0, avg_hold_days: 14.1 },
  actual_stats: { total_trades: 6, win_rate_pct: 66.7, avg_pnl_gbp: 180.3, total_pnl_gbp: 1081.8, avg_hold_days: 11.5 },
  yearly_breakdown: YEARS.map((y, i) => ({ entry_year: y, num_trades: 8 + i, avg_pnl_gbp: 150 + i * 10.5, total_pnl_gbp: (8 + i) * (150 + i * 10.5), avg_hold_days: 12 + i * 0.5, win_rate_pct: 55 + i })),
};
const TRADES = {
  filters: { year: null, market: 'ALL' },
  backtest_trades: Array.from({ length: 30 }, (_, i) => {
    const entry = 100 + i;
    const exit = entry * (i % 3 === 0 ? 0.95 : 1.08);
    return {
      id: i + 1, ticker: ['NVDA', 'MSFT', 'BARC'][i % 3], market: i % 3 === 2 ? 'UK' : 'US',
      entry_date: `2023-0${(i % 9) + 1}-01`, exit_date: `2023-0${(i % 9) + 1}-20`, holding_days: 19,
      entry_price: entry, exit_price: Number(exit.toFixed(2)), pnl_gbp: Number(((exit - entry) * 10 / 1.27).toFixed(2)),
      pnl_pct: Number(((exit - entry) / entry * 100).toFixed(2)), exit_reason: i % 3 === 0 ? 'Stop' : 'Rebalance',
      was_profitable: i % 3 !== 0, entry_year: 2023,
    };
  }),
  actual_trades: [],
};
const OPEN_POSITIONS = {
  filters: { market: 'ALL' },
  open_positions: [{ ticker: 'TSLA', market: 'US', entry_date: '2026-06-01', entry_price: 210.0, current_price: 228.5, unrealized_pnl_gbp: 145.67, unrealized_pnl_pct: 8.81, days_held: 32 }],
  summary: { count: 1, total_unrealized_pnl_gbp: 145.67 },
};

async function mockBenchmark(page, { openPositions = OPEN_POSITIONS } = {}) {
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  await page.route(/\/strategy\/benchmark\/open-positions/, (r) => r.fulfill(json(openPositions)));
  await page.route(/\/strategy\/benchmark\/summary/, (r) => r.fulfill(json(SUMMARY)));
  await page.route(/\/strategy\/benchmark\/trades/, (r) => r.fulfill(json(TRADES)));
}

const index = (page) => page.getByTestId('section-index');

async function expectReached(page, id) {
  const heading = page.locator(`#${id}`).locator('h1, h2, h3, h4').first();
  await expect(heading).toBeInViewport();
  const { y, vh, atEnd } = await heading.evaluate((el) => ({
    y: el.getBoundingClientRect().top,
    vh: window.innerHeight,
    atEnd: Math.ceil(window.scrollY + window.innerHeight) >= document.documentElement.scrollHeight - 1,
  }));
  if (!atEnd) expect(y, `${id}: heading top in the top quarter`).toBeLessThanOrEqual(vh / 4);
  await expect(heading).toBeFocused();
  // Not covered by a sticky bar or the index: the top element at the heading's
  // centre is the heading itself (or inside it).
  const uncovered = await heading.evaluate((el) => {
    const r = el.getBoundingClientRect();
    const hit = document.elementFromPoint(r.left + Math.min(r.width / 2, 40), r.top + r.height / 2);
    return !!hit && (hit === el || el.contains(hit));
  });
  expect(uncovered, `${id}: heading is covered`).toBe(true);
}

// ---------------------------------------------------------------------------
// Trade Plan
// ---------------------------------------------------------------------------

test('SC-SIX-01: Trade Plan lists its sections in order; What-if sizing only with a positive stop', async ({ page }) => {
  await mockTradePlan(page);
  await page.goto(PLAN_URL);
  const links = index(page).getByRole('link');
  await expect(links).toHaveCount(6, { timeout: 15000 });
  await expect(links).toHaveText(PLAN_LABELS.filter((l) => l !== 'What-if sizing'));
  for (const id of PLAN_IDS.filter((i) => i !== 'sizing')) {
    await expect(page.locator(`section#${id} h2`)).toBeVisible();
  }

  const stop = page.getByTestId('planned-stop-price-input');
  for (const bad of ['0', '-1']) {
    await stop.fill(bad);
    await expect(page.getByTestId('section-link-sizing')).toHaveCount(0);
  }
  await stop.fill('140');
  await expect(links).toHaveText(PLAN_LABELS);
  await expect(page.getByTestId('what-if-sizing-preview-panel')).toBeVisible();
  await stop.fill('');
  await expect(page.getByTestId('section-link-sizing')).toHaveCount(0);
  await expect(page.locator('section#sizing')).toBeHidden(); // kept mounted, hidden (SC-SIX-09)
});

test('SC-SIX-02: each Trade Plan link reaches its heading in one click, focuses it and sets ?section=', async ({ page }) => {
  await mockTradePlan(page);
  await page.goto(PLAN_URL);
  await page.getByTestId('planned-stop-price-input').fill('140');
  await expect(index(page).getByRole('link')).toHaveCount(7, { timeout: 15000 });
  for (const id of [...PLAN_IDS].reverse()) {
    await page.getByTestId(`section-link-${id}`).click();
    await expectReached(page, id);
    await expect(page).toHaveURL(new RegExp(`section=${id}(&|$)`));
    await expect(page).toHaveURL(/ticker=NVDA/);
    await expect(page.getByTestId(`section-link-${id}`)).toHaveAttribute('aria-current', 'true');
  }
  // Replace navigation: Back leaves the page rather than stepping through sections.
  expect(await page.evaluate(() => window.history.length)).toBeLessThanOrEqual(2);
});

test('SC-SIX-03: ?section=rules opens Trade Plan at Rules; an unknown id does nothing', async ({ page }) => {
  await mockTradePlan(page);
  await page.goto(`${PLAN_URL}&section=rules`);
  await expect(page.getByTestId('section-link-rules')).toBeVisible({ timeout: 15000 });
  await expectReached(page, 'rules');

  await page.goto('about:blank'); // a hash-only change would keep the scroll position
  await page.goto(`${PLAN_URL}&section=nowhere`);
  await expect(page.getByTestId('section-link-basics')).toBeVisible({ timeout: 15000 });
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
  await expect(page.getByTestId('section-link-basics')).toHaveAttribute('aria-current', 'true');
});

test('SC-SIX-04: aria-current follows the page after scrolling to a later section', async ({ page }) => {
  await mockTradePlan(page);
  await page.goto(PLAN_URL);
  await expect(page.getByTestId('section-link-basics')).toHaveAttribute('aria-current', 'true', { timeout: 15000 });
  await page.locator('#thesis h2').evaluate((el) => el.scrollIntoView({ block: 'start' }));
  await expect(page.getByTestId('section-link-thesis')).toHaveAttribute('aria-current', 'true');
  await expect(page.getByTestId('section-link-basics')).not.toHaveAttribute('aria-current', 'true');
  await page.evaluate(() => window.scrollTo(0, 0));
  await expect(page.getByTestId('section-link-basics')).toHaveAttribute('aria-current', 'true');
});

test('SC-SIX-05: at 390 px the Trade Plan index is a sticky pill row and the page does not scroll sideways', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await mockTradePlan(page);
  await page.goto(PLAN_URL);
  await page.getByTestId('planned-stop-price-input').fill('140');
  await expect(index(page).getByRole('link')).toHaveCount(7, { timeout: 15000 });
  for (const id of PLAN_IDS) {
    const box = await page.getByTestId(`section-link-${id}`).boundingBox();
    expect(box.height, `${id}: link height`).toBeGreaterThanOrEqual(44);
  }
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(0);

  await page.getByTestId('section-link-checklist').click();
  await expectReached(page, 'checklist');
  // Sticky under the fixed 64 px mobile header.
  const navBox = await index(page).boundingBox();
  expect(Math.round(navBox.y)).toBe(64);
});

// ---------------------------------------------------------------------------
// Strategy Benchmark
// ---------------------------------------------------------------------------

test('SC-SIX-06: Strategy Benchmark has the index on the Benchmark tab only, with one-click reach', async ({ page }) => {
  await mockBenchmark(page);
  await page.goto('/#/StrategyBenchmark');
  const links = index(page).getByRole('link');
  await expect(links).toHaveText(['Open positions', 'Performance parity', 'Yearly breakdown', 'Trade log'], { timeout: 15000 });
  for (const id of ['trade-log', 'yearly', 'parity', 'open-positions']) {
    await page.getByTestId(`section-link-${id}`).click();
    await expectReached(page, id);
    await expect(page).toHaveURL(new RegExp(`section=${id}(&|$)`));
  }

  await page.getByTestId('benchmark-tab-version-comparison').click();
  await expect(page).toHaveURL(/tab=version-comparison/);
  await expect(index(page)).toHaveCount(0);

  await page.goto('/#/StrategyBenchmark?tab=backtest-rule-change&section=trade-log');
  await expect(page.getByTestId('benchmark-tab-backtest-rule-change')).toHaveAttribute('aria-selected', 'true', { timeout: 15000 });
  await expect(index(page)).toHaveCount(0);
});

test('SC-SIX-06b: ?section=trade-log opens the Benchmark tab at the trade log; empty Open positions is left out', async ({ page }) => {
  await mockBenchmark(page, { openPositions: { filters: { market: 'ALL' }, open_positions: [], summary: { count: 0, total_unrealized_pnl_gbp: null } } });
  await page.goto('/#/StrategyBenchmark?section=trade-log');
  await expect(index(page).getByRole('link')).toHaveText(['Performance parity', 'Yearly breakdown', 'Trade log'], { timeout: 15000 });
  await expectReached(page, 'trade-log');
});

test('SC-SIX-07: Strategy Benchmark at 390 px has no page-level horizontal scroll', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await mockBenchmark(page);
  await page.goto('/#/StrategyBenchmark');
  await expect(index(page).getByRole('link')).toHaveCount(4, { timeout: 15000 });
  await page.getByTestId('section-link-trade-log').click();
  await expectReached(page, 'trade-log');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(0);
});

for (const theme of ['light', 'dark']) {
  test(`SC-SIX-08: the section index passes axe with every contrast check rated (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await mockBenchmark(page);
    await page.goto('/#/StrategyBenchmark');
    await expect(index(page).getByRole('link')).toHaveCount(4, { timeout: 15000 });
    const results = await new AxeBuilder({ page }).include('[data-testid="section-index"]').analyze();
    expect(results.violations).toEqual([]);
    expect(results.incomplete.filter((r) => r.id === 'color-contrast')).toEqual([]);
  });
}

test('SC-SIX-09: real link hrefs; What-if inputs survive a stop edit; no pin after a reachable jump', async ({ page }) => {
  await mockTradePlan(page);
  await page.goto(PLAN_URL);
  await expect(page.getByTestId('section-link-rules')).toHaveAttribute('href', '#/TradePlan?ticker=NVDA&market=US&section=rules', { timeout: 15000 });

  const stop = page.getByTestId('planned-stop-price-input');
  await stop.fill('140');
  await page.getByTestId('what-if-entry-price-input').fill('150');
  await stop.fill('');
  await expect(page.getByTestId('section-link-sizing')).toHaveCount(0);
  await expect(page.locator('section#sizing')).toBeHidden();
  await stop.fill('140');
  await expect(page.getByTestId('what-if-entry-price-input')).toHaveValue('150');

  // Rules can reach the top quarter, so scrolling back up moves aria-current at once.
  await page.getByTestId('section-link-rules').click();
  await expect(page.getByTestId('section-link-rules')).toHaveAttribute('aria-current', 'true');
  await page.locator('#thesis h2').evaluate((el) => el.scrollIntoView({ block: 'start' }));
  await expect(page.getByTestId('section-link-thesis')).toHaveAttribute('aria-current', 'true');
});

test('SC-SIX-09b: switching Strategy Benchmark tabs drops ?section=, so returning does not jump', async ({ page }) => {
  await mockBenchmark(page);
  await page.goto('/#/StrategyBenchmark');
  await page.getByTestId('section-link-trade-log').click({ timeout: 15000 });
  await expect(page).toHaveURL(/section=trade-log/);
  await page.getByTestId('benchmark-tab-version-comparison').click();
  await expect(page).not.toHaveURL(/section=/);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.getByTestId('benchmark-tab-benchmark').click();
  await expect(index(page).getByRole('link')).toHaveCount(4, { timeout: 15000 });
  await page.waitForTimeout(300);
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
});
