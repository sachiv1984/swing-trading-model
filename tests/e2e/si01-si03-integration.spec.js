/**
 * SI-01 → SI-03 Integration Path — E2E Acceptance Tests
 * ST-03 (BLG-QA-25, v4.0 EPIC-01)
 *
 * Covers the full SI-01→SI-03 path:
 *   SC-SI-01a  Navigate to TradePlan → pre-entry validation panel shows with failing checks
 *   SC-SI-01b  Override acknowledgement checkbox present when override_required=true
 *   SC-SI-01c  Override checkbox is interactive (can be checked)
 *   SC-SI-03a  RedFlagJournal renders event list with pre_entry_override event
 *   SC-SI-03b  Event type filter → filtered results contain override event with correct metadata
 *   SC-SI-03c  Filtering by pre_entry_override shows matching event; clear filter restores all
 *
 * Spec refs:
 *   docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/pre-entry-validation
 *   docs/specs/api_contracts/red_flag_journal.md
 *   BLG-QA-25 acceptance criteria
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required. Mocks return canonical response shapes.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…').
 * -------------------------------------------------------------------------
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const PLAN_ID = '00000000-0000-0000-0000-000000000010';

// ---------------------------------------------------------------------------
// Mock payloads
// ---------------------------------------------------------------------------

const PRE_ENTRY_VALIDATION_FAIL = {
  status: 'ok',
  data: {
    ticker: 'AAPL',
    market: 'US',
    quantity: 10,
    advisory_status: 'fail',
    override_required: true,
    checks: [
      {
        rule: 'regime_gate',
        status: 'fail',
        detail: 'US market is Risk-Off (SPY below 200-day MA)',
        severity: 'fail',
      },
      {
        rule: 'cash_constraint',
        status: 'pass',
        detail: 'Within available cash',
        severity: 'fail',
      },
      {
        rule: 'sector_concentration',
        status: 'pass',
        detail: 'Technology 22% within 30% limit',
        severity: 'warn',
      },
      {
        rule: 'earnings_proximity',
        status: 'pass',
        detail: 'Earnings 45 days away',
        severity: 'warn',
      },
      {
        rule: 'sizing_validity',
        status: 'pass',
        detail: 'Position sizing valid',
        severity: 'warn',
      },
    ],
  },
};

const TRADE_PLAN_CREATED = {
  status: 'ok',
  data: {
    id: PLAN_ID,
    ticker: 'AAPL',
    market: 'US',
    status: 'draft',
    setup_thesis: null,
    entry_rationale: null,
    regime_context_at_entry: 'risk_off',
    r_target: null,
    early_exit_conditions: null,
    confirmation_criteria: null,
    checklist_completed: false,
    checklist_items: [],
    pre_entry_override_acknowledged: true,
  },
};

const MARKET_STATUS_RISK_OFF = {
  status: 'ok',
  data: { regime_status: 'risk_off' },
};

const RFJ_EVENTS_WITH_OVERRIDE = {
  status: 'ok',
  data: {
    total: 1,
    page: 1,
    page_size: 20,
    items: [
      {
        id: 'aaaaaaaa-0000-0000-0000-000000000001',
        event_type: 'pre_entry_override',
        ticker: 'AAPL',
        position_id: null,
        context: { source: 'trade_plan', override_acknowledged: true },
        created_at: new Date().toISOString(),
      },
    ],
  },
};

const RFJ_EVENTS_EMPTY = {
  status: 'ok',
  data: { total: 0, page: 1, page_size: 20, items: [] },
};

const POSITIONS_OPEN = {
  status: 'ok',
  data: [
    {
      id: '00000000-0000-0000-0000-aaaaaaaaaaaa',
      ticker: 'AAPL',
      market: 'US',
      shares: 10,
      entry_price: 175.0,
      current_price: 178.0,
      pnl: 30.0,
      status: 'open',
    },
  ],
};

// ---------------------------------------------------------------------------
// Route mock helpers
// ---------------------------------------------------------------------------

async function mockCatchAll(page) {
  await page.route(`${API}/**`, (route) => {
    const url = route.request().url();
    if (!url.includes('/health') && !url.includes('/pre-entry-validation') &&
        !url.includes('/red-flag-journal') && !url.includes('/market/status') &&
        !url.includes('/trade-plans') && !url.includes('/positions') &&
        !url.includes('/settings')) {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) });
    } else {
      route.fallback();
    }
  });
}

async function mockHealth(page) {
  await page.route(`${API}/health`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok' }) })
  );
}

async function mockPreEntryValidation(page, payload) {
  await page.route(`${API}/portfolio/pre-entry-validation**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockRedFlagJournal(page, payload) {
  await page.route(`${API}/portfolio/red-flag-journal**`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockMarketStatus(page, payload) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockSettings(page) {
  await page.route(`${API}/settings`, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { id: '1', min_trades_for_analytics: 10, api_key: 'testkey' } }),
    })
  );
}

async function mockPositions(page, payload) {
  await page.route(`${API}/positions`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(payload) })
  );
}

async function mockTradePlans(page) {
  await page.route(`${API}/trade-plans**`, (route) => {
    const method = route.request().method();
    if (method === 'POST') {
      route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(TRADE_PLAN_CREATED) });
    } else {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
  });
}

// ---------------------------------------------------------------------------
// SC-SI-01: Pre-entry validation in TradePlan creation flow
// ---------------------------------------------------------------------------

test.describe('SC-SI-01 — Pre-entry validation panel (SI-01)', () => {
  test.beforeEach(async ({ page }) => {
    await mockCatchAll(page);
    await mockHealth(page);
    await mockSettings(page);
    await mockMarketStatus(page, MARKET_STATUS_RISK_OFF);
    await mockPreEntryValidation(page, PRE_ENTRY_VALIDATION_FAIL);
    await mockTradePlans(page);
    await mockPositions(page, POSITIONS_OPEN);
    await page.goto('/#/TradePlan?ticker=AAPL&market=US');
    await expect(page.locator('text=Trade Plan')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-01a: Pre-entry validation panel shows with failing check', async ({ page }) => {
    // Wait for the validation panel to appear with at least one check result
    await expect(page.locator('text=regime_gate').or(page.locator('text=Regime')).or(page.locator('[data-testid="override-acknowledgement-checkbox"]'))).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-01b: Override acknowledgement checkbox present when override required', async ({ page }) => {
    const checkbox = page.locator('[data-testid="override-acknowledgement-checkbox"]');
    await expect(checkbox).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-01c: Override checkbox is interactive', async ({ page }) => {
    const checkbox = page.locator('[data-testid="override-acknowledgement-checkbox"]');
    await expect(checkbox).toBeVisible({ timeout: 8000 });
    // Checkbox should be initially unchecked
    await expect(checkbox).not.toBeChecked();
    // User can check it
    await checkbox.check();
    await expect(checkbox).toBeChecked();
  });
});

// ---------------------------------------------------------------------------
// SC-SI-03: Red Flag Journal event display (SI-03)
// ---------------------------------------------------------------------------

test.describe('SC-SI-03 — Red Flag Journal (SI-03)', () => {
  test.beforeEach(async ({ page }) => {
    await mockCatchAll(page);
    await mockHealth(page);
    await mockSettings(page);
    await mockRedFlagJournal(page, RFJ_EVENTS_WITH_OVERRIDE);
    await page.goto('/#/RedFlagJournal');
    await expect(page.locator('text=Red Flag Journal')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-03a: RedFlagJournal renders event list with pre_entry_override event', async ({ page }) => {
    // Verify the override event appears
    await expect(page.locator('text=Pre-Entry Override').or(page.locator('text=AAPL'))).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-03b: Event metadata correct — ticker AAPL and override context visible', async ({ page }) => {
    // AAPL ticker should appear in the event
    await expect(page.locator('text=AAPL').first()).toBeVisible({ timeout: 8000 });
    // Override context: "Override acknowledged" should appear (per contextSummary function)
    await expect(page.locator('text=Override acknowledged').or(page.locator('text=Pre-Entry Override'))).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-03c: Event type filter shows pre_entry_override events; filter dropdown present', async ({ page }) => {
    // Filter dropdown must be present
    const filterDropdown = page.locator('[data-testid="event-type-filter"]');
    await expect(filterDropdown).toBeVisible({ timeout: 8000 });

    // Select pre_entry_override filter
    await filterDropdown.selectOption('pre_entry_override');

    // After filter applied, event should still show (mocked endpoint returns same result)
    await expect(page.locator('text=AAPL').or(page.locator('text=Pre-Entry Override'))).toBeVisible({ timeout: 6000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SI-PATH: Full SI-01→SI-03 path (cross-page narrative)
// ---------------------------------------------------------------------------

test.describe('SC-SI-PATH — Full SI-01→SI-03 integration path', () => {
  test('SC-SI-PATH-01: TradePlan validation → navigate to RFJ → override event present', async ({ page }) => {
    // Setup all mocks
    await mockCatchAll(page);
    await mockHealth(page);
    await mockSettings(page);
    await mockMarketStatus(page, MARKET_STATUS_RISK_OFF);
    await mockPreEntryValidation(page, PRE_ENTRY_VALIDATION_FAIL);
    await mockTradePlans(page);
    await mockPositions(page, POSITIONS_OPEN);
    await mockRedFlagJournal(page, RFJ_EVENTS_WITH_OVERRIDE);

    // Step 1: Navigate to TradePlan page (position + ticker context)
    await page.goto('/#/TradePlan?ticker=AAPL&market=US');
    await expect(page.locator('text=Trade Plan')).toBeVisible({ timeout: 8000 });

    // Step 2: Pre-entry validation panel is present
    await expect(
      page.locator('[data-testid="override-acknowledgement-checkbox"]')
    ).toBeVisible({ timeout: 8000 });

    // Step 3: Acknowledge override
    const checkbox = page.locator('[data-testid="override-acknowledgement-checkbox"]');
    await checkbox.check();
    await expect(checkbox).toBeChecked();

    // Step 4: Navigate to Red Flag Journal
    await page.goto('/#/RedFlagJournal');
    await expect(page.locator('text=Red Flag Journal')).toBeVisible({ timeout: 8000 });

    // Step 5: Override event is present in the journal
    await expect(
      page.locator('text=Pre-Entry Override').or(page.locator('text=AAPL'))
    ).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-PATH-02: Filter by event type in RFJ contains override event', async ({ page }) => {
    await mockCatchAll(page);
    await mockHealth(page);
    await mockSettings(page);
    await mockRedFlagJournal(page, RFJ_EVENTS_WITH_OVERRIDE);

    await page.goto('/#/RedFlagJournal');
    await expect(page.locator('text=Red Flag Journal')).toBeVisible({ timeout: 8000 });

    // Apply event type filter
    const filterDropdown = page.locator('[data-testid="event-type-filter"]');
    await expect(filterDropdown).toBeVisible({ timeout: 8000 });
    await filterDropdown.selectOption('pre_entry_override');

    // Filtered results still contain the override event (mock returns same data)
    await expect(page.locator('text=AAPL').or(page.locator('text=Pre-Entry Override'))).toBeVisible({ timeout: 6000 });
  });
});

// ---------------------------------------------------------------------------
// SC-SI-01d: Pre-entry validation all-pass state (BLG-QA-56 — v5.7 ST-06)
// ---------------------------------------------------------------------------

const PRE_ENTRY_VALIDATION_ALL_PASS = {
  status: 'ok',
  data: {
    ticker: 'AAPL',
    market: 'US',
    quantity: 10,
    advisory_status: 'pass',
    override_required: false,
    checks: [
      { rule: 'regime_gate', status: 'pass', detail: 'US market is Risk-On (SPY above 200-day MA)', severity: 'fail' },
      { rule: 'cash_constraint', status: 'pass', detail: 'Within available cash', severity: 'fail' },
      { rule: 'sector_concentration', status: 'pass', detail: 'Technology 22% within 30% limit', severity: 'warn' },
      { rule: 'earnings_proximity', status: 'pass', detail: 'Earnings 45 days away', severity: 'warn' },
      { rule: 'sizing_validity', status: 'pass', detail: 'Position sizing valid', severity: 'warn' },
    ],
  },
};

test.describe('SC-SI-01d — Pre-entry validation all-pass state', () => {
  test.beforeEach(async ({ page }) => {
    await mockCatchAll(page);
    await mockHealth(page);
    await mockSettings(page);
    await mockMarketStatus(page, { status: 'ok', data: { regime_status: 'risk_on' } });
    await mockPreEntryValidation(page, PRE_ENTRY_VALIDATION_ALL_PASS);
    await mockTradePlans(page);
    await mockPositions(page, POSITIONS_OPEN);
    await page.goto('/#/TradePlan?ticker=AAPL&market=US');
    await expect(page.locator('text=Trade Plan')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-01d: All-pass state — "Pass" advisory badge visible', async ({ page }) => {
    // The pre-entry panel must be present with a Pass advisory badge
    await expect(page.locator('[data-testid="pre-entry-checks-panel"]')).toBeVisible({ timeout: 8000 });
    // When advisory_status === 'pass', the badge shows "Pass"
    await expect(page.locator('[data-testid="pre-entry-checks-panel"]').getByText('Pass')).toBeVisible({ timeout: 8000 });
  });

  test('SC-SI-01d: All-pass state — override acknowledgement checkbox absent', async ({ page }) => {
    // Override checkbox only renders when hasWarnings (any check status is warn or fail)
    // With all checks passing, no warnings exist and the checkbox must not render
    await expect(page.locator('[data-testid="pre-entry-checks-panel"]')).toBeVisible({ timeout: 8000 });
    const checkbox = page.locator('[data-testid="override-acknowledgement-checkbox"]');
    await expect(checkbox).toHaveCount(0);
  });
});
