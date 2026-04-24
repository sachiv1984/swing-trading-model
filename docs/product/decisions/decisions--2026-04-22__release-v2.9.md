Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.9
Cycle: 2026-04-22__release-v2.9
Last Updated: 2026-04-24

Superseded by: v2.9 ship — 2026-04-24
Changelog: docs/product/changelog.md#v29
Cycle: 2026-04-22__release-v2.9

## Planning Decisions — v2.9 Arc 1 Foundation

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| DS-01 (Screener Engine, H) deferred to v3.0 | BLG-SPEC-21/23 specs must exist before DS-01 implementation begins; those specs are first-class deliverables of this release | Product Owner | 2026-04-22 |
| DS-02 (Screener Results Page) deferred to v3.0 | Depends on DS-01; DS-01 deferred | Product Owner | 2026-04-22 |
| DS-04 (Earnings Calendar) deferred to v3.0 | M effort; no blocking dependency on v2.9 items; defer to preserve scope | Product Owner | 2026-04-22 |
| DS-03, DS-05, DS-06 in scope for v2.9 | Arc 1 infrastructure items; DS-03 is S effort, DS-05 is M effort; both are prerequisites for DS-01; DS-06 is display-only and batches with DS-05 naturally | Product Owner | 2026-04-22 |
| BLG-GOV-14/15 in scope (governance debt) | CF-1 and CF-2 from v2.8 closure; address now as EPIC-04 governance sprint within v2.9 | Product Owner | 2026-04-22 |
| BLG-AI-01 and TEST-GAP-EPIC-04 in scope | AI governance debt from v2.8; small items (S effort) with clear ACs | Product Owner | 2026-04-22 |
| BLG-GOV-08 retirement recommended | 5 consecutive deferrals; L effort; P3 priority; no evidence of friction from prompt length; Arc 1 execution bandwidth should not be diverted. Recommend retire at next `groom backlog` run. | Product Owner | 2026-04-22 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (specs) and EPIC-03 (governance/QA) in Sprint 1 | Spec and governance prerequisites must exist before Arc 1 implementation begins | Product Owner | 2026-04-22 |
| EPIC-02 (implementation) in Sprint 2 | DS-05 requires BLG-SPEC-22 (Sprint 1); DS-06 requires BLG-GOV-16 sign-off (Sprint 1) | Product Owner | 2026-04-22 |
| BLG-GOV-16 (§13 review) must precede DS-06 implementation | BLG-GOV-16 is a hard gate for DS-06 per roadmap notation; sign-off must be recorded before ST-07 ACs are finalized | Strategy Rules & System Intent Owner | 2026-04-22 |
| BLG-SPEC-22 (Alpaca contract) must precede DS-05 implementation | DS-05 implementation must reference the contract; no ad-hoc endpoint selection allowed | Head of Specs Team | 2026-04-22 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None   | —           | —         | —           | —         |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-04-22__release-v2.9
