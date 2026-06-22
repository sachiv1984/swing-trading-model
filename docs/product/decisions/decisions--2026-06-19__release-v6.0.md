Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v6.0
Cycle: 2026-06-19__release-v6.0
Last Updated: 2026-06-22

Superseded by: v6.0 ship — 2026-06-22
Changelog: docs/product/changelog.md#v6.0
Verification report: claude/cycles/2026-06-19__release-v6.0/verification_report.md
Cycle: 2026-06-19__release-v6.0

## Planning Decisions — v6.0 Signal Correctness, User Intelligence & SI-05 Effectiveness

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| BLG-BE-36 elevated to P0 Correctness Fast-Track and placed as first story | Signal card shows wrong share counts on every signal — signal_service uses cash-allocation model instead of canonical risk-based model from sizing_service.py. Correctness fast-track (roadmap_prompt.md v7.4) mandates P0 correctness items appear first in Now horizon. | Product Owner | 2026-06-18 (rebalance) |
| BLG-FEAT-46 and BLG-FEAT-20 promoted to P1 to address Product Value Alert | Last rebalance recorded U/(total) ratio = 0.093, triggering Product Value Alert. v6.0 must achieve ≥25% U-story ratio per sprint. Morning Briefing and net-of-costs are highest-impact user-facing items ready for implementation. | Product Owner | 2026-06-18 (rebalance) |
| BLG-OPS-70 reclassified from "firm" (roadmap annotation) to conditional | Gate-clearing date ~2026-06-23 falls within sprint window; STEP 1.4b mandatory rule requires conditional classification. OA-BLG-OPS-70: reclassification noted in run_manifest.md. | Head of Specs Team (STEP 1.4b mandatory) | 2026-06-19 |
| BLG-FE-64 retained as conditional despite 5 consecutive returns | Perennial-return check (STEP 1.4a) surfaced 5 consecutive returns. PO disposition (a): retain conditional — gate clears 2026-06-21 (2 days from planning); evidence is updated (SI-03 live 28 days). Gate genuinely imminent. | Product Owner | 2026-06-19 |
| All 2026-07-04 items retained as conditional | Three items (BLG-GOV-112, BLG-GOV-115, BLG-OPS-59) have 3 consecutive returns with unchanged gate date. PO disposition (a): retain conditional — gate is a scheduled effectiveness review event, 15 days from planning. | Product Owner | 2026-06-19 |
| PT-04 (Setup Quality Score) deferred — sprint planning check | LL-RP-v59-03 carry-forward: 13 closed trades at ~1.5/week; gate projects ~2026-07-02. Sprint planning must re-check count; if ≥20, eligible for conditional sprint addition. | PMO Lead | 2026-06-19 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (Signal Correctness) executes first | P0 priority; correctness fast-track mandate; unblocked (no dependencies) | Product Owner | 2026-06-19 |
| EPIC-02 (User Intelligence) follows EPIC-01 | P1 priority; addresses Product Value Alert; both stories are independent of each other within EPIC-02 | Product Owner | 2026-06-19 |
| EPIC-03 runs after EPIC-01; parallel with EPIC-02 is possible | BLG-FEAT-47 (screener telemetry) and BLG-OPS-70 (ops verification) are independent; can run in parallel with EPIC-02 if capacity permits | PMO Lead | 2026-06-19 |
| EPIC-04 executes last and only after gate confirmation | All EPIC-04 items are conditional; gates must be explicitly confirmed clear before sprint planning assigns them. ST-06 must precede ST-07 within Cluster A | PMO Lead | 2026-06-19 |
| S2-06 (BLG-FE-64) must complete before S2-07 (BLG-FE-41) can begin | BLG-FE-41 explicitly depends on BLG-FE-64 pre-brief; design review brief is the input to the review | Head of Specs Team | 2026-06-19 |

### Accepted risks

None. No escalations were raised during this release planning cycle.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-06-19__release-v6.0
