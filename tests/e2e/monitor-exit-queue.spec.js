/**
 * v9.13 ST-01 (BLG-FE-226, EPIC-01) — the Daily Position Monitor's exits open the real exit flow.
 *
 * Design source: docs/design/2026-10-16__release-v9.13/monitor-exit-queue/decision_record.md §6
 * Spec: positions.md §Daily Position Monitor Exit Queue
 *
 *   SC-MEQ-01  A suggested stop exit opens ExitModal with "Stop Loss Hit" pre-selected, records one
 *              POST /positions/{id}/exit (never PATCH /positions/{id}), and the position leaves
 *              the open list (AC 2, AC 4a)
 *   SC-MEQ-02  A failed exit shows the inline error, keeps the modal and its values, and Cancel
 *              reopens the Monitor with the position still selected (AC 3, AC 4b)
 *   SC-MEQ-03  Two queued positions: progress reads "Exit 1 of 2" then "Exit 2 of 2", the
 *              risk-off suggestion pre-selects "Risk-Off Signal", and the toast counts both
 *   SC-MEQ-04  Cancel while an exit request is in flight: the Monitor reopens, and when the request
 *              then succeeds the queue does not advance (no second ExitModal, no toast) (DoQ finding)
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

function makePosition(overrides = {}) {
  return {
    id: 'pos-stop', ticker: 'STOP', market: 'US', status: 'open',
    entry_price: 100, current_price: 85, current_price_native: 85,
    stop_price: 90, stop_price_native: 90, current_trailing_stop: 90, current_trailing_stop_native: 90,
    shares: 10, fx_rate: 1.27, live_fx_rate: 1.27,
    holding_days: 20, grace_period: false, grace_days_remaining: null,
    risk_off_exit: false, entry_date: '2026-09-01', pnl: -150, pnl_percent: -15,
    ...overrides,
  };
}

const STOP_HIT = makePosition();
const UK_RISK_OFF = makePosition({
  id: 'pos-ro', ticker: 'RISK.L', market: 'UK', current_price: 120, current_price_native: 120,
  stop_price: 90, fx_rate: 1, live_fx_rate: 1,
});

/**
 * Stubs the Dashboard. `state.open` is the open-position list GET /positions returns;
 * a successful exit removes the position from it, as the backend would.
 * Returns the list of position-route requests seen ("METHOD path").
 */
async function stubDashboard(page, state, { exitStatus = 200, regimes = [], exitGate = null } = {}) {
  const calls = [];
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/market/regime**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: regimes }) })
  );
  await page.route(new RegExp(`${API}/positions(/.*)?$`), async (r) => {
    const req = r.request();
    const path = new URL(req.url()).pathname;
    calls.push(`${req.method()} ${path}`);
    if (req.method() === 'GET' && path === '/positions') {
      return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(state.open) });
    }
    const exit = path.match(/^\/positions\/([^/]+)\/exit$/);
    if (req.method() === 'POST' && exit) {
      if (exitGate) await exitGate;
      if (exitStatus !== 200) {
        return r.fulfill({ status: exitStatus, contentType: 'application/json', body: JSON.stringify({ detail: 'Price feed unavailable' }) });
      }
      state.open = state.open.filter((p) => p.id !== exit[1]);
      return r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { position_id: exit[1] } }) });
    }
    return r.fulfill({ status: 405, contentType: 'application/json', body: JSON.stringify({ detail: 'Method Not Allowed' }) });
  });
  return calls;
}

async function openMonitor(page) {
  // The "Daily Monitor" quick action is a plain onClick <div>: click its heading.
  await page.getByRole('heading', { name: 'Daily Monitor' }).click();
  await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible({ timeout: 10000 });
}

async function selectAndConfirm(page, tickers) {
  const monitor = page.getByRole('dialog');
  for (const t of tickers) await monitor.getByText(t, { exact: true }).click();
  await page.getByRole('button', { name: 'Exit Selected' }).click();
}

