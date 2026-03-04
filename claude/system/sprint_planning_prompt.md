**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-03
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Sprint Planning Engine — Governance Prompt

(Backlog-Driven, Capacity-Confirmed, Criteria-Gated, Sign-Off-Sealed)

---

## 1. Purpose

Convert a release-planned backlog slice into a time-boxed, executable sprint by:
- Confirming available capacity against the backlog slice
- Defining a sprint goal owned by the Product Owner
- Selecting and confirming the sprint scope within capacity
- Verifying every entering item has defined acceptance criteria and an explicit owner
- Resolving cross-item dependencies and sequencing
- Producing a signed-off sprint backlog that Phase 3 can execute without ambiguity

This routine does **NOT**:
- Add, remove, or reprioritise items in the global backlog
- Alter the release plan or re-scope the release
- Begin any execution work
- Make strategy or architecture decisions

Sprint Planning is the bridge between a Published release plan and an executable sprint. Its outputs are hard gate inputs to Phase 3.

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
plan sprint [--cycle "<cycle_id>"] [--mode "strict|standard"] [--dry-run]
```

Rules:
- Invocation must start with `plan sprint` (case-insensitive match allowed).
- `--cycle` optional: if omitted, load `active_cycle` from `.claude_current_state.json`. If absent or ambiguous, halt.
- `--mode` optional:
  - `strict`: halt on any missing acceptance criteria, unclear owner, or unresolved dependency
  - `standard` (default): proceed with flags on minor gaps; still halt on hard gates
- `--dry-run` optional: read all inputs and produce a planning preview without writing any artefacts or updating state

If invocation is not exact, do not run. Treat as conversational.

**Who issues this command:** The PMO Lead persona, after Phase 1B has reached `Published` status.

**Tool call budget:** This routine typically requires 10–20 tool calls. Proceed through steps without requesting confirmation unless a hard gate fires.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Binding governance stack (precedence order):

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

This routine may not override any of the above.

Shared standards (escalation format, halt report format, identifier conventions, resumability): `claude/system/shared_standards.md`.

---

## 4. Required Authority Roles

Minimum required roles for this routine:

- Product Owner
- Head of Specs Team
- PMO Lead
- Director of Quality
- FinOps & Resource Architect

Verify: each role has an agent file in `claude/agents/` containing `**Role:** <Role Name>`. If any required role is missing or malformed: halt.

---

## 5. Source-of-Truth Planning Inputs

| Input | Location | Required |
|-------|----------|---------|
| Global state pointer | `.claude_current_state.json` | Hard gate |
| Release plan state | `claude/cycles/<cycle_id>/state.json` | Hard gate |
| Backlog slice | `claude/cycles/<cycle_id>/stage4_backlog_slice.md` | Hard gate |
| Committed backlog | `claude/backlog/backlog.md` | Required |
| Execution plan (EPICs) | `claude/cycles/<cycle_id>/stage3_execution_plan.md` | Required |
| Capacity check | `claude/cycles/<cycle_id>/stage4_5_capacity_check.md` | Required |
| Cycle summary | `claude/cycles/<cycle_id>/cycle_summary.md` | Required |
| Workforce capacity | `claude/roadmap/workforce_capacity.md` | Required (if present) |

---

## 6. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/cycles/<cycle_id>/sprint_goal.md` (create)
- `claude/cycles/<cycle_id>/sprint_backlog.md` (create)
- `claude/cycles/<cycle_id>/sprint_capacity.md` (create)
- `claude/cycles/<cycle_id>/sprint_planning_notes.md` (create — dependency map and sequencing rationale)
- `claude/cycles/<cycle_id>/sprint_escalations.md` (create if escalations raised during planning)
- `.claude_current_state.json` (status update only — STEP 7)

You must **not** modify:
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed)
- `claude/cycles/<cycle_id>/state.json` (owned by Release Planning engine)
- `claude/backlog/backlog.md` (no grooming during sprint planning)
- `claude/roadmap/current_roadmap.md`
- Any canonical spec, strategy, or governance document

Violation → halt.

---

## 7. Acceptance Criteria Standard (Hard Requirement)

Every item entering the sprint backlog must have acceptance criteria defined before the sprint may be sealed. Acceptance criteria must be structured as:

