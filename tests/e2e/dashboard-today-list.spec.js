/**
 * Dashboard "Today" list — ST-06 (BLG-FE-254, EPIC-02, v9.16)
 *
 * Spec: docs/specs/frontend/pages/dashboard.md v4.0 §1B (TL-01..TL-29)
 * Design brief: docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md §2.2
 *
 * Every scenario runs in the dark and the light theme. TL-09 and TL-10 (Stops moved) were added by
 * ST-10 (BLG-FE-254, EPIC-04, v9.17) once ST-09 (BLG-BE-205) put stop_last_moved_date and
 * previous_stop on GET /positions: SC-TL-09, SC-TL-09b and SC-TL-10. SC-TL-STOPS asserts the
 * group does not render, with no placeholder, while no position has those fields (TL-13).
 * TL-20 is the CI copy check scripts/check_ui_copy_forbidden_phrases.py, not a Playwright scenario.
 *
 * Infrastructure: page.route() network interception, clock fixed at NOW. No live backend.
 * ROUTING NOTE: App uses HashRouter — navigate via page.goto('/#/…').
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const API = 'http://localhost:8000';
const NOW = new Date('2026-11-09T12:00:00');
const TODAY = '2026-11-09';
const YESTERDAY = '2026-11-08';
// NOW is a Monday: the Stops moved window is today and the previous weekday, Friday (DEV-EPIC04-ST10-01).
const PREV_WEEKDAY = '2026-11-06';
const US_EXPLANATION =
  'US market regime could not be measured: index data is unavailable. New entries in this market are blocked until it is measured.';

const MARKET_ON = {
  status: 'ok',
  data: {
    spy: { price: 500, ma200: 480, is_risk_on: true, regime_status: 'risk_on' },
    ftse: { price: 7800, ma200: 7600, is_risk_on: true, regime_status: 'risk_on' },
    fx_rate: 1.27,
  },
};
const MARKET_US_UNKNOWN = {
  status: 'ok',
  data: {
    spy: { price: null, ma200: null, is_risk_on: null, regime_status: 'unknown' },
    ftse: { price: 7800, ma200: 7600, is_risk_on: false, regime_status: 'risk_off' },
    fx_rate: 1.27,
  },
};

function pos(overrides = {}) {
  return {
    id: `pos-${overrides.ticker || 'ORD'}`, ticker: 'ORD', market: 'US', status: 'open',
    entry_price: 100, current_price: 110, current_price_native: 110,
    current_trailing_stop: 90, current_trailing_stop_native: 90,
    stop_price: 90, stop_price_native: 90, shares: 10, fx_rate: 1, live_fx_rate: 1,
    holding_days: 20, grace_period: false, grace_days_remaining: null,
    risk_off_exit: false, entry_date: '2026-09-01', pnl: 100, pnl_percent: 10,
    position_state: 'PROFITABLE', days_in_state: 3,
    ...overrides,
  };
}
const riskOff = (ticker) => pos({ ticker, risk_off_exit: true });
const breached = (ticker) => pos({ ticker, current_price: 85, current_price_native: 85 });
const inGraceBreached = (ticker) => pos({ ticker, current_price: 85, current_price_native: 85, grace_period: true, grace_days_remaining: 4 });
const moved = (ticker, date, previous, current, market = 'US') => pos({
  ticker, market, stop_last_moved_date: date, previous_stop: previous,
  current_trailing_stop_native: current, stop_price_native: current,
});
const graceLeft = (ticker, n) => pos({ ticker, grace_period: n != null, grace_days_remaining: n });
const signal = (ticker, overrides = {}) => ({
  id: `sig-${ticker}`, ticker, market: 'US', status: 'new', signal_date: TODAY, rank: 1, ...overrides,
});

const json = (body, status = 200) => ({ status, contentType: 'application/json', body: JSON.stringify(body) });

/**
 * Mocks the three Today-list sources. Each source is { body } or { fail: true }, optionally
 * with delayMs. Returns live request counters per source.
 */
