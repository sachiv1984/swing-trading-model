**Owner:** Head of Specs Team
**Status:** Active
**Version:** 2.0
**Last Updated:** 2026-03-02
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Claude Governance Prompt — Release Planning Engine (Cycle-Based, Reusable, Escalation-Aware, State-Driven, Mutation-Safe)

## Purpose
Translate an already-approved roadmap release (e.g., v1.7, v1.8) into an execution-ready plan:
- Sequencing, dependencies, acceptance gates, verification approach
- A release backlog slice (without reprioritising the global backlog)
- Optional GitHub issue plan (or issue import text)

This routine is **NOT** a roadmap rebalance. It may **NOT** add/replace/defer/kill initiatives or alter strategy boundaries. Those remain reserved for the Roadmap Rebalance Engine.

---

## Delegated Authority Model (User Delegation)
The user delegates operational decision-making to the defined role agents. During this routine:
- Each authority role may decide within its chartered domain.
- Domain blocks remain binding (Quality and Strategy blocks cannot be overridden by Product Owner).
- If an escalation requires information that is not present in-repo and cannot be inferred safely, the routine must record the escalation and halt.

Non-decision roles (Facilitator, Challenger) have no decision authority. They enforce process and demand clarity only.

---

## Invocation Rule (Hard Gate)
This routine executes ONLY when the user issues the explicit command:

plan release --version "<vX.Y>" [--date "YYYY-MM-DD"] [--timebox "<text>"] [--capacity "<text>"] [--mode "<strict|standard>"] [--issues "<none|import|gh>"] [--auto-escalate "<true|false>"]

Rules:
- Invocation must start with `plan release` (case-insensitive allowed).
- `--version` is required and must match a planned release label in `claude/roadmap/current_roadmap.md` (e.g., `v1.7`).
- `--date` optional (defaults to today, YYYY-MM-DD).
- `--timebox` optional (e.g., "1 week", "2 weeks", "1 sprint").
- `--capacity` optional (e.g., "solo-dev evenings", "full-time", "part-time").
- `--mode` optional:
  - `strict`: halt on any missing prerequisite, unclear scope, or failed hard gate
  - `standard`: proceed with explicit assumptions and flags where allowed, but still halt on hard gates
- `--issues` optional:
  - `none`: do not generate issue artifacts
  - `import`: create `issue_import.md` only
  - `gh`: attempt to create GitHub issues via `gh` CLI; if unavailable, fall back to `import`
- `--auto-escalate` optional:
  - `true` (default): system creates, routes, and attempts to resolve escalations using delegated authority
  - `false`: system records blockers only and halts without attempting resolution

If invocation is not exact, do not run. Treat as conversational.

---

## Canonical Governance Sources (Non-Negotiable)
Binding governance stack:
- claude/charter/team_charter.md (role authority, conflict rules, escalation + accepted risk constraints)
- claude/charter/document_lifecycle_guide.md (lifecycle rules)
- claude/strategy/strategy_rules.md (system intent, boundaries)

This routine may not override any of the above.

---

