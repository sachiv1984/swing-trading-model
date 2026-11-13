/**
 * Trade Plan — the pre-entry acknowledgement resets when the check result changes
 * ST-12 (BLG-FE-278, EPIC-05, v9.17)
 *
 * Spec: docs/specs/frontend/pages/trade_plan.md v1.26 §5e (Acknowledgement reset), option (a)
 * clear on change (RISK-05, Strategy Rules & System Intent Owner, 2026-11-12).
 * Design: docs/design/2026-11-11__release-v9.17/trade-plan-found-defects/decision_record.md §2.
 *
 * Result key = advisory_status + the set of {rule, status} pairs (not detail, not captured_at).
 *
 *   SC-TPAR-01  Tick at WARN; a quantity change brings a new FAIL → box unticked and the reset note
 *               shows; saving without ticking sends acknowledged false with the FAIL snapshot, and
 *               Trade Entry, linking that plan, shows the panel with the unacknowledged reason line
 *   SC-TPAR-02  Ticking again hides the note; a refetch with the same result (entry price changed,
 *               same statuses, different detail) keeps the box ticked with no note
 *   SC-TPAR-03  A result that returns to PASS hides the box and the note, and saves false
 *   SC-TPAR-04  Edit: the stored acknowledgement shows when the first result's key equals the
 *               stored snapshot's key
 *   SC-TPAR-05  Edit: a first result whose key differs from the stored snapshot starts unticked
 *               with the note
 *
 * Infrastructure: page.route() network interception — no live backend. Clock fixed so the
 * snapshot is fresh for Trade Entry's 24-hour rule (position_form.md v1.14).
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const NOW = new Date('2026-11-13T12:00:00Z');
const RESET_NOTE = 'The check results changed. Review them and tick again to acknowledge.';
const UNACK_REASON = "The linked plan's checks had warnings that were not acknowledged.";

const checks = (cash, detail = 'Cash check') => [
  { rule: 'regime_gate', status: 'pass', detail: 'UK market is risk-on' },
  { rule: 'cash_constraint', status: cash, detail },
];
// Quantity decides the outcome: up to 50 shares PASS, up to 200 WARN, above that FAIL.
const outcomeFor = (quantity, entryPrice) => {
  const q = Number(quantity);
  if (q <= 50) return { advisory_status: 'pass', checks: checks('pass') };
  if (q <= 200) return { advisory_status: 'warn', checks: checks('warn', `Cash within 5% of limit at ${entryPrice || 'market'}`) };
  return { advisory_status: 'fail', checks: checks('fail', 'Insufficient cash') };
};

const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

async function mockApp(page, { editPlan = null, onPost, onPut } = {}) {
  await page.clock.setFixedTime(NOW);
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(json({ status: 'ok', data: { spy: { price: 521, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7200, is_risk_on: true }, fx_rate: 1.27 } }))
  );
  await page.route(new RegExp(`${API}/portfolio/pre-entry-validation`), (r) => {
    const url = new URL(r.request().url());
    return r.fulfill(json({ status: 'ok', data: outcomeFor(url.searchParams.get('quantity'), url.searchParams.get('entry_price')) }));
  });
  await page.route(`${API}/trade-plans`, (r) => {
    if (r.request().method() === 'POST') {
      const body = r.request().postDataJSON();
      if (onPost) onPost(body);
      return r.fulfill(json({ status: 'ok', data: { ...body, id: 'plan-tpar-new' } }, 201));
    }
    return r.fulfill(json({ status: 'ok', data: [] }));
  });
  if (editPlan) {
    await page.route(`${API}/trade-plans/${editPlan.id}`, (r) => {
      if (r.request().method() === 'PUT' && onPut) onPut(r.request().postDataJSON());
      return r.fulfill(json({ status: 'ok', data: editPlan }));
    });
  }
}

const box = (page) => page.getByTestId('override-acknowledgement-checkbox');
const note = (page) => page.getByTestId('acknowledgement-reset-note');
const badge = (page, label) => page.getByTestId('pre-entry-checks-panel').getByText(label, { exact: true });
const shares = (page) => page.getByTestId('planned-quantity-input');

async function openNewPlan(page) {
  await page.goto('/#/TradePlan?ticker=LGEN&market=UK');
  await expect(page.getByTestId('planned-entry-price-input')).toBeVisible({ timeout: 10000 });
}

async function tickAtWarn(page) {
  await shares(page).fill('100');
  await expect(badge(page, 'Warn')).toBeVisible({ timeout: 8000 });
  await expect(note(page)).toHaveCount(0); // the first result is not a change
  await box(page).check();
  await expect(box(page)).toBeChecked();
}

test('SC-TPAR-01: a new FAIL unticks the box; saving unacknowledged reaches Trade Entry as unacknowledged', async ({ page }) => {
  let posted = null;
  await mockApp(page, { onPost: (b) => { posted = b; } });
  await openNewPlan(page);
  await tickAtWarn(page);

  await shares(page).fill('500');
  await expect(badge(page, 'Fail')).toBeVisible({ timeout: 8000 });
  await expect(box(page)).not.toBeChecked();
  await expect(note(page)).toHaveText(RESET_NOTE);

  // Save stays enabled (advisory).
  await page.getByRole('button', { name: /save plan/i }).click();
  await expect.poll(() => posted).not.toBeNull();
  expect(posted.pre_entry_override_acknowledged).toBe(false);
  expect(posted.pre_entry_validation_snapshot.advisory_status).toBe('fail');
  expect(posted.pre_entry_validation_snapshot.captured_at).toBe(NOW.toISOString());

  // Trade Entry, linked to the plan just saved (position_form.md v1.14 §Pre-Entry Checks).
  const saved = { ...posted, id: 'plan-tpar-new', updated_at: NOW.toISOString() };
  await page.route(`${API}/trade-plans`, (r) => r.fulfill(json({ status: 'ok', data: [saved] })));
  await page.route(`${API}/trade-plans/${saved.id}`, (r) => r.fulfill(json({ status: 'ok', data: saved })));
  await page.goto('/#/TradeEntry');
  await expect(page.getByTestId('link-trade-plan-select')).toBeVisible({ timeout: 10000 });
  await page.getByPlaceholder('e.g., AAPL or VOD.L').fill('LGEN');
  await page.getByPlaceholder('0.00').first().fill('100');
  await page.getByPlaceholder('Fetched automatically if blank').fill('2');
  await page.getByPlaceholder('0', { exact: true }).fill('500');
  await page.getByTestId('link-trade-plan-select').click();
  await page.getByRole('option', { name: /LGEN/ }).click();

  await expect(page.getByTestId('pre-entry-rerun-reason')).toHaveText(UNACK_REASON, { timeout: 10000 });
  await expect(page.getByTestId('pre-entry-checks-panel')).toHaveCount(1);
  await expect(page.getByTestId('pre-entry-checks-on-plan')).toHaveCount(0);
});

test('SC-TPAR-02: ticking again hides the note; the same result refetched keeps the tick', async ({ page }) => {
  await mockApp(page);
  await openNewPlan(page);
  await tickAtWarn(page);

  await shares(page).fill('500');
  await expect(note(page)).toBeVisible({ timeout: 8000 });
  await box(page).check();
  await expect(note(page)).toHaveCount(0);

  // Back to WARN: a key change again, so the tick clears once more.
  await shares(page).fill('150');
  await expect(badge(page, 'Warn')).toBeVisible({ timeout: 8000 });
  await expect(box(page)).not.toBeChecked();
  await box(page).check();

  // Entry price changes the request and the detail text, not the {rule, status} pairs.
  await page.getByTestId('planned-entry-price-input').fill('101');
  await expect(page.getByTestId('pre-entry-check-cash_constraint')).toContainText('at 101', { timeout: 8000 });
  await expect(box(page)).toBeChecked();
  await expect(note(page)).toHaveCount(0);
});

test('SC-TPAR-03: a result back at PASS hides the box and the note and saves false', async ({ page }) => {
  let posted = null;
  await mockApp(page, { onPost: (b) => { posted = b; } });
  await openNewPlan(page);
  await tickAtWarn(page);

  await shares(page).fill('20');
  await expect(badge(page, 'Pass')).toBeVisible({ timeout: 8000 });
  await expect(box(page)).toHaveCount(0);
  await expect(note(page)).toHaveCount(0);

  await page.getByRole('button', { name: /save plan/i }).click();
  await expect.poll(() => posted).not.toBeNull();
  expect(posted.pre_entry_override_acknowledged).toBe(false);
  expect(posted.pre_entry_validation_snapshot.advisory_status).toBe('pass');
});

const storedPlan = (snapshot) => ({
  id: 'plan-tpar-edit', ticker: 'LGEN', market: 'UK', status: 'draft', position_id: null, checklist_items: [],
  planned_quantity: 100, planned_entry_price: 100, planned_stop_price: 90,
  pre_entry_override_acknowledged: true,
  pre_entry_validation_snapshot: snapshot,
});

test('SC-TPAR-04: edit — the stored tick shows when the first result matches the stored snapshot', async ({ page }) => {
  // Same statuses as the live WARN, older detail and capture time: the same key.
  const plan = storedPlan({ captured_at: '2026-11-12T09:00:00.000Z', advisory_status: 'warn', checks: checks('warn', 'older detail'), inputs: {} });
  let put = null;
  await mockApp(page, { editPlan: plan, onPut: (b) => { put = b; } });
  await page.goto(`/#/TradePlan?edit=${plan.id}`);
  await expect(badge(page, 'Warn')).toBeVisible({ timeout: 10000 });
  await expect(box(page)).toBeChecked();
  await expect(note(page)).toHaveCount(0);

  await page.getByRole('button', { name: /update plan/i }).click();
  await expect.poll(() => put).not.toBeNull();
  expect(put.pre_entry_override_acknowledged).toBe(true);
});

test('SC-TPAR-05: edit — a first result that differs from the stored snapshot starts unticked with the note', async ({ page }) => {
  // Stored when the plan passed; the market has moved since and the checks now WARN.
  const plan = storedPlan({ captured_at: '2026-11-12T09:00:00.000Z', advisory_status: 'pass', checks: checks('pass'), inputs: {} });
  let put = null;
  await mockApp(page, { editPlan: plan, onPut: (b) => { put = b; } });
  await page.goto(`/#/TradePlan?edit=${plan.id}`);
  await expect(badge(page, 'Warn')).toBeVisible({ timeout: 10000 });
  await expect(box(page)).not.toBeChecked();
  await expect(note(page)).toHaveText(RESET_NOTE);

  await page.getByRole('button', { name: /update plan/i }).click();
  await expect.poll(() => put).not.toBeNull();
  expect(put.pre_entry_override_acknowledged).toBe(false);
});
