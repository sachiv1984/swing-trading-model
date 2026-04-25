# Sprint Planning Notes — 2026-04-25__release-v3.0

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-25
**Cycle:** 2026-04-25__release-v3.0

---

## Backlog Slice Source

Original — `claude/cycles/2026-04-25__release-v3.0/stage4_backlog_slice.md`

No amendment file in use (`amended_backlog_slice_path` absent in `.claude_current_state.json`).

---

## Deferred Items

No items deferred at sprint planning. All 16 backlog slice items included within capacity.

---

## Pre-Sprint Required Decisions (from cycle_summary.md)

| Decision | Status | Notes |
|----------|--------|-------|
| [RISK-01] DS-01 ST-02/ST-03 feasibility — split if needed | **RESOLVED** | Head of Engineering confirms ST-02 (M) and ST-03 (M) feasible as individual stories. BLG-SPEC-21 provides deterministic spec; BLG-QA-09 provides test data. No split required. |
| [Design gate] Design gate for DS-02 must pass before Sprint 2 | **RESOLVED** | Design gate passed 2026-04-25. `design_gate.md` filed. Sprint 2 may open once EPIC-01 ST-04 merged. |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 (ticker_universe schema defined) | Internal — soft | Resolved (same sprint; execute ST-01 first) |
| ST-03 | ST-02 (OHLCV data interface) | Internal — logical | Resolved (same sprint; execute ST-01→ST-02→ST-03) |
| ST-04 | ST-01 (ticker_universe), ST-02 (pipeline), ST-03 (engine) | Internal — hard | Resolved (serialised in Sprint 1) |
| ST-05 | ST-04 (`GET /screener/results` endpoint) | Cross-sprint — hard | Resolved (Sprint 2 may not open until ST-04 merged to main) |
| ST-06 | ST-05 (on screener results page) | Internal EPIC-02 | Resolved (same sprint) |
| ST-07 | ST-05 (on screener results page) | Internal EPIC-02 | Resolved (same sprint) |
| ST-13 | ST-12 (same version bump — may share commit) | Internal EPIC-04 | Resolved (same sprint; execute ST-12+ST-13 together) |
| ST-08–ST-11 | None | Independent | Sprint 2 (parallel to EPIC-02) |
| ST-12, ST-14–ST-16 | None | Independent | Sprint 1 (parallel to EPIC-01) |

---

## Execution Sequence

### Sprint 1 (EPIC-01 + EPIC-04)

**EPIC-04 can run in full parallel with EPIC-01 — no shared dependencies.**

EPIC-01 order (internal dependency chain):
1. ST-01 — Ticker Universe Data Model + Endpoints (foundation: DB schema before batch engine)
2. ST-02 — OHLCV Data Pipeline Service (after ST-01 schema defined)
3. ST-03 — ATR + Regime Detection + Signal Scoring Engine (after ST-02 interface defined)
4. ST-04 — Screener Batch Engine + API Endpoints (after ST-01+02+03 complete)

EPIC-04 order (all independent; no prescribed ordering):
5. ST-12 + ST-13 — execution_prompt.md §2 + §3.1.A patches (same file; combine in one commit if same version bump)
6. ST-14 — prompt_change_log.md retrospective entries (scan first before writing)
7. ST-15 — Consecutive Losing Streak Metric (analytics extension)
8. ST-16 — AI Journal Model Version Contract (documentation)

**Sprint 1 gate before Sprint 2 opens:** EPIC-01 ST-04 merged to main.

### Sprint 2 (EPIC-02 + EPIC-03)

EPIC-02 order (dependency on ST-05):
1. ST-05 — Screener Results Page (new page, requires ST-04 endpoint)
2. ST-06 — Watchlist Promotion Flow (on screener page, after ST-05 scaffolded)
3. ST-07 — News Panel Attachment (on screener page, after ST-05 scaffolded; Strategy Rules Owner counter-sign at DoQ)

