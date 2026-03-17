**Owner:** Sprint Execution Engine
**Class:** Supporting Document (Class 3)
**Status:** Active — updated as delegated items are completed or returned
**Version:** 0.1
**Last Updated:** 2026-03-17
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Delegation Log — v2.0 Sprint

**Cycle:** 2026-03-17__release-v2.0
**Generated:** 2026-03-17T06:00:00Z

This log records all items delegated to human owners during sprint execution. Items remain in this log until marked `completed` or `returned_to_backlog`.

---

## Summary

| Item | Delegation Class | Assigned To | Status | GH Issue |
|------|-----------------|-------------|--------|----------|
| ST-12 | `delegated_backend` | Head of Engineering | `Unblocked` | #73 |
| ST-02 | `delegated_frontend` | Base44 Frontend Prompt Owner | `Unblocked` | #75 |
| ST-04 | `delegated_backend` | Head of Engineering | `Unblocked` | #81 |
| ST-05 | `delegated_frontend` | Base44 Frontend Prompt Owner | `Unblocked` | #82 |
| ST-17 | `delegated_decision` | Head of Specs Team | `Unblocked` | #79 |
| ST-20 | `delegated_qa` | QA & Testing Owner | `blocked_qa` | #80 |
| ST-13 | `delegated_backend` | Head of Engineering + Head of Specs Team | `Unblocked` | #83 |
| ST-18 | `delegated_decision` | Head of Specs Team | `Unblocked` | #84 |
| ST-19 | `delegated_decision` | Head of Specs Team | `Unblocked` | #85 |

---

## Detail Records

---

### ST-12

**Title:** Fix GET /portfolio — add missing required fields
**EPIC:** EPIC-04
**Delegation class:** `delegated_backend`
**Assigned to:** Head of Engineering
**Priority:** P1 — Sprint item 1
**GH Issue:** #73
**Status:** `blocked_backend`
**Delegated at:** 2026-03-17T06:00:00Z

**Context:**
`GET /portfolio` does not return `initial_value`, `net_deposits`, `current_drawdown_percent`, or `peak_portfolio_value`. These 4 fields are required by `portfolio_endpoints.md` v1.9.0. This is the P1 issue from v1.10 QA (GAP-03, BLG-BE-01).

**Spec references:**
- `docs/specs/api_contracts/portfolio_endpoints.md` — GET /portfolio response schema
- `docs/specs/data_model.md §2` — positions table (source for drawdown calculation)
- `docs/testing/v1.7-qa-scenario-gaps.md — GAP-03`

**Acceptance criteria (from sprint backlog):**
- `GET /portfolio` returns `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value`
- Values match formulas in `portfolio_endpoints.md`
- `tests/test_portfolio_integration.py` assertions for these 4 fields pass
- GAP-03 scenario in `v1.7-qa-scenario-gaps.md` moves to PASS

**Completion signal:** Commit on `exec/2026-03-17__release-v2.0/EPIC-04` branch with format `[EPIC-04][ST-12] <description>`, closes #73.

---

### ST-02

**Title:** Frontend: add top_n and lookback_days controls to Signals page
**EPIC:** EPIC-01
**Delegation class:** `delegated_frontend`
**Assigned to:** Base44 Frontend Prompt Owner
**Priority:** Core
**GH Issue:** #75
**Status:** `blocked_frontend`
**Delegated at:** 2026-03-17T06:00:00Z
**Dependency:** ST-01 is `done` — `signals.md` spec is available

**Context:**
The Signals page currently uses hard-coded defaults for `top_n` (5) and `lookback_days` (252). The frontend must expose these as user controls with 500ms debounce re-fetch.

**Spec references:**
- `docs/specs/frontend/pages/signals.md v0.1` — full page spec including control behaviour
- `docs/specs/api_contracts/signal_endpoints.md` — `top_n` (int, default 5), `lookback_days` (int, default 252)

**Acceptance criteria (from sprint backlog):**
- `top_n` input (numeric, default 5, min 1) visible on Signals page
- `lookback_days` input (numeric, default 252, min 20) visible on Signals page
- Changing either value triggers API re-fetch with 500ms debounce
- Invalid values reset to defaults; no API call made for invalid input
- Empty state shown when no signals returned
- Behaviour matches `signals.md v0.1` spec in full

**Completion signal:** Commit on `exec/2026-03-17__release-v2.0/EPIC-01` branch with format `[EPIC-01][ST-02] <description>`, closes #75.

---

### ST-04

