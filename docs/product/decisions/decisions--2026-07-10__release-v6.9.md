Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v6.9
Cycle: 2026-07-10__release-v6.9
Last Updated: 2026-07-10

Superseded by: v6.9 ship — 2026-07-10
Changelog: docs/product/changelog.md#v6.9
Verification report: claude/cycles/2026-07-10__release-v6.9/verification_report.md
Cycle: 2026-07-10__release-v6.9

## Planning Decisions — v6.9 On-Demand Compliance Recheck & Gap Risk Flag

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope v6.9 to exactly the two named mandatory Product Value Alert pull-forwards (`BLG-FEAT-64`, `BLG-FEAT-65`) — no additional items added | 2nd consecutive Product Value Alert (ratio 0.18) named these as the explicit anchor candidates at rebalance `2026-07-10__scheduled`; Now horizon was intentionally left empty (Option (b)), delegating scoping authority to this release planning invocation; no other backlog item carries a `Provisional-Target: v6.9` signal | Product Owner | 2026-07-10 |
| Treat SI-02 gate condition 1 as still NOT MET, do not pull SI-02-adjacent work into this release | Live production query this session confirmed 20 total closed trades / 11 trade plans / 0 linked — identical to the v6.8 closure finding; carry-forward item 2 from `2026-07-08__release-v6.8/lessons_learnt_closure.md` explicitly warns not to expect the gate to clear from the `BLG-BE-46` fix alone | Product Owner | 2026-07-10 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 and EPIC-02 may execute in either order or in parallel | No shared data model, endpoint, or component dependency between the two features | Head of Specs Team | 2026-07-10 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-10__release-v6.9
