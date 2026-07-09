Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-09
Cycle: 2026-07-08__release-v6.8

---

# Sprint Capacity — 2026-07-08__release-v6.8

## 1.1 Capacity Inputs

```
Sprint duration:    ~12-14 working days (single sprint; solo developer, evenings/weekends)
Available FTE:      1 (solo operator — Backend Engineering, Frontend/Base44, QA execution, Spec authoring, Governance all performed by same operator across roles)
Total capacity:     ~12-14 working days (per workforce_capacity.md Sprint Capacity Baseline, effective 2026-05-27)
Skill constraints:  None scarce for this scope — EPIC-01 requires Backend Engineering + Cybersecurity & Trust + Infrastructure & Operations; EPIC-02 requires Product Owner + Head of UX & Design (delegated_frontend); EPIC-03 requires Head of Specs Team + PMO Lead plus domain sign-offs (Metrics & Analytics, Director of Quality, FinOps & Resource Architect, Infrastructure & Operations, Cybersecurity & Trust). No overlapping scarce-skill contention across the three EPICs — all roles performed by the same solo operator, sequencing (not skill availability) is the binding constraint.
Warn threshold:     Effort > 14 days
```

## 1.2 Item Effort Mapping

| EPIC | Story | Effort estimate (source: release_plan.md Execution Plan / Capacity Check) |
|------|-------|------|
| EPIC-01 | ST-01 (BLG-BE-46) | M (~1–2 days, mid-point 1.5) |
| EPIC-01 | ST-02 (BLG-SEC-08) | S (~0.5 day) |
| EPIC-01 | ST-03 (BLG-SEC-07) | XS (<1h, mid-point 0.1) |
| EPIC-01 | ST-04 (BLG-OPS-99) | S (~0.5 day) |
| EPIC-02 | ST-05 (BLG-FEAT-52) | S (~2–3 days, mid-point 2.5, descoped from L) |
| EPIC-02 | ST-06 (BLG-FEAT-71) | S (~1–2 days, mid-point 1.5) |
| EPIC-03 | ST-07 (BLG-SPEC-58) | S (~0.5 day) |
| EPIC-03 | ST-08 (BLG-SPEC-59) | S (~0.5 day) |
| EPIC-03 | ST-09 (BLG-SPEC-60) | S (~0.5 day) |
| EPIC-03 | ST-10 (BLG-SPEC-61) | S (~0.5 day) |
| EPIC-03 | ST-11 (BLG-QA-64) | M (~1 day) |
| EPIC-03 | ST-12 (BLG-GOV-134) | S (~0.5 day) |
| EPIC-03 | ST-13 (BLG-OPS-74) | S (<0.5 day, mid-point 0.4) |
| EPIC-03 | ST-14 (BLG-FE-77) | M (~1–2 days, mid-point 1.5) |
| EPIC-03 | ST-15 (BLG-OPS-61) | S (~0.5–1 day, mid-point 0.75) |
| EPIC-03 | ST-16 (BLG-GOV-123) | XS (~1h, mid-point 0.15) |
| EPIC-03 | ST-17 (BLG-OPS-71) | S (~1 day) |

No item is missing an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

```
EPIC-01 total:  1.5 + 0.5 + 0.1 + 0.5 ≈ 2.6 days
EPIC-02 total:  2.5 + 1.5 ≈ 4.0 days
EPIC-03 total:  0.5+0.5+0.5+0.5+1.0+0.5+0.4+1.5+0.75+0.15+1.0 ≈ 7.3 days
Grand total:    ≈13.9 days
Capacity:       ~12-14 days
Outcome:        PASS — within confirmed capacity, no over-allocation. Matches release_plan.md Capacity Check outcome (PASS, not WARN). capacity_warn_acknowledged = false (not applicable — no WARN was issued).
```

This is the largest single-sprint firm scope by story count since v6.3 (15 stories) / v6.4 (13 stories) — 17 stories, ≈13.9 days sits near the top of the 12–14 day baseline (≈99–116% utilisation depending on which end of the range is used). RISK-04 (recorded in `release_plan.md` Risk Register) flags the resulting context-switching overhead of 11 concurrent EPIC-03 items for a solo developer; mitigation is that EPIC-03 items are fully independent and parallelisable, and are the first candidates to trim if early-sprint velocity signals slippage (lowest strategic weight of the three EPICs). No phasing/split across two sprints is required at planning time — all 17 items are firm scope in Sprint 1.

## 1.4 Gate-Conditional Deferred Items

None. All 17 items from the authoritative backlog slice (`stage4_backlog_slice.md`) are firm scope, ungated, and included in this sprint. No `## Conditional (Deferred)` section required.
