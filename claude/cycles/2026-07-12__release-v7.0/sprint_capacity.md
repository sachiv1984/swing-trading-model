**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-13
**Cycle:** 2026-07-12__release-v7.0

---

# Sprint Capacity — 2026-07-12__release-v7.0

## 1.1 Capacity Inputs

```
Sprint duration:    ~12–14 working days (workforce_capacity.md, Effective 2026-05-27 baseline)
Available FTE:      1 (solo developer, evenings/weekends)
Total capacity:     ~12–14 capacity units (days)
Skill constraints:  None flagged — all 15 items are autonomous-class (spec authoring, backend, frontend); no scarce/role-locked skill named
```

## 1.2 Item Effort Mapping

| EPIC-ID | ST Item | Effort Estimate | Source |
|---------|---------|------------------|--------|
| EPIC-01 | ST-01 (BLG-SPEC-80) | S | `stage4_backlog_slice.md#ST-01` |
| EPIC-01 | ST-02 (BLG-FE-102) | S (~0.25–0.5 day) | `stage4_backlog_slice.md#ST-02` |
| EPIC-01 | ST-03 (BLG-FE-97) | S (~0.5 day) | `stage4_backlog_slice.md#ST-03` |
| EPIC-01 | ST-04 (BLG-QA-95) | S | `stage4_backlog_slice.md#ST-04` |
| EPIC-01 | ST-05 (BLG-FE-104) | S | `stage4_backlog_slice.md#ST-05` |
| EPIC-02 | ST-06 (BLG-SPEC-71) | S (~0.5 day) | `stage4_backlog_slice.md#ST-06` |
| EPIC-02 | ST-07 (BLG-BE-50) | S (~1 day) | `stage4_backlog_slice.md#ST-07` |
| EPIC-02 | ST-08 (BLG-FE-95) | XS (<1h) | `stage4_backlog_slice.md#ST-08` |
| EPIC-02 | ST-09 (BLG-FE-96) | XS (<1h) | `stage4_backlog_slice.md#ST-09` |
| EPIC-02 | ST-10 (BLG-SPEC-73) | XS (<1h) | `stage4_backlog_slice.md#ST-10` |
| EPIC-02 | ST-11 (BLG-BE-51) | XS (<1h) | `stage4_backlog_slice.md#ST-11` |
| EPIC-02 | ST-12 (BLG-BE-38) | XS (~2h) | `stage4_backlog_slice.md#ST-12` |
| EPIC-03 | ST-13 (BLG-FEAT-69) | M (~2 days) | `stage4_backlog_slice.md#ST-13` |
| EPIC-03 | ST-14 (BLG-FEAT-70) | M (~2 days) | `stage4_backlog_slice.md#ST-14` |
| EPIC-03 | ST-15 (BLG-FEAT-68) | S (~1 day) | `stage4_backlog_slice.md#ST-15` |

No `[ESTIMATE REQUIRED]` placeholders — all 15 items carry confirmed effort estimates, consistent with `release_plan.md ## Capacity Check` per-EPIC totals (EPIC-01 ~2.35 days, EPIC-02 ~2.15 days, EPIC-03 ~5.0 days).

## 1.3 Total Effort vs Capacity

Total estimated effort: ~9.5 days (5 EPIC-01 items + 7 EPIC-02 items + 3 EPIC-03 items).
Confirmed capacity: ~12–14 days.

**Effort is within capacity — no over-allocation.** ~9.5 of ~12–14 days used (~68–79% utilisation), consistent with the release plan's own scope-maximisation rationale (full, well-justified utilisation with buffer retained for estimate variance). No scope reduction required at STEP 3. Capacity check outcome from `release_plan.md` is `PASS`, not `warn` — no Product Owner over-capacity acknowledgement required.

## 1.4 Gate-Conditional Deferred Items

No ST items in `execution_state.json` are recorded as `status: deferred_at_planning` with a `gate_condition` for this cycle — the authoritative backlog slice contains exactly the 15 items above, all `include`. All gate-conditional candidates (SI-02/SI-04/PO-02/Arc-4/Arc-6-gated items, e.g. `BLG-FEAT-73/74/75`, `BLG-SPEC-35`, `BLG-GOV-28`) were excluded at release planning, not deferred at sprint planning — see `release_plan.md §Scope → Items explicitly deferred`. No `## Conditional (Deferred)` section applies.

---

**Outcome: PASS.** No phasing recommendation required.
