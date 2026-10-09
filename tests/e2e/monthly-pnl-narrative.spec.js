/**
 * AI summary on the Monthly P&L report — ST-25 (BLG-FEAT-59, EPIC-04, v9.11)
 *
 * Design source: docs/design/2026-10-08__release-v9.11/monthly-pnl-ai-narrative/decision_record.md §8
 * Spec: docs/specs/frontend/pages/reports.md §AI Summary (Monthly P&L Narrative) (v0.21)
 * §13: docs/product/decisions/decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md
 *
 * AC 1: "The narrative section renders on Monthly P&L as optional and dismissible (Playwright)".
 *
 * Coverage:
 *   SC-MPN-01  Not-generated state: card, badge and exact caption render; no POST until Generate (optional)
 *   SC-MPN-02  A stored summary from GET renders populated with no POST (on request only)
 *   SC-MPN-03  Generate shows the text and "Generated …"
 *   SC-MPN-04  Hide removes the card, survives a reload, Show restores it; throwing storage -> visible (dismissible)
 *   SC-MPN-05  A tax-year change fires a new GET; a late POST response for the old year is discarded
 *   SC-MPN-06  source "fallback" shows the fallback note
 *   SC-MPN-07  A 500 shows the error and keeps the previous text; a 429 shows the API message
 *   SC-MPN-08  No card when the month list is empty
 *   SC-MPN-09  axe: no serious/critical violations in the card, populated and in the error state, both themes
 *
 * Infrastructure: page.route() interception, no live backend. HashRouter: go to /#/Reports, then
 * click the "Monthly P&L" tab. The page selects the current UK tax year by default.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const API = 'http://localhost:8000';
const NARRATIVE = new RegExp(`${API}/reports/monthly-pnl/narrative`);
const MONTHLY = new RegExp(`${API}/reports/monthly-pnl(?!\\?format=csv|/narrative)`);

function currentUkTaxYear() {
  const now = new Date();
  const y = now.getFullYear();
  const beforeApril6 = now.getMonth() < 3 || (now.getMonth() === 3 && now.getDate() < 6);
  return beforeApril6 ? y - 1 : y;
}
const YEAR = currentUkTaxYear();
const LABEL = `${YEAR}/${String(YEAR + 1).slice(2)}`;
const CAPTION = 'Describes your recorded figures only. Not a forecast, recommendation or tax advice.';
const TEXT = `In the ${LABEL} tax year so far you closed 6 trades with realised P&L of £220.50.`;

const month = (m, overrides = {}) => ({
  year: YEAR, month: m, realised_pnl_gbp: 110.25, trade_count: 3, null_fee_trade_count: 0,
  snapshotted: true, restated: false, snapshot_realised_pnl_gbp: 110.25, restated_diff_gbp: 0, ...overrides,
});

const narrative = (overrides = {}) => ({
  year: YEAR, narrative: TEXT, source: 'ai', generated_at: new Date().toISOString(), advisory: true, ...overrides,
});
const emptyNarrative = (year = YEAR) => ({ year, narrative: null, source: null, generated_at: null, advisory: true });

async function mockBase(page, months = [month(5), month(6)]) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: [] }) })
  );
  await page.route(MONTHLY, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', data: months, estimated_unrealised_pnl: null, unrealised_note: null, compliance_summary: null }),
    })
  );
}

// getData(year) -> GET payload; post(route, body) -> handles the POST. Returns the list of POST bodies seen.
async function mockNarrative(page, { getData = (y) => emptyNarrative(y), post } = {}) {
  const posts = [];
  await page.route(NARRATIVE, async (route) => {
    const req = route.request();
    if (req.method() === 'GET') {
      const y = Number(new URL(req.url()).searchParams.get('year'));
      return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: getData(y) }) });
    }
    const body = JSON.parse(req.postData() || '{}');
    posts.push(body);
    if (post) return post(route, body);
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: narrative({ year: body.year }) }) });
  });
  return posts;
}

async function gotoMonthlyTab(page) {
  await page.goto('/#/Reports');
  await page.getByRole('button', { name: /monthly p&l/i }).click();
}

test('SC-MPN-01: the card renders unprompted, with badge and caption, and nothing is generated until Generate', async ({ page }) => {
  await mockBase(page);
  const posts = await mockNarrative(page);
  await gotoMonthlyTab(page);

  const card = page.getByTestId('monthly-narrative-card');
  await expect(card).toBeVisible({ timeout: 8000 });
  await expect(card.getByRole('heading', { name: 'AI summary' })).toBeVisible();
  await expect(page.getByTestId('monthly-narrative-badge')).toHaveText('AI Advisory');
  await expect(page.getByTestId('monthly-narrative-caption')).toHaveText(CAPTION);
  await expect(card).toContainText('Get a short written summary of these months.');
  await expect(page.getByTestId('monthly-narrative-generate')).toHaveText('Generate summary');
  await page.waitForTimeout(500);
  expect(posts).toHaveLength(0);
});

test('SC-MPN-02: a stored summary from GET renders populated with no POST', async ({ page }) => {
  await mockBase(page);
  const posts = await mockNarrative(page, { getData: () => narrative() });
  await gotoMonthlyTab(page);

  await expect(page.getByTestId('monthly-narrative-text')).toHaveText(TEXT, { timeout: 8000 });
  await expect(page.getByTestId('monthly-narrative-generate')).toHaveText('Regenerate');
  await expect(page.getByTestId('monthly-narrative-generated-at')).toContainText('Generated');
  await page.waitForTimeout(500);
  expect(posts).toHaveLength(0);
});

test('SC-MPN-03: Generate shows the summary and when it was generated', async ({ page }) => {
  await mockBase(page);
  const posts = await mockNarrative(page);
  await gotoMonthlyTab(page);

  await page.getByTestId('monthly-narrative-generate').click();
  await expect(page.getByTestId('monthly-narrative-text')).toHaveText(TEXT, { timeout: 8000 });
  await expect(page.getByTestId('monthly-narrative-generated-at')).toContainText('Generated');
  expect(posts).toEqual([{ year: YEAR, regenerate: false }]);

  // Regenerate asks for a fresh summary.
  await page.getByTestId('monthly-narrative-generate').click();
  await expect.poll(() => posts.length).toBe(2);
  expect(posts[1]).toEqual({ year: YEAR, regenerate: true });
});

test('SC-MPN-04: Hide removes the card, survives a reload, and Show restores it', async ({ page }) => {
  await mockBase(page);
  await mockNarrative(page);
  await gotoMonthlyTab(page);

  await page.getByTestId('monthly-narrative-hide').click();
  await expect(page.getByTestId('monthly-narrative-card')).toHaveCount(0);
  await expect(page.getByTestId('monthly-narrative-show')).toBeVisible();

  await page.reload();
  await page.getByRole('button', { name: /monthly p&l/i }).click();
  await expect(page.getByTestId('monthly-narrative-show')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-narrative-card')).toHaveCount(0);

  await page.getByTestId('monthly-narrative-show').click();
  await expect(page.getByTestId('monthly-narrative-card')).toBeVisible();
});

test('SC-MPN-04b: with storage that throws, the card is visible', async ({ page }) => {
  await page.addInitScript(() => {
    const original = Storage.prototype.getItem;
    Storage.prototype.getItem = function (key) {
      if (key === 'reports.monthlyNarrative.hidden') throw new Error('blocked');
      return original.call(this, key);
    };
  });
  await mockBase(page);
  await mockNarrative(page);
  await gotoMonthlyTab(page);
  await expect(page.getByTestId('monthly-narrative-card')).toBeVisible({ timeout: 8000 });
});

test('SC-MPN-05: a tax-year change fetches that year; a late response for the old year is discarded', async ({ page }) => {
  await mockBase(page);
  const gets = [];
  let releaseOldPost;
  const oldPostHeld = new Promise((resolve) => { releaseOldPost = resolve; });
  await mockNarrative(page, {
    getData: (y) => { gets.push(y); return emptyNarrative(y); },
    post: async (route, body) => {
      await oldPostHeld;
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ status: 'ok', data: narrative({ year: body.year }) }) });
    },
  });
  await gotoMonthlyTab(page);
  await expect(page.getByTestId('monthly-narrative-card')).toBeVisible({ timeout: 8000 });

  await page.getByTestId('monthly-narrative-generate').click();
  await expect(page.getByTestId('monthly-narrative-generate')).toHaveText('Generating…');

  await page.getByTestId('monthly-tax-year-filter').click();
  await page.getByRole('option', { name: `${YEAR - 1}/${String(YEAR).slice(2)}` }).click();
  await expect.poll(() => gets.includes(YEAR - 1)).toBe(true);

  releaseOldPost();
  await page.waitForTimeout(500);
  await expect(page.getByTestId('monthly-narrative-text')).toHaveCount(0);
  await expect(page.getByTestId('monthly-narrative-generate')).toHaveText('Generate summary');
});

test('SC-MPN-06: a fallback summary shows the fallback note', async ({ page }) => {
  await mockBase(page);
  await mockNarrative(page, { getData: () => narrative({ source: 'fallback', narrative: `${LABEL} so far: realised P&L of £220.50.` }) });
  await gotoMonthlyTab(page);
  await expect(page.getByTestId('monthly-narrative-fallback-note')).toHaveText(
    "The AI summary couldn't be checked against your figures, so a standard summary is shown.", { timeout: 8000 });
});

test('SC-MPN-07: a failure keeps the previous text; a 429 shows the API message', async ({ page }) => {
  await mockBase(page);
  let status = 500;
  await mockNarrative(page, {
    getData: () => narrative(),
    post: (route) => route.fulfill({
      status, contentType: 'application/json',
      body: JSON.stringify({ status: 'error', message: status === 429 ? 'Daily limit for AI summaries reached. Try again tomorrow.' : 'Internal server error' }),
    }),
  });
  await gotoMonthlyTab(page);
  await expect(page.getByTestId('monthly-narrative-text')).toHaveText(TEXT, { timeout: 8000 });

  await page.getByTestId('monthly-narrative-generate').click();
  const error = page.getByTestId('monthly-narrative-error');
  await expect(error).toHaveText('Could not write the summary. Try again shortly.');
  await expect(error).toHaveAttribute('role', 'status');
  await expect(page.getByTestId('monthly-narrative-text')).toHaveText(TEXT);

  status = 429;
  await page.getByTestId('monthly-narrative-generate').click();
  await expect(error).toHaveText('Daily limit for AI summaries reached. Try again tomorrow.');
});

test('SC-MPN-08: no card when the tax year has no months', async ({ page }) => {
  await mockBase(page, []);
  await mockNarrative(page);
  await gotoMonthlyTab(page);
  await expect(page.getByText('No closed trades in scope.')).toBeVisible({ timeout: 8000 });
  await expect(page.getByTestId('monthly-narrative-card')).toHaveCount(0);
});

for (const theme of ['dark', 'light']) {
  test(`SC-MPN-09: axe finds no serious or critical violation in the card, populated and in error (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem('theme', t), theme);
    await mockBase(page);
    await mockNarrative(page, {
      getData: () => narrative(),
      post: (route) => route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ status: 'error', message: 'x' }) }),
    });
    await gotoMonthlyTab(page);
    await expect(page.getByTestId('monthly-narrative-text')).toBeVisible({ timeout: 8000 });
    if (theme === 'dark') await expect(page.locator('html')).toHaveClass(/\bdark\b/);
    else await expect(page.locator('html')).not.toHaveClass(/\bdark\b/);

    const scan = async () => {
      await page.waitForTimeout(800); // let entrance animations settle
      const results = await new AxeBuilder({ page }).include('[data-testid="monthly-narrative-card"]').analyze();
      return results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical').map((v) => v.id);
    };
    expect(await scan()).toEqual([]);
    await page.getByTestId('monthly-narrative-generate').click();
    await expect(page.getByTestId('monthly-narrative-error')).toBeVisible();
    expect(await scan()).toEqual([]);
  });
}
