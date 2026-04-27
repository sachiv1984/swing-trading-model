/**
 * Positions Table View — P&L Column Acceptance Tests
 * ST-04 (BLG-FE-06, v2.4) — Fix missing P&L (GBP) column on Positions page
 * Covers: V-PATH2-01
 *
 * Spec refs:
 *   docs/specs/frontend/pages/positions.md §Table View
 *   docs/specs/frontend/pages/positions.md §DEV-EPIC02-ST05-03 (resolved)
 *
 * What these tests cover:
 *   V-PATH2-01  Table View renders separate P&L (GBP) and P&L % columns
 *   V-PATH2-02  Positive P&L values render in green (emerald-400)
 *   V-PATH2-03  Negative P&L values render in red (rose-400)
 *   V-PATH2-04  P&L (GBP) column shows absolute £ value; P&L % shows percentage
 *
 * What requires DoQ manual visual verification (not covered here):
 *   - Exact £70.05 and £96.05 values on staging with seed data
 *   - Colour rendering (emerald vs rose) — CSS class applied but rendering is visual
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

const { test, expect } = require("@playwright/test");

const SEED_POSITIONS = [
  {
    id: "pos-001",
    ticker: "LGEN",
    market: "UK",
    entry_price: 2.40,
    current_price: 2.50,
    current_price_native: 2.50,
    stop_price: 2.20,
    stop_price_native: 2.20,
    shares: 300,
    pnl: 70.05,
    pnl_percent: 4.17,
    holding_days: 5,
    grace_days_remaining: null,
    status: "open",
    entry_date: "2026-03-20",
    initial_stop: 2.20,
    tags: null,
  },
  {
    id: "pos-002",
    ticker: "BARC",
    market: "UK",
    entry_price: 1.85,
    current_price: 2.10,
    current_price_native: 2.10,
    stop_price: 1.65,
    stop_price_native: 1.65,
    shares: 400,
    pnl: 96.05,
    pnl_percent: 13.65,
    holding_days: 8,
    grace_days_remaining: null,
    status: "open",
    entry_date: "2026-03-15",
    initial_stop: 1.65,
    tags: null,
  },
  {
    id: "pos-003",
    ticker: "TSCO",
    market: "UK",
    entry_price: 3.10,
    current_price: 2.90,
    current_price_native: 2.90,
    stop_price: 2.80,
    stop_price_native: 2.80,
    shares: 200,
    pnl: -38.50,
    pnl_percent: -6.21,
    holding_days: 12,
    grace_days_remaining: null,
    status: "open",
    entry_date: "2026-03-10",
    initial_stop: 2.80,
    tags: null,
  },
];

async function mockRoutes(page) {
  await page.route("**/positions*", (route) => {
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ status: "ok", data: { positions: SEED_POSITIONS } }),
    });
  });
  await page.route("**/portfolio*", (route) => {
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ status: "ok", data: { cash: 10000, initial_cash: 10000 } }),
    });
  });
  await page.route("**/analytics/**", (route) => {
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ status: "ok", data: { last_sync_at: null } }),
    });
  });
  await page.route("**/compliance/**", (route) => {
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ status: "ok", data: [] }) });
  });
  // Stub Layout-level endpoints so sidebar badge doesn't cause unhandled network errors
  await page.route("**/alerts/history", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route("**/watchlist**", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ items: [] }) })
  );
}

test.describe("Positions Table View — P&L Columns (V-PATH2-01 to V-PATH2-04)", () => {
  test.beforeEach(async ({ page }) => {
    await mockRoutes(page);
    await page.goto("/#/positions");
    await page.waitForLoadState('networkidle');
    // Switch to Table View — button has aria-label="Table view"
    await page.getByRole("button", { name: /table view/i }).click();
    await page.waitForTimeout(300); // allow React re-render after view switch
  });

  test("V-PATH2-01 — Table View has separate P&L (GBP) and P&L % column headers", async ({ page }) => {
    await expect(page.getByRole("columnheader", { name: "P&L (GBP)" })).toBeVisible();
    await expect(page.getByRole("columnheader", { name: "P&L %" })).toBeVisible();
  });

  test("V-PATH2-02 — Positive P&L rows have emerald colour class applied", async ({ page }) => {
    // LGEN: pnl = 70.05 (positive)
    const lgenRow = page.getByRole("row").filter({ hasText: "LGEN" });
    const pnlCell = lgenRow.getByText("£70.05");
    await expect(pnlCell).toBeVisible();
    // Parent should have emerald colour class
    const pnlDiv = pnlCell.locator("..");
    await expect(pnlDiv).toHaveClass(/text-emerald-400/);
  });

  test("V-PATH2-03 — Negative P&L rows have rose colour class applied", async ({ page }) => {
    // TSCO: pnl = -38.50 (negative)
    const tscoRow = page.getByRole("row").filter({ hasText: "TSCO" });
    const pnlCell = tscoRow.getByText("£38.50");
    await expect(pnlCell).toBeVisible();
    const pnlDiv = pnlCell.locator("..");
    await expect(pnlDiv).toHaveClass(/text-rose-400/);
  });

  test("V-PATH2-04 — P&L (GBP) and P&L % display in separate cells", async ({ page }) => {
    const barcRow = page.getByRole("row").filter({ hasText: "BARC" });
    // GBP value in its own cell
    await expect(barcRow.getByText("£96.05")).toBeVisible();
    // Percentage in separate cell
    await expect(barcRow.getByText(/\+13\.6%/)).toBeVisible();
  });
});
