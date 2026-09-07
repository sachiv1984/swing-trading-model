Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07

---

## ESC-EXEC-20260907-01

- **Raised at:** 2026-09-07T07:55:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-03__release-v9.1
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-21 / EPIC-04
- **Trigger type:** Strategy
- **Blocking statement:** ST-21 requires adding a ST-06/BLG-FEAT-90 row to `claude/strategy/strategy_rules.md` §13.5's roster table, referencing the CONDITIONAL §13 clearance review. `claude/strategy/strategy_rules.md` is outside this routine's write scope (execution_prompt.md §7 — "Never modify governance files unless explicitly instructed... `claude/strategy/`" per CLAUDE.md §2). The story's own acceptance criteria explicitly require the edit be made "under Strategy Rules & System Intent Owner authority, in a session/prompt whose write scope explicitly covers `claude/strategy/`" — this routine cannot self-authorise that write.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** Strategy Rules & System Intent Owner (human or a session/prompt with explicit `claude/strategy/` write scope) adds the roster row and confirms CLAUDE.md §6 governance file edit checklist steps 1–4 if `strategy_rules.md`'s version is bumped.
- **SLA due-by:** 2026-09-10T07:55:00Z (72 hours — Strategy boundary)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**

## ESC-EXEC-20260907-02

- **Raised at:** 2026-09-07T07:55:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-09-03__release-v9.1
- **Step:** STEP 3.1.D (delegated_decision)
- **ST/EPIC item:** ST-26 / EPIC-04
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-26 requires physically creating `claude/roadmap/displacement_debt_register.md` (seeded content per `roadmap_prompt.md` STEP 8) and closing `ESC-EXEC-20260727-02` / `ESC-EXEC-20260818-02`. `claude/roadmap/*` is outside this routine's write scope (execution_prompt.md §7 explicitly excludes `claude/roadmap/*`; the story's own note in `stage4_backlog_slice.md` confirms this: "deferred to this story because `execution_prompt.md`'s write scope does not permit Sprint Execution to write `claude/roadmap/*`"). Carried forward from `ESC-EXEC-20260818-02` (`claude/cycles/2026-08-17__release-v8.9/execution_escalations.md`), still Open/non-blocking as of this cycle.
- **Owning authority:** PMO Lead
- **Unblock criteria:** PMO Lead (or Head of Specs Team, per the story's note) creates the register file with the seeded content from `roadmap_prompt.md` STEP 8, then closes both `ESC-EXEC-20260727-02` and `ESC-EXEC-20260818-02`.
- **SLA due-by:** 2026-09-08T07:55:00Z (24 hours — Lifecycle/Process Integrity)
- **Blocks execution:** No
- **Disposition:** Open
- **Resolution summary:**
