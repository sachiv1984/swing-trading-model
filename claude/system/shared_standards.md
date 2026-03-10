**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.7
**Last Updated:** 2026-03-10

# Shared Standards — All Governed Routines

This file defines standards that apply across all five governance prompts. Each prompt references this file rather than repeating these definitions. When a prompt says "per shared_standards", read this file.

---

## 1. Governance Stack (Precedence Order)

All governed routines operate under this binding stack:

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

No routine, user instruction, or delivery pressure may override the above.

---

## 2. Hard Gate Semantics

A **hard gate** is a condition that must be satisfied before execution may continue. When a hard gate fails:

1. Stop execution immediately
2. Output the halt report (§5 below)
3. Update state to `Blocked` before halting (do not halt without writing state)
4. Wait for user — do not attempt to self-resolve

A hard gate may only be cleared by the relevant domain authority. The Facilitator may not waive a hard gate.

---

## 3. Identifier Standards

| Type | Format | Required at |
|------|--------|-------------|
| Scope items | `S2-01`, `S2-02` | Stage 2 (Release Planning) |
| Epics | `EPIC-01`, `EPIC-02` | Stage 3 (Release Planning) |
| Stories | `ST-01`, `ST-02` | Sprint Backlog |
| Tasks | `TASK-01` | Sprint Backlog (optional) |
| Risks | `RISK-01`, `RISK-02` | Stage 3 (Release Planning) |
| Escalations (Release Planning) | `ESC-YYYYMMDD-nn` | Escalations file |
| Escalations (Sprint Execution) | `ESC-EXEC-YYYYMMDD-nn` | Execution escalations file |
| Escalations (Delivery Verification) | `ESC-VERIF-YYYYMMDD-nn` | Verification escalations file |
| Escalations (Post-Ship Closure) | `ESC-CLOSE-YYYYMMDD-nn` | Closure record |
| Delegation records | `DEL-YYYYMMDD-nn` | Delegation log |

IDs must be stable — never renumber existing IDs. Missing IDs on required fields is a Process Integrity failure that halts execution.

---

## 4. Escalation Record Format

Used in:
- `claude/cycles/<cycle_id>/escalations.md` (Release Planning)
- `claude/cycles/<cycle_id>/execution_escalations.md` (Sprint Execution)
- `claude/cycles/<cycle_id>/verification_escalations.md` (Delivery Verification)
- `claude/cycles/<cycle_id>/closure_escalations.md` (Post-Ship Closure)

These files are **append-only**. Never edit a previous entry.

### Header (create on first write)

```
Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
```

### Entry format

```
## <ESC-ID>

- **Raised at:** <ISO-8601 UTC>
- **Routine:** <Roadmap Rebalance | Release Planning | Sprint Execution | Delivery Verification | Post-Ship Closure>
- **Cycle ID:** <cycle_id>
- **Step:** <step number or name>
- **ST/EPIC item:** <if applicable>
- **Trigger type:** Lifecycle | Strategy | Quality | Workforce | GitHub | Human-Delegation | Other
- **Blocking statement:** <one paragraph, precise and factual>
- **Owning authority:** <role>
- **Unblock criteria:** <what must be true to resume>
- **SLA due-by:** <date/time>
- **Blocks execution:** Yes | No
- **Disposition:** Open | Resolved | Accepted Risk | Deferred
- **Resolution summary:** <complete when closing; include evidence links>
```

### Escalation SLAs

| Trigger Type | SLA | Can Be Accepted Risk? |
|-------------|-----|-----------------------|
| Lifecycle / Process Integrity | 24 hours | **Never** |
| Strategy boundary | 72 hours | **Never** |
| Quality | Before execution | **Never** |
| Workforce / Capacity | Next planning checkpoint | Yes — Product Owner only |
| Schedule / Delivery | Next planning checkpoint | Yes — Product Owner only |

Strategy, Quality, and Lifecycle escalations may never be marked Accepted Risk. Attempting to do so is a governance violation requiring a routine halt.

