**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v2.7
**Cycle:** 2026-04-13__release-v2.7
**Last Updated:** 2026-04-16

---

# Lessons Learnt — Post-Ship Closure — v2.7

## Cross-Cycle Recurrence Check

**Prior cycle closure file:** `claude/cycles/2026-04-11__release-v2.6/lessons_learnt_closure.md` — **not found**. v2.6 post-ship closure was not run as a standalone cycle (v2.6 was closed retroactively at v2.7 post-ship). Recurrence check against prior closure: not possible.

---

## Closure-Phase Observations

| # | Observation | Classification |
|---|-------------|----------------|
| 1 | **Scope document not pre-created.** `docs/product/scope/scope--2026-04-13__release-v2.7-*.md` was referenced in `.claude_current_state.json` but did not exist at closure start. Created at STEP 4 with correct scope items and Superseded status. | Process gap — advisory |
| 2 | **Two backlog items (BLG-GOV-18, BLG-GOV-19) not formally added to backlog.md at sprint planning time.** They were referenced in the backlog slice as `Backlog item:` but were never entered into `backlog.md`. Added at STEP 3 in completed state. | Process gap — advisory |
| 3 | **v2.6 lacked standalone post-ship closure.** Two v2.6 items (scope doc, changelog entry) were retroactively completed at v2.7 closure. Roadmap RA:v2.6 annotation also retired at v2.7. This adds friction at the next cycle closure. | Process gap — recurring risk |
| 4 | **New canonical specs registered in Specs_Index.md.** `analytics_endpoints.md v2.1.0`, `signal_endpoints.md v1.1`, and `spec_dependency_map.md v1.0` were not registered in the Specs_Index at delivery time. Registered at STEP 7. | Deferred registration — advisory |
| 5 | **Immediate action applied: Playwright patterns documentation.** `docs/team_skills/quality/playwright_patterns.md` v1.0 created from Phase 3, Obs 4 (LIFO route ordering fix pattern codified). | Immediate action applied |

---

## Lessons Learnt Action Summary

### Records Reviewed

| Record | Location | Observations reviewed |
|--------|----------|-----------------------|
| Release Planning lessons | `claude/cycles/2026-04-13__release-v2.7/lessons_learnt.md` | 4 planning observations |
| Sprint Execution lessons | `claude/cycles/2026-04-13__release-v2.7/lessons_learnt_cycle.md` — Phase 3 | 4 observations + 2 carry-forwards |
| Delivery Verification lessons | `claude/cycles/2026-04-13__release-v2.7/lessons_learnt_cycle.md` — Phase 4 | 4 observations |

### Immediate Actions Applied: 1

| # | Action | Document updated | Version |
|---|--------|-----------------|---------|
| 1 | Playwright LIFO route ordering fix pattern documented | `docs/team_skills/quality/playwright_patterns.md` | v1.0 (created) |

### Deferred to Next Cycle: 3

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | Add DoQ sign-off block formal `Date:` field reminder to `execution_prompt.md §3.2.A` | Director of Quality + Head of Specs Team | v2.8 |
| 2 | Clarify deviation register terminology in sprint_close.md template: "Deviations filed" = spec deviations only; process notations → execution_state.json notes column | PMO Lead + Head of Specs Team | v2.8 |
| 3 | BLG-GOV-08 (engine prompt compression) — PO decision needed at v2.8 planning after 4 consecutive deferrals (v2.4–v2.7): promote to sprint story or retire from backlog | Product Owner + Head of Specs Team | v2.8 planning |

### Escalated for Decision: 0

None.

---

## Carry-Forward

| # | Item | Source | Owner | Target cycle |
|---|------|--------|-------|--------------|
| 1 | DoQ sign-off block formal `Date:` field — add reminder to `execution_prompt.md §3.2.A` | Phase 3, Obs 2 / Phase 4, Obs 1 | Director of Quality | v2.8 |
| 2 | Deviation register terminology clarification in sprint_close.md template | Phase 4, Obs 3 | PMO Lead | v2.8 |
| 3 | BLG-GOV-08 engine prompt compression — PO promotion/retire decision | Planning Obs 2 | Product Owner | v2.8 planning |
| 4 | AC-6 (ST-08): Market Correlation frontend rendering — raise formal backlog item for v2.8 | Phase 3 carry-forward | Head of Engineering | v2.8 |
| 5 | BLG-QA-13: Author scenario coverage for market correlation (SC-CORR-01–04) and supplementary indicators (SC-SIG-IND-01–02) | TSG-v27-01 | QA & Testing Owner | v2.8 |
| 6 | Ensure scope document is created at release planning time (not deferred to post-ship) — add note to release_planning_prompt.md §5 Artefacts checklist | Closure Obs 1 | Head of Specs Team | v2.8 |
| 7 | Sprint planning should formally add BLG-GOV-18/19-style new governance items to backlog.md at the time the backlog slice is created | Closure Obs 2 | PMO Lead | v2.8 |
