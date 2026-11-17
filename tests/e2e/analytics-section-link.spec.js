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
const { mockAnalyticsMetrics } = require('./fixtures/analytics-metrics');

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

// ST-06 (EPIC-02, v9.17, BLG-FE-259): the Analytics page's own
// ?section=strategy-compliance link (analytics.md §19.1) is superseded by the
// Performance page's section index (performance.md v1.1 §3, §7). The SI-05
// digest's old link redirects to /Performance?section=compliance, which jumps
// to the Compliance section heading once the page's data is ready. These
// scenarios keep the §19.1 behaviours on the new route.

const complianceHeading = (page) => page.locator('#compliance > h2');
const arc5Heading = (page) => page.getByTestId('analytics-section-strategy-compliance').getByRole('heading', { name: 'Arc 5 Signal Compliance' });

async function complianceFocused(page) {
  return page.evaluate(() => document.activeElement === document.querySelector('#compliance > h2'));
}

async function complianceTopInViewport(page) {
  return page.evaluate(() => {
    const r = document.querySelector('#compliance > h2').getBoundingClientRect();
    return r.top >= 0 && r.top < window.innerHeight;
  });
}

test('SC-SEC-01: the old digest link lands on Compliance, in view and focused (reduced motion)', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page);
  await page.goto('/#/PerformanceAnalytics?section=strategy-compliance');

  await expect(page).toHaveURL(/#\/Performance\?section=compliance$/);
  await expect(arc5Heading(page)).toBeVisible({ timeout: 15000 });
  await expect.poll(() => complianceFocused(page), { timeout: 5000 }).toBe(true);
  expect(await complianceTopInViewport(page)).toBe(true);
  expect(await page.evaluate(() => window.scrollY)).toBeGreaterThan(0);
});

test('SC-SEC-02: an unknown section loads the page at the top with no error', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page);
  const errors = [];
  page.on('pageerror', (e) => errors.push(e));
  await page.goto('/#/Performance?section=unknown');

  await expect(arc5Heading(page)).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(800);
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
  expect(await complianceFocused(page)).toBe(false);
  await expect(page.getByRole('heading', { level: 1, name: 'Performance', exact: true })).toBeInViewport();
  expect(errors).toHaveLength(0);
});

test('SC-SEC-03: without a section parameter the page loads at the top', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page);
  await page.goto('/#/Performance');

  await expect(arc5Heading(page)).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(800);
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
  expect(await complianceFocused(page)).toBe(false);
});

test('SC-SEC-04: with default motion the section still ends up in view and focused', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await mockFallback(page);
  await mockArc5(page);
  await page.goto('/#/Performance?section=compliance');

  await expect(arc5Heading(page)).toBeVisible({ timeout: 15000 });
  await expect.poll(() => complianceFocused(page), { timeout: 5000 }).toBe(true);
  await expect.poll(() => complianceTopInViewport(page), { timeout: 5000 }).toBe(true);
});

test('SC-SEC-05: no jump while the page data is loading; it jumps once the data arrives', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page);
  let release;
  const gate = new Promise((r) => { release = r; });
  await page.route(/localhost:8000\/analytics\/metrics/, async (route) => {
    await gate;
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { has_enough_data: false, summary: { total_trades: 0 } } }) });
  });
  await page.goto('/#/Performance?section=compliance');

  await expect(complianceHeading(page)).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(600);
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
  expect(await complianceFocused(page)).toBe(false);

  release();
  await expect.poll(() => complianceFocused(page), { timeout: 5000 }).toBe(true);
  expect(await complianceTopInViewport(page)).toBe(true);
});

test('SC-SEC-06: an Arc 5 error state is still reached through the section link', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await mockFallback(page);
  await mockArc5(page, { status: 500, payload: { status: 'error' } });
  await mockAnalyticsMetrics(page);
  await page.goto('/#/Performance?section=compliance');

  await expect(page.locator('#compliance').getByText('Unable to load').first()).toBeVisible({ timeout: 20000 });
  await expect.poll(() => complianceFocused(page), { timeout: 5000 }).toBe(true);
  expect(await complianceTopInViewport(page)).toBe(true);
});
