**Owner:** Head of Specs Team
**Status:** Active

# Change Log — Amendment Cycle Engine

This file contains the historical change log for `claude/system/amendment_cycle_prompt.md`.
The prompt itself contains only the current version — full history is here.

---

| Version | Date | Change |
|---------|------|--------|
| 1.6 | 2026-03-14 | AUD-2026-03-13-016: Deprecation notice added to STEP 8 secondary output — `amendment_lessons.md` deprecated as of v1.5; will not be produced from v2.0 onward; canonical record is `lessons_learnt_cycle.md` Amendment section. |
| 1.5 | 2026-03-10 | IMP-37: STEP 8 — primary output changed to append `## Amendment — <AMD-id>` section to `claude/cycles/<original_cycle_id>/lessons_learnt_cycle.md` via `lessons_learnt_prompt.md §3.6`; idempotency guard built into prompt §3.6. Secondary output `amendment_lessons.md` retained for backward compat. STEP 9 commit: `lessons_learnt_cycle.md` added. §9 completion condition: `lessons_learnt_cycle.md` Amendment section appended condition added. |
| 1.4 | 2026-03-10 | IMP-35 (gap 3): STEP 8 — prompt change log idempotency guard added; before appending to `prompt_change_log.md` for any action-now patch, check for existing entry with matching prompt filename + version string; if present: skip. IMP-39: §10 Withdrawal — backlog rollback instruction added; if STEP 5 completed before withdrawal, `backlog.md` amendment marker must be reversed; `amendment_state.json.backlog_rollback_required` and `backlog_rollback_completed` fields defined. |
| 1.3 | 2026-03-10 | IMP-49: STEP -1.4 — `stage3_execution_plan.md` replaced with `release_plan.md` (schema v2 detection via `state.json.prompt_schema_version`); backward compatibility note for pre-v2.11 cycles. §4 and §4.1 references updated to match. IMP-51: STEP 2.5 added — explicit procedural step to release backlog lock before STEP 3 human ratification begins; lock re-acquired at STEP 5.1. STEP -1.1 parenthetical updated to reference STEP 2.5. Governance invariant added. |
| 1.2 | 2026-03-08 | IMP-09: Added atomicity guard to STEP -1.1 — backlog lock acquired with marker `AMEND-CHECK:<cycle_id>` before `sprint_sealed` is read; lock released after STEP 5 or on any halt. Governance invariant added. |
| 1.1 | 2026-03-07 | Added Lifecycle Guard (valid from-states: `Sprint_Planning_Complete` with `sprint_sealed = false`). |
| 1.0 | 2026-03-07 | Initial version. |
