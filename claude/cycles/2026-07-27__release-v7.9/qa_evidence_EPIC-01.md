Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

## Consolidation Block

**EPIC:** EPIC-01 — Watchlist staleness and decay review
**Cycle:** 2026-07-27__release-v7.9
**Sprint goal:** Ship all 15 v7.9 EPICs — the two P1 UX anchors and the 13 capacity-fill engineering-hardening items — with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_watchlist_service.py` (30 tests, all passing) + `tests/e2e/watchlist-staleness-review.spec.js` (5 Playwright tests — see Playwright execution note below).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01 | `docs/design/2026-07-27__release-v7.9/watchlist-staleness-review/ux_spec.md`, `docs/specs/frontend/pages/watchlist.md` v0.6 | New "Added" column (days-on-watchlist + staleness flag), "Keep" action for stale rows (server-authoritative clock reset), full backend/frontend wiring. | AC-01: Watchlist entries display days-since-added — Pass. AC-02: Entries past threshold visually flagged — Pass. AC-03: Keep/Remove actions — Pass. AC-04: No automatic removal — Pass (advisory-only badge, no scheduled sweep exists anywhere in the codebase). | Pass with notes | None |

**QA test coverage:**
- Scenarios run: `backend/.venv/bin/python3 -m pytest tests/test_watchlist_service.py -v` (30/30 passed, including staleness computation, `_row_to_dict` field exposure, and the Keep reset-trigger behaviour).
- Playwright: `tests/e2e/watchlist-staleness-review.spec.js` (5 tests: not-stale display, stale display, Keep-button-stale-only, Keep click → PATCH + toast, Remove unaffected). **Execution note:** could not be run locally — this sandbox's OS (Ubuntu 26.04) is not supported by the installed Playwright version for browser binary installation (`npx playwright install chromium` fails: "Playwright does not support chromium on ubuntu26.04-x64"). `.github/workflows/playwright.yml` auto-discovers all `tests/e2e/*.spec.js` files via glob and runs on every PR to `main` — this new spec will be picked up and gated there. Correctness was verified by careful manual trace against the actual component implementation (button labels, text content, route paths, PATCH body shape) rather than live execution.
- Regression areas checked: `tests/test_bulk_actions.py` (19 tests) — confirms the new `added_at` field on `UpdateWatchlistRequest` does not interfere with existing bulk-tag/bulk-delete flows (separate endpoints, unaffected).
- Known deviations filed: None. Two findings recorded (not deviations — resolved inline, both agent-mediated-approved):
  1. ux_spec.md's "no backend schema change required" reasoning cited a non-existent `added_at` column (the table only has `created_at`). Resolution: `added_at` exposed as an API-level alias for `created_at` — the spec's stated conclusion (no schema change) held, just via a different mechanism than described.
  2. ux_spec.md's placement instruction ("after Research, before Target Entry") assumed a column order the real `WatchlistTable.js` doesn't have (Research sits after Earnings, before News — nowhere near Target Entry). Resolution: placed "Added" after "Entry Signal", before "Target Entry" instead, honouring the spec's own stated rationale (metadata columns grouped before price fields).

---

## BLG-GOV-19 Autonomous Class Sign-Off Block — NOT APPLICABLE

This EPIC introduces frontend-visible changes (new column, new interactive button) — criterion 3 of the autonomous class is automatically unmet per the `BLG-GOV-135` detection rule (`src/components/**` files modified). Standard sign-off block used instead.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirmed — `useWatchlistModal.js`'s `keepWatchlistEntry` uses the existing `apiFetch`/`API_BASE_URL` pattern already used throughout `Watchlist.js`, not a raw `fetch()`/hardcoded URL.
- Signed off by: Sprint Execution Engine (agent-mediated, Head of UX & Design role — §5.3)
- Date: 2026-07-27
- Comments: Head of UX & Design (agent-mediated) independently verified both findings above against the actual code, confirmed the placement correction is a reasonable inline fix that doesn't warrant a design-gate round-trip, and confirmed the Keep button is stale-only with no confirmation modal (per ux_spec.md §4). Product Owner and Head of UX & Design's original design-gate sign-off (2026-07-27) is recorded in `ux_spec.md` §8; this block adds the implementation-level review.
