Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.7
Cycle: 2026-08-12__release-v8.7
Last Updated: 2026-08-13
Superseded by: v8.7 ship — 2026-08-13
Changelog: docs/product/changelog.md#v8.7
Verification report: claude/cycles/2026-08-12__release-v8.7/verification_report.md

## Planning Decisions — v8.7 User Features, Data-Integrity Closure & Cross-Domain Hardening

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sequence EPIC-01 (user-facing product features & UX completion) first in the Execution Plan, ahead of debt/process EPICs | Explicit user instruction: "use full capacity, user features to be prioritised" | Product Owner (per user directive) | 2026-08-12 |
| Draw scope directly from the ungated backlog pool via `scripts/scan_backlog_gate_conditions.py` rather than a formal roadmap Now-horizon | No formal `## v8.7` roadmap section exists; `2026-08-11__scheduled` rebalance recorded STEP 8.1 Option (b) — defer, 4th consecutive firing, consistent with the established backlog-driven-scoping pattern since v8.0 | Product Owner | 2026-08-12 |
| Include `BLG-BE-96` (EPIC-02) as a mandatory, non-negotiable item regardless of user-features-first ordering | Carries an explicit v8.6 Product Owner risk-acceptance condition: "do not defer further" (`qa_evidence_EPIC-02.md`) | Product Owner (standing decision, ratified 2026-08-12) | 2026-08-12 |
| Target 25.25 estimated days against the confirmed 24–28 day capacity band (no scope trim) | Satisfies "full capacity" without exceeding the confirmed ceiling or requiring a WARN-level capacity outcome | Product Owner | 2026-08-12 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| `BLG-FE-157` (EPIC-03) sequenced alongside/after `BLG-FE-156` (EPIC-01) within the same sprint window | Coverage authoring should follow the modal token conversion to avoid selector drift (RISK-03) | PMO Lead | 2026-08-12 |
| `BLG-BE-96`'s live-DB checks scheduled without further deferral | v8.6 attempt could only exercise mocked-DB tests; a second consecutive deferral would leave the underlying 0/11-linked-trade-plans risk class unverified for two full release cycles | Product Owner | 2026-08-12 |

### Accepted risks

None. (Risk register entries RISK-01 through RISK-07 are tracked in `release_plan.md §Execution Plan`; none required formal risk acceptance — all have an in-scope mitigation path.)

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-12__release-v8.7
