Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v3.6
Cycle: 2026-05-16__release-v3.6
Last Updated: 2026-05-16

## Release Scope — v3.6 Arc 4 Data Integrity + Arc 2 Quality Score + Debt Clearance

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Arc 4 Data Capture Foundation — snapshot `planned_entry_price` at trade entry; compute `entry_delta_pct` in plan-vs-reality; update PlanVsReality frontend display |
| S2-02 | EPIC-02 | Arc 2 Completion: PT-04 Setup Quality Score — spec authoring + backend scoring endpoint + frontend display in Pre-Trade Research View (gated: 20+ closed trades confirmed by PO) |
| S2-03 | EPIC-03 | QA, Spec & UX Debt — SC-RV-18/19 Playwright coverage (BLG-FE-32 + TEST-GAP-EPIC-03-v33); research endpoint HTTP error differentiation (BLG-SPEC-27); research page UX fix: regime lozenge + font (BLG-FE-26) |
| S2-04 | EPIC-04 | Governance Maintenance — execution_prompt.md patches (§13 gate story pattern, deviations_filed, sprint_close three-field block, Phase 3 lessons_learnt_cycle.md reference); prompt_change_log.md missing entries (OA-RP-01–04) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| PO-02 Journal Pattern Recognition | Gate: 6+ months AI-summarised journal data (not yet met — AI Journal Summarisation shipped 2026-04-20) | v3.7+ |
| PO-03 Behavioural Error Taxonomy | Depends on PO-02; gate not met | v3.7+ |
| PO-04 Reflection ↔ Outcome Correlation | Depends on PO-02; gate: 50+ trades with plans | v3.8+ |
| PO-05 Lightweight Replay Mode | VH effort; data accumulation required | v3.8+ |
| BLG-FEAT-20 Net-of-costs tracking | Not standalone sprint item; Arc 4 data model timing | v3.7+ |
| BLG-FE-27 Nav bar redesign exploration | P3 Low; non-blocking | TBD |
| BLG-OPS-13 API performance baseline | Requires live environment + human coordination | TBD |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-05-16__release-v3.6
