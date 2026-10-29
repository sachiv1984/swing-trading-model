/**
 * v9.12 ST-26 (BLG-SEC-41, EPIC-04): the Settings save bar shows the last logged change.
 *
 * Design source: docs/design/2026-10-12__release-v9.12/settings-copy-and-last-change/decision_record.md §2.2, §6
 * Spec: docs/specs/frontend/pages/settings.md §Last Change Line (v1.9)
 * Contract: docs/specs/api_contracts/settings_endpoints.md v1.5.0 (GET /settings last_change)
 *
 *   SC-SLC-01  One field changed: "Last change: {label} {old} → {new} · {d MMM yyyy, HH:mm} · Settings page"
 *   SC-SLC-02  Several fields in one save: "... and {n} more ...", full list in the title tooltip
 *   SC-SLC-03  last_change null: "No changes recorded yet."
 *   SC-SLC-04  A source other than settings_page reads "API"
 *   SC-SLC-05  Save sends X-Request-Source: settings_page, omits last_change, and the line updates from the refetch
 *
 * Infrastructure: page.route() network interception, no live backend. The browser runs in UTC
 * so the viewer-local time is deterministic.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

test.use({ timezoneId: 'UTC' });

const BASE_ROW = { id: 'settings-1', default_currency: 'GBP', theme: 'dark', default_risk_percent: 1.5 };

function lastChange(changes, { at = '2026-10-15T08:30:00+00:00', source = 'settings_page' } = {}) {
  return { ...changes[0], changed_at: at, request_source: source, changes };
}

async function stubSettings(page, getRows, onWrite) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(new RegExp(`${API}/settings`), (r) => {
    if (r.request().method() === 'GET') {
      return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: getRows() }) });
    }
    if (onWrite) onWrite(r.request());
    return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { id: 'settings-1' } }) });
  });
}

test('SC-SLC-01: one changed field renders label, old → new, local time and source', async ({ page }) => {
  const row = { ...BASE_ROW, last_change: lastChange([{ field: 'default_risk_percent', old_value: '1', new_value: '1.5' }]) };
  await stubSettings(page, () => [row]);
  await page.goto('/#/Settings');
  await expect(page.getByTestId('settings-last-change')).toHaveText(
    'Last change: Default Risk % Per Trade 1 → 1.5 · 15 Oct 2026, 08:30 · Settings page',
    { timeout: 10000 }
  );
});

test('SC-SLC-02: several fields in one save show "and n more" with the full list in the tooltip', async ({ page }) => {
  const row = {
    ...BASE_ROW,
    last_change: lastChange([
      { field: 'uk_commission', old_value: '9.95', new_value: '7.5' },
      { field: 'stamp_duty_rate', old_value: '0.005', new_value: '0.004' },
      { field: 'theme', old_value: 'dark', new_value: 'light' },
    ]),
  };
  await stubSettings(page, () => [row]);
  await page.goto('/#/Settings');
  const line = page.getByTestId('settings-last-change');
  await expect(line).toHaveText(
    'Last change: UK Commission (£) 9.95 → 7.5 and 2 more · 15 Oct 2026, 08:30 · Settings page',
    { timeout: 10000 }
  );
  await expect(line).toHaveAttribute(
    'title',
    'UK Commission (£) 9.95 → 7.5\nUK Stamp Duty Rate 0.005 → 0.004\nTheme dark → light'
  );
});

test('SC-SLC-03: with nothing logged the line reads "No changes recorded yet."', async ({ page }) => {
  await stubSettings(page, () => [{ ...BASE_ROW, last_change: null }]);
  await page.goto('/#/Settings');
  await expect(page.getByTestId('settings-last-change')).toHaveText('No changes recorded yet.', { timeout: 10000 });
});

test('SC-SLC-04: a change from any other source reads "API"', async ({ page }) => {
  const row = {
    ...BASE_ROW,
    last_change: lastChange([{ field: 'min_trades_for_analytics', old_value: '10', new_value: '1200' }], { source: 'api' }),
  };
  await stubSettings(page, () => [row]);
  await page.goto('/#/Settings');
  await expect(page.getByTestId('settings-last-change')).toHaveText(
    'Last change: Minimum Trades for Analytics 10 → 1,200 · 15 Oct 2026, 08:30 · API',
    { timeout: 10000 }
  );
});

test('SC-SLC-05: save sends X-Request-Source and the line updates from the refetched settings', async ({ page }) => {
  let row = { ...BASE_ROW, last_change: null };
  let write = null;
  await stubSettings(page, () => [row], (request) => {
    write = { headers: request.headers(), body: request.postDataJSON() };
    row = {
      ...row,
      default_risk_percent: 2,
      last_change: lastChange([{ field: 'default_risk_percent', old_value: '1.5', new_value: '2' }], { at: '2026-10-15T09:05:00+00:00' }),
    };
  });
  await page.goto('/#/Settings');
  const line = page.getByTestId('settings-last-change');
  await expect(line).toHaveText('No changes recorded yet.', { timeout: 10000 });

  await page.getByLabel('Default Risk % Per Trade').fill('2');
  await page.getByRole('button', { name: /Save Settings/ }).click();

  await expect(line).toHaveText(
    'Last change: Default Risk % Per Trade 1.5 → 2 · 15 Oct 2026, 09:05 · Settings page',
    { timeout: 10000 }
  );
  expect(write.headers['x-request-source']).toBe('settings_page');
  expect(write.body).not.toHaveProperty('last_change');
});
