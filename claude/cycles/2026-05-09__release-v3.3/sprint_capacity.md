**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-10
**Cycle:** 2026-05-09__release-v3.3

---

# Sprint Capacity — v3.3 Arc 3 In-Trade Risk Management

---

## 1.1 Capacity Inputs

```
Sprint duration:    2 sprints × ~8–12 working days (solo-dev evening/weekend model)
Available FTE:      ~1 FTE part-time (solo dev)
Sprint 1 capacity:  ~8–12 days
Sprint 2 capacity:  ~8–12 days
Cycle capacity:     ~16–24 days (mid-point ~20 days)
Skill constraints:  Backend Engineering (primary), Frontend, Spec & Governance authorship,
                    QA & Testing (Playwright)
```

*Source: `release_plan.md ## Capacity Check`; `workforce_capacity.md` (sprint-level capacity reflects consistent solo-dev model since v1.7).*

---

## 1.2 Item Effort Mapping

| EPIC | ST Item | Type | Estimate | Sprint |
|------|---------|------|----------|--------|
| EPIC-01 | ST-01 — Positions data model + migration | Backend / Data Model | XS–S (~0.5–1d) | 1 |
| EPIC-01 | ST-02 — Position lifecycle state machine backend | Backend / Service | S–M (~1–2d) | 1 |
| EPIC-01 | ST-03 — Position lifecycle state frontend display | Frontend | S–M (~1–2d) | 1 |
| **EPIC-01 subtotal** | | | **~2.5–5d** | **Sprint 1** |
| EPIC-02 | ST-04 — Grace Period Decision Support backend | Backend | XS–S (~0.5–1d) | 2 |
| EPIC-02 | ST-05 — Grace Period Decision Support frontend | Frontend | S–M (~1–2d) | 2 |
| EPIC-02 | ST-06 — Stop Management Workflow backend | Backend | XS–S (~0.5–1d) | 2 |
| EPIC-02 | ST-07 — Stop Management Workflow frontend | Frontend | S–M (~1–2d) | 2 |
| **EPIC-02 subtotal** | | | **~3–6d** | **Sprint 2** |
| EPIC-03 | ST-08 — PT-02 research API contract + provenance spec | Specification | S–M (~1–2d) | 1 |
| EPIC-03 | ST-09 — PT-02 canonical research view spec + UX spec | Specification + UX | S–M (~1–2d) | 1 |
| EPIC-03 | ST-10 — Research view test scenario library + protocol | QA | XS–S (~0.5–1d) | 1 |
| EPIC-03 | ST-11 — Entry checklist Playwright E2E tests | QA / Test Automation | S–M (~1–2d) | 1 |
| EPIC-03 | ST-12 — Research integration tests + latency + security + governance | QA + Ops + Governance | S–M (~1–2d) | 1 |
| **EPIC-03 subtotal** | | | **~4.5–9d** | **Sprint 1** |
| EPIC-04 | ST-13 — execution_prompt governance patches (OA-01/02) | Governance | XS (~0.5d) | 1 |
| EPIC-04 | ST-14 — Policy patches: design gate check + deferral policy (OA-03/05) | Governance | XS (~0.5d) | 1 |
| EPIC-04 | ST-15 — PT-05 entry checklist §13 compliance review | Governance | XS (~0.25d) | 1 |
| EPIC-04 | ST-16 — Feature flag rollout (BLG-FEAT-13 mandatory) | Platform Feature | S–M (~1–2d) | 2 |
| EPIC-04 | ST-17 — Trade plan abandonment + badges + quick wins | Product Feature + Frontend | M–L (~2–3d) | 2 |
| **EPIC-04 subtotal** | | | **~4.25–6.25d** | **Sprint 1+2** |

---

## 1.3 Total Effort vs Capacity

| Metric | Sprint 1 | Sprint 2 | Cycle Total |
|--------|----------|----------|-------------|
| Estimated effort (low) | ~7.5d | ~6.75d | ~14.25d |
| Estimated effort (high) | ~14d | ~11.25d | ~25.25d |
| Mid-point estimate | ~10.75d | ~9d | ~19.75d |
| Available capacity | ~8–12d | ~8–12d | ~16–24d |
| Mid-point capacity | ~10d | ~10d | ~20d |

**Capacity gate outcome: ⚠ WARN**

Mid-point effort (~19.75d) is approximately equal to mid-point capacity (~20d). Plan is feasible but leaves minimal margin. The phasing recommendation from the release plan has been adopted:

- **Sprint 1 (10 stories):** EPIC-01 (ST-01–03) + EPIC-03 (ST-08–12) + EPIC-04 ST-13/14/15
- **Sprint 2 (7 stories):** EPIC-02 (ST-04–07) + EPIC-04 ST-16/17

If Sprint 1 capacity is exceeded, EPIC-04 ST-15 (XS) can move to Sprint 2 without blocking dependencies.

**Product Owner capacity WARN acknowledgement: [REQUIRED — see sign-off gate]**
