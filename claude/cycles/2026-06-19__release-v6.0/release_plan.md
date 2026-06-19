Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v6.0
Cycle: 2026-06-19__release-v6.0
Last Updated: 2026-06-19

---

# Release Plan — v6.0 Signal Correctness, User Intelligence & SI-05 Effectiveness

---

## Readiness

**Lifecycle guard:** status = Closed → valid entry state for Release Planning. ✅
**Post-ship precondition:** post_ship_complete = true; next_cycle_unblocked = true. ✅
**Roadmap alignment:** v6.0 section present in current_roadmap.md. ✅
**Prior cycle closure:** 2026-06-17__release-v5.9 — Closed_with_actions; post_ship_complete = true. ✅
**Design gate:** Not required. Scan of scope candidates found no "design decision required" language. All frontend work follows existing patterns (DashboardHome extension, data field addition, screener panel enhancement). ✅

**Product Value Alert context:** Last rebalance (2026-06-19) recorded Product Value Alert (ratio=0.093). v6.0 scope addresses this: 3 U-classified stories (BLG-BE-36 correctness, BLG-FEAT-46 Morning Briefing, BLG-FEAT-20 net-of-costs) from 5 firm stories = 60% user-value ratio (firm scope only). ✅

**Skill-Silo Alert context:** Last rebalance recorded Skill-Silo Alert (G+D+P=90.7%). v6.0 firm scope: 3U + 1G + 1D = 40% G+D ratio. Within the 40% ceiling (per roadmap_prompt.md v7.4). Conditional scope (EPIC-04) is G/D/P-heavy — sprint planning must manage to ≤40% per sprint. ⚠ Advisory noted.

---

## Scope

### S2 Items

| S2-ID | BLG-ID | Title | Priority | Effort | Class | Classification |
|-------|--------|-------|----------|--------|-------|----------------|
| S2-01 | BLG-BE-36 | Align signal_service suggested_shares to risk-based sizing model | P0 | S | U | **Firm** |
| S2-02 | BLG-FEAT-46 | Trader's Morning Briefing dashboard | P1 | M | U | **Firm** |
| S2-03 | BLG-FEAT-20 | Net-of-costs performance tracking | P1 | M | U | **Firm** |
| S2-04 | BLG-FEAT-47 | Screener data quality telemetry | P1 | S | G | **Firm** |
| S2-05 | BLG-OPS-70 | SI-05 deep link AC-04 staging confirmation | P2 | XS | D | **Conditional** (gate ~2026-06-23; within-sprint per STEP 1.4b) |
| S2-06 | BLG-FE-64 | RFJ design review pre-brief | P2 | S | P | **Conditional** (gate 2026-06-21; within-sprint per STEP 1.4b) |
| S2-07 | BLG-FE-41 | Red Flag Journal visual design review | P3 | M | P | **Conditional** (gate 2026-06-21; depends on S2-06; within-sprint) |
| S2-08 | BLG-GOV-112 | SI-05 digest weekly cadence review | P2 | S | G | **Conditional** (gate 2026-07-04; within-sprint) |
| S2-09 | BLG-GOV-115 | SI-05 digest actionability metric definition | P2 | S | G | **Conditional** (gate 2026-07-04; within-sprint) |
| S2-10 | BLG-GOV-130 | SI-05 Phase 2 activation decision scope | P2 | S | G | **Conditional** (gate 2026-07-04; within-sprint) |
| S2-11 | BLG-OPS-59 | SI-05 service production p99 latency baseline review | P2 | S | D | **Conditional** (gate 2026-07-04; within-sprint) |

**Firm scope items: 4** (S2-01 through S2-04)
**Conditional scope items: 7** (S2-05 through S2-11)
**Total scope items: 11**

