**Owner:** Head of Specs Team
**Status:** Active

# Change Log — Backlog Management Engine

This file contains the historical change log for `claude/system/backlog_management_prompt.md`.
The prompt itself contains only the current version — full history is here.

---

| Version | Date | Change |
|---------|------|--------|
| 1.6 | 2026-05-10 | ST-14 (EPIC-04, v3.3) — OA-03/CF-03 patch. STEP 3.5 added — Deferral Age Validation: for each Active/Parked item, count consecutive deferral cycles; if 3+ consecutive deferrals with no named PO re-deferral, flag as health-check blocker and surface to Product Owner with three options (re-defer with reason, assign release, or kill); named re-deferral format: `> PO re-deferral YYYY-MM-DD: [reason]`; re-deferral resets deferral counter; kill recommendation surfaced after 3+ deferrals and 2+ cycles of no PO engagement. Companion policy: `docs/governance/backlog_deferral_policy.md` v1.0 created. Authority: PMO Lead (ST-14, 2026-05-10). |
| 1.5 | 2026-05-09 | Modular prompt refactor — changelog extracted to `claude/system/changelogs/backlog_management_changelog.md`; §3 Canonical Governance Sources replaced with reference to `claude/system/shared/governance_stack.md`. Version bumped as part of modular refactor (OPERATIONAL_GUIDE v3.70). |
| 1.4 | 2026-03-22 | AUD-2026-03-21-005 (LL-RP-v22-01): STEP 4.5 added — ID uniqueness scan across closed items table and archive before health summary is produced. Detects duplicate item IDs in `## Closed Items` section and `backlog_archive.md`; records duplicates in health summary with "Investigate" flag; blocks further archiving of duplicated IDs without Product Owner confirmation. |
| 1.3 | 2026-03-16 | Post-ship closure v1.10 deferred patch applied. STEP 4 (Promotion Shortlist): endpoint reference check added (LL-v1.10-P3-2) — before listing any item as a Promote Candidate, verify all endpoint references in the item's AC exist in the canonical spec file; if gap found, add spec-gap notice to backlog.md and exclude item from shortlist until resolved. Prevents mid-sprint deviations from unresolvable AC. |
| 1.2 | 2026-03-07 | IMP-02: Added `last_groom_backlog_utc` and `last_groom_backlog_outcome` state write to STEP 7 (global state update). Added `.claude_current_state.json` to §5 write scope (Phase 1M state fields only) and to STEP 7 commit list. |
| 1.1 | 2026-03-06 | Widened valid trigger windows to include pre-`run roadmap` invocation alongside Post-Ship Closure. Both windows now explicitly equal. Added known gap note for Phase 1 skipped path. Added lock conflict guidance to §2. Expanded §6 classification table to include Blocked — Stale Blocker as a distinct classification. Added stale blocker row to STEP 5 change plan and STEP 6.2/6.3 outputs. Added promotion shortlist advisory note to §6 and health report template. |
| 1.0 | 2026-03-04 | Initial version. |
