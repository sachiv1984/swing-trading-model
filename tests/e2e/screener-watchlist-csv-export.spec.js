/**
 * CSV export for Screener results and Watchlist (ST-03, EPIC-01, v9.6, BLG-FEAT-97)
 *
 * Design source: docs/design/2026-09-21__release-v9.6/screener-watchlist-csv-export/decision_record.md §5
 * Specs: docs/specs/frontend/pages/screener_results.md v1.7 §5.3, watchlist.md v0.8
 *
 * Covers observable AC (ST-03 AC-01, AC-02):
 *   SC-CSV-01  Screener: "Download CSV" downloads a dated file whose header row equals the rendered table headers
 *   SC-CSV-02  Screener: the export is the displayed rows after the active filter and sort, not the full result set
 *   SC-CSV-03  Screener: cell values are machine-readable (plain numbers, label text, raw 0-1 signal)
 *   SC-CSV-04  Screener: button is disabled with "Nothing to export" at zero displayed rows
 *   SC-CSV-05  Watchlist: header row equals the rendered headers minus the checkbox and Actions columns; row selection has no effect
 *   SC-CSV-06  Watchlist: string cells starting = + - @ get the formula-injection guard, numbers do not, RFC 4180 quoting applied
 *   SC-CSV-07  Watchlist: button is disabled with "Nothing to export" when the list is empty
 *   SC-CSV-08  A generation failure shows the "CSV download failed" error toast and no crash
 *
 * Infrastructure: Playwright page.route() network interception. No live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const fs = require('fs');
const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const json = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function readDownload(page, button) {
  const [download] = await Promise.all([page.waitForEvent('download'), button.click()]);
  const text = fs.readFileSync(await download.path(), 'utf8');
  return { filename: download.suggestedFilename(), text, lines: text.split('\r\n').filter((l) => l !== '') };
}

const renderedHeaders = (page) =>
  page.locator('table thead th').evaluateAll((ths) => ths.map((th) => th.textContent.trim()));

const localDate = () => {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
};

function makeResult(o = {}) {
  return {
    ticker: 'AAPL', market: 'US', price: 175.5, currency: 'USD', atr: 3.2, atr_pct: 0.0183,
    regime_status: 'risk_on', signal_score: 0.82, sector: 'Technology',
    proximity_to_entry_zone: 0.01, news_headline_count: 3, ...o,
  };
}

async function stubScreener(page, results) {
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/screener/regime-distribution**`, (route) =>
    route.fulfill(json({ ok: true, data: { window: '30d', run_count: 1, total_observations: 1, risk_on_count: 1, risk_off_count: 0, risk_on_pct: 100, risk_off_pct: 0 } })));
  await page.route(`${API}/screener/results**`, (route) =>
    route.fulfill(json({
      results, run_id: 'run-001', run_timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
      total: results.length, limit: 200, offset: 0,
    })));
  await page.route(`${API}/earnings/AAPL**`, (route) =>
    route.fulfill(json({ ticker: 'AAPL', days_until_earnings: 12, next_earnings_date: '2026-10-03' })));
}

const SCREENER_ROWS = [
  makeResult({ ticker: 'AAPL', signal_score: 0.82 }),
  makeResult({ ticker: 'MSFT', signal_score: 0.91, price: 410.25, atr: 5.1, sector: 'Technology', proximity_to_entry_zone: 0.04, news_headline_count: 0 }),
  makeResult({ ticker: 'VOD.L', market: 'UK', currency: 'GBP', price: 72.1, atr: 1.2, signal_score: 0.55, sector: 'Communication', proximity_to_entry_zone: 0.2, news_headline_count: 0 }),
  makeResult({ ticker: 'XOM', signal_score: 0.3, sector: null, regime_status: 'risk_off', price: 118, atr: 2.4, proximity_to_entry_zone: null, news_headline_count: 5 }),
];

async function gotoScreener(page, rows = SCREENER_ROWS) {
  await stubScreener(page, rows);
  await page.goto('/#/Screener');
  await expect(page.locator('table tbody tr').first()).toBeVisible({ timeout: 10000 });
}

// ---------------------------------------------------------------------------
// Screener
// ---------------------------------------------------------------------------

test('SC-CSV-01: Screener download is a dated file whose header row equals the rendered table headers', async ({ page }) => {
  await gotoScreener(page);
  const btn = page.getByTestId('screener-download-csv');
  await expect(btn).toBeEnabled();
  await expect(btn).toContainText('Download CSV');
  const { filename, lines } = await readDownload(page, btn);
  expect(filename).toBe(`screener-results-${localDate()}.csv`);
  const headers = await renderedHeaders(page);
  expect(headers).toEqual(['Ticker', 'Market', 'Price', 'ATR', 'Regime', 'Signal', 'Sector', 'Entry Zone', 'Earnings', 'News']);
  expect(lines[0].split(',')).toEqual(headers);
  expect(lines).toHaveLength(1 + SCREENER_ROWS.length);
});

test('SC-CSV-02: Screener exports the displayed rows after the active filter and sort', async ({ page }) => {
  await gotoScreener(page);
  // Default sort is Signal descending: MSFT .91, AAPL .82, VOD.L .55, XOM .3
  let { lines } = await readDownload(page, page.getByTestId('screener-download-csv'));
  expect(lines.slice(1).map((l) => l.split(',')[0])).toEqual(['MSFT', 'AAPL', 'VOD', 'XOM']);

  await page.getByTestId('market-filter-us').click();
  ({ lines } = await readDownload(page, page.getByTestId('screener-download-csv')));
  expect(lines.slice(1).map((l) => l.split(',')[0])).toEqual(['MSFT', 'AAPL', 'XOM']);

  // Sorting by Price ascending changes the exported order
  await page.getByRole('columnheader', { name: 'Price' }).click();
  ({ lines } = await readDownload(page, page.getByTestId('screener-download-csv')));
  expect(lines.slice(1).map((l) => l.split(',')[0])).toEqual(['XOM', 'AAPL', 'MSFT']);
});

test('SC-CSV-03: Screener cell values are machine-readable, not presentation-formatted', async ({ page }) => {
  await gotoScreener(page);
  await expect(page.locator('tr', { hasText: 'AAPL' }).getByText('12d')).toBeVisible({ timeout: 10000 });
  const { lines } = await readDownload(page, page.getByTestId('screener-download-csv'));
  const byTicker = Object.fromEntries(lines.slice(1).map((l) => [l.split(',')[0], l.split(',')]));
  // Ticker,Market,Price,ATR,Regime,Signal,Sector,Entry Zone,Earnings,News
  expect(byTicker.AAPL).toEqual(['AAPL', 'US', '175.5', '3.2', 'Risk On', '0.82', 'Technology', 'In zone', '12', '3']);
  expect(byTicker.MSFT.slice(0, 8)).toEqual(['MSFT', 'US', '410.25', '5.1', 'Risk On', '0.91', 'Technology', 'Near entry']);
  expect(byTicker.MSFT[9]).toBe(''); // zero headline count -> empty
  expect(byTicker.VOD.slice(0, 2)).toEqual(['VOD', 'UK']); // UK suffix stripped, as displayed
  expect(byTicker.XOM.slice(4, 9)).toEqual(['Risk Off', '0.3', '', '', '']); // missing sector/entry zone/earnings -> empty
  // No currency symbols, thousands separators or % signs anywhere in data rows
  expect(lines.slice(1).join('\n')).not.toMatch(/[$£%]/);
});

test('SC-CSV-04: Screener button is disabled with "Nothing to export" when everything is filtered out', async ({ page }) => {
  // UK row is risk_off, so "UK" + "Risk-On only" leaves zero displayed rows
  await gotoScreener(page, [
    makeResult({ ticker: 'AAPL' }),
    makeResult({ ticker: 'VOD.L', market: 'UK', currency: 'GBP', regime_status: 'risk_off', news_headline_count: 0 }),
  ]);
  const btn = page.getByTestId('screener-download-csv');
  await expect(btn).toBeEnabled();
  await page.getByTestId('market-filter-uk').click();
  await page.getByRole('button', { name: /risk-on only/i }).click();
  await expect(page.getByText('No tickers match your current filters.')).toBeVisible();
  await expect(btn).toBeDisabled();
  await expect(btn).toHaveAttribute('title', 'Nothing to export');
});

test('SC-CSV-04b: Screener button is disabled in the empty (no results) state', async ({ page }) => {
  await stubScreener(page, []);
  await page.goto('/#/Screener');
  const btn = page.getByTestId('screener-download-csv');
  await expect(btn).toBeVisible({ timeout: 10000 });
  await expect(btn).toBeDisabled();
});

// ---------------------------------------------------------------------------
// Watchlist
// ---------------------------------------------------------------------------

const entry = (id, ticker, o = {}) => ({
  id, ticker, market: 'US', company_name: `${ticker} Inc.`, signal_status: 'watch', tags: [],
  target_entry_price: 150.5, initial_stop_price: 142, current_stop_price: 144.25,
  created_at: '2026-07-20T10:00:00Z', updated_at: '2026-07-20T10:00:00Z', added_at: '2026-07-20T10:00:00Z',
  days_on_watchlist: 5, is_stale: false, ...o,
});

async function gotoWatchlist(page, entries) {
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/watchlist`, (route) =>
    route.request().method() === 'GET' ? route.fulfill(json({ status: 'ok', data: entries })) : route.continue());
  await page.route(`${API}/watchlist/tags`, (route) => route.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/screener/results`, (route) =>
    route.fulfill(json({ data: [{ ticker: 'AAPL' }] }))); // AAPL has research data
  await page.route(`${API}/earnings/AAPL**`, (route) =>
    route.fulfill(json({ ticker: 'AAPL', days_until_earnings: 7, next_earnings_date: '2026-09-28' })));
  await page.goto('/#/Watchlist');
}

test('SC-CSV-05: Watchlist header row equals the rendered headers minus checkbox and Actions; selection has no effect', async ({ page }) => {
  await gotoWatchlist(page, [entry('1', 'AAPL'), entry('2', 'VOD.L', { market: 'UK', signal_status: 'no_signal' }), entry('3', 'NVDA')]);
  await expect(page.locator('table tbody tr').first()).toBeVisible({ timeout: 10000 });
  await expect(page.locator('tr', { hasText: 'AAPL' }).getByText('7d', { exact: true })).toBeVisible({ timeout: 10000 });

  // Select one row — the export must still contain every displayed row
  await page.getByRole('checkbox', { name: 'Select NVDA' }).click();

  const btn = page.getByTestId('watchlist-download-csv');
  const { filename, lines } = await readDownload(page, btn);
  expect(filename).toBe(`watchlist-${localDate()}.csv`);

  const rendered = await renderedHeaders(page);
  expect(rendered[0]).toBe('');            // selection checkbox column
  expect(rendered[rendered.length - 1]).toBe('Actions');
  const dataHeaders = rendered.slice(1, -1);
  expect(dataHeaders).toEqual(['Ticker', 'Market', 'Entry Signal', 'Added', 'Target Entry', 'Stop (Initial)', 'Stop (Current)', 'Earnings', 'Research', 'News']);
  expect(lines[0].split(',')).toEqual(dataHeaders);
  expect(lines).toHaveLength(4); // header + 3 rows, regardless of selection

  const byTicker = Object.fromEntries(lines.slice(1).map((l) => [l.split(',')[0], l.split(',')]));
  expect(byTicker.AAPL).toEqual(['AAPL', 'US', 'Watch', '5', '150.5', '142', '144.25', '7', 'Yes', 'Yes']);
  expect(byTicker['VOD.L']).toEqual(['VOD.L', 'UK', 'No Signal', '5', '150.5', '142', '144.25', '', 'No', 'No']);
});

test('SC-CSV-06: Formula-injection guard on string cells, RFC 4180 quoting, numbers untouched', async ({ page }) => {
  await gotoWatchlist(page, [
    entry('1', '=SUM(A1)'),
    entry('2', '+CMD'),
    entry('3', '-X'),
    entry('4', '@HANDLE'),
    entry('5', 'A,B"C', { current_stop_price: -1.5 }),
  ]);
  await expect(page.locator('table tbody tr').first()).toBeVisible({ timeout: 10000 });
  const { lines } = await readDownload(page, page.getByTestId('watchlist-download-csv'));
  const tickers = lines.slice(1).map((l) => l.split(',')[0]);
  expect(tickers).toContain("'=SUM(A1)");
  expect(tickers).toContain("'+CMD");
  expect(tickers).toContain("'-X");
  expect(tickers).toContain("'@HANDLE");
  // Comma + quote in a value -> quoted with doubled quotes; the negative NUMBER is written bare, unguarded
  const quoted = lines.find((l) => l.startsWith('"A,B""C"'));
  expect(quoted).toBeDefined();
  expect(quoted).toContain(',-1.5,');
  expect(quoted).not.toContain("'-1.5");
});

test('SC-CSV-07: Watchlist button is disabled with "Nothing to export" when the list is empty', async ({ page }) => {
  await gotoWatchlist(page, []);
  const btn = page.getByTestId('watchlist-download-csv');
  await expect(btn).toBeVisible({ timeout: 10000 });
  await expect(btn).toBeDisabled();
  await expect(btn).toHaveAttribute('title', 'Nothing to export');
  // Placement: immediately left of "+ Add Ticker"
  const btnBox = await btn.boundingBox();
  const addBox = await page.getByRole('button', { name: /add ticker/i }).first().boundingBox();
  expect(btnBox.x + btnBox.width).toBeLessThanOrEqual(addBox.x + 1);
});

// ---------------------------------------------------------------------------
// Failure
// ---------------------------------------------------------------------------

test('SC-CSV-08: A generation failure shows the "CSV download failed" toast', async ({ page }) => {
  await page.addInitScript(() => {
    URL.createObjectURL = () => { throw new Error('blob failure'); };
  });
  await gotoWatchlist(page, [entry('1', 'AAPL')]);
  await expect(page.locator('table tbody tr').first()).toBeVisible({ timeout: 10000 });
  await page.getByTestId('watchlist-download-csv').click();
  await expect(page.getByText('CSV download failed. Please try again.')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('watchlist-download-csv')).toBeEnabled();
});