### Items Explicitly Deferred
| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-25 (PT-04 Setup Quality Score) | Gate not met: 13 closed trades (need 20); trajectory ~2026-07-02 — eligible for sprint planning conditional add if gate clears | Post-gate |
| SI-02 frontend (BLG-FE-52/53) | Gate not met: <20 closed trades | Post-gate |
| BLG-FE-76 (heat-map) | Roadmap note: targets v6.1 as first dedicated user-value cycle post-governance-consolidation | v6.1 |
| All Arc 4/5/6 gated features | Data-density or trade-count gates not met | TBD |

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Strategy Rules & System Intent Owner; Head of Engineering | RISK-01 | First — P0 correctness fast-track |
| EPIC-02 | S2-02, S2-03 | Head of UX & Design; Financial Reporting & Records Owner | RISK-02, RISK-03 | After EPIC-01 |
| EPIC-03 | S2-04, S2-05 | Head of UX & Design; Infrastructure & Operations Owner | RISK-04 | After EPIC-01; parallel with EPIC-02 possible |
| EPIC-04 | S2-06, S2-07, S2-08, S2-09, S2-10, S2-11 | PMO Lead; Product Owner; Head of UX & Design | RISK-05 | Conditional — activates when respective gates clear within sprint |

**EPIC-04 note:** EPIC-04 is a conditional EPIC with two gate clusters:
- Cluster A (gate 2026-06-21): S2-06 (BLG-FE-64) and S2-07 (BLG-FE-41). S2-07 depends on S2-06 completing first.
- Cluster B (gate 2026-07-04): S2-08, S2-09, S2-10, S2-11. These are independent within Cluster B.

If Cluster A gates clear during sprint (2026-06-21), EPIC-04 Cluster A activates. If Cluster B gates clear (2026-07-04 — end of sprint window), Cluster B activates. If any gates are not met by sprint close, items return to backlog.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Strategy Rules & System Intent Owner must confirm risk-based formula is canonical before implementation; if contested, story blocks | Medium | Scope entry includes explicit sign-off step; blocking condition flagged in AC | null |
| RISK-02 | EPIC-02 | BLG-FEAT-46 composes from 5 existing endpoints; if any endpoint data contract has changed, frontend integration may surface gaps | Low | Endpoints are stable (GET /portfolio/grace-period-alerts, GET /positions, GET /portfolio/red-flag-journal, GET /earnings/{ticker}, GET /analytics/arc5-compliance) — all confirmed live | null |
| RISK-03 | EPIC-02 | BLG-FEAT-20 requires additive trade data fields (commission, spread cost); migration must be backward-compatible | Low | Scope explicitly scoped to optional fields only; existing R-multiple unaffected where cost data absent | null |
| RISK-04 | EPIC-03 | BLG-OPS-70 depends on SI-05 digest delivery event (~2026-06-23); delivery may be delayed or digest may not fire on expected date | Low | Classified conditional per STEP 1.4b; returns to backlog if not confirmed by sprint close | null |
| RISK-05 | EPIC-04 | Multiple within-sprint date gates; if gates missed, all EPIC-04 items return to backlog (7th consecutive deferral for BLG-FE-64) | High | Sprint planning must explicitly track gate dates and confirm clearance before scheduling EPIC-04 work. BLG-FE-64 perennial-return advisory surfaced at STEP 1.4a — PO has made explicit disposition (retain conditional). | null |

---

## Capacity Check

### Effort Band Lookup (STEP 0 / scored_initiatives.md)
- BLG-OPS-59: Effort Band S (from scored_initiatives.md 2026-06-08 cycle table) — Tier 1 resolution
- All other v6.0 scope items: no matching rows in scored_initiatives.md — Tier 3 resolution (backlog estimates)

### Effort Estimates

