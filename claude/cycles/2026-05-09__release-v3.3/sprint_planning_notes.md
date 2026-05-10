**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-10
**Cycle:** 2026-05-09__release-v3.3

---

# Sprint Planning Notes — 2026-05-09__release-v3.3

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-09__release-v3.3/stage4_backlog_slice.md`

No amendment file present (`amended_backlog_slice_path` = "" in state.json).

---

## Preflight Gate Results (STEP -1)

| Check | Result |
|-------|--------|
| -1.1 Global State | ✅ status=Published; no amended backlog slice |
| -1.2 Release Plan Sealed | ✅ Published, publish_eligible=true, open_escalations=[], deferred_execution_blockers=[] |
| -1.3 Design Gate | ✅ design_gate_status=Passed (2026-05-09T00:30:00Z) — entered from Design_Gate_Passed; no bypass audit required |
| -1.4 Backlog Slice Present | ✅ 4 EPICs, 17 ST items |
| -1.5 Required Files | ✅ All present (.claude_current_state.json, state.json, stage4_backlog_slice.md, backlog.md, release_plan.md (schema v2), cycle_summary.md, workforce_capacity.md) |
| -1.6 Authority Roles | ✅ Product Owner, Head of Specs Team, PMO Lead, Director of Quality, FinOps & Resource Architect all present in claude/agents/ |
| -1.7 Lessons Learnt Prompt | ✅ claude/system/lessons_learnt_prompt.md exists (v1.9) |
| -1.8 Write Test | ✅ Write permission confirmed; test file cleaned up |
| -1.9 pip-audit | ✅ Clean — no known vulnerabilities in backend/requirements.txt (69 packages scanned) |
| -1.10 Required Decisions | ✅ Both resolved (see below) |
| -1.11 Prompt Change Log | Advisory — see below |
| STEP 0 Branch Check | ✅ Current branch: main |

---

## Pre-Sprint Required Decisions — Resolution Record (STEP -1.10)

| Decision | Owner | Status | Resolution |
|----------|-------|--------|------------|
| [RISK-01] Position state machine back-fill strategy — confirm handling of open positions with no prior state | Head of Engineering | ✅ Resolved | ST-01 ACs specify: GRACE for positions opened within last 10 trading days; UNKNOWN otherwise. UNKNOWN is a valid display state handled gracefully in ST-03. Design gate notes confirm: "confirmed mitigated by UNKNOWN state handling specified in ST-01 ACs and ST-03 UX spec §6." |
| [RISK-05] Design gate pass — UX specs for IT-01/IT-02/IT-03 signed off by Head of UX & Design | Head of UX & Design + Product Owner | ✅ Resolved | Design gate PASSED 2026-05-09. UX specs produced for ST-03, ST-05, ST-07, ST-17. All 17 items cleared (4 Design Required, 1 Design Pre-Approved, 12 Design Not Applicable). |

---

## Carry-Forward Items from Prior Cycle (v3.2 — STEP 0)

5 carry-forward items from cycle 2026-05-05__release-v3.2 lessons_learnt_closure.md `## Deferred to next cycle`:

| Item | Source | Status in v3.3 |
|------|--------|----------------|
| LL-v3.2-P3-01 Sealed-file integrity check at EPIC session start | Phase 3, friction 1 | ✅ In scope: EPIC-04 ST-13 |
| LL-v3.2-P4-02 Playwright mock payload advisory | Phase 4, friction 2 | ✅ In scope: EPIC-04 ST-13 |
| LL-v3.2-RP-01 Backlog 3-cycle deferral policy | RP, R-01 | ✅ In scope: EPIC-04 ST-14 |
| LL-v3.2-RP-02 PMO Lead OA completion before cycle close | RP, R-02 | Ongoing monitoring — OA-04 |
| LL-v3.2-RP-03 Design gate "before sprint planning" check | RP, R-03 | ✅ In scope: EPIC-04 ST-14 |

Carry-forward items reviewed: 5 items from cycle 2026-05-05__release-v3.2.

---

## Pre-Sprint Vulnerability Scan (STEP -1.9)

**pip-audit result: clean**

No known vulnerabilities found. 69 packages scanned from `backend/requirements.txt`. Scan date: 2026-05-10.

---

## Prompt Change Log Hygiene Advisory (STEP -1.11)

The prompt change log was comprehensively updated on 2026-05-09 (modular prompt refactor + v3.2 post-ship patches). The last log entries for all Class 6 governed prompts are dated 2026-05-09 and the sprint_planning_prompt.md header (v2.7) matches the log. No divergence detected in the files checked.

⚠ Advisory: Governance files that will be modified in EPIC-04 ST-13 and ST-14 (execution_prompt.md, sprint_planning_prompt.md, backlog_management_prompt.md) must follow CLAUDE.md §6 checklist in the same commit — version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md PREPENDED row. This is noted as an EPIC-04 execution requirement, not a planning blocker.

