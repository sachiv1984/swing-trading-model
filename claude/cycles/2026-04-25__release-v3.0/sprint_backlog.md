# Sprint Backlog — 2026-04-25__release-v3.0

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-04-25
**Cycle:** 2026-04-25__release-v3.0
**Release:** v3.0
**Sprint Goal:** Deliver the Arc 1 screener engine backend (Sprint 1) and the screener results page with watchlist promotion, news panel, ops/QA extensions, and keyboard shortcuts (Sprint 2), completing the v3.0 Screener Engine & Results Page feature set.
**Backlog Slice Source:** original `claude/cycles/2026-04-25__release-v3.0/stage4_backlog_slice.md`

---

## Sprint 1

### EPIC-01 — Arc 1 Screener Engine

**Maps to:** S2-01 (DS-01)
**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Estimated effort:** ~4–6 days (H)
**Risk IDs:** RISK-01
**Execution sequence:** 1 (Sprint 1 primary deliverable)
**Sprint 1 gate:** ST-04 merged to main before Sprint 2 opens

#### ST-01 — Ticker Universe Data Model + Endpoints

**Owner:** Head of Engineering
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None
**Notes:** Foundation for EPIC-01 batch engine. DB migration must be idempotent. Default seed data from BLG-QA-09. Endpoint test suite + SystemStatus.js count update required per CLAUDE.md §2. OpenAPI spec entry required.

---

#### ST-02 — OHLCV Data Pipeline Service

**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** ST-01 (ticker_universe schema defined — soft dependency; execute after ST-01)
**Notes:** US tickers via alpaca_service.py; UK tickers (.L) via yahoo_finance_service.py. Alpaca fallback per BLG-SPEC-22 §6. All external calls mockable via BLG-QA-08 in CI. RISK-01 resolved — M effort confirmed feasible by Head of Engineering.

---

#### ST-03 — ATR + Regime Detection + Signal Scoring Engine

**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** ST-02 (OHLCV data interface defined — logical dependency; execute after ST-02)
**Notes:** Purely computational — deterministic for given OHLCV input. All tests use BLG-QA-09 synthetic data (no live API calls in tests). RISK-01 resolved — M effort confirmed feasible by Head of Engineering.

---

#### ST-04 — Screener Batch Engine + API Endpoints

**Owner:** Head of Engineering + Backend Engineering Patterns Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** ST-01 (ticker_universe table), ST-02 (OHLCV pipeline), ST-03 (computation engine)
**Notes:** `screener_results` table schema defined here. Both endpoints must be registered in test suite + openapi.yaml. Integration test using BLG-QA-08 mock harness required. **Sprint 1 gate deliverable** — must be merged to main before Sprint 2 opens.

---

### EPIC-04 — Governance, Deferred Patches & Quick Wins

**Maps to:** S2-09, S2-10, S2-11, S2-12, S2-13
**Owner:** Head of Specs Team + PMO Lead
**Estimated effort:** ~2–3 days (5 × S)
**Risk IDs:** None
**Execution sequence:** Parallel to EPIC-01 (fully independent)

#### ST-12 — execution_prompt.md §2 Deferred Patch

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** None
**Notes:** CLAUDE.md §6 governance file edit checklist applies — version bump, OPERATIONAL_GUIDE.md update, prompt_change_log.md entry required in same commit. May combine ST-12 + ST-13 in one commit if same version bump. Closes OA-v29-02.

---

#### ST-13 — execution_prompt.md §3.1.A Deferred Patch

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** ST-12 (same file — may share version bump and commit)
**Notes:** Instruction is advisory/non-blocking. If combined with ST-12 in same commit: both story IDs must appear in commit message per CLAUDE.md §2. Closes OA-v29-03.

---

#### ST-14 — prompt_change_log.md Retrospective Entries

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None
**Notes:** Scan full `## Changes` table (not top-first — per STEP -1.11 scan order note) for sprint_planning_prompt.md entries. If v2.3→v2.4 and v2.4→v2.5 entries absent: add retrospective entries. Closes OA-v29-01.

---

#### ST-15 — Consecutive Losing Streak Metric

**Owner:** Head of Engineering + PMO Lead
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None
**Notes:** Design Pre-Approved: analytics.md v1.7 §3 already specifies `loss_streak` display slot. Backend must compute and return `advanced_metrics.loss_streak` (or equivalent) from closed trades. Metric definition added to canonical metrics_definitions.md. No new API endpoint needed if existing analytics endpoint can be extended.

---

#### ST-16 — Model Version Contract for AI Journal

