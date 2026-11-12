/**
 * Positions decision-first table helpers (ST-01, BLG-FE-260, EPIC-01, v9.17).
 *
 * From ST-01 the Positions Table view shows six data columns by default; Entry
 * price, Initial stop, Shares, P&L (GBP), Days held, State, Grace, Earnings,
 * Alerts, Last reviewed and the stop provenance line live in an expanded row
 * (positions.md v2.25 §Decision-First Table, §Expanded Row). Specs that assert
 * on those fields open the row first with these helpers.
 *
 * Not a spec file: holds no test() calls.
 */

'use strict';

/** Open the expanded row for one ticker; returns the detail row locator. */
async function expandPositionRow(page, ticker) {
  const chevron = page.getByRole('button', { name: `Show details for ${ticker}`, exact: true });
  await chevron.waitFor({ state: 'visible', timeout: 8000 });
  if ((await chevron.getAttribute('aria-expanded')) !== 'true') {
    await chevron.click();
  }
  const controls = await chevron.getAttribute('aria-controls');
  const detail = page.locator(`[id="${controls}"]`);
  await detail.waitFor({ state: 'visible', timeout: 5000 });
  return detail;
}

/**
 * Open every row's expanded details. Waits briefly for the rows; when the table
 * renders no rows (empty or error state) it returns without failing, so the
 * calling spec's own assertions decide the outcome.
 */
async function expandAllPositionRows(page) {
  const chevrons = page.locator('[data-testid="position-expand"][aria-expanded="false"]');
  const appeared = await page
    .locator('[data-testid="position-expand"]')
    .first()
    .waitFor({ state: 'visible', timeout: 5000 })
    .then(() => true, () => false);
  if (!appeared) return;
  let n = await chevrons.count();
  while (n > 0) {
    await chevrons.first().click();
    const next = await chevrons.count();
    if (next >= n) break;
    n = next;
  }
}

/** The detail row for a ticker (open it first). */
function positionDetail(page, ticker) {
  return page.locator(`[data-testid="position-detail"][data-detail-for="${ticker}"]`);
}

module.exports = { expandPositionRow, expandAllPositionRows, positionDetail };
