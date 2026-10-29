/**
 * v9.13 ST-03 (BLG-FE-227, EPIC-01) — one shared exit-reason module.
 *
 * Design source: docs/design/2026-10-16__release-v9.13/exit-reason-badges/decision_record.md §6
 * Spec: trade_history.md §Exit Reason Labels and Badges; reflections.md §5.2; trade_reflection.md §4
 *
 *   SC-ERB-01  Module: every legacy alias resolves to a stored value; every stored value has exactly
 *              one §8 category (data_model.md §3, ST-02); unknown values show as stored, null as "—"
 *   SC-ERB-02  Trade Reflections cards, dark theme: each of the six stored values (and a legacy key)
 *              shows its short label and its family's dark badge colour (AC 2, AC 4)
 *   SC-ERB-03  Same in the light theme, with the light badge tokens (AC 4)
 *   SC-ERB-04  Light-theme axe scan of the Trade Reflections badges: no color-contrast violation
 *   SC-ERB-05  The Trade Reflection modal's Exit Reason row shows the full label, legacy keys resolved (AC 2)
 *   SC-ERB-06  Trade History rows use the same short labels and badge colours (AC 3)
 *
 * Infrastructure: page.route() network interception — no live backend required.
 * Theme: Layout.js reads localStorage["theme"] (default "dark") on mount.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/PageKey').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');
const AxeBuilder = require('@axe-core/playwright').default;
const {
  EXIT_REASONS, EXIT_REASON_VALUES, EXIT_REASON_ALIASES,
  SECTION_8_STOP_LOSS, SECTION_8_RISK_OFF, SECTION_8_MANUAL,
  resolveExitReason, exitReasonLabel, exitReasonShortLabel, exitReasonCategory,
} = require('../../src/constants/exitReasons.js');

const API = 'http://localhost:8000';

// Tailwind 3 palette: {family}-100 (light) and {family}-500 at 20% (dark).
const BADGE_BG = {
  rose: { light: 'rgb(255, 228, 230)', dark: 'rgba(244, 63, 94, 0.2)' },
  cyan: { light: 'rgb(207, 250, 254)', dark: 'rgba(6, 182, 212, 0.2)' },
  amber: { light: 'rgb(254, 243, 199)', dark: 'rgba(245, 158, 11, 0.2)' },
  violet: { light: 'rgb(237, 233, 254)', dark: 'rgba(139, 92, 246, 0.2)' },
  emerald: { light: 'rgb(209, 250, 229)', dark: 'rgba(16, 185, 129, 0.2)' },
  blue: { light: 'rgb(219, 234, 254)', dark: 'rgba(59, 130, 246, 0.2)' },
};

// One trade per stored value, plus a legacy key (stop_hit → Stop Loss Hit).
const CASES = [
  ...EXIT_REASON_VALUES.map((value, i) => ({ ticker: `T${i}`, stored: value, expect: value })),
  { ticker: 'LEGACY', stored: 'stop_hit', expect: 'Stop Loss Hit' },
];

function makeTrade({ ticker, stored }, i) {
  return {
    id: `trade-${i}`, ticker, market: 'US', entry_date: '2026-09-01', exit_date: '2026-09-20',
    entry_price: 100, exit_price: 110, shares: 10, pnl: 100, pnl_pct: 10, pnl_percent: 10,
    holding_days: 19, exit_reason: stored, net_r_multiple: 1.2,
  };
}

async function stubTrades(page) {
  const trades = CASES.map(makeTrade);
  await page.route(new RegExp(`${API}/`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(new RegExp(`${API}/trades(\\?.*)?$`), (r) =>
    r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ trades, avg_fee_drag_pct: null }) })
  );
}

async function openReflections(page, theme) {
  if (theme === 'light') await page.addInitScript(() => window.localStorage.setItem('theme', 'light'));
  await stubTrades(page);
  await page.goto('/#/TradeReflection');
  await expect(page.getByTestId('exit-reason-badge')).toHaveCount(CASES.length, { timeout: 10000 });
}

function cardFor(page, ticker) {
  return page.getByRole('button').filter({ has: page.getByText(ticker, { exact: true }) });
}

test.describe('Shared exit-reason module (ST-03)', () => {
  test('SC-ERB-01: aliases resolve, each stored value has one §8 category, unknown and null fall back', () => {
    expect(EXIT_REASON_VALUES).toHaveLength(6);
    for (const [alias, value] of Object.entries(EXIT_REASON_ALIASES)) {
      expect(EXIT_REASON_VALUES).toContain(value);
      expect(resolveExitReason(alias)).toBe(value);
    }
    const categories = new Set([SECTION_8_STOP_LOSS, SECTION_8_RISK_OFF, SECTION_8_MANUAL]);
    for (const value of EXIT_REASON_VALUES) {
      expect(categories.has(exitReasonCategory(value))).toBe(true);
    }
    // Matches data_model.md §3 Exit Reason Values (ST-02).
    expect(EXIT_REASON_VALUES.filter((v) => exitReasonCategory(v) === SECTION_8_STOP_LOSS).sort())
      .toEqual(['Stop Loss Hit', 'Trailing Stop']);
    expect(EXIT_REASON_VALUES.filter((v) => exitReasonCategory(v) === SECTION_8_RISK_OFF)).toEqual(['Risk-Off Signal']);
    expect(exitReasonCategory(null)).toBe(SECTION_8_MANUAL);
    expect(exitReasonLabel('Rebalance')).toBe('Rebalance');
    expect(exitReasonShortLabel('Rebalance')).toBe('Rebalance');
    expect(exitReasonLabel(null)).toBe('—');
    expect(exitReasonShortLabel(undefined)).toBe('—');
  });

  for (const theme of ['dark', 'light']) {
    test(`SC-ERB-0${theme === 'dark' ? 2 : 3}: Trade Reflections badges show each short label and ${theme} colour`, async ({ page }) => {
      await openReflections(page, theme);
      for (const c of CASES) {
        const badge = cardFor(page, c.ticker).getByTestId('exit-reason-badge');
        const entry = EXIT_REASONS[c.expect];
        await expect(badge).toHaveText(entry.short);
        await expect(badge).toHaveCSS('background-color', BADGE_BG[entry.colour][theme]);
      }
    });
  }

  test('SC-ERB-04: light-theme axe scan finds no color-contrast violation on the badges', async ({ page }) => {
    await openReflections(page, 'light');
    const results = await new AxeBuilder({ page })
      .include('[data-testid="exit-reason-badge"]')
      .withRules(['color-contrast'])
      .analyze();
    expect(results.violations).toEqual([]);
  });

  test('SC-ERB-05: the Trade Reflection modal shows the full label, legacy keys resolved', async ({ page }) => {
    await openReflections(page, 'dark');
    for (const [ticker, label] of [['LEGACY', 'Stop Loss Hit'], [`T${EXIT_REASON_VALUES.indexOf('Partial Profit Taking')}`, 'Partial Profit Taking']]) {
      await cardFor(page, ticker).click();
      const dialog = page.getByRole('dialog');
      await expect(dialog).toBeVisible();
      await expect(dialog.getByText('Exit Reason', { exact: true }).locator('..')).toContainText(label);
      await page.keyboard.press('Escape');
      await expect(dialog).toHaveCount(0);
    }
  });

  test('SC-ERB-06: Trade History rows use the same short labels and badge colours', async ({ page }) => {
    await stubTrades(page);
    await page.goto('/#/TradeHistory');
    const badges = page.getByTestId('exit-reason-badge');
    await expect(badges).toHaveCount(CASES.length, { timeout: 10000 });
    for (const c of CASES) {
      const entry = EXIT_REASONS[c.expect];
      const badge = page.getByRole('row').filter({ has: page.getByText(c.ticker, { exact: true }) }).getByTestId('exit-reason-badge');
      await expect(badge).toHaveText(entry.short);
      await expect(badge).toHaveCSS('background-color', BADGE_BG[entry.colour].dark);
    }
  });
});
