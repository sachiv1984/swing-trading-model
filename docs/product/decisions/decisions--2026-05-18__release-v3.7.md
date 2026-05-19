Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v3.7
Cycle: 2026-05-18__release-v3.7
Last Updated: 2026-05-19

Superseded by: v3.7 ship — 2026-05-18
Changelog: docs/product/changelog.md#v37
Verification report: claude/cycles/2026-05-18__release-v3.7/verification_report.md
Cycle: 2026-05-18__release-v3.7

## Planning Decisions — v3.7 Signal-to-Watchlist Workflow + Arc 2 Completion + Governance Hardening

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Prioritise BLG-FE-33 + BLG-FE-34 as S2-01 P1 scope | Signals page currently shows "Add Position" as primary CTA, bypassing the signal → watchlist → research → plan → entry workflow the system is designed to enforce. P1 priority — core workflow discipline. Both items explicitly targeted v3.7 at filing. | Product Owner | 2026-05-18 |
| Include PT-04 (S2-02) as conditional scope | Arc 2 PT-04 (Setup Quality Score) was deferred from v3.6 due to gate condition. Gate (20+ closed trades) must be confirmed by Product Owner at design gate. If confirmed, EPIC-02 proceeds; if not, defers to v3.8. | Product Owner | 2026-05-18 |
| Exclude Arc 4 PO-02/03/04 from v3.7 scope | Data density gates not met. PO-02 requires 6+ months of AI-summarised journal entries; AI Journal live ~1 month. Premature to schedule — no implementation value until gate met. | Product Owner | 2026-05-18 |
| Include S2-03 governance patches as P1 process scope | 5 deferred patches from v3.6 lessons learnt closure all target v3.7. Three affect execution_prompt.md (active recurrence risk); one affects qa_evidence_template.md (BLG-GOV-19 misapplication recurrence). Process integrity requires prompt patch. | Head of Specs Team | 2026-05-18 |
| Include BLG-GOV-23 (scored_initiatives.md refresh) in S2-04 | OA-RP-05 carried 2 consecutive cycles; v3.6 closure recurrence check stated "if not addressed before v3.7 roadmap, treat as escalation." BLG-GOV-23 filed 2026-05-18 — include in v3.7 to resolve escalation risk. | Facilitator | 2026-05-18 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-04 merges first | Smallest EPIC, zero dependencies, purely additive — minimises shared-file conflict surface for subsequent EPICs | PMO Lead | 2026-05-18 |
| EPIC-03 merges second | Governance patches have no dependency on product EPICs; should land early to reduce execution_prompt.md version drift during sprint | Head of Specs Team | 2026-05-18 |
| EPIC-01 merges third | Signals workflow is the core user-facing value of v3.7; merges after governance patches are clean | Product Owner | 2026-05-18 |
| EPIC-02 merges last (conditional) | Arc 2 PT-04 is conditional on gate — must be confirmed and planned after core EPICs are stable; sprint 2 only | Product Owner | 2026-05-18 |
| BLG-FE-34 (ST-03) sequenced after BLG-FE-33 (ST-01+ST-02) within EPIC-01 | BLG-FE-34 signal context panel requires the signal → watchlist linkage from BLG-FE-33 to pass signal data through to the trade plan form | Head of Engineering | 2026-05-18 |
| Sprint 1: EPIC-04 + EPIC-03 + EPIC-01; Sprint 2: EPIC-02 (conditional) | Phasing matches merge order; front-loads P1 user-facing value; Sprint 2 reserved for conditional gate-dependent work | PMO Lead | 2026-05-18 |

### Accepted risks

None.

*(No escalations raised — RISK-01 and RISK-02 are conditional flags managed via pre-sprint gate check and story sequencing respectively; neither required an escalation record.)*

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-05-18__release-v3.7
