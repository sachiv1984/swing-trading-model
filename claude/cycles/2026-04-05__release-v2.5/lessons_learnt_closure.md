**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-04-10
**Cycle:** 2026-04-05__release-v2.5

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v2.5 Integration Baseline, Quick Wins & Governance Debt — post-ship closure
Run: 2026-04-05__release-v2.5
Reviewed by: PMO Lead
Date filed: 2026-04-10
Prior cycle closure file checked: `claude/cycles/2026-03-31__release-v2.4/lessons_learnt_closure.md` — found. Recurrence check completed.

---

## What Worked Well

- **All three prior cycle carry-forwards fully resolved:** CF-1 (execution_prompt.md STEP 8 governance file edit reminder) and CF-2 (delivery_verification_prompt.md pre-seal Date gate) applied via ST-12 in sprint. CF-3 (hook configuration) confirmed already resolved (OA-03: no hook configured). First post-ship closure in two cycles with zero outstanding deferred patches carried forward from the prior cycle.
- **All 13 stories delivered at velocity 1.00:** No items returned to backlog. One delegation (DEL-01, ST-06) resolved within the cycle session. The sprint close, delivery verification, and post-ship closure all completed in the same session without restarts.
- **Closure STEP 7 resolved TSG-v24-01:** Test scenarios SC-ATR-01, SC-DEDUP-01/02, SC-STOP-01 created by ST-13 fully resolve the v2.4 correctness gap. Specs_Index updated.
- **No deviation compliance corrections required at STEP 5:** DEV-ST14-01 entry in `slippage_scenarios.md` contained all six required fields and was correctly marked RESOLVED in v2.5. No missing-field remediation needed this closure.
- **Scope and decisions documents cleanly Superseded:** Both `scope--2026-04-05__release-v2.5-integration-baseline-quick-wins-governance.md` and `decisions--2026-04-05__release-v2.5.md` were Active at closure start and correctly Superseded at STEP 4.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type B — Process Gap: qa_evidence_EPIC-01.md commit not pushed before PR merge (recurrence).

**Recurrence:** Yes — same issue occurred in v2.5 Phase 3 and Phase 4 (two references in lessons_learnt_cycle.md). Variant of prior cycle's LL-v2.4-P4-01 (qa_evidence file existence gate), but the gap here is not file non-existence — it is file-committed-but-not-pushed. The execution_prompt.md v3.0 gate (LL-v2.4-P4-01) checks for local file existence; it does not check whether the branch is pushed to remote before PR raise.

**What happened:**
Commit `78dd783` created the EPIC-01 DoQ sign-off in `qa_evidence_EPIC-01.md` on the local EPIC-01 branch but was not pushed before the PR was merged. At sprint close, the file was missing from main and required a cherry-pick (`git cherry-pick 78dd783` → commit `a47df1c`).

**Where in the routine:** Sprint Execution STEP 5 (Sprint Close) / Phase 4 delivery verification artefact check

**Root cause:** Operational discipline gap — no prompted check before PR raise to confirm branch is pushed (`git log --not origin/<branch>`). The existing gate confirms file existence locally; it does not confirm the file has been pushed to the remote branch before the PR is merged.

**Blast radius analysis:**
- What would have propagated: qa_evidence artefact missing from main; delivery verification preflight at STEP -1.2A would fail or find the sprint_close.md referencing a file not present on main.
- When it would have surfaced: Post-ship closure STEP 8.5 artefact check, or at the next run audit.
- Recovery cost if uncaught: Low — git cherry-pick; minor process debt.

**Process patch:**

→ Deferred patch:
  - Target file: `claude/system/execution_prompt.md`
  - Section: STEP 5.1 QA Evidence File Existence Check (added at v3.0 for LL-v2.4-P4-01)
  - Change required: Extend the check to also verify the exec branch has been pushed to origin before sprint close (`git log --not origin/<branch>` — if non-empty, any unpushed commits must be listed and the engine must push or flag). An unpushed commit including a qa_evidence file at sprint close is a soft gate requiring explicit push before proceeding.
  - Owner: Head of Specs Team
  - Target: v2.6

---

### Friction Item 2

**Classification:** Type C — Documentation Accuracy: `fee-drag-scenarios.md` referenced in qa_evidence_EPIC-03.md as "authored 2026-04-06" but was never created.

