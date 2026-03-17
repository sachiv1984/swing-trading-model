# Workforce Capacity

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-17 (roadmap rebalance — cycle 2026-03-17__item-v1.10)

> ⚠️ Standing Notice: This document records workforce planning estimates. All effort figures are indicative. Canonical project records take precedence.

---

## Capacity Released — Cycle 2026-03-01__item-3.2

### Completed item: 3.2 QWB Quick Wins Bundle (v1.6.1)

| Field | Value |
|-------|-------|
| Estimated effort released | ~8–10.5 hours |
| Skills released | Frontend development, backend API, spec authoring |
| Duration | One-off bundle — no ongoing allocation |
| Constraints | None |

---

## v1.7 — Foundation & Governance Initiatives

| Initiative | Estimated FTE effort | Skills required | Duration | Opportunity cost |
|-----------|---------------------|-----------------|----------|-----------------|
| BLG-TECH-04 CI/CD | ~1 day | DevOps / backend engineering | 1 sprint | Low — unblocked, bounded scope |
| §13 Boundary Review | ~0.5 day | Product Owner + Strategy Rules owner | 1 session | Low — governance task |
| Metrics Defs — Heat Formula | ~0.5 day | Metrics Definitions owner | 1 session | Low — definitional task |
| Structured Logging | ~1 day | Head of Engineering | 1 sprint | Medium — pre-req for v2.0 |
| API Versioning Decision | ~0.5 day | Product Owner + API Contracts owner | 1 session | Low — decision record |
| **v1.7 total** | **~3.5 days** | Mixed — engineering, spec, product | — | — |

**Assessment:** v1.7 is primarily governance and foundation work. Total estimated effort ~3.5 days. No scarce skill conflicts identified. All items are bounded and low-complexity individually. No workforce constraint violation.

---

## v1.8 — Risk Dashboard

| Initiative | Estimated FTE effort | Skills required | Duration | Opportunity cost |
|-----------|---------------------|-----------------|----------|-----------------|
| 3.4 Risk Dashboard | ~3–4 days | Frontend + backend + Metrics Definitions | 1–2 sprints | Medium — displaces v1.9 start |

**Assessment:** Pre-requisite is Metrics Definitions (heat formula, v1.7). No workforce conflict. Feasible post v1.7.

---

## v1.9 — User Value & Insight

| Initiative | Estimated FTE effort | Skills required | Duration | Opportunity cost |
|-----------|---------------------|-----------------|----------|-----------------|
| BLG-FEAT-08 Compliance Metrics | ~1 day | Metrics Definitions owner | 1 sprint | Low |
| 5.1 Trade Reflection Template | ~1–2 days | Frontend + backend | 1 sprint | Low |
| 5.2 Cohort Analysis | ~1–2 days | Backend + analytics | 1 sprint | Low |
| 5.3 Dashboard Homepage | ~1–2 days | Frontend | 1 sprint | Low |
| **v1.9 total** | **~4–7 days** | Mixed | — | — |

**Assessment:** All v1.9 items are low-to-medium effort with no scarce skill conflicts. Sequential delivery feasible within a single sprint.

---

## v2.0 — Reporting & Alerts

| Initiative | Estimated FTE effort | Skills required | Duration | Opportunity cost |
|-----------|---------------------|-----------------|----------|-----------------|
| 3.5 Alerts & Notifications | ~4–5 days (+ QA) | Backend async, email/SMS infra, frontend, QA | 2–3 sprints | High — largest feature to date |
| 4.1b Tax-Year P&L | ~1–2 days | Backend + financial spec | 1 sprint | Low |
| 4.1c Server-Side PDF | ~1–2 days | Backend (WeasyPrint) | 1 sprint | Low |
| 4.3 Signal Exposure (gated) | ~0.5 day frontend | Frontend only (backend ready) | 1 sprint | Low — only after gate cleared |
| **v2.0 total** | **~7–10 days** | Mixed — highest complexity release | — | — |

**Assessment:** 3.5 Alerts is the most workforce-intensive item in the entire roadmap. QA testing surface for notification delivery is materially larger than effort estimate implies. Pre-conditions (v1.7 observability + API versioning + QA planning session) are hard gates. Do not allocate workforce to 3.5 until all three pre-conditions are confirmed. No scarce skill conflict that forces a kill — but capacity must be reserved and explicitly confirmed before v2.0 pre-alignment opens.

---

## Workforce Economics Gate Assessment

**FinOps & Resource Architect finding:** No workforce constraints are violated by the current roadmap. The v1.7 → v1.8 → v1.9 → v2.0 sequencing is appropriate. The 3.5 Alerts hard gate pre-conditions ensure workforce is not allocated prematurely to the most complex and resource-intensive feature. No Replace, Defer, or Kill is forced by workforce constraints in this cycle.

Scarce skill note: Metrics Definitions owner is required for both v1.7 (heat formula) and v1.9 (BLG-FEAT-08). These should not run concurrently. Confirmed sequential sequencing (v1.7 heat formula before v1.9 BLG-FEAT-08 may proceed) already satisfies this constraint.

---

## Capacity Released — Cycle 2026-03-04__item-3.4

### Trigger: v1.7 Foundation & Governance — Complete (2026-03-03)

| Field | Value |
|-------|-------|
| Estimated effort released | ~3.5–4 days (6 EPICs: CI/CD, §13 review, metrics defs, logging, API versioning, spec debt) |
| Skills released | Governance/spec: Product Owner, Strategy Rules owner, Metrics owner. Engineering: backend/CI. |
| Duration | Immediately available for v1.8 |
| Constraints | None — all v1.7 work is complete and verified |

### New Backlog Items Added (from IW-20260304-01 — STEP 5 Advance)

