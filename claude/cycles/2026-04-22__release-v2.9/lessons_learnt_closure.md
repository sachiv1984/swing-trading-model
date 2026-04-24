# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v2.9 — Arc 1 Foundation: Stock Discovery & Screening Spec & Infrastructure
Run: 2026-04-22__release-v2.9
Reviewed by: PMO Lead
Date filed: 2026-04-24
Prior cycle checked: 2026-04-17__release-v2.8 (lessons_learnt_closure.md loaded — recurrence check complete)

---

## What worked well

- **15/15 stories at 1.00 velocity** — all 4 EPICs merged cleanly; no delegation blocks, no returned items, no deferred stories. Largest v2.x sprint by story count and first full Arc 1 delivery cycle.
- **Both v2.8 deferred patches (BLG-GOV-14/15) converted to sprint stories** — ST-11 and ST-12 delivered execution_prompt.md §3.2 governance patches and STEP 5.1.B advisory, confirming the carry-forward mechanism reliably converts closure actions into sprint scope.
- **§13 governance gate (BLG-GOV-16) cleared within the same sprint** — no mid-sprint compliance block; strategy rules review completed before DS-06 implementation began.
- **CI mock harness (BLG-QA-08) delivered** — Alpaca and Yahoo Finance APIs now mockable in CI; deterministic screener test infrastructure in place for Arc 1 screener engine work in v3.0.
- **Closure-phase deferred patches confirmed resolved** — v2.8 Friction Items 3 and 4 (execution_prompt.md reclassification counter-sign note; EPIC-level DoQ consolidation block requirement) both resolved by ST-11. No recurrence escalation needed.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type D — Cognitive Fatigue: execution_state.json created independently on two EPIC branches causing add/add merge conflict.

**Recurrence:** No — first identification (Phase 3, v2.9)

**What happened:**
EPIC-01 and EPIC-02 both created `execution_state.json` independently during sprint execution. When EPIC-02 was rebased onto main after EPIC-01/EPIC-03 merged, an add/add conflict required manual resolution. CLAUDE.md §8 correctly governed the resolution (took EPIC-02 as canonical), but the conflict was avoidable.

**Where in the routine:**
Phase 3 Sprint Execution — EPIC merge order step.

**Root cause:** Process gap — no protocol designates a single EPIC branch as the execution_state.json owner. All branches may independently create the file.

**Blast radius analysis:**
- What would have propagated: Repeated add/add merge conflicts on every multi-EPIC sprint that creates execution_state.json.
- When it would have surfaced: At EPIC merge time (caught this cycle by CLAUDE.md §8).
- Recovery cost if uncaught: Low-medium — CLAUDE.md §8 provides resolution guidance; conflict resolution adds latency but not risk if §8 is followed.

**Process patch:**
→ Deferred patch (cannot apply without Head of Specs Team session):
  - File: `claude/system/execution_prompt.md`
  - Section: §2 EPIC execution order advisory
  - Change required: Nominate a single EPIC branch as execution_state.json owner at sprint planning; all other EPIC branches must check for its existence before creating their own version. Add note in the merge order advisory.
  - Owner: Head of Specs Team
  - Target: v3.0 sprint planning

---

### Friction Item 2

**Classification:** Type D — Cognitive Fatigue: test_scenarios field in execution_state.json was empty for all EPICs despite tests being created and run during the sprint.

**Recurrence:** No — first identification (Phase 4, v2.9)

**What happened:**
Tests were created and referenced in qa_evidence files for all EPICs. However, the `test_scenarios` field in execution_state.json was left empty for all 4 EPICs. Phase 4 identified this as a state hygiene gap — test evidence existed but was not pre-registered in the execution state record.

**Where in the routine:**
Phase 4 Delivery Verification — §6 Test Coverage Assessment.

**Root cause:** Cognitive fatigue — execution_prompt.md does not include a reminder to populate `test_scenarios` when tests are created. QA evidence was the natural capture point for test references; execution state received no test cross-reference.

**Blast radius analysis:**
- What would have propagated: Persistent empty test_scenarios fields across all future sprints; metric integrity of execution state test tracking degraded.
- When it would have surfaced: At delivery verification §6 (caught this cycle; noted as advisory).
- Recovery cost if uncaught: Low — test evidence still exists in qa_evidence; state field is informational.

**Process patch:**
→ Deferred patch (cannot apply without Head of Specs Team session):
  - File: `claude/system/execution_prompt.md`
  - Section: §3.1.A story completion checklist (after test creation substep)
  - Change required: Add note at the point of test creation: "populate test_scenarios in execution_state.json with the test file paths as tests are created."
  - Owner: Head of Specs Team
  - Target: v3.0 sprint planning

---

### Friction Item 3

**Classification:** Type A — Governance Drift: sprint_planning_prompt.md version gap (v2.3→v2.5) not logged in prompt_change_log.md.

**Recurrence:** No — first identification (Release Planning lessons, v2.9 planning)

