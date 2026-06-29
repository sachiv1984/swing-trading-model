**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-29
**Cycle:** 2026-06-26__release-v6.3

---

# Sprint Capacity — 2026-06-26__release-v6.3

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | 2 sprints (~2–3 weeks each) |
| Available FTE | Solo developer |
| Per-sprint capacity | ~12–14 working days (revised 2026-05-27; source: workforce_capacity.md) |
| Total 2-sprint capacity | ~24–28 working days |
| Warn threshold | > 14 days per sprint |
| Capacity source | release_plan.md §Capacity Check + workforce_capacity.md |

**Skill constraints:** None. Solo operator model — all roles fulfilled by a single developer. No scarce skill conflicts identified at release planning. Per workforce_capacity.md assessment: no workforce constraint violations.

## Item Effort Mapping

| EPIC | ST-ID | Story | Effort (days) | Class | Sprint |
|------|-------|-------|--------------|-------|--------|
| EPIC-01 | ST-01 | Fix AI journal summary on Trade History tab (BLG-BE-39) | 0.5 | Firm | Sprint 1 |
| EPIC-01 | ST-02 | Fix R-multiple not displaying on Reflection page (BLG-FE-79) | 0.5 | Firm | Sprint 1 |
| EPIC-01 | ST-03 | AI endpoint per-endpoint rate limiting hardening (BLG-OPS-81) | 0.5 | Firm | Sprint 1 |
| EPIC-01 | ST-04 | AI response injection risk assessment (BLG-GOV-146) | 0.5 | Firm | Sprint 1 |
| EPIC-01 | ST-05 | AI feature advisory disclaimer visibility assessment (BLG-GOV-147) | 0.25 | Conditional | Sprint 1 |
| EPIC-01 | ST-06 | API contract review checklist for AI advisory endpoints (BLG-GOV-148) | 0.5 | Conditional | Sprint 1 |
| EPIC-02 | ST-07 | Nightly stop computation CI simulation tests (BLG-QA-65) | 1.0 | Firm | Sprint 1 |
| EPIC-02 | ST-08 | Strategy signal regression test specification (BLG-QA-66) | 0.5 | Firm | Sprint 1 |
| EPIC-02 | ST-09 | AI chat response schema validation tests (BLG-QA-67) | 0.5 | Conditional | Sprint 1 |
| EPIC-02 | ST-10 | §13 boundary test suite for AI advisory endpoints (BLG-QA-68) | 0.5 | Conditional | Sprint 1 |
| EPIC-03 | ST-11 | Strategy Benchmark page: compare live trades against backtest (BLG-FEAT-53) | 5.0 | Firm | Sprint 2 |
| EPIC-03 | ST-12 | Morning briefing progressive disclosure (BLG-FE-80) | 0.5 | Firm | Sprint 2 |
| EPIC-03 | ST-13 | Background scheduler health monitoring endpoint (BLG-OPS-79) | 0.5 | Conditional | Sprint 2 |
| EPIC-03 | ST-14 | Measure live latency for POST /ai/daily-briefing and POST /ai/chat (BLG-OPS-78) | 0.25 | Conditional | Sprint 2 |
| EPIC-03 | ST-15 | Render deployment rollback procedure documentation (BLG-OPS-80) | 0.25 | Conditional | Sprint 2 |
| **Total** | | | **11.75** | **9.0 firm + 2.75 conditional** | |

## Total Effort vs Capacity

| Sprint | EPICs | Firm effort | Conditional | Total (all included) | Capacity | Status |
|--------|-------|------------|-------------|---------------------|----------|--------|
| Sprint 1 | EPIC-01 + EPIC-02 | 3.5 days | 1.75 days | 5.25 days | 12–14 days | ✅ Within capacity |
| Sprint 2 | EPIC-03 | 5.5 days | 1.0 days | 6.5 days | 12–14 days | ✅ Within capacity |
| **Release total** | | **9.0 days** | **2.75 days** | **11.75 days** | **24–28 days** | ⚠ WARN (see note) |

**Capacity WARN note:** Release plan capacity check outcome is `warn`. Per the original 10–15 hrs/week estimate at release planning, 11.75 days was at the upper bound of 2-sprint capacity. Per the revised workforce_capacity.md baseline (2026-05-27: 12–14 days/sprint), 11.75 total days is well within 2-sprint capacity (24–28 days). The WARN reflects original estimate conservatism, not actual over-allocation. Sprint 1 utilisation ~38%; Sprint 2 utilisation ~46–54% of per-sprint capacity.

## Capacity WARN Acknowledgement

**Product Owner acknowledgement (IMP-41):** The Product Owner acknowledges the capacity WARN from release planning. Per the revised per-sprint baseline (12–14 days/sprint), all 15 stories (8 firm + 7 conditional) are within combined 2-sprint capacity. Sprint 1 (~5.25d) and Sprint 2 (~6.5d) are each well within the 12–14 day per-sprint window. PO accepts all items for sprint inclusion.

*Acknowledgement recorded: 2026-06-29. Mode: standard. Authority: Product Owner via `plan sprint` invocation.*

## Conditional (Deferred)

No items deferred at planning. All 7 conditional items included across both sprints (Sprint 1 total 5.25d and Sprint 2 total 6.5d are each well within the 12–14 day per-sprint capacity).

**ST-13 (BLG-OPS-79)** is included in Sprint 2 but carries a within-sprint architecture review gate: the v6.2 background scheduler architecture must be reviewed before implementation begins. This is a within-sprint sequencing constraint, not a deferral.

**ST-14 (BLG-OPS-78)** requires a production deployment to be accessible for live timing measurements. Execution should proceed at the end of Sprint 2 after the Sprint 2 merge is live.

> **Gate re-invocation:** If any item's gate condition prevents completion during the planned sprint, do not add or modify items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-26__release-v6.3 --reason "<gate condition not met>"`) to adjust the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition or removal.
