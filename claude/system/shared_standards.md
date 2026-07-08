**Owner:** Head of Specs Team
**Status:** Active
**Version:** 3.9
**Last Updated:** 2026-07-06

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

### SLA Breach Rule (IMP-40)

Any escalation open for 72 hours without resolution triggers a mandatory `BLOCKED_SLA_BREACH` notice. On the next invocation after the 72-hour threshold is crossed:

- The engine writes a `BLOCKED_SLA_BREACH` notice to the active cycle escalations file (same §5 halt report format, gate name: `SLA_BREACH`).
- The engine sets `blocked_sla_breached = true` in `.claude_current_state.json`.
- The engine halts — no step may proceed until the breach is resolved by the owning authority named in the escalation record.

The 72-hour clock applies regardless of escalation trigger type (overrides the type-specific SLA in the table above). The owning authority must either resolve the escalation or formally accept risk (where permitted) before the engine may resume.

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

### 7.1 Structural Append-Verification Procedure (canonical, reusable — BLG-GOV-168)

`claude/roadmap/decision_log.md` has a confirmed structural guard (`roadmap_prompt.md` STEP 9). The procedure below generalises that guard into a single reusable block. Every engine that appends to one of the four files in the table must apply this exact procedure at its write step — do not restate or paraphrase it inline; reference this section.

**Procedure:**
1. **Before write:** count existing entries in the target file (count occurrences of the file's entry-header pattern, e.g. via `grep -c '^## ESC-EXEC-'`).
2. **Perform the append.**
3. **After write:** re-count entries using the same pattern.
4. **Verify:**
   - New count = old count + 1 exactly (not zero — a silent no-op; not more than one — an unintended double-append).
   - No existing entry's text changed (diff the file's pre-write content against post-write, excluding the newly appended entry — confirm every prior line is byte-identical).
5. **If either check fails:** halt. Do not proceed past a failed structural verification. Report which check failed (count mismatch vs. altered prior entry) in the halt report.

**Applies to:**

| File | Entry header pattern | Owning engine |
|------|----------------------|----------------|
| `claude/cycles/<cycle_id>/escalations.md` | `^## ESC-` | `release_planning_prompt.md` |
| `claude/cycles/<cycle_id>/execution_escalations.md` | `^## ESC-EXEC-` | `execution_prompt.md` |
| `claude/cycles/<cycle_id>/verification_escalations.md` | `^## ESC-VERIF-` | `delivery_verification_prompt.md` |
| `claude/cycles/<cycle_id>/delegation_log.md` | `^## DEL-` | `execution_prompt.md` |
| `claude/roadmap/decision_log.md` | `^## DEC-` (or equivalent decision entry marker) | `roadmap_prompt.md` (existing guard — reference model for this procedure) |

Each owning engine's write step for its file(s) above must state: "Apply the Structural Append-Verification Procedure per `shared_standards.md §7.1`" at the point of append — not a re-description of the steps.

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
- `gh_issue_template.md` (Owner: Head of Specs Team, Class: 6)

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
| `run post-ship` | Closure plan — every step listed, every write that would be made, every flag. Note: STEP 11 (`manage roadmap`) and STEP 12 (`groom backlog`) also pass through `--dry-run`. |
| `manage roadmap` | Change plan — items to retire, items to flag |
| `groom backlog` | Change plan — items to archive, items to flag |
| `run design-gate` | Design gate preview — classification table, gap list, required design artefacts; no gate record, no state write, no commit |
| `run roadmap` | Rebalance preview — capacity analysis, displacement candidates, scoring matrix, backlog impact |
| `run ideas` | Submission window summary — counts per agent, ideas available for STEP 4 |
| `run ideas housekeeping` | Housekeeping preview — terminal rows to archive, rejected-but-strong revival candidates, pipeline health advisory; no ideas_register.md writes, no archive writes |
| `plan release --dry-run` | Scope extraction preview — roadmap item, tentative EPIC/ST structure, artefacts that would be created (release_plan.md, backlog_slice, design_gate.md if required); no artefact writes, no state updates |
| `run delivery verification --dry-run` | Verification plan — list of all STEP checks with their precondition sources; no verification_report.md written, no .claude_current_state.json update |
| `amend cycle --dry-run` | Amendment preview — proposed backlog slice delta, scope changes, authority ratification requirements; no state.json writes, no slice artefact created |
| `run audit` | N/A — `claude/audit.py` is read-only by design (produces a report + a PATCH manifest for Claude Code to apply separately); no `--dry-run` flag needed, no writes occur during the audit run itself |

