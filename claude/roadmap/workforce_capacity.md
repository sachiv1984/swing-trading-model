# Workforce Capacity

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-28 (rebalance 2026-07-28__scheduled — Standard tier (CPS=N/A, 0 active initiatives); no FTE changes; sprint capacity ceiling held unchanged at ~24-28 days/sprint — user asked whether to raise it ahead of this rebalance; v7.9 ran at ~95-110% utilisation (1st cycle at top of the current band) but only 1 data point exists so far (the 2026-07-17 raise was backed by 5 consecutive high-utilisation cycles) — recommendation: hold through v7.10, revisit once a 2nd high-utilisation cycle confirms the pattern; 42 new backlog items added (IW-20260728-01, all S/M effort, no sprint commitment made; 1 idea resolved directly as a BLG-OPS-90 gate-status update, 2 consolidated into BLG-GOV-269); Skill-Silo Alert: rolling-3-cycle avg 65.8% (v7.7/v7.8/v7.9), >40% ceiling, 2nd consecutive worsening reading (up from 64.5%) — not yet the 3-reading mandatory threshold; no ungated P1/P2 U-item exists in the backlog (BLG-FEAT-73/74 both gate-blocked) — best available advisory pull-forward candidate is BLG-FEAT-88 (P3, newly filed); Product Value Ratio 0.38 Advisory (window v7.5-v7.9, down from 0.42) — still above the 0.30 Alert floor, no mandatory pull-forward; STEP 8.1 Option (b) — defer again, no new anchor-quality item ready this cycle); prior — 2026-07-24 (rebalance 2026-07-24__scheduled — Standard tier (CPS=N/A, 0 active initiatives); no FTE changes; 34 new backlog items added (all S/M/XS effort, no sprint commitment made); Skill-Silo Alert: rolling-3-cycle avg 56.5% (v7.5/v7.6/v7.7 story counts: G+D+P=13 of 23 total), >40% ceiling, but a **net improvement** from the prior 80.9% reading (v7.1/v7.2/v7.3) — breaks the 2-consecutive-worsening streak before the v8.3 mandatory-≥2-U-items clause could trigger; Product Value Ratio 0.42 Advisory (window v7.3–v7.7, improved from 0.39) — no mandatory pull-forward; advisory candidate `BLG-FE-128` (in-app "what's new" panel, ungated) named for the next `plan release`; STEP 8.1 Option (b) — defer, no new anchor-quality item ready this cycle); prior — 2026-07-17 (out-of-band PO capacity decision, scoped edit — DL-069 — sprint capacity baseline raised ~12–14 → ~24–28 days/sprint, warn threshold 14→28; sprint cadence formally declared at ~1–2 calendar days between sprint starts; rationale: last 5 shipped cycles each closed same-day-to-next-day against declared 12–14 day effort loads); prior history retained — see prior entries in version control (last full entry retained here: 2026-07-17 out-of-band capacity decision, DL-069; chain truncated 2026-07-28 per BLG-GOV-283, header-history retention convention).

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

## Sprint Capacity & Cadence Baseline (Effective 2026-07-17)

**Decision:** Sprint capacity baseline raised from ~12–14 days/sprint to ~24–28 days/sprint. Sprint cadence formally declared at ~1–2 calendar days between sprint starts, back-to-back permitted immediately after the prior cycle's post-ship closure. Out-of-band PO capacity decision (scoped edit, not a full roadmap rebalance) — actioned directly at PO request per session 2026-07-17.

| Field | Previous | Revised |
|-------|----------|---------|
| Per-sprint capacity | ~12–14 working days | ~24–28 working days |
| Warn threshold | Effort > 14 days | Effort > 28 days |
| Sprint cadence | Not formally declared (ad hoc; one historical calc in this file assumed a 3-day cadence) | ~1–2 calendar days between sprint starts — back-to-back sprints permitted |
| Rationale | ~12–14 days assumed evenings/weekends solo-developer pace | Last 5 shipped cycles (`2026-07-10__release-v6.9` through `2026-07-16__release-v7.3`) each closed same calendar day to next-day (0–1 days elapsed) against a declared 12–14 day effort-load, indicating sustained actual throughput is at minimum double the prior baseline with headroom remaining |

This raises how many actionable (A-category, ungated) backlog items can be pulled into a single sprint's backlog slice — it does not clear gates on T/D/L-category items, which remain blocked on their stated condition regardless of declared capacity.

Release planning and sprint planning engines should use ~24–28 days per sprint as the capacity baseline going forward. A `warn` outcome is appropriate when estimated effort exceeds 28 days per sprint; `pass` when within 24–28 days. PO may acknowledge a `warn` to proceed as before.

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

