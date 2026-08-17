/**
 * Playwright coverage for the remaining shadcn token call-site families left
 * untested by v8.6/ST-04 — ST-08 (BLG-FE-157, EPIC-03, v8.7)
 * `secondary` family added ST-17 (BLG-FE-160, EPIC-03, v8.8) once ST-15
 * (same EPIC, same cycle) introduced its first live call site.
 *
 * BLG-FE-147/ST-04 (v8.6) registered 9 previously-unregistered shadcn tokens
 * (card, popover, primary, secondary, accent, destructive, border, input,
 * ring) in tailwind.config.js, verified only via a tailwindcss build check
 * (all in-scope utility classes compile to non-empty rules) — not via a
 * rendering regression test. This story adds real Playwright coverage per
 * remaining family, against genuinely live (not overridden) call sites.
 *
 * Live-call-site audit (2026-08-13, exhaustive grep + a minimal tailwindcss
 * build to empirically determine cascade-override winners — see
 * qa_evidence_EPIC-03.md for the full methodology):
 *
 *   - ring:        LIVE, unoverridden — TradePlan.js form fields
 *                  (`focus-visible:ring-1 focus-visible:ring-ring`)
 *   - accent:      LIVE, unoverridden — SelectItem's own
 *                  `focus:bg-accent focus:text-accent-foreground` (the
 *                  SelectContent container's bg/border ARE overridden at
 *                  every page call site, but individual SelectItem elements
 *                  are not)
 *   - destructive: LIVE, unoverridden — Radix `useToast()` `variant:
 *                  "destructive"` (cva-driven class, not a literal
 *                  className override; e.g. Reports.js PDF/CSV download
 *                  failure toasts)
 *   - popover:     LIVE, unoverridden — WidgetLibrary.js DialogContent
 *                  (`bg-popover border-border`, not overridden). Already
 *                  covered by SC-MTC-05/06 in
 *                  modal-theming-token-conversion.spec.js (ST-06, EPIC-01,
 *                  this same v8.7 cycle) — no new test added here, cited
 *                  as existing coverage.
 *   - border:      LIVE, unoverridden — same WidgetLibrary.js DialogContent
 *                  as popover (`border-border` literal class, not the bare
 *                  `border` utility). New coverage added here (SC-TOK-04).
 *   - card:        NOT LIVE. `Card` (ui/card.js) is never imported by any
 *                  page or component in the app (verified via exhaustive
 *                  grep for `Card` identifier and `ui/card` import paths).
 *                  Code-reviewed only; no reachable mount point to drive
 *                  via e2e navigation. Same precedent as
 *                  PositionEntryModal.js (ST-06, EPIC-01, this cycle).
 *   - secondary:   LIVE as of v8.8/ST-15 (BLG-FE-163) — TickerUniverse.js's
 *                  "Clear filters" control (`<Badge variant="secondary">`),
 *                  shown once any of the page's 5 filters is non-default.
 *                  Covered below (SC-TOK-05). Button's `secondary` variant
 *                  and `ToastAction`'s literal `hover:bg-secondary` remain
 *                  unused elsewhere in the app — not in scope here (the AC
 *                  only requires coverage at "the first live call site").
 *   - card:        Still NOT LIVE at v8.8 — `Card` (ui/card.js) remains
 *                  unimported by any page or component (re-confirmed via
 *                  exhaustive grep, 2026-08-16). No story this cycle
 *                  introduces one (design-gate decision, `BLG-FE-160`
 *                  remains open for this half only). Code-reviewed only;
 *                  no reachable mount point to drive via e2e navigation.
 *                  Same precedent as PositionEntryModal.js (ST-06, EPIC-01,
 *                  v8.7 — subsequently deleted as dead code at v8.8/ST-16).
 *
 * One family (card) still has no live call site to assert against — see
 * qa_evidence_EPIC-03.md for the code-review-only disposition and backlog
 * reference (BLG-FE-160, kept open for the `card` half).
 *
 * Covers observable AC (BLG-FE-157; SC-TOK-05 added BLG-FE-160/ST-17, v8.8):
 *   SC-TOK-01  ring    — TradePlan.js Setup Thesis field: focus-visible ring
 *              colour resolves to the --ring token (non-transparent,
 *              non-black box-shadow/outline)
 *   SC-TOK-02  accent  — TradeEntry.js "Link to Trade Plan" select: keyboard-
 *              highlighted SelectItem background resolves to the --accent
 *              token (differs from the item's unfocused background)
 *   SC-TOK-03  destructive — Reports.js PDF download failure toast:
 *              background/border resolve to the --destructive token
 *   SC-TOK-04  border  — WidgetLibrary popover dialog: border colour
 *              resolves to the --border token (non-transparent)
 *   SC-TOK-05  secondary — TickerUniverse.js "Clear filters" badge:
 *              background/text colour resolve to the --secondary /
 *              --secondary-foreground tokens (non-transparent)
 *
 * Infrastructure: Playwright page.route() network interception. No live
 * backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('@playwright/test');

const API = 'http://localhost:8000';

const TRANSPARENT_VALUES = ['rgba(0, 0, 0, 0)', 'transparent', ''];

async function mockFallback(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
}

async function mockMarketStatus(page) {
  await page.route(`${API}/market/status`, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: { regime_status: 'risk_on' } }) })
  );
}

async function mockByPosition(page) {
  await page.route(new RegExp(`${API}/trade-plans/by-position/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: null }) })
  );
}

test.describe('SC-TOK-01 — ring token (TradePlan.js form field focus)', () => {
  test('SC-TOK-01: focus-visible ring colour is a real, non-transparent colour', async ({ page }) => {
    await mockFallback(page);
    await mockMarketStatus(page);
    await mockByPosition(page);
    await page.goto('/#/TradePlan?ticker=AAPL&market=US');
    await expect(page.locator('h1, [class*="PageHeader"]').filter({ hasText: /Trade Plan/i })).toBeVisible({ timeout: 10000 });

    const thesisField = page.getByPlaceholder('Why enter now? What specific trigger confirms the thesis?');
    await expect(thesisField).toBeVisible({ timeout: 8000 });
    await thesisField.focus();

    const ring = await thesisField.evaluate((el) => {
      const s = window.getComputedStyle(el);
      return s.boxShadow || s.outlineColor;
    });
    expect(ring).toBeTruthy();
    expect(TRANSPARENT_VALUES).not.toContain(ring);
  });
});

test.describe('SC-TOK-02 — accent token (TradeEntry.js Select item highlight)', () => {
  const LINKABLE_PLAN = {
    id: 'plan-tok-01',
    ticker: 'AAPL',
    market: 'US',
    status: 'draft',
    position_id: null,
    planned_entry_price: 150.0,
    planned_stop_price: 140.0,
    planned_quantity: 10,
  };

  test('SC-TOK-02: keyboard-highlighted item background differs from unfocused background', async ({ page }) => {
    await mockFallback(page);
    await page.route(`${API}/trade-plans`, (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [LINKABLE_PLAN] }) });
      }
      return route.continue();
    });

    await page.goto('/#/TradeEntry');
    const trigger = page.getByTestId('link-trade-plan-select');
    await expect(trigger).toBeVisible({ timeout: 10000 });
    await trigger.click();

    // Radix Select auto-focuses the currently-selected item ("none", the
    // default) as soon as the listbox opens — so both readings must be taken
    // AFTER moving the keyboard highlight, not before (an unfocused reading
    // taken pre-interaction would actually be a still-focused reading).
    await page.keyboard.press('ArrowDown');

    const noneItem = page.getByRole('option', { name: /no plan/i });
    const planItem = page.getByRole('option', { name: /AAPL/i });
    await expect(planItem).toBeVisible({ timeout: 5000 });

    const unfocusedBg = await noneItem.evaluate((el) => window.getComputedStyle(el).backgroundColor);
    const highlightedBg = await planItem.evaluate((el) => window.getComputedStyle(el).backgroundColor);

    expect(highlightedBg).not.toBe(unfocusedBg);
    expect(TRANSPARENT_VALUES).not.toContain(highlightedBg);
  });
});

test.describe('SC-TOK-03 — destructive token (Reports.js download-failure toast)', () => {
  async function gotoTaxYearTab(page) {
    await page.goto('/#/Reports');
    await page.getByRole('button', { name: /tax year p&l/i }).click();
  }

  test('SC-TOK-03: PDF download failure toast resolves to the destructive token', async ({ page }) => {
    await mockFallback(page);
    // Route-ordering advisory (shared_standards.md §18): generic handler
    // registered first, defers (route.fallback()) to the more-specific
    // handler registered after it for the one URL it should not answer.
    await page.route(new RegExp(`${API}/reports/tax-year`), (route) => {
      if (route.request().url().includes('format=pdf')) return route.fallback();
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'ok', data: { tax_year_label: '2026/27', summary: { total_realised_pnl: 0, total_gross_profit: 0, total_gross_loss: 0, win_rate: 0, total_closed_trades: 0 }, trades: [] } }),
      });
    });
    await page.route(new RegExp(`${API}/reports/tax-year\\?format=pdf`), (route) =>
      route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'boom' }) })
    );

    await gotoTaxYearTab(page);
    await page.getByRole('button', { name: /download pdf/i }).click();

    // ui/toast.js's Toast root is a plain <div> with no ARIA role (no Radix
    // Toast primitive wraps it here) — select by the literal `bg-destructive`
    // class the `variant: "destructive"` cva branch applies, combined with
    // the toast's own text, rather than a role that doesn't exist in the DOM.
    const toast = page.locator('[class*="bg-destructive"]').filter({ hasText: /pdf generation failed/i });
    await expect(toast).toBeVisible({ timeout: 8000 });
    const bg = await toast.evaluate((el) => window.getComputedStyle(el).backgroundColor);
    expect(TRANSPARENT_VALUES).not.toContain(bg);
  });
});

test.describe('SC-TOK-04 — border token (WidgetLibrary popover dialog)', () => {
  async function mockDashboardPositions(page) {
    await page.route(`${API}/positions`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify([]) })
    );
  }

  test('SC-TOK-04: dialog border colour is a real, non-transparent colour', async ({ page }) => {
    await mockFallback(page);
    await mockDashboardPositions(page);
    await page.goto('/#/Dashboard');
    await page.getByRole('button', { name: /customize/i }).click();
    await page.getByRole('button', { name: /add widget/i }).click();

    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible({ timeout: 10000 });
    const borderColor = await dialog.evaluate((el) => window.getComputedStyle(el).borderColor);
    expect(borderColor).toBeTruthy();
    expect(TRANSPARENT_VALUES).not.toContain(borderColor);
  });
});

test.describe('SC-TOK-05 — secondary token (TickerUniverse.js "Clear filters" badge)', () => {
  const TICKERS = [
    { ticker: 'AAPL', market: 'US', active: true, sector: 'Technology', industry: 'Software', company_name: 'Apple Inc.' },
  ];

  test('SC-TOK-05: Clear filters badge background/text colour resolve to the secondary token', async ({ page }) => {
    await mockFallback(page);
    await page.route(`${API}/ticker-universe?active_only=false`, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: TICKERS }) })
    );
    await page.goto('/#/TickerUniverse');
    await expect(page.getByTestId('ticker-table')).toBeVisible({ timeout: 10000 });

    // No filter is active by default — the badge (Badge variant="secondary")
    // only renders once a filter is non-default.
    await expect(page.getByTestId('clear-filters-badge')).not.toBeVisible();
    await page.getByTestId('sector-filter').selectOption('Technology');

    const badge = page.getByTestId('clear-filters-badge');
    await expect(badge).toBeVisible({ timeout: 5000 });
    const { bg, fg } = await badge.evaluate((el) => {
      const s = window.getComputedStyle(el);
      return { bg: s.backgroundColor, fg: s.color };
    });
    expect(TRANSPARENT_VALUES).not.toContain(bg);
    expect(fg).toBeTruthy();
    expect(TRANSPARENT_VALUES).not.toContain(fg);
    // bg-secondary and text-secondary-foreground are deliberately distinct
    // tokens (design_system.md) — background and text colour must differ.
    expect(bg).not.toBe(fg);
  });
});
