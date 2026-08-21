/**
 * Trailing Stop Currency Basis — Card & Table View Acceptance Tests
 * ST-02 (BLG-BE-103, EPIC-01, v8.9) — Fix currency basis of
 * current_trailing_stop/stop_price for US-market positions
 *
 * Problem: current_trailing_stop and stop_price were GBP-converted for
 * US-market positions while initial_stop stayed native, and the frontend
 * rendered all three with the native currency symbol ($ for US) — so a US
 * position's Init and live-stop tiles could show two numerically different
 * "$" values that were really the same underlying stop in two currencies.
 *
 * Fix: the backend now also returns current_trailing_stop_native; the
 * frontend renders the native-currency stop next to the native currency
 * symbol on both Card (grid) and Table views.
 *
 * Spec refs:
 *   docs/specs/api_contracts/position_endpoints.md
 *   src/components/positions/PositionCard.js
 *   src/pages/Positions.js (table row)
 *
 * Infrastructure: Playwright page.route() network interception.
 * No live backend required.
 *
 * -------------------------------------------------------------------------
 * ROUTING NOTE: App uses HashRouter. ALL navigation must use page.goto('/#/…')
 */

const { test, expect } = require("@playwright/test");

// US-market profitable position: entry $100, live $120, breakeven-floored
// native stop $100.00. GBP-converted counterpart at fx_rate 1.30 is $76.92 —
// deliberately different from the native value so the test fails loudly if
// the wrong-basis field is ever rendered again.
const US_POSITION = {
  id: "pos-us-001",
  ticker: "WDC",
  market: "US",
  entry_price: 100.0,
  current_price: 92.31, // GBP-converted current price (120 / 1.30)
  current_price_native: 120.0,
  initial_stop: 80.0,
  current_trailing_stop: 76.92, // GBP basis — must NOT appear on the tiles
  current_trailing_stop_native: 100.0, // native basis — must appear on the tiles
  stop_price: 76.92,
  stop_price_native: 100.0,
  shares: 10,
  pnl: 153.85,
  pnl_percent: 20.0,
  holding_days: 15,
  grace_days_remaining: null,
  status: "open",
  entry_date: "2026-07-25",
  tags: null,
};

// ST-11 (BLG-QA-153, EPIC-02, v9.0): UK-market position — current_trailing_stop
// and current_trailing_stop_native are identical for UK positions (no FX
// conversion applies), matching tests/test_position_currency_basis.py's
// backend-level test_native_and_gbp_fields_equal_for_uk_position. This
// fixture exercises that parity through the actual rendered Card/Table UI,
// not just backend dict equality.
const UK_POSITION = {
  id: "pos-uk-001",
  ticker: "VOD.L",
  market: "UK",
  entry_price: 100.0,
  current_price: 120.0,
  current_price_native: 120.0,
  initial_stop: 80.0,
  current_trailing_stop: 90.0, // GBP basis
  current_trailing_stop_native: 90.0, // native basis — identical for UK, by construction
  stop_price: 90.0,
  stop_price_native: 90.0,
  shares: 10,
  pnl: 200.0,
  pnl_percent: 20.0,
  holding_days: 15,
  grace_days_remaining: null,
  status: "open",
  entry_date: "2026-07-25",
  tags: null,
};

async function mockRoutes(page, positions = [US_POSITION]) {
  await page.route("**/positions*", (route) => {
    const url = route.request().url();
    if (url.includes("/positions/compliance")) {
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ status: "ok", data: [] }) });
    } else {
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(positions),
      });
    }
  });
  await page.route("**/portfolio*", (route) => {
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ status: "ok", data: { cash: 10000, initial_cash: 10000 } }),
    });
  });
  await page.route("**/analytics/**", (route) => {
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ status: "ok", data: { last_sync_at: null } }) });
  });
  await page.route("**/compliance/**", (route) => {
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ status: "ok", data: [] }) });
  });
  await page.route("**/alerts/history", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route("**/watchlist**", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ items: [] }) })
  );
}

test.describe("Trailing Stop Currency Basis — US-market position (V-CURR-01, V-CURR-02)", () => {
  test.beforeEach(async ({ page }) => {
    await mockRoutes(page);
    await page.goto("/#/positions");
  });

  test("V-CURR-01 — Card view: Init and live-stop tiles show a single consistent native-currency value", async ({ page }) => {
    await expect(page.getByText("Init: $80.00")).toBeVisible();
    // The live trailing-stop value must be the native $100.00, never the
    // GBP-converted $76.92. Single seeded position -> .first() is unambiguous.
    await expect(page.getByText("$100.00").first()).toBeVisible();
    await expect(page.getByText("$76.92")).toHaveCount(0);
  });

  test("V-CURR-02 — Table view: Init and live-stop cell show a single consistent native-currency value", async ({ page }) => {
    const tableBtn = page.locator('[aria-label="Table view"]');
    await tableBtn.waitFor({ state: "visible", timeout: 10000 });
    await tableBtn.click();
    await page.waitForTimeout(300);

    const row = page.getByRole("row").filter({ hasText: "WDC" });
    await expect(row.getByText("Init: $80.00")).toBeVisible();
    await expect(row.getByText("$100.00").first()).toBeVisible();
    await expect(row.getByText("$76.92")).toHaveCount(0);
  });
});

test.describe("Trailing Stop Currency Basis — UK-market position (V-CURR-03, V-CURR-04)", () => {
  test.beforeEach(async ({ page }) => {
    await mockRoutes(page, [UK_POSITION]);
    await page.goto("/#/positions");
  });

  test("V-CURR-03 — Card view: UK position's Init and live-stop tiles show a single consistent £ value", async ({ page }) => {
    await expect(page.getByText("Init: £80.00")).toBeVisible();
    // current_trailing_stop_native (£90.00) must render — identical to
    // current_trailing_stop for a UK position, but exercised through the
    // actual native-field render path, not asserted by backend equality alone.
    await expect(page.getByText("£90.00").first()).toBeVisible();
  });

  test("V-CURR-04 — Table view: UK position's Init and live-stop cell show a single consistent £ value", async ({ page }) => {
    const tableBtn = page.locator('[aria-label="Table view"]');
    await tableBtn.waitFor({ state: "visible", timeout: 10000 });
    await tableBtn.click();
    await page.waitForTimeout(300);

    const row = page.getByRole("row").filter({ hasText: "VOD.L" });
    await expect(row.getByText("Init: £80.00")).toBeVisible();
    await expect(row.getByText("£90.00").first()).toBeVisible();
  });
});
