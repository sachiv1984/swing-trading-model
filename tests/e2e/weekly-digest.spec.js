/**
 * E2E: Weekly Digest page — ST-09 (BLG-FEAT-14 FE component, v2.4); readable
 * weekly summary with onward links in v9.18 (ST-14, ST-15, ST-16, EPIC-03),
 * weekly_digest.md v0.5 §2 / WD-01–WD-04.
 *
 * Scenarios:
 *   SC-DIG-01      Page heading
 *   SC-DIG-02a/b   Five plain-language figures; no "Field", "Unit" or "timestamp" text (WD-01, light/dark)
 *   SC-DIG-03      Values: signed GBP, counts, second lines, freshness caption in UTC
 *   SC-DIG-04      Null delta, null staleness and zero values (WD-04)
 *   SC-DIG-05      Error state
 *   SC-DIG-06      No "compliance" label; the page reads the new journal fields (WD-02)
 *   SC-DIG-07      Journal completion uses the closed-trade counts (WD-04; ST-14 ruling)
 *   SC-DIG-08      Realised P&L lands on Performance Summary, Last 7 Days (WD-03)
 *   SC-DIG-09      Journal completion lands on Performance Compliance (WD-03)
 *   SC-DIG-10      Red flags lands on Journal → Red flags (WD-03)
 *   SC-DIG-11      A failed figure shows "Not available" and is not linked
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
    red_flags_7d: 2,
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

const API = "http://localhost:8000";
const figures = (page) => page.getByTestId("digest-figures");
const figure = (page, field) => page.getByTestId(`digest-figure-${field}`);
const link = (page, field) => page.getByTestId(`digest-link-${field}`);

async function serveDigest(page, data) {
  await page.unroute("**/digest/weekly");
  await page.route("**/digest/weekly", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ status: "ok", data: { ...SEED.data, ...data } }),
    })
  );
}

async function gotoDigest(page) {
  await page.goto("/#/WeeklyDigest");
  await expect(figures(page)).toBeVisible({ timeout: 8000 });
}

// SC-DIG-01: Page heading is rendered
test("SC-DIG-01: renders Weekly Digest heading", async ({ page }) => {
  await page.goto('/#/WeeklyDigest');
  // Scope to main to avoid matching the sidebar nav link
  await expect(page.locator('main').getByText("Weekly Digest").first()).toBeVisible({ timeout: 8000 });
});

// SC-DIG-02 (ST-15, WD-01): plain-language figures, no table vocabulary.
for (const theme of ["light", "dark"]) {
  test(`SC-DIG-02${theme === "light" ? "a" : "b"}: five plain-language figures, no Field/Unit/timestamp (${theme})`, async ({ page }) => {
    await page.addInitScript((t) => window.localStorage.setItem("theme", t), theme);
    await gotoDigest(page);
    await expect(figures(page).locator("dt")).toHaveText([
      "Realised P&L, last 7 days",
      "Change in open P&L, last 7 days",
      "Alerts, last 7 days",
      "Journal completion (all closed trades)",
      "Red flags, last 7 days",
    ]);
    const main = page.locator("main");
    await expect(main.locator("table")).toHaveCount(0);
    for (const word of [/\bField\b/, /\bUnit\b/, /timestamp/i, /as_of_utc|_7d\b/]) {
      await expect(main.getByText(word)).toHaveCount(0);
    }
    await expect(main.getByText("Your last 7 days in figures. Most figures link to the page where you review them.")).toBeVisible();
    if (theme === "dark") await expect(page.locator("html")).toHaveClass(/dark/);
  });
}

