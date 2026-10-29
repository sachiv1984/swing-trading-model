/**
 * v9.13 ST-04 (BLG-BE-182, EPIC-01) — checklist_skipped events and recorded event types.
 *
 * Design source: docs/design/2026-10-16__release-v9.13/red-flag-journal-recorded-types/decision_record.md §5
 * Spec: red_flag_journal.md (page) v1.4 §4, §5, §7; red_flag_journal.md (contract) v1.1.0
 *
 *   SC-RFR-01  Saving a plan with an incomplete checklist sends its checklist; the journal then shows one
 *              Checklist Skipped row with "{n} of {m} checklist items unchecked when the plan was saved" (AC 1)
 *   SC-RFR-02  The two types with no writer are disabled and suffixed "— not yet recorded" (AC 2)
 *   SC-RFR-03  Both empty states show the recorded-types note (AC 2)
 *   SC-RFR-04  A stored filter naming an unrecorded type resets to "All types"
 *
 * The backend writer itself is covered by tests/test_red_flag_checklist_skipped.py; here the POST
 * mock applies the same rule (one event per save with unchecked items) to the body the page sends.
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const NOTE = 'Pre-entry overrides and skipped checklists are recorded here. Stop and drawdown prompt dismissals are not recorded yet.';

async function stubJournal(page, events) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(new RegExp(`${API}/portfolio/red-flag-journal`), (r) => {
    const type = new URL(r.request().url()).searchParams.get('event_type');
    const items = events.filter((e) => !type || e.event_type === type);
    r.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { total: items.length, page: 1, page_size: 20, items } }),
    });
  });
}

test.describe('Red Flag Journal recorded types (ST-04)', () => {
  test('SC-RFR-01: an incomplete checklist on save appears as one Checklist Skipped row', async ({ page }) => {
    const events = [];
    await stubJournal(page, events);
    await page.route(`${API}/market/status`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { regime_status: 'risk_on' } }) })
    );
    await page.route(new RegExp(`${API}/trade-plans$`), (r) => {
      const req = r.request();
      if (req.method() !== 'POST') {
        return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
      }
      const body = req.postDataJSON();
      const items = body.checklist_items || [];
      const unchecked = items.filter((i) => i.checked !== true).length;
      if (items.length && unchecked) {
        events.push({
          id: 'evt-1', event_type: 'checklist_skipped', ticker: body.ticker, position_id: null,
          context: { source: 'trade_plan', plan_id: 'plan-new', unchecked_items: unchecked, total_items: items.length },
          created_at: new Date().toISOString(),
        });
      }
      return r.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { id: 'plan-new', ...body } }) });
    });

    await page.goto('/#/TradePlan?ticker=NVDA&market=US');
    const save = page.getByRole('button', { name: 'Save Plan' });
    await expect(save).toBeEnabled({ timeout: 10000 });
    const posted = page.waitForRequest((req) => req.method() === 'POST' && /\/trade-plans$/.test(req.url()));
    await save.click();
    const sent = (await posted).postDataJSON();
    expect(sent.checklist_items.length).toBeGreaterThan(0);
    expect(sent.checklist_items.some((i) => i.checked !== true)).toBe(true);
    expect(events).toHaveLength(1);

    const { unchecked_items: n, total_items: m } = events[0].context;
    await page.goto('/#/RedFlagJournal');
    // Exclude the filter's own "Checklist Skipped" <option>.
    const rows = page.getByText('Checklist Skipped', { exact: true }).and(page.locator(':not(option)'));
    await expect(rows).toHaveCount(1, { timeout: 10000 });
    await expect(page.getByText(`${n} of ${m} checklist items unchecked when the plan was saved`)).toBeVisible();
    await expect(page.getByText('NVDA', { exact: true })).toBeVisible();
  });

  test('SC-RFR-02: types with no writer are disabled and labelled "not yet recorded"', async ({ page }) => {
    await stubJournal(page, []);
    await page.goto('/#/RedFlagJournal');
    const filter = page.getByTestId('event-type-filter');
    await expect(filter).toBeVisible({ timeout: 10000 });
    for (const [value, label, disabled] of [
      ['', 'All types', false],
      ['pre_entry_override', 'Pre-Entry Override', false],
      ['checklist_skipped', 'Checklist Skipped', false],
      ['stop_prompt_dismissed', 'Stop Prompt Dismissed — not yet recorded', true],
      ['drawdown_prompt_dismissed', 'Drawdown Prompt Dismissed — not yet recorded', true],
    ]) {
      const option = filter.locator(`option[value="${value}"]`);
      await expect(option).toHaveText(label);
      if (disabled) await expect(option).toBeDisabled();
      else await expect(option).toBeEnabled();
    }
  });

  test('SC-RFR-03: both empty states carry the recorded-types note', async ({ page }) => {
    await stubJournal(page, []);
    await page.goto('/#/RedFlagJournal');
    await expect(page.getByText('No strategy deviations recorded yet')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('recorded-types-note')).toHaveText(NOTE);

    await page.getByTestId('event-type-filter').selectOption('checklist_skipped');
    await expect(page.getByText('No events match your current filters.')).toBeVisible();
    await expect(page.getByTestId('empty-state').getByRole('button', { name: 'Clear filters' })).toBeVisible();
    await expect(page.getByTestId('recorded-types-note')).toHaveText(NOTE);
  });

  test('SC-RFR-04: a stored filter naming an unrecorded type resets to All types', async ({ page }) => {
    await page.addInitScript(() => window.localStorage.setItem('redFlagJournal.filters', JSON.stringify({
      version: 1, data: { eventTypeFilter: 'stop_prompt_dismissed', tickerFilter: '', sinceFilter: '' },
    })));
    await stubJournal(page, []);
    await page.goto('/#/RedFlagJournal');
    await expect(page.getByTestId('event-type-filter')).toHaveValue('', { timeout: 10000 });
    await expect(page.getByText('No strategy deviations recorded yet')).toBeVisible();
  });
});