| Field | Requirement |
|-------|-------------|
| Technical | What must be built or changed — observable behaviour |
| Quality | What QA must verify — specific test scenarios |
| Security | Any security check required (may be "N/A — no security surface changed" if justified) |
| Verification | How the Director of Quality will confirm this item is done |

If any required field is absent:
- In `strict` mode: halt — the item cannot enter the sprint.
- In `standard` mode: flag the gap, add a placeholder marked `[AC REQUIRED]`, and record as an outstanding action. The sprint cannot be sealed until all `[AC REQUIRED]` placeholders are resolved.

**The sprint backlog may not be signed off while any item has an unresolved `[AC REQUIRED]` placeholder.**

---

## 8. Capacity Standard

Capacity is confirmed against:
- Available FTE from `sprint_capacity.md` (derived from `workforce_capacity.md` and `stage4_5_capacity_check.md`)
- Sprint duration (in working days)
- Skill requirements per EPIC and ST item

Over-allocation rule: the sprint scope must not exceed confirmed available capacity. If selection causes over-allocation:
- In `strict` mode: halt and require Product Owner to remove items.
- In `standard` mode: flag the over-allocation and surface to Product Owner for explicit acceptance. Record the decision. The sprint cannot be sealed until the Product Owner has explicitly accepted or resolved the over-allocation.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

Purpose: fail fast before any planning work begins.

### -1.1 Global State Check

Read `.claude_current_state.json`:
- `status` must be `Published`, `Validated`, or `Committed`
- If `status` is `Sprint_Planning_Complete` or later: a sprint has already been planned for this cycle. Halt — do not re-plan without explicit Product Owner instruction.
- If `status` is `Blocked`: resolve release planning escalations before planning the sprint.
- If `status` is anything else below `Committed`: Phase 1B has not completed. Halt.

### -1.2 Release Plan Sealed

Read `claude/cycles/<cycle_id>/state.json`:
- `status` must be `Published`
- `publish_eligible` must be `true`
- `open_escalations` must be empty
- If any of these fail: halt — the release plan is not sealed.

### -1.3 Backlog Slice Present

Confirm `claude/cycles/<cycle_id>/stage4_backlog_slice.md` exists and contains at least one EPIC with at least one ST item.

If absent or empty: halt.

### -1.4 Required Files Present

Verify all inputs in Section 5 exist. If any required file is missing: halt and report exactly which.

### -1.5 Required Authority Roles Exist

Verify agent files per Section 4. If any missing: halt.

### -1.6 Lessons Learnt Prompt Present

Confirm `claude/system/lessons_learnt_prompt.md` exists. If missing: halt.

### -1.7 Write Permission Test

Create a temporary marker file in `claude/cycles/<cycle_id>/` and confirm it can be written. Remove it. If write fails: halt.

---

## STEP 0 — Load Release Context

Extract from the backlog slice and execution plan:

1. From `stage4_backlog_slice.md`: all EPICs with their EPIC IDs, descriptions, and ST items. Note any items already marked as deferred or blocked.
2. From `stage3_execution_plan.md`: sequencing dependencies, risk IDs associated with EPICs, estimated effort per EPIC.
3. From `stage4_5_capacity_check.md`: confirmed available capacity (FTE, skills, duration). If the check result was `warn`: surface the warning to the user before proceeding.
4. From `cycle_summary.md`: the sprint goal candidate (if the release planning engine proposed one), any outstanding escalations deferred to execution.
5. From `workforce_capacity.md` (if present): skill availability constraints.

Produce a load summary confirming:
- Number of EPICs loaded
- Number of ST items loaded
- Confirmed capacity (FTE and duration)
- Any deferred execution blockers from the release plan escalations file

---

## STEP 1 — Capacity Baseline

Write: `claude/cycles/<cycle_id>/sprint_capacity.md`

### 1.1 Capacity Inputs

Derive from `stage4_5_capacity_check.md` and `workforce_capacity.md`:

```
Sprint duration:    <N working days>
Available FTE:      <N> (<role breakdown if known>)
Total capacity:     <FTE × days = capacity units>
Skill constraints:  <list any scarce or role-locked skills>
```

### 1.2 Item Effort Mapping

For each EPIC and its ST items, record the effort estimate from `stage3_execution_plan.md`. If an ST item has no effort estimate:
- In `strict` mode: halt — all items must have estimates.
- In `standard` mode: flag as `[ESTIMATE REQUIRED]` and record as an outstanding action. The sprint cannot be sealed until all estimates are present.

