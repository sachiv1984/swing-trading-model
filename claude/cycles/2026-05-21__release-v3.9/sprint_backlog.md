Owner: Product Owner
Class: Planning Document (Class 4)
Status: Sealed
Last Updated: 2026-05-22
Cycle: 2026-05-21__release-v3.9

---

# Sprint Backlog — v3.9

---

## Sprint Scope

**Firm stories:** 12 (ST-01–ST-12)
**Conditional stories:** 2 (ST-13, ST-14 — deferred_at_planning; PT-04 gate not met)
**Sprints:** 2

---

## Merge Order

**Sprint 1:** EPIC-02 → EPIC-01

**Sprint 2:** EPIC-04 → EPIC-03

**execution_state.json owner:** EPIC-02 (first EPIC in execution order — creates cycle-wide execution_state.json at STEP 0; all subsequent EPICs append their section).

**Shared file rebasing (mandatory):**
- `docs/reference/openapi.yaml`: EPIC-02 owns canonical at Sprint 1 merge; EPIC-01 rebases after EPIC-02 merges; EPIC-03 rebases after EPIC-01 merges before finalising its openapi changes
- `backend/database.py`: same rebase sequence as openapi.yaml
- All later EPICs must `git merge origin/main` before finalising changes to any shared file

---

## Sprint 1

### EPIC-02 — Ticker Universe Management Enhancements

**Branch:** `exec/2026-05-21__release-v3.9/EPIC-02`
**Owner:** Head of Backend Engineering; Head of UX & Design
**Delegation class:** autonomous
**Effort:** ~0.5–1 day
**Risk:** RISK-02

#### ST-05 — Strip .L suffix from Ticker Universe page display labels

**Delegation:** autonomous
**Effort:** XS
**AC reference:** `stage4_backlog_slice.md#ST-05`
**Spec references:**
- `docs/specs/frontend/pages/ticker_universe.md`
- `tests/e2e/ticker-universe.spec.js` (SC-TU-DISP-01)
**Test scenarios:** `tests/e2e/ticker-universe.spec.js` — SC-TU-DISP-01 (LSE suffix stripped in display)

#### ST-06 — Add company_name column to ticker universe and display on management page

**Delegation:** autonomous
**Effort:** S
**AC reference:** `stage4_backlog_slice.md#ST-06`
**Spec references:**
- `docs/specs/frontend/pages/ticker_universe.md`
- `docs/specs/api_contracts/ticker_universe_api_contract.md`
- `tests/e2e/ticker-universe.spec.js` (SC-TU-COMP-01)
**Test scenarios:** `tests/e2e/ticker-universe.spec.js` — SC-TU-COMP-01 (company name visible)

---

### EPIC-01 — Screener Data Quality & Reliability

**Branch:** `exec/2026-05-21__release-v3.9/EPIC-01`
**Owner:** Head of Backend Engineering; Head of UX & Design
**Delegation class:** autonomous
**Effort:** ~2–3 days
**Risk:** RISK-01

#### ST-01 — Fix Yahoo Finance crumb/401 rate-limiting in screener batch

**Delegation:** autonomous
**Effort:** M
**AC reference:** `stage4_backlog_slice.md#ST-01`
**Spec references:**
- `backend/services/screener_batch_service.py` (implementation target)
**Test scenarios:** unit tests — crumb refresh trigger, backoff; integration test

#### ST-02 — Fix sector/industry data silently dropped in screener batch

**Delegation:** autonomous
**Effort:** XS
**AC reference:** `stage4_backlog_slice.md#ST-02`
**Spec references:**
- `backend/services/screener_batch_service.py` (implementation target)
**Test scenarios:** unit test — sector/industry propagation through batch → compute_screener_result

#### ST-03 — Remove invalid DAY ticker and investigate PHNX.L from ticker universe

**Delegation:** autonomous
**Effort:** XS
**AC reference:** `stage4_backlog_slice.md#ST-03`
**Spec references:**
- `backend/tickers_full_list.csv` (implementation target)
**Test scenarios:** manual verification against screener run

#### ST-04 — Add degraded-run warning banner to screener results page

**Delegation:** autonomous
**Effort:** S
**AC reference:** `stage4_backlog_slice.md#ST-04`
**Spec references:**
- `docs/specs/frontend/pages/screener_results.md`
- `docs/design/2026-05-21__release-v3.9/degraded-run-banner/ux_spec.md`
- `tests/e2e/screener.spec.js` (SC-SCR-DEG-01, SC-SCR-DEG-02)
**Test scenarios:** `tests/e2e/screener.spec.js` — SC-SCR-DEG-01 (banner present), SC-SCR-DEG-02 (banner absent)

