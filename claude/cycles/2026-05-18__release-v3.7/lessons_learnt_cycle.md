Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-18
Cycle: 2026-05-18__release-v3.7

---

## Phase 3

**Cycle:** 2026-05-18__release-v3.7
**Generated:** 2026-05-18
**Prior cycle file checked:** claude/cycles/2026-05-16__release-v3.6/lessons_learnt_cycle.md — not found (file is lessons_learnt.md, Release Planning phase only). Recurrence check against Phase 3 patterns not possible; no prior Sprint Execution lessons_learnt_cycle.md exists.

---

### Friction Items

| # | Friction Item | Type | Recurrence? | Blast Radius | Patch Target | Action |
|---|---------------|------|-------------|--------------|--------------|--------|
| 1 | EPIC-01 QA sign-off not recorded before PR merge — `Date:` field in qa_evidence_EPIC-01.md was blank when PR #430 was merged. Retrospective sign-off applied at sprint close. | Governance process | Unknown (no prior Phase 3 LL available) | Sprint close blocked at STEP 5.1 until retrospective sign-off applied. If not caught: delivery verification preflight fails. | execution_prompt.md §3.2.B pre-condition check; merge gate STEP 4 | Defer — STEP 4 merge gate already requires non-blank Date before merge; this instance was a human bypass. No prompt patch required. |
| 2 | DEL-20260518-01 delegation log not updated to terminal state when ST-10 completed — entry showed `Pending` at sprint close despite work being done (commit ccac35c0). Required manual correction at STEP 5.0. | Delegation tracking | Unknown | Misleading delegation log; STEP 5.0 hard gate fires; sprint close delayed. | execution_prompt.md §3.1.B / §3.1.C — HARD GATE: update delegation log atomically with execution_state.json on item completion | Defer — existing §3.1.B hard gate language ("These two writes are atomic") is correct; human follow-through gap, not a prompt gap. |
| 3 | Playwright Smoke Tests job timeout (EPIC-04 PR #431) — second CI run for smoke tests timed out at 15m (job cancelled by GitHub runner). Required re-run; first run passed in 2m7s. No test failure. | GitHub integration friction | Unknown | Appears as a failing check; Product Owner sees blocked PR; delays merge. | smoke-tests.yml timeout-minutes setting | Defer — runner allocation variability; timeout could be increased from 15→25min as a low-priority hardening item if recurrence observed. |
| 4 | scored_initiatives.md staleness resolved this sprint (ST-11 / BLG-GOV-23 / OA-RP-05) — previously flagged in v3.6 Release Planning LL observation #5 as open for 8+ cycles. The file is now current through Arc 6. | Governance process — resolved | First confirmed resolution after 8+ cycles open | If left unresolved: all CPS estimates fall to Tier 3 (inline estimates); roadmap scoring degrades. | No patch needed — resolved. Advisory to refresh at each Arc boundary going forward. | None — resolved. |

---

### Outstanding Actions

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | Consider increasing smoke-tests.yml `timeout-minutes` from 15→25 if CI timeout recurs on a subsequent PR. | QA & Testing Owner | Next cycle if recurrence |
| 2 | Enforce DoQ sign-off date recorded before PR merge — consider adding a PR checklist item or pre-merge comment template to prevent recurrence of gap #1. | Director of Quality | Next cycle |

---

### What Went Well

- Sprint goal fully met with zero spec deviations across 8 stories — cleanest sprint in recent cycles
- Both delegation records resolved within the sprint window (no carry-forwards)
- EPIC-02 gate deferral handled cleanly at planning — no mid-sprint disruption
- scored_initiatives.md staleness resolved after 8+ cycles — OA-RP-05 closed
- Autonomous class sign-off (BLG-GOV-19) worked correctly for EPIC-03 — no unnecessary DoQ delegation on pure governance patches
