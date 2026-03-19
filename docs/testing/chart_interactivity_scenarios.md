**Owner:** QA & Testing Owner
**Class:** Class 2
**Status:** Canonical
**Version:** 0.1
**Last Updated:** 2026-03-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Sprint Item:** ST-11 — EPIC-04 (v2.1)
**Design Source:** docs/design/2026-03-18__release-v2.1/chart-interactivity/ux_spec.md

---

# Chart Interactivity Test Scenarios — ST-11 (CHART-IX)

## Purpose

Test scenarios covering the interactivity enhancements added to three analytics charts in ST-11:
1. Monthly Performance Heatmap — tile click drill-down modal
2. Underwater Equity Curve — hover tooltip, scroll/button zoom, click-drag pan, Reset
3. R-Multiple Analysis (§9) — bar hover tooltip

**Hard constraint (all scenarios):** No displayed value may differ from the canonical backend response. Client-side re-derivation is not permitted for any metric — tooltip values must be read from the data the chart already holds.

---

## SC-CHART-IX-01 — Monthly Heatmap: Tile Click Drill-Down

**Priority:** P1
**Chart:** Monthly Performance Heatmap (§4 of analytics.md)

### SC-CHART-IX-01a — Tile with trades opens modal

**Precondition:** Analytics page loaded with ≥1 closed trade in at least one calendar month.

**Steps:**
1. Identify a heatmap tile with `trades > 0`.
2. Click the tile.

**Expected:**
- A modal opens with title: `"Trades — [Month YYYY]"` (e.g. `"Trades — Jan 2026"`).
- A summary line appears: `"[n] trades · Total P&L: £X.XX"` where n = count of trades in that month and Total P&L = sum of their P&L values.
- A table lists only trades from that calendar month, with columns: Ticker, Exit Date, P&L (signed, colour-coded: green for positive, red for negative), R-Multiple (shown if calculable from stop price; `—` otherwise), Exit Reason.
- Trade month attribution uses `exit_date` (not entry date).
- The originating tile receives a 2px inset ring in the focus/accent colour.
- No additional API call is made (trades are from the already-loaded dataset).

### SC-CHART-IX-01b — Modal close behaviours

**Precondition:** Modal is open (SC-CHART-IX-01a passed).

**Steps (test each independently):**
1. Click the **X** button in the modal header.
2. Click the backdrop (outside the modal panel).
3. Press the **Escape** key.

**Expected:** Modal closes on each action. The tile selection ring is removed.

### SC-CHART-IX-01c — Tile with 0 trades — not clickable

**Precondition:** Analytics page loaded with a heatmap tile showing 0 trades.

**Steps:**
1. Hover over the 0-trade tile.
2. Click the tile.

**Expected:**
- Cursor remains `default` (no pointer cursor).
- No modal opens.
- No visual selected state is applied.

### SC-CHART-IX-01d — Trade data integrity in modal

**Precondition:** A specific month is known to contain exactly N trades with a known total P&L.

**Steps:**
1. Click that month's heatmap tile.
2. Count the rows in the modal trade table.
3. Verify the summary total P&L.

**Expected:**
- Row count = N.
- Summary P&L matches the sum of all individual trade P&L values shown in the table.
- P&L values in the table match the trade data already loaded (no re-computation).

---

## SC-CHART-IX-02 — Underwater Equity Curve: Zoom

**Priority:** P1
**Chart:** Underwater Equity Curve (§5 of analytics.md)

### SC-CHART-IX-02a — Scroll wheel zooms in

**Precondition:** Analytics page loaded with > 4 closed trades. Chart at default (full range).

**Steps:**
1. Hover the mouse over the Underwater Equity Curve chart area.
2. Scroll the mouse wheel upward (zoom in).

**Expected:**
- The chart time axis narrows — fewer data points are visible.
- The Y-axis (drawdown %) auto-scales to the visible range.
- A **"Reset"** button appears in the chart header.
- A muted hint "Scroll to zoom" may appear and fade within 3 seconds of first hover (optional).

### SC-CHART-IX-02b — `+` button zooms in

**Precondition:** Chart at default (full range) with > 4 data points.

**Steps:**
1. Click the `+` zoom button in the chart header.

**Expected:** Chart time axis narrows (same effect as scroll up). Reset button appears.

### SC-CHART-IX-02c — `−` button zooms out

**Precondition:** Chart is zoomed in.

**Steps:**
1. Click the `−` zoom button.

**Expected:** Chart time axis expands. Reset button remains visible while still zoomed.

### SC-CHART-IX-02d — Minimum zoom boundary

**Precondition:** Chart is already at 4 data points or fewer.

**Steps:**
1. Attempt to zoom in further (scroll up or click `+`).

**Expected:** Chart does not zoom further. Minimum of 4 data points is preserved.

### SC-CHART-IX-02e — Reset restores full range

**Precondition:** Chart is zoomed in; Reset button is visible.

