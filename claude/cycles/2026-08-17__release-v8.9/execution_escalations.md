Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-18

# Execution Escalations — 2026-08-17__release-v8.9

Append-only. Never edit a previous entry.

---

## ESC-EXEC-20260818-02

- **Raised at:** 2026-08-18T13:15:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-17__release-v8.9
- **Step:** 3.1 (write-scope self-correction)
- **ST/EPIC item:** ST-21 / EPIC-06
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-21 (BLG-GOV-264) requires "`claude/roadmap/displacement_debt_register.md` created with the seeded content" as AC-1. `claude/roadmap/*` is unconditionally listed as "Must not modify" in `execution_prompt.md` §7's write-scope hard gate, with no exception (unlike `claude/system/*` governance prompts, which CLAUDE.md §6 explicitly sanctions for sprint-story edits, and unlike `claude/backlog/backlog.md`, which has its own narrow explicit carve-out). This engine initially created the file directly (an error, self-caught and reverted before commit) — the file genuinely cannot be created by Sprint Execution Engine, only by a live Roadmap Rebalance Engine invocation (`run roadmap` / `manage roadmap`), which does hold that write scope. This is the same conclusion the original ST-14 design (`claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md`) reached, tracked as `ESC-EXEC-20260727-02` in that (now-sealed) cycle's own `execution_escalations.md`.
- **Owning authority:** Roadmap Rebalance Engine / Head of Specs Team
- **Unblock criteria:** At the next `run roadmap` or `manage roadmap` invocation, `roadmap_prompt.md` STEP 8 (v9.16, already wired by this cycle's ST-21) creates `claude/roadmap/displacement_debt_register.md` on its first trigger (a new displacement candidate is flagged), using the create-if-absent instruction and seed content already in place. If no displacement candidate is flagged for several cycles, Head of Specs Team may create the file directly outside a governed routine instead of waiting indefinitely.
- **SLA due-by:** N/A — Workforce/Capacity-class, no fixed due-by; tracked for the next natural trigger.
- **Blocks execution:** No — the prompt-wiring half of ST-21 (STEP 8 instruction, `roadmap_prompt.md` v9.15→v9.16) is genuinely completable by Sprint Execution and is done; only the physical file-creation half is deferred.
- **Disposition:** Open
- **Resolution summary:** (to be completed when a live Roadmap Rebalance Engine invocation creates the file) — this record supersedes, without touching, the sealed `ESC-EXEC-20260727-02` in `claude/cycles/2026-07-27__release-v7.9/execution_escalations.md` (CLAUDE.md "never modify sealed artefacts" — that cycle has `closure_record.md`/`closure_state.json`, so its own escalation entry cannot be edited or closed from this cycle). When the file is eventually created, both this record AND the original `ESC-EXEC-20260727-02`'s intent are satisfied; the original sealed record should be left as-is (a resolved-in-spirit historical artefact), with the actual live resolution tracked here instead.
