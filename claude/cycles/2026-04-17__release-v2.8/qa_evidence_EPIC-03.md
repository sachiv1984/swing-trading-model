**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-04-19

---

# QA Evidence — EPIC-03: Governance Process Hardening

**EPIC:** EPIC-03 — Governance Process Hardening
**Cycle:** 2026-04-17__release-v2.8
**Sprint goal:** Deliver v2.8 in full: complete the v2.7 deferred market correlation frontend, fill the CORR/SIG-IND test scenario gaps, apply three governance hardening patches, and ship AI journal summarisation (backend + frontend) within the §13 compliance boundary.
**Test scenarios used:** Derived from spec + AC (no pre-existing test scenario files for EPIC-03 governance changes)

---

## ST-04 — DoQ Date Field Reminder Patch

**Spec reference:** `claude/system/execution_prompt.md §3.2.A`
**Commit SHA:** ef3f75c
**Delegation class:** autonomous

**What was built:** Updated `execution_prompt.md §3.2.A` Date field requirement note (LL-v2.3-EX-01) to explicitly state the Date field must be non-blank before the PR can be opened (§3.2.B pre-condition, BLG-GOV-18) — not only before the merge gate runs. Version bumped v3.6→v3.7. OPERATIONAL_GUIDE.md §8 and §14 updated v3.6→v3.7, OPERATIONAL_GUIDE.md v3.60→v3.61. prompt_change_log.md appended.

**Acceptance criteria verification:**
- [x] `execution_prompt.md §3.2.A` updated: explicit reminder Date field must be non-blank before PR can be opened
- [x] Version bumped: execution_prompt.md v3.6→v3.7
- [x] OPERATIONAL_GUIDE.md §8 source prompt header updated v3.6→v3.7
- [x] OPERATIONAL_GUIDE.md §14 Execution Engine Source updated v3.6→v3.7
- [x] `prompt_change_log.md` entry appended
- [x] CLAUDE.md §6 checklist fully applied

**Deviations:** None

---

## ST-05 — Sprint Close Terminology Clarification

**Spec reference:** `claude/system/execution_prompt.md §5.3 sprint_close template`
**Commit SHA:** f3b273b
**Delegation class:** autonomous

**What was built:** Updated `execution_prompt.md §5.3` "Deviations filed" bullet to explicitly state these are spec deviations only (implementation diverges from spec; filed via `/dev-file`), and that process notations, execution observations, and deferred items belong in `execution_state.json` notes column or `execution_escalations.md`. Fix is in a governed prompt file — CLAUDE.md §6 checklist applied. Version bumped v3.7→v3.8. OPERATIONAL_GUIDE.md updated v3.61→v3.62. prompt_change_log.md appended.

**Acceptance criteria verification:**
- [x] Sprint close template clarified: "Deviations filed" refers to spec deviations only
- [x] Process notations / execution observations directed to execution_state.json notes or execution_escalations.md
- [x] Fix is in governed prompt file — CLAUDE.md §6 checklist applied (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry)

**Deviations:** None

---

## ST-06 — Backlog Archive Deduplication

**Spec reference:** `claude/backlog/backlog_archive.md`
**Commit SHA:** adf4e45
**Delegation class:** autonomous
**PO confirmation:** Recorded 2026-04-18 — retain most recent entry per duplicate ID; remove earlier copies.

**What was built:** Ran Python deduplication script on `claude/backlog/backlog_archive.md`. 147 total entries found; 64 earlier duplicate entries removed; 83 unique IDs retained. Verified: 0 remaining duplicates; 0 active backlog IDs present in archive post-deduplication. `Last Updated` header updated to 2026-04-18.

**Acceptance criteria verification:**
- [x] Product Owner confirmed deduplication approach: retain most recent entry per duplicate ID; remove earlier copies
- [x] `backlog_archive.md` contains no duplicate `###` item headers (verified: 0 remaining)
- [x] No active backlog IDs present in archive post-deduplication (verified via cross-check with backlog.md)
- [x] `backlog_archive.md` Last Updated header updated to 2026-04-18
- Note: `groom backlog` ID uniqueness scan will confirm PASS when next run (BLG-GOV-13 resolution)

**Deviations:** None

---

## EPIC-level consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-04 | execution_prompt.md §3.2.A | §3.2.A Date note updated: PR-open pre-condition added | All §6 checklist items; version bumped; OG updated; change log appended | Pass | None |
| ST-05 | execution_prompt.md §5.3 | §5.3 Deviations filed clarified: spec deviations only | §6 checklist items; version bumped; OG updated; change log appended | Pass | None |
| ST-06 | backlog_archive.md | 64 duplicate entries removed; 83 unique IDs retained | PO confirmed; 0 duplicates; 0 active IDs in archive; Last Updated updated | Pass | None |

**QA test coverage:**
- Scenarios run: manual acceptance review (code review of diff)
- Regression areas checked: execution_prompt.md §3.2.A, §5.3; OPERATIONAL_GUIDE.md §8, §14; backlog_archive.md uniqueness
- Known deviations filed: None

**QA sign-off block:**
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): N/A — no frontend changes in this EPIC
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-04-18
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable, no frontend changes, engine signer populated).

**Product Owner acceptance:**
- [x] ST-04 — delivery accepted: §3.2.A Date reminder added; self-referential proof present; §6 checklist fully applied
- [x] ST-05 — delivery accepted: §5.3 terminology clarified; fix correctly in governed prompt; §6 checklist applied
- [x] ST-06 — delivery accepted: 64 duplicates removed, 0 remaining, 0 active IDs in archive; `groom backlog` scan not yet re-run post-deduplication (open action: confirm PASS on next Phase 1M run — not a merge blocker given manual verification)
- [x] No deviations requiring escalation
- [x] Delivery aligns with sprint intent: v2.7 carry-forward governance obligations closed
- Accepted by: Product Owner
- Date: 2026-04-19