| Item | Est. Effort | Skills | Priority |
|------|------------|--------|---------|
| BLG-NEW-01 Golden Output CI Baseline | 1–3 days | Engineering + QA | P1 |
| BLG-NEW-02 Backtest Stop Reconciliation | 1–3 days | Engineering + QA | P1 (after BLG-NEW-01) |
| BLG-NEW-03 Unavailability Failure Mode | ~0.5 day | Governance | P1 |
| BLG-NEW-04 AI Governance Policy | ~0.5 day | Governance | P2 |
| BLG-NEW-05 Dependency Vulnerability Scanning | ~0.5 day | Engineering (CI) | P1 |
| BLG-NEW-07 Running API Changelog | ~0.5 day | Documentation | P1 |
| BLG-NEW-08 OpenAPI Drift Detection CI | ~0.5 day | Engineering (CI) | P1 |
| BLG-NEW-06 (merged into 4.1b) | — | — | — |

**Skill-Silo check (v1.8 scope):** Governance load ~21%. Within 20–60% bounds. No alert triggered. Product Owner sign-off capacity confirmed.

**Assessment:** New backlog items are predominantly execution-heavy (CI, engineering). Combined with the Risk Dashboard (execution-heavy), v1.8 is well-balanced. The small governance items (BLG-NEW-03, 04, 07) are low-effort and can be delivered alongside engineering work without creating a governance bottleneck.

---

## Capacity Released — Cycle 2026-03-06__item-3.4

### Completed item: 3.4 Risk Dashboard (v1.8 — shipped 2026-03-06)

| Field | Value |
|-------|-------|
| Estimated effort released | ~3–4 days (EPIC-01 through EPIC-04: frontend, backend, CI/CD, governance) |
| Skills released | Frontend development (Base44), Backend (FastAPI), QA execution, API Contracts authoring, Spec authoring, CI/DevOps, Governance/PMO |
| Duration freed | Immediately available for v1.9 pre-alignment |
| Constraints | None — v1.8 is fully verified and closed |

### New Backlog Items Added (from cycle 2026-03-06__item-3.4 — DL-006)

| Item | Est. Effort | Skills | Priority |
|------|------------|--------|---------|
| BLG-NEW-09 R-Multiple Distribution Report | ~1–2 days | Backend + Metrics Definitions | P2 |
| BLG-NEW-10 Canonical Test Scenario Library | ~1–3 days (scoped) | QA + Engineering | P1 |
| BLG-NEW-11 Canonical Terms Glossary | ~1 day | Head of Specs Team | P2 |
| BLG-NEW-12 Service Layer Test Coverage Standard | ~0.5 day (doc) + CI setup | Backend Engineering + QA | P1 |

**Metrics Definitions owner sequencing constraint:** BLG-FEAT-08 definitions must precede BLG-NEW-09 implementation. LL-05 capacity check must confirm Metrics Definitions owner availability before v1.9 pre-alignment opens (applies to both BLG-FEAT-08 and BLG-NEW-09).

**Skill-Silo check (this cycle's additions):** Governance load 17% (below 20% floor). Product Owner sign-off capacity confirmed. No pull-forward required. No skill-silo alert issued.

**Assessment:** v1.9 scope is well-balanced — execution-heavy user value features (5.1, 5.2, 5.3, BLG-RD fixes) combined with low-governance-overhead quality standards (BLG-NEW-10, 12) and a spec governance item (BLG-NEW-11). Metrics Definitions owner is the key capacity constraint to monitor at v1.9 pre-alignment (LL-05).

---

## Capacity Released — Cycle 2026-03-17__item-v1.10

### Completed item: v1.10 — Operations & Quality Foundation (shipped 2026-03-16)

| Field | Value |
|-------|-------|
| Estimated effort released | ~15–20 days (5 EPICs: dev environment, CohortAnalysis refactor, API integration tests, QA scenario gaps, multi-sprint delivery) |
| Skills released | Infrastructure & Operations Owner (staging env), Backend Engineering (CohortAnalysis refactor), QA & Testing (integration tests, QA scenarios), Head of Specs Team (governance), PMO Lead (sprint coordination) |
| Duration freed | Immediately available for v2.0 pre-alignment |
| Constraints | None — v1.10 fully verified and closed (verification_status: Verified_with_deviations; all deviations tracked in backlog as BLG-BE-01, BLG-BE-02, TEST-GAP-EPIC-02) |

### New Backlog Items Added (from cycle 2026-03-17__item-v1.10 — DL-009)

| Item | Est. Effort | Skills | Priority |
|------|------------|--------|---------|
| BLG-OPS-02 Production Deployment Runbook | ~0.5–1 day | Infrastructure & Operations Owner | P2 |
| BLG-DATA-01 Positions Table Data Dictionary | ~0.5–1 day | Data Model Domain & Schema Owner | P2 |
| BLG-TECH-07 Database Migration Governance Standard | ~0.5–1 day | Backend Engineering + Head of Engineering | P2 |

**Skill-Silo check (v2.0 scope, this cycle):** Governance load ~0% (all v2.0 items are execution-heavy: 4.1b spec+implementation, 4.3 frontend spec+implementation). Below 20% floor. Product Owner sign-off capacity confirmed. No Skill-Silo Alert issued. Sign-off capacity: adequate — v2.0 scope well-defined with clear spec ownership (4.1b: Financial Reporting Records Owner; 4.3: Frontend UX spec + Strategy Rules owner for scope enforcement).

**Assessment:** v2.0 is the lowest-overhead delivery candidate to date: 4.3 is frontend-only (~0.5 day), 4.1b is low-medium effort. The largest item (3.5 Alerts) remains gated. With v1.10 capacity freed, engineering and ops capacity is available. No workforce constraint violation for v2.0 scope.
