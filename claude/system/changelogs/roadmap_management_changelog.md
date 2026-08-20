**Owner:** Head of Specs Team
**Status:** Active

# Change Log — Roadmap Management Engine

This file contains the historical change log for `claude/system/roadmap_management_prompt.md`.
The prompt itself contains only the current version — full history is here.

---

| Version | Date | Change |
|---------|------|--------|
| 1.5 | 2026-08-18 | Sprint execution `2026-08-17__release-v8.9` EPIC-06/ST-22 (BLG-GOV-260): STEP 5.2 gains a stale `RA:` marker pruning rule. `current_roadmap.md` §3 accumulates already-retired `*RA:vX.Y retired — see roadmap_archive.md...*` one-line pointers indefinitely (18+ visible as of this cycle, back to v5.0) with no forcing function to remove them, even though `roadmap_archive.md` remains the permanent record. Rule: in the same STEP 5.2 write, prune (delete outright) any already-retired pointer line whose version is more than 3 shipped releases older than the current highest-numbered release referenced in the document — counted as the number of shipped release versions strictly between the pointer's version and the current highest (inclusive of the highest, exclusive of the pointer's own version). Active (non-retired) marker blocks are never pruned by this rule. STEP 5.3's run log template gains a new `RA: markers pruned` count field (default 0). Authority: Head of Specs Team (Sprint Execution Engine, agent-mediated, ST-22, 2026-08-18). |
| 1.4 | 2026-05-09 | Modular refactor: changelog extracted to changelogs/roadmap_management_changelog.md; §3 Canonical Governance Sources replaced with reference to shared/governance_stack.md. |
| 1.3 | 2026-03-21 | LL-01-patch-4.3 (recurrence escalation, 2 cycles): STEP 5.4 added — when retiring a completed item, also update `initiative_register.md` (remove from Active Initiatives, append to Completed table with ship date and release). `initiative_register.md` added to §5 write scope. STEP 6 commit updated to include `initiative_register.md`. Resolves the register staleness pattern that recurred in cycles 2026-03-18__item-4.3 and 2026-03-21__item-3.5. |
| 1.2 | 2026-03-07 | IMP-02: Added `last_manage_roadmap_utc` and `last_manage_roadmap_outcome` state write to STEP 6 (global state update). Added `.claude_current_state.json` to §5 write scope (Phase 1M state fields only) and to STEP 6 commit list. |
| 1.1 | 2026-03-06 | Widened valid trigger windows to include pre-`run roadmap` invocation alongside Post-Ship Closure. Both windows now explicitly equal. Added known gap note for Phase 1 skipped path. Restructured §2 with explicit trigger window table for clarity. |
| 1.0 | 2026-03-04 | Initial version. |
