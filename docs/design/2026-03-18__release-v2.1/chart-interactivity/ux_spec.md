**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner
**Approved date:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Items:** ST-11 (CHART-IX)
**Frontend spec target:** docs/specs/frontend/pages/analytics.md (update §4, §5, §9 — v1.4 → v1.5)

---

# UX Spec — Chart Interactivity Enhancements (ST-11)

## 1. Purpose & User Goal

The three existing analytics charts are static visualisations. Users cannot interrogate individual data points or drill into specific months. Adding interactivity surfaces the data the user already has in more actionable ways — without recalculating or re-deriving values.

**User goal:** Hover over a chart to see exact values; zoom the equity curve to inspect a specific period; click a heatmap month to see the trades behind it.

**Constraint (non-negotiable):** No client-side re-derivation of values. All displayed values must match canonical backend response exactly.

---

## 2. Scope

Three charts are in scope for this story:
1. **Monthly Performance Heatmap** (§4 of analytics.md) — drill-down added; tooltip already exists
2. **Underwater Equity Curve** (§5 of analytics.md) — tooltip added; zoom added
3. **R-Multiple Distribution** (§9 of analytics.md) — tooltip added

---

## 3. Monthly Performance Heatmap — Drill-Down

### 3.1 Existing behaviour (retain)
- Hover tooltip: shows month, P&L, trade count, win rate. Already specced in analytics.md §4. No change.

### 3.2 New: Click → Drill-down
- Clicking a heatmap tile filters the trade list below the chart (or opens a contextual panel) to show only the trades from that month.
- **Implementation approach:** The drill-down filters the existing Trade History data in-context on the Analytics page. It does not navigate away. It does not re-fetch from the API.

**Drill-down behaviour:**
- Clicked tile receives a selected state (ring/border highlight using design system focus colour).
- A dismissible filter banner appears above the trade section: `"Showing trades from [Month YYYY] — [n trades]"` with a **"Clear filter"** X button.
- Clicking "Clear filter" or clicking the same tile again: removes the selection and restores the full trade view.
- Clicking a different tile: immediately updates the filter to the new month.

**Tile selected state:**
- Add a 2px inset ring in the design system's focus/accent colour.
- The tile's P&L colour and content do not change on selection.

**Data source:** `trades_for_charts` (already loaded on the analytics page). Month attribution: use `exit_date` for trade month assignment, consistent with how `monthly_data` is computed.

**Edge cases:**
- Tile with 0 trades: clicking has no effect (no drill-down action; cursor: default).
- Tile not in current period: should not be clickable (already handled by the period selector).

---

## 4. Underwater Equity Curve — Tooltip + Zoom

### 4.1 Tooltip (new)

Each data point on the equity curve is hoverable. Tooltip shows:
- **Date** — trade exit date (or date of the data point)
- **Drawdown %** — signed percentage below peak (e.g. `–8.3%`)
- **Drawdown £** — absolute amount below peak in GBP (e.g. `–£412.00`) if available from backend response
- **Peak equity** — the peak value at the time (GBP)

Tooltip positioning: follow cursor within the chart bounds; flip to left side if cursor is in the right 30% of the chart.

Data source: `trades_for_charts` cumulative sequence (same as the current chart render). All values displayed are derived from the same data the chart uses — no additional API call.

**Note on "derived":** The tooltip values are read directly from the chart's data series (each point already has date, drawdown % and amount). This is not client-side re-derivation — it is surfacing values already computed server-side and present in the chart data.

### 4.2 Zoom (new)

**Zoom type:** Time-axis zoom (x-axis only). Y-axis (drawdown %) auto-scales to the zoomed range.

**Trigger:** Scroll wheel over the chart, or pinch on touch. Alternatively (desktop fallback): two zoom buttons (`+` / `−`) in the chart's top-right corner.

**Zoom range constraints:**
- Minimum zoom: 4 data points (prevents over-zooming into a single-trade view)
- Maximum zoom: full data range (i.e. fully zoomed out = default state)
- Scroll/pinch zooms centred on the cursor position.

**Pan:** When zoomed in, the user can click-drag the chart to pan left/right within the zoomed range.

**Reset zoom:** A **"Reset"** button (small, top-right of chart) appears only when the user has zoomed in. Clicking restores the full range.

**Interaction states:**
- Default (not zoomed): no Reset button visible.
- Zoomed: Reset button visible; zoom buttons' state reflects current zoom level.
- A muted "Scroll to zoom" hint label may appear on first interaction and fade after 3s.

---

## 5. R-Multiple Distribution — Tooltip

### 5.1 Existing behaviour
The R-Multiple Distribution chart (§9 / §16 of analytics.md) is a bar/distribution chart showing the count of trades in each R-multiple bucket. Currently static.

### 5.2 New: Hover tooltip

Tooltip on each bar:
- **R-multiple range** — e.g. `"1.0R – 1.5R"` or `"< –1.0R"`
- **Trade count** — e.g. `"4 trades"`
- **% of total** — e.g. `"22% of closed trades"`

The `% of total` is computed from the backend-returned distribution data (total count is already in the response). This is a display transformation of returned data, not independent client-side re-derivation.

Tooltip positioning: follow cursor; flip if near chart edge.

---

## 6. Interaction Summary Table

| Chart | Interaction | New or Retained |
|-------|-------------|-----------------|
| Monthly Heatmap | Hover tooltip (month, P&L, trades, win rate) | Retained (already specced) |
| Monthly Heatmap | Click tile → drill-down to monthly trades | **New** |
| Underwater Equity Curve | Hover tooltip (date, drawdown %, £, peak) | **New** |
| Underwater Equity Curve | Scroll/pinch zoom on time axis | **New** |
| Underwater Equity Curve | Click-drag pan (when zoomed) | **New** |
| Underwater Equity Curve | Reset zoom button | **New** |
| R-Multiple Distribution | Hover tooltip (R range, count, % of total) | **New** |

---

## 7. UX Decisions Recorded

| Decision | Rationale |
|----------|-----------|
| Drill-down does not navigate away | Context is preserved; the user can compare the drilled view to the full chart without losing their place |
| Zoom on equity curve only (not heatmap or R-multiple) | Equity curve is time-series; zoom is meaningful. Heatmap is already monthly-granularity. R-multiple is a histogram; zooming would not improve readability. |
| Pan via click-drag (not scrollbar) | More intuitive for chart navigation; chart width is already constrained by the page layout |
| Tooltip for R-multiple shows % of total | Count alone is less informative; % reveals distribution shape without requiring re-computation |
| No new API calls for interactivity | All interaction state is derived from data already loaded; no latency introduced |
