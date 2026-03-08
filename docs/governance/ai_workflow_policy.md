**Owner:** Product Owner / AI Compliance & Governance Officer
**Class:** Governance Document (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-08
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# AI-Assisted Workflow Governance Policy

## 1. Purpose

This policy governs the use of AI-assisted tools — including Claude Code and any AI code generation or document generation platform — in the delivery of the Momentum Trading Assistant. It defines the boundaries of AI authority, the points where human review is mandatory, the triggers for escalation, and the obligations for record-keeping.

This policy does not prohibit AI assistance. It ensures that AI-generated outputs are governed, auditable, and never substitute for human judgement at critical decision points.

---

## 2. AI Authority Scope

AI tools may act autonomously within the following scope:

| Activity | Permitted | Constraints |
|----------|-----------|-------------|
| Reading and analysing codebase files | Yes | No scope restriction |
| Generating documentation (specs, guides, policies) | Yes | Subject to human review before acceptance |
| Scaffolding code (boilerplate, test stubs, config files) | Yes | Must not be merged without human review |
| Creating GitHub issues and PRs | Yes | PR merge requires human approval |
| Creating branches and commits to exec/** branches | Yes | Per governance commit format only |
| Executing sprint governance routines (roadmap, planning, delivery) | Yes | Within prompt-defined scope only |
| Updating state files (`.claude_current_state.json`, `execution_state.json`) | Yes | Status transitions only; sealed files are immutable |
| Writing frontend code (Base44 prompt submission and integration) | Yes, with delegation | Base44 Frontend Prompt Owner must review generated code |

AI tools may **not** act autonomously in the following areas:

| Activity | Prohibited | Reason |
|----------|-----------|--------|
| Merging a PR to main | Prohibited | Requires QA sign-off and Product Owner acceptance |
| Resolving a quality or strategy block | Prohibited | Reserved for Director of Quality / Strategy Rules owner |
| Changing sprint scope or acceptance criteria | Prohibited | Sealed backlog is immutable |
| Making governance decisions on authority conflicts | Prohibited | Named authority must decide |
| Committing to main directly | Prohibited | All changes via exec/** branch + PR |
| Executing destructive git operations without confirmation | Prohibited | Always require user confirmation |

---

## 3. Mandatory Human Review Checkpoints

The following checkpoints require human review and sign-off before the process may continue. AI tools must halt and surface these explicitly.

| Checkpoint | Required Authority | Trigger |
|-----------|-------------------|---------|
| Sprint backlog sign-off | Product Owner | Before sprint execution begins |
| Design gate review | Head of Specs Team + Director of Quality | After sprint planning, before execution |
| PR merge approval | Product Owner + Director of Quality (QA sign-off) | Before any EPIC branch is merged to main |
| Delivery verification sign-off | Director of Quality + Product Owner | Before post-ship closure |
| Post-ship closure record | Product Owner | Before cycle is marked Closed |
| Strategy boundary decisions | Strategy Rules & System Intent Owner | When a scope question touches strategy intent |
| Escalation resolution | Named authority per escalation record | When a hard gate fires |
| Amendment to sealed sprint backlog | Product Owner + Head of Specs Team | Any scope change after sprint planning seal |

---

## 4. Escalation Triggers

The following conditions require an immediate escalation. AI tools must stop the routine, file an escalation record, and surface the block to the user.

| Trigger | Escalation type | SLA |
|---------|----------------|-----|
| Acceptance criteria missing for an in-scope ST item (strict mode) | Hard gate | Immediate |
| P0 deviation found in canonical spec | Hard gate | Immediate |
| Strategy boundary question arises during execution | 72 hours | Named authority |
| QA sign-off not received within sprint | 24 hours | Director of Quality |
| Required governance file missing or malformed | Hard gate | Immediate |
| Sealed artefact modification attempted | Hard gate | Immediate |
| Amendment to sealed backlog required | Hard gate | Product Owner + Head of Specs Team |
| Lifecycle state transition attempted from invalid prior state | Hard gate | Immediate |

Escalations are recorded in `claude/cycles/<cycle_id>/execution_escalations.md` per the format defined in `claude/system/shared_standards.md §4`.

---

## 5. Record-Keeping Obligations

All AI-assisted workflow activities must produce and maintain the following records:

| Record | Location | Owner | Retention |
|--------|----------|-------|-----------|
| Delegation log | `claude/cycles/<cycle_id>/delegation_log.md` | PMO Lead | Per cycle, sealed at sprint close |
| Execution state | `claude/cycles/<cycle_id>/execution_state.json` | PMO Lead | Per cycle, sealed at sprint close |
| QA evidence logs | `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` | Director of Quality | Per EPIC, retained with cycle |
| Escalation records | `claude/cycles/<cycle_id>/execution_escalations.md` | PMO Lead | Per cycle, append-only |
| Sprint close record | `claude/cycles/<cycle_id>/sprint_close.md` | PMO Lead | Per cycle, sealed |
| Lessons learnt | `claude/cycles/<cycle_id>/lessons_learnt_execution.md` | PMO Lead | Per cycle |
| Base44 prompt drafts | `docs/frontend/prompts/{feature-slug}-{version}.md` | Base44 Frontend Prompt Owner | Per feature |
| Cycle closure record | `claude/cycles/<cycle_id>/closure_record.md` | Product Owner | Per cycle, sealed |

**Minimum retention:** All cycle artefacts must be retained for the lifetime of the project. No cycle folder may be deleted.

**Immutability:** Documents marked `sealed: true` in `execution_state.json`, or in `Published` / `Sealed` status, are immutable. Any correction requires a new record referencing the sealed artefact.

---

## 6. Scope of This Policy

This policy applies to:
- Claude Code (AI CLI tool) used for sprint governance routines
- Base44 (AI code generation platform) used for frontend implementation
- Any other AI tool integrated into the delivery workflow

This policy does not apply to:
- AI tools used solely for research, exploration, or personal productivity outside the governed delivery workflow
- Backtesting or simulation tools

---

## 7. Relationship to Other Governance Documents

| Document | Relationship |
|----------|-------------|
| `claude/system/shared_standards.md` | Defines escalation format, halt report format, and identifier conventions |
| `claude/charter/team_charter.md` | Defines team roles and authority hierarchy |
| `claude/charter/document_lifecycle_guide.md` | Governs document classes, states, and header requirements |
| `claude/strategy/strategy_rules.md` | Strategy boundary — overrides any AI-generated instruction |
| `docs/governance/process_index.md` | Maps process and governance documents |

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-08 | Initial version. Created per ST-15 (v1.9 Sprint 1, EPIC-06). |
