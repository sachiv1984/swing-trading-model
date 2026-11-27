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

const { test, expect } = require('./fixtures/api-status-guard');
const { expandAllPositionRows, positionDetail } = require('./fixtures/positions-table');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';

// page name -> Set of axe rule IDs grandfathered as pre-existing (see
// module docstring). Each entry maps to its own filed backlog item.
const KNOWN_VIOLATIONS = {
  DashboardHome: new Set([]), // BLG-FE-165 fixed v9.1/ST-01 — AiDisclaimer.js badge bg-amber-600 -> bg-amber-700
  Positions: new Set([]),
  TradePlan: new Set([]), // BLG-FE-166 fixed v9.1/ST-02 — aria-label added to Market/Status/Setup Type selects
  // BLG-FE-167 (button-name) and BLG-FE-168 (label) fixed v9.1/ST-03/ST-04 —
  // aria-label added to Select triggers, id/htmlFor pairing added to Inputs.
  // BLG-FE-169 (color-contrast, Settings subtitle) fixed v9.1/ST-05: not a
  // colour defect — PageHeader.js's description text already uses the
  // approved text-slate-600 dark:text-slate-400 token. Root cause was a
  // scan-timing race against the page's framer-motion fade-in (see
  // runAxeScan's pre-scan wait, below) — axe-core occasionally sampled the
  // text mid-animation at <1 opacity, producing a transient low-contrast
  // reading. Fixed at the scan level (runAxeScan waits out the entrance
  // animation), confirmed with 5 consecutive clean local runs.
  Settings: new Set([]),
  // ST-19 (BLG-QA-195, EPIC-04, v9.10): pages added to the scan, keyed
  // "<page>:<theme>". The scan's button-name findings (unlabelled Select
  // triggers on Reports and Notification History, unlabelled preference
  // Switches) were fixed in the same story. The light-theme color-contrast findings
  // (BLG-FE-200) were fixed in v9.12 ST-23 with the light-theme token pairs in
  // design_system.md §Light-Theme Colour Tokens, so neither theme has a baseline entry.
  'ReportsMonthly:dark': new Set([]),
  'ReportsTaxYear:dark': new Set([]),
  'NotificationPreferences:dark': new Set([]),
  'NotificationsHistory:dark': new Set([]),
  'ReportsMonthly:light': new Set([]),
  // ST-37 (BLG-QA-196, EPIC-06, v9.11): Replay page, both selector modes and a populated
  // result, in both themes. The dark theme has no baseline entries (its one finding, the
  // Risk-Off badge's contrast, was fixed in the same story). The light-theme color-contrast
  // entries were removed by ST-26 (BLG-FE-209, v9.13), which applied the light-theme tokens.
  'ReplayDateRange:dark': new Set([]),
  'ReplayTradeSet:dark': new Set([]),
  'ReplayResult:dark': new Set([]),
  'ReplayDateRange:light': new Set([]),
  'ReplayTradeSet:light': new Set([]),
  'ReplayResult:light': new Set([]),
  'ReportsTaxYear:light': new Set([]),
  'NotificationPreferences:light': new Set([]),
  'NotificationsHistory:light': new Set([]),
  // ST-09 (BLG-FE-264, EPIC-03, v9.16): the four shell pages in the light theme.
  'DashboardHome:light': new Set([]),
  'PositionsEmpty:light': new Set([]),
  'PositionsPopulated:light': new Set([]),
  'PositionsPopulatedTable:light': new Set([]),
  'TradePlan:light': new Set([]),
  'Settings:light': new Set([]),
  // ST-09 scope ruling (Product Owner, 2026-11-10): the other consumers of the
  // converted shells, in populated states, in the light theme.
  'DashboardPopulated:light': new Set([]),
  'TradeHistoryExpanded:light': new Set([]),
  'WeeklyDigest:light': new Set([]),
  // EPIC-03 review pass 1 (Product Owner ruling, 2026-11-10): the Trade Entry
  // card is themed so ST-10's text-app-fg input text reads in light.
  // label (Risk % and entry date inputs) and button-name (market Select):
  // pre-existing and theme-independent, BLG-FE-286.
  'TradeEntry:light': new Set(['label', 'button-name']),
  // EPIC-03 review pass 2: the pre-entry advisory badges, rendered.
  'TradeEntryPreEntry:light': new Set([]),
  // ST-08 / BLG-FE-303: Trade Entry with the Setup Thesis Digest rendered. Same
  // pre-existing, theme-independent Trade Entry findings as above (BLG-FE-286).
  'TradeEntrySetupThesisDigest:light': new Set(['label', 'button-name']),
  'TradeEntrySetupThesisDigest:dark': new Set(['label', 'button-name']),
};

// ST-20 (BLG-QA-260, EPIC-04, v9.18): axe returns contrast it cannot decide
// (text on a translucent tint, a gradient or an image, or partly covered) as
// `incomplete`, not as a violation, so a 4.48:1 grace pill once passed the
// light scan (v9.16 EPIC-03). Every scan logs its incomplete color-contrast
// nodes, split into page content and the app shell (sidebar and top header,
// whose 6-8 nodes repeat on every full-page scan: gradient logo text, the
// gradient active nav item, nav links axe calls partly covered). A scan whose
// name is in this set also fails on any page-content node. The set is every
// scan whose page content had none on 2026-11-23; add a scan once its log shows
// "0 page content".
const STRICT_INCOMPLETE_CONTRAST = new Set([
  'DashboardPopulated:light',
  'JournalNotes:light',
  'JournalRedFlags:dark',
  'JournalRedFlags:light',
  'JournalReflections:light',
  'Notifications:light',
  'NotificationsEmpty:light',
  'NotificationsNotSent:light',
  'ReplayDateRange:dark',
  'ReplayDateRange:light',
  'ReplayTradeSet:dark',
  'ReplayTradeSet:light',
  'ResearchLanding:dark',
  'ResearchLanding:light',
  'StrategyVsBacktest:dark',
  'StrategyVsBacktest:light',
  'TickerUniverse:dark',
  'TickerUniverse:light',
  'WeeklyDigest:light',
]);

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

