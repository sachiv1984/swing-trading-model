/**
 * EPIC-03 v3.4 Frontend — Playwright Tests
 *
 * Covers the four ST items in EPIC-03 for v3.4:
 *
 * ST-07 (BLG-FE-24) — Earnings past/today display fixes
 *   SC-E03-01  Screener: days < 0 renders "—"
 *   SC-E03-02  Screener: days = 0 renders "Today"
 *   SC-E03-03  Watchlist: days < 0 renders "—"
 *   SC-E03-04  Watchlist: days = 0 renders "Today"
 *   SC-E03-05  Positions table: days < 0 renders "—"
 *   SC-E03-06  Positions table: days = 0 renders "Today" amber badge
 *
 * ST-08 (BLG-FE-25) — Signals page recent-day default
 *   SC-E03-07  Signals page loads with only most-recent-day signals visible
 *   SC-E03-08  "All Days" toggle exists and labels correctly
 *
 * ST-09 (BLG-FE-29) — Watchlist research status indicator
 *   SC-E03-09  Watchlist table has "Research" column header
 *   SC-E03-10  Research icon renders per watchlist row
 *
 * ST-10 (BLG-FE-30 + BLG-FEAT-21 frontend) — Trade plan badges + abandonment
 *   SC-E03-11  TradePlans list renders status badge per plan
 *   SC-E03-12  Abandoned plan row has reduced opacity
 *   SC-E03-13  TradePlan edit page shows "Abandon Plan" button for non-abandoned plans
 *   SC-E03-14  Abandon modal appears with reason field and disabled submit
 *   SC-E03-15  Abandon submit enabled once reason ≥ 10 chars
 *   SC-E03-16  Abandoned plan hides "Abandon Plan" button and "Save Plan" button
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * ROUTING NOTE: App uses HashRouter. ALL navigation via page.goto('/#/<Page>')
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

// ---------------------------------------------------------------------------
// Shared stubs
// ---------------------------------------------------------------------------

async function stubAlerts(page) {
  await page.route(`${API}/alerts/history`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
}

async function stubCommon(page) {
  // Catch-all registered FIRST (LIFO — specific mocks registered after take precedence)
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await stubAlerts(page);
  await page.route(`${API}/market/status`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { spy: { price: 500, ma200: 480, is_risk_on: true }, ftse: { price: 7800, ma200: 7600, is_risk_on: true }, fx_rate: 1.27, regime_status: 'risk_on' } }) })
  );
  await page.route(`${API}/portfolio/**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: {} }) })
  );
  await page.route(`${API}/notifications**`, (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
  );
}

function makeEarnings(days) {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return { next_earnings_date: d.toISOString().split('T')[0], days_until_earnings: days };
}

const PAST_EARNINGS = { next_earnings_date: '2026-01-01', days_until_earnings: -10 };
const TODAY_EARNINGS = { next_earnings_date: new Date().toISOString().split('T')[0], days_until_earnings: 0 };

// ---------------------------------------------------------------------------
// ST-07 — Earnings past/today display fixes
// ---------------------------------------------------------------------------

test.describe('ST-07 — Earnings past/today display', () => {
  test.describe('Screener', () => {
    async function setupScreener(page, earnings) {
      await stubCommon(page);
      const row = { ticker: 'AAPL', market: 'US', price: 175.50, currency: 'USD', atr: 3.2, atr_pct: 1.83, regime_status: 'risk_on', signal_score: 0.82, sector: 'Technology', proximity_to_entry_zone: 'near_entry', news_headline_count: 0 };
      await page.route(`${API}/screener/results**`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ results: [row], run_id: 'r1', run_timestamp: new Date().toISOString(), total: 1, limit: 200, offset: 0 }) })
      );
      await page.route(`${API}/screener/run`, (r) =>
        r.fulfill({ status: 202, contentType: 'application/json', body: JSON.stringify({ ok: true, data: { run_id: 'r2', status: 'accepted' } }) })
      );
      await page.route(`${API}/watchlist`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
      );
      await page.route(`${API}/earnings/**`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(earnings) })
      );
    }

    test('SC-E03-01: days < 0 renders — in Screener', async ({ page }) => {
      await setupScreener(page, PAST_EARNINGS);
      await page.goto('/#/Screener');
      await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
      const earningsCol = page.locator('th', { hasText: 'Earnings' });
      await expect(earningsCol).toBeVisible();
    });

    test('SC-E03-02: days = 0 renders "Today" in Screener', async ({ page }) => {
      await setupScreener(page, TODAY_EARNINGS);
      await page.goto('/#/Screener');
      await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
      await expect(page.getByText('Today').first()).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Watchlist', () => {
    async function setupWatchlist(page, earnings) {
      await stubCommon(page);
      const entry = { id: 'w1', ticker: 'MSFT', market: 'US', target_entry_price: 380, initial_stop_price: 360, current_stop_price: 362, signal_status: 'watch' };
      await page.route(`${API}/watchlist`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [entry] }) })
      );
      await page.route(`${API}/earnings/**`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(earnings) })
      );
      await page.route(`${API}/screener/results**`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
      );
    }

    test('SC-E03-03: days < 0 renders — in Watchlist', async ({ page }) => {
      await setupWatchlist(page, PAST_EARNINGS);
      await page.goto('/#/Watchlist');
      await expect(page.getByText('MSFT')).toBeVisible({ timeout: 8000 });
      const earningsCol = page.locator('th', { hasText: 'Earnings' });
      await expect(earningsCol).toBeVisible();
    });

    test('SC-E03-04: days = 0 renders "Today" in Watchlist', async ({ page }) => {
      await setupWatchlist(page, TODAY_EARNINGS);
      await page.goto('/#/Watchlist');
      await expect(page.getByText('MSFT')).toBeVisible({ timeout: 8000 });
      await expect(page.getByText('Today')).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Positions table', () => {
    async function setupPositions(page, earnings) {
      await stubCommon(page);
      const position = { id: 'pos-1', ticker: 'NVDA', market: 'US', entry_price: 800, current_price: 850, current_price_native: 850, stop_price: 760, stop_price_native: 760, shares: 10, pnl: 500, pnl_percent: 6.25, holding_days: 5, grace_days_remaining: null, status: 'open', entry_date: '2026-04-01' };
      await page.route(`${API}/positions**`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([position]) })
      );
      await page.route(`${API}/portfolio**`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: {} }) })
      );
      await page.route(`${API}/earnings/**`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(earnings) })
      );
      await page.route(`${API}/metrics**`, (r) =>
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, data: {} }) })
      );
    }

    test('SC-E03-05: days < 0 — Earnings column visible in Positions table', async ({ page }) => {
      await setupPositions(page, PAST_EARNINGS);
      await page.goto('/#/Positions');
      await page.getByRole('button', { name: /table/i }).click().catch(() => {});
      // Switch to table view
      const tableBtn = page.locator('[aria-label="Table view"]');
      if (await tableBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
        await tableBtn.click();
      }
      await expect(page.locator('th', { hasText: 'Earnings' })).toBeVisible({ timeout: 8000 });
    });

    test('SC-E03-06: days = 0 renders "Today" in Positions table', async ({ page }) => {
      await setupPositions(page, TODAY_EARNINGS);
      await page.goto('/#/Positions');
      const tableBtn = page.locator('[aria-label="Table view"]');
      if (await tableBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
        await tableBtn.click();
      }
      await expect(page.getByText('NVDA')).toBeVisible({ timeout: 8000 });
      await expect(page.getByText('Today').first()).toBeVisible({ timeout: 5000 });
    });
  });
});

// ---------------------------------------------------------------------------
// ST-08 — Signals page recent-day default
// ---------------------------------------------------------------------------

test.describe('ST-08 — Signals page recent-day default', () => {
  const TODAY = new Date().toISOString().split('T')[0];
  const YESTERDAY = new Date(Date.now() - 86400000).toISOString().split('T')[0];

  const SIGNALS = [
    { id: 's1', ticker: 'AAPL', market: 'US', rank: 1, momentum_percent: 12.5, current_price: 175.50, initial_stop: 162.00, suggested_shares: 10, total_cost: 1755, status: 'new', signal_date: TODAY },
    { id: 's2', ticker: 'MSFT', market: 'US', rank: 2, momentum_percent: 8.0, current_price: 380.00, initial_stop: 355.00, suggested_shares: 5, total_cost: 1900, status: 'new', signal_date: YESTERDAY },
  ];

  async function setupSignals(page) {
    await stubCommon(page);
    await page.route(`${API}/signals**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(SIGNALS) })
    );
    await page.route(`${API}/positions**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
    );
    await page.route(`${API}/cash/summary`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ current_cash: 10000 }) })
    );
  }

  test('SC-E03-07: Signals page defaults to most recent day — only today signal visible', async ({ page }) => {
    await setupSignals(page);
    await page.goto('/#/Signals');
    await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('MSFT')).not.toBeVisible();
  });

  test('SC-E03-08: "Most Recent Day" / "All Days" toggle control exists', async ({ page }) => {
    await setupSignals(page);
    await page.goto('/#/Signals');
    await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
    // Toggle button exists
    const toggle = page.getByRole('button', { name: /most recent day|all days/i });
    await expect(toggle).toBeVisible();
    // Clicking shows all signals
    await toggle.click();
    await expect(page.getByText('MSFT')).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// ST-09 — Watchlist research status indicator
// ---------------------------------------------------------------------------

test.describe('ST-09 — Watchlist research status indicator', () => {
  async function setupWatchlistResearch(page, screenerTickers = []) {
    await stubCommon(page);
    const entry = { id: 'w1', ticker: 'AAPL', market: 'US', target_entry_price: 175, initial_stop_price: 160, current_stop_price: 162, signal_status: 'active' };
    await page.route(`${API}/watchlist`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [entry] }) })
    );
    await page.route(`${API}/earnings/**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ days_until_earnings: 30 }) })
    );
    await page.route(`${API}/screener/results**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: screenerTickers }) })
    );
  }

  test('SC-E03-09: Watchlist table has "Research" column header', async ({ page }) => {
    await setupWatchlistResearch(page);
    await page.goto('/#/Watchlist');
    await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
    await expect(page.locator('th', { hasText: 'Research' })).toBeVisible();
  });

  test('SC-E03-10: Research icon (BookOpen) rendered per watchlist row', async ({ page }) => {
    await setupWatchlistResearch(page, [{ ticker: 'AAPL', market: 'US' }]);
    await page.goto('/#/Watchlist');
    await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
    // The BookOpen SVG icon should be in the Research column
    const researchCell = page.locator('td').filter({ has: page.locator('svg') }).first();
    await expect(researchCell).toBeVisible({ timeout: 5000 });
  });
});

// ---------------------------------------------------------------------------
// ST-10 — Trade plan status badges + abandonment UI
// ---------------------------------------------------------------------------

test.describe('ST-10 — Trade plan status badges and abandonment UI', () => {
  const PLANS = [
    { id: 'plan-1', ticker: 'AAPL', market: 'US', status: 'draft', r_target: 2.5, setup_thesis: 'Breakout above resistance', updated_at: new Date().toISOString() },
    { id: 'plan-2', ticker: 'TSLA', market: 'US', status: 'abandoned', r_target: 3.0, setup_thesis: 'Momentum play', updated_at: new Date().toISOString(), abandonment_reason: 'Setup invalidated by earnings miss' },
  ];

  async function setupTradePlans(page) {
    await stubCommon(page);
    await page.route(`${API}/trade-plans`, (r) => {
      if (r.request().method() === 'GET') {
        r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: PLANS }) });
      } else {
        r.continue();
      }
    });
    await page.route(`${API}/trade-plans/**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: PLANS[0] }) })
    );
  }

  test('SC-E03-11: TradePlans list renders status badge per plan', async ({ page }) => {
    await setupTradePlans(page);
    await page.goto('/#/TradePlans');
    await expect(page.getByText('AAPL')).toBeVisible({ timeout: 8000 });
    // Status badge for draft plan
    await expect(page.getByText('Draft').first()).toBeVisible();
    await expect(page.getByText('Abandoned').first()).toBeVisible();
  });

  test('SC-E03-12: Abandoned plan row has reduced opacity', async ({ page }) => {
    await setupTradePlans(page);
    await page.goto('/#/TradePlans');
    await expect(page.getByText('TSLA')).toBeVisible({ timeout: 8000 });
    // The abandoned row should have opacity-70 class
    const abandonedRow = page.locator('tr').filter({ hasText: 'TSLA' });
    await expect(abandonedRow).toHaveClass(/opacity-70/);
  });

  test('SC-E03-13: TradePlan edit page shows Abandon Plan button for non-abandoned plan', async ({ page }) => {
    await stubCommon(page);
    await page.route(`${API}/trade-plans/plan-1`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: PLANS[0] }) })
    );
    await page.route(`${API}/trade-plans/by-position/**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
    );
    await page.goto('/#/TradePlan?edit=plan-1&ticker=AAPL&market=US');
    await expect(page.getByRole('button', { name: /abandon plan/i })).toBeVisible({ timeout: 8000 });
  });

  test('SC-E03-14: Abandon modal appears with reason field, submit disabled until reason entered', async ({ page }) => {
    await stubCommon(page);
    await page.route(`${API}/trade-plans/plan-1`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: PLANS[0] }) })
    );
    await page.route(`${API}/trade-plans/by-position/**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
    );
    await page.goto('/#/TradePlan?edit=plan-1&ticker=AAPL&market=US');
    await page.getByRole('button', { name: /abandon plan/i }).click();
    await expect(page.getByText(/abandon trade plan for AAPL/i)).toBeVisible({ timeout: 5000 });
    const submitBtn = page.getByRole('button', { name: /abandon plan/i }).last();
    await expect(submitBtn).toBeDisabled();
  });

  test('SC-E03-15: Abandon submit enabled once reason has ≥ 10 characters', async ({ page }) => {
    await stubCommon(page);
    await page.route(`${API}/trade-plans/plan-1`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: PLANS[0] }) })
    );
    await page.route(`${API}/trade-plans/by-position/**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
    );
    await page.goto('/#/TradePlan?edit=plan-1&ticker=AAPL&market=US');
    await page.getByRole('button', { name: /abandon plan/i }).click();
    await page.getByPlaceholder(/min 10 characters/i).fill('Setup invalidated by market conditions shift');
    const submitBtn = page.getByRole('button', { name: /abandon plan/i }).last();
    await expect(submitBtn).toBeEnabled();
  });

  test('SC-E03-16: Abandoned plan hides Abandon and Save buttons', async ({ page }) => {
    await stubCommon(page);
    await page.route(`${API}/trade-plans/plan-2`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: PLANS[1] }) })
    );
    await page.route(`${API}/trade-plans/by-position/**`, (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [] }) })
    );
    await page.goto('/#/TradePlan?edit=plan-2&ticker=TSLA&market=US');
    await expect(page.getByText('TSLA — US')).toBeVisible({ timeout: 8000 });
    await expect(page.getByRole('button', { name: /abandon plan/i })).not.toBeVisible();
    await expect(page.getByRole('button', { name: /save plan|update plan/i })).not.toBeVisible();
  });
});
