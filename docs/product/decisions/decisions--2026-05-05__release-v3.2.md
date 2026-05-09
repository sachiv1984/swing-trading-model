Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.2
Cycle: 2026-05-05__release-v3.2
Last Updated: 2026-05-08
Lifecycle Guide: claude/charter/document_lifecycle_guide.md

---

## Planning Decisions — v3.2 Arc 2 Pre-Trade Research & Planning

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| PT-02 frontend is primary deliverable; PT-03 bundled with PT-02 as S2-02 | PT-02 backend shipped v3.1; frontend is the outstanding Arc 2 obligation. PT-03 backend is already live — integration cost is low and value is immediate | Product Owner | 2026-05-05 |
| PT-05 (Entry Checklist) included in v3.2 as EPIC-02 | Both PT-02 and PT-05 were deferred from v3.1; sequencing PT-05 in Sprint 2 (after PT-02) satisfies the roadmap dependency | Product Owner | 2026-05-05 |
| BLG-FEAT-13 (gated feature rollout) deferred to v3.3 | Arc 2 is already at WARN capacity; BLG-FEAT-13 is P3 with no Arc 2 dependency. 2nd consecutive deferral — mandatory for v3.3 | Product Owner | 2026-05-05 |
| BLG-FE-22 (Screener UX spec) treated as design gate prerequisite, not sprint story | Explicitly flagged "before v3.2 sprint planning" — design gate is the correct phase for this deliverable | Product Owner | 2026-05-05 |
| OA-02 to OA-05 (D-01 to D-04) actioned as EPIC-03 sprint stories | 4 deferred v3.1 lessons_learnt items have been outstanding one cycle; governance debt should not carry further | Product Owner | 2026-05-05 |
| BLG-GOV-11 (cycle artefact inventory) included as ST-17 | 3rd consecutive deferral; mandatory action in v3.2 per backlog notes | PMO Lead | 2026-05-05 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sprint 1: EPIC-01 + EPIC-03; Sprint 2: EPIC-02 + EPIC-04 | EPIC-01 (PT-02 frontend) is the highest-value deliverable; EPIC-03 (governance patches) is lightweight and clears OA backlog. EPIC-02 (PT-05) must follow EPIC-01 merge | PMO Lead | 2026-05-05 |
| Design gate required before sprint planning seals | BLG-FE-22 (Screener UX spec) must inform PT-02 story acceptance criteria; RISK-01 classified High with "must resolve before sprint planning seal" disposition | Product Owner + Head of UX & Design | 2026-05-05 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | — | — | — |

### Supersession note
Superseded by: v3.2 ship — 2026-05-08
Changelog: docs/product/changelog.md#v3.2
Cycle: 2026-05-05__release-v3.2
