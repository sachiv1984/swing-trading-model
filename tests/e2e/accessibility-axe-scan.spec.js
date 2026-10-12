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
  // Switches) were fixed in the same story. The light-theme color-contrast findings are BLG-FE-200: the pages
  // use dark-only classes and design_system.md defines no light-mode tokens,
  // so they could not be fixed in-story. Remove those entries when
  // BLG-FE-200 closes. The dark theme has no baseline entries.
  'ReportsMonthly:dark': new Set([]),
  'ReportsTaxYear:dark': new Set([]),
  'NotificationPreferences:dark': new Set([]),
  'NotificationsHistory:dark': new Set([]),
  'ReportsMonthly:light': new Set(['color-contrast']), // BLG-FE-200
  // ST-37 (BLG-QA-196, EPIC-06, v9.11): Replay page, both selector modes and a populated
  // result, in both themes. The dark theme has no baseline entries (its one finding, the
  // Risk-Off badge's contrast, was fixed in the same story). The light-theme color-contrast
  // findings are the same dark-only-classes gap as BLG-FE-200, filed for Replay as
  // BLG-FE-209; remove these entries when it closes.
  'ReplayDateRange:dark': new Set([]),
  'ReplayTradeSet:dark': new Set([]),
  'ReplayResult:dark': new Set([]),
  'ReplayDateRange:light': new Set(['color-contrast']), // BLG-FE-209
  'ReplayTradeSet:light': new Set(['color-contrast']), // BLG-FE-209
  'ReplayResult:light': new Set(['color-contrast']), // BLG-FE-209
  'ReportsTaxYear:light': new Set(['color-contrast']), // BLG-FE-200
  'NotificationPreferences:light': new Set(['color-contrast']), // BLG-FE-200
  'NotificationsHistory:light': new Set(['color-contrast']), // BLG-FE-200
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

async function runAxeScan(page, pageName) {
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
          summary: { total_realised_pnl: 115, total_gross_profit: 175, total_gross_loss: -60, win_rate: 50, total_closed_trades: 7, restated_month_count: 1 },
          trades: [], estimated_unrealised_pnl: 0, unrealised_note: null,
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

for (const theme of ['dark', 'light']) {
  test.describe(`Reports and Notifications axe scan — ${theme} theme (ST-19)`, () => {
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await mockRoutes(page);
      await mockSt19Routes(page);
    });

    test(`Reports Monthly tab with a restated month expanded (${theme})`, async ({ page }) => {
      await page.goto('/#/Reports');
      await page.getByRole('button', { name: /monthly p&l/i }).click();
      const marker = page.getByTestId('monthly-restated-marker');
      await expect(marker).toBeVisible({ timeout: 10000 });
      await marker.click();
      await expect(page.getByTestId('monthly-restatement-detail')).toBeVisible();
      // Confirm the theme actually applied, so a light run is not a second dark run.
      if (theme === 'dark') {
        await expect(page.locator('html')).toHaveClass(/\bdark\b/);
      } else {
        await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);
      }
      await runAxeScan(page, `ReportsMonthly:${theme}`);
    });

    test(`Reports Tax Year tab with the restated-months notice (${theme})`, async ({ page }) => {
      await page.goto('/#/Reports');
      await page.getByRole('button', { name: /tax year p&l/i }).click();
      await expect(page.getByTestId('taxyear-restated-notice')).toBeVisible({ timeout: 10000 });
      await runAxeScan(page, `ReportsTaxYear:${theme}`);
    });

    test(`Notification preferences (${theme})`, async ({ page }) => {
      await page.goto('/#/notifications/preferences');
      await expect(page.getByText('Stop Loss Approach').first()).toBeVisible({ timeout: 10000 });
      await runAxeScan(page, `NotificationPreferences:${theme}`);
    });

    test(`Notification history (${theme})`, async ({ page }) => {
      await page.goto('/#/notifications/history');
      await page.waitForLoadState('networkidle');
      await expect(page.getByText('AAPL').first()).toBeVisible({ timeout: 10000 });
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
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await mockRoutes(page);
      await mockReplayRoutes(page);
      await page.goto('/#/Replay');
      await expect(page.getByRole('heading', { name: 'Replay Mode' })).toBeVisible({ timeout: 10000 });
      if (theme === 'dark') {
        await expect(page.locator('html')).toHaveClass(/\bdark\b/);
      } else {
        await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);
      }
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

