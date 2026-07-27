**Owner:** Head of Specs Team
**Status:** Active

# Change Log — Idea Intake Engine

This file contains the historical change log for `claude/system/idea_intake_prompt.md`.
The prompt itself contains only the current version — full history is here.

---

| Version | Date | Change |
|---------|------|--------|
| 2.8 | 2026-07-27 | Roadmap rebalance `2026-07-27__scheduled` STEP 11 Friction Item 1: §2.0 step 5 backlog-scope-overlap check upgraded from prose-advisory to a mandatory act (outcome still non-blocking) — the submitting agent must grep-check `backlog.md` for each planned topic before finalising it and explicitly record the result; a submission restating an existing item with no materially new angle no longer counts toward the agent's minimum. Root cause: the pre-v2.8 check existed as advisory prose but was not actually performed at submission-generation time across 20+ idea-intake windows — this cycle's retroactive STEP 4 check found 23 of 44 (52%) submissions duplicated existing open backlog items. Authority: Head of Specs Team. *(Note: rows for 2.3–2.7 are absent from this file — `prompt_change_log.md`/`OPERATIONAL_GUIDE.md` §14 confirm v2.3 (2026-05-09), v2.4 (2026-06-02), v2.5 (2026-06-09) occurred; v2.6/v2.7 bumps not found by a quick search either. Flagged, not backfilled, this cycle — see `lessons_learnt.md`.)* |
| 2.2 | 2026-03-24 | AUD-2026-03-21-001: STEP 3 — added explicit `per_agent_submission_count` computation instruction. Field existed in JSON schema since v1.3 but lacked derivation rule; IW-20260321-01 was produced without the field. Computation: for each agent slug in `eligible_agents`, count Idea IDs in `submissions_received` containing that slug. |
| 2.1 | 2026-03-18 | LL-01-patch (cycle 2026-03-18__item-4.3): STEP -0.5 added — stale idea horizon check. Before opening a window, Facilitator checks `ideas_register.md` for rows at Parked-cycle-2; if ≥15 rows, surfaces stale warning advisory in window announcement and summary. Register-model-correct version of the LL-01-patch originally filed in cycle 2026-03-17__item-v1.10 (which referenced the now-retired submissions folder model). |
| 2.0 | 2026-03-17 | ST-19 (EPIC-06): Replaced per-file submission model with single `ideas_register.md` register. §1 purpose, §5 write scope, §6 naming (→ Idea ID + register location), §9 lifecycle table, and §10 invariants updated. STEP 0 creates register if absent; STEP 1 reads parked rows from register; STEP 2.1 appends register rows; STEP 4 window summary path updated; STEP 5 commit updated. Schema: `shared_standards.md §16.5`. |
| 1.3 | 2026-03-14 | AUD-2026-03-13-018: STEP 3 ideas_window.json schema — added `per_agent_submission_count` map field. Enables roadmap STEP 4 to read per-agent counts directly without re-scanning submission files. |
| 1.2 | 2026-03-06 | Updated all `Status: Parked` references to `Parked-cycle-<n>` to align with roadmap_prompt.md v2.0 stale idea expiry logic. STEP 1 read instruction, STEP 0 window announcement, §9 lifecycle table, and §10 governance invariants updated. Added `Parked Cycle` column to window summary Parked Ideas table. Added explicit governance invariant documenting the cycle count as authoritative for stale idea expiry. |
| 1.1 | 2026-03-03 | Removed "Proposed Displacement" as a required submission field. Replaced with "What Would You Stop?" as a non-binding thinking prompt — "No view — leave to debate" is a valid answer. Displacement is now determined in STEP 5 of the roadmap engine. Updated required fields table, submission quality check, and governance invariants accordingly. Updated idea_template.md to match. |
| 1.0 | 2026-03-03 | Initial version. |
