Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Release: v3.6
Cycle: 2026-05-16__release-v3.6
Last Updated: 2026-05-16

---

# Cycle Summary — v3.6 Arc 4 Data Integrity + Arc 2 Quality Score + Debt Clearance

## Release Overview

| Field | Value |
|-------|-------|
| Release | v3.6 |
| Cycle ID | 2026-05-16__release-v3.6 |
| Theme | Arc 4 Data Integrity + Arc 2 Quality Score + Debt Clearance |
| Sprint count | 2 |
| Stories | 10 (ST-01 through ST-10) |
| EPICs | 4 (EPIC-01 through EPIC-04) |
| Mode | standard |
| Capacity outcome | WARN (within 2-sprint phased capacity) |

## Sprint Structure

| Sprint | EPICs | Key deliveries |
|--------|-------|---------------|
| Sprint 1 | EPIC-04, EPIC-03, EPIC-01 (partial) | Governance patches (ST-09/10); QA/spec/UX debt (ST-06/07/08); Arc 4 data capture backend (ST-01); PT-04 spec + gate confirmation (ST-03) |
| Sprint 2 | EPIC-01 (remainder), EPIC-02 (conditional) | PlanVsReality frontend update (ST-02); PT-04 backend + frontend (ST-04/05, if gate confirmed) |

## Scope Summary

| S2-ID | EPIC | Theme | Stories |
|-------|------|-------|---------|
| S2-01 | EPIC-01 | Arc 4 Data Capture (planned_entry_price + entry_delta_pct) | ST-01, ST-02 |
| S2-02 | EPIC-02 | PT-04 Setup Quality Score (gated) | ST-03, ST-04, ST-05 |
| S2-03 | EPIC-03 | QA, Spec & UX Debt (BLG-FE-32, TEST-GAP-EPIC-03-v33, BLG-SPEC-27, BLG-FE-26) | ST-06, ST-07, ST-08 |
| S2-04 | EPIC-04 | Governance patches (4× execution_prompt.md; 4× change log OAs) | ST-09, ST-10 |

## Key Risks

| RISK-ID | Description | Disposition |
|---------|-------------|-------------|
| RISK-01 | planned_entry_price migration must handle null for historical trades | Mitigated: nullable field + conditional display |
| RISK-02 | PT-04 gate (20+ closed trades) not yet confirmed | Conditional gate: PO confirms before sprint planning seals |
| RISK-03 | BLG-SPEC-27 may need openapi.yaml changes | Mitigated: scoped backend only; same-commit update required |

## Deferred Items

7 items explicitly deferred — see scope document. Primary: PO-02/03/04/05 gated by data accumulation (PO-02 needs 6+ months journal data; ~5 months remaining from v2.8 ship date 2026-04-20).

## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-02] PT-04 gate confirmation — Product Owner must confirm 20+ closed trades before sprint planning seals. If confirmed: EPIC-02 proceeds in Sprint 2. If not confirmed: EPIC-02 defers to v3.7. — Owner: Product Owner

## Design Gate Status

**Design gate required:** Yes

Frontend-visible changes in this release:
- ST-02: PlanVsReality component — entry_delta_pct display
- ST-05: Setup Quality Score badge + tooltip in Pre-Trade Research View (conditional on gate)
- ST-08: Research page UX fix (regime lozenge + font)

Sprint Planning may proceed with `--bypass` if Head of UX & Design + Product Owner provide bypass rationale for any specific story. For ST-07 (backend-only HTTP error codes) and ST-06 (test-only), no design gate work required.

## Advisory Outstanding Actions

| # | Action | Owner | Source |
|---|--------|-------|--------|
| OA-RP-01 | Add sprint_planning_prompt.md v3.0→v3.1 entry to prompt_change_log.md | Head of Specs Team | STEP -1.7 |
| OA-RP-02 | Add execution_prompt.md v3.18→v3.20 entries to prompt_change_log.md | Head of Specs Team | STEP -1.7 |
| OA-RP-03 | Add delivery_verification_prompt.md v2.1→v2.2 entry to prompt_change_log.md | Head of Specs Team | STEP -1.7 |
| OA-RP-04 | Add backlog_management_prompt.md v1.6→v1.7 entry to prompt_change_log.md | Head of Specs Team | STEP -1.7 |
| OA-RP-05 | scored_initiatives.md refresh: add Arc 3/4 entries (IT-06, PO-01, PT-04); update Effort Band column | Facilitator / PMO Lead | LL v3.5 OA-1 + run manifest STEP 0 |

*OA-RP-01–04 are directly addressed by EPIC-04 ST-09 AC-04.*

## Merge Order

EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02

Rationale: Governance patches first (no shared-file conflicts); QA/spec/UX second; Arc 4 data model third; PT-04 last (most dependent and conditional).

## Publish Gate Summary

| Condition | Status |
|-----------|--------|
| open_escalations empty | ✅ Pass |
| deferred_execution_blockers empty | ✅ Pass |
| stage4_5_capacity_check warn (standard mode allows) | ✅ Pass |
| stage5_5_cross_stage_integrity pass | ✅ Pass |
| stage5_7_decision_record_integrity pass | ✅ Pass |
| stage1_readiness pass | ✅ Pass |
| stage3_5_model_integrity pass | ✅ Pass |
| plan_structured, plan_executable, backlog_committed true | ✅ Pass |
| Scope document present | ✅ Pass |
| Decisions document present | ✅ Pass |
| locks released | ✅ Pass |

**Publish Gate: PASS** — status = Validated, publish_eligible = true
