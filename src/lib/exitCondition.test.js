// ST-19 (BLG-QA-262, EPIC-04, v9.18): table-driven unit tests for the shared
// §8 exit-condition predicate (positions.md §Exit Dialog Pre-Selection and
// Deep Link). Each input is tried as null, missing, a numeric string, a
// non-numeric string and 0.
import {
  isPostGraceStopBreach,
  getExitCondition,
  exitPreselectNote,
  EXIT_REASON_RISK_OFF,
  EXIT_REASON_STOP,
} from "./exitCondition";

// Out of grace, GBP price 100 against a GBP trailing stop 90: no condition.
function pos(overrides = {}) {
  return {
    ticker: "AAA",
    market: "US",
    grace_period: false,
    risk_off_exit: false,
    current_price: 100,
    current_trailing_stop: 90,
    ...overrides,
  };
}

function without(field) {
  const p = pos({ current_price: 80 });
  delete p[field];
  return p;
}

const RISK_OFF_US =
  "Pre-selected because the US market is in a risk-off regime (index below its 200-day average).";
const STOP_NOTE = "Pre-selected because the price is at or below the trailing stop and the grace period has ended.";

describe("isPostGraceStopBreach", () => {
  test.each([
    ["price above the stop", {}, false],
    ["price below the stop", { current_price: 80 }, true],
    ["price exactly at the stop", { current_price: 90 }, true],
    ["price just above the stop", { current_price: 90.01 }, false],
    ["in grace, below the stop", { grace_period: true, current_price: 80 }, false],
    ["grace_period \"false\" string, below the stop", { grace_period: "false", current_price: 80 }, false],
    ["grace_period 0, below the stop", { grace_period: 0, current_price: 80 }, false],
    ["price null", { current_price: null }, false],
    ["price 0", { current_price: 0 }, false],
    ["price as numeric string, below", { current_price: "80" }, true],
    ["price non-numeric string", { current_price: "abc" }, false],
    ["price empty string", { current_price: "" }, false],
    ["stop null", { current_price: 80, current_trailing_stop: null }, false],
    ["stop 0", { current_price: 80, current_trailing_stop: 0 }, false],
    ["stop as numeric string", { current_price: 80, current_trailing_stop: "90" }, true],
    ["stop non-numeric string", { current_price: 80, current_trailing_stop: "abc" }, false],
    ["negative stop", { current_price: 80, current_trailing_stop: -1 }, false],
    ["negative price", { current_price: -1 }, false],
  ])("%s → %p", (_label, overrides, expected) => {
    expect(isPostGraceStopBreach(pos(overrides))).toBe(expected);
  });

  // grace_period null or missing is not pinned here: BLG-FE-289 decides whether
  // it reads as out of grace. positionUrgency.test.js checks that the tier and
  // the cells agree on it.
  test.each([["current_price"], ["current_trailing_stop"]])("missing %s → false", (field) => {
    expect(isPostGraceStopBreach(without(field))).toBe(false);
  });

  test.each([[null], [undefined], [{}]])("position %p → false", (p) => {
    expect(isPostGraceStopBreach(p)).toBe(false);
  });
});

describe("getExitCondition", () => {
  test.each([
    ["none", {}, { reason: null, riskOff: false, stopBreach: false }],
    ["risk-off only", { risk_off_exit: true }, { reason: EXIT_REASON_RISK_OFF, riskOff: true, stopBreach: false }],
    ["stop only", { current_price: 80 }, { reason: EXIT_REASON_STOP, riskOff: false, stopBreach: true }],
    [
      "both: risk-off takes precedence",
      { risk_off_exit: true, current_price: 80 },
      { reason: EXIT_REASON_RISK_OFF, riskOff: true, stopBreach: true },
    ],
    ["risk-off in grace", { risk_off_exit: true, grace_period: true }, { reason: EXIT_REASON_RISK_OFF, riskOff: true, stopBreach: false }],
    ["risk_off_exit null", { risk_off_exit: null }, { reason: null, riskOff: false, stopBreach: false }],
    ["risk_off_exit \"true\" string", { risk_off_exit: "true" }, { reason: null, riskOff: false, stopBreach: false }],
    ["risk_off_exit 1", { risk_off_exit: 1 }, { reason: null, riskOff: false, stopBreach: false }],
  ])("%s", (_label, overrides, expected) => {
    expect(getExitCondition(pos(overrides))).toEqual(expected);
  });

  test.each([["risk_off_exit"], ["market"]])("missing %s → no risk-off", (field) => {
    const p = pos();
    delete p[field];
    expect(getExitCondition(p).riskOff).toBe(false);
  });

  test.each([[null], [undefined], [{}]])("position %p → no condition", (p) => {
    expect(getExitCondition(p)).toEqual({ reason: null, riskOff: false, stopBreach: false });
  });
});

describe("exitPreselectNote", () => {
  test.each([
    ["no condition", {}, null],
    ["risk-off, US", { risk_off_exit: true }, RISK_OFF_US],
    [
      "risk-off, UK",
      { risk_off_exit: true, market: "UK" },
      "Pre-selected because the UK market is in a risk-off regime (index below its 200-day average).",
    ],
    ["risk-off and stop", { risk_off_exit: true, current_price: 80 }, `${RISK_OFF_US} The price is also at or below the trailing stop.`],
    ["stop only", { current_price: 80 }, STOP_NOTE],
    ["stop in grace", { grace_period: true, current_price: 80 }, null],
  ])("%s", (_label, overrides, text) => {
    expect(exitPreselectNote(pos(overrides))).toBe(text);
  });

  // The API sends market "US" or "UK"; anything other than "UK" reads as US.
  test.each([[null], [undefined], ["uk"], [""]])("risk-off with market %p → US wording", (market) => {
    expect(exitPreselectNote(pos({ risk_off_exit: true, market }))).toBe(RISK_OFF_US);
  });

  test.each([[null], [undefined], [{}]])("position %p → null", (p) => {
    expect(exitPreselectNote(p)).toBeNull();
  });
});