---

## 5. Standard Halt Report Format

When a hard gate fires or a blocking condition is encountered, output exactly this structure:

```
🛑 HALT — <Gate Name>

Routine:     <Roadmap Rebalance | Release Planning | Sprint Execution | Delivery Verification | Post-Ship Closure>
Cycle:       <cycle_id>
Step:        <step number>
Gate:        <gate name>

What failed:
  <specific condition that failed — one sentence per failed item>

Evidence found:
  <what was checked and what was found — be specific, not generic>

Evidence missing:
  <what would be needed to pass this gate>

State written:
  <confirm state file updated to Blocked, or explain why not>

To resume:
  <exact command to re-invoke once the condition is resolved>
  e.g.: run sprint --cycle "2026-03-02__release-v1.7"
```

Do not halt with a terse message. Always output the full halt report so the user knows exactly what is needed.

---

## 6. GitHub CLI Commands (Standard Operations)

Use `gh` CLI for all GitHub operations. Do not use the GitHub API directly.

### Issue operations

```bash
# Create issue (body content per claude/system/gh_issue_template.md)
gh issue create \
  --title "[ST-xx] <title>" \
  --body "<populated gh_issue_template.md>" \
  --label "sprint" --label "EPIC-xx"

# Update issue to in-progress
gh issue edit <number> --add-label "in-progress"

# View issue (to check if it exists)
gh issue list --search "[ST-xx]" --json number,title,state
```

**Issue body format:** Use `claude/system/gh_issue_template.md` as the body template. Variable mapping:
- `{{ID}}` → EPIC-xx (the parent epic)
- `{{ST_ID}}` → ST-xx (the story)
- `{{TITLE}}` → story title from `sprint_backlog.md`
- `{{CYCLE_ID}}` → active cycle_id from `.claude_current_state.json`
- `{{PARENT_EPIC}}` → EPIC-xx
- `{{OBJECTIVE_TEXT}}`, `{{AC_1}}` etc. → from acceptance criteria in `sprint_backlog.md`

**Do not manually close issues** that will be closed by `governance_sync.yml` on push. Issues are auto-closed by CI when a commit with `[EPIC-xx][ST-xx]` format is pushed to an `exec/**` branch.

### PR operations

```bash
# Create PR
gh pr create \
  --title "[EPIC-xx] <epic description>" \
  --body "<body per prompt spec>" \
  --base main \
  --head exec/<cycle_id>/EPIC-xx

# Check PR status
gh pr view <number> --json state,reviews,statusCheckRollup

# List open PRs for this cycle
gh pr list --search "exec/<cycle_id>" --json number,title,state
```

### Branch operations

```bash
# Create EPIC branch from main
git checkout main && git pull
git checkout -b exec/<cycle_id>/EPIC-xx
git push -u origin exec/<cycle_id>/EPIC-xx

# Check if branch exists remotely
git ls-remote --heads origin exec/<cycle_id>/EPIC-xx
```

---

## 7. Append-Only File Rule

The following files are append-only within their cycle. Never edit a previous entry:

- `claude/cycles/<cycle_id>/escalations.md`
- `claude/cycles/<cycle_id>/execution_escalations.md`
- `claude/cycles/<cycle_id>/verification_escalations.md`
- `claude/cycles/<cycle_id>/delegation_log.md`
- `claude/roadmap/decision_log.md`

If a correction is needed to a previous entry, append a correction note referencing the original entry ID. Do not overwrite.

---

## 8. Resumability Protocol

Every governed routine is resumable. On every invocation:

1. **First action:** Read the relevant state file (`state.json`, `execution_state.json`, or `.claude_current_state.json` for post-ship)
2. If the file exists and status is not `not_started` or `Initialized`: you are resuming
3. Skip all completed steps (any step whose output artefact exists and is valid)
4. Re-evaluate all `blocked_*` items: check whether their unblock criteria are now met
5. Resume from the first incomplete or newly unblocked item
6. Never re-execute a step that already produced a valid output

