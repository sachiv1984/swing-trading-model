/**
 * Trade plan lifecycle, end to end (ST-26, BLG-QA-23, EPIC-06, v9.16)
 *
 * One journey through the app as built after EPIC-02 (ST-07 "Plan this", ST-08 suggested size):
 *
 *   SC-TPL-01  Signals "Plan this" → Trade Plan pre-filled; the Setup Quality Score is visible;
 *              entering the stop pre-fills Planned Shares with the §4.1 suggestion; Save Plan
 *              creates a `draft` plan carrying the suggested size
 *   SC-TPL-02  Reopening the saved plan shows the same quality score (it is recomputed per
 *              ticker, not stored on the plan, so "persistence" means it survives a reload)
 *   SC-TPL-03  Trade Plans → "Start Trade" → Trade Entry pre-filled from the plan; Create Position
 *              sends trade_plan_id; the plan moves `draft` → `active` and gains position_id
 *   SC-TPL-04  Positions → Exit → Confirm Exit closes the position and writes a trade
 *   SC-TPL-05  Trade History → expand the trade → Plan vs Reality shows the values the backend
 *              formulas give for the plan and fills entered above (R achieved, R target, R delta,
 *              entry delta, adherence badge, state at exit)
 *
 * The scenarios run as one test because each step depends on state the previous one wrote.
 *
 * Mock backend: page.route() over an in-memory store (`db`). The write handlers copy the
 * backend's own rules so the journey's state is the state production would hold:
 *   - POST /portfolio/position: initial stop = entry − 5×ATR (calculations.py::calculate_initial_stop);
 *     an explicit trade_plan_id links the plan and sets status `active` (position_service.py::add_position)
 *   - POST /positions/{id}/exit: planned_entry_price is snapshotted from the ticker's signal
 *     current_price (position_service.py, Arc 4 PO-01); the plan's status is left unchanged — see
 *     the known gap below
 *   - GET /trades/{id}/plan-vs-reality: a port of plan_vs_reality_service.py::compute_plan_vs_reality.
 *     The formulas themselves are unit-tested in tests/test_plan_vs_reality.py; this test checks that
 *     the numbers entered through the UI reach that comparison and are displayed correctly. The
 *     expected values below are worked by hand, not read back from the port.
 *
 * Known gap (BLG-BE-211, filed by this story): data_model.md §Trade Plan Lifecycle says `active` →
 * `closed` happens when the linked position closes, but no backend code path writes `closed`. This
 * test therefore does not assert the plan's status after the exit; when BLG-BE-211 ships, add that
 * assertion (Trade Plans badge "Closed") and make the exit handler below set it.
 *
 * Infrastructure: page.route() network interception — no live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const SIGNAL = {
  id: 'sig-tpl-0001', ticker: 'AAPL', market: 'US', signal_date: '2026-11-09', rank: 1,
  momentum_percent: 18.5, current_price: 182.3, price_gbp: 143.0, atr_value: 3.45,
  volatility: 0.012, initial_stop: 165.05, suggested_shares: 10, allocation_gbp: 1430.0,
  total_cost: 1430.0, status: 'new', ma200: 160, regime_on: true,
};

const QUALITY = {
  gate_not_met: false, ticker: 'AAPL', score: 82, matching_trades: 25, win_rate: 72.0,
  average_pnl_pct: 4.5, score_explanation: 'Based on 25 closed trades.',
};

// Values the user enters along the journey.
const PLAN_STOP = '165.05';
const PLAN_R_TARGET = '2';
const PLAN_EARLY_EXIT = 'Close below the 50-day MA';
const ACTUAL_ENTRY = '184';
const ACTUAL_ATR = '3.45';
const EXIT_PRICE = 210; // the Positions row's native price; the Exit modal defaults to it

const ok = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
const round2 = (n) => Math.round(n * 100) / 100;

// ─── Port of backend/services/plan_vs_reality_service.py ──────────────────────
function computePlanVsReality(trade, position, plan) {
  const entry = trade.entry_price;
  const exit = trade.exit_price;
  const stop = position ? position.initial_stop : null;
  const risk = stop == null ? null : entry - stop;
  const rAchieved = risk ? round2((exit - entry) / risk) : null;
  const rTarget = plan.r_target == null ? null : Number(plan.r_target);
  const rDelta = rAchieved != null && rTarget != null ? round2(rAchieved - rTarget) : null;

  const plannedStop = plan.planned_stop_price == null ? null : Number(plan.planned_stop_price);
  let stopDiscipline = 'not_captured';
  if (plannedStop != null && stop != null) {
    const diff = (Math.abs(stop - plannedStop) / plannedStop) * 100;
    stopDiscipline = diff <= 1.0 ? 'on_plan' : diff <= 5.0 ? 'minor_deviation' : 'deviation';
  }

  const plannedEntry = trade.planned_entry_price;
  const entryDelta = plannedEntry ? round2(((entry - plannedEntry) / plannedEntry) * 100) : null;

  const exitReason = trade.exit_reason;
  const early = plan.early_exit_conditions;
  let flag = 'on_plan';
  if (entryDelta != null && Math.abs(entryDelta) > 2.0) flag = 'entry_deviation';
  else if (stopDiscipline === 'deviation') flag = 'stop_deviation';
  else if (exitReason && early) {
    const kw = ['stop', 'loss', 'cut', 'early', 'trailing'];
    const r = exitReason.toLowerCase();
    if (kw.some((k) => r.includes(k)) && kw.some((k) => early.toLowerCase().includes(k))) flag = 'on_plan';
    else flag = ['target', 'target hit'].includes(r) ? 'on_plan' : 'early_exit';
  }

  return {
    plan_linked: true, trade_plan_id: plan.id, r_achieved: rAchieved, r_target: rTarget, r_delta: rDelta,
    entry_delta_pct: entryDelta, stop_discipline: stopDiscipline, exit_reason_actual: exitReason,
    exit_reason_planned: early || null, lifecycle_state_at_exit: position ? position.position_state : null,
    plan_adherence_flag: flag, deviation_note: null,
  };
}

// ─── Stateful mock backend ────────────────────────────────────────────────────
async function mockBackend(page) {
  const db = { plans: [], positions: [], trades: [], log: [] };
  const now = () => new Date().toISOString();

  // Catch-all first; later routes take precedence.
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(ok({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(ok({ status: 'ok', data: { spy: { price: 521, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7200, is_risk_on: true }, fx_rate: 1.27 } }))
  );
  await page.route(`${API}/cash/summary`, (r) => r.fulfill(ok({ status: 'ok', current_cash: 20000 })));
  await page.route(new RegExp(`${API}/signals(\\?.*)?$`), (r) => {
    const status = new URL(r.request().url()).searchParams.get('status');
    const data = status ? [SIGNAL].filter((s) => s.status === status) : [SIGNAL];
    return r.fulfill(ok({ status: 'ok', data }));
  });
  await page.route(/\/portfolio\/size/, (r) =>
    r.fulfill(ok({ status: 'ok', data: {
      valid: true, suggested_shares: 10.7, risk_amount: 200, stop_distance: 17.25, estimated_cost: 1535,
      estimated_fees: 0, fx_rate_used: 1.27, cash_sufficient: true, available_cash: 20000,
      concentration_adjusted: false, concentration_reason: null,
    } }))
  );

  // Trade plans: list/create, then by id, then the fixed sub-paths (registered last so they win).
  await page.route(new RegExp(`${API}/trade-plans(\\?.*)?$`), (r) => {
    const req = r.request();
    if (req.method() === 'POST') {
      const body = req.postDataJSON();
      const plan = { ...body, id: 'plan-tpl-0001', status: body.status || 'draft', position_id: null, created_at: now(), updated_at: now() };
      db.plans.push(plan);
      db.log.push(['plan', plan.status]);
      return r.fulfill({ ...ok({ status: 'ok', data: plan }), status: 201 });
    }
    const ticker = new URL(req.url()).searchParams.get('ticker');
    return r.fulfill(ok({ status: 'ok', data: ticker ? db.plans.filter((p) => p.ticker === ticker) : db.plans }));
  });
  await page.route(new RegExp(`${API}/trade-plans/[^/?]+$`), (r) => {
    const id = new URL(r.request().url()).pathname.split('/').pop();
    const plan = db.plans.find((p) => p.id === id);
    if (r.request().method() === 'PUT' && plan) Object.assign(plan, r.request().postDataJSON(), { updated_at: now() });
    return r.fulfill(ok({ status: 'ok', data: plan || null }));
  });
  await page.route(new RegExp(`${API}/trade-plans/by-position/`), (r) => {
    const id = new URL(r.request().url()).pathname.split('/').pop();
    return r.fulfill(ok({ status: 'ok', data: db.plans.filter((p) => p.position_id === id) }));
  });
  await page.route(new RegExp(`${API}/trade-plans/setup-quality-score\\?ticker=AAPL`), (r) => r.fulfill(ok({ status: 'ok', data: QUALITY })));
  await page.route(`${API}/trade-plans/tags`, (r) => r.fulfill(ok({ status: 'ok', data: [] })));

  // Position entry — position_service.py::add_position.
  await page.route(`${API}/portfolio/position`, (r) => {
    const body = r.request().postDataJSON();
    const initialStop = round2(body.entry_price - 5 * body.atr_value);
    const position = {
      id: 'pos-tpl-0001', ticker: body.ticker, market: body.market, entry_price: body.entry_price,
      shares: body.shares, fx_rate: body.fx_rate, atr_value: body.atr_value, initial_stop: initialStop,
      entry_date: new Date().toISOString(), status: 'open', position_state: 'PROFITABLE',
    };
    db.positions.push(position);
    const plan = body.trade_plan_id ? db.plans.find((p) => p.id === body.trade_plan_id) : null;
    let linked = false;
    if (plan && !plan.position_id) {
      Object.assign(plan, { position_id: position.id, status: 'active', updated_at: now() });
      db.log.push(['plan', 'active']);
      linked = true;
    }
    db.lastEntry = body;
    return r.fulfill(ok({ status: 'ok', data: {
      ticker: body.ticker, total_cost: 1450, fees_paid: 2.2, entry_price: body.entry_price,
      initial_stop: initialStop, remaining_cash: 18550, position_id: position.id,
      trade_plan_linked: linked, trade_plan_id: linked ? plan.id : null,
    } }));
  });

  // Positions page (shape as positions-exit-modal.spec.js).
  const openRows = () => db.positions.filter((p) => p.status === 'open').map((p) => ({
    ...p, current_price: round2(EXIT_PRICE / 1.25), current_price_native: EXIT_PRICE, live_fx_rate: 1.25,
    stop_price: round2(p.initial_stop / 1.25), stop_price_native: p.initial_stop, current_trailing_stop: p.initial_stop,
    pnl: 200, pnl_percent: 14.1, holding_days: 20, grace_days_remaining: null, risk_off_exit: false,
    lifecycle_state: p.position_state, days_in_state: 5, tags: null, last_reviewed_at: new Date().toISOString(),
  }));
  await page.route('**/positions*', (r) => {
    const url = r.request().url();
    if (/\/(compliance|grace-period-alerts|gap-risk|exit)/.test(url)) return r.fallback();
    return r.fulfill(ok(openRows()));
  });
  await page.route('**/positions/*/gap-risk', (r) =>
    r.fulfill(ok({ status: 'ok', data: { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false } }))
  );
  await page.route('**/positions/compliance*', (r) => r.fulfill(ok({ status: 'ok', data: [] })));
  await page.route('**/positions/grace-period-alerts', (r) => r.fulfill(ok({ data: [] })));
  await page.route('**/portfolio/drawdown-status', (r) => r.fulfill(ok({ status: 'ok', data: { threshold_breached: false } })));
  await page.route('**/portfolio/concentration-status', (r) => r.fulfill(ok({ status: 'ok', data: { any_breach: false } })));

  // Exit — position_service.py close path.
  await page.route('**/positions/*/exit', (r) => {
    const id = new URL(r.request().url()).pathname.split('/').slice(-2)[0];
    const body = r.request().postDataJSON();
    const position = db.positions.find((p) => p.id === id);
    position.status = 'closed';
    const hasPlan = db.plans.some((p) => p.position_id === id);
    const trade = {
      id: 'trade-tpl-0001', position_id: id, ticker: position.ticker, market: position.market,
      entry_date: position.entry_date.slice(0, 10), exit_date: body.exit_date,
      entry_price: position.entry_price, exit_price: body.exit_price, shares: body.shares,
      pnl: round2((body.exit_price - position.entry_price) * body.shares / body.exit_fx_rate),
      pnl_pct: round2(((body.exit_price - position.entry_price) / position.entry_price) * 100),
      exit_reason: body.exit_reason || 'Manual Exit', fee_drag_pct: null, slippage_pct: null,
      tags: [], entry_note: null, exit_note: null,
      planned_entry_price: hasPlan ? SIGNAL.current_price : null,
    };
    db.trades.push(trade);
    db.lastExit = body;
    return r.fulfill(ok({ status: 'ok', data: { position_id: id, exit_price: body.exit_price, shares: body.shares } }));
  });

  // Trade History.
  await page.route(/\/trades$/, (r) =>
    r.fulfill(ok({ status: 'ok', total_trades: db.trades.length, win_rate: 100, total_pnl: 0, avg_slippage_pct: null, avg_fee_drag_pct: null, trades: db.trades }))
  );
  await page.route(/\/trades\/[^/]+\/plan-vs-reality$/, (r) => {
    const id = new URL(r.request().url()).pathname.split('/').slice(-2)[0];
    const trade = db.trades.find((t) => t.id === id);
    const position = trade && db.positions.find((p) => p.id === trade.position_id);
    const plan = position && db.plans.find((p) => p.position_id === position.id);
    if (!plan) return r.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ detail: 'No trade plan found for this trade' }) });
    return r.fulfill(ok({ status: 'ok', data: computePlanVsReality(trade, position, plan) }));
  });

  return db;
}

