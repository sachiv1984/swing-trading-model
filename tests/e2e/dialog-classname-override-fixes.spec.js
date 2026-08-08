/**
 * Dialog className-Override Fixes — ST-15 (BLG-FE-142, EPIC-04, v8.4)
 *
 * This project's cn() (src/lib/utils.js) is plain clsx with no tailwind-merge,
 * so a Dialog* consumer's className override does not reliably beat the base
 * component's own hardcoded className (src/components/ui/dialog.js) for the
 * same CSS property — the winner is decided by Tailwind's compiled stylesheet
 * order, not by prop precedence. See docs/ops/dialog_classname_override_audit_2026-08-07.md
 * for the full audit (method: a real `tailwindcss` build of the project's own
 * config was inspected to determine actual winners, not assumed from
 * documentation) and the "!"-prefix fix pattern (matching ComplianceRecheckModal.js,
 * ST-11, EPIC-03, v8.3).
 *
 * Coverage — each scenario asserts the actual computed style of the property
 * that was previously silently losing to the base component:
 *
 *   SC-DCO-01  WidgetLibrary DialogContent: max-width and display are the
 *              override's values (max-w-2xl / flex), not the base's (max-w-lg / grid)
 *   SC-DCO-02  WidgetLibrary DialogTitle: font-weight is the override's value
 *              (bold/700), not the base's (semibold/600)
 *   SC-DCO-03  MonitorModal DialogContent: max-width and display are the
 *              override's values (max-w-2xl / flex), not the base's (max-w-lg / grid)
 *   SC-DCO-04  ExportModal DialogTitle: font-weight is the override's value
 *              (bold/700), not the base's (semibold/600)
 *   SC-DCO-05  TradeReflectionModal DialogContent: max-width and display are the
 *              override's values (max-w-2xl / flex), not the base's (max-w-lg / grid)
 *   SC-DCO-06  TradePlan.js Abandon-plan DialogContent: border-radius is the
 *              override's value (rounded-2xl), not the base's responsive
 *              sm:rounded-lg, at a >=640px viewport
 *   SC-DCO-07  WatchlistModal DialogFooter: justify-content is the override's
 *              value (space-between), not the base's responsive sm:justify-end,
 *              at a >=640px viewport
 *
 * Infrastructure: Playwright page.route() network interception. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 * Default viewport (playwright.config.js) is 1280x900 — above the 640px `sm:`
 * breakpoint relevant to SC-DCO-06/07.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

/** Dashboard.js's positions queries (base44.entities.Position.list/filter) hit GET
 *  /positions, which returns a raw array (not the {status,data} wrapper) — registered
 *  after mockFallback so this more specific route takes precedence for that URL. */
async function mockDashboardPositions(page) {
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
}

/** Reads the computed style of the first open [role="dialog"] element. */
async function dialogComputedStyle(page, properties) {
  const dialog = page.getByRole('dialog');
  await expect(dialog).toBeVisible({ timeout: 5000 });
  return dialog.evaluate((el, props) => {
    const cs = window.getComputedStyle(el);
    return Object.fromEntries(props.map((p) => [p, cs[p]]));
  }, properties);
}

// ---------------------------------------------------------------------------
// SC-DCO-01/02 — WidgetLibrary (Dashboard)
// ---------------------------------------------------------------------------

test('SC-DCO-01/02: WidgetLibrary DialogContent honours max-w-2xl/flex, DialogTitle honours font-bold', async ({ page }) => {
  await mockFallback(page);
  await mockDashboardPositions(page);
  await page.goto('/#/Dashboard');

  await page.getByRole('button', { name: /customize/i }).click();
  await page.getByRole('button', { name: /add widget/i }).click();

  await expect(page.getByRole('heading', { name: 'Widget Library' })).toBeVisible({ timeout: 10000 });

  const { maxWidth, display } = await dialogComputedStyle(page, ['maxWidth', 'display']);
  expect(maxWidth).toBe('672px'); // max-w-2xl = 42rem
  expect(display).toBe('flex');

  const title = page.getByRole('heading', { name: 'Widget Library' });
  const fontWeight = await title.evaluate((el) => window.getComputedStyle(el).fontWeight);
  expect(fontWeight).toBe('700'); // font-bold
});

// ---------------------------------------------------------------------------
// SC-DCO-03 — MonitorModal (Dashboard)
// ---------------------------------------------------------------------------

test('SC-DCO-03: MonitorModal DialogContent honours max-w-2xl/flex', async ({ page }) => {
  await mockFallback(page);
  await mockDashboardPositions(page);
  await page.goto('/#/Dashboard');

  // The "Daily Monitor" quick action is a plain onClick <div>, not a <button> —
  // click via its heading text instead of a button role.
  await page.getByRole('heading', { name: 'Daily Monitor' }).click();

  await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible({ timeout: 10000 });

  const { maxWidth, display } = await dialogComputedStyle(page, ['maxWidth', 'display']);
  expect(maxWidth).toBe('672px'); // max-w-2xl = 42rem
  expect(display).toBe('flex');
});

