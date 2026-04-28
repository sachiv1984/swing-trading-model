Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-04-28
Cycle: 2026-04-25__release-v3.0

---

# Lessons Learnt Closure — 2026-04-25__release-v3.0

Produced by: post_ship_closure.md STEP 8.5 (via lessons_learnt_prompt.md §3.5)
Filed: 2026-04-28
Reviewed by: PMO Lead

---

## Records Reviewed

| Record | File | Phase | Friction Items | Action Items |
|--------|------|-------|----------------|--------------|
| Release Planning | claude/cycles/2026-04-25__release-v3.0/lessons_learnt.md | Release | 0 | 0 |
| Sprint Execution | claude/cycles/2026-04-25__release-v3.0/lessons_learnt.md (§Phase 3) | Phase 3 | 4 | 1 deferred |
| Delivery Verification | claude/cycles/2026-04-25__release-v3.0/lessons_learnt_cycle.md | Phase 4 | 2 | 2 deferred |

**Total friction items reviewed:** 6 (4 Phase 3 + 2 Phase 4)

---

## Consolidated Action Summary

### Immediate Actions Applied: 0

No action items were classified as `immediate` — no template, prompt, or process document changes could be made unambiguously this session. All action items deferred to v3.1.

### Deferred to Next Cycle: 3

| # | Item | Owner | Target | Source |
|---|------|-------|--------|--------|
| D-01 | execution_prompt.md §3.1.A — add reclassification backfill instruction: "If stories are reclassified from delegated_frontend to autonomous mid-sprint, the accepting engine must backfill test_scenarios in execution_state.json at the time of reclassification." Recurring administrative gap (v2.9 + v3.0) with identified root cause. | Head of Specs Team | v3.1 sprint | Phase 4, lessons_learnt_cycle.md |
| D-02 | execution_prompt.md STEP 8.5 — add explicit note: "Output target is `lessons_learnt_cycle.md` — do NOT append to `lessons_learnt.md` (Release Planning artefact). Create `lessons_learnt_cycle.md` if absent." Phase 3 content in v3.0 was written to `lessons_learnt.md` instead of the correct target. | Head of Specs Team | v3.1 sprint | Phase 4, lessons_learnt_cycle.md |
| D-03 | Playwright test authoring — consider `waitFor` (targeted element/state assertion) over `waitForLoadState('networkidle')` as the default pattern for pages with SDK calls. `networkidle` can hang on unmocked SDK endpoints; targeted `waitFor` is more reliable. Apply at next E2E spec authoring session. | QA & Testing Owner | Next E2E authoring | Phase 3, lessons_learnt.md §Phase 3 |

### Escalated for Decision: 0

No items require authority decision.

---

## Closure-Phase Observations

### Documents Updated This Run

| Document | Action | Status |
|----------|--------|--------|
| docs/product/changelog.md | v3.0 entry written (4 EPICs, 16 stories, DEV-01 resolved) | ✅ |
| claude/roadmap/current_roadmap.md | v3.0 marked ✅ Complete; version headers updated | ✅ |
| claude/backlog/backlog.md | 7 items marked COMPLETE; 3 provisional targets updated v3.0→v3.1 | ✅ |
| docs/product/scope/scope--*.md | Status → Superseded | ✅ |
| docs/product/decisions/*.md | Status → Superseded | ✅ |
| docs/System_status_report.md | v3.0 sprint section prepended | ✅ |
| claude/cycles/velocity_metrics.md | v3.0 row appended (16/16, 1.00) | ✅ |
| docs/specs/Specs_Index.md | TSG-v29-02 resolved; TSG-v30-01 added (not_applicable); new API contracts registered; health_endpoints.md version updated; DEV-01 resolved in screener_results.md | ✅ |

### Deviation Compliance

No new deviations filed this sprint. DEV-01 (P3, from v2.9) resolved in v3.0. ST-11 cross-EPIC process deviation documented in both qa_evidence files — no canonical spec impact.

### Endpoint Coverage Drift Advisory (STEP 6)

Advisory check deferred — live environment required for api_performance_baseline.md comparison. New endpoints introduced this cycle: GET /ticker-universe, POST /ticker-universe, DELETE /ticker-universe/{ticker}, GET /screener/results, POST /screener/run. These are not yet in api_performance_baseline.md. Raised as outstanding action OA-v30-01.

---

## Carry-Forward

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| CF-01 | D-01 (execution_prompt §3.1.A reclassification backfill): recurring gap across v2.9 and v3.0; root cause identified — must convert to sprint story in v3.1 EPIC-04 equivalent | If not addressed in v3.1, future mid-sprint reclassifications will continue to miss test_scenarios backfill; audit risk | Head of Specs Team / PMO Lead |
| CF-02 | D-02 (execution_prompt STEP 8.5 output target): Phase 3 lessons were filed to `lessons_learnt.md` (Release Planning file) — `lessons_learnt_cycle.md` gap creates confusion at closure; fix is low-effort | Continuity risk if Phase 4 reviewer cannot find Phase 3 lessons in expected file | Head of Specs Team |
| CF-03 | D-03 (Playwright waitFor pattern): `networkidle` caused CI flakiness in v3.0; the `waitFor` pattern is a known improvement; should be adopted at next E2E authoring session | Continued CI instability risk on pages with SDK calls | QA & Testing Owner |
