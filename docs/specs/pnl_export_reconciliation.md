**Owner:** Financial Reporting & Records Owner
**Class:** Canonical Specification (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-20
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

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | ST-03 (EPIC-03, v7.6, BLG-FEAT-79): Initial version. Specifies the two-way closure-state reconciliation between `trade_history` and `trade_plans`, the explicit non-goal of numeric P&L comparison (no financial columns on `trade_plans`), and the implementation location. |
