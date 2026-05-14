**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-14
**Cycle:** 2026-05-14__release-v3.4

---

# Sprint Planning Notes — 2026-05-14__release-v3.4

## Backlog Slice Source

Original — `claude/cycles/2026-05-14__release-v3.4/stage4_backlog_slice.md`

No amendment file present (`amended_backlog_slice_path` absent). Source confirmed original.

---

## Carry-Forward Items from Prior Cycle (v3.3)

3 carry-forward items from `claude/cycles/2026-05-09__release-v3.3/lessons_learnt_closure.md ## Deferred Actions`:

| # | Item | v3.4 Response |
|---|------|--------------|
| 1 | Frontend delegation pattern — front-load frontend | EPIC-03 (quick wins) in Sprint 1; EPIC-01 (Arc 3 frontend) in Sprint 2 — directly addressed in release plan |
| 2 | Merge order discipline: establish explicit merge order at STEP 3 start, document in execution_state.json | Merge order established: EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02 (cycle_summary key decision 4) — execution engine must record in execution_state.json at STEP 3 |
| 3 | QA evidence branch advisory: when resuming on a different EPIC branch, check remote branches before flagging QA evidence as missing | Advisory carried forward — execution engine should check `git show origin/EPIC-xx:path` before flagging missing QA evidence |

Items 4 and 5 are targeted at v3.5 (Head of Specs Team and PMO Lead owners — not actioned in v3.4).

---

## Pre-Sprint Vulnerability Scan

pre-sprint pip-audit: **clean** — 0 vulnerabilities found (scan run 2026-05-14 against `backend/requirements.txt`).

---

## Pre-Sprint Required Decisions

Per `cycle_summary.md ## Pre-sprint Planning Required Decisions`:

| Decision | Owner | Status |
|----------|-------|--------|
| [RISK-01] IT-04/05 UX specs — Design gate must produce UX specs for Drawdown Review Prompt and Concentration Limits Warning UI | Head of UX & Design + Product Owner | ✅ RESOLVED — design gate passed 2026-05-14; UX specs produced: `docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md` and `docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md` |

No unresolved pre-sprint required decisions. Sprint backlog can be sealed.

---

## Prompt Change Log Hygiene Check

All Class 6 governance prompt versions match the most recent change log entries. No gaps detected.

| Prompt | Current version | Last log entry | Status |
|--------|----------------|---------------|--------|
| sprint_planning_prompt.md | v2.8 | v2.7→v2.8 (2026-05-10) | ✅ |
| execution_prompt.md | v3.18 | v3.17→v3.18 (2026-05-13) | ✅ |
| delivery_verification_prompt.md | v2.1 | v2.0→v2.1 (2026-05-09) | ✅ |
| roadmap_prompt.md | v6.0 | v5.1→v6.0 (2026-05-13) | ✅ |
| release_planning_prompt.md | v2.27 | v2.26→v2.27 (2026-05-09) | ✅ |
| design_gate_prompt.md | v1.3 | v1.2→v1.3 (2026-05-09) | ✅ |
| post_ship_closure.md | v2.6 | v2.5→v2.6 (2026-05-09) | ✅ |
| backlog_management_prompt.md | v1.6 | v1.5→v1.6 (2026-05-10) | ✅ |
| roadmap_management_prompt.md | v1.4 | v1.3→v1.4 (2026-05-09) | ✅ |
| amendment_cycle_prompt.md | v1.8 | v1.7→v1.8 (2026-05-09) | ✅ |
| idea_intake_prompt.md | v2.3 | v2.2→v2.3 (2026-05-09) | ✅ |

---

## Pre-Sprint Backlog Advisory

No items found in `claude/backlog/backlog.md` with `Provisional-Target: Before v3.4 sprint planning`. Advisory: none required.

---

## Deferred Items

No items deferred during planning. All 14 stories are within confirmed capacity (WARN acknowledged at release planning).

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| *(none)* | — | — |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | ST-11 (EPIC-04) must merge before EPIC-01 sprint begins | Internal cross-EPIC | Sequencing constraint — Sprint 1 → Sprint 2 |
| ST-02 | ST-11 (same above) | Internal cross-EPIC | Same |
| ST-03 | ST-11 (same above) | Internal cross-EPIC | Same |
| ST-05 | ST-04 (backend must be merged or available for frontend integration) | Internal EPIC-02 | Recommended sequence: ST-04 before ST-05 |
| ST-06 | DS-03 sector data (shipped v2.9, live on main) | External data | Resolved — pre-existing |
| ST-10 | DS-06 migration + abandonment API (shipped v3.3 ST-17) | External backend | Resolved — pre-existing |
| All EPIC-01 stories | UX specs from v3.3 design gate | Spec dependency | Resolved — specs confirmed in design_gate.md |
| All EPIC-02 stories | UX specs from v3.4 design gate | Spec dependency | Resolved — design gate passed 2026-05-14 |