---

## Sprint 2

### EPIC-04 — Governance & Process Patches

**Branch:** `exec/2026-05-21__release-v3.9/EPIC-04`
**Owner:** Head of Specs Team; Director of Quality
**Delegation class:** autonomous
**Effort:** ~2–3 days
**Risk:** RISK-04
**Pre-execution note:** Director of Quality must confirm ST-12 PR template checklist item is active before this EPIC's execution begins (CF-3 2-cycle escalation).

#### ST-09 — execution_prompt.md patches — test_scenarios guidance and createPageUrl delegation note

**Delegation:** autonomous
**Effort:** S
**AC reference:** `stage4_backlog_slice.md#ST-09`
**Spec references:**
- `claude/system/execution_prompt.md`
- `claude/system/OPERATIONAL_GUIDE.md`
- `claude/system/prompt_change_log.md`
**Test scenarios:** governance-drift skill post-commit

#### ST-10 — sprint_planning_prompt.md patch — planning-deferred items in execution_state.json

**Delegation:** autonomous
**Effort:** S
**AC reference:** `stage4_backlog_slice.md#ST-10`
**Spec references:**
- `claude/system/sprint_planning_prompt.md`
- `claude/system/OPERATIONAL_GUIDE.md`
- `claude/system/prompt_change_log.md`
**Test scenarios:** governance-drift skill post-commit

#### ST-11 — BLG-GOV-25 — Add --dry-run support to plan release and run delivery verification

**Delegation:** autonomous
**Effort:** M
**AC reference:** `stage4_backlog_slice.md#ST-11`
**Spec references:**
- `claude/system/release_planning_prompt.md`
- `claude/system/delivery_verification_prompt.md`
- `claude/system/shared_standards.md`
- `claude/system/OPERATIONAL_GUIDE.md`
- `claude/system/prompt_change_log.md`
**Test scenarios:** manual dry-run invocation to verify no writes; governance-drift skill post-commit

#### ST-12 — QA evidence pre-merge enforcement — PR template checklist item

**Delegation:** autonomous
**Effort:** S
**Authority:** Director of Quality
**AC reference:** `stage4_backlog_slice.md#ST-12`
**Spec references:**
- `.github/pull_request_template.md`
**Test scenarios:** manual review of PR template

---

### EPIC-03 — Arc 5 Red Flag Journal (SI-03)

**Branch:** `exec/2026-05-21__release-v3.9/EPIC-03`
**Owner:** Head of Backend Engineering; Head of UX & Design
**Delegation class:** autonomous
**Effort:** ~3–4 days
**Risk:** RISK-03
**Pre-execution note:** SI-01 stores override acknowledgement as BOOLEAN on trade_plans only — no events table exists. ST-07 must create `red_flag_events` table and add event write path to pre-entry validation override flow (per sprint planning RISK-03 resolution).

#### ST-07 — Red Flag Journal — data model and backend

**Delegation:** autonomous
**Effort:** M
**AC reference:** `stage4_backlog_slice.md#ST-07`
**Spec references:**
- `docs/specs/api_contracts/portfolio_endpoints.md`
- `docs/reference/openapi.yaml`
- `backend/routers/test.py`
**Test scenarios:** unit tests — empty journal, pagination, filter by event_type, filter by ticker; integration test for SI-01 event write path

#### ST-08 — Red Flag Journal — frontend display

**Delegation:** autonomous
**Effort:** M
**AC reference:** `stage4_backlog_slice.md#ST-08`
**Spec references:**
- `docs/specs/frontend/pages/red_flag_journal.md`
- `docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md`
- `tests/e2e/red-flag-journal.spec.js` (SC-RFJ-01, SC-RFJ-02, SC-RFJ-03)
**Test scenarios:** `tests/e2e/red-flag-journal.spec.js` — SC-RFJ-01 (page renders with mocked events), SC-RFJ-02 (empty state), SC-RFJ-03 (filter narrows results)

---

## Deferred at Planning

| Story | EPIC | Gate Condition |
|-------|------|----------------|
| ST-13 | EPIC-05 | 20+ closed trades not confirmed by PO (2026-05-22) |
| ST-14 | EPIC-05 | 20+ closed trades not confirmed by PO (2026-05-22); depends on ST-13 |

---

## Product Owner Sign-Off

Product Owner: Approved
Date: 2026-05-22