| Story | BLG-ID | Effort Band | Mid-point | Classification |
|-------|--------|-------------|-----------|----------------|
| ST-01 | BLG-BE-36 | S | 0.5 day | Firm |
| ST-02 | BLG-FEAT-46 | M | 2.5 days | Firm |
| ST-03 | BLG-FEAT-20 | M | 2.5 days | Firm |
| ST-04 | BLG-FEAT-47 | S | 1.0 day | Firm |
| ST-05 | BLG-OPS-70 | XS | 0.1 day | Conditional |
| ST-06 | BLG-FE-64 | S | 0.5 day | Conditional |
| ST-07 | BLG-FE-41 | M | 1.5 days | Conditional |
| ST-08 | BLG-GOV-112 | S | 0.5 day | Conditional |
| ST-09 | BLG-GOV-115 | S | 0.75 day | Conditional |
| ST-10 | BLG-GOV-130 | S | 0.5 day | Conditional |
| ST-11 | BLG-OPS-59 | S (scored) | 0.5 day | Conditional |

**Firm scope total:** 0.5 + 2.5 + 2.5 + 1.0 = **6.5 days mid-point**
**All conditional total:** 0.1 + 0.5 + 1.5 + 0.5 + 0.75 + 0.5 + 0.5 = **4.35 days**
**Total if all activate:** **~10.85 days**

**Assumed capacity:** Solo developer, ~10–12 working days per sprint.

**Outcome:** PASS (firm scope) — 6.5 days well within capacity. WARN (if all conditional activate) — ~10.85 days approaches capacity ceiling but remains feasible. Sprint planning should phase EPIC-04 into conditional slots only after gates confirmed.

### Phasing Recommendation
*Required because total with all conditional items approaches capacity.*

- **Phase 1 — Sprint days 1–7 (firm scope):** EPIC-01 (0.5d), EPIC-02 (5d), EPIC-03 firm portion (1d) = 6.5 days
- **Phase 2 — Sprint days 7–12 (conditional, as gates clear):**
  - EPIC-03 S2-05 (0.1d, gates ~2026-06-23)
  - EPIC-04 Cluster A: ST-06 + ST-07 (2.0d, gates 2026-06-21)
  - EPIC-04 Cluster B: ST-08–11 (2.25d, gates 2026-07-04)

Ordering rationale: Firm items first to guarantee Product Value Alert commitment (3 U-stories). Conditional items staged by gate date. EPIC-04 Cluster B may extend to the last day of the sprint; Product Owner should confirm sprint close date allows time for 2026-07-04 gate items.

---

## Integrity Validation — 3.5 Local Model Integrity

**Check:** All S2-IDs map to EPICs ✅
- S2-01 → EPIC-01; S2-02, S2-03 → EPIC-02; S2-04, S2-05 → EPIC-03; S2-06 through S2-11 → EPIC-04

**Check:** All EPIC-IDs have `Maps to:` declared ✅ (see stage4_backlog_slice.md)

**Check:** All RISK-IDs in EPIC table appear in Risk Register ✅
- EPIC-01 → RISK-01; EPIC-02 → RISK-02, RISK-03; EPIC-03 → RISK-04; EPIC-04 → RISK-05

**Check:** No orphaned references ✅

**Check:** EPIC-04 conditional gate structure is logically consistent:
- Cluster A (gate 2026-06-21): ST-06 must precede ST-07 ✅ (dependency noted in stage4_backlog_slice.md)
- Cluster B items are independent within cluster ✅

**Result: stage3_5_model_integrity = pass**

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**5.5 Cross-Stage:**
- All S2-IDs (S2-01 through S2-11) appear in both § Scope table and stage4_backlog_slice.md ✅
- All EPIC-IDs in stage4_backlog_slice.md match stage3 execution plan (EPIC-01 through EPIC-04) ✅
- All RISK-IDs in EPIC table (RISK-01 through RISK-05) appear in Risk Register Summary ✅
- All ST-IDs in stage4_backlog_slice.md map to their parent EPIC-IDs ✅
- No orphaned S2, EPIC, RISK, or ST references ✅

**5.7 Decision Record Integrity:** `artifacts.escalations = not_started` (no escalations raised) → STEP 5.7 NOT APPLICABLE. ✅

**Result:**
- stage5_5_cross_stage_integrity = pass
- stage5_7_decision_record_integrity = not_applicable