### 1.3 Total Effort vs Capacity

Calculate: total estimated effort across all candidate items vs confirmed capacity.

If total effort > capacity:
- Flag over-allocation with a breakdown by EPIC.
- This gap must be resolved in STEP 3 (scope selection).

Header block for `sprint_capacity.md`:
```
Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
Cycle: <cycle_id>
```

---

## STEP 2 — Sprint Goal Definition

Write: `claude/cycles/<cycle_id>/sprint_goal.md`

### 2.1 Goal Derivation

The sprint goal is a single sentence describing the primary outcome of this sprint. It must:
- Be owned and approved by the Product Owner
- Reference the release feature or roadmap item this sprint advances
- Be concrete enough that at sprint close, it is unambiguous whether it was achieved
- Not be a list of tasks — it is an outcome statement

If `cycle_summary.md` contains a proposed sprint goal from Phase 1B: surface it as a candidate. The Product Owner must explicitly confirm or replace it.

If no candidate exists: surface the release version and feature name and ask the Product Owner to define the goal before proceeding.

**The sprint goal is a hard gate.** Sprint planning may not proceed past STEP 2 without a confirmed sprint goal.

### 2.2 Sprint Goal Record Structure

```markdown
# Sprint Goal — <cycle_id>

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Cycle:** <cycle_id>

## Goal

<One sentence — sprint outcome statement>

## Release Context

- Release: <vX.Y>
- Feature: <feature name>
- Roadmap item: <item ID and name>

## Confirmed by

Product Owner: [AWAITING SIGN-OFF]
Date: <date>
```

`[AWAITING SIGN-OFF]` must be replaced with the Product Owner's explicit confirmation before the sprint backlog can be sealed.

---

## STEP 3 — Scope Selection

### 3.1 Candidate Item Review

For each EPIC and ST item from the backlog slice, review:
- Is this item within confirmed capacity?
- Does this item have an owner (from `stage3_execution_plan.md`)?
- Does this item have acceptance criteria defined, or will they be drafted in STEP 4?
- Is this item blocked by an unresolved dependency or escalation?

Classify each item:
- `include` — within capacity, owned, can be AC-confirmed
- `defer` — over-capacity or blocked; return to backlog slice for next sprint
- `flag` — has an issue that must be resolved before it can be included (missing owner, missing estimate, deferred execution blocker)

### 3.2 Capacity Gate

The selected `include` items must not exceed confirmed capacity.

If over-allocated after selection:
- Surface the gap to the Product Owner with a clear breakdown (which EPICs/items to remove to come within capacity).
- The Product Owner decides which items to defer. Record the decision.
- Do not proceed until either:
  - Scope is within capacity, or
  - The Product Owner has explicitly accepted the over-allocation with a recorded rationale (permitted in `standard` mode only).

### 3.3 Deferred Items

For each item classified `defer`:
- Record the reason (capacity, blocked dependency, missing prerequisite)
- Confirm it remains in `claude/backlog/backlog.md` with its current status (do not modify the backlog)
- Note it in `sprint_planning_notes.md` for carry-forward to the next sprint planning run

---

## STEP 4 — Acceptance Criteria Confirmation

For every `include` item, confirm acceptance criteria against the standard in Section 7.

### 4.1 Criteria Source

Acceptance criteria may come from:
- `stage4_backlog_slice.md` (if defined during release planning)
- `stage3_execution_plan.md` (if defined at EPIC level)
- Drafted during this step (if not yet defined)

### 4.2 Drafting Criteria

If acceptance criteria are not yet defined for an item, draft them now using the Section 7 structure. Surface the draft to the Head of Specs Team for confirmation before the item can be sealed.

The Head of Specs Team must confirm:
- Technical criteria are testable and observable
- Quality criteria name specific test scenarios (not "tested")
- Security criteria are explicitly stated or explicitly waived with justification
- Verification criteria are sufficient for the Director of Quality to sign off

### 4.3 Director of Quality Readiness Check

For each `include` EPIC, confirm with the Director of Quality that:
- The QA criteria are sufficient for them to produce `qa_evidence_EPIC-xx.md` at sprint close
- There are no known test coverage gaps that would block sign-off

