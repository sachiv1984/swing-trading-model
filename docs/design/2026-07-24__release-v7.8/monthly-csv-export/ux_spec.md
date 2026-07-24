**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Active
**Last Updated:** 2026-07-24
**Cycle:** 2026-07-24__release-v7.8
**Backlog source:** BLG-FEAT-81
**Maps to:** EPIC-05, ST-05

---

# UX Spec — Monthly Realized P&L CSV Export

## 1. Problem

`reports.md`'s Monthly P&L Report (§Monthly P&L Report) has no export control — only the Tax Year tab has PDF/CSV export (§Page Header Controls). Users who want a monthly-granularity export currently have no way to get one; they must derive it manually from the tax-year CSV.

## 2. Placement & Pattern

**Decision:** reuse the Tax Year tab's "Download CSV" button verbatim (idle/generating/success/error states, same visual weight, same interaction model) — no new pattern invented. Placed at the top of the **Monthly P&L Report** view, aligned right, as a header control for that view specifically (the Monthly P&L Report and Tax Year tab are separate views on the Reports page; each gets its own export control scoped to its own data).

```
Monthly P&L Report                              [ Download CSV ]
```

On narrow screens: button drops below the section header, full width — same responsive rule as the Tax Year tab's header controls.

## 3. Export Content

Exports exactly the rows currently rendered in the **Monthly Financial Table** (`reports.md` §Monthly Financial Table) for whatever range is already loaded (current and prior calendar years, per that section) — no separate date-range picker. Columns: `Year`, `Month`, `Realised P&L (GBP)`, `Trades` — same fields as the on-screen table, no client-side recalculation (consistent with the page's existing "must not recalculate P&L" rule, `reports.md` §API Reference).

**Reconciliation (AC):** for any calendar year present in both exports, summing that year's rows in the monthly CSV must equal the realised P&L total in that year's Tax Year CSV — both derive from the same `trade_history.pnl` ledger, just grouped differently (by month vs. by UK tax year). This is a verification check for QA evidence at sprint execution, not a UI-visible feature.

## 4. Button States (identical pattern to Tax Year §Download CSV Button States)

| State | Label | Behaviour |
|-------|-------|-----------|
| Idle | **"Download CSV"** (with download icon) | Enabled when the Monthly P&L Report has loaded successfully |
| Generating | **"Generating…"** (spinner replaces icon) | Button disabled; fires `GET /reports/monthly-pnl?format=csv` |
| Success | Returns to Idle | Browser file download begins; no success toast required |
| Error | Returns to Idle | Toast notification: `"CSV generation failed. Please try again."` (auto-dismiss 5s) |

Valid for empty ranges (zero closed trades in any month) — same rule as the Tax Year export. Button always enabled once the Monthly P&L Report loads.

## 5. Backend Dependency

Requires a new `format=csv` handler on `GET /reports/monthly-pnl` (today only returns JSON), mirroring the existing `GET /reports/tax-year?format=csv` implementation. Implementation detail for sprint execution — API contract entry required in `docs/specs/api_contracts/` in the same commit per `CLAUDE.md` §2.

## 6. Out of Scope

- CSV export of the §Unrealised P&L Card or §Strategy Compliance Section figures (AC scope is the monthly realised P&L table only, matching the Tax Year export's scope of the realised summary/trades table, not its Unrealised P&L Card)
- A unified "export both" control — kept as two independent buttons on two independent views, consistent with the page's existing tab/view separation

## 7. Compliance Check

No conflict with `strategy_rules.md §13` — a read-only export of already-displayed, already-approved data, no new computation.

## 8. Sign-off

- **Head of UX & Design:** Approved — 2026-07-24 (verbatim reuse of existing CSV export pattern, per §2/§4)
- **Product Owner:** Approved — 2026-07-24
