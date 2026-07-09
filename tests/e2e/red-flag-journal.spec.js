/**
 * Red Flag Journal Page — Playwright Tests
 * ST-08 (EPIC-03, v3.9)
 *
 * Covers:
 *   SC-RFJ-01: Page renders with mocked events list (event type label, ticker, date visible)
 *   SC-RFJ-02: Empty state renders when API returns 0 events
 *   SC-RFJ-03: Filter by event_type narrows results in mocked response
 *
 * Infrastructure:
 * - Playwright page.route() network interception — no live backend required.
 * - ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/RedFlagJournal').
 * - LIFO ordering: catch-all registered FIRST so specific mocks take precedence.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const PAGE_URL = '/#/RedFlagJournal';

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

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

// ---------------------------------------------------------------------------
// Setup helpers
// ---------------------------------------------------------------------------

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
  await page.getByRole('heading', { name: 'Red Flag Journal' }).waitFor({ timeout: 8000 });
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

test.describe('Red Flag Journal', () => {

  test('SC-RFJ-01: Page renders with mocked events list — event type, ticker, date visible', async ({ page }) => {
    await setup(page, makeJournalResponse(MOCK_EVENTS));

    // Page title visible
    await expect(page.getByRole('heading', { name: 'Red Flag Journal' })).toBeVisible({ timeout: 8000 });

    // Event rows rendered
    const rows = page.getByTestId('event-row');
    await expect(rows).toHaveCount(2, { timeout: 8000 });

    // First row: Pre-Entry Override label
    await expect(rows.first()).toContainText('Pre-Entry Override');

    // First row: AAPL ticker
    const firstTicker = rows.first().getByTestId('event-ticker');
    await expect(firstTicker).toHaveText('AAPL');

    // First row: date visible (relative time)
    const firstDate = rows.first().getByTestId('event-date');
    await expect(firstDate).toBeVisible();

    // Second row: Checklist Skipped
    await expect(rows.nth(1)).toContainText('Checklist Skipped');
    await expect(rows.nth(1).getByTestId('event-ticker')).toHaveText('NVDA');
  });

  test('SC-RFJ-02: Empty state renders when API returns 0 events', async ({ page }) => {
    await setup(page, makeJournalResponse([], 0));

    // Page title visible
    await expect(page.getByRole('heading', { name: 'Red Flag Journal' })).toBeVisible({ timeout: 8000 });

    // Empty state message
    await expect(page.getByTestId('empty-state')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('No strategy deviations recorded yet')).toBeVisible();

    // No event rows
    await expect(page.getByTestId('event-row')).toHaveCount(0);
  });

  test('SC-RFJ-04: Pagination — Next button navigates to page 2 and loads additional events', async ({ page }) => {
    const PAGE_SIZE = 20;

    // Build 21 events: 20 on page 1, 1 on page 2 — total > page size triggers pagination
    function makeEvents(count, startIndex = 0) {
      return Array.from({ length: count }, (_, i) => ({
        id: `00000000-0000-0000-0000-${String(startIndex + i).padStart(12, '0')}`,
        event_type: i % 2 === 0 ? 'pre_entry_override' : 'checklist_skipped',
        ticker: i % 2 === 0 ? 'AAPL' : 'MSFT',
        position_id: null,
        context: {},
        created_at: new Date(Date.now() - (startIndex + i) * 3600 * 1000).toISOString(),
      }));
    }

    const PAGE1_EVENTS = makeEvents(PAGE_SIZE, 0);
    const PAGE2_EVENTS = makeEvents(1, PAGE_SIZE);
    const TOTAL = 21;

    await mockFallback(page);
    await page.route(new RegExp(`${API}/portfolio/red-flag-journal`), (route) => {
      const url = new URL(route.request().url());
      const pg = parseInt(url.searchParams.get('page') || '1', 10);
      const items = pg === 1 ? PAGE1_EVENTS : PAGE2_EVENTS;
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(makeJournalResponse(items, TOTAL)),
      });
    });

    await page.goto(PAGE_URL);
    // Wait for page 1 rows to render — element-specific wait (no networkidle)
    await expect(page.getByTestId('event-row').first()).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('event-row')).toHaveCount(PAGE_SIZE, { timeout: 8000 });

    // Next button must be present and enabled (total > page size → totalPages > 1)
    const nextButton = page.getByRole('button', { name: /next/i });
    await expect(nextButton).toBeVisible({ timeout: 5000 });
    await expect(nextButton).toBeEnabled();

    // Click Next to load page 2
    await nextButton.click();

    // Page 2: 1 event row visible
    await expect(page.getByTestId('event-row')).toHaveCount(1, { timeout: 8000 });
  });

  test('SC-RFJ-03: Filter by event_type narrows results in mocked response', async ({ page }) => {
    // Initially returns both events
    await mockFallback(page);

    let callCount = 0;
    await page.route(new RegExp(`${API}/portfolio/red-flag-journal`), (route) => {
      callCount++;
      const url = new URL(route.request().url());
      const eventType = url.searchParams.get('event_type');
      let items = MOCK_EVENTS;
      if (eventType === 'pre_entry_override') {
        items = MOCK_EVENTS.filter((e) => e.event_type === 'pre_entry_override');
      }
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(makeJournalResponse(items)),
      });
    });

    await page.goto(PAGE_URL);

    // Initially 2 rows
    await expect(page.getByTestId('event-row')).toHaveCount(2, { timeout: 8000 });

    // Apply event_type filter
    await page.getByTestId('event-type-filter').selectOption('pre_entry_override');

    // Wait for filtered results
    await expect(page.getByTestId('event-row')).toHaveCount(1, { timeout: 6000 });
    await expect(page.getByTestId('event-row').first()).toContainText('Pre-Entry Override');
  });

});