**Scope of read operations:** Read operations (file reads, git queries, pip-audit scans) are always permitted in dry-run mode. A dry-run that cannot read required inputs should halt with a standard halt report, not silently produce an empty plan.

**Re-invocation after dry-run:** A dry-run does not advance lifecycle state. After reviewing the dry-run output, re-invoke without `--dry-run` to execute.

---

## 14. Preflight Field Scope (IMP-22)

To reduce repeated full-file reads of `.claude_current_state.json` across consecutive engine preflights, each engine must read only the field set listed below at preflight (STEP -1 / STEP 0), unless a specific later step explicitly requires an unlisted field.

**Section-scoped read rule:** "Engines must read only the fields specified in their `shared_preflight_fields` entry from `.claude_current_state.json`, not the full file, unless a field outside the set is explicitly required by a named step."

| Engine | Minimum preflight fields |
|--------|--------------------------|
| Release Planning (`plan release`) | `status`, `active_cycle`, `prior_cycle`, `post_ship_complete`, `next_cycle_unblocked` |
| Design Gate (`run design-gate`) | `status`, `active_cycle`, `design_gate_required` |
| Sprint Planning (`plan sprint`) | `status`, `active_cycle`, `design_gate_status`, `design_gate_bypass_authority`, `design_gate_bypass_reason`, `sprint_sealed` |
| Sprint Execution (`run sprint`) | `status`, `active_cycle`, `amended_backlog_slice_path`, `sprint_sealed`, `sprint_planning` |
| Delivery Verification (`run delivery verification`) | `status`, `active_cycle`, `amended_backlog_slice_path` |
| Post-Ship Closure (`run post-ship`) | `status`, `active_cycle`, `verification_status`, `next_cycle_unblocked` |
| Amendment Cycle (`amend cycle`) | `status`, `active_cycle`, `sprint_sealed` |
| Roadmap Rebalance (`run roadmap`) | `status`, `active_cycle` |

Fields not in this list may be read when a specific named step requires them. Full-file reads remain acceptable for engines with fewer than three tool calls budgeted for state loading.

---

## 15. Spec Debt Item Lifecycle (IMP-43)

**Spec debt items** (identified by prefix `BLG-SPEC-*`) represent deviations between what was built and the canonical spec, where the spec itself must be updated to reflect the agreed authoritative requirement.

### 15.1 Creation trigger

A spec debt item is created when:
- A deviation is noted during Phase 3 execution (STEP 5.3 in `execution_prompt.md`) or Phase 4 verification (STEP 3) AND
- The resolution requires a spec update (not just a backlog implementation item)

### 15.2 Required fields

Each `BLG-SPEC-*` entry in `backlog.md` must contain:

| Field | Description |
|-------|-------------|
| `BLG-SPEC-*` ID | Stable, unique, never renumbered |
| Affected spec file | Full path to the spec file that must be updated |
| Section | The specific section or table within the spec |
| Deviation description | What the implementation does vs. what the spec says |
| Canonical requirement | The authoritative requirement as it should read after correction |
| Priority | P0–P3 (same scale as deviation register) |
| Owner | Role responsible for the spec update |
| Target release | Release in which the spec update is expected |

### 15.3 Acceptance criteria for closure

A `BLG-SPEC-*` item is closed when:
1. The affected spec file has been updated to reflect the canonical requirement
2. The update has been reviewed by the Head of Specs Team
3. The Head of Specs Team has recorded sign-off (inline comment or PR review)

### 15.4 Closing authority

**Head of Specs Team sign-off is required** to mark a `BLG-SPEC-*` item as complete. No other role may close a spec debt item.

