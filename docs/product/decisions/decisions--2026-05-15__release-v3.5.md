Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.5
Cycle: 2026-05-15__release-v3.5
Last Updated: 2026-05-15

## Planning Decisions — v3.5 Arc 3 Completion + Arc 4 Foundation

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| IT-06 scoped conditional on §13 review PASS | IT-06 connects to Alpaca execution infrastructure; §13 review required before pre-alignment per roadmap §6 gate; review story (ST-01) included unconditionally; implementation stories conditional | Strategy Rules & System Intent Owner | 2026-05-15 |
| PO-01 (Plan vs Reality Analysis) included as Arc 4 first feature | PT-01 (Trade Plan Object) is live and used (shipped v3.1); position lifecycle data captured (v3.3–v3.4); roadmap explicitly names Arc 4 start for v3.5 | Product Owner | 2026-05-15 |
| BLG-GOV-21 (Arc 4 data requirements capture) included as prerequisite | Arc 4 planning begins in v3.5 per roadmap; data requirements capture must precede PO-01 implementation to prevent mid-arc data model gaps | Product Owner + Head of UX & Design | 2026-05-15 |
| BLG-FE-26 (Research page UX review) deferred again | P3 priority; 3 cycles deferred without blocking workflow impact; design system work better sequenced at Arc 4/5 design gate when broader UX investment is warranted | Product Owner | 2026-05-15 |
| All five Provisional-Target v3.5 backlog items included | BLG-QA-19, BLG-SPEC-29/30/31, BLG-GOV-22 all P2–P3 and XS–S effort; clear v3.5 target; includes all LL v3.4 deferred governance patches | Product Owner | 2026-05-15 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-04 (Governance Patches) Sprint 1 first | Governance patches clear process debt early; prevents recurrence in execution of same sprint | PMO Lead | 2026-05-15 |
| EPIC-03 (Spec & QA Debt) Sprint 1 in parallel with EPIC-04 | No dependencies between EPICs; spec corrections are small and front-loadable | PMO Lead | 2026-05-15 |
| EPIC-01 §13 review (ST-01) Sprint 1 before implementation | §13 determination gates all IT-06 implementation; if FAIL, Sprint 2 capacity reallocated to Arc 4 | Strategy Rules & System Intent Owner | 2026-05-15 |
| EPIC-02 (Arc 4 Foundation) Sprint 2 | BLG-GOV-21 data requirements doc first; PO-01 backend then frontend; allows design gate time to produce PO-01 UX spec before Sprint 2 seals | Head of Engineering + PMO Lead | 2026-05-15 |
| PO-01 frontend may be phased to v3.6 | If IT-06 §13 PASS creates capacity pressure in Sprint 2, PO-01 backend ships v3.5 and frontend phases to v3.6; PO-01 backend has standalone value (data capture begins) | Product Owner | 2026-05-15 |

### Accepted risks

None — no escalations raised in this planning cycle requiring Accepted Risk records.

### Supersession note

Superseded by: v3.5 ship — 2026-05-15
Changelog: docs/product/changelog.md#v35
Verification report: claude/cycles/2026-05-15__release-v3.5/verification_report.md
Cycle: 2026-05-15__release-v3.5
