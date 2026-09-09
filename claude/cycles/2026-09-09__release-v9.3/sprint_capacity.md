Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-09
Cycle: 2026-09-09__release-v9.3

# Sprint Capacity — 2026-09-09__release-v9.3

## 1.1 Capacity Inputs

```
Sprint duration:    Single sprint (per release_plan.md sealed_assumptions.timebox)
Available FTE:      1 (solo developer + AI execution engine, full capacity)
Total capacity:     ~24–28 working-day-equivalent effort units (workforce_capacity.md, unchanged since 2026-07-17__scheduled)
Skill constraints:  None flagged in release_plan.md ## Execution Plan. Head of Specs Team is named across EPIC-04 and EPIC-05 sign-offs — no concurrency conflict since all EPIC-04/05 items are S/M effort and sequenced within the sprint, not simultaneous.
```

## 1.2 Item Effort Mapping

Source: `stage4_backlog_slice.md` per-item `**Effort:**` field; band-to-day conversion per `workforce_capacity.md ## Canonical Effort Band → Days Conversion Table` (XS=0.15d, S=0.5d, M=2.5d, L=3.5d). No `[ESTIMATE REQUIRED]` placeholders — all 27 items carry a defined effort band (confirmed by `release_plan.md`'s STEP 3.5 Local Model Integrity check).

### EPIC-01 — Backend Reliability & Data Correctness Debt (8.00d)

| Item | Effort | Days |
|------|--------|------|
| ST-01 | M | 2.50 |
| ST-02 | M | 2.50 |
| ST-03 | M | 2.50 |
| ST-04 | S | 0.50 |

### EPIC-02 — QA & Test Infrastructure Debt (5.00d)

| Item | Effort | Days |
|------|--------|------|
| ST-05 | S | 0.50 |
| ST-06 | M | 2.50 |
| ST-07 | S | 0.50 |
| ST-08 | S | 0.50 |
| ST-09 | S | 0.50 |
| ST-10 | S | 0.50 |

### EPIC-03 — Operations & Cost Monitoring Debt (6.50d)

| Item | Effort | Days |
|------|--------|------|
| ST-11 | S | 0.50 |
| ST-12 | S | 0.50 |
| ST-13 | S | 0.50 |
| ST-14 | M | 2.50 |
| ST-15 | M | 2.50 |

### EPIC-04 — Spec & Documentation Debt (4.50d)

| Item | Effort | Days |
|------|--------|------|
| ST-16 | S | 0.50 |
| ST-17 | M | 2.50 |
| ST-18 | S | 0.50 |
| ST-19 | S | 0.50 |
| ST-20 | S | 0.50 |

### EPIC-05 — Governance Process Debt & Security (3.50d)

| Item | Effort | Days |
|------|--------|------|
| ST-21 | S | 0.50 |
| ST-22 | S | 0.50 |
| ST-23 | S | 0.50 |
| ST-24 | S | 0.50 |
| ST-25 | S | 0.50 |
| ST-26 | S | 0.50 |
| ST-27 | S | 0.50 |

## 1.3 Total Effort vs Capacity

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 8.00 |
| EPIC-02 | 5.00 |
| EPIC-03 | 6.50 |
| EPIC-04 | 4.50 |
| EPIC-05 | 3.50 |
| **Total** | **27.50** |

27.50 days vs confirmed ~24–28 day band → **within capacity, no over-allocation.** Matches `release_plan.md ## Capacity Check` exactly (independently re-derived here, not copied). No items require deferral on capacity grounds. **Capacity check outcome: pass, no WARN** — no Phasing Recommendation exists for this cycle (none was produced at release planning), so no phasing decision point applies at STEP 0.

## 1.4 Gate-Conditional Deferred Items

None. All 27 items are ungated at scope selection (per `release_plan.md ## Readiness` Gate-Condition Proximity Scan — no item in this cycle's scope touches the SI-02/PO-02/PO-04 gate family). `ST-01`'s and `ST-21`'s gate conditions (screener ≥60 days live; 30+ days AI endpoint usage, respectively) were both confirmed cleared at release planning (2026-08-08). No `status: deferred_at_planning` entries are required at `execution_state.json` initialisation for this cycle.

## 1.5 Minimum Capacity Buffer Floor (Advisory)

27.50 ÷ 28 (band ceiling) = **98.2% of confirmed capacity — exceeds the 95% buffer floor recommendation.**

This is expected and consistent with the explicit Product Owner instruction at release planning ("use full capacity") and matches the target zone of recent cycles (v9.1 27.50d, v9.2 27.55d). Surfaced per §1.5 as a "buffer floor exceeded" note (distinct from the harder over-100%-of-capacity WARN, which did not fire — capacity check outcome remains `pass`).

**Product Owner acknowledgement:** Proceed at full scope (27.50d / 98.2%). Rationale: explicit "use full capacity" instruction stands from release planning; accepted low in-sprint slippage buffer given the debt-clearance nature of scope (23 of 27 items are S/M-effort documentation/process/instrumentation items with low individual execution risk; the 4 items requiring live-environment evidence — ST-13, ST-21, ST-27, and the ST-08 visual-QA pass — are all small, isolated, single-owner tasks). — Product Owner, 2026-09-09.
