/**
 * Trade History summary win rate — break-even trades
 * ST-15 (EPIC-03, v9.15) — BLG-FE-239
 *
 * metrics_definitions.md §Win Rate: win_rate = count(pnl > 0) / total_trades × 100.
 * §Risk/Reward Ratio: a pnl = 0 trade is in neither Avg Win nor Avg Loss.
 *
 *   SC-THWR-01  Trades of P&L +10, 0 and −10 show a 33.3% win rate (AC 1)
 *   SC-THWR-02  The break-even trade counts in Total Trades but not as W or L (1W / 1L)
 *   SC-THWR-03  Avg Winner and Avg Loser exclude the break-even trade (+£10.00 / −£10.00)
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter. Navigate via page.goto('/#/TradeHistory').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

function trade(id, ticker, pnl, exitDate) {
  return {
    id,
    ticker,
    market: 'UK',
    entry_date: '2026-09-01',
    exit_date: exitDate,
    entry_price: 100.0,
    exit_price: 100.0 + pnl / 10,
    shares: 10,
    pnl,
    pnl_pct: pnl / 10,
    pnl_percent: pnl / 10,
    fee_drag_pct: null,
    slippage_pct: null,
    commission_gbp: null,
    spread_cost_gbp: null,
    net_r_multiple: null,
    exit_reason: 'Manual Exit',
    tags: [],
  };
}

const TRADES = [
  trade('thwr-win', 'AAA', 10, '2026-09-10'),
  trade('thwr-even', 'BBB', 0, '2026-09-11'),
  trade('thwr-loss', 'CCC', -10, '2026-09-12'),
];

async function mockApi(page) {
  await page.route(new RegExp(`${API}/`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route(`${API}/trades`, route =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          total_trades: TRADES.length,
          win_rate: 33.3,
          total_pnl: 0,
          avg_slippage_pct: null,
          avg_fee_drag_pct: null,
          trades: TRADES,
        },
      }),
    })
  );
  await page.route(new RegExp(`${API}/trades/.+/reflection`), route =>
    route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ status: 'error' }) })
  );
  await page.route(new RegExp(`${API}/trades/.+/plan-vs-reality`), route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { plan_linked: false } }) })
  );
}

function statsCard(page, title) {
  return page
    .locator('div.rounded-2xl')
    .filter({ has: page.getByText(title, { exact: true }) })
    .first();
}

test.describe('Trade History win rate with a break-even trade (ST-15)', () => {
  test.beforeEach(async ({ page }) => {
    await mockApi(page);
    await page.goto('/#/TradeHistory');
    await expect(page.getByText('AAA').first()).toBeVisible({ timeout: 10000 });
  });

  test('SC-THWR-01: +10, 0 and −10 show a 33.3% win rate', async ({ page }) => {
    await expect(statsCard(page, 'Win Rate')).toContainText('33.3%');
  });

  test('SC-THWR-02: the break-even trade is neither a win nor a loss', async ({ page }) => {
    const total = statsCard(page, 'Total Trades');
    await expect(total).toContainText('3');
    await expect(total).toContainText('1W / 1L');
  });

  test('SC-THWR-03: Avg Winner and Avg Loser exclude the break-even trade', async ({ page }) => {
    await expect(statsCard(page, 'Avg Winner')).toContainText('10.00');
    await expect(statsCard(page, 'Avg Loser')).toContainText('10.00');
    // Under the old pnl >= 0 test Avg Winner was (10 + 0) / 2 = £5.00.
    await expect(statsCard(page, 'Avg Winner')).not.toContainText('5.00');
  });
});
