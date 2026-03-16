**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-16
**Class:** Governance Prompt (Class 6)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Governance Invariants — Momentum Trading Assistant

Canonical list of system-wide non-negotiable invariants. All engines reference this file.
Do not duplicate these lists inline in engine prompts.

Consolidated from: `roadmap_prompt.md §9`, `claude/README.md §3`, `claude/charter/team_charter.md §6`.

## Core Invariants (All Routines)

- Authority is explicit and role-bound — no implied or delegated authority without charter
- One owner exists per decision domain
- All documents comply with lifecycle rules per `claude/charter/document_lifecycle_guide.md`
- Workforce capacity is finite and explicit — no initiative without opportunity cost
- No initiative exists without displacement unless net-zero gate is satisfied
- Delivery pressure never redefines strategy intent or canonical truth
- Strategy / Quality / Lifecycle risks may never be Accepted Risk

## Lifecycle Invariants

- Decision log (`claude/roadmap/decision_log.md`) is append-only
- Archive files are append-only — entries may not be edited after filing
- Backlog lock must be acquired before any backlog write
- Prompt version increment must have a matching `prompt_change_log.md` entry in the same commit
- Hard gate status changes must reference an evidence artefact

## Write Scope Invariants

- Each engine may only write to files listed in its §5 Write Scope
- `.claude_current_state.json` status may only be written at designated sync steps
- State may only advance along defined transitions (`lifecycle_schema.json` is authoritative)

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-16 | Initial version — consolidated from `roadmap_prompt.md §9`, `claude/README.md §3`, `claude/charter/team_charter.md §6`. AUD-2026-03-13-006. |
