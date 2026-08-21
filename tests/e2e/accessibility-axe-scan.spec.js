/**
 * Standalone axe-core Accessibility CI Scan (ST-21, BLG-QA-83, EPIC-04, v9.0)
 *
 * Runs an automated WCAG accessibility scan (@axe-core/playwright) against
 * a representative set of pages, in CI, on every PR. This is a baseline
 * scan (catches structural/programmatic accessibility violations axe can
 * detect automatically — missing labels, colour-contrast failures,
 * landmark/ARIA misuse, etc.) — it does not replace a manual accessibility
 * review for things axe cannot evaluate (keyboard-only navigation flow,
 * screen-reader announcement quality, cognitive load).
 *
 * Pages scanned (4, above the story's minimum of 3), chosen for variety of
 * UI pattern: a data-dense dashboard (DashboardHome), a card/table toggle
 * view (Positions), a long multi-section form (TradePlan), and a settings
 * page (Settings, form controls + toggles).
 *
 * Only "serious" and "critical" impact violations fail the test — "minor"
 * and "moderate" are logged but non-blocking, consistent with how a
 * baseline CI gate should behave (catch clear regressions without being so
 * strict that unrelated pre-existing findings block every future PR; see
 * the console output in a failing run for the full violation list
 * regardless of severity).
 *
 * KNOWN_VIOLATIONS baseline: this is the FIRST axe-core scan ever run
 * against this app, and it found 5 genuine, pre-existing serious/critical
 * violations across the 4 scanned pages on introduction — filed as
 * BLG-FE-165 through BLG-FE-169 (claude/backlog/backlog.md), not fixed
 * here (out of scope for "add the scan" — fixing app-wide accessibility
 * debt is a separate, larger body of work). Grandfathering them below
 * means the gate goes live now (this story's own AC) without either (a)
 * failing every future PR on day one for pre-existing debt, or (b)
 * silently hiding genuinely new violations — a NEW violation not in this
 * exact (page, ruleId) baseline still fails the build. Remove an entry
 * here in the same commit that closes its corresponding backlog item.
 *
 * Infrastructure: Playwright page.route() network interception. No live
 * backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

'use strict';

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';

// page name -> Set of axe rule IDs grandfathered as pre-existing (see
// module docstring). Each entry maps to its own filed backlog item.
const KNOWN_VIOLATIONS = {
  DashboardHome: new Set(['color-contrast']), // BLG-FE-165
  Positions: new Set([]),
  TradePlan: new Set(['select-name']), // BLG-FE-166
  // BLG-FE-169's color-contrast finding (Settings subtitle) was observed
  // once during initial exploration but did not reproduce across repeated
  // runs of this exact spec afterward — kept grandfathered defensively in
  // case it's a near-threshold/rendering-timing-dependent finding that
  // resurfaces, rather than silently dropped; see BLG-FE-169 for detail.
  Settings: new Set(['button-name', 'label', 'color-contrast']), // BLG-FE-167, BLG-FE-168, BLG-FE-169
};

async function mockRoutes(page) {
  // Broad catch-all: every API call not given a more specific mock below
  // gets a generic 200 empty-envelope response — sufficient for a
  // structural accessibility scan, which does not depend on realistic
  // data volume or content.
  await page.route(new RegExp(`${API}/`), (route) => {
    const url = route.request().url();
    if (url.includes('/market/status')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { spy: { is_risk_on: true }, ftse: { is_risk_on: true } } }),
      });
    }
    if (url.includes('/settings')) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: [{ id: 'settings-1', default_risk_percent: 1.0 }] }),
      });
    }
    // GET /positions returns a bare array, not the {status, data} envelope
    // (same shape tests/e2e/position-stop-currency-basis.spec.js's own
    // mockRoutes uses) — the envelope form here causes a real
    // "allPositions.filter is not a function" runtime error in
    // src/pages/Positions.js, which would otherwise falsely surface as
    // spurious axe-core findings against React's dev-mode error overlay
    // rather than the actual page content.
    if (url.includes('/positions/compliance')) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
    }
    if (/\/positions(\?|$)/.test(url)) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) });
  });
}

async function runAxeScan(page, pageName) {
  const results = await new AxeBuilder({ page }).analyze();
  const known = KNOWN_VIOLATIONS[pageName] || new Set();

  const seriousOrCritical = results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
  const grandfathered = seriousOrCritical.filter((v) => known.has(v.id));
  const blocking = seriousOrCritical.filter((v) => !known.has(v.id));
  const nonBlocking = results.violations.filter((v) => v.impact !== 'serious' && v.impact !== 'critical');

  if (grandfathered.length > 0) {
    console.log(`[axe-core] ${pageName}: ${grandfathered.length} pre-existing (grandfathered, tracked in backlog) violation(s):`);
    for (const v of grandfathered) {
      console.log(`  - [${v.impact}] ${v.id}: ${v.help} (${v.nodes.length} node(s))`);
    }
  }
  if (nonBlocking.length > 0) {
    console.log(`[axe-core] ${pageName}: ${nonBlocking.length} non-blocking (minor/moderate) violation(s):`);
    for (const v of nonBlocking) {
      console.log(`  - [${v.impact}] ${v.id}: ${v.help} (${v.nodes.length} node(s))`);
    }
  }

  if (blocking.length > 0) {
    const detail = blocking
      .map((v) => `  - [${v.impact}] ${v.id}: ${v.help} (${v.nodes.length} node(s)) — ${v.helpUrl}`)
      .join('\n');
    throw new Error(`[axe-core] ${pageName}: ${blocking.length} NEW serious/critical accessibility violation(s) (not in the KNOWN_VIOLATIONS baseline):\n${detail}`);
  }

  return results;
}

test.describe('Standalone axe-core Accessibility Scan (ST-21)', () => {
  test.beforeEach(async ({ page }) => {
    await mockRoutes(page);
  });

  test('DashboardHome has no serious/critical accessibility violations', { tag: ['@smoke'] }, async ({ page }) => {
    await page.goto('/#/DashboardHome');
    await page.waitForLoadState('networkidle');
    await runAxeScan(page, 'DashboardHome');
  });

  test('Positions has no serious/critical accessibility violations', { tag: ['@smoke'] }, async ({ page }) => {
    await page.goto('/#/positions');
    await page.waitForLoadState('networkidle');
    await runAxeScan(page, 'Positions');
  });

  test('TradePlan has no serious/critical accessibility violations', { tag: ['@smoke'] }, async ({ page }) => {
    await page.goto('/#/TradePlan?ticker=AAPL&market=US');
    await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
    await runAxeScan(page, 'TradePlan');
  });

  test('Settings has no serious/critical accessibility violations', { tag: ['@smoke'] }, async ({ page }) => {
    await page.goto('/#/Settings');
    await page.waitForLoadState('networkidle');
    await runAxeScan(page, 'Settings');
  });
});
