Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-09
Cycle: 2026-05-05__release-v3.2

---

# Lessons Learnt Closure — v3.2 Arc 2 Pre-Trade Research & Planning

---

## Sources Reviewed

| Source | Location | Sections read |
|--------|----------|---------------|
| Release Planning lessons | `claude/cycles/2026-05-05__release-v3.2/lessons_learnt.md` | All action items (R-01, R-02, R-03) |
| Sprint Execution + Verification lessons | `claude/cycles/2026-05-05__release-v3.2/lessons_learnt_cycle.md` | Phase 3 (5 friction items) + Phase 4 (4 friction items) |

---

## Consolidated Action Summary

### Immediate actions applied: 2

| # | Source | Friction item | Action applied | Document updated | Version |
|---|--------|--------------|----------------|-----------------|---------|
| LL-v3.2-P3-02 | Phase 3, friction 2 | Cross-EPIC selector regression: ST-11 test failed CI after EPIC-02 removed `#checklist_completed` element | Added §3.1.A step 13 Cross-spec selector check — when story modifies/removes/renames a DOM element, scan all Playwright specs for stale selectors and update in same commit | `execution_prompt.md` | v3.14→v3.15 |
| LL-v3.2-P4-01 | Phase 4, friction 1 | BLG-GOV-19 autonomous class misapplication on EPIC-01 (frontend-visible changes, criterion 3 not met) | Strengthened §3.2.A BLG-GOV-19 sign-off block template: explicit 4-criterion ✓/✗ checklist; Criterion 3 requires positive check of src/pages/ and src/components/ before claiming autonomous class | `execution_prompt.md` | v3.14→v3.15 |

### Action-now items with no action required: 4

| # | Source | Item | Disposition |
|---|--------|------|-------------|
| Phase 3, friction 3 | STEP 5.0A pr_status sync functioned correctly | Confirmed working — no process change needed |
| Phase 3, friction 4 | Autonomous reclassification path (ST-05/06 → autonomous) | Confirmed working pattern — no action required |
| Phase 3, friction 5 | All OA-02–05 governance carry-forward items delivered | Confirmed working pattern — no action required |
| Phase 4, friction 3 | Two-pass verification was correct outcome (gate functioning as designed) | No process change needed — friction caused by BLG-GOV-19 misapplication resolved by LL-v3.2-P4-01 |
| Phase 4, friction 4 | Same as above — gate functioned correctly | Confirmed — no additional action |

### Deferred to next cycle: 3

| # | Source | Item | Owner | Target |
|---|--------|------|-------|--------|
| LL-v3.2-P3-01 | Phase 3, friction 1 | Sealed-file integrity check at EPIC session start: STEP 0 check in execution_prompt should scan git diff for staged changes to sealed files (stage4_backlog_slice.md etc.) and halt if detected | Head of Specs Team | v3.3 |
| LL-v3.2-P4-02 | Phase 4, friction 2 | Playwright mock payload advisory: §14 test authoring standard to add note requiring mock payloads to match canonical API spec response shape (nested objects) | Head of Specs Team | v3.3 |
| LL-v3.2-RP-01 | Release Planning, R-01 | Backlog policy: any P3 item deferred 3+ consecutive cycles must enter next release scope or receive named re-deferral from Product Owner | PMO Lead | v3.3 planning |
| LL-v3.2-RP-02 | Release Planning, R-02 | OA completion before next cycle opens — PMO Lead to resolve owned OAs before post-ship closure of the following cycle | PMO Lead | Ongoing |
| LL-v3.2-RP-03 | Release Planning, R-03 | Design gate must explicitly consume "before sprint planning" backlog items — sprint_planning_prompt.md STEP -1 check for open "before sprint planning" items | Head of Specs Team | v3.3 (if frontend scope) |

### Escalated for decision: 0

None.

---

## Closure-Phase Observations

- TSG-v31-01 and TSG-v31-03 (v3.1 test coverage gaps) both resolved this cycle by ST-11 and ST-12 — test scenario registration carry-forward mechanism working correctly.
- TSG-v31-02 (research endpoint Playwright coverage) resolved by EPIC-01 delivering pre-trade-research.spec.js (SC-RES-01–13, 14/14 pass).
- TSG-v32-01 added to Specs Index §18 — BLG-QA-14 (entry checklist Playwright) target v3.3.
- Scope and decisions documents marked Superseded as expected.
- Endpoint coverage advisory: pre-existing 6-endpoint gap (58 openapi vs 52 baseline) covered by BLG-OPS-13. No new endpoints in v3.2.
- No deviation compliance corrections needed — zero spec deviations this sprint.

---

## Carry-Forward

| # | Item | Type | Target cycle | Owner |
|---|------|------|--------------|-------|
| CF-01 | LL-v3.2-P3-01: Sealed-file integrity STEP 0 check in execution_prompt | Governance hardening | v3.3 | Head of Specs Team |
| CF-02 | LL-v3.2-P4-02: Mock payload API shape advisory in §14 | Test authoring standard | v3.3 | Head of Specs Team |
| CF-03 | LL-v3.2-RP-01: Backlog policy — 3-cycle deferral rule | Process policy | v3.3 planning | PMO Lead |
