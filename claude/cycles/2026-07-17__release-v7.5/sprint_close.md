Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-20
Cycle: 2026-07-17__release-v7.5

# Sprint Close — 2026-07-17__release-v7.5

## Sprint Goal

Ship all four v7.5 UI feature expansions — global command palette, user-defined price alerts, bulk actions, and saved filters/calendar view — each fully wired to its now-locked design artefact and observable in the running app.

## Items Done

### EPIC-01 — Global Command Palette (PR #1016, merged)

| ST | Title | Commit SHA | Spec References |
|----|-------|-----------|-------------------|
| ST-01 | Wire global Cmd/Ctrl-K command palette (BLG-FE-115) | `6376db60` | `docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md`; `docs/specs/frontend/pages/navigation.md`; `docs/specs/blg_fe_115_pre_implementation_readiness_pass.md` |

### EPIC-02 — Custom Price Alerts (PR #1017, merged)

| ST | Title | Commit SHA | Spec References |
|----|-------|-----------|-------------------|
| ST-02 | Add user-created price-alert data model, UI, and delivery integration (BLG-FE-116) | `661d67f5` (original); `660d17b0` (post-EPIC-03 conflict resolution, run against EPIC-03's own merge, not EPIC-02's) | `docs/design/2026-07-17__release-v7.5/custom-price-alerts/ux_spec.md`; `docs/specs/frontend/pages/notifications.md`; `docs/specs/blg_fe_116_pre_implementation_readiness_pass.md`; `docs/specs/api_contracts/alerts_endpoints.md`; `docs/specs/data_model.md` |

### EPIC-03 — Bulk Actions Toolbar (PR #1018, merged)

| ST | Title | Commit SHA | Spec References |
|----|-------|-----------|-------------------|
| ST-03 | Add multi-select and bulk-action toolbar to Watchlist/TradePlans (BLG-FE-117) | `0181f330` (original); `660d17b0` (post-EPIC-02 conflict resolution) | `docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md`; `docs/specs/frontend/pages/watchlist.md`; `docs/specs/frontend/pages/trade_plan.md`; `docs/specs/api_contracts/watchlist_endpoints.md`; `docs/specs/api_contracts/trade_plan_endpoints.md`; `docs/specs/data_model.md` |

### EPIC-04 — Saved Filters & Calendar View (PR #1019, merged)

| ST | Title | Commit SHA | Spec References |
|----|-------|-----------|-------------------|
| ST-04 | Add named saved filter presets and a calendar view (BLG-FE-118) | `e0d7a933` (original); `c3c6b15a` (post-EPIC-02/EPIC-03 conflict resolution) | `docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md`; `docs/specs/frontend/pages/trade_history.md`; `docs/specs/api_contracts/saved_filters_endpoints.md`; `docs/specs/api_contracts/reports_endpoints.md`; `docs/specs/data_model.md` |

All four stories were reclassified `delegated_frontend` → `autonomous` at STEP 0 per LL-v2.3-CL-01 (frontend delivery model default is engine-autonomous) — the engine fully implemented backend and frontend for all four.

## Items Returned to Backlog

None — all four EPICs were delivered within the sprint.

## Items Delegated and Outstanding

None — all four stories completed autonomously; no delegation records were created (`delegated_items: []`).

## QA Evidence Logs Produced

- `claude/cycles/2026-07-17__release-v7.5/qa_evidence_EPIC-01.md` — Director of Quality sign-off, dated 2026-07-17
- `claude/cycles/2026-07-17__release-v7.5/qa_evidence_EPIC-02.md` — Director of Quality sign-off, dated 2026-07-20
- `claude/cycles/2026-07-17__release-v7.5/qa_evidence_EPIC-03.md` — Director of Quality sign-off, dated 2026-07-20
- `claude/cycles/2026-07-17__release-v7.5/qa_evidence_EPIC-04.md` — Director of Quality sign-off, dated 2026-07-20

All four EPICs had frontend-visible changes, so `BLG-GOV-19` autonomous-class DoQ sign-off was unavailable (Criterion 3 unmet per `BLG-GOV-135`) in every case. Per explicit user direction, Claude acted as Director of Quality (per `claude/agents/director_of_quality.md`, Owner field confirmed matching) and independently re-verified each EPIC against its committed branch state — not a rubber-stamp: fresh checkout from the actual merge commit, full regression re-run, `git diff main..HEAD --stat` scope review, and a spot-check of at least one specific implementation detail against the spec text, for all four EPICs. Claude also acted as Product Owner (per `claude/agents/product_owner.md`) to review and comment acceptance on all four PRs. Per explicit user instruction ("I will merge myself"), the engine did not merge any PR — the user performed all four merges.

## Process Notes

