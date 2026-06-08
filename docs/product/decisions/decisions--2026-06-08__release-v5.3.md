Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v5.3
Cycle: 2026-06-08__release-v5.3
Last Updated: 2026-06-08

## Planning Decisions — v5.3 Spec Debt, Security Hardening & Ops Governance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-SPEC-49–52 (actual contract authoring) alongside BLG-SPEC-53 (resolution plan) | Both the planning doc and the implementation are needed in the same release; authoring contracts without a resolution plan risks inconsistent format; plan-then-implement in same sprint removes inter-release dependency | Product Owner | 2026-06-08 |
| Include CF-1 (qa_evidence_template.md) and CF-2 (execution_prompt.md STEP 5.3A) as P1 sprint stories | These are carry-forward items from v5.2 lessons learnt with target "v5.3 sprint planning review" — must not slip to v5.4 | Head of Specs Team | 2026-06-08 |
| Defer BLG-GOV-105 (Arc 6 PS-03 §13 threshold pre-assessment) to Unscheduled | Provisional-Target was Unscheduled in the backlog; Arc 6 is not yet on the Next horizon — not urgent enough to pull into v5.3 at 22-story load | Product Owner | 2026-06-08 |
| Defer BLG-GOV-112 and BLG-OPS-59 to v5.4 | Both have gates clearing ~2026-07-04 (SI-05 effectiveness review / 4 weeks production) — after any plausible v5.3 sprint window | PMO Lead | 2026-06-08 |
| BLG-GOV-106 (PT-04 gate check) treated as OA-RP-01, not a sprint story | This is a pre-condition gate check (query the DB), not a sprint deliverable; PMO Lead to complete before sprint planning seals | PMO Lead; Product Owner | 2026-06-08 |
| BLG-GOV-111 (design gate pre-assessment) resolved inline | All 22 firm + 3 conditional items assessed in this planning run — zero new UI/UX components; design gate not required | Head of UX & Design; Product Owner | 2026-06-08 |
| 2-sprint phasing (Sprint 1: EPIC-01+02, Sprint 2: EPIC-03+04) | Total scope (~90–126 hrs mid-point) exceeds solo-dev single-sprint capacity; phasing prioritises P1 spec debt and security items first | PMO Lead | 2026-06-08 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 before EPIC-04 (cross-sprint dependency) | BLG-QA-54 (coverage matrix update) must capture EPIC-01 contract authoring; EPIC-04 merges in Sprint 2 after EPIC-01 contracts are committed to main | Head of Specs Team | 2026-06-08 |
| BLG-SPEC-53 (resolution plan) stories ST-04–ST-07 sequenced after ST-01 within EPIC-01 | Resolution plan and QA AC definition (ST-01, ST-03) should complete before contract authoring starts (ST-04–ST-07) to ensure consistent acceptance criteria | Head of Specs Team | 2026-06-08 |
| EPIC-03 merge before EPIC-04 in Sprint 2 | CF-1 (qa_evidence_template.md patch) in EPIC-03 must land before EPIC-04 delivery verification uses the updated template | Head of Specs Team | 2026-06-08 |

### Accepted risks

None — no escalations raised; all risks managed within scope decisions.

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-06-08__release-v5.3
