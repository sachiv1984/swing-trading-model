// ST-09 (BLG-UX-11, EPIC-02, v9.18): quiet-day collapse logic
// (dashboard.md v4.4 §3A). Expected values are written from the spec's table
// and worked examples (decision record §2.4), not from the code.
import {
  QUIET_DAY_ITEMS,
  BRIEFING_PANEL_KEYS,
  STATUS_ROW_KEYS,
  isFolded,
  foldedItems,
  shownCount,
  mdGridCols,
} from "./quietDay";

describe("isFolded — only loaded, error-free and empty folds", () => {
  test.each([
    // [isLoading, error, empty, folded]
    [false, null, true, true],
    [false, undefined, true, true],
    [false, null, false, false],
    [true, null, true, false], // still loading: its own skeleton shows
    [true, null, false, false],
    [false, new Error("500"), true, false], // an error is not empty
    [false, "Unable to load", true, false],
    [false, new Error("500"), false, false],
    [false, null, undefined, false], // no empty test supplied: never folds
    [false, null, null, false],
    [false, null, 0, false], // only a real `true` folds, not a falsy count
    [false, null, "true", false],
  ])("isLoading=%p error=%p empty=%p → %p", (isLoading, error, empty, expected) => {
    expect(isFolded({ isLoading, error, empty })).toBe(expected);
  });
});

describe("foldedItems — the line lists folded names in the §3A table order", () => {
  test("all eleven folded (quiet-day fixture) reads in table order", () => {
    const all = new Set(QUIET_DAY_ITEMS.map((i) => i.key).reverse());
    expect(foldedItems(all).map((i) => i.name).join(" · ")).toBe(
      "Screener hits · Positions to watch · Red flags · Earnings · Compliance · AI briefing · Open positions · Portfolio heat · In grace · Recent activity · What's new"
    );
  });

  test("one open position, healthy: Cards 1 and 2 shown, the other nine listed", () => {
    const folded = new Set(QUIET_DAY_ITEMS.map((i) => i.key).filter((k) => k !== "open-positions" && k !== "portfolio-heat"));
    expect(foldedItems(folded).map((i) => i.name)).toEqual([
      "Screener hits", "Positions to watch", "Red flags", "Earnings", "Compliance", "AI briefing", "In grace", "Recent activity", "What's new",
    ]);
  });

  test.each([[new Set()], [[]], [null], [undefined]])("nothing folded (%p) → empty line", (input) => {
    expect(foldedItems(input)).toEqual([]);
  });

  test("a revealed disclosure entry stays in the line after its card loads or has data", () => {
    // AI briefing revealed, then regenerated: no longer folded, still listed.
    expect(foldedItems(new Set(["earnings"]), new Set(["ai-briefing"])).map((i) => i.key)).toEqual(["earnings", "ai-briefing"]);
  });

  test("a revealed key that is not a disclosure entry is not added", () => {
    expect(foldedItems(new Set(), new Set(["earnings"]))).toEqual([]);
  });

  test("an unknown key is ignored", () => {
    expect(foldedItems(new Set(["not-a-card", "earnings"])).map((i) => i.key)).toEqual(["earnings"]);
  });

  test("the two disclosure entries are AI briefing and What's new; every other entry has a target", () => {
    expect(QUIET_DAY_ITEMS.filter((i) => i.disclosure).map((i) => i.key)).toEqual(["ai-briefing", "whats-new"]);
    for (const item of QUIET_DAY_ITEMS.filter((i) => !i.disclosure)) expect(item.to).toMatch(/^\//);
  });
});

describe("shownCount — containers hide only when every element has folded", () => {
  const all = new Set(QUIET_DAY_ITEMS.map((i) => i.key));
  test.each([
    // [folded, revealed, briefing panel shown, Cards 1–3 shown]
    [all, new Set(), 0, 0],
    [all, new Set(["ai-briefing"]), 1, 0], // revealing the briefing shows the panel
    [new Set(["in-grace"]), new Set(), 6, 2],
    [new Set(), new Set(), 6, 3],
    [new Set(["open-positions", "portfolio-heat", "in-grace"]), new Set(), 6, 0],
  ])("folded=%p revealed=%p", (folded, revealed, briefing, row) => {
    expect(shownCount(BRIEFING_PANEL_KEYS, folded, revealed)).toBe(briefing);
    expect(shownCount(STATUS_ROW_KEYS, folded, revealed)).toBe(row);
  });
});

describe("mdGridCols — n shown cards take n columns", () => {
  test.each([
    [1, "md:grid-cols-1"],
    [2, "md:grid-cols-2"],
    [3, "md:grid-cols-3"],
    [5, "md:grid-cols-5"],
    [0, "md:grid-cols-1"], // hidden container: any value is harmless
    [6, "md:grid-cols-1"],
    [-1, "md:grid-cols-1"],
    [undefined, "md:grid-cols-1"],
  ])("%p → %p", (n, cls) => {
    expect(mdGridCols(n)).toBe(cls);
  });
});
