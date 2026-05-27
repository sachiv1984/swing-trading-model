# Workforce Capacity

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-27 (throughput revision — sprint capacity baseline raised; rebalance cadence changed to every 2nd cycle)

> ⚠️ Standing Notice: This document records workforce planning estimates. All effort figures are indicative. Canonical project records take precedence.

---

## Sprint Capacity Baseline (Effective 2026-05-27)

**Decision:** Sprint capacity baseline raised from ~8–10 days/sprint to ~12–14 days/sprint (solo developer, evenings/weekends). This is a deliberate upward revision to increase release throughput in response to backlog growth outpacing delivery rate (CPS 1.15 at 2026-05-27 rebalance).

| Field | Previous | Revised |
|-------|----------|---------|
| Per-sprint capacity | ~8–10 working days | ~12–14 working days |
| Warn threshold | Effort > 10 days | Effort > 14 days |
| Rationale | Conservative baseline | Reflects actual sustained pace across v3.x–v4.x cycles |

Release planning and sprint planning engines should use ~12–14 days per sprint as the capacity baseline. A `warn` outcome is appropriate when estimated effort exceeds 14 days per sprint; `pass` when within 12–14 days. PO may acknowledge a `warn` to proceed as before.

**Rebalance cadence:** Rebalances now run every 2nd cycle (post-ship closure emits advisory). PO may override and run on any cycle.

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

---

## Capacity Released — Cycle 2026-03-21__item-3.5

### Completed items: v2.1 — Alerts, Watchlists & Enhancements (shipped 2026-03-21)

| Field | Value |
|-------|-------|
| Estimated effort released | ~12–16 days (6 EPICs: ADR-003, Alerts, Watchlists, Chart Interactivity, Tax/Slippage, Spec Debt & QA) |
| Skills released | Backend async (Telegram/email), Frontend (Alerts UI, Watchlists, Chart Interactivity), QA & Testing (scenario authoring + execution), API Contracts, Spec authoring, PMO coordination |
| Duration freed | Immediately available for v2.2 pre-alignment |
| Constraints | OA-01–OA-05 deferred actions from post-ship closure carry into v2.2 capacity planning |

### New Backlog Items Added (from IW-20260321-01 and stale idea clearing — cycle 2026-03-21__item-3.5)

| Item | Est. Effort | Skills | Priority |
|------|------------|--------|---------|
| BLG-SEC-01 API Key Authentication | ~1 day | Backend Engineering + Frontend | P1 |
| BLG-FEAT-12 Alert History Table | ~2–3 days | Backend Engineering + Frontend + Data Model | P2 |
| BLG-FEAT-10 Alert Threshold Customisation | ~2–3 days | Backend Engineering + Frontend | P2 |
| BLG-FEAT-11 Strategy Compliance Score (SPS=4, display-only) | ~3–5 days | Backend Engineering + Frontend + Strategy Rules | P2 |
| BLG-SPEC-T01 Spec-to-Test Traceability Matrix | ~1–2 days | Director of Quality + Head of Specs Team | P2 |
| BLG-FEAT-09 Metrics Staleness Indicator | ~1–2 days | Backend Engineering + Frontend | P2 |
| BLG-QA-02 Test Automation Readiness Assessment | ~0.5–1 day | QA & Testing Owner + Director of Quality | P2 |
| BLG-FE-02 Loading State Standardisation | ~1–2 days | Frontend | P3 |
| BLG-FE-03 User-Facing Error Message Mapping | ~1–2 days | Frontend | P3 |
| BLG-OPS-05 API Performance Baseline | ~0.5–1 day | Head of Engineering | P3 |
| BLG-OPS-06 Health Check Endpoint | <1 hour | Backend Engineering | P3 |
| BLG-SEC-02 Content Security Policy Headers | <1 hour | Frontend + Cybersecurity | P3 |

**Total new backlog additions:** ~13–24 days estimated effort (4.6–8.6 sprints at 3-day sprint cadence)

**Skill-Silo check (cycle additions):** Governance load ~15% (BLG-SPEC-T01 + BLG-QA-02 are documentation/process items; remainder is execution). Within 15–60% bounds. No Skill-Silo Alert triggered. Product Owner sign-off capacity confirmed.