// SC-DIG-03 (ST-15): values, second lines and the freshness caption.
test("SC-DIG-03: values, second lines and the UTC freshness caption", async ({ page }) => {
  await gotoDigest(page);
  // formatCurrency signed: typographic minus U+2212 before the symbol.
  await expect(figure(page, "realised_pnl_7d").locator("dd")).toHaveText("+£166.10");
  await expect(figure(page, "unrealised_pnl_delta_7d").locator("dd")).toHaveText("−£42.80");
  await expect(link(page, "alerts_fired_7d")).toHaveText("5");
  await expect(link(page, "alerts_fired_7d")).toHaveAttribute("href", "#/notifications?since_days=7");
  await expect(page.getByTestId("digest-second-link-alerts_fired_7d")).toHaveText("3 marked read");
  await expect(page.getByTestId("digest-second-link-alerts_fired_7d")).toHaveAttribute("href", "#/notifications?since_days=7&read=true");
  await expect(figure(page, "journal_completion_rate_current").locator("dd")).toHaveText("80.0%A week ago: 75.0%");
  await expect(link(page, "red_flags_7d")).toHaveText("2");
  // Accessible name "{label}: {value}".
  await expect(page.getByRole("link", { name: "Realised P&L, last 7 days: +£166.10" })).toBeVisible();
  // UTC, not the browser's zone.
  await expect(page.getByTestId("digest-as-of")).toHaveText(
    "Figures as of 1 Apr 2026, 10:30 UTC · portfolio snapshot 18.5 hours old"
  );
});

// SC-DIG-04 (ST-15, WD-04): null delta, no snapshot, and zero values.
test("SC-DIG-04: null delta, no snapshot and zeros", async ({ page }) => {
  await serveDigest(page, {
    unrealised_pnl_delta_7d: null,
    staleness_hours: null,
    realised_pnl_7d: -0.004,
    alerts_fired_7d: 0,
    alerts_dismissed_7d: 0,
    red_flags_7d: 0,
  });
  await gotoDigest(page);
  await expect(figure(page, "unrealised_pnl_delta_7d").locator("dd")).toHaveText("Not enough history yet");
  await expect(figure(page, "realised_pnl_7d").locator("dd")).toHaveText("£0.00");
  await expect(link(page, "alerts_fired_7d")).toHaveText("0");
  await expect(link(page, "red_flags_7d")).toHaveText("0");
  await expect(page.getByTestId("digest-as-of")).toHaveText(/· no portfolio snapshot yet$/);
  await expect(page.locator("main").getByText("—", { exact: true })).toHaveCount(0);
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

// SC-DIG-06 (ST-14, WD-02): no label says "compliance" for the journal
// completion rate, and the page reads the new field names.
test("SC-DIG-06: journal completion rate is not labelled compliance", async ({ page }) => {
  // Deprecated aliases differ on purpose: the page must show the new fields.
  await serveDigest(page, { journal_completion_rate_current: 72.5, compliance_score_current: 11.1 });
  await gotoDigest(page);
  const main = page.locator("main");
  await expect(link(page, "journal_completion_rate_current")).toHaveText("72.5%");
  await expect(main.getByText(/^11\.1%$/)).toHaveCount(0);
  await expect(main.getByText(/compliance/i)).toHaveCount(0);
});

// SC-DIG-07 (ST-14 ruling 2026-11-27): the trade counts tell "no closed
// trades" from "no notes", and a failed query (null) is not shown as 0.
test("SC-DIG-07: journal completion uses the closed-trade counts", async ({ page }) => {
  const row = () => figure(page, "journal_completion_rate_current").locator("dd");

  // Every closed trade is from this week: none before the cutoff.
  await serveDigest(page, { journal_completion_rate_current: 66.7, closed_trades_total: 3,
                            journal_completion_rate_7d_ago: 0.0, closed_trades_total_7d_ago: 0 });
  await gotoDigest(page);
  await expect(row()).toHaveText("66.7%A week ago: no closed trades");

  // No closed trades at all: muted and unlinked.
  await serveDigest(page, { journal_completion_rate_current: 0.0, closed_trades_total: 0,
                            journal_completion_rate_7d_ago: 0.0, closed_trades_total_7d_ago: 0 });
  await page.reload();
  await expect(row()).toHaveText("No closed trades yet", { timeout: 8000 });
  await expect(link(page, "journal_completion_rate_current")).toHaveCount(0);

  // Trades but no notes: a real 0.0%.
  await serveDigest(page, { journal_completion_rate_current: 0.0, closed_trades_total: 3,
                            journal_completion_rate_7d_ago: 0.0, closed_trades_total_7d_ago: 3 });
  await page.reload();
  await expect(row()).toHaveText("0.0%A week ago: 0.0%", { timeout: 8000 });

  // Failed query: null, not zero.
  await serveDigest(page, { journal_completion_rate_current: null, closed_trades_total: null,
                            journal_completion_rate_7d_ago: null, closed_trades_total_7d_ago: null });
  await page.reload();
  await expect(row()).toHaveText("Not available", { timeout: 8000 });
});

// Landing pages (WD-03): answer every other API call with an empty OK so
// Performance and Journal render their sections; the digest stub wins.
async function mockLandingPages(page) {
  await page.route(new RegExp(`${API}/`), (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ status: "ok", data: [] }) })
  );
  await page.route(/localhost:8000\/portfolio\/red-flag-journal/, (route) =>
    route.fulfill({ status: 200, contentType: "application/json",
      body: JSON.stringify({ status: "ok", data: { total: 0, page: 1, page_size: 20, items: [] } }) })
  );
  await serveDigest(page, {});
}