---

## Rebalance 2026-07-16__scheduled

8 new backlog items (4 consolidated pre-implementation readiness passes covering 23 of 44 idea submissions + 2 cross-cutting folds, plus 4 standalone items) — all S/M/L effort, single-developer-context, no scarce-skill contention.

| Item | Effort | Skill Category | Notes |
|------|--------|-----------------|-------|
| BLG-SPEC-91 | M (~2-3 days) | Frontend / UX Spec | Command palette (BLG-FE-115) pre-implementation pass |
| BLG-SPEC-92 | L (~3-4 days) | Backend / Data Spec | Custom price alerts (BLG-FE-116) pre-implementation pass — largest of the four, spans data model + backend + security + §13 |
| BLG-SPEC-93 | M (~2 days) | Backend / QA Spec | Bulk actions (BLG-FE-117) pre-implementation pass |
| BLG-SPEC-94 | M (~2-3 days) | Data / Frontend Spec | Saved filters & calendar (BLG-FE-118) pre-implementation pass |
| BLG-OPS-112, BLG-GOV-239 | S | Ops / AI Governance | Standalone, ungated |
| BLG-FEAT-78, BLG-QA-112 | S | Product Feature / QA | Both gate-conditional (BLG-FE-116 ship; BLG-FE-115-119 release scoping respectively) |

**Governance load %:** N/A — no roadmap-initiative-level capacity consumed this cycle (backlog-level pre-work only).

**Key finding this cycle:** Skill-Silo rolling-3-cycle average worsened for the first time in 4 readings (54.2%→66.7%), driven by v7.2's all-debt/pre-work composition (0 U-tagged stories) entering the 3-cycle window while v6.9's very light 0%-reading window rolled out. This is not yet a 3+-consecutive-worsening trigger, but it is worth flagging: the next release's scope decision (naming `BLG-FE-109/110/111/115/116/117/118` as anchor candidates) is well-positioned to reverse this trend, since all 7 are genuine build-and-ship U-items.

**v7.3+ capacity outlook:** Now horizon unchanged (3 items). The 4 new pre-implementation readiness passes (`BLG-SPEC-91-94`) should be considered as fast, low-effort precursors to the next `plan release` rather than release-scope items themselves — consistent with how `BLG-SPEC-89/90` served the same function for `BLG-FE-109/110/111` ahead of v7.2.

**Workforce constraints:** None new.

---

## Rebalance 2026-07-17__scheduled

25 new backlog items (24 standalone + 1 consolidated, `BLG-SPEC-95`, covering 9 of 44 idea submissions) — all S/M/L(/XS) effort, single-developer-context, no scarce-skill contention.

| Item | Effort | Skill Category | Notes |
|------|--------|-----------------|-------|
| BLG-SPEC-95 | L (~5-7 days) | Frontend / UX / QA Spec, consolidated | v7.4 UI-heavy release readiness bundle — dependencies, UX specs, design review, Playwright/analytics/regression-tag coverage for all 4 anchor items |
| BLG-GOV-241–250 | S–M | Governance / Process | 10 standalone governance/process items (AI compliance, API contract tooling, Skill-Silo mitigation, §13 cadence, DL-069 capacity verification) |
| BLG-FEAT-79/80 | M | Product Feature | Financial reconciliation, SI-02 acceleration investigation |
| BLG-FE-120/121 | M/S | Frontend | Shared notification primitive, shared confirmation-modal component |
| BLG-BE-64–67 | S–M | Backend / Data Model | Pagination helper, error envelope, index review, position_state enum registry |
| BLG-SEC-18/19 | M/S | Security | Rate-limit audit, dependency CVE sweep cadence |
| BLG-QA-113/114 | S/M | QA / Process | Endpoint coverage audit, mock fixture standardisation |
| BLG-OPS-113/114 | S/M | Operations | window_summary archival, Render health-check alerting |

**Governance load %:** N/A — no roadmap-initiative-level capacity consumed this cycle (backlog-level pre-work only; `BLG-SPEC-95` is v7.4 pre-implementation scope, not sprint-committed).

**Skill-Silo advisory (STEP 7.1):** Rolling 3-cycle average (v7.1 6/7=85.7%, v7.2 5/5=100%, v7.3 4/7=57.1%) = **80.9%**, above the 40% ceiling — Alert persists, **2nd consecutive worsening reading** (66.7%→80.9%). Not yet the 3-reading mandatory-≥2-U-items threshold, but the trend is adverse for a 2nd straight cycle. PO response this cycle: commit all 4 `BLG-FE-115/116/117/118` build-and-ship-shaped U-items to v7.4 (pre-emptively exceeds the ≥2-item guidance) rather than wait for the mandatory trigger to fire.

