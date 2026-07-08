# Workforce Capacity

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-08 (rebalance 2026-07-08__scheduled — Standard tier (CPS=N/A, 0 active initiatives); no FTE changes; 40 new/updated backlog items, 2 approved as mandatory pull-forward candidates (BLG-FEAT-52 ungated, BLG-FEAT-71 new); Skill-Silo Alert: rolling-3-cycle avg 78.0% (>40% ceiling, 2nd consecutive improvement); Product Value Alert (ratio 0.26) independently mandated the same pull-forward outcome)

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

---

## Cycle 2026-06-08__scheduled — Workforce Economics Assessment

**Date:** 2026-06-08
**Run tier:** Standard
**Items evaluated:** 22 new backlog items (19 Promoted-Added + 3 Promoted-Backlog)

| Item | Effort | Skill Category | Notes |
|------|--------|---------------|-------|
| BLG-SPEC-53/54 | M + S | Head of Specs, API Contracts, Engineering | Spec debt resolution |
| BLG-QA-51–54 | S + S + M + S | QA Lead, Director of Quality | QA governance |
| BLG-OPS-57–59 | S + S + S | Infra/Ops, Cybersecurity, Engineering | Operational hardening |
| BLG-FE-66/67 | S + S | Frontend, UX | UX review + scope definition |
| BLG-GOV-104–111 | M + S × 7 | Strategy Owner, PO, PMO, AI Compliance, various | Governance |
| BLG-GOV-112–114 | S × 3 | PO, Director of Quality, Data Model | Gate-conditional |

**Governance load %:** ~35% (BLG-GOV items: 11 of 22 = 50% by count; by effort ≈ 35% due to smaller S vs M items in exec category)
**Execution load %:** ~65%

**Skill-Silo check:** Governance = 35% < 60% ceiling. No Skill-Silo Alert.
Floor check: Governance > 20% — PO sign-off capacity confirmed. All items are autonomous-class; sole operator cadence unchanged.

**Workforce constraints:** None. All items are S or M effort. v5.3 candidate pool is manageable within standard sprint capacity.

---

## Rebalance 2026-06-09__scheduled

**Date:** 2026-06-09
**Run tier:** Standard
**Items evaluated:** 8 new backlog items (all gate-conditional Promoted-Backlog); 0 new Promoted-Added initiatives

| Item | Effort | Skill Category | Notes |
|------|--------|---------------|-------|
| BLG-GOV-115 | S | Metrics Analytics, Infra/Ops | Gate-conditional on 2026-07-04 |
| BLG-FE-68/70 | M + M | Frontend, Metrics Analytics | Gate-conditional on BLG-FE-45 |
| BLG-FE-69/71 | M + S | Frontend, UX | Gate-conditional on Phase 2 decision |
| BLG-FEAT-45 | S | Financial Reporting | Gate-conditional ≥ 2026-08-05 |
| BLG-SPEC-55 | S | API Contracts | Gate-conditional on PO-02 imminence |
| BLG-QA-55 | S | QA Lead, Director of Quality | Gate-conditional on ≥20 closed trades |

**Governance load %:** ~65% (5 of 8 items are governance/spec/analytics documents; high governance proportion but all gate-conditional so no immediate sprint impact)
**Execution load %:** ~35%

**Skill-Silo advisory:** Governance = 65% at ceiling threshold. However, all 8 items are gate-conditional — none enter sprint planning until gates clear. No active sprint impact. Advisory noted per STEP 7.1.

**v5.4 capacity outlook:** Candidate v5.4 scope (~11 items from candidate list in cycle_record.md) is S–M effort throughout. Estimated 8–12 stories. Within standard sprint capacity.

---

## Rebalance 2026-07-01__scheduled

**Date:** 2026-07-01
**Run tier:** Standard
**Items evaluated:** 1 item — BLG-BE-40 (STEP 8.0 Production Correctness Fast-Track, mandatory addition to v6.4 Now horizon); 0 new Promoted-Added initiatives

| Item | Effort | Skill Category | Notes |
|------|--------|---------------|-------|
| BLG-BE-40 | XS | Backend Engineering / Data Model | P1 correctness bug — mandatory Now horizon inclusion per STEP 8.0, no PO discretion |