async function waitForEntranceAnimations(page) {
  // ST-07 (BLG-QA-157, EPIC-03, v9.2): condition-based replacement for the
  // fixed 1000ms sleep this helper used previously. framer-motion drives its
  // animated values (opacity included) via a direct inline `style` attribute
  // rather than a CSS class, both while animating and once settled — so
  // polling for "no element still has an inline opacity below its settled
  // value" detects the actual end of the fade instead of guessing a duration
  // long enough to outlast it. This resolves as soon as the page has
  // actually settled (typically well under the design_system.md v1.12
  // 500ms time-to-full-opacity ceiling), rather than always paying a fixed
  // 1000ms regardless of how long the animation actually took.
  try {
    await page.waitForFunction(
      () => {
        const stillAnimating = Array.from(document.querySelectorAll('[style*="opacity"]')).some((el) => {
          const opacity = parseFloat(getComputedStyle(el).opacity);
          return !Number.isNaN(opacity) && opacity < 0.98;
        });
        return !stillAnimating;
      },
      // ST-08: waitForFunction's second argument is the page-function argument;
      // options go third. Passed second, the 3s cap was ignored, so a page with a
      // persistent low-opacity element (an open Radix dialog) waited out the test.
      undefined,
      { timeout: 3000 },
    );
  } catch (e) {
    // Timeout guard, not an assertion: if some element never reaches 0.98
    // (e.g. an unrelated element with its own persistent low-opacity inline
    // style, not a framer-motion entrance fade), proceed rather than fail
    // the scan outright — this wait is a race-avoidance step, not itself
    // a correctness check.
  }
}

async function runAxeScan(page, pageName, { include } = {}) {
  // BLG-FE-169 root cause (v9.1/ST-05): PageHeader.js (and other page-level
  // containers) fade in via framer-motion (opacity 0 -> 1, ~0.3-0.8s
  // default transition). page.waitForLoadState('networkidle') does not
  // wait for in-progress CSS/JS animations — if axe-core's scan lands
  // mid-fade, the text's rendered opacity is transiently <1, producing a
  // real-but-transient low-contrast reading against an otherwise-compliant
  // token (text-slate-600 dark:text-slate-400, ~4.5:1+ at full opacity).
  // This is what made the Settings subtitle finding "non-reproduce
  // across repeated runs" — it's a scan-timing race, not a colour defect.
  // Waiting out the entrance animation before scanning removes the race.
  await waitForEntranceAnimations(page);
  // `include` (ST-09, v9.16) limits a scan to one region, for a page whose
  // other regions are tracked separately.
  const builder = new AxeBuilder({ page });
  if (include) builder.include(include);
  const results = await builder.analyze();
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

  const incompleteContrast = results.incomplete
    .filter((r) => r.id === 'color-contrast')
    .flatMap((r) => r.nodes);
  const inShell = await nodesInAppShell(page, incompleteContrast);
  const shellIncomplete = incompleteContrast.filter((_, i) => inShell[i]);
  const contentIncomplete = incompleteContrast.filter((_, i) => !inShell[i]);
  const strictIncomplete = STRICT_INCOMPLETE_CONTRAST.has(pageName);
  if (incompleteContrast.length > 0) {
    console.log(`[axe-core] ${pageName}: ${incompleteContrast.length} incomplete color-contrast node(s), contrast not decided by axe (${contentIncomplete.length} page content, ${shellIncomplete.length} app shell)${strictIncomplete ? '' : '; logged only, not in STRICT_INCOMPLETE_CONTRAST'}:`);
    for (const n of contentIncomplete) console.log(`  - ${describeNode(n)}`);
    for (const n of shellIncomplete) console.log(`  - [shell] ${describeNode(n)}`);
  }

  const failures = [];
  if (blocking.length > 0) {
    const detail = blocking
      .map((v) => `  - [${v.impact}] ${v.id}: ${v.help} (${v.nodes.length} node(s)) — ${v.helpUrl}\n`
        // ST-08: name the first nodes, so a CI failure says which element to fix.
        + v.nodes.slice(0, 5).map((n) => `      ${describeNode(n)}`).join('\n'))
      .join('\n');
    failures.push(`${blocking.length} NEW serious/critical accessibility violation(s) (not in the KNOWN_VIOLATIONS baseline):\n${detail}`);
  }
  if (strictIncomplete && contentIncomplete.length > 0) {
    const detail = contentIncomplete.slice(0, 5).map((n) => `      ${describeNode(n)}`).join('\n');
    failures.push(`${contentIncomplete.length} incomplete color-contrast node(s) in page content on a STRICT_INCOMPLETE_CONTRAST page; give the text a solid background or a definite contrast:\n${detail}`);
  }
  if (failures.length > 0) {
    throw new Error(`[axe-core] ${pageName}: ${failures.join('\n')}`);
  }

  return results;
}

// For each axe node, whether it sits in the app shell (Layout.js: the sidebar
// <aside> or the top <header>, both outside <main>). Shell nodes repeat on
// every full-page scan, so the strict rule judges page content only and the
// shell's nodes are logged. Dialogs portal outside <main> but are not in the
// shell, so they count as page content. A node axe targets inside an iframe
// or shadow root (target length > 1) counts as content.
async function nodesInAppShell(page, nodes) {
  const selectors = nodes.map((n) => (n.target.length === 1 ? n.target[0] : null));
  return page.evaluate((sels) => sels.map((sel) => {
    if (!sel) return false;
    const el = document.querySelector(sel);
    if (!el) return false;
    // Only the layout's own aside/header: never inside <main> or a dialog
    // (PR #2311 review — an aside in page content or a dialog's header is content).
    if (el.closest('main') || el.closest('[role="dialog"], [role="alertdialog"]')) return false;
    return Boolean(el.closest('aside') || el.closest('header'));
  }), selectors);
}

// One line per axe node: selector | markup | axe's reason (truncated).
function describeNode(n) {
  const reason = (n.any[0] || n.all[0] || n.none[0] || {}).message || '';
  return `${n.target.join(' ')} | ${n.html.slice(0, 140)} | ${reason}`.slice(0, 400);
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

// ---------------------------------------------------------------------------
// ST-19 (BLG-QA-195, EPIC-04, v9.10): Reports and Notifications pages, in
// dark and light themes. Reports is scanned in the states the story names:
// the Monthly tab with a restated month expanded, and the Tax Year tab with
// the restated-months notice. Theme is set through the same localStorage
// "theme" key Layout.js reads on mount.
// ---------------------------------------------------------------------------

const RESTATED_MONTH = {
  year: 2026, month: 5, realised_pnl_gbp: 175, trade_count: 4, null_fee_trade_count: 0,
  snapshotted: true, restated: true, snapshot_realised_pnl_gbp: 150, restated_diff_gbp: 25,
};
const PLAIN_MONTH = {
  year: 2026, month: 4, realised_pnl_gbp: -60, trade_count: 3, null_fee_trade_count: 0,
  snapshotted: true, restated: false, snapshot_realised_pnl_gbp: -60, restated_diff_gbp: 0,
};

const { TD_PREFS_ALL_ON: ALL_PREFS } = require('./mocks/notifications-mock-data');

const HISTORY = {
  status: 'ok',
  data: {
    total: 2,
    evaluations: [
      {
        id: 'eval-1', evaluation_timestamp: '2026-10-05T08:00:00Z', rule_type: 'stop_loss_approach', symbol: 'AAPL',
        triggered: true, notification_sent: true,
        values_compared: { stop_price: 42.1, current_price: 43.5, gap_pct: 3.3, threshold_pct: 5.0 },
      },
      {
        id: 'eval-2', evaluation_timestamp: '2026-10-05T07:00:00Z', rule_type: 'grace_period_warning', symbol: 'VOD',
        triggered: false, notification_sent: false, values_compared: {},
      },
    ],
  },
};

async function mockSt19Routes(page) {
  await page.route(new RegExp(`${API}/reports/monthly-pnl(?!\\?format=csv)`), (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: [RESTATED_MONTH, PLAIN_MONTH], estimated_unrealised_pnl: null, unrealised_note: null, compliance_summary: null }),
    })
  );
  await page.route(new RegExp(`${API}/reports/tax-year(?!\\?format=csv)`), (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          tax_year_label: '2026/27',
          summary: { total_realised_pnl: 115, total_gross_profit: 175, total_gross_loss: -60, win_rate: 50, total_closed_trades: 7, restated_month_count: 1, estimated_unrealised_pnl: 0, unrealised_note: null, unrealised_price_stale_count: 1 },
          trades: [],
        },
      }),
    })
  );
  await page.route(/\/notifications\/preferences/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ALL_PREFS) })
  );
  await page.route(/\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(HISTORY) })
  );
}

