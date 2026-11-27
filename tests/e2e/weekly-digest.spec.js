/**
 * E2E: Weekly Digest page — ST-09 (BLG-FEAT-14 FE component, v2.4)
 *
 * Scenarios: SC-DIG-01 through SC-DIG-07
 */
import { test, expect } from "./fixtures/api-status-guard";

const DIGEST_URL = "/digest/weekly";
const SEED = {
  status: "ok",
  data: {
    realised_pnl_7d: 166.10,
    unrealised_pnl_delta_7d: -42.80,
    alerts_fired_7d: 5,
    alerts_dismissed_7d: 3,
    journal_completion_rate_current: 80.0,
    journal_completion_rate_7d_ago: 75.0,
    closed_trades_total: 20,
    closed_trades_total_7d_ago: 16,
    compliance_score_current: 80.0,
    compliance_score_7d_ago: 75.0,
    staleness_hours: 18.5,
    as_of_utc: "2026-04-01T10:30:00+00:00",
  },
};

test.beforeEach(async ({ page }) => {
  await page.route("**/digest/weekly", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(SEED) })
  );
  // Stub Layout-level endpoints so the sidebar doesn't block rendering
  await page.route("**/alerts/history", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ data: { evaluations: [] } }) })
  );
  await page.route("**/watchlist**", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ items: [] }) })
  );
  await page.route("**/portfolio/positions**", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ data: { positions: [] } }) })
  );
});

// SC-DIG-01: Page heading is rendered
test("SC-DIG-01: renders Weekly Digest heading", async ({ page }) => {
  await page.goto('/#/WeeklyDigest');
  // Scope to main to avoid matching the sidebar nav link
  await expect(page.locator('main').getByText("Weekly Digest").first()).toBeVisible({ timeout: 8000 });
});

// SC-DIG-02: Table contains all 8 field rows with values from API response
test("SC-DIG-02: all 8 digest fields are displayed", async ({ page }) => {
  await page.goto('/#/WeeklyDigest');
  await expect(page.getByText("Realised P&L (7d)")).toBeVisible({ timeout: 8000 });
  await expect(page.getByText("Unrealised P&L Delta (7d)")).toBeVisible();
  await expect(page.getByText("Alerts Fired (7d)")).toBeVisible();
  await expect(page.getByText("Alerts Dismissed (7d)")).toBeVisible();
  await expect(page.getByText("Journal completion (all closed trades)")).toBeVisible();
  await expect(page.getByText("Journal completion (a week ago)")).toBeVisible();
  await expect(page.getByText("Data Staleness")).toBeVisible();
  await expect(page.getByText("As of (UTC)")).toBeVisible();
});

// SC-DIG-03: Numeric values are rendered correctly
test("SC-DIG-03: numeric values formatted from API response", async ({ page }) => {
  await page.goto('/#/WeeklyDigest');
  // Scope numeric checks to table cells to avoid matching badges/nav elements
  await expect(page.locator('td').filter({ hasText: /^£166\.10$/ }).first()).toBeVisible({ timeout: 8000 });
  // ST-01 (EPIC-01, v9.8): renders via the shared formatCurrency helper — typographic minus
  // U+2212 placed BEFORE the currency symbol, not an ASCII hyphen after it.
  await expect(page.locator('td').filter({ hasText: /^−£42\.80$/ }).first()).toBeVisible();
  await expect(page.locator('td').filter({ hasText: /^5$/ }).first()).toBeVisible();
  await expect(page.locator('td').filter({ hasText: /^3$/ }).first()).toBeVisible();
  await expect(page.locator('td').filter({ hasText: /^80\.0%$/ }).first()).toBeVisible();
  await expect(page.locator('td').filter({ hasText: /^75\.0%$/ }).first()).toBeVisible();
  await expect(page.locator('td').filter({ hasText: /^18\.5 h$/ }).first()).toBeVisible();
});