**Governance load %:** N/A — no governance/spec items added this cycle
**Execution load %:** 100% (single correctness item)

**Skill-Silo advisory:** Rolling 3-cycle average (v6.1 55.6%, v6.2 30.8%, v6.3 73.3%) = 53.2%, above the 40% ceiling — Alert triggered per STEP 7.1. Mandatory pull-forward scan identified BLG-FEAT-54 (Open Positions panel, U-story, P2) as the pull-forward candidate; PO acknowledged for consideration at `plan release v6.4`.

**v6.4 capacity outlook:** Now horizon carries only BLG-BE-40 (XS) at this stage; full v6.4 scope deferred to `plan release v6.4` per STEP 8.1 Option (b). No capacity constraint identified.

**Workforce constraints:** None new. Gate-conditional items create no immediate FTE demand.

---

## Rebalance 2026-07-03__scheduled

**Date:** 2026-07-03
**Run tier:** Standard
**Items evaluated:** 0 new backlog items this cycle (idea intake skipped — 34 open ideas ≥ 20 threshold; all 34 re-parked, none advanced/backlogged). 0 new Promoted-Added initiatives.

**Skill-Silo advisory:** Rolling 3-cycle average (v6.3 86.7%, v6.4 76.9%, v6.5 87.5%) = **83.7%**, above the 40% ceiling — Alert triggered per STEP 7.1, **worse again** than the prior reading (64.8%), despite v6.5's release plan naming two nominal U-item pull-forwards (BLG-FE-46, BLG-FEAT-41). Under this cycle's classification, only BLG-FE-46 counted as U — BLG-FEAT-41 (thesis adoption rate metric) was reclassified D at STEP 2.4 because its shipped description names only a metrics-definition spec update, no user-visible endpoint or UI panel. This is itself a material finding: the "does 2 U-items correct the ceiling" carry-forward test (DF-17/LP-04) was confounded by classification-method disagreement over whether BLG-FEAT-41 actually counted as user-facing — see STEP 11 friction log.

Three consecutive Alert cycles now (v6.3-area through this one), each worse than the last despite an attempted correction. Per the standing STEP 7.1 wording (added v8.0): the PO should strongly consider committing **more than one** substantive U-item at the next release rather than a single small item.

Mandatory pull-forward scan of `backlog.md` (P0/P1/P2 first, ungated, no blockers): no P0/P1 user-facing item is currently ungated. Highest-priority ungated candidate found: **BLG-FE-82** (Colour contrast audit sweep, P2, S effort, Owner: Head of UX & Design, no gate) — though this is audit-shaped (produces findings + follow-up items) rather than a direct feature, it is the best available candidate under the letter of the rule. Secondary candidate for PO consideration alongside it: **BLG-FEAT-52** (Trade tagging and tag-based performance filtering, P3, no gate) — a substantive feature-shaped item, offered given the severity/duration of this Alert and the wording's advice to consider multiple items.

**v6.6 capacity outlook:** Now horizon remains empty; STEP 8.1 gate applies (see `run_manifest.md`/`cycle_record.md`). No capacity constraint identified at roadmap level — all evaluation is advisory pending `plan release`.

**Workforce constraints:** None new.

---

## Rebalance 2026-07-02__scheduled

**Date:** 2026-07-02
**Run tier:** Standard
**Items evaluated:** 24 new backlog items (from idea intake IW-20260702-01 disposition — 8 immediately-actionable, 16 gate-conditional); 0 new Promoted-Added initiatives

| Item | Effort | Skill Category | Notes |
|------|--------|---------------|-------|
| BLG-GOV-154, BLG-GOV-156 | S | Governance / API Design | Process conventions, ungated/lightly-gated |
| BLG-QA-69, BLG-QA-70, BLG-QA-71 | S–M | QA / Testing | 1 immediately actionable, 2 gate-conditional |
| BLG-BE-41, BLG-BE-42 | S–M | Backend Engineering | 1 immediately actionable, 1 gate-conditional |
| BLG-SEC-09 | S | Security Verification | Immediately actionable |
| BLG-SPEC-62, BLG-SPEC-63, BLG-SPEC-65, BLG-SPEC-66 | S–M | Spec Debt | 1 immediately actionable, 3 gate-conditional |
| BLG-FE-81, BLG-FE-82, BLG-FE-83, BLG-FE-84 | S–M | Frontend / UX | 2 immediately actionable, 2 gate-conditional |
| BLG-FEAT-55–60 | M–L | Product Feature / AI | All gate-conditional (AI adoption window, data density, or dependent feature) |
| BLG-OPS-84, BLG-OPS-85 | S | FinOps / Ops | Both gate-conditional (annual cadence / dependent item) |

