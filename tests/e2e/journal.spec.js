/**
 * Journal page — Playwright tests
 * ST-05 (EPIC-02, v9.17, BLG-FE-258). Spec: docs/specs/frontend/pages/journal.md v1.1 §7.
 *
 * Covers:
 *   SC-JNL-01  JA-01, JA-14  heading, tab order, opens on Reflections, tab title
 *   SC-JNL-02  JA-02         ?section= opens a tab; unknown value opens Reflections
 *   SC-JNL-03  JA-03         selecting a tab replaces ?section= (Back leaves the Journal)
 *   SC-JNL-04  JA-04         ARIA tablist, Left/Right arrows, axe scan of the tabs (light and dark)
 *   SC-JNL-05  JA-05         counts only once a section has loaded; none while loading or on error
 *   SC-JNL-06  JA-06, JA-16  shared ticker filter: pre-filled from ?ticker=, kept across tabs,
 *                            key-by-key typing (06c),
 *                            partial and ".L"-blind in the browser, exact upper-cased for red flags
 *   SC-JNL-07  JA-07         Reflections grid, both empty states, loading, reflection modal
 *   SC-JNL-08  JA-08         Red flags list, its own filters, pagination, empty and error states
 *   SC-JNL-09  JA-09         Position notes: open and closed cards, four filters, both empty states, GBP P&L
 *   SC-JNL-10  JA-10         item links; no nested-interactive violation on Reflections
 *   SC-JNL-11  JA-11         a red-flag 500 shows in its panel only; other tabs still load
 *   SC-JNL-12  JA-12, JA-18  old routes redirect (replace), keeping the query string
 *   SC-JNL-13  JA-13, JA-21  Positions: no journal view, heading "Positions", "Position notes" link
 *   SC-JNL-15  JA-15         no /ai/ request from any tab
 *   SC-JNL-17  JA-17         red flags refetch 300 ms after typing stops, at once on Enter;
 *                            a saved ticker in localStorage is ignored
 *   SC-JNL-19  JA-19         a section's data is requested only when its tab is first opened
 *   SC-JNL-20  JA-20         at 375 px: tabs scroll, filter full width, no page-level horizontal scroll
 *
 * JA-14's sidebar and palette parts are in sidebar-nav-groups.spec.js (SC-SNV-08)
 * and page-labels-single-source.spec.js (SC-PL-01/02).
 *
 * Fixtures follow the contracts: GET /positions returns open positions only (raw
 * array; pnl in GBP), GET /trades returns closed trades with notes and tags
 * (trade_endpoints.md; pnl in GBP). US P&L is the native gain divided by an
 * FX rate, so the rounding is not exact.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';

// US: (110 - 100) * 7 / 1.27 = 55.118… → 55.12 GBP. UK in pounds.
const TRADES = [
  { id: 't-aapl', ticker: 'AAPL', market: 'US', entry_date: '2026-09-01', exit_date: '2026-09-20', shares: 7, entry_price: 100, exit_price: 110, pnl: 55.12, pnl_pct: 10, pnl_percent: 10, holding_days: 20, exit_reason: 'Target Reached', entry_note: 'Breakout on volume', exit_note: 'Hit the target zone', tags: ['momentum'], net_r_multiple: 1.25 },
  { id: 't-lgen', ticker: 'LGEN.L', market: 'UK', entry_date: '2026-08-04', exit_date: '2026-08-29', shares: 400, entry_price: 2.5, exit_price: 2.35, pnl: -60, pnl_pct: -6, pnl_percent: -6, holding_days: 26, exit_reason: 'Stop Loss', entry_note: 'Dividend run-up', exit_note: null, tags: ['income'], net_r_multiple: -1 },
  { id: 't-msft', ticker: 'MSFT', market: 'US', entry_date: '2026-07-10', exit_date: '2026-07-30', shares: 3, entry_price: 400, exit_price: 412, pnl: 28.35, pnl_pct: 3, pnl_percent: 3, holding_days: 21, exit_reason: 'Manual Exit', entry_note: null, exit_note: null, tags: [], net_r_multiple: null },
];

// Open positions (GET /positions is open-only). NVDA: (520 - 500) * 4 / 1.27 = 62.99 GBP.
const OPEN_POSITIONS = [
  { id: 'p-nvda', ticker: 'NVDA', market: 'US', status: 'open', entry_date: '2026-10-01', entry_price: 500, current_price: 520, shares: 4, pnl: 62.99, pnl_percent: 4, entry_note: 'Earnings gap held', tags: ['momentum'] },
  { id: 'p-aapl', ticker: 'AAPL', market: 'US', status: 'open', entry_date: '2026-10-20', entry_price: 120, current_price: 118, shares: 5, pnl: -7.87, pnl_percent: -1.67, entry_note: 'Second entry', tags: [] },
];

const RED_FLAGS = [
  { id: 'e-1', event_type: 'pre_entry_override', ticker: 'AAPL', position_id: null, context: { source: 'trade_plan', override_acknowledged: true }, created_at: new Date(Date.now() - 3600e3).toISOString() },
  { id: 'e-2', event_type: 'checklist_skipped', ticker: 'LGEN.L', position_id: null, context: { unchecked_items: 2, total_items: 6 }, created_at: new Date(Date.now() - 7200e3).toISOString() },
];

function ok(body) {
  return { status: 200, contentType: 'application/json', body: JSON.stringify(body) };
}

/**
 * Stubs the three Journal sources. Options: trades, positions, redFlags,
 * redFlagTotal, redFlagStatus, delay (ms per source key), requests (array that
 * collects every API request path+query).
 */
