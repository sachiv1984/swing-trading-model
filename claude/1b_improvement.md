# Phase 1B — Release Planning Artefacts Consolidation

## Objective
Replace multiple intermediate files with a single consolidated file, `release_plan.md`, while keeping final outputs separate for efficiency and clarity.

## Engine Instructions

1. Collapse intermediate reasoning artefacts:
   - stage1_readiness.md
   - stage2_scope_extraction.md
   - stage3_execution_plan.md
   - stage3_5_model_integrity.md
   - stage4_5_capacity_check.md
   - stage5_5_cross_stage_integrity.md
   - stage5_7_decision_record_integrity.md
   **Into:** release_plan.md

2. Structure `release_plan.md` with sections:
   - ## Readiness
   - ## Scope
   - ## Execution Plan
   - ## Capacity Check
   - ## Integrity Validation
   - ## Backlog Slice

3. Retain **final artefacts separately**:
   - scope--{cycle}.md
   - decisions--{cycle}.md
   - stage4_backlog_slice.md

4. Update all internal references in:
   - `.claude_current_state.json`
   - lifecycle guide (`claude/charter/document_lifecycle_guide.md`) 
   - Phase 1B instructions
   to point to `release_plan.md` for all intermediate reasoning outputs.

5. Token efficiency:
   - All intermediate reasoning remains inside `release_plan.md`.
   - Preserve formatting, headings, and content fidelity.

6. Commit & log changes:
   - Add entry to `claude/system/prompt_change_log.md`: "Intermediate Release Planning artefacts collapsed into release_plan.md, final outputs retained."

## Exit Criteria
- `release_plan.md` contains all collapsed content, fully structured.
- References updated in lifecycle guide, `.claude_current_state.json`, and Phase 1B instructions.
- prompt_change_log.md entry created and committed.