async function mockSources(page, { market = { body: MARKET_ON }, positions = { body: [] }, signals = { body: [] } } = {}) {
  const counts = { market: 0, positions: 0, signals: 0 };
  await page.route(new RegExp(`${API}/`), (r) => r.fulfill(json({ status: 'ok', data: [] })));
  const handler = (name, src) => async (route) => {
    counts[name] += 1;
    if (src.delayMs) await new Promise((res) => setTimeout(res, src.delayMs));
    if (src.fail) return route.fulfill(json({ status: 'error', message: 'boom' }, 500));
    return route.fulfill(json(src.body));
  };
  await page.route(`${API}/market/status`, handler('market', market));
  await page.route(`${API}/positions`, handler('positions', positions));
  await page.route(`${API}/signals`, handler('signals', signals));
  return counts;
}

async function gotoDashboard(page) {
  await page.goto('/#/DashboardHome');
  await expect(page.getByTestId('today-list')).toBeVisible({ timeout: 10000 });
}

const list = (page) => page.getByTestId('today-list');
const group = (page, g) => page.getByTestId(`today-group-${g}`);

for (const theme of ['dark', 'light']) {
  test.describe(`Today list (${theme} theme)`, () => {
    test.beforeEach(async ({ page }) => {
      await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
      await page.clock.setFixedTime(NOW);
    });

    test(`SC-TL-01 (${theme}): the Today list is the first element after the page title`, async ({ page }) => {
      await mockSources(page, { signals: { body: [signal('AAA')] } });
      await gotoDashboard(page);
      if (theme === 'dark') await expect(page.locator('html')).toHaveClass(/\bdark\b/);
      else await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);
      await expect(list(page)).toHaveText(/Due today/);
      const firstAfterTitle = await page.evaluate(() => {
        const h1 = document.querySelector('main h1') || document.querySelector('h1');
        const todayList = document.querySelector('[data-testid="today-list"]');
        const others = [...document.querySelectorAll('[data-testid="morning-briefing"], [data-testid="today-list"] ~ *')];
        const titleBlock = h1.parentElement;
        return {
          followsTitle: titleBlock.nextElementSibling === todayList,
          beforeBriefing: others.every((el) => el === todayList || (todayList.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)),
        };
      });
      expect(firstAfterTitle).toEqual({ followsTitle: true, beforeBriefing: true });
    });

    test(`SC-TL-02 (${theme}): the groups render in the order regime, exits, grace, stops, signals`, async ({ page }) => {
      await mockSources(page, {
        positions: { body: [riskOff('RSK'), graceLeft('GRC', 1), moved('MOV', TODAY, 80, 85)] },
        signals: { body: [signal('SIG')] },
      });
      await gotoDashboard(page);
      await expect(group(page, 'signals')).toBeVisible();
      const order = await list(page).locator('[data-testid^="today-group-"]').evaluateAll(
        (els) => els.map((e) => e.getAttribute('data-testid'))
      );
      expect(order).toEqual(['today-group-regime', 'today-group-exits', 'today-group-grace', 'today-group-stops', 'today-group-signals']);
    });

    test(`SC-TL-03/04 (${theme}): regime shows US then UK with badges; UNKNOWN keeps its description; rows link to Signals`, async ({ page }) => {
      await mockSources(page, { market: { body: MARKET_US_UNKNOWN }, signals: { body: [signal('SIG')] } });
      await gotoDashboard(page);
      const rows = group(page, 'regime').getByRole('link');
      await expect(rows).toHaveCount(2);
      await expect(rows.nth(0)).toContainText('US (SPY)');
      await expect(rows.nth(1)).toContainText('UK (FTSE)');
      const unknown = page.getByTestId('regime-unknown-SPY');
      await expect(unknown).toHaveText('UNKNOWN ?');
      await expect(unknown).toHaveAccessibleDescription(US_EXPLANATION);
      await expect(page.getByTestId('today-item-regime-US')).toHaveAccessibleDescription(US_EXPLANATION);
      await expect(page.getByTestId('today-item-regime-UK')).toContainText('RISK-OFF ✗');
      await expect(page.getByTestId('today-item-regime-US')).toHaveAttribute('href', '#/Signals');
      await page.getByTestId('today-item-regime-UK').click();
      await expect(page).toHaveURL(/#\/Signals/);
    });

    test(`SC-TL-05/06/21/22 (${theme}): exits due lists the predicate's positions, risk-off first then A–Z, with header count and sub-line`, async ({ page }) => {
      await mockSources(page, {
        positions: { body: [breached('ZBR'), riskOff('YRO'), inGraceBreached('GRB'), pos({ ticker: 'OKK' }), breached('ABR'), riskOff('BRO')] },
      });
      await gotoDashboard(page);
      const exits = group(page, 'exits');
      await expect(exits.getByTestId('today-header')).toHaveText('Exits due · 4');
      // dashboard.md v4.1 TL-21: the Market regime header has no count.
      await expect(group(page, 'regime').getByTestId('today-header')).toHaveText('Market regime');
      await expect(exits).toContainText('These positions meet a strategy exit condition (§8). Nothing is exited automatically.');
      const tickers = await exits.locator('[data-testid^="today-item-exits-"]').evaluateAll(
        (els) => els.map((e) => e.getAttribute('data-testid').replace('today-item-exits-', ''))
      );
      expect(tickers).toEqual(['BRO', 'YRO', 'ABR', 'ZBR']);
      await expect(exits.getByTestId('today-item-exits-BRO')).toContainText('RISK OFF');
      await expect(exits.getByTestId('today-item-exits-ABR')).toContainText('STOP REACHED');
      await expect(exits.getByTestId('today-item-exits-GRB')).toHaveCount(0);
    });

    test(`SC-TL-07 (${theme}): "Review exit" opens that position's exit dialog`, async ({ page }) => {
      await mockSources(page, { positions: { body: [pos({ ticker: 'OKK' }), breached('BRC')] } });
      await page.route(`${API}/positions/grace-period-alerts`, (r) => r.fulfill(json({ status: 'ok', data: [] })));
      await gotoDashboard(page);
      const link = list(page).getByRole('link', { name: 'Review exit for BRC' });
      await expect(link).toHaveAttribute('href', '#/Positions?exit=pos-BRC');
      await link.click();
      await expect(page.getByRole('dialog')).toBeVisible({ timeout: 8000 });
      await expect(page.getByRole('dialog')).toContainText('BRC');
    });

    test(`SC-TL-08 (${theme}): more than 5 exits shows 5 rows and "+N more" to Positions`, async ({ page }) => {
      await mockSources(page, { positions: { body: ['A', 'B', 'C', 'D', 'E', 'F', 'G'].map((t) => breached(`X${t}`)) } });
      await gotoDashboard(page);
      const exits = group(page, 'exits');
      await expect(exits.locator('[data-testid^="today-item-exits-"]')).toHaveCount(5);
      await expect(exits.getByTestId('today-overflow-exits')).toHaveText('+2 more');
      await expect(exits.getByTestId('today-overflow-exits')).toHaveAttribute('href', '#/Positions');
    });

    test(`SC-TL-11/12 (${theme}): new signals keep API order, show no rank, and link to Research`, async ({ page }) => {
      await mockSources(page, { signals: { body: [signal('ZZZ', { rank: 1 }), signal('AAA', { rank: 2 }), signal('MMM', { rank: 3 })] } });
      await gotoDashboard(page);
      const signals = group(page, 'signals');
      const tickers = await signals.locator('[data-testid^="today-item-signals-"]').evaluateAll(
        (els) => els.map((e) => e.getAttribute('data-testid').replace('today-item-signals-', ''))
      );
      expect(tickers).toEqual(['ZZZ', 'AAA', 'MMM']);
      const digitOnly = await signals.locator('li *').evaluateAll(
        (els) => els.filter((e) => /^\d+$/.test(e.textContent.trim())).length
      );
      expect(digitOnly).toBe(0);
      const research = signals.getByRole('link', { name: 'Research AAA' });
      await expect(research).toHaveAttribute('href', '#/research/AAA');
    });

    test(`SC-TL-13 (${theme}): an empty group other than regime is not rendered`, async ({ page }) => {
      await mockSources(page, { positions: { body: [riskOff('RSK')] } });
      await gotoDashboard(page);
      await expect(group(page, 'exits')).toBeVisible();
      await expect(group(page, 'regime')).toBeVisible();
      await expect(group(page, 'signals')).toHaveCount(0);
      await expect(group(page, 'grace')).toHaveCount(0);
    });

    test(`SC-TL-14 (${theme}): a quiet day shows only the one-line summary with both regime badges`, async ({ page }) => {
      await mockSources(page, {
        market: { body: MARKET_US_UNKNOWN },
        positions: { body: [pos({ ticker: 'OKK' })] },
        signals: { body: [signal('OLD', { signal_date: YESTERDAY })] },
      });
      await gotoDashboard(page);
      const quiet = page.getByTestId('today-quiet');
      await expect(quiet).toBeVisible();
      await expect(quiet).toHaveText('Nothing due today · US UNKNOWN ? · UK RISK-OFF ✗');
      await expect(quiet.getByTestId('regime-unknown-SPY')).toHaveAccessibleDescription(US_EXPLANATION);
      await expect(list(page).locator('[data-testid^="today-group-"]')).toHaveCount(0);
    });

    test(`SC-TL-15 (${theme}): loading shows one skeleton row per group; resolved groups render while others load`, async ({ page }) => {
      await mockSources(page, {
        positions: { body: [riskOff('RSK')] },
        signals: { body: [signal('SIG')], delayMs: 3000 },
      });
      await page.goto('/#/DashboardHome');
      await expect(group(page, 'exits')).toContainText('RSK', { timeout: 10000 });
      await expect(page.getByTestId('today-skeleton-signals')).toHaveCount(1);
      await expect(list(page).locator('.animate-spin')).toHaveCount(0);
      await expect(group(page, 'signals')).toContainText('SIG', { timeout: 10000 });
      await expect(page.getByTestId('today-skeleton-signals')).toHaveCount(0);
    });

    test(`SC-TL-15b (${theme}): before any source resolves, each group shows one skeleton row`, async ({ page }) => {
      await mockSources(page, {
        market: { body: MARKET_ON, delayMs: 4000 },
        positions: { body: [riskOff('RSK')], delayMs: 4000 },
        signals: { body: [signal('SIG')], delayMs: 4000 },
      });
      await page.goto('/#/DashboardHome');
      await expect(list(page)).toBeVisible({ timeout: 10000 });
      for (const g of ['regime', 'exits', 'grace', 'stops', 'signals']) {
        await expect(page.getByTestId(`today-skeleton-${g}`)).toHaveCount(1);
      }
      await expect(page.getByTestId('today-quiet')).toHaveCount(0);
      await expect(group(page, 'exits')).toContainText('RSK', { timeout: 10000 });
    });

    test(`SC-TL-16/25 (${theme}): a failed source shows its error line with Retry, no quiet line, and Retry refetches only that source`, async ({ page }) => {
      const counts = await mockSources(page, { signals: { fail: true } });
      await gotoDashboard(page);
      const error = page.getByTestId('today-error-signals');
      await expect(error).toContainText("Couldn't load New signals.", { timeout: 10000 });
      await expect(group(page, 'regime')).toBeVisible();
      await expect(page.getByTestId('today-quiet')).toHaveCount(0);
      const before = { ...counts };
      await error.getByRole('button', { name: 'Retry' }).click();
      await expect.poll(() => counts.signals).toBeGreaterThan(before.signals);
      expect(counts.positions).toBe(before.positions);
      expect(counts.market).toBe(before.market);
    });

    test(`SC-TL-17 (${theme}): all sources failing shows "Today's list is unavailable." with Retry`, async ({ page }) => {
      await mockSources(page, { market: { fail: true }, positions: { fail: true }, signals: { fail: true } });
      await gotoDashboard(page);
      const unavailable = page.getByTestId('today-unavailable');
      await expect(unavailable).toContainText("Today's list is unavailable.", { timeout: 15000 });
      await expect(unavailable.getByRole('button', { name: 'Retry' })).toBeVisible();
    });

    test(`SC-TL-18/19 (${theme}): Card 4 and the Exit Conditions Met row are gone; the list has no data-changing buttons`, async ({ page }) => {
      await mockSources(page, {
        positions: { body: [riskOff('RSK'), graceLeft('GRC', 1)] },
        signals: { body: [signal('SIG')] },
      });
      await gotoDashboard(page);
      await expect(group(page, 'signals')).toBeVisible();
      await expect(page.getByTestId('exit-conditions-card')).toHaveCount(0);
      await expect(page.getByText('Signal Status', { exact: true })).toHaveCount(0);
      await expect(list(page).getByRole('button')).toHaveCount(0);
    });

    test(`SC-TL-23 (${theme}): grace ends today lists only remaining = 1, A–Z, linking to the position`, async ({ page }) => {
      await mockSources(page, { positions: { body: [graceLeft('ZGR', 1), graceLeft('TWO', 2), graceLeft('NUL', null), graceLeft('AGR', 1)] } });
      await gotoDashboard(page);
      const grace = group(page, 'grace');
      await expect(grace.getByTestId('today-header')).toHaveText('Grace ends today · 2');
      const rows = grace.getByRole('link');
      await expect(rows).toHaveCount(2);
      await expect(rows.nth(0)).toContainText('AGR');
      await expect(rows.nth(1)).toContainText('ZGR');
      await expect(rows.nth(0)).toContainText('Grace ends today — the trailing stop applies from the next session');
      await expect(rows.nth(0)).toHaveAttribute('href', '#/Positions?position=pos-AGR');
    });

    test(`SC-TL-24 (${theme}): grace and signals cap at 5 with "+N more"`, async ({ page }) => {
      const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
      await mockSources(page, {
        positions: { body: letters.map((t) => graceLeft(`G${t}`, 1)) },
        signals: { body: letters.map((t) => signal(`S${t}`)) },
      });
      await gotoDashboard(page);
      await expect(group(page, 'grace').locator('[data-testid^="today-item-grace-"]')).toHaveCount(5);
      await expect(page.getByTestId('today-overflow-grace')).toHaveText('+2 more');
      await expect(page.getByTestId('today-overflow-grace')).toHaveAttribute('href', '#/Positions');
      await expect(group(page, 'signals').locator('[data-testid^="today-item-signals-"]')).toHaveCount(5);
      await expect(page.getByTestId('today-overflow-signals')).toHaveText('+2 more');
      await expect(page.getByTestId('today-overflow-signals')).toHaveAttribute('href', '#/Signals');
    });

    test(`SC-TL-26 (${theme}): a failed GET /positions and a failed GET /market/status show their error lines`, async ({ page }) => {
      await mockSources(page, { market: { fail: true }, positions: { fail: true }, signals: { body: [signal('SIG')] } });
      await gotoDashboard(page);
      await expect(page.getByTestId('today-error-exits')).toContainText("Couldn't load Exits due.", { timeout: 15000 });
      await expect(page.getByTestId('today-error-grace')).toContainText("Couldn't load Grace ends today.");
      await expect(page.getByTestId('today-error-stops')).toContainText("Couldn't load Stops moved.");
      await expect(page.getByTestId('today-error-regime')).toContainText("Couldn't load Market regime.");
      await expect(group(page, 'signals')).toContainText('SIG');
    });

    test(`SC-TL-27 (${theme}): at 375px the groups stack full width in order`, async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 900 });
      await mockSources(page, {
        positions: { body: [riskOff('RSK'), graceLeft('GRC', 1)] },
        signals: { body: [signal('SIG')] },
      });
      await gotoDashboard(page);
      await expect(group(page, 'signals')).toBeVisible();
      const boxes = await list(page).locator('[data-testid^="today-group-"]').evaluateAll((els) =>
        els.map((e) => { const r = e.getBoundingClientRect(); return { top: r.top, width: r.width, parent: e.parentElement.getBoundingClientRect().width }; })
      );
      expect(boxes).toHaveLength(4);
      for (let i = 1; i < boxes.length; i += 1) expect(boxes[i].top).toBeGreaterThan(boxes[i - 1].top);
      for (const b of boxes) expect(Math.abs(b.width - b.parent)).toBeLessThan(1);
    });

    test(`SC-TL-28 (${theme}): with Card 4 removed, Recent Activity spans its row at 1440px`, async ({ page }) => {
      await page.setViewportSize({ width: 1440, height: 900 });
      await mockSources(page);
      await gotoDashboard(page);
      const card = page.getByText('Recent Activity', { exact: true }).locator('xpath=ancestor::a[1]');
      await expect(card).toBeVisible();
      const widths = await card.evaluate((a) => ({ card: a.getBoundingClientRect().width, row: a.parentElement.getBoundingClientRect().width }));
      expect(Math.abs(widths.card - widths.row)).toBeLessThan(1);
    });

    test(`SC-TL-29 (${theme}): new signals use the local-date filter and count every status`, async ({ page }) => {
      await mockSources(page, {
        signals: {
          body: [
            signal('NEW', { status: 'new' }),
            signal('WAT', { status: 'watchlisted' }),
            signal('DIS', { status: 'dismissed' }),
            signal('ENT', { status: 'entered' }),
            signal('CRE', { signal_date: null, created_date: `${TODAY}T08:00:00` }),
            signal('OLD', { signal_date: YESTERDAY }),
          ],
        },
      });
      await gotoDashboard(page);
      const signals = group(page, 'signals');
      await expect(signals.getByTestId('today-header')).toHaveText('New signals · 5');
      await expect(signals.getByTestId('today-item-signals-OLD')).toHaveCount(0);
      await expect(signals.getByTestId('today-item-signals-DIS')).toBeVisible();
    });

    test(`SC-TL-09 (${theme}): stops moved lists today's and the previous weekday's moves A–Z, "Stop moved from {previous} to {current}" in native currency`, async ({ page }) => {
      await mockSources(page, {
        positions: {
          body: [
            moved('ZUS', TODAY, 85, 90.5),
            moved('OLD', '2026-11-05', 70, 75),
            moved('SUN', YESTERDAY, 70, 75),
            moved('LOW', TODAY, 90, 88),
            moved('AUK.L', PREV_WEEKDAY, 1.2, 1.25, 'UK'),
            pos({ ticker: 'NVR' }),
          ],
        },
      });
      await gotoDashboard(page);
      const stops = group(page, 'stops');
      await expect(stops.getByTestId('today-header')).toHaveText('Stops moved · 2');
      const rows = stops.getByRole('link');
      await expect(rows).toHaveCount(2);
      await expect(rows.nth(0)).toHaveText('AUK.LStop moved from £1.20 to £1.25');
      await expect(rows.nth(1)).toHaveText('ZUSStop moved from $85.00 to $90.50');
      await expect(stops.getByTestId('today-item-stops-OLD')).toHaveCount(0);
      await expect(stops.getByTestId('today-item-stops-NVR')).toHaveCount(0);
      await expect(stops.getByTestId('today-item-stops-LOW')).toHaveCount(0);
      await expect(page.getByTestId('today-quiet')).toHaveCount(0);
    });

    test(`SC-TL-09c (${theme}): a move older than the previous weekday does not show and leaves the quiet-day line`, async ({ page }) => {
      await mockSources(page, { positions: { body: [moved('OLD', '2026-11-05', 70, 75)] } });
      await gotoDashboard(page);
      await expect(page.getByTestId('today-quiet')).toBeVisible();
      await expect(group(page, 'stops')).toHaveCount(0);
    });

    test(`SC-TL-09b (${theme}): more than 5 stops moved show 5 rows and "+N more" to Positions`, async ({ page }) => {
      const tickers = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
      await mockSources(page, { positions: { body: tickers.map((t) => moved(`MV${t}`, TODAY, 80, 85)) } });
      await gotoDashboard(page);
      const stops = group(page, 'stops');
      await expect(stops.getByTestId('today-header')).toHaveText('Stops moved · 7');
      await expect(stops.locator('[data-testid^="today-item-stops-"]')).toHaveCount(5);
      await expect(page.getByTestId('today-overflow-stops')).toHaveText('+2 more');
      await expect(page.getByTestId('today-overflow-stops')).toHaveAttribute('href', '#/Positions');
    });

    test(`SC-TL-10 (${theme}): a stops moved row links to /Positions?position={id}`, async ({ page }) => {
      await mockSources(page, { positions: { body: [moved('MOV', TODAY, 80, 85)] } });
      await gotoDashboard(page);
      const row = page.getByTestId('today-item-stops-MOV');
      await expect(row).toHaveAttribute('href', '#/Positions?position=pos-MOV');
      await row.click();
      await expect(page).toHaveURL(/#\/Positions\?position=pos-MOV$/);
    });

    test(`SC-TL-STOPS (${theme}): the Stops moved group and any placeholder are absent while no position has stop_last_moved_date`, async ({ page }) => {
      await mockSources(page, {
        positions: { body: [riskOff('RSK'), graceLeft('GRC', 1)] },
        signals: { body: [signal('SIG')] },
      });
      await gotoDashboard(page);
      await expect(group(page, 'signals')).toBeVisible();
      await expect(group(page, 'stops')).toHaveCount(0);
      await expect(page.getByTestId('today-skeleton-stops')).toHaveCount(0);
      await expect(list(page)).not.toContainText(/stops? moved/i);
    });
  });
}
