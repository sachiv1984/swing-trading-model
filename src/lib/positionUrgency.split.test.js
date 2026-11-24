// ST-27 (BLG-BE-223, EPIC-05, v9.18): urgency tier 0 "Split to confirm" and the
// suppressed stop and exit tests (positions.md v2.30 §Split Detected State;
// strategy_rules.md §9.1). In a file of its own so EPIC-04's ST-19
// positionUrgency.test.js can land without a conflict; ST-19's CI job runs it.
import {
  URGENCY_TIER,
  getUrgencyTier,
  sortByUrgency,
  stopDistancePct,
  stopDistanceR,
  formatStopDistance,
} from "./positionUrgency";
import { getExitCondition, isPostGraceStopBreach, isSplitPending } from "./exitCondition";

const PENDING = {
  id: "split-1", ratio: 2, ratio_label: "2:1", effective_date: "2026-11-23", source: "yahoo",
  shares_before: 10, shares_after: 20, shares_after_is_whole: true,
  entry_before: 200, entry_after: 100, stop_before: 180, stop_after: 90, cost_before: 2000, cost_after: 2000,
};

// The worked example on day D: price 104 (post-split) against the stored stop 180.
function mu(overrides = {}) {
  return {
    ticker: "MU", market: "US", grace_period: false,
    current_price: 80, current_price_native: 104,
    current_trailing_stop: 138.46, current_trailing_stop_native: 180,
    entry_price: 200, initial_stop: 180, risk_off_exit: false,
    split_pending: null,
    ...overrides,
  };
}

describe("isSplitPending", () => {
  test.each([
    [null, false],
    [undefined, false],
    [{}, true],
    [PENDING, true],
    ["2:1", false],
    [0, false],
  ])("split_pending=%p -> %p", (value, expected) => {
    expect(isSplitPending({ split_pending: value })).toBe(expected);
  });

  test("a missing position is not pending", () => {
    expect(isSplitPending(null)).toBe(false);
    expect(isSplitPending(undefined)).toBe(false);
  });
});

describe("tier 0 and suppression, full input product", () => {
  // split pending x price at/below stop x risk-off x grace
  const cases = [];
  for (const pending of [false, true]) {
    for (const breach of [false, true]) {
      for (const riskOff of [false, true]) {
        for (const grace of [false, true]) {
          cases.push([pending, breach, riskOff, grace]);
        }
      }
    }
  }

  test.each(cases)("pending=%p breach=%p riskOff=%p grace=%p", (pending, breach, riskOff, grace) => {
    const p = mu({
      split_pending: pending ? PENDING : null,
      current_price: breach ? 80 : 200,
      risk_off_exit: riskOff,
      grace_period: grace,
    });
    const tier = getUrgencyTier(p);
    const cond = getExitCondition(p);
    if (pending) {
      expect(tier).toBe(URGENCY_TIER.SPLIT_TO_CONFIRM);
      expect(cond).toEqual({ reason: null, riskOff: false, stopBreach: false });
      expect(isPostGraceStopBreach(p)).toBe(false);
      expect(stopDistancePct(p)).toBeNull();
      expect(stopDistanceR(p)).toBeNull();
      expect(formatStopDistance(p)).toBe("—");
    } else {
      expect(tier).not.toBe(URGENCY_TIER.SPLIT_TO_CONFIRM);
      if (riskOff) expect(tier).toBe(URGENCY_TIER.EXIT_CONDITION);
      else if (breach && !grace) expect(tier).toBe(URGENCY_TIER.STOP_REACHED);
    }
  });
});

describe("ordering", () => {
  test("tier 0 sorts above an exit condition and a stop breach", () => {
    const riskOff = mu({ ticker: "AAA", risk_off_exit: true });
    const breach = mu({ ticker: "BBB" });
    const healthy = mu({ ticker: "CCC", current_price: 200 });
    const split = mu({ ticker: "ZZZ", split_pending: PENDING });
    expect(sortByUrgency([healthy, breach, riskOff, split]).map((p) => p.ticker)).toEqual(["ZZZ", "AAA", "BBB", "CCC"]);
  });

  test("after confirmation the position takes its normal tier (worked example: tier 4, 13.5% to stop)", () => {
    // Confirmed: 20 shares at 100, stop 90, price 104 -> (104 - 90) / 104 = 13.46%.
    const confirmed = mu({
      split_pending: null, current_price_native: 104, current_trailing_stop_native: 90,
      current_price: 80, current_trailing_stop: 69.23, entry_price: 100, initial_stop: 90,
    });
    expect(getUrgencyTier(confirmed)).toBe(URGENCY_TIER.OTHER);
    expect(stopDistancePct(confirmed)).toBeCloseTo(13.46, 1);
  });

  test("two pending splits sort by ticker", () => {
    const a = mu({ ticker: "AMD", split_pending: PENDING });
    const b = mu({ ticker: "NVDA", split_pending: PENDING });
    expect(sortByUrgency([b, a]).map((p) => p.ticker)).toEqual(["AMD", "NVDA"]);
  });
});
