/**
 * Stateful mock backend for the trade plan lifecycle journey.
 * Used by tests/e2e/trade-plan-lifecycle.spec.js (ST-26) and tests/e2e/arc2-happy-path.spec.js (ST-24),
 * EPIC-06, v9.16. See trade-plan-lifecycle.spec.js's header for which backend rules each write
 * handler copies, and for the known gap tracked by BLG-BE-211 (plan not moved to `closed` on exit).
 *
 * Partial copies: POST /portfolio/position links only an explicit trade_plan_id; the backend's
 * get_unlinked_trade_plan_for_entry auto-link fallback is not modelled, so a test where the frontend
 * omits trade_plan_id fails here even though production might still link by ticker. The initial stop
 * is rounded to 2 dp; the backend does not round. POST /portfolio/size returns a fixed fixture, not a
 * §4.1 calculation.
 */

'use strict';

const API = 'http://localhost:8000';
const EXIT_PRICE = 210; // the Positions row's native price; the Exit modal defaults to it

const SIGNAL_ID = 'sig-tpl-0001';
const SIGNAL = {
  id: SIGNAL_ID, ticker: 'AAPL', market: 'US', signal_date: '2026-11-09', rank: 1,
  momentum_percent: 18.5, current_price: 182.3, price_gbp: 143.0, atr_value: 3.45,
  volatility: 0.012, initial_stop: 165.05, suggested_shares: 10, allocation_gbp: 1430.0,
  total_cost: 1430.0, status: 'new', ma200: 160, regime_on: true,
};

const QUALITY = {
  gate_not_met: false, ticker: 'AAPL', score: 82, matching_trades: 25, win_rate: 72.0,
  average_pnl_pct: 4.5, score_explanation: 'Based on 25 closed trades.',
};

const SCREENER_ROW = {
  ticker: 'AAPL', market: 'US', price: 182.3, currency: 'USD', atr: 3.45, atr_pct: 1.9,
  regime_status: 'risk_on', signal_score: 0.85, sector: 'Technology',
  proximity_to_entry_zone: 'near_entry', news_headline_count: 0,
};

const RESEARCH = {
  ticker: 'AAPL', market: 'US',
  signal: { signal_id: SIGNAL_ID, direction: 'long', signal_date: '2026-11-09', status: 'active', rank: 1, atr: 3.45, entry_price: 182.3, stop_price: 165.05, r_target: 2 },
  regime: { label: 'risk_on', spy_risk_on: true, ftse_risk_on: true },
  sector: { sector: 'Technology', industry: 'Consumer Electronics' },
  screener: { in_latest_results: true, latest_run_timestamp: '2026-11-10T06:00:00Z', score: 85, atr_pct: 0.019 },
  earnings: { next_earnings_date: '2027-01-28', days_until_earnings: 79, fiscal_quarter: 'Q1 2027', data_source: 'yfinance' },
};

const HEAT = {
  valid: true, current_heat_percent: 4.0, prospective_heat_percent: 5.0, incremental_heat_percent: 1.0,
  prospective_risk_gbp: 200, portfolio_value_gbp: 20000, ticker: 'AAPL',
};

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
  // Screener and Research View (Arc 2 PT-02/PT-03), for the arc-level happy path.
  await page.route(`${API}/screener/results**`, (r) =>
    r.fulfill(ok({ results: [SCREENER_ROW], run_id: 'run-tpl', run_timestamp: now(), total: 1, limit: 200, offset: 0 }))
  );
  await page.route(`${API}/screener/regime-distribution**`, (r) =>
    r.fulfill(ok({ ok: true, data: { window: '30d', run_count: 1, total_observations: 1, risk_on_count: 1, risk_off_count: 0, risk_on_pct: 100, risk_off_pct: 0 } }))
  );
  await page.route(`${API}/watchlist`, (r) => r.fulfill(ok({ items: [] })));
  await page.route(`${API}/research/AAPL`, (r) => r.fulfill(ok({ status: 'ok', data: RESEARCH })));
  await page.route(new RegExp(`${API}/portfolio/prospective-heat`), (r) => r.fulfill(ok({ status: 'ok', data: HEAT })));

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

module.exports = { API, SIGNAL, QUALITY, RESEARCH, EXIT_PRICE, computePlanVsReality, mockBackend };