**Key finding this cycle:** The v7.4 anchor scope (4 P1 U-shaped features) is now formally version-labelled (STEP 8.1 Option (a), closing `BLG-GOV-240`), giving the next `plan release v7.4` invocation a clean, already-committed U-heavy scope to draw from — the structural fix most likely to break the 2-cycle Skill-Silo worsening trend before it reaches the mandatory threshold.

**v7.4+ capacity outlook:** Now horizon = v7.4 (4 anchor items + `BLG-SPEC-95` pre-work). `BLG-SPEC-95` should be sequenced first (or in parallel) at sprint planning, consistent with the `BLG-SPEC-91-94`/`BLG-SPEC-89/90` precedent of fast, low-effort precursors ahead of the substantive feature stories.

**Workforce constraints:** None new.

---

## Rebalance 2026-07-27__scheduled

21 new backlog items (from 44 `IW-20260727-01` submissions, 23 rejected as duplicates/covered) — all S/M/L effort, single-developer-context, no scarce-skill contention.

| Item | Effort | Skill Category | Notes |
|------|--------|-----------------|-------|
| BLG-SPEC-105 | M (~2-3 days) | Data Model / Spec | trade_plan-to-position FK linkage schema documentation |
| BLG-GOV-258/259/260/261/262/263 | S–L | Governance / Process | displacement debt register, effort-band retrospective, RA-marker retirement, deferred-patch index, §12.2 threshold, cross-EPIC execution_state.json structural fix (L, ~3-5 days) |
| BLG-FE-129/130/131 | S | Frontend / Spec | dark-mode AC checklist, chart WCAG contrast checklist, motion/timing design-gate checklist |
| BLG-FEAT-85/86/87 | S–M | Product Feature | P&L tax-lot reconciliation, drift-detection metric, trailing-stop explainer tooltip |
| BLG-BE-73/74 | M | Backend | manual-override audit trail, nightly backtest data-integrity CI smoke test |
| BLG-OPS-120/121/122 | S–M | Operations | cost-tag infra spend, staging credential provisioning, CI cache warm-up |
| BLG-QA-123/124/125/126 | S–M | QA / Process | visual-regression refresh cadence, cross-EPIC smoke tagging, test.py pre-commit hook, SystemStatus.js fallback snapshot test |

**Governance load %:** N/A — no roadmap-initiative-level capacity consumed this cycle (backlog-level additions only, all `Provisional-Target: TBD`).

