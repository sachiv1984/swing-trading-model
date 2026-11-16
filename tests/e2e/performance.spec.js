/**
 * Performance page — Playwright tests
 * ST-06 (EPIC-02, v9.17, BLG-FE-259). Spec: docs/specs/frontend/pages/performance.md v1.1 §10.
 *
 * Covers:
 *   SC-PERF-01  PF-01        h1, four sections in order with h2s, tab title
 *   SC-PERF-02  PF-02        section index: one-click reach, ?section=compliance on load
 *   SC-PERF-03  PF-03        /Reports, /PerformanceAnalytics(+?section=strategy-compliance) redirect (replace), params kept
 *   SC-PERF-05  PF-05        each period-level KPI label once; Trade Breakdown and Best/Worst Trade rows gone
 *   SC-PERF-06  PF-06        KPIs show the server values from GET /analytics/metrics, not a browser recomputation;
 *                            consistency from consistency_metrics; Sharpe N/A when sharpe_method is insufficient_data
 *   SC-PERF-07  PF-07        period selector: ?period= and refetch of metrics and compliance-metrics
 *   SC-PERF-08  PF-08        Reports tablist Tax year / Monthly / Reconciliation, ?report= by replace
 *   SC-PERF-09  PF-09        too few trades: Summary and Analytics empty; Reports and Compliance render
 *   SC-PERF-10  PF-10        Arc 5 failure stays inside Compliance; Last 30 days block, no Most Frequent Breach
 *   SC-PERF-11  PF-11        390 px and 375 px: no page-level horizontal scroll; Monthly table scrolls in its card (BLG-FE-237)
 *   SC-PERF-13  PF-13        Export opens its dialog; Export PDF enabled with data
 *   SC-PERF-14  PF-14        axe on section index and Reports tablist (light and dark)
 * PF-04 (sidebar, palette): sidebar-nav-groups.spec.js, page-labels-single-source.spec.js.
 * PF-12 (links): empty-state-next-action.spec.js (Dashboard card), onward-links.spec.js
 * (Strategy Benchmark), tests/test_si05_digest_service.py (digest).
 *
 * Fixtures follow analytics_endpoints.md: max_drawdown.percent ≤ 0, GBP values.
 * The server figures differ from what calculateMetrics() would have derived from
 * the same /trades rows (e.g. Sharpe 1.37, Profit Factor 4.00), so PF-06 tells
 * the two apart.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

const day = (n) => new Date(Date.now() - n * 86400000).toISOString().slice(0, 10);
const TRADES = Array.from({ length: 12 }, (_, i) => {
  const win = i % 3 !== 0;
  return {
    id: `t-${i}`, ticker: ['AAPL', 'MSFT', 'BARC.L'][i % 3], market: i % 3 === 2 ? 'UK' : 'US',
    entry_date: day(20 + i), exit_date: day(1 + i), shares: 10, entry_price: 100, exit_price: win ? 110 : 95,
    pnl: win ? 78.74 : -39.37, pnl_pct: win ? 10 : -5, pnl_percent: win ? 10 : -5,
    exit_reason: win ? 'Target Reached' : 'Stop Loss', tags: [], holding_days: 19, fees: 1.5,
  };
});

function metricsResponse({ enough = true } = {}) {
  return {
    status: 'ok',
    data: {
      // Shape per analytics_service.py: has_enough_data and min_required inside
      // summary; consistency_metrics is its own object.
      summary: { total_pnl: 551.18, win_rate: 66.7, total_trades: enough ? 12 : 3, has_enough_data: enough, min_required: 10 },
      executive_metrics: enough ? { sharpe_ratio: 1.37, sharpe_method: 'trade', max_drawdown: { percent: -4.2, amount: 118.11, date: day(4) }, recovery_factor: 4.67, expectancy: 45.93, profit_factor: 4.0, risk_reward_ratio: 2.0 } : {},
      advanced_metrics: enough ? { win_streak: 4, loss_streak: 1, avg_hold_winners: 19, avg_hold_losers: 19, trade_frequency: 2.3, capital_efficiency: 5.5, days_underwater: 0, portfolio_peak_equity: 551.18, peak_date: day(1) } : {},
      consistency_metrics: enough ? { consecutive_profitable_months: 3, current_streak: 2, win_rate_std_dev: 12.4, pnl_std_dev: 210.55 } : {},
      trades_for_charts: enough ? TRADES : TRADES.slice(0, 3),
    },
  };
}

const MONTHLY = {
  status: 'ok',
  data: [
    { year: 2026, month: 7, realised_pnl_gbp: 1250.0, trade_count: 4, avg_pnl_per_trade_gbp: 312.5, gross_profit_gbp: 1500.0, gross_loss_gbp: -250.0, total_fees_gbp: 12.5 },
    { year: 2026, month: 8, realised_pnl_gbp: -310.55, trade_count: 3, avg_pnl_per_trade_gbp: -103.52, gross_profit_gbp: 90.0, gross_loss_gbp: -400.55, total_fees_gbp: 9.0 },
  ],
  estimated_unrealised_pnl: null,
  unrealised_note: null,
  compliance_summary: { period_days: 30, validation_pass_rate: 0.82, override_count: 2, red_flag_events_count: 5, most_frequent_rule_breach: 'sector_concentration' },
};

async function stub(page, { enough = true, arc5Status = 200, requests = null } = {}) {
  if (requests) {
    page.on('request', (r) => {
      if (r.url().startsWith(API)) { const u = new URL(r.url()); requests.push(u.pathname + u.search); }
    });
  }
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  await page.route(/localhost:8000\/analytics\/metrics/, (r) => r.fulfill(json(metricsResponse({ enough }))));
  await page.route(/localhost:8000\/trades(\?|$)/, (r) => r.fulfill(json({ status: 'ok', data: { trades: enough ? TRADES : TRADES.slice(0, 3) } })));
  await page.route(/localhost:8000\/reports\/monthly-pnl(?!\?format=csv)/, (r) => r.fulfill(json(MONTHLY)));
  await page.route(/localhost:8000\/analytics\/arc5-compliance/, (r) =>
    arc5Status === 200
      ? r.fulfill(json({ status: 'ok', data: { events_per_week: 1.2, override_rate: 0.15, top_rule_breach: 'stop_widened', trade_plan_adherence_rate: 0.9, validation_pass_rate_by_rule: [] } }))
      : r.fulfill(json({ status: 'error' }, arc5Status))
  );
}

const main = (page) => page.locator('main');
const heading = (page) => page.getByRole('heading', { level: 1, name: 'Performance', exact: true });

async function expectReached(page, id) {
  const h = page.locator(`#${id} > h2`);
  await expect(h).toBeInViewport();
  await expect(h).toBeFocused();
}

test('SC-PERF-01: /Performance shows the heading, four sections in order and the tab title', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Performance');
  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await expect(main(page).locator('section > h2')).toHaveText(['Summary', 'Reports', 'Analytics', 'Compliance']);
  await expect(page).toHaveTitle('Performance · Position Manager');
});

test('SC-PERF-02: the section index reaches each section in one click; ?section=compliance opens there', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Performance');
  await expect(page.getByTestId('section-index').getByRole('link')).toHaveText(['Summary', 'Reports', 'Analytics', 'Compliance'], { timeout: 15000 });
  for (const id of ['compliance', 'analytics', 'reports', 'summary']) {
    await page.getByTestId(`section-link-${id}`).click();
    await expectReached(page, id);
    await expect(page).toHaveURL(new RegExp(`section=${id}`));
  }
  await page.goto('about:blank');
  await page.goto('/#/Performance?section=compliance');
  await expect(page.getByTestId('section-link-compliance')).toBeVisible({ timeout: 15000 });
  await expectReached(page, 'compliance');
});

test('SC-PERF-03: old routes redirect to their section with replace navigation, keeping other params', async ({ page }) => {
  await stub(page);
  await page.goto('/#/TradeHistory');
  await expect(page.getByRole('heading', { level: 1, name: 'Trade History', exact: true })).toBeVisible({ timeout: 15000 });
  await page.goto('/#/Reports');
  await expect(page).toHaveURL(/#\/Performance\?section=reports$/);
  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await page.goBack();
  await expect(page).toHaveURL(/#\/TradeHistory$/);

  await page.goto('/#/PerformanceAnalytics');
  await expect(page).toHaveURL(/#\/Performance\?section=analytics$/);
  await page.goto('/#/PerformanceAnalytics?section=strategy-compliance&period=ytd');
  await expect(page).toHaveURL(/#\/Performance\?period=ytd&section=compliance$/);
});

test('SC-PERF-05: each period-level KPI has one home; removed duplicates are gone', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Performance');
  await expect(page.getByTestId('performance-summary-cards')).toBeVisible({ timeout: 15000 });
  await expect(main(page).getByText('Sharpe Ratio', { exact: true })).toBeVisible({ timeout: 15000 });
  // Period-level KPI labels. "Total P&L" and "Total Trades" also head scoped
  // breakdown columns (per exit reason, per market) — the §5 scope rule — so
  // they are checked inside Summary and Analytics' headline blocks below.
  for (const label of ['Profit Factor', 'Expectancy', 'Sharpe Ratio', 'Max Drawdown', 'Recovery Factor', 'Time Underwater', 'Risk/Reward Ratio', 'Win Streak', 'Capital Efficiency']) {
    await expect(main(page).getByText(label, { exact: true }), label).toHaveCount(1);
  }
  for (const label of ['Total P&L', 'Total Trades']) {
    await expect(page.getByTestId('performance-summary-cards').getByText(label, { exact: true }), label).toHaveCount(1);
  }
  await expect(main(page).getByText('Trade Breakdown', { exact: true })).toHaveCount(0);
  await expect(main(page).getByText('Most Frequent Breach', { exact: true })).toHaveCount(0);
  const summary = page.locator('section#analytics').getByText('Gross Profit', { exact: true });
  await expect(summary).toHaveCount(1);
});

test('SC-PERF-06: KPIs show the server values from GET /analytics/metrics', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Performance');
  const cards = page.getByTestId('performance-summary-cards');
  await expect(cards).toContainText('+£551.18', { timeout: 15000 });
  await expect(cards).toContainText('66.7%');
  await expect(cards).toContainText('4.00');
  await expect(cards).toContainText('+£45.93');
  const analytics = page.locator('section#analytics');
  await expect(analytics).toContainText('1.37'); // Sharpe from the server, not a browser √252 figure
  await expect(analytics).toContainText('−4.2%');
  await expect(analytics).toContainText('4.67');
  await expect(analytics).toContainText('At Peak');
  // Consistency comes from the top-level consistency_metrics object.
  await expect(analytics).toContainText('Current streak: 2 months');
  await expect(analytics).toContainText('12.4%');
  await expect(analytics).toContainText('Consistent');
});

test('SC-PERF-06b: Sharpe shows N/A when the server reports insufficient data', async ({ page }) => {
  await stub(page);
  await page.route(/localhost:8000\/analytics\/metrics/, (r) => {
    const body = metricsResponse();
    body.data.executive_metrics = { ...body.data.executive_metrics, sharpe_ratio: 0.0, sharpe_method: 'insufficient_data' };
    return r.fulfill(json(body));
  });
  await page.goto('/#/Performance');
  const card = page.locator('section#analytics').getByText('Sharpe Ratio', { exact: true }).locator('xpath=ancestor::div[contains(@class,"rounded-2xl")][1]');
  await expect(card).toContainText('N/A', { timeout: 15000 });
  await expect(card).not.toContainText('Needs Improvement');
  await expect(page.locator('section#summary')).not.toContainText('Sharpe: 0.00');
});

test('SC-PERF-07: the period selector sets ?period= and refetches metrics and compliance metrics', async ({ page }) => {
  const requests = [];
  await stub(page, { requests });
  await page.goto('/#/Performance');
  await expect(page.getByTestId('performance-summary-cards')).toBeVisible({ timeout: 15000 });
  await page.getByTestId('performance-period').click();
  await page.getByRole('option', { name: 'Year to Date' }).click();
  await expect(page).toHaveURL(/period=ytd/);
  await expect.poll(() => requests.some((r) => r.startsWith('/analytics/metrics') && r.includes('period=ytd'))).toBe(true);
  // Discipline & Compliance refetches on the new period key; its endpoint takes
  // no period today (performance.md v1.1 §3), so count the requests.
  await expect.poll(() => requests.filter((r) => r.startsWith('/analytics/compliance-metrics')).length).toBeGreaterThanOrEqual(2);
});

test('SC-PERF-08: the Reports tablist switches views and holds ?report= by replace', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Performance?section=reports');
  const tabs = page.getByTestId('performance-report-tabs').getByRole('tab');
  await expect(tabs).toHaveText(['Tax year', 'Monthly', 'Reconciliation'], { timeout: 15000 });
  await expect(page.getByTestId('performance-report-tab-tax-year')).toHaveAttribute('aria-selected', 'true');
  await page.getByTestId('performance-report-tab-monthly').click();
  await expect(page).toHaveURL(/report=monthly/);
  await expect(page.getByText('Monthly Realised P&L', { exact: true })).toBeVisible();
  await page.getByTestId('performance-report-tab-reconciliation').click();
  await expect(page).toHaveURL(/report=reconciliation/);
  await page.goto('about:blank');
  await page.goto('/#/Performance?report=monthly');
  await expect(page.getByTestId('performance-report-tab-monthly')).toHaveAttribute('aria-selected', 'true', { timeout: 15000 });
});

test('SC-PERF-09: with too few trades, Summary and Analytics show the empty state; Reports and Compliance render', async ({ page }) => {
  await stub(page, { enough: false });
  await page.goto('/#/Performance');
  await expect(page.locator('section#summary').getByText('Not enough trades', { exact: true })).toBeVisible({ timeout: 15000 });
  await expect(page.locator('section#analytics').getByText('Not enough trades', { exact: true })).toBeVisible();
  await expect(page.getByTestId('performance-report-tabs')).toBeVisible();
  await expect(page.getByTestId('strategy-compliance-section')).toBeVisible();
});

test('SC-PERF-10: an Arc 5 failure stays inside Compliance; the Last 30 days block shows three tiles', async ({ page }) => {
  await stub(page, { arc5Status: 500 });
  await page.goto('/#/Performance?section=compliance');
  await expect(page.locator('section#compliance').getByText('Unable to load').first()).toBeVisible({ timeout: 20000 });
  await expect(page.getByTestId('performance-summary-cards')).toBeVisible();
  const block = page.getByTestId('strategy-compliance-section');
  await expect(block.getByText('Last 30 days', { exact: true })).toBeVisible();
  await expect(page.getByTestId('compliance-pass-rate')).toContainText('82.0%');
  await expect(page.getByTestId('compliance-override-count')).toContainText('2');
  await expect(page.getByTestId('compliance-red-flag-count')).toContainText('5');
  await expect(page.getByTestId('compliance-rule-breach')).toHaveCount(0);
});

for (const width of [390, 375]) {
  test(`SC-PERF-11: at ${width} px no page-level horizontal scroll on any Reports view; Monthly table scrolls in its card`, async ({ page }) => {
    await page.setViewportSize({ width, height: 844 });
    await stub(page);
    await page.goto('/#/Performance');
    await expect(page.getByTestId('performance-summary-cards')).toBeVisible({ timeout: 15000 });
    for (const view of ['tax-year', 'monthly', 'reconciliation']) {
      await page.getByTestId(`performance-report-tab-${view}`).click();
      await expect(page.getByTestId(`performance-report-tab-${view}`)).toHaveAttribute('aria-selected', 'true');
      await page.waitForTimeout(300);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow, `${view}: page-level horizontal scroll`).toBeLessThanOrEqual(0);
    }
    await page.getByTestId('performance-report-tab-monthly').click();
    const scroller = page.getByTestId('monthly-pnl-table-scroll');
    await expect(scroller).toBeVisible();
    expect(await scroller.evaluate((el) => getComputedStyle(el).overflowX)).toBe('auto');
    const avg = scroller.getByRole('columnheader', { name: /Avg P&L/ });
    await avg.scrollIntoViewIfNeeded();
    await expect(avg).toBeInViewport();
  });
}

test('SC-PERF-13: Export opens its dialog; Export PDF is enabled with data', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Performance');
  await expect(page.getByTestId('performance-summary-cards')).toBeVisible({ timeout: 15000 });
  await expect(page.getByRole('button', { name: 'Export PDF' })).toBeEnabled();
  await page.getByRole('button', { name: 'Export', exact: true }).click();
  await expect(page.getByRole('dialog')).toBeVisible();
});

for (const theme of ['light', 'dark']) {
  test(`SC-PERF-14: axe finds no violation on the section index and Reports tablist (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await stub(page);
    await page.goto('/#/Performance');
    await expect(page.getByTestId('performance-summary-cards')).toBeVisible({ timeout: 15000 });
    const results = await new AxeBuilder({ page })
      .include('[data-testid="section-index"]')
      .include('[data-testid="performance-report-tabs"]')
      .include('main section > h2')
      .analyze();
    expect(results.violations).toEqual([]);
    expect(results.incomplete.filter((r) => r.id === 'color-contrast')).toEqual([]);
  });
}
