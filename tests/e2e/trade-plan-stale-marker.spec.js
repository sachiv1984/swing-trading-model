/**
 * Stale marker for unactioned trade plans — Trade Plans list (ST-02, EPIC-01, v9.6, BLG-FE-180)
 *
 * Design source: docs/design/2026-09-21__release-v9.6/trade-plan-stale-marker/decision_record.md §5
 * Spec: docs/specs/frontend/pages/trade_plan.md v1.15 §4.6
 *
 * Covers observable AC (ST-02 AC-01, AC-02):
 *   SC-TPS-01  Pre-entry plan last updated 15 days ago shows "Stale (15 days)"
 *   SC-TPS-02  Same statuses at 10 days show no marker (a newer plan does not)
 *   SC-TPS-03  Boundary: exactly 14 whole days shows no marker; 15 shows it (N > 14)
 *   SC-TPS-04  active / closed / abandoned plans never show the marker, even at 30 days
 *   SC-TPS-05  Marker is display-only text (not a button), keeps the status badge, has aria-label + title
 *
 * `updated_at` is derived from the real clock with a 1h margin so whole-day floors are stable.
 * Infrastructure: Playwright page.route() network interception. HashRouter — navigate via '/#/…'.
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';
const HOUR = 3600 * 1000;
const DAY = 24 * HOUR;

const daysAgo = (n) => new Date(Date.now() - n * DAY - HOUR).toISOString(); // n whole days + 1h
const json = (data) => ({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data }) });

const plan = (id, ticker, status, days) => ({
  id, ticker, market: 'US', status, position_id: null, r_target: 2, setup_thesis: 'thesis',
  created_at: daysAgo(days + 5), updated_at: daysAgo(days),
});

async function gotoList(page, plans) {
  await page.route(new RegExp(`${API}/`), (route) => route.fulfill(json([])));
  await page.route(`${API}/trade-plans/tags`, (route) => route.fulfill(json([])));
  await page.route(`${API}/trade-plans`, (route) => route.fulfill(json(plans)));
  await page.goto('/#/TradePlans');
  await expect(page.getByText(plans[0].ticker, { exact: true })).toBeVisible({ timeout: 10000 });
}

const rowFor = (page, ticker) => page.locator('tr', { hasText: ticker });

test('SC-TPS-01: A pre-entry plan last updated 15 days ago shows the stale marker', async ({ page }) => {
  await gotoList(page, [plan('a', 'AAA', 'draft', 15)]);
  await expect(rowFor(page, 'AAA').getByTestId('stale-plan-marker')).toHaveText('Stale (15 days)');
});

test('SC-TPS-02: The same statuses at 10 days show no marker', async ({ page }) => {
  await gotoList(page, [
    plan('a', 'AAA', 'draft', 10),
    plan('b', 'BBB', 'research_pending', 10),
    plan('c', 'CCC', 'research_complete', 10),
    plan('d', 'DDD', 'entry_conditions_set', 10),
  ]);
  await expect(page.getByTestId('stale-plan-marker')).toHaveCount(0);
});

test('SC-TPS-03: Boundary — 14 whole days shows no marker, 15 shows it, for all four pre-entry statuses', async ({ page }) => {
  const statuses = ['draft', 'research_pending', 'research_complete', 'entry_conditions_set'];
  const plans = [];
  statuses.forEach((st, i) => {
    plans.push(plan(`e${i}`, `EQ${i}`, st, 14)); // N = 14 -> not stale
    plans.push(plan(`o${i}`, `OV${i}`, st, 15)); // N = 15 -> stale
  });
  await gotoList(page, plans);
  for (let i = 0; i < statuses.length; i++) {
    await expect(rowFor(page, `EQ${i}`).getByTestId('stale-plan-marker')).toHaveCount(0);
    await expect(rowFor(page, `OV${i}`).getByTestId('stale-plan-marker')).toHaveText('Stale (15 days)');
  }
});

test('SC-TPS-04: active, closed and abandoned plans are never marked, even at 30 days', async ({ page }) => {
  await gotoList(page, [
    plan('a', 'AAA', 'active', 30),
    plan('b', 'BBB', 'closed', 30),
    plan('c', 'CCC', 'abandoned', 30),
  ]);
  await expect(page.getByTestId('stale-plan-marker')).toHaveCount(0);
});

test('SC-TPS-05: The marker is display-only text alongside the unchanged status badge, with aria-label and title', async ({ page }) => {
  await gotoList(page, [plan('a', 'AAA', 'research_pending', 20)]);
  const row = rowFor(page, 'AAA');
  const marker = row.getByTestId('stale-plan-marker');
  await expect(marker).toHaveAttribute('aria-label', 'Last updated 20 days ago — plan is stale');
  await expect(marker).toHaveAttribute('title', /Last updated .+\. Display only — nothing happens automatically\./);
  await expect(marker).toHaveClass(/text-amber-600/);
  await expect(marker).toHaveClass(/dark:text-amber-400/);
  // Not interactive: no button/link role, no "Keep" action anywhere in the row
  expect(await marker.evaluate((el) => el.tagName)).toBe('SPAN');
  await expect(row.getByRole('button', { name: /keep/i })).toHaveCount(0);
  // Status badge is unchanged and still present
  await expect(row.getByText('Research Pending', { exact: true })).toBeVisible();
});
