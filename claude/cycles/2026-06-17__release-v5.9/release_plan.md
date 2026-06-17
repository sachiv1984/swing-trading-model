**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-17__release-v5.9
**Published:** 2026-06-17

---

# Release Plan — v5.9

## Readiness

Prior cycle: 2026-06-17__release-v5.8 — Closed_with_actions. post_ship_complete=true. next_cycle_unblocked=true.

Preflight: PASS. All required files present. All required agent roles verified. No amendment in progress. No stale backlog lock.

§-1.2: v5.9 confirmed on roadmap (RA:v5.9 section present). PASS.

Perennial-return items addressed: BLG-FE-64 (5 returns), BLG-FE-41 (2 returns), BLG-GOV-112/115/OPS-59 (3 returns). PO active dispositions recorded per §1.4a. All classified conditional per STEP 1.4b mandatory rule.

## Scope

| S2-ID | Description | Stories | Status |
|-------|-------------|---------|--------|
| S2-01 | Governance Simplification Candidates SC-03–SC-07 | BLG-GOV-125, 126, 127, 128, 129 | Firm |
| S2-02 | Red Flag Journal UX Pre-work | BLG-FE-64, BLG-FE-41 | Conditional — gate 2026-06-21 |
| S2-03 | SI-05 Production Deep-Link Verification | BLG-OPS-70 | Conditional — gate ~2026-06-23 |
| S2-04 | SI-05 Effectiveness Review & Phase 2 Decision | BLG-GOV-112, BLG-GOV-113, BLG-GOV-115, BLG-OPS-59, BLG-GOV-130 | Conditional — gate 2026-07-04 |

**Items explicitly deferred:** BLG-GOV-124 (SC-02 RESUME PRECHECK removal) — deferred: higher-effort/risk simplification, P3, no sprint urgency. BLG-FE-40 (RFJ filter state persistence) — deferred: gate not triggered (30 days active use). All other backlog items not in v5.9 roadmap section — unchanged.

**Firm count:** 5 (S2-01 items only)
**Conditional count:** 8 (S2-02: 2, S2-03: 1, S2-04: 5)
**Total scope items:** 13

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Specs Team | RISK-01 | None — ready immediately; merge first |
| EPIC-02 | S2-02, S2-03, S2-04 | PMO Lead; Infrastructure & Operations Owner; Metrics Definitions & Analytics Owner | RISK-02 | After gates clear: S2-02/03 after 2026-06-21/23; S2-04 after 2026-07-04 |

**EPIC-01 notes:** All 5 stories are governance-only prompt simplifications (SC-03–SC-07 from GCA-2026-06-17). No backend or frontend changes. Estimated XS–S effort each (~1 hour each, ~5 hours total). Ready to execute immediately.

**EPIC-02 notes:** Three natural sub-groups within EPIC-02: (a) BLG-FE-64+41 — design review pre-brief + design review, gate 2026-06-21; (b) BLG-OPS-70 — production deep-link verification, gate ~2026-06-23; (c) BLG-GOV-112/113/115/OPS-59/GOV-130 — SI-05 effectiveness review and Phase 2 decision, gate 2026-07-04. Sprint planning engine should split EPIC-02 across Sprint 1 (a+b, conditional) and Sprint 2 (c, conditional).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Governance prompt version drift if CLAUDE.md §6 steps not followed precisely (version bump, §14, change log) | Medium | All 5 stories are template-edit only; version bump checklist applies to each | null |
| RISK-02 | EPIC-02 | 5 of 8 conditional items gated on 2026-07-04 (3rd consecutive gate-deferral cycle for BLG-GOV-112/115/OPS-59); 3 items gated on 2026-06-21/23 (BLG-FE-64 is 5th consecutive deferral) | High | STEP 1.4b mandatory conditional classification; gate owner confirmation required before promoting to firm; Sprint 2 cannot begin until 2026-07-04 gate explicitly confirmed by gate owner | null |

## Capacity Check

**Effort Band resolution (STEP 4.5 three-tier rule):**
- BLG-OPS-59: Effort Band S (from scored_initiatives.md)
- All other v5.9 scope items: no row in scored_initiatives.md (added after 2026-06-07) → inline estimate, no advisory

| EPIC | Items | Estimate (hrs) | Source |
|------|-------|---------------|--------|
| EPIC-01 | 5 × XS–S | 4–6 hrs | Inline (GCA-2026-06-17 sizing: each SC is XS–S) |
| EPIC-02 (S2-02) | BLG-FE-64 (0.5d), BLG-FE-41 (1-2d) | 4–20 hrs | Inline |
| EPIC-02 (S2-03) | BLG-OPS-70 (XS) | <1 hr | Inline |
| EPIC-02 (S2-04) | 5 × S (0.5d each) | 20–25 hrs | Inline; BLG-OPS-59 from scored_initiatives.md |

**Total estimated:** 28–52 hours across 2 sprints.

**Phasing Recommendation (WARN — Sprint 2 calendar gap):**

Sprint 2 cannot begin before 2026-07-04 (gate condition for 5 conditional items). The interval between Sprint 1 close and Sprint 2 open is approximately 2 weeks. This does not indicate infeasibility — it reflects a planned waiting period for the gate.

- Sprint 1 (now to ~2026-06-25): EPIC-01 (firm, 4–6 hrs) + EPIC-02 S2-02/03 subset (conditional near-term, ~5–21 hrs) — ~9–27 hrs. Within capacity.
- Sprint 2 (after 2026-07-04): EPIC-02 S2-04 subset (conditional, ~20–25 hrs) — within single-sprint capacity.

Overall: WARN (calendar gap in Sprint 2 start). PASS for sprint-level feasibility.

## Integrity Validation

**Cross-Stage Integrity (STEP 5.5):**
- All S2-IDs (S2-01–S2-04) map to EPICs ✓
- All EPIC IDs in backlog slice reference correct S2 items ✓
- All RISK-IDs in EPIC table appear in Risk Register ✓
- No orphaned references ✓

STEP 5.5 result: **PASS**

Decision Record Integrity: N/A (no escalations raised; decisions record created as standard artefact).
