Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-17

# QA Evidence — EPIC-03 (v7.5)

## Consolidation Block

**EPIC:** EPIC-03 — Bulk actions on list/table views
**Cycle:** 2026-07-17__release-v7.5
**Sprint goal:** Ship all four v7.5 UI feature expansions — global command palette, user-defined price alerts, bulk actions, and saved filters/calendar view — each fully wired to its now-locked design artefact and observable in the running app.
**Test scenarios used:** tests/e2e/bulk-actions-toolbar.spec.js (SC-BAT-01 through SC-BAT-12); tests/test_bulk_actions.py (19 unit test scenarios)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-03 | docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md; docs/specs/frontend/pages/watchlist.md v0.4 §Bulk Actions; docs/specs/frontend/pages/trade_plan.md v0.7 §11; docs/specs/blg_fe_117_pre_implementation_readiness_pass.md; docs/specs/api_contracts/watchlist_endpoints.md v1.1; docs/specs/api_contracts/trade_plan_endpoints.md v0.7 | Shared `BulkActionToolbar.js` component (checkbox selection, inline Bulk Tag expand, destructive-action confirmation, partial-failure toast with expandable per-row detail); row checkboxes + header select-all on Watchlist and Trade Plans; 6 new batch-mutation endpoints (`GET/POST /watchlist/tags`, `/bulk-tag`, `DELETE /watchlist/bulk`, `POST /trade-plans/bulk-tag`, `PUT /trade-plans/bulk-archive`, `DELETE /trade-plans/bulk`) | AC: Rows in Watchlist and TradePlans tables are multi-selectable | Pass | None |
| ST-03 | (same as above) | (same as above) | AC: A bulk-action toolbar appears once one or more rows are selected | Pass | None |
| ST-03 | (same as above) | (same as above) | AC: Bulk tag/archive/remove operations apply to all selected rows in a single action | Pass | None (2 implementation notes below — intent matches spec) |

**QA test coverage:**
- Scenarios run: `tests/e2e/bulk-actions-toolbar.spec.js` — SC-BAT-01 (checkboxes present), SC-BAT-02 (toolbar absent at zero-selected, appears at 1+), SC-BAT-03 (Clear deselects all), SC-BAT-04 (select-all header checkbox), SC-BAT-05 (Watchlist Bulk Tag — correct POST body, success toast, selection cleared), SC-BAT-06/07 (Watchlist Bulk Remove — confirmation required, Cancel retains selection), SC-BAT-08 (Trade Plans toolbar shows Bulk Tag/Archive/Delete), SC-BAT-09 (active-plan excluded-count note), SC-BAT-10 (Trade Plans Bulk Delete — correct ids), SC-BAT-11 (Trade Plans Bulk Tag — correct ids/tags), SC-BAT-12 (partial-failure toast + expandable per-row detail, failed row remains selected). All 12 run live against `npm start` (real dev server, `page.route()` API interception) — 12/12 pass.
- `tests/test_bulk_actions.py` — 19 unit scenarios covering `watchlist_service.bulk_tag_watchlist` (merge-not-replace, not-found handling, invalid-tag filtering, empty/over-cap rejection), `bulk_delete_watchlist` (partial-failure shape), `get_all_watchlist_tags`, and `database.bulk_tag_trade_plans`/`bulk_archive_trade_plans` (active-status exclusion, mixed-batch partial result, not-found handling)/`bulk_delete_trade_plans`. All mocked — no live DB calls.
- Regression areas checked: `tests/e2e/trade-plan.spec.js` (52/52 pass incl. SC-TP-07a/07b which specifically assert Positions/Watchlist still render after route changes), `tests/e2e/system-status.spec.js` (19/19 pass, incl. updated SC-SS-01b fallback-count assertion for the new 95-endpoint total), `tests/e2e/smoke-critical-paths.spec.js` (3/3 pass). Backend: full `pytest` suite 692 passed, 2 skipped (pre-existing), 0 failed.
- Known deviations filed: None. Two implementation notes (not filed deviations, per LL-v3.4-P3-03 intent-match — spec silence/ambiguity resolved at implementation time, not a divergence from an explicit requirement):
  1. **Watchlist Bulk Tag endpoint mapping.** `ux_spec.md` §2.4 and `watchlist.md` §Bulk Tag state the submit call as "reusing the position-tag endpoint" (`POST /positions/bulk-tag` per the readiness pass AC-01 mapping). On implementation, this doesn't fit: `watchlist` entries are explicitly pre-position (per `watchlist_service.py`'s own module docstring, "pre-position ticker monitoring list") and the `watchlist` table has no tags column or relationship to `positions` at all — the readiness pass's endpoint list also only proposed 3 endpoints total (`positions/bulk-tag`, `trade-plans/bulk`, `watchlist/bulk`), omitting a watchlist-tag endpoint entirely. Built instead: a new `tags TEXT[]` column on `watchlist` (data_model.md v2.12→v2.13) and a dedicated `POST /watchlist/bulk-tag` endpoint, following the exact same per-entity pattern the readiness pass established for the other two entities. Intent (bulk-tag capability on Watchlist, per the locked AC) matches fully; only the specific endpoint/table named in the readiness pass prose was inapplicable.
  2. **Bulk Archive reason field.** `ux_spec.md` §2.5's bulk confirmation dialog (`"{Delete/Archive} {N} selected trade plan(s)?"`) defines no reason-textarea field, unlike the single-item Abandon modal's required reason (§8.2, min 10 chars). Implemented `PUT /trade-plans/bulk-archive` to apply a fixed system reason string (`"Bulk archived via Trade Plans bulk-action toolbar"`) rather than collecting one per plan — consistent with the design's deliberately simpler bulk confirmation flow.

