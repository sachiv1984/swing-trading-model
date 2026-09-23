**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-23__release-v9.7
**Story:** ST-02 (EPIC-02, BLG-FE-186)

# Decision Record — Clone Preserves Source Setup Type

## 1. Problem

`trade_plan.md` §4.5's Clone as New Plan copy/reset table (v1.15) does not mention `setup_type` at all — it was omitted from both the "Copied" and "Reset / not copied" columns when §4.5 was written (v9.6). In the live implementation (`TradePlan.js`), the clone effect does not carry `setup_type` forward from the source plan, so it lands `null` on the cloned form. Separately, an existing pre-population effect (`linkedSignal`, used for brand-new plans against a watchlisted ticker) fires whenever `!editId && linkedSignal` — which is also true for a clone, since cloning uses the same "new plan" URL shape (`?clone_from=`) rather than an edit route. That effect sets `setup_type: prev.setup_type || "Momentum Continuation"`. Because the clone never populated `prev.setup_type`, a clone of a ticker that also happens to have a live watchlisted signal silently gets overwritten to "Momentum Continuation" regardless of the source plan's actual Setup Type.

## 2. Decision

### 2.1 Clone copies `setup_type`

`setup_type` is added to §4.5's "Copied" column: the clone always carries the source plan's `setup_type` forward unchanged, including when the value is `null` (a source plan with no Setup Type set clones to no Setup Type set — this is not backfilled from a watchlisted signal).

### 2.2 Watchlisted-signal auto-fill must not override a copied value

No behaviour change is needed to the pre-population effect's own condition (`prev.setup_type || "Momentum Continuation"`) once 2.1 is implemented — copying the source value first means the auto-fill's existing "only fill if empty" guard already does the right thing. This decision exists to make that interaction explicit and spec'd, not to introduce a new guard: **the spec's intent is that an explicit copied value always wins over the watchlisted-signal default**, so any future refactor of either code path must preserve that ordering.

### 2.3 Scope

This is a correctness fix to existing, already-approved clone behaviour (§4.5 was designed to be a full-fidelity copy of the source plan's own field values, per its "Copied" column's existing intent for `setup_thesis`/`invalidation_condition`/`r_target`) — no new component, layout, or interaction is introduced. Classified Design Required only because the omission was in the copy/reset table itself, not in a rendering detail; the fix is documenting the table correctly and confirming the implementation matches it.

## 3. §13 Compliance

No AI call, no recommendation. §13 pre-check does not apply.

## 4. Frontend Spec Impact

`trade_plan.md` v1.15 → v1.16: §4.5's copy/reset table gains a `setup_type` row in "Copied"; a footnote records the auto-fill ordering in §2.2 above.

## 5. Testability (CLAUDE.md §2)

Playwright: clone a plan with a non-null `setup_type` whose ticker also has a live watchlisted signal — the cloned form must show the source's `setup_type`, not "Momentum Continuation". A second case: clone a plan with `setup_type = null` and a watchlisted-signal ticker — the cloned form retains the existing auto-fill behaviour (fills "Momentum Continuation") since there is no copied value to protect.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-23.
Product Owner: confirmed, 2026-09-23.