**Title:** Backend: implement GET /reports/tax-year endpoint
**EPIC:** EPIC-02
**Delegation class:** `delegated_backend`
**Assigned to:** Head of Engineering
**Priority:** Core
**GH Issue:** #81
**Status:** `blocked_backend`
**Delegated at:** 2026-03-17T06:00:00Z

**Context:**
New backend endpoint implementing the UK tax-year P&L report. The spec was pre-completed (ST-03 — `reports_endpoints.md v0.1`). This item is the backend implementation of that spec.

**Spec references:**
- `docs/specs/api_contracts/reports_endpoints.md v0.1` — full endpoint contract
- `docs/specs/data_model.md §3` — `trade_history` table (source for realised P&L)
- `docs/specs/data_model.md §2` — `positions` table (source for `estimated_unrealised_pnl`)

**Acceptance criteria (from sprint backlog):**
- `GET /reports/tax-year?year=YYYY` returns the response shape defined in `reports_endpoints.md §4`
- Realised P&L sourced from `trade_history` filtered by `exit_date` within the UK tax year (6 Apr YYYY to 5 Apr YYYY+1)
- `estimated_unrealised_pnl` sourced from open `positions.pnl` (open status, not attribution by date)
- `year` parameter > current year returns HTTP 400
- Integration tests pass (or new tests added) covering: basic tax year, empty year, future year 400, field presence

**Completion signal:** Commit on `exec/2026-03-17__release-v2.0/EPIC-02` branch with format `[EPIC-02][ST-04] <description>`, closes #81.

---

### ST-05

**Title:** Frontend: implement Tax-Year P&L Report view
**EPIC:** EPIC-02
**Delegation class:** `delegated_frontend`
**Assigned to:** Base44 Frontend Prompt Owner
**Priority:** Core
**GH Issue:** #82
**Status:** `blocked_frontend`
**Delegated at:** 2026-03-17T06:00:00Z
**Dependency:** ST-04 must be completed and live on staging before frontend integration testing

**Context:**
New Reports page (or section) implementing the tax-year P&L report view as specified in `reports.md v0.1`. Depends on ST-04 backend endpoint.

**Spec references:**
- `docs/specs/frontend/pages/reports.md v0.1` — full page spec
- `docs/specs/api_contracts/reports_endpoints.md v0.1` — response contract

**Acceptance criteria (from sprint backlog):**
- Reports page accessible from main navigation
- UK disclaimer banner displayed
- Year selector defaulting to current UK tax year; future years disabled
- Summary bar showing `total_realised_pnl_gbp`, `total_trades`, `winning_trades`, `losing_trades`, `win_rate_percent`
- Trades table with all fields per `reports_endpoints.md §4.1` response schema
- Unrealised P&L card showing `estimated_unrealised_pnl_gbp` with `unrealised_note`
- Empty state shown when `trades` array is empty
- Behaviour matches `reports.md v0.1` spec in full

**Completion signal:** Commit on `exec/2026-03-17__release-v2.0/EPIC-02` branch with format `[EPIC-02][ST-05] <description>`, closes #82.

---

### ST-17

**Title:** Specs directory audit — lifecycle compliance and gap identification
**EPIC:** EPIC-05
**Delegation class:** `delegated_decision`
**Assigned to:** Head of Specs Team
**Priority:** Core
**GH Issue:** #79
**Status:** `blocked_decision`
**Delegated at:** 2026-03-17T06:00:00Z

**Context:**
Full audit of `docs/specs/` for lifecycle compliance: correct owner fields, version headers, status values, cross-references. Also identifies any undocumented gaps (specs referenced but not existing). Effort estimated ~12 hrs mid.

**Spec references:**
- `docs/specs/` (full directory)
- `claude/charter/document_lifecycle_guide.md` (compliance standard)
- `docs/specs/Specs_Index.md` (authoritative index to check against)

**Acceptance criteria (from sprint backlog):**
- All spec documents audited against `document_lifecycle_guide.md` requirements
- Non-compliant documents flagged with backlog items filed
- New gaps identified and added to `Specs_Index.md §6` or backlog
- Audit summary committed to `claude/cycles/2026-03-17__release-v2.0/` or `docs/ops/`

**Completion signal:** Commit on `exec/2026-03-17__release-v2.0/EPIC-05` branch with format `[EPIC-05][ST-17] <description>`, closes #79.

---

### ST-20

