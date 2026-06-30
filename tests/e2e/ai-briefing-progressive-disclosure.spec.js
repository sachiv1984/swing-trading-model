/**
 * AI Daily Briefing — Progressive Disclosure Playwright Tests
 * ST-12 (EPIC-03, v6.3) — BLG-FE-80
 *
 * Covers expand/collapse progressive disclosure for AiDailyBriefing.js:
 *
 *   SC-PD-01  All three sections (Market Context, Signals, Ask the AI) visible after briefing loads
 *   SC-PD-02  Each section has a visible toggle button
 *   SC-PD-03  Collapsing a section hides its content; expanding restores it (AC-01, AC-02)
 *   SC-PD-04  Default state is all sections expanded (AC-04)
 *   SC-PD-05  Collapse state persists across page reloads via localStorage (AC-03, AC-05)
 *             Playwright: expand all → collapse market context → reload → verify still collapsed
 *
 * HashRouter: all navigation via page.goto('/#/…')
 * localStorage: seeded directly via page.evaluate() to control persist state.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const STORAGE_KEY = 'ai-briefing-collapsed-sections-v1'; // gitleaks:allow

const BRIEFING_PAYLOAD = {
  summary: 'Markets are stable. SPY risk-on. NVDA near trailing stop — monitor closely.',
  actions: [
    { type: 'MONITOR', ticker: 'NVDA', description: 'Within 3% of trailing stop.' },
    { type: 'HOLD', ticker: 'AAPL', description: 'No action required today.' },
  ],
  generated_at: '2026-06-30T08:30:00Z',
  advisory: true,
  model: 'claude-sonnet-4-6',
};

// ---------------------------------------------------------------------------
// Shared route stubs
// ---------------------------------------------------------------------------

async function stubRoutes(page) {
  await page.route('**/ai/daily-briefing', route =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(BRIEFING_PAYLOAD),
    })
  );
  await page.route('**/portfolio/gate-metrics**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ closed_trades_count: 5, gate_threshold: 20, gate_met: false }) })
  );
  await page.route('**/positions/grace-period-alerts**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/positions**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route('**/portfolio**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/market/status**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ spy: { is_risk_on: true, price: 530 }, ftse: { is_risk_on: true, price: 8300 }, fx_rate: 1.25 }) })
  );
  await page.route('**/signals**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route('**/analytics/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route('**/alerts/history**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/screener/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ results: [] }) })
  );
  await page.route('**/compliance/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route('**/red-flag-journal**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/earnings/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null }) })
  );
}

async function loadDashboardWithBriefing(page) {
  await page.goto('/#/');
  await expect(page.getByTestId('ai-daily-briefing-card')).toBeVisible({ timeout: 8000 });
  // Trigger briefing generation
  await page.getByTestId('regenerate-briefing-btn').click();
  await expect(page.getByTestId('briefing-content')).toBeVisible({ timeout: 8000 });
}

// ---------------------------------------------------------------------------
// SC-PD-01 — Three sections visible after briefing loads (AC-01)
// ---------------------------------------------------------------------------

test.describe('SC-PD-01 — All three sections visible after briefing loads', () => {
  test('SC-PD-01: Market Context, Signals, Ask the AI section headers are visible', async ({ page }) => {
    await stubRoutes(page);
    await loadDashboardWithBriefing(page);

    await expect(page.getByTestId('section-toggle-market_context')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('section-toggle-signals')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('section-toggle-chat_prompt')).toBeVisible({ timeout: 5000 });

    await expect(page.getByText('Market Context', { exact: true })).toBeVisible({ timeout: 3000 });
    await expect(page.getByText('Signals', { exact: true })).toBeVisible({ timeout: 3000 });
    await expect(page.getByText('Ask the AI', { exact: true })).toBeVisible({ timeout: 3000 });
  });
});

// ---------------------------------------------------------------------------
// SC-PD-02 — Each section has a visible toggle button (AC-01)
// ---------------------------------------------------------------------------

test.describe('SC-PD-02 — Each section has a visible toggle button', () => {
  test('SC-PD-02: Toggle buttons are interactive elements', async ({ page }) => {
    await stubRoutes(page);
    await loadDashboardWithBriefing(page);

    const marketToggle = page.getByTestId('section-toggle-market_context');
    const signalsToggle = page.getByTestId('section-toggle-signals');
    const chatToggle = page.getByTestId('section-toggle-chat_prompt');

    await expect(marketToggle).toBeVisible({ timeout: 5000 });
    await expect(signalsToggle).toBeVisible({ timeout: 5000 });
    await expect(chatToggle).toBeVisible({ timeout: 5000 });

    // All toggles must be button elements
    await expect(marketToggle).toHaveAttribute('aria-expanded', 'true');
    await expect(signalsToggle).toHaveAttribute('aria-expanded', 'true');
    await expect(chatToggle).toHaveAttribute('aria-expanded', 'true');
  });
});

// ---------------------------------------------------------------------------
// SC-PD-03 — Collapsing hides content; expanding restores it (AC-01, AC-02)
// ---------------------------------------------------------------------------

