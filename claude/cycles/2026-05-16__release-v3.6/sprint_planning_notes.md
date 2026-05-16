**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-16
**Cycle:** 2026-05-16__release-v3.6

---

# Sprint Planning Notes — 2026-05-16__release-v3.6

## Backlog Slice Source

Original — `claude/cycles/2026-05-16__release-v3.6/stage4_backlog_slice.md`

No amended backlog slice (`amended_backlog_slice_path` absent from state.json).

---

## Pre-Sprint Vulnerability Scan

**Tool:** pip-audit v1.x
**Result:** Clean — no known vulnerabilities across 68 dependencies.
**Timestamp:** 2026-05-16

---

## Carry-Forward Items

5 carry-forward items from `claude/cycles/2026-05-15__release-v3.5/lessons_learnt_closure.md`:

| # | Observation | Disposition in v3.6 |
|---|-------------|---------------------|
| 1 | §13 gate story pattern proved effective but not yet documented in governance prompts | Addressed: EPIC-04 ST-09 AC-01 |
| 2 | deviations_filed metadata ambiguity (`false` = "not filed" vs "check completed clean") | Addressed: EPIC-04 ST-10 AC-01 |
| 3 | sprint_close template lacks three-field verification readiness block | Addressed: EPIC-04 ST-10 AC-02 |
| 4 | Phase 3 lessons_learnt_cycle.md section absent — created by delivery verification | Addressed: EPIC-04 ST-10 AC-03 |
| 5 | scored_initiatives.md last updated 2026-03-31 (8+ cycles ago); Arc 3/4 entries missing | Not addressed this sprint; roadmap engine advisory — carry forward |

---

## Capacity WARN Acknowledgement

Capacity check outcome: **WARN** (standard mode).

Total active-scope effort (~3.25–3.5 days) approaches solo-dev 2-sprint capacity ceiling (~3–4 days). Phasing distributes risk: Sprint 1 is ~2.75–3 days; Sprint 2 is ~0.5 day (buffer available).

Product Owner acknowledgement: **recorded** — `capacity_warn_acknowledged = true` set at release planning (state.json). PO confirmed WARN-mode acceptable with phased delivery; EPIC-02 deferral removes the capacity ceiling risk entirely.

---

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-03 (EPIC-02) | Design gate: PO confirmed <20 closed trades on 2026-05-16; PT-04 gate not met | Yes — v3.7 if gate met |
| ST-04 (EPIC-02) | Depends on ST-03 spec; deferred with EPIC-02 | Yes — v3.7 |
| ST-05 (EPIC-02) | Depends on ST-03 + ST-04; deferred with EPIC-02 | Yes — v3.7 |

All 3 items remain in `claude/backlog/backlog.md` with their current status. No backlog modification required.

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-10 | ST-09 | Internal (same file: execution_prompt.md) | Resolved — sequential in Sprint 1 |
| ST-02 | ST-01 | Internal (frontend requires backend field + API) | Resolved — ST-01 in Sprint 1, ST-02 in Sprint 2 |
| ST-04 | ST-03 | Internal (spec must precede implementation) | Moot — EPIC-02 fully deferred |
| ST-05 | ST-03, ST-04 | Internal (spec + backend precede frontend) | Moot — EPIC-02 fully deferred |
| ST-07 | None | — | None |
| ST-06 | None | — | None |
| ST-08 | None | — | None |
| ST-09 | None | — | None |

---

## Execution Sequence

**Sprint 1** (EPICs 04, 03, 01 — partial):

1. EPIC-04/ST-09 — execution_prompt.md §13 gate story pattern formalisation
2. EPIC-04/ST-10 — execution_prompt.md metadata + sprint_close patches (after ST-09; same file)
3. EPIC-03/ST-06 — SC-RV-18/19 Playwright coverage (parallel with EPIC-04)
4. EPIC-03/ST-07 — Research endpoint HTTP error code differentiation (parallel with EPIC-04)
5. EPIC-03/ST-08 — Research page UX fix (parallel with EPIC-04)
6. EPIC-01/ST-01 — Capture planned_entry_price at trade entry (parallel with EPIC-03/04)

**Sprint 2** (EPIC-01 — remainder):

7. EPIC-01/ST-02 — Update PlanVsReality component for entry_delta_pct

---

## Multi-EPIC Execution Notes

**execution_state.json owner:** EPIC-04 (first in merge order).

EPIC-03 and EPIC-01 branches must check for execution_state.json before creating — if found, read and append their EPIC section rather than overwrite.

**Merge order:** EPIC-04 → EPIC-03 → EPIC-01

Rationale:
- EPIC-04 first: governance patches only; no shared-file conflicts with other EPICs
- EPIC-03 second: openapi.yaml touches (ST-07 AC-05); merges before EPIC-01
- EPIC-01 last: openapi.yaml touches (ST-01 AC-06); must rebase onto main after EPIC-03 merges to avoid drift

---

## Shared File Ownership Advisory

| File | EPICs Modifying | Owner EPIC | Advisory |
|------|----------------|-----------|---------|
| `openapi.yaml` | EPIC-01, EPIC-03 | EPIC-03 (merges first) | EPIC-01 branch must rebase onto `origin/main` after EPIC-03 PR merges before finalising openapi.yaml changes |
| `claude/system/execution_prompt.md` | EPIC-04 only | EPIC-04 | No shared-file conflict |
| `backend/routers/test.py` | EPIC-01 (ST-01 AC-07), EPIC-03 (ST-07 AC-01 implicit) | EPIC-03 (merges first) | EPIC-01 must rebase and update endpoint count after EPIC-03 merges |

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — nullable field + conditional display; regression test with null data |
| RISK-02 | EPIC-02 (ST-03/04/05) | Resolved — gate not met; EPIC-02 deferred to v3.7 |
| RISK-03 | EPIC-03 (ST-07) | Valid — scoped backend only; openapi.yaml same-commit update per CLAUDE.md §2 |

---

## Hygiene Advisories

**Prompt change log gaps (STEP -1.7 scan):**

| Prompt | Current Version | Last Logged | Gap |
|--------|----------------|-------------|-----|
| sprint_planning_prompt.md | v3.1 | v3.0 (2026-05-15) | v3.0→v3.1 (OA-RP-01) |
| execution_prompt.md | v3.20 | v3.18 (2026-05-13) | v3.18→v3.20 (OA-RP-02) |
| delivery_verification_prompt.md | v2.2 | v2.1 (2026-05-09) | v2.1→v2.2 (OA-RP-03) |
| backlog_management_prompt.md | v1.7 | v1.6 (2026-05-10) | v1.6→v1.7 (OA-RP-04) |

All 4 gaps are addressed by EPIC-04 ST-09 AC-04 in this sprint. Non-blocking.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| scored_initiatives.md refresh (Arc 3/4 entries missing; v3.5 LL carry-forward) | Facilitator / PMO Lead | No — carry-forward advisory for roadmap engine |
| OA-RP-01–04: prompt change log gap entries | Head of Specs Team | No — addressed by EPIC-04 ST-09 AC-04 within this sprint |

No actions marked `Blocker? Yes`. Sprint seals immediately.