---

## Capacity WARN Advisory (IMP-41)

⚠ WARN: Estimated cycle effort (~19.75d mid-point) is approximately equal to available capacity (~20d mid-point). Plan is feasible but tight with minimal margin.

The phasing recommendation adopted from the release plan allocates:
- Sprint 1: ~10.75d effort vs ~10d capacity mid-point (borderline — EPIC-03 spec stories are doc-heavy and may run lighter)
- Sprint 2: ~9d effort vs ~10d capacity mid-point (comfortable with margin)

Contingency: EPIC-04 ST-15 (XS, ~0.25d) can move to Sprint 2 without impacting sequencing if Sprint 1 is constrained.

**Product Owner must explicitly acknowledge this WARN before scope selection is confirmed.** Acknowledgement recorded at sign-off gate (sprint_backlog.md Product Owner Sign-Off section).

---

## Deferred Items

None — all 17 backlog slice items are included in sprint scope. No items require deferral due to capacity or unresolved blockers.

---

## Scope Classification

| Item | Sprint | Delegation Class | Notes |
|------|--------|-----------------|-------|
| ST-01 | 1 | autonomous | Backend data model + migration; no UX change |
| ST-02 | 1 | autonomous | Backend service; no UX change |
| ST-03 | 1 | delegated_frontend | New frontend controls (state badge); UX spec locked at v1.5 |
| ST-04 | 2 | autonomous | Backend endpoint; no UX change |
| ST-05 | 2 | delegated_frontend | New alert card on positions page; UX spec locked at v1.5 |
| ST-06 | 2 | autonomous | Backend endpoint; no UX change |
| ST-07 | 2 | delegated_frontend | New trail stop panel/modal; UX spec locked at v1.5 |
| ST-08 | 1 | autonomous | Spec authorship; no UX change |
| ST-09 | 1 | autonomous | Spec + UX spec authorship; no pre-gate artefact required |
| ST-10 | 1 | autonomous | QA documentation; no UX change |
| ST-11 | 1 | autonomous | Playwright E2E test authorship; test scenarios well-defined; no human mid-task decision required |
| ST-12 | 1 | autonomous | Integration tests + ops + governance docs; no UX change |
| ST-13 | 1 | autonomous | Governance prompt edits only; no UX change |
| ST-14 | 1 | autonomous | Governance prompt edits + policy doc; no UX change |
| ST-15 | 1 | autonomous | §13 compliance review document; no UX change |
| ST-16 | 2 | delegated_backend | New platform capability (feature flag infrastructure); backend infra + proof-of-concept wrapping of ST-03 badge; requires staging verification |
| ST-17 | 2 | delegated_frontend | Multiple frontend changes across trade_plan, watchlist, signals pages; UX spec locked |

---

## Test Scenario Gap Flags (LL-v2.0-P4-2)

Items classified `delegated_frontend` that introduce new user-facing controls require test_scenarios flag:

| Item | New Controls | Flag |
|------|-------------|------|
| ST-03 | Position state badge (5 states), `days_in_state` display, "Next state trigger" tooltip | EPIC-01 `test_scenarios` → pending — QA & Testing Owner to author before Sprint 2 |
| ST-05 | Grace period alert card on positions page | EPIC-02 `test_scenarios` → pending — QA & Testing Owner to author before Sprint 2 ends |
| ST-07 | Trail stop panel/modal with confirm/cancel | EPIC-02 `test_scenarios` → pending (same) |
| ST-17 | Abandonment action + modal; status badges (7 states); research indicator; signals date picker | EPIC-04 `test_scenarios` → pending — QA & Testing Owner to author before Sprint 2 closes |

Note: ST-11 creates Playwright E2E tests for existing entry checklist functionality (EPIC-02 domain, v3.2). These scenarios will populate EPIC-02's test_scenarios during ST-11 execution.

---

## Dependency Map

| Item | Depends On | Type | Notes |
|------|-----------|------|-------|
| ST-02 | ST-01 | Internal | Backend service requires data model fields |
| ST-03 | ST-02 | Internal | Frontend display requires backend service |
| ST-03 | ST-09 UX spec | Spec | Research view UX spec not required for ST-03; position lifecycle UX spec from design gate locked ✅ |
| ST-04 | EPIC-01 (all ST-01,02,03) | Cross-EPIC | Uses position_state infrastructure |
| ST-05 | ST-04 | Internal | Frontend requires backend endpoint |
| ST-05 | ST-09 | Spec | Research view canonical spec referenced for data field alignment (advisory) |
| ST-06 | EPIC-01 (all ST-01,02,03) | Cross-EPIC | Uses position_state and stop price join |
| ST-07 | ST-06 | Internal | Frontend requires backend endpoint |
| ST-09 | ST-08 | Internal | Canonical spec references provenance spec (ST-08) for source attribution |
| ST-10 | ST-09 | Internal | Test scenarios reference canonical spec field list |
| ST-12 | ST-08, ST-09 | Internal | Integration test for /research/{ticker}; latency baseline references spec |
| ST-16 | ST-03 | Internal | Proof-of-concept flag wraps ST-03's lifecycle badge; ST-03 must be complete first |
| ST-13 | None | — | Self-contained governance patch |
| ST-14 | None | — | Self-contained governance patch |
| ST-15 | None | — | Self-contained §13 review doc |
| ST-17 | None | — | Self-contained quick wins; no hard dep on Arc 3 items |

