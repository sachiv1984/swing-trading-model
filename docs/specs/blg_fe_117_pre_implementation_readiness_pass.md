**Owner:** Backend Engineering Patterns Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-16
**Story:** ST-06 (BLG-SPEC-93, EPIC-04, v7.3)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# BLG-FE-117 Pre-Implementation Readiness Pass — Bulk Actions

## 1. Purpose

Close every pre-implementation information gap for `BLG-FE-117` (multi-select + bulk tag/archive/remove actions) before it can be scoped into a future sprint (candidate: v7.4). This is a spec/scoping pass only — no code is written here. `BLG-FE-117` itself remains deferred (see `stage4_backlog_slice.md#Deferred-Items`).

## 2. AC-01 — Single-Call Batch-Mutation Endpoint Pattern

**Finding: no existing batch-mutation endpoint pattern exists in `backend/routers/` to extend.** Grep across `backend/routers/*.py` for `batch`/`bulk` found only `screener_batch_service` (a batch **read** — running the screener across many tickers, not a mutation) — no precedent for a single-call multi-row **write**. The only mutation candidates today are strictly single-item: `PATCH /positions/{position_id}/tags` (replaces one position's tag set), `DELETE /trade-plans/{id}`, `DELETE /watchlist/{entry_id}` (`docs/specs/api_contracts/position_endpoints.md`, `trade_plan_endpoints.md`, `watchlist_endpoints.md`).

**Proposed pattern (for `BLG-FE-117` to apply):** one endpoint per (entity, action) pair, accepting an array of IDs, consistent with the project's existing per-entity router structure (no new generic "bulk" router):

```
POST /positions/bulk-tag        { ids: [uuid], tags: [string] }   -- applies PATCH /positions/{id}/tags semantics per id
DELETE /trade-plans/bulk        { ids: [uuid] }                    -- applies DELETE /trade-plans/{id} semantics per id
DELETE /watchlist/bulk          { ids: [uuid] }                    -- applies DELETE /watchlist/{entry_id} semantics per id
```

**Partial-failure handling (the key new design question a batch endpoint introduces that single-item endpoints don't have):** each endpoint must process all IDs and return a per-ID result array rather than failing the whole call on the first error — consistent with `conventions.md`'s standard success envelope, extended with a results breakdown:

```json
{
  "status": "ok",
  "data": {
    "succeeded": ["id1", "id2"],
    "failed": [{ "id": "id3", "reason": "not_found" }]
  }
}
```

This avoids an all-or-nothing transaction across unrelated rows (a failure on one trade plan should not block deleting the other 9 selected). Full envelope/error-shape conformance to `conventions.md §2`/`§13` otherwise applies unchanged. Max batch size (recommend capping at 100, consistent in spirit with the 10-tag/20-char limits already set on `PATCH /positions/{id}/tags`) is an implementation-time decision for `BLG-FE-117`, not fixed here.

## 3. AC-02 — Base44 Prompt Template

Added below (§8 of this pass) and cross-filed into `docs/specs/frontend/base44_prompt_template_library.md` in the same commit (Case B, `execution_prompt.md` STEP 3.1.A — the created artefact is its own spec reference).

## 4. AC-03 — §13 Pre-Check

**PASS.** Confirmed against `claude/strategy/strategy_rules.md §13.1`/`§13.2` ("human-in-the-loop by design"; "not an automated trading bot"). Bulk actions are, by construction, a **user-initiated batch of the exact same manual mutations already available one-at-a-time today** (tag, delete a trade plan, delete a watchlist entry) — the user explicitly selects rows and explicitly presses one bulk-action button, identical in kind to today's single-row action requiring an explicit click. No new automated decision-making, no scheduled/triggered execution, no trade or position-sizing logic is introduced — this is strictly a UI/API efficiency feature over existing human-initiated mutations. No follow-up required; no decision escalation needed.

## 5. AC-04 — Playwright Coverage Plan (Scenario List, Not Yet Implemented)

Per `claude/system/shared_standards.md §18` (Playwright Test Authoring Standard — no `networkidle`, mock payloads must match the canonical API spec shape), the following scenarios should be authored when `BLG-FE-117` implements:

1. Select 2+ rows via checkbox → bulk-action toolbar appears with correct selected-count.
2. Deselect all → toolbar returns to zero-selected state (see AC-05).
3. Bulk tag action on a mixed valid/invalid ID set → mocked `succeeded`/`failed` response renders correctly (toast/inline feedback distinguishes the two, per the AC-01 partial-failure response shape).
4. Bulk delete (trade plans or watchlist) → confirmation step required before the destructive call fires (no existing precedent for a confirm-dialog-free destructive bulk action anywhere in the codebase — `BLG-FE-117` must not skip this).
5. Select-all-visible vs select-all-matching-filter (if pagination/filtering is in scope for the target page) — distinguish explicitly in the UI copy per the scenario, to avoid a user believing "select all" selected more rows than are currently visible.
6. Dual-theme rendering of the toolbar and its selected-count badge (per `Base44 Prompt Template Library §4` Dual-Theme Verification Call-Out — mandatory for any visual story).

Mock payloads for scenario 3 must mirror the exact `succeeded`/`failed` shape defined in AC-01, once that shape is finalised in `openapi.yaml` at implementation time — not a flattened approximation (`shared_standards.md §18` Mock payload advisory).

## 6. AC-05 — `DataState`/Design-System Consistency for Zero-Selected State

**Finding: genuine gap — no existing toolbar or "N selected" pattern exists.** Grep across `design_system.md` and `src/pages/` found no existing multi-select toolbar precedent (the only existing checkbox usages — `TradePlan.js`'s single acknowledgement checkbox, `ComplianceRecheckModal.js` — are single-checkbox confirmation controls, not row-multi-select). This is a new UI pattern, not a reuse of an existing one.

**Recommended design (for `BLG-FE-117` to apply and formalise in `design_system.md` at implementation time):** the bulk-action toolbar itself should not render at all when zero rows are selected (no "0 selected" empty state to design — the toolbar's presence *is* the selected-state indicator, consistent with the common "contextual toolbar" convention and avoiding a wasted `DataState` empty-state build for a state that's better expressed as "toolbar absent"). This is simpler than reusing `DataState` and is the recommendation carried forward; `BLG-FE-117` should confirm this against the Head of UX & Design at implementation time rather than treating it as fixed by this pass, since it is a UX judgment call, not a technical constraint.

## 7. Scope Completeness Summary

All 5 acceptance criteria (AC-01 through AC-05) addressed: AC-01 (new batch-mutation pattern designed per entity, with an explicit partial-failure response shape — the genuine new design question a batch endpoint raises over single-item endpoints), AC-02 (delivered as a library entry, §8 below / `base44_prompt_template_library.md`), AC-03 (§13 pre-check **PASS**, no follow-up), AC-04 (six-scenario Playwright coverage plan drafted, referencing the project's mock-payload and no-`networkidle` standards), AC-05 (documented as a genuine new-pattern gap with a recommended toolbar-absent design, flagged for UX confirmation rather than fixed here). `BLG-FE-117`'s own acceptance criteria at its next sprint planning cycle should reference this readiness pass as its implementation baseline.

## 8. Base44 Prompt Template — Bulk-Action Toolbar (Multi-Select + Bulk-Action Pattern)

*(Cross-filed into `docs/specs/frontend/base44_prompt_template_library.md` in the same commit — reproduced here for this pass's own completeness.)*

**Use when:** delegating `BLG-FE-117` or any future story adding row-level multi-select with a bulk-action toolbar.

**Reusable fragment — Behaviour Rules section:**
```
- Row-level checkbox selection; bulk-action toolbar renders only when 1+ rows are selected (no zero-selected empty state to design — see readiness pass AC-05).
- Toolbar shows a live selected-count and the available bulk actions for the current entity (tag / archive / remove, per AC-01's per-entity endpoint set).
- Destructive bulk actions (delete/archive) require an explicit confirmation step before the API call fires — no existing precedent for a confirm-free destructive bulk action in this codebase.
- Partial failures must be surfaced per-row (not a single opaque "some failed" toast) — read succeeded/failed arrays from the response and reflect the failed subset back to the user with per-item reasons.
```

**Reusable fragment — Non-Functional Rules section:**
```
- Any new toolbar background/border/badge token must ship as an explicit light+dark Tailwind pair (BLG-FE-87/88/95 precedent).
- Batch endpoint calls must be capped (recommend 100 IDs/call) — do not fire one API call per selected row from the client.
```

**Reusable fragment — Expected Outcome section:**
```
Selecting 1+ rows reveals a bulk-action toolbar with an accurate selected-count; bulk tag/archive/remove actions succeed or partially-fail with per-row feedback; destructive actions require confirmation; toolbar disappears at zero-selected; both light and dark theme render correctly.
```

## 9. Known Deviations

None. This is a net-new readiness/confirmation artefact; no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-16 | 1.0 | Initial readiness pass (ST-06, EPIC-04, v7.3) — §13 pre-check PASS |
