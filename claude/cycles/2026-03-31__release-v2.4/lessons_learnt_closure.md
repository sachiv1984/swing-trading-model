**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-04-03
**Cycle:** 2026-03-31__release-v2.4

---

# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v2.4 Correctness, Insight & Governance Hardening — post-ship closure
Run: 2026-03-31__release-v2.4
Reviewed by: PMO Lead
Date filed: 2026-04-03
Prior cycle closure file checked: `claude/cycles/2026-03-24__release-v2.3/lessons_learnt_closure.md` — found. Recurrence check completed.

---

## What Worked Well

- **v2.3 carry-forward items CF-1 through CF-3 fully resolved:** All five second-recurrence execution items (LL-v2.2-EX-01/02/04, LL-v2.3-CL-01/02) applied in execution_prompt.md v2.9; canonical spec propagation note applied in delivery_verification_prompt.md v1.7. All four carry-forward items actioned.
- **Three action-now patches applied at STEP 8:** LL-v2.4-EX-01 (delegation log Unblocked hard gate — third recurrence), LL-v2.4-P4-01 (QA evidence file existence check — second recurrence), LL-v2.4-P4-02 (pre-met path QA evidence requirement). Execution prompt advanced to v3.0. OPERATIONAL_GUIDE to v3.44.
- **DEV-ST14-01 three missing fields remediated at STEP 5:** `slippage_scenarios.md` Known Deviations entry was missing Canonical requirement, Target resolution release, and Owner fields — all added in the same closure session, restoring full 6-field compliance.
- **Backlog fully recovered after hook-induced file destruction:** `backlog.md` was overwritten by a user-prompt-submit hook capturing the `run post-ship` command text. Recovery via `git checkout HEAD -- claude/backlog/backlog.md` restored all content; all session changes (4 new items, 13 COMPLETE markings) were re-applied in the same session with no data loss.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type A — Governance Drift: Two prompt version bumps (execution_prompt.md v2.8→v2.9 and delivery_verification_prompt.md v1.6→v1.7) were applied during the v2.4 cycle without corresponding entries in `claude/system/prompt_change_log.md`, violating CLAUDE.md §6 step 4.

**Recurrence:** No — first instance of this specific gap (missing log entries from mid-sprint prompt applications).

**What happened:**
During v2.4 sprint execution (EPIC-06 ST-16), the v2.3 closure deferred patches were applied to execution_prompt.md (v2.8→v2.9) and delivery_verification_prompt.md (v1.6→v1.7). Both changes were substantive and correctly version-bumped, but neither produced a `prompt_change_log.md` entry at the time of application. The gap was detected at post-ship STEP 8.5 when the prior cycle's outstanding patches were cross-checked against the log. The two missing entries were appended as an action-now fix during this closure session.

**Where in the routine:** Sprint Execution STEP 8 (commit) / Post-Ship Closure STEP 8.5 (prompt change log cross-check)

**Root cause:** Process gap — the CLAUDE.md §6 checklist mandates prompt_change_log.md update atomically with any governed prompt edit. When applying deferred patches from a prior closure during sprint execution, the sprint execution engine (execution_prompt.md) does not have an explicit substep reminding the engine to append to prompt_change_log.md for any governance file modifications applied in-sprint.

