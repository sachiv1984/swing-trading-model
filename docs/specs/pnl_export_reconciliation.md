**Owner:** Financial Reporting & Records Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-09-15 (v9.4 ST-16/BLG-FR-02: added §8 Journal-Derived P&L vs Broker-Statement Import Reconciliation — spec/dependency-mapping only, blocked on BLG-QA-122)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# P&L Export ↔ Trade Plan Closure Reconciliation

**Added:** ST-03 (EPIC-03, v7.6, BLG-FEAT-79)

## 1. Purpose

The tax-year P&L CSV/PDF export (`GET /reports/tax-year`, shipped v7.0, hardened v7.1) is sourced entirely from `trade_history` — it has no dependency on `trade_plans`. `trade_plans.status` is updated independently (see `docs/specs/data_model.md §trade_plans`) and can drift from `trade_history` if a plan's closure is never reconciled against the actual realised-P&L record it should correspond to (e.g. a partial fill, a manual correction, or a plan closed without the linked position ever completing the exit flow that writes a `trade_history` row).

This document specifies the reconciliation logic that detects that drift. It does not change the P&L export itself — `trade_history` remains the sole system of record for realised P&L (per `docs/specs/api_contracts/backend_engineering_patterns.md` — no change to that boundary).

## 2. Inputs

| Input | Source | Key fields used |
|-------|--------|------------------|
| Realised trades | `trade_history` (`database.get_trade_history(portfolio_id)`) | `id`, `position_id`, `ticker`, `pnl`, `exit_date` |
| Trade plans | `trade_plans` (`database.get_trade_plans(portfolio_id)`) | `id`, `position_id`, `ticker`, `status` |

Both tables link via `position_id` (nullable on both sides — see `data_model.md §trade_history`, `§trade_plans`). Reconciliation is scoped to rows where `position_id` is non-null on at least one side of a comparison; a `trade_history` row with no `position_id` was never linked to a plan and is not a mismatch (not every realised trade originates from a trade plan).

## 3. Reconciliation Rules

Two mismatch types are checked, both keyed on `position_id`:

1. **`closed_plan_no_trade_history`** — a `trade_plans` row has `status = 'closed'` but no `trade_history` row exists for the same `position_id`. This means the plan was marked closed without a corresponding realised-P&L record ever being written — an audit trail gap, since the tax-year export would never include this position even though the plan asserts it is done.
2. **`trade_history_plan_not_closed`** — a `trade_history` row exists for a `position_id` (i.e. the position was realised and is in the P&L export), and a `trade_plans` row exists for the same `position_id`, but that plan's `status` is not `'closed'` (still `'draft'` or `'active'`). This means the export already reflects the trade as realised, but its plan record has not caught up — a stale-state gap, not a financial discrepancy (no P&L figure is stored on `trade_plans` to compare numerically; see §4).

A `position_id` with a `trade_history` row and no `trade_plans` row at all is **not** a mismatch — most trades have no linked plan, and that is expected, not an error.

## 4. Explicit Non-Goal: No Numeric P&L Comparison

`trade_plans` stores no realised financial figures (no `pnl`, `exit_price`, or `proceeds` columns — see `data_model.md §trade_plans`). It is a pre-trade reasoning document (thesis, `r_target`, checklist), not a financial record. Reconciliation therefore cannot and does not compare a "planned P&L" against an "actual P&L" — that comparison already exists, at the individual-trade level, as `GET /trades/{id}/plan-vs-reality` (`backend/services/plan_vs_reality_service.py`, R-multiple/entry/stop deviation only). This document's reconciliation is a **structural closure-state check**, not a numeric one.

## 5. Implementation

Pure logic: `backend/services/pnl_reconciliation_service.py::reconcile_pnl_vs_trade_plans(trade_history, trade_plans) -> Dict` — takes already-fetched row lists (no DB coupling), returns:

```python
{
    "trade_history_count": int,
    "trade_plans_closed_count": int,
    "mismatches": [
        {"type": "closed_plan_no_trade_history", "position_id": str, "trade_plan_id": str, "ticker": str},
        {"type": "trade_history_plan_not_closed", "position_id": str, "trade_history_id": str, "trade_plan_id": str, "ticker": str, "plan_status": str},
    ],
}
```

Wrapper: `run_reconciliation(portfolio_id) -> Dict` — fetches from `database.get_trade_history` / `database.get_trade_plans` and calls the pure function.

## 6. Production Run Record