No circular dependencies detected.

---

## Execution Sequence

### Sprint 1 (10 stories — EPIC-01 + EPIC-03 + EPIC-04 ST-13/14/15)

Recommended execution order (can be parallelised where no dependency):

1. **ST-13** — execution_prompt governance patches (autonomous; unblocked; short; clears OA-01/02)
2. **ST-14** — sprint_planning + backlog governance patches (autonomous; unblocked; clears OA-03/05)
3. **ST-15** — PT-05 §13 compliance review (autonomous; unblocked; XS effort)
4. **ST-01** — Positions data model + migration (autonomous; unblocked; EPIC-01 start)
5. **ST-08** — PT-02 research API contract + provenance spec (autonomous; unblocked; EPIC-03 start; parallel with ST-01)
6. **ST-02** — Position lifecycle state machine backend (autonomous; after ST-01)
7. **ST-09** — Canonical research view spec + UX spec (autonomous; after ST-08)
8. **ST-10** — Research view test scenario library + protocol (autonomous; after ST-09)
9. **ST-11** — Entry checklist Playwright E2E tests (autonomous; unblocked; can run parallel to ST-09/10)
10. **ST-12** — Research integration tests + latency + security + governance (autonomous; after ST-08/09)
11. **ST-03** — Position lifecycle state frontend display (delegated_frontend; after ST-02 + position lifecycle UX spec locked ✅)

*Note: ST-03 should close Sprint 1 as it's delegated_frontend and depends on ST-02.*

### Sprint 2 (7 stories — EPIC-02 + EPIC-04 ST-16/17)

12. **ST-04** — Grace Period Decision Support backend (autonomous; after EPIC-01 complete)
13. **ST-06** — Stop Management Workflow backend (autonomous; after EPIC-01 complete; parallel with ST-04)
14. **ST-05** — Grace Period Decision Support frontend (delegated_frontend; after ST-04)
15. **ST-07** — Stop Management Workflow frontend (delegated_frontend; after ST-06)
16. **ST-16** — Feature flag rollout (delegated_backend; after ST-03 complete for proof-of-concept)
17. **ST-17** — Trade plan abandonment + badges + quick wins (delegated_frontend; independent; can run parallel to ST-04/06)

---

## Risk Flags

| Risk ID | Associated EPIC | Description | Mitigation Status |
|---------|----------------|-------------|------------------|
| RISK-01 | EPIC-01 | Position state machine complexity — back-fill edge cases | Valid — mitigated by UNKNOWN initial state (ST-01 ACs + design gate); resolved as pre-sprint required decision |
| RISK-02 | EPIC-02 | Stop Management — missing stop values (null current_stop) | Valid — ST-06 AC specifies null-safe handling; frontend disables button when no stop set |
| RISK-03 | EPIC-03 | Spec authoring dependency — EPIC-03 Sprint 1 must complete before EPIC-02 frontend designs finalise | Valid — sequencing enforced: EPIC-03 starts Sprint 1 day 1; EPIC-02 frontend only in Sprint 2 |
| RISK-04 | EPIC-04 | BLG-FEAT-13 scope creep risk — new platform capability | Valid — AC strictly scoped to env-var/config-file, one proof-of-concept gate on ST-03 badge |
| RISK-05 | Release | Design gate required before sprint planning | Resolved ✅ — design gate PASSED 2026-05-09 |

---

## Outstanding Actions

| Action | Owner | Required Before Seal? | Notes |
|--------|-------|----------------------|-------|
| Product Owner: explicitly acknowledge capacity WARN (⚠ ~20d effort vs ~20d capacity mid-point) | Product Owner | Yes | IMP-41 requirement; record in sprint_backlog.md sign-off block |
| Product Owner: confirm sprint goal statement | Product Owner | Yes | STEP 6.2 hard gate |
| Product Owner: confirm scope (all 17 stories, 2 sprints) | Product Owner | Yes | STEP 6.2 hard gate |
| EPIC-04 ST-13/14 execution: follow CLAUDE.md §6 checklist for governance prompt edits | Head of Specs Team / PMO Lead | No (execution phase) | Prompt change log advisory — not a planning blocker |
| QA & Testing Owner: author test scenarios for EPIC-01, EPIC-02, EPIC-04 delegated_frontend items | QA & Testing Owner | No (before sprint close) | Test scenario gap flags per LL-v2.0-P4-2 |