EPIC-03 order (all independent; can run in parallel with EPIC-02):
4. ST-08 — External API Health Check Extension
5. ST-09 — AI Journal Monitoring Metrics
6. ST-10 — AI Audit Service Unit Tests
7. ST-11 — Keyboard Shortcuts (display-layer, independent)

---

## Test Scenario Gap Flags (LL-v2.0-P4-2)

Per STEP 3.1 delegation class assignment rule: delegated_frontend items introducing new pages or new user-facing controls must have test_scenarios flagged as pending.

| EPIC | Affected Stories | Flag |
|------|-----------------|------|
| EPIC-02 | ST-05 (new page), ST-06 (new promotion flow), ST-07 (new panel) | `test_scenarios` field in EPIC-02 `execution_state.json` = **pending — QA & Testing Owner to author test scenarios before Sprint 2 begins** |
| EPIC-03 | ST-11 (new keyboard shortcut reference UI) | `test_scenarios` field in EPIC-03 `execution_state.json` = **pending — QA & Testing Owner to author before Sprint 2 begins** |

**Action:** QA & Testing Owner should author scenario files for EPIC-02 and EPIC-03 ST-11 during Sprint 1 so they are ready when Sprint 2 opens.

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 DS-01 complexity | Valid — BLG-SPEC-21/22/QA-09 scaffolding strong; ST-02/ST-03 confirmed feasible (Head of Engineering 2026-04-25). Monitor during execution. |
| RISK-02 | EPIC-02 hard dep on EPIC-01 | Valid — serialised sprint plan; ST-05 blocked until ST-04 merged. BLG-SPEC-23 defines API contract so frontend component work can proceed against contract. |
| RISK-03 | ST-11 keyboard shortcuts text input interference | Valid — AC explicitly requires input-focus guard; implementable with standard activeElement check. |

---

## Pre-Sprint Vulnerability Scan

pip-audit scan (2026-04-25): **Clean** — 0 known vulnerabilities across 70 dependencies (fastapi 0.135.1, starlette 0.49.1, uvicorn 0.24.0, requests 2.33.0, pydantic 2.7.0, anthropic 0.34.2, yfinance 1.3.0, and 63 others). No high/critical CVEs found.

---

## Governance Hygiene Advisory (STEP -1.11)

⚠ Prompt change log gap detected: `sprint_planning_prompt.md` current v2.5 — no entry found in `claude/system/prompt_change_log.md`. This gap is the subject of ST-14 (OA-v29-01), which will scan for and add retrospective entries (v2.3→v2.4, v2.4→v2.5) during Sprint 1 execution. Advisory only — does not block planning.

---

## ST-07 Special Note: Strategy Rules Owner Counter-Sign

ST-07 (Screener News Panel Attachment) requires a Strategy Rules Owner counter-sign at DoQ per BLG-GOV-16 §13 sign-off conditions. The news panel is display-only (no sentiment analysis, no advisory content) per the existing sign-off. The counter-sign confirms the implementation remains display-only. EPIC-02 DoQ consolidation block must explicitly list and confirm this story-level authority sign-off per execution_prompt.md v3.9 §3.2.A.

---

## Carry-Forward from Prior Cycle

Checked most recently completed cycle (2026-04-22__release-v2.9 — lessons_learnt.md): 2 carry-forward items, both addressed as EPIC-04 sprint stories:
- CF-1: Multi-EPIC execution_state.json add/add conflict risk → ST-12
- CF-2: test_scenarios field empty in execution_state.json → ST-13

No further carry-forward.

---

## Outstanding Actions

| Action | Owner | Blocker? |
|--------|-------|---------|
| QA & Testing Owner to author test scenarios for EPIC-02 and EPIC-03 ST-11 before Sprint 2 | QA & Testing Owner | No (advisory; Sprint 2 may open without this, but scenarios should be ready) |
| Sprint_planning_prompt.md log gap (v2.3→v2.4→v2.5) — retrospective entries | ST-14 execution (Sprint 1) | No (ST-14 will close OA-v29-01) |
