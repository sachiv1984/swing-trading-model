/**
 * E2E: Weekly Digest page — ST-09 (BLG-FEAT-14 FE component, v2.4)
 *
 * Scenarios: SC-DIG-01 through SC-DIG-05
 */
import { test, expect } from "@playwright/test";

const DIGEST_URL = "/digest/weekly";
const SEED = {
  status: "ok",
  data: {
    realised_pnl_7d: 166.10,
    unrealised_pnl_delta_7d: -42.80,
    alerts_fired_7d: 5,
    alerts_dismissed_7d: 3,
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
  await expect(page.getByText("Compliance Score (current)")).toBeVisible();
  await expect(page.getByText("Compliance Score (7d ago)")).toBeVisible();
  await expect(page.getByText("Data Staleness")).toBeVisible();
  await expect(page.getByText("As of (UTC)")).toBeVisible();
});

// SC-DIG-03: Numeric values are rendered correctly
test("SC-DIG-03: numeric values formatted from API response", async ({ page }) => {
  await page.goto('/#/WeeklyDigest');
  // Scope numeric checks to table cells to avoid matching badges/nav elements
  await expect(page.locator('td').filter({ hasText: /^£166\.10$/ }).first()).toBeVisible({ timeout: 8000 });
  await expect(page.locator('td').filter({ hasText: /^£-42\.80$/ }).first()).toBeVisible();
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
