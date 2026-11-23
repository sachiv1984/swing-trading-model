// ST-19 (BLG-QA-262, EPIC-04, v9.18): table-driven unit tests for the urgency
// order (positions.md §Decision-First Table). Each input is tried as null,
// missing, a numeric string, a non-numeric string, 0 and a negative number.
// Known bugs are recorded with knownFailing (src/test-utils/knownFailing.js)
// and the backlog item that fixes them.
import {
  URGENCY_TIER,
  NEAR_STOP_PCT,
  isInGrace,
  stopDistancePct,
  stopDistanceR,
  getUrgencyTier,
  sortByUrgency,
  compareByUrgency,
  stopDistanceClass,
  formatStopDistance,
} from "./positionUrgency";
import { knownFailing } from "../test-utils/knownFailing";

// A US position out of grace: GBP fields on the breach/percentage basis, native
// fields on the R basis (current_trailing_stop = native ÷ 1.30 FX). Price is 10%
// above the stop; R = (130 − 117) ÷ (120 − 110) = 1.3.
function pos(overrides = {}) {
  return {
    ticker: "AAA",
    market: "US",
    grace_period: false,
    risk_off_exit: false,
    current_price: 100,
    current_trailing_stop: 90,
    current_price_native: 130,
    current_trailing_stop_native: 117,
    entry_price: 120,
    initial_stop: 110,
    ...overrides,
  };
}

function without(field) {
  const p = pos();
  delete p[field];
  return p;
}

describe("stopDistancePct", () => {
  test("base case: (100 − 90) ÷ 100 × 100 = 10", () => {
    expect(stopDistancePct(pos())).toBeCloseTo(10);
  });

  test.each([
    ["current_price", null, null],
    ["current_price", undefined, null],
    ["current_price", "", null],
    ["current_price", "100", 10],
    ["current_price", "abc", null],
    ["current_price", 0, null],
    ["current_price", -5, null],
    ["current_trailing_stop", null, null],
    ["current_trailing_stop", "", null],
    ["current_trailing_stop", "90", 10],
    ["current_trailing_stop", "abc", null],
    ["current_trailing_stop", 0, null],
    ["current_trailing_stop", -1, null],
  ])("%s = %p → %p", (field, value, expected) => {
    const result = stopDistancePct(pos({ [field]: value }));
    if (expected === null) expect(result).toBeNull();
    else expect(result).toBeCloseTo(expected);
  });

  test.each([["current_price"], ["current_trailing_stop"]])("missing %s → null", (field) => {
    expect(stopDistancePct(without(field))).toBeNull();
  });

  test("price below the stop is negative", () => {
    expect(stopDistancePct(pos({ current_price: 80 }))).toBeCloseTo(-12.5);
  });

  test.each([[null], [undefined], [{}]])("position %p → null", (p) => {
    expect(stopDistancePct(p)).toBeNull();
  });
});

describe("stopDistanceR", () => {
  test("base case: (130 − 117) ÷ (120 − 110) = 1.3", () => {
    expect(stopDistanceR(pos())).toBeCloseTo(1.3);
  });

  const FIELDS = ["current_price_native", "current_trailing_stop_native", "entry_price", "initial_stop"];

  test.each(FIELDS.flatMap((f) => [[f, null], [f, undefined], [f, ""], [f, "abc"]]))("%s = %p → null", (field, value) => {
    expect(stopDistanceR(pos({ [field]: value }))).toBeNull();
  });

  test.each(FIELDS)("missing %s → null", (field) => {
    expect(stopDistanceR(without(field))).toBeNull();
  });

  test.each([
    ["current_price_native", "130"],
    ["current_trailing_stop_native", "117"],
    ["entry_price", "120"],
    ["initial_stop", "110"],
  ])("%s as numeric string %p → 1.3", (field, value) => {
    expect(stopDistanceR(pos({ [field]: value }))).toBeCloseTo(1.3);
  });

  test.each([
    ["entry equals the initial stop", { entry_price: 110 }],
    ["entry below the initial stop", { entry_price: 100 }],
    ["entry 0", { entry_price: 0 }],
  ])("no positive risk (%s) → null", (_label, overrides) => {
    expect(stopDistanceR(pos(overrides))).toBeNull();
  });

  test("initial stop 0 keeps a positive risk: (130 − 117) ÷ 120", () => {
    expect(stopDistanceR(pos({ initial_stop: 0 }))).toBeCloseTo(13 / 120);
  });

  test("price below the stop is a negative R", () => {
    expect(stopDistanceR(pos({ current_price_native: 112 }))).toBeCloseTo(-0.5);
  });

  // AC (ST-19): a 0 stop has no distance. stopDistanceR has no stop > 0 guard,
  // unlike stopDistancePct, so it reports (130 − 0) ÷ 10 = 13R.
  knownFailing("a 0 trailing stop → null", ["BLG-FE-292"], () => {
    expect(stopDistanceR(pos({ current_trailing_stop_native: 0 }))).toBeNull();
  });

  knownFailing("a negative trailing stop → null", ["BLG-FE-292"], () => {
    expect(stopDistanceR(pos({ current_trailing_stop_native: -1 }))).toBeNull();
  });

  // No case for a 0 native price: GET /positions never sends one (a missing
  // live price falls back to the stored price, then the entry price,
  // position_service.py get_positions_with_prices).
});