If the Director of Quality flags a gap: record it as an outstanding action. In `strict` mode: the EPIC cannot enter the sprint until resolved.

---

## STEP 5 — Dependency Mapping and Sequencing

Write: `claude/cycles/<cycle_id>/sprint_planning_notes.md`

### 5.1 Dependency Identification

For each `include` EPIC and ST item:
- Identify cross-item dependencies (items that must complete before another can start)
- Identify external dependencies (delegated items, third-party blockers, infrastructure requirements)
- Identify spec dependencies (items that require a spec section to be locked before execution can begin)

### 5.2 Sequencing

Produce an execution order for EPICs and ST items that:
- Respects all identified dependencies
- Sequences spec-dependent items after their spec locks are confirmed
- Groups autonomous items before delegated items where possible (to unblock delegation early)
- Surfaces any circular dependencies as a blocking issue

If a circular dependency is detected: halt and surface to PMO Lead and Head of Specs Team.

### 5.3 Risk Flags

From `stage3_execution_plan.md` risk register: confirm which risk IDs are associated with `include` items. For each:
- Confirm the risk mitigation approach is still valid
- Flag any risk that has materialised since release planning (if known) as an escalation item

### Sprint Planning Notes Structure

```markdown
# Sprint Planning Notes — <cycle_id>

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Cycle:** <cycle_id>

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-xx | <reason> | Yes / No |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-xx | ST-yy | Internal | Resolved |

## Execution Sequence

<Ordered list of EPICs and ST items>

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-xx | EPIC-xx | Valid / Changed / Materialised |

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| <action> | <role> | Yes / No |
```

---

## STEP 6 — Sprint Backlog Production

Write: `claude/cycles/<cycle_id>/sprint_backlog.md`

### 6.1 Sprint Backlog Structure

```markdown
# Sprint Backlog — <cycle_id>

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Cycle:** <cycle_id>
**Release:** <vX.Y>
**Sprint Goal:** <goal from sprint_goal.md>

---

## Sprint Scope

### EPIC-xx — <Epic Title>

**Maps to:** S2-xx
**Owner:** <role from execution plan>
**Estimated effort:** <N capacity units>
**Risk IDs:** RISK-xx (if applicable)
**Execution sequence:** <N>

#### ST-xx — <Story Title>

**Owner:** <role>
**Estimated effort:** <N>
**Delegation class:** autonomous | delegated_backend | delegated_frontend | delegated_qa | delegated_decision

**Acceptance Criteria:**

| Dimension | Criteria |
|-----------|---------|
| Technical | <observable behaviour> |
| Quality | <specific test scenario> |
| Security | <check required> / N/A — <justification> |
| Verification | <how Director of Quality confirms done> |

**Dependencies:** ST-yy (must complete first) / None

**Notes:** <any flags, deferred execution blockers, or risks>

---

*(repeat for each ST item and EPIC)*

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | <N units> |
| Total estimated effort (in-scope) | <N units> |
| Utilisation | <N%> |
| Over-allocation | Yes (accepted by PO) / No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-xx | EPIC-xx | <reason> |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| <action> | <role> | Yes / No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** [AWAITING SIGN-OFF]
**Scope confirmed:** [AWAITING SIGN-OFF]
**Capacity confirmed:** [AWAITING SIGN-OFF]
**Signed off by:** Product Owner
**Date:** [AWAITING SIGN-OFF]
```

### 6.2 Sign-Off Gate (Hard Gate)

The sprint backlog is not sealed until:
- All `[AWAITING SIGN-OFF]` fields are replaced with explicit Product Owner confirmation and a date
- All `[AC REQUIRED]` placeholders are resolved
- All `[ESTIMATE REQUIRED]` placeholders are resolved
- No outstanding actions are marked `Blocker? Yes`
- Sprint goal confirmed in `sprint_goal.md`

If any of the above are unresolved: the sprint backlog status remains `Active` (not `Sealed`). Phase 3 may not be invoked.

Once all conditions are met:
- Update `sprint_backlog.md` status: `Active` → `Sealed`
- Update `sprint_goal.md` to reflect confirmed sign-off

---

## STEP 7 — Global State Update (Hard Requirement)

Update `.claude_current_state.json`:

