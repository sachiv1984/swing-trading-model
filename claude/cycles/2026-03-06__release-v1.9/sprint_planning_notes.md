**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-06
**Cycle:** 2026-03-06__release-v1.9

# Sprint Planning Notes — 2026-03-06__release-v1.9

---

## 1. Deferred Items

None. All 19 items included in sprint scope (ST-06 pre-completed; 18 remaining items selected). Over-allocation accepted pending Product Owner sign-off per sprint_capacity.md §4.

---

## 2. Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | — | — | Independent (Metrics Definitions first within item) |
| ST-02 | ST-01 (metrics canonical) | Internal spec gate | Unresolved — ST-01 must complete before ST-02 implementation |
| ST-03 | ST-01 (cohort defs batched) | Internal spec gate | Metrics batch — ST-01 metrics update may include cohort defs |
| ST-04 | ST-01 (R-multiple formula canonical) | Internal spec gate | Unresolved — R-multiple formula must be in metrics_definitions.md before implementation |
| ST-05 | — | — | Independent |
| ST-06 | — | — | **PRE-COMPLETED 2026-03-06** |
| ST-07 | — | — | Independent (backend-only) |
| ST-08 | ST-07 | Soft (backend-first or mock) | ST-07 backend deploy unblocks currency display; ST-08 can proceed with mock |
| ST-09 | ST-07 | Soft (backend-first or mock) | Same as ST-08 |
| ST-10 | — | — | Independent (cosmetic-only) |
| ST-11 | — | — | Independent; enables ST-12 scenario infrastructure |
| ST-12 | EPIC-01, EPIC-02, EPIC-03 delivery | Sequential (distributed) | Scenarios authored as each feature completes |
| ST-13 | — | — | Independent |
| ST-14 | — | — | Independent |
| ST-15 | — | — | Independent |
| ST-16 | — | — | Independent |
| ST-17 | — | — | Independent (BLG-SPEC-D2 resolved v1.8 — no blocker) |
| ST-18 | — | — | Independent |
| ST-19 | — | — | Independent (7 small items; parallelisable) |

**No circular dependencies detected.**

---

## 3. Execution Sequence

### Wave 1 — Parallel start (no dependencies)

| Order | Item | Rationale |
|-------|------|-----------|
| 1a | ST-06 | **DONE** — drawdown spec alignment resolved 2026-03-06 |
| 1b | ST-07 | Backend currency fix; deploy early to unblock frontend waves |
| 1c | ST-10 | Cosmetic fixes; no backend dependency |
| 1d | ST-11 | Seeded test infra setup; enables scenario execution throughout sprint |
| 1e | ST-13 | Service coverage standard; independent CI work |
| 1f | ST-14–ST-19 | All EPIC-06 doc items; autonomous; can run in parallel with all above |

### Wave 2 — After Wave 1 backend deployed

| Order | Item | Rationale |
|-------|------|-----------|
| 2a | ST-08 | Requires backend currency fix (or mock) |
| 2b | ST-09 | Requires backend currency fix (or mock) |
| 2c | ST-01 | Metrics definitions; gates ST-02, ST-03 partial, ST-04 |

### Wave 3 — After metrics definitions canonical (ST-01 complete)

| Order | Item | Rationale |
|-------|------|-----------|
| 3a | ST-02 | Depends on ST-01 |
| 3b | ST-03 | Depends on ST-01 cohort defs |
| 3c | ST-04 | Depends on ST-01 R-multiple formula |
| 3d | ST-05 | Independent; placed last due to composite endpoint pre-alignment decision |

### Wave 4 — Distributed throughout sprint

| Order | Item | Rationale |
|-------|------|-----------|
| 4 | ST-12 | Phase 2 scenarios authored as each Wave 2/3 feature completes |

---

## 4. Risk Flags (from stage3_execution_plan.md)

| Risk ID | Associated Item | Status | Mitigation |
|---------|----------------|--------|------------|
| RISK-01 | EPIC-01 (ST-01) | RESOLVED — LL-05 PASS | Metrics Definitions owner confirmed available |
| RISK-02 | EPIC-01 (ST-02) | Monitor | Data Model owner must confirm trade_reflections schema before ST-02 backend begins. Note in ST-02 pre-conditions. |
| RISK-03 | EPIC-02 (ST-03, ST-04) | Mitigation active | Batch metrics defs into single ST-01 update sprint |
| RISK-04 | EPIC-03 (ST-05) | Advisory | Composite endpoint: aggregation-only constraint enforced at execution |
| RISK-05 | EPIC-04 (ST-08) | Monitor | Base44 entity store fallback approach to be confirmed at ST-08 pre-alignment |
| RISK-06 | EPIC-04 (ST-06) | **RESOLVED 2026-03-06** | ST-06 complete; risk closed |
| RISK-07 | EPIC-05 (ST-11) | Monitor | Test infra approach (seeded DB vs mock layer) to be decided at ST-11 start |
| RISK-08 | EPIC-06 (ST-17) | Closed | BLG-SPEC-D2 resolved in v1.8; no blocker |
| RISK-09 | EPIC-06 (ST-19) | Monitor | Head of Specs Team to verify ADR-002 location at sprint start |

---

## 5. Pre-Sprint Decisions Required (before execution begins)

| Decision | Owner | Required Before |
|----------|-------|----------------|
| Sprint phasing: single sprint (6–9 weeks) vs phased 2-sprint approach | Product Owner | Sprint backlog sign-off |
| ST-11 test infra approach: seeded SQLite vs mock layer vs fixture API | QA & Testing Owner + Head of Engineering | ST-11 start |
| ST-05 composite endpoint: implement or use individual calls | Head of Engineering | ST-05 start |
| ST-08 entity store fallback: disable per component vs add error overlay | Base44 Frontend Prompt Owner | ST-08 start |

---

## 6. Outstanding Actions at Planning

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Product Owner: confirm sprint goal wording | Product Owner | Yes |
| Product Owner: confirm scope (single sprint or phased) | Product Owner | Yes |
| Product Owner: confirm over-allocation explicitly accepted | Product Owner | Yes |
| Data Model & Domain Schema Owner: confirm trade_reflections schema in data_model.md | Data Model Owner | Before ST-02 execution (not a seal blocker) |
| Head of Specs Team: verify ADR-002 location (RISK-09) | Head of Specs Team | Before ST-19 execution (not a seal blocker) |

---

## 7. pip-audit Status

Pre-sprint pip-audit run 2026-03-06: **clean — 0 vulnerabilities.** No action required.