test.describe('SC-PD-03 — Collapse hides content; expand restores it', () => {
  test('SC-PD-03a: Collapsing Market Context hides the summary text', async ({ page }) => {
    await stubRoutes(page);
    await loadDashboardWithBriefing(page);

    // Content visible before collapse
    await expect(page.getByTestId('section-content-market_context')).toBeVisible({ timeout: 5000 });
    await expect(page.getByText('Markets are stable.')).toBeVisible({ timeout: 3000 });

    // Collapse
    await page.getByTestId('section-toggle-market_context').click();
    await expect(page.getByTestId('section-toggle-market_context')).toHaveAttribute('aria-expanded', 'false');
    await expect(page.getByTestId('section-content-market_context')).not.toBeVisible();

    // Expand again — content returns
    await page.getByTestId('section-toggle-market_context').click();
    await expect(page.getByTestId('section-toggle-market_context')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.getByTestId('section-content-market_context')).toBeVisible({ timeout: 3000 });
    await expect(page.getByText('Markets are stable.')).toBeVisible({ timeout: 3000 });
  });

  test('SC-PD-03b: Collapsing Signals hides the action list', async ({ page }) => {
    await stubRoutes(page);
    await loadDashboardWithBriefing(page);

    await expect(page.getByTestId('briefing-actions')).toBeVisible({ timeout: 5000 });

    await page.getByTestId('section-toggle-signals').click();
    await expect(page.getByTestId('section-toggle-signals')).toHaveAttribute('aria-expanded', 'false');
    await expect(page.getByTestId('briefing-actions')).not.toBeVisible();
  });

  test('SC-PD-03c: Collapsing Ask the AI hides the chat input', async ({ page }) => {
    await stubRoutes(page);
    await loadDashboardWithBriefing(page);

    await expect(page.getByTestId('briefing-chat-input')).toBeVisible({ timeout: 5000 });

    await page.getByTestId('section-toggle-chat_prompt').click();
    await expect(page.getByTestId('section-toggle-chat_prompt')).toHaveAttribute('aria-expanded', 'false');
    await expect(page.getByTestId('briefing-chat-input')).not.toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// SC-PD-04 — Default state: all sections expanded (AC-04)
// ---------------------------------------------------------------------------

test.describe('SC-PD-04 — Default state is all sections expanded', () => {
  test('SC-PD-04: On first load with no localStorage entry, all sections are expanded', async ({ page }) => {
    await stubRoutes(page);

    // Clear any prior localStorage to simulate a new user
    await page.addInitScript(() => {
      localStorage.removeItem('ai-briefing-collapsed-sections-v1');
    });

    await loadDashboardWithBriefing(page);

    await expect(page.getByTestId('section-toggle-market_context')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.getByTestId('section-toggle-signals')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.getByTestId('section-toggle-chat_prompt')).toHaveAttribute('aria-expanded', 'true');

    await expect(page.getByTestId('section-content-market_context')).toBeVisible({ timeout: 3000 });
    await expect(page.getByTestId('section-content-signals')).toBeVisible({ timeout: 3000 });
    await expect(page.getByTestId('section-content-chat_prompt')).toBeVisible({ timeout: 3000 });
  });
});

// ---------------------------------------------------------------------------
// SC-PD-05 — Collapse state persists across page reloads (AC-03, AC-05)
// Playwright: expand all → collapse market context → reload → verify still collapsed
// ---------------------------------------------------------------------------

test.describe('SC-PD-05 — Collapse state persists via localStorage (AC-05)', () => {
  test('SC-PD-05: Expand all → collapse market context → reload → market context still collapsed', async ({ page }) => {
    await stubRoutes(page);

    // Clear localStorage once via evaluate (not addInitScript — addInitScript runs on every
    // navigation including page.reload(), which would erase the state we're trying to persist).
    await page.goto('/#/');
    await page.evaluate((key) => localStorage.removeItem(key), STORAGE_KEY);

    // Reload so React reads the now-clean localStorage → all sections default to expanded.
    await page.reload();
    await expect(page.getByTestId('ai-daily-briefing-card')).toBeVisible({ timeout: 8000 });
    await page.getByTestId('regenerate-briefing-btn').click();
    await expect(page.getByTestId('briefing-content')).toBeVisible({ timeout: 8000 });

    // Verify all expanded
    await expect(page.getByTestId('section-toggle-market_context')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.getByTestId('section-toggle-signals')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.getByTestId('section-toggle-chat_prompt')).toHaveAttribute('aria-expanded', 'true');

    // Collapse only market context
    await page.getByTestId('section-toggle-market_context').click();
    await expect(page.getByTestId('section-toggle-market_context')).toHaveAttribute('aria-expanded', 'false');
    await expect(page.getByTestId('section-content-market_context')).not.toBeVisible();

    // Confirm localStorage was written
    const stored = await page.evaluate((key) => localStorage.getItem(key), STORAGE_KEY);
    const parsed = JSON.parse(stored);
    expect(parsed.market_context).toBe(true);

    // Reload — routes persist (page.route() survives reload); localStorage is NOT cleared
    // because we are no longer using addInitScript.
    await page.reload();
    await expect(page.getByTestId('ai-daily-briefing-card')).toBeVisible({ timeout: 8000 });
    await page.getByTestId('regenerate-briefing-btn').click();
    await expect(page.getByTestId('briefing-content')).toBeVisible({ timeout: 8000 });

    // Market context must still be collapsed after reload
    await expect(page.getByTestId('section-toggle-market_context')).toHaveAttribute('aria-expanded', 'false');
    await expect(page.getByTestId('section-content-market_context')).not.toBeVisible();

    // Other sections must remain expanded
    await expect(page.getByTestId('section-toggle-signals')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.getByTestId('section-content-signals')).toBeVisible({ timeout: 3000 });
    await expect(page.getByTestId('section-toggle-chat_prompt')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.getByTestId('section-content-chat_prompt')).toBeVisible({ timeout: 3000 });
  });
});
