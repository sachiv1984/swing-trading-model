Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07
Cycle: 2026-09-07__release-v9.2

# Sprint Capacity — 2026-09-07__release-v9.2

## 1.1 Capacity Inputs

```
Sprint duration:    Single sprint (per release_plan.md sealed_assumptions.timebox)
Available FTE:      1 (solo developer + AI execution engine, full capacity)
Total capacity:     ~24–28 working-day-equivalent effort units (workforce_capacity.md, unchanged since 2026-07-17__scheduled)
Skill constraints:  None flagged in release_plan.md ## Execution Plan. Note: Metrics Definitions & Analytics Owner is named on both EPIC-01 (ST-01) and several EPIC-04/05 sign-offs (ST-26, ST-35, ST-40, ST-48) — no concurrency conflict since all are S/XS effort and sequenced across the sprint, not simultaneous.
```

## 1.2 Item Effort Mapping

Source: `stage4_backlog_slice.md` per-item `**Effort:**` field; band-to-day conversion per `release_plan.md ## Capacity Check` (XS≈0.15d, S≈0.5d, M≈2.5d, L≈3.5d). No `[ESTIMATE REQUIRED]` placeholders — all 56 items carry a defined effort band (confirmed by `release_plan.md`'s STEP 3.5 Local Model Integrity check).

### EPIC-01 — Arc 5 Compliance Score Low-Volume Advisory (0.50d)

| Item | Effort | Days |
|------|--------|------|
| ST-01 | S | 0.50 |

### EPIC-02 — Frontend Accessibility & Spec Compliance (0.95d)

| Item | Effort | Days |
|------|--------|------|
| ST-02 | XS | 0.15 |
| ST-03 | XS | 0.15 |
| ST-04 | XS | 0.15 |
| ST-05 | S | 0.50 |

### EPIC-03 — QA & CI Reliability Debt (4.45d)

| Item | Effort | Days |
|------|--------|------|
| ST-06 | XS | 0.15 |
| ST-07 | S | 0.50 |
| ST-08 | XS | 0.15 |
| ST-09 | S | 0.50 |
| ST-10 | S | 0.50 |
| ST-11 | XS | 0.15 |
| ST-12 | S | 0.50 |
| ST-13 | S | 0.50 |
| ST-14 | S | 0.50 |
| ST-15 | S | 0.50 |
| ST-16 | S | 0.50 |

### EPIC-04 — Governance Process Debt (13.00d)

| Item | Effort | Days |
|------|--------|------|
| ST-17 – ST-42 (26 items) | S (each) | 0.50 each — 13.00 total |

### EPIC-05 — Spec, Tech & Ops Debt (8.65d)

| Item | Effort | Days |
|------|--------|------|
| ST-43 | S | 0.50 |
| ST-44 | S | 0.50 |
| ST-45 | S | 0.50 |
| ST-46 | S | 0.50 |
| ST-47 | S | 0.50 |
| ST-48 | S | 0.50 |
| ST-49 | M | 2.50 |
| ST-50 | S | 0.50 |
| ST-51 | S | 0.50 |
| ST-52 | XS | 0.15 |
| ST-53 | S | 0.50 |
| ST-54 | S | 0.50 |
| ST-55 | S | 0.50 |
| ST-56 | S | 0.50 |

## 1.3 Total Effort vs Capacity

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 0.50 |
| EPIC-02 | 0.95 |
| EPIC-03 | 4.45 |
| EPIC-04 | 13.00 |
| EPIC-05 | 8.65 |
| **Total** | **27.55** |

27.55 days vs confirmed ~24–28 day band → **within capacity, no over-allocation.** No items require deferral on capacity grounds.

## 1.4 Gate-Conditional Deferred Items

None. All 56 items are ungated at scope selection — `BLG-FEAT-44`'s (ST-01) gate condition cleared at release planning STEP 1 (103 days elapsed since v4.1 ship, ≥ 90-day threshold) and its formal owner sign-off was resolved as a Pre-sprint Planning Required Decision (see `sprint_planning_notes.md`). No `status: deferred_at_planning` entries are required at `execution_state.json` initialisation for this cycle.

## 1.5 Minimum Capacity Buffer Floor (Advisory)

27.55 ÷ 28 (band ceiling) = **98.4% of confirmed capacity — exceeds the 95% buffer floor recommendation.**

This is expected and consistent with the explicit Product Owner instruction at release planning ("use full capacity") and matches the target zone of the three preceding cycles (v8.9 26.1d, v9.0 27.15d, v9.1 27.50d). Surfaced per §1.5 as a "buffer floor exceeded" note (distinct from the harder over-100%-of-capacity WARN, which did not fire — capacity check outcome remains `pass`).

**Product Owner acknowledgement:** Proceed at full scope (27.55d / 98.4%). Rationale: explicit "use full capacity" instruction stands from release planning; no in-sprint slippage buffer beyond the ~0.45d headroom to the band ceiling, but 51 of 56 items are S/XS-effort documentation/process items with low individual execution risk, and the two UI-facing EPICs (01/02, 1.45d combined) already cleared the design gate with locked artefacts — the risk profile does not warrant trimming scope. — Product Owner, 2026-09-07.
