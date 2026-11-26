/**
 * Trade History rules filter — Playwright tests
 * ST-13 (EPIC-02, v9.18, BLG-FE-320). Spec: docs/specs/frontend/pages/trade_history.md v1.18 §Rules Filter;
 * metrics_definitions.md v1.36.0 §Rules Followed; design record
 * docs/design/2026-11-18__release-v9.18/rules-followed-filter/decision_record.md.
 *
 * Covers:
 *   SC-RF-01  RF-01  With followed, broken and not-known closed trades, each option shows only its trades
 *                    and the summary counts match
 *   SC-RF-02  RF-02  A legacy trade with rules_followed null (or no field) appears only under "Not known"
 *   SC-RF-03         ?rules= holds the option (replace); a summary number selects its option; the option
 *                    AND-combines with the market filter and the counts follow the other filters
 *   SC-RF-04         The expanded row shows "Rules: Followed" / "Rules: Broken: {labels}" / "Rules: Not known …"
 *   SC-RF-05         A combination with no trades shows "No trades match these filters." and Clear filters
 *   SC-RF-06         The rules option is saved with a preset and restored when it is applied
 *   SC-RF-08         The rules option is kept with the stored filters and restored on a later visit (review fix)
 *   SC-RF-07         axe: the filter and the counts have no violation and every contrast check rated (light, dark)
 *
 * Fixture shape: GET /trades rows as backend/services/trade_service.py writes them, with the
 * server-computed rules_followed / rules_broken.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

const trade = (id, ticker, market, rules_followed, rules_broken, extra = {}) => ({
  id, ticker, market, entry_date: '2026-10-01', exit_date: '2026-10-20', shares: 10, entry_price: 100, exit_price: 110,
  pnl: 100, pnl_pct: 10, pnl_percent: 10, holding_days: 19, exit_reason: 'Stop Loss Hit', entry_note: null,
  exit_note: null, tags: [], fill_price: null, slippage_pct: null, fee_drag_pct: null, commission_gbp: null,
  spread_cost_gbp: null, net_r_multiple: null, rules_followed, rules_broken, ...extra,
});

const { rules_followed: _drop, rules_broken: _drop2, ...LEGACY_BASE } = trade('t-leg', 'OLDX', 'US', null, []);
const TRADES = [
  trade('t-fol', 'FOLA', 'US', true, []),
  trade('t-fol-uk', 'FOLB.L', 'UK', true, []),
  trade('t-brk', 'BRKA', 'US', false, ['pre_entry_override', 'checklist_skipped']),
  trade('t-unk', 'UNKA', 'US', null, []),
  LEGACY_BASE, // an older payload with no rules fields at all
];

async function mockTradeHistory(page, { presets = [], onSavePreset } = {}) {
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/trades`, (route) =>
    route.fulfill(json({ status: 'ok', data: { total_trades: TRADES.length, win_rate: 100, total_pnl: 500, trades: TRADES } }))
  );
  await page.route(`${API}/saved-filters`, (route) => {
    const method = route.request().method();
    if (method === 'GET') return route.fulfill(json({ status: 'ok', data: presets }));
    if (method === 'POST') {
      const body = route.request().postDataJSON();
      onSavePreset?.(body);
      return route.fulfill(json({ status: 'ok', data: { id: 'sf-new', ...body } }));
    }
    return route.fallback();
  });
}

async function gotoTradeHistory(page, query = '') {
  await page.addInitScript(() => window.localStorage.removeItem('tradeHistory.filters'));
  await page.goto(`/#/TradeHistory${query}`);
  await expect(page.getByRole('heading', { level: 1, name: 'Trade History', exact: true })).toBeVisible({ timeout: 15000 });
  await expect(page.getByTestId('rules-summary')).toBeVisible({ timeout: 15000 });
}

const rowTickers = async (page) =>
  (await page.locator('tbody tr').filter({ has: page.locator('td') }).allInnerTexts())
    .map((t) => (t.match(/\b(FOLA|FOLB|BRKA|UNKA|OLDX)\b/) || [])[1])
    .filter(Boolean);

test('SC-RF-01: each option shows only its trades; the counts match (RF-01)', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page);

  await expect(page.getByTestId('rules-summary')).toHaveText('2 followed · 1 broken · 2 not known');
  await expect(page.getByTestId('rules-filter-all')).toHaveAttribute('aria-pressed', 'true');
  await expect.poll(async () => (await rowTickers(page)).sort()).toEqual(['BRKA', 'FOLA', 'FOLB', 'OLDX', 'UNKA']);

  await page.getByTestId('rules-filter-followed').click();
  await expect.poll(async () => (await rowTickers(page)).sort()).toEqual(['FOLA', 'FOLB']);

  await page.getByTestId('rules-filter-broken').click();
  await expect.poll(async () => (await rowTickers(page)).sort()).toEqual(['BRKA']);

  await page.getByTestId('rules-filter-unknown').click();
  await expect.poll(async () => (await rowTickers(page)).sort()).toEqual(['OLDX', 'UNKA']);
});

test('SC-RF-02: a legacy trade with no rules value appears only under "Not known" (RF-02)', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page, '?rules=followed');
  await expect.poll(async () => (await rowTickers(page)).sort()).toEqual(['FOLA', 'FOLB']);
  await page.getByTestId('rules-filter-broken').click();
  await expect.poll(async () => (await rowTickers(page)).sort()).toEqual(['BRKA']);
  await page.getByTestId('rules-filter-unknown').click();
  await expect.poll(async () => await rowTickers(page)).toContain('OLDX');
});

test('SC-RF-03: ?rules= holds the option; a count selects it; it AND-combines with Market', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page);

  await page.getByTestId('rules-summary-broken').click();
  await expect(page).toHaveURL(/rules=broken/);
  await expect(page.getByTestId('rules-filter-broken')).toHaveAttribute('aria-pressed', 'true');
  await page.getByTestId('rules-filter-all').click();
  await expect(page).not.toHaveURL(/rules=/);

  // Market UK leaves one trade; the counts follow the other filters.
  await page.getByRole('combobox', { name: 'Market' }).click();
  await page.getByRole('option', { name: 'UK' }).click();
  await expect(page.getByTestId('rules-summary')).toHaveText('1 followed · 0 broken · 0 not known');
  await page.getByTestId('rules-filter-followed').click();
  await expect.poll(async () => await rowTickers(page)).toEqual(['FOLB']);
});

test('SC-RF-04: the expanded row states the rules result in words', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page);

  await page.getByText('BRKA').first().click();
  await expect(page.getByTestId('trade-rules-line-t-brk')).toHaveText('Rules: Broken: Pre-Entry Override, Checklist Skipped');
  await page.getByText('FOLA').first().click();
  await expect(page.getByTestId('trade-rules-line-t-fol')).toHaveText('Rules: Followed');
  await page.getByText('OLDX').first().click();
  await expect(page.getByTestId('trade-rules-line-t-leg')).toHaveText('Rules: Not known (no entry check recorded)');
});

test('SC-RF-05: a combination with no trades says so and offers Clear filters', async ({ page }) => {
  await mockTradeHistory(page);
  await gotoTradeHistory(page, '?rules=broken');
  await page.getByRole('combobox', { name: 'Market' }).click();
  await page.getByRole('option', { name: 'UK' }).click();

  const empty = page.getByTestId('trades-filtered-empty');
  await expect(empty).toContainText('No trades match these filters.');
  await empty.getByRole('button', { name: 'Clear filters' }).click();
  await expect(page).not.toHaveURL(/rules=/);
  await expect.poll(async () => (await rowTickers(page)).length).toBe(5);
});

test('SC-RF-06: the rules option is saved with a preset and restored when applied', async ({ page }) => {
  let saved = null;
  const preset = { id: 'sf-1', name: 'Broken only', filter_state: { market: 'all', result: 'all', dateFrom: '', dateTo: '', tags: [], rules: 'broken' }, created_at: '2026-11-20T10:00:00Z', updated_at: '2026-11-20T10:00:00Z' };
  await mockTradeHistory(page, { presets: [preset], onSavePreset: (b) => { saved = b; } });
  await gotoTradeHistory(page);

  await page.getByTestId('rules-filter-unknown').click();
  await page.getByText('Save current filters as…').click();
  await page.getByPlaceholder('Preset name').fill('Not known');
  await page.getByRole('button', { name: 'Save', exact: true }).click();
  await expect.poll(() => saved).not.toBeNull();
  expect(saved.filter_state.rules).toBe('unknown');

  await page.locator('button[role="combobox"]').nth(2).click();
  await page.getByRole('option', { name: 'Broken only' }).click();
  await expect(page.getByTestId('rules-filter-broken')).toHaveAttribute('aria-pressed', 'true');
  await expect.poll(async () => await rowTickers(page)).toEqual(['BRKA']);
});

test('SC-RF-08: the rules option is kept with the stored filters and restored on a later visit', async ({ page }) => {
  await mockTradeHistory(page);
  // Not gotoTradeHistory: its init script clears the stored filters on every navigation.
  await page.goto('/#/TradeHistory');
  await page.evaluate(() => window.localStorage.removeItem('tradeHistory.filters'));
  await page.reload();
  await expect(page.getByTestId('rules-summary')).toBeVisible({ timeout: 15000 });
  await page.getByTestId('rules-filter-broken').click();
  await expect(page).toHaveURL(/rules=broken/);
  // Leave and come back by the sidebar route, with no query string. Journal
  // renders on the catch-all mock (Positions does not: it needs an array).
  await page.goto('/#/Journal');
  await expect(page.getByRole('heading', { level: 1, name: 'Journal', exact: true })).toBeVisible({ timeout: 15000 });
  await page.goto('/#/TradeHistory');
  await expect(page.getByTestId('rules-filter-broken')).toHaveAttribute('aria-pressed', 'true', { timeout: 15000 });
  await expect(page).toHaveURL(/rules=broken/);
  await expect.poll(async () => await rowTickers(page)).toEqual(['BRKA']);
});

for (const theme of ['light', 'dark']) {
  test(`SC-RF-07: axe passes on the rules filter and counts (${theme})`, async ({ page }) => {
    // A viewport that holds the counts: at 720 px they sit at the lower edge,
    // where axe cannot decide contrast (elmPartiallyObscuring).
    await page.setViewportSize({ width: 1280, height: 1400 });
    await page.addInitScript((t) => {
      window.localStorage.setItem('theme', t);
      window.localStorage.setItem('command-palette-tooltip-seen', 'true');
    }, theme);
    await mockTradeHistory(page);
    await gotoTradeHistory(page, '?rules=broken');
    const results = await new AxeBuilder({ page })
      .include('[data-testid="rules-filter"]')
      .include('[data-testid="rules-summary"]')
      .analyze();
    expect(results.violations).toEqual([]);
    expect(results.incomplete.filter((r) => r.id === 'color-contrast')).toEqual([]);
  });
}
