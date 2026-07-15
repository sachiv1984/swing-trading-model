Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v7.2
Cycle: 2026-07-15__release-v7.2
Last Updated: 2026-07-15

## Planning Decisions — v7.2 Dashboard & Trade-Plan UX Hardening

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Pull all 8 roadmap v7.2 Now-horizon candidates into scope (5 P1 UX items + 3 P2 supporting readiness-pass items) — no deferrals | All 8 items are ungated, `Provisional-Target: v7.2`, and were purpose-anchored to this release at the 2026-07-15__scheduled rebalance (STEP 8.1 Option (a)) | Product Owner | 2026-07-15 |
| Group scope into 5 EPICs rather than 8 independent stories, pairing each `BLG-SPEC-*` readiness pass with its dependent `BLG-FE-*` implementation item(s) | `BLG-SPEC-89`/`BLG-SPEC-90` exist specifically to de-risk their paired implementation items before sprint planning; grouping keeps the dependency explicit in the plan structure | Head of Specs Team | 2026-07-15 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| `EPIC-01` (`BLG-FE-55`) sequenced first, ahead of `EPIC-02`/`EPIC-03` | Roadmap annotation explicitly recommends this — mobile responsiveness findings may affect scope/approach for the four dashboard/trade-plan UX items | Head of UX & Design (roadmap-carried recommendation) | 2026-07-15 |
| `BLG-SPEC-89` must complete before `BLG-FE-109` enters sprint planning; `BLG-SPEC-90` must complete before `BLG-FE-110`/`BLG-FE-111` enter sprint planning | Both readiness passes exist to close pre-implementation gaps (contract, data model, §13 boundary, design system formalisation) identified during idea intake — sprint planning should not seal on the implementation items until their readiness pass has landed | Head of Specs Team | 2026-07-15 |
| `BLG-QA-111`'s combined design review + shared Playwright suite plan should be scheduled ahead of sprint planning, covering `EPIC-02`, `EPIC-03`, and `EPIC-04` | Avoids four independent design reviews / four separate Playwright spec files for closely related dashboard/trade-plan surface changes, per `BLG-QA-111`'s own AC and CLAUDE.md's frontend Playwright coverage requirement | Director of Quality | 2026-07-15 |

### Accepted risks
None — no Accepted Risk escalations raised this cycle. All 5 risk-register entries (see `release_plan.md §Execution Plan → Risk Register Summary`) are mitigated in-plan (Medium/Low priority, or High priority with an explicit in-scope mitigation item), with no `escalation_ref`.

### Supersession note
Superseded by: v7.2 ship — 2026-07-15
Changelog: docs/product/changelog.md#v7.2
Cycle: 2026-07-15__release-v7.2
