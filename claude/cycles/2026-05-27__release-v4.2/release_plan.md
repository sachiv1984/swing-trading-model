**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-27__release-v4.2

---

# Release Plan — v4.2

## Readiness

### Preconditions
- Prior cycle 2026-05-26__release-v4.1: status = Closed ✅
- post_ship_complete = true ✅
- next_cycle_unblocked = true ✅
- Backlog lock: not held ✅

### Advisory — BLG-GOV-58 Resolved Before Planning
BLG-GOV-58 (execution_prompt.md STEP 5.2 returned_to_backlog clarification) was formally listed as Provisional-Target v4.2 (OA-2 v4.1). This item's ACs were met by AUD-2026-05-27-003 / execution_prompt.md v3.29 on 2026-05-27 — prior to this release planning run. BLG-GOV-58 should be marked COMPLETE in backlog at next groom backlog run. No v4.2 story required.

### 1.1 Backlog Age Advisory
0 spec/documentation debt items in v4.2 candidate scope have been in the backlog 2+ cycles without story assignment. All candidate items were created 2026-05-27__scheduled (DL-035) or are OA carry-forwards from v4.1 (OA-3: BLG-OPS-35). No advisory warning.

### 1.2 Provisional-Target Advisory
ℹ 11 items carry `Provisional-Target: v4.2` (GOV-57/59/61/63/64/65/66, OPS-35/36/38/39, SPEC-42). 3 additional items included with non-v4.2 or unscheduled targets: BLG-GOV-60 (Before SI-02 sprint planning seals), BLG-QA-37 (P1, direct), BLG-BE-22 (P2, direct). Scope authority at STEP 2.

### 1.3 Design-Gate Language Scan
Design dependency scan: 0 items flagged. All v4.2 scope items are governance, operations, spec, or backend assessment type — no UX design decisions required.

---

## Scope

### S2 Scope Items

| S2-ID | Item | Type | Priority | Effort | Backlog IDs |
|-------|------|------|----------|--------|-------------|
| S2-01 | Claude API Compliance & Security | Governance / Security | P1–P2 | S–XS (×4) | BLG-GOV-64/65/66, BLG-OPS-38 |
| S2-02 | Operational Monitoring & Baselines | Operations | P1–P3 | S (×3) | BLG-OPS-35/36/39 |
| S2-03 | Claude API Implementation & Spec Debt | Backend / Spec / QA | P1–P2 | M+S+S+S | BLG-GOV-63, BLG-SPEC-42, BLG-QA-37, BLG-BE-22 |
| S2-04 | Governance Preparation & Pre-Planning | Governance | P1–P3 | S+S+S+XS | BLG-GOV-57/59/60/61 |

**Items explicitly deferred from v4.2 scope:**
- BLG-GOV-60 (SI-02 prerequisites checklist) — included as S2-04; delivery target "before SI-02 sprint planning seals" — remains appropriate
- BLG-SPEC-41 (SI-02 drift score metric) — gate-conditional on SI-02 sprint imminent; deferred until SI-02 gates clear
- BLG-GOV-62 (SI-04 §13 pre-assessment) — gate-conditional on SI-04 sprint planning imminent; deferred
- BLG-GOV-68 (backlog inter-dependency tracking) — gate-conditional on 20+ concurrent items; deferred
- BLG-OPS-37 (Anthropic tier cost assessment) — gate-conditional on BLG-OPS-36 completion; deferred to post-v4.2
- BLG-GOV-67 (SI-05 Phase 1) — gate clears 2026-06-21; not plannable in this sprint
- BLG-QA-38, BLG-QA-36 — lower priority; deferred to v4.2+

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing |
|---------|-------------|-------|----------|------------|
| EPIC-01 | S2-01 | Cybersecurity & Trust Lead; AI Compliance Officer | RISK-01 | Sprint 1 — no dependencies |
| EPIC-02 | S2-02 | FinOps & Resource Architect; Infrastructure & Operations Owner | RISK-02 | Sprint 1 — OA-3 obligation; BLG-OPS-36 before BLG-OPS-39 recommended |
| EPIC-03 | S2-03 | Head of Backend Engineering; AI Compliance Officer; Head of Specs Team | RISK-03 | Sprint 2 — BLG-GOV-63 (audit trail) ideally ships before BLG-OPS-36 monthly review for data fidelity; SPEC-42 + QA-37 independent |
| EPIC-04 | S2-04 | PMO Lead; Head of Specs Team; Product Owner | RISK-04 | Sprint 2 — SI-02 checklist (GOV-60) must complete before SI-02 sprint planning trigger |

