/**
 * Formatting-helper migration — ST-01 (BLG-FE-184, EPIC-01, v9.8)
 *
 * Spec: docs/specs/frontend/design_system.md v1.21 §Number and Currency Formatting
 * Allow-list: docs/design/2026-09-28__release-v9.8/ST-01-formatting-migration-allowlist.md
 *
 * ST-01 migrated the remaining toFixed()/toLocaleString() money/percent/R display
 * call sites (outside src/lib/format.js) to the shared formatCurrency/formatPercent/
 * formatR helpers, and along the way fixed ~13 pre-existing "exact-zero P&L renders
 * green" colour bugs (a `>= 0` two-way threshold instead of a `> 0`/`< 0`/neutral
 * three-way split) across several of the touched components.
 *
 * This suite is a representative sample (not exhaustive — that would require one
 * assertion per migrated file) covering the two *observable* AC bullets from
 * stage4_backlog_slice.md#ST-01:
 *   - "Zero P&L renders unsigned in the neutral tone wherever P&L is coloured"
 *   - the shared helper's canonical money/percent output shape is used at a
 *     representative migrated call site
 * The first (non-observable) AC bullet — "0 unmigrated call sites outside an
 * explicit allow-list" — is a static/code-scan criterion, verified by grep against
 * the allow-list doc at story completion, not a Playwright-testable behaviour.
 *
 * Component under test: TagPerformance (src/components/analytics/TagPerformance.js),
 * rendered on the Performance Analytics page. Chosen because it exhibits both the
 * money-format migration (formatCurrency, signed) and the zero-P&L three-way colour
 * fix in one component, keeping the mock surface small.
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PerformanceAnalytics').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API_BASE = 'http://localhost:8000';

function daysAgo(n) {
  return new Date(Date.now() - n * 86400000).toISOString();
}

function trade(o) {
  return {
    id: `t-${o.ticker}`,
    ticker: o.ticker,
    market: 'UK',
    entry_price: 100,
    exit_price: 100,
    shares: 10,
    exit_reason: 'MANUAL',
    entry_date: daysAgo(10),
    exit_date: daysAgo(2),
    holding_days: 8,
    tags: o.tags,
    pnl: o.pnl,
    ...o,
  };
}

const TRADES = [
  trade({ ticker: 'WINNER', tags: ['Breakout'], pnl: 500 }),
  trade({ ticker: 'BREAKEVEN', tags: ['Breakeven-Tag'], pnl: 0 }),
];

async function setupAnalyticsPage(page) {
  // Catch-all first (lowest priority) — see market-correlation.spec.js precedent.
  await page.route(new RegExp(`${API_BASE}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );

  await page.route(`${API_BASE}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ trades: TRADES }) })
  );

  // min_trades_for_analytics: 0 — bypasses the "need N closed trades" empty-state gate.
  await page.route(`${API_BASE}/settings`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [{ min_trades_for_analytics: 0 }] }) })
  );

  const tradesResponsePromise = page.waitForResponse((resp) => resp.url().endsWith('/trades'), { timeout: 15000 });

  await page.goto('/#/PerformanceAnalytics');
  await tradesResponsePromise;
  await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 10000 });
}

test('SC-ST01-01: TagPerformance Total P&L renders via the shared formatCurrency helper (signed, grouped, 2dp)', async ({ page }) => {
  await setupAnalyticsPage(page);

  const winnerRow = page.locator('tr', { hasText: 'Breakout' });
  await expect(winnerRow).toBeVisible({ timeout: 8000 });
  await expect(winnerRow).toContainText('+£500.00');
});

test('SC-ST01-02: TagPerformance renders an exact-zero tag P&L in the neutral tone, not emerald or rose', async ({ page }) => {
  await setupAnalyticsPage(page);

  const zeroRow = page.locator('tr', { hasText: 'Breakeven-Tag' });
  await expect(zeroRow).toBeVisible({ timeout: 8000 });

  // Total P&L and Avg P&L cells are the 4th and 5th <td> in the row.
  const cells = zeroRow.locator('td');
  const totalPnlCell = cells.nth(3);
  const avgPnlCell = cells.nth(4);

  await expect(totalPnlCell).toContainText('£0.00');
  await expect(totalPnlCell).not.toHaveClass(/text-emerald-400/);
  await expect(totalPnlCell).not.toHaveClass(/text-rose-400/);
  await expect(totalPnlCell).toHaveClass(/text-slate-300/);

  await expect(avgPnlCell).toContainText('£0.00');
  await expect(avgPnlCell).not.toHaveClass(/text-emerald-400/);
  await expect(avgPnlCell).not.toHaveClass(/text-rose-400/);
  await expect(avgPnlCell).toHaveClass(/text-slate-300/);
});
