/**
 * Research View → Trade Plan carries the market (ST-13, BLG-FE-281, EPIC-05, v9.17)
 *
 * research_view.md v1.5 §4.7: "Create Trade Plan" navigates to
 * /TradePlan?ticker={ticker}&market={market}, with market from GET /research/{ticker}.
 * Before v9.17 the link sent only the ticker, and TradePlan.js defaults a missing market
 * to US, so a UK plan was sized and priced as US. "View full plan" opens edit mode,
 * which loads the plan's stored market.
 *
 *   SC-RCPM-01  UK ticker (VOD.L) → Create Trade Plan → market UK in the URL, the Market
 *               field and the header; the suggested-size request is sent with market UK
 *               and no FX rate; the What-If panel has no USD FX field (amounts in £)
 *   SC-RCPM-02  US ticker (AAPL) → Create Trade Plan → market US, unchanged
 *   SC-RCPM-03  UK ticker with a stored plan → View full plan → edit mode shows the stored
 *               market UK (no market parameter needed)
 *
 * Infrastructure: page.route() network interception — no live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const UK_PLAN_ID = '00000000-0000-0000-0000-000000000013';

const research = (ticker, market) => ({
  status: 'ok',
  data: {
    ticker,
    market,
    signal: null,
    regime: { label: 'risk_on', spy_risk_on: true, ftse_risk_on: true },
    sector: { sector: 'Communication Services', industry: 'Telecom Services' },
    screener: null,
    earnings: null,
  },
});

const UK_PLAN = {
  id: UK_PLAN_ID, ticker: 'VOD.L', market: 'UK', status: 'draft', position_id: null,
  setup_type: 'Momentum Continuation', setup_thesis: '', entry_rationale: '',
  checklist_items: [], planned_entry_price: null, planned_stop_price: null, planned_quantity: null,
};

const json = (body) => ({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });

async function mockApp(page, { ticker, market, plans = [] }) {
  const sizeRequests = [];
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill(json({ status: 'ok', data: { spy: { price: 521, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7200, is_risk_on: true }, fx_rate: 1.27 } }))
  );
  await page.route(new RegExp(`${API}/research/`), (r) => r.fulfill(json(research(ticker, market))));
  await page.route(new RegExp(`${API}/trade-plans\\?ticker=`), (r) => r.fulfill(json({ status: 'ok', data: plans })));
  await page.route(`${API}/trade-plans/${UK_PLAN_ID}`, (r) => r.fulfill(json({ status: 'ok', data: UK_PLAN })));
  await page.route(`${API}/portfolio/size`, (r) => {
    sizeRequests.push(r.request().postDataJSON());
    return r.fulfill(json({ status: 'ok', data: { valid: true, suggested_shares: 100, cash_sufficient: true } }));
  });
  return sizeRequests;
}

async function openResearch(page, ticker) {
  await page.goto(`/#/research/${ticker}`);
  await expect(page.getByRole('heading', { level: 1 }).filter({ hasText: /Research/i })).toBeVisible({ timeout: 10000 });
}

const marketField = (page) => page.locator('[aria-labelledby="trade-plan-market-label"]');

test('SC-RCPM-01: a UK ticker\'s Create Trade Plan opens a UK plan', async ({ page }) => {
  const sizeRequests = await mockApp(page, { ticker: 'VOD.L', market: 'UK' });
  await openResearch(page, 'VOD.L');

  await page.getByRole('button', { name: 'Create Trade Plan' }).click();
  await expect(page).toHaveURL(/#\/TradePlan\?ticker=VOD\.L&market=UK$/, { timeout: 5000 });
  await expect(marketField(page)).toHaveValue('UK', { timeout: 8000 });
  await expect(page.getByText('VOD.L — UK')).toBeVisible();

  await page.getByTestId('planned-entry-price-input').fill('0.72');
  await page.getByTestId('planned-stop-price-input').fill('0.65');
  await expect.poll(() => sizeRequests.length, { timeout: 5000 }).toBeGreaterThan(0);
  const last = sizeRequests[sizeRequests.length - 1];
  expect(last.market).toBe('UK');
  expect(last.fx_rate).toBeUndefined();

  // §5d: the What-If panel asks for a USD FX rate on US plans only; a UK plan works in £.
  // The panel opens expanded.
  await expect(page.getByTestId('what-if-entry-price-input')).toBeVisible();
  await expect(page.getByTestId('what-if-fx-rate-input')).toHaveCount(0);
});

test('SC-RCPM-02: a US ticker\'s Create Trade Plan still opens a US plan', async ({ page }) => {
  const sizeRequests = await mockApp(page, { ticker: 'AAPL', market: 'US' });
  await openResearch(page, 'AAPL');

  await page.getByRole('button', { name: 'Create Trade Plan' }).click();
  await expect(page).toHaveURL(/#\/TradePlan\?ticker=AAPL&market=US$/, { timeout: 5000 });
  await expect(marketField(page)).toHaveValue('US', { timeout: 8000 });
  await expect(page.getByText('AAPL — US')).toBeVisible();

  await page.getByTestId('planned-entry-price-input').fill('180');
  await page.getByTestId('planned-stop-price-input').fill('170');
  await expect.poll(() => sizeRequests.length, { timeout: 5000 }).toBeGreaterThan(0);
  expect(sizeRequests[sizeRequests.length - 1].market).toBe('US');
  await expect(page.getByTestId('what-if-fx-rate-input')).toBeVisible();
});

test('SC-RCPM-03: View full plan opens the stored plan in its stored market', async ({ page }) => {
  await mockApp(page, { ticker: 'VOD.L', market: 'UK', plans: [UK_PLAN] });
  await openResearch(page, 'VOD.L');

  await page.getByRole('button', { name: 'View full plan' }).click();
  await expect(page).toHaveURL(new RegExp(`#/TradePlan\\?edit=${UK_PLAN_ID}&ticker=VOD\\.L$`), { timeout: 5000 });
  await expect(marketField(page)).toHaveValue('UK', { timeout: 8000 });
});