test.describe('Daily Position Monitor exit queue (ST-01)', () => {
  test('SC-MEQ-01: a suggested stop exit records POST /positions/{id}/exit and leaves the open list', async ({ page }) => {
    const state = { open: [STOP_HIT] };
    const calls = await stubDashboard(page, state);
    await page.goto('/#/Dashboard');
    await openMonitor(page);
    await expect(page.getByRole('dialog')).toContainText('Stop price hit');

    await selectAndConfirm(page, ['STOP']);

    const exitDialog = page.getByRole('dialog');
    await expect(exitDialog).toContainText('Exit Position');
    await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toHaveCount(0);
    await expect(page.getByTestId('exit-reason-select')).toContainText('Stop Loss Hit');
    await expect(page.getByTestId('exit-reason-preselect-note')).toHaveText(
      'Pre-selected from the Daily Position Monitor: the price is at or below the stop.'
    );
    await expect(page.getByTestId('exit-queue-progress')).toHaveCount(0);

    const exitRequest = page.waitForRequest((req) => req.method() === 'POST' && req.url().endsWith('/positions/pos-stop/exit'));
    await page.getByRole('button', { name: 'Confirm Exit' }).click();
    const body = (await exitRequest).postDataJSON();
    expect(body).toMatchObject({ shares: 10, exit_price: 85, exit_reason: 'Stop Loss Hit', exit_fx_rate: 1.27 });

    await expect(page.getByText('Exited 1 position.')).toBeVisible();
    await expect(page.getByRole('dialog')).toHaveCount(0);

    expect(calls.filter((c) => c === 'POST /positions/pos-stop/exit')).toHaveLength(1);
    expect(calls.some((c) => c.startsWith('PATCH /positions/'))).toBe(false);

    await openMonitor(page);
    await expect(page.getByRole('dialog')).toContainText('No open positions to monitor');
  });

  test('SC-MEQ-02: a failed exit shows the error, keeps the values, and Cancel returns to the Monitor', async ({ page }) => {
    const state = { open: [STOP_HIT] };
    await stubDashboard(page, state, { exitStatus: 500 });
    await page.goto('/#/Dashboard');
    await openMonitor(page);
    await selectAndConfirm(page, ['STOP']);

    const note = page.getByRole('dialog').locator('textarea');
    await note.fill('Exited on the Monitor suggestion');
    await page.getByRole('button', { name: 'Confirm Exit' }).click();

    const error = page.getByTestId('exit-error');
    await expect(error).toBeVisible();
    await expect(error).toHaveAttribute('role', 'alert');
    await expect(error).toContainText('Could not record the exit for STOP. Nothing was changed for this position.');
    await expect(error).toContainText('Price feed unavailable');
    await expect(page.getByRole('dialog')).toContainText('Exit Position');
    await expect(note).toHaveValue('Exited on the Monitor suggestion');
    await expect(page.getByRole('button', { name: 'Confirm Exit' })).toBeEnabled();

    await page.getByRole('button', { name: 'Cancel' }).click();
    await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible();
    await expect(page.getByRole('dialog')).toContainText('1 position selected for exit');
    await expect(page.getByRole('button', { name: 'Exit Selected' })).toBeVisible();
  });

  test('SC-MEQ-03: two queued positions show "Exit 1 of 2" then "Exit 2 of 2"', async ({ page }) => {
    const state = { open: [STOP_HIT, UK_RISK_OFF] };
    await stubDashboard(page, state, {
      regimes: [{ market: 'UK', status: 'risk_off' }, { market: 'US', status: 'risk_on' }],
    });
    await page.goto('/#/Dashboard');
    await openMonitor(page);
    await expect(page.getByRole('dialog')).toContainText('Market risk off');
    await selectAndConfirm(page, ['STOP', 'RISK.L']);

    const progress = page.getByTestId('exit-queue-progress');
    await expect(progress).toHaveText(
      'Exit 1 of 2 from the Daily Position Monitor. You are about to close your position in STOP.'
    );
    await page.getByRole('button', { name: 'Confirm Exit' }).click();

    await expect(progress).toHaveText(
      'Exit 2 of 2 from the Daily Position Monitor. You are about to close your position in RISK.L.'
    );
    await expect(page.getByTestId('exit-reason-select')).toContainText('Risk-Off Signal');
    await expect(page.getByTestId('exit-reason-preselect-note')).toHaveText(
      'Pre-selected from the Daily Position Monitor: the UK market is in a risk-off regime.'
    );
    await page.getByRole('button', { name: 'Confirm Exit' }).click();

    await expect(page.getByText('Exited 2 positions.')).toBeVisible();
    await expect(page.getByRole('dialog')).toHaveCount(0);
  });

  test('SC-MEQ-04: cancelling during an in-flight exit ends the queue even if the request succeeds', async ({ page }) => {
    let release;
    const exitGate = new Promise((resolve) => { release = resolve; });
    const state = { open: [STOP_HIT, UK_RISK_OFF] };
    await stubDashboard(page, state, {
      exitGate,
      regimes: [{ market: 'UK', status: 'risk_off' }, { market: 'US', status: 'risk_on' }],
    });
    await page.goto('/#/Dashboard');
    await openMonitor(page);
    await selectAndConfirm(page, ['STOP', 'RISK.L']);

    const posted = page.waitForRequest((req) => req.method() === 'POST' && req.url().endsWith('/positions/pos-stop/exit'));
    await page.getByRole('button', { name: 'Confirm Exit' }).click();
    await posted;
    await expect(page.getByRole('button', { name: 'Exiting…' })).toBeDisabled();

    await page.keyboard.press('Escape');
    await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible();

    const response = page.waitForResponse((res) => res.url().endsWith('/positions/pos-stop/exit'));
    release();
    await response;

    // The exit is recorded (STOP leaves the list) but the queue stays ended.
    await expect(page.getByRole('dialog')).not.toContainText('STOP');
    await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible();
    await expect(page.getByTestId('exit-queue-progress')).toHaveCount(0);
    await expect(page.getByText(/Exited \d+ position/)).toHaveCount(0);
    await expect(page.getByRole('dialog')).toContainText('1 position selected for exit');
  });
});
