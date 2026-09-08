**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-29, EPIC-04, v9.2, BLG-GOV-253 — checklist created)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Onboarding Checklist — New Governance Agent Role

Use this checklist whenever a new named authority role is introduced into the governance system (e.g. a new `claude/agents/<role>.md` charter file, referenced from a governance prompt's Agent Integrity or Delegated Authority sections). For the fuller step-by-step procedure behind each item, see `claude/system/agent_onboarding_runbook.md` (ST-32).

- [ ] **Charter file created** at `claude/agents/<role_slug>.md`, following the existing header format (`Role`, `Reports to`, `Governance alignment`, `Scope`, `Status`, `Version`, `Last Updated`) and a Purpose / Core Responsibility structure matching sibling role files.
- [ ] **Required-roles lists updated.** Search every governance prompt's `## Agent Integrity (Required Roles)` (or equivalent §6-numbered) section for whether this role should be added. Not every new role belongs on every engine's list — add only where the role's domain is actually load-bearing for that phase.
- [ ] **Delegation classification reviewed.** If the role will receive delegated work (per `execution_prompt.md` §5.1), confirm which delegation class(es) route to it and that the classification rules text names the role explicitly where needed.
- [ ] **Agent-mediated sign-off eligibility confirmed.** Per `execution_prompt.md` §5.3, a role is sign-off-eligible when its decisions are reviewable against documented criteria in its own charter. Confirm the new charter's Purpose/Core Responsibility sections state criteria concrete enough to review against — a role with only vague responsibility language cannot receive agent-mediated sign-off and must be flagged as always-human until its charter is sharpened.
- [ ] **Reports-to / governance-alignment chain verified** — confirm the named `Reports to` and `Governance alignment` roles already exist as charter files (no dangling reference to an undefined role).
- [ ] **`CLAUDE.md` §6 checklist applied** if onboarding required any governance prompt edit (version bump, `OPERATIONAL_GUIDE.md` §14 sync, phase section header sync, `prompt_change_log.md` entry).
- [ ] **First sign-off dry run.** Before relying on the new role's agent-mediated sign-off in a live governed routine, perform one dry-run review against a real (already-decided) prior artefact in its domain, to confirm the criteria in its charter are specific enough to produce a decision, not just a rubber stamp.

Sign-off on the checklist definition itself (not each individual use): Head of Specs Team.
