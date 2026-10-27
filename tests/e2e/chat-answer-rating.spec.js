/**
 * AI Chat Answer Rating — Playwright E2E Tests
 * ST-22 (EPIC-03, v9.13) — BLG-FE-208
 * Design: docs/design/2026-10-16__release-v9.13/chat-answer-rating/decision_record.md
 * Spec: docs/specs/frontend/pages/positions.md §AI Trade Advisor Widget §Answer Rating
 *
 * Covers:
 *   SC-CAR-01: A model answer (with answer_id) can be rated Useful once: POST body, selected
 *              state, both buttons disabled, "Thanks — recorded." (AC 1)
 *   SC-CAR-02: The rating persists: after closing and re-opening the widget, rating the same
 *              answer again is refused (409) and the first rating is shown (AC 1)
 *   SC-CAR-03: No rating control on a fixed fallback message, an answer without answer_id,
 *              or a user bubble (decision record §2.1)
 *   SC-CAR-04: Save failed: both buttons re-enabled and unselected, inline error (decision §6)
 *   SC-CAR-05: Rated-state colours and an axe colour-contrast scan of the rating group,
 *              in dark and light themes (the panel is dark in both)
 *
 * Infrastructure: page.route() interception; no live backend. HashRouter: '/#/Positions'.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const ANSWER_ID = '3f2b7c1e-9a4d-4e21-8c55-0d6f1a2b3c4d';
const CHAT_RE = /\/ai\/chat$/;
const RATING_RE = /\/ai\/chat\/[^/]+\/rating$/;

async function stubPositionsRoutes(page) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance') || url.includes('/grace-period-alerts')) {
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

async function stubChat(page, { answerId = ANSWER_ID, status = 200 } = {}) {
  await page.route(CHAT_RE, (route) => {
    if (status !== 200) {
      return route.fulfill({ status, contentType: 'application/json', body: JSON.stringify({ detail: 'Internal error' }) });
    }
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        response: 'You have no open positions.',
        advisory: true,
        model: 'claude-sonnet-4-6',
        ...(answerId ? { answer_id: answerId } : {}),
      }),
    });
  });
}

// A stateful rating endpoint: the first rating is stored, later ones get 409.
async function stubRating(page, { failWith = null } = {}) {
  const calls = [];
  let stored = null;
  await page.route(RATING_RE, (route) => {
    const body = route.request().postDataJSON();
    calls.push({ url: route.request().url(), body });
    if (failWith) {
      return route.fulfill({ status: failWith, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'boom' }) });
    }
    if (stored) {
      return route.fulfill({
        status: 409,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'error', message: 'This answer has already been rated.', data: stored }),
      });
    }
    stored = { answer_id: ANSWER_ID, rating: body.rating, rated_at: '2026-10-27T09:30:00+00:00' };
    return route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: stored }) });
  });
  return calls;
}

async function ask(page) {
  await page.getByTestId('ai-chat-open-btn').click();
  await expect(page.getByTestId('ai-chat-panel')).toBeVisible({ timeout: 5000 });
  await page.getByTestId('ai-chat-input').fill('How many positions do I have?');
  await page.getByTestId('ai-chat-submit').click();
  await expect(page.getByTestId('ai-chat-answer')).toBeVisible({ timeout: 8000 });
}

test.describe('ST-22 — AI chat answer rating', () => {
  test('SC-CAR-01: a model answer can be rated Useful once', async ({ page }) => {
    await stubPositionsRoutes(page);
    await stubChat(page);
    const calls = await stubRating(page);
    await page.goto('/#/Positions');
    await ask(page);

    const group = page.getByTestId('chat-rating');
    await expect(group).toHaveAttribute('role', 'group');
    await expect(group).toHaveAttribute('aria-label', 'Rate this answer');
    const useful = page.getByTestId('chat-rating-useful');
    const notUseful = page.getByTestId('chat-rating-not-useful');
    await expect(useful).toHaveAttribute('aria-pressed', 'false');

    await useful.click();
    await expect(useful).toHaveAttribute('aria-pressed', 'true');
    await expect(notUseful).toHaveAttribute('aria-pressed', 'false');
    await expect(useful).toBeDisabled();
    await expect(notUseful).toBeDisabled();
    await expect(page.getByTestId('chat-rating-thanks')).toHaveText('Thanks — recorded.');
    expect(calls).toHaveLength(1);
    expect(calls[0].url).toContain(`/ai/chat/${ANSWER_ID}/rating`);
    expect(calls[0].body).toEqual({ rating: 'useful' });

    // The thanks note goes after 3 s; the selected state stays.
    await expect(page.getByTestId('chat-rating-thanks')).toHaveCount(0, { timeout: 5000 });
    await expect(useful).toHaveAttribute('aria-pressed', 'true');
  });

  test('SC-CAR-02: the rating persists — after re-opening, the first rating is shown, not replaced', async ({ page }) => {
    await stubPositionsRoutes(page);
    await stubChat(page);
    const calls = await stubRating(page);
    await page.goto('/#/Positions');
    await ask(page);
    await page.getByTestId('chat-rating-useful').click();
    await expect(page.getByTestId('chat-rating-useful')).toHaveAttribute('aria-pressed', 'true');

    // History clears on close; the rating is held server-side.
    await page.getByTestId('ai-chat-close').click();
    await ask(page);
    await expect(page.getByTestId('chat-rating-useful')).toHaveAttribute('aria-pressed', 'false');
    await page.getByTestId('chat-rating-not-useful').click();

    await expect(page.getByTestId('chat-rating-useful')).toHaveAttribute('aria-pressed', 'true');
    await expect(page.getByTestId('chat-rating-not-useful')).toHaveAttribute('aria-pressed', 'false');
    await expect(page.getByTestId('chat-rating-useful')).toBeDisabled();
    await expect(page.getByTestId('chat-rating-error')).toHaveCount(0);
    expect(calls.map((c) => c.body.rating)).toEqual(['useful', 'not_useful']);
  });

  test('SC-CAR-03a: no rating control on the fixed error message or the user bubble', async ({ page }) => {
    await stubPositionsRoutes(page);
    await stubChat(page, { status: 500 });
    await page.goto('/#/Positions');
    await page.getByTestId('ai-chat-open-btn').click();
    await page.getByTestId('ai-chat-input').fill('How many positions do I have?');
    await page.getByTestId('ai-chat-submit').click();
    await expect(page.getByText(/unable to get a response/i)).toBeVisible({ timeout: 8000 });
    await expect(page.getByTestId('chat-rating')).toHaveCount(0);
  });

  test('SC-CAR-03b: no rating control on an answer without answer_id', async ({ page }) => {
    await stubPositionsRoutes(page);
    await stubChat(page, { answerId: null });
    await page.goto('/#/Positions');
    await ask(page);
    await expect(page.getByTestId('chat-rating')).toHaveCount(0);
  });

  test('SC-CAR-04: a failed save re-enables both buttons and shows an error', async ({ page }) => {
    await stubPositionsRoutes(page);
    await stubChat(page);
    await stubRating(page, { failWith: 500 });
    await page.goto('/#/Positions');
    await ask(page);
    await page.getByTestId('chat-rating-not-useful').click();

    const error = page.getByTestId('chat-rating-error');
    await expect(error).toHaveText("Couldn't save your rating. Try again.", { timeout: 8000 });
    await expect(error).toHaveAttribute('role', 'status');
    for (const id of ['chat-rating-useful', 'chat-rating-not-useful']) {
      await expect(page.getByTestId(id)).toBeEnabled();
      await expect(page.getByTestId(id)).toHaveAttribute('aria-pressed', 'false');
    }
  });

  for (const theme of ['dark', 'light']) {
    test(`SC-CAR-05: rated colours and axe colour contrast of the rating group (${theme})`, async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await stubPositionsRoutes(page);
      await stubChat(page);
      await stubRating(page);
      await page.goto('/#/Positions');
      await ask(page);

      const unrated = await new AxeBuilder({ page }).include('[data-testid="chat-rating"]').withRules(['color-contrast']).analyze();
      expect(unrated.violations.filter((v) => v.id === 'color-contrast')).toEqual([]);

      await page.getByTestId('chat-rating-useful').click();
      await expect(page.getByTestId('chat-rating-useful')).toHaveCSS('color', 'rgb(52, 211, 153)'); // emerald-400
      const rated = await new AxeBuilder({ page }).include('[data-testid="chat-rating"]').withRules(['color-contrast']).analyze();
      // Disabled controls are exempt from WCAG contrast; axe skips them, so check the enabled state above.
      expect(rated.violations.filter((v) => v.id === 'color-contrast')).toEqual([]);
    });
  }
});
