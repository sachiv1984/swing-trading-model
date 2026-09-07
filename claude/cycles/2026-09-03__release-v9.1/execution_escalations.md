Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07

---

## ESC-EXEC-20260907-03

- **Raised at:** 2026-09-07T08:31:09Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-03__release-v9.1
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-34 / EPIC-05
- **Trigger type:** Strategy
- **Blocking statement:** ST-34 requires adding a worked example of the ATR-based sizing edge case to `claude/strategy/strategy_rules.md`. `claude/strategy/*` is outside this routine's write scope (execution_prompt.md §7 — CLAUDE.md §2 explicitly prohibits modifying `claude/strategy/` unless explicitly instructed by the relevant prompt). The story's own AC requires "Strategy Rules & System Intent Owner sign-off" and "no functional/behavioural change (documentation only)" — this routine cannot self-authorise the write even for a documentation-only change to this file.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** Strategy Rules & System Intent Owner (human or a session/prompt with explicit `claude/strategy/` write scope) adds the worked example and confirms it is documentation-only (no functional/behavioural change).
- **SLA due-by:** 2026-09-10T08:31:09Z (72 hours — Strategy boundary)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**

## ESC-EXEC-20260907-04

- **Raised at:** 2026-09-07T08:31:09Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-03__release-v9.1
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-35 / EPIC-05
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-35 requires documenting a minimum-interval guideline between scheduled rebalances in `claude/charter/team_charter.md` or `CLAUDE.md` §5, with "Director of HR + Head of Specs Team sign-off." Both target files are outside this routine's write scope: `claude/charter/*` is explicitly prohibited by CLAUDE.md §2 unless explicitly instructed by the relevant prompt; `CLAUDE.md` itself carries a standing write-authority grant to Head of Specs Team specifically (`shared_standards.md` §17), not to Sprint Execution's general write scope.
- **Owning authority:** Head of Specs Team (with Director of HR co-sign per the story's own AC)
- **Unblock criteria:** Head of Specs Team (human, or a session/prompt with explicit `claude/charter/`/`CLAUDE.md` write authority) adds the guideline and obtains Director of HR co-sign.
- **SLA due-by:** 2026-09-08T08:31:09Z (24 hours — Lifecycle/Process Integrity)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**
