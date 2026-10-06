/**
 * v9.10 ST-08 / ST-09 (BLG-FE-198 / BLG-FE-199, EPIC-02) — exit-condition surfacing.
 *
 * Design source: docs/design/2026-10-06__release-v9.10/exit-condition-surfacing/decision_record.md §5
 * Specs: positions.md §Exit Dialog Pre-Selection and Deep Link; dashboard.md §1A Exit Conditions Met Row
 *
 *   SC-ECP-01..04  Shared predicate (src/lib/exitCondition.js): priority order and grace boundary
 *   SC-EXD-01  Risk-off position opens the exit dialog with "Risk-Off Signal" and its note
 *   SC-EXD-02  Post-grace breached position opens with "Stop Loss Hit" and its note
 *   SC-EXD-03  In-grace breached position and an ordinary position open with "Manual Exit", no note
 *   SC-EXD-04  Changing the selection hides the note
 *   SC-EXD-05  /#/Positions?exit={id} opens the right dialog and the parameter is cleared
 *   SC-EXC-01  Dashboard card lists qualifying positions with reason pills and Review exit links
 *   SC-EXC-02  Dashboard card is absent when no position qualifies
 *
 * Infrastructure: page.route() network interception — no live backend required.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const { getExitCondition } = require('../../src/lib/exitCondition.js');

const API = 'http://localhost:8000';

function makePosition(overrides = {}) {
  return {
    id: 'pos-ord', ticker: 'ORDY', market: 'US', status: 'open',
    entry_price: 100, current_price: 110, current_price_native: 110,
    current_trailing_stop: 90, current_trailing_stop_native: 90,
    stop_price: 90, stop_price_native: 90, shares: 10, fx_rate: 1, live_fx_rate: 1,
    holding_days: 20, grace_period: false, grace_days_remaining: null,
    risk_off_exit: false, entry_date: '2026-09-01', pnl: 100, pnl_percent: 10,
    position_state: 'PROFITABLE', days_in_state: 3,
    ...overrides,
  };
}

const RISK_OFF = makePosition({ id: 'pos-ro', ticker: 'RISK', risk_off_exit: true });
const BREACHED = makePosition({ id: 'pos-br', ticker: 'BRCH', current_price: 85, current_price_native: 85 });
const IN_GRACE_BREACHED = makePosition({
  id: 'pos-gr', ticker: 'GRCE', current_price: 85, current_price_native: 85,
  grace_period: true, grace_days_remaining: 4, holding_days: 6,
});
const ORDINARY = makePosition();

// ---------------------------------------------------------------------------
// Predicate
// ---------------------------------------------------------------------------

test.describe('Shared exit-condition predicate', () => {
  test('SC-ECP-01: risk-off takes priority over a stop breach', () => {
    const c = getExitCondition({ ...BREACHED, risk_off_exit: true });
    expect(c).toEqual({ reason: 'Risk-Off Signal', riskOff: true, stopBreach: true });
  });
  test('SC-ECP-02: post-grace price at the stop is a breach', () => {
    expect(getExitCondition(makePosition({ current_price: 90 })).reason).toBe('Stop Loss Hit');
  });
  test('SC-ECP-03: in grace, a breach is not an exit condition', () => {
    expect(getExitCondition(IN_GRACE_BREACHED).reason).toBeNull();
  });
  test('SC-ECP-04: no stop computed (0) and ordinary positions have no condition', () => {
    expect(getExitCondition(makePosition({ current_trailing_stop: 0, current_price: 1 })).reason).toBeNull();
    expect(getExitCondition(ORDINARY).reason).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// Exit dialog
// ---------------------------------------------------------------------------

async function stubPositionsPage(page, positions) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { spy: { price: 500, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7600, is_risk_on: true }, fx_rate: 1.27 } }) })
  );
  await page.route(`${API}/positions**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) })
  );
  await page.route(`${API}/positions/grace-period-alerts`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function openTable(page, path = '/#/Positions') {
  await page.goto(path);
  await page.waitForLoadState('domcontentloaded');
  const tableBtn = page.locator('[aria-label="Table view"]');
  if (await tableBtn.isVisible({ timeout: 3000 }).catch(() => false)) await tableBtn.click();
}

async function openExitFor(page, ticker) {
  await page.getByRole('button', { name: `Exit ${ticker}`, exact: true }).click();
  await expect(page.getByRole('dialog')).toBeVisible();
}

test.describe('Exit dialog pre-selection (ST-08)', () => {
  test('SC-EXD-01: risk-off position pre-selects Risk-Off Signal with a note', async ({ page }) => {
    await stubPositionsPage(page, [RISK_OFF]);
    await openTable(page);
    await openExitFor(page, 'RISK');
    await expect(page.getByTestId('exit-reason-select')).toContainText('Risk-Off Signal');
    await expect(page.getByTestId('exit-reason-preselect-note')).toHaveText(
      'Pre-selected because the US market is in a risk-off regime (index below its 200-day average).'
    );
  });

  test('SC-EXD-02: post-grace breached position pre-selects Stop Loss Hit with a note', async ({ page }) => {
    await stubPositionsPage(page, [BREACHED]);
    await openTable(page);
    await openExitFor(page, 'BRCH');
    await expect(page.getByTestId('exit-reason-select')).toContainText('Stop Loss Hit');
    await expect(page.getByTestId('exit-reason-preselect-note')).toHaveText(
      'Pre-selected because the price is at or below the trailing stop and the grace period has ended.'
    );
  });

  for (const [label, pos] of [['in-grace breached', IN_GRACE_BREACHED], ['ordinary', ORDINARY]]) {
    test(`SC-EXD-03: ${label} position defaults to Manual Exit with no note`, async ({ page }) => {
      await stubPositionsPage(page, [pos]);
      await openTable(page);
      await openExitFor(page, pos.ticker);
      await expect(page.getByTestId('exit-reason-select')).toContainText('Manual Exit');
      await expect(page.getByTestId('exit-reason-preselect-note')).toHaveCount(0);
    });
  }

  test('SC-EXD-04: choosing a different reason hides the note', async ({ page }) => {
    await stubPositionsPage(page, [BREACHED]);
    await openTable(page);
    await openExitFor(page, 'BRCH');
    await expect(page.getByTestId('exit-reason-preselect-note')).toBeVisible();
    await page.getByTestId('exit-reason-select').click();
    await page.getByRole('option', { name: 'Manual Exit' }).click();
    await expect(page.getByTestId('exit-reason-select')).toContainText('Manual Exit');
    await expect(page.getByTestId('exit-reason-preselect-note')).toHaveCount(0);
  });

  test('SC-EXD-05: ?exit= deep link opens that dialog and clears the parameter', async ({ page }) => {
    await stubPositionsPage(page, [ORDINARY, BREACHED]);
    // No view switch here: the deep-linked dialog opens over the page straight away.
    await page.goto('/#/Positions?exit=pos-br');
    await expect(page.getByRole('dialog')).toBeVisible({ timeout: 8000 });
    await expect(page.getByRole('dialog')).toContainText('BRCH');
    await expect(page.getByTestId('exit-reason-select')).toContainText('Stop Loss Hit');
    await expect.poll(() => page.url()).not.toContain('exit=');
  });
});

// ---------------------------------------------------------------------------
// Dashboard card
// ---------------------------------------------------------------------------

async function gotoDashboard(page, positions) {
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(`${API}/positions`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) })
  );
  await page.goto('/#/DashboardHome');
  await expect(page.getByTestId('morning-briefing')).toBeVisible({ timeout: 10000 });
}

test.describe('Exit Conditions Met row (ST-09)', () => {
  test('SC-EXC-01: lists qualifying positions with pills and exit links', async ({ page }) => {
    await gotoDashboard(page, [RISK_OFF, BREACHED, IN_GRACE_BREACHED, ORDINARY]);
    const card = page.getByTestId('exit-conditions-card');
    await expect(card).toBeVisible({ timeout: 8000 });
    await expect(card.getByTestId('exit-conditions-count')).toHaveText('(2)');
    await expect(card.getByTestId('exit-conditions-row-pos-ro')).toContainText('RISK OFF');
    await expect(card.getByTestId('exit-conditions-row-pos-br')).toContainText('STOP REACHED');
    await expect(card.getByTestId('exit-conditions-row-pos-gr')).toHaveCount(0);
    await expect(card).toContainText('Nothing is exited automatically.');
    const link = card.getByRole('link', { name: 'Review exit for BRCH' });
    await expect(link).toHaveAttribute('href', '#/Positions?exit=pos-br');
  });

  test('SC-EXC-02: absent when no position qualifies', async ({ page }) => {
    await gotoDashboard(page, [IN_GRACE_BREACHED, ORDINARY]);
    await expect(page.getByTestId('morning-briefing')).toBeVisible();
    await expect(page.getByTestId('exit-conditions-card')).toHaveCount(0);
  });
});
