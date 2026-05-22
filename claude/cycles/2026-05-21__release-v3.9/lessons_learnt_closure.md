Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-22
Cycle: 2026-05-21__release-v3.9

---

# Lessons Learnt Closure — v3.9

**Phase:** Post-Ship Closure
**Cycle:** 2026-05-21__release-v3.9
**Generated:** 2026-05-22
**Records reviewed:** lessons_learnt.md (Release Planning), lessons_learnt_cycle.md (Phase 3 + Phase 4)

---

## Closure Observations

1. **Document closure was clean:** All required artefacts located without difficulty. changelog.md, roadmap, backlog, scope, decisions, velocity_metrics all updated in a single pass. No stale or missing documents encountered.

2. **Deviation compliance: N/A** — Zero deviations filed this cycle. STEP 5 is not applicable. The process notation for ST-01 AC-04 (BLG-QA-24) is already correctly filed in the backlog.

3. **Stale parked item surfaced:** BLG-FEAT-25 (PT-04 Setup Quality Score) has been deferred_at_planning for 4 consecutive cycles (v3.6, v3.7, v3.8, v3.9). STALE note added to backlog.md; outstanding action recorded in closure_record.md §6.

4. **Endpoint coverage drift: 1 new endpoint** — GET /portfolio/red-flag-journal (v3.9 ST-07) not yet in api_performance_baseline.md. BLG-OPS-13 scope updated (22→23 endpoints). Advisory raised.

5. **Specs Index gap resolved:** `portfolio_endpoints.md` was not registered in §3.4 API contracts list. Added with current version (v2.3).

6. **Lessons learnt action application rate: 0 immediate, 2 deferred.** Both deferred items are owned by Head of Specs Team and target v3.10. Pattern from prior cycles (createPageUrl, QA pre-merge) confirms the governance patch mechanism works — 5 carry-forward items from v3.8 all resolved in v3.9.

---

## Lessons Learnt Action Summary

### Records reviewed

| Record | Location | Action items found |
|--------|----------|--------------------|
| Release Planning | claude/cycles/2026-05-21__release-v3.9/lessons_learnt.md | 0 — no actions, observations only |
| Sprint Execution (Phase 3) | claude/cycles/2026-05-21__release-v3.9/lessons_learnt_cycle.md §Phase 3 | 2 deferred, 1 positive (E-type, no change) |
| Delivery Verification (Phase 4) | claude/cycles/2026-05-21__release-v3.9/lessons_learnt_cycle.md §Phase 4 | 1 deferred (aligned to Phase 3), 2 positive (E-type, no change) |

### Immediate actions applied: 0

No immediate actions required. All E-type (positive pattern confirmations) require no process changes.

### Deferred to v3.10: 2

| # | Item | Owner | Target |
|---|------|-------|--------|
| 1 | **merge_gate stale state on resume** — epics_merged remained [] after out-of-band GitHub UI merges between engine sessions; STEP 5.0A required correction. Recommendation: document expected re-invocation after each EPIC merge more prominently in STEP 4 output block. | Head of Specs Team | v3.10 |
| 2 | **Staging-only AC designation at sprint planning** — ST-01 AC-04 ("no >5% OHLCV failures under normal YF conditions") was an environment-dependent AC that required staging-only evidence designation. Recommendation: when writing ACs for network-dependent stories, flag staging-only ACs in sprint_backlog.md at planning time to reduce surprise P3 notations at execution. | Head of Specs Team | v3.10 |

### Decision required: 0

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | merge_gate.epics_merged is not updated during out-of-band GitHub merges between engine sessions, requiring correction at STEP 5.0A each time | Sprint Planning should note in the sprint capacity document that re-invoking the execution engine after each EPIC merge keeps merge_gate current; STEP 4 merge gate output block should flag this expectation | Sprint Planning |
| 2 | Environment-dependent ACs (live API integrations that cannot be unit-tested in CI) should be designated staging-only evidence at sprint planning, not discovered retrospectively at execution QA sign-off | Release Planning / Sprint Planning should flag ACs that reference live external service behaviour (Yahoo Finance, Alpaca) and prompt for staging-only evidence designation before sprint_backlog.md is sealed | Release Planning |
