// ST-12 (BLG-UX-19, EPIC-02, v9.18): checklist system statuses (trade_plan.md
// v1.30 §6; design record trade-plan-checklist-status §5). Expected values are
// written from the record's worked examples, not from the code.
import {
  positionSizeStatus,
  positionSizeText,
  stopLevel,
  stopText,
  withSystemStatus,
  judgementItems,
  judgementComplete,
} from "./checklistStatus";

const snap = (cash, sector, sizing, extra = []) => ({
  captured_at: "2026-11-26T10:00:00Z",
  advisory_status: "pass",
  checks: [
    { rule: "regime_gate", status: "fail" }, // not a size rule: never counted
    { rule: "cash_constraint", status: cash },
    { rule: "sector_concentration", status: sector },
    { rule: "earnings_proximity", status: "warn" }, // not a size rule
    { rule: "sizing_validity", status: sizing },
    ...extra,
  ],
});

describe("record §5 worked examples", () => {
  test.each([
    // [label, snapshot, stop, size text, stop text]
    ["no shares, no stop", null, "", "Not checked yet", "✗ Not set"],
    ["10 shares, no stop", snap("pass", "pass", "skipped"), "", "✓ Pass", "✗ Not set"],
    ["stop 0", snap("pass", "pass", "fail"), "0", "✗ Fail — see Pre-Entry Checks", "✗ Not set"],
    ["cash fails", snap("fail", "pass", "pass"), "142", "✗ Fail — see Pre-Entry Checks", "✓ Set: 142.00 USD"],
    ["sector warns", snap("pass", "warn", "pass"), "142", "! Warning — see Pre-Entry Checks", "✓ Set: 142.00 USD"],
    ["panel error (no snapshot)", null, "142", "Not checked yet", "✓ Set: 142.00 USD"],
  ])("%s", (_label, snapshot, stop, sizeText, stopTxt) => {
    expect(positionSizeText(positionSizeStatus(snapshot))).toBe(sizeText);
    expect(stopText(stop, "US")).toBe(stopTxt);
  });
});

describe("positionSizeStatus — worst of the three size rules", () => {
  test.each([
    [snap("skipped", "skipped", "skipped"), null], // all skipped: no result
    [{ checks: [] }, null],
    [{}, null],
    [undefined, null],
    [snap("warn", "fail", "pass"), "fail"],
    [snap("warn", "pass", "warn"), "warn"],
    [snap("pass", "skipped", "pass"), "pass"],
    [snap("pass", "pass", "pass", [{ rule: "cash_constraint", status: "fail" }]), "fail"],
    [snap("weird", "pass", "skipped"), "pass"], // unknown status ignored
    [{ checks: [null, { rule: "sizing_validity", status: "warn" }] }, "warn"],
  ])("%j → %p", (snapshot, expected) => {
    expect(positionSizeStatus(snapshot)).toBe(expected);
  });
  test("other rules failing never affect it", () => {
    expect(positionSizeStatus(snap("pass", "pass", "pass"))).toBe("pass");
  });
});

describe("stopLevel and stopText", () => {
  test.each([
    ["142", 142],
    ["142.5", 142.5],
    [" 0.75 ", 0.75],
    [142, 142],
    ["0", null],
    [0, null],
    ["-1", null],
    [-1, null],
    ["", null],
    ["   ", null],
    ["abc", null],
    ["1e3", 1000], // the number input accepts it and the form saves 1000
    ["142.", 142],
    [null, null],
    [undefined, null],
    [true, null],
    [NaN, null],
  ])("%p → %p", (value, expected) => {
    expect(stopLevel(value)).toBe(expected);
  });
  test("UK shows GBP, US shows USD, 2 dp", () => {
    expect(stopText("95.5", "UK")).toBe("✓ Set: 95.50 GBP");
    expect(stopText(142, "US")).toBe("✓ Set: 142.00 USD");
  });
  test("read-only wording when no snapshot was saved", () => {
    expect(positionSizeText(null, { readOnly: true })).toBe("Not checked when saved");
    expect(positionSizeText("pass", { readOnly: true })).toBe("✓ Pass");
  });
});

// A v1.29 plan: all four ticked, no auto flag (record §4 worked example).
const LEGACY = [
  { id: "signal_confirmed", label: "Strategy signal confirmed", checked: true },
  { id: "heat_limit_checked", label: "Position size within heat limits", checked: true },
  { id: "stop_defined", label: "Stop level defined", checked: true },
  { id: "research_reviewed", label: "Pre-trade research reviewed", checked: true },
];

describe("withSystemStatus — saved shape (§6.5)", () => {
  test("system items carry auto: true and checked = status; judgement ticks are kept", () => {
    const out = withSystemStatus(LEGACY, { sizeStatus: "warn", stopValue: "" });
    expect(out.map((i) => i.id)).toEqual(["signal_confirmed", "heat_limit_checked", "stop_defined", "research_reviewed"]);
    expect(out[1]).toEqual({ id: "heat_limit_checked", label: "Position size checks", checked: false, auto: true });
    expect(out[2]).toEqual({ id: "stop_defined", label: "Stop level defined", checked: false, auto: true });
    expect(out[0].checked).toBe(true);
    expect(out[3].checked).toBe(true);
  });
  test("pass and a stop set save both as checked", () => {
    const out = withSystemStatus(LEGACY, { sizeStatus: "pass", stopValue: "142" });
    expect(out[1].checked).toBe(true);
    expect(out[2].checked).toBe(true);
  });
  test("no result saves the size item unchecked", () => {
    expect(withSystemStatus(LEGACY, { sizeStatus: null, stopValue: "142" })[1].checked).toBe(false);
  });
  test.each([[null], [undefined], [[]]])("%p → []", (items) => {
    expect(withSystemStatus(items, { sizeStatus: "pass", stopValue: 1 })).toEqual([]);
  });
});

describe("judgement items and completion", () => {
  test("the legacy plan loads its two judgement ticks, with their indexes", () => {
    expect(judgementItems(LEGACY).map(({ item, index }) => [item.id, index, item.checked])).toEqual([
      ["signal_confirmed", 0, true],
      ["research_reviewed", 3, true],
    ]);
  });
  test.each([
    [[true, true], true],
    [[true, false], false],
    [[false, false], false],
  ])("ticks %p → complete %p (system items ignored)", ([a, b], expected) => {
    const items = [
      { id: "signal_confirmed", checked: a },
      { id: "heat_limit_checked", checked: false, auto: true },
      { id: "stop_defined", checked: false, auto: true },
      { id: "research_reviewed", checked: b },
    ];
    expect(judgementComplete(items)).toBe(expected);
  });
  test("no judgement items is not complete", () => {
    expect(judgementComplete([{ id: "stop_defined", checked: true }])).toBe(false);
    expect(judgementComplete([])).toBe(false);
  });
});
