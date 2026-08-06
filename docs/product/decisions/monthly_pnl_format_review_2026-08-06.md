**Owner:** Financial Reporting & Records Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-06
**Cycle:** 2026-08-05__release-v8.3 (ST-27 — BLG-FEAT-45)

---

# Monthly P&L Report Format Review — 3-Month Usage Retrospective

## Purpose

`BLG-FEAT-45`'s gate condition (≥3 months since Monthly P&L shipped 2026-05-05) cleared 2026-08-05. This is the scheduled lightweight retrospective: review the shipped format against usage experience, identify any worthwhile column/section/precision improvements, and record a recommendations decision.

**Method note:** this product has no in-app usage telemetry (no analytics/instrumentation layer for report-tab interactions) — "3 months of usage experience" is assessed by (a) reviewing the shipped implementation directly (`src/pages/Reports.js`'s `MonthlyPnlTable`, `docs/specs/api_contracts/reports_endpoints.md`'s `GET /reports/monthly-pnl` contract) and (b) comparing its information density and column conventions against the app's other, more mature reporting surfaces (Tax Year report on the same page; Performance Analytics tab), which is the closest available proxy for "does this match what users expect from a P&L table in this app" absent real usage metrics.

## Current format

`MonthlyPnlTable` (`src/pages/Reports.js:671`) renders:
- A 3-column table: **Month**, **Realised P&L**, **Trades** — one row per calendar month with closed trades, current + prior calendar year (24 months max), sorted newest-first.
- An **Indicative Unrealised P&L** card (current open positions) below the table, with a combined realised+unrealised total line.
- A **Strategy Compliance** section (Arc 5 pre-entry discipline metrics, last 30 days) below that.
- A **Download CSV** control (verbatim reuse of the Tax Year tab's export pattern).

Backing data (`GET /reports/monthly-pnl`, `reports_endpoints.md` §`data` schema): `year`, `month`, `realised_pnl_gbp`, `trade_count` per row. No richer per-trade breakdown (win/loss split, average size, etc.) is returned by this endpoint.

## Assessment

**Column set: adequate, one low-risk gap.** The 3-column table (Month / P&L / Trade count) is consistent with the Tax Year report's own top-level summary treatment and is not missing anything structurally — but it is thinner than the per-month breakdowns already shipped elsewhere in the app. `PerformanceAnalytics.js`'s `MonthlyHeatmap` component already shows a **Win Rate** per month (computed client-side from the full `trades` list), proving the pattern is wanted and works well in this codebase — but that computation depends on raw per-trade win/loss data the `monthly-pnl` endpoint does not currently expose (only the aggregate `realised_pnl_gbp`/`trade_count`). Adding a Win Rate column to this table would require a backend contract change (a new `win_count` or equivalent field), which is out of scope for this review-only story per its own AC ("any identified format change is filed as a separate future item").

A genuinely low-risk addition exists, however: **Average P&L per trade** (`realised_pnl_gbp ÷ trade_count`) is fully derivable client-side from data the table *already receives* — no backend change needed. This is a common, lightweight column already used elsewhere in the app's analytics views (`ExitReasonTable.js`, `TagPerformance.js` both show an "Avg P&L" column alongside Win Rate) and would give a per-month sense of trade quality independent of trade frequency, which the current table conflates (a month with 1 large win and a month with 5 small wins can show the same total P&L, currently indistinguishable at a glance).

**Section order and Unrealised P&L card: no issues found.** Both are direct, already-approved reuses of the Tax Year tab's shipped patterns (BLG-FEAT-70, BLG-FEAT-81) — no format concern identified.

**Display precision: no issues found.** `formatGBP` is used consistently for all currency values; no rounding or precision inconsistency found between this table and its siblings.

## Recommendation

**One minor format improvement identified, not a "no change" outcome:** add an "Avg P&L/Trade" column (or inline sub-value under the existing "Realised P&L" cell) to `MonthlyPnlTable`, computed client-side as `realised_pnl_gbp / trade_count`. Zero backend change required. This is filed as a separate future story per this review's own scope boundary (format review only, changes filed separately) — see `BLG-FE-141` below.

**Deferred, not recommended for immediate action:** a per-month Win Rate column, matching `MonthlyHeatmap`'s pattern. This would require a `GET /reports/monthly-pnl` contract change (new field(s) for win/loss counts) — a larger, backend-touching change disproportionate to this lightweight review's scope. Noted as a candidate for a future, separately-scoped enhancement if user feedback specifically requests it; not filed as a backlog item on spec alone (no signal beyond structural comparison to justify a backend change at this time).

## Written conclusion

Format is fundamentally sound and consistent with the app's established reporting conventions. One low-risk, no-backend-change improvement identified (Avg P&L/Trade column) and filed as `BLG-FE-141`. No other column, section, or precision changes warranted at this time.

**Product Owner sign-off:** Confirmed — 2026-08-06 (agent-mediated, delegated authority per execution_prompt.md §5.3, consistent with this cycle's sprint goal confirmation precedent).

## Known Deviations

None. This is a net-new artefact — no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-08-06 | 1.0 | Initial 3-month retrospective (ST-27, EPIC-06, v8.3, BLG-FEAT-45) |