**Governance load %:** ~46% (11 of 24 items are GOV/QA/SPEC/SEC process or spec-debt items)
**Execution load %:** ~54% (13 of 24 are FE/BE/FEAT/OPS execution items)

**Skill-Silo advisory:** Rolling 3-cycle average (v6.2 30.8%, v6.3 86.7%, v6.4 76.9%) = **64.8%**, above the 40% ceiling — Alert triggered per STEP 7.1, worse than the prior 53.2% reading. Bundling a single U-story pull-forward (BLG-FEAT-54, v6.4) did not correct this. Mandatory pull-forward scan identified **BLG-FE-46** (Claude thesis feedback mechanism, U-story, P3, S effort, no gate) as the pull-forward candidate; PO acknowledged for `plan release v6.5`, with an advisory that more than one U-item should be prioritised next release if the ceiling is to be meaningfully corrected.

**v6.5 capacity outlook:** Now horizon remains empty; full v6.5 scope deferred to `plan release v6.5` per STEP 8.1 Option (b). All 24 new items are gate-conditional or small/unscheduled — no capacity constraint identified at roadmap level.

**Workforce constraints:** None new. Gate-conditional items create no immediate FTE demand.

---

## Rebalance 2026-07-06__scheduled

**Date:** 2026-07-06
**Run tier:** Standard
**Items evaluated:** 25 new backlog items (from ideas 3-cycle hard cap disposition — 25 gate-conditional, 8 rejected, 1 resolved as a governance-prompt patch); 0 new Promoted-Added initiatives

| Item | Effort | Skill Category | Notes |
|------|--------|---------------|-------|
| BLG-FEAT-61, BLG-FEAT-62, BLG-FEAT-63 | S–M | Product Feature | All gate-conditional (usage signal, trade count, or AI-adoption date) |
| BLG-GOV-171–177 | S–M | Governance / Process | All gate-conditional (opportunistic/audit-bundle or signal-triggered) |
| BLG-QA-75, BLG-QA-76, BLG-QA-77, BLG-QA-78 | S–M | QA / Testing | All gate-conditional (first-incident or audit-bundle triggers) |
| BLG-OPS-88, BLG-OPS-89, BLG-OPS-90, BLG-OPS-91, BLG-OPS-92 | S | FinOps / Infrastructure | All gate-conditional (scheduled cadence or signal-triggered) |
| BLG-SPEC-67 | M | Spec Debt | Gate-conditional (audit-bundle) |
| BLG-BE-43, BLG-BE-44, BLG-BE-45 | S–M | Backend Engineering | All gate-conditional (design-phase trigger, stability window, or audit-bundle) |
| BLG-FE-90 | S | Frontend / UX | Gate-conditional (signal-triggered) |
| BLG-SEC-10 | S | Security / QA | Gate-conditional (30-day production observation window) |

**Governance load %:** ~48% (12 of 25 items are GOV/QA/SPEC/SEC process or spec-debt items)
**Execution load %:** ~52% (13 of 25 are FE/BE/FEAT/OPS execution items)

**Skill-Silo advisory:** Rolling 3-cycle average (v6.4 76.9%, v6.5 87.5%, v6.6 75.0%) = **79.8%**, above the 40% ceiling — Alert remains triggered per STEP 7.1, but improved for the first time after 3 consecutive worsening readings (was 83.7%). This cycle adopted a mandatory (not advisory) pull-forward clause in `roadmap_prompt.md` §7.1 (v8.2→v8.3) — after 3+ consecutive worsening/unresolved readings, the Product Owner must commit ≥2 build-and-ship-shaped U-items (per the STEP 2.4 story-shape distinction) at the next release, not merely "nominal" U-items. Mandatory pull-forward scan (LP-05 gate-verified) identified **BLG-FE-87** (P1, ungated, build-and-ship-shaped) and **BLG-FE-88** (P2, same defect class, ungated) as candidates for `plan release v6.7`; **BLG-FEAT-52** explicitly excluded — its own backlog entry confirms an unmet PO-02 gate (previously missed at `2026-07-03__scheduled` due to a non-standard `**Gate:**` field label, caught this cycle via direct inspection).