**Assessment:** v2.1 freed substantial multi-skill capacity (Backend, Frontend, QA, Spec). The new backlog is front-loaded with P1 security (BLG-SEC-01) and P2 feature enhancements. BLG-FEAT-11 (SPS=4) is the only boundary-adjacent item and requires Strategy Rules owner involvement — this is the primary capacity constraint for v2.2. Sequencing recommendation: BLG-SEC-01 first (P1 security gap), then BLG-QA-02 + BLG-SPEC-T01 (quality foundations), then alert enhancements (BLG-FEAT-10/12) after BLG-OPS-04 alert scheduling design completes. BLG-OPS-06 and BLG-SEC-02 are XS items appropriate for any sprint as fast-follow tasks. No workforce constraint violation identified for the projected v2.2 scope.

---

## New Backlog Items Added — Cycle 2026-03-24__scheduled (Scheduled Rebalance)

*Source: roadmap rebalance cycle 2026-03-24__scheduled — 8 new backlog items from ideas pool review (BLG-OPS-07/08/09, BLG-QA-03/04/05/06, BLG-FE-05). v2.2 shipped; v2.3 pool now 23 items.*

### New Items (cycle 2026-03-24__scheduled)

| Item | Est. Effort | Skills | Priority |
|------|------------|--------|---------|
| BLG-OPS-07 System Health Check Playbook | ~0.5 day | Infrastructure & Operations Owner (documentation) | P3 |
| BLG-QA-03 Canonical Test Execution Report Template | ~0.5 day | QA Lead (process governance) | P3 |
| BLG-QA-04 Integration Test Coverage Report | ~1.0 day | QA & Testing Owner + CI Engineering | P3 |
| BLG-QA-05 Critical-path Smoke Test (Playwright) | ~2.0 days | QA & Testing Owner + Frontend (Playwright) | P2 |
| BLG-OPS-08 Staging Data Reset Script | ~0.5 day | Infrastructure & Operations Owner + Backend Engineering | P3 |
| BLG-OPS-09 Database Size Monitoring Alert | ~0.5 day | FinOps & Resource Architect + Backend Engineering | P2 |
| BLG-FE-05 Alert Notification Badge | ~0.5 day | Base44 Frontend Prompt Owner | P3 |
| BLG-QA-06 Test Data Seed Script Library | ~1.0 day | QA & Testing Owner + Backend Engineering | P2 |
| **Total new** | **~6.5 days** | Mixed — QA dominant | — |

**Combined v2.3 pool estimate:** ~37–47 days total (23 items). Release planning will scope a 2–3 sprint plan from this pool. No scarce skill conflicts identified. QA automation domain is dominant in new additions (4 items, ~4.5 days) — already represented by existing BLG-QA-01.

**Skill-Silo check (cycle additions):** Governance load 0% (all new items are execution-heavy: QA, infrastructure, frontend). Below 20% floor. Product Owner sign-off capacity confirmed (v2.3 will be scoped by release planning). No Skill-Silo Alert issued.

**Sequencing note:** BLG-OPS-08 (staging reset) is a prerequisite for BLG-QA-05 (smoke test) and BLG-QA-04 (coverage report) — schedule BLG-OPS-08 first in whatever sprint targets QA automation. BLG-QA-06 (seed scripts) is a companion prerequisite for BLG-QA-05.

---

## v2.4 — Candidate Pool Economics (Roadmap Rebalance 2026-03-31__scheduled)

*New items added to v2.4 candidate pool. Final allocation determined at release planning.*

| Initiative | Estimated FTE effort | Skills required | Duration | Opportunity cost |
|-----------|---------------------|-----------------|----------|-----------------|
| BLG-FEAT-14 — Weekly trading review digest | ~2–3 days | Backend (endpoint), Frontend (digest component) | 1 sprint | Medium — competes with BLG-BE-05, BLG-FE-06 bug fix priority |
| BLG-OPS-10 — Render hosting tier review | ~0.25 day | FinOps, Infrastructure | 1 session | Very low — document only |
| BLG-BE-06 — Alert evaluation idempotency | ~1–2 days | Backend Engineering | 1 sprint | Low — backend-only, no frontend |
| BLG-GOV-09 — Cycle velocity metric | ~0.5 day | PMO Lead, Head of Engineering | 1 session | Low — documentation task |
| **4-item total (new)** | **~4–6 days** | Backend, Frontend, FinOps, PMO | — | — |

**Combined v2.4 backlog pool** (11 existing + 4 new = 15 items): ~40–55 days estimated effort across all 15 items.