**Title:** QA: CohortAnalysis test scenarios
**EPIC:** EPIC-05
**Delegation class:** `delegated_qa`
**Assigned to:** QA & Testing Owner
**Priority:** P3 — stretch
**GH Issue:** #80
**Status:** `blocked_qa`
**Delegated at:** 2026-03-17T06:00:00Z

**Context:**
Author or update `docs/testing/analytics_scenarios.md` with CohortAnalysis test scenarios covering `GET /analytics/cohort` endpoint and the CohortAnalysis frontend component (analytics.md §15).

**Spec references:**
- `docs/specs/frontend/pages/analytics.md §15` — CohortAnalysis component spec
- `docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort` — endpoint contract
- `docs/testing/analytics_scenarios.md` (to be created or updated)

**Acceptance criteria (from sprint backlog):**
- Test scenarios documented covering: normal cohort data, empty cohort, boundary conditions (min_trades threshold)
- Scenarios reference specific fields from `analytics_endpoints.md`
- Document committed and registered in `docs/testing/` index (if one exists)

**Completion signal:** Commit on `exec/2026-03-17__release-v2.0/EPIC-05` branch with format `[EPIC-05][ST-20] <description>`, closes #80.

---

### ST-13

**Title:** GET /portfolio/prospective-heat — spec and backend implementation (stretch)
**EPIC:** EPIC-04
**Delegation class:** `delegated_backend`
**Assigned to:** Head of Engineering + Head of Specs Team
**Priority:** P3 — stretch
**GH Issue:** #83
**Status:** `blocked_backend`
**Delegated at:** 2026-03-17T06:00:00Z
**Dependency:** ST-12 must be complete first (EPIC-04 priority ordering)

**Context:**
`GET /portfolio/prospective-heat` is referenced by the ProspectiveHeatPanel frontend component but has no spec and no backend implementation. This stretch item closes the gap: author spec in `portfolio_endpoints.md`, implement backend endpoint, enable currently-skipped `TestProspectiveHeat` tests.

**Spec references:**
- `docs/specs/api_contracts/portfolio_endpoints.md` — spec to be authored here
- `docs/specs/Specs_Index.md §6.3` — open gap record
- `tests/test_portfolio_integration.py::TestProspectiveHeat` — currently `@unittest.skip`

**Acceptance criteria (from sprint backlog):**
- `GET /portfolio/prospective-heat` spec authored in `portfolio_endpoints.md`
- Backend implementation returns the specified response shape
- `TestProspectiveHeat` skip decorator removed; all tests in that class pass
- Gap record in `Specs_Index.md §6.3` updated to RESOLVED

**Completion signal:** Commits on `exec/2026-03-17__release-v2.0/EPIC-04` branch with format `[EPIC-04][ST-13] <description>`, closes #83.

---

### ST-18

**Title:** Rewrite roadmap_prompt.md
**EPIC:** EPIC-06 (parallel governance track)
**Delegation class:** `delegated_decision`
**Assigned to:** Head of Specs Team
**Priority:** Core (parallel track)
**GH Issue:** #84
**Status:** `blocked_decision`
**Delegated at:** 2026-03-17T06:00:00Z

**Context:**
`claude/system/roadmap_prompt.md` rewrite. Governance improvement item. Does not block product EPICs. Head of Specs Team owns authoring and sign-off.

**Spec references:**
- `claude/system/roadmap_prompt.md` (rewrite target)
- `OPERATIONAL_GUIDE.md §6 and §14`
- Governance file edit checklist: `CLAUDE.md §6` must be followed — version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md entry

**Acceptance criteria (from sprint backlog):**
- `roadmap_prompt.md` rewritten per governance improvement spec
- `CLAUDE.md §6` checklist completed (version bump, OPERATIONAL_GUIDE update, change log entry)
- Head of Specs Team sign-off recorded in commit message

**Completion signal:** Commit on `exec/2026-03-17__release-v2.0/EPIC-06` branch with format `[EPIC-06][ST-18] <description>`, closes #84.

---

### ST-19

**Title:** Rewrite idea_intake_prompt.md and update shared_standards.md §16
**EPIC:** EPIC-06 (parallel governance track)
**Delegation class:** `delegated_decision`
**Assigned to:** Head of Specs Team
**Priority:** Core (parallel track)
**GH Issue:** #85
**Status:** `blocked_decision`
**Delegated at:** 2026-03-17T06:00:00Z

**Context:**
`claude/system/idea_intake_prompt.md` rewrite, `roadmap_prompt.md` STEP 4 update, and `shared_standards.md §16` schema addition. Governance improvement item. Does not block product EPICs.

