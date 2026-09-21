**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-21
**Cycle:** 2026-09-21__release-v9.6

# Sprint Capacity — 2026-09-21__release-v9.6

## 1.1 Capacity Inputs

```
Sprint duration:    single sprint (~1–2 calendar days between sprint starts per workforce_capacity.md, effective 2026-07-17 cadence declaration)
Available FTE:      Solo developer, evenings/weekends (workforce_capacity.md)
Total capacity:     ~24–28 working-day-equivalents (confirmed band, unchanged since 2026-07-17; the re-baseline review is ST-29 / BLG-GOV-328 in this very sprint)
Skill constraints:  Two human-access dependencies (ST-16 Actions-write token + Telegram receipt; ST-22 live-DB write access), one live-staging dependency (ST-18), and one owner decision on live behaviour (ST-09). None is a double-booking of a role; all are hand-offs the sole developer cannot self-serve.
```

## 1.2 Item Effort Mapping

Source: `release_plan.md ## Execution Plan` / `## Capacity Check` (schema v2). Day-equivalents per each item's own `**Effort:**` field, falling back to the `workforce_capacity.md` Canonical Effort Band → Days table (XS=0.15d, S=0.5d, M=2.5d, L=3.5d). No `[ESTIMATE REQUIRED]` placeholders — all 32 items carry a resolved estimate (confirmed at Release Planning's Stage 3.5 integrity check and re-confirmed here against the sealed slice).

| EPIC | Items | Subtotal (days) |
|------|-------|-------------------|
| EPIC-01 — Product Features & Frontend Build-and-Ship | 6 | 6.75 |
| EPIC-02 — Financial Reporting & Records Integrity | 2 | 2.75 |
| EPIC-03 — Backend & Platform Engineering Debt | 5 | 4.55 |
| EPIC-04 — Operations & Security Debt | 4 | 1.90 |
| EPIC-05 — QA & Test Coverage Debt | 4 | 3.65 |
| EPIC-06 — Spec & Documentation Debt | 5 | 4.15 |
| EPIC-07 — Governance Process Debt | 6 | 4.25 |
| **Total** | **32** | **28.00** |

## 1.3 Total Effort vs Capacity

28.00 days vs confirmed ~24–28 day band. **Within band — no over-allocation.** Sits at the exact ceiling (100.0% of the 28-day ceiling), matching the Product Owner's explicit "use full capacity" instruction recorded at Release Planning. Sensitivity: 27.90 days under a band-letter-only reading of the same 32 items. Capacity check outcome carried from Release Planning: **pass, no WARN** (the WARN threshold is > 28 days), so no `### Phasing Recommendation` exists and none was required. No STEP 3 scope trim required.

**Effort-uncertainty note.** The 28.00 figure is a midpoint total, not a guaranteed ceiling. Three items carry sizing risk in the upward direction — ST-08 (`BLG-FR-05`, likely a new table/migration; RISK-02), ST-09 (`BLG-BE-119`, code scope depends on which formula is ratified; RISK-03) and ST-18 (`BLG-QA-171`, a bare `M`). With zero buffer, any overrun is absorbed by returning items to the backlog in reverse selection order (last-selected first), never silently (RISK-08).

## 1.4 Gate-Conditional Deferred Items

No ST items in this sprint's scope are conditionally deferred (`status: deferred_at_planning` with a `gate_condition`) — all 32 items in the authoritative backlog slice enter the sprint in full, and no within-sprint date gate applies to any included item (`Status at sprint open: ready` throughout). Items conditionally excluded at Release Planning (`BLG-FEAT-59`/`60`/`63`, `BLG-FE-84`, `BLG-GOV-140`/`141`/`142`, `BLG-OPS-88` — date gate 2026-09-24) are not in this sprint's slice; see `sprint_planning_notes.md ## Deferred Items`.

## 1.5 Minimum Capacity Buffer Floor (Advisory)

`28.00 ÷ 28 (confirmed capacity ceiling) = 1.000` — **exceeds the 95% buffer floor recommendation** (§1.5) by 5 percentage points, i.e. a 0% standing buffer against the ceiling (scope is 1.4 days over the 95% floor of 26.6 days). Recorded as an explicit "buffer floor exceeded" note, distinct from the harder over-100%-of-capacity WARN (not triggered — 28.00 is not > 28). This matches the tightest fit on record (v9.5 was 99.96%).

**Product Owner acknowledgement (proceed / trim):** *Proceed.* The buffer-floor overage is a direct, already-disclosed consequence of the Product Owner's explicit "use full capacity" instruction given at Release Planning (`release_plan.md` RISK-08, `cycle_summary.md`, 2026-09-21) — the scope was deliberately curated to the top of the confirmed band via the P2-first / category-balanced selection method, not arrived at incidentally. Recorded agent-mediated, on the same basis as the v9.5 seal. Mitigation is the reverse-selection-order return rule above rather than a scope trim.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-09-21 | Initial publication — capacity baseline for 2026-09-21__release-v9.6, 28.00d / 32-item scope, pass/no-WARN, buffer floor exceeded (acknowledged). |
