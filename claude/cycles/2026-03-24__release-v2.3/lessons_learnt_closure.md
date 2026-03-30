**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-30
**Cycle:** 2026-03-24__release-v2.3

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v2.3 Quality Automation & User Insight — post-ship closure
Run: 2026-03-24__release-v2.3
Reviewed by: PMO Lead
Date filed: 2026-03-30
Prior cycle closure file checked: `claude/cycles/2026-03-21__release-v2.2/lessons_learnt_closure.md` — found. Recurrence check completed.

---

## What Worked Well

- **v2.2 Carry-Forward CF-1 (LL-CL-v22-01) fully resolved:** The backlog reference synchronisation patch applied to `delivery_verification_prompt.md` v1.6 prevented the stale-reference recurrence from v2.2. STEP 5 deviation compliance check found BLG-FE-06 correctly filed in verification_report.md — no stale placeholder references this cycle.
- **Two Phase 3 deferred patches elevated to action-now:** STEP 8 review identified two Phase 3 "defer" items with sufficient specificity to apply immediately (LL-v2.3-EX-01 Date field enforcement, LL-v2.3-EX-02 mid-sprint reclassification guidance). Both applied to `execution_prompt.md` v2.7→v2.8, logged in `prompt_change_log.md`, and `OPERATIONAL_GUIDE.md` updated to v3.39.
- **verification_report.md §4 deviation register was complete:** Both P2 deviations (DEV-EPIC02-ST05-03, V-CHART-05a/b/c) had full fields — rationale, backlog items, dual sign-off (PO + DoQ). STEP 5 required only the canonical spec propagation fix (see Friction Item 1).
- **Carry-forward review was feasible:** v2.2 `lessons_learnt_closure.md` existed and all three carry-forward items could be checked. CF-2 (LL-CL-v22-01 backlog sync) resolved. CF-1 (sprint planning advisory) applied as LL-v2.2-SP-01. CF-3 (backlog ID uniqueness) applied via `backlog_management_prompt.md` v1.4 (AUD-2026-03-21). All three addressed.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type C — Dependency Stall: Delivery verification creates deviation backlog items but does not propagate deviation entries to canonical specs

**Recurrence:** Not checkable as an identical item — v2.2 Friction Item 1 was a related but distinct gap (stale backlog reference in an *existing* deviation entry); this cycle's gap is a deviation present in verification_report.md but *absent entirely* from the canonical spec's Known Deviations section.

**What happened:**
At post-ship closure STEP 5 (deviation compliance check), `docs/specs/frontend/pages/positions.md` had no Known Deviations section and no entry for DEV-EPIC02-ST05-03. The deviation had been identified and backlogged (BLG-FE-06) during delivery verification and recorded in `verification_report.md §4`, but neither the execution engine nor the verification engine propagated it to the canonical spec. The Known Deviations section and full entry were created at STEP 5 during this closure run.

**Where in the routine:** STEP 5 — Canonical Spec Deviation Compliance Check

**Root cause:** Process gap — `delivery_verification_prompt.md` STEP 3 creates the backlog item and records the deviation in the verification report but does not require checking whether the canonical spec has a Known Deviations entry. Canonical specs are not in the verification engine's write scope during normal Phase 4 execution. The closure engine is the first routine with a cross-spec deviation compliance gate.

**Blast radius analysis:**
- What would have propagated: `positions.md` would remain non-authoritative regarding the P&L (GBP) column omission; any engineer working on positions.md in a future sprint would not surface the known deviation during pre-work spec review.
- When it would have surfaced: Next `run audit` or next sprint touching `positions.md` (v2.4 BLG-FE-06).
- Recovery cost if uncaught: Low — single section add; no functional impact.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/delivery_verification_prompt.md`
  - Section: STEP 3 (Deviation Register — deviation filing and backlog item creation)
  - Change required: After creating a backlog item for a P1/P2/P3 deviation, verify that the canonical spec named in the deviation record has a Known Deviations section with an entry for this deviation. If absent: create the section and entry in the same session, using the standard Known Deviation fields (description, canonical requirement, priority, target resolution release, owner, backlog reference).
  - Owner: Head of Specs Team
  - Target: v2.4

---

### Friction Item 2

**Classification:** Type D — Cognitive Fatigue: delegation_log.md captured near-empty in sprint close commit

**Recurrence:** No — no prior instance of this specific commit-state discrepancy in prior closure files.

**What happened:**
Sprint close commit `a12233f` captured `delegation_log.md` as an approximately 1-line file (header only) rather than its 524-line working copy content. The `git add` at STEP 7 staged the near-empty version. Discovered at delivery verification STEP -1 when `git diff` for the delegation log showed "rewrite (99%)" — indicating the index held an effectively empty file while the working copy held the full content. The correct 524-line content was re-committed as part of the delivery verification commit `b2121e7` (permissible — file was correct in working directory throughout).

**Where in the routine:** Sprint Close STEP 7 (commit sprint close artefacts) / Post-ship closure preflight

**Root cause:** Cognitive fatigue under context-window pressure at sprint close. The delegation_log.md had been written incrementally across a multi-session sprint, and the file's disk state was not verified against working copy expectations before the `git add`. The tool write sequence left the index in a near-empty state rather than the full working copy.

**Blast radius analysis:**
- What would have propagated: If the delivery verification preflight had not caught it, the delegation log in HEAD would have remained near-empty, breaking traceability for all 13 DEL entries. The audit trail for the v2.3 cycle's delegation decisions would have been invisible in git history.
- When it would have surfaced: `run audit` or manual review of cycle artefacts.
- Recovery cost if uncaught: Medium — re-commit would still be possible, but git history would show the gap and require explanation.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/execution_prompt.md`
  - Section: STEP 7 (Seal and commit sprint close artefacts)
  - Change required: Before staging and committing sprint close artefacts, verify that `delegation_log.md` has a line count consistent with the number of DEL entries recorded in `execution_state.json.delegated_items` (each entry is multiple lines). If the line count is suspiciously low (e.g., fewer than 10 lines when delegated_items is non-empty), surface a warning and confirm before proceeding with `git add`.
  - Owner: Head of Specs Team
  - Target: v2.4

