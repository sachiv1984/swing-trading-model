**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.5
**Cycle:** 2026-05-30__release-v4.5
**Published:** 2026-05-30

---

# Release Plan — v4.5 Governance Prompt Hardening, Audit Debt & SI-02 Spec Pre-Planning

---

## Readiness

**Prior cycle:** 2026-05-29__release-v4.4 — Closed (Verified, Closed_with_actions, completed_cycle_count=30)
**Post-ship complete:** true | **Next cycle unblocked:** true
**Audit status:** AUD-2026-05-30 (2026-05-30) — Overall 74 (▼4 from prior); Tier 1 patches applied in audit commit (AUD-001/002/004/006); Tier 2 open: AUD-003 (BLG-GOV-70, stale — must enter v4.5), AUD-005 (agent headers)
**Outstanding actions from v4.4:** 4 (all execution_prompt.md patches — OA-01–04, all targeting v4.5)

**Readiness advisories:**
- ⚠ Advisory: BLG-GOV-70 (AUD-003) has been deferred 2+ cycles. Per audit, this must enter v4.5 sprint. Included in S2-01. ✓
- ℹ 4 items carry `Provisional-Target: v4.5` (BLG-GOV-70/75/76/77). All in scope. ✓
- ℹ 2 carry-forward items from v4.4 lessons_learnt_closure.md both addressed by S2-01 scope. ✓
- ℹ Design dependency scan: 0 items flagged.
- ℹ No v4.5 initiatives in scored_initiatives.md — using STEP 4 estimates.

---

## Scope

### S2-01 — OA Resolution: Execution Prompt Hardening
**Source:** v4.4 closure_record.md OA-01–04; AUD-2026-05-30-003 (BLG-GOV-70 stale)
**Items:** BLG-GOV-70, BLG-GOV-75, BLG-GOV-76, BLG-GOV-77
**Owner:** Head of Specs Team
**Rationale:** All 4 items are execution_prompt.md governance patches required before v4.5 sprint execution; v4.4 OA resolution is a hard expectation; BLG-GOV-70 is stale per audit and must enter.

### S2-02 — Governance Infrastructure: Agent Header Standardization
**Source:** AUD-2026-05-30-005
**Items:** 5 agent files (api_contracts_documentation_owner.md, backend_engineering_patterns_owner.md, data_model_domain_schema_owner.md, frontend_specs_ux_documentation_owner.md, metrics_definitions_analytics_owner.md)
**Owner:** Head of Specs Team
**Rationale:** Audit Tier 2 — standardizes 5 non-compliant agent `**Role:**` headers; enables automated compliance scanning; document_hygiene score +15.

### S2-03 — SI-02 Spec Pre-Sprint Completion (Conditional)
**Source:** BLG-GOV-39, BLG-SPEC-41, BLG-SPEC-37
**Gate condition:** Product Owner confirms SI-02 sprint planning is imminent before Sprint 2 seals.
**Owner:** Head of Specs Team + Metrics Definitions & Analytics Canonical Owner + Data Model & Domain Schema Owner
**Rationale:** v4.4 completed all SI-02 pre-design work (BLG-BE-17/18/20/23, BLG-FE-52/53, BLG-QA-31). The remaining gap before SI-02 sprint planning can seal is: §13 boundary review, drift score metric definition, and data schema pre-definition. These are Sprint 2 items conditional on PO gate confirmation.

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-62 — SI-04 §13 pre-assessment | SI-04 sprint planning not yet imminent | TBD |
| BLG-SPEC-35 — PO-02 §13 boundary review | Arc 4 PO-02 not in active planning window | TBD |
| BLG-GOV-32 — Gate-condition clearing tracker | Release planning prompt modification; scope v4.6+ | v4.6 |
| BLG-GOV-30/31/55 | Already resolved per prompt_change_log.md (grooming outstanding) | Archive |

