Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Release: v3.0
Cycle: 2026-04-25__release-v3.0
Last Updated: 2026-04-25

---

# Cycle Summary — v3.0 Arc 1 Remainder: Screener Engine & Results Page

**Published:** 2026-04-25
**Mode:** Standard
**Capacity outcome:** WARN (DS-01 H effort; 16 stories; historical 1.00 velocity supports delivery)

---

## Release Summary

| Field | Value |
|-------|-------|
| Release | v3.0 |
| Theme | Arc 1 Remainder: Screener Engine & Results Page |
| EPICs | 4 (EPIC-01 through EPIC-04) |
| Stories | 16 (ST-01 through ST-16) |
| Sprints | 2 |
| Deferred items | 6 (DS-04, BLG-FEAT-13, BLG-FEAT-19, BLG-FE-16, BLG-GOV-11, BLG-OPS-13) |

---

## Sprint Plan

| Sprint | EPICs | Stories | Theme |
|--------|-------|---------|-------|
| Sprint 1 | EPIC-01, EPIC-04 | ST-01–ST-04, ST-12–ST-16 (9 stories) | Screener engine backend + governance deferred patches |
| Sprint 2 | EPIC-02, EPIC-03 | ST-05–ST-11 (7 stories) | Screener frontend + ops/QA/quick wins |

**Design gate required between Sprint 1 and Sprint 2** (before EPIC-02 opens).

---

## Key Scope Decisions

- **DS-01 (screener engine)** is the core Arc 1 deliverable — H effort, 4 stories (ST-01–ST-04)
- **DS-02 + DS-07 + BLG-FE-18** bundled into EPIC-02 — complete screener frontend experience
- **DS-04 deferred to v3.1** — no spec exists; independent of screener engine flow
- **v2.9 deferred patches resolved in Sprint 1** — EPIC-04 (ST-12/13) before sprint execution begins
- **OA-v29-01 closed in Sprint 1** — prompt_change_log.md retrospective entries (ST-14)

---

## Risks

| RISK-ID | Description | Priority | Sprint |
|---------|-------------|----------|--------|
| RISK-01 | DS-01 implementation complexity — most complex backend work to date | Medium | Sprint 1 |
| RISK-02 | EPIC-02 hard dependency on EPIC-01 — serialised sprint order required | Medium | Sprint 2 |
| RISK-03 | BLG-FE-19 keyboard shortcuts may interfere with text inputs | Low | Sprint 2 |

---

## Pre-sprint Planning Required Decisions

The following must be resolved before sprint planning seals (before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-01] DS-01 implementation scope — at sprint planning, confirm story-level breakdown for ST-02/ST-03 is feasible; if OHLCV pipeline and ATR+regime+scoring engine are too large as individual stories, split further (e.g. ST-02a OHLCV + ST-02b ATR, ST-03a regime + ST-03b scoring) — Owner: Head of Engineering + PMO Lead
- [ ] [Design gate] Design gate for DS-02 must be run between Sprint 1 and Sprint 2; EPIC-02 cannot open until design gate passes on screener_results.md — Owner: Head of UX & Design + Product Owner

---

## Outstanding Actions Resolved This Cycle

| OA | Resolution |
|----|-----------|
| OA-v29-01 (prompt_change_log.md gap) | Assigned to ST-14 (EPIC-04 Sprint 1) — will close on delivery |
| OA-v29-02 (execution_prompt.md §2 patch) | Assigned to ST-12 (EPIC-04 Sprint 1) — will close on delivery |
| OA-v29-03 (execution_prompt.md §3.1.A patch) | Assigned to ST-13 (EPIC-04 Sprint 1) — will close on delivery |

---

## Carry-Forward from v2.9

| # | Item | Addressed in v3.0 |
|---|------|-------------------|
| 1 | Multi-EPIC execution_state.json add/add conflict risk | ST-12 (execution_prompt.md §2 owner designation) |
| 2 | test_scenarios field empty in execution_state.json | ST-13 (execution_prompt.md §3.1.A population note) |
