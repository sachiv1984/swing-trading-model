**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-17
**Approved by:** Product Owner — 2026-07-17
**Story:** ST-03 — Multi-select and bulk-action toolbar on Watchlist/TradePlans (EPIC-03, BLG-FE-117)
**Depends on:** `docs/specs/blg_fe_117_pre_implementation_readiness_pass.md` — this artefact adopts that readiness pass's batch-mutation endpoint pattern, toolbar-absent-at-zero-selected recommendation (§AC-05), and Playwright scenario list as its technical baseline
**Cycle:** 2026-07-17__release-v7.5

---

# UX Specification — Bulk Actions Toolbar

## 1. Context

Watchlist and Trade Plans tables today support only single-row actions (Edit/Remove, Edit/Delete). The readiness pass confirmed no existing multi-select or toolbar pattern exists anywhere in the codebase — this is a net-new UI pattern applied identically to both tables. It also confirmed no existing batch-mutation endpoint exists; new per-entity batch endpoints (`POST /positions/bulk-tag`, `DELETE /trade-plans/bulk`, `DELETE /watchlist/bulk`) are the technical foundation this spec assumes.

## 2. Decision

### 2.1 Row Selection

Each table row on Watchlist and Trade Plans gains a checkbox as the first column (left of Ticker). The table header gains a header checkbox: unchecked → checked selects all rows currently visible (i.e. all rows matching the active filter, not all rows in the dataset if paginated — see §2.5).

Selecting a row highlights it with a subtle background tint (consistent with existing row-hover treatment, but persistent while selected).

### 2.2 Bulk-Action Toolbar

Per readiness pass AC-05 recommendation (adopted): **the toolbar does not render at all when zero rows are selected.** Its presence is itself the selected-state indicator — no "0 selected" empty state is designed.

When 1+ rows are selected, a toolbar renders directly above the table (below the page header / above the existing filter or Add button row), containing:

| Element | Content |
|---------|---------|
| Selected count | `"{N} selected"` |
| Bulk actions | Buttons for the actions valid on this table (see §2.3) |
| Clear selection | "Clear" (text button, right-aligned) — deselects all rows, toolbar disappears |

### 2.3 Available Actions Per Table

| Table | Available bulk actions |
|-------|------------------------|
| Watchlist | Bulk Tag, Bulk Remove |
| Trade Plans | Bulk Tag, Bulk Archive*, Bulk Delete |

*"Archive" on Trade Plans maps to the existing "Abandon" status transition (`trade_plan.md` §8) applied to each selected plan — reuses the existing single-plan abandonment semantics, not a new status. Bulk Archive is hidden from selection if any selected plan already has `status = 'active'` (mirrors the existing single-item Abandon hide rule) — instead, an inline note in the toolbar reads: `"{N} active plan(s) excluded — cannot be archived."` and the action applies only to the eligible subset.

### 2.4 Bulk Tag Flow

Clicking "Bulk Tag" opens an inline expand (not a modal) below the toolbar with the existing Tag Editor component (autocomplete input, reused from `journal_components.md` §4 / `trade_plan.md` §5c). Tags entered here are **added to** (not replacing) each selected row's existing tag set. Submit calls the entity's bulk-tag endpoint (`POST /positions/bulk-tag` for Watchlist entries — reusing the position-tag endpoint per readiness pass AC-01's mapping — or the trade-plan equivalent).

### 2.5 Bulk Delete / Bulk Archive — Confirmation (readiness pass AC-04 scenario 4)

Both are destructive. Clicking the action shows a confirmation dialog (reuses the existing modal confirmation pattern, e.g. Watchlist's Remove confirmation):

> `"{Delete / Archive} {N} selected trade plan(s)?"` (or "watchlist entries")

- Primary destructive button confirms and fires the batch call.
- "Cancel" dismisses; selection is retained.

### 2.6 Partial-Failure Feedback (readiness pass AC-01 response shape)

The batch response returns `{ succeeded: [...], failed: [{id, reason}] }`. On completion:

- If all succeeded: toast `"{N} {items} updated."`; rows removed/updated; selection cleared.
- If partial failure: toast `"{N} succeeded, {M} failed."` with an inline expandable detail listing the failed IDs and their `reason` (e.g. ticker, reason string) — per-row feedback, not a single opaque message (readiness pass AC-01 hard requirement).

### 2.7 Select-All Scope

"Select all" (header checkbox) selects all rows in the **current filtered/visible view only**, not the full unfiltered dataset. The toolbar's selected-count label makes this unambiguous: `"{N} selected"` where N always equals the count of checked rows, never an inferred "all matching" total. This avoids the readiness pass's flagged risk of a user believing "select all" selected more than is visible (AC-04 scenario 5). Neither Watchlist nor Trade Plans currently paginate, so this distinction is dormant today but the copy convention is fixed now to avoid rework if pagination is added later.

## 3. §13 Compliance

Per readiness pass AC-03 (PASS): bulk actions are a user-initiated batch of the same manual mutations already available one row at a time (tag, delete, abandon). No new automated decision-making or scheduled execution. No trade or position-sizing logic.

## 4. States

| State | Behaviour |
|-------|-----------|
| 0 selected | Toolbar absent |
| 1+ selected | Toolbar visible, count + actions shown |
| Bulk Tag expanded | Tag Editor inline below toolbar |
| Destructive action clicked | Confirmation dialog shown |
| Batch call in flight | Toolbar action buttons disabled; spinner on the active button |
| Batch — all succeeded | Toast; rows updated/removed; selection cleared; toolbar disappears |
| Batch — partial failure | Toast + expandable per-row detail; failed rows remain selected/visible |

## 5. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-17
- **Product Owner:** Approved — 2026-07-17
