**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-16
**Cycle:** 2026-09-15__release-v9.5

# Sprint Capacity — 2026-09-15__release-v9.5

## 1.1 Capacity Inputs

```
Sprint duration:    single sprint (~1–2 calendar days between sprint starts per workforce_capacity.md Effective 2026-07-17 cadence declaration)
Available FTE:      Solo developer, evenings/weekends (workforce_capacity.md)
Total capacity:     ~24–28 working-day-equivalents (confirmed band, unchanged since 2026-07-17; re-baseline review deferred to filed backlog item BLG-GOV-328 rather than decided ad hoc this cycle)
Skill constraints:  None flagged as double-booked. RISK-05 notes ST-37/ST-38 (EPIC-05) both edit `workforce_capacity.md` — sequenced, not parallel (see `sprint_planning_notes.md`).
```

## 1.2 Item Effort Mapping

Source: `release_plan.md ## Execution Plan` / `## Capacity Check` (schema v2). Effort bands and day-equivalents per `workforce_capacity.md` Canonical Effort Band → Days Conversion Table (XS=0.15d, S=0.5d, M=2.5d, L=3.5d). No `[ESTIMATE REQUIRED]` placeholders — all 43 items carry a resolved effort estimate in `stage4_backlog_slice.md` (confirmed at Release Planning's own Stage 3.5 Local Model Integrity check).

| EPIC | Items | Subtotal (days) |
|------|-------|-------------------|
| EPIC-01 — Backend & Platform Engineering Debt | 4 | 6.00 |
| EPIC-02 — Operations & Security Debt | 10 | 6.30 |
| EPIC-03 — QA & Test Coverage Debt | 7 | 3.20 |
| EPIC-04 — Spec & Documentation Debt | 9 | 7.34 |
| EPIC-05 — Governance Process Debt | 9 | 3.95 |
| EPIC-06 — Frontend & UX Debt | 4 | 1.20 |
| **Total** | **43** | **27.99** |

## 1.3 Total Effort vs Capacity

27.99 days vs confirmed ~24–28 day band. **Within band — no over-allocation.** Sits at the exact top of the band (99.96% of the 28-day ceiling — the tightest full-capacity fit on record), matching the Product Owner's explicit "use full capacity" instruction recorded at Release Planning (`release_plan.md`, `cycle_summary.md`). Capacity check outcome carried from Release Planning: **pass, no WARN**. No STEP 3 scope trim required.

## 1.4 Gate-Conditional Deferred Items

No ST items in this sprint's scope are conditionally deferred (`status: deferred_at_planning` with a `gate_condition`) — all 43 items in the authoritative backlog slice enter the sprint in full. See `sprint_planning_notes.md ## Deferred Items` for the items excluded at Release Planning (out of this engine's scope to re-litigate).

## 1.5 Minimum Capacity Buffer Floor (Advisory)

`27.99 ÷ 28 (confirmed capacity ceiling) = 0.9996` — **exceeds the 95% buffer floor recommendation** (§1.5), and is in fact the tightest fit against the ceiling of any cycle on record (edging out `2026-09-14__release-v9.4`'s 98.4%). Recorded as an explicit "buffer floor exceeded" note, distinct from the harder over-100%-of-capacity WARN (not triggered — 27.99 < 28).

**Product Owner acknowledgement:** The buffer-floor overage is a direct, already-disclosed consequence of the Product Owner's explicit "use full capacity" instruction given at Release Planning (`release_plan.md`, `cycle_summary.md`, 2026-09-15) — the scope was deliberately curated to the top of the confirmed band via the canonical P1-first/P2-first/category-balanced selection method, not arrived at incidentally. Proceeding with the full 43-item scope is treated as the Product Owner's standing acknowledgement of the buffer-floor overage; no separate trim is warranted.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-09-16 | Initial publication — capacity baseline for 2026-09-15__release-v9.5, 27.99d / 43-item scope, pass/no-WARN, buffer floor exceeded (acknowledged). |
