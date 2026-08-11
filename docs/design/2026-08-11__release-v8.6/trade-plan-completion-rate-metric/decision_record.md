**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-11
**Cycle:** 2026-08-11__release-v8.6
**Story:** ST-01 (BLG-FEAT-32, EPIC-01)

# UX Decision Record — Trade Plan Completion Rate (Performance Analytics Page)

## 1. Problem

No view shows what proportion of created trade plans are completed (result in a closed trade) vs abandoned — the completion rate PT-04 (Setup Quality Score, shipped v6.1) was scoped to eventually correlate against. Classified Design Required per `design_gate_prompt.md` §6 ("new data displayed").

## 2. Decision

A new, compact **"Trade Plan Completion Rate"** section on the Performance Analytics page (`analytics.md`), appended after §20 Behavioural Drift as new §21 — the same "append after the last shipped metric section" placement convention used by every prior analytics addition (Cohort Analysis, Discipline & Compliance, Market Correlation, Arc 5 Signal Compliance, Behavioural Drift all followed this pattern).

**Contents — three summary cards** (matching the §13 Consistency Metrics 3-card layout, the closest existing precedent for a small, non-chart metric group):

| Card | Field | Format |
|------|-------|--------|
| Plans Created | `plans_created` | integer |
| Completion Rate | `completion_rate` | percentage, 1dp, coloured green ≥60%, amber 40–59%, red <40% (mirrors the existing Win Rate Consistency qualitative-threshold convention, §13) |
| Plans Abandoned | `plans_abandoned` | integer + `(N%)` of `plans_created` in muted secondary-text token (`text-slate-600 dark:text-slate-400`, per `design_system.md`'s canonical secondary-text token) |

`plans_completed` is not given its own card — it is implied by `completion_rate` and shown instead as a one-line summary beneath the cards: `"{plans_completed} of {plans_created} plans completed"`.

**Optional segmentation (AC's "Optional: segmented by setup quality score tier"):** a small breakdown table beneath the summary cards, one row per PT-04 quality tier (`Excellent` / `Good` / `Fair` / `Low` — the exact labels already established at `trade_plan.md` §7a), each row showing that tier's own `completion_rate`. Rendered only when the backend response includes tier-segmented data; omitted entirely (not shown as an empty table) when it doesn't, consistent with this page's existing null-safety convention (`analytics.md` "Empty & Null Safety").

## 3. Rationale

- Reusing the §13 Consistency Metrics 3-card shape avoids introducing a new card-layout pattern for what is, structurally, the same kind of small numeric-summary group.
- Reusing the existing green/amber/red threshold convention (already established for Win Rate Consistency, §13) and the canonical secondary-text token (§Color Usage, `design_system.md`) keeps this section visually consistent with the rest of the page rather than inventing a new colour rule.
- The quality-tier breakdown is optional per the AC and per the backend response shape — designing it as an omit-if-absent table (rather than a required stub) avoids committing to backend scope this design gate doesn't own.
- No new component: percentage cards and a simple breakdown table are both existing primitives on this page.

## 4. Data source and edge cases

- New aggregate query: `plans_created`, `plans_completed`, `plans_abandoned`, `completion_rate` (source: `trade_plans.status` — `completed` when a closed trade exists via the position linkage strengthened by `BLG-BE-91`/ST-03 this same cycle; `abandoned` per existing status enum).
- Zero plans created: render the section's `DataState` `empty` branch (`design_system.md` §Data States) with the message `"No trade plans created yet."` — not a `0%` completion rate, which would misleadingly imply plans existed and none completed.
- `plans_abandoned` percentage denominator is `plans_created`, guarding div-by-zero the same way as every other percentage field on this page (`Empty & Null Safety`).

## 5. Scope boundary

Performance Analytics page only. Does not touch `trade_plan.md`'s own detail/list views, PT-04's score display (§7a, unchanged), or `BLG-BE-91`'s entry-flow enforcement work (this cycle, EPIC-02) beyond consuming its downstream effect on plan/position linkage completeness. Does not add a trend-over-time view — the AC calls for a computable/displayable metric, not a historical chart; a trend view remains a future option if this proves insufficient.

## §13 check

Aggregation and display of existing trade-plan/position data; no automated decision, no AI call. Not applicable.
