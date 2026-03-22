**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-03-22
**Cycle:** 2026-03-21__release-v2.2
**Release:** v2.2
**Sprint Goal:** Ship a secured, observable alert system: authenticate the Render API against public access, complete the alert engine with configurable thresholds and evaluation history, close QA scenario gaps from v2.1, and deliver three governance process improvements that streamline all future cycles.
**Backlog Slice Source:** claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md (original)

---

# Sprint Backlog — v2.2 Security, Alert Maturity & Quality

---

## Sprint 1 — Security + Quick Wins + Alert Design

---

### EPIC-01 — Security Hardening

**Maps to:** S2-01
**Owner:** Cybersecurity & Trust Lead + Backend Engineering Patterns Owner + Base44 Frontend Prompt Owner
**Estimated effort:** ~1–1.5 days
**Risk IDs:** RISK-01
**Execution sequence:** 1 (highest priority — ship before any other EPIC)

#### ST-01 — API Key Authentication for Render Deployment

**Owner:** Backend Engineering Patterns Owner + Base44 Frontend Prompt Owner
**Estimated effort:** M (~1 day)
**Delegation class:** delegated_backend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None — first priority
**Notes:** Backend middleware + frontend env-var wiring must ship together in same EPIC-01 branch (same PR or back-to-back PRs). DoQ must confirm: (a) no endpoint left unprotected; (b) frontend env-var wiring confirmed; (c) 401 path tested. RISK-01: coordinated frontend+backend change — do not merge backend without frontend side ready.

---

#### ST-02 — Content Security Policy Headers

**Owner:** Cybersecurity & Trust Lead + Base44 Frontend Prompt Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** Can bundle with ST-01 PR or follow immediately in same EPIC-01 branch
**Notes:** Frontend config change only (meta tag or Render headers). No UX change. Browser console clean verification required.

---

### EPIC-03 — Bug Fixes & Operational Quick Wins

**Maps to:** S2-03
**Owner:** Head of Engineering + Infrastructure & Operations Owner + Base44 Frontend Prompt Owner
**Estimated effort:** ~0.5–1 day
**Risk IDs:** RISK-03
**Execution sequence:** 2 (can run in parallel with EPIC-01; no dependency)

#### ST-06 — Fix CSV Export Function Name Import Bug

**Owner:** Head of Engineering
**Estimated effort:** XS (<15 min)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** None
**Notes:** Bundle with ST-07 and ST-08 into a single EPIC-03 PR. Confirm incorrect import present before fix (regression note in PR). RISK-03: verify `GET /trades/export/csv` returns valid CSV without ImportError after fix.

---

#### ST-07 — Fix Slippage StatsCard Gradient Key

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** XS (<30 min)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** None
**Locked spec:** `docs/specs/frontend/pages/trade_history.md` v1.3
**Notes:** Replace `"cyan"` gradient key with a supported key (e.g. `"slate"` or `"violet"`). Code review sufficient for DoQ sign-off; visual check preferred. Bundle with ST-06 and ST-08 in EPIC-03 PR.

---

#### ST-08 — Health Check Endpoint

**Owner:** Infrastructure & Operations Owner + Backend Engineering Patterns Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None
**Notes:** `GET /health` must return 200 with JSON schema per AC-1. `openapi.yaml` update required in same commit. Bundle with ST-06 and ST-07 in EPIC-03 PR.

---

### EPIC-02 — Alert System Maturity (Sprint 1 item only)

**Maps to:** S2-02
**Owner:** Product Owner + Backend Engineering Patterns Owner + Data Model & Domain Schema Owner
**Estimated effort (full EPIC):** ~5–7 days
**Risk IDs:** RISK-02
**Execution sequence:** 3 (Sprint 1 item is design decision; implementation items in Sprint 2)

#### ST-03 — Alert Scheduling: Define Trigger Mechanism and Rule Behaviour

