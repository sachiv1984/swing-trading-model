/**
 * Analytics Section Link — ST-04 (EPIC-01, v9.16, BLG-FE-253)
 *
 * analytics.md v2.3 §19.1: /PerformanceAnalytics?section=strategy-compliance
 * opens Analytics scrolled to Arc 5 Signal Compliance, once the section has
 * rendered (data, error or empty state — not the skeleton), then focuses the
 * section heading. Unknown/missing section → page loads at the top, no error.
 * Design: docs/design/2026-11-06__release-v9.16/digest-section-link/decision_record.md
 * The digest footer link itself is covered by tests/test_si05_digest_service.py
 * (test_deep_links_include_strategy_compliance_section_link).
 *
 * Scenarios:
 *   SC-SEC-01  Reduced motion: section in the viewport, heading focused (design record §6)
 *   SC-SEC-02  ?section=unknown loads at the top with no error (design record §6)
 *   SC-SEC-03  No section param: page loads at the top, heading not focused
 *   SC-SEC-04  Default motion: the section still ends up in view and focused
 *   SC-SEC-05  No scroll while the section shows its skeleton; scrolls once data arrives
 *   SC-SEC-06  Error state counts as rendered: scrolls to the section's error state
 *   SC-SEC-07  If the user scrolls before the section is ready, it does not scroll them
 *
 * ROUTING NOTE: App uses HashRouter — navigate with page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';

const ARC5_OK = {
  status: 'ok',
  data: {
    events_per_week: 2.3,
    override_rate: 0.143,
    top_rule_breach: 'regime_gate',
    trade_plan_adherence_rate: 0.725,
    total_closed_trades: 40,
  },
};

function buildMockTrades(count = 12) {
  const now = new Date();
  return Array.from({ length: count }, (_, i) => ({
    id: `trade-${i}`,
    ticker: 'AAPL',
    market: 'US',
    entry_date: new Date(now.getTime() - (i + 5) * 86400000).toISOString(),
    exit_date: new Date(now.getTime() - i * 86400000).toISOString(),
    entry_price: 100,
    exit_price: 105,
    pnl: 50,
    shares: 10,
  }));
}

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: {} }) })
  );
  await page.route(new RegExp(`${API}/trades$`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: buildMockTrades() }) })
  );
}

async function mockArc5(page, { payload = ARC5_OK, status = 200, gate = null } = {}) {
  await page.route(new RegExp(`${API}/analytics/arc5-compliance`), async (route) => {
    if (gate) await gate;
    await route.fulfill({ status, contentType: 'application/json', body: JSON.stringify(payload) });
  });
}

const section = (page) => page.getByTestId('analytics-section-strategy-compliance');
const heading = (page) => section(page).getByRole('heading', { name: 'Arc 5 Signal Compliance' });

async function headingIsFocused(page) {
  return page.evaluate(() => {
    const el = document.querySelector('#strategy-compliance h2');
    return !!el && document.activeElement === el;
  });
}

async function sectionTopInViewport(page) {
  return page.evaluate(() => {
    const r = document.getElementById('strategy-compliance').getBoundingClientRect();
    return r.top >= 0 && r.top < window.innerHeight;
  });
}

test('SC-SEC-01: with reduced motion, the section link puts the section in view and focuses its heading', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page);
  await page.goto('/#/PerformanceAnalytics?section=strategy-compliance');

  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await expect(section(page)).toHaveAttribute('id', 'strategy-compliance');
  await expect(heading(page)).toHaveAttribute('tabindex', '-1');
  await expect.poll(() => headingIsFocused(page), { timeout: 5000 }).toBe(true);
  await expect(section(page)).toBeInViewport();
  expect(await sectionTopInViewport(page)).toBe(true);
  expect(await page.evaluate(() => window.scrollY)).toBeGreaterThan(0);
  // The query stays in the URL.
  await expect(page).toHaveURL(/\?section=strategy-compliance$/);
});

test('SC-SEC-02: an unknown section loads the page at the top with no error', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page);
  await page.goto('/#/PerformanceAnalytics?section=unknown');

  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(800);
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
  expect(await headingIsFocused(page)).toBe(false);
  await expect(page.getByRole('heading', { level: 1, name: 'Analytics', exact: true })).toBeInViewport();
});

test('SC-SEC-03: without a section parameter the page loads at the top', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page);
  await page.goto('/#/PerformanceAnalytics');

  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(800);
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
  expect(await headingIsFocused(page)).toBe(false);
});

test('SC-SEC-04: with default motion the section still ends up in view and focused', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await mockFallback(page);
  await mockArc5(page);
  await page.goto('/#/PerformanceAnalytics?section=strategy-compliance');

  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await expect.poll(() => headingIsFocused(page), { timeout: 5000 }).toBe(true);
  await expect.poll(() => sectionTopInViewport(page), { timeout: 5000 }).toBe(true);
});

test('SC-SEC-05: no scroll while the section shows its skeleton; it scrolls once data arrives', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  let release;
  const gate = new Promise((r) => { release = r; });
  await mockArc5(page, { gate });
  await page.goto('/#/PerformanceAnalytics?section=strategy-compliance');

  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(800);
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
  expect(await headingIsFocused(page)).toBe(false);

  release();
  await expect.poll(() => headingIsFocused(page), { timeout: 5000 }).toBe(true);
  expect(await sectionTopInViewport(page)).toBe(true);
});

test('SC-SEC-06: the section error state counts as rendered and is scrolled to', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page, { payload: { status: 'error', detail: 'boom' }, status: 500 });
  await page.goto('/#/PerformanceAnalytics?section=strategy-compliance');

  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await expect.poll(() => headingIsFocused(page), { timeout: 15000 }).toBe(true);
  expect(await sectionTopInViewport(page)).toBe(true);
});

test('SC-SEC-07: if the user scrolls before the section is ready, the page does not scroll them', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  let release;
  const gate = new Promise((r) => { release = r; });
  await mockArc5(page, { gate });
  await page.goto('/#/PerformanceAnalytics?section=strategy-compliance');

  await expect(heading(page)).toBeVisible({ timeout: 15000 });
  await page.mouse.move(700, 400);
  await page.mouse.wheel(0, 120);
  await page.waitForTimeout(300);
  const before = await page.evaluate(() => window.scrollY);

  release();
  await expect(section(page).getByText('Top Rule Breach')).toBeVisible({ timeout: 5000 });
  await page.waitForTimeout(600);
  expect(await headingIsFocused(page)).toBe(false);
  expect(Math.abs((await page.evaluate(() => window.scrollY)) - before)).toBeLessThan(5);
});
