/**
 * Red Flag Journal — Filter State Persistence
 * ST-02 (EPIC-01, v6.6, BLG-FE-40)
 *
 * Covers:
 *   SC-RFJ-05a: Filter state persists across page reload (localStorage)
 *   SC-RFJ-05b: Stale/corrupt localStorage filter state clears gracefully without error
 *
 * Kept as a separate spec file (not appended to red-flag-journal.spec.js) because that
 * file is currently excluded from CI via playwright.config.js testIgnore (BLG-QA-64 —
 * pre-existing, unrelated UI-text-mismatch failures). This file is not excluded.
 *
 * Infrastructure:
 * - Playwright page.route() network interception — no live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/RedFlagJournal').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const PAGE_URL = '/#/RedFlagJournal';
const STORAGE_KEY = 'redFlagJournal.filters';

const MOCK_EVENTS = [
  {
    id: '550e8400-e29b-41d4-a716-446655440001',
    event_type: 'pre_entry_override',
    ticker: 'AAPL',
    position_id: null,
    context: { source: 'trade_plan', override_acknowledged: true },
    created_at: new Date(Date.now() - 3600 * 1000).toISOString(),
  },
  {
    id: '550e8400-e29b-41d4-a716-446655440002',
    event_type: 'checklist_skipped',
    ticker: 'NVDA',
    position_id: null,
    context: { source: 'trade_plan' },
    created_at: new Date(Date.now() - 7200 * 1000).toISOString(),
  },
];

function makeJournalResponse(items = MOCK_EVENTS, total = null) {
  return {
    status: 'ok',
    data: {
      total: total !== null ? total : items.length,
      page: 1,
      page_size: 20,
      items,
    },
  };
}

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockJournal(page, response) {
  await page.route(new RegExp(`${API}/portfolio/red-flag-journal`), (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(response),
    })
  );
}

async function setup(page, journalResponse) {
  await mockFallback(page);
  await mockJournal(page, journalResponse);
  await page.goto(PAGE_URL);
  await expect(page.getByTestId('event-type-filter')).toBeVisible({ timeout: 8000 });
}

test.describe('Red Flag Journal — filter state persistence', () => {

  test('SC-RFJ-05a: Filter state persists across page reload', async ({ page }) => {
    await setup(page, makeJournalResponse(MOCK_EVENTS));

    // Set event type filter and ticker filter
    await page.getByTestId('event-type-filter').selectOption('checklist_skipped');
    await page.getByTestId('ticker-filter-input').fill('NVDA');
    await page.getByTestId('ticker-filter-input').press('Enter');

    // Reload the page — same mocks still apply
    await page.reload();
    await expect(page.getByTestId('event-type-filter')).toBeVisible({ timeout: 8000 });

    // Filter controls restored from localStorage
    await expect(page.getByTestId('event-type-filter')).toHaveValue('checklist_skipped');
    await expect(page.getByTestId('ticker-filter-input')).toHaveValue('NVDA');
  });

  test('SC-RFJ-05b: Stale/corrupt localStorage filter state is cleared gracefully without error', async ({ page }) => {
    await mockFallback(page);
    await mockJournal(page, makeJournalResponse(MOCK_EVENTS));

    // Seed localStorage with a version-mismatched payload before the app loads
    await page.addInitScript((key) => {
      window.localStorage.setItem(
        key,
        JSON.stringify({ version: 999, data: { eventTypeFilter: 'checklist_skipped' } })
      );
    }, STORAGE_KEY);

    const errors = [];
    page.on('pageerror', (err) => errors.push(err));

    await page.goto(PAGE_URL);

    // No JS error surfaced, page renders normally with default (cleared) filters
    await expect(page.getByRole('heading', { name: 'Red Flag Journal' })).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('event-type-filter')).toHaveValue('');
    expect(errors).toHaveLength(0);

    // Stale entry was removed rather than left corrupt
    const stored = await page.evaluate((key) => window.localStorage.getItem(key), STORAGE_KEY);
    expect(stored === null || JSON.parse(stored).version === 1).toBeTruthy();
  });

});
