**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-17
**Cycle:** 2026-03-17__release-v2.0

---

# Sprint Planning Notes — 2026-03-17__release-v2.0

---

## Backlog Slice Source

Original — `claude/cycles/2026-03-17__release-v2.0/stage4_backlog_slice.md`
(`amended_backlog_slice_path` was empty at STEP -1.1)

---

## Pre-Sprint Completed Items

| Item | Completed | Evidence |
|------|-----------|----------|
| ST-03 | Pre-sprint (design gate session) | `docs/specs/api_contracts/reports_endpoints.md` v0.1; committed; dual sign-off confirmed |
| ST-11 | Pre-sprint (QA session) | `qa_notification_planning.md` filed; RISK-01 resolved; EPIC-03 deferred v2.1 |

---

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-06 | EPIC-03 | EPIC-03 deferred to v2.1 — no async notification infrastructure; no spec | v2.1 (after BLG-TECH-08 ADR) |
| ST-07 | EPIC-03 | Same | v2.1 |
| ST-08 | EPIC-03 | Same | v2.1 |
| ST-09 | EPIC-03 | Same | v2.1 |
| ST-10 | EPIC-03 | Same | v2.1 |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal spec gate | Resolved at planning — ST-01 must complete (register + sign-off) before ST-02 begins |
| ST-04 | ST-03 *(pre-completed)* | Internal spec gate | ✅ Pre-cleared — ST-03 done and signed off |
| ST-04 | ST-16 (recommended) | Internal governance | ST-16 should precede ST-04 if any database schema change is required |
| ST-05 | ST-04 | Internal backend gate | ST-04 endpoint must be live on staging before ST-05 frontend integration |
| ST-13 | None | — | Independent; stretch |
| ST-20 | None | — | Independent; stretch |
| ST-18, ST-19 | None | — | Parallel track; no sprint dependency |

No circular dependencies detected. ✅

---

## Execution Sequence

**Track 1 — Product sprint (primary)**

1. **ST-12** — P1: Fix GET /portfolio missing 4 fields (item 1; no dependencies; blocks nothing but must ship first)
2. **ST-16** — Database Migration Governance Standard (precedes any schema change in ST-04)
3. **ST-01** — Signals page spec: register signals.md in Specs_Index.md; confirm Head of Specs Team sign-off
4. **ST-02** — Signals page: implement top_n / lookback_days controls (depends on ST-01)
5. **ST-04** — Implement GET /reports/tax-year endpoint (ST-03 pre-cleared; ST-16 recommended before)
6. **ST-05** — Frontend: tax-year P&L report view (depends on ST-04 live on staging)
7. **ST-14** — Production Deployment Runbook (independent; can run in parallel with ST-04/ST-05)
8. **ST-15** — Positions Table Data Dictionary (independent)
9. **ST-17** — Spec Coverage Inventory (independent; largest item; best started early and run in parallel)

**Stretch (execute if capacity remains)**

10. **ST-13** — GET /portfolio/prospective-heat spec + implementation (P3)
11. **ST-20** — CohortAnalysis regression scenario (P3)

**Track 2 — Parallel governance track (EPIC-06)**

- **ST-18** — Roadmap stage document consolidation (parallel; no sprint dependency)
- **ST-19** — Ideas register (parallel; no sprint dependency)

*ST-17 and EPIC-06 items are large parallel workstreams that should begin early and run concurrently with Track 1.*

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-03 | ✅ Resolved — EPIC-03 deferred to v2.1; qa_notification_planning.md filed |
| RISK-02 | EPIC-02 | ✅ Resolved — ST-03 pre-completed; reports_endpoints.md v0.1 signed off |
| RISK-03 | EPIC-01 | ✅ Resolved at design gate — signals.md v0.1 authored; ST-01 registration + sign-off in sprint |
| RISK-04 | EPIC-04 | Active — ST-12 is Sprint item 1; BLG-BE-01 must ship; no further mitigation needed |
| RISK-05 | EPIC-06 | Active but manageable — EPIC-06 parallel track; Head of Specs Team sign-off + CLAUDE.md §6 checklist required before commit |

---

## Pre-Sprint Vulnerability Scan

pip-audit not installed (`pip-audit: command not found`). Scan could not be executed.

**Recommendation:** Install pip-audit (`pip install pip-audit`) before sprint execution begins. Run manually against `backend/requirements.txt` before ST-04 backend work begins. If high/critical CVEs are found, surface to Product Owner and Head of Engineering before merging backend changes.

Last confirmed clean scan: Sprint 2 v1.9 (2026-03-11 — per `.claude_current_state.json sprint2_planning.pip_audit: "clean"`)

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| pip-audit: install and run before ST-04 backend execution begins | Head of Engineering | No (advisory) |

No blockers. ✅
