/**
 * Decision cards for Positions on narrow screens — ST-02 (BLG-FE-261, EPIC-01, v9.17)
 *
 * Spec: docs/specs/frontend/pages/positions.md v2.25 §Responsive Behavior (Table v2.25 row),
 *       §Decision-First Table
 * Design: docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md §4, §10
 *
 * AC (stage4_backlog_slice.md#ST-02): at 390px width, Positions shows cards with
 * no horizontal page scroll.
 *
 *   SC-POSDC-01  At 390 × 844 the Table view renders one decision card per position,
 *                in the same urgency order as the table, and no table
 *   SC-POSDC-02  No horizontal page scroll at 390px (Table view collapsed and with
 *                details open; Grid view)
 *   SC-POSDC-03  Each card leads with Ticker, market pill, Action needed, Price, Stop,
 *                To stop and P&L %, using the table's copy
 *   SC-POSDC-04  Details opens the expanded-row grid in 2 columns; aria-expanded toggles
 *   SC-POSDC-05  The action buttons sit in the card footer, visible, at least 44 × 44 px
 *   SC-POSDC-06  At md (768px) and wider the table renders instead of the cards
 *   SC-POSDC-07  A ?position= deep link opens that card's details
 *
 * Mock layer: page.route(). HashRouter: navigate with '/#/…'.
 */

'use strict';

const { test, expect } = require('./fixtures/api-status-guard');

const { stubPositionsPage, DECISION_FIXTURES } = require('./fixtures/positions-table');

const PHONE = { width: 390, height: 844 };
// Same fixtures as SC-POSDF (ST-01), so the expected order matches the table's.
const { ALL } = DECISION_FIXTURES;
const URGENCY_ORDER = ['RISK', 'BRCH', 'NEAR', 'WARN', 'OTHR', 'GRCB'];

async function gotoCards(page, { positions = ALL, hash = '/#/Positions' } = {}) {
  await page.setViewportSize(PHONE);
  await stubPositionsPage(page, positions);
  await page.goto(hash);
  const tableBtn = page.locator('[aria-label="Table view"]');
  await tableBtn.waitFor({ state: 'visible', timeout: 10000 });
  await tableBtn.click();
  await page.waitForSelector('[data-testid="position-decision-card"]', { timeout: 8000 });
}

const card = (page, ticker) => page.getByTestId('position-decision-card').filter({
  has: page.getByRole('button', { name: `Show details for ${ticker}`, exact: true }),
});

async function cardOrder(page) {
  const labels = await page
    .getByTestId('position-decision-card')
    .getByTestId('position-card-details')
    .evaluateAll((els) => els.map((el) => el.getAttribute('aria-label')));
  return labels.map((l) => l.replace('Show details for ', ''));
}

async function pageScrollWidth(page) {
  return page.evaluate(() => document.documentElement.scrollWidth);
}

