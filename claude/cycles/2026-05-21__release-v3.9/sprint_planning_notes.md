Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-22
Cycle: 2026-05-21__release-v3.9

---

# Sprint Planning Notes — v3.9

---

## Carry-Forward Items Reviewed

5 carry-forward items from cycle `2026-05-19__release-v3.8` (source: lessons_learnt_closure.md `## Carry-Forward`):

| Item | Owner | Disposition in v3.9 |
|------|-------|---------------------|
| Duplicate GitHub issues audit/close | PMO Lead | PMO housekeeping during sprint execution (not a story) |
| createPageUrl map in delegation template | Head of Specs Team | ST-09 (EPIC-04) |
| QA evidence pre-merge enforcement (ESCALATION — 2-cycle) | Director of Quality | ST-12 (EPIC-04); DoQ must confirm PR template checklist item is active before EPIC-04 execution begins |
| test_scenarios population guidance | Head of Specs Team | ST-09 (EPIC-04) |
| Planning-deferred in execution_state.json | Head of Specs Team | ST-10 (EPIC-04) |

All 5 carry-forward items addressed in v3.9 scope. ✅

---

## Pre-Sprint Required Decisions

### [RISK-03] SI-01 Override Event Persistence — Resolved

**Finding:** Code review of `backend/routers/pre_entry_validation.py` and `backend/database.py` confirmed SI-01 stores `pre_entry_override_acknowledged` as a BOOLEAN column on the `trade_plans` table only. No separate events table exists. Override events are NOT independently persisted to a log.

**Impact on ST-07:** ST-07 must both (a) create the `red_flag_events` table (AC-01) and (b) modify the pre-entry validation override path to write a `pre_entry_override` event to `red_flag_events` at confirmation time (AC-02). This is already within ST-07's defined scope — no scope change required.

**Disposition:** Risk confirmed IN scope. ST-07 execution engine notified. ✅

### [RISK-05] PT-04 Gate — Resolved

**Finding:** Product Owner confirmed < 20 closed trades (2026-05-22). PT-04 gate NOT met.

**Disposition:** EPIC-05 (ST-13, ST-14) excluded from sprint backlog. Recorded as `deferred_at_planning` with `gate_condition: "20+ closed trades not confirmed by PO (2026-05-22)"`. ✅

---

## Capacity WARN Acknowledgement

Product Owner explicitly acknowledged the capacity WARN (2026-05-22). Firm scope (~7–10 days) is within available capacity (~11 days). EPIC-05 exclusion resolves the WARN condition entirely. `capacity_warn_acknowledged: true`.

---

## Pre-Sprint Backlog Advisory

No `Provisional-Target: Before v3.9 sprint planning` items found in `claude/backlog/backlog.md`. Advisory clear. ✅

---

## Prompt Change Log Gap Advisory

⚠ **Prompt change log gap:** `claude/system/roadmap_prompt.md` current v6.5 — last logged entry is v6.4 (2026-05-21 prompt compression row). The v6.4→v6.5 bump applied during the 2026-05-21 scheduled rebalance (action-now patch) has no corresponding change log entry. Add a prepended row per CLAUDE.md §6.

*Advisory only — does not block sprint planning.*

---

## Dependency Map

### Sprint 1 Dependencies

```
EPIC-02 (ST-05, ST-06) — parallel-safe with EPIC-01; no cross-dependencies
EPIC-01 (ST-01, ST-02, ST-03, ST-04):
  - ST-01 highest priority (P1 YF rate-limiting)
  - ST-02, ST-03 can run after ST-01 (independent backend fixes)
  - ST-04 (degraded-run banner) depends on ST-01 (OHLCV failure tracking added in ST-01)
  - No external dependencies
```

### Sprint 2 Dependencies

```
EPIC-04 (ST-09, ST-10, ST-11, ST-12) — parallel-safe with EPIC-03; governance-only
EPIC-03 (ST-07, ST-08):
  - ST-07 (backend) must complete before ST-08 (frontend)
  - ST-07 uses backend infra from EPIC-01 (already merged at Sprint 2 start)
  - No external dependencies beyond EPIC-01 merge
```

### Cross-Sprint Dependencies

EPIC-03 (Sprint 2) shares backend infra patterns with EPIC-01 (Sprint 1). EPIC-01 must be merged to `main` before EPIC-03 execution begins. This is already reflected in the sprint sequencing (EPIC-01/02 → EPIC-03/04).

---

## Multi-EPIC Execution Notes

**Sprints:** 2 (Sprint 1: EPIC-01, EPIC-02; Sprint 2: EPIC-03, EPIC-04)
**Total EPICs in scope:** 4 firm (EPIC-01–04)

