**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-03__release-v5.0
**Release:** v5.0
**Published:** 2026-06-03

---

# Release Plan — v5.0: Governance Hardening, Product Correctness & SI-05 Pre-work

## Readiness

**Status:** PASS (advisory items noted in run_manifest.md)
**Prior cycle:** 2026-06-02__release-v4.9 — Closed_with_actions; post_ship_complete=true
**Capacity assumption:** Double capacity (user-specified)
**Mode:** Standard

Design dependency scan: 1 item (BLG-FE-60 PO channel decision — deliverable within sprint, not pre-sprint blocker). Design gate: **not required** (no new UX requiring design sign-off pre-sprint).

Gate proximity: BLG-GOV-67 gate clears 2026-06-21 (18 days). All other gates ≥ 2027.

---

## Scope

**Items in scope:**

| S2-ID | Items | Theme |
|-------|-------|-------|
| S2-01 | BLG-GOV-79, BLG-GOV-81, BLG-GOV-83 | Governance document patches |
| S2-02 | BLG-GOV-80, BLG-GOV-82 | Governance engine structural fixes |
| S2-03 | BLG-FEAT-43, BLG-BE-25, BLG-OPS-52 | Product correctness & ops |
| S2-04 | BLG-FE-60, BLG-GOV-86, BLG-GOV-87, BLG-GOV-88, BLG-BE-26 | SI-05 Phase 1 pre-work |
| S2-05 | BLG-GOV-67 | SI-05 Phase 1 implementation [CONDITIONAL: gate 2026-06-21] |

**Items deferred:** All other v5.0+ backlog items — gate conditions not met or not scheduled.

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing |
|---------|-------------|-------|----------|------------|
| EPIC-01 | S2-01 | Head of Specs Team | RISK-03 | First (no dependencies) |
| EPIC-02 | S2-02 | Head of Specs Team | RISK-01 | After EPIC-01 (prompt_change_log.md append order) |
| EPIC-03 | S2-03 | Head of Backend Engineering | — | After EPIC-02 |
| EPIC-04 | S2-04, S2-05 | Product Owner / Head of Specs Team | RISK-02 | After EPIC-03; ST-09 before ST-10 within EPIC |

**Merge order:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04
**Sprint structure:** Sprint 1 (firm: ST-01–ST-13) → Sprint 2 conditional (ST-14 if gate clears 2026-06-21)

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-02 | BLG-GOV-82 requires adding last_audit_cycle_count to .claude_current_state.json schema + lifecycle_schema.json; schema evolution risk | Medium | Backward-compatible nullable field; null handling defined in post_ship_closure.md patch | null |
| RISK-02 | EPIC-04 | BLG-GOV-67 gate (2026-06-21) may not clear if SI-01/SI-03 availability is disrupted | Low | Gate is date-based (30 days post 2026-05-22); both features have been live and stable; very low probability of disruption | null |
| RISK-03 | EPIC-01 | BLG-GOV-79: all 7 target entries appear already present in prompt_change_log.md (possibly added as Tier 1 during AUD-2026-06-02). Story scope may narrow to verification-only | Low | ST-01 verifies first; appends only if gaps confirmed; story size S accommodates both outcomes | null |

---

## Capacity Check

**Capacity assumption:** Double capacity — estimated 40–48 hrs available (vs standard ~20–24 hrs)

**Effort band lookup (scored_initiatives.md tier 1 — 5 items; tier 3 — 9 items):**

| EPIC | Stories | Effort | Hours (mid) | Source |
|------|---------|--------|-------------|--------|
| EPIC-01 | ST-01 (S), ST-02 (S), ST-03 (XS) | S+S+XS | 7 | Tier 3 inline |
| EPIC-02 | ST-04 (M), ST-05 (M) | M+M | 12 | Tier 3 inline |
| EPIC-03 | ST-06 (S), ST-07 (S), ST-08 (XS) | S+S+XS | 7 | Tier 3 inline |
| EPIC-04 firm | ST-09/10/11/12/13 (all S) | 5×S | 15 | 5 items: scored_initiatives.md S band |
| EPIC-04 cond | ST-14 (M) | M | 6 | Tier 3 inline |
| **Total firm** | **13 stories** | | **~41 hrs** | |
| **Total w/cond** | **14 stories** | | **~47 hrs** | |

**Result: PASS** — 41 hrs firm / 47 hrs with conditional; within double capacity (48 hrs). No phasing required.

### Phasing Recommendation
Not required — all firm stories fit comfortably in Sprint 1. Conditional ST-14 held for Sprint 2 pending gate confirmation on 2026-06-21.

---

## Integrity Validation

### 5.5 Cross-Stage Integrity

| Check | Result |
|-------|--------|
| All S2-IDs map to EPICs | PASS — S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04+S2-05→EPIC-04 |
| All EPIC IDs in backlog slice match stage3 | PASS — EPIC-01/02/03/04 consistent |
| All RISK-IDs in EPIC table appear in register | PASS — RISK-01/02/03 all in register |
| No orphaned references | PASS |

### 5.7 Decision Record Integrity

Decision record present at `docs/product/decisions/decisions--2026-06-03__release-v5.0.md`. No Accepted Risk escalations. All mandatory template fields populated. **PASS**