**Owner:** Head of Specs Team + PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`
**Dependencies:** None
**Notes:** New document creation (Class 2 or 3). Contract must be referenced in ai_audit_service.py. Closes BLG-AI-02.

---

## Sprint 2

*Sprint 2 opens after EPIC-01 ST-04 is merged to main. Design gate already passed (2026-04-25). EPIC-02 and EPIC-03 are parallel.*

### EPIC-02 — Arc 1 Screener Frontend

**Maps to:** S2-02, S2-03, S2-04 (DS-02, DS-07, BLG-FE-18)
**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** ~2–3 days (M + S + S)
**Risk IDs:** RISK-02
**Execution sequence:** 2 (Sprint 2, after EPIC-01 ST-04 merged)
**Spec locked:** `docs/specs/frontend/pages/screener_results.md` v1.0
**Pre-condition:** EPIC-01 ST-04 merged to main; design gate passed ✅

**Test scenarios flag:** EPIC-02 `test_scenarios` in execution_state.json = **pending — QA & Testing Owner to author before Sprint 2 begins** (LL-v2.0-P4-2 — new page + new user-facing controls).

#### ST-05 — Screener Results Page

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** M (~1–1.5 days)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** ST-04 (GET /screener/results endpoint merged to main)
**Notes:** Locked spec: screener_results.md v1.0 §4–§10. Route: `/screener` per screener_results.md §2. DoQ sign-off requires local run or staging evidence — code review alone insufficient for frontend-visible AC. Evidence method must be stated explicitly in DoQ block.

---

#### ST-06 — Watchlist Promotion Flow

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** ST-05 (on screener results page — scaffolding must exist)
**Notes:** Locked spec: screener_results.md v1.0 §8. Inline confirmation popover (not modal). DoQ sign-off requires evidence of promotion flow (local run or staging).

---

#### ST-07 — Screener News Panel Attachment

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** ST-05 (on screener results page — scaffolding must exist)
**Notes:** Locked spec: screener_results.md v1.0 §9. Display-only per BLG-GOV-16 §13 — no new data sources, no sentiment. **Strategy Rules Owner counter-sign required at DoQ** (execution_prompt.md v3.9 §3.2.A — domain-specific authority sign-off must appear in EPIC-02 DoQ consolidation block). Evidence method: local run for toggle behaviour.

---

### EPIC-03 — Operations, Observability & Test Quality

**Maps to:** S2-05, S2-06, S2-07, S2-08
**Owner:** Infrastructure & Operations Owner + QA & Testing Owner
**Estimated effort:** ~2 days (4 × S)
**Risk IDs:** RISK-03
**Execution sequence:** 3 (Sprint 2, parallel to EPIC-02)

**Test scenarios flag:** EPIC-03 `test_scenarios` in execution_state.json = **pending — QA & Testing Owner to author for ST-11 before Sprint 2 begins** (new keyboard shortcut reference UI; LL-v2.0-P4-2).

#### ST-08 — External API Health Check Extension

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None
**Notes:** Extends GET /health — non-breaking. Lightweight ping (not full data fetch — rate limit safety). Degraded response when external API unreachable.

---

#### ST-09 — AI Journal Monitoring Metrics

**Owner:** Infrastructure & Operations Owner + Backend Engineering Patterns Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** None (ai_audit_log table available from BLG-AI-01)
**Notes:** Non-blocking — returns `{"status": "unavailable"}` if audit data absent. Sources from ai_audit_log table.

---

#### ST-10 — AI Audit Service Unit Tests

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** None (ai_audit_service.py shipped v2.9)
**Notes:** No live DB required — mock or TestClient pattern per existing test suite. Covers ensure_ai_audit_table, log_ai_summary_run, query_audit_log.

---

#### ST-11 — Keyboard Shortcuts

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_frontend
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None
**Notes:** Locked spec: navigation.md v1.1 §Keyboard Shortcuts; design artefact: docs/design/2026-04-25__release-v3.0/keyboard-shortcuts/ux_spec.md v1.0. Display-layer event handlers only. Suppression rule for text inputs required. Sidebar footer hint implementation per navigation.md v1.1. DoQ sign-off must state which pages were tested.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~17 working days (2 sprints, solo dev) |
| Total estimated effort (in-scope) | ~10–14 days |
| Sprint 1 utilisation | ~6–9 of ~10 days |
| Sprint 2 utilisation | ~4–5 of ~7 days |
| Over-allocation | No — within capacity |
| Capacity WARN acknowledged | Yes — Product Owner 2026-04-25 |

## Items Deferred This Sprint

None — all 16 backlog slice items included.

## Deferred Execution Blockers Accepted

N/A — `deferred_execution_blockers` was empty in release plan.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| QA & Testing Owner to author test scenarios for EPIC-02 and EPIC-03 ST-11 before Sprint 2 | QA & Testing Owner | No |
| sprint_planning_prompt.md log gap retrospective entries | ST-14 (Sprint 1) | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed — 2026-04-25
**Scope confirmed:** confirmed — 2026-04-25 (all 16 stories; 2-sprint plan)
**Capacity confirmed:** confirmed — 2026-04-25 (WARN acknowledged; historical 1.00 velocity supports delivery)
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-04-25
