Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v4.2
Cycle: 2026-05-27__release-v4.2
Last Updated: 2026-05-29

## Planning Decisions — v4.2 Claude API Governance, SI-02 Pre-Work Readiness & Spec Debt

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-GOV-63 (Claude API audit trail) as M-effort backend implementation in Sprint 2 | Enables BLG-OPS-36 monthly review data fidelity; analogous to BLG-GOV-35 Gemini pattern (low-risk); Sprint 1 baselines (BLG-OPS-36) can run against existing logging if GOV-63 not yet complete | Product Owner | 2026-05-27 |
| Include BLG-GOV-60 (SI-02 prerequisites checklist) in S2-04 despite non-v4.2 target | Target is "before SI-02 sprint planning seals" — v4.2 is the immediate next sprint; completing the checklist now unblocks SI-02 sprint planning at earliest gate-clear date | PMO Lead | 2026-05-27 |
| BLG-BE-22 (prompt caching assessment) as optional v4.2 item | Sprint 2 WARN on capacity; BLG-BE-22 is S-effort P2 with no hard deadline — defer to post-v4.2 if Sprint 2 overloads, retain in scope if not | Product Owner | 2026-05-27 |
| Defer BLG-SPEC-41, BLG-GOV-62 (SI-02/SI-04 gate-conditional items) | Both gated on sprint planning imminent triggers not yet met; forced inclusion before gate clear has no delivery value | Head of Specs Team | 2026-05-27 |
| BLG-GOV-58 not included (pre-resolved) | Resolved by AUD-2026-05-27-003 (execution_prompt.md v3.29) before planning commenced; ACs met; mark COMPLETE at next groom backlog | Head of Specs Team | 2026-05-27 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Merge order Sprint 1: EPIC-01 → EPIC-02 | EPIC-01 (pure policy/docs) can merge first as self-contained; EPIC-02 (baselines) depends on EPIC-01 log hygiene policy being defined | PMO Lead | 2026-05-27 |
| Merge order Sprint 2: EPIC-04 → EPIC-03 | EPIC-04 (governance prep docs) is independent and lower risk; EPIC-03 (GOV-63 backend) merges last as it modifies backend code | PMO Lead | 2026-05-27 |
| BLG-OPS-36 (monthly review) in Sprint 1, BLG-GOV-63 (audit trail) in Sprint 2 | Monthly review can run against existing basic logging; formal audit trail implementation sprint-2 improves future review fidelity | Infrastructure & Operations Owner | 2026-05-27 |

### Accepted risks

None. No escalations raised during this release planning cycle.

### Supersession note

Superseded by: v4.2 ship — 2026-05-29
Changelog: docs/product/changelog.md#v42
Cycle: 2026-05-27__release-v4.2