test.describe('Positions decision cards on narrow screens (ST-02, BLG-FE-261)', () => {
  test('SC-POSDC-01 — at 390px the Table view renders cards in urgency order, not the table', async ({ page }) => {
    await gotoCards(page);
    await expect(page.getByTestId('position-decision-card')).toHaveCount(ALL.length);
    expect(await cardOrder(page)).toEqual(URGENCY_ORDER);
    await expect(page.getByTestId('position-row')).toHaveCount(0);
    await expect(page.locator('main table thead')).toHaveCount(0);
    await expect(page.getByTestId('urgency-caption')).toHaveText('Sorted by what needs attention first');
  });

  test('SC-POSDC-02 — no horizontal page scroll at 390px', async ({ page }) => {
    await gotoCards(page);
    expect(await pageScrollWidth(page)).toBeLessThanOrEqual(PHONE.width);

    // With every card's details open (the widest content on the page).
    const buttons = page.getByTestId('position-card-details');
    const n = await buttons.count();
    for (let i = 0; i < n; i += 1) await buttons.nth(i).click();
    await expect(page.getByTestId('position-detail')).toHaveCount(n);
    expect(await pageScrollWidth(page)).toBeLessThanOrEqual(PHONE.width);

    // The Grid view (one card per row below md) also fits.
    await page.locator('[aria-label="Grid view"]').click();
    await expect(page.getByTestId('position-decision-card')).toHaveCount(0);
    expect(await pageScrollWidth(page)).toBeLessThanOrEqual(PHONE.width);
  });

  test('SC-POSDC-03 — each card leads with the table\'s fields and copy', async ({ page }) => {
    await gotoCards(page);
    const near = card(page, 'NEAR');
    await expect(near).toContainText('NEAR');
    await expect(near).toContainText('US');
    for (const label of ['Price', 'Stop', 'To stop']) {
      await expect(near.locator('dt', { hasText: new RegExp(`^${label}$`) })).toHaveCount(1);
    }
    await expect(near.getByTestId('stop-distance')).toHaveText('0.4R · 3.8%');
    await expect(near.getByTestId('stop-distance')).toHaveClass(/text-app-negative/);
    await expect(near.getByTestId('stop-value')).toBeVisible();
    await expect(near).toContainText('+4.0%');

    await expect(card(page, 'RISK').getByTestId('action-needed')).toHaveText('RISK OFF');
    await expect(card(page, 'BRCH').getByTestId('action-needed')).toHaveText('STOP REACHED');
    await expect(card(page, 'BRCH').getByTestId('breach-badge')).toBeVisible();
    // The Stop value and its BREACH badge stay inside their field: neither runs
    // into the To stop field beside it.
    const toStopBox = await card(page, 'BRCH').getByTestId('stop-distance').boundingBox();
    for (const id of ['stop-value', 'breach-badge']) {
      const box = await card(page, 'BRCH').getByTestId(id).boundingBox();
      expect(box.x + box.width).toBeLessThanOrEqual(toStopBox.x);
    }
    await expect(near.getByTestId('action-needed')).toHaveText('Near stop');
    await expect(card(page, 'GRCB').getByTestId('action-needed')).toHaveText('Grace ends today');
    await expect(card(page, 'GRCB').getByTestId('stop-distance')).toHaveText('Not enforced (grace)');
    await expect(card(page, 'OTHR').getByTestId('action-needed')).toHaveText('—');
  });

  test('SC-POSDC-04 — Details opens the expanded-row grid in 2 columns', async ({ page }) => {
    await gotoCards(page);
    await expect(page.getByTestId('position-detail')).toHaveCount(0);
    const details = card(page, 'BRCH').getByTestId('position-card-details');
    await expect(details).toHaveAttribute('aria-expanded', 'false');
    await expect(details).toHaveAttribute('aria-controls', 'position-detail-pos-brc');
    await details.click();
    await expect(details).toHaveAttribute('aria-expanded', 'true');
    const detail = page.locator('#position-detail-pos-brc');
    await expect(detail).toBeVisible();
    for (const label of ['Entry price', 'Initial stop', 'Shares', 'P&L (GBP)', 'Days held', 'State', 'Grace', 'Earnings', 'Alerts', 'Last reviewed', 'Stop provenance']) {
      await expect(detail.locator('dt', { hasText: new RegExp(`^${label.replace(/[()&]/g, '\\$&')}$`) })).toHaveCount(1);
    }
    await expect(detail.getByTestId('lifecycle-badge')).toHaveText('LOSING');
    const columns = await detail.locator('dl').evaluate((el) => getComputedStyle(el).gridTemplateColumns.split(' ').length);
    expect(columns).toBe(2);
    await details.click();
    await expect(page.locator('#position-detail-pos-brc')).toHaveCount(0);
  });

  test('SC-POSDC-05 — the action buttons sit in the card footer at 44 × 44 px or more', async ({ page }) => {
    await gotoCards(page);
    const footer = card(page, 'OTHR').getByTestId('position-card-actions');
    await expect(footer.getByRole('button', { name: 'Exit OTHR' })).toBeVisible();
    await expect(footer.getByRole('button', { name: 'Edit OTHR' })).toBeVisible();
    await expect(footer.getByRole('button', { name: 'Recheck compliance for OTHR' })).toBeVisible();
    await expect(footer.getByRole('button', { name: 'View Trail' })).toBeVisible();
    const buttons = footer.getByRole('button');
    const count = await buttons.count();
    expect(count).toBeGreaterThanOrEqual(4);
    for (let i = 0; i < count; i += 1) {
      const box = await buttons.nth(i).boundingBox();
      expect(box.width).toBeGreaterThanOrEqual(44);
      expect(box.height).toBeGreaterThanOrEqual(44);
    }
    // Details is also a 44px target.
    const detailsBox = await card(page, 'OTHR').getByTestId('position-card-details').boundingBox();
    expect(detailsBox.height).toBeGreaterThanOrEqual(44);
  });

  test('SC-POSDC-06 — at md and wider the table renders instead of the cards', async ({ page }) => {
    await gotoCards(page);
    await page.setViewportSize({ width: 768, height: 900 });
    await page.waitForSelector('[data-testid="position-row"]', { timeout: 5000 });
    await expect(page.getByTestId('position-decision-card')).toHaveCount(0);
    await expect(page.getByTestId('position-row')).toHaveCount(ALL.length);
    await page.setViewportSize({ width: 767, height: 900 });
    await expect(page.getByTestId('position-decision-card')).toHaveCount(ALL.length);
    await expect(page.getByTestId('position-row')).toHaveCount(0);
  });

  test('SC-POSDC-07 — a ?position= deep link opens that card\'s details', async ({ page }) => {
    await gotoCards(page);
    await page.goto('/#/Positions?position=pos-oth');
    await expect(page.locator('#position-detail-pos-oth')).toBeVisible();
    await expect(card(page, 'OTHR').getByTestId('position-card-details')).toHaveAttribute('aria-expanded', 'true');
    expect(await cardOrder(page)).toEqual(URGENCY_ORDER);
  });
});