### 15.5 Validation rule (Phase 1M — Backlog Management)

The Backlog Management Engine (`groom backlog`) validates spec debt items against their `spec_update_status`:
- `open`: spec file not yet updated — item remains in backlog
- `in_progress`: spec file update in a live PR — flag for tracking
- `review_pending`: update merged but Head of Specs Team sign-off not yet recorded — flag
- `closed`: Head of Specs Team sign-off confirmed — mark item complete and archive

---

## 16. Governed JSON Schemas

Inline JSON schemas in engine prompts must be replaced with a reference to this section.
Format for reference: "Schema: per `shared_standards.md §16.N`"

### 16.1 sprint_backlog_index.json

Produced by: `sprint_planning_prompt.md` STEP 6.1A
Consumed by: `execution_prompt.md` STEP -1.1

```json
{
  "cycle_id": "<cycle_id>",
  "generated_utc": "<ISO-8601 UTC>",
  "epics": {
    "EPIC-xx": {
      "st_items": ["ST-xx", "ST-yy"],
      "backlog_slice_refs": ["stage4_backlog_slice.md#ST-xx", "stage4_backlog_slice.md#ST-yy"]
    }
  }
}
```

### 16.2 stage4_issue_manifest.json

Produced by: `release_planning_prompt.md` STEP 4 (IMP-24)
Consumed by: `sync gh` inline handler

```json
[
  {
    "id": "ST-xx",
    "title": "<story title>",
    "epic": "EPIC-xx",
    "description": "<one-line description from backlog slice>",
    "ac_summary": "<concise summary of acceptance criteria>",
    "labels": ["sprint", "EPIC-xx", "cycle:<cycle_id>"],
    "assignee": null
  }
]
```

One entry per ST item in `stage4_backlog_slice.md`. The `cycle:<cycle_id>` label is the idempotency key for GitHub issue creation (CLAUDE.md §4 / `sync gh` handler).

### 16.3 Delegation Log Schema

Produced by: `execution_prompt.md` — append on every delegated item
Consumed by: `execution_prompt.md` STEP 5.0 (outcome check), `post_ship_closure.md`

**Header (create on first write):**

```
Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
```

**Delegation Record Format** (`DEL-<YYYYMMDD>-<nn>`):

```
## DEL-<YYYYMMDD>-<nn>

- **ST Item:** ST-xx — <title>
- **EPIC:** EPIC-xx
- **Classification:** delegated_backend | delegated_frontend | delegated_qa | delegated_decision
- **Assigned to:** Head of Engineering | Base44 Frontend Prompt Owner | Director of Quality | <named role>
- **GitHub Issue:** #<number>
- **Branch:** exec/<cycle_id>/EPIC-xx
- **Delegated at:** <ISO-8601 UTC>
- **What is needed:** <specific, actionable description — not generic>
- **Spec reference:** <path to locked canonical spec that governs this item>  [backend/frontend items only]
- **Base44 prompt draft:** <attached or linked>  [delegated_frontend items only]
- **Unblock criteria:** <what must be true / what evidence is required>
- **Commit format required:** `[EPIC-xx][ST-xx] <description>` pushed to `exec/<cycle_id>/EPIC-xx`
- **Status:** Pending | In Progress | Unblocked | Cancelled
```

**Compliance rules:**
- "What is needed" must be specific enough that the assignee can act without further clarification. Vague delegations are non-compliant.
- For `delegated_backend`: "What is needed" must reference the specific layer(s) required (router / service / database) and the canonical spec section.
- For `delegated_frontend`: the Base44 prompt draft field is mandatory, covering all six required sections (context, change, API contract, behaviour rules, non-functional rules, expected outcome).

### 16.4 SLA Breach Tracking (Execution Engine)

On each re-invocation of the execution engine, check all open escalation timestamps against the current time. If any escalation has been open for **72 hours or more** without resolution, the SLA Breach Rule in `shared_standards.md §4` applies:

