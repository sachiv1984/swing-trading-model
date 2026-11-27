import { digestFigures, formatAsOfUtc, freshnessCaption, DIGEST_LINKS } from "./weeklyDigest";

// Real-shaped: the keys and types _fetch_weekly_digest_data returns.
const BASE = {
  realised_pnl_7d: 166.1,
  unrealised_pnl_delta_7d: -42.8,
  alerts_fired_7d: 5,
  alerts_dismissed_7d: 3,
  journal_completion_rate_current: 72.5,
  journal_completion_rate_7d_ago: 70.3,
  closed_trades_total: 40,
  closed_trades_total_7d_ago: 37,
  compliance_score_current: 72.5,
  compliance_score_7d_ago: 70.3,
  red_flags_7d: 2,
  staleness_hours: 18.5,
  as_of_utc: "2026-11-27T14:15:06.123456+00:00",
};

const row = (data, field) => digestFigures(data).find((r) => r.field === field);

describe("digestFigures order and labels", () => {
  test("five rows in spec order, no 'compliance' label", () => {
    const rows = digestFigures(BASE);
    expect(rows.map((r) => r.label)).toEqual([
      "Realised P&L, last 7 days",
      "Change in open P&L, last 7 days",
      "Alerts, last 7 days",
      "Journal completion (all closed trades)",
      "Red flags, last 7 days",
    ]);
    rows.forEach((r) => expect(r.label.toLowerCase()).not.toContain("compliance"));
  });
});

describe("realised P&L", () => {
  test.each([
    ["gain", 166.1, "+£166.10", false],
    ["loss", -42.8, "−£42.80", false],
    ["zero is a value, unsigned", 0, "£0.00", false],
    ["rounds to zero", -0.004, "£0.00", false],
    ["null", null, "Not available", true],
    ["missing", undefined, "Not available", true],
  ])("%s", (_l, v, text, muted) => {
    const r = row({ ...BASE, realised_pnl_7d: v }, "realised_pnl_7d");
    expect(r.value).toBe(text);
    expect(r.muted).toBe(muted);
    expect(r.href).toBe(muted ? null : DIGEST_LINKS.realised_pnl_7d);
  });

  test("links to Performance Summary on the Last 7 Days period", () => {
    expect(DIGEST_LINKS.realised_pnl_7d).toBe("/Performance?section=summary&period=last_7_days");
  });
});

describe("change in open P&L", () => {
  test.each([
    [-42.8, "−£42.80", false],
    [12.5, "+£12.50", false],
    [0, "£0.00", false],
    [null, "Not enough history yet", true],
  ])("%p", (v, text, muted) => {
    const r = row({ ...BASE, unrealised_pnl_delta_7d: v }, "unrealised_pnl_delta_7d");
    expect(r).toMatchObject({ value: text, muted, href: null });
  });
});

describe("alerts", () => {
  test.each([
    [5, 3, "5", "3 marked read"],
    [0, 0, "0", "0 marked read"],
    [1, 1, "1", "1 marked read"],
  ])("fired %p read %p", (fired, read, text, second) => {
    const r = row({ ...BASE, alerts_fired_7d: fired, alerts_dismissed_7d: read }, "alerts_fired_7d");
    expect(r.value).toBe(text);
    expect(r.href).toBe("/notifications?since_days=7");
    expect(r.secondLine).toEqual({ text: second, href: "/notifications?since_days=7&read=true" });
  });

  test("null count is not linked", () => {
    const r = row({ ...BASE, alerts_fired_7d: null, alerts_dismissed_7d: null }, "alerts_fired_7d");
    expect(r).toMatchObject({ value: "Not available", muted: true, href: null, secondLine: null });
  });
});

describe("journal completion (ST-14 counts)", () => {
  test.each([
    // label, overrides, value, muted, linked, second line
    ["normal", {}, "72.5%", false, true, "A week ago: 70.3%"],
    ["no closed trades", { journal_completion_rate_current: 0, closed_trades_total: 0, journal_completion_rate_7d_ago: 0, closed_trades_total_7d_ago: 0 }, "No closed trades yet", true, false, null],
    ["trades, no notes", { journal_completion_rate_current: 0, closed_trades_total: 3, journal_completion_rate_7d_ago: 0, closed_trades_total_7d_ago: 3 }, "0.0%", false, true, "A week ago: 0.0%"],
    ["every trade this week", { journal_completion_rate_current: 66.7, closed_trades_total: 3, journal_completion_rate_7d_ago: 0, closed_trades_total_7d_ago: 0 }, "66.7%", false, true, "A week ago: no closed trades"],
    ["one trade, 100%", { journal_completion_rate_current: 100, closed_trades_total: 1, journal_completion_rate_7d_ago: 100, closed_trades_total_7d_ago: 1 }, "100.0%", false, true, "A week ago: 100.0%"],
    ["query failed", { journal_completion_rate_current: null, closed_trades_total: null }, "Not available", true, false, null],
    ["7d-ago query failed", { journal_completion_rate_7d_ago: null, closed_trades_total_7d_ago: null }, "72.5%", false, true, null],
    ["deprecated aliases are not read", { compliance_score_current: 11.1 }, "72.5%", false, true, "A week ago: 70.3%"],
  ])("%s", (_l, over, value, muted, linked, second) => {
    const r = row({ ...BASE, ...over }, "journal_completion_rate_current");
    expect(r.value).toBe(value);
    expect(r.muted).toBe(muted);
    expect(r.href).toBe(linked ? "/Performance?section=compliance" : null);
    expect(r.secondLine?.text ?? null).toBe(second);
  });
});

describe("red flags", () => {
  test.each([
    [2, "2", "/Journal?section=red-flags"],
    [0, "0", "/Journal?section=red-flags"],
    [null, "Not available", null],
  ])("%p", (v, text, href) => {
    expect(row({ ...BASE, red_flags_7d: v }, "red_flags_7d")).toMatchObject({ value: text, href });
  });
});

describe("formatAsOfUtc", () => {
  test.each([
    ["afternoon", "2026-11-27T14:15:06.123456+00:00", "27 Nov 2026, 14:15"],
    ["UTC midnight stays the same day", "2026-11-27T00:00:00+00:00", "27 Nov 2026, 00:00"],
    ["offset input is shown in UTC", "2026-11-27T00:30:00+01:00", "26 Nov 2026, 23:30"],
    ["null", null, null],
    ["garbage", "not a date", null],
  ])("%s", (_l, iso, text) => {
    expect(formatAsOfUtc(iso)).toBe(text);
  });
});

describe("freshnessCaption", () => {
  test.each([
    ["with snapshot", {}, "Figures as of 27 Nov 2026, 14:15 UTC · portfolio snapshot 18.5 hours old"],
    ["whole hours keep 1 dp", { staleness_hours: 2 }, "Figures as of 27 Nov 2026, 14:15 UTC · portfolio snapshot 2.0 hours old"],
    ["no snapshot", { staleness_hours: null }, "Figures as of 27 Nov 2026, 14:15 UTC · no portfolio snapshot yet"],
  ])("%s", (_l, over, text) => {
    expect(freshnessCaption({ ...BASE, ...over })).toBe(text);
  });

  test("no raw ISO and no 'timestamp' text", () => {
    const text = freshnessCaption(BASE);
    expect(text).not.toMatch(/T\d\d:|\+00:00|timestamp/i);
  });
});
