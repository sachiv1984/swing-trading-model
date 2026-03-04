# Workforce Capacity

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-01

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
