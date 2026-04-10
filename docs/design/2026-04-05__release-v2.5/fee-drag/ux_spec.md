**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-04-06
**Cycle:** 2026-04-05__release-v2.5
**Story:** ST-09 — Fee drag metric on Trade History
**Approved by:** Product Owner (2026-04-06)

---

# UX Decision Record — Fee Drag Metric (ST-09)

## Purpose

Define the visual and interaction specification for the "Avg Fee Drag" StatsCard and "Fee Drag %" column added to the Trade History page in v2.5.

---

## Component 1 — Avg Fee Drag StatsCard

### Data Source
- Field: `avg_fee_drag_pct` from GET /trades response envelope
- Computed server-side: mean of `fee_drag_pct` across all trades with `gross_proceeds > 0`

### Layout
- Positioned after "Avg Slippage" in the Summary Stats row
- Same StatsCard component used by all other summary stats on the page
- Must render with gradient background (consistent with other StatsCards)

### Display Format
- Value: `+X.XX%` — always prefixed with `+` to denote cost direction (fees are a cost)
- Example: `+0.42%`
- Decimal precision: 2dp

### Colour Treatment
- Use amber/orange tone from design system (e.g. `color="amber"` or equivalent)
- Rationale: fee drag is always a cost (no green/red binary — not profit/loss); amber conveys a neutral-to-unfavourable cost metric
- Do NOT use green/red — those are reserved for P&L and slippage direction

### Tooltip (info icon ⓘ adjacent to label)
> "Average Fee Drag = Total exit fees / Gross proceeds × 100"
> "Higher % means a greater proportion of gross proceeds consumed by fees."

### Null / Empty State
- Not applicable: `avg_fee_drag_pct` is always populated when at least one trade has `gross_proceeds > 0`
- If no trades exist (empty state): component not rendered (standard empty state behaviour)

---

## Component 2 — Fee Drag % Column in TradeHistoryTable

### Data Source
- Field: `fee_drag_pct` per trade from GET /trades response
- Computed server-side: `exit_fees / gross_proceeds × 100`, rounded to 2dp

### Column Position
- After "Slippage" column; before "Days held" column
- Column header label: **"Fee Drag %"**

### Column Header Tooltip (info icon ⓘ)
> "Fee Drag % = Exit fees / Gross proceeds × 100"
> "Measures the proportion of gross sale proceeds consumed by broker exit fees."

### Display Format
- `+X.XX%` — always prefixed with `+` (fee is always a cost)
- Examples: `+0.38%`, `+1.20%`, `+0.05%`

### Colour Treatment
- Amber/neutral tone — consistent with the StatsCard
- Do NOT use green/red (fee drag is not directional in the P&L sense)

### Null Handling
- Always populated: `fee_drag_pct` is always present for closed trades with `gross_proceeds > 0`
- No `—` state required per AC

### Sortable
- Yes — ascending and descending
- Sort direction: ascending = lowest fee drag first

### Naming Constraint
- The metric is labelled **"Fee Drag %"** throughout — never "slippage"
- Tooltip and column header must not contain the word "slippage"

---

## Interaction Notes

- No new interactive behaviour introduced — StatsCard and table column follow existing page patterns
- Row expansion (expandable journal) is not affected
- Filter panel is not affected

---

## Frontend Spec Update Required

`docs/specs/frontend/pages/trade_history.md` must be updated to v1.5 to reflect this design.

Updates required:
1. Summary Stats section: add "Avg Fee Drag" stat entry
2. Trade History Table columns list: add "Fee Drag %" column
3. New "Fee Drag % Column" spec section (parallel to existing Slippage Column section)