If the state file does not exist: this is a fresh run. Proceed from STEP -1.

**Post-Ship Closure resumability:** The closure engine maintains `claude/cycles/<cycle_id>/closure_state.json`. On re-invocation, STEP 0 reads this file: if `status = Closed`, the cycle is already closed (halt); if `status = In_Progress`, resume from the first step with value `not_started` or `fail`; if the file does not exist, this is a fresh run. This follows the same resumability model as the execution and release planning engines.

---

## 9. Lifecycle Compliance Quick Reference

Every governed artefact must have a complete header. Minimum required fields by class:

| Class | Required Fields |
|-------|----------------|
| Class 1 (Canonical) | Owner, Status: Canonical, Version, Last Updated |
| Class 3 (Operational Record) | Owner, Status: Operational Record, Report Date, Filed |
| Class 4 (Planning Document) | Owner, Class: Planning Document (Class 4), Status, Last Updated |
| Class 6 (Governance Prompt) | Owner, Status: Active, Version, Last Updated |

A document without a complete header is non-compliant and must not be relied upon. Non-compliant documents discovered during a routine: apply header remediation (headers only) and continue.

---

## 10. Lifecycle Validation Rules (Lifecycle Guard)

All engines that write `.claude_current_state.json` status must apply this guard on every invocation, before executing any step.

### 10.1 Allowed Entry States

| Engine | Command | Valid from-states | Additional preconditions |
|--------|---------|-------------------|--------------------------|
| Release Planning | `plan release` | `Closed` | `post_ship_complete = true` **and** `next_cycle_unblocked = true` must be present in `.claude_current_state.json` (checked at STEP -1.6) |
| Design Gate | `run design-gate` | `Release_Planning_Complete` | — |
| Sprint Planning | `plan sprint` | `Release_Planning_Complete` (design N/A), `Design_Gate_Passed` | When entering from `Release_Planning_Complete`: `design_gate_bypass_authority` + `design_gate_bypass_reason` required in state (STEP -1.3) |
| Sprint Execution | `run sprint` | `Sprint_Planning_Complete`, `Executing` (resume), `Closed` (multi-sprint only: `sprint_planning.sprint2_deferred` non-empty AND `sprint_sealed = true` AND `post_ship_complete = true`) | Multi-sprint exception: `Closed` is valid only when the same `cycle_id` is being continued across sprints (Sprint N closed, Sprint N+1 resuming). See `lifecycle_schema.json` for full entry condition. |
| Delivery Verification | `run delivery verification` | `Sprint_Complete` | — |
| Post-Ship Closure | `run post-ship` | `Verified`, `Verified_with_deviations` | — |
| Amendment Cycle | `amend cycle` | `Sprint_Planning_Complete` (before sprint_sealed = true) | Acquire backlog lock before reading `sprint_sealed` (STEP -1.1) |

### 10.2 Guard Algorithm

On engine invocation:

1. Read `.claude_current_state.json` → record `current_status`
2. Check `current_status` against the engine's valid from-states (table above)
3. **If `current_status = Blocked`:** read `prior_status`. If `prior_status` is a valid from-state for this engine, proceed as if status = `prior_status`. Otherwise, halt — the block is in the wrong phase for this engine.
4. **If `current_status` is not in valid from-states and is not `Blocked`:** halt immediately with a Lifecycle hard gate (§2 + §5 format). Write `status = Blocked` and `prior_status = <current_status>` to `.claude_current_state.json` before emitting the halt report.
5. **If valid:** continue to engine steps.

### 10.3 State Write Rules

- An engine may only write a state value that is in its allowed `to` transitions (see `lifecycle_schema.json`).
- Write `status` only at the defined completion signal step. Do not set an in-progress state at an earlier step unless the transition explicitly defines an intermediate state (e.g., `Executing` is a valid in-progress write for Sprint Execution).
- Before writing `status`, confirm the value in `.claude_current_state.json` has not changed since step 1. If it has changed (concurrent write), halt with `ESC-YYYYMMDD-nn` (Lifecycle trigger) without overwriting.