async function stub(page, opts = {}) {
  const {
    trades = TRADES, positions = OPEN_POSITIONS, redFlags = RED_FLAGS, redFlagTotal = null,
    redFlagStatus = 200, positionsStatus = 200, delay = {}, requests = null,
  } = opts;
  if (requests) {
    page.on('request', (req) => {
      if (req.url().startsWith(API)) {
        const u = new URL(req.url());
        requests.push({ path: u.pathname, search: u.search, at: Date.now() });
      }
    });
  }
  const wait = (key) => (delay[key] ? new Promise((r) => setTimeout(r, delay[key])) : Promise.resolve());
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(ok({ status: 'ok', data: [] })));
  await page.route(/localhost:8000\/trades(\?|$)/, async (route) => {
    await wait('trades');
    await route.fulfill(ok({ status: 'ok', data: { total_trades: trades.length, trades } }));
  });
  await page.route(/localhost:8000\/positions$/, async (route) => {
    await wait('positions');
    if (positionsStatus !== 200) return route.fulfill({ status: positionsStatus, contentType: 'application/json', body: '{}' });
    return route.fulfill(ok(positions));
  });
  await page.route(/localhost:8000\/portfolio\/red-flag-journal/, async (route) => {
    await wait('redFlags');
    if (redFlagStatus !== 200) {
      return route.fulfill({ status: redFlagStatus, contentType: 'application/json', body: JSON.stringify({ status: 'error' }) });
    }
    const params = new URL(route.request().url()).searchParams;
    const ticker = params.get('ticker');
    const items = ticker ? redFlags.filter((e) => e.ticker.toUpperCase() === ticker) : redFlags;
    const total = redFlagTotal ?? items.length;
    return route.fulfill(ok({ status: 'ok', data: { total, page: Number(params.get('page') || 1), page_size: 20, items } }));
  });
  // No reflection saved yet for any trade (the modal opens on an empty form).
  await page.route(/localhost:8000\/trades\/[^/]+\/reflection/, (route) =>
    route.fulfill(ok({ status: 'ok', data: null }))
  );
}

const heading = (page) => page.getByRole('heading', { level: 1, name: 'Journal', exact: true });
const tab = (page, name) => page.getByRole('tab', { name: new RegExp(`^${name}( \\(\\d+\\))?$`) });
const panel = (page, section) => page.getByTestId(`journal-panel-${section}`);
const filter = (page) => page.getByTestId('journal-ticker-filter');

// ---------------------------------------------------------------------------

test('SC-JNL-01: /Journal shows "Journal", three tabs in order, opens on Reflections; tab title', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Journal');
  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  const tabs = page.getByRole('tablist').getByRole('tab');
  await expect(tabs).toHaveCount(3);
  await expect(tabs.nth(0)).toHaveText(/^Reflections/);
  await expect(tabs.nth(1)).toHaveText(/^Red flags/);
  await expect(tabs.nth(2)).toHaveText(/^Position notes/);
  await expect(tab(page, 'Reflections')).toHaveAttribute('aria-selected', 'true');
  await expect(panel(page, 'reflections').getByTestId('reflection-card')).toHaveCount(3);
  await expect(page).toHaveTitle('Journal · Position Manager');
});

