Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v4.1
Cycle: 2026-05-26__release-v4.1
Last Updated: 2026-05-26

---

# Release Plan — v4.1 — Governance Hardening, Spec Debt, Arc 5 Compliance + SI-02 Pre-Planning

---

## Readiness

**Release:** v4.1
**Prior cycle status:** Closed (post_ship_complete: true, next_cycle_unblocked: true)
**Completed cycle count:** 26
**Audit:** AUD-2026-05-21 (overall: 79 — passing threshold)
**Last rebalance:** 2026-05-25__scheduled (DL-034)
**Design gate required:** No — no new UX patterns; scope is governance/spec/minor features

### Carry-Forward Items (from v4.0 post-ship closure)

| OA # | Action | Escalation Level | Target |
|------|--------|-----------------|--------|
| OA-01 | execution_prompt.md: merge-gate hard gate (2nd recurrence — failure = systemic process failure) | CLAUDE.md §2 mandate risk if missed | v4.1 |
| OA-02 | sprint_planning_prompt.md + sprint_backlog.md: staging-only AC designation (2nd recurrence — failure = CLAUDE.md §2 mandated rule) | CLAUDE.md §2 mandate risk if missed | v4.1 |
| OA-03 | sprint_close_reminder.yml: confirm fires after each EPIC merge; investigate v4.0 delay | PMO Lead action, monitoring | v4.1 kickoff |
| OA-04 | delivery_verification_prompt.md STEP 5.0A: pr_number null guard | Head of Specs Team, monitoring | v4.1 |

OA-01 and OA-02 are 2nd recurrence escalations — must be actioned as stories in this release.
OA-03 is PMO Lead action (investigation/confirmation), addressed as a task in ST-01's EPIC.
OA-04 is first occurrence, addressed as ST-03.

### Backlog Age Advisory (STEP 1.1)

⚠ Advisory: 2 spec/documentation debt items aged 2+ cycles without story assignment:
- BLG-SPEC-33 (SI-03 Red Flag Journal API contract) — Provisional-Target v4.0, missed v4.0 (OA from rebalance); promoted to story ST-04 in this release
- BLG-SPEC-34 (SI-01 Pre-Entry Validation API contract) — Provisional-Target v4.0, missed v4.0; promoted to story ST-05 in this release

Both items promoted to sprint stories in v4.1 scope — advisory resolved.

### Provisional-Target Advisory (STEP 1.2)

22 backlog items carry `Provisional-Target: v4.1` signal. 15 are included in scope (see §Scope). 7 are deferred:
- BLG-GOV-40, GOV-42, GOV-43, GOV-47, GOV-48, GOV-50, GOV-52, GOV-53 — lower priority; not blocking execution
- BLG-FE-45, FE-46, FE-47, FE-49 — FE work not required for v4.1 delivery
- BLG-FEAT-40 Provisional-Target is "Unscheduled" but included in ST-08 as precondition for BLG-FEAT-42

### Design Dependency Scan (STEP 1.3)

Design dependency scan: 0 items flagged. No "Product Owner to decide" or design-gate language found in v4.1 scope candidates.

---

## Scope

### S2 Scope Items

| S2-ID | EPIC | Description | Backlog refs |
|-------|------|-------------|-------------|
| S2-01 | EPIC-01 | Governance Prompt Hardening — patch execution_prompt (merge-gate), sprint_planning_prompt (staging-only AC), delivery_verification_prompt (pr_number null guard) | OA-01, OA-02, OA-04 |
| S2-02 | EPIC-02 | API Contract Spec Debt Batch 1 — formal API contract docs for SI-03 Red Flag Journal, SI-01 Pre-Entry Validation, Arc 5 analytics endpoint | BLG-SPEC-33, SPEC-34, SPEC-40 |
| S2-03 | EPIC-03 | Gemini Thesis API Contract — formal contract for POST /trade-plans/{plan_id}/generate-thesis (gate: S2-02 SI-03 contract closed) | BLG-SPEC-38 |
| S2-04 | EPIC-03 | Arc 5 P&L Compliance Integration — composite score formula definition + monthly P&L compliance metrics section | BLG-FEAT-40, BLG-FEAT-42 |
| S2-05 | EPIC-03 | Gemini Cost Alerting — daily Telegram alert when Gemini API spend exceeds configurable threshold | BLG-OPS-34 |
| S2-06 | EPIC-03 | Frontend: Research View signal_type column + Arc5ComplianceSection frontend spec | BLG-FE-44, BLG-FE-48 |
| S2-07 | EPIC-03 | Staging Verification Bundle — deferred staging-only ACs from v4.0 (Arc5ComplianceSection E2E, Gemini staging, ticker validation staging, CI/CD deploy hook) | BLG-QA-28, QA-29, QA-30, BLG-OPS-28 |
| S2-08 | EPIC-04 | SI-02 Pre-Planning — data model gap analysis, §13 evidence criteria pre-definition, data prerequisite audit, DB query performance assessment | BLG-SPEC-39, GOV-44, GOV-46, GOV-51 |
| S2-09 | EPIC-04 | Security + Governance Patches — Gemini API key scope minimization review, STEP 12.1 artefact presence check | BLG-GOV-49, GOV-56 |
| S2-10 | EPIC-04 | SI-05 Phase 1 Roadmap Annotation — formal scope annotation for SI-05 Phase 1 (Red Flag + compliance trend) | BLG-GOV-54 |
| S2-11 | EPIC-04 | Operational Reviews — api perf baseline update (v4.0 new endpoints), Gemini usage first monthly review, P&L attribution gate check | BLG-OPS-29, OPS-30, OPS-32 |

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| PT-04 (Arc 2 performance analytics) | Gate not met: 20+ closed trades required; current trade count insufficient | v4.x (gate-conditional) |
| Arc 6 (PS-01 through PS-05) | Gate not met: 50–100+ trades required | Arc 6 horizon |
| BLG-OPS-33 (staging parity audit) | Gate: v4.1 sprint planning complete | v4.2 or post-v4.1 |
| BLG-GOV-40/42/43/47/48/50/52/53 | Lower priority; capacity constrained; no blocking dependency | v4.x backlog |
| BLG-FE-45/46/47/49 | UX/FE items not required for v4.1 objectives | v4.x backlog |

