**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-08-04
**Cycle:** 2026-08-04__release-v8.2
**Backlog source:** BLG-FEAT-88
**Maps to:** EPIC-01, ST-01

---

# Decision Record — P&L Reconciliation Report

## 1. Problem

The Monthly P&L CSV export and individual trade records are both user-facing, but nothing confirms — or lets the user confirm — that the two reconcile to the same totals. `reports.md` already documents *internal* reconciliation rules between the Monthly CSV and Tax Year CSV (§Monthly CSV Export) and between the Combined Total and `GET /portfolio.total_pnl` (§Unrealised P&L Card), but both are QA-verified facts stated in prose — neither is a user-visible confirmation. This item adds a dedicated view that surfaces a system-total-vs-export-total comparison directly to the user.

## 2. Scope

**In scope:** a new "Reconciliation" tab on the Reports page (4th tab alongside Performance / Tax Year / Monthly), showing the system-computed realised P&L total for a selected year against an independently re-derived sum of that year's individual trade export rows, with a pass/fail match indicator.

**Out of scope:** reconciling unrealised P&L (already covered, with caveats, by the existing Combined Total note) or portfolio `total_pnl` (already covered by the existing approximate-tie-back rule). This view is scoped to the realised-P&L / trade-export relationship named in BLG-FEAT-88's problem statement.

## 3. Design Approach

No new visual language — this reuses existing, already-approved components verbatim:

- **Year Selector:** the page's existing shared control (`reports.md` §Year Selector)
- **Stat cards:** the same `text-xs uppercase tracking-wide` label / `text-lg font-semibold` value pattern used throughout the page (e.g. SI-02 Gate Status's Total Closed Trades / Linked to a Trade Plan grid)
- **Match badge:** the SI-02 Gate Status `MET`/`NOT MET` badge component verbatim — `bg-emerald-500/20 text-emerald-400 border-emerald-500/30` for a match, `bg-amber-500/20 text-amber-400 border-amber-500/30` for a discrepancy — relabelled "✓ Reconciled" / "⚠ Discrepancy — £X.XX difference"
- **Profit/loss colour convention:** `text-emerald-400` / `text-rose-400`, consistent with every other P&L figure on this page

## 4. Data Contract (shape only — not an implementation)

`GET /reports/reconciliation?year=YYYY` (new endpoint):

```
{
  "system_total_pnl_gbp": number,   // existing Tax Year summary realised total — unchanged computation
  "export_total_pnl_gbp": number,   // independently re-derived sum of trade_history.pnl for the year,
                                     // via a separate query path from the one powering the CSV export,
                                     // so a divergence is meaningful rather than definitionally impossible
  "matched": boolean                // server-computed, equal within £0.01 rounding tolerance
}
```

This design gate specifies the contract shape the endpoint must satisfy; implementing it (and filing the corresponding `## GET /reports/reconciliation` entry in `docs/specs/api_contracts/reports_endpoints.md` plus `docs/reference/openapi.yaml`, per `CLAUDE.md` §2) is sprint-execution scope, not design-gate scope.

## 5. States

| State | Content |
|-------|---------|
| Loading | Skeleton placeholder, matches existing page loading pattern |
| Success | Year Selector, System Total card, Export Total card, match badge |
| Error | "Unable to load reconciliation data" |
| Empty (no trades in selected year) | "No trade data available for {year} — reconciliation not applicable" |

## 6. Compliance Check

No conflict with `strategy_rules.md §13` — this is a read-only display of two already-existing computed figures; no new automated decision, scoring, or recommendation. Not an analytics/metrics feature under the canonical metric-definitions umbrella (it's a data-integrity confirmation, not a performance metric).

## 7. Sign-off

- **Head of UX & Design:** Approved — 2026-08-04 (reuses existing badge/card visual language verbatim; no new visual pattern introduced)
- **Financial Reporting & Records Owner:** Scope confirmed as matching BLG-FEAT-88's acceptance criteria — 2026-08-04
- **Product Owner:** Approved — 2026-08-04