// Confirm the theme actually applied before scanning, so a light run is not a second
// dark run. ST-35 (BLG-QA-216, EPIC-05, v9.14) moved this from the Reports Monthly test
// into every Reports/Notifications and Replay scan.
async function expectThemeApplied(page, theme) {
  if (theme === 'dark') {
    await expect(page.locator('html')).toHaveClass(/\bdark\b/);
  } else {
    await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);
  }
}

for (const theme of ['dark', 'light']) {
  test.describe(`Reports and Notifications axe scan — ${theme} theme (ST-19)`, () => {
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await mockRoutes(page);
      await mockSt19Routes(page);
    });

    test(`Reports Monthly tab with a restated month expanded (${theme})`, async ({ page }) => {
      await page.goto('/#/Performance?section=reports');
      await page.getByTestId('performance-report-tab-monthly').click();
      const marker = page.getByTestId('monthly-restated-marker');
      await expect(marker).toBeVisible({ timeout: 10000 });
      await marker.click();
      await expect(page.getByTestId('monthly-restatement-detail')).toBeVisible();
      await expectThemeApplied(page, theme);
      // ST-06 (v9.17): Reports is one section of the Performance page; scan
      // that section, as this test scanned the Reports page before. The other
      // sections' analytics components are ST-08's token sweep.
      await runAxeScan(page, `ReportsMonthly:${theme}`, { include: 'section#reports' });
    });

    test(`Reports Tax Year tab with the restated-months notice (${theme})`, async ({ page }) => {
      await page.goto('/#/Performance?section=reports');
      await page.getByTestId('performance-report-tab-tax-year').click();
      await expect(page.getByTestId('taxyear-restated-notice')).toBeVisible({ timeout: 10000 });
      await expectThemeApplied(page, theme);
      await runAxeScan(page, `ReportsTaxYear:${theme}`, { include: 'section#reports' });
    });

    test(`Notification preferences (${theme})`, async ({ page }) => {
      await page.goto('/#/notifications/preferences');
      await expect(page.getByText('Stop Loss Approach').first()).toBeVisible({ timeout: 10000 });
      await expectThemeApplied(page, theme);
      await runAxeScan(page, `NotificationPreferences:${theme}`);
    });

    test(`Notification history (${theme})`, async ({ page }) => {
      await page.goto('/#/notifications/history');
      await page.waitForLoadState('networkidle');
      await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 10000 });
      await expectThemeApplied(page, theme);
      await runAxeScan(page, `NotificationsHistory:${theme}`);
    });
  });
}

// ---------------------------------------------------------------------------
// ST-37 (BLG-QA-196, EPIC-06, v9.11) — Replay page (src/pages/Replay.js):
// Date Range mode, Trade Set mode with the checkbox list, and a populated
// result, each in dark and light themes. Mocks follow replay-mode.spec.js.
// ---------------------------------------------------------------------------

const REPLAY_TRADES = [
  { id: '11111111-1111-1111-1111-111111111111', ticker: 'NVDA', exit_date: '2026-05-12' },
  { id: '22222222-2222-2222-2222-222222222222', ticker: 'AAPL', exit_date: '2026-04-01' },
];

const REPLAY_RESULT = {
  status: 'ok',
  data: {
    retrospective_notice: 'Retrospective result — shows what the current rules would have produced over this past period. Not a prediction of future performance.',
    run: {
      mode: 'date_range', date_from: '2026-03-01', date_to: '2026-06-30',
      requested_trade_count: 2, replayed_trade_count: 2, skipped: [],
      rule_set: { stop_loss_mode: 'profit_lock', atr_mult: 2, initial_atr_mult: 5, profit_atr_mult: 2, min_hold_days: 10, risk_off_mode: 'single' },
      price_data_source: 'yfinance', price_data_fingerprint: 'sha256:deadbeef',
    },
    summary: { trade_count: 2, win_count: 1, win_rate_pct: 50, total_simulated_pnl_gbp: 73.91, excluded_from_gbp_total: 0 },
    trades: [
      { trade_id: REPLAY_TRADES[0].id, ticker: 'NVDA', market: 'US', currency: 'USD', entry_date: '2026-03-04', entry_price: 121.5,
        shares: 10, initial_stop: 110.2, simulated_exit_date: '2026-05-12', simulated_exit_price: 133.1, simulated_exit_reason: 'Stop',
        holding_days: 69, simulated_pnl_native: 114.0, simulated_pnl_gbp: 89.63, fx_basis: 'entry_fx_rate' },
      { trade_id: REPLAY_TRADES[1].id, ticker: 'AAPL', market: 'US', currency: 'USD', entry_date: '2026-03-10', entry_price: 170.0,
        shares: 5, initial_stop: 160.0, simulated_exit_date: '2026-04-01', simulated_exit_price: 166.0, simulated_exit_reason: 'Risk-Off',
        holding_days: 22, simulated_pnl_native: -20, simulated_pnl_gbp: -15.72, fx_basis: 'entry_fx_rate' },
    ],
  },
};

async function mockReplayRoutes(page) {
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { total_trades: 2, win_rate: 50, total_pnl: 0, trades: REPLAY_TRADES } }) })
  );
  await page.route(`${API}/replay/run`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(REPLAY_RESULT) })
  );
}

