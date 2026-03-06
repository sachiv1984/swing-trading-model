**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-06
**Cycle:** 2026-03-06__release-v1.9

# Design Gate Record — 2026-03-06__release-v1.9

## Gate Status: PASSED

Completed: 2026-03-06
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed (design artefacts approved)
Head of Specs Team: confirmed (frontend specs lifecycle-compliant)

---

## Item Classification Summary

| ST-ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|-------|-------|----------------|-----------------|---------------|-------------|
| ST-01 | Compliance Metrics | Design Required | `docs/design/2026-03-06__release-v1.9/compliance-metrics/ux_spec.md` | `analytics.md` v1.3 (§17) | ✅ Cleared |
| ST-02 | Trade Reflection Template | Design Required | `docs/design/2026-03-06__release-v1.9/trade-reflection/ux_spec.md` | `trade_reflection.md` v0.1 (new) | ✅ Cleared |
| ST-03 | Cohort Analysis | Design Required | `docs/design/2026-03-06__release-v1.9/cohort-analysis/ux_spec.md` | `analytics.md` v1.3 (§15) | ✅ Cleared |
| ST-04 | R-Multiple Distribution | Design Required | `docs/design/2026-03-06__release-v1.9/r-multiple-distribution/ux_spec.md` | `analytics.md` v1.3 (§16) | ✅ Cleared |
| ST-05 | Dashboard Homepage | Design Required | `docs/design/2026-03-06__release-v1.9/dashboard-home/ux_spec.md` | `dashboard.md` v2.0 | ✅ Cleared |
| ST-06 | Drawdown Spec Alignment | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-07 | Backend: US Currency Conversion | Design Pre-Approved | N/A | `risk_dashboard.md` v0.1.6 | ✅ Cleared |
| ST-08 | Frontend: Error States | Design Pre-Approved | N/A | `risk_dashboard.md` v0.1.6 | ✅ Cleared |
| ST-09 | Frontend: Table/Column Fixes | Design Pre-Approved | N/A | `risk_dashboard.md` v0.1.6 | ✅ Cleared |
| ST-10 | Frontend: HeatGauge + Cosmetic | Design Pre-Approved | N/A | `risk_dashboard.md` v0.1.6 | ✅ Cleared |
| ST-11 | Test Scenario Library Phase 1 | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-12 | Test Scenario Library Phase 2 | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-13 | Service Coverage Standard | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-14 | Canonical Terms Glossary | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-15 | AI Governance Policy | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-16 | Document /market/status | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-17 | settings_model.md | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-18 | Error Response Standard | Design Not Applicable | N/A | N/A | ✅ Cleared |
| ST-19 | Spec/Doc Debt Small Fixes | Design Not Applicable | N/A | N/A | ✅ Cleared |

**Classification totals:** Design Required: 5 · Design Pre-Approved: 4 · Design Not Applicable: 10

---

## Blocked Items

None.

---

## Design Artefacts Produced This Cycle

| ST-ID | Artefact | Location | Approved by |
|-------|----------|----------|-------------|
| ST-01 | UX decision record — Compliance Metrics | `docs/design/2026-03-06__release-v1.9/compliance-metrics/ux_spec.md` | Product Owner — 2026-03-06 |
| ST-02 | UX decision record — Trade Reflection Template | `docs/design/2026-03-06__release-v1.9/trade-reflection/ux_spec.md` | Product Owner — 2026-03-06 |
| ST-03 | UX decision record — Cohort Analysis | `docs/design/2026-03-06__release-v1.9/cohort-analysis/ux_spec.md` | Product Owner — 2026-03-06 |
| ST-04 | UX decision record — R-Multiple Distribution | `docs/design/2026-03-06__release-v1.9/r-multiple-distribution/ux_spec.md` | Product Owner — 2026-03-06 |
| ST-05 | UX decision record — Dashboard Homepage | `docs/design/2026-03-06__release-v1.9/dashboard-home/ux_spec.md` | Product Owner — 2026-03-06 |

---

## Frontend Spec Versions Locked for Sprint Planning

| ST-ID | Spec | Version | Change |
|-------|------|---------|--------|
| ST-01 | `docs/specs/frontend/pages/analytics.md` | v1.3 | New §17 Discipline & Compliance |
| ST-02 | `docs/specs/frontend/pages/trade_reflection.md` | v0.1 | New spec |
| ST-03 | `docs/specs/frontend/pages/analytics.md` | v1.3 | New §15 Cohort Analysis |
| ST-04 | `docs/specs/frontend/pages/analytics.md` | v1.3 | New §16 R-Multiple Distribution (Backend) |
| ST-05 | `docs/specs/frontend/pages/dashboard.md` | v2.0 | Full rewrite — session summary home page |
| ST-07 | `docs/specs/frontend/pages/risk_dashboard.md` | v0.1.6 | No change — spec already canonical |
| ST-08 | `docs/specs/frontend/pages/risk_dashboard.md` | v0.1.6 | No change — spec already canonical |
| ST-09 | `docs/specs/frontend/pages/risk_dashboard.md` | v0.1.6 | No change — spec already canonical |
| ST-10 | `docs/specs/frontend/pages/risk_dashboard.md` | v0.1.6 | No change — spec already canonical |

---

## Notes

1. **ST-04 vs existing §9 R-Multiple Analysis:** analytics.md §9 performs client-side R-multiple calculation. ST-04 (§16) adds a server-side canonical version. Both coexist. §16 is the canonical metric; §9 remains a visualisation aid. This distinction is documented in the updated analytics.md API Dependency note.

2. **ST-02 data model dependency:** `trade_reflection.md` §10 notes that a `trade_reflections` storage table must be defined by the Data Model & Domain Schema Owner in `data_model.md` before backend implementation. This is a sprint pre-condition for ST-02 implementation, not a design gate blocker.

3. **ST-05 composite endpoint:** If a `GET /dashboard/summary` endpoint is introduced, it must be documented in API contracts and openapi.yaml. The design gate approves the layout and data model; the endpoint decision is deferred to sprint pre-alignment.

4. **RISK-06 (drawdown spec alignment — ST-06):** RESOLVED 2026-03-06. Head of Specs Team reviewed backend implementation and confirmed split-source data model (see `risk_dashboard.md §4.1` v0.1.7). DEV-ST03-08 closed. Sprint planning may seal without this blocker.
