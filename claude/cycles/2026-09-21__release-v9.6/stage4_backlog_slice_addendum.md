**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-09-21__release-v9.6

# Post-Gate-Correction Addendum — 2026-09-21__release-v9.6

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

None of these changes adds or removes an item, changes a priority, or changes an effort estimate. Each is a clarification within an item's existing scope that the sealed text did not capture precisely enough (`design_gate_prompt.md` §4.1). Full rationale for each is in the linked design decision record.

## ST-01 — Cloned plan starts as `draft`, not `planned`
**Found at:** Design Gate STEP 2.2
**Correction:** AC 2 ("The cloned plan has status `planned`…") names a status that does not exist. `trade_plans.status` is `draft | research_pending | research_complete | entry_conditions_set | active | closed | abandoned` (`backend/database.py::ensure_trade_plans_extended_status`; `data_model.md` §Position & Trade Plan Lifecycle State Diagram; `trade_plan.md` §9). The lifecycle's only entry state is `draft`. Read AC 2 as: "The cloned plan has status `draft`, fresh dates and no `position_id`." Also fixed by the design: price-level fields and checklist completion state are not copied.
**Design record:** `docs/design/2026-09-21__release-v9.6/trade-plan-clone/decision_record.md`
**Date:** 2026-09-21

## ST-02 — "`planned`" means the four pre-entry statuses; age is measured from `updated_at`
**Found at:** Design Gate STEP 2.2
**Correction:** Same non-existent `planned` status as ST-01. The story's intent (plans not yet acted on) is applied to `draft`, `research_pending`, `research_complete` and `entry_conditions_set`; `active`, `closed` and `abandoned` are never marked. "Older than the threshold" is measured as whole days since `updated_at`, with the marker shown when `N > 14` (first appears at 15). Threshold is a single named constant. Display-only, as in the source scope.
**Design record:** `docs/design/2026-09-21__release-v9.6/trade-plan-stale-marker/decision_record.md`
**Date:** 2026-09-21

## ST-03 — Control label is "Download CSV"; export is the displayed rows
**Found at:** Design Gate STEP 2.2
**Correction:** The source scope's "Export CSV control" adopts the label already used on Reports ("Download CSV") for consistency. "Columns equal the visible columns" is read as the table's full desktop column set excluding the selection checkbox and Actions column, independent of viewport width; rows are those currently displayed after filters and sort. Adds a spreadsheet-formula-injection guard on string cells.
**Design record:** `docs/design/2026-09-21__release-v9.6/screener-watchlist-csv-export/decision_record.md`
**Date:** 2026-09-21

## ST-04 — Preference semantics and the reflection re-entry point
**Found at:** Design Gate STEP 2.2
**Correction:** (1) "Respects `NotificationPreferences`" is applied per the existing model: the toggle governs **email delivery only**; the in-app feed row is always created; the new "Reflection Reminder" email toggle **defaults to Off**. (2) The reflection is a route-less, skippable modal, so the reminder needs a way back to it: its "Write reflection" link targets `/TradeHistory?reflect={trade_id}`, which Trade History uses to open the existing `TradeReflectionModal`. This re-entry is part of the story's delivery, not a new item. (3) "Dismissing" is the existing "Mark as read"; completing the reflection after the reminder exists auto-marks it read.
**Design record:** `docs/design/2026-09-21__release-v9.6/reflection-reminder/decision_record.md`
**Date:** 2026-09-21

## ST-05 — Audit baseline and exclusion criterion for "0 audited empty states without a next-action link"
**Found at:** Design Gate STEP 2.2
**Correction:** The AC is measured against a defined audit. Baseline at this gate: 20 `emptyHeading` call sites — 4 already compliant, 5 to add an action, 9 dashboard cards to verify, 2 excluded as system-populated only (`AiDailyBriefing`, `WhatsNewCard`). For dashboard cards a next-action link is satisfied by the card's own `to` link. The story re-runs `grep -rn emptyHeading src` at build time; the baseline is not a substitute. The one trailing-period heading drift in `TradePlanCompletionRateSection.js` is fixed in the same touch.
**Design record:** `docs/design/2026-09-21__release-v9.6/empty-state-next-action/decision_record.md`
**Date:** 2026-09-21

## ST-06 — The convention the AC measures against is now defined
**Found at:** Design Gate STEP 2.2
**Correction:** AC ("identical negative/decimal conventions") presupposed a convention that existed in no spec. It is now `design_system.md` v1.21 §Number and Currency Formatting (typographic minus, en-GB grouping, 2 dp money, signed P&L, `—` for missing). The migration will change some visible strings (grouping separators, `-` → `−`, an explicit sign on Positions' P&L cell, 1 dp → 2 dp R-multiples); existing Playwright assertions matching the old strings are updated in the same commit and listed in the QA evidence file.
**Design record:** `docs/design/2026-09-21__release-v9.6/number-format-convention/decision_record.md`
**Date:** 2026-09-21

## ST-08 — Snapshot store is per month; the tax-year table gets a derived notice, not its own snapshot
**Found at:** Design Gate STEP 2.2
**Correction:** The sealed slice title says "snapshot of Monthly P&L **and the tax-year table**", but the source item (`BLG-FR-05`) scopes a snapshot "per closed month" and its ACs cover only that. The design follows the source item: one snapshot store (per closed month); the Tax Year summary bar shows an API-supplied "includes k restated month(s)" notice instead of holding a second snapshot. No acknowledge/re-baseline action. Months already closed at ship are baselined once, not retroactively flagged. If a tax-year-level snapshot is wanted, it is a separate item.
**Design record:** `docs/design/2026-09-21__release-v9.6/monthly-pnl-restatement-diff/decision_record.md`
**Date:** 2026-09-21
