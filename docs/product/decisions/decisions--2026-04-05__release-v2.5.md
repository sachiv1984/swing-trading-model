Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v2.5
Cycle: 2026-04-05__release-v2.5
Last Updated: 2026-04-10

Superseded by: v2.5 ship — 2026-04-10
Changelog: docs/product/changelog.md#v25
Verification report: claude/cycles/2026-04-05__release-v2.5/verification_report.md
Cycle: 2026-04-05__release-v2.5

## Planning Decisions — v2.5 Integration Baseline, Quick Wins & Governance Debt

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include all 7 P2 backlog items (BLG-OPS-12, BLG-BE-08, BLG-BE-09, BLG-BE-07, BLG-GOV-10, BLG-GOV-12, TEST-GAP-EPIC-01-v24) | Clear all P2 items from v2.5 candidate pool before scheduling P3 items | Product Owner | 2026-04-05 |
| Include v2.4 deferred prompt patches as ST-12 | CF-2 carry-forward required scheduling by release planning; patches are S-effort and should precede sprint execution | Product Owner | 2026-04-05 |
| Include BLG-FEAT-15 (fee drag metric) as P3 item | Well-defined scope (S effort), all data already stored, no schema changes needed, high analytical value | Product Owner | 2026-04-05 |
| Defer BLG-FE-09, BLG-SPEC-D17, BLG-GOV-11, BLG-GOV-14 to v2.6 | New items from 2026-04-05 rebalance; Skill-Silo Alert warned of 100% governance-heavy additions; these are P3 and can wait one cycle | Product Owner | 2026-04-05 |
| Defer BLG-GOV-08 (prompt compression) to v2.6+ | L effort; not urgent; BLG-FE-09 was already deprioritising it | Product Owner | 2026-04-05 |
| Defer BLG-FEAT-13 (feature rollout capability) to v2.6 | P3; M effort; not urgent for current scale | Product Owner | 2026-04-05 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sprint 1: EPIC-04 + EPIC-01 | Governance patches (prompt fixes, batch push fix, backlog rule) should be applied before any sprint execution that relies on them; System Status reliability is highest P2 item | PMO Lead | 2026-04-05 |
| Sprint 2: EPIC-02 + EPIC-03 | Investigation and feature work after governance baseline; EPIC-02 investigations may surface backlog items that inform future releases | PMO Lead | 2026-04-05 |
| S2-01 before S2-02/S2-03 within EPIC-01 | Auth forwarding fix must be working before endpoint sync and categorisation are meaningful | Head of Engineering | 2026-04-05 |
| S2-09 (fee drag) requires HoST co-authorship | 3 canonical spec updates + openapi.yaml — highest coordination cost; EPIC-03 branch must start from up-to-date main after EPIC-01 merges | Head of Specs Team | 2026-04-05 |
| EPIC-02: S2-04/S2-05 before S2-06 preferred | Latency investigation benefits from knowing integration state of Reports and Signals pages | Head of Engineering | 2026-04-05 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-04-05__release-v2.5
