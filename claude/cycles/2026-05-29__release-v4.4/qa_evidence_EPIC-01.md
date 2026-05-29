Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-29

# QA Evidence — EPIC-01 — Governance Prompt Patches

**EPIC:** EPIC-01 — Governance Prompt Patches
**Cycle:** 2026-05-29__release-v4.4
**Sprint goal:** Apply all 5 governance patches carried forward from v4.3 and produce the SI-02 pre-planning artefacts that unlock the Behavioural Drift Detection implementation sprint.
**Test scenarios used:** Derived from spec + AC (all changes are governance documentation edits — no automated test scenarios applicable)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `claude/system/roadmap_prompt.md` | Added STEP 8.1 after STEP 8 in roadmap_prompt.md: Extended-tier no-change advisory for empty Now horizon when no next-release section in current_roadmap.md; v6.5→v6.6; OPERATIONAL_GUIDE.md §6 + §14 updated; prompt_change_log.md entry appended. Covers AC-01, AC-02, AC-03, AC-04, AC-05. | AC-01: Advisory note at STEP 8.1 with exact advisory text. AC-02: Condition scoped to Extended-tier + no-change + Now empty + no next-release section. AC-03: v6.5→v6.6. AC-04: OPERATIONAL_GUIDE.md §6 + §14 updated. AC-05: prompt_change_log.md entry appended. | Pass | None |
| ST-02 | `claude/system/sprint_planning_prompt.md` | Added BLG-GOV-72 frontend classification fast-path section to §3.1 delegation class assignment with 3 explicit default-autonomous conditions and delegation override rule; v3.7→v3.8; OPERATIONAL_GUIDE.md §7 + §14 updated; prompt_change_log.md entry appended. Covers AC-01, AC-02, AC-03, AC-04, AC-05. | AC-01: Fast-path section added to story classification step. AC-02: Three conditions listed with default-autonomous rule. AC-03: v3.7→v3.8. AC-04: OPERATIONAL_GUIDE.md §7 + §14 updated. AC-05: prompt_change_log.md entry appended. | Pass | None |
| ST-03 | `claude/system/execution_prompt.md` | Updated §5.3 Protocol step 5: when sign_off_record.status = "cleared" for delegated story with no DEV-* record, also set deviations_filed = true; condition precisely scoped; v3.32→v3.33; OPERATIONAL_GUIDE.md §8 + §14 updated; prompt_change_log.md entry appended. Covers AC-01, AC-02, AC-03, AC-04, AC-05. | AC-01: Delegation sign-off substep updated with auto-set rule. AC-02: Condition scoped: delegated + cleared + no DEV-* → deviations_filed=true. AC-03: v3.32→v3.33. AC-04: OPERATIONAL_GUIDE.md §8 + §14 updated. AC-05: prompt_change_log.md entry appended. | Pass | None |
| ST-04 | `claude/system/templates/qa_evidence_template.md` | Added delegated_qa sign-off format note to Standard Sign-Off Block: two valid formats (i) individual DoQ sign-off; (ii) aggregate "Director of Quality: Confirmed — [owner] ([N] stories), YYYY-MM-DD" format; both valid; EPIC-level DoQ always required; v1.3→v1.4; OPERATIONAL_GUIDE.md §14 QA Evidence Template row added; prompt_change_log.md entry appended. Covers AC-01, AC-02, AC-03, AC-04, AC-05. | AC-01: DoQ sign-off block updated for delegated_qa pattern. AC-02: Both valid format variants shown. AC-03: Template clarifies both variants valid. AC-04: v1.3→v1.4. AC-05: OPERATIONAL_GUIDE.md §14 row updated; prompt_change_log.md entry added. | Pass | None |
| ST-05 | `claude/system/release_planning_prompt.md` | Added RESUME PRECHECK note to STEP 7 Intermediate global state sync section with exact verbatim text from AC; v2.31→v2.32; OPERATIONAL_GUIDE.md §6B + §14 updated; prompt_change_log.md entry appended. Covers AC-01, AC-02, AC-03, AC-04, AC-05. | AC-01: STEP 7 Intermediate global state sync updated with RESUME PRECHECK note. AC-02: Note text matches AC verbatim. AC-03: v2.31→v2.32. AC-04: OPERATIONAL_GUIDE.md §6B + §14 updated. AC-05: prompt_change_log.md entry appended. | Pass | None |

**QA test coverage:**
- Scenarios run: manual acceptance review (code review of governance documentation edits)
- Regression areas checked: roadmap_prompt.md STEP 8 flow, sprint_planning_prompt.md §3.1 classification logic, execution_prompt.md §5.3 sign-off protocol, qa_evidence_template.md sign-off block, release_planning_prompt.md STEP 7 sync block
- Known deviations filed: None

---

## DoQ Sign-Off

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓
- [x] Criterion 3: No frontend-visible change — no React page or UI component created or modified — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-05-29
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable by reading the patched governance files, no frontend changes, engine signer populated). All 5 governance prompt patches verified against AC in commit 45909ef295c5e22a95d357d090b06f485b73502c. OPERATIONAL_GUIDE.md v4.13→v4.18 with all phase section headers and §14 governance table updated. No deviations identified.
