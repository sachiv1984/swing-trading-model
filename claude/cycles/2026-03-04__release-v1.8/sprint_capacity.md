**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Sprint Capacity — 2026-03-04__release-v1.8

## Release: v1.8 — Risk Dashboard

---

## 1. Capacity Inputs

| Field | Value | Source |
|-------|-------|--------|
| Sprint model | Milestone-based (no hard calendar deadline) | Stage 4.5 capacity check — WARN accepted in standard mode |
| Available FTE | 1 (solo developer) | workforce_capacity.md |
| Working pattern | Evenings (~1–1.5 hrs/session) | Prior release pattern (v1.6.1, v1.7) |
| Effective throughput | ~1–1.5 hours per working day | Observed velocity |
| Equivalent capacity | ~10–15 hrs over 2 weeks (~1.5–2 full-time days) | Derived |
| Extended capacity (6 weeks) | ~60–90 hrs (~8–12 full-time days) | Milestone-based envelope |
| Skill availability | Full-stack, spec authoring, CI/DevOps, QA authoring | All within single-developer capability |
| Scarce skills | None — no scarce skill conflicts per workforce_capacity.md | |

**Capacity model:** Milestone-based. EPIC-01 (Risk Dashboard) is the release gate. EPICs 02–04 trail within the same release. No hard timebox; delivery confirmed when each EPIC is done.

---

## 2. Item Effort Mapping

| Item | EPIC | Effort Estimate | Skill Domain |
|------|------|-----------------|--------------|
| ST-01 | EPIC-01 | ~0.5 day | Spec authoring (**COMPLETE** — done at Design Gate) |
| ST-02 | EPIC-01 | ~0.25 day | Backend engineering |
| ST-03 | EPIC-01 | ~2–3 days | Frontend implementation |
| ST-04 | EPIC-01 | ~0.5 day | QA scenario authoring |
| ST-05 | EPIC-02 | ~1 day | Backend/CI engineering + QA |
| ST-06 | EPIC-02 | ~0.5 day | Backend/CI engineering |
| ST-07 | EPIC-02 | ~0.5 day | CI/DevOps |
| ST-08 | EPIC-02 | ~0.5 day | CI/DevOps |
| ST-09 | EPIC-03 | ~0.5 day | Spec authoring |
| ST-10 | EPIC-03 | ~1 day | API spec / reference |
| ST-11 | EPIC-04 | ~0.5 day | Governance documentation |
| ST-12 | EPIC-04 | ~0.5 day | API documentation |

---

## 3. Effort Totals by EPIC

| EPIC | Items | Total Effort | Notes |
|------|-------|-------------|-------|
| EPIC-01 | ST-01–ST-04 | ~3.25–4.25 days | ST-01 already done; net remaining ~2.75–3.75 days |
| EPIC-02 | ST-05–ST-08 | ~2.5 days | All independent of EPIC-01 |
| EPIC-03 | ST-09–ST-10 | ~1.5 days | ST-10 independent; ST-09 now unblocked |
| EPIC-04 | ST-11–ST-12 | ~1 day | Both fully independent |
| **Total** | **12** | **~8.25–9.25 days** | |

---

## 4. Capacity Assessment

| Dimension | Value | Status |
|-----------|-------|--------|
| Total estimated effort | ~8.25–9.25 days | — |
| Strict 2-week capacity | ~1.5–2 full-time days | ❌ Over-allocated |
| Milestone-based capacity (~6 weeks) | ~10–12 full-time days | ✅ Within bounds |
| Over-allocation (strict) | Yes | Accepted by Product Owner — milestone-based delivery |
| Skill conflicts | None | ✅ |

**Product Owner acceptance of over-allocation:** Recorded. Delivery is milestone-based; EPIC-01 is the release gate. EPICs 02–04 trail within the v1.8 release window. No hard deadline imposed.

---

## 5. Skill Silo Assessment (from workforce_capacity.md)

Governance load ~21% (ST-09, ST-11, ST-12 = ~1.5 days of ~8 total). Within 20–60% bounds. No alert triggered. Engineering-heavy sprint (frontend, backend, CI) with supporting governance tasks. Well-balanced per FinOps & Resource Architect assessment.
