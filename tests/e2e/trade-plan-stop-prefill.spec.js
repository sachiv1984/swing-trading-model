/**
 * Trade Plan — Stop pre-fill from the signal and the stored-stop line
 * ST-14 (BLG-FE-282, EPIC-05, v9.17)
 *
 * Spec: docs/specs/frontend/pages/trade_plan.md §5a.3 (pre-fill) and §5f (stored-stop line).
 * Design: docs/design/2026-11-11__release-v9.17/trade-plan-found-defects/decision_record.md §4.
 * Addendum: the pre-fill is the Signal Context panel's "Suggested stop" (signal initial_stop, else
 * current_price − 5 × ATR) from one helper; the stored-stop line compares the planned stop with
 * Planned Entry − 5 × ATR.
 *
 * Data shape (signal_service.py): GET /signals returns atr_value in GBP for BOTH markets
 * (US: native ATR / live FX), while current_price and initial_stop are native. The fixtures copy
 * that shape: US atr_value 2.7165 = 3.45 / 1.27. The ATR the page uses is the native one
 * (getSignalAtr: UK atr_value; US (current_price − initial_stop) / 5). PR #2260 review P2: the
 * first version subtracted the GBP atr_value from a USD entry and was tested with a USD fixture.
 *
 *   SC-TPSP-01  "Plan this", real-shaped US signal: Stop = initial_stop 165.05, the panel's suggested
 *               stop; the panel's ATR is the native $3.45, not the stored GBP 2.72; an untouched
 *               pre-fill shows no stored-stop line (the P2 regression: it used to say "about $168.72")
 *   SC-TPSP-02  Watchlisted lookup (no signal_id), UK with real rounding: Stop = initial_stop 0.63;
 *               ATR (0.72 − 0.63) / 5 = £0.02; no line at the signal's price (re-review finding a)
 *   SC-TPSP-03  A typed stop is not overwritten: it survives an entry change, and the line states
 *               the stop Trade Entry will store with both values (entry 180 → $162.75; yours $160.00)
 *   SC-TPSP-04  A stop within 0.005 of the §5 stop shows no line
 *   SC-TPSP-04b A US signal without initial_stop: no native ATR, so no pre-fill and no line (the GBP
 *               atr_value is never used against a USD price)
 *   SC-TPSP-05  Edit mode does not pre-fill: a stored plan without a stop stays blank
 *   SC-TPSP-06  A pre-filled stop belongs to its ticker: changing the ticker clears an untouched
 *               pre-fill, and a typed stop survives the ticker change (DoQ review finding 1)
 *   SC-TPSP-07  A stop typed (or typed and cleared) before the signal arrives is not overwritten
 *               when it does (DoQ review finding 2)
 *   SC-TPSP-08  A UK signal without initial_stop pre-fills current_price − 5 × atr_value (0.72 − 0.15 = 0.57)
 *
 * Infrastructure: page.route() network interception — no live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const US_SIGNAL = {
  id: 'sig-tpsp-us', ticker: 'AAPL', market: 'US', signal_date: '2026-11-12', rank: 1, status: 'new',
  momentum_percent: 18.5, current_price: 182.3, atr_value: 2.7165, initial_stop: 165.05, regime: 'on',
};
const UK_SIGNAL = {
  id: 'sig-tpsp-uk', ticker: 'VOD.L', market: 'UK', signal_date: '2026-11-12', rank: 2, status: 'watchlisted',
  // Real rounding: price 0.7249 → current_price 0.72 (2 dp), ATR 0.0191 (4 dp), initial_stop
  // round(0.7249 − 0.0955, 2) = 0.63. 0.72 − 5 × 0.0191 = 0.6245 would not match the stop.
  momentum_percent: 9.1, current_price: 0.72, atr_value: 0.0191, initial_stop: 0.63, regime: 'on',
};
const US_NO_STOP_SIGNAL = { ...US_SIGNAL, id: 'sig-tpsp-nostop', initial_stop: null };
const UK_NO_STOP_SIGNAL = { ...UK_SIGNAL, id: 'sig-tpsp-uk-nostop', atr_value: 0.03, initial_stop: null };

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

test('SC-TPSP-01: "Plan this" pre-fills the suggested stop; an untouched pre-fill shows no line', async ({ page }) => {
  await mockApp(page, { signals: [US_SIGNAL] });
  await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${US_SIGNAL.id}&entry_price=182.3`);

  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 10000 });
  await expect(stop(page)).toHaveValue('165.05');
  await expect(page.getByTestId('signal-context-panel')).toContainText('$165.05');
  // Native ATR from the USD stop, not the stored GBP atr_value ($2.72).
  await expect(page.getByTestId('signal-context-atr')).toHaveText('$3.45');
  await expect(entry(page)).toHaveValue('182.3');
  // Planned stop equals the §5 stop at this entry: no line.
  await expect(page.getByTestId('plan-suggested-size')).toBeVisible({ timeout: 5000 });
  await expect(note(page)).toHaveCount(0);
});

test('SC-TPSP-02: the watchlisted lookup pre-fills Stop with the signal\'s initial stop', async ({ page }) => {
  await mockApp(page, { watchlisted: [UK_SIGNAL] });
  await page.goto('/#/TradePlan?ticker=VOD.L&market=UK');

  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 10000 });
  await expect(stop(page)).toHaveValue('0.63');
  await expect(page.getByTestId('signal-context-panel')).toContainText('£0.63');
  await expect(page.getByTestId('signal-context-atr')).toHaveText('£0.02');
  // The watchlisted route has no entry_price; at the signal's price the pre-fill is the §5 stop.
  await entry(page).fill('0.72');
  await expect(page.getByTestId('plan-suggested-size')).toBeVisible({ timeout: 5000 });
  await expect(note(page)).toHaveCount(0);
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
  await mockApp(page, { signals: [US_SIGNAL] });
  await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${US_SIGNAL.id}&entry_price=182.3`);
  await expect(stop(page)).toHaveValue('165.05', { timeout: 10000 });
  await stop(page).fill('165.054'); // within 0.005
  await expect(page.getByTestId('plan-suggested-size')).toBeVisible({ timeout: 5000 });
  await expect(note(page)).toHaveCount(0);
});

test('SC-TPSP-04b: a US signal without initial_stop gives no pre-fill and no line', async ({ page }) => {
  await mockApp(page, { signals: [US_NO_STOP_SIGNAL] });
  await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${US_NO_STOP_SIGNAL.id}&entry_price=182.3`);
  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('signal-context-atr')).toHaveCount(0);
  await expect(stop(page)).toHaveValue('');
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

test('SC-TPSP-06: changing the ticker clears an untouched pre-filled stop, not a typed one', async ({ page }) => {
  await mockApp(page, { signals: [US_SIGNAL] });
  await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${US_SIGNAL.id}&entry_price=182.3`);
  await expect(stop(page)).toHaveValue('165.05', { timeout: 10000 });

  const ticker = page.getByPlaceholder('e.g. AAPL');
  await ticker.fill('MSFT');
  await expect(stop(page)).toHaveValue('');

  // A stop the user typed is theirs, whatever the ticker.
  await stop(page).fill('300');
  await ticker.fill('NVDA');
  await expect(stop(page)).toHaveValue('300');
});

for (const [label, typed] of [['typed', '150'], ['typed and cleared', '']]) {
  test(`SC-TPSP-07 (${label}): a stop ${label} before the signal arrives is kept`, async ({ page }) => {
    await mockApp(page, { signals: [US_SIGNAL] });
    let release;
    const signalGate = new Promise((resolve) => { release = resolve; });
    // Registered after mockApp, so it takes precedence: /signals answers only once released.
    await page.route(`${API}/signals`, async (r) => {
      await signalGate;
      return r.fulfill(json({ status: 'ok', data: [US_SIGNAL] }));
    });
    await page.goto(`/#/TradePlan?ticker=AAPL&market=US&signal_id=${US_SIGNAL.id}&entry_price=182.3`);
    await expect(stop(page)).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('signal-context-panel')).toHaveCount(0);

    await stop(page).fill('150');
    if (typed === '') await stop(page).fill('');
    release();

    await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('signal-context-panel')).toContainText('$165.05');
    await expect(stop(page)).toHaveValue(typed);
  });
}

test('SC-TPSP-08: a UK signal without initial_stop pre-fills current_price − 5 × ATR', async ({ page }) => {
  await mockApp(page, { watchlisted: [UK_NO_STOP_SIGNAL] });
  await page.goto('/#/TradePlan?ticker=VOD.L&market=UK');
  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 10000 });
  await expect(stop(page)).toHaveValue('0.57');
  await expect(page.getByTestId('signal-context-panel')).toContainText('£0.57');
});
