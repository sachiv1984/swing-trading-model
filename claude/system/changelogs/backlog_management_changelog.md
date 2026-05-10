**Owner:** Head of Specs Team
**Status:** Active

# Change Log — Backlog Management Engine

This file contains the historical change log for `claude/system/backlog_management_prompt.md`.
The prompt itself contains only the current version — full history is here.

---

| Version | Date | Change |
|---------|------|--------|
| 1.4 | 2026-03-22 | AUD-2026-03-21-005 (LL-RP-v22-01): STEP 4.5 added — ID uniqueness scan across closed items table and archive before health summary is produced. Detects duplicate item IDs in `## Closed Items` section and `backlog_archive.md`; records duplicates in health summary with "Investigate" flag; blocks further archiving of duplicated IDs without Product Owner confirmation. |
| 1.3 | 2026-03-16 | Post-ship closure v1.10 deferred patch applied. STEP 4 (Promotion Shortlist): endpoint reference check added (LL-v1.10-P3-2) — before listing any item as a Promote Candidate, verify all endpoint references in the item's AC exist in the canonical spec file; if gap found, add spec-gap notice to backlog.md and exclude item from shortlist until resolved. Prevents mid-sprint deviations from unresolvable AC. |
| 1.2 | 2026-03-07 | IMP-02: Added `last_groom_backlog_utc` and `last_groom_backlog_outcome` state write to STEP 7 (global state update). Added `.claude_current_state.json` to §5 write scope (Phase 1M state fields only) and to STEP 7 commit list. |
| 1.1 | 2026-03-06 | Widened valid trigger windows to include pre-`run roadmap` invocation alongside Post-Ship Closure. Both windows now explicitly equal. Added known gap note for Phase 1 skipped path. Added lock conflict guidance to §2. Expanded §6 classification table to include Blocked — Stale Blocker as a distinct classification. Added stale blocker row to STEP 5 change plan and STEP 6.2/6.3 outputs. Added promotion shortlist advisory note to §6 and health report template. |
| 1.0 | 2026-03-04 | Initial version. |
