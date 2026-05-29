**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-05-29__release-v4.4
**Release:** v4.4
**Published:** 2026-05-29

---

# Release Plan — v4.4

Governance Patches, SI-02 Pre-Planning Sprint & Ops Hardening

---

## Readiness

**Prior cycle:** 2026-05-29__release-v4.3 | Status: Closed_with_actions | post_ship_complete: true

**Lifecycle guard:** status = Closed → valid from-state for Release Planning ✅

**Carry-forward (STEP 0):** 2 items from 2026-05-29__release-v4.3 lessons_learnt_closure.md. Both resolved:
- BLG-GOV-71 in backlog → included in v4.4 EPIC-01 (ST-01) ✅
- BLG-GOV-72 in backlog → included in v4.4 EPIC-01 (ST-02) ✅

**Backlog age advisory:** BLG-BE-17/18 in backlog since 2026-05-22__scheduled (4 cycles). Both gated items awaiting "SI-02 sprint planning imminent" — gate now met. No process concern.

**Provisional-Target advisory:** 6 items carry Provisional-Target: v4.4 (BLG-GOV-69/71/72/73/74, BLG-OPS-43). 7 SI-02 items carry Provisional-Target: Unscheduled but explicitly listed in v4.4 roadmap entry. 13 candidates total.

**Design dependency scan:** 0 items flagged. Design gate NOT required for this release.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

| ID | Item | Source | Priority | Notes |
|----|------|--------|----------|-------|
| S2-01 | Governance Prompt Patches | BLG-GOV-69/71/72/73/74 + LL-v4.3-2 | P2/P3 | 5 stories; all XS; Head of Specs Team |
| S2-02 | SI-02 Backend Pre-Planning | BLG-BE-17/18/20/23 | P1/P2 | 4 stories; S-M; backend design documents |
| S2-03 | SI-02 Frontend & QA Pre-Planning | BLG-FE-52/53 + BLG-QA-31 | P1/P2 | 3 stories; S; FE/QA design documents |
| S2-04 | Ops Documentation Hardening | BLG-OPS-43 | P3 | 1 story; XS; OPERATIONAL_GUIDE §7 update |

**Items explicitly deferred:**
- BLG-GOV-70 — spec_references policy for documentation-creation stories (Provisional-Target: v4.5; not v4.4)
- All Arc 6 items — gate: 50-100+ trades with plans
- PT-04 Setup Quality Score — gate: 20+ closed trades (formally parked; PO decision 2026-05-19)
- SI-02 implementation (Behavioural Drift Detection) — pre-planning only in v4.4; full sprint after pre-planning artefacts complete
- BLG-GOV-67 — SI-05 early delivery — gate: SI-02 pre-planning complete (deferred pending v4.4 artefacts)

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Specs Team | RISK-01 | First (no dependencies) |
| EPIC-02 | S2-02 | Head of Backend Engineering + Head of Engineering | RISK-02 | After EPIC-01; ST-09 after ST-06+07+08 |
| EPIC-03 | S2-03 | Frontend Specs & UX Documentation Owner; QA & Testing Owner | RISK-03 | After EPIC-02 outputs (FE-53 after FE-52; QA-31 after BE-20) |
| EPIC-04 | S2-04 | Infrastructure & Operations Owner | RISK-04 | Independent; any sprint |

EPIC-01 note: ST-05 (release_planning_prompt.md STEP 7 patch) references v4.3 lessons_learnt.md LL-2 — no separate BLG item; tracked via lessons record.

EPIC-03 note: BLG-FE-53 depends on BLG-FE-52 output (component interface must be defined before interaction spec). BLG-QA-31 depends on BLG-BE-20 output (Playwright scenarios need architecture context).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Governance patches touching Class 6 prompts — risk of missed OPERATIONAL_GUIDE §14 sync or changelog entry | Low | Governance File Edit Checklist (CLAUDE.md §6) applied per story; each story's AC includes version bumps | null |
| RISK-02 | EPIC-02 | BLG-BE-20 + BLG-BE-23 have "sprint initiated" gate conditions — if pre-design outputs (BE-17/18) discover scope gaps, BE-20 architecture may be blocked mid-sprint | Medium | Sequence BE-20/BE-23 after BE-17/18/23 outputs; Product Owner to confirm gate interpretation at sprint planning | null |
| RISK-03 | EPIC-03 | FE-52 → FE-53 sequential dependency — FE-53 cannot proceed without FE-52 component interface output | Low | Sprint planning must enforce FE-52 before FE-53; both are S effort (~1 day each) | null |
| RISK-04 | EPIC-04 | Single-story EPIC — thin EPIC; merges quickly | Low | Merge EPIC-04 early to avoid end-of-sprint overhead; OPERATIONAL_GUIDE is Class 6 — governance edit checklist applies | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

