Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.4
Cycle: 2026-05-14__release-v3.4
Last Updated: 2026-05-14

**Superseded by:** v3.4 ship — 2026-05-14
**Changelog:** docs/product/changelog.md#v3.4
**Verification report:** claude/cycles/2026-05-14__release-v3.4/verification_report.md
**Cycle:** 2026-05-14__release-v3.4

## Planning Decisions — v3.4 Arc 3 In-Trade Risk Management (continued)

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| IT-06 Alpaca Paper Trading deferred | §13 review gate not cleared — paper trading touches execution infrastructure; cannot proceed until gate is cleared | Product Owner + Strategy Rules owner | 2026-05-14 |
| PT-04 Setup Quality Score deferred | Gate condition (20+ closed trades) not yet met | Product Owner | 2026-05-14 |
| BLG-FE-23/24/25/29/30 included in v3.4 | Deferred from v3.3 ST-17; P2/P3 quick wins with Provisional-Target v3.3; appropriate to clear in v3.4 alongside Arc 3 frontend work | Product Owner | 2026-05-14 |
| BLG-FE-31 included as Sprint 1 first item | Component library needed as reference before EPIC-01 implementation (as stated in item acceptance criteria) | Product Owner + Head of Specs Team | 2026-05-14 |
| EPIC-02 (IT-04/05) sequenced Sprint 2, post design gate | IT-04/05 are new Arc 3 features requiring UX specs — design gate must produce these before sprint planning seals EPIC-02 | Product Owner + PMO Lead | 2026-05-14 |
| Arc 3 frontend (EPIC-01) sequenced Sprint 2 | UX specs exist from v3.3; component library (BLG-FE-31, Sprint 1) should be consulted first; EPIC-01 is implementation-ready | Head of Engineering | 2026-05-14 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sprint 1: EPIC-03 + EPIC-04 | Front-load quick wins and spec/docs; carry-forward LL-v3.3 item 1 — front-loading frontend (EPIC-03 is frontend quick wins) | PMO Lead + Product Owner | 2026-05-14 |
| Sprint 2: EPIC-01 + EPIC-02 | Arc 3 new functionality after design gate; EPIC-01 implementation using component library reference from EPIC-04 | PMO Lead | 2026-05-14 |
| BLG-FE-31 first in Sprint 1 | Must precede EPIC-01 frontend implementation per acceptance criteria | Head of Specs Team | 2026-05-14 |
| Merge order: EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02 | LL-v3.3 carry-forward item 2 — governance EPIC (EPIC-04) first; Arc 3 backend/frontend last. Document in execution_state.json. | Head of Engineering | 2026-05-14 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | | No escalations raised in this cycle | | |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-05-14__release-v3.4