1. Write `BLOCKED_SLA_BREACH` notice to `execution_escalations.md` (same §5 halt report format, gate name: `SLA_BREACH`).
2. Set `blocked_sla_breached = true` in `.claude_current_state.json`.
3. Halt — no step may proceed until the breach is resolved by the owning authority.

Reference: `execution_prompt.md` STEP 3.1.D (delegated_decision items) and STEP 5.1 (Sprint_Complete state write).

### 16.5 ideas_register.md Schema

**File:** `claude/ideas/ideas_register.md`
**Produced by:** `idea_intake_prompt.md` STEP 2 (append row) and STEP 4 (update row status)
**Consumed by:** `roadmap_prompt.md` STEP 4 (idea classification and document management)

**File header (create on first write):**

```markdown
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** <date>
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Ideas Register
```

**Register table (append new rows; update existing rows in-place):**

| Idea ID | Title | Submitter | Window | Submitted At | Status | Park Count | Park Rationale | Step 4 | Step 5 |
|---------|-------|-----------|--------|--------------|--------|------------|----------------|--------|--------|

**Column definitions:**

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| Idea ID | string | Yes | Unique identifier: `IDEA-<agent-slug>-<YYYYMMDD>-<nn>` |
| Title | string | Yes | Short idea title |
| Submitter | string | Yes | Full role name of submitting agent |
| Window | string | Yes | Window ID (e.g. `IW-20260304-01`) |
| Submitted At | date | Yes | ISO date (YYYY-MM-DD) |
| Status | enum | Yes | One of: `Submitted`, `Advancing`, `Parked-cycle-<n>`, `Rejected`, `Promoted-Added`, `Promoted-Rejected`, `Withdrawn` |
| Park Count | integer | Conditional | Number of consecutive cycles parked; required when Status = `Parked-cycle-<n>`; `—` otherwise |
| Park Rationale | string | Conditional | PO one-line rationale; required on every park action; `—` if never parked |
| Step 4 | string | Conditional | Product Owner classification from most recent roadmap run; `—` if no roadmap run yet |
| Step 5 | string | Conditional | Debate outcome from most recent roadmap run; `—` if not advanced to debate |

**Compliance rules:**
- Rows are append-only for new ideas; never deleted
- Status field is the only column updated after initial row creation (except Park Count, Park Rationale, Step 4, Step 5 — updated on each roadmap run)
- A park action without a written Park Rationale is treated as Reject-not-strong by the roadmap engine
- `Status: Parked-cycle-<n>` where n ≥ 3 triggers stale idea surfacing in roadmap STEP 4.5

---

## §16.6 Backlog Item Provisional-Target Field

**Used by:** Roadmap Engine (write at STEP 9), Release Planning Engine (read at STEP 1.2)

### Field syntax

```
**Provisional-Target:** v<X.Y> | TBD | Unscheduled
```

### Horizon-to-release mapping rules

| Roadmap horizon | Provisional-Target value |
|-----------------|--------------------------|
| `Now` | Next planned release label in `current_roadmap.md` Now horizon (e.g. `v2.3`) |
| `Next` | Release label in the Next horizon of `current_roadmap.md` (e.g. `v2.4`) |
| `Later` | `Unscheduled` |
| Horizon tier has no release label | `TBD` |
| Horizon structure absent from roadmap | `TBD` |

**Rules:**
- The field must be present on every newly promoted item written to `backlog.md` at STEP 9.
- `TBD` is the explicit fallback when no release label can be resolved — the field is **never blank**.
- The field is a signal, not a commitment. Release planning may include or exclude items regardless of `Provisional-Target` value; deviation requires explicit PO rationale.

---

## §16.7 scored_initiatives.md Effort Band Column and Handoff Contract

**Used by:** Roadmap Engine (write at STEP 9), Release Planning Engine (read at STEP 0 / STEP 4.5)

### Effort band column

`claude/scoring/scored_initiatives.md` must carry an `Effort Band` column for all active roadmap initiatives:

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort Band |
|---|---|---|---|---|---|---|---|---|
| Initiative name | ... | ... | ... | ... | ... | ... | ... | S \| M \| L \| XS |