**Spec references:**
- `claude/system/idea_intake_prompt.md` (rewrite target)
- `claude/system/roadmap_prompt.md STEP 4` (update target)
- `claude/system/shared_standards.md §16` (schema to be added)
- Governance file edit checklist: `CLAUDE.md §6` must be followed for each governance file modified

**Acceptance criteria (from sprint backlog):**
- `idea_intake_prompt.md` rewritten per governance improvement spec
- `roadmap_prompt.md` STEP 4 updated
- `shared_standards.md §16` schema added
- `CLAUDE.md §6` checklist completed for all files modified
- Head of Specs Team sign-off recorded

**Completion signal:** Commit(s) on `exec/2026-03-17__release-v2.0/EPIC-06` branch with format `[EPIC-06][ST-19] <description>`, closes #85.

---

## Outcome Updates (2026-03-17 — Sprint Resume)

The following items have been unblocked and completed since initial delegation. Recorded per STEP 5.0 requirement.

---

### ST-12 — Unblocked

**Status:** `Unblocked`
**Commit:** `04ed5e8` on `exec/2026-03-17__release-v2.0/EPIC-04`
**Outcome:** Fixed. Empty-positions early-return path in `portfolio_service.py` updated to call `get_total_deposits_withdrawals()` and `get_drawdown_fields()`. `TestGetPortfolioEmpty` and `TestGetPortfolioFieldContract` pass. GAP-03 scenario marked PASS.

---

### ST-13 — Unblocked

**Status:** `Unblocked`
**Commits:** `279e832` (implementation), `8858824` (backlog update) on `exec/2026-03-17__release-v2.0/EPIC-04`
**Outcome:** Spec authored (`portfolio_endpoints.md` v2.0.0) and `routers/prospective_heat.py` implemented. 7 `TestProspectiveHeat` tests pass. `@unittest.skip` removed. DEV-ST05-01 closed.

---

### ST-02 — Unblocked

**Status:** `Unblocked`
**Commit:** `3ef82f7` on `exec/2026-03-17__release-v2.0/EPIC-01`
**Outcome:** `top_n` and `lookback_days` controls added to Signals page. 500ms debounce re-fetch implemented.

---

### ST-04 — Unblocked

**Status:** `Unblocked`
**Commit:** `dde5664` on `exec/2026-03-17__release-v2.0/EPIC-02`
**Outcome:** `GET /reports/tax-year` endpoint implemented. Integration tests pass.

---

### ST-05 — Unblocked

**Status:** `Unblocked`
**Commit:** `04b765f` on `exec/2026-03-17__release-v2.0/EPIC-02`
**Outcome:** Tax Year P&L view added to Reports page as tab.

---

### ST-17 — Unblocked

**Status:** `Unblocked`
**Commit:** `8ce92ba` on `exec/2026-03-17__release-v2.0/EPIC-05`
**Outcome:** `docs/specs/spec_coverage_inventory.md` produced. 38 docs audited, 7 gap actions identified. Registered in Specs_Index.md §8.

---

### ST-18 — Unblocked

**Status:** `Unblocked`
**Commits:** `03e0060`, `7858d91` on `exec/2026-03-17__release-v2.0/EPIC-06`
**Outcome:** `roadmap_prompt.md` v3.0→v4.0: cycle_record.md pattern extended to all tiers. CLAUDE.md §6 checklist completed.

---

### ST-19 — Unblocked

**Status:** `Unblocked`
**Commit:** `a236678` on `exec/2026-03-17__release-v2.0/EPIC-06`
**Outcome:** `idea_intake_prompt.md` v1.3→v2.0: per-file model replaced with `ideas_register.md`. 44 ideas migrated. 45 files archived.

---

### ST-20 — Still blocked_qa (awaiting Director of Quality sign-off)

**Status:** `blocked_qa`
**Commit:** `4adbe21` on `exec/2026-03-17__release-v2.0/EPIC-04` (cross-branch process deviation — item belongs to EPIC-05)
**Outcome:** `docs/testing/analytics_scenarios.md` created with SC-CA-BACKEND-01, SC-CA-BACKEND-02, SC-CA-BACKEND-03. Awaiting Director of Quality sign-off in `qa_evidence_EPIC-05.md`.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-17 | Initial version. Sprint execution init — all delegated items registered. |
| 0.2 | 2026-03-17 | Outcome updates: ST-12, ST-13, ST-02, ST-04, ST-05, ST-17, ST-18, ST-19 → Unblocked. ST-20 → still blocked_qa. Summary table updated. |