const planStatusBadge = (page, label) =>
  page.locator('tr', { hasText: 'AAPL' }).getByText(label, { exact: true });

test('SC-TPL-01..05: a plan goes from "Plan this" to a closed trade and its Plan vs Reality', async ({ page }) => {
  test.setTimeout(120000);
  const db = await mockBackend(page);

  // ── SC-TPL-01: create the plan from a signal, with the quality score visible ──
  await page.goto('/#/Signals');
  await page.getByTestId('signal-plan-this-AAPL').click();
  await expect(page).toHaveURL(/#\/TradePlan\?/, { timeout: 8000 });
  await expect(page.getByTestId('planned-entry-price-input')).toHaveValue('182.3', { timeout: 8000 });
  await expect(page.getByTestId('signal-context-panel')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('setup-quality-score-panel')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82');

  await page.getByTestId('planned-stop-price-input').fill(PLAN_STOP);
  await expect(page.getByTestId('plan-suggested-size')).toHaveText('Suggested size: 10 shares (§4.1, 1% risk)', { timeout: 5000 });
  await expect(page.getByTestId('planned-quantity-input')).toHaveValue('10');
  await page.getByPlaceholder('e.g. 2.5').fill(PLAN_R_TARGET);
  await page.getByPlaceholder('Under what conditions would you exit before the stop is hit?').fill(PLAN_EARLY_EXIT);
  await page.getByRole('button', { name: /save plan/i }).click();
  await expect(page.getByText('Trade plan saved successfully.')).toBeVisible({ timeout: 8000 });

  expect(db.plans).toHaveLength(1);
  expect(db.plans[0]).toMatchObject({
    ticker: 'AAPL', market: 'US', status: 'draft', position_id: null,
    planned_entry_price: 182.3, planned_stop_price: 165.05, planned_quantity: 10, r_target: 2,
    early_exit_conditions: PLAN_EARLY_EXIT,
  });

  // ── SC-TPL-02: the quality score is still shown when the saved plan is reopened ──
  await page.goto('/#/TradePlan?edit=plan-tpl-0001');
  await expect(page.getByTestId('planned-stop-price-input')).toHaveValue('165.05', { timeout: 10000 });
  await expect(page.getByTestId('setup-quality-score-value')).toHaveText('82', { timeout: 8000 });

  // ── SC-TPL-03: start the trade from the plan; the plan links and becomes active ──
  await page.goto('/#/TradePlans');
  await expect(planStatusBadge(page, 'Draft')).toBeVisible({ timeout: 10000 });
  await page.getByTestId('start-trade-from-plan-plan-tpl-0001').click();
  await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 5000 });
  await expect(page.getByPlaceholder('e.g., AAPL or VOD.L')).toHaveValue('AAPL', { timeout: 8000 });
  await expect(page.getByPlaceholder('0', { exact: true })).toHaveValue('10');
  await expect(page.getByPlaceholder('0.00').first()).toHaveValue('182.3');
  await page.getByPlaceholder('0.00').first().fill(ACTUAL_ENTRY);
  await page.getByPlaceholder('Fetched automatically if blank').fill(ACTUAL_ATR);
  await page.getByRole('button', { name: /create position/i }).click();
  await expect(page.getByText('Linked to trade plan for AAPL.', { exact: false })).toBeVisible({ timeout: 8000 });
  await expect(page).toHaveURL(/#\/Positions/, { timeout: 8000 });

  expect(db.lastEntry).toMatchObject({ ticker: 'AAPL', trade_plan_id: 'plan-tpl-0001', entry_price: 184, shares: 10, atr_value: 3.45 });
  expect(db.plans[0]).toMatchObject({ status: 'active', position_id: 'pos-tpl-0001' });
  expect(db.log).toEqual([['plan', 'draft'], ['plan', 'active']]);

  await page.goto('/#/TradePlans');
  await expect(planStatusBadge(page, 'Active')).toBeVisible({ timeout: 10000 });
  await expect(page.getByTestId('start-trade-from-plan-plan-tpl-0001')).toHaveCount(0);

  // ── SC-TPL-04: close the position ──
  await page.goto('/#/Positions');
  await page.waitForSelector('text=AAPL', { timeout: 8000 });
  await page.locator('[aria-label="Table view"]').click();
  await page.getByRole('button', { name: 'Exit AAPL' }).click();
  const modal = page.getByRole('dialog', { name: 'Exit Position' });
  await expect(modal).toBeVisible({ timeout: 5000 });
  await modal.getByRole('button', { name: 'Confirm Exit' }).click();
  await expect(modal).toBeHidden({ timeout: 5000 });

  expect(db.lastExit).toMatchObject({ shares: 10, exit_price: EXIT_PRICE });
  expect(db.positions[0].status).toBe('closed');
  expect(db.trades).toHaveLength(1);

  // ── SC-TPL-05: Plan vs Reality for the closed trade ──
  // Worked by hand from the values entered above:
  //   initial stop   = 184 − 5 × 3.45                  = 166.75
  //   R achieved     = (210 − 184) / (184 − 166.75)     = 1.507 → +1.51R
  //   R delta        = 1.51 − 2                         = −0.49R
  //   entry delta    = (184 − 182.30) / 182.30 × 100    = +0.93%   (planned entry snapshotted from the signal)
  //   stop vs plan   = |166.75 − 165.05| / 165.05       = 1.03% → minor_deviation (not a stop deviation)
  //   adherence      = exit reason is not a target and the plan has early-exit conditions → Early Exit
  await page.goto('/#/TradeHistory');
  await expect(page.locator('h1')).toBeVisible({ timeout: 10000 });
  await page.getByText('AAPL').first().click();
  const pvr = page.getByTestId('plan-vs-reality-section');
  await expect(pvr).toBeVisible({ timeout: 8000 });
  await expect(pvr).toContainText('+1.51R');
  await expect(pvr).toContainText('Target: 2R');
  await expect(pvr).toContainText('−0.49R vs target');
  await expect(pvr).toContainText('+0.93%');
  await expect(pvr).toContainText(`Planned: ${PLAN_EARLY_EXIT}`);
  await expect(pvr).toContainText('PROFITABLE');
  await expect(pvr).toContainText('Early Exit');
});