Effort band is assigned by the Roadmap Engine at promotion time.

### Three-tier resolution rule for STEP 4.5

| Tier | Condition | Action |
|------|-----------|--------|
| 1 | Row present in `scored_initiatives.md` AND `Effort Band` value present | Use effort band as primary sizing input; note "from scored_initiatives.md" |
| 2 | Row present BUT `Effort Band` cell empty or absent | Use STEP 4 estimate; emit advisory: "⚠ [N] EPIC(s) have no effort band in scored_initiatives.md — falling back to inline estimate." |
| 3 | No matching row in `scored_initiatives.md` | Use STEP 4 estimate; no advisory required |

### Handoff contract

- The Roadmap Engine writes; the Release Planning Engine reads. No other engine writes to this field.
- The Release Planning Engine must not modify `claude/scoring/scored_initiatives.md` — STEP 0 load is read-only.
- If `scored_initiatives.md` is absent from the filesystem: record "scored_initiatives.md: not present" in the STEP 0 load summary and proceed with STEP 4 estimates only.

---

## §16.8 lessons_learnt_closure.md Carry-Forward Section Schema

**Used by:** Post-Ship Closure Engine (write at STEP 8.5), Roadmap Engine / Release Planning Engine / Sprint Planning Engine (read at STEP 0)

### Section schema

```markdown
## Carry-Forward
Items: N

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | <one-sentence observation from this cycle> | <what the engine should do differently next cycle> | Roadmap \| Release Planning \| Sprint Planning \| All |
```

**Rules:**
- Absence of the `## Carry-Forward` section OR zero rows is valid — means no carry-forwards for this cycle.
- Maximum 5 items. Fewer is better — only include items with a clear, engine-actionable implication.
- Engine values: `Roadmap`, `Release Planning`, `Sprint Planning`, `All`.
- Items must be specific and actionable — not general observations.

### STEP 0 read protocol (for Roadmap, Release Planning, Sprint Planning engines)

1. Identify the most recently completed cycle: highest YYYY-MM-DD cycle ID where `post_ship_complete = true` in `.claude_current_state.json`.
2. Read `claude/cycles/<most_recent_cycle_id>/lessons_learnt_closure.md`.
3. If `## Carry-Forward` section is present and non-empty: surface each item as an advisory in session output; record in the run manifest as "Carry-forward items reviewed: N items from cycle `<cycle_id>`."
4. If section absent or has zero rows: record "No carry-forward items from prior cycle `<cycle_id>`" in run manifest and proceed.
5. Do not halt on absence. This step is advisory only.

---

## §16.9 ideas_window.json Schema

**Produced by:** idea_intake_prompt.md (STEP 2 — window open; STEP 10 — window close)
**Consumed by:** roadmap_prompt.md (STEP -1.6 trigger check)

Required fields:
```json
{
  "window_id": "IW-YYYYMMDD-nn",
  "opened_utc": "<ISO 8601>",
  "opened_by": "<role>",
  "status": "Open | Closed",
  "eligible_agents": ["<agent_slug>", ...],
  "submissions_received": ["<IDEA-ID>", ...],
  "per_agent_submission_count": { "<agent_slug>": <int>, ... },
  "closed_utc": "<ISO 8601 | null>",
  "closed_by": "<role | null>"
}
```
`per_agent_submission_count`: computed at STEP 3 by counting IDEA IDs in `submissions_received` containing each agent slug. Required field — must be present before window closes.

---

## 16.10 sprint_planning_notes.md Schema

**Produced by:** `sprint_planning_prompt.md` STEP 5
**Consumed by:** Sprint Execution Engine (STEP 0 advisory carry-forward read)

**Document title:** `# Sprint Planning Notes — <cycle_id>`

**Header block (required):**

```
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Cycle:** <cycle_id>
```

**Required sections:**

```markdown
## Backlog Slice Source

Original / Amended — <file path used>

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

## Pre-Sprint Vulnerability Scan

<pip-audit result: clean / findings listed / tool unavailable>

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| <action> | <role> | Yes / No |
```

