**Owner:** Head of Specs Team
**Class:** Planning Record (Class 3)
**Status:** Published
**Version:** 1.0
**Cycle:** 2026-06-09__release-v5.4
**Last Updated:** 2026-06-09

---

# Release Plan — v5.4: Ops Monitoring, UX Debt Clearance & Governance Patches

---

## Readiness

**Release:** v5.4
**Theme:** SI-05 ops monitoring follow-through, UX debt clearance (pre-entry panel, Red Flag Journal), governance patches

### Readiness Checks

| Check | Result | Notes |
|-------|--------|-------|
| Roadmap item present | ✅ PASS | v5.4 section added 2026-06-09__scheduled (DL-042, STEP 8.1 Option(a)) |
| Prior cycle closed | ✅ PASS | v5.3 Closed_with_actions; post_ship_complete=true |
| Backlog items scoped | ✅ PASS | 7 items identified (4 firm Sprint 1; 3 conditional Sprint 2) |
| Gate-blocked items identified | ✅ PASS | BLG-GOV-91 deferred (SI-04 gate NOT MET); BLG-FE-68-71 deferred |
| Completed items removed | ✅ PASS | BLG-FE-47, BLG-FE-49, DP-2 all complete/applied — excluded |

### Advisories

- ⚠ **Backlog age:** BLG-GOV-92 aged 2+ cycles (v5.2, v5.3) without story assignment. Promoted to Sprint 1 story in this release.
- ℹ **Provisional-Target:** 2 items carry `Provisional-Target: v5.4` (BLG-OPS-60, BLG-GOV-115). 5 items unscheduled.
- ℹ **Design dependency scan:** 0 items flagged.
- ℹ **PT-04 gate re-verification (per backlog note):** 6 closed trades (same as v5.3); 11 total; gate NOT MET. PT-04 remains parked.

### Gate Proximity Table

| Item | Gate condition | Trajectory | Projected clear |
|------|---------------|------------|-----------------|
| BLG-FE-64 | SI-03 live ≥30 days (2026-06-21) | On track | 2026-06-21 |
| BLG-OPS-59 | SI-05 in production ≥4 weeks (≥2026-07-04) | On track | 2026-07-04 |
| BLG-GOV-115 | 2026-07-04 effectiveness review complete | On track | 2026-07-04 |
| BLG-GOV-112 | 2026-07-04 effectiveness review complete | On track | 2026-07-04 |
| PT-04 / SI-02 | ≥20 closed trades | ~0.5/month net | Unknown — not in window |
| PO-02 | ≥6 months AI journals | ~1/month | ~2026-11-05 |
| BLG-GOV-91 | SI-04 sprint planning imminent | SI-04 in Later horizon | Not in window |

---

## Scope

### S2 Scope Items

| ID | Backlog ref | Description | Priority | Effort | Gate |
|----|------------|-------------|----------|--------|------|
| S2-01 | BLG-OPS-60 | Add v5.3 new endpoints to api_performance_baseline.md | P3 | S | None |
| S2-02 | BLG-FE-56 | Pre-entry panel: separate warn/fail override acknowledgement flow | P2 | S | None |
| S2-03 | BLG-FE-64 | RFJ visual design review pre-brief | P2 | S | 2026-06-21 |
| S2-04 | BLG-GOV-92 | SI-05 Phase 2 activation criteria definition | P2 | S | None (before Nov 2026) |
| S2-05 | BLG-OPS-59 | SI-05 p99 production latency baseline review | P2 | S | ≥2026-07-04 |
| S2-06 | BLG-GOV-115 | SI-05 digest actionability metric definition | P2 | S | 2026-07-04 |
| S2-07 | BLG-GOV-112 | SI-05 digest weekly cadence review | P2 | S | 2026-07-04 |

**Firm scope:** S2-01 through S2-04 (4 items)
**Conditional scope:** S2-05 through S2-07 (3 items; gate ≥2026-07-04)

### Explicitly Deferred

| Item | Reason |
|------|--------|
| BLG-GOV-91 | Gate NOT MET — SI-04 in Later horizon; gate triggers when SI-04 enters sprint planning |
| BLG-FE-68/70 | Gate NOT MET — BLG-FE-45 not complete |
| BLG-FE-69/71 | Gate NOT MET — BLG-GOV-92 Phase 2 decision required first (BLG-GOV-92 in-sprint) |
| BLG-QA-55 | Gate NOT MET — ≥20 closed trades (same gate as SI-02) |
| BLG-SPEC-55 | Gate NOT MET — PO-02 sprint planning not imminent |
| BLG-FEAT-45 | Gate NOT MET — ≥2026-08-05 (3+ months since Monthly P&L shipped) |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-05 | Infrastructure & Operations Owner | RISK-01 | S2-05 after Sprint 2 gate (2026-07-04) |
| EPIC-02 | S2-02, S2-03 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-02 | S2-03 after 2026-06-21 |
| EPIC-03 | S2-04, S2-06, S2-07 | Product Owner; Metrics Definitions & Analytics Owner | RISK-03 | S2-06/S2-07 after Sprint 2 gate (2026-07-04) |

**Sprint structure:**
- Sprint 1 (firm): EPIC-01 ST-01, EPIC-02 ST-02+ST-03, EPIC-03 ST-04
- Sprint 2 (conditional, gate 2026-07-04): EPIC-01 ST-05, EPIC-03 ST-06+ST-07

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | BLG-OPS-59 requires Render production log access — p99 extraction from live environment | Medium | Infrastructure & Operations Owner to confirm log access before Sprint 2 execution | null |
| RISK-02 | EPIC-02 | BLG-FE-64 gate (2026-06-21) not yet cleared; execution before gate would violate backlog constraint | Low | Sprint 1 execution after 2026-06-21; gate confirm at sprint planning | null |
| RISK-03 | EPIC-03 | SI-05 effectiveness review (BLG-GOV-113) must complete before Sprint 2 items execute; review not yet run | Medium | Sprint 2 gate-conditional on effectiveness review completing 2026-07-04; PO confirms go/no-go before Sprint 2 seals | null |

---

## Integrity Validation — 3.5 Local Model Integrity

All S2 IDs map to EPICs. All EPIC IDs declared. All RISK IDs in EPIC table appear in Risk Register. No orphaned references. Cross-stage IDs consistent.

**Result:** ✅ PASS

---

## Capacity Check

| EPIC | Stories | Sprint | Effort estimate | Source |
|------|---------|--------|----------------|--------|
| EPIC-01 | ST-01 | 1 | S (~0.5 day) | Inline |
| EPIC-02 | ST-02, ST-03 | 1 | S+S (~1.5 days) | Inline |
| EPIC-03 | ST-04 | 1 | S (~0.5 day) | Inline |
| EPIC-01 | ST-05 | 2 | S (~0.5 day) | Scored (BLG-OPS-59 in scored_initiatives.md) |
| EPIC-03 | ST-06, ST-07 | 2 | S+S (~1 day) | Inline |

**Sprint 1 total:** ~2.5 days
**Sprint 2 total (conditional):** ~1.5 days
**Grand total:** ~4 days

Capacity: solo-dev, standard pace. ~4 days is well within single-sprint capacity. No WARN triggered.

**Capacity feasibility: PASS**
