/**
 * Decision-first Positions table — ST-01 (BLG-FE-260, EPIC-01, v9.17)
 *
 * Spec: docs/specs/frontend/pages/positions.md v2.25 §Decision-First Table
 * Design: docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md §2–§3, §10
 *
 * AC (stage4_backlog_slice.md#ST-01): the default view shows about 6 columns in
 * urgency order; expanding a row shows the rest.
 *
 *   SC-POSDF-01  Rows render in urgency tier order (exit condition → stop reached →
 *                near stop → other), with the in-grace breach in tier 4
 *   SC-POSDF-02  Header has the expand column, 6 data columns and Actions; caption shown
 *   SC-POSDF-03  "To stop" reads "{x.x}R · {y.y}%" with the Risk Dashboard colour bands;
 *                in grace it reads "Not enforced (grace)"
 *   SC-POSDF-04  "Action needed" shows RISK OFF / STOP REACHED / Near stop /
 *                Grace ends today / —
 *   SC-POSDF-05  Expanding a row shows every §3.2 field; collapsed by default;
 *                several rows may be open; the chevron toggles aria-expanded
 *   SC-POSDF-06  A ?position= deep link opens that row's details
 *   SC-POSDF-07  Within a tier, ties sort by distance then ticker A–Z
 *
 * Mock layer: page.route(). HashRouter: navigate with '/#/…'.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const {
  makePosition, stubPositionsPage, DECISION_FIXTURES,
} = require('./fixtures/positions-table');

const {
  ALL,
} = DECISION_FIXTURES;

async function gotoTable(page, positions = ALL, hash = '/#/Positions') {
  await stubPositionsPage(page, positions);
  await page.goto(hash);
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 10000 });
  await tableBtn.click();
  await page.waitForSelector('[data-testid="position-row"]', { timeout: 8000 });
}

const row = (page, ticker) => page.getByTestId('position-row').filter({ hasText: ticker });

async function tickerOrder(page) {
  const rows = page.getByTestId('position-row');
  const n = await rows.count();
  const out = [];
  for (let i = 0; i < n; i += 1) {
    out.push(((await rows.nth(i).locator('td').nth(1).innerText()).split(/\s/)[0]).trim());
  }
  return out;
}

test.describe('Decision-first Positions table (ST-01, BLG-FE-260)', () => {
  test('SC-POSDF-01 — rows render in urgency tier order; the in-grace breach is tier 4', async ({ page }) => {
    await gotoTable(page);
    // Tier 1 RISK, tier 2 BRCH, tier 3 NEAR, then tier 4 by distance %:
    // WARN 10.0, OTHR 16.7, then GRCB, whose stop is not enforced in grace and so
    // has no distance (sorts last in its tier) even though its price is below the stop.
    expect(await tickerOrder(page)).toEqual(['RISK', 'BRCH', 'NEAR', 'WARN', 'OTHR', 'GRCB']);
  });

  test('SC-POSDF-02 — header has expand, six data columns and Actions; caption shown', async ({ page }) => {
    await gotoTable(page);
    const headers = page.locator('thead th');
    await expect(headers).toHaveCount(8);
    const texts = (await headers.allInnerTexts()).map((t) => t.trim().toUpperCase());
    expect(texts.slice(1)).toEqual(['TICKER', 'PRICE', 'STOP', 'TO STOP', 'P&L %', 'ACTION NEEDED', 'ACTIONS']);
    await expect(page.getByTestId('urgency-caption')).toHaveText('Sorted by what needs attention first');
    // Fields moved to the expanded row are not table columns any more.
    await expect(page.getByRole('columnheader', { name: 'Entry Price' })).toHaveCount(0);
    await expect(page.getByRole('columnheader', { name: 'Last Reviewed' })).toHaveCount(0);
  });

  test('SC-POSDF-03 — To stop shows R and %, colour bands, and the grace wording', async ({ page }) => {
    await gotoTable(page);
    const near = row(page, 'NEAR').getByTestId('stop-distance');
    await expect(near).toHaveText('0.4R · 3.8%');
    await expect(near).toHaveClass(/text-app-negative/);
    const warn = row(page, 'WARN').getByTestId('stop-distance');
    await expect(warn).toHaveText('1.1R · 10.0%');
    await expect(warn).toHaveClass(/text-app-warning/);
    const other = row(page, 'OTHR').getByTestId('stop-distance');
    await expect(other).toHaveText('2.0R · 16.7%');
    await expect(other).toHaveClass(/text-app-fg/);
    const grace = row(page, 'GRCB').getByTestId('stop-distance');
    await expect(grace).toHaveText('Not enforced (grace)');
    await expect(grace).toHaveClass(/text-app-muted/);
    await expect(row(page, 'GRCB').getByTestId('stop-value')).toHaveText('Not enforced (grace)');
    // The in-grace row shows no breach badge.
    await expect(row(page, 'GRCB').getByTestId('breach-badge')).toHaveCount(0);
    await expect(row(page, 'BRCH').getByTestId('breach-badge')).toBeVisible();
  });

  test('SC-POSDF-04 — Action needed reuses the existing copy by tier', async ({ page }) => {
    await gotoTable(page);
    await expect(row(page, 'RISK').getByTestId('action-needed')).toHaveText('RISK OFF');
    await expect(row(page, 'BRCH').getByTestId('action-needed')).toHaveText('STOP REACHED');
    await expect(row(page, 'NEAR').getByTestId('action-needed')).toHaveText('Near stop');
    await expect(row(page, 'GRCB').getByTestId('action-needed')).toHaveText('Grace ends today');
    await expect(row(page, 'OTHR').getByTestId('action-needed')).toHaveText('—');
  });

  test('SC-POSDF-05 — expanding a row shows every remaining field', async ({ page }) => {
    await gotoTable(page);
    await expect(page.getByTestId('position-detail')).toHaveCount(0);
    const chevron = page.getByRole('button', { name: 'Show details for BRCH' });
    await expect(chevron).toHaveAttribute('aria-expanded', 'false');
    await expect(chevron).toHaveAttribute('aria-controls', 'position-detail-pos-brc');
    await chevron.click();
    await expect(chevron).toHaveAttribute('aria-expanded', 'true');
    const detail = page.locator('#position-detail-pos-brc');
    await expect(detail).toBeVisible();
    for (const label of ['Entry price', 'Initial stop', 'Shares', 'P&L (GBP)', 'Days held', 'State', 'Grace', 'Earnings', 'Alerts', 'Last reviewed', 'Stop provenance']) {
      await expect(detail.locator('dt', { hasText: new RegExp(`^${label.replace(/[()&]/g, '\\$&')}$`) })).toHaveCount(1);
    }
    await expect(detail.getByTestId('lifecycle-badge')).toHaveText('LOSING');
    await expect(detail.getByTestId('last-reviewed-cell')).toBeVisible();
    // Several rows may be open at once.
    await page.getByRole('button', { name: 'Show details for OTHR' }).click();
    await expect(page.getByTestId('position-detail')).toHaveCount(2);
    // Toggling closes it again.
    await chevron.click();
    await expect(page.locator('#position-detail-pos-brc')).toHaveCount(0);
  });

  test('SC-POSDF-06 — a ?position= deep link opens that row', async ({ page }) => {
    await stubPositionsPage(page, ALL);
    await page.goto('/#/Positions');
    await page.locator('[aria-label="Table view"]').click();
    await page.waitForSelector('[data-testid="position-row"]');
    await page.goto('/#/Positions?position=pos-oth');
    await expect(page.locator('#position-detail-pos-oth')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Show details for OTHR' })).toHaveAttribute('aria-expanded', 'true');
    // The order is unchanged by the deep link.
    expect((await tickerOrder(page))[4]).toBe('OTHR');
  });

  test('SC-POSDF-07 — ties within a tier sort by distance, then ticker A–Z', async ({ page }) => {
    const a = makePosition({ id: 'pos-a', ticker: 'BBBB' });
    const b = makePosition({ id: 'pos-b', ticker: 'AAAA' });
    const c = makePosition({ id: 'pos-c', ticker: 'CCCC', current_trailing_stop: null, current_trailing_stop_native: null });
    await gotoTable(page, [c, a, b]);
    expect(await tickerOrder(page)).toEqual(['AAAA', 'BBBB', 'CCCC']);
    await expect(row(page, 'CCCC').getByTestId('stop-distance')).toHaveText('—');
  });
});