// SC-DIG-04: Null fields show em-dash fallback
test("SC-DIG-04: null unrealised_pnl_delta_7d renders em-dash", async ({ page }) => {
  await page.route("**/digest/weekly", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        status: "ok",
        data: { ...SEED.data, unrealised_pnl_delta_7d: null, staleness_hours: null },
      }),
    })
  );
  await page.goto('/#/WeeklyDigest');
  await expect(page.locator('table').first()).toBeVisible({ timeout: 8000 });
  // null values render as em-dash in td cells
  const cells = await page.locator('td').filter({ hasText: /^—$/ }).all();
  expect(cells.length).toBeGreaterThanOrEqual(2);
});

// SC-DIG-05: API error state is shown
test("SC-DIG-05: error state rendered on API failure", async ({ page }) => {
  await page.route("**/digest/weekly", (route) =>
    route.fulfill({ status: 500, contentType: "application/json", body: JSON.stringify({ status: "error" }) })
  );
  await page.goto('/#/WeeklyDigest');
  // DataState renders "Try again" button on error
  await expect(page.getByRole("button", { name: /try again/i })).toBeVisible({ timeout: 8000 });
});

// SC-DIG-06 (ST-14, EPIC-03, v9.18, BLG-SPEC-204): no label says "compliance"
// for the journal completion rate, and the page reads the new field names.
test("SC-DIG-06: journal completion rate is not labelled compliance", async ({ page }) => {
  await page.route("**/digest/weekly", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        status: "ok",
        // Deprecated aliases differ on purpose: the page must show the new fields.
        data: { ...SEED.data, journal_completion_rate_current: 72.5, compliance_score_current: 11.1 },
      }),
    })
  );
  await page.goto('/#/WeeklyDigest');
  const main = page.locator('main');
  await expect(main.getByText("Journal completion (all closed trades)")).toBeVisible({ timeout: 8000 });
  await expect(main.getByText(/^72\.5%$/)).toBeVisible();
  await expect(main.getByText(/^11\.1%$/)).toHaveCount(0);
  await expect(main.getByText(/compliance/i)).toHaveCount(0);
});

// SC-DIG-07 (ST-14, ruling 2026-11-27): the trade counts tell "no closed
// trades" from "no notes", and a failed query (null) is not shown as 0.
test("SC-DIG-07: journal completion uses the closed-trade counts", async ({ page }) => {
  const serve = (data) =>
    page.route("**/digest/weekly", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ status: "ok", data: { ...SEED.data, ...data } }),
      })
    );
  const main = page.locator("main");

  // Every closed trade is from this week: none before the cutoff.
  await serve({ journal_completion_rate_current: 66.7, closed_trades_total: 3,
                journal_completion_rate_7d_ago: 0.0, closed_trades_total_7d_ago: 0 });
  await page.goto("/#/WeeklyDigest");
  await expect(main.getByText(/^66\.7%$/)).toBeVisible({ timeout: 8000 });
  await expect(main.getByText("No closed trades", { exact: true })).toBeVisible();
  await expect(main.getByText(/^0\.0%$/)).toHaveCount(0);

  // No closed trades at all.
  await page.unroute("**/digest/weekly");
  await serve({ journal_completion_rate_current: 0.0, closed_trades_total: 0,
                journal_completion_rate_7d_ago: 0.0, closed_trades_total_7d_ago: 0 });
  await page.reload();
  await expect(main.getByText("No closed trades yet", { exact: true })).toBeVisible({ timeout: 8000 });
  await expect(main.getByText(/^0\.0%$/)).toHaveCount(0);

  // Trades but no notes: a real 0.0%.
  await page.unroute("**/digest/weekly");
  await serve({ journal_completion_rate_current: 0.0, closed_trades_total: 3,
                journal_completion_rate_7d_ago: 0.0, closed_trades_total_7d_ago: 3 });
  await page.reload();
  await expect(main.getByText(/^0\.0%$/)).toHaveCount(2, { timeout: 8000 });

  // Failed query: null, not zero.
  await page.unroute("**/digest/weekly");
  await serve({ journal_completion_rate_current: null, closed_trades_total: null,
                journal_completion_rate_7d_ago: null, closed_trades_total_7d_ago: null });
  await page.reload();
  await expect(main.getByText("Not available", { exact: true })).toHaveCount(2, { timeout: 8000 });
  await expect(main.getByText(/no closed trades/i)).toHaveCount(0);
});
