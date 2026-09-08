**Owner:** Director of HR
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-32, EPIC-04, v9.2, BLG-GOV-271 — runbook created)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Agent Onboarding Runbook — Adding a New Governance Role

This is the step-by-step procedure behind `claude/charter/governance_role_onboarding_checklist.md` (ST-29). Follow this runbook when a new named governance authority role is being introduced.

## 1. Establish the Need

Before creating a role, confirm it is solving a real gap: a decision, sign-off, or accountability currently has no named owner, or an existing role is carrying disproportionate breadth (see `roadmap_prompt.md` §7.2 Cross-Role Workload Balance Check for the diagnostic signal that might surface this). Adding a role is not free — every role added increases the Agent Integrity list surface area every governed routine must check.

## 2. Draft the Charter

Create `claude/agents/<role_slug>.md` using an existing role file as a template (e.g. `finops_resource_architect.md`). Required sections:
- Header block: `Role`, `Reports to`, `Governance alignment`, `Scope`, `Status`, `Version` (start at `1.0`), `Last Updated`
- `1. Purpose` — why this role exists, in terms of a gap it closes
- `2. Core Responsibility` — what it owns, stated concretely enough to support agent-mediated sign-off later (per `execution_prompt.md` §5.3 — vague responsibility language cannot be reviewed against)

## 3. Wire Into Governance Prompts

For each governed routine (`roadmap_prompt.md`, `sprint_planning_prompt.md`, `execution_prompt.md`, `delivery_verification_prompt.md`, `post_ship_closure.md`, `release_planning_prompt.md`, `design_gate_prompt.md`, `backlog_management_prompt.md`, `ideas_housekeeping_prompt.md`, `roadmap_management_prompt.md`):
1. Read its `Agent Integrity (Required Roles)` section (or equivalent).
2. Decide whether this new role is load-bearing for that phase — i.e. does the phase produce a decision, sign-off, or gate this role should own or be consulted on? If yes, add it to the list.
3. If the role receives delegated execution work, update `execution_prompt.md` §5.1's classification rules to name it where applicable.
4. Apply `CLAUDE.md` §6's Governance File Edit Checklist for every prompt file touched (version bump, `OPERATIONAL_GUIDE.md` §14 sync, phase section header sync, `prompt_change_log.md` entry).

## 4. Validate Sign-Off Eligibility

Per `execution_prompt.md` §5.3, agent-mediated sign-off requires criteria reviewable against the charter. Read the drafted charter back and ask: could a reviewer (human or agent) point to a specific line and say "this criterion is met/unmet" for a real artefact? If the charter only supports subjective judgment calls with no stated criteria, either sharpen the charter or mark the role always-human-sign-off until it is sharpened.

## 5. Dry-Run the First Sign-Off

Before the role's sign-off is relied on in a live governed routine, perform one dry run: pick a real, already-decided prior artefact in the role's domain and have the role (agent-mediated or human) review it against its own charter criteria, blind to the actual historical decision. Compare. A dry run that reproduces the historical decision is a good signal the charter's criteria are specific enough to be useful; a dry run that diverges materially means the charter needs another pass before the role is trusted in production governance flow.

## 6. Announce and Close Out

Record the new role's introduction in `prompt_change_log.md` (as part of the same commit as any prompt edits from §3) and note it in the next `run_manifest.md`'s "Decision authorities and non-decision roles activated" line so downstream sessions are aware of the addition.

## Sign-Off

**Director of HR:** Approved. This runbook correctly sequences charter drafting before governance-prompt wiring, and the dry-run step (§5) closes a real gap — without it, a role's first live sign-off would be its only test of whether the charter's criteria are actually usable. Sprint Execution Engine (agent-mediated, Director of HR role — §5.3), 2026-09-08.