**Recurrence:** No — first instance of referencing a future-artefact path in qa_evidence as if it existed.

**What happened:**
The consolidation section of `qa_evidence_EPIC-03.md` referenced `docs/testing/fee-drag-scenarios.md` as an existing file. BLG-QA-07 was the backlog item for authoring that file; at the time of qa_evidence write, the file did not exist. This created an inaccurate qa_evidence reference that surfaced at delivery verification as TSG-V25-02.

**Where in the routine:** Phase 3 QA evidence / Phase 4 delivery verification §6

**Root cause:** Documentation accuracy — when a test scenario file is planned but not yet created, the qa_evidence should reference the backlog item (BLG-QA-07), not the future file path.

**Blast radius analysis:**
- What would have propagated: qa_evidence would contain references to files that do not exist; Specs_Index test coverage tracking would be inaccurate.
- When it would have surfaced: Immediately at delivery verification §6 test coverage check.
- Recovery cost if uncaught: Low — documentation correction only; BLG-QA-07 was filed.

**Process patch:**

→ Deferred patch (advisory):
  - No prompt change required — operational documentation discipline.
  - Rule to reinforce: When writing qa_evidence, if a test scenario file is planned but not created in this sprint, reference the backlog item ID, not a future file path.
  - Owner: QA & Testing Owner (discipline enforcement)
  - Target: Standing guidance — no cycle target

---

## Cross-Cycle Recurrence Check

**Prior cycle carry-forwards status:**

| # | Prior cycle carry-forward | v2.5 resolution |
|---|--------------------------|-----------------|
| 1 | execution_prompt.md STEP 8 governance file edit reminder (CF-2 in v2.4 lessons_learnt.md) | **RESOLVED** — ST-12 applied the STEP 8 reminder to execution_prompt.md v3.0→v3.1 in this cycle |
| 2 | delivery_verification_prompt.md pre-seal Date gate (CF-2 in v2.4 lessons_learnt.md) | **RESOLVED** — ST-12 applied the pre-seal Date gate to delivery_verification_prompt.md v1.7→v1.8 in this cycle |
| 3 | Hook configuration (user-prompt-submit-hook write target) | **RESOLVED** — OA-03 confirmed no hook configured; no corrective action required |

**New recurrence detection:**
- Friction Item 1 (qa_evidence file committed but not pushed): Variant recurrence of LL-v2.4-P4-01. Existing gate in execution_prompt.md v3.0 checks local file existence; it does not check remote push state. Deferred patch filed above.
- No recurrence requiring escalation.

---

## STEP 8 Action Summary — Lessons Learnt Review

### From `lessons_learnt.md` (Release Planning)

| Item | Disposition | Notes |
|------|-------------|-------|
| OA-01: CF-1 sprint planning governance hygiene | Immediate, already applied | Sprint_planning_prompt.md v2.4→v2.5 STEP -1.11 added during sprint planning |
| OA-02: prompt_change_log audit/backfill | Immediate, already applied | Full audit confirmed all entries present; false positive from top-first scan |
| OA-03: hook configuration review | Immediate, already applied | No hook configured; standing constraint documented |
| Friction Item 1: prompt log hygiene for design_gate/amendment/roadmap engines | Deferred | Other engines should receive similar §6 edit reminders; Head of Specs Team, v2.6 |

### From `lessons_learnt_cycle.md` Phase 3

| Item | Disposition | Notes |
|------|-------------|-------|
| Commit ID format (all ST IDs in message) | Immediate, already applied | CLAUDE.md §2 updated mid-sprint; lessons_learnt.md backlog-add entry added |
| Role ownership check before actioning OA | No action needed | Existing memory entry feedback_role_ownership_check.md covers this |
| qa_evidence not pushed before PR merge | Deferred | Deferred patch above (Friction Item 1) for execution_prompt.md |
| execution_state.json on EPIC branch not main | No action needed | §8 CLAUDE.md conflict resolution handles correctly |
| DataTable.js TableHead onClick silent drop | No action needed | Caught by staging visual test — process worked; DataTable.js spread pattern now in place |

### From `lessons_learnt_cycle.md` Phase 4

