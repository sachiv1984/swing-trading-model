Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-29

---

# QA Evidence — EPIC-01: Governance Patch Resolution

**EPIC:** EPIC-01 — Governance Patch Resolution
**Cycle:** 2026-05-29__release-v4.3
**Sprint goal:** Deliver v4.3 by resolving all 3 outstanding v4.2 governance patches, clearing the QA backlog, completing operations and security hardening documentation, and shipping the Arc 5 P&L compliance section and frontend fixes — establishing a clean, well-tested baseline before the next feature arc.
**Test scenarios used:** Derived from spec + AC (governance documentation — no Playwright or staging scenarios applicable)

---

## Evidence Table

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | claude/system/execution_prompt.md#STEP 3.2.A | Advisory added to STEP 3.2.A: "After completing DoQ sign-off and committing qa_evidence_EPIC-xx.md, update execution_state.json `qa_signed_off: true` in the same commit." execution_prompt.md v3.30→v3.31. OPERATIONAL_GUIDE.md v4.10→v4.11. | AC-01: Advisory present in STEP 3.2.A. AC-02: Version bumped v3.30→v3.31. AC-03: OPERATIONAL_GUIDE.md §14 updated. AC-04: prompt_change_log.md entry appended. AC-05: HoST sign-off recorded. | Pass | None |
| ST-02 | claude/system/execution_prompt.md#STEP 5.3; #STEP 8 | Hard gate added to STEP 8: `git branch --show-current` must return `main`; halt with instructions if not. Advisory added to STEP 5.3 warning to verify on main before writing close artefacts. HoST decision: gate. execution_prompt.md v3.31→v3.32. OPERATIONAL_GUIDE.md v4.11→v4.12. | AC-01: HoST decision recorded (gate). AC-02: STEP 8 hard gate and STEP 5.3 advisory implemented. AC-03: Version bumped v3.31→v3.32. AC-04: OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md appended. AC-05: HoST sign-off recorded. | Pass | None |
| ST-03 | claude/system/templates/qa_evidence_template.md | Advisory added to consolidation table section: "Evidence table rows should map 1:1 to backlog slice ACs. When consolidating multiple ACs into one row, note which AC IDs are covered in the Evidence column." Template version 1.2→1.3. | AC-01: Advisory text present. AC-02: Version bumped 1.2→1.3; Class 6 checklist not applicable (template not in OPERATIONAL_GUIDE §14). AC-03: HoST sign-off recorded. | Pass | None |
| ST-04 | claude/system/OPERATIONAL_GUIDE.md#7.8 | §7.8 Staging-Only AC Categories Reference table added to OPERATIONAL_GUIDE.md with 5 categories, pattern descriptions, and examples from BLG-QA-24/28/29/30/35 (v3.7–v4.2 range). Designation rule added. OPERATIONAL_GUIDE.md v4.12→v4.13. | AC-01: Reference table produced with 5 staging-only AC categories. AC-02: 5 examples from v3.7–v4.2 (BLG-QA-24/28/29/30/35 — all 4 required IDs present). AC-03: Integrated into OPERATIONAL_GUIDE.md §7.8 (HoST decision). AC-04: HoST and DoQ sign-off recorded. | Pass | None |
| ST-05 | N/A (new document) | AI feature inventory produced at docs/ai/ai_feature_inventory.md covering all 3 AI-touching features: Claude thesis generation, AI journal summarisation, daily cost alert. Each entry includes all required fields (feature name, endpoint, model, purpose, §13 status, data inputs/outputs). | AC-01: Document filed at docs/ai/ai_feature_inventory.md. AC-02: All 3 features covered. AC-03: All required fields present in each entry. AC-04: AICGO and Strategy Rules & System Intent Owner reviewed and approved. | Pass | None |

**QA test coverage:**
- Scenarios run: Code review verification of governance prompt edits, template changes, and documentation artefacts against acceptance criteria
- Regression areas checked: execution_prompt.md STEP 3.2.A, STEP 5.3, STEP 8; qa_evidence_template.md consolidation block; OPERATIONAL_GUIDE.md §7 (Sprint Planning) and §14 (governance table); docs/ai/ new section
- Known deviations filed: None

---

## Sign-Off Block

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✗ (ST-02 classification was delegated_decision; resolved via agent-mediated HoST decision but initial classification was delegated_decision)
- Criterion 1 fails → Standard sign-off block required

> **Authoring note:** EPIC-01 has no frontend-visible changes and all AC is verifiable by code review. Criterion 1 fails only because ST-02 required a preliminary HoST decision before implementation; the actual implementation was fully autonomous. Standard sign-off below.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked (governance prompt versioning, OPERATIONAL_GUIDE §14 consistency, template content)
- [x] No frontend components modified — this EPIC modifies only governance prompts, templates, and documentation artefacts
- Signed off by: Director of Quality
- Date: 2026-05-29
- Comments: EPIC-01 is a governance documentation sprint. All 5 stories produce code-review-verifiable artefacts with no frontend changes, no staging dependencies, and no observable UI behaviour. All governance file edit checklist requirements (CLAUDE.md §6) verified: version bumps, OPERATIONAL_GUIDE §14 updates, and prompt_change_log.md entries are consistent and complete. No deviations filed.
