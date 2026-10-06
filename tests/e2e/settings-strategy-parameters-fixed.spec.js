/**
 * v9.10 ST-01 (BLG-BE-138, EPIC-01): Settings shows the fixed §11 strategy parameters.
 *
 * Parameter-authority ruling (a), 2026-10-06 (ESC-EXEC-20261006-01).
 * Design source: docs/design/2026-10-06__release-v9.10/stop-parameter-settings-presentation/decision_record.md §5
 * Spec: docs/specs/frontend/pages/settings.md §Strategy Parameter Presentation
 *
 *   SC-SPF-01  With no settings row, the four parameters show 10 / 14 / 5.0 / 2.0
 *   SC-SPF-02  The fixed caption is present and none of the four renders as an <input>
 *   SC-SPF-03  A stored row with the old wrong values (5 / 2 / 3) still shows the §11 values
 *   SC-SPF-04  Saving omits the four fixed fields; Default Risk % is still sent
 *   SC-SPF-05  Trade Entry system initial stop uses 5× ATR regardless of the stored row
 *
 * Infrastructure: page.route() network interception — no live backend required.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function stubSettings(page, rows, onWrite) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(new RegExp(`${API}/settings`), (r) => {
    const method = r.request().method();
    if (method === 'GET') {
      return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: rows }) });
    }
    if (onWrite) onWrite(r.request().postDataJSON());
    return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { id: 'settings-1' } }) });
  });
}

const EXPECTED = {
  'min-hold-days': '10',
  'atr-period': '14',
  'atr-multiplier-initial': '5.0',
  'atr-multiplier-trailing': '2.0',
};

async function expectSection11Values(page) {
  for (const [id, value] of Object.entries(EXPECTED)) {
    const cell = page.getByTestId(`strategy-param-${id}`);
    await expect(cell).toBeVisible({ timeout: 10000 });
    await expect(cell.locator('p').nth(1)).toHaveText(value);
    await expect(cell.locator('input')).toHaveCount(0);
  }
}

test('SC-SPF-01: with no settings row, the parameters show the §11 values', async ({ page }) => {
  await stubSettings(page, []);
  await page.goto('/#/Settings');
  await expectSection11Values(page);
});

test('SC-SPF-02: fixed caption present; no input for the four parameters', async ({ page }) => {
  await stubSettings(page, []);
  await page.goto('/#/Settings');
  await expect(page.getByTestId('strategy-params-fixed-caption')).toHaveText(
    'These parameters are fixed by the strategy rules (§11) and are shown for reference.'
  );
  for (const id of ['settings-min-hold-days', 'settings-atr-period', 'settings-atr-multiplier-initial', 'settings-atr-multiplier-trailing']) {
    await expect(page.locator(`#${id}`)).toHaveCount(0);
  }
  await expect(page.locator('#settings-default-risk-percent')).toBeEditable();
});

test('SC-SPF-03: a stored row with the old wrong values still shows §11', async ({ page }) => {
  await stubSettings(page, [{
    id: 'settings-1', min_hold_days: 5, atr_period: 14, atr_multiplier_initial: 2, atr_multiplier_trailing: 3,
    default_risk_percent: 1.0,
  }]);
  await page.goto('/#/Settings');
  await expectSection11Values(page);
});

test('SC-SPF-04: saving omits the fixed fields and still sends Default Risk %', async ({ page }) => {
  let sent = null;
  await stubSettings(page, [{ id: 'settings-1', min_hold_days: 5, atr_multiplier_initial: 2, default_risk_percent: 1.5 }], (body) => { sent = body; });
  await page.goto('/#/Settings');
  await expectSection11Values(page);
  await page.getByRole('button', { name: /save/i }).first().click();
  await expect.poll(() => sent, { timeout: 8000 }).not.toBeNull();
  for (const field of ['min_hold_days', 'atr_period', 'atr_multiplier_initial', 'atr_multiplier_trailing']) {
    expect(sent).not.toHaveProperty(field);
  }
  expect(sent.default_risk_percent).toBe(1.5);
});

// ---------------------------------------------------------------------------
// Trade Entry suggested stop uses the fixed 5x initial multiplier (ST-01 AC 4).
// It previously fell back to 2x when no settings row loaded.
// ---------------------------------------------------------------------------

test('SC-SPF-05: Trade Entry system stop is entry − 5×ATR even when a stored row says 2×', async ({ page }) => {
  await stubSettings(page, [{ id: 'settings-1', atr_multiplier_initial: 2, default_risk_percent: 1.0 }]);
  await page.goto('/#/TradeEntry');
  await expect(page.locator('input[placeholder*="AAPL"]')).toBeVisible({ timeout: 10000 });
  await page.locator('input[placeholder="0.00"]').first().fill('100');
  await page.getByPlaceholder('Fetched automatically if blank').fill('4');
  // ST-07 (BLG-FE-197): the suggestion hint became the read-only system stop panel.
  const panel = page.getByTestId('system-initial-stop');
  await expect(panel).toContainText('Entry − 5× ATR (§5)');
  await expect(page.getByTestId('system-initial-stop-value')).toContainText('80.00'); // 100 − 5 × 4
});
