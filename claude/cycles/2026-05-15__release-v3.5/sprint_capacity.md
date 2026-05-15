**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-15
**Cycle:** 2026-05-15__release-v3.5

---

# Sprint Capacity — v3.5 Arc 3 Completion + Arc 4 Foundation

---

## 1.1 Capacity Inputs

```
Sprint duration:    2 sprints (~5–6 days Sprint 1, ~6–8 days Sprint 2)
Available FTE:      1 (solo dev — evenings pace)
Total capacity:     ~10–12 days across both sprints
Skill constraints:  Strategy Rules & System Intent Owner required for ST-01 (§13 review);
                    Head of UX & Design required for ST-03 (paper trading UX spec — already created at design gate);
                    QA Lead required for ST-10 sign-off;
                    Head of UX & Design + Product Owner required for ST-04 sign-off
```

Source: `release_plan.md ## Capacity Check` + `workforce_capacity.md`
Scored initiatives: 0 matching entries (pre-Arc 3/4 file). All estimates are inline.

---

## 1.2 Item Effort Mapping

### Sprint 1

| EPIC | ST Item | Effort estimate | Source |
|------|---------|-----------------|--------|
| EPIC-04 | ST-11 (BLG-GOV-22 sprint_planning_prompt.md patch) | S (~0.5 day) | Inline |
| EPIC-04 | ST-12 (execution_prompt.md deviation advisory patches) | S (~0.5 day) | Inline |
| EPIC-04 | ST-13 (Sprint close / LL formatting improvements) | S (~0.5 day) | Inline |
| EPIC-03 | ST-07 (BLG-SPEC-29 sessionStorage correction) | XS (~0.25 day) | Inline |
| EPIC-03 | ST-08 (BLG-SPEC-30 HTTP verb correction) | XS (~0.25 day) | Inline |
| EPIC-03 | ST-09 (BLG-SPEC-31 React Query v5 scan) | S (~0.5 day) | Inline |
| EPIC-03 | ST-10 (BLG-QA-19 research view regression protocol) | S (~0.5 day) | Inline |
| EPIC-01 | ST-01 (§13 compliance review) | XS (~0.25 day) | Inline |
| **Sprint 1 total** | | **~3.25–4.25 days** | |

### Sprint 2 (conditional on ST-01 outcome)

#### Scenario A — §13 PASS (IT-06 in scope)

| EPIC | ST Item | Effort estimate | Source |
|------|---------|-----------------|--------|
| EPIC-01 | ST-02 (Alpaca backend sync service) | M (~2–3 days) | Inline |
| EPIC-01 | ST-03 (Paper positions display panel) | M (~2 days) | Inline |
| EPIC-02 | ST-04 (Arc 4 data requirements capture) | S (~0.5 day) | Inline |
| EPIC-02 | ST-05 (PO-01 backend calculation service) | M–H (~3–4 days) | Inline |
| EPIC-02 | ST-06 (PO-01 frontend comparison view) | M (~2 days) | Inline |
| **Sprint 2 total (§13 PASS)** | | **~9.5–11.5 days** | |

#### Scenario B — §13 FAIL (EPIC-01 reduced to ST-01 only)

| EPIC | ST Item | Effort estimate | Source |
|------|---------|-----------------|--------|
| EPIC-02 | ST-04 (Arc 4 data requirements capture) | S (~0.5 day) | Inline |
| EPIC-02 | ST-05 (PO-01 backend calculation service) | M–H (~3–4 days) | Inline |
| EPIC-02 | ST-06 (PO-01 frontend comparison view) | M (~2 days) | Inline |
| **Sprint 2 total (§13 FAIL)** | | **~5.5–6.5 days** | |

---

## 1.3 Total Effort vs Capacity

### Scenario A (§13 PASS)

| Metric | Value |
|--------|-------|
| Sprint 1 estimated effort | ~3.25–4.25 days |
| Sprint 2 estimated effort | ~9.5–11.5 days |
| Total estimated effort | ~12.75–15.75 days |
| Confirmed capacity | ~10–12 days |
| **Over-allocation** | **~2–4 days** |
| Natural release valve | ST-06 (PO-01 frontend) phaseable to v3.6 — saves ~2 days |
| Adjusted total (ST-06 deferred) | ~10.75–13.75 days — within range with phasing |

### Scenario B (§13 FAIL)

| Metric | Value |
|--------|-------|
| Sprint 1 estimated effort | ~3.25–4.25 days |
| Sprint 2 estimated effort | ~5.5–6.5 days |
| Total estimated effort | ~8.75–10.75 days |
| Confirmed capacity | ~10–12 days |
| **Over-allocation** | None — within capacity |

---

## Capacity Outcome

**WARN** — Total effort under Scenario A (13–16 days) exceeds confirmed capacity (~10–12 days). Phasing options:
1. Defer ST-06 (PO-01 frontend, M effort) to v3.6 if Sprint 2 capacity is tight — releases ~2 days.
2. §13 FAIL (RISK-01) is the primary release valve: eliminates ~4–5 days of Sprint 2 scope automatically.

**Product Owner acknowledgement required before sprint seals.** See `sprint_planning_notes.md ## Capacity WARN Acknowledgement`.
