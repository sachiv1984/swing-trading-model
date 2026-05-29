**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-05-29__release-v4.3
**Release:** v4.3
**Published:** 2026-05-29

---

# Release Plan — v4.3 Governance Consolidation, QA Debt Clearance & Ops Hardening

---

## Readiness

**Release preconditions:**
- Prior cycle (v4.2) closed: ✅ Closed_with_actions (2026-05-29)
- Post-ship complete: ✅ true
- Backlog groomed: ✅ 102 active items post-v4.2 groom (2026-05-29)
- Roadmap current: ✅ v4.3 section added under PO authority (2026-05-29)

**Backlog age advisory:** 8 items carry overdue Provisional-Target signals (v4.1 or v4.2). All are now absorbed into v4.3 scope. Recommendation actioned — no further advisory.

**Provisional-Target advisory:** Items with Provisional-Target: v4.3 — 1 direct match (BLG-OPS-42). Additional v4.1/v4.2 overdue items included in scope per backlog age review.

**Design dependency scan:** 0 items flagged. No UX/design decisions required. Design Gate: NOT_REQUIRED.

**Gate-conditional items excluded from scope:** SI-02 pre-planning cluster (7 items gated on <20 closed trades); BLG-GOV-67 SI-05 Phase 1 (gate clears 2026-06-21 — deferred to v4.4).

```yaml
# state.json update:
artifacts.stage1_readiness: pass
```

---

## Scope

### Items in Scope

| S2-ID | Description | Source items | Priority |
|-------|-------------|-------------|---------|
| S2-01 | Governance Prompt Patches (v4.2 OA resolution) | OA-1/2/3 from v4.2 closure record | P1 |
| S2-02 | Governance Hardening | BLG-GOV-42, BLG-GOV-47 | P1/P2 |
| S2-03 | QA Debt Clearance | BLG-QA-28/29/30/32/33/35/36/38 | P2 |
| S2-04 | Operations & Security Hardening | BLG-OPS-33, BLG-OPS-42, BLG-GOV-36, BLG-GOV-50 | P2 |
| S2-05 | Frontend Polish & Arc 5 Feature | BLG-FE-50, BLG-FE-51, BLG-FE-38 | P2 |

### Items Explicitly Deferred

| Item | Reason |
|------|--------|
| BLG-SPEC-37, BLG-SPEC-41, BLG-BE-17, BLG-BE-23, BLG-FE-52, BLG-FE-53, BLG-GOV-39 | SI-02 pre-planning cluster — gated: <20 closed trades (PO confirmed); SI-02 sprint planning not imminent |
| BLG-GOV-67 (SI-05 Phase 1) | Gate: SI-01+SI-03 live ≥30 days — clears 2026-06-21; deferred to v4.4 |
| BLG-GOV-33, BLG-GOV-34 | Arc 4 data density assessments — advisory; lower urgency than sprint items; deferred |
| BLG-QA-31 | SI-02 Playwright pre-design — gate: SI-02 sprint planning imminent |
| BLG-FE-25 (PT-04) | Gate: ≥20 closed trades — not met |

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02 | Head of Specs Team | RISK-01 | First — OA items are sprint-seal prerequisites |
| EPIC-02 | S2-03 | Director of Quality; QA Lead | RISK-02 | After EPIC-01 (QA coverage matrix references governance patches) |
| EPIC-03 | S2-04 | Infrastructure & Operations Owner; Cybersecurity & Trust Lead | RISK-03 | Parallel to EPIC-02 |
| EPIC-04 | S2-05 | Frontend Engineer; Financial Reporting & Records Owner | RISK-04 | Parallel to EPIC-02 |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Carry-forward OA items must complete before v4.3 sprint seal; if deferred again they become 2nd-recurrence escalations | Medium | All 3 OA items are stories ST-01/02/03 in EPIC-01; prioritised first in Sprint 1 | null |
| RISK-02 | EPIC-02 | Staging verifications (ST-06/07/08) require live staging environment with valid env vars; if staging is not configured, these are blocked | Medium | Items were deferred from v4.0/v4.1 because staging env was not configured; BLG-OPS-33 (ST-13) in EPIC-03 confirms parity first; staging-only ACs designated at sprint planning | null |
| RISK-03 | EPIC-03 | BLG-OPS-33 (staging parity audit) must run before ST-06/07/08 staging verifications to confirm env parity | Low | EPIC-03 sequenced to Sprint 2; BLG-OPS-33 to be first story in Sprint 2 | null |
| RISK-04 | EPIC-04 | ST-18 (Arc 5 compliance in monthly P&L) is a code change requiring Playwright coverage or staging sign-off per CLAUDE.md §2 | Low | Observable AC — Playwright test or staging sign-off required; designated as staging-only AC at sprint planning if Playwright not feasible in-sprint | null |

