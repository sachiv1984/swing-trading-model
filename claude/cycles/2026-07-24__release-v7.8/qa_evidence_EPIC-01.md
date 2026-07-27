Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-26

# QA Evidence — EPIC-01 (v7.8)

**EPIC:** EPIC-01 — In-app "what's new" panel for most recent release
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_changelog_service.py`, `tests/e2e/whats-new-panel.spec.js` (new, SC-WN-01..05)

## ST-01 — Build in-app "what's new" panel sourced from changelog.md

**Spec reference:** `docs/specs/frontend/pages/dashboard.md#6A`, `docs/specs/api_contracts/changelog_endpoints.md`, `docs/specs/frontend/design_system.md`
**Commit:** `6d989028` (implementation `4a20acaa`)

**What was built:** `GET /changelog/latest` (new endpoint) parses `docs/product/changelog.md`'s most recent version block server-side on every request and returns `{version, changes}` — no hardcoded frontend copy, satisfying "updates automatically on the next release without manual wiring." `WhatsNewCard.js` (new component) renders this via the standard `DataState` pattern, placed below `GateProgressStrip` in `DashboardHome.js` per dashboard.md §6A's precise placement instruction. Truncates to 8 bullets client-side with a non-interactive "+N more" trailer per spec. `DataState.js` extended with optional `errorHeading`/`errorBody` props (backward compatible) to support the spec's custom "Unable to load release notes" copy.

**Same-commit CLAUDE.md §2 compliance:** `docs/specs/api_contracts/changelog_endpoints.md` (new, `## GET /changelog/latest` at correct depth), `docs/reference/openapi.yaml` (new `Changelog` tag + path, 3.13.0→3.14.0), `docs/specs/api_contracts/api_changelog.md` (new top entry), `backend/routers/test.py` (new test_cases entry, AST-verified 99→100), `src/pages/SystemStatus.js` fallback count (99→100) + `tests/e2e/system-status.spec.js` `SC-SS-01b` updated in the same commit. `docs/ops/api_performance_baseline.md` §30 registration added with agent-mediated Infrastructure & Operations Owner sign-off (§5.3) — **first review round returned Blocked**: the reviewer independently checked the document's own version-tracking convention and found the header (`**Version:**`) and §9 Document History table had not been bumped/appended, unlike every prior §26–§29 addition. Corrected (header → 2.18, new History row added) and re-reviewed to **Approved**.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `dashboard.md#6A` | `WhatsNewCard.js` + `GET /changelog/latest` | Panel shows most recent release's `### Changes shipped` entries | Pass | None |
| ST-01 | (same) | Server-side parse on every request, no hardcoded copy | Panel updates automatically on next release, no manual wiring | Pass | None |
| ST-01 | (same) | `DataState` loading/error/empty branches wired | Empty/loading states follow existing `DataState` pattern | Pass | None |

**QA test coverage:**
- Backend: `tests/test_changelog_service.py` — 5 tests (most-recent-version extraction, missing file, no version headings, no changes-shipped table, live integration check against the real `docs/product/changelog.md`). All pass.
- Frontend: `tests/e2e/whats-new-panel.spec.js` — 5 scenarios: SC-WN-01 (ready state, version header + ordered bullets), SC-WN-02 (11 changes → 8 bullets + "+3 more"), SC-WN-03 (empty state), SC-WN-04 (error state, custom heading), SC-WN-05 (loading spinner). **Actually executed locally (2026-07-27)** against a real Chromium (system `snap` browser via a local, uncommitted `executablePath` override — this sandbox's bundled-Playwright-browser download is unsupported on its OS, but a real browser could still be driven once pointed at one). **First run found a real bug**: `WhatsNewCard.js` read `data?.data`, but `api.changelog.latest()` → `doFetch()` already unwraps the `{status, data}` envelope, so the second `.data` access always resolved to `undefined` — the card would have always rendered the empty state ("Nothing to show") in production regardless of actual data. 3 of 5 scenarios failed (SC-WN-01/02/05) before the fix. Fixed (commit `453e1d23`, one-line change: `data?.data` → `data`) and re-run — all 5 pass. Grepped all other new frontend files this sprint (EPIC-05, EPIC-06) for the same `data?.data` pattern — none found; isolated to this component. Will still run in real CI (`playwright.yml`) at PR open for final confirmation.
- Regression: full backend suite (759 tests) — all pass, no behavioural change to any existing endpoint or component (confirmed `DataState`'s new props default to the original strings, verified by reading every other call site — none pass `errorHeading`/`errorBody`, so behaviour is unchanged there).
- Known deviations filed: None.

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-01 is the only story, classified `autonomous`.
- Criterion 3 (no frontend-visible change): **✗ — FAILS.** This EPIC creates `src/components/dashboard/home/WhatsNewCard.js` and modifies `src/components/ui/DataState.js`, `src/pages/DashboardHome.js` (all under `src/components/**`/`src/pages/**`), which per the BLG-GOV-135 detection rule automatically disqualifies the autonomous sign-off class regardless of Playwright coverage.

**Autonomous class does not apply.** Standard sign-off (Director of Quality, human) is required below.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [ ] Signed off by: Director of Quality
- Date: **[AWAITING SIGN-OFF]**
- Comments: Playwright tests (SC-WN-01..05) actually executed locally against a real browser on 2026-07-27 — all 5 pass (see QA test coverage above; this run also caught and led to fixing a real double-unwrap bug in `WhatsNewCard.js`). Still needs CI-green confirmation (`playwright.yml`) as final confirmation before/alongside sign-off. This EPIC creates/modifies frontend components, so BLG-GOV-19 autonomous sign-off does not apply — human Director of Quality review required per CLAUDE.md §2 frontend testing gate. Domain-authority note: `api_performance_baseline.md` §30's Infrastructure & Operations Owner sign-off (agent-mediated, §5.3) is recorded separately above per BLG-GOV-14 — confirmed cleared after one corrective round.