**What happened:**
sprint_planning_prompt.md version advanced from v2.3 to v2.5 without an intermediate v2.4 prompt_change_log entry. The advisory was raised at v2.9 release planning (OA-v29-01) and deferred to Head of Specs Team. No action was taken during the sprint; item remains open.

**Where in the routine:**
Release Planning (OA-v29-01 advisory).

**Root cause:** Process gap — version bump was applied without a corresponding change log entry; two increments (v2.3→v2.4→v2.5) occurred without log entries.

**Blast radius analysis:**
- What would have propagated: Incomplete governance audit trail for sprint_planning_prompt.md versions v2.4 and v2.5; no change summary for future reference.
- When it would have surfaced: At next governance audit.
- Recovery cost if uncaught: Low — retrospective log entries can be added; no functional impact.

**Process patch:**
→ Deferred patch:
  - File: `claude/system/prompt_change_log.md`
  - Section: sprint_planning_prompt.md rows
  - Change required: Add retrospective entries for sprint_planning_prompt.md v2.3→v2.4 and v2.4→v2.5 based on commit history or OPERATIONAL_GUIDE §14 diff.
  - Owner: Head of Specs Team
  - Target: v3.0 sprint planning

---

## Recurrence Escalations

Checking prior cycle (2026-04-17__release-v2.8) lessons_learnt_closure.md deferred patches:

**v2.8 deferred patches:**
1. execution_prompt.md §3.2.A reclassification note (Friction Item 3) — **Resolved**: delivered as ST-11 (BLG-GOV-14) in v2.9 execution_prompt.md v3.8→v3.9. ✓
2. execution_prompt.md §3.2 DoQ sign-off template (Friction Item 4) — **Resolved**: delivered as ST-11 (BLG-GOV-14) in v2.9 execution_prompt.md v3.8→v3.9. ✓

No recurrences from prior cycle. Both carry-forward items resolved in v2.9.

None requiring escalation.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `docs/product/changelog.md` | v2.9 entry | New versioned entry written for v2.9 | N/A (operational record) | Not applicable |
| `claude/roadmap/current_roadmap.md` | §1 Current Version + RA:v2.9 annotation + §8 release table | v2.9 marked ✅ Complete; v3.0–v3.1 row added; version header updated | N/A | Not applicable |
| `claude/backlog/backlog.md` | 12 items | 12 shipped items marked ✅ COMPLETE (2026-04-24); BLG-OPS-13 added; BLG-FE-18 and TEST-GAP-ST14 confirmed present | N/A | Not applicable |
| `docs/product/scope/scope--2026-04-22__release-v2.9-arc-1-foundation-stock-discovery-screening-spec.md` | Header | Status Active → Superseded; supersession note added | N/A | Not applicable |
| `docs/product/decisions/decisions--2026-04-22__release-v2.9.md` | Header | Status Active → Superseded; supersession note added | N/A | Not applicable |
| `docs/specs/Specs_Index.md` | §3.4b screener UX spec path; §14.1 TSG-v28-01; new §15 | screener_results.md path corrected; TSG-v28-01 resolved; TSG-v29-02 added | N/A | Not applicable |
| `claude/cycles/velocity_metrics.md` | Velocity History table | v2.9 row appended (Planned=15, Completed=15, velocity=1.00); rolling 6-cycle average updated to 1.00 (v2.4–v2.9) | N/A | Not applicable |

---

## New files created this run

- `claude/cycles/2026-04-22__release-v2.9/closure_state.json` — post-ship closure engine state tracker
- `claude/cycles/2026-04-22__release-v2.9/lessons_learnt_closure.md` — this file
- `claude/cycles/2026-04-22__release-v2.9/closure_record.md` — post-ship closure record (produced STEP 9)

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | §2 EPIC execution order advisory | Nominate single EPIC branch as execution_state.json owner at sprint planning; other branches check for existence before creating. Add merge order advisory note. | Head of Specs Team | v3.0 sprint planning |
| `claude/system/execution_prompt.md` | §3.1.A story completion checklist | Add note to populate test_scenarios in execution_state.json with test file paths when tests are created during story execution. | Head of Specs Team | v3.0 sprint planning |
| `claude/system/prompt_change_log.md` | sprint_planning_prompt.md rows | Retrospective entries for v2.3→v2.4 and v2.4→v2.5 version increments (OA-v29-01). | Head of Specs Team | v3.0 sprint planning |

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Multi-EPIC sprints risk add/add conflicts on execution_state.json when all branches create it independently — CLAUDE.md §8 resolved it this cycle but adds merge latency | Sprint Planning Engine: at sprint planning, designate one EPIC branch as execution_state.json owner; other EPICs should coordinate or rebase before creating their version | Sprint Planning |
| 2 | test_scenarios field in execution_state.json was empty for all 4 EPICs despite tests being created; test evidence lived only in qa_evidence files — creates a state integrity gap that could affect future automated tooling reading execution state | Sprint Execution Engine: execution_prompt.md §3.1.A should include a populate-test_scenarios step at the point tests are created; not just a Phase 4 advisory | Sprint Planning |