for (const theme of ['dark', 'light']) {
  test.describe(`Replay page axe scan — ${theme} theme (ST-37)`, () => {
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((t) => {
        window.localStorage.setItem('theme', t);
        // The first-session ⌘K hint toast (Layout.js) fades in 1.2s after load;
        // a scan that lands while it fades reads it as undecided page content
        // (ReplayTradeSet:dark, run 45456088330). Same suppression as the ST-08 scans.
        window.localStorage.setItem('command-palette-tooltip-seen', 'true');
      }, theme);
      await mockRoutes(page);
      await mockReplayRoutes(page);
      await page.goto('/#/Replay');
      await expect(page.getByRole('heading', { name: 'Replay', exact: true })).toBeVisible({ timeout: 10000 });
      await expectThemeApplied(page, theme);
    });

    test(`Replay — Date Range mode (${theme})`, async ({ page }) => {
      await expect(page.getByTestId('replay-date-range-controls')).toBeVisible();
      await runAxeScan(page, `ReplayDateRange:${theme}`);
    });

    test(`Replay — Trade Set mode with the checkbox list (${theme})`, async ({ page }) => {
      await page.getByTestId('replay-mode-tab-trade-set').click();
      await expect(page.getByTestId(`replay-trade-checkbox-${REPLAY_TRADES[0].id}`)).toBeVisible({ timeout: 8000 });
      await runAxeScan(page, `ReplayTradeSet:${theme}`);
    });

    test(`Replay — populated result (${theme})`, async ({ page }) => {
      await page.getByTestId('replay-date-from').fill('2026-03-01');
      await page.getByTestId('replay-date-to').fill('2026-06-30');
      await page.getByTestId('replay-run-button').click();
      await expect(page.getByTestId('replay-results-table')).toBeVisible({ timeout: 10000 });
      await runAxeScan(page, `ReplayResult:${theme}`);
    });
  });
}


// ---------------------------------------------------------------------------
// ST-09 (BLG-FE-264, EPIC-03, v9.16): light-theme scans of the four shell
// pages named by the story's AC: Dashboard, Positions (empty and populated,
// in card and table view), Trade Plan and Settings. The body base, DashboardCard,
// DataTable and PageHeader moved to the app-* semantic colour tokens
// (design_system.md v1.25 §Semantic Colour Tokens), so these pages no longer
// render dark-only shells in the light theme. No baseline entries: a
// color-contrast finding here fails the build.
// ---------------------------------------------------------------------------

const ST09_POSITIONS = [
  {
    id: 'pos-st09-us', ticker: 'WDC', market: 'US', entry_price: 100.0, current_price: 92.31,
    current_price_native: 120.0, initial_stop: 80.0, current_trailing_stop: 76.92,
    current_trailing_stop_native: 100.0, stop_price: 76.92, stop_price_native: 100.0, shares: 10,
    pnl: 153.85, pnl_percent: 20.0, holding_days: 15, grace_days_remaining: null, status: 'open',
    entry_date: '2026-07-25', tags: null,
  },
  {
    id: 'pos-st09-uk', ticker: 'VOD.L', market: 'UK', entry_price: 120.0, current_price: 100.0,
    current_price_native: 100.0, initial_stop: 95.0, current_trailing_stop: 95.0,
    current_trailing_stop_native: 95.0, stop_price: 95.0, stop_price_native: 95.0, shares: 10,
    pnl: -200.0, pnl_percent: -16.67, holding_days: 3, grace_days_remaining: 2, status: 'open',
    entry_date: '2026-11-05', tags: null,
  },
];

