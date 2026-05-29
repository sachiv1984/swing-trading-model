Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v4.4
Cycle: 2026-05-29__release-v4.4
Last Updated: 2026-05-29

## Planning Decisions — v4.4 Governance Patches, SI-02 Pre-Planning Sprint & Ops Hardening

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-GOV-69 in EPIC-01 despite being filed at delivery verification (not post-ship) | BLG-GOV-69 and BLG-GOV-74 address the same qa_evidence_template.md delegated_qa format gap — combining into single story ST-04 avoids duplication and reduces story count | Product Owner | 2026-05-29 |
| Include all 7 SI-02 pre-planning items despite Provisional-Target: Unscheduled | v4.4 roadmap entry explicitly lists these items; PO authority to advance gated items when gate condition is met; "SI-02 sprint planning imminent" gate is met by v4.4 being the pre-planning sprint | Product Owner | 2026-05-29 |
| Include BLG-BE-20 and BLG-QA-31 as conditional scope items | Gate: "SI-02 sprint planning initiated" — interpreted as: these items are sequenced after BLG-BE-17/18/23 outputs within the same sprint; sprint planning to confirm sequencing | Product Owner | 2026-05-29 |
| Exclude BLG-GOV-70 | Provisional-Target: v4.5 — filed after v4.3 delivery verification; not in v4.4 roadmap entry; low P3 priority | Product Owner | 2026-05-29 |
| Keep EPIC-04 as standalone EPIC for BLG-OPS-43 | Consistent with prior cycle pattern of 4-EPIC structure; BLG-OPS-43 is an Infrastructure & Operations Owner story — clean EPIC ownership boundary | Product Owner | 2026-05-29 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Sprint 1: EPIC-01 + EPIC-04 | Governance patches resolve carry-forward items (BLG-GOV-71/72) and must be applied before next sprint planning; all XS effort — fast to complete | Product Owner | 2026-05-29 |
| Sprint 2: EPIC-02 + EPIC-03 | SI-02 pre-planning is the bulk of the release; BLG-FE-53 depends on BLG-FE-52 output; BLG-QA-31 depends on BLG-BE-20 | Product Owner | 2026-05-29 |
| EPIC-03 merge order: EPIC-01 → EPIC-04 (Sprint 1); EPIC-02 → EPIC-03 (Sprint 2) | EPIC-02 backend outputs are inputs to EPIC-03 FE/QA pre-design; EPIC-03 FE-53 and QA-31 must follow BE-20 and FE-52 respectively | Head of Specs Team | 2026-05-29 |

### Accepted risks

None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-05-29__release-v4.4