describe("isInGrace", () => {
  test.each([
    [true, true],
    [false, false],
  ])("grace_period = %p → %p", (value, expected) => {
    expect(isInGrace(pos({ grace_period: value }))).toBe(expected);
  });
  // Any other value (null, missing, "true", 1) is not pinned here: BLG-FE-289
  // decides how a non-boolean grace_period reads. The getUrgencyTier cases
  // below check that the tier and the cells agree on it.
});

describe("getUrgencyTier", () => {
  test.each([
    ["risk-off, healthy price", { risk_off_exit: true }, URGENCY_TIER.EXIT_CONDITION],
    ["risk-off and breached", { risk_off_exit: true, current_price: 80 }, URGENCY_TIER.EXIT_CONDITION],
    ["risk-off in grace", { risk_off_exit: true, grace_period: true }, URGENCY_TIER.EXIT_CONDITION],
    ["post-grace breach", { current_price: 80 }, URGENCY_TIER.STOP_REACHED],
    ["price exactly at the stop", { current_price: 90 }, URGENCY_TIER.STOP_REACHED],
    ["3% above the stop", { current_price: 92.78 }, URGENCY_TIER.NEAR_STOP],
    ["exactly 5% (price 100, stop 95)", { current_trailing_stop: 95 }, URGENCY_TIER.NEAR_STOP],
    ["just under 5% (price 100, stop 95.01)", { current_trailing_stop: 95.01 }, URGENCY_TIER.NEAR_STOP],
    ["just over 5% (price 100, stop 94.99)", { current_trailing_stop: 94.99 }, URGENCY_TIER.OTHER],
    ["just over 5% above the stop", { current_price: 94.8 }, URGENCY_TIER.OTHER],
    ["10% above the stop", {}, URGENCY_TIER.OTHER],
    ["in grace and breached (stop not enforced)", { grace_period: true, current_price: 80 }, URGENCY_TIER.OTHER],
    ["in grace and near", { grace_period: true, current_price: 92 }, URGENCY_TIER.OTHER],
    ["risk_off_exit as the string \"true\"", { risk_off_exit: "true" }, URGENCY_TIER.OTHER],
    ["risk_off_exit null", { risk_off_exit: null }, URGENCY_TIER.OTHER],
    ["price null", { current_price: null }, URGENCY_TIER.OTHER],
    ["price 0", { current_price: 0 }, URGENCY_TIER.OTHER],
    ["price as numeric string, breached", { current_price: "80" }, URGENCY_TIER.STOP_REACHED],
    ["price non-numeric string", { current_price: "abc" }, URGENCY_TIER.OTHER],
    ["stop null", { current_trailing_stop: null }, URGENCY_TIER.OTHER],
    ["stop 0", { current_trailing_stop: 0 }, URGENCY_TIER.OTHER],
    ["stop as numeric string, near", { current_trailing_stop: "97" }, URGENCY_TIER.NEAR_STOP],
  ])("%s → tier %p", (_label, overrides, tier) => {
    expect(getUrgencyTier(pos(overrides))).toBe(tier);
  });

  test("the near-stop band is the Risk Dashboard's 5%", () => {
    expect(NEAR_STOP_PCT).toBe(5);
  });

  test.each([[null], [undefined], [{}]])("position %p → tier 4", (p) => {
    expect(getUrgencyTier(p)).toBe(URGENCY_TIER.OTHER);
  });

  // AC (ST-19): a null or missing grace_period is tiered the way the cells show
  // it. The Stop and To stop cells (Positions.js StopValue, StopDistance) branch
  // on isInGrace, which reads null as out of grace, so they show the stop, the
  // distance in red and, for a breach, the BREACH badge. The tier tests
  // grace_period === false, so the same row ranks tier 4 with "—" in Action
  // needed. Each case asserts the null row gets the tier of the state isInGrace
  // gives it, so it starts failing whichever way BLG-FE-289 settles null.
  const tierAsCellsShowIt = (p) => getUrgencyTier({ ...p, grace_period: isInGrace(p) });
  const nullGraceCases = [
    ["grace_period null, breached (BREACH badge shown)", pos({ grace_period: null, current_price: 80 })],
    ["grace_period missing, breached", (() => { const p = without("grace_period"); p.current_price = 80; return p; })()],
    ["grace_period null, 3% above the stop (red distance shown)", pos({ grace_period: null, current_price: 92.78 })],
  ];
  for (const [label, p] of nullGraceCases) {
    knownFailing(`${label} → the tier its cells show`, ["BLG-FE-289"], () => {
      expect(getUrgencyTier(p)).toBe(tierAsCellsShowIt(p));
    });
  }

  test("grace_period null, 10% above the stop: cells and tier agree (no condition)", () => {
    const p = pos({ grace_period: null });
    expect(getUrgencyTier(p)).toBe(tierAsCellsShowIt(p));
  });

  test.each([
    ["negative price", { current_price: -1 }],
    ["negative stop", { current_trailing_stop: -1 }],
  ])("%s → tier 4", (_label, overrides) => {
    expect(getUrgencyTier(pos(overrides))).toBe(URGENCY_TIER.OTHER);
  });
});

