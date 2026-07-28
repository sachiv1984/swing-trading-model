Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v7.9
Cycle: 2026-07-27__release-v7.9
Last Updated: 2026-07-28

Superseded by: v7.9 ship — 2026-07-28
Changelog: docs/product/changelog.md#v7-9-capacity-fill-engineering-hardening-2026-07-28
Cycle: 2026-07-27__release-v7.9

## Planning Decisions — v7.9 Capacity-Fill & Engineering Hardening

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope v7.9 as a backlog-driven release (no formal roadmap section) via the STEP -1.2 Option (b) equivalence | The `2026-07-27__scheduled` rebalance recorded a STEP 8.1 Option (b) defer (Now horizon fully empty); `plan release` is the named next scoping moment, matching the v7.8 precedent | Product Owner (delegated authority, this session) | 2026-07-27 |
| Include all 15 ungated, ready P1/P2/P3 candidates needed to reach the top of the confirmed capacity band | Explicit user instruction: "ensure you use the full capacity" | Product Owner (delegated authority, this session) | 2026-07-27 |
| Exclude `BLG-FEAT-56` despite its date-based gate sub-condition having elapsed | No evidence available this session to confirm the "established, validated AI-touchpoint usage" sub-condition; excluding rather than assuming pass | Product Owner (delegated authority, this session) | 2026-07-27 |
| Exclude `BLG-FEAT-73`/`BLG-FEAT-74` | Consistent with the already-executed perennial-return disposition (`manage roadmap`, 2026-07-27) — parked until gate permanently clears | Product Owner (prior session, ratified here) | 2026-07-27 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-04 sequenced after EPIC-06 (soft preference, not a hard dependency) | Both touch the financial-reporting/audit-trail domain (Financial Reporting & Records Owner); sequencing them adjacently reduces context-switching risk, not a blocking dependency | Head of Specs Team | 2026-07-27 |
| EPIC-01, EPIC-02, EPIC-05 flagged for Design Gate before Sprint Planning seals | All three carry at least one observable UI acceptance criterion (RISK-01) | Head of Specs Team | 2026-07-27 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| n/a | Workforce/Capacity | Scope intentionally sized to ~95-110% utilisation of the confirmed ~24-28 day capacity band (no formal escalation raised — within-ceiling per STEP 4.5, user-directed, not an over-allocation WARN requiring Accepted Risk) | Product Owner (user instruction, this session) | n/a |

*(No formal Accepted Risk escalation was raised this cycle — capacity outcome is `pass`, not `warn`/`fail`, so the escalation subroutine was not triggered.)*

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-27__release-v7.9