**Blast radius analysis:**
- What would have propagated: prompt_change_log.md would have remained gap-ridden — versions v2.9 and v1.7 exist in the files but have no log entry linking them to the triggering friction items. Future audit or lessons learnt cross-checks would find the versions but no explanatory log entry.
- When it would have surfaced: `run audit` scan of prompt_change_log.md or future post-ship closure recurrence check against this cycle.
- Recovery cost if uncaught: Low — entries can be reconstructed from changelog blocks in the prompt files themselves; no functional impact.

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/prompt_change_log.md`
  - Section: Changes table
  - Change: Two missing entries appended — execution_prompt.md v2.8→v2.9 (2026-03-31) and delivery_verification_prompt.md v1.6→v1.7 (2026-03-31) — reconstructed from the files' own changelog blocks.
  - Version: N/A (append-only log — no version bump; content corrected)
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Not applicable (this IS the log entry)

→ Deferred patch (structural prevention):
  - File: `claude/system/execution_prompt.md`
  - Section: STEP 8 (Commit sprint close artefacts) or a new §6.1 sub-note
  - Change required: Add a governance file edit reminder note — if any governance prompt or CLAUDE.md §6-governed file was modified during this sprint execution run (including applying deferred patches), the engine must append to `claude/system/prompt_change_log.md` before committing. One entry per file modified.
  - Owner: Head of Specs Team
  - Target: v2.5

---

### Friction Item 2

**Classification:** Type A — Governance Drift: verification_report.md §9 Product Owner and Director of Quality sign-off blocks were sealed with blank Date fields.

**Recurrence:** No — prior instances (v2.3 qa_evidence blank date) were addressed by LL-v2.3-EX-01 (execution_prompt.md QA sign-off template); the verification_report.md seal-gate equivalent does not exist.

**What happened:**
At post-ship closure STEP -1.3 (lifecycle guard), the `verification_report.md` §9 sign-off blocks for Product Owner and Director of Quality contained empty Date fields. The document was already sealed (committed, immutable). The global state (`.claude_current_state.json` status = `Verified_with_deviations`) and the delivery verification commit record were treated as authoritative evidence of completed sign-off; the blank dates were recorded as a documentation gap in closure STEP 0 and flagged for the closure record outstanding actions. The sealed status prevented in-session correction.

**Where in the routine:** Post-Ship Closure STEP -1.3 (lifecycle guard) / Delivery Verification STEP 9 (seal)

**Root cause:** Template omission — `delivery_verification_prompt.md` STEP 8/9 (output template for `verification_report.md §9`) does not include a pre-seal gate checking that both sign-off Date fields are non-blank before sealing. The QA evidence equivalent gate exists (LL-v2.3-EX-01 added it to qa_evidence), but the verification_report itself lacks this gate.

**Blast radius analysis:**
- What would have propagated: Post-ship closure lifecycle guards consistently find blank verification_report sign-off dates; the gap accumulates across cycles as a documentation quality deficit.
- When it would have surfaced: Post-ship closure preflight every cycle where verification_report dates were left blank.
- Recovery cost if uncaught: Low (documentation gap only — sign-offs were given, just not dated); however repeated cycles of this finding degrade trust in the sign-off completeness check.

**Process patch:**

→ Deferred patch:
  - File: `claude/system/delivery_verification_prompt.md`
  - Section: STEP 8 or STEP 9 (verification report seal / sign-off gate)
  - Change required: Before sealing `verification_report.md`, verify that §9 Product Owner and Director of Quality sign-off blocks both have non-blank Date fields. If either is blank: surface for completion before proceeding. Mirror the non-blank enforcement applied to qa_evidence via LL-v2.3-EX-01.
  - Owner: Head of Specs Team
  - Target: v2.5

---

### Friction Item 3

**Classification:** Type D — Cognitive Fatigue: user-prompt-submit hook captured `run post-ship` command text and overwrote `claude/backlog/backlog.md` at session start.

**Recurrence:** No — first instance of hook-induced file destruction.

**What happened:**
When the user issued the `run post-ship` command, the Claude Code `user-prompt-submit-hook` processed the input text and wrote it to `claude/backlog/backlog.md`, completely overwriting the file with the literal text "run post-ship". This was detected at STEP 3 (backlog update) when the file was observed to be near-empty. Recovery required `git checkout HEAD -- claude/backlog/backlog.md` (restoring from last commit) followed by re-application of all in-session changes (4 new backlog items added earlier in the session, then the 13 COMPLETE markings required by STEP 3). Total re-application time approximately 15 minutes of context.

**Where in the routine:** Post-Ship Closure STEP 3 (backlog update)

**Root cause:** Hook configuration — the user-prompt-submit-hook is configured to write the prompt text to a target file. The hook appears to have targeted `backlog.md` either intentionally (for a different use case) or as a misconfiguration. The post-ship closure engine has no write-scope guard that would detect an external file modification mid-run.

**Blast radius analysis:**
- What would have propagated: If not caught — `backlog.md` would have been committed as a near-empty file, losing all active backlog items. Recovery from git would have been possible but required a corrective commit on the main branch.
- When it would have surfaced: Immediately on inspection; or at the next backlog management cycle when items were found missing.
- Recovery cost if uncaught: Medium — git restore is trivial; the backlog history of 13 COMPLETE markings from v2.4 would have been lost and re-application would require re-reading the verification_report and execution_state.

**Process patch:**

→ Deferred patch:
  - File: User's Claude Code hook configuration (not a governance prompt)
  - Section: user-prompt-submit-hook definition
  - Change required: Review and correct the user-prompt-submit-hook configuration so that it does not write prompt text to `claude/backlog/backlog.md`. Determine the intended target file for the hook and restrict its write scope accordingly.
  - Owner: Infrastructure & Operations Owner
  - Target: v2.5 (before next governed sprint execution)

---

## Recurrence Escalations

None. No friction item from this closure is a recurrence of a prior closure friction item with an open outstanding action. The v2.3 closure outstanding patches (execution_prompt.md v2.9, delivery_verification_prompt.md v1.7) were applied during the v2.4 sprint cycle. The prompt_change_log gap (Friction Item 1) is a first-instance finding.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/execution_prompt.md` | §3.1.D delegated_decision unblock detection | LL-v2.4-EX-01 (third recurrence): hard gate added requiring delegation log updated to Unblocked atomically with status=done | v2.9→v3.0 | Yes — appended to `claude/system/prompt_change_log.md` |
| `claude/system/execution_prompt.md` | STEP 5.1 QA Evidence File Existence Check | LL-v2.4-P4-01 (second recurrence): verify qa_evidence_EPIC-xx.md exists for every merged EPIC before sprint close; missing file is a hard gate | v2.9→v3.0 | Yes — appended to `claude/system/prompt_change_log.md` |
| `claude/system/execution_prompt.md` | §3.1.A pre-met path note | LL-v2.4-P4-02: pre-met items still require qa_evidence_EPIC-xx.md with DoQ sign-off; pre-met does not mean unverified | v2.9→v3.0 | Yes — appended to `claude/system/prompt_change_log.md` |
| `claude/system/OPERATIONAL_GUIDE.md` | §8 source prompt header + §14 governance table | execution_prompt.md v2.9→v3.0 reflected in both locations | v3.43→v3.44 | Yes — appended to `claude/system/prompt_change_log.md` |
| `claude/system/prompt_change_log.md` | Changes table | Backfilled two missing entries: execution_prompt.md v2.8→v2.9 and delivery_verification_prompt.md v1.6→v1.7 (both applied 2026-03-31 without log entries) | N/A (append-only) | Not applicable |