**Frontend testing gate (CLAUDE.md / LL-v3.1-EX-01):** All 3 ACs are observable UI behaviour (checkbox multi-select, toolbar appearance, bulk action execution) — sprint_backlog.md's ST-03 entry lists no staging-only ACs, and all are Playwright-covered in CI (`tests/e2e/bulk-actions-toolbar.spec.js`), satisfying the hard gate without a staging run.

**Autonomous class eligibility check (BLG-GOV-19):** Not applicable — this EPIC creates `src/components/shared/BulkActionToolbar.js` and modifies `src/pages/Watchlist.js`, `src/pages/TradePlans.js`, `src/components/watchlist/WatchlistRow.js`/`WatchlistTable.js`/`WatchlistNewsRow.js` (frontend-visible change under `src/components/**` and `src/pages/**`), so Criterion 3 is automatically unmet per the BLG-GOV-135 detection rule. Standard Sign-Off Block below applies; Playwright coverage evidence is recorded above per the fail-path instruction.

**Dependency note:** `src/components/ui/checkbox.js` (a pre-existing, previously-unwired scaffold component, same pattern as EPIC-01's `cmdk` gap) required `@radix-ui/react-checkbox` to be installed — added to `package.json`/`package-lock.json` in this commit (confirmed via `Module not found` compile error surfaced during live Playwright verification, then resolved).

**Endpoint dispatch fix (drive-by, required for this story's own test.py registration to pass):** `backend/routers/test.py`'s `test_all_endpoints()` internal HTTP dispatcher only handled GET/POST/DELETE, so the new `PUT /trade-plans/bulk-archive` entry (and 3 pre-existing PATCH/PUT entries: `PATCH /signals/{id}`, `PUT /trade-plans/{id}`, `PATCH /trades/{id}/costs`) always fell through to the `else: raise ValueError` branch and reported `status: "error"` whenever the suite actually ran. Added PUT/PATCH dispatch branches and switched DELETE to `client.request("DELETE", ..., json=...)` so bodies are forwarded (needed for the new bulk DELETE endpoints). This is a small, directly-adjacent correctness fix required for this story's own new entry to report `pass` rather than `error` — not scope creep.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — `Watchlist.js`/`TradePlans.js`/`BulkActionToolbar.js` use `apiFetch`/`API_BASE_URL` from `src/api/base44Client.js`, the same pattern as sibling pages in this domain.
- Signed off by: Director of Quality
- Date: 2026-07-20
- Comments: Independent re-verification performed against the actual committed branch state (`exec/2026-07-17__release-v7.5/EPIC-03` @ `90290942`), not a rubber-stamp — fresh checkout (`git checkout` + `git pull`), full re-run from that exact commit: backend `pytest` 692 passed, 2 pre-existing skips, 0 failed; full e2e suite 591 passed, 3 pre-existing skips, 0 failed (15.6 min). Reviewed `git diff main..HEAD --stat` — 24 files changed, all within the documented scope (watchlist/trade-plans bulk endpoints, shared BulkActionToolbar.js, `@radix-ui/react-checkbox` dependency addition, contract/openapi/perf-baseline docs, tests) — no unrelated changes bundled in. Spot-checked the fixed bulk-archive abandonment reason string in the committed `trade_plans.py` against the documented value — matches verbatim. No P0/P1 defects found. Frontend testing gate satisfied — both observable ACs are Playwright-covered, no staging-only ACs for this story. Cleared for PR.
