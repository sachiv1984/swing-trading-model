**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-19
**Cycle:** 2026-05-19__release-v3.8
**Release:** v3.8
**Sprint Goal:** Enrich trade plan creation with setup type, news context, and AI-assisted thesis; make `ticker_universe` the sole authoritative source; and deliver SI-01 Pre-Entry Rule Validation as a non-blocking advisory panel.
**Backlog Slice Source:** `claude/cycles/2026-05-19__release-v3.8/stage4_backlog_slice.md` (original)

---

# Sprint Backlog — 2026-05-19__release-v3.8

---

## Sprint Scope

### Merge Order (Multi-EPIC)

**Merge sequence:** EPIC-04 → EPIC-03 → EPIC-01

- **execution_state.json owner:** EPIC-04 (first in execution order). EPIC-03 and EPIC-01 check for existence before creating.
- **Shared files:** `docs/reference/openapi.yaml`, `backend/routers/test.py`, `docs/specs/data_model.md` — EPIC-04 owns canonical versions; EPIC-03 and EPIC-01 must rebase onto `main` after EPIC-04 merges.

---

### Sprint 1 — EPICs 04, 03, 01 (gate)

---

#### EPIC-04 — Platform & Governance

**Maps to:** S2-04, S2-05
**Owner:** Head of UX & Design; Head of Backend Engineering; Head of Specs Team
**Estimated effort:** 1.5–2.5 days
**Risk IDs:** RISK-04
**Execution sequence:** 1st (fewest shared file conflicts)

---

##### ST-10 — Governance Debt Clearance