**Optional sections** (include when applicable):
- `## Pre-Sprint Backlog Advisory` — unconverted "Before Sprint Planning" items (STEP -1 advisory 7)
- `## Carry-Forward Items` — from prior cycle STEP 0 advisory
- `## Capacity WARN Acknowledgement` — when capacity check outcome is `warn`

---

## 16.11 sprint_backlog.md Schema

**Produced by:** `sprint_planning_prompt.md` STEP 6
**Consumed by:** Sprint Execution Engine (STEP -1 / STEP 0 load), Post-Ship Closure Engine

**Document title:** `# Sprint Backlog — <cycle_id>`

**Header block (required):**

```
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active | Sealed
**Last Updated:** <date>
**Cycle:** <cycle_id>
**Release:** <vX.Y>
**Sprint Goal:** <goal from sprint_goal.md>
**Backlog Slice Source:** <original stage4_backlog_slice.md | amended: path>
```

**Structure:**

```markdown
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

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-xx`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** ST-yy (must complete first) / None

**Notes:** <any flags, deferred execution blockers, or risks>

**Staging-only ACs:** [REQUIRED] List each AC from `stage4_backlog_slice.md` that carries `[staging-only evidence]` or requires live external API calls, deploy hook verification, or staging-environment behaviour that CI cannot reproduce — e.g. "AC-02 (live API response behaviour)", "AC-05 (Telegram alert on staging)". Write `None` **only** when every AC for this story is verifiable in CI. This field is enforced at the sign-off gate: `None` when staging-only ACs exist is a seal blocker (OA-02, 2nd recurrence, v4.1 ST-02).

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

## Deferred Execution Blockers Accepted

| Blocker | Accepted by | Date |
|---------|-------------|------|
| <blocker description> | Product Owner | <date> |

*(omit section if deferred_execution_blockers was empty)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| <action> | <role> | Yes / No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** [AWAITING SIGN-OFF]
**Scope confirmed:** [AWAITING SIGN-OFF]
**Capacity confirmed:** [AWAITING SIGN-OFF]
**Deferred execution blockers accepted (if any):** [AWAITING SIGN-OFF / N/A]
**Signed off by:** Product Owner
**Date:** [AWAITING SIGN-OFF]
```

**Status transition:** `Active` → `Sealed` when sign-off gate (STEP 6.2) passes. `sprint_sealed = true` in `.claude_current_state.json` must be set concurrently. Phase 3 may not invoke while status is `Active`.

---

## 17. `.claude/skills/` Write Authority (BLG-GOV-167)

No governed engine's declared Write Scope (§7 pattern, `claude/system/shared/governance_preamble.md §Write-Scope`) includes `.claude/skills/`. Skill files (`.claude/skills/**/SKILL.md`) are process tooling that sits adjacent to, but outside, the five governed routines — they are invoked directly by the user or by Claude Code's skill dispatch, not by any of the phase engines.

This left a gap: a deferred patch to `.claude/skills/commit-check/SKILL.md` (adding a diff-verification step) carried unresolved across three consecutive cycles (v6.4 → v6.5 → v6.6) because no engine's write scope covered the file, and no explicit authority was named to action it outside a governed routine.

**Provision:** The **Head of Specs Team** holds standing write authority over `.claude/skills/**`, independent of any single engine's per-run Write Scope. This authority may be exercised:
- Directly, at any time, without opening a governed cycle — skill files are process tooling, not release-scoped artefacts.
- As part of a sprint story (e.g. an EPIC-02-style governance-hardening story), in which case the story's own Write Scope entry for `claude/system/`-class files extends to cover the specific `.claude/skills/` path named in the story's acceptance criteria.

**Compliance rule:** Any commit that edits a file under `.claude/skills/` must be authored or reviewed by the Head of Specs Team (directly, or via delegated sprint-story execution under this provision). No other role may modify `.claude/skills/` content.

This closes the 3-cycle carry-forward escalation `ESC-CLOSE-20260706-01`.

---

## Change Log

See: [`claude/system/changelogs/shared_standards_changelog.md`](changelogs/shared_standards_changelog.md)