test('SC-JNL-02: ?section= opens red flags and notes; an unknown value opens Reflections', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Journal?section=red-flags');
  await expect(tab(page, 'Red flags')).toHaveAttribute('aria-selected', 'true', { timeout: 15000 });
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(2);

  await page.goto('/#/Journal?section=notes');
  await expect(tab(page, 'Position notes')).toHaveAttribute('aria-selected', 'true', { timeout: 15000 });
  await expect(panel(page, 'notes').getByTestId('position-note-card')).toHaveCount(5);

  await page.goto('/#/Journal?section=bogus');
  await expect(tab(page, 'Reflections')).toHaveAttribute('aria-selected', 'true', { timeout: 15000 });
});

test('SC-JNL-03: selecting a tab updates ?section= with no history entry', async ({ page }) => {
  await stub(page);
  await page.goto('/#/TradeHistory');
  await expect(page.getByRole('heading', { level: 1, name: 'Trade History', exact: true })).toBeVisible({ timeout: 15000 });
  await page.goto('/#/Journal');
  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await tab(page, 'Red flags').click();
  await expect(page).toHaveURL(/#\/Journal\?section=red-flags$/);
  await tab(page, 'Position notes').click();
  await expect(page).toHaveURL(/#\/Journal\?section=notes$/);
  await page.goBack();
  await expect(page).toHaveURL(/#\/TradeHistory$/);
});

for (const theme of ['light', 'dark']) {
  test(`SC-JNL-04: the tabs are an ARIA tablist moved by arrow keys; axe finds no violation (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await stub(page);
    await page.goto('/#/Journal');
    await expect(panel(page, 'reflections').getByTestId('reflection-card')).toHaveCount(3, { timeout: 15000 });
    await expect(page.getByRole('tablist')).toHaveCount(1);
    await expect(page.getByRole('tabpanel')).toHaveCount(1); // inactive panels are hidden

    await tab(page, 'Reflections').focus();
    await page.keyboard.press('ArrowRight');
    await expect(tab(page, 'Red flags')).toHaveAttribute('aria-selected', 'true');
    await expect(tab(page, 'Red flags')).toBeFocused();
    await page.keyboard.press('ArrowRight');
    await expect(tab(page, 'Position notes')).toHaveAttribute('aria-selected', 'true');
    await page.keyboard.press('ArrowLeft');
    await expect(tab(page, 'Red flags')).toHaveAttribute('aria-selected', 'true');
    await expect(page).toHaveURL(/section=red-flags/);

    // All three counts are showing, so the scan covers populated tabs.
    await expect(page.getByTestId('journal-tab-count-notes')).toBeVisible();
    const results = await new AxeBuilder({ page }).include('[data-testid="journal-tabs"]').analyze();
    expect(results.violations).toEqual([]);
    // Solid token backgrounds: every contrast check must be a definite pass.
    expect(results.incomplete.filter((r) => r.id === 'color-contrast')).toEqual([]);
  });
}

test('SC-JNL-05: a tab shows its count only once its section has loaded', async ({ page }) => {
  await stub(page, { redFlagTotal: 7, delay: { redFlags: 1500 }, positionsStatus: 500 });
  await page.goto('/#/Journal');
  // Reflections loaded: 3 closed trades listed.
  await expect(tab(page, 'Reflections')).toHaveText('Reflections (3)', { timeout: 15000 });
  // Unopened tabs show no count.
  await expect(tab(page, 'Red flags')).toHaveText('Red flags');
  await expect(tab(page, 'Position notes')).toHaveText('Position notes');

  // Red flags loading: still no count; loaded: the response total, not the rows shown.
  await tab(page, 'Red flags').click();
  await expect(panel(page, 'red-flags').getByTestId('loading-state')).toBeVisible();
  await expect(tab(page, 'Red flags')).toHaveText('Red flags');
  await expect(tab(page, 'Red flags')).toHaveText('Red flags (7)', { timeout: 15000 });

  // Position notes errors: no count.
  await tab(page, 'Position notes').click();
  await expect(panel(page, 'notes').getByText('Unable to load position notes')).toBeVisible({ timeout: 15000 });
  await expect(tab(page, 'Position notes')).toHaveText('Position notes');

  // The count follows the shared filter (items listed under the current filters).
  await filter(page).fill('LGEN');
  await expect(tab(page, 'Reflections')).toHaveText('Reflections (1)');
});

test('SC-JNL-06: ?ticker= pre-fills the filter; every section shows only that ticker; kept across tabs', async ({ page }) => {
  const requests = [];
  await stub(page, { requests });
  await page.goto('/#/Journal?ticker=AAPL');
  await expect(filter(page)).toHaveValue('AAPL', { timeout: 15000 });

  const reflections = panel(page, 'reflections').getByTestId('reflection-card');
  await expect(reflections).toHaveCount(1);
  await expect(reflections.first()).toContainText('AAPL');

  await tab(page, 'Red flags').click();
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(1, { timeout: 15000 });
  await expect(panel(page, 'red-flags').getByTestId('event-ticker')).toHaveText('AAPL');
  expect(requests.some((r) => r.path === '/portfolio/red-flag-journal' && /ticker=AAPL(&|$)/.test(r.search))).toBe(true);

  await tab(page, 'Position notes').click();
  const notes = panel(page, 'notes').getByTestId('position-note-card');
  await expect(notes).toHaveCount(2, { timeout: 15000 }); // open AAPL + closed AAPL
  for (const card of await notes.all()) await expect(card).toContainText('AAPL');

  await expect(filter(page)).toHaveValue('AAPL');
  await expect(page).toHaveURL(/ticker=AAPL/);

  // Typing mirrors to ?ticker= (replace navigation).
  await filter(page).fill('NVDA');
  await expect(page).toHaveURL(/ticker=NVDA/);
  await expect(notes).toHaveCount(1);
});

test('SC-JNL-06c: typing key by key keeps every character, edits in the middle, and Enter uses the box', async ({ page }) => {
  const requests = [];
  await stub(page, { requests });
  await page.goto('/#/Journal?section=red-flags');
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(2, { timeout: 15000 });
  const box = filter(page);
  await box.click();
  await box.pressSequentially('lgen.l');
  await box.press('Enter');
  await expect(box).toHaveValue('lgen.l');
  await expect(page).toHaveURL(/ticker=lgen\.l/);
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(1, { timeout: 15000 });
  expect(requests.some((r) => r.path === '/portfolio/red-flag-journal' && /ticker=LGEN\.L(&|$)/.test(r.search))).toBe(true);
  expect(requests.some((r) => r.path === '/portfolio/red-flag-journal' && /ticker=LGEN\.(&|$)/.test(r.search))).toBe(false);

  // Edit in the middle: "AAPL" → "AMPL" by replacing the second character.
  await box.fill('');
  await box.pressSequentially('AAPL');
  await box.press('Home');
  await box.press('ArrowRight');
  await box.press('Delete');
  await box.pressSequentially('M');
  await expect(box).toHaveValue('AMPL');
  await expect(page).toHaveURL(/ticker=AMPL/);
});

test('SC-JNL-06b: partial ".L"-blind match in the browser; exact upper-cased ticker for red flags and the .L hint', async ({ page }) => {
  const requests = [];
  await stub(page, { requests });
  await page.goto('/#/Journal');
  const reflections = panel(page, 'reflections').getByTestId('reflection-card');
  await expect(reflections).toHaveCount(3, { timeout: 15000 });

  await filter(page).fill('aa');
  await expect(reflections).toHaveCount(1);
  await expect(reflections.first()).toContainText('AAPL');

  await filter(page).fill('LGEN');
  await expect(reflections).toHaveCount(1);
  await expect(reflections.first()).toContainText('LGEN.L');

  await tab(page, 'Position notes').click();
  await expect(panel(page, 'notes').getByTestId('position-note-card')).toHaveCount(1, { timeout: 15000 });
  // JA-16: partial match in Position notes too — "aa" finds the open and closed AAPL.
  await filter(page).fill('aa');
  await expect(panel(page, 'notes').getByTestId('position-note-card')).toHaveCount(2);
  await filter(page).fill('LGEN');
  await expect(panel(page, 'notes').getByTestId('position-note-card')).toHaveCount(1);
  // Closed UK card reads "LGEN", as open UK positions do (GET /positions drops ".L").
  await expect(panel(page, 'notes').getByTestId('position-note-card').first()).toContainText('LGEN');
  await expect(panel(page, 'notes').getByTestId('position-note-card').first()).not.toContainText('LGEN.L');

  // Red flags: "LGEN" is sent as typed and finds nothing; the hint names .L.
  await tab(page, 'Red flags').click();
  await expect(panel(page, 'red-flags').getByText('No events for LGEN. UK tickers need the .L suffix here, e.g. LGEN.L.')).toBeVisible({ timeout: 15000 });
  expect(requests.some((r) => r.path === '/portfolio/red-flag-journal' && /ticker=LGEN(&|$)/.test(r.search))).toBe(true);

  // "lgen.l" is upper-cased and finds the UK event.
  await filter(page).fill('lgen.l');
  await filter(page).press('Enter');
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(1, { timeout: 15000 });
  expect(requests.some((r) => r.path === '/portfolio/red-flag-journal' && /ticker=LGEN\.L(&|$)/.test(r.search))).toBe(true);
  // Reflections still matches it, ".L" or not.
  await tab(page, 'Reflections').click();
  await expect(reflections).toHaveCount(1);
});

test('SC-JNL-07: Reflections renders the card grid, loading, both empty states and the reflection modal', async ({ page }) => {
  await stub(page, { delay: { trades: 1000 } });
  await page.goto('/#/Journal');
  await expect(panel(page, 'reflections').locator('.animate-spin')).toBeVisible({ timeout: 15000 });
  const cards = panel(page, 'reflections').getByTestId('reflection-card');
  await expect(cards).toHaveCount(3, { timeout: 15000 });
  await expect(cards.first()).toContainText('AAPL');
  await expect(cards.first()).toContainText('+£55.12');

  // Card body opens the reflection modal.
  await cards.first().getByRole('button').click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).toHaveCount(0);

  // Filtered empty: the filter matches no closed trade.
  await filter(page).fill('ZZZ');
  const empty = panel(page, 'reflections').getByTestId('reflections-empty');
  await expect(empty).toContainText('No closed trades match ZZZ.');
  await empty.getByRole('button', { name: 'Clear filter' }).click();
  await expect(filter(page)).toHaveValue('');
  await expect(cards).toHaveCount(3);
});

test('SC-JNL-07b: Reflections with no closed trades shows the reflections.md §6 message', async ({ page }) => {
  await stub(page, { trades: [] });
  await page.goto('/#/Journal');
  await expect(panel(page, 'reflections').getByText('No closed trades yet — close a trade to write your first reflection.')).toBeVisible({ timeout: 15000 });
});

test('SC-JNL-08: Red flags renders its event list, own filters, pagination, empty and error states', async ({ page }) => {
  await stub(page, { redFlagTotal: 25 });
  await page.goto('/#/Journal?section=red-flags');
  const p = panel(page, 'red-flags');
  await expect(p.getByTestId('event-row')).toHaveCount(2, { timeout: 15000 });
  await expect(p.getByTestId('event-type-filter')).toBeVisible();
  await expect(p.getByText('From date')).toBeVisible();
  await expect(p.getByTestId('ticker-filter-input')).toHaveCount(0); // replaced by the shared filter
  await expect(p.getByText('Page 1 of 2')).toBeVisible();
  await expect(p.getByText('25 events recorded')).toBeVisible();
  // Pagination moves to page 2 and requests it.
  const page2 = page.waitForRequest((r) => r.url().includes('/portfolio/red-flag-journal') && r.url().includes('page=2'));
  await p.getByRole('button', { name: 'Next' }).click();
  await page2;
  await expect(p.getByText('Page 2 of 2')).toBeVisible();
  await expect(p.getByRole('button', { name: 'Next' })).toBeDisabled();
});

test('SC-JNL-08b: Red flags empty state', async ({ page }) => {
  await stub(page, { redFlags: [] });
  await page.goto('/#/Journal?section=red-flags');
  await expect(panel(page, 'red-flags').getByText('No strategy deviations recorded yet')).toBeVisible({ timeout: 15000 });
});

test('SC-JNL-09: Position notes shows open and closed cards with GBP P&L, and its four filters', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Journal?section=notes');
  const p = panel(page, 'notes');
  const cards = p.getByTestId('position-note-card');
  await expect(cards).toHaveCount(5, { timeout: 15000 });
  // Most recently entered first: AAPL (open, 20 Oct), NVDA (open, 1 Oct), AAPL (closed, 1 Sep)…
  await expect(cards.nth(0)).toContainText('Second entry');
  await expect(cards.nth(1)).toContainText('NVDA');
  await expect(cards.nth(2)).toContainText('CLOSED');
  // P&L in GBP for a US position (no "$").
  await expect(cards.nth(1)).toContainText('+£62.99');
  await expect(cards.nth(1)).not.toContainText('$62.99');
  await expect(cards.nth(2)).toContainText('+£55.12');

  // Closed card: Exit Details expands the exit note.
  await cards.nth(2).getByRole('button', { name: /Exit Details/ }).click();
  await expect(cards.nth(2)).toContainText('Hit the target zone');

  // Note-text search
  await p.getByLabel('Search in notes').fill('dividend');
  await expect(cards).toHaveCount(1);
  await expect(cards.first()).toContainText('LGEN');
  await p.getByLabel('Search in notes').fill('');

  // Tag filter
  await p.getByRole('button', { name: 'All tags' }).click();
  await p.getByRole('button', { name: 'momentum' }).click();
  await expect(cards).toHaveCount(2);
  await p.getByRole('button', { name: '1 selected' }).click();

  // Win/Loss: losers only (P&L < 0)
  await p.getByLabel('Winners or losers').selectOption('loss');
  await expect(cards).toHaveCount(0);
  await expect(p.getByTestId('notes-no-match')).toContainText('No positions match your filters.');
  await p.getByLabel('Winners or losers').selectOption('all');
  await p.locator('button', { hasText: 'momentum' }).last().click(); // dismiss the pill
  await expect(cards).toHaveCount(5);

  // Date range (entry date)
  await p.getByLabel('Entry date from').fill('2026-09-15');
  await expect(cards).toHaveCount(2);

  // Shared ticker on top; "Clear filters" clears it too.
  await filter(page).fill('NVDA');
  await expect(cards).toHaveCount(1);
  await filter(page).fill('MSFT');
  await expect(cards).toHaveCount(0);
  await p.getByTestId('notes-no-match').getByRole('button', { name: 'Clear filters' }).click();
  await expect(filter(page)).toHaveValue('');
  await expect(cards).toHaveCount(5);
});

test('SC-JNL-09b: Position notes with no positions at all offers a path to enter one', async ({ page }) => {
  await stub(page, { trades: [], positions: [] });
  await page.goto('/#/Journal?section=notes');
  const empty = panel(page, 'notes').getByTestId('notes-empty');
  await expect(empty).toContainText('No positions yet.', { timeout: 15000 });
  await empty.getByRole('button', { name: 'Enter a position' }).click();
  await expect(page).toHaveURL(/#\/TradeEntry$/);
});

test('SC-JNL-10: item links go to Trade History and Positions; no nested interactive element on Reflections', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Journal');
  const cards = panel(page, 'reflections').getByTestId('reflection-card');
  await expect(cards).toHaveCount(3, { timeout: 15000 });
  await expect(cards.nth(1).getByTestId('reflection-view-trade')).toHaveAttribute('href', '#/TradeHistory?ticker=LGEN.L');
  const axe = await new AxeBuilder({ page }).include('[data-testid="journal-panel-reflections"]').withRules(['nested-interactive']).analyze();
  expect(axe.violations).toEqual([]);

  await tab(page, 'Red flags').click();
  await expect(panel(page, 'red-flags').getByTestId('event-trade-history-link').first()).toHaveAttribute('href', '#/TradeHistory?ticker=AAPL', { timeout: 15000 });

  await tab(page, 'Position notes').click();
  const notes = panel(page, 'notes').getByTestId('position-note-card');
  await expect(notes).toHaveCount(5, { timeout: 15000 });
  await expect(notes.nth(1).getByTestId('note-open-position')).toHaveText('Open position');
  await expect(notes.nth(1).getByTestId('note-open-position')).toHaveAttribute('href', '#/Positions?position=p-nvda');
  await expect(notes.nth(2).getByTestId('note-open-position')).toHaveCount(0); // closed: no item link

  // "View trade" opens Trade History filtered to the ticker.
  await tab(page, 'Reflections').click();
  await cards.first().getByTestId('reflection-view-trade').click();
  await expect(page).toHaveURL(/#\/TradeHistory\?ticker=AAPL$/);
  await expect(page.getByTestId('trade-history-ticker-filter')).toContainText('AAPL', { timeout: 15000 });
});

test('SC-JNL-11: a red-flag fetch failure shows in its panel only; other tabs still load', async ({ page }) => {
  await stub(page, { redFlagStatus: 500 });
  await page.goto('/#/Journal?section=red-flags');
  await expect(panel(page, 'red-flags').getByTestId('error-state')).toBeVisible({ timeout: 20000 });
  await expect(tab(page, 'Red flags')).toHaveText('Red flags');
  await tab(page, 'Reflections').click();
  await expect(panel(page, 'reflections').getByTestId('reflection-card')).toHaveCount(3, { timeout: 15000 });
  await tab(page, 'Position notes').click();
  await expect(panel(page, 'notes').getByTestId('position-note-card')).toHaveCount(5, { timeout: 15000 });
});

test('SC-JNL-12: old routes redirect to their Journal section with replace navigation, keeping the query', async ({ page }) => {
  await stub(page);
  await page.goto('/#/TradeHistory');
  await expect(page.getByRole('heading', { level: 1, name: 'Trade History', exact: true })).toBeVisible({ timeout: 15000 });

  await page.goto('/#/TradeReflection');
  await expect(page).toHaveURL(/#\/Journal\?section=reflections$/);
  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await page.goBack();
  await expect(page).toHaveURL(/#\/TradeHistory$/);

  await page.goto('/#/RedFlagJournal');
  await expect(page).toHaveURL(/#\/Journal\?section=red-flags$/);
  await expect(tab(page, 'Red flags')).toHaveAttribute('aria-selected', 'true', { timeout: 15000 });

  await page.goto('/#/RedFlagJournal?ticker=AAPL');
  await expect(page).toHaveURL(/#\/Journal\?section=red-flags&ticker=AAPL$/);
  await expect(filter(page)).toHaveValue('AAPL', { timeout: 15000 });

  // A stray ?section= on the old route is dropped in favour of the route's own.
  await page.goto('/#/TradeReflection?section=notes&ticker=MSFT');
  await expect(page).toHaveURL(/#\/Journal\?section=reflections&ticker=MSFT$/);
});

test('SC-JNL-13: Positions has no journal view, its heading is "Positions", and "Position notes" opens the notes', async ({ page }) => {
  await stub(page);
  await page.goto('/#/Positions');
  await expect(page.getByRole('heading', { level: 1, name: 'Positions', exact: true })).toBeVisible({ timeout: 15000 });
  await expect(page.getByRole('button', { name: 'Journal view' })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Grid view' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Table view' })).toBeVisible();

  // JA-21: the link sits before the Daily Monitor button.
  const link = page.getByTestId('positions-notes-link');
  await expect(link).toHaveText('Position notes');
  const before = await link.evaluate((el) => {
    const monitor = document.querySelector('[data-testid="daily-monitor-button"]');
    return !!monitor && !!(el.compareDocumentPosition(monitor) & Node.DOCUMENT_POSITION_FOLLOWING);
  });
  expect(before).toBe(true);

  await link.click();
  await expect(page).toHaveURL(/#\/Journal\?section=notes$/);
  await expect(tab(page, 'Position notes')).toHaveAttribute('aria-selected', 'true', { timeout: 15000 });
  await expect(page.getByRole('heading', { name: 'Trade Journal' })).toHaveCount(0);
});

test('SC-JNL-15: the Journal calls no /ai/ endpoint from any tab', async ({ page }) => {
  const requests = [];
  await stub(page, { requests });
  await page.goto('/#/Journal');
  await expect(panel(page, 'reflections').getByTestId('reflection-card')).toHaveCount(3, { timeout: 15000 });
  await tab(page, 'Red flags').click();
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(2, { timeout: 15000 });
  await tab(page, 'Position notes').click();
  await expect(panel(page, 'notes').getByTestId('position-note-card')).toHaveCount(5, { timeout: 15000 });
  await page.waitForTimeout(500);
  expect(requests.filter((r) => r.path.startsWith('/ai/'))).toEqual([]);
});

test('SC-JNL-17: red flags refetch 300 ms after typing stops, or at once on Enter', async ({ page }) => {
  const requests = [];
  await stub(page, { requests });
  await page.goto('/#/Journal?section=red-flags');
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(2, { timeout: 15000 });
  // install() alone lets time run on; pause it so only runFor() moves it.
  await page.clock.install();
  await page.clock.pauseAt(Date.now() + 1000);
  const flagCalls = (ticker) => requests.filter((r) => r.path === '/portfolio/red-flag-journal' && new URLSearchParams(r.search).get('ticker') === ticker);

  await filter(page).fill('AAPL');
  await page.clock.runFor(250);
  await page.waitForTimeout(200);
  expect(flagCalls('AAPL')).toHaveLength(0);
  await page.clock.runFor(100);
  await expect.poll(() => flagCalls('AAPL').length).toBe(1);

  await filter(page).fill('LGEN.L');
  await filter(page).press('Enter');
  await expect.poll(() => flagCalls('LGEN.L').length).toBe(1);
});

test('SC-JNL-17b: a saved red-flag ticker is ignored; ?ticker= wins', async ({ page }) => {
  const requests = [];
  await page.addInitScript(() => window.localStorage.setItem('redFlagJournal.filters', JSON.stringify({
    version: 1, data: { eventTypeFilter: '', tickerFilter: 'TSLA', sinceFilter: '' },
  })));
  await stub(page, { requests });
  await page.goto('/#/Journal?section=red-flags');
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(2, { timeout: 15000 });
  await expect(filter(page)).toHaveValue('');
  await page.goto('/#/Journal?section=red-flags&ticker=AAPL');
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(1, { timeout: 15000 });
  const flagCalls = requests.filter((r) => r.path === '/portfolio/red-flag-journal');
  expect(flagCalls.some((r) => /TSLA/.test(r.search))).toBe(false);
  expect(flagCalls.some((r) => /ticker=AAPL/.test(r.search))).toBe(true);
});

test('SC-JNL-19: a section\'s data is requested only when its tab is first opened', async ({ page }) => {
  const requests = [];
  await stub(page, { requests });
  await page.goto('/#/Journal');
  await expect(panel(page, 'reflections').getByTestId('reflection-card')).toHaveCount(3, { timeout: 15000 });
  await page.waitForTimeout(500);
  const flagCount = () => requests.filter((r) => r.path === '/portfolio/red-flag-journal').length;
  const positionsCount = () => requests.filter((r) => r.path === '/positions').length;
  expect(flagCount()).toBe(0);
  expect(positionsCount()).toBe(0);

  await tab(page, 'Red flags').click();
  await expect(panel(page, 'red-flags').getByTestId('event-row')).toHaveCount(2, { timeout: 15000 });
  expect(flagCount()).toBe(1);
  expect(positionsCount()).toBe(0);

  await tab(page, 'Position notes').click();
  await expect(panel(page, 'notes').getByTestId('position-note-card')).toHaveCount(5, { timeout: 15000 });
  expect(positionsCount()).toBe(1);

  // Switching back keeps the data: no refetch of red flags.
  await tab(page, 'Red flags').click();
  await page.waitForTimeout(300);
  expect(flagCount()).toBe(1);
});

test('SC-JNL-20: at 375 px the tabs scroll, the filter is full width, and the page does not scroll sideways', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 800 });
  await stub(page, { redFlagTotal: 1234 });
  await page.goto('/#/Journal?section=notes');
  await expect(panel(page, 'notes').getByTestId('position-note-card')).toHaveCount(5, { timeout: 15000 });
  // Load every count so the tab strip is at its widest.
  await tab(page, 'Reflections').click();
  await tab(page, 'Red flags').click();
  await expect(tab(page, 'Red flags')).toHaveText('Red flags (1234)', { timeout: 15000 });

  const list = page.getByTestId('journal-tabs');
  const overflowX = await list.evaluate((el) => getComputedStyle(el).overflowX);
  expect(overflowX).toBe('auto');
  const listBox = await list.boundingBox();
  const filterBox = await filter(page).boundingBox();
  expect(Math.abs(filterBox.width - listBox.width)).toBeLessThanOrEqual(2);
  for (const section of ['reflections', 'red-flags', 'notes']) {
    await page.getByTestId(`journal-tab-${section}`).click();
    // The selected tab follows ?section=, which react-router commits in a
    // transition: wait for it, so the panel measured is this section's.
    await expect(page.getByTestId(`journal-tab-${section}`)).toHaveAttribute('aria-selected', 'true');
    await expect(panel(page, section)).toBeVisible();
    const scroll = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(scroll, `${section}: page-level horizontal scroll`).toBeLessThanOrEqual(0);
  }
});