### 10.4 Blocked State Protocol

When any hard gate fires during execution:

1. Set `prior_status` = current `status` value in `.claude_current_state.json`
2. Set `status` = `Blocked`
3. Write `.claude_current_state.json` — this write must complete before the halt report is emitted
4. Emit halt report (§5 format); include "State written: status = Blocked, prior_status = <value>"
5. Wait for user — do not self-resolve

To clear `Blocked`: the domain authority identified in the escalation record must resolve the block. On resolution, restore `status` from `prior_status` and clear `prior_status` to `null`.

### 10.5 Phase Skip Rule

Forward-only movement is enforced by the entry state check (§10.2). An engine that cannot pass the entry check must not execute, regardless of delivery pressure. No timeline instruction or user override may waive a Lifecycle hard gate.

### 10.6 Full State Machine Reference

`claude/system/lifecycle_schema.json` is the **machine-readable source of truth** for all valid states and transitions. The table in §10.1 is a human-readable summary; in any conflict, `lifecycle_schema.json` prevails. Every engine must read `lifecycle_schema.json` to validate transitions rather than relying solely on the §10.1 table. The schema includes: all valid states, all transitions with entry conditions and completion signals, and concurrent-write prevention rules.

---

## 11. Prompt Version Control (IMP-10)

Any increment to a governance prompt version **must** be accompanied by an entry in `claude/system/prompt_change_log.md` in the same commit.

**Rule:** A prompt whose version number is not recorded in `prompt_change_log.md` is considered non-compliant. During Release Planning STEP -1 (advisory check), the engine verifies that each governed prompt's current version appears in the change log.

**Scope:** Applies to all Class 6 Governance Prompts in `claude/system/`:

- `release_planning_prompt.md`
- `sprint_planning_prompt.md`
- `execution_prompt.md`
- `delivery_verification_prompt.md`
- `post_ship_closure.md`
- `design_gate_prompt.md`
- `amendment_cycle_prompt.md`
- `roadmap_management_prompt.md`
- `backlog_management_prompt.md`
- `roadmap_prompt.md`

**Simultaneity rule:** A `prompt_change_log.md` entry must be created in the **same commit** as the prompt version increment it records. An entry created after the fact (in a separate commit) is non-compliant. When applying prompt patches, stage both the modified prompt file and the updated `prompt_change_log.md` in the same `git add` + `git commit` sequence.

**Enforcement:** STEP -1 of Release Planning (advisory, not hard gate) verifies the current version of each prompt appears in `prompt_change_log.md`. Missing entries are flagged as advisory warnings; the release planning engine may proceed but must record the gap as an outstanding action.

---

---

## 12. Parallel EPIC Branch Merge Sequencing

When multiple EPIC branches are active simultaneously in the same sprint, `execution_state.json` merge conflicts are structurally inevitable — both branches modify the same governance file independently. Apply the following convention to prevent cascading conflict rounds.

**Rule 1 — Merge sequence:** When multiple EPIC branches are ready for merge, merge them in dependency order (logical dependencies first; alphabetical by EPIC ID if no dependencies exist). Do not merge multiple EPIC branches to main simultaneously.

**Rule 2 — Conflict resolution rule:** On a merge conflict in `execution_state.json`, keep the version from the more recently-merged EPIC branch (the EPIC with the later completion timestamp). The earlier EPIC's state additions are preserved in its QA evidence file and `sprint_close.md` and do not need to be in the merged state file.

**Rule 3 — GOVERNANCE commit after each merge:** After each EPIC branch merges to main, update `execution_state.json` on main directly via a GOVERNANCE commit before the next EPIC branch opens a PR. This prevents the next EPIC's PR from showing a conflict on `execution_state.json` at open time.

**Why this matters:** Without this convention, a 4-EPIC sprint with parallel branches requires 3 conflict resolution rounds, each triggering a CI re-run (~3–5 minutes each). Cumulative latency: 30–60 minutes per sprint close. With this convention, conflict rounds are eliminated.

