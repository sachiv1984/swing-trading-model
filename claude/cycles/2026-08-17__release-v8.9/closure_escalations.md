Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21 (both escalations resolved same-session — ESC-CLOSE-20260821-01 as Head of Specs Team false-positive investigation, ESC-CLOSE-20260821-02 as Head of Specs Team direct action)

## ESC-CLOSE-20260821-01

- **Raised at:** 2026-08-21T00:00:00Z
- **Routine:** Post-Ship Closure
- **Cycle ID:** 2026-08-17__release-v8.9
- **Step:** STEP 8 (Lessons Learnt Review and Application)
- **ST/EPIC item:** N/A — governance-prompt clarification, not tied to a shipped story
- **Trigger type:** Quality
- **Blocking statement:** `lessons_learnt_cycle.md`'s Phase 4 record (this cycle) recorded a recurrence escalation per `shared_standards.md §6.4`: the recommendation to clarify `qa_evidence_template.md`/`execution_prompt.md §5.3`'s CI-green restatement requirement as per-fix (not per-EPIC) was first filed at `2026-08-12__release-v8.7` Phase 4 closure, re-deferred once at `2026-08-14__release-v8.8` closure, and has now carried 2 consecutive cycles with no `prompt_change_log.md` entry and no textual change found in either target file. Per §6.4, this crosses the automatic-escalation threshold rather than being silently re-deferred a 3rd time.
- **Owning authority:** Head of Specs Team
- **Unblock criteria:** Head of Specs Team decides: (a) apply the per-fix clarification to `qa_evidence_template.md`/`execution_prompt.md §5.3` (with the standard CLAUDE.md §6 governance file edit checklist applied), (b) reject the recommendation with rationale recorded, or (c) explicitly re-scope/re-defer with a new target cycle and reason for the further delay.
- **SLA due-by:** 2026-08-24T00:00:00Z (72 hours from raise)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** **False positive — already applied, no action needed.** Investigated as Head of Specs Team (2026-08-21). The CI-green per-fix restatement clarification was in fact applied at `2026-08-12__release-v8.7` post-ship closure STEP 8 (immediate lessons-learnt action, `LL-v8.7-P4-01`) — `qa_evidence_template.md` v1.10→v1.11, Standard Sign-Off Block: *"Applies per CI-triggered fix, not once per EPIC (LL-v8.7-P4-01, applied v8.7)..."* (confirmed present verbatim, header dated 2026-08-13). `OPERATIONAL_GUIDE.md` §14 Change Log row 4.161 independently confirms the same. The recurrence-check tooling at both `2026-08-14__release-v8.8` and `2026-08-17__release-v8.9` closures searched `execution_prompt.md §5.3` and `prompt_change_log.md` for the fix but never actually read `qa_evidence_template.md` itself — the file the friction item's own Process Patch named as the target — producing a false "still not applied" finding that compounded across 2 cycles into this escalation. No governance-prompt edit needed. Filed `BLG-GOV-312` (P3) to strengthen `lessons_learnt_prompt.md §3.7`'s recurrence check: when a deferred patch names a specific target file in its own Process Patch entry, that file must be read directly (not just grepped by keyword, and not substituted for a same-topic sibling file) before concluding "not applied". Closed same-session as raised — no SLA breach.

---

## ESC-CLOSE-20260821-02

- **Raised at:** 2026-08-21T00:00:00Z
- **Routine:** Post-Ship Closure
- **Cycle ID:** 2026-08-17__release-v8.9
- **Step:** STEP 8 (Lessons Learnt Review and Application)
- **ST/EPIC item:** N/A — governance-prompt clarification, not tied to a shipped story
- **Trigger type:** Quality
- **Blocking statement:** `lessons_learnt_cycle.md`'s Phase 4 record (this cycle) recorded a second recurrence escalation per `shared_standards.md §6.4`: the recommendation to add a canonical "Sandbox Access Constraint" disclosure block to `shared_standards.md` was first filed at `2026-08-12__release-v8.7` Phase 4 closure, re-deferred once at `2026-08-14__release-v8.8` closure, and has now carried 2 consecutive cycles with no `prompt_change_log.md` entry and no such block found in `shared_standards.md`. Per §6.4, this crosses the automatic-escalation threshold rather than being silently re-deferred a 3rd time.
- **Owning authority:** Head of Specs Team
- **Unblock criteria:** Head of Specs Team decides: (a) author the canonical disclosure block in `shared_standards.md` (with the standard CLAUDE.md §6 governance file edit checklist applied), (b) reject the recommendation with rationale recorded, or (c) explicitly re-scope/re-defer with a new target cycle and reason for the further delay.
- **SLA due-by:** 2026-08-24T00:00:00Z (72 hours from raise)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary:** **Applied.** Acting as Head of Specs Team (2026-08-21), authored `shared_standards.md` §16.16 Sandbox Access Constraint Disclosure Block — canonical constraint statement plus 3 stable disclosure IDs (`SBX-NO-LIVE-DB`, `SBX-NO-LIVE-STAGING`, `SBX-NO-LIVE-EXTERNAL-API`) for `qa_evidence_EPIC-xx.md` entries to cite going forward. Full CLAUDE.md §6 governance file edit checklist applied in the same commit: `shared_standards.md` v3.28→v3.29; `OPERATIONAL_GUIDE.md` §14 table + self-row + Change Log top row updated to v4.169; `claude/system/prompt_change_log.md` and `claude/system/changelogs/shared_standards_changelog.md` both appended. Backlog item `BLG-GOV-313` filed and marked complete for traceability. Closed same-session as raised — no SLA breach.