**Owner:** Head of Specs Team
**Estimated effort:** XS (<0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** None
**Notes:** Execute first within EPIC-04 — fastest delivery, zero dependencies. Adds `gh_issue_template.md` to OPERATIONAL_GUIDE §14 and implements DoQ sign-off date enforcement mechanism.

---

##### ST-09 — Ticker Universe Management Page

**Owner:** Head of UX & Design; Head of Backend Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None (execute after ST-10 within EPIC-04)
**Notes:** RISK-04 — retiring `public.tickers` startup sync requires `ticker_universe` seeded with defaults before sync removal. Playwright coverage required for add/toggle/delete/filter scenarios. Backend changes (new routes) must be registered in `backend/routers/test.py` and `openapi.yaml` per CLAUDE.md §2.

---

#### EPIC-03 — Trade Plan Form Enhancements

**Maps to:** S2-03
**Owner:** Head of UX & Design; Backend Engineering Patterns Owner
**Estimated effort:** 2.0–3.0 days
**Risk IDs:** RISK-03
**Execution sequence:** 2nd (after EPIC-04 merges to main; must rebase before finalising openapi.yaml / data_model.md)

---

##### ST-06 — Setup Type Classification Field

**Owner:** Head of UX & Design; Backend Engineering Patterns Owner
**Estimated effort:** S (~0.5 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** None (first in EPIC-03 chain)
**Notes:** DB migration for `setup_type` column required. `POST /trade-plans` and `PUT /trade-plans/{id}` must accept and persist. `setup_type` registered in `openapi.yaml`. Playwright: verify dropdown renders, saves, and displays correctly. Must complete before ST-08.

---

##### ST-07 — News Context Panel on Trade Plan Form

**Owner:** Head of UX & Design
**Estimated effort:** S (~0.5 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** None (execute in parallel with ST-06 or after; Alpaca News API already integrated)
**Notes:** Backend: confirm `GET /news/{ticker}` proxy endpoint exists (screener news route) or add one. Register in `openapi.yaml` if new. collapsed state persisted in localStorage per ticker. Must complete before ST-08.

---

##### ST-08 — AI-Assisted Thesis Generation

**Owner:** Head of UX & Design; Backend Engineering Patterns Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** ST-06 (setup type dropdown must be available), ST-07 (news context panel must be available)
**Notes:** RISK-03 — ST-08 is last in the EPIC-03 dependency chain. Phase 1 template-engine only — no external API key required. Gemini integration hidden entirely (not disabled) when API key absent. "AI draft" badge required; clears on first user edit.

---

#### EPIC-01 — Arc 5 Strategy Integrity Foundation (Sprint 1 Gate)

**Maps to:** S2-01
**Owner:** Strategy Rules & System Intent Owner; Head of Backend Engineering; Head of UX & Design
**Estimated effort:** 0.5 days (Sprint 1 gate only)
**Risk IDs:** RISK-02
**Execution sequence:** 3rd (gate story ST-01 runs in Sprint 1; ST-02/ST-03 execute in Sprint 2 after §13 PASS)

---

##### ST-01 — §13 Review Gate for SI-01 Pre-Entry Rule Validation

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** XS (~0.5 days, delegated_decision)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None (gate story; no upstream dependency)
**Notes:** RISK-02 — §13 review outcome determines Sprint 2 scope. If §13 FAIL: ST-02 and ST-03 are blocked; EPIC-01 removed from Sprint 2. If §13 PASS: binding conditions recorded in `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`. ST-02 and ST-03 may not begin execution until ST-01 is `status: done`.

---

### Sprint 2 — EPIC-01 (Implementation, gated by ST-01 §13 PASS)

---

#### EPIC-01 (continued) — Arc 5 Strategy Integrity Foundation

**Estimated effort:** 2.0–4.0 days
**Execution sequence:** continues on exec branch from Sprint 1 (EPIC-01 gate; must rebase onto main after EPIC-03 merges)

---

##### ST-02 — SI-01 Backend — Pre-Entry Validation Service

**Owner:** Head of Backend Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** ST-01 §13 PASS (hard gate — do not begin until ST-01 is done)
**Notes:** `GET /portfolio/pre-entry-validation?ticker={ticker}&quantity={n}` endpoint. Non-blocking advisory output. All 5 rule types (regime gate, position sizing, sector concentration, earnings proximity, cash constraint) must be covered. Registered in `backend/routers/test.py` and `openapi.yaml`. Unit tests for all 5 rule types required. §13 binding conditions (from ST-01 decisions record) applied verbatim.

---

##### ST-03 — SI-01 Frontend — Pre-Entry Validation Panel

**Owner:** Head of UX & Design
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** ST-01 §13 PASS, ST-02 (backend endpoint)
**Notes:** Advisory panel — non-blocking. Override flow with override acknowledgement recorded on trade plan object. §13 binding conditions applied: display-only advisory, no automatic blocking of plan submission. Playwright: panel renders; override flow works; plan saves with override recorded.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~10 working days (2-sprint cycle, 1.0 FTE) |
| Total estimated effort (in-scope, 8 stories) | 5–10 days (mid ~8 days) |
| Utilisation | ~80% (mid estimate) |
| Over-allocation | No |
| EPIC-02 removed | PT-04 parked — PO decision 2026-05-19: gate not met (< 20 closed trades) |

---

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-04 — PT-04 Backend Setup Quality Score | EPIC-02 | PO decision 2026-05-19: PT-04 gate not met (< 20 closed trades); formally parked in backlog |
| ST-05 — PT-04 Frontend Setup Quality Score Display | EPIC-02 | Depends on ST-04; same gate applies |

---

## Deferred Execution Blockers Accepted

*(No deferred execution blockers — `deferred_execution_blockers` is empty in state.json.)*

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| v3.6 changelog entry reconstruction (`docs/product/changelog.md`) | PMO Lead | No — due before v3.8 closes |
| Smoke-tests.yml timeout review (if CI timeout recurs) | QA & Testing Owner | No — advisory; trigger is recurrence |
| design_gate.md merge to main (currently on hotfix branch) | PMO Lead | No — design gate passed per state.json; advisory only |

No outstanding actions marked `Blocker? Yes`. Sprint seal conditions met.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-05-19
**Scope confirmed:** Confirmed — 8 stories (EPIC-04/03/01); EPIC-02 removed (PT-04 parked, gate not met)
**Capacity confirmed:** Confirmed — ~8 days mid-estimate, no over-allocation; capacity WARN resolved by EPIC-02 removal
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-05-19
