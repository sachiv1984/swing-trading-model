**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-06
**Cycle:** 2026-03-06__release-v1.9

# Sprint Capacity — 2026-03-06__release-v1.9

---

## 1. Capacity Inputs

| Parameter | Value | Source |
|-----------|-------|--------|
| Developer type | Solo developer | workforce_capacity.md + stage4_5_capacity_check.md |
| Working pace | Evenings + weekends | Prior cycle pattern (confirmed) |
| Available hours/week | ~10–15 hours | stage4_5_capacity_check.md §1 |
| Sprint duration | Open (no fixed timebox; solo dev project) | No --timebox flag at invocation |
| Total confirmed capacity (1 sprint, 1–2 weeks) | ~15–25 hours | stage4_5_capacity_check.md §1 |
| Skill constraints | All skills self-held (solo dev) | workforce_capacity.md |
| Metrics Definitions owner | Confirmed available (LL-05 PASS) | stage4_5_capacity_check.md §4 |

---

## 2. Item Effort Mapping

| ST-ID | EPIC | Title | Estimate (low–high hrs) | Mid-point | Delegation Class |
|-------|------|-------|------------------------|-----------|-----------------|
| ST-01 | EPIC-01 | Canonicalise Basic Compliance Metrics | 6–8 | 7 | delegated_backend + delegated_frontend |
| ST-02 | EPIC-01 | Structured Trade Reflection Template | 8–12 | 10 | delegated_backend + delegated_frontend |
| ST-03 | EPIC-02 | Cohort Analysis | 8–12 | 10 | delegated_backend + delegated_frontend |
| ST-04 | EPIC-02 | R-Multiple Distribution Report | 6–10 | 8 | delegated_backend + delegated_frontend |
| ST-05 | EPIC-03 | Dashboard Homepage / Session Summary | 6–10 | 8 | delegated_frontend |
| ST-06 | EPIC-04 | Drawdown Data Source Spec Alignment | 1–3 | — | **COMPLETE** (resolved 2026-03-06) |
| ST-07 | EPIC-04 | Risk Dashboard Backend: US Currency Conversion | 3–6 | 4.5 | delegated_backend |
| ST-08 | EPIC-04 | Risk Dashboard Frontend: Error States & Entity Fallback | 2–4 | 3 | delegated_frontend |
| ST-09 | EPIC-04 | Risk Dashboard Frontend: Table and Column Fixes | 2–4 | 3 | delegated_frontend |
| ST-10 | EPIC-04 | Risk Dashboard Frontend: HeatGauge and Cosmetic Fixes | 1–3 | 2 | delegated_frontend |
| ST-11 | EPIC-05 | Canonical Test Scenario Library Phase 1 | 6–10 | 8 | delegated_qa |
| ST-12 | EPIC-05 | Canonical Test Scenario Library Phase 2 | 4–8 | 6 | delegated_qa |
| ST-13 | EPIC-05 | Service Layer Test Coverage Standard | 3–6 | 4.5 | delegated_backend + delegated_qa |
| ST-14 | EPIC-06 | Canonical Terms Glossary | 2–4 | 3 | autonomous |
| ST-15 | EPIC-06 | AI-Assisted Workflow Governance Policy | 2–4 | 3 | autonomous |
| ST-16 | EPIC-06 | Document GET /market/status Endpoint | 2–4 | 3 | autonomous |
| ST-17 | EPIC-06 | Create settings_model.md | 2–4 | 3 | autonomous |
| ST-18 | EPIC-06 | Define Error Response Standard | 2–4 | 3 | autonomous |
| ST-19 | EPIC-06 | Spec/Doc Debt Small Fixes (7 items) | 2–4 | 3 | autonomous |

**ST-06 pre-completed:** effort consumed = ~2 hrs (not counted against sprint capacity).

---

## 3. Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| In-scope items (excluding ST-06) | 18 |
| Total estimated effort — low | ~62 hours |
| Total estimated effort — high | ~113 hours |
| Total estimated effort — mid | ~90 hours |
| Confirmed sprint capacity (1–2 weeks) | ~15–25 hours |
| Over-allocation factor | ~3–6x |
| Over-allocation status | **YES — requires Product Owner explicit acceptance** |

---

## 4. Over-Allocation Advisory

The v1.9 scope is a full release — 6 EPICs, 19 story items, ~90 hours mid-estimate. At solo-dev evenings-and-weekends pace (10–15 hrs/week), this equates to approximately 6–9 weeks of elapsed calendar time.

**This is expected and pre-anticipated.** The stage4_5_capacity_check.md §3 explicitly noted: "Product Owner to confirm at sprint planning whether all 6 EPICs are targeted in a single sprint, or whether a phased approach is preferred. Governance supports multi-sprint within a release planning cycle."

### Phasing Options (for Product Owner consideration)

**Option A — Single Sprint (6–9 weeks elapsed)**
All 18 remaining items included. Over-allocation accepted. No items deferred.

**Option B — Phased approach (2 sprints)**
- Sprint 1: EPIC-04 (defect resolution — highest ROI, immediately visible) + EPIC-05 Phase 1 (test infra unblocks scenario execution) + EPIC-06 (doc hygiene — autonomous, can run in parallel) ≈ 30–40 hrs
- Sprint 2: EPIC-01 + EPIC-02 + EPIC-03 (new user value features) + EPIC-05 Phase 2 ≈ 40–50 hrs

Product Owner decision required at sprint sign-off. Sprint backlog reflects full scope pending that decision; items can be deferred from sign-off if Option B is chosen.

---

## 5. Pre-Sprint pip-audit Result

**Outcome: clean — 0 vulnerabilities** (run 2026-03-06 against backend/requirements.txt)

No CVE-related scope additions required.

---

## 6. Summary

| Check | Result |
|-------|--------|
| Skill constraints | None — all skills self-held |
| LL-05 (Metrics Definitions owner) | PASS |
| Estimates complete | All 18 remaining items have estimates |
| Over-allocation | YES — ~3–6x; Product Owner acceptance required |
| pip-audit | Clean |