**S2-ID coverage:**
- S2-01 → EPIC-01 ✅
- S2-02 → EPIC-02 ✅
- S2-03 → EPIC-03 ✅
- S2-04 → EPIC-04 ✅

**EPIC Maps-to completeness:**
- EPIC-01 → S2-01 ✅
- EPIC-02 → S2-02 ✅
- EPIC-03 → S2-03 ✅
- EPIC-04 → S2-04 ✅

**RISK coverage:**
- RISK-01 → EPIC-01 ✅
- RISK-02 → EPIC-02 ✅
- RISK-03 → EPIC-03 ✅
- RISK-04 → EPIC-04 ✅

**Orphaned references:** None detected.

**Gate conditions:** RISK-02 documents conditional items (BLG-BE-20, BLG-QA-31). These are noted as conditional in stage4_backlog_slice.md.

**Model executable:** Yes — all EPICs have owners, all stories are traceable to backlog items or tracked lessons actions, all dependencies documented.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort estimates per EPIC:**

| EPIC | Stories | Effort | Est. Hours | Notes |
|------|---------|--------|------------|-------|
| EPIC-01 | 5 | 5 × XS (~0.5 hr each) | ~2.5 hrs | Pure documentation edits to Class 6 prompts |
| EPIC-02 | 4 | 2 × M (~8–12 hrs) + 2 × S (~4–6 hrs) | ~24–32 hrs | Research/design documents; no code |
| EPIC-03 | 3 | 3 × S (~4–6 hrs each) | ~12–18 hrs | Research/design documents; no code |
| EPIC-04 | 1 | 1 × XS (~0.5 hr) | ~0.5 hrs | Single OPERATIONAL_GUIDE section addition |
| **Total** | **13** | | **~39–53 hrs** | |

**Available capacity:** Solo-dev part-time (evenings + weekends). Based on prior cycle patterns: ~20–30 hrs per sprint.

**Assessment: WARN — total effort (39–53 hrs mid-range ~46 hrs) exceeds a single sprint at part-time capacity.**

### Phasing Recommendation

Estimated total effort: ~39–53 hrs (mid-point ~46 hrs). Available capacity per sprint: ~20–30 hrs.

- **Sprint 1: EPIC-01 + EPIC-04** — ~3 hrs. All governance/ops patches. Fast, independent, high governance priority.
- **Sprint 2: EPIC-02 + EPIC-03** — ~36–50 hrs. SI-02 pre-planning (backend + frontend + QA). Sequencing: BE-17/18 first → BE-20/23 → FE-52 → FE-53 → QA-31.

Rationale: Governance patches are blocking for carry-forward resolution (BLG-GOV-71/72 must be applied before next sprint planning). SI-02 pre-planning items are independent of each other and can be parallelised (backend + frontend in same sprint). 

Note: If governance patches can be completed in a single day, Sprint 1 + Sprint 2 may collapse to a single short sprint. Sprint planning to assess. The phasing here provides a conservative two-sprint structure.

```yaml
artifacts.stage4_5_capacity_check: warn
attributes.capacity_feasible: warn
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**5.5 Cross-Stage Check:**

| Check | Result |
|-------|--------|
| All S2 IDs mapped to EPICs | PASS — S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04→EPIC-04 |
| All EPIC IDs in backlog slice match EPIC IDs in stage3 | PASS — verified in stage4_backlog_slice.md |
| All RISK IDs in EPIC table appear in Risk Register | PASS — RISK-01 through RISK-04 all present |
| No orphaned references | PASS |
| decisions--2026-05-29__release-v4.4.md present | PASS — created at STEP 3 |
| All mandatory template fields populated in decisions record | PASS |

**5.7 Decision Record Integrity:**
- decisions--2026-05-29__release-v4.4.md: present ✅
- No escalations were raised → no AR/SRB records to verify
- Mandatory template fields: Release, Cycle, Last Updated, scope decisions, sequencing decisions, accepted risks (None) — all populated ✅

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: pass
attributes.cross_stage_integrity: pass
attributes.decisions_validated: pass
```
