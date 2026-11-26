// ST-13 (BLG-FE-320, EPIC-02, v9.18): Trade History rules filter
// (trade_history.md v1.18 §Rules Filter). Expected values written from the spec.
import { parseRulesParam, rulesState, matchesRules, rulesCounts, rulesLine } from "./rulesFilter";

const F = { id: "f", rules_followed: true, rules_broken: [] };
const B = { id: "b", rules_followed: false, rules_broken: ["pre_entry_override", "checklist_skipped"] };
const N = { id: "n", rules_followed: null, rules_broken: [] };
const LEGACY = { id: "l" }; // no field at all (older payload)

describe("rulesState: only a real true/false classifies", () => {
  test.each([
    [F, "followed"],
    [B, "broken"],
    [N, "unknown"],
    [LEGACY, "unknown"],
    [{ rules_followed: "true" }, "unknown"],
    [{ rules_followed: 0 }, "unknown"],
    [null, "unknown"],
  ])("%j → %p", (t, s) => expect(rulesState(t)).toBe(s));
});

describe("matchesRules: each option shows only its trades (RF-01, RF-02)", () => {
  const all = [F, B, N, LEGACY];
  test.each([
    ["all", ["f", "b", "n", "l"]],
    ["followed", ["f"]],
    ["broken", ["b"]],
    ["unknown", ["n", "l"]], // a legacy trade appears only under Not known
    ["bogus", ["f", "b", "n", "l"]],
  ])("%p → %p", (opt, ids) => expect(all.filter((t) => matchesRules(t, opt)).map((t) => t.id)).toEqual(ids));
});

test("rulesCounts adds up to the trades given", () => {
  expect(rulesCounts([F, B, N, LEGACY, F])).toEqual({ followed: 2, broken: 1, unknown: 2 });
  expect(rulesCounts([])).toEqual({ followed: 0, broken: 0, unknown: 0 });
  expect(rulesCounts(null)).toEqual({ followed: 0, broken: 0, unknown: 0 });
});

describe("parseRulesParam", () => {
  test.each([["followed", "followed"], ["broken", "broken"], ["unknown", "unknown"], ["all", "all"], [null, "all"], ["", "all"], ["Followed", "all"]])(
    "%p → %p", (v, out) => expect(parseRulesParam(v)).toBe(out));
});

describe("rulesLine", () => {
  test.each([
    [F, "Followed"],
    [B, "Broken: Pre-Entry Override, Checklist Skipped"],
    [{ rules_followed: false, rules_broken: [] }, "Broken"],
    [{ rules_followed: false, rules_broken: ["new_reason"] }, "Broken: new_reason"],
    [N, "Not known (no entry check recorded)"],
    [LEGACY, "Not known (no entry check recorded)"],
  ])("%j → %p", (t, text) => expect(rulesLine(t)).toBe(text));
});