*Trigger: Friction Item 1, lessons_learnt_execution.md — cycle 2026-03-06__release-v1.9 Sprint 1. Confirmed by Head of Specs Team.*

---

## 13. Dry-Run Standard

The following engines support `--dry-run`. The guarantee is identical in all cases:

**Dry-run guarantee:** No writes to any file. No state updates to `.claude_current_state.json`. No git commits. No GitHub operations (issues, PRs, branch creation). The output is a plan or preview only.

| Engine | `--dry-run` produces |
|--------|---------------------|
| `plan sprint` | Sprint planning preview — capacity, scope, AC gaps, sequencing, pip-audit result |
| `run sprint` | Dry-run execution report — item classification, delegation targets, spec references, anticipated blockers |
| `run post-ship` | Closure plan — every step listed, every write that would be made, every flag |
| `manage roadmap` | Change plan — items to retire, items to flag |
| `groom backlog` | Change plan — items to archive, items to flag |

**Scope of read operations:** Read operations (file reads, git queries, pip-audit scans) are always permitted in dry-run mode. A dry-run that cannot read required inputs should halt with a standard halt report, not silently produce an empty plan.

**Re-invocation after dry-run:** A dry-run does not advance lifecycle state. After reviewing the dry-run output, re-invoke without `--dry-run` to execute.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.7 | 2026-03-10 | IMP-45: §13 Dry-Run Standard added — defines guarantee, engine coverage table, read-operation scope, and re-invocation note. IMP-50: §4 Post-Ship Closure escalation target updated from `closure_record.md §6` to `closure_escalations.md`. IMP-58: §11 Prompt Version Control — simultaneity rule added (prompt_change_log.md entry must be in the same commit as the version increment). IMP-61: §10.6 Full State Machine Reference — strengthened: `lifecycle_schema.json` declared as machine-readable source of truth that prevails over §10.1 table in any conflict. |
| 1.6 | 2026-03-10 | §10.1 Sprint Execution row updated — added `Closed` (multi-sprint exception) as valid from-state when `sprint_planning.sprint2_deferred` non-empty and `sprint_sealed = true` and `post_ship_complete = true`. Formalises the Sprint N+1 re-entry path for multi-sprint cycles. Triggered by closure_record §6 Action #2, 2026-03-06__release-v1.9. |
| 1.5 | 2026-03-09 | §12 added — Parallel EPIC Branch Merge Sequencing: merge ordering convention (dependency order), conflict resolution rule (keep more recent EPIC's version), GOVERNANCE commit after each merge. Triggered by Friction Item 1 in `claude/cycles/2026-03-06__release-v1.9/lessons_learnt_execution.md`. Immediate action — Head of Specs Team confirmed. |
| 1.4 | 2026-03-08 | IMP-04: §10.1 updated — Release Planning row adds `post_ship_complete` + `next_cycle_unblocked` preconditions; Sprint Planning row adds design gate bypass audit requirement; Amendment Cycle row adds backlog lock precondition. IMP-06: Release Planning precondition added. IMP-10: §11 Prompt Version Control added. |
| 1.3 | 2026-03-07 | Updated §8 Post-Ship Closure resumability note — replaced `closure_record.md` prose-scan approach with `closure_state.json` structured file (IMP-01). |
| 1.2 | 2026-03-07 | Added §10 Lifecycle Validation Rules — transition guard algorithm, entry state table, blocked state protocol, phase skip rule, schema reference. |
| 1.1 | 2026-03-03 | Updated "three governance prompts" to "five". Added `ESC-VERIF-YYYYMMDD-nn` and `ESC-CLOSE-YYYYMMDD-nn` to identifier standards. Added Delivery Verification and Post-Ship Closure to escalation file list, escalation entry routine field, and halt report routine field. Added `verification_escalations.md` to append-only file list. Added Post-Ship Closure resumability note to §8. |
| 1.0 | 2026-03-02 | Initial version. |