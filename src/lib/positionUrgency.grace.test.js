// ST-10 (BLG-FE-308, EPIC-02, v9.18): one grace definition across the Dashboard
// (dashboard.md v4.4 §4B; design record dashboard-quiet-day §3). Expected values
// are written from the spec's worked table, not from the code.
import {
  isInGrace,
  graceDaysRemaining,
  isGraceEndingToday,
  isGraceEndingWithin,
  minGraceDaysRemaining,
  nextEndsText,
} from "./positionUrgency";

// §4B worked rows A–E.
const A = { ticker: "A", grace_period: true, grace_days_remaining: 10, status: "GRACE" }; // held 0 days
const B = { ticker: "B", grace_period: true, grace_days_remaining: 1, status: "GRACE" }; // held 9 days
const C = { ticker: "C", grace_period: false, grace_days_remaining: null, status: "GRACE" }; // held 10, stale status
const D = { ticker: "D", grace_period: true, grace_days_remaining: 2, status: "OPEN" }; // held 8, lagging status
const E = { ticker: "E", grace_period: false, grace_days_remaining: null, status: "PROFITABLE" }; // held 30
const FIVE = [A, B, C, D, E];

describe("§4B worked table", () => {
  test("every grace count is 3 (A, B, D)", () => {
    expect(FIVE.filter(isInGrace).map((p) => p.ticker)).toEqual(["A", "B", "D"]);
  });
  test("grace ends today: B only", () => {
    expect(FIVE.filter(isGraceEndingToday).map((p) => p.ticker)).toEqual(["B"]);
  });
  test("ending within 2 days: B and D", () => {
    expect(FIVE.filter((p) => isGraceEndingWithin(p, 2)).map((p) => p.ticker)).toEqual(["B", "D"]);
  });
  test("Card 3 reads \"Ends today\" (minimum remaining 1)", () => {
    expect(minGraceDaysRemaining(FIVE)).toBe(1);
    expect(nextEndsText(minGraceDaysRemaining(FIVE))).toBe("Ends today");
  });
});

describe("graceDaysRemaining — only an in-grace position's finite day count", () => {
  test.each([
    // [grace_period, grace_days_remaining, expected]
    [true, 3, 3],
    [true, "3", 3], // numeric string
    [true, 0, 0],
    [true, -1, -1],
    [true, null, null], // in grace, no day count: counted in grace, no "ends" text
    [true, undefined, null],
    [true, "", null],
    [true, "abc", null], // non-numeric string
    [true, " ", null], // whitespace is not 0
    [true, " 4 ", 4],
    [true, true, null], // a boolean is not 1
    [true, Infinity, null],
    [false, 1, null], // disagreeing row: not in grace, so its day count is ignored
    [null, 1, null],
    ["true", 1, null], // only a real boolean true is in grace
  ])("grace_period=%p remaining=%p → %p", (gp, days, expected) => {
    expect(graceDaysRemaining({ grace_period: gp, grace_days_remaining: days })).toBe(expected);
  });
  test("a missing position is not in grace", () => {
    expect(graceDaysRemaining(null)).toBeNull();
    expect(graceDaysRemaining(undefined)).toBeNull();
  });
});

describe("isGraceEndingToday and isGraceEndingWithin at the boundaries", () => {
  test.each([
    // [days, endsToday, within2]
    [null, false, false],
    [0, false, false], // grace has ended: not "ending"
    [-1, false, false],
    [1, true, true],
    [2, false, true],
    [3, false, false],
    ["1", true, true],
  ])("in grace, %p days left → today %p, within 2 %p", (days, today, within2) => {
    const p = { grace_period: true, grace_days_remaining: days };
    expect(isGraceEndingToday(p)).toBe(today);
    expect(isGraceEndingWithin(p, 2)).toBe(within2);
  });
  test("a row with grace_period false and 1 day left is neither", () => {
    const p = { grace_period: false, grace_days_remaining: 1 };
    expect(isGraceEndingToday(p)).toBe(false);
    expect(isGraceEndingWithin(p, 2)).toBe(false);
  });
});

describe("minGraceDaysRemaining", () => {
  test.each([
    [[], null],
    [null, null],
    [[{ grace_period: true, grace_days_remaining: null }], null], // in grace, no day count
    [[{ grace_period: false, grace_days_remaining: 1 }, { grace_period: true, grace_days_remaining: 4 }], 4],
    [[{ grace_period: true, grace_days_remaining: 7 }, { grace_period: true, grace_days_remaining: 3 }], 3],
  ])("%j → %p", (positions, expected) => {
    expect(minGraceDaysRemaining(positions)).toBe(expected);
  });
});

describe("nextEndsText (risk_dashboard.md §5.2)", () => {
  test.each([
    [null, null],
    [undefined, null],
    [-1, "Grace period has ended"],
    [0, "Grace period has ended"],
    [1, "Ends today"],
    [2, "Next ends in 1 day"],
    [3, "Next ends in 2 days"],
    [10, "Next ends in 9 days"],
  ])("%p → %p", (days, text) => {
    expect(nextEndsText(days)).toBe(text);
  });
});