---

## Execution Sequence

```
Sprint 1 (Phase 1):
  1. EPIC-04 (Spec, QA & Documentation Debt)
     ST-11 — Research view component library (first — required before EPIC-01 begins)
     ST-12 — Screener morning routine UX spec
     ST-13 — trade_plan.md §6.2 spec update + AI journal review cadence
     ST-14 — Screener accuracy test protocol

  2. EPIC-03 (Frontend Quick Wins) — concurrent with EPIC-04 or after
     ST-07 — Research page UK suffix + negative earnings display
     ST-08 — Signals page default to most recent day
     ST-09 — Watchlist research status indicator
     ST-10 — Trade plan status badges + abandonment UI

Sprint 2 (Phase 2): — after Sprint 1 complete and EPIC-04 ST-11 merged
  3. EPIC-01 (Arc 3 Frontend Completion)
     ST-01 — Position lifecycle state frontend (IT-01)
     ST-02 — Grace Period Decision Support frontend (IT-02)
     ST-03 — Stop Management Workflow frontend (IT-03)

  4. EPIC-02 (Arc 3 Risk Prompts) — after design gate artefacts available
     ST-04 — Drawdown-Triggered Review Prompt backend (IT-04)
     ST-05 — Drawdown-Triggered Review Prompt frontend (IT-04)
     ST-06 — Position Concentration Limits backend + frontend (IT-05)

Merge order (per cycle_summary Key Decision 4): EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02
```

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-02 | **Resolved** — design gate passed 2026-05-14; UX specs produced for IT-04 and IT-05 |
| RISK-02 | EPIC-01 | Valid — TEST-GAP-EPIC-01/02-v33 Playwright scenarios must be authored alongside implementation; scenario IDs listed in AC (SC-LS-01–04, SC-GP-01–03, SC-TS-01–03) |
| RISK-03 | EPIC-02 ST-06 | Valid (Low) — DS-03 sector data quality; ST-06 AC includes graceful degradation for missing sector data |
| RISK-04 | Release-level | Valid (Medium) — capacity WARN; acknowledged by PO; EPIC-02 slip-to-v3.5 is the risk buffer if Sprint 2 over-runs |

---

## Test Scenario Gap Flags (delegated_frontend items with new controls)

The following `delegated_frontend` stories introduce new pages or user-facing controls. The Execution Engine must flag `test_scenarios` as `pending — QA & Testing Owner to author before PR merge` in execution_state.json at STEP 3:

| Story | New control type | Notes |
|-------|-----------------|-------|
| ST-01 | Lifecycle state badge (per row on positions page) | AC includes specific Playwright scenario IDs: SC-LS-01–04 |
| ST-02 | Grace period alert card (dismissible) | AC includes SC-GP-01–03 |
| ST-03 | Stop trail guided panel (confirm/cancel) | AC includes SC-TS-01–03 |
| ST-05 | Drawdown review prompt (dismissible) | Playwright E2E or human staging sign-off required (AC) |
| ST-06 | Concentration warning indicator (threshold) | Playwright E2E or human staging sign-off required (AC) |
| ST-08 | "Show all" toggle / date picker on signals page | New control added alongside default-change |
| ST-09 | Research status icon/badge per watchlist row | New indicator |
| ST-10 | Status badges + abandonment UI (reason input, confirm/cancel) | Multiple new controls |

---

## Design Gate Path Note (ST-03)

The backlog slice references `docs/design/2026-05-09__release-v3.3/stop-trail-panel/ux_spec.md` for ST-03. The design_gate.md for v3.4 confirms the actual artefact is at `docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md`. The correct path should be used in PR descriptions and implementation. No action needed before sprint execution — advisory only.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Merge order EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02 must be documented in execution_state.json at Execution STEP 3 | Head of Engineering | No (execution-time) |
| QA evidence branch advisory: check remote branches before flagging missing QA evidence | QA & Testing Owner | No (execution-time) |
| ST-03 UX spec path discrepancy noted in design_gate.md — use correct path in PR | Head of Engineering | No (advisory) |
