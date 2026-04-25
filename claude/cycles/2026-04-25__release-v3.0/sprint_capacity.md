Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-04-25
Cycle: 2026-04-25__release-v3.0

---

# Sprint Capacity — v3.0 Arc 1 Remainder: Screener Engine & Results Page

---

## 1. Capacity Inputs

```
Sprint duration:    2 sprints (Sprint 1 ~10 working days, Sprint 2 ~7 working days)
Available FTE:      1.0 (solo dev — all roles served by execution engine)
Total capacity:     ~17 working days across both sprints
Skill constraints:  None — all required skills available (backend, frontend, governance, QA)
```

**Source:** `claude/roadmap/workforce_capacity.md` — solo dev, historical velocity 1.00 across 6 cycles.
**Capacity outcome (release planning):** WARN — DS-01 H effort + 16 stories; acknowledged by Product Owner at planning.

---

## 2. Item Effort Mapping

| EPIC | Stories | Effort Band | Estimated Days | Sprint |
|------|---------|-------------|----------------|--------|
| EPIC-01 | ST-01–ST-04 (4 stories) | H (DS-01 roadmap) | ~4–6 days | Sprint 1 |
| EPIC-04 | ST-12–ST-16 (5 stories) | 5 × S | ~2–3 days | Sprint 1 |
| **Sprint 1 total** | **9 stories** | H + 5×S | **~6–9 days** | — |
| EPIC-02 | ST-05–ST-07 (3 stories) | M + S + S | ~2–3 days | Sprint 2 |
| EPIC-03 | ST-08–ST-11 (4 stories) | 4 × S | ~2 days | Sprint 2 |
| **Sprint 2 total** | **7 stories** | M + 6×S | **~4–5 days** | — |
| **Grand total** | **16 stories** | — | **~10–14 days** | — |

---

## 3. Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Available capacity (Sprint 1) | ~10 working days |
| Available capacity (Sprint 2) | ~7 working days |
| Total available capacity | ~17 working days |
| Estimated effort (Sprint 1) | ~6–9 days |
| Estimated effort (Sprint 2) | ~4–5 days |
| Total estimated effort | ~10–14 days |
| Estimated utilisation | ~60–82% |
| Over-allocation | No — within capacity at historical 1.00 velocity |

**Capacity WARN acknowledged:** Product Owner confirmed 2026-04-25 — DS-01 H effort and 16 total stories is the most ambitious v3.0 scope. Historical velocity at 1.00 over 6 cycles supports delivery. Sprint 1 is the heavier sprint; EPIC-04 (governance patches) runs independently of EPIC-01 and can be executed in parallel to reduce Sprint 1 critical path.

---

## 4. Skill Constraints

No scarce skill constraints. All required domains covered:
- Backend engineering (EPIC-01): Head of Engineering + Backend Engineering Patterns Owner
- Frontend (EPIC-02, EPIC-03 ST-11): Base44 Frontend Prompt Owner
- Ops/QA (EPIC-03): Infrastructure & Operations Owner + QA & Testing Owner
- Governance/docs (EPIC-04): Head of Specs Team + PMO Lead

**RISK-01 resolved:** Head of Engineering confirms ST-02 (OHLCV pipeline, M) and ST-03 (ATR+regime+scoring, M) are appropriately scoped given BLG-SPEC-21 deterministic spec and BLG-QA-09 test data library. No further story split required.