// ---------------------------------------------------------------------------
// SC-DCO-04 — ExportModal (Reports)
// ---------------------------------------------------------------------------

test('SC-DCO-04: ExportModal DialogTitle honours font-bold', async ({ page }) => {
  await mockFallback(page);
  await page.goto('/#/Reports');

  await page.getByRole('button', { name: 'Export' }).click();

  const title = page.getByRole('heading', { name: 'Export Report' });
  await expect(title).toBeVisible({ timeout: 10000 });

  const fontWeight = await title.evaluate((el) => window.getComputedStyle(el).fontWeight);
  expect(fontWeight).toBe('700'); // font-bold
});

// ---------------------------------------------------------------------------
// SC-DCO-05 — TradeReflectionModal (TradeReflection)
// ---------------------------------------------------------------------------

const TRADE_WITH_REFLECTION = {
  id: 'dco-t1',
  ticker: 'NVDA',
  market: 'US',
  entry_price: 500.0,
  exit_price: 545.0,
  exit_reason: 'target',
  exit_date: '2026-05-15',
  holding_days: 14,
  pnl: 562.5,
  net_r_multiple: 1.5,
};

async function mockTradeReflectionRoutes(page) {
  await page.route('**/trades**', (route) => {
    const url = route.request().url();
    if (url.includes('/reflection') || url.includes('/costs')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({}) });
    }
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ trades: [TRADE_WITH_REFLECTION] }),
    });
  });
}

test('SC-DCO-05: TradeReflectionModal DialogContent honours max-w-2xl/flex', async ({ page }) => {
  await mockFallback(page);
  await mockTradeReflectionRoutes(page);
  await page.goto('/#/TradeReflection');

  const card = page.locator('button').filter({ hasText: 'NVDA' }).first();
  await expect(card).toBeVisible({ timeout: 8000 });
  await card.click();

  const dialog = page.getByRole('dialog');
  await expect(dialog).toBeVisible({ timeout: 10000 });

  const { maxWidth, display } = await dialogComputedStyle(page, ['maxWidth', 'display']);
  expect(maxWidth).toBe('672px'); // max-w-2xl = 42rem
  expect(display).toBe('flex');
});

// ---------------------------------------------------------------------------
// SC-DCO-06 — TradePlan.js Abandon-plan modal
// ---------------------------------------------------------------------------

const PLAN_ID = '00000000-0000-0000-0000-0000000000dc';

const EXISTING_PLAN_DETAIL = {
  status: 'ok',
  data: {
    id: PLAN_ID,
    ticker: 'AAPL',
    market: 'US',
    status: 'draft',
    setup_thesis: 'Breakout above 50d MA on volume',
    entry_rationale: 'Confirmed with signal',
    regime_context_at_entry: 'risk_on',
    r_target: 2.0,
    early_exit_conditions: 'Close below 50d MA',
    confirmation_criteria: 'Volume > 1.5x avg',
    checklist_items: [
      { id: 'signal_confirmed', label: 'Strategy signal confirmed', checked: true },
      { id: 'stop_defined', label: 'Stop level defined', checked: false },
    ],
  },
};

test('SC-DCO-06: TradePlan Abandon-plan DialogContent honours rounded-2xl at >=640px', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { regime_status: 'risk_on' } }) })
  );
  await page.route(new RegExp(`${API}/trade-plans/${PLAN_ID}$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(EXISTING_PLAN_DETAIL) })
  );

  const qs = new URLSearchParams({ edit: PLAN_ID, ticker: 'AAPL', market: 'US' }).toString();
  await page.goto(`/#/TradePlan?${qs}`);
  await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });

  await page.getByRole('button', { name: /abandon plan/i }).click();

  const { borderRadius } = await dialogComputedStyle(page, ['borderRadius']);
  expect(borderRadius).toBe('16px'); // rounded-2xl = 1rem
});

// ---------------------------------------------------------------------------
// SC-DCO-07 — WatchlistModal DialogFooter
// ---------------------------------------------------------------------------

test('SC-DCO-07: WatchlistModal DialogFooter honours justify-between at >=640px', async ({ page }) => {
  await mockFallback(page);
  await page.route(`${API}/watchlist`, (route) => {
    if (route.request().method() === 'GET') {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
    return route.continue();
  });
  await page.goto('/#/Watchlist');
  await expect(page.getByText('Your watchlist is empty')).toBeVisible({ timeout: 10000 });

  await page.getByRole('button', { name: 'Add Ticker' }).first().click();
  await expect(page.getByRole('heading', { name: 'Add Ticker to Watchlist' })).toBeVisible({ timeout: 5000 });

  const footer = page.locator('[class*="justify-between"]').filter({ has: page.getByRole('button', { name: /add to watchlist/i }) });
  await expect(footer.first()).toBeVisible({ timeout: 5000 });
  const justifyContent = await footer.first().evaluate((el) => window.getComputedStyle(el).justifyContent);
  expect(justifyContent).toBe('space-between');
});
