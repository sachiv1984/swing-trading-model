**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.1
**Cycle:** 2026-04-29__release-v3.1
**Last Updated:** 2026-04-29

---

# Release Plan — v3.1 Arc 2 Start: Trade Plan Object & Pre-Trade Research Foundation

---

## Readiness

### Release Candidate Inputs

| Source | Item | Status |
|--------|------|--------|
| Roadmap §4 Arc 1 | DS-04 Earnings Calendar Integration | Deferred v3.0 → v3.1; no spec yet |
| Roadmap §4 Arc 2 | PT-01 Trade Plan Object | Roadmap-approved; no spec yet |
| Roadmap §4 Arc 2 | PT-02 Pre-Trade Research View (backend only) | Roadmap-approved; no spec yet |
| Roadmap §4 Arc 2 | PT-03 Prospective Heat at Entry | Deferred to v3.2 (with PT-02 frontend) |
| Roadmap §4 Arc 2 | PT-04 Setup Quality Score | Gate: 20+ closed trades — deferred to v3.2+ |
| Roadmap §4 Arc 2 | PT-05 Pre-Trade Entry Checklist | Deferred to v3.2 (depends on PT-02 frontend) |
| Backlog P1 | BLG-FE-20 UK ticker display & watchlist promotion bug | Provisional-Target: v3.1 |
| Backlog P2 | BLG-FEAT-19 Monthly P&L summary report | Provisional-Target: v3.1 |
| Backlog P2 | BLG-QA-10 Screener scenario library | Provisional-Target: v3.1 |
| Backlog P2 | BLG-QA-11 Screener accuracy test protocol | Provisional-Target: v3.1 |
| Backlog P3 | BLG-SEC-03 Alpaca API key rotation policy | Provisional-Target: v3.1 |
| Backlog P3 | BLG-SEC-04 External API credential audit | Provisional-Target: v3.1 |
| Backlog P3 | BLG-GOV-17 External API dependency risk register | Provisional-Target: v3.1 |
| Carry-forward CF-01 | execution_prompt.md §3.1.A reclassification backfill | Must convert to sprint story |
| Carry-forward CF-02 | execution_prompt.md STEP 8.5 output target | Must convert to sprint story |

### Readiness Checks

**Spec readiness:** PT-01, PT-02, DS-04 have no canonical specs — spec authoring is a sprint deliverable (ST-01, ST-04, part of ST-07). This is the normal Arc 2 pattern. Spec stories are sequenced first in each EPIC.

**Dependency readiness:** PT-02 backend (ST-05) depends on PT-01 backend being live. PT-02 frontend is deferred to v3.2 pending design gate. DS-04 is independent of Arc 2 items. All backlog items are self-contained.

**1.1 Backlog Age Advisory:** §7 Spec Debt Backlog: no active items. No items aged 2+ cycles without story assignment.

**1.2 Provisional-Target Advisory:** 7 items carry `Provisional-Target: v3.1`. 0 additional items have Provisional-Target matching v3.1 (PT-01/PT-02/DS-04 are roadmap items, not backlog). 2 items (CF-01, CF-02) have no Provisional-Target — carry-forward from prior cycle.

**1.3 Design Dependency Scan:** 0 scope candidate backlog items flagged with "Product Owner to decide" or design-gate language. Design gate required for Trade Plan frontend (PT-01) and Earnings Calendar frontend (DS-04) — flagged as RISK-02 and normal design gate trigger. Design dependency scan: 0 items flagged (design gate need is architecture-driven, not keyword-triggered).

---

## Scope

### Stage 2 Scope Items

| S2-ID | Epic | Description | Source |
|-------|------|-------------|--------|
| S2-01 | EPIC-01 | Arc 2 Foundation — Trade Plan Object: data model spec, backend CRUD, frontend creation/detail flow | Roadmap PT-01 |
| S2-02 | EPIC-02 | Pre-Trade Research View Foundation: API contract spec + backend data-aggregation endpoint (PT-02 frontend deferred v3.2) | Roadmap PT-02 |
| S2-03 | EPIC-03 | Arc 1 Completion: Earnings Calendar Integration (DS-04) — backend endpoint + frontend display on screener/watchlist/positions | Roadmap DS-04 |
| S2-04 | EPIC-03 | Screener Quality & Bug Fix: UK ticker display/promotion bug (BLG-FE-20, P1), screener accuracy protocol (BLG-QA-11), screener scenario library (BLG-QA-10) | Backlog P1/P2 |
| S2-05 | EPIC-04 | External API Security & Governance: Alpaca key rotation policy (BLG-SEC-03), credential audit (BLG-SEC-04), API dependency risk register (BLG-GOV-17) | Backlog P3 |
| S2-06 | EPIC-04 | Monthly P&L Summary Reporting: month-by-month P&L breakdown complementing annual tax-year report (BLG-FEAT-19) | Backlog P2 |
| S2-07 | EPIC-04 | Governance Prompt Patches: execution_prompt §3.1.A reclassification backfill (CF-01), execution_prompt STEP 8.5 output target fix (CF-02) | Carry-forward |

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| PT-02 Frontend (Pre-Trade Research View UI) | Design gate required before implementation; scope boundary with v3.2 | v3.2 |
| PT-03 (Prospective Heat at Entry) | Depends on PT-02 frontend | v3.2 |
| PT-04 (Setup Quality Score) | Gate: 20+ closed trades required; data precondition not yet met | v3.2+ |
| PT-05 (Pre-Trade Entry Checklist) | Embedded in Trade Plan flow (PT-02); deferred with PT-02 frontend | v3.2 |