| Item | Disposition | Notes |
|------|-------------|-------|
| Sprint close not run before verification | No action needed | Hard gate fired correctly; STEP -1 caught status. Operational discipline |
| qa_evidence_EPIC-01.md missing from main | Deferred | Same as Friction Item 1 above |
| fee-drag-scenarios.md referenced but not created | No action needed | Deferred patch advisory above (Friction Item 2); BLG-QA-07 filed |
| TSG-V25-01 test_scenarios field disambiguation | Deferred | Low priority — consider distinguishing "executed this sprint" vs "reference for future execution" in execution_state.json schema; PMO Lead / Head of Specs Team, v2.6 |

### Consolidated Action Summary

- **Immediate actions applied this run:** 0 (all applicable items were already applied during sprint execution)
- **Deferred to next cycle (v2.6):** 3
  1. execution_prompt.md STEP 5.1 — extend unpushed-commit check to qa_evidence files before sprint close (Owner: Head of Specs Team)
  2. Prompt log hygiene for design_gate_prompt.md, amendment_cycle_prompt.md, roadmap_prompt.md — add §6 edit reminders (Owner: Head of Specs Team)
  3. execution_state.json test_scenarios schema — consider "executed this sprint" vs "reference for future execution" distinction (Owner: PMO Lead / Head of Specs Team — low priority)
- **Escalated for decision:** 0

---

## Process improvements actioned this run

None — all applicable immediate actions were applied during sprint execution (ST-12 for CF-1 and CF-2). No action-now patches required at post-ship closure.

---

## Closure-phase observations

| Area | Observation |
|------|-------------|
| STEP 3 (Backlog) | ST-12 has no backlog ref (governance debt CF-2) — noted in closure record. 12 of 13 stories had backlog items; ST-12 is sourced from lessons_learnt_closure carry-forward. |
| STEP 5 (Deviation compliance) | DEV-ST14-01 in slippage_scenarios.md — RESOLVED with all 6 fields. No missing-field corrections needed. |
| STEP 7 (Specs Index) | TSG-v24-01 resolved; TSG-v23-01 V-CHART-05a/b/c and TSG-v22-02 SC-HEALTH-01 resolution targets updated to v2.6; TSG-V25-01/02 entries added. |
| Context continuity | This post-ship closure was resumed from a compacted conversation. No information loss detected — all required artefacts read from file system. |

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | STEP 5.1 QA Evidence File Existence Check | Extend check to verify exec branch is pushed to remote before sprint close; unpushed qa_evidence commits are a soft gate | Head of Specs Team | v2.6 |
| `claude/system/design_gate_prompt.md` | STEP (applicable commit or finish step) | Add governance file edit reminder: if any §6-governed file was modified during design gate execution, append to prompt_change_log.md | Head of Specs Team | v2.6 |
| `claude/system/amendment_cycle_prompt.md` | STEP (applicable commit or finish step) | Add governance file edit reminder per CLAUDE.md §6 | Head of Specs Team | v2.6 |
| `claude/roadmap/roadmap_prompt.md` | STEP (applicable commit or finish step) | Add governance file edit reminder per CLAUDE.md §6 | Head of Specs Team | v2.6 |

---

## Escalations

None.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | qa_evidence commits are sometimes pushed to origin after PR merge rather than before — the execution_prompt STEP 5.1 existence check does not detect this | Sprint planning for v2.6 should confirm execution_prompt.md STEP 5.1 is patched to check remote push state before sprint close is accepted | Sprint Planning |
| 2 | design_gate, amendment_cycle, and roadmap prompt engines lack the §6 governance file edit reminder added to execution_prompt.md via ST-12 — a coverage gap that could cause prompt_change_log.md entries to be missed when those engines apply governed file edits | Head of Specs Team should schedule patches to all three engines in v2.6; the same STEP 8 pattern (check for in-session §6-governed file edits → append to prompt_change_log.md) should be universal | Sprint Planning / Execution |
| 3 | execution_state.json test_scenarios field is used for both "scenarios run in this sprint" and "scenarios that should be run in a future sprint" — this ambiguity caused TSG-V25-01 to be assessed not_applicable at delivery verification | PMO Lead to propose schema clarification (e.g. test_scenarios_executed vs test_scenarios_reference) for consideration at v2.6 sprint planning | Sprint Planning |