**Skill-Silo advisory (STEP 7.1):** Rolling 3-cycle average (v7.6 6/8=75%, v7.7 7/11=63.6%, v7.8 7/12=58.3%) = **64.5%**, above the 40% ceiling — Alert persists, **1st worsening reading** in a new streak (56.5%→64.5%), following the v7.5/v7.6/v7.7 reading that had broken the prior 2-consecutive-worsening streak. Not yet the 3-reading mandatory-≥2-U-items threshold. Advisory pull-forward candidates named: `BLG-FEAT-87` (this cycle's new trailing-stop explainer tooltip) and `BLG-FE-128` (carried from the prior cycle, still unshipped).

**Key finding this cycle:** `BLG-GOV-263` (cross-EPIC `execution_state.json` structural fix, L effort) is the highest-effort item filed this cycle and directly addresses a cost that has scaled up across 3 consecutive multi-EPIC sprints (v7.6→v7.8) — worth prioritising ahead of further Skill-Silo-adjacent process items, since it reduces recurring execution-engine overhead rather than adding another one-off governance document.

**v7.9+ capacity outlook:** Now horizon empty (STEP 8.1 Option (b) deferred). No committed scope yet — next `plan release` should draw from this cycle's ungated U-shaped additions (`BLG-FEAT-87`) plus the still-open `BLG-FE-128` to address the Skill-Silo trend before it reaches 3 consecutive worsening readings.

**Workforce constraints:** None new.

---

## Rebalance 2026-07-28__scheduled

42 new backlog items filed (from 44 `IW-20260728-01` submissions; 1 idea resolved directly — `BLG-OPS-90` gate-status update, no new row; 2 ideas consolidated into one item, `BLG-GOV-269`) — all S/M effort, single-developer-context, no scarce-skill contention.

| Item | Effort | Skill Category | Notes |
|------|--------|-----------------|-------|
| BLG-GOV-265–282 (18 items) | S–M | Governance / Process / AI Compliance / Metrics | Process trackers, checklists, spec-cross-reference checks, one gate-status resolution follow-through (`BLG-OPS-90`) |
| BLG-SEC-22/23 | S | Security | Pre-commit secrets-scanning gate; AI-endpoint security checklist |
| BLG-BE-75/76/77/78 | M | Backend Engineering | Retry/backoff extension, idempotency-key pattern, trade-plan audit trail, auto-generated data dictionary |
| BLG-FE-132/133/134 | S–M | Frontend / UX | Base44 theme-compliance prompt section, ad hoc component inventory, keyboard-nav/focus-order audit |
| BLG-SPEC-106/107/108 | S | Spec Debt | OpenAPI auth-scheme completeness, FX audit-trail completeness, form-validation-message spec |
| BLG-QA-128–134 (7 items) | S–M | QA / Testing | Contract check, DEV-* consolidation + trend index, shard-balance audit, staging sign-off tracker, endpoint coverage audit, regression runtime budget |
| BLG-OPS-123/124/125/126 | S | Operations | DB storage cost trend, Render build-path-filter audit (2nd `BLG-OPS-90`-class incident confirmed), commit-format lint hook, backup/DR runbook |
| BLG-FEAT-88 | M | Product Feature | P&L/tax reconciliation report — the only new genuinely user-facing (U) item filed this cycle |

**Governance load %:** ~90% (38 of 42 items are GOV/SEC/SPEC/QA-process/BE-tech-debt; only `BLG-FEAT-88` is a clean U-shaped feature, and 3 more — `BLG-FE-132/133/134`, `BLG-BE-77/78` — are frontend/backend but debt/process-shaped, not user-visible features). This is the most governance/debt-heavy idea-intake window on record, consistent with the "genuinely novel user-facing ideas are increasingly rare at this backlog scale" observation first noted at `2026-07-27__scheduled`.

**Skill-Silo advisory (STEP 7.1):** Rolling 3-cycle average (v7.7 7/11=63.6%, v7.8 7/12=58.3%, v7.9 11/15=73.3%) = **65.8%** (25 of 38 stories), above the 40% ceiling — Alert persists, **2nd consecutive worsening reading** (64.5%→65.8%), following the 1st worsening reading recorded at `2026-07-27__scheduled`. Not yet the 3-reading mandatory-≥2-U-items threshold, but one more worsening reading at the next completed cycle would trigger it. **Candidate gate verification (LP-05) performed:** the two most obvious P1 U-shaped candidates, `BLG-FEAT-73` (SI-02 frontend) and `BLG-FEAT-74` (PO-05 replay mode), are both still gate-blocked (SI-02 confirmed NOT MET again today via the EPIC-08 live re-check — see STEP 2.3 note; PO-05 has no §13 pre-clearance and is VH effort) — neither qualifies as an ungated candidate. No other ungated P1/P2 U-item exists in the backlog at all (checked structurally: every ungated `BLG-FEAT-*`/`BLG-FE-*` item at P1/P2 is debt/refactor-shaped, not build-and-ship). Advisory pull-forward candidate named for next `plan release`: **`BLG-FEAT-88`** (P&L/tax reconciliation report, P3, newly filed this cycle, ungated, genuinely user-facing) — the best available candidate under the letter of the rule, though its P3 priority and the absence of any ungated P1/P2 U-item is itself the more important finding here.

**Sprint capacity re-evaluation (this cycle's specific trigger — user asked "should I increase sprint capacity?" ahead of this rebalance):** Held unchanged at ~24–28 working-day-equivalent units (Effective 2026-07-17). `v7.9` ran at ~95–110% utilisation (top of band) and shipped all 15 items clean with zero deviations — the same shape of evidence (sustained high throughput, no strain) that justified the 2026-07-17 raise, but that raise was backed by **5 consecutive cycles** at high utilisation before being adopted; `v7.9` is only the **first** cycle at the top of the *current* band. No sprint has run since `v7.9` closed (this is a scheduled rebalance, not a completion-triggered one), so there is no second data point yet. Recommendation stands: hold the ceiling through `v7.10` and revisit at the next capacity-relevant checkpoint (next scheduled rebalance or post-ship closure) once a second high-utilisation cycle confirms the pattern rather than raising on one data point.

**v7.10+ capacity outlook:** Now horizon empty (STEP 8.1 Option (b) deferred again — see `cycle_record.md`). Next `plan release` should draw from the now-181-item-strong A-category (ungated, actionable) backlog pool; `BLG-FEAT-88` is the lead Skill-Silo-mitigating U-item candidate if the PO wants to pre-empt the 3rd-consecutive-worsening threshold before it fires.

**Workforce constraints:** None new.

---

## Rebalance 2026-08-11__scheduled

39 new backlog items filed (from 44 `IW-20260809-01` submissions; 1 idea resolved directly — `BLG-BE-30` gate removal, no new row; 6 ideas consolidated into 3 items — `BLG-BE-91`, `BLG-SPEC-124`, `BLG-GOV-303`; 1 idea rejected strong) — all S/M effort, single-developer-context, no scarce-skill contention.

| Item | Effort | Skill Category | Notes |
|------|--------|-----------------|-------|
| BLG-GOV-299–306 (8 items) | S–M | Governance / Process / FinOps / Strategy Policy | Cost retrospectives, workload-threshold definition, escalation tracker, Roadmap Unlock Tracker (consolidated), gate re-estimate cadence, §13 policy question, change-justification template |
| BLG-SEC-30/31/32 | S–M | Security | Gemini prompt-injection test, rate-limit audit, dependency license scan |
| BLG-BE-89–94 (6 items) | S–M | Backend Engineering | Gemini retry/backoff extension, N+1 query audit, trade-plan linkage enforcement + DB safeguard (consolidated, escalated P1), multi-currency rounding check, tax-year boundary export check, Research View latency review |
| BLG-SPEC-119–128 (10 items) | S–M | Spec Debt | Endpoint sunset tracker, contract freshness check, Base44 provenance tag + diff checklist, gated DataState variant (consolidated), prop-naming audit, spec-to-backlog traceability audit, glossary consolidation, 90-day window definition, gate-metric naming consistency |
| BLG-QA-140–147 (8 items) | S | QA / Testing | Field-population audit, DEV-* recurrence report, DoD spot-check, service-layer coverage report, Arc5ComplianceSection Playwright audit, test-env parity check, test.py re-audit, regression trend report |
| BLG-OPS-139/140/141 | S | Operations | Render headroom reassessment, build/deploy path filter documentation (prevents a 3rd `BLG-OPS-82/90`-class incident), staging data-reset cadence |
| BLG-FEAT-84 | M | Product Feature | Thesis pre-mortem / invalidation-condition capture |

**Governance load %:** ~92% (36 of 39 items are GOV/SEC/SPEC/QA-process/OPS-shaped; only `BLG-FEAT-84` is a clean U-shaped feature, and `BLG-BE-91` — while D-shaped, not U — is this cycle's single highest-leverage item, see below). The most governance/debt-heavy idea-intake window on record by this measure, exceeding even `2026-07-28__scheduled`'s ~90%.

**Skill-Silo advisory (STEP 7.1):** Rolling 3-cycle average (v8.3 27/27=100%, v8.4 29/31=93.5%, v8.5 19/25=76.0%) = **89.8%**, above the 40% ceiling — Alert persists, **3rd consecutive worsening reading** (65.8%→89.8%, following 56.5%→64.5%→65.8% at the prior three readings). **This crosses the mandatory-≥2-build-and-ship-U-item pull-forward threshold for the first time since the clause was adopted (v8.3).** Exhaustive candidate gate verification (LP-05) — including a corrected re-scan of P3 `Product Feature / Analytics` items previously missed by a blank-line-boundary scan artefact — found exactly **1** qualifying ungated candidate (`BLG-FEAT-32`, gate cleared: PT-04 shipped v6.1) against a requirement for 2. Product Owner response: accept the shortfall with written rationale (no second genuine candidate exists — every other item in the backlog is either governance/debt-shaped or gated on conditions tracing back to the same root cause), name `BLG-FEAT-32` (escalated P3→P2) as the sole candidate, and commit the next release's highest-leverage capacity to the structural fix (`BLG-BE-91`, escalated to P1) instead of a second performative candidate naming. Full reasoning in `cycle_record.md` STEP 7.1.

**Cross-role workload balance (STEP 7.2):** Not recomputed this cycle (advisory-only, no material change expected — see `cycle_record.md` STEP 7.2).

**v8.6+ capacity outlook:** Now horizon empty (STEP 8.1 Option (b) deferred, 4th consecutive firing). Next `plan release` should prioritise `BLG-FEAT-32` (P2, ungated, clean U-item) and `BLG-BE-91` (P1, root-cause structural fix for the SI-02/Arc-5 blocker cluster) ahead of further governance/debt scope, to begin correcting both the Product Value Ratio and Skill-Silo readings before a 4th consecutive worsening reading compounds the finding further.

**Sprint capacity:** Not re-evaluated this cycle (no explicit trigger; held at ~24-28 working-day-equivalent units per the `2026-07-28__scheduled` reasoning, unchanged — `v8.0`–`v8.5` all shipped at or near full planned scope with 1.00 average velocity ratio, no strain signal).

**Workforce constraints:** None new.
