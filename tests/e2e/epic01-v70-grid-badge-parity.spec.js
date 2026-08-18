/**
 * EPIC-01 v7.0 — Positions Grid View Badge Parity
 *
 * Closes the Grid View Playwright coverage gap identified in
 * qa_evidence_EPIC-02.md (v6.9): SC-RO-* (epic01-v62-stops-alerts.spec.js) and
 * SC-GR-* (gap-risk-flag.spec.js) verify the RISK OFF / GAP RISK badges and the
 * trailing-stop breach indicator via Table View only. This file provides the
 * Grid View equivalent — parity confirmation for ST-02/ST-03 (BLG-FE-102/BLG-FE-97).
 *
 * Coverage (ST-04, BLG-QA-95):
 *
 *   SC-GVP-01  RISK OFF badge shown in Grid View when risk_off_exit=true (ST-02/AC-01)
 *   SC-GVP-02  RISK OFF badge uses spec colour #1E40AF / "RISK OFF" label (ST-02/AC-02)
 *   SC-GVP-03  No RISK OFF badge when risk_off_exit=false (ST-02/AC-01)
 *   SC-GVP-04  GAP RISK badge shown in Grid View, amber-600 background (parity w/ SC-GR-08)
 *   SC-GVP-05  Both badges coexist, stacked in the dedicated alert row (ST-02/AC-03, ST-05)
 *   SC-GVP-06  Initial Stop and trailing stop values both shown on the card (ST-03/AC-01)
 *   SC-GVP-07  Breach icon shown when current_price <= current_trailing_stop (ST-03/AC-02)
 *   SC-GVP-08  No breach icon when current_price > current_trailing_stop (ST-03/AC-02)
 *   SC-GVP-09  Table View behaviour unchanged — breach still renders as a pill, not an icon (ST-03/AC-03)
 *
 * Spec refs:
 *   docs/specs/frontend/pages/positions.md §Alerts Column (Grid View badge placement, v2.3)
 *   docs/specs/frontend/pages/positions.md §Trailing Stop Column
 *   docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md
 *
 * ROUTING NOTE: App uses HashRouter — all navigation via page.goto('/#/…').
 * Grid View is the default viewMode — no view-switch click required.
 */

'use strict';

const { test, expect } = require('@playwright/test');

function makePosition(overrides = {}) {
  const merged = {
    id: 'pos-gvp-01',
    ticker: 'AAPL',
    market: 'US',
    entry_price: 150.00,
    current_price: 120.00,
    current_price_native: 150.00,
    stop_price: 130.00,
    stop_price_native: 162.50,
    shares: 10,
    pnl: -300.00,
    pnl_percent: -20.00,
    holding_days: 15,
    grace_days_remaining: null,
    status: 'open',
    entry_date: '2026-05-01',
    initial_stop: 130.00,
    current_trailing_stop: 0,
    risk_off_exit: false,
    tags: null,
    ...overrides,
  };
  // ST-02 (BLG-BE-103, v8.9): these fixtures predate current_trailing_stop_native
  // and don't model currency conversion — mirror current_trailing_stop unless a
  // test explicitly overrides it, so existing scenarios asserting on a single
  // trailing-stop number keep exercising the same value under the corrected
  // native-display field (PositionCard.js/Positions.js now render
  // current_trailing_stop_native, not the GBP-basis current_trailing_stop).
  if (merged.current_trailing_stop_native === undefined) {
    merged.current_trailing_stop_native = merged.current_trailing_stop;
  }
  return merged;
}

const NO_FLAG = { flagged: false, reasons: [], avg_gap_pct: null, event_count: 0, insufficient_history: false };
const EARNINGS_FLAG = { flagged: true, reasons: ['earnings'], avg_gap_pct: 2.3, event_count: 14, insufficient_history: false };

async function stubGridView(page, positions, gapRiskPayload = NO_FLAG) {
  await page.route('**/positions*', (route) => {
    const url = route.request().url();
    if (url.includes('/compliance-recheck') || url.includes('/positions/compliance') || url.includes('/gap-risk')) {
      return route.continue();
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(positions) });
  });
  await page.route('**/portfolio*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { cash: 10000, initial_cash: 50000 } }) })
  );
  await page.route('**/analytics/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { last_sync_at: null } }) })
  );
  await page.route('**/positions/compliance*', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route('**/earnings/**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ next_earnings_date: null, days_until_earnings: null }) })
  );
  await page.route('**/positions/*/gap-risk', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: gapRiskPayload }) })
  );
  await page.route('**/alerts/history**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route('**/watchlist**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ items: [] }) })
  );
  await page.goto('/#/Positions');
  await page.waitForSelector(`text=${positions[0]?.ticker || 'AAPL'}`, { timeout: 8000 });
}

// ---------------------------------------------------------------------------
// ST-02 — RISK OFF badge (Grid View)
// ---------------------------------------------------------------------------