**Steps:**
1. Click the **"Reset"** button.

**Expected:**
- Chart returns to the full data range.
- The Reset button disappears.

### SC-CHART-IX-02f — Reset button not shown when not zoomed

**Precondition:** Chart at default (full range).

**Expected:** The "Reset" button is not visible in the chart header.

---

## SC-CHART-IX-03 — Underwater Equity Curve: Pan

**Priority:** P1
**Chart:** Underwater Equity Curve (§5 of analytics.md)

### SC-CHART-IX-03a — Click-drag pans while zoomed

**Precondition:** Chart is zoomed in to a sub-range of trades.

**Steps:**
1. Click and hold the mouse button on the chart.
2. Drag left (to pan toward more recent trades).
3. Release the mouse button.

**Expected:**
- While dragging, the visible range shifts in the direction of the drag.
- Released: the chart settles on the new range.
- The same number of data points remains visible (the window size does not change; only its position shifts).

### SC-CHART-IX-03b — No pan when not zoomed

**Precondition:** Chart is at full range (not zoomed in).

**Steps:**
1. Click and drag on the chart.

**Expected:** No range shift occurs. Chart remains static.

---

## SC-CHART-IX-04 — Underwater Equity Curve: Hover Tooltip

**Priority:** P1
**Chart:** Underwater Equity Curve (§5 of analytics.md)

### SC-CHART-IX-04a — Tooltip shows correct fields on hover

**Precondition:** Chart rendered with ≥ 3 trades.

**Steps:**
1. Hover over a data point on the curve.

**Expected:**
- Tooltip appears showing:
  - **Date** — the `exit_date` of that trade, formatted as a readable date.
  - **Drawdown %** — signed percentage (e.g. `–8.30%`).
  - **Current equity** — cumulative P&L at that trade in GBP.
  - **Peak equity** — peak cumulative P&L at that point in GBP.
- Tooltip repositions: follows the cursor; flips to the left when cursor is in the right 30% of the chart area.
- No values are recomputed — all displayed values are read from the chart data series.

### SC-CHART-IX-04b — Tooltip works while zoomed

**Precondition:** Chart is zoomed in to a sub-range.

**Steps:**
1. Hover over a visible data point.

**Expected:** Tooltip displays correct values for that point (same fields as SC-CHART-IX-04a).

---

## SC-CHART-IX-05 — R-Multiple Analysis: Bar Hover Tooltip

**Priority:** P1
**Chart:** R-Multiple Analysis / Distribution histogram (§9 of analytics.md)

### SC-CHART-IX-05a — Tooltip shows R range, count, percentage

**Precondition:** Analytics page loaded with ≥ 10 closed trades with valid stop prices.

**Steps:**
1. Hover over any bar in the R-Multiple Distribution histogram.

**Expected:**
- Tooltip appears showing:
  - **R-multiple range** — the bucket label (e.g. `"1R to 2R"`, `"-3R+"`).
  - **Trade count** — e.g. `"4 trades"`.
  - **% of total** — e.g. `"22% of closed trades"`.
- `% of total` = `count / total_valid_trades × 100`, rounded to nearest integer.
- Tooltip positioning: follows cursor; flips if near chart edge.

### SC-CHART-IX-05b — Zero-count bar shows count correctly

**Precondition:** At least one R-multiple bucket has 0 trades (common for extreme buckets).

**Steps:**
1. Hover over a bar with 0 count.

**Expected:**
- Tooltip shows: bucket label, `"0 trades"`, `"0% of closed trades"`.

### SC-CHART-IX-05c — Percentage sums are consistent

**Precondition:** All 7 buckets are visible.

**Steps:**
1. Hover over each of the 7 bars and note the % values.
2. Sum all percentages.

**Expected:** Sum is 100% (rounding may cause ±1% discrepancy across 7 buckets; this is acceptable).

---

## SC-CHART-IX-06 — Cross-Chart Data Integrity

**Priority:** P1

### SC-CHART-IX-06a — Heatmap modal P&L matches heatmap tile

**Steps:**
1. Note the P&L value shown on a heatmap tile (e.g. `+£823`).
2. Click the tile.
3. Observe the modal summary total P&L.

**Expected:** Modal summary P&L matches tile P&L exactly (both sourced from the same trade data).

### SC-CHART-IX-06b — No new network requests on interactivity

**Steps:**
1. Open browser DevTools → Network tab.
2. Perform each interactive action: click heatmap tile, zoom equity curve, hover tooltip on each chart.

**Expected:** No new API calls are made during any interactive action. All interaction is over already-loaded data.

---

## Sign-Off

| Role | Sign-Off | Date | Evidence Method |
|------|----------|------|-----------------|
| QA & Testing Owner | Granted — 2026-03-18 | 2026-03-18 | Authoring review |
| Director of Quality | Pending | — | Local run required |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-18 | Initial scenarios. ST-11 / EPIC-04 (v2.1). 6 scenario groups, 16 sub-scenarios. |