Per this item's acceptance criteria ("run once against production data with results recorded"), a one-time run was executed against production via the existing read-only `GET /trades` and `GET /trade-plans` endpoints (no new endpoint added — this is an operator-executed audit, not a user-facing feature). Results are recorded in `claude/cycles/2026-07-20__release-v7.6/qa_evidence_EPIC-03.md`.

## 7. Follow-Up

This is a one-time audit deliverable per BLG-FEAT-79's acceptance criteria, not a recurring job. If mismatches are found, they are filed as individual follow-up backlog items rather than fixed here (data correction requires case-by-case review — bulk auto-correction of `trade_plans.status` risks masking a real partial-fill or manual-correction scenario that a human should look at).

---

## 8. Journal-Derived P&L vs Broker-Statement Import Reconciliation (Spec/Dependency-Mapping Only — Blocked)

**Added:** ST-16 (EPIC-04, v9.4, BLG-FR-02)

**Status: not implementable this cycle.** This section defines the reconciliation calculation and tolerance so the spec is ready the moment its dependency clears — it does not itself add a runnable check. See §8.4.

### 8.1 Purpose

`BLG-FR-02` identified a gap distinct from §1–§7 above: there is no check comparing the system's own journal-derived realised P&L total (the same figure the tax-year P&L export at `GET /reports/tax-year` is sourced from — see §1) against the total reported on an imported broker statement for the same period. Today any discrepancy between the two is caught only if a user notices it manually.

### 8.2 Reconciliation Calculation

For a given reconciliation period (a tax year, to match the export this figure is compared against):

```
journal_total   = SUM(trade_history.pnl WHERE exit_date IN period)   # existing GET /reports/tax-year source data, see §1
broker_total    = <broker-statement-imported realised P&L for the same period>   # not yet obtainable — see §8.4
delta           = journal_total - broker_total
within_tolerance = abs(delta) <= max(tolerance_abs, tolerance_pct * abs(broker_total))
```

### 8.3 Acceptable Tolerance

`tolerance_abs = £1.00`, `tolerance_pct = 0.5%` (whichever is larger). Rationale: the two totals are expected to diverge by small, explainable amounts even when both are correct — FX-rate rounding on US-market trades (journal uses `fx_rate_used` at trade time, §Consistency Rules → GBP-Basis FX-Conversion Display Pattern in `design_system.md`; a broker statement uses its own settlement-date rate), and commission/fee timing differences (a broker statement may net fees into the same line the journal records separately). A tolerance tighter than this would flag routine, non-error divergence as a mismatch; a looser one risks masking a real data-entry or import error. This mirrors the tolerance-definition pattern already used for `trailing_stop_action_rate` (`metrics_definitions.md` — numeric Validation Tolerances subsection, ST-03/EPIC-01/v8.9) rather than inventing a new convention.

A discrepancy outside tolerance would surface the same way `mismatches` are reported in §5 above (a structured result the caller inspects) — no new UI surface is specified here, since none is implementable until §8.4 clears.

### 8.4 Dependency on BLG-QA-122 (Blocked)

This reconciliation cannot be implemented or run — not even as a one-time audit — because **no broker-statement import mechanism exists**. `BLG-QA-122` (Broker statement reconciliation) is gate-conditional on exactly this: "A broker statement import mechanism exists," and per `current_roadmap.md` §2 Product Scope Exclusions, broker API integration (execution) is a deferred, not strategically excluded, product boundary with no import path today.

`broker_total` in §8.2 has no data source until `BLG-QA-122`'s gate clears (a broker API import or a manual statement-upload path, whichever ships first). This document fixes the calculation and tolerance in advance precisely so that, once an import mechanism exists, implementation can proceed directly against this spec rather than re-deriving the reconciliation logic at that time.

### 8.5 Follow-Up

No implementation backlog item is filed by this story — implementation remains correctly scoped under `BLG-QA-122` itself, which already tracks the blocking dependency. Re-visit this section when `BLG-QA-122`'s gate criteria are met.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-09-15 | ST-16 (EPIC-04, v9.4, BLG-FR-02): Added §8 — journal-derived P&L vs broker-statement import reconciliation calculation and tolerance (`£1.00` or `0.5%`, whichever larger), with an explicit dependency note against `BLG-QA-122`'s blocked status. Spec/dependency-mapping only this cycle — not implementable until the `BLG-QA-122` gate clears (no broker-statement import mechanism exists). |
| 1.0 | 2026-07-20 | ST-03 (EPIC-03, v7.6, BLG-FEAT-79): Initial version. Specifies the two-way closure-state reconciliation between `trade_history` and `trade_plans`, the explicit non-goal of numeric P&L comparison (no financial columns on `trade_plans`), and the implementation location. |
