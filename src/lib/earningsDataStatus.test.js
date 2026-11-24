import {
  isEarningsUnavailable, isCacheableAnswer, UNAVAILABLE_ANSWER, GAP_RISK_UNAVAILABLE, createAnswerCache,
  UNAVAILABLE_HOLD_MS,
} from "./earningsDataStatus";

describe("isEarningsUnavailable", () => {
  test.each([
    ["unavailable", { data_status: "unavailable", days_until_earnings: null }, true],
    ["ok with a date", { data_status: "ok", days_until_earnings: 3 }, false],
    ["ok with no date", { data_status: "ok", days_until_earnings: null }, false],
    ["no data_status (older backend)", { days_until_earnings: null }, false],
    ["other string", { data_status: "UNAVAILABLE" }, false],
    ["null", null, false],
    ["undefined", undefined, false],
    ["string", "unavailable", false],
  ])("%s", (_label, answer, expected) => {
    expect(isEarningsUnavailable(answer)).toBe(expected);
  });
});

describe("isCacheableAnswer", () => {
  test.each([
    ["unavailable is not cached", { data_status: "unavailable" }, false],
    ["ok with a date is cached", { data_status: "ok", days_until_earnings: 3 }, true],
    ["ok with no date is cached", { data_status: "ok", days_until_earnings: null }, true],
    ["no data_status is cached", { days_until_earnings: 5 }, true],
    ["gap-risk ok is cached", { flagged: false, data_status: "ok" }, true],
    ["gap-risk unavailable is not cached", { flagged: false, data_status: "unavailable" }, false],
    ["null is not cached", null, false],
    ["undefined is not cached", undefined, false],
  ])("%s", (_label, answer, expected) => {
    expect(isCacheableAnswer(answer)).toBe(expected);
  });
});

describe("UNAVAILABLE_ANSWER (a failed request)", () => {
  test("reads as unavailable and is not cached", () => {
    expect(isEarningsUnavailable(UNAVAILABLE_ANSWER)).toBe(true);
    expect(isCacheableAnswer(UNAVAILABLE_ANSWER)).toBe(false);
    expect(UNAVAILABLE_ANSWER.days_until_earnings).toBeNull();
  });
});

describe("createAnswerCache", () => {
  const OK = { data_status: "ok", days_until_earnings: 3 };
  const UNAVAILABLE = { data_status: "unavailable", days_until_earnings: null };

  test("the hold is 60 seconds", () => {
    expect(UNAVAILABLE_HOLD_MS).toBe(60000);
  });

  test.each([
    // [label, answer, read at (ms after set), expected]
    ["ok, read at once", OK, 0, OK],
    ["ok, read an hour later (session)", OK, 3600000, OK],
    ["unavailable, read at once", UNAVAILABLE, 0, UNAVAILABLE],
    ["unavailable, 1 ms before the hold ends", UNAVAILABLE, 59999, UNAVAILABLE],
    ["unavailable, exactly at the hold", UNAVAILABLE, 60000, undefined],
    ["unavailable, after the hold", UNAVAILABLE, 60001, undefined],
    ["null is not stored", null, 0, undefined],
    ["undefined is not stored", undefined, 0, undefined],
  ])("%s", (_label, answer, after, expected) => {
    const cache = createAnswerCache();
    cache.set("AAPL:US", answer, 1000);
    expect(cache.get("AAPL:US", 1000 + after)).toEqual(expected);
  });

  test("an ok answer replaces a held unavailable one", () => {
    const cache = createAnswerCache();
    cache.set("k", UNAVAILABLE, 0);
    cache.set("k", OK, 10);
    expect(cache.get("k", 10 + 3600000)).toEqual(OK);
  });

  test("a failed request after an ok answer clears it", () => {
    const cache = createAnswerCache();
    cache.set("k", OK, 0);
    cache.set("k", null, 1);
    expect(cache.get("k", 2)).toBeUndefined();
  });

  test("an unknown key is undefined", () => {
    expect(createAnswerCache().get("nope", 0)).toBeUndefined();
  });
});

describe("GAP_RISK_UNAVAILABLE (a failed gap-risk request)", () => {
  test("is unflagged, unavailable and held rather than cached", () => {
    expect(GAP_RISK_UNAVAILABLE.flagged).toBe(false);
    expect(isEarningsUnavailable(GAP_RISK_UNAVAILABLE)).toBe(true);
    const cache = createAnswerCache();
    cache.set("p1", GAP_RISK_UNAVAILABLE, 0);
    expect(cache.get("p1", 59999)).toBe(GAP_RISK_UNAVAILABLE);
    expect(cache.get("p1", 60000)).toBeUndefined();
  });
});