### Sprint Phasing Recommendation (WARN advisory)

See §Capacity Check below.

- **Sprint 1:** EPIC-01 (5 stories) + EPIC-04 (3 stories) = 8 stories — governance hardening + frontend
- **Sprint 2:** EPIC-02 (7 stories) + EPIC-03 (3 stories) = 10 stories — QA debt + operations

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result | Notes |
|-------|--------|-------|
| All S2-IDs map to EPICs | ✅ PASS | S2-01/02 → EPIC-01; S2-03 → EPIC-02; S2-04 → EPIC-03; S2-05 → EPIC-04 |
| All RISK-IDs in EPIC table appear in Risk Register | ✅ PASS | RISK-01/02/03/04 all present |
| No orphaned references | ✅ PASS | All scope items trace to EPIC; all risks trace to EPIC |
| Sequencing consistency | ✅ PASS | EPIC-01 first; EPIC-02/03 after; EPIC-04 parallel to EPIC-02 |

```yaml
# state.json update:
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
status: Planning
```

---

## Capacity Check

**Effort estimates (no scored_initiatives.md matches — inline estimates):**

| EPIC | Stories | Effort (mid-point) |
|------|---------|-------------------|
| EPIC-01 | 5 | 4 hrs (3 × XS + 2 × S) |
| EPIC-02 | 7 | 8 hrs (3 × XS + 2 × S + 2 × M) |
| EPIC-03 | 3 | 4 hrs (1 × XS + 1 × S + 1 × M) |
| EPIC-04 | 3 | 4 hrs (1 × XS + 1 × S + 1 × M) |
| **Total** | **18** | **~20 hrs** |

**Available capacity:** solo-dev evenings, 2 sprints ≈ 20–24 hrs total.

**Outcome:** ⚠ WARN — total estimated effort (20 hrs) is at the upper bound of available capacity. Not infeasible over 2 sprints but leaves minimal buffer.

### Phasing Recommendation

- **Sprint 1:** EPIC-01 (4 hrs) + EPIC-04 (4 hrs) = ~8 hrs — within capacity
- **Sprint 2:** EPIC-02 (8 hrs) + EPIC-03 (4 hrs) = ~12 hrs — tight; staging verifications (ST-06/07/08) are human-delegate tasks with minimal code effort

Ordering rationale: EPIC-01 (governance OA resolution) must land first — it contains sprint-seal prerequisites. EPIC-04 (frontend) is lightweight and pairs well with governance in Sprint 1. EPIC-02 (QA) and EPIC-03 (ops) are data-gathering/verification tasks suitable for Sprint 2.

```yaml
# state.json update:
artifacts.stage4_5_capacity_check: warn
attributes.capacity_feasible: warn
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**5.5 Cross-Stage Integrity:**

| Check | Result |
|-------|--------|
| All S2 IDs map to EPICs | ✅ S2-01/02→EPIC-01; S2-03→EPIC-02; S2-04→EPIC-03; S2-05→EPIC-04 |
| All EPIC IDs in backlog slice match stage3 | ✅ EPIC-01/02/03/04 all present |
| All RISK IDs in EPIC table appear in Risk Register | ✅ RISK-01/02/03/04 all present |
| No orphaned references | ✅ |

**5.7 Decision Record Integrity:** No escalations raised; decisions record contains only sequencing decisions. ✅ Pass.

```yaml
# state.json update:
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: pass
attributes.cross_stage_integrity: pass
attributes.decisions_validated: pass
```