---

## Execution Plan

### EPIC Table

| EPIC-ID | Sprint | Scope items | Owner | Key risk | Sequencing constraint |
|---------|--------|-------------|-------|----------|-----------------------|
| EPIC-01 | 1 | S2-01 | Head of Specs Team | RISK-01 | First — 2nd recurrence escalations must not slip |
| EPIC-02 | 1 | S2-02 | API Contracts Documentation Owner | RISK-02 | Concurrent with EPIC-01; EPIC-03 ST-07 gates on EPIC-02 |
| EPIC-03 | 2 | S2-03, S2-04, S2-05, S2-06, S2-07 | Head of Engineering + QA Lead | RISK-03 | After EPIC-02 (ST-07 gates on BLG-SPEC-33); EPIC-04 independent |
| EPIC-04 | 2 | S2-08, S2-09, S2-10, S2-11 | Strategy Rules Owner + Ops Owner | RISK-04 | After Sprint 1 complete; independent from EPIC-03 |

**EPIC-02 note:** BLG-SPEC-33 (SI-03 Red Flag Journal contract) must be closed before ST-07 (BLG-SPEC-38, Gemini thesis contract) commences. ST-07 is in EPIC-03 Sprint 2, so the gate is naturally satisfied by sprint ordering.

**EPIC-04 note:** SI-02 pre-planning work (S2-08) is input to SI-02 sprint planning in a future cycle — no deployment required; all artefacts are documents/reviews.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | OA-01/OA-02 are 2nd recurrence — if missed again, CLAUDE.md §2 mandate required. Prompt changes involve careful read-before-write of governed prompts. | High | Assign to Head of Specs Team; treat as hard gate in sprint planning seal | null |
| RISK-02 | EPIC-02 | BLG-SPEC-33/34 are overdue by 1 cycle; missing contracts block downstream features and compliance. | Medium | Include as Sprint 1 stories; block EPIC-03 ST-07 on EPIC-02 completion | null |
| RISK-03 | EPIC-03 | BLG-OPS-34 (Gemini cost alerting) and BLG-FEAT-42 (P&L integration) are both M effort items in Sprint 2; combined with staging bundle may be capacity-tight. | Medium | Staging bundle (ST-11) is low-risk verification work; can parallelize with EPIC-04 if needed | null |
| RISK-04 | EPIC-04 | SI-02 pre-planning artefacts must be complete before SI-02 sprint planning opens. Pre-work is all documentation — no deployment risk. | Low | All S2-08 items are document/review outputs; low implementation risk | null |

---

## Integrity Validation — 3.5 Local Model Integrity

### S2 → EPIC Mapping Check

| S2-ID | Declared EPIC | EPIC exists? | Status |
|-------|---------------|-------------|--------|
| S2-01 | EPIC-01 | Yes | ✅ |
| S2-02 | EPIC-02 | Yes | ✅ |
| S2-03 | EPIC-03 | Yes | ✅ |
| S2-04 | EPIC-03 | Yes | ✅ |
| S2-05 | EPIC-03 | Yes | ✅ |
| S2-06 | EPIC-03 | Yes | ✅ |
| S2-07 | EPIC-03 | Yes | ✅ |
| S2-08 | EPIC-04 | Yes | ✅ |
| S2-09 | EPIC-04 | Yes | ✅ |
| S2-10 | EPIC-04 | Yes | ✅ |
| S2-11 | EPIC-04 | Yes | ✅ |

