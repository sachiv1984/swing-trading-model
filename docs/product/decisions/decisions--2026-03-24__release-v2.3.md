Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v2.3
Cycle: 2026-03-24__release-v2.3
Last Updated: 2026-03-24

---

## Planning Decisions — v2.3 Quality Automation & User Insight

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-FEAT-11 (Strategy Compliance Score) despite SPS=4 | High user value (daily visibility of stop discipline); display-only constraint fully specified in AC; Strategy Rules sign-off required at delivery verification per existing process | Product Owner + Strategy Rules & System Intent Owner | 2026-03-24 |
| Include BLG-QA-05 (smoke test) and BLG-QA-06 (seed scripts) as a bundle with BLG-OPS-08 prerequisite | QA automation is a strategic v2.3 priority; BLG-OPS-08 is a hard prerequisite and must be Sprint 1; phasing ensures no wasted sprint planning overhead | QA & Testing Owner + Infrastructure & Operations Owner | 2026-03-24 |
| Include BLG-UX-01 (sidebar nav) conditionally, requiring Product Owner design decision before engineering sprint | BLG-UX-01 is P2 and genuinely valuable, but engineering cannot proceed without the grouping/pattern decision; conditioning on design protects sprint capacity | Product Owner | 2026-03-24 |
| Include BLG-GOV-08 (engine prompt compression) as conditional/stretch in Sprint 3 | L effort governance task with clear value (token reduction, audit-identified); conditional status means it does not block release if capacity is consumed by UX-01 or feature scope | Head of Specs Team | 2026-03-24 |
| Defer BLG-GOV-03 (simplify artefact sealing) to v2.4 | Circular concern: modifying the release planning engine schema mid-cycle while running that engine introduces unnecessary risk; best deferred to a stable release | Head of Specs Team | 2026-03-24 |
| Defer BLG-FE-03, BLG-BE-04, BLG-OPS-05, TEST-GAP-EPIC-05-SLIP to v2.4 | All P3; displaced in priority queue by higher-value QA automation and feature items per roadmap rebalance displacement signals | Product Owner | 2026-03-24 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| BLG-OPS-08 (staging reset) in Sprint 1 | Hard prerequisite for BLG-QA-06 and BLG-QA-05; must be established before seed scripts are written | Infrastructure & Operations Owner | 2026-03-24 |
| BLG-SPEC-D14 (health spec) in Sprint 1 | XS item; BLG-OPS-07 (health playbook) references v1.1 spec, so the spec must be published first | API Contracts Owner | 2026-03-24 |
| EPIC-01 (FEAT-11 + FEAT-09) in Sprint 2 | Allows Sprint 1 to establish the QA and ops infrastructure; FEAT-11 SPS=4 sign-off benefits from non-rushed time allocation in Sprint 2 | Product Owner | 2026-03-24 |
| BLG-UX-01 deferred within cycle to Sprint 3 conditional | Product Owner design decision required before engineering sprint; Sprint 3 provides the latest possible slot before the cycle closes | Product Owner | 2026-03-24 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None   | —           | No escalations raised; all risks mitigated via sequencing and conditionals | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-03-24__release-v2.3
