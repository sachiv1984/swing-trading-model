Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-17

---

# QA Evidence Log — EPIC-06 Governance Tooling

**EPIC:** EPIC-06 — Governance Tooling (Parallel Track)
**Cycle:** 2026-03-17__release-v2.0
**Branch:** exec/2026-03-17__release-v2.0/EPIC-06
**Sprint goal:** Ship the v2.0 core product scope: fix the P1 portfolio response defect, deliver the UK tax-year P&L report endpoint and frontend view, and expose the signal exposure controls — making all three production-ready in a single sprint.

**Note:** EPIC-06 is a parallel governance track. Its changes (roadmap_prompt.md, idea_intake_prompt.md) take effect at the next `run roadmap` invocation after v2.0 ships. Not a blocker for product EPIC PRs.

---

## EPIC-06 Consolidation

**Test scenarios used:** Derived from spec + AC (governance prompt rewrites — functional verification at next `run roadmap`)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-18 | `claude/system/roadmap_prompt.md v4.0`; `OPERATIONAL_GUIDE.md v3.24` | roadmap_prompt.md v3.0→v4.0: cycle_record.md pattern all tiers; CLAUDE.md §6 checklist | All AC met; prompt change log updated | Pending QA | None |
| ST-19 | `claude/system/idea_intake_prompt.md v2.0`; `shared_standards.md v2.3` | idea_intake_prompt.md v1.3→v2.0; ideas_register.md created; 44 ideas migrated | All AC met; CLAUDE.md §6 checklist | Pending QA | None |

**ST-18 — Roadmap Stage Document Consolidation (BLG-GOV-01)**

**Commits:** `03e0060`, `7858d91` on `exec/2026-03-17__release-v2.0/EPIC-06`

**What was built:**
`roadmap_prompt.md` v3.0→v4.0. All STEP 2–8 write targets updated from per-stage files to `cycle_record.md` section references for all three tiers (Lightweight/Standard/Extended). STEP 9 write plan template updated with `cycle_record.md` entry. STEP 4 updated to load from `ideas_register.md` (ST-19 integration). OPERATIONAL_GUIDE.md §6 engine steps table updated. Prompt change log appended. CLAUDE.md §6 checklist completed.

**Acceptance criteria:**
- [x] `roadmap_prompt.md` v4.0 completed
- [x] All stage file references removed (only `cycle_record.md` section references remain)
- [x] Applies to all three tiers
- [x] STEP 9 write plan template updated
- [x] OPERATIONAL_GUIDE.md §6 updated
- [x] CLAUDE.md §6 governance checklist completed

**ST-19 — Ideas Register (BLG-GOV-02)**

**Commit:** `a236678` on `exec/2026-03-17__release-v2.0/EPIC-06`

**What was built:**
`idea_intake_prompt.md` v1.3→v2.0: per-file model replaced with `ideas_register.md` register model. `claude/ideas/ideas_register.md` created with 44 ideas migrated from IW-20260304-01. 45 prior submission files archived to `claude/ideas/submissions/archive/`. `shared_standards.md` v2.3: §16.5 ideas_register.md schema added. `OPERATIONAL_GUIDE.md` §5 updated. CLAUDE.md §6 checklist completed.

**Acceptance criteria:**
- [x] `idea_intake_prompt.md` v2.0 completed
- [x] `ideas_register.md` created with all ideas migrated
- [x] Prior per-file submissions archived
- [x] `shared_standards.md` §16.5 schema added
- [x] CLAUDE.md §6 governance checklist completed

**QA test coverage:**
- Scenarios run: Manual review of prompt changes against AC; functional test deferred to next `run roadmap` invocation
- Regression areas checked: roadmap_prompt.md tier coverage; idea_intake_prompt.md register model; OPERATIONAL_GUIDE.md consistency
- Known deviations filed: None

**QA sign-off block:** *(Director of Quality completes this)*
> **Authoring note:** When completing the sign-off block, update all AC table rows from "Pending" to "Pass" or "Pass with notes" in the same edit.
- [ ] All acceptance criteria verified (governance prompt changes reviewed)
- [ ] No unresolved P0 or P1 deviations
- [ ] Note: functional verification of prompt changes occurs at next `run roadmap` invocation
- Signed off by: Director of Quality
- Date:
- Comments:
