/**
 * Trade Plan — Stop pre-fill from the signal and the stored-stop line
 * ST-14 (BLG-FE-282, EPIC-05, v9.17)
 *
 * Spec: docs/specs/frontend/pages/trade_plan.md §5a.3 (pre-fill) and §5f (stored-stop line).
 * Design: docs/design/2026-11-11__release-v9.17/trade-plan-found-defects/decision_record.md §4.
 * Addendum: the pre-fill is the Signal Context panel's "Suggested stop" (signal initial_stop, else
 * current_price − 5 × atr_value) from one helper; the stored-stop line compares the planned stop
 * with Planned Entry − 5 × atr_value.
 *
 *   SC-TPSP-01  "Plan this" (signal_id) with no initial_stop: Stop = current_price − 5×ATR
 *               (182.30 − 5 × 3.45 = 165.05), the same value the panel shows; no stored-stop line
 *   SC-TPSP-02  Watchlisted lookup (no signal_id): Stop = the signal's initial_stop (UK, 0.62)
 *   SC-TPSP-03  A typed stop is not overwritten: it survives an entry change, and the line states
 *               the stop Trade Entry will store with both values (entry 180 → $162.75; yours $160.00)
 *   SC-TPSP-04  A stop within 0.005 of the §5 stop shows no line
 *   SC-TPSP-04b A signal with no ATR shows no line (its initial_stop still pre-fills)
 *   SC-TPSP-05  Edit mode does not pre-fill: a stored plan without a stop stays blank
 *
 * Infrastructure: page.route() network interception — no live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const US_SIGNAL = {
  id: 'sig-tpsp-us', ticker: 'AAPL', market: 'US', signal_date: '2026-11-12', rank: 1, status: 'new',
  momentum_percent: 18.5, current_price: 182.3, atr_value: 3.45, initial_stop: null, regime: 'on',
};
const UK_SIGNAL = {
  id: 'sig-tpsp-uk', ticker: 'VOD.L', market: 'UK', signal_date: '2026-11-12', rank: 2, status: 'watchlisted',
  momentum_percent: 9.1, current_price: 0.72, atr_value: 0.02, initial_stop: 0.62, regime: 'on',
};
const NO_ATR_SIGNAL = { ...US_SIGNAL, id: 'sig-tpsp-noatr', atr_value: null, initial_stop: 170 };

const json = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });

async function mockApp(page, { signals = [], watchlisted = [], editPlan = null } = {}) {
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(json({ status: 'ok', data: { spy: { price: 521, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7200, is_risk_on: true }, fx_rate: 1.27 } }))
  );
  await page.route(`${API}/signals`, (r) => r.fulfill(json({ status: 'ok', data: signals })));
  await page.route(`${API}/signals?status=watchlisted`, (r) => r.fulfill(json({ status: 'ok', data: watchlisted })));
  await page.route(`${API}/portfolio/size`, (r) =>
    r.fulfill(json({ status: 'ok', data: { valid: true, suggested_shares: 10, cash_sufficient: true } }))
  );
  if (editPlan) {
    await page.route(`${API}/trade-plans/${editPlan.id}`, (r) => r.fulfill(json({ status: 'ok', data: editPlan })));
  }
}

const stop = (page) => page.getByTestId('planned-stop-price-input');
const entry = (page) => page.getByTestId('planned-entry-price-input');
const note = (page) => page.getByTestId('plan-stored-stop-note');

test('SC-TPSP-01: "Plan this" pre-fills Stop with entry − 5×ATR, the panel\'s suggested stop', async ({ page }) => {
  await mockApp(page, { signals: [US_SIGNAL] });
  await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${US_SIGNAL.id}&entry_price=182.3`);

  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 10000 });
  await expect(stop(page)).toHaveValue('165.05');
  await expect(page.getByTestId('signal-context-panel')).toContainText('$165.05');
  await expect(entry(page)).toHaveValue('182.3');
  // Planned stop equals the §5 stop at this entry: no line.
  await expect(page.getByTestId('plan-suggested-size')).toBeVisible({ timeout: 5000 });
  await expect(note(page)).toHaveCount(0);
});

test('SC-TPSP-02: the watchlisted lookup pre-fills Stop with the signal\'s initial stop', async ({ page }) => {
  await mockApp(page, { watchlisted: [UK_SIGNAL] });
  await page.goto('/#/TradePlan?ticker=VOD.L&market=UK');

  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 10000 });
  await expect(stop(page)).toHaveValue('0.62');
  await expect(page.getByTestId('signal-context-panel')).toContainText('£0.62');
});

test('SC-TPSP-03: a typed stop is kept when the entry changes, and the line states the stored stop', async ({ page }) => {
  await mockApp(page, { signals: [US_SIGNAL] });
  await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${US_SIGNAL.id}&entry_price=182.3`);
  await expect(stop(page)).toHaveValue('165.05', { timeout: 10000 });

  await stop(page).fill('160');
  await entry(page).fill('180');
  await expect(stop(page)).toHaveValue('160');

  // §5 stop = 180 − 5 × 3.45 = 162.75.
  await expect(note(page)).toHaveText(
    "Trade Entry will store a stop of about $162.75 (entry − 5×ATR, using the signal's ATR of $3.45; §5). The suggested size above uses your stop of $160.00.",
    { timeout: 5000 }
  );

  // Clearing the field is also the user's choice: it stays clear.
  await stop(page).fill('');
  await entry(page).fill('181');
  await expect(stop(page)).toHaveValue('');
  await expect(note(page)).toHaveCount(0);
});

test('SC-TPSP-04: no line when the stop is within 0.005 of the §5 stop', async ({ page }) => {
  await mockApp(page, { signals: [US_SIGNAL, NO_ATR_SIGNAL] });
  await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${US_SIGNAL.id}&entry_price=182.3`);
  await expect(stop(page)).toHaveValue('165.05', { timeout: 10000 });
  await stop(page).fill('165.054'); // within 0.005
  await expect(page.getByTestId('plan-suggested-size')).toBeVisible({ timeout: 5000 });
  await expect(note(page)).toHaveCount(0);
});

test('SC-TPSP-04b: no line when the signal has no ATR', async ({ page }) => {
  await mockApp(page, { signals: [NO_ATR_SIGNAL] });
  await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${NO_ATR_SIGNAL.id}&entry_price=182.3`);
  await expect(stop(page)).toHaveValue('170', { timeout: 10000 });
  await stop(page).fill('150');
  await expect(page.getByTestId('plan-suggested-size')).toBeVisible({ timeout: 5000 });
  await expect(note(page)).toHaveCount(0);
});

test('SC-TPSP-05: edit mode does not pre-fill the stop', async ({ page }) => {
  const plan = {
    id: 'plan-tpsp-edit', ticker: 'VOD.L', market: 'UK', status: 'draft', position_id: null, checklist_items: [],
    planned_entry_price: 0.72, planned_stop_price: null, planned_quantity: null,
  };
  await mockApp(page, { watchlisted: [UK_SIGNAL], editPlan: plan });
  await page.goto(`/#/TradePlan?edit=${plan.id}`);
  await expect(entry(page)).toHaveValue('0.72', { timeout: 10000 });
  await expect(stop(page)).toHaveValue('');
});