**Skill constraints for release planning:**
- Backend Engineering is the primary capacity ceiling — sequencing BLG-BE-05, BLG-BE-06, BLG-FEAT-14 endpoint work, and BLG-SPEC-D15/D16 backend touches will be critical.
- Governance load (BLG-GOV-09, BLG-OPS-10, BLG-GOV-08, BLG-GOV-03) is ~15% of total — below 20% floor. Release planner must schedule governance items alongside execution items to maintain Product Owner sign-off capacity.
- No scarce skill conflicts at backlog level — conflicts will surface at release planning as sprint allocation is finalised.

**Assessment:** Pool is healthy and well-balanced. No workforce constraint violations at rebalance time. Release planning should sequence P2 bug fixes (BLG-BE-05, BLG-FE-06, BLG-SPEC-D16) early to clear technical debt, then layer in new feature work.

---

## v2.5 — Candidate Pool Economics (Roadmap Rebalance 2026-04-05__scheduled)

*New items added to v2.5 candidate pool from ideas advancing in this cycle. Final allocation determined at release planning (v2.5 planning not yet started).*

| Initiative | Estimated FTE effort | Skills required | Duration | Opportunity cost |
|-----------|---------------------|-----------------|----------|-----------------|
| BLG-FE-09 — Define Frontend Performance Budget | ~0.5 day | Frontend + Head of Engineering | 1 session | Very low — documentation/spec only; no implementation |
| BLG-SPEC-D17 — Spec Dependency Map | ~1–2 days | Head of Specs Team + PMO Lead | 1–2 sessions | Low — governance documentation |
| BLG-GOV-14 — Governance Health Score | ~1–2 days | PMO Lead + Governance Facilitator | 1 sprint | Low — lightweight metric + tracking |
| **3-item total (new this cycle)** | **~2.5–4.5 days** | Frontend spec, Spec governance, PMO governance | — | — |

**Skill-Silo check (cycle additions):** Governance/documentation load 100% (all 3 new items are governance, spec debt, or documentation — no execution items added this cycle). Skill-Silo Alert TRIGGERED (threshold >80% governance). Pull-forward candidate BLG-OPS-12 (Alerting Dependencies Runbook, P2) was surfaced; Product Owner confirmed it is already in the backlog at appropriate priority. No further pull-forward required. Alert acknowledged.

**Combined v2.5 backlog pool** (existing items + 3 new = approximately 23 total items post-v2.4 ship): Exact pool count determined at release planning. No scarce skill conflicts at backlog level.

**Assessment:** The 3 new items are all P3 / low-effort governance, spec debt, and documentation work. No workforce constraint violations at rebalance time. Release planning for v2.5 should ensure governance-heavy items are balanced against execution items when selecting the sprint scope — the Skill-Silo Alert from this cycle is a direct input to that decision.


---

## No-Change Run — Cycle 2026-04-17__scheduled

**Scheduled rebalance — no new FTE allocation required.**

No initiatives were added, replaced, deferred, or killed. No new backlog items promoted to roadmap level. Existing v2.8 backlog pool (8 P3 items) unchanged.

**Skill-Silo check:** Governance load = 0% (no new items of any category). Below 20% floor. Product Owner sign-off capacity confirmed — no new sign-off actions required at rebalance time. No pull-forward candidate required.

**Assessment:** v2.8 backlog pool is as-is. Release planning will determine the v2.8 sprint allocation from the 8 existing P3 items.

---

## New Backlog Items Added — Cycle 2026-04-24__scheduled (Scheduled Rebalance)

*Source: roadmap rebalance cycle 2026-04-24__scheduled — 2 new backlog items from gate-cleared ideas (BLG-FE-19, BLG-OPS-14). v2.9 shipped; v3.0 candidate pool now 14 items.*

### New Items (cycle 2026-04-24__scheduled)

| Item | Est. Effort | Skills | Priority |
|------|------------|--------|---------|
| BLG-FE-19 Keyboard Shortcuts | ~0.5 day | Base44 Frontend Prompt Owner | P3 |
| BLG-OPS-14 AI Journal Monitoring Metrics | ~0.5 day | Backend Engineering + AI Compliance & Governance Officer | P3 |
| **Total new** | **~1 day** | Frontend, Backend, AI Compliance | — |

**Skill-Silo check (cycle additions):** Governance load = 0% (both new items are execution-heavy: frontend implementation, backend metrics endpoint). Below 20% floor. Product Owner sign-off capacity confirmed. No Skill-Silo Alert issued.

**Assessment:** 2 S-effort P3 items added. No scarce skill conflicts. Both items are well-bounded and low-complexity. v3.0 candidate pool is balanced; release planning will allocate from the full 14-item pool.
