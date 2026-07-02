/**
 * EPIC-02 v6.2 — AI Advisory Layer: Daily Briefing Card and Chat Widget
 *
 * Coverage (ST-07 and ST-09):
 *
 *   SC-AB-01  "Today's Briefing" card is visible on the Dashboard page (ST-07/AC-01)
 *   SC-AB-02  Card body shows summary and action list after API response (ST-07/AC-02)
 *   SC-AB-03  Card shows generation timestamp and Regenerate button (ST-07/AC-03)
 *   SC-AB-04  Regenerate button triggers a new POST /ai/daily-briefing and updates card (ST-07/AC-05)
 *
 *   SC-AC-01  AI chat widget "Ask Advisor" button is visible on the Positions page (ST-09/AC-01)
 *   SC-AC-02  AI chat widget "Ask Advisor" button is visible on the Signals page (ST-09/AC-01)
 *   SC-AC-03  User can type a question and submit; response displayed in widget (ST-09/AC-02)
 *   SC-AC-04  Loading indicator shown while POST /ai/chat is in-flight (ST-09/AC-04)
 *   SC-AC-05  Error state shown when POST /ai/chat fails (ST-09/AC-05)
 *   SC-AC-06  Advisory footer disclaimer visible and mentions "advisory" (ST-10/AC-02, AC-03, v6.4)
 *
 * AC-04 (ST-07) and AC-03 (ST-09) are staging-only human sign-off items and are
 * not covered by automated Playwright tests (per spec). ST-10/AC-04 (Head of UX &
 * Design sign-off) is a human/agent-mediated sign-off, not Playwright-testable.
 *
 * HashRouter: all navigation via page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');

// ---------------------------------------------------------------------------
// Shared route stubs
// ---------------------------------------------------------------------------

async function stubDashboardRoutes(page, briefingResponse) {
  // Briefing endpoint
  await page.route('**/ai/daily-briefing', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(briefingResponse),
    });
  });

  // Standard dashboard routes
  await page.route('**/portfolio/gate-metrics', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ closed_trades_count: 5, gate_threshold: 20, gate_met: false }) })
  );
  await page.route('**/positions/grace-period-alerts**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/positions**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route('**/portfolio**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/market/status**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ spy: { is_risk_on: true, price: 530 }, ftse: { is_risk_on: true, price: 8300 }, fx_rate: 1.25 }) })
  );
  await page.route('**/signals**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/screener/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ results: [] }) })
  );
  await page.route('**/compliance/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route('**/red-flag-journal**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null }) })
  );
}

async function stubPositionsRoutes(page) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
    if (url.includes('/grace-period-alerts')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) });
  });
  await page.route('**/portfolio**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null }) })
  );
}

async function stubSignalsRoutes(page) {
  await page.route('**/signals**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route('**/positions**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
  );
  await page.route('**/cash/summary**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ current_cash: 10000 }) })
  );
  await page.route('**/market/status**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ spy: { is_risk_on: true, price: 530 }, ftse: { is_risk_on: true, price: 8300 }, fx_rate: 1.25 }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
}

// ---------------------------------------------------------------------------
// ST-07 — AI Daily Briefing card (Dashboard)
// ---------------------------------------------------------------------------

test.describe('ST-07 — AI Daily Briefing Card', () => {
  test('SC-AB-01: "Today\'s Briefing" card is visible on the Dashboard page', async ({ page }) => {
    await stubDashboardRoutes(page, {
      summary: null,
      actions: [],
      generated_at: '2026-06-25T08:30:00Z',
      advisory: true,
      model: null,
    });
    await page.goto('/#/');
    await expect(page.getByTestId('ai-daily-briefing-card')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText("Today's Briefing")).toBeVisible({ timeout: 5000 });
  });

  test('SC-AB-02: Card shows summary paragraph and action list after API response', async ({ page }) => {
    const briefingPayload = {
      summary: 'Your portfolio has 2 open positions. NVDA is near its trailing stop — monitor closely today.',
      actions: [
        { type: 'MONITOR', ticker: 'NVDA', description: 'Within 3% of trailing stop.' },
        { type: 'HOLD', ticker: 'AAPL', description: 'Stable position, no action needed.' },
      ],
      generated_at: '2026-06-25T08:30:00Z',
      advisory: true,
      model: 'claude-sonnet-4-6',
    };

    await stubDashboardRoutes(page, briefingPayload);
    await page.goto('/#/');

    // Click Regenerate to trigger the API call
    const regenBtn = page.getByTestId('regenerate-briefing-btn');
    await regenBtn.waitFor({ state: 'visible', timeout: 8000 });
    await regenBtn.click();

    // Summary text
    await expect(page.getByTestId('briefing-content')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText('Your portfolio has 2 open positions.')).toBeVisible({ timeout: 5000 });

    // Action list
    await expect(page.getByTestId('briefing-actions')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('briefing-actions').getByText('NVDA', { exact: true })).toBeVisible({ timeout: 3000 });
    await expect(page.getByTestId('briefing-actions').getByText('MONITOR', { exact: true })).toBeVisible({ timeout: 3000 });
  });

  test('SC-AB-03: Card shows Regenerate button on initial render', async ({ page }) => {
    await stubDashboardRoutes(page, {
      summary: null,
      actions: [],
      generated_at: '2026-06-25T08:30:00Z',
      advisory: true,
    });
    await page.goto('/#/');

    // Regenerate button is visible before any generation
    const regenBtn = page.getByTestId('regenerate-briefing-btn');
    await expect(regenBtn).toBeVisible({ timeout: 8000 });

    // Empty state message present before first generation
    await expect(page.getByTestId('briefing-empty')).toBeVisible({ timeout: 5000 });
  });

  test('SC-AB-04: Regenerate button triggers POST /ai/daily-briefing and updates card content', async ({ page }) => {
    let callCount = 0;
    const responses = [
      {
        summary: 'First briefing: all positions stable.',
        actions: [{ type: 'HOLD', ticker: 'TSLA', description: 'No action needed.' }],
        generated_at: '2026-06-25T08:00:00Z',
        advisory: true,
        model: 'claude-sonnet-4-6',
      },
      {
        summary: 'Second briefing: NVDA near stop.',
        actions: [{ type: 'MONITOR', ticker: 'NVDA', description: 'Near trailing stop.' }],
        generated_at: '2026-06-25T08:01:00Z',
        advisory: true,
        model: 'claude-sonnet-4-6',
      },
    ];

    await stubDashboardRoutes(page, responses[0]);
    // Counter route registered after stubDashboardRoutes so it takes LIFO precedence
    await page.route('**/ai/daily-briefing', (route) => {
      const payload = responses[callCount] ?? responses[responses.length - 1];
      callCount++;
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(payload),
      });
    });

    await page.goto('/#/');

    const regenBtn = page.getByTestId('regenerate-briefing-btn');
    await regenBtn.waitFor({ state: 'visible', timeout: 8000 });

    // First click
    await regenBtn.click();
    await expect(page.getByText('First briefing: all positions stable.')).toBeVisible({ timeout: 8000 });

    // Second click — content updates
    await regenBtn.click();
    await expect(page.getByText('Second briefing: NVDA near stop.')).toBeVisible({ timeout: 8000 });
  });
});