**Note on BLG-GOV-30/31/55:** These appear as open in backlog.md but were resolved:
- BLG-GOV-30: resolved 2026-05-22 (shared_standards.md §16.11 + sprint_planning_prompt.md §7)
- BLG-GOV-31: resolved 2026-05-22 (sprint_planning_prompt.md v3.6 §1.4)
- BLG-GOV-55: resolved per CLAUDE.md §2 ("same sprint" API contract rule already present)
These should be archived by the next `groom backlog` run.

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Specs Team | RISK-01 | Sprint 1; before sprint planning seal |
| EPIC-02 | S2-02 | Head of Specs Team | RISK-02 | Sprint 1; parallel to EPIC-01 |
| EPIC-03 | S2-03 | HoST + Metrics + Data Model owners | RISK-03 | Sprint 2; gate-conditional |

**EPIC-01 notes:** All 4 stories modify execution_prompt.md and require CLAUDE.md §6 governance file edit checklist (version bumps, OPERATIONAL_GUIDE.md §14 update, prompt_change_log.md entry). Apply in a single EPIC commit to minimize version bump overhead. EPIC-01 must complete before v4.5 sprint planning seals (OA deadline).

**EPIC-02 notes:** 5 agent files; one story. No version bumps required (agent files are role documents, not Class 6 governance prompts). Fast autonomous delivery.

**EPIC-03 notes:** Conditional on PO gate. Stories are document-creation deliverables (delegated_decision or delegated review). EPIC-03 does not block EPIC-01/02 completion or publication.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | 4 execution_prompt.md patches require coordinated version bumps; if applied in wrong order or to wrong branch, OPERATIONAL_GUIDE §14 may become inconsistent | Medium | Group all 4 as stories in single EPIC; apply §6 checklist per story; OPERATIONAL_GUIDE §14 updated once in final commit | null |
| RISK-02 | EPIC-02 | Agent file header standardization is cosmetic — low risk but 5 files to edit simultaneously | Low | Single story, single commit, reviewed against preflight_common.md §2 role check | null |
| RISK-03 | EPIC-03 | SI-02 sprint planning gate (20+ closed trades) may not be met; SPEC-37/41/GOV-39 pre-work would be premature | Medium | EPIC-03 conditional on explicit PO confirmation; if gate not met, sprint Sprint 2 is empty and cycle closes with 6 stories | null |

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result | Notes |
|-------|--------|-------|
| All S2 IDs map to EPICs | PASS | S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03 |
| All EPICs declare Maps to | PASS | See EPIC table above |
| All RISK IDs referenced in EPIC table appear in Risk Register | PASS | RISK-01/02/03 all present |
| No orphaned references | PASS | No free-text epics; all IDs stable |
| Conditional EPIC declared as conditional | PASS | EPIC-03 gate condition documented |

---

## Capacity Check

**Capacity assumptions:** solo-dev evenings (standard)
**Timebox:** 2 sprints

| EPIC | Stories | Effort estimate | Source |
|------|---------|-----------------|--------|
| EPIC-01 | 4 | 4 × XS (~0.5 hr each) = ~2 hrs | STEP 4 inline |
| EPIC-02 | 1 | 1 × S (~1 day) = ~8 hrs | STEP 4 inline |
| EPIC-03 | 3 (conditional) | 3 × S-M (~1–2 days each) = ~12–20 hrs | STEP 4 inline |

**Sprint 1 firm:** ~10 hrs (EPIC-01 + EPIC-02) — within standard solo-dev sprint capacity.
**Sprint 2 conditional:** ~12–20 hrs — within solo-dev sprint capacity if gate is met.

**Capacity verdict:** WARN — total estimated 22–30 hrs across 2 sprints. Sprint 1 is well within capacity. Sprint 2 is conditional; if gate is not met, Sprint 2 has no firm stories and cycle closes with 5 stories (Sprint 1 only).

### Phasing Recommendation

- **Sprint 1:** EPIC-01 (4 stories, ~2 hrs) + EPIC-02 (1 story, ~8 hrs) = ~10 hrs — within capacity
- **Sprint 2:** EPIC-03 (3 conditional stories, ~12–20 hrs) — conditional on SI-02 gate; deferred if not met

Sprint 1 must complete EPIC-01 before sprint planning seals (OA requirement). Sprint 2 ordered after Sprint 1 by design; no blocking dependency between EPIC-01 and EPIC-02.
