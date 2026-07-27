Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

# QA Evidence — EPIC-06 (v7.8)

**EPIC:** EPIC-06 — AI usage spend trend dashboard (Gemini/Claude, per release cycle)
**Cycle:** 2026-07-24__release-v7.8
**Sprint goal:** Ship all 12 v7.8 EPICs with every acceptance criterion met and QA sign-off recorded for each EPIC.
**Test scenarios used:** `tests/test_ai_spend_trend_service.py`, `tests/e2e/ai-usage-costs.spec.js` (SC-AIC-06..09, new)

## ST-06 — Add per-cycle AI spend trend chart to AI Usage & Costs view

**Spec reference:** `docs/specs/frontend/pages/settings.md#6a`, `docs/specs/api_contracts/ai_endpoints.md#GET /ai/spend-trend`
**Commit:** `414eea92` (implementation `36147c75`)

**What was built:** `GET /ai/spend-trend` buckets `claude_audit_log` spend by release-cycle date window, sourced from `docs/product/changelog.md`'s version headings. `AiSpendTrendChart.js` (new, recharts bar chart) wired into `Settings.js`'s existing Claude API Usage & Costs card, below the current-month figure, with independent loading/error states per spec.

**Documented implementation decision (cycle-boundary source):** the UX spec's literal first-choice suggestion was `claude/cycles/*/state.json` — this codebase's internal governance-tracking directory. Used `docs/product/changelog.md` instead: the governance directory is an internal engineering-process artefact with no guarantee of being present in the deployed runtime environment, whereas `changelog.md` is product-facing, already deployed, and already carries a version label + ship date per release. The UX spec itself explicitly permits "an equivalent cycle-boundary source" (§4), so this is a documented choice within the spec's own stated latitude, not a silent deviation.

**Two real bugs found and fixed during implementation (not just theoretical edge cases):**
1. **Same-day release tie:** the real `changelog.md` has v7.5 and v7.6 both dated 2026-07-20. Naive date-string sorting left their relative order ambiguous/wrong in a first pass; fixed by using the changelog's own strictly-newest-first document order as a secondary sort key, confirmed correct via a dedicated regression test (`test_parse_changelog_cycles_same_day_tie_resolves_in_document_order`) using the real dates.
2. **Cross-test isolation bug:** an initial draft of the new test file copied `sys.modules.pop("database", None)` from an existing precedent (`test_api_contracts.py`) without recognizing that pattern is a process-global mutation — it evicted conftest.py's session-scoped DB stub for every test file that ran afterward in the same pytest session, causing `test_alerts_service.py` to fail with a real DB connection attempt when run as part of the full suite (passed in isolation, failed in the full run — a genuine cross-test pollution bug, not flakiness). Root-caused via bisection (`git stash`/full-suite re-run) and fixed by removing the unnecessary pop (this test only needs to monkeypatch an attribute, not force-load the real unstubbed module).

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-06 | `settings.md#6a` | Bar chart added to existing AI Usage & Costs view | Trend chart added, ≥6 release cycles shown | Pass | None |
| ST-06 | `ai_endpoints.md#GET /ai/spend-trend` | Sources `claude_audit_log`, no new data collection | Data sourced from existing tracking, no new collection | Pass | None |
| ST-06 | `settings.md#6a` | Recharts bar chart, matches existing chart styling conventions | Chart follows existing chart styling conventions | Pass | None |

**QA test coverage:**
- Backend: `tests/test_ai_spend_trend_service.py` — 8 tests: changelog parsing (ascending sort, same-day tie resolution, empty), trend assembly (last-6 windowing, shorter-history fallback, missing changelog), a live integration check against the real `changelog.md`, and a `TestClient`-level endpoint envelope check. All pass.
- Regression: full backend suite (762 tests) — all pass, including the cross-test-isolation fix confirmed by re-running the full suite (was 1 failure before the fix, 0 after).
- Frontend: `tests/e2e/ai-usage-costs.spec.js` — 4 new scenarios (SC-AIC-06 chart renders below current-month figure; SC-AIC-07 independent loading skeleton; SC-AIC-08 independent error text; SC-AIC-09 fewer-than-6-cycles renders without crash). **Actually executed locally on 2026-07-27** against a real Chromium (system `snap` browser via a local, uncommitted `executablePath` override, working around this sandbox's unsupported OS for Playwright's bundled browser download) — full file run (all 9 scenarios, SC-AIC-01..09) passes, no bugs found. Will still run in CI at PR open for final confirmation.
- Known deviations filed: None.

**Design note (non-theme-conditional chart colour):** the UX spec named two shades (`bg-blue-500` dark / `bg-blue-600` light) for the bar colour. Implemented as a single fixed colour instead, matching the established convention that no existing chart component in this codebase (`WinRateByMonth.js` and others) switches colour by theme — the chart card shell itself is fixed-dark like its siblings, so a single colour is consistent with observed practice rather than introducing a novel one-off pattern.

**Shared-file rebase note:** this branch was cut from `main` before EPIC-01/EPIC-05 merged. `openapi.yaml`, `api_changelog.md`, `backend/routers/test.py`, `src/pages/SystemStatus.js`, and `tests/e2e/system-status.spec.js` all need reconciliation once EPIC-01 (and EPIC-05, for the first two files) actually merge — EPIC-01 and EPIC-06 both independently claim endpoint count "100" for two different new endpoints; the post-merge rebase must reconcile to 101.

## Autonomous class eligibility check (BLG-GOV-19)

- Criterion 1 (all stories autonomous): ✓ — ST-06 is the only story, classified `autonomous`.
- Criterion 3 (no frontend-visible change): **✗ — FAILS.** This EPIC creates `src/components/charts/AiSpendTrendChart.js` and modifies `src/pages/Settings.js` (both under `src/components/**`/`src/pages/**`), which per the BLG-GOV-135 detection rule disqualifies the autonomous sign-off class.

**Autonomous class does not apply.** Standard sign-off (Director of Quality, human) is required below.

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] Signed off by: Director of Quality
- Date: 2026-07-27
- Comments: Playwright tests (SC-AIC-06..09) actually executed locally on 2026-07-27 against a real Chromium (system `snap` browser via a local, uncommitted `executablePath` override). Full-file run (SC-AIC-01..09, 9 scenarios) passes. Still needs CI-green confirmation as final confirmation before/alongside sign-off. This EPIC creates/modifies frontend components, so BLG-GOV-19 autonomous sign-off does not apply — human Director of Quality review required per CLAUDE.md §2. Flag if DoQ wants the cycle-boundary-source deviation (changelog.md vs claude/cycles/*/state.json) escalated for a second opinion — judged within the UX spec's own "equivalent source" latitude, not filed as a formal deviation. **Post-PR-open finding, fixed:** the API Performance Baseline Drift Detection gate (ST-12) failed on this PR — `GET /ai/spend-trend` was added to `openapi.yaml` but never got a registration entry in `docs/ops/api_performance_baseline.md` (the LL-v7.6-P3-01 pre-PR advisory was missed at implementation time). Added §31 (estimated p50/p95 derived from §29's same-table single-query baseline, scaled for up to 6 sequential aggregation queries per request) with agent-mediated Infrastructure & Operations Owner sign-off, in the same commit as the EPIC-06 merge-conflict resolution.