**execution_state.json owner:** EPIC-02 (first EPIC in Sprint 1 execution order; creates the cycle-wide execution_state.json). All subsequent EPICs (EPIC-01, EPIC-04, EPIC-03) must check for existing execution_state.json before creating their own — read and append their EPIC section.

**Merge order — Sprint 1:** EPIC-02 → EPIC-01
**Merge order — Sprint 2:** EPIC-04 → EPIC-03

---

## Shared File Ownership Advisory

| Shared File | EPICs | Ownership |
|-------------|-------|-----------|
| `docs/reference/openapi.yaml` | EPIC-01 (ST-04), EPIC-02 (ST-06), EPIC-03 (ST-07) | EPIC-02 owns canonical version (first to merge); EPIC-01 rebases after EPIC-02; EPIC-03 rebases after EPIC-01 merge before finalising |
| `backend/database.py` | EPIC-01 (ST-04), EPIC-02 (ST-06), EPIC-03 (ST-07) | Same ownership rule as openapi.yaml |
| `backend/routers/test.py` | EPIC-03 (ST-07) | EPIC-03 sole owner in Sprint 2 |
| `src/App.js`, `src/pages.config.js` | EPIC-03 (ST-08) | EPIC-03 sole owner in Sprint 2 |
| `claude/system/execution_prompt.md` | EPIC-04 (ST-09) | EPIC-04 sole owner |
| `claude/system/sprint_planning_prompt.md` | EPIC-04 (ST-10) | EPIC-04 sole owner |
| `claude/system/release_planning_prompt.md`, `delivery_verification_prompt.md`, `shared_standards.md` | EPIC-04 (ST-11) | EPIC-04 sole owner |
| `.github/pull_request_template.md` | EPIC-04 (ST-12) | EPIC-04 sole owner |

Later EPICs must rebase onto `main` after earlier EPICs merge before finalising changes to any shared file.

---

## Risk Flag Confirmations

| Risk | Status |
|------|--------|
| RISK-01: YF crumb fix incomplete | Accepted — degraded-run warning (ST-04) provides secondary signal; mitigation in scope |
| RISK-02: company_name backfill silent failure | Accepted — ST-06 AC includes null-safe display; CSV validation in scope |
| RISK-03: SI-01 event persistence | Resolved — ST-07 scope confirmed covers table creation + write path |
| RISK-04: governance patch version management | Mitigated — CLAUDE.md §6 checklist + prompt-sync skill post-commit |
| RISK-05: PT-04 gate | Resolved — gate not met; EPIC-05 deferred_at_planning |

---

## Delegation Class Assignments

| Story | Classification | Justification |
|-------|---------------|---------------|
| ST-01 | `autonomous` | Backend-only; no UX change |
| ST-02 | `autonomous` | Backend-only; no UX change |
| ST-03 | `autonomous` | Backend-only; no UX change |
| ST-04 | `autonomous` | Backend + frontend; execution engine delivers both; Playwright ACs defined |
| ST-05 | `autonomous` | Frontend display-only label strip; no new controls |
| ST-06 | `autonomous` | Backend migration + frontend column; execution engine delivers both; Playwright ACs defined |
| ST-07 | `autonomous` | Backend-only; no UX change |
| ST-08 | `autonomous` | New frontend page; execution engine delivers; Playwright ACs SC-RFJ-01/02/03 defined |
| ST-09 | `autonomous` | Governance prompt edit only |
| ST-10 | `autonomous` | Governance prompt edit only |
| ST-11 | `autonomous` | Governance prompt edits to 3 files |
| ST-12 | `autonomous` | PR template edit only |

---

## Deferred Items

| Story | EPIC | Reason | Status |
|-------|------|--------|--------|
| ST-13 | EPIC-05 | PT-04 gate: < 20 closed trades (confirmed by PO 2026-05-22) | deferred_at_planning |
| ST-14 | EPIC-05 | PT-04 gate: depends on ST-13; gate not met | deferred_at_planning |

Both remain in `claude/backlog/backlog.md` with current status. Carry forward to next sprint planning run when gate is re-evaluated.

---

## Outstanding Actions

| # | Action | Owner | Blocker? | When |
|---|--------|-------|----------|------|
| 1 | Confirm DoQ PR template checklist item is live (CF-3) | Director of Quality | No (advisory — escalated) | Before EPIC-04 execution begins |
| 2 | Add prompt_change_log.md entry for roadmap_prompt.md v6.4→v6.5 | Head of Specs Team | No | Before next governance commit |
| 3 | Audit and close duplicate GitHub issues from v3.8 | PMO Lead | No | During sprint execution |