---

## Execution Plan

### Epic Table

| EPIC-ID | Scope Items | Owner | Key Risk | Sequencing Constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Specs Team + Data Model Owner | RISK-01: No canonical spec for Trade Plan | Sprint 1 first; ST-01 (spec) must precede ST-02 (backend) must precede ST-03 (frontend); design gate pass required before ST-03 |
| EPIC-02 | S2-02 | Head of Specs Team + API Contracts Owner | RISK-02: PT-02 frontend design gate gates v3.2 delivery | Sprint 2 only; depends on EPIC-01 ST-02 complete; no frontend stories (deferred) |
| EPIC-03 | S2-03, S2-04 | Backend Engineering Patterns Owner + QA Owner | RISK-03: DS-04 Yahoo Finance data quality unknown | BLG-FE-20 (ST-06) Sprint 1 first (P1 bug); DS-04 spec authored before backend; QA items Sprint 2 |
| EPIC-04 | S2-05, S2-06, S2-07 | Infrastructure Ops + Financial Reporting + PMO | RISK-04: CF-01/02 patches are governance prompt changes (changelog required) | Sprint 1; all S/XS effort; must include prompt_change_log.md entries for ST-13/ST-14 |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | No canonical spec exists for Trade Plan Object (data_model.md, api_contracts) — implementation cannot begin without spec | High | ST-01 authors spec first; Data Model Domain Owner + HoST sign-off required before ST-02 begins | null |
| RISK-02 | EPIC-01, EPIC-02 | Trade Plan frontend and Pre-Trade Research View are new UI surfaces — design gate must pass before frontend stories | Medium | Design gate run (Phase 1.5) between Release Planning and Sprint Planning; PT-02 frontend deferred to v3.2 | null |
| RISK-03 | EPIC-03 | DS-04 Earnings Calendar depends on Yahoo Finance data — quality and refresh rate not yet validated for earnings dates | Medium | Spec authoring (part of ST-07) validates data source; if data quality insufficient, scope to best-effort display with data freshness caveat | null |
| RISK-04 | EPIC-04 | CF-01 + CF-02 are governance prompt patches — CLAUDE.md §6 checklist mandatory (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry) | Low | CLAUDE.md §6 checklist enforced at commit-check; commit blocked until all 4 steps complete | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**EPIC dependency chain:** EPIC-02 depends on EPIC-01 (PT-01 data model must exist before PT-02 research view aggregates it). EPIC-03 and EPIC-04 are independent of each other and of EPICs 01/02. No circular dependencies.

**Scope coverage:** All S2-xx items map to at least one EPIC. All EPICs map to at least one S2 item. RISK-01 through RISK-04 each relate to a named EPIC. No orphan scope items.

**Deferred items rationale validated:** PT-02 frontend deferred because design gate is a structural requirement before new UI pages. PT-03/PT-05 deferred because they logically depend on PT-02 frontend. PT-04 deferred because the 20+ trade gate is a data precondition. All deferral reasons are objective and testable.

**Internal consistency:** Sprint 1 scope (EPIC-03 BLG-FE-20, EPIC-04 items, EPIC-01 ST-01/ST-02) contains no unsatisfied dependencies for Sprint 1 start. Sprint 2 scope (EPIC-01 ST-03, EPIC-02 ST-04/ST-05, EPIC-03 ST-08/ST-10) correctly depends on Sprint 1 completion.

**Result: PASS** — model is internally consistent and executable.

---

## Capacity Check

**Effort estimates (inline — Arc 2 items not in scored_initiatives.md):**