async function headingInView(page, selector) {
  await expect(page.locator(selector)).toBeInViewport({ timeout: 15000 });
}

// SC-DIG-08 (ST-16, WD-03; ruling 2026-11-27): realised P&L lands on
// Performance Summary on the Last 7 Days period, the digest's own window.
test("SC-DIG-08: realised P&L lands on Performance Summary, Last 7 Days", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await mockLandingPages(page);
  await gotoDigest(page);
  await link(page, "realised_pnl_7d").click();
  await expect(page).toHaveURL(/#\/Performance\?section=summary&period=last_7_days$/);
  await expect(page.getByTestId("performance-period")).toHaveText("Last 7 Days", { timeout: 15000 });
  await headingInView(page, "#summary > h2");
});

// SC-DIG-09 (ST-16, WD-03): journal completion lands on Performance Compliance.
test("SC-DIG-09: journal completion lands on Performance Compliance", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await mockLandingPages(page);
  await gotoDigest(page);
  await link(page, "journal_completion_rate_current").click();
  await expect(page).toHaveURL(/#\/Performance\?section=compliance$/);
  await headingInView(page, "#compliance > h2");
  await expect.poll(() => page.evaluate(() => document.activeElement === document.querySelector("#compliance > h2")),
    { timeout: 5000 }).toBe(true);
});

// SC-DIG-10 (ST-16, WD-03): red flags lands on Journal → Red flags.
test("SC-DIG-10: red flags lands on Journal, Red flags tab", async ({ page }) => {
  await mockLandingPages(page);
  await gotoDigest(page);
  await link(page, "red_flags_7d").click();
  await expect(page).toHaveURL(/#\/Journal\?section=red-flags$/);
  await expect(page.getByRole("tab", { name: /^Red flags( \(\d+\))?$/ })).toHaveAttribute("aria-selected", "true", { timeout: 15000 });
});

// SC-DIG-11: a figure whose query failed (null) says so and is never linked.
test("SC-DIG-11: a failed figure shows Not available and is not linked", async ({ page }) => {
  await serveDigest(page, { red_flags_7d: null, alerts_fired_7d: null, alerts_dismissed_7d: null });
  await gotoDigest(page);
  await expect(figure(page, "red_flags_7d").locator("dd")).toHaveText("Not available");
  await expect(figure(page, "alerts_fired_7d").locator("dd")).toHaveText("Not available");
  await expect(link(page, "red_flags_7d")).toHaveCount(0);
  await expect(link(page, "alerts_fired_7d")).toHaveCount(0);
  await expect(link(page, "realised_pnl_7d")).toHaveCount(1);
});
