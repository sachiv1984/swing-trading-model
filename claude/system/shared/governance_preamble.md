**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-21

---

# Shared Governance Preamble

Callable shared module. Invoked from the Write Scope, Agent Integrity, and Governance Invariants sections of all phase prompts. Contains canonical boilerplate — engines keep only their phase-specific content inline and reference this file for the common pattern.

---

## §Write-Scope

**Pattern (every engine):**

> During this routine you may write **only** to the paths listed in this engine's Write Scope section. Any file not listed is prohibited. Bash commands whose side-effects write outside the permitted scope are also prohibited.
>
> You must **not** modify: sealed artefacts (`sealed: true` flag or listed as `(sealed)` in the engine prompt), `claude/strategy/strategy_rules.md`, or any governance document outside the engine's declared scope.
>
> **Violation → halt.**

**Sealed-file rule:** Files marked `sealed: true` or explicitly listed as sealed in an engine's Write Scope are immutable. No engine may modify them — not even to fix a typo. Amendment requires a new cycle.

**Bash side-effect rule:** Shell commands that write files as a side-effect (e.g. test runners, scripts, build tools) are subject to the same restriction. If the side-effect cannot be scoped to permitted paths, the command is prohibited.

---

## §Agent-Integrity

**Standard verification procedure (all engines):**

For each required role name listed in the engine's Authority Roles section:
1. Locate the agent file under `claude/agents/`.
2. Confirm the file exists.
3. Confirm it contains a `**Role:** <Role Name>` line matching the role name exactly.

If any required agent file is missing **or** the `**Role:**` line is absent or mismatched: **halt** and report which roles are non-compliant. Do not proceed until all required roles are verified.

> **Known format note (execution engine only):** `head_of_specs_team.md` uses `**Role:** Head of Specs Team` in its header block rather than a dedicated role line. Treat this as compliant — the string is present in the file.

---

## §Invariants

System-wide invariants: `claude/system/invariants.md`. Violation → halt.

**Common cross-engine invariants (apply in every phase):**

- **Delivery pressure does not override governance.** No timeline instruction changes a hard gate or relaxes a quality standard.
- **No autonomous merge.** QA sign-off and Product Owner acceptance are always required before any PR merges to `main`. The engine never merges without both.
- **Commit format is non-negotiable.** `[EPIC-xx][ST-xx]` prefix on every commit to `exec/**` branches. `[GOVERNANCE]` prefix on governance-only commits. Format errors are process deviations.
- **PR title is non-negotiable.** `[EPIC-xx]` or `[GOVERNANCE]` in title. `quality_gate.yml` blocks merge without it.
- **Write scope is strictly bounded.** ∀ file write: must be in the engine's declared write scope. Proceed → halt with file path and violated rule if not.
- **Amendment slice supersedes original.** If `amended_backlog_slice_path` is set in `.claude_current_state.json`, use that file exclusively. Executing from the original slice when an amendment has sealed is a process integrity failure.
- **State advances only along defined transitions.** `lifecycle_schema.json` is authoritative for valid state machine transitions. No engine may write a status value that does not follow from the current status.
- **Every block is recorded.** Nothing is silently skipped. Blocked items are documented and surfaced to the user.

---

*This module is shared across all six phase engines: Roadmap Rebalance, Release Planning, Sprint Planning, Sprint Execution, Delivery Verification, and Post-Ship Closure.*