| EPIC | Stories | Effort Band | Estimated Days (mid) |
|------|---------|-------------|----------------------|
| EPIC-01 | ST-01 (S), ST-02 (M), ST-03 (M) | — | 0.75 + 2.5 + 2.5 = 5.75 days |
| EPIC-02 | ST-04 (S), ST-05 (M) | — | 0.75 + 2.5 = 3.25 days |
| EPIC-03 | ST-06 (S), ST-07 (M), ST-08 (M), ST-09 (S), ST-10 (M) | from scored_initiatives: QA-10=M, QA-11=S | 0.5 + 2.0 + 2.0 + 0.75 + 2.0 = 7.25 days |
| EPIC-04 | ST-11 (S), ST-12 (S), ST-13 (S), ST-14 (S) | from scored_initiatives: SEC-03=S, SEC-04=XS, GOV-17=XS | 0.75 + 0.75 + 0.5 + 0.5 = 2.5 days |
| **Total** | 14 stories | — | **~18.75 days (mid-point)** |

**Available capacity estimate:** Solo dev, evenings/weekends, 2-sprint cycle. Assumed 8–12 days available capacity.

**Outcome: WARN** — estimated 18.75 days exceeds typical 2-sprint solo dev capacity (8–12 days). The estimate includes significant spec authoring overhead (ST-01, ST-04, part of ST-07) which is typically faster than implementation.

### Phasing Recommendation

**Available capacity:** 10 days (mid-point estimate for 2-sprint solo dev cycle)
**Estimated total effort:** ~18.75 days

**Proposed Phasing:**

Phase 1 (Sprint 1): EPIC-01 ST-01/ST-02 + EPIC-03 ST-06/ST-07/ST-09 + EPIC-04 ST-11/ST-12/ST-13/ST-14
- Estimated: 0.75 + 2.5 + 0.5 + 2.0 + 0.75 + 0.75 + 0.75 + 0.5 + 0.5 = **~9.0 days**
- Delivers: Trade Plan data model + backend, P1 bug fix, earnings calendar backend, screener protocol, governance docs
- Rationale: All spec/foundational work; no frontend work blocked by design gate

Phase 2 (Sprint 2): EPIC-01 ST-03 + EPIC-02 ST-04/ST-05 + EPIC-03 ST-08/ST-10
- Estimated: 2.5 + 0.75 + 2.5 + 2.0 + 2.0 = **~9.75 days**
- Delivers: Trade Plan frontend, Pre-Trade Research View spec + backend, earnings calendar frontend, screener scenario library
- Rationale: All frontend and complex work; design gate must clear before ST-03

Note: Sprint 2 at ~9.75 days also exceeds solo capacity. Sprint planning should review scope and consider deferring ST-10 (BLG-QA-10, M effort) or ST-05 (PT-02 backend, M effort) to v3.2 if capacity is tight. Sprint Planning Engine will make the final call.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**S2-01 → EPIC-01:** Present in Execution Plan. EPIC-01 stories (ST-01/02/03) cover spec + backend + frontend = full S2-01 scope. ✅
**S2-02 → EPIC-02:** Present in Execution Plan. EPIC-02 stories (ST-04/05) cover spec + backend = partial S2-02 scope (frontend explicitly deferred). Deferred items listed in Scope §Deferred. ✅
**S2-03 → EPIC-03:** Present. ST-07 (DS-04 backend) + ST-08 (DS-04 frontend) cover S2-03 fully. ✅
**S2-04 → EPIC-03:** Present. ST-06 (BLG-FE-20) + ST-09 (BLG-QA-11) + ST-10 (BLG-QA-10) cover S2-04 fully. ✅
**S2-05 → EPIC-04:** Present. ST-12 (BLG-SEC-03+BLG-SEC-04+BLG-GOV-17) covers S2-05 fully. ✅
**S2-06 → EPIC-04:** Present. ST-11 (BLG-FEAT-19) covers S2-06 fully. ✅
**S2-07 → EPIC-04:** Present. ST-13 (CF-01) + ST-14 (CF-02) cover S2-07 fully. ✅

**All RISK IDs referenced in EPIC table appear in Risk Register Summary:** RISK-01 through RISK-04. ✅
**All deferred items from Stage 2 explicitly listed in §Deferred:** PT-02 frontend, PT-03, PT-04, PT-05. ✅
**Stage 4 backlog slice will reference EPIC IDs exactly** (verified at STEP 4). ✅

**Result: PASS**

---

## Integrity Validation — 5.7 Decision Record Integrity

Decisions record created at STEP 3: `docs/product/decisions/decisions--2026-04-29__release-v3.1.md`. ✅

No Accepted Risk escalations were raised (all blockers resolved via scope deferral or sequencing constraints within the release). `open_escalations = []`. No AR or SRB decision records required.

**Result: NOT_APPLICABLE** (no AR/SRB decision records — no escalations raised during this planning run)