*EPIC-03 note: BLG-GOV-63 (audit trail M-effort) is a backend implementation; all other EPIC-03 items are documentation/assessment. BLG-OPS-36 (monthly review) in EPIC-02 can run using existing basic logging if GOV-63 is not yet complete — BLG-OPS-36 scoped to "or equivalent" data source.*

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Anthropic API key scope review may find broader-than-expected exposure | Low | All items are advisory/documentation; no production changes required if review passes | null |
| RISK-02 | EPIC-02 | BLG-OPS-35 api_performance_baseline requires live environment run; may depend on Claude API thesis being called in staging | Low | Infrastructure & Operations Owner coordinates timing; estimated baseline acceptable if live run not feasible in sprint | null |
| RISK-03 | EPIC-03 | BLG-GOV-63 audit trail (M effort) may surface schema migration requirement | Medium | Scope modelled on BLG-GOV-35 Gemini pattern (shipped); Claude equivalent analogous; migration overhead low | null |
| RISK-04 | EPIC-04 | SI-02 prerequisites checklist (GOV-60) requires consolidating 8+ pre-planning items; scope uncertainty in checklist design | Low | PMO Lead owns; 2-cycle pre-work context exists; S effort is realistic | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**S2 → EPIC mapping check:**
- S2-01 → EPIC-01 ✅ (GOV-64/65/66, OPS-38)
- S2-02 → EPIC-02 ✅ (OPS-35/36/39)
- S2-03 → EPIC-03 ✅ (GOV-63, SPEC-42, QA-37, BE-22)
- S2-04 → EPIC-04 ✅ (GOV-57/59/60/61)

**EPIC → RISK check:**
- EPIC-01 → RISK-01 ✅
- EPIC-02 → RISK-02 ✅
- EPIC-03 → RISK-03 ✅
- EPIC-04 → RISK-04 ✅

**Sequencing integrity:**
- Sprint 1 (EPIC-01 + EPIC-02): independent, no external dependencies ✅
- Sprint 2 (EPIC-03 + EPIC-04): EPIC-03 ideally after EPIC-02 (for BLG-OPS-36 data); EPIC-04 independent ✅
- No circular dependencies ✅
- All backlog items exist and confirmed in backlog.md ✅

**Integrity result: PASS**

---

## Capacity Check

**Effort summary:**

| EPIC | Items | Estimated effort | Sprint |
|------|-------|-----------------|--------|
| EPIC-01 | 4 items (3×XS/S + 1×S) | ~2.25 days | Sprint 1 |
| EPIC-02 | 3 items (3×S) | ~2.5 days | Sprint 1 |
| EPIC-03 | 4 items (1×M + 3×S) | ~4.5 days | Sprint 2 |
| EPIC-04 | 4 items (3×S + 1×XS) | ~3.25 days | Sprint 2 |

**Total estimated:** ~12.5 days across 2 sprints  
**Sprint 1:** ~4.75 days | **Sprint 2:** ~7.75 days

### Phasing Recommendation

Sprint 2 carries more load (M-effort GOV-63 + 7 S/XS items). Capacity warn applies.

- **Sprint 1 (EPIC-01 + EPIC-02):** ~4.75 days — within capacity. Sequence: EPIC-01 first (pure docs/policy), EPIC-02 second (OA-3 obligation + baselines).
- **Sprint 2 (EPIC-03 + EPIC-04):** ~7.75 days — slightly above typical solo sprint capacity. Option: defer BLG-BE-22 (prompt caching assessment, S, P2) to post-v4.2 if sprint overloads. Core EPIC-03 items (GOV-63 + SPEC-42 + QA-37) remain.

**Merge order:** EPIC-01 → EPIC-02 (Sprint 1); EPIC-04 → EPIC-03 (Sprint 2, GOV-63 backend last to allow independent parallel progress).

**Capacity verdict: WARN** (Sprint 2 slightly over; manageable with optional BLG-BE-22 deferral at sprint planning).