test('SC-GVP-01: RISK OFF badge shown in Grid View when risk_off_exit=true', async ({ page }) => {
  const pos = makePosition({ risk_off_exit: true });
  await stubGridView(page, [pos]);

  const badge = page.locator('[data-testid="risk-off-badge"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toContainText('RISK OFF');
});

test('SC-GVP-02: RISK OFF badge uses spec colour #1E40AF', async ({ page }) => {
  const pos = makePosition({ risk_off_exit: true });
  await stubGridView(page, [pos]);

  const badge = page.locator('[data-testid="risk-off-badge"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toHaveCSS('background-color', 'rgb(30, 64, 175)'); // #1E40AF
});

test('SC-GVP-03: No RISK OFF badge when risk_off_exit=false', async ({ page }) => {
  const pos = makePosition({ risk_off_exit: false });
  await stubGridView(page, [pos]);

  await expect(page.locator('[data-testid="risk-off-badge"]')).not.toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// ST-02 (v6.9 parity) — GAP RISK badge (Grid View)
// ---------------------------------------------------------------------------

test('SC-GVP-04: GAP RISK badge shown in Grid View with amber-600 background', async ({ page }) => {
  const pos = makePosition();
  await stubGridView(page, [pos], EARNINGS_FLAG);

  const badge = page.locator('[data-testid="gap-risk-badge"]').first();
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toContainText('GAP RISK');
  await expect(badge).toHaveCSS('background-color', 'rgb(217, 119, 6)'); // #D97706
});

// ---------------------------------------------------------------------------
// ST-05 — Combined badge stacking (Grid View)
// ---------------------------------------------------------------------------

test('SC-GVP-05: RISK OFF and GAP RISK badges coexist, stacked in the alert row', async ({ page }) => {
  const pos = makePosition({ risk_off_exit: true });
  await stubGridView(page, [pos], EARNINGS_FLAG);

  const alertRow = page.locator('[data-testid="grid-alerts-row"]');
  await expect(alertRow).toBeVisible({ timeout: 5000 });

  const riskOffBadge = page.locator('[data-testid="risk-off-badge"]');
  const gapBadge = page.locator('[data-testid="gap-risk-badge"]').first();
  await expect(riskOffBadge).toBeVisible({ timeout: 5000 });
  await expect(gapBadge).toBeVisible({ timeout: 5000 });

  // Stack order: RISK OFF above GAP RISK (positions.md §Alerts Column "Stacked-state spacing")
  const riskOffBox = await riskOffBadge.boundingBox();
  const gapBox = await gapBadge.boundingBox();
  expect(riskOffBox.y).toBeLessThan(gapBox.y);
});

// ---------------------------------------------------------------------------
// ST-03 — Trailing stop value + breach icon (Grid View)
// ---------------------------------------------------------------------------

test('SC-GVP-06: Initial Stop and trailing stop values both shown on the card', async ({ page }) => {
  const pos = makePosition({ initial_stop: 130.00, current_trailing_stop: 115.00, current_price: 118.00 });
  await stubGridView(page, [pos]);

  await expect(page.locator('text=/Init:.*130/').first()).toBeVisible({ timeout: 5000 });
  await expect(page.locator('text=/\\$115\\.00/').first()).toBeVisible({ timeout: 5000 });
});

test('SC-GVP-07: Breach icon shown when current_price <= current_trailing_stop', async ({ page }) => {
  // GBP price 110 <= trailing stop 120 -> breach
  const pos = makePosition({ current_price: 110.00, current_trailing_stop: 120.00 });
  await stubGridView(page, [pos]);

  await expect(page.locator('[data-testid="trail-stop-breach-icon"]').first()).toBeVisible({ timeout: 5000 });
});

test('SC-GVP-08: No breach icon when current_price > current_trailing_stop', async ({ page }) => {
  const pos = makePosition({ current_price: 135.00, current_trailing_stop: 115.00 });
  await stubGridView(page, [pos]);

  await expect(page.locator('[data-testid="trail-stop-breach-icon"]')).not.toBeVisible({ timeout: 5000 });
});

// ---------------------------------------------------------------------------
// ST-03/AC-03 — Table View unaffected (breach remains a pill, not an icon)
// ---------------------------------------------------------------------------

test('SC-GVP-09: Table View breach indicator unchanged — still a pill, not an icon', async ({ page }) => {
  const pos = makePosition({ current_price: 110.00, current_trailing_stop: 120.00 });
  await stubGridView(page, [pos]);

  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 8000 });
  await tableBtn.click();
  await page.waitForSelector('table', { timeout: 5000 });

  // ST-09 (EPIC-02, v7.0, BLG-FE-96, merged post-EPIC-01): breach badge colour/label/testid
  // updated to match spec (#EA580C, "⚠ BREACH") — selector updated during EPIC-03's post-merge
  // rebase reconciliation (flagged in EPIC-02's execution_state.json process_notes).
  const badge = page.locator('[data-testid="breach-badge"]');
  await expect(badge).toBeVisible({ timeout: 5000 });
  await expect(badge).toContainText('BREACH');
});