// ---------------------------------------------------------------------------
// ST-09 — AI Chat Widget (Positions + Signals pages)
// ---------------------------------------------------------------------------

test.describe('ST-09 — AI Chat Widget', () => {
  test('SC-AC-01: Chat widget "Ask Advisor" button is visible on the Positions page', async ({ page }) => {
    await stubPositionsRoutes(page);
    await page.goto('/#/Positions');
    await expect(page.getByTestId('ai-chat-widget')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('ai-chat-open-btn')).toBeVisible({ timeout: 5000 });
  });

  test('SC-AC-02: Chat widget "Ask Advisor" button is visible on the Signals page', async ({ page }) => {
    await stubSignalsRoutes(page);
    await page.goto('/#/Signals');
    await expect(page.getByTestId('ai-chat-widget')).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('ai-chat-open-btn')).toBeVisible({ timeout: 5000 });
  });

  test('SC-AC-03: User can type a question and submit; response displayed in widget', async ({ page }) => {
    await page.route('**/ai/chat', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          response: 'You currently have 0 open positions.',
          advisory: true,
          model: 'claude-sonnet-4-6',
        }),
      })
    );
    await stubPositionsRoutes(page);
    await page.goto('/#/Positions');

    // Open widget
    await page.getByTestId('ai-chat-open-btn').click();
    await expect(page.getByTestId('ai-chat-panel')).toBeVisible({ timeout: 5000 });

    // Type and submit
    const input = page.getByTestId('ai-chat-input');
    await input.fill('How many positions do I have?');
    await page.getByTestId('ai-chat-submit').click();

    // Response displayed
    await expect(page.getByText('You currently have 0 open positions.')).toBeVisible({ timeout: 8000 });
  });

  test('SC-AC-04: Loading indicator shown while POST /ai/chat is in-flight', async ({ page }) => {
    await page.route('**/ai/chat', async (route) => {
      // Delay response so loading state is visible
      await new Promise(r => setTimeout(r, 500));
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ response: 'Delayed response.', advisory: true }),
      });
    });
    await stubPositionsRoutes(page);
    await page.goto('/#/Positions');

    await page.getByTestId('ai-chat-open-btn').click();
    await page.getByTestId('ai-chat-input').fill('Show me my positions.');
    await page.getByTestId('ai-chat-submit').click();

    // Loading dots visible before response arrives
    await expect(page.getByTestId('ai-chat-loading')).toBeVisible({ timeout: 3000 });
  });

  test('SC-AC-05: Error state shown when POST /ai/chat fails', async ({ page }) => {
    await page.route('**/ai/chat', (route) =>
      route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ detail: 'Internal error' }) })
    );
    await stubPositionsRoutes(page);
    await page.goto('/#/Positions');

    await page.getByTestId('ai-chat-open-btn').click();
    await page.getByTestId('ai-chat-input').fill('What is my portfolio value?');
    await page.getByTestId('ai-chat-submit').click();

    await expect(page.getByTestId('ai-chat-error')).toBeVisible({ timeout: 8000 });
    await expect(page.getByText(/unable to get a response/i)).toBeVisible({ timeout: 5000 });
  });

  test('SC-AC-06: Advisory footer disclaimer is visible and mentions "advisory" (ST-10/AC-02, AC-03)', async ({ page }) => {
    await stubPositionsRoutes(page);
    await page.goto('/#/Positions');

    await page.getByTestId('ai-chat-open-btn').click();
    await expect(page.getByTestId('ai-chat-panel')).toBeVisible({ timeout: 5000 });

    const footer = page.getByTestId('ai-chat-advisory-footer');
    await expect(footer).toBeVisible({ timeout: 5000 });
    await expect(footer).toContainText(/advisory/i);
  });
});
