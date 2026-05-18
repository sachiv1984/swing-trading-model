Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Release: v3.7
Cycle: 2026-05-18__release-v3.7
Last Updated: 2026-05-18

---

# Cycle Summary — v3.7 Signal-to-Watchlist Workflow + Arc 2 Completion + Governance Hardening

## Release at a Glance

| Field | Value |
|-------|-------|
| Release | v3.7 |
| Cycle ID | 2026-05-18__release-v3.7 |
| Plan published | 2026-05-18 |
| Prior cycle | 2026-05-16__release-v3.6 (Closed_with_actions) |
| EPICs | 4 (EPIC-01 through EPIC-04) |
| Stories | 11 (8 in Sprint 1; 3 conditional in Sprint 2) |
| Sprints planned | 2 (Sprint 2 conditional on PT-04 gate) |
| Capacity check | WARN (with EPIC-02: ~12.5 days across 2 sprints; without: ~8.5 days in 1 sprint) |
| Design gate required | Yes (EPIC-01 BLG-FE-33/FE-34, EPIC-02 PT-04) |
| Merge order | EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02 |

## Theme

**v3.7 addresses three parallel priorities:**

1. **Workflow discipline (S2-01 / EPIC-01):** The Signals page currently bypasses the system's own funnel discipline by showing "Add Position" as the primary CTA. BLG-FE-33 closes this gap — replacing it with "Add to Watchlist" and enforcing signal → watchlist → research → plan → entry. BLG-FE-34 eliminates the context-switch problem in trade plan authoring by surfacing signal data directly in the form.

2. **Arc 2 completion (S2-02 / EPIC-02 — conditional):** PT-04 (Setup Quality Score) is the last remaining Arc 2 feature, deferred from v3.6 due to the 20+ closed trades gate. If Product Owner confirms the gate at design gate, EPIC-02 proceeds in Sprint 2. If not, it defers to v3.8.

3. **Governance hardening + debt (S2-03/04 / EPIC-03/04):** Three execution_prompt.md patches and one qa_evidence_template.md patch deferred from v3.6 lessons learnt closure. Database stub conftest consolidation closes a recurring CI debugging risk. scored_initiatives.md refresh resolves OA-RP-05 (2 consecutive cycles open).

## Sprint Allocation

| Sprint | EPICs | Stories | Est. effort |
|--------|-------|---------|-------------|
| Sprint 1 | EPIC-04, EPIC-03, EPIC-01 | ST-09 through ST-11, ST-07/ST-08, ST-01 through ST-03 | ~8.5 days |
| Sprint 2 | EPIC-02 (conditional) | ST-04 through ST-06 | ~4 days (if gate met) |

## Pre-sprint Planning Required Decisions

The following High-priority decision must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] PT-04 gate confirmation — Product Owner must confirm closed trade count ≥ 20 before EPIC-02 can be sprint-planned. If not confirmed, EPIC-02 defers to v3.8 and Sprint 2 is omitted. — Owner: Product Owner

## Carry-Forward Items for Sprint Planning

1. **deviations_filed recurrence (LL-v3.6 carry-forward item 1):** Before execution begins, Sprint Planning Engine should confirm sub-step 10a is present in execution_prompt.md (delivered by ST-07 in Sprint 1 of this release). If ST-07 patches execution_prompt.md, execution should use the updated version from Sprint 1 onwards.
2. **BLG-GOV-19 autonomous class (LL-v3.6 carry-forward item 2):** Sprint Execution Engine should flag BLG-GOV-19 class eligibility for any story with observable AC, per the qa_evidence_template.md patch (ST-08).

## Outstanding Advisory Items

| Item | Source | Status |
|------|--------|--------|
| Prompt change log gaps (execution_prompt.md v3.18→v3.22, sprint_planning_prompt.md v3.0→v3.2, backlog_management_prompt.md v1.6→v1.7) | STEP -1.7 advisory | ST-07 includes retroactive entries — resolves at ST-07 delivery |
| scored_initiatives.md staleness (OA-RP-05) | LL-v3.6 carry-forward item 3 | ST-11 in scope — resolves at ST-11 delivery |
| BLG-FE-27 (nav bar redesign, 3+ cycles without story) | Backlog age advisory | Not in scope — Provisional-Target: Arc 3/4 |

## Design Gate Status

Not started. Design gate required before sprint planning seals. Scope for design gate:
- EPIC-01: BLG-FE-33 signals page (Add to Watchlist UX) + BLG-FE-34 trade plan form (Signal Context panel)
- EPIC-02: PT-04 quality score display location (trade plan detail + research view)

Run: `run design-gate --cycle 2026-05-18__release-v3.7`
