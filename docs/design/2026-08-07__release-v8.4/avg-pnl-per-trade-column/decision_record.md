**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-07
**Cycle:** 2026-08-07__release-v8.4
**Story:** ST-01 (BLG-FE-141, EPIC-01)

# UX Decision Record — Avg P&L/Trade Column (Monthly P&L Report)

## 1. Problem

The Monthly Financial Table on the Monthly P&L Report (`docs/specs/frontend/pages/reports.md` §Monthly Financial Table) currently displays `Year`, `Month`, `Realised P&L`, `Trades` per row. It has no per-trade average figure — a user reading a month with a large realised P&L and a large trade count has no quick way to see whether that month's edge was a few big wins or many small ones. No prior artefact covers this column, so it is classified Design Required per `design_gate_prompt.md` §6 ("new data displayed"). The genuine design decision is narrow (placement, formatting, colour, and the zero-trade edge case), so this is scoped as a lightweight decision record rather than a full UX spec.

## 2. Column

| Column | Field | Notes |
|--------|-------|-------|
| Avg P&L/Trade | *derived* | `realised_pnl_gbp / trade_count` for that row, GBP, 2dp |

Placement: rightmost column, after `Trades` — reads left-to-right as "here's the month, here's the total, here's the count, here's the average," matching the natural derivation order.

This is client-side display arithmetic on two already-fetched fields from the same row — not a recalculation of `realised_pnl_gbp` itself, and not a new endpoint. Consistent with the page's existing "no client-side recalculation" rule, which the Combined Total Line (§Unrealised P&L Card) already establishes permits exactly this kind of derived-display arithmetic on already-fetched values.

## 3. Formatting and colour

Same currency formatting as `Realised P&L` (£, 2dp, thousands separator). Same colour rule too: `text-emerald-400` if positive, `text-rose-400` if negative or zero — consistent with `Realised P&L`'s existing green-positive/red-negative-or-zero convention (§Monthly Financial Table), so the two columns read as a matched pair rather than introducing a second colour rule for the page to track.

## 4. Zero-trade edge case (the genuine decision this record exists for)

`trade_count = 0` makes `realised_pnl_gbp / trade_count` undefined. Display **"—"** (em dash, no colour) rather than `£0.00`, `NaN`, or `Infinity` — `£0.00` would misleadingly imply a computed zero average rather than "no trades to average." This matches the page's existing empty-state convention of using a dash/explicit "no data" treatment rather than a numeric placeholder (see §Monthly Financial Table empty state, "No monthly P&L data available yet.", for the same no-fabricated-zero principle at the table level).

Single-trade months: no special case — `realised_pnl_gbp / 1` is just `realised_pnl_gbp`, correct as-is.

## 5. Scope boundary

Applies to the Monthly Financial Table only. Does not touch the Tax Year tab's table (out of scope per the story), the Monthly CSV export (unaffected — export column set is unchanged by this story), or the Unrealised P&L Card / Strategy Compliance Section.

## §13 check

Purely presentational derived arithmetic; no automated decision or AI call. Not applicable.