**v6.7 capacity outlook:** Now horizon remains empty; full v6.7 scope deferred to `plan release v6.7` per STEP 8.1 Option (b). All 25 new items are gate-conditional or small/unscheduled — no capacity constraint identified at roadmap level. The mandatory pull-forward clause constrains `plan release v6.7`'s scope decision (≥2 build-and-ship U-items required), which should be weighed at that engine's own STEP 4.5/7.

**Workforce constraints:** None new. Gate-conditional items create no immediate FTE demand.

---

## Rebalance 2026-07-08__scheduled

Both approved candidates (`BLG-FEAT-52` ungated/descoped, new `BLG-FEAT-71`) are S-effort, single-developer-context, no scarce-skill contention. 39 further Promoted-Backlog items (idea-driven, window `IW-20260708-01`) are all S–M effort, gate-conditional or immediately unscheduled — no capacity constraint identified.

| Item | Effort | Skill Category | Notes |
|------|--------|-----------------|-------|
| BLG-FEAT-52 (ungated), BLG-FEAT-71, BLG-FEAT-69, BLG-FEAT-70 | S–M | Product Feature | 2 are mandatory pull-forward candidates; 2 are ordinary backlog additions |
| BLG-GOV-178–189 | S–M | Governance / Process | All gate-conditional or None-gated backlog items |
| BLG-QA-79–85 | S–M | QA / Testing | All None-gated except BLG-QA-81 (implicit — contrast work now stable) |
| BLG-OPS-93–100 | S–M | FinOps / Infrastructure | BLG-OPS-99 (X-API-Key provisioning) is P1, resolves the LP-08 credential gap |
| BLG-SEC-11 | S | Security | None-gated |
| BLG-SPEC-68–70 | S–M | Spec Debt | All None-gated |
| BLG-BE-47–49 | S–M | Backend Engineering | All None-gated |
| BLG-FE-91–94 | S–M | Frontend / UX | All None-gated |

**Governance load %:** ~50% (20 of 40 items are GOV/QA/SPEC/SEC process or spec-debt items)
**Execution load %:** ~50% (20 of 40 are FE/BE/FEAT/OPS execution items)

**Skill-Silo advisory:** Rolling 3-cycle average (v6.5 87.5%, v6.6 75.0%, v6.7 71.4%) = **78.0%**, above the 40% ceiling — Alert remains triggered, 2nd consecutive improvement (down from 79.8%). The v8.3 mandatory-≥2-U-items escalation clause (3+ consecutive worsening readings) is not independently re-triggered this reading. However, the STEP 2.4 Product Value Alert (ratio 0.26, first time below the 0.30 floor) independently mandated the same pull-forward outcome — already actioned via `BLG-FEAT-52` (ungated) + `BLG-FEAT-71` (new), both approved at STEP 5.

**Key finding this cycle:** `BLG-BE-46` (filed same day, P1) shows the SI-02 gate's true status is materially worse than believed — 0 linked trade-plans (not 15 or 20) due to a `trade_plans.position_id` linkage bug, despite 20 total closed trades being confirmed accurate via `GET /trades`. This does not change workforce capacity directly but should be weighed heavily at the next `plan release` scoping decision (SI-02 frontend work remains gated regardless of trade-count optimism).

**v6.8+ capacity outlook:** Now horizon remains empty; scope deferred to next `plan release` per STEP 8.1 Option (b). The 2 mandatory pull-forward candidates (`BLG-FEAT-52`, `BLG-FEAT-71`) should anchor that release's U-item minimum.

**Workforce constraints:** None new. `BLG-OPS-99` (X-API-Key provisioning) remains the most consequential unresolved gap — blocks direct production verification of the SI-02 gate and similar data-dependent gates going forward.