describe("sortByUrgency and compareByUrgency", () => {
  test.each([[null], [undefined], [[]]])("%p → []", (input) => {
    expect(sortByUrgency(input)).toEqual([]);
  });

  test("tier, then distance ascending, then ticker; grace and missing distances last in tier 4", () => {
    const rows = [
      pos({ ticker: "HEALTHY", current_price: 120 }),
      pos({ ticker: "GRACE", grace_period: true, current_price: 91 }),
      pos({ ticker: "NOPRICE", current_price: null }),
      pos({ ticker: "NEAR", current_price: 93 }),
      pos({ ticker: "RISKOFF", risk_off_exit: true }),
      pos({ ticker: "BREACH", current_price: 85 }),
      pos({ ticker: "OK2", current_price: 110 }),
      pos({ ticker: "OK1", current_price: 110 }),
    ];
    expect(sortByUrgency(rows).map((p) => p.ticker)).toEqual([
      "RISKOFF",
      "BREACH",
      "NEAR",
      "OK1",
      "OK2",
      "HEALTHY",
      "GRACE",
      "NOPRICE",
    ]);
  });

  test("does not mutate its input", () => {
    const rows = [pos({ ticker: "B" }), pos({ ticker: "A" })];
    sortByUrgency(rows);
    expect(rows.map((p) => p.ticker)).toEqual(["B", "A"]);
  });

  test("compareByUrgency agrees with sortByUrgency", () => {
    const rows = [pos({ ticker: "B", current_price: 85 }), pos({ ticker: "A" }), pos({ ticker: "C", risk_off_exit: true })];
    expect([...rows].sort(compareByUrgency)).toEqual(sortByUrgency(rows));
  });

  test("a missing ticker sorts as an empty string, not \"undefined\"", () => {
    const rows = [pos({ ticker: "A" }), pos({ ticker: undefined })];
    expect(sortByUrgency(rows)[0].ticker).toBeUndefined();
  });
});

describe("stopDistanceClass", () => {
  test.each([
    [null, "text-app-muted"],
    [undefined, "text-app-muted"],
    [-3, "text-app-negative"],
    [0, "text-app-negative"],
    [5, "text-app-negative"],
    [4.99, "text-app-negative"],
    [5.01, "text-app-warning"],
    [14.99, "text-app-warning"],
    [15, "text-app-warning"],
    [15.01, "text-app-fg"],
  ])("%p → %s", (pct, cls) => {
    expect(stopDistanceClass(pct)).toBe(cls);
  });
});

describe("formatStopDistance", () => {
  test.each([
    ["both parts", {}, "1.3R · 10.0%"],
    ["no R (entry at the initial stop)", { entry_price: 110 }, "— · 10.0%"],
    ["no percentage (GBP price missing)", { current_price: null }, "1.3R · —"],
    ["neither part", { current_price: null, entry_price: null }, "—"],
    ["breached", { current_price: 80, current_price_native: 104 }, "-1.3R · -12.5%"],
  ])("%s → %s", (_label, overrides, text) => {
    expect(formatStopDistance(pos(overrides))).toBe(text);
  });

  // BLG-FE-292 AC: a position with current_trailing_stop_native = 0 shows "—" for R.
  knownFailing("a 0 stop shows \"—\"", ["BLG-FE-292"], () => {
    expect(formatStopDistance(pos({ current_trailing_stop: 0, current_trailing_stop_native: 0 }))).toBe("—");
  });
});