---

## Recurrence Escalations

None. Both friction items are either not checkable (no prior instance) or confirmed non-recurrences relative to prior closure files.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §5.1 QA sign-off block template | LL-v2.3-EX-01: Date field requirement note added — Date must be non-blank when sign-off is completed; checkboxes pre-checked in template | v2.7→v2.8 | Yes — appended to `claude/system/prompt_change_log.md` |
| `claude/system/execution_prompt.md` | §5.1 Delegation Classification | LL-v2.3-EX-02: Mid-sprint reclassification guidance added — when story classification changes after delegation record created, cancel the log entry immediately | v2.7→v2.8 | Yes — appended to `claude/system/prompt_change_log.md` |
| `claude/system/OPERATIONAL_GUIDE.md` | §8 source prompt header + §14 governance table | execution_prompt.md v2.7→v2.8 reflected in both locations | v3.38→v3.39 | Yes — appended to `claude/system/prompt_change_log.md` |

---

## New files created this run

None.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/delivery_verification_prompt.md` | STEP 3 (Deviation Register) | After creating a backlog item for a deviation, verify and update canonical spec Known Deviations section in the same session | Head of Specs Team | v2.4 |
| `claude/system/execution_prompt.md` | STEP 7 (Seal and commit) | Add pre-commit line count check for delegation_log.md — warn if suspiciously small relative to delegated_items count | Head of Specs Team | v2.4 |
| `claude/system/execution_prompt.md` | §5.1 Delegation Classification table | Update `delegated_frontend` table entry — description still references "Base44 code generation (prompt → generate → review → integrate pattern)"; this model is superseded by engine-autonomous delivery per 2026-03-26 decision | Head of Specs Team | v2.4 |
| `claude/system/execution_prompt.md` | STEP 3.1.A (post-merge confirmation) | [SECOND RECURRENCE — LL-v2.2-EX-01] "Update delegation log entry to Unblocked" substep still not reliably triggered in-flight; two sprint cycles of bulk STEP 5.0 cleanup suggest prompt phrasing insufficient — consider stronger gate language | Head of Specs Team | v2.4 — action-now priority |
| `claude/system/execution_prompt.md` | STEP 4 merge gate completion block | [SECOND RECURRENCE — LL-v2.2-EX-02] Sprint close advisory still not preventing delivery verification being invoked before STEP 5 | Head of Specs Team | v2.4 — action-now priority |
| `claude/system/execution_prompt.md` | §9.1 schema note | [SECOND RECURRENCE — LL-v2.2-EX-04] spec_references empty for tooling/infrastructure items still triggering traceability gap flags at delivery verification | Head of Specs Team | v2.4 — action-now priority |

---

## Escalations

None.

---

## Carry-Forward

Items: 4

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Three second-recurrence Phase 3/4 items (delegation log in-flight updates LL-v2.2-EX-01, sprint close advisory LL-v2.2-EX-02, spec_references for tooling LL-v2.2-EX-04) were deferred again to v2.4 despite strong prior-cycle wording — prompt changes applied but not behavioural-effective | Sprint planning for v2.4 should schedule an engine patch session before the sprint starts specifically for these three items; do not absorb them into regular sprint backlog where they risk deferral again | Sprint Planning |
| 2 | `delegated_frontend` classification in execution_prompt.md §5.1 still references Base44 code generation model (superseded 2026-03-26 by engine-autonomous delivery decision) | Sprint planning should note this classification drift and ensure execution engine is not triggering Base44 delegation patterns for frontend stories in v2.4 | Sprint Planning |
| 3 | Post-ship STEP 5 (deviation compliance) caught a deviation (DEV-EPIC02-ST05-03) that was present in verification_report.md but absent from the canonical spec — this is the second time closure has been the first gate to enforce canonical spec propagation (v2.2 caught stale backlog references; v2.3 caught missing Known Deviations section) | Release planning for v2.4 should confirm the delivery_verification_prompt.md patch (deferred above) is scheduled as an early priority — closure is too late in the cycle to be the first canonical spec enforcement gate | Release Planning |
| 4 | v2.3 introduced the autonomous frontend delivery model (engine replacing Base44) mid-sprint, resulting in 12 of 13 delegation entries being cancelled. The governance tooling (delegation_log schema, execution_state.json classification) was not designed for this scenario | Roadmap should consider whether the autonomous frontend model warrants a governance prompt update cycle (simplifying delegation tooling for fully autonomous sprints) before v2.4 execution | Roadmap |
