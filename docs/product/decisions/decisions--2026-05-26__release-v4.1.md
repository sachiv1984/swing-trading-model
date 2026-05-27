Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v4.1
Cycle: 2026-05-26__release-v4.1
Last Updated: 2026-05-27
Superseded by: v4.1 ship — 2026-05-27
Changelog: docs/product/changelog.md#v41
Cycle: 2026-05-26__release-v4.1

## Planning Decisions — v4.1 Governance Hardening, Spec Debt, Arc 5 Compliance + SI-02 Pre-Planning

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include OA-01 (execution_prompt merge-gate) and OA-02 (sprint_planning staging-only AC) as mandatory Sprint 1 stories | 2nd recurrence escalations — if missed in v4.1, CLAUDE.md §2 mandate required per v4.0 closure record | Product Owner; Head of Specs Team | 2026-05-26 |
| Include BLG-SPEC-33 and BLG-SPEC-34 as Sprint 1 stories | Overdue by 1 cycle (Provisional-Target was v4.0); downstream features (SPEC-38, FEAT-42) gate on these | Product Owner | 2026-05-26 |
| Bundle BLG-FEAT-40 (composite score formula) into same story as BLG-FEAT-42 (P&L integration) | FEAT-42 lists FEAT-40 as a precondition; both are S/M effort and naturally sequential; separating adds overhead without benefit | Product Owner | 2026-05-26 |
| Bundle BLG-QA-28/29/30 + BLG-OPS-28 into single staging verification story (ST-11) | All are XS staging-only verification tasks from v4.0 deferred ACs; natural bundle for a single sprint slot | Director of Quality | 2026-05-26 |
| Bundle BLG-GOV-44/46/51 into ST-13, BLG-GOV-49/54/56 into ST-14, BLG-OPS-29/30/32 into ST-15 | All grouped by theme (SI-02 pre-planning, security+governance patches, operational reviews); all S effort; bundling reduces story overhead | PMO Lead | 2026-05-26 |
| Exclude PT-04 from v4.1 scope | Gate not met: requires 20+ closed trades; current count insufficient | Product Owner | 2026-05-26 |
| Exclude Arc 6 items from v4.1 scope | Gate not met: requires 50–100+ trades | Product Owner | 2026-05-26 |
| Design gate NOT required for v4.1 | Scope contains no new UX patterns: governance prompts, API contracts, documentation, and minor features only | Head of UX & Design; Product Owner | 2026-05-26 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 + EPIC-02 in Sprint 1; EPIC-03 + EPIC-04 in Sprint 2 | OA-01/OA-02 are 2nd recurrence — must ship first; API contract spec debt blocks EPIC-03 ST-07 (Gemini thesis contract gates on SI-03 contract) | PMO Lead | 2026-05-26 |
| EPIC-02 ST-04 (BLG-SPEC-33) must complete before EPIC-03 ST-07 (BLG-SPEC-38) commences | BLG-SPEC-38 lists BLG-SPEC-33 as explicit gate condition; both in different sprints by design | Head of Specs Team | 2026-05-26 |
| EPIC-04 (SI-02 pre-planning) independent of EPIC-03 within Sprint 2 | EPIC-04 is all documentation/reviews with no deployment; can run in parallel with EPIC-03 implementation | PMO Lead | 2026-05-26 |
| Recommended merge order: EPIC-01 → EPIC-02 (Sprint 1); EPIC-04 → EPIC-03 (Sprint 2) | EPIC-04 doc artefacts are faster to produce; EPIC-03 has M effort items (ST-08, ST-09) that benefit from being last | PMO Lead | 2026-05-26 |
| ST-09 (BLG-OPS-34, M effort) and ST-11 (staging bundle) are deferral candidates if Sprint 2 is capacity-constrained | ST-09 is monitoring-only; ST-11 is verification-only — neither blocks SI-02 pre-planning or future spec work | Product Owner | 2026-05-26 |

### Accepted risks

None — no Accepted Risk escalations raised in this cycle.

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-05-26__release-v4.1
