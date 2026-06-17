**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-17__release-v5.8
**Release:** v5.8
**Published:** 2026-06-17

---

# Release Plan — v5.8

**Theme:** RFJ UX Design Completion, SI-05 Effectiveness Review & Production Hardening

---

## Readiness

| Check | Status | Notes |
|-------|--------|-------|
| post_ship_complete | ✓ | v5.7 closed 2026-06-17 |
| next_cycle_unblocked | ✓ | |
| Roadmap declaration | ✓ | `next_release: v5.8`; header "Next planned release: v5.8" |
| Backlog lock | ✓ | No prior lock present |
| Carry-forward actioned | ✓ | BLG-FE-64 firm; FRONTEND_URL included |
| Prior lessons action-now items | ✓ | 0 action-now items in v5.7 closure |

**Gate 2026-06-21:** SI-03 live ≥30 days (from 2026-05-22). Gate clears 4 days into sprint window. BLG-FE-64 and BLG-FE-41 are eligible as firm Sprint 1 stories — gate is time-certain.

**Gate 2026-07-04:** SI-05 Phase 1 first effectiveness review (BLG-GOV-113). Three Sprint 2 items conditional on this gate.

---

## Scope

### Items in Scope

| S2-ID | BLG-ID | Title | Type | Effort | Conditional |
|-------|--------|-------|------|--------|-------------|
| S2-01 | BLG-FE-64 | RFJ design review pre-brief | Frontend/UX | XS | No — gate 2026-06-21 (time-certain) |
| S2-02 | BLG-FE-41 | Red Flag Journal visual design review | Frontend/UX | M | No — gate 2026-06-21 (time-certain) |
| S2-03 | — | FRONTEND_URL production env var configuration | Ops | XS | No |
| S2-04 | BLG-GOV-101 | Governance model complexity assessment | Governance | M | No — gate met (0 open audit items post-AUD-2026-06-16) |
| S2-05 | BLG-GOV-112 | SI-05 digest weekly cadence review | Governance | S | Yes — gate 2026-07-04 |
| S2-06 | BLG-GOV-115 | SI-05 digest actionability metric definition | Governance | S | Yes — gate 2026-07-04 |
| S2-07 | BLG-OPS-59 | SI-05 service production p99 latency review | Ops | S | Yes — gate 2026-07-04 |

**Firm stories:** S2-01 through S2-04 (4)
**Conditional stories:** S2-05 through S2-07 (3, gate 2026-07-04)
**Total:** 7

### Items Explicitly Deferred

| Item | Reason |
|------|--------|
| BLG-FEAT-25 PT-04 Setup Quality Score | Gate not met: 13/20 closed trades. Re-verify when PO confirms 20+ closed trades |
| BLG-GOV-112, BLG-GOV-115, BLG-OPS-59 (if gate fails) | Conditional — returned to backlog if 2026-07-04 gate not cleared at sprint planning |
| SI-02 frontend, SI-04, SI-05 Phase 2 | Trade count gate / Later horizon |
| Arc 6 features | Gate: 100+ trades, 18+ months history |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-03, S2-04 | Head of UX & Design; PMO Lead | RISK-01: BLG-FE-41 scope may expand once pre-brief (S2-01) completes | Sprint 1; S2-01 before S2-02 (pre-brief scopes the review) |
| EPIC-02 | S2-05, S2-06, S2-07 | Product Owner; Infrastructure & Operations Owner | RISK-02: 2026-07-04 gate may not clear if SI-05 effectiveness review is delayed | Sprint 2; entire EPIC conditional on 2026-07-04 gate |

**EPIC-01 note:** S2-01 (pre-brief, XS) should be completed first as it scopes S2-02. Both can sit in the same sprint; S2-02 begins once S2-01 defines the review scope. S2-03 (FRONTEND_URL) and S2-04 (governance assessment) are independent.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | BLG-FE-41 scope expands beyond the pre-brief definition | Low | S2-01 pre-brief explicitly caps scope; Head of UX & Design owns scope boundary | null |
| RISK-02 | EPIC-02 | SI-05 effectiveness review (BLG-GOV-113) not complete by 2026-07-04 | Medium | EPIC-02 is conditional — if gate doesn't clear, return all 3 stories to backlog and close as Sprint 2 deferred | null |

---

## Capacity Check

| EPIC | Stories | Effort estimate | Sprint |
|------|---------|----------------|--------|
| EPIC-01 | 4 (S2-01/02/03/04) | XS + M + XS + M ≈ 3–4 days | Sprint 1 |
| EPIC-02 | 3 (S2-05/06/07) | S + S + S ≈ 1.5 days | Sprint 2 (conditional) |

**Total estimated effort:** ~4.5–5.5 days across 2 sprints.

Solo-dev capacity: standard. **Capacity check: PASS** — well within 1-sprint solo-dev budget for Sprint 1; Sprint 2 is conditional and lightweight.

### Phasing Recommendation

- **Sprint 1:** EPIC-01 (4 firm stories, ~3–4 days) — UX design, ops, governance assessment
- **Sprint 2:** EPIC-02 (3 conditional stories, ~1.5 days) — SI-05 effectiveness review items; only if 2026-07-04 gate confirmed cleared at Sprint 2 gate check

---

## Integrity Validation — 3.5 Local Model Integrity

- S2-01 → EPIC-01: ✓ mapped
- S2-02 → EPIC-01: ✓ mapped; depends on S2-01 (same sprint, sequential)
- S2-03 → EPIC-01: ✓ mapped; independent
- S2-04 → EPIC-01: ✓ mapped; independent; gate met per 0 open audit items
- S2-05 → EPIC-02: ✓ mapped; conditional on 2026-07-04
- S2-06 → EPIC-02: ✓ mapped; conditional on 2026-07-04
- S2-07 → EPIC-02: ✓ mapped; conditional on 2026-07-04
- All RISK-IDs in EPIC table appear in Risk Register: ✓
- No orphaned S2-IDs: ✓

**Result: PASS**
