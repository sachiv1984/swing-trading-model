**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-14
**Cycle:** 2026-09-14__release-v9.4

# Sprint Capacity — 2026-09-14__release-v9.4

## 1.1 Capacity Inputs

```
Sprint duration:    single sprint (~1–2 calendar days between sprint starts per workforce_capacity.md Effective 2026-07-17 cadence declaration)
Available FTE:      Solo developer, evenings/weekends (workforce_capacity.md)
Total capacity:     ~24–28 working-day-equivalents (confirmed band, unchanged since 2026-07-17; re-baseline review deferred to BLG-GOV-328 rather than decided ad hoc this cycle)
Skill constraints:  None flagged — Metrics Definitions owner and Backend Engineering are the only historically-scarce skills and neither is double-booked this cycle (see EPIC ownership table below)
```

## 1.2 Item Effort Mapping

Source: `release_plan.md ## Execution Plan` / `## Capacity Check` (schema v2). Effort bands and day-equivalents per `workforce_capacity.md` Canonical Effort Band → Days Conversion Table (XS=0.15d, S=0.5d, M=2.5d, L=3.5d). No `[ESTIMATE REQUIRED]` placeholders — all 28 items carry a resolved effort estimate in `stage4_backlog_slice.md`.

| EPIC | Items | Subtotal (days) |
|------|-------|-------------------|
| EPIC-01 — Backend & Platform Engineering Debt | 5 | 8.50 |
| EPIC-02 — QA & Test Coverage Debt | 3 | 0.45 |
| EPIC-03 — Operations & Security Debt | 4 | 1.65 |
| EPIC-04 — Spec, Documentation & Financial Reporting Debt | 5 | 5.45 |
| EPIC-05 — Governance Process & AI Compliance Debt | 6 | 7.00 |
| EPIC-06 — Frontend, UX & Product Debt | 5 | 4.50 |
| **Total** | **28** | **27.55** |

## 1.3 Total Effort vs Capacity

27.55 days vs confirmed ~24–28 day band. **Within band — no over-allocation.** Sits at the top of the band (98.4% of the 28-day ceiling), matching the Product Owner's explicit "use full capacity" instruction recorded at Release Planning (`release_plan.md`, `cycle_summary.md`). Capacity check outcome carried from Release Planning: **pass, no WARN**. No STEP 3 scope trim required.

## 1.4 Gate-Conditional Deferred Items

No ST items in this sprint's scope are conditionally deferred (`status: deferred_at_planning` with a `gate_condition`) — the authoritative backlog slice's 28 items enter the sprint in full; no `execution_state.json` for this cycle carries a pre-existing deferred entry to preserve. See `sprint_planning_notes.md ## Deferred Items` for the items excluded at Release Planning (out of this engine's scope to re-litigate).

## 1.5 Minimum Capacity Buffer Floor (Advisory)

`27.55 ÷ 28 (confirmed capacity ceiling) = 0.984` — **exceeds the 95% buffer floor recommendation** (§1.5). Recorded as an explicit "buffer floor exceeded" note, distinct from the harder over-100%-of-capacity WARN (not triggered — 27.55 < 28).

**Product Owner acknowledgement:** The buffer-floor overage is a direct, already-disclosed consequence of the Product Owner's explicit "use full capacity" instruction given at Release Planning (`release_plan.md`, `cycle_summary.md`, 2026-09-14) — the scope was deliberately curated to the top of the confirmed band, not arrived at incidentally. Proceeding with full 28-item scope is treated as the Product Owner's standing acknowledgement of the buffer-floor overage; no separate trim is warranted. Ties `2026-09-07__release-v9.2`'s exact 27.55-day figure, which also ran at this same ratio without in-sprint capacity incident.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-09-14 | Initial publication — capacity baseline for 2026-09-14__release-v9.4, 27.55d / 28-item scope, pass/no-WARN, buffer floor exceeded (acknowledged). |
