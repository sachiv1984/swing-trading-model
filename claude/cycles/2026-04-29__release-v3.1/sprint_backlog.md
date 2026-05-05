**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-04-29
**Cycle:** 2026-04-29__release-v3.1
**Release:** v3.1
**Sprint Goal:** Establish the Arc 2 foundation by delivering the Trade Plan object (data model spec, backend CRUD, and frontend creation flow), the Pre-Trade Research View backend aggregation endpoint, and completing Arc 1 with the Earnings Calendar integration — alongside the P1 UK screener bug fix, security and governance documentation, and two governance prompt patches from carry-forward.
**Backlog Slice Source:** original stage4_backlog_slice.md

---

# Sprint Backlog — 2026-04-29__release-v3.1

---

## Sprint Scope

---

### EPIC-01 — Arc 2 Foundation: Trade Plan Object

**Maps to:** S2-01
**Owner:** Head of Specs Team + Data Model Domain & Schema Owner
**Estimated effort:** ~6.0 days (ST-01: 0.75d + ST-02: 2.5d + ST-03: 2.5d + spec authoring compression expected)
**Risk IDs:** RISK-01 (no canonical spec yet), RISK-02 (design gate for frontend)
**Execution sequence:** Sprint 1 (ST-01, ST-02), Sprint 2 (ST-03)

#### ST-01 — Trade Plan spec authoring: data model schema + API contract

**Owner:** Head of Specs Team + Data Model Domain & Schema Owner
**Estimated effort:** S (~0.75 day)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None
**Notes:** Must complete before ST-02 begins. Data Model Domain & Schema Owner and HoST sign-off required before ST-02 can start. RISK-01 mitigation.

---

#### ST-02 — Trade Plan backend: migration, CRUD endpoints, test registration

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M (~2.5 days)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** ST-01 (must complete first)
**Notes:** Unblocks ST-03 (Sprint 2) and ST-04 (Sprint 2). Requires ST-01 spec sign-off before start.

---

#### ST-03 — Trade Plan frontend: creation flow and detail view

**Owner:** Head of Specs Team (frontend delivery — autonomous engine)
**Estimated effort:** M (~2.5 days)
**Sprint:** Sprint 2
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** ST-02 (backend must be live), design gate pass (satisfied — passed 2026-04-29)
**Notes:** Test scenario gap flag (LL-v2.0-P4-2): new data entry form surface → `test_scenarios` in execution_state.json must be set to "pending — QA & Testing Owner to author before next sprint on this domain" at execution time.

---

### EPIC-02 — Pre-Trade Research View Foundation

**Maps to:** S2-02
**Owner:** Head of Specs Team + API Contracts & Documentation Owner
**Estimated effort:** ~3.25 days (ST-04: 0.75d + ST-05: 2.5d)
**Risk IDs:** RISK-02 (PT-02 frontend deferred to v3.2 — design gate gates v3.2 delivery)
**Execution sequence:** Sprint 2 only (depends on EPIC-01 ST-02 complete)

#### ST-04 — Pre-Trade Research View API contract spec authoring

**Owner:** Head of Specs Team + API Contracts & Documentation Owner
**Estimated effort:** S (~0.75 day)
**Sprint:** Sprint 2
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** ST-02 (Trade Plan data model available as context)
**Notes:** Must complete before ST-05 begins. API Contracts Documentation Owner sign-off required.

---

#### ST-05 — Pre-Trade Research View backend: aggregation endpoint

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M (~2.5 days)
**Sprint:** Sprint 2
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** ST-04 (spec must precede implementation)
**Notes:** PT-02 frontend is explicitly deferred to v3.2 pending design gate. This story delivers the backend foundation only. Graceful nulls required for data not yet available (DS-04 earnings if not complete at ST-05 time).

---

### EPIC-03 — Arc 1 Completion & Screener Quality

**Maps to:** S2-03, S2-04
**Owner:** Backend Engineering Patterns Owner + QA & Testing Owner
**Estimated effort:** ~7.25 days (ST-06: 0.5d + ST-07: 2.0d + ST-09: 0.75d + ST-08: 2.0d + ST-10: 2.0d)
**Risk IDs:** RISK-03 (DS-04 Yahoo Finance data quality)
**Execution sequence:** Sprint 1 (ST-06, ST-07, ST-09), Sprint 2 (ST-08, ST-10)

#### ST-06 — Fix screener UK ticker display and watchlist promotion (BLG-FE-20)