### RISK → EPIC Back-Link Check

All 4 RISK-IDs (RISK-01 through RISK-04) reference valid EPIC-IDs in the EPIC table. ✅

### Design Gate Language

No design-gate language detected in scope items. Design gate: NOT required. ✅

**Integrity result: PASS** — all S2 IDs map to valid EPICs; all RISK IDs declared in EPIC table appear in Risk Register; no orphaned references.

---

## Capacity Check

**Estimation method:** inline estimate (no matching scored_initiatives.md effort band rows for v4.1 items)

### Effort Estimates by Sprint

| Sprint | EPIC | Stories | Estimated effort |
|--------|------|---------|-----------------|
| Sprint 1 | EPIC-01 | ST-01, ST-02, ST-03 | ~3 days (3 × S) |
| Sprint 1 | EPIC-02 | ST-04, ST-05, ST-06 | ~3 days (3 × S) |
| Sprint 1 total | | 6 stories | ~6 days |
| Sprint 2 | EPIC-03 | ST-07 (S), ST-08 (M+S), ST-09 (M), ST-10 (XS+S), ST-11 (XS×4) | ~10 days |
| Sprint 2 | EPIC-04 | ST-12 (M), ST-13 (S×3), ST-14 (S×3), ST-15 (S×3) | ~7 days |
| Sprint 2 total | | 9 stories | ~17 days |
| **Grand total** | | **15 stories** | **~23 days** |

**Available capacity (solo developer, evenings/weekends):** ~8–10 days per sprint (conservative)

**Outcome: WARN** — Sprint 2 estimated effort (~17 days) exceeds typical solo-developer sprint capacity. Sprint 1 (~6 days) is within capacity.

### Phasing Recommendation

**Estimated total:** ~23 days mid-point. Available: ~16–20 days across 2 sprints.

| Phase | Sprint | EPICs | Estimated effort | Note |
|-------|--------|-------|-----------------|------|
| Phase 1 | Sprint 1 | EPIC-01, EPIC-02 | ~6 days | Within capacity; must-do OA items + spec debt batch 1 |
| Phase 2 | Sprint 2 | EPIC-03, EPIC-04 | ~17 days | Exceeds single-sprint capacity; see ordering rationale |

**Sprint 2 ordering rationale:** EPIC-04 (S2-08 through S2-11) is entirely documentation/review work — lower risk and potentially parallelizable with EPIC-03 implementation. Recommended order within Sprint 2: EPIC-04 first (reviews/docs can run alongside EPIC-03 implementation), then EPIC-03 implementation stories (ST-07 → ST-08 → ST-09 → ST-10 → ST-11). If capacity is constrained, ST-11 (staging bundle — verifications only) and ST-10 (FE-44 is XS) can slip to v4.2 with no functional regression.

Sprint planning should confirm capacity and optionally defer ST-09 (BLG-OPS-34, M effort) or ST-11 to v4.2 if needed.

---

## Cross-Stage Integrity (STEP 5.5)

### Cross-Stage Checks

| Check | Status |
|-------|--------|
| All S2-IDs appear in backlog slice EPIC mapping | ✅ Verified |
| All EPIC-IDs in backlog slice match EPIC table (EPIC-01 through EPIC-04) | ✅ Verified |
| All RISK-IDs in EPIC table appear in Risk Register | ✅ Verified |
| No orphaned backlog slice references | ✅ Verified |
| decisions--2026-05-26__release-v4.1.md present | ✅ Created at STEP 3 |
| All mandatory template fields populated | ✅ Verified |
| deferred_execution_blockers empty | ✅ None |
| open_escalations empty | ✅ None |

**Cross-stage integrity result: PASS**
**Decision record integrity: PASS**

---

## Publish Gate

| Condition | Status |
|-----------|--------|
| open_escalations empty | ✅ |
| deferred_execution_blockers empty | ✅ |
| stage4_5_capacity_check = warn (allowed in standard mode) | ✅ |
| stage5_5_cross_stage_integrity = pass | ✅ |
| stage5_7_decision_record_integrity = pass | ✅ |
| stage1_readiness = pass | ✅ |
| stage3_5_model_integrity = pass | ✅ |
| plan_structured = true | ✅ |
| plan_executable = true | ✅ |
| backlog_committed = true | ✅ |
| scope document present | ✅ |
| decisions record present | ✅ |
| backlog_lock.status = released | ✅ |

**Publish gate: PASS — status = Validated, publish_eligible = true**
