**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-11
**Cycle:** 2026-03-06__release-v1.9
**Sprint:** 2 of 2

---

# Sprint Planning Notes — 2026-03-06__release-v1.9 Sprint 2

---

## Backlog Slice Source

Original — `claude/cycles/2026-03-06__release-v1.9/stage4_backlog_slice.md`

No `amended_backlog_slice_path` set in `.claude_current_state.json`.

---

## Multi-Sprint Re-Entry Note

This is Sprint 2 of a 2-sprint v1.9 cycle. Sprint 1 items (EPIC-04, EPIC-05 Phase 1, EPIC-06) were delivered and verified (2026-03-09). All §6 outstanding actions from the Sprint 1 closure record resolved 2026-03-10.

**Lifecycle Guard Process Gap (recorded as lesson learnt):** The sprint planning lifecycle guard requires status = `Design_Gate_Passed` or `Release_Planning_Complete` as valid from-states. For Sprint 2 re-entry, the current status is `Sprint_Planning_Complete`. This is a process gap in the lifecycle schema for multi-sprint cycles. The user (Product Owner) explicitly issued `plan sprint` per the execution engine halt report and sprint_backlog.md Sprint 1 direction. This explicit PO instruction satisfies the -1.1 exception requirement. The lifecycle schema should be patched to formally allow `Sprint_Planning_Complete → Sprint_Planning_Complete` (re-entry) for multi-sprint cycles — filed as lesson learnt below.

---

## Deferred Items

No items deferred from Sprint 2 scope. All 6 items are included:

| Item | EPIC | Reason | Sprint 3 Candidate? |
|------|------|--------|---------------------|
| — | — | — | — |

*(All Sprint 2 items are in scope. If the Product Owner defers any at sign-off, this table will be updated.)*

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | — | — | Independent (spec-first within item; no external gate) |
| ST-02 | ST-01 complete (metrics canonical) | Internal spec gate | Unresolved — ST-01 metrics_definitions.md update must commit before ST-02 backend begins |
| ST-02 | Data Model owner schema confirmation | Pre-condition | Advisory — confirm trade_reflections schema before ST-02 backend (not a planning blocker; at-execution pre-condition) |
| ST-03 | ST-01 (cohort defs may batch into metrics update) | Advisory batch | ST-01 and ST-03 metrics updates can be batched into single metrics_definitions.md commit |
| ST-04 | ST-01 (R-multiple formula canonical) | Internal spec gate | ST-01 R-multiple formula must be canonical before ST-04 backend compute begins |
| ST-05 | — | — | Independent; all data from existing endpoints |
| ST-12 | ST-01, ST-02, ST-03, ST-04, ST-05 | Distributed | Scenarios authored as each feature completes — no single blocker |

**No circular dependencies detected.**

---

## Execution Sequence

### Wave 1 — Parallel start (no blockers)

| Order | Item | Rationale |
|-------|------|-----------|
| 1a | ST-01 | Metrics definitions first; unblocks ST-02, ST-04; metrics batch with ST-03 defs advisable |
| 1b | ST-05 | Independent dashboard homepage; no backend dependency |

### Wave 2 — After ST-01 metrics canonical

| Order | Item | Rationale |
|-------|------|-----------|
| 2a | ST-03 | Cohort Analysis — cohort metric defs batched with ST-01 or added in ST-01 PR |
| 2b | ST-04 | R-Multiple — R-multiple formula must be in metrics_definitions.md |
| 2c | ST-02 | Trade Reflection Template — ST-01 must complete; data model owner schema confirmation required before backend |

### Wave 3 — Distributed throughout sprint

| Order | Item | Rationale |
|-------|------|-----------|
| 3 | ST-12 | Phase 2 test scenarios authored as each Wave 1/2 feature completes |

---

## Risk Flags

| Risk ID | Associated Item | Status | Mitigation |
|---------|----------------|--------|------------|
| RISK-01 | EPIC-01 (ST-01) | PASS — LL-05 confirmed Stage 4.5 | Metrics Definitions owner confirmed available |
| RISK-02 | EPIC-01 (ST-02) | Monitor | Data Model & Domain Schema Owner must confirm trade_reflections schema before ST-02 backend. Record in ST-02 pre-conditions at execution. |
| RISK-03 | EPIC-02 (ST-03, ST-04) | Mitigation active | Batch metrics defs into single ST-01 update — ST-03 cohort defs and ST-04 R-multiple formula in same metrics_definitions.md commit |
| RISK-04 | EPIC-03 (ST-05) | Advisory | Composite endpoint: aggregation-only constraint enforced at execution. Head of Engineering to decide at ST-05 start whether composite endpoint is needed or individual calls sufficient. |

---

## Pre-Sprint Vulnerability Scan

pip-audit run 2026-03-11: **clean — 0 vulnerabilities** across all 55 dependencies. No action required. Scan output recorded.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Product Owner: confirm sprint goal wording | Product Owner | Yes |
| Product Owner: confirm Sprint 2 scope (all 6 items) | Product Owner | Yes |
| Product Owner: confirm over-allocation acceptance (~49 hrs vs ~25 hrs capacity) | Product Owner | Yes |
| Data Model & Domain Schema Owner: confirm trade_reflections schema before ST-02 execution | Data Model Owner | No — before ST-02 execution only |
| Head of Engineering: composite endpoint decision for ST-05 | Head of Engineering | No — at ST-05 execution start |

---

## Lesson Learnt — Lifecycle Schema Gap (Sprint 2 Planning)

| Item | Friction | Proposed Fix | Owner | Target |
|------|---------|-------------|-------|--------|
| Sprint 2 lifecycle re-entry | Sprint planning lifecycle guard valid from-states (`Design_Gate_Passed`, `Release_Planning_Complete`) do not include `Sprint_Planning_Complete`. Multi-sprint cycles need a re-entry path after Sprint 1 closes. | Patch `lifecycle_schema.json` to allow `Sprint_Planning_Complete → Sprint_Planning_In_Progress` transition (multi-sprint condition, requires explicit PO instruction). Update `shared_standards.md §10.1` and `sprint_planning_prompt.md §2` to document the multi-sprint re-entry exception formally. | Head of Specs Team | Before next multi-sprint cycle |
