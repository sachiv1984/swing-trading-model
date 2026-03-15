Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v1.10
Cycle: 2026-03-15__release-v1.10
Last Updated: 2026-03-15

---

## Planning Decisions — v1.10 Operations & Quality Foundation

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-TECH-06 (CohortAnalysis fix) in v1.10 | Architecture debt item with regression risk; backlog target was v1.10; cost is low (< 1 day); aligns with quality foundation theme | Head of Engineering | 2026-03-15 |
| Include BLG-API-01 (integration tests) in v1.10 | QA infrastructure gap; Director of Quality identified gap at ST-11 (2026-03-09); backlog target v1.10; complements staging environment | Director of Quality | 2026-03-15 |
| Assign BLG-QA-01 as new BLG-ID for TEST-GAP-EPIC-06 | Item had no BLG-ID (orphan notice). Advisory from STEP 1.1: 3 cycles without story assignment. Promoting to ST-07 in this release resolves the orphan. | QA & Testing Owner | 2026-03-15 |
| BLG-OPS-01 must enter as Prerequisite item | LL-01 from cycle 2026-03-15__item-5.3: staging environment must precede or accompany new features, not be a peer item. If phasing occurs, EPIC-01 enters Phase 1. | PMO Lead | 2026-03-15 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (BLG-OPS-01) first — P1 prerequisite | Lessons learnt LL-01: dev environment gap must precede feature work; no phasing may deprioritise EPIC-01 to Sprint 2 | Infrastructure & Operations Owner | 2026-03-15 |
| EPIC-02 (BLG-TECH-06) independent | Frontend-only refactor; no backend changes required; no blocking dependencies | Head of Engineering | 2026-03-15 |
| EPIC-03 (QA) after or alongside EPIC-01 | BLG-API-01 CI tests benefit from staging environment being in place, but are not hard-blocked by it | QA & Testing Owner | 2026-03-15 |

### Accepted risks

None — no Accepted Risk escalations raised in this cycle.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-03-15__release-v1.10