**Owner:** Product Owner (decision) + Backend Engineering Patterns Owner (spec authoring)
**Estimated effort:** S–M (~0.5–1 day)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** None (first item in EPIC-02; gates ST-04 and ST-05)
**Notes:** This is a design + spec story. Product Owner must document: (a) evaluation frequency; (b) cooldown policy; (c) market_regime_change source of truth; (d) preferred trigger mechanism. Decisions documented in `docs/product/decisions/` or `docs/specs/` update. No implementation in this story. **ST-04 and ST-05 may not begin until ST-03 AC 1–4 are complete.** RISK-02: if PO defers scheduling to v2.3, must be explicitly documented in ST-03 output with deferred implementation options stated.

---

## Sprint 2 — Alert Maturity + QA Coverage

**Gate: ST-03 complete before ST-04 and ST-05 begin**

---

### EPIC-02 — Alert System Maturity (Sprint 2 items)

**Execution sequence:** 4 (Sprint 2, EPIC-02 implementation — gated on ST-03)

#### ST-04 — Alert Threshold Customisation

**Owner:** Backend Engineering Patterns Owner + Base44 Frontend Prompt Owner
**Estimated effort:** M (~2–3 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** ST-03 (must be complete — scheduling design + schema confirmed)
**Locked spec:** `docs/specs/frontend/pages/notifications.md` v0.2
**Design artefact:** `docs/design/2026-03-21__release-v2.2/alert-threshold-customisation/ux_spec.md`
**Notes:** New threshold input fields on alert creation/edit UI; threshold visible on alert list view. Per design gate v0.2 spec. `alerts_endpoints.md` + `openapi.yaml` update required if request/response shape changes. DoQ: threshold customisation verified (local run or staging); default behaviour regression confirmed. **Test scenario gap flag:** QA & Testing Owner to author alert threshold customisation test scenarios before Sprint 2 delivery verification.

---

#### ST-05 — Alert History Table

**Owner:** Data Model & Domain Schema Owner + Backend Engineering Patterns Owner + Base44 Frontend Prompt Owner
**Estimated effort:** M (~2–3 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** ST-03 (scheduling design confirms evaluation frequency and what to record)
**Locked spec:** `docs/specs/frontend/pages/notifications.md` v0.2
**Design artefact:** `docs/design/2026-03-21__release-v2.2/alert-history-table/ux_spec.md`
**Notes:** New `alert_evaluations` table + `GET /alerts/history` endpoint + frontend `/notifications/history` tab. Schema migration must include down migration. `alerts_endpoints.md` + `openapi.yaml` update required in same commit. DoQ: history persists across evaluate calls (staging or local); migration runs cleanly; down migration tested. **Test scenario gap flag:** QA & Testing Owner to author alert history test scenarios before Sprint 2 delivery verification.

---

### EPIC-04 — QA Coverage (Sprint 2 items)

**Maps to:** S2-04
**Owner:** Director of Quality + QA & Testing Owner
**Estimated effort (full EPIC):** ~3.5–4 days
**Risk IDs:** RISK-04
**Execution sequence:** 5 (concurrent with EPIC-02 Sprint 2 items — no dev dependency)

#### ST-11 — Test Automation Readiness Assessment

**Owner:** QA & Testing Owner + Director of Quality
**Estimated effort:** XS–S (~0.5–1 day)
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None (but should complete before ST-12)
**Notes:** Produce readiness assessment doc in `docs/testing/` or as cycle artefact. Quantify current automation coverage. Director of Quality sign-off required.

---

#### ST-09 — Execute Notification Scenarios on Staging

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None (no dev dependency; staging must be available)
**Notes:** Execute SC-NOTIF-01 through SC-NOTIF-08. RISK-04: 3 of 8 scenarios require open positions — partial execution acceptable; document blockers per AC-3. Director of Quality sign-off on evidence record.

---

#### ST-10 — Create Watchlist Test Scenarios

**Owner:** QA & Testing Owner
**Estimated effort:** S–M (~1 day)
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** None
**Notes:** Create `docs/testing/watchlist_scenarios.md` with SC-WATCH-01 through SC-WATCH-06. SC-WATCH-06 must reference deferred AC-6 from ST-10 (v2.1) DoQ sign-off. Director of Quality sign-off.

---

## Sprint 3 — Governance + QA Traceability

---

### EPIC-04 — QA Coverage (Sprint 3 item)

**Execution sequence:** 6 (after ST-11 complete)

#### ST-12 — Spec-to-Test Traceability Matrix

**Owner:** Director of Quality + Head of Specs Team
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_qa
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** ST-11 (readiness assessment confirms scope); ST-17 shipped v2.1 (Spec Coverage Inventory — cleared)
**Notes:** Matrix for at least 3 canonical specs (alert rules, portfolio, positions recommended). Each AC maps to ≥1 scenario ID or flagged as gap. Gap entries added to TEST-GAP tracking. Director of Quality + Head of Specs Team sign-off.

---

### EPIC-05 — Governance Process Enhancements

**Maps to:** S2-05
**Owner:** Head of Specs Team
**Estimated effort:** ~3–6 days
**Risk IDs:** RISK-05
**Execution sequence:** 7 (concurrent with ST-12; no cross-EPIC dependency)

**EPIC-05 governance invariant:** All three stories (ST-13, ST-14, ST-15) require CLAUDE.md §6 edit checklist compliance for every file modified: (a) version bumped; (b) OPERATIONAL_GUIDE §14 updated; (c) phase section source prompt header updated; (d) `prompt_change_log.md` entry added — all in same commit. Do not commit without all four steps complete for each file.

#### ST-13 — Roadmap Engine: Provisional-Target Field at Backlog Promotion

**Owner:** Head of Specs Team
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None
**Notes:** Modify `roadmap_prompt.md` STEP 9 + `shared_standards.md` + `release_planning_prompt.md` STEP 1. All three files require §6 checklist (version bump, OPERATIONAL_GUIDE §14, source prompt header, prompt_change_log.md). DoQ (Head of Specs Team self-authoring): permitted; external DoQ review of checklist compliance still required.

---

#### ST-14 — Release Planning: Load scored_initiatives.md for Effort Band Handoff

**Owner:** Head of Specs Team
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None (logically paired with ST-13 — same §6 checklist pattern)
**Notes:** Modify `release_planning_prompt.md` STEP 0 + STEP 4 + `shared_standards.md`. §6 checklist required for all modified files.

---

#### ST-15 — Structured Lessons Learnt Carry-Forward Block

**Owner:** Head of Specs Team
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_decision
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None (logically paired with ST-13 and ST-14)
**Notes:** Modify `roadmap_prompt.md`, `release_planning_prompt.md`, `sprint_planning_prompt.md`, `post_ship_closure.md`. All modified files require §6 checklist. Largest set of file changes in EPIC-05 — allocate adequate time for checklist compliance.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (3 sprints) | ~9–12 days |
| Total estimated effort (in-scope) | ~13–20 days (mid: ~16 days) |
| Utilisation | ~133% at mid-point |
| Over-allocation | Yes — accepted by Product Owner (3-sprint phasing plan; EPIC-05 is lowest-risk deferral if Sprint 3 proves over-capacity) |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| (none) | — | All 15 backlog slice items are in scope across the 3-sprint phased delivery |

## Deferred Execution Blockers Accepted

*(deferred_execution_blockers was empty — section omitted)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| pip-audit: install and run before Sprint 1 execution begins | Head of Engineering | No |
| Author alert threshold customisation test scenarios | QA & Testing Owner | No (before Sprint 2 delivery verification) |
| Author alert history test scenarios | QA & Testing Owner | No (before Sprint 2 delivery verification) |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed
**Scope confirmed:** confirmed — all 15 stories across 3-sprint phased delivery; capacity WARN acknowledged; EPIC-05 identified as lowest-risk deferral if Sprint 3 proves over-capacity
**Capacity confirmed:** confirmed — WARN acknowledged; 3-sprint phasing plan accepted
**Deferred execution blockers accepted:** N/A
**Signed off by:** Product Owner
**Date:** 2026-03-22