---

## New files created this run

None — all outputs are updates to existing files or new cycle artefacts (closure_record.md, lessons_learnt_closure.md) per the governed post-ship write scope.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | STEP 8 or §6.1 sub-note | Add governance file edit reminder — if any §6-governed file modified during sprint execution, engine must append to prompt_change_log.md before commit | Head of Specs Team | v2.5 |
| `claude/system/delivery_verification_prompt.md` | STEP 8/9 (verification report seal) | Before sealing verification_report.md, verify §9 sign-off Date fields are non-blank; surface for completion if blank | Head of Specs Team | v2.5 |
| Hook configuration | user-prompt-submit-hook | Review and restrict hook write target — must not write prompt text to claude/backlog/backlog.md | Infrastructure & Operations Owner | v2.5 |

---

## Escalations

None.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | v2.4 sprint applied two prompt patches (execution_prompt.md v2.9, delivery_verification_prompt.md v1.7) mid-sprint without prompt_change_log.md entries — a recurring gap pattern where deferred patches are applied in-sprint but the log requirement is missed | Sprint planning for v2.5 should include a governance hygiene note: any in-sprint prompt edits (including deferred patch application) must be logged in prompt_change_log.md in the same session as the edit; sprint execution engine needs a structural reminder at STEP 8 | Sprint Planning |
| 2 | verification_report.md §9 sign-off Date fields were blank at sealing — the same enforcement that prevents blank qa_evidence dates (LL-v2.3-EX-01) does not exist for the verification_report itself | Release planning for v2.5 should confirm the delivery_verification_prompt.md STEP 8/9 seal gate patch (deferred above) is scheduled as a priority; post-ship closure lifecycle guards will continue to fail without it | Release Planning |
| 3 | trade_history.md Known Deviations entry for DEV-ST14-01 remains absent — verified that the v1.7 canonical spec sync note was applied to delivery_verification_prompt.md but the Phase 4 verification engine (read-only for canonical specs) deferred the entry to Head of Specs Team rather than creating it; closure STEP 5 did not complete this outstanding action | Head of Specs Team must create the trade_history.md Known Deviations section and DEV-ST14-01 entry before v2.5 sprint execution begins; future closure engines should include this as an explicit STEP 5 completion check | All |