```json
{
  "status": "Sprint_Planning_Complete",
  "sprint_goal_path": "claude/cycles/<cycle_id>/sprint_goal.md",
  "sprint_backlog_path": "claude/cycles/<cycle_id>/sprint_backlog.md",
  "sprint_capacity_path": "claude/cycles/<cycle_id>/sprint_capacity.md",
  "sprint_sealed": true,
  "last_sync_utc": "<ISO-8601 UTC>"
}
```

`sprint_sealed` must only be set to `true` when the sign-off gate in STEP 6.2 has passed. If the sign-off gate has not passed:
- Set `sprint_sealed: false`
- Set `status: "Sprint_Planning_In_Progress"`
- The engine is resumable — re-invoke `plan sprint` once outstanding items are resolved

---

## STEP 8 — Commit

Commit all artefacts created by this routine:

```
git add claude/cycles/<cycle_id>/sprint_goal.md
git add claude/cycles/<cycle_id>/sprint_backlog.md
git add claude/cycles/<cycle_id>/sprint_capacity.md
git add claude/cycles/<cycle_id>/sprint_planning_notes.md
git add claude/cycles/<cycle_id>/sprint_escalations.md   (if created)
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Sprint planning complete: <cycle_id>"
git push origin <current-branch>
```

If git operations are unavailable: output the exact files to stage and the commit message. Mark as "Ready to commit."

Commit may only proceed if `sprint_sealed = true`. If the sprint is not yet sealed, do not commit — the artefacts are still in progress.

---

## 9. Escalation

If a planning blocker arises that cannot be resolved by the PMO Lead within this routine (e.g. a capacity constraint requiring a workforce decision, an acceptance criteria gap requiring a Head of Specs Team ruling, a scope conflict requiring Product Owner arbitration):

- Create or append `claude/cycles/<cycle_id>/sprint_escalations.md`
- Use escalation format per `claude/system/shared_standards.md` §4
- Escalation ID format: `ESC-PLAN-YYYYMMDD-nn`
- Record the blocking statement, owning authority, unblock criteria, and SLA
- Set `.claude_current_state.json` status to `Sprint_Planning_Blocked`
- Halt

Re-invoke `plan sprint` once the blocking condition is resolved. The engine resumes from the first incomplete step.

---

## 10. Completion Condition

The run is complete only if:

- `sprint_goal.md` exists with confirmed Product Owner sign-off
- `sprint_backlog.md` exists with status `Sealed` and Product Owner sign-off
- `sprint_capacity.md` exists with capacity baseline
- `sprint_planning_notes.md` exists with dependency map and sequencing
- No outstanding actions marked `Blocker? Yes`
- No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders unresolved
- `.claude_current_state.json` status = `Sprint_Planning_Complete` and `sprint_sealed = true`
- STEP 8 commit complete (or commit manifest produced)

---

## 11. Resumability

On every invocation, the engine first checks:

1. Does `sprint_backlog.md` exist?
   - If yes and status is `Sealed`: sprint is already planned. Halt with confirmation message.
   - If yes and status is `Active`: resume from the first outstanding item (unresolved AC, missing sign-off, open blocker).
   - If no: fresh run, proceed from STEP -1.

2. Does `sprint_goal.md` exist?
   - If yes with sign-off: STEP 2 complete, skip.
   - If yes without sign-off: resume at STEP 2 sign-off gate.
   - If no: fresh run from STEP 2.

3. Does `sprint_capacity.md` exist?
   - If yes: STEP 1 complete, skip.
   - If no: run STEP 1.

Per `claude/system/shared_standards.md` §8 — never re-execute a step that already produced a valid output.

---

## 12. Governance Invariants

- **No scope changes.** The backlog slice is sealed. Sprint planning selects from it; it does not change it.
- **No AC-less items.** An item without confirmed acceptance criteria may not enter the sprint backlog.
- **No over-allocation without explicit Product Owner acceptance.** Capacity is a hard constraint unless explicitly overridden.
- **Product Owner sign-off is a hard gate.** The sprint backlog may not be sealed without it.
- **Dependencies must be resolved before sequencing is final.** Circular dependencies always halt.
- **Delegation classification is set at planning time.** Each ST item's delegation class is recorded in the sprint backlog so Phase 3 can load and act without re-classifying.
- **Delivery pressure never overrides these gates.** A sprint that skips sign-off is not a sprint — it is unplanned execution.