- EPIC-01 merged first (2026-07-17) with no cross-EPIC conflict, since it was the only EPIC merged before the other three branches diverged further.
- EPIC-02, EPIC-03, and EPIC-04 were implemented, tested, and pushed while all three sat in parallel awaiting Director of Quality sign-off (an always-human gate) — the engine continued to the next EPIC rather than stalling the sprint on one item, per `execution_prompt.md` §1 Purpose ("do not block the entire sprint on one item").
- Merge order was EPIC-02 (PR #1017, merged 2026-07-20T10:42:26Z), then EPIC-03 (PR #1018, merged 2026-07-20T11:13:11Z), then EPIC-04 (PR #1019, merged 2026-07-20T11:42:51Z). Each of EPIC-03 and EPIC-04 hit the anticipated cross-EPIC conflict against the already-merged EPIC(s) ahead of it, resolved per CLAUDE.md §8 Cross-EPIC Merge Conflict Resolution:
  - **EPIC-03 vs main (EPIC-02 already merged):** conflicts in `backend/routers/test.py`, `src/pages/SystemStatus.js`, `tests/e2e/system-status.spec.js` (union of endpoint registrations, 98 total), `docs/specs/data_model.md` (EPIC-03's watchlist-tags migration renumbered v2.13→v2.14 to sit after EPIC-02's canonical v2.12→v2.13), `docs/ops/api_performance_baseline.md` (§26 price-alerts kept as EPIC-02 authored it, §27 bulk-actions-toolbar placed after it), and `execution_state.json` (union of `completed_items`, chronological `process_notes` merge). Resolution commit `660d17b0`, verified `mergeable: MERGEABLE` and full CI green before the user merged.
  - **EPIC-04 vs main (EPIC-02 + EPIC-03 already merged):** same files plus `docs/reference/openapi.yaml` (union of schema additions — `SavedFilter`/`CreateSavedFilterRequest` alongside `BulkTagRequest`/`BulkIdsRequest`/`BulkActionResult`; version bumped 3.11.0→3.12.0 to reflect EPIC-04's new paths), endpoint count reaching 102 total, EPIC-04's independently-authored `api_performance_baseline.md` §26 renumbered to §28 (after EPIC-02's §26 and EPIC-03's §27), and its `data_model.md` saved_filters migration renumbered v2.14→v2.15. Resolution commit `c3c6b15a`, verified `mergeable: MERGEABLE` and full CI green before the user merged.
- A real regression was caught and fixed during EPIC-04's own independent verification pass (not a merge-conflict artefact): the pre-existing `tests/e2e/net-r-trade-history.spec.js` crashed because its generic catch-all mock returns `{data:{}}` (object, not array) for unmocked endpoints, and the newly-mounted `SavedFiltersControl`/`CalendarView` called `.map()` on that non-array data. Fixed with `Array.isArray(json.data)` guards at both call sites; full e2e suite re-confirmed clean after the fix. See `qa_evidence_EPIC-04.md` and `execution_state.json` ST-04 notes.
- No orphaned post-merge commits found on any of the four EPIC branches (`git log origin/main..origin/exec/.../EPIC-xx` empty for all four) — no reconciliation required per LL-v6.8-P3-01.
- Post-merge `execution_state.json` sync (this session): `merge_gate.epics_merged` set to all four EPICs, `merge_gate.all_merged: true`, EPIC-04's epic-level `status`/`pr_status` updated to `merged` (was `done`/`open`, stale from before the user's final merge confirmation). Committed to `main` as `[GOVERNANCE] EPIC-04 merged — all epics_merged, merge_gate.all_merged=true` (commit `deebe623`) before proceeding to this sprint close.

## Deviations Filed This Sprint

None — all four EPICs' deviation checks confirmed implementation intent matched spec throughout. A small number of implementation notes were recorded (not filed spec deviations, per `LL-v3.4-P3-03`, since intent matched spec): EPIC-01's query-param vs path-param TradePlan detail route; EPIC-02 had none; EPIC-03's watchlist Bulk Tag column design and fixed bulk-archive abandonment reason; EPIC-04's `react-day-picker` v10 API usage and no-op `onDayClick` workaround. Full detail in each EPIC's `qa_evidence_EPIC-xx.md` and `execution_state.json` notes.

## Open Escalations

None.

## Net Outcome vs Sprint Goal

All four v7.5 UI feature expansions shipped in full, matching the sprint goal exactly: the global Cmd/Ctrl-K command palette, user-defined custom price alerts (data model, UI, and delivery integration), the bulk actions toolbar on Watchlist and Trade Plans, and named saved filter presets with a calendar view on Trade History. Each is fully wired to its locked design artefact and observable in the running app. No scope was deferred; no items were returned to backlog.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