## Source-of-Truth Planning Inputs
Authoritative planning inputs:
- claude/roadmap/current_roadmap.md
- claude/backlog/backlog.md
- docs/specs/* (canonical specs as needed for readiness checks)
- docs/reference/openapi.yaml (supporting reference; align when needed)

---

## Agent Integrity (Required Roles)
Minimum required roles for this routine:
- Product Owner
- Head of Specs Team
- PMO Lead
- Director of Quality
- Infrastructure & Operations Owner
- Strategy Rules & System Intent Owner
- FinOps & Resource Architect
- Facilitator
- Challenger

If any required role is missing or malformed (agent file absent or missing the required `**Role:** <Role Name>` line), halt.

---

## Write Scope Restriction (Hard Gate)
During this routine you may write only to:
- claude/cycles/<cycle_id>/*
- claude/backlog/backlog.md  (release slice only; no global reprioritisation)
- claude/roadmap/current_roadmap.md (ONLY to add execution notes/links under the existing release section; no scope change)
- docs/product/decisions/* (ONLY when required to resolve an escalation under the rules below; must be lifecycle-compliant)
- claude/scoring/* (only if explicitly requested by Product Owner for sequencing support)

You must not modify:
- source code
- claude/strategy/strategy_rules.md
- claude/roadmap/initiative_register.md
- claude/roadmap/decision_log.md (reserved for irreversible roadmap decisions in rebalance)
- any doc outside allowed scope

Violation → halt.

---

## Identifier Standards (Hard Requirement)
To enable deterministic cross-stage integrity checks, all stage artefacts MUST use stable IDs.

### ID Formats
- Stage 2 scope items: `S2-01`, `S2-02`, ...
- Stage 3 epics: `EPIC-01`, `EPIC-02`, ...
- Stage 3 stories/tasks (optional but recommended): `ST-01`, `TASK-01`, ...
- Risks: `RISK-01`, `RISK-02`, ...
- Escalations: `ESC-YYYYMMDD-nn`

### Mapping Rules
- Every Stage 2 scope item MUST have an `S2-xx` ID.
- Every Stage 3 epic MUST have an `EPIC-xx` ID and MUST declare:
  - `Maps to: S2-xx, S2-yy`
- Every risk MUST have an ID and MUST declare:
  - `Relates to: EPIC-xx` OR `Release-level`
- Stage 4 backlog slice MUST reference EPIC IDs exactly (no free-text epics).

If IDs are missing, treat as a **Process Integrity** failure:
- Record a ⛔ Blocker
- If `--auto-escalate=true`, invoke the Escalation Handling Subroutine
- Halt if not remediable in-place without changing scope

---

## Cycle Folder + State (Required)
Define:
- date = `--date` or today (YYYY-MM-DD)
- release = `--version` (e.g., v1.7)
- cycle_id = `{date}__release-{release}` (example: `2026-03-02__release-v1.7`)

Create:
- `claude/cycles/<cycle_id>/`

State file (required):
- `claude/cycles/<cycle_id>/state.json`

The routine is **state-driven**:
- If `state.json` exists, resume from the recorded state.
- If the cycle folder exists but `state.json` is missing, rebuild state from artefacts present, write `state.json`, then continue.
- Steps MUST update `state.json` at completion.

---

# State Machine Model (Reduced Macro-States)

## Canonical macro-states
- `Initialized`  — run manifest + state created
- `Planning`     — plan being constructed and internally executable
- `Committed`    — backlog slice committed (release slice written)
- `Validated`    — feasibility + integrity + decisions validated + publish gate eligible
- `Published`    — summary + lessons filed and publish gate passed
- `Blocked`      — one or more Open escalations exist, or publish gate cannot pass

## State semantics (no overlap)
- **Planning** means “Stage 3 exists and Stage 3.5 passed.”
- **Committed** means “Stage 4 passed.”
- **Validated** means “Stage 4.5 + Stage 5.5 + Stage 5.7 (if triggered) passed AND Publish Gate eligible.”
- **Published** means “Cycle summary + lessons exist AND publish gate passed.”

All detailed checks remain in artifacts + attributes; macro-states are phase markers.

---

# Mandatory End-to-End Process (Single Run)

## Gate Semantics (Definitions)
**Hard Gate:** Any FAIL halts immediately (no continuation).
**Conditional Gate:** FAIL may be remediated or escalated; the run halts only if the resulting escalation remains Open or blocks publishing/execution.
**Advisory Check:** WARN-only; never creates blockers; never escalates; never halts.

### Global Rule — Blockers Must Route
If any step produces one or more ⛔ Blockers:
- If `--auto-escalate=true`: invoke the **ESCALATION HANDLING SUBROUTINE** immediately after that step.
- If `--auto-escalate=false`: record blockers in the step output and **HALT**.

### Global Rule — State Must Be Updated
At the end of every step:
- Update `state.json` with:
  - macro status
  - artifact statuses
  - open escalations (IDs)
  - last transition timestamp (UTC)
If state cannot be updated: halt.

---

## STEP -1 — Preflight Gate (Hard Gate)
Purpose: fail fast on missing prerequisites.

### -1.1 Required Files Present
Verify these exist:
- claude/charter/team_charter.md
- claude/charter/document_lifecycle_guide.md
- claude/strategy/strategy_rules.md
- claude/roadmap/current_roadmap.md
- claude/backlog/backlog.md
If any are missing: halt and report exactly which.

### -1.2 Verify Release Exists on the Roadmap
Open `claude/roadmap/current_roadmap.md` and confirm the requested `--version` exists as a planned release section.
- If not found: halt (this routine cannot invent new releases).

### -1.3 Required Authority Roles Exist (Agent Integrity)
Verify agent files exist under `claude/agents/` for the minimum required roles listed above and contain the correct `**Role:**` line.
If any missing/malformed: halt.

### -1.4 Write Permission Test (Non-Destructive)
Create a temporary marker file under `claude/cycles/<cycle_id>/` and confirm it can be written.
Remove it if possible; if not, keep it and record it in the run manifest.

---

## STEP 0 — Create Run Manifest + Initialize State (Hard Requirement; must be first write)
Create:
- `claude/cycles/<cycle_id>/run_manifest.md`

Class: Operational Record (Class 3)
Owner: Infrastructure & Operations Owner
Status: Filed

Header (required fields):
Owner: Infrastructure & Operations Documentation Owner
Status: Operational Record
Deployment Version: N/A
Report Date: <date>
Environment: Governance
Generated By: Claude Code (Release Planning Engine)
Filed: <date filed>

Then create or update:
- `claude/cycles/<cycle_id>/state.json`

State.json schema (minimum required keys):
```json
{
  "cycle_id": "<cycle_id>",
  "release": "<vX.Y>",
  "date": "YYYY-MM-DD",
  "mode": "strict|standard",
  "issues_mode": "none|import|gh",
  "auto_escalate": true,

  "status": "Initialized",
  "publish_eligible": false,
  "last_transition_utc": "<ISO-8601 UTC>",

  "mutation_seq": 0,
  "assumptions": {
    "timebox": "<text or empty>",
    "capacity": "<text or empty>"
  },

  "artifact_fingerprints": {
    "stage2_scope_extraction": "<fingerprint or empty>",
    "stage3_execution_plan": "<fingerprint or empty>",
    "stage4_backlog_slice": "<fingerprint or empty>",
    "escalations": "<fingerprint or empty>"
  },


   "locks": {
      "backlog_lock": {
        "required": true,
        "lock_file": "claude/backlog/.lock",
        "owned": false,
        "owner_cycle_id": "",
        "owner_release": "",
        "acquired_utc": "",
        "status": "not_checked|acquired|blocked|released|stale_detected"
      }
    },

  "mutations": [],
  "invalidated_steps": [],

  "open_escalations": [],
  "deferred_escalations": [],
  "deferred_execution_blockers": [],
  "accepted_risk_escalations": [],

  "attributes": {
    "plan_structured": false,
    "plan_executable": false,
    "backlog_committed": false,
    "capacity_feasible": "not_started|pass|warn|fail|blocked",
    "cross_stage_integrity": "not_started|pass|fail|blocked",
    "decisions_validated": "not_started|pass|fail|not_applicable|blocked"
  },

  "artifacts": {
    "run_manifest": "present|missing",
    "backlog_lock": "not_checked|acquired|blocked|released|stale_detected",
    "stage1_readiness": "not_started|pass|fail|blocked",
    "stage2_scope_extraction": "not_started|pass|fail|blocked",
    "stage3_execution_plan": "not_started|pass|fail|blocked",
    "stage3_5_model_integrity": "not_started|pass|fail|blocked",
    "stage4_backlog_slice": "not_started|pass|fail|blocked",
    "stage4_5_capacity_check": "not_started|pass|warn|fail|blocked",
    "stage5_5_cross_stage_integrity": "not_started|pass|fail|blocked",
    "stage5_7_decision_record_integrity": "not_started|pass|fail|not_applicable|blocked",
    "cycle_summary": "not_started|present",
    "lessons_learnt": "not_started|present",
    "escalations": "not_started|present"
  }
}
```
If the run manifest cannot be written in a lifecycle-compliant way: halt immediately.
If state.json cannot be created/updated: halt immediately.

Update state:

- status = `Initialized`
- artifacts.run_manifest = `present`
- assumptions.timebox = value from invocation (or empty)
- assumptions.capacity = value from invocation (or empty)

---

## RESUME RULE (State-Driven Execution)

If `state.json` exists:

- Continue from the first step whose artifact status is `not_started` or `fail` or `blocked`,
- BUT do not rerun steps marked `pass` unless required by invalidation (see RESUME PRECHECK).

If status is `Blocked`:

- Invoke Escalation Handling Subroutine first.
- If all required escalations are resolved/deferred/accepted-risk per rules, resume from the appropriate next step.

If `state.json` is missing but artifacts exist:

- Rebuild state from artifacts:
- mark as `pass` any stage file present that satisfies the step’s requirements
- otherwise mark as `not_started`
- Write `state.json` and continue.

---

## RESUME PRECHECK — Mutation Detection & Invalidation (Hard Gate)

### Purpose

Prevent stale “pass” stamps after any mutation to assumptions or tracked artifacts. Execute:

- at the start of any run after STEP 0, and
- immediately after resolving any escalation that changes assumptions or artifacts.

### Tracked items

- `stage2_scope_extraction.md`
- `stage3_execution_plan.md`
- `stage4_backlog_slice.md`
- `escalations.md`
- assumptions: `timebox`, `capacity`

Fingerprint rule:

- A fingerprint is any deterministic representation of current content, e.g. file length + last modified time, or a simple content hash.
- If fingerprints cannot be computed: HALT.

### Detection

1. Recompute current fingerprints.
2. Compare to `state.json.artifact_fingerprints` and `state.json.assumptions`.
3. If any differ, record a mutation:
- `mutation_seq += 1`
- append to `mutations[]`: timestamp, changed_keys, reason
- update fingerprints and assumptions in state.json.

### Invalidation map

If a tracked item changes, invalidate dependent steps by setting their artifact status to `not_started` and recording them in `invalidated_steps[]`.

Rules:

- If `stage2_scope_extraction` changed → invalidate: STEP 3, STEP 3.5, STEP 4, STEP 5.5
- If `stage3_execution_plan` changed → invalidate: STEP 3.5, STEP 4, STEP 5.5
- If `stage4_backlog_slice` changed → invalidate: STEP 5.5
- If `escalations` changed in a way that adds/removes decision records or Accepted Risk → invalidate: STEP 5.7 and Publish Gate evaluation

Safety policy (required):

- Always re-run STEP 4.5 after any resume where:
- timebox changed OR capacity changed OR STEP 4.5 previously failed/blocked, OR
- any workforce escalation was opened/resolved in this cycle.
Implementation: set `artifacts.stage4_5_capacity_check = not_started` and `attributes.capacity_feasible = not_started`.

Efficiency policy (required):

- Re-run STEP 5.5 only if Stage 2/3/4 changed (fingerprint-based), i.e. only when at least one of:
- stage2_scope_extraction fingerprint changed, OR
- stage3_execution_plan fingerprint changed, OR
- stage4_backlog_slice fingerprint changed.
Otherwise do not invalidate STEP 5.5.

### Resume position

After applying invalidations:

- Resume from the earliest invalidated step (lowest numbered step).
If no invalidations exist:
- Continue normal resume rule.

### Lock consistency check (Hard Gate)
If artifacts.backlog_lock == "acquired" in state.json:
- Verify the lock file exists and is owned by `<cycle_id>`.
- If not, record a blocker and HALT (inconsistent lock state).

---

## ESCALATION HANDLING SUBROUTINE — Callable (Delegated Authority)

Trigger:

- Invoke whenever any step produces ⛔ Blockers AND `--auto-escalate=true`, OR when `status=Blocked`.

Create or append:

- `claude/cycles/<cycle_id>/escalations.md`

Escalations file rules:

- Location is always within the cycle folder: `claude/cycles/<cycle_id>/escalations.md`
- Append-only within the cycle (do not edit previous entries)
- Start with header:

Owner: PMO Lead

Class: Planning Document (Class 4)

Status: Active

Last Updated: <date></date>

Each escalation entry must include:

- Escalation ID: `ESC-YYYYMMDD-nn`
- Raised by step
- Trigger type: Lifecycle | Strategy | Quality | Workforce | Schedule/Delivery | Other
- Owning authority role
- Unblock criteria + required evidence
- SLA due-by
- Disposition: Open | Resolved | Accepted Risk | Deferred
- Resolution summary + evidence links (required when closing)

If Disposition is Deferred, the entry MUST additionally include:

- Deferred by: <role></role>
- Deferred reason
- Next trigger (type + condition + target date/cycle)
- Blocks execution: Yes | No
- Safe to proceed scope (required if Blocks execution = No)

Default SLAs:

- Lifecycle / Process Integrity: 24 hours
- Strategy boundary (§13): 72 hours
- Quality: before execution begins
- Workforce: next planning checkpoint
- Schedule/Delivery: next planning checkpoint

When escalations.md is created:

- artifacts.escalations = present

### Accepted Risk Governance Constraint (Hard Gate)

- Strategy/Quality/Lifecycle may NEVER be Accepted Risk.
- Workforce/Schedule-Delivery may be Accepted Risk ONLY by Product Owner AND only with AR decision record.

### Deferred Governance Constraint (Hard Gate)

- Only owning authority may mark Deferred (by domain).
- Deferred requires trigger and Blocks execution field.
- No auto-carry; must be re-acknowledged next cycle.
- Deferred does not bypass Strategy/Quality/Lifecycle blocks; publish depends on publish gate.

### Decision Record Controls (Minimal Anti-Drift Set)

- Typed decisions only: AR or SRB.
- Naming:
- AR: `docs/product/decisions/AR-<release>-<cycle_id>-<esc_id>.md`
- SRB: `docs/product/decisions/SRB-<release>-<cycle_id>-<esc_id>.md`
- Mandatory template: header + required sections; missing field → HALT.

### Escalation Mutation Rule (Hard Gate)

If resolving an escalation modifies assumptions or Stage 2/3/4 artifacts or decision records:

- Update fingerprints/assumptions in state.json
- Execute RESUME PRECHECK invalidation map
- Do not proceed until required invalidated steps are re-run

### Escalation → State update rules

After processing escalations, update state.json:

- open_escalations, deferred_escalations, accepted_risk_escalations
- deferred_execution_blockers = deferred items with Blocks execution=Yes
If any Open escalations remain:
- status = Blocked
- HALT

---

# Steps (unchanged artifacts; updated macro-state assignments)

## STEP 1 — Release Readiness Validation

Write: `stage1_readiness.md`
Update state.json:

- artifacts.stage1_readiness = pass|fail|blocked

## STEP 2 — Scope Extraction (No Scope Changes Allowed)

Write: `stage2_scope_extraction.md` (S2 IDs required)
Update state.json:

- artifacts.stage2_scope_extraction = pass|fail|blocked

## STEP 3 — Execution Plan

Write: `stage3_execution_plan.md` (EPIC IDs + Maps to + RISK IDs required)
Update state.json:

- artifacts.stage3_execution_plan = pass|fail|blocked
- attributes.plan_structured = true on pass
- status = Planning when Stage 3 exists (pass) even if not yet executable

## STEP 3.5 — Local Model Integrity Check (Conditional Gate)
Classification: Conditional Gate (halts only if escalation remains Open / blocking)

Write: `stage3_5_model_integrity.md`
Update state.json:

- artifacts.stage3_5_model_integrity = pass|fail|blocked
- attributes.plan_executable = true on pass
- status remains Planning (now meaning “plan executable”)

## STEP 3.9 — Shared Write Lock Preflight (Hard Gate)
Purpose:
- Enforce strict concurrency control for shared backlog writes.

Shared resource:
- Backlog file: `claude/backlog/backlog.md`
- Lock file: `claude/backlog/.lock`

Hard rules:
- If `claude/backlog/.lock` exists and is not owned by the current `cycle_id`, HALT.
- No auto-deletion of existing locks is permitted.
- Stale locks follow the manual stale protocol only.

Lock acquisition procedure:
1) If `claude/backlog/.lock` does NOT exist:
   - Create it with the following contents (plain text or JSON is acceptable, must be deterministic):
     - cycle_id: `<cycle_id>`
     - release: `<release>`
     - acquired_utc: `<ISO-8601 UTC>`
     - acquired_by: "Release Planning Engine"
   - Update `state.json`:
     - locks.backlog_lock.owned = true
     - locks.backlog_lock.owner_cycle_id = `<cycle_id>`
     - locks.backlog_lock.owner_release = `<release>`
     - locks.backlog_lock.acquired_utc = `<timestamp>`
     - locks.backlog_lock.status = "acquired"
     - artifacts.backlog_lock = "acquired"

2) If `claude/backlog/.lock` exists:
   - Read its recorded owner cycle_id.
   - If owner cycle_id == `<cycle_id>`:
     - Treat as re-entrant: proceed.
     - Update `state.json` artifacts.backlog_lock = "acquired"
   - If owner cycle_id != `<cycle_id>`:
     - Record a ⛔ Blocker:
       - Trigger type: Lifecycle / Process Integrity
       - Owning authority: PMO Lead
       - Unblock criteria: "Backlog lock must be manually released or declared stale under protocol"
       - Evidence: include lock file contents
     - If `--auto-escalate=true`: invoke Escalation Handling Subroutine.
     - Set state.json:
       - locks.backlog_lock.owned = false
       - locks.backlog_lock.owner_cycle_id = <from lock file>
       - locks.backlog_lock.owner_release = <from lock file if present>
       - locks.backlog_lock.status = "blocked"
       - artifacts.backlog_lock = "blocked"
     - HALT.

Stale protocol (detect only; do not clear):
- If lock appears stale based on timestamp threshold defined by PMO Lead, you may:
  - set locks.backlog_lock.status = "stale_detected"
  - set artifacts.backlog_lock = "stale_detected"
  - create a blocker requiring manual stale resolution
- You may not delete or overwrite the lock automatically.

## STEP 4 — Backlog Slice (commitment)

Write: `stage4_backlog_slice.md` + update backlog slice section

### STEP 4 Precondition — Backlog Lock Required (Hard Gate)
Before writing to `claude/backlog/backlog.md`:
- Verify `claude/backlog/.lock` exists AND contains owner_cycle_id == `<cycle_id>`.
If not true:
- Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: PMO Lead)
- Invoke escalation subroutine if auto-escalate=true
- HALT

Update state.json:

- artifacts.stage4_backlog_slice = pass|fail|blocked
- attributes.backlog_committed = true on pass
- status = Committed on pass

### STEP 4 Postcondition — Release Backlog Lock (Strict)
After successfully updating `claude/backlog/backlog.md`:
- Remove `claude/backlog/.lock`
- Update `state.json`:
  - locks.backlog_lock.status = "released"
  - locks.backlog_lock.owned = false
  - artifacts.backlog_lock = "released"

If the environment does not permit removing the lock file:
- Record a blocker and HALT (lock cannot be left ambiguous).

## STEP 4.5 — Capacity Feasibility Sense Check (Conditional Gate)
Classification: Conditional Gate (halts only if escalation remains Open / blocking)

Write: `stage4_5_capacity_check.md`
Update state.json:

- artifacts.stage4_5_capacity_check = pass|warn|fail|blocked
- attributes.capacity_feasible = pass|warn|fail|blocked
(NOTE: this step is forced to rerun by RESUME PRECHECK per safety policy)

## STEP 5 — Roadmap Annotation (optional)

## STEP 5.5 — Cross-Stage Integrity Validation (Hard Gate)

Write: `stage5_5_cross_stage_integrity.md`
Update state.json:

- artifacts.stage5_5_cross_stage_integrity = pass|fail|blocked
- attributes.cross_stage_integrity = pass|fail|blocked
(NOTE: rerun only if Stage 2/3/4 changed, fingerprint-based)

## STEP 5.7 — Decision Record Integrity Validation (Hard Gate)

Write: `stage5_7_decision_record_integrity.md` only if triggered
Update state.json:

- artifacts.stage5_7_decision_record_integrity = pass|fail|blocked|not_applicable
- attributes.decisions_validated = pass|fail|not_applicable|blocked

## STEP 7 — Cycle Summary

Write: `cycle_summary.md`

## STEP 8 — Lessons Learnt

Write: `lessons_learnt.md`

---

# Publish Gate (Hard Constraint)

## Publish Gate — Deferred Execution Blockers

The run may be marked Validated/Published only if:

- open_escalations is empty, AND
- every Deferred escalation has `Blocks execution: No`, AND
- artifacts.stage4_5_capacity_check is pass OR warn (warn allowed only if mode=standard), AND
- artifacts.stage5_5_cross_stage_integrity is pass, AND
- artifacts.stage5_7_decision_record_integrity is pass OR not_applicable

If any Deferred escalation has `Blocks execution: Yes`:

- status MUST be Blocked (or remain non-Published)
- publish_eligible = false
- HALT (do not mark Published)

If Publish Gate passes:

- status = Validated
- publish_eligible = true
Else:
- publish_eligible = false

---

## Completion Condition (Run Success)

The run is incomplete unless:

- cycle folder exists at `claude/cycles/<cycle_id>/`
- `state.json` exists and reflects mutation_seq, fingerprints, and publish_eligible
- required stage files exist and are compliant for this run
- if auto-escalate=true and blockers occurred, escalations.md exists
- Publish Gate passes
- cycle_summary.md and lessons_learnt.md exist

On success:

- status = Published
- last_transition_utc = now
- publish_eligible = true
- open_escalations = []