**Owner:** Backend Engineering Patterns Owner (frontend fix in autonomous delivery)
**Estimated effort:** S (~0.5 day)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** None
**Notes:** P1 priority — execute first in Sprint 1. UK-market users currently unable to correctly add tickers to watchlist. Bug fix on existing Screener.js component — no new page or controls introduced.

---

#### ST-07 — Earnings Calendar backend + OpenAPI (DS-04)

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M (~2.0 days)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** None
**Notes:** Includes spec authoring for earnings endpoints contract. RISK-03 — Yahoo Finance data quality validated during spec authoring; graceful null response if earnings date unavailable. Unblocks ST-08 in Sprint 2.

---

#### ST-09 — Screener accuracy test protocol (BLG-QA-11)

**Owner:** Director of Quality
**Estimated effort:** S (~0.75 day)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None
**Notes:** Director of Quality sign-off required. Referenced by ST-10 (Sprint 2). Protocol document delivered as `docs/qa/screener_accuracy_protocol.md`.

---

#### ST-08 — Earnings Calendar frontend (DS-04)

**Owner:** Head of Specs Team (frontend delivery — autonomous engine)
**Estimated effort:** M (~2.0 days)
**Sprint:** Sprint 2
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** ST-07 (backend must be live), design gate pass (satisfied — passed 2026-04-29)
**Notes:** Test scenario gap flag (LL-v2.0-P4-2): new UI elements on 3 existing pages (screener results table, watchlist page, open positions page) → `test_scenarios` in execution_state.json must be set to "pending — QA & Testing Owner to author before next sprint on this domain" at execution time.

---

#### ST-10 — Screener scenario library (BLG-QA-10)

**Owner:** QA & Testing Owner
**Estimated effort:** M (~2.0 days)
**Sprint:** Sprint 2
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** ST-09 (protocol as reference)
**Notes:** QA & Testing Owner sign-off required. ≥10 scenarios required covering normal, edge, and error cases. Delivered as `docs/qa/screener_scenarios.md`.

---

### EPIC-04 — Operations, Governance & Quick Wins

**Maps to:** S2-05, S2-06, S2-07
**Owner:** Infrastructure & Operations Owner + Financial Reporting & Records Owner + PMO Lead
**Estimated effort:** ~2.5 days (ST-11: 0.75d + ST-12: 0.75d + ST-13: 0.5d + ST-14: 0.5d)
**Risk IDs:** RISK-04 (governance prompt patches require CLAUDE.md §6 checklist)
**Execution sequence:** Sprint 1 — all four stories

#### ST-11 — Monthly P&L summary report (BLG-FEAT-19)

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** S (~0.75 day)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None
**Notes:** Backend endpoint + frontend extension to existing reporting section. Not a new page — extends existing financial reporting UI with a new monthly breakdown table.

---

#### ST-12 — External API security policy docs & dependency risk register (BLG-SEC-03, BLG-SEC-04, BLG-GOV-17)

**Owner:** Cybersecurity & Trust Lead + PMO Lead
**Estimated effort:** S (~0.75 day combined)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** None
**Notes:** Three documents: Alpaca key rotation policy, external API credential inventory, external API dependency register. Cybersecurity & Trust Lead acceptance required for first two; PMO Lead acceptance for third.

---

#### ST-13 — execution_prompt.md §3.1.A reclassification backfill instruction (CF-01)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** Governance prompt patch — CLAUDE.md §6 checklist mandatory (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry, all 4 steps). Can be committed together with ST-14 in a single version bump. RISK-04 item.

---

#### ST-14 — execution_prompt.md STEP 8.5 output target fix (CF-02)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Sprint:** Sprint 1
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None
**Notes:** Governance prompt patch — CLAUDE.md §6 checklist mandatory. Can combine with ST-13 into single version bump commit. Optional CF-03 Playwright `waitFor` advisory may be included as a brief note in E2E testing guidance section. RISK-04 item.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~10 days |
| Total estimated effort (in-scope) | ~18.75 days |
| Utilisation | ~188% |
| Over-allocation | Yes — accepted by Product Owner (2026-04-29) |

---

## Items Deferred This Sprint

None — all 14 backlog slice items included in scope.

---

## Deferred Execution Blockers Accepted

N/A — `deferred_execution_blockers` was empty.

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| CF-03: Adopt Playwright `waitFor` pattern at next E2E authoring session | QA & Testing Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — sprint planning initiated 2026-04-29 with full knowledge of scope and capacity WARN
**Scope confirmed:** Confirmed — all 14 stories included; over-allocation accepted per standard-mode protocol
**Capacity confirmed:** Confirmed — WARN acknowledged; capacity_warn_acknowledged = true
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-04-29
