Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.3
Cycle: 2026-05-09__release-v3.3
Last Updated: 2026-05-09

## Planning Decisions — v3.3 Arc 3 In-Trade Risk Management

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include IT-01, IT-02, IT-03; defer IT-04/05/06 | Arc 3 opens with position lifecycle foundation + two immediately useful decision-support features (grace period + stop management). IT-04/05 build on IT-01; sequence naturally to v3.4. IT-06 needs §13 review. | Product Owner | 2026-05-09 |
| BLG-FEAT-13 mandatory inclusion | 3rd consecutive deferral; roadmap note explicitly marks "mandatory for v3.3". Product Owner must not carry forward again without a named decision record. | Product Owner | 2026-05-09 |
| PT-04 deferred (gate not met) | Requires 20+ closed trades — gate not met at plan date. Carry to v3.4+ gate-dependent. | Product Owner | 2026-05-09 |
| Research view spec closure as EPIC-03 | PT-02 shipped in v3.2 without canonical spec, API contract, or provenance spec. Six P1 items marked "Before v3.3 sprint planning" — must be in Sprint 1 to unblock EPIC-02 frontend designs and comply with process requirements. | Head of Specs Team | 2026-05-09 |
| BLG-FE-26 deferred | P3; research page UX issues (regime lozenge, font) are cosmetic and non-blocking. Deferred to v3.4. | Product Owner | 2026-05-09 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 before EPIC-02 | IT-01 (Position Lifecycle Manager) introduces the position_state field and state machine service. IT-02 (Grace Period) and IT-03 (Stop Management) need the lifecycle state infrastructure to function correctly. | Head of Engineering | 2026-05-09 |
| EPIC-03 Sprint 1 (parallel with EPIC-01) | Research view specs are independent of Arc 3 backend work. Sprint 1 parallel track maximises velocity. Spec outputs are needed before Sprint 2 EPIC-02 frontend designs. | Head of Specs Team | 2026-05-09 |
| EPIC-04 governance patches Sprint 1; BLG-FEAT-13 Sprint 2 | Governance patches (OA-01/02/05) are autonomous-class — no backend dependency. BLG-FEAT-13 (feature flag infrastructure) is best delivered after the Arc 3 foundation is confirmed, then wrapped behind a flag proof-of-concept in Sprint 2. | PMO Lead | 2026-05-09 |
| Design gate required | v3.3 has frontend-visible changes across EPIC-01 and EPIC-02 (position state display, grace period prompt, stop management guided UI). Design gate must produce UX specs for these three surfaces before sprint planning seals. | Head of UX & Design | 2026-05-09 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No accepted risk escalations in this cycle | — | None |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-05-09__release-v3.3