async function mockSt09PopulatedPositions(page) {
  await page.route(new RegExp(`${API}/positions(\\?|$)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ST09_POSITIONS) })
  );
  // Review pass 3: render both earnings badge variants (Today, and near-term
  // within 5 days) in the Positions table, which the white shell exposed.
  await page.route(new RegExp(`${API}/earnings/`), (route) => {
    const days = route.request().url().includes('/earnings/WDC') ? 0 : 3;
    return route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ days_until_earnings: days, next_earnings_date: '2026-11-13' }),
    });
  });
}

test.describe('Shell pages axe scan — light theme (ST-09)', () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await mockRoutes(page);
  });

  test('Dashboard (light)', async ({ page }) => {
    await page.goto('/#/DashboardHome');
    await page.waitForLoadState('networkidle');
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'DashboardHome:light');
  });

  test('Positions, empty (light)', async ({ page }) => {
    await page.goto('/#/positions');
    await page.waitForLoadState('networkidle');
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'PositionsEmpty:light');
  });

  test('Positions, populated card view (light)', async ({ page }) => {
    await mockSt09PopulatedPositions(page);
    await page.goto('/#/positions');
    await expect(page.getByText('WDC').first()).toBeVisible({ timeout: 10000 });
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'PositionsPopulated:light');
  });

  test('Positions, populated table view (light)', async ({ page }) => {
    await mockSt09PopulatedPositions(page);
    await page.goto('/#/positions');
    const tableBtn = page.locator('[aria-label="Table view"]');
    await tableBtn.waitFor({ state: 'visible', timeout: 10000 });
    await tableBtn.click();
    await expect(page.getByRole('row').filter({ hasText: 'WDC' })).toBeVisible({ timeout: 10000 });
    // ST-01 (BLG-FE-260, v9.17): Earnings lives in the expanded row; opening every
    // row also puts the detail grid in the scan.
    await expandAllPositionRows(page);
    await expect(positionDetail(page, 'WDC').getByText('Today')).toBeVisible({ timeout: 10000 });
    await expect(positionDetail(page, 'VOD.L').getByText('⚠ 3d')).toBeVisible({ timeout: 10000 });
    await expectThemeApplied(page, 'light');
    // With the old bare text-amber-400 rendered, axe still reported no
    // color-contrast violation on this scan (checked 2026-11-10; it does not
    // always decide text on translucent fills, BLG-QA-260), so the earnings
    // badges' light colour is asserted directly:
    // amber-800 (rgb 146, 64, 14) on amber-500/15 over white measures 6.32:1.
    await expect(positionDetail(page, 'WDC').getByText('Today')).toHaveCSS('color', 'rgb(146, 64, 14)');
    await expect(positionDetail(page, 'VOD.L').getByText('⚠ 3d')).toHaveCSS('color', 'rgb(146, 64, 14)');
    await runAxeScan(page, 'PositionsPopulatedTable:light');
  });

  test('Trade Plan (light)', async ({ page }) => {
    await page.goto('/#/TradePlan?ticker=AAPL&market=US');
    await expect(page.locator('h1').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'TradePlan:light');
  });

  test('Settings (light)', async ({ page }) => {
    await page.goto('/#/Settings');
    await page.waitForLoadState('networkidle');
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'Settings:light');
  });
});

// ---------------------------------------------------------------------------
// ST-09 scope ruling (Product Owner, 2026-11-10): turning DataTable and
// DashboardCard white in the light theme exposed dark-only content in their
// other consumers. These scans cover those consumers in populated states:
// the Dashboard cards holding data, Trade History with a journal row
// expanded, and the Weekly Digest table.
// ---------------------------------------------------------------------------

const ST09_TRADES = [
  {
    id: 'trade-st09-win', ticker: 'AAPL', market: 'US', entry_date: '2026-10-01', exit_date: '2026-10-20',
    entry_price: 170, exit_price: 184, shares: 100, pnl: 1400, pnl_pct: 8.24, fee_drag_pct: 0.45,
    slippage_pct: -0.25, net_r_multiple: 1.8, exit_reason: 'Trailing stop',
    entry_note: 'Breakout above the 50-day high on volume.', exit_note: 'Trail hit after earnings drift.',
    tags: ['breakout'],
  },
  {
    id: 'trade-st09-loss', ticker: 'VOD.L', market: 'UK', entry_date: '2026-10-05', exit_date: '2026-10-12',
    entry_price: 75, exit_price: 70, shares: 200, pnl: -1000, pnl_pct: -6.67, fee_drag_pct: null,
    slippage_pct: 0.5, net_r_multiple: -1.0, exit_reason: 'Initial stop', entry_note: null, exit_note: null, tags: [],
  },
];

async function mockSt09Populated(page) {
  await mockSt09PopulatedPositions(page);
  await page.route(new RegExp(`${API}/positions(\\?|$)`), (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify(ST09_POSITIONS.map((p, i) => (i === 1 ? { ...p, grace_period: true, grace_end_date: '2026-11-12' } : p))),
    })
  );
  await page.route(new RegExp(`${API}/portfolio(\\?|$)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { portfolio_heat_percent: 18.2, positions: [] } }) })
  );
  await page.route(new RegExp(`${API}/trades(\\?|$)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', total_trades: 2, win_rate: 50, total_pnl: 400, trades: ST09_TRADES }) })
  );
  await page.route(new RegExp(`${API}/signals(\\?|$)`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([{ id: 'sig-1', ticker: 'MSFT', market: 'US', status: 'new' }]) })
  );
  await page.route(/\/analytics\/arc5-compliance/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { validation_pass_rate_by_rule: { stop: 0.9, size: 0.8 } } }) })
  );
  await page.route(/\/portfolio\/red-flag-journal/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { total: 2, items: [] } }) })
  );
  await page.route(/\/digest\/weekly/, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: {
          realised_pnl_7d: 166.1, unrealised_pnl_delta_7d: -42.8, alerts_fired_7d: 5, alerts_dismissed_7d: 3,
          compliance_score_current: 80.0, compliance_score_7d_ago: 75.0, staleness_hours: 18.5,
          as_of_utc: '2026-04-01T10:30:00+00:00',
        },
      }),
    })
  );
}

test.describe('Shell consumers axe scan, populated — light theme (ST-09)', () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await mockRoutes(page);
    await mockSt09Populated(page);
  });

  test('Dashboard with populated cards (light)', async ({ page }) => {
    // v9.18 EPIC-02 ST-09: empty cards now fold (dashboard.md §3A), so Card 1's
    // text sits at the viewport's lower edge at 720 px, where axe reports it
    // undecided (elmPartiallyObscuring, no related node). A viewport that holds
    // the whole page keeps the scan independent of where the fold leaves it.
    await page.setViewportSize({ width: 1280, height: 1600 });
    await page.goto('/#/DashboardHome');
    await expect(page.getByText('Heat elevated — monitor closely')).toBeVisible({ timeout: 10000 });
    await page.waitForLoadState('networkidle');
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'DashboardPopulated:light');
  });

  // Scoped to the trade table (the DataTable shell and its expanded journal
  // row). The rest of the Trade History page (filters panel, AI Journal
  // Summary, saved-filters select, view toggle) is outside the converted
  // shells and was already dark-only in the light theme before ST-09: BLG-FE-285.
  test('Trade History with a journal row expanded (light)', async ({ page }) => {
    await page.goto('/#/TradeHistory');
    await page.getByText('AAPL').first().click();
    await expect(page.getByText('Breakout above the 50-day high on volume.')).toBeVisible({ timeout: 10000 });
    await page.waitForLoadState('networkidle');
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'TradeHistoryExpanded:light', { include: 'table' });
  });

  test('Trade Entry (light)', async ({ page }) => {
    await page.goto('/#/TradeEntry');
    await expect(page.getByPlaceholder('e.g., AAPL or VOD.L')).toBeVisible({ timeout: 10000 });
    await page.getByPlaceholder('e.g., AAPL or VOD.L').fill('AAPL');
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'TradeEntry:light');
  });

  // Review pass 2: the catch-all mock returns no checks, so the scans above
  // never render PreEntryValidationPanel's pass/warn/fail badges. This one
  // does, and scopes the scan to the panel.
  test('Trade Entry pre-entry checks with pass, warn and fail badges (light)', async ({ page }) => {
    await page.route(new RegExp(`${API}/portfolio/pre-entry-validation`), (route) =>
      route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            advisory_status: 'warn',
            checks: [
              { rule: 'regime_gate', status: 'pass', detail: 'UK market is risk-on' },
              { rule: 'cash_constraint', status: 'warn', detail: 'Cash is close to the limit' },
              { rule: 'concentration', status: 'fail', detail: 'Position exceeds the concentration limit' },
            ],
          },
        }),
      })
    );
    await page.goto('/#/TradeEntry');
    await page.getByPlaceholder('e.g., AAPL or VOD.L').fill('LGEN');
    await page.getByPlaceholder('0.00').first().fill('100');
    await page.getByPlaceholder('Fetched automatically if blank').fill('2');
    await page.getByPlaceholder('0', { exact: true }).fill('10');
    const panel = page.getByTestId('pre-entry-checks-panel');
    await expect(panel.getByTestId('pre-entry-check-regime_gate')).toBeVisible({ timeout: 10000 });
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'TradeEntryPreEntry:light', { include: '[data-testid="pre-entry-checks-panel"]' });
  });

  test('Weekly Digest (light)', async ({ page }) => {
    await page.goto('/#/WeeklyDigest');
    await expect(page.getByText('Realised P&L (7d)')).toBeVisible({ timeout: 10000 });
    await expectThemeApplied(page, 'light');
    await runAxeScan(page, 'WeeklyDigest:light');
  });
});

// ---------------------------------------------------------------------------
// EPIC-03 review pass 4 (v9.16) kept three DataState consumers on a card that
// was dark in both themes, using the `dark` class. ST-08 (BLG-FE-265, v9.17)
// themes those cards, so in the light theme the card is white and the
// empty-state heading is slate-900 (17.85:1 on white).
// ---------------------------------------------------------------------------

for (const [page_, route, heading] of [
  ['Trade Plans', '/#/TradePlans', 'No trade plans yet'],
  ['Watchlist', '/#/Watchlist', 'Your watchlist is empty'],
  ['Notifications', '/#/Notifications', 'No notifications yet'],
]) {
  test(`${page_} empty-state heading is dark text on a themed card in the light theme (ST-08)`, async ({ page }) => {
    await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
    await mockRoutes(page);
    await page.route(new RegExp(`${API}/notifications\\?`), (r) =>
      r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { notifications: [], has_more: false } }) })
    );
    await page.goto(route);
    const h = page.getByText(heading, { exact: true });
    await expect(h).toBeVisible({ timeout: 10000 });
    await expectThemeApplied(page, 'light');
    await expect(h).toHaveCSS('color', 'rgb(15, 23, 42)');
    await runAxeScan(page, `${page_.replace(/ /g, '')}Empty:light`);
  });
}

// ---------------------------------------------------------------------------
// ST-08 (BLG-FE-265, EPIC-03, v9.17): every routed page in the light theme.
// AC: "axe color-contrast passes in the light theme on every routed page".
// Pages already scanned whole above (Dashboard, Positions, Trade Plan,
// Settings, Weekly Digest, Trade Entry, Replay, Notification preferences and
// history) are not repeated. Trade History was scanned above only inside its
// table (BLG-FE-285), so the whole page is scanned here in both views. Each
// page is scanned populated, with the payloads in
// fixtures/routed-pages-populated.js (copied from each page's own spec) or
// the ST-09 populated stubs. No baseline entries.
// ---------------------------------------------------------------------------

const routed = require('./fixtures/routed-pages-populated');

// Trade History: ST-09's populated stubs plus the calendar's GET
// /reports/daily-pnl payload from saved-filters-calendar-view.spec.js.
async function mockTradeHistoryPopulated(page) {
  await mockRoutes(page);
  await mockSt09Populated(page);
  await page.route(new RegExp(`${API}/reports/daily-pnl.*`), (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({
        status: 'ok',
        data: [{ day: 3, realised_pnl_gbp: 100, trade_count: 1 }, { day: 17, realised_pnl_gbp: -50, trade_count: 1 }],
        estimated_unrealised_pnl: 340.5,
        unrealised_note: 'Indicative only — not a tax liability.',
      }),
    })
  );
}

const ST08_PAGES = [
  // [name, route, mock, text that proves the data rendered, optional step, optional scan scope]
  ['TradePlans', '/#/TradePlans', routed.mockTradePlans, 'AAA'],
  ['Signals', '/#/Signals', routed.mockSignals, 'VOD'],
  ['Screener', '/#/Screener', routed.mockScreener, 'BARC'],
  // v9.18 ST-08 (BLG-FE-323): Strategy Benchmark is Performance's "Strategy vs
  // backtest" section. Scanned on its own (scoped to the section) so it keeps
  // its strict incomplete-contrast rule; the full Performance scan below
  // covers it again inside the page.
  ['StrategyVsBacktest', '/#/Performance?section=strategy-vs-backtest', routed.mockPerformance, 'TSLA', null, '#strategy-vs-backtest'],
  ['SystemStatus', '/#/SystemStatus', routed.mockSystemStatus, 'GET /signals', async (page) => {
    await page.getByRole('button', { name: /Run Tests/ }).click();
  }],
  ['TickerUniverse', '/#/settings/ticker-universe', routed.mockTickerUniverse, 'British American Tobacco'],
  ['Watchlist', '/#/Watchlist', routed.mockWatchlist, 'VOD.L'],
  ['ResearchLanding', '/#/Research', routed.catchAll, null],
  ['ResearchTicker', '/#/research/AAPL', routed.mockResearch, 'Apple reports record quarterly revenue'],
  ['RiskDashboard', '/#/RiskDashboard', routed.mockRiskDashboard, 'ALPHA'],
  ['TradeHistory', '/#/TradeHistory', mockTradeHistoryPopulated, 'AAPL'],
  // Page states reached by an action (BLG-FE-303): each component only renders
  // once the user does something, so the step drives the page into that state.
  ['TradePlanWhatIfSizing', '/#/TradePlan?ticker=AAPL&market=US', routed.mockWhatIfSizing, null, async (page) => {
    await page.getByTestId('planned-stop-price-input').fill('780.00');
    await expect(page.getByTestId('what-if-sizing-preview-panel')).toBeVisible({ timeout: 10000 });
    await page.getByTestId('what-if-entry-price-input').fill('850.00');
    await expect(page.getByTestId('what-if-suggested-shares')).toHaveText('17.8571 shares', { timeout: 10000 });
    await expect(page.getByText(/approaching 40% concentration limit/)).toBeVisible({ timeout: 10000 });
  }],
  ['TradeEntrySetupThesisDigest', '/#/TradePlans', routed.mockSetupThesisDigest, null, async (page) => {
    await page.getByTestId('start-trade-from-plan-plan-tsd-01').click();
    await expect(page).toHaveURL(/#\/TradeEntry/, { timeout: 10000 });
    await expect(page.getByTestId('setup-thesis-digest-panel')).toBeVisible({ timeout: 10000 });
  }],
  ['SettingsAiSpendTrend', '/#/Settings', routed.mockAiSpendTrend, null, async (page) => {
    const chart = page.getByTestId('ai-spend-trend-chart');
    await expect(chart).toBeVisible({ timeout: 10000 });
    // axe skips SVG <text>, so the axis label colour is asserted: --app-muted is
    // slate-600 in light (7.58:1 on white) and slate-400 in dark.
    const dark = await page.evaluate(() => document.documentElement.classList.contains('dark'));
    await expect(chart.locator('.recharts-cartesian-axis-tick-value').first())
      .toHaveCSS('fill', dark ? 'rgb(148, 163, 184)' : 'rgb(71, 85, 105)');
  }],
  ['CashManagementModal', '/#/Positions', routed.mockCashManagement, null, async (page) => {
    await page.getByTestId('cash-management-trigger-desktop').click();
    await expect(page.getByRole('dialog').getByText('Cash Management')).toBeVisible({ timeout: 10000 });
  }],
  ['DailyMonitorModal', '/#/Positions', routed.mockDailyMonitor, null, async (page) => {
    await page.getByTestId('daily-monitor-button').click();
    await expect(page.getByRole('heading', { name: 'Daily Position Monitor' })).toBeVisible({ timeout: 10000 });
    await expect(page.getByRole('dialog').getByText('RISK.L', { exact: true })).toBeVisible({ timeout: 10000 });
  }],
  ['AdvisorChatError', '/#/Positions', routed.mockAdvisorChatError, null, async (page) => {
    await page.getByTestId('ai-chat-open-btn').click();
    await page.getByTestId('ai-chat-input').fill('What is my portfolio value?');
    await page.getByTestId('ai-chat-submit').click();
    await expect(page.getByTestId('ai-chat-error')).toBeVisible({ timeout: 10000 });
  }],
  ['AdvisorChatOpen', '/#/Positions', routed.mockAdvisorChat, null, async (page) => {
    await page.getByTestId('ai-chat-open-btn').click();
    await expect(page.getByTestId('ai-chat-panel')).toBeVisible({ timeout: 10000 });
    await page.getByTestId('ai-chat-input').fill('How many positions do I have?');
    await page.getByTestId('ai-chat-submit').click();
    await expect(page.getByText('You currently have 0 open positions.')).toBeVisible({ timeout: 10000 });
  }],
  ['TradeHistoryCalendar', '/#/TradeHistory', mockTradeHistoryPopulated, null, async (page) => {
    await expect(page.locator('main').getByText('AAPL').first()).toBeVisible({ timeout: 15000 });
    await page.getByRole('button', { name: 'Calendar' }).click();
    await expect(page.getByText(/Unrealised P&L/)).toBeVisible({ timeout: 10000 });
  }],
  ['JournalReflections', '/#/Journal?section=reflections', routed.mockJournal, 'LGEN'],
  ['JournalRedFlags', '/#/Journal?section=red-flags', routed.mockJournal, null, async (page) => {
    await expect(page.getByTestId('event-type-label')).toHaveCount(2, { timeout: 15000 });
  }],
  ['JournalNotes', '/#/Journal?section=notes', routed.mockJournal, 'NVDA'],
  ['Performance', '/#/Performance', routed.mockPerformance, 'Profit Factor'],
  ['Notifications', '/#/notifications', routed.mockNotifications, 'Stop Loss Approaching: LGEN'],
];

// The dark run guards the sweep's promise that dark values are unchanged.
for (const theme of ['light', 'dark']) {
  test.describe(`Every routed page, populated — ${theme} theme (ST-08)`, () => {
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((t) => {
        window.localStorage.setItem('theme', t);
        // The first-session ⌘K hint (Layout.js) is a toast shown 1.2s after load;
        // a scan that lands while it fades in reads it mid-animation (flaky).
        window.localStorage.setItem('command-palette-tooltip-seen', 'true');
      }, theme);
    });

    for (const [name, route, mock, marker, step, include] of ST08_PAGES) {
      test(`${name} (${theme})`, async ({ page }) => {
        // The two modal states take longer than the 30s default; every other entry keeps it.
        if (name.endsWith('Modal')) test.setTimeout(60000);
        await mock(page);
        await page.goto(route);
        await expect(page.locator('main h1').first()).toBeVisible({ timeout: 15000 });
        if (step) await step(page);
        if (marker) await expect(page.locator('main').getByText(marker, { exact: false }).first()).toBeVisible({ timeout: 15000 });
        await expectThemeApplied(page, theme);
        await runAxeScan(page, `${name}:${theme}`, { include });
      });
    }
  });
}

// ---------------------------------------------------------------------------
// ST-01 (BLG-FE-311, EPIC-01, v9.18): the open states of the four formerly
// mouse-only controls, both themes. AC 2: axe passes with the heatmap detail
// and the Screener popover open, with no `button-name` or `aria-dialog-name`
// violation. The Screener news panel, an expanded Alert History row and the
// open AI Journal Summary are the other conditional states the story touches
// (first-time-right check 4), so they are scanned too. Keyboard behaviour is
// in keyboard-operable-controls.spec.js.
// ---------------------------------------------------------------------------

const { mockAnalyticsMetrics: st01MockAnalyticsMetrics } = require('./fixtures/analytics-metrics');
const { ALL_TRADES: ST01_TRADES, ANALYTICS_SETTINGS: ST01_SETTINGS } = require('./mocks/analytics-mock-data');

async function st01MockHeatmap(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) }));
  await page.route(`${API}/trades`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ST01_TRADES) }));
  await page.route(`${API}/settings`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(ST01_SETTINGS) }));
  await st01MockAnalyticsMetrics(page, { trades: ST01_TRADES });
}

async function st01MockAlertHistory(page) {
  await routed.catchAll(page);
  await page.route(/\/alerts\/history/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(HISTORY) }));
}

async function st01MockTradeHistory(page) {
  await routed.catchAll(page);
  await page.route(/\/trades$/, (route) => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      status: 'ok',
      trades: [{
        id: 'st01-t1', ticker: 'AAPL', market: 'US', entry_date: '2026-03-01', exit_date: '2026-03-15',
        entry_price: 200, exit_price: 220, shares: 10, pnl: 199.5, pnl_pct: 9.95, exit_reason: 'Target Reached', tags: [],
      }],
      total_pnl: 199.5, total_trades: 1, win_rate: 100,
    }),
  }));
}

// [name, route, mock, step that opens the state]
const ST01_STATES = [
  ['HeatmapDetailOpen', '/#/Performance?section=analytics', st01MockHeatmap, async (page) => {
    await expect(page.locator('[class*="animate-spin"]')).toHaveCount(0, { timeout: 20000 });
    await page.locator('button[role="combobox"]').first().click();
    await page.locator('[role="option"]').filter({ hasText: 'All Time' }).click();
    await page.getByRole('button').filter({ hasText: '2026-01' }).click();
    await expect(page.getByRole('dialog', { name: /Trades\s*—\s*Jan 2026/ })).toBeVisible({ timeout: 5000 });
  }],
  ['ScreenerWatchlistPopoverOpen', '/#/Screener', routed.mockScreener, async (page) => {
    await expect(page.locator('main').getByText('BARC').first()).toBeVisible({ timeout: 15000 });
    await page.locator('main').getByRole('button', { name: 'Watchlist', exact: true }).first().click();
    await expect(page.getByRole('button', { name: 'Cancel', exact: true })).toBeVisible();
  }],
  ['ScreenerNewsPanelOpen', '/#/Screener', routed.mockScreener, async (page) => {
    await expect(page.locator('main').getByText('BARC').first()).toBeVisible({ timeout: 15000 });
    await page.locator('main').getByTitle('Show news headlines').first().click();
    await expect(page.getByRole('button', { name: /^Close news for / })).toBeVisible();
  }],
  ['AlertHistoryRowExpanded', '/#/notifications/history', st01MockAlertHistory, async (page) => {
    await page.getByTestId('alert-history-expand').first().click();
    await expect(page.locator('#alert-history-detail-eval-1')).toBeVisible({ timeout: 10000 });
  }],
  ['AiJournalSummaryOpen', '/#/TradeHistory', st01MockTradeHistory, async (page) => {
    await page.getByTestId('ai-journal-summary-toggle').click();
    await expect(page.locator('#ai-journal-summary-panel')).toBeVisible({ timeout: 10000 });
  }],
];

for (const theme of ['light', 'dark']) {
  test.describe(`Keyboard-operable controls, open states — ${theme} theme (ST-01)`, () => {
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((t) => {
        window.localStorage.setItem('theme', t);
        window.localStorage.setItem('command-palette-tooltip-seen', 'true');
      }, theme);
    });

    for (const [name, route, mock, step] of ST01_STATES) {
      test(`${name} (${theme})`, async ({ page }) => {
        test.setTimeout(60000);
        await mock(page);
        await page.goto(route);
        await step(page);
        await expectThemeApplied(page, theme);
        const results = await runAxeScan(page, `${name}:${theme}`);
        // AC 2 names these two rules; neither may appear at any impact.
        const named = results.violations.filter((v) => v.id === 'button-name' || v.id === 'aria-dialog-name');
        expect(named.map((v) => v.id)).toEqual([]);
      });
    }
  });
}

// ---------------------------------------------------------------------------
// ST-02 (BLG-FE-312, EPIC-01, v9.18): the open Exit dialog, light and dark.
// AC 1: each visible label resolves to its input with getByLabel. AC 2: axe
// passes on the open dialog with no `label` violation at any impact. A US
// position is used so the US-only FX rate field is also present.
// ---------------------------------------------------------------------------

for (const theme of ['light', 'dark']) {
  test(`Exit dialog open, labels linked to inputs (${theme}) (ST-02)`, async ({ page }) => {
    test.setTimeout(60000);
    await page.addInitScript((t) => {
      window.localStorage.setItem('theme', t);
      window.localStorage.setItem('command-palette-tooltip-seen', 'true');
    }, theme);
    await mockRoutes(page);
    await mockSt09PopulatedPositions(page);
    await page.goto('/#/positions');
    const tableBtn = page.locator('[aria-label="Table view"]');
    await tableBtn.waitFor({ state: 'visible', timeout: 10000 });
    await tableBtn.click();
    await page.getByRole('button', { name: 'Exit WDC' }).click();
    const dialog = page.getByRole('dialog', { name: 'Exit Position' });
    await expect(dialog).toBeVisible({ timeout: 5000 });

    // Every visible label: its `for` points at a control, and getByLabel with
    // the exact label text resolves to that one control.
    for (const label of [
      'Shares to Exit',
      /^Exit Price \(\$\)$/,
      'Exit Date',
      'FX rate — USD per £1 (GBP/USD)',
      'Exit Reason',
      'Exit Note (Optional)',
    ]) {
      const labelEl = dialog.locator('label').filter({ hasText: label });
      await expect(labelEl).toHaveCount(1);
      const forId = await labelEl.getAttribute('for');
      expect(forId).toBeTruthy();
      const field = dialog.getByLabel(label, { exact: true });
      await expect(field).toHaveCount(1);
      await expect(field).toHaveAttribute('id', forId);
    }
    // The Exit Reason select's accessible name comes from its visible label.
    await expect(dialog.getByRole('combobox', { name: 'Exit Reason', exact: true })).toHaveCount(1);
    // Typing through a label reaches its input.
    await dialog.getByLabel('Exit Note (Optional)', { exact: true }).fill('Target reached');
    await expect(dialog.getByRole('textbox', { name: 'Exit Note (Optional)' })).toHaveValue('Target reached');

    await expectThemeApplied(page, theme);
    const results = await runAxeScan(page, `ExitDialogOpen:${theme}`);
    expect(results.violations.filter((v) => v.id === 'label').map((v) => v.id)).toEqual([]);
  });
}

// ---------------------------------------------------------------------------
// ST-03 (BLG-FE-318, EPIC-01, v9.18): the Feed with the new "Not sent" line
// (both texts) and Notification Preferences with its new "Telegram Alerts"
// heading, light and dark. Preferences is already scanned by the ST-19 block;
// the Feed state with the delivery line is new.
// ---------------------------------------------------------------------------

for (const theme of ['light', 'dark']) {
  test(`Notifications feed with Not sent lines (${theme}) (ST-03)`, async ({ page }) => {
    await page.addInitScript((t) => {
      window.localStorage.setItem('theme', t);
      window.localStorage.setItem('command-palette-tooltip-seen', 'true');
    }, theme);
    await routed.catchAll(page);
    const feed = [
      ['n-1', 'Stop Loss Approach — AAA', 'not_sent', 'telegram_not_configured'],
      ['n-2', 'Stop Loss Approach — BBB', 'not_sent', 'delivery_failed'],
      ['n-3', 'Stop Loss Approach — CCC', 'sent', null],
    ].map(([id, title, delivery_status, delivery_reason]) => ({
      id, alert_type: 'stop_loss_approach', title, message: `${title} message`, read: false,
      created_at: new Date(Date.now() - 3600 * 1000).toISOString(), context: null, delivery_status, delivery_reason,
    }));
    await page.route(/localhost:8000\/notifications\?/, (route) => route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: { notifications: feed, total: 3, page: 1, per_page: 50, has_more: false } }),
    }));
    await page.goto('/#/notifications');
    await expect(page.getByTestId('notification-not-sent')).toHaveCount(2, { timeout: 10000 });
    await expectThemeApplied(page, theme);
    await runAxeScan(page, `NotificationsNotSent:${theme}`);
  });
}

// ST-20 (BLG-QA-260, EPIC-04, v9.18): the incomplete color-contrast rule itself.
// A probe paragraph on a gradient, inside <main>, is a contrast axe cannot
// decide, so it comes back as `incomplete` page content. ResearchLanding:dark
// is in STRICT_INCOMPLETE_CONTRAST and has no such node of its own.
test.describe('axe incomplete color-contrast (ST-20)', () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem('theme', 'dark');
      window.localStorage.setItem('command-palette-tooltip-seen', 'true');
    });
    await routed.catchAll(page);
    await page.goto('/#/Research');
    await expect(page.locator('main h1').first()).toBeVisible({ timeout: 15000 });
    await expectThemeApplied(page, 'dark');
    await page.evaluate(() => {
      const probe = document.createElement('p');
      probe.id = 'axe-incomplete-probe';
      probe.textContent = 'Contrast probe on a gradient';
      probe.style.backgroundImage = 'linear-gradient(90deg, #ffffff, #000000)';
      probe.style.color = '#777777';
      document.querySelector('main').appendChild(probe);
    });
  });

  test('SC-AXEINC-01: a scan logs its incomplete color-contrast nodes', async ({ page }) => {
    const lines = [];
    const log = console.log;
    console.log = (...args) => { lines.push(args.join(' ')); log(...args); };
    try {
      // A name outside the strict set: logged, not failed.
      await runAxeScan(page, 'ResearchLandingProbe:dark');
    } finally {
      console.log = log;
    }
    const output = lines.join('\n');
    expect(output).toMatch(/ResearchLandingProbe:dark: \d+ incomplete color-contrast node\(s\).*\(1 page content, \d+ app shell\)/);
    expect(output).toContain('#axe-incomplete-probe');
  });

  test('SC-AXEINC-02: a strict-set scan fails on an incomplete color-contrast node', async ({ page }) => {
    expect(STRICT_INCOMPLETE_CONTRAST.has('ResearchLanding:dark')).toBe(true);
    await expect(runAxeScan(page, 'ResearchLanding:dark')).rejects.toThrow(/1 incomplete color-contrast node\(s\) in page content on a STRICT_INCOMPLETE_CONTRAST page[\s\S]*#axe-incomplete-probe/);
  });
});
