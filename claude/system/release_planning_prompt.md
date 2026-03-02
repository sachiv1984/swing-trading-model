**Owner:** Head of Specs Team 
**Status:** Active 
**Version:** 1.7 
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

# State Machine Model (Hard Requirement)

## Canonical states
- `Initialized`
- `ReadinessValidated`
- `ScopeLocked`
- `PlanDrafted`
- `PlanExecutable`
- `Committed`
- `Feasible`
- `IntegrityPassed`
- `DecisionsValidated` (or `NotApplicable`)
- `Published`
- `Blocked`
- `Deferred`

## State transition rule
A state transition may occur only when:
- the required artefact(s) for that state exist and are compliant, AND
- no Open escalations block progress for that transition (per escalation rules).

If Open escalations exist:
- State MUST be `Blocked` with escalation IDs recorded.

---

# Mandatory End-to-End Process (Single Run)

### Global Rule — Blockers Must Route
If any step produces one or more ⛔ Blockers:
- If `--auto-escalate=true`: invoke the **ESCALATION HANDLING SUBROUTINE** immediately after that step.
- If `--auto-escalate=false`: record blockers in the step output and **HALT**.

### Global Rule — State Must Be Updated
At the end of every step:
- Update `state.json` with:
  - current state
  - artefact statuses
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

Manifest must record:
- Invocation command text
- Release version targeted
- Inputs used (file paths)
- Activated roles (authorities + process roles)
- Any preflight marker file created
- Mode: strict|standard
- Issues mode: none|import|gh
- Auto-escalate: true|false

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
  "mutations": [],
  "invalidated_steps": [],
  "open_escalations": [],
  "deferred_escalations": [],
  "deferred_execution_blockers": [],
  "accepted_risk_escalations": [],
  "artifacts": {
    "run_manifest": "present|missing",
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

Prevent stale “pass” stamps after any mutation to assumptions or tracked artifacts. This routine must be executed:

- at the start of any run after STEP 0, and
- immediately after resolving any escalation that changes assumptions or artifacts.

### Fingerprints (what to track)

Tracked items:

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
- append to `mutations[]`:
- timestamp, changed_keys, reason (e.g. "Workforce escalation resolution: timebox change")
- update fingerprints and assumptions in state.json.

### Invalidation Map (dependency graph)

If a tracked item changes, invalidate dependent steps by setting their artifact status to `not_started` and recording them in `invalidated_steps[]`.

Rules:

- If `stage2_scope_extraction` changed → invalidate: STEP 3, STEP 3.5, STEP 4, STEP 5.5
- If `stage3_execution_plan` changed → invalidate: STEP 3.5, STEP 4, STEP 5.5
- If `stage4_backlog_slice` changed → invalidate: STEP 5.5
- If `escalations` changed in a way that adds/removes decision records or Accepted Risk → invalidate: STEP 5.7 and Publish Gate evaluation

Special rule (your chosen safety policy):

- Always re-run STEP 4.5 after any resume where:
- timebox changed OR capacity changed OR STEP 4.5 previously failed/blocked, OR
- any workforce escalation was opened/resolved in this cycle.
Implementation: set `artifacts.stage4_5_capacity_check = not_started`.

Special rule (your chosen efficiency policy):

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

---

## ESCALATION HANDLING SUBROUTINE — Callable (Delegated Authority)

Trigger:

- Invoke this subroutine whenever any step produces ⛔ Blockers AND `--auto-escalate=true`, OR when state is `Blocked`.

Create or append:

- `claude/cycles/<cycle_id>/escalations.md`

Escalations file rules:

- Location is always within the cycle folder: `claude/cycles/<cycle_id>/escalations.md`
- Append-only within the cycle (do not edit previous entries)
- Start the file with a minimal header block suitable for a cycle-local planning artefact:

Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date></date>

Where:

- `<release>` = value of `--version` (e.g., v1.7)
- `<cycle_id>` = `{date}__release-{release}`
- `<esc_id>` = escalation ID (ESC-YYYYMMDD-nn)

Each escalation entry must include:

- Escalation ID: `ESC-YYYYMMDD-nn`
- Raised by step: e.g., `STEP 3.5`
- Trigger type: Lifecycle | Strategy | Quality | Workforce | Schedule/Delivery | Other
- Owning authority role
- Unblock criteria + required evidence
- SLA due-by (default if not specified below)
- Disposition: Open | Resolved | Accepted Risk | Deferred
- Resolution summary + evidence links (required when closing)

If Disposition is Deferred, the entry MUST additionally include:

- Deferred by: <role></role>
- Deferred reason: <one paragraph=""></one>
- Next trigger:
- Trigger type: date | event | dependency | decision
- Trigger condition: <concrete></concrete>
- Target date or target cycle: <value></value>
- Blocks execution: Yes | No
- Safe to proceed scope (required if Blocks execution = No): <what is="" safe="" to="" do=""></what>

Default SLAs (unless a step specifies otherwise):

- Lifecycle / Process Integrity: 24 hours
- Strategy boundary (§13): 72 hours
- Quality: before execution begins
- Workforce: next planning checkpoint
- Schedule/Delivery: next planning checkpoint

When escalations.md is created, update state:

- artifacts.escalations = `present`

---

### Accepted Risk Governance Constraint (Hard Gate)

“Accepted Risk” is an irreversible decision and is permitted only under strict rules.

#### AR-1: Non-acceptable domains (may NEVER be Accepted Risk)

The following trigger types may not be marked “Accepted Risk” under any circumstances:

- Strategy
- Quality
- Lifecycle

If an escalation is in one of these domains, valid dispositions are:

- Open (until resolved), or
- Deferred (only with a named trigger and next action)
Any attempt to mark these as “Accepted Risk” is a governance violation:
- Immediately set disposition back to Open
- Record a note in the escalation entry: “Accepted Risk not permitted for this domain”
- HALT

#### AR-2: Acceptable domains (permitted only with constraints)

Only these trigger types may be marked “Accepted Risk”:

- Workforce
- Schedule/Delivery
And only by:
- Product Owner (accepting authority)

---

### Deferred Governance Constraint (Hard Gate)

#### D-1: Authority

Only the owning authority role for the escalation’s trigger type may set Disposition=Deferred:

- Lifecycle → Head of Specs Team
- Strategy → Strategy Rules & System Intent Owner
- Quality → Director of Quality
- Workforce → FinOps & Resource Architect
- Schedule/Delivery → Product Owner
- Other → Product Owner (must not mask Strategy/Quality/Lifecycle)

Facilitator/Challenger may not mark Deferred.

#### D-2: Required fields

A Deferred escalation is invalid unless all required Deferred fields are present:

- Deferred by (role)
- Deferred reason
- Next trigger (type + condition + target date/cycle)
- Blocks execution (Yes/No)
- If Blocks execution=No: Safe to proceed scope

If any field is missing:

- Disposition must be treated as Open
- HALT

#### D-3: No auto-carry

Deferred does not carry forward automatically. It must be explicitly re-acknowledged in the next cycle.

#### D-4: Deferred does not bypass blocks

Deferred does not override Strategy/Quality/Lifecycle blocking authority. Whether the run can publish depends on Blocks execution and the Publish Gate.

---

### Decision Record Controls (Minimal Anti-Drift Set)

#### DR-1: Typed decision records only (Release Planning)

Decision records created by this routine are restricted to exactly two types:

- AR = Accepted Risk (Workforce or Schedule/Delivery only)
- SRB = Strategy Rules Boundary confirmation (“boundaries unchanged”)
No other decision record types may be created in Release Planning. If needed, halt.

#### DR-2: Naming convention (required)

- Accepted Risk: `docs/product/decisions/AR-<release>-<cycle_id>-<esc_id>.md`
- Strategy Boundary confirmation: `docs/product/decisions/SRB-<release>-<cycle_id>-<esc_id>.md`

#### DR-3: Mandatory template (hard requirement)

Any decision record created MUST follow this exact template.

Header (required):
Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
Decision Type: AR | SRB
Decision ID: &lt;matches filename exactly, including AR-/SRB- prefix>
Related Escalation: <esc-yyyymmdd-nn>
Related Cycle: &lt;cycle_id>
Applies To Release: &lt;vX.Y>
Time Boundary: This release only</esc-yyyymmdd-nn></date>

Body sections (required):

## Decision

## Context

## Risk / Impact

## Guardrails (Non-Negotiable)

- Strategy boundaries unchanged: Yes/No (explain)
- Quality gates not bypassed: Yes/No (explain)
- Lifecycle compliance maintained: Yes/No (explain)
- No scope change inside Release Planning: Yes/No (explain)

## Evidence

## Follow-up

If any required header field or section is missing:

- The decision record is non-compliant
- The escalation may not be closed as Accepted Risk / Resolved-via-Decision
- HALT

---

### Resolution loop behaviour (delegated authority)

For each Open escalation:

- Switch to the owning authority agent perspective and attempt resolution within allowed write scope.

A) Lifecycle / Process Integrity (Head of Specs Team)

- If resolvable via local artefact remediation (IDs missing, mapping lines missing, acceptance criteria missing, missing risk links): fix artefacts inside the cycle folder (and permitted files) and mark Resolved.
- If it requires scope change or writes outside allowed scope: keep Open and HALT.

B) Strategy (§13 / boundaries) (Strategy Rules & System Intent Owner)

- If resolvable by creating a decision record confirming “boundaries unchanged” WITHOUT editing strategy_rules.md, create:
`docs/product/decisions/SRB-<release>-<cycle_id>-<esc_id>.md`
using the mandatory template and mark Resolved with evidence link.
- If it requires changing strategy_rules.md: keep Open and HALT (out of scope).

C) Quality (Director of Quality)

- If resolvable by clarifying acceptance gates and verification criteria inside planning artefacts: update stage1/stage3 and mark Resolved.
- If it requires evidence not present (re-testing, missing specs, missing datasets): keep Open and HALT.

D) Workforce (FinOps & Resource Architect)

- If resolvable by sequencing/timebox/capacity assumptions without changing scope: update stage3 plan and mark Resolved.
- If it requires scope change or displacement: keep Open and HALT (requires Roadmap Rebalance Engine).

E) Schedule/Delivery (Product Owner)

- If resolvable by sequencing adjustments, explicit timeboxing, or adding non-scope-changing guardrails: update stage3/stage4 notes and mark Resolved.
- If the only path is to knowingly accept schedule risk without affecting Strategy/Quality/Lifecycle: may mark Accepted Risk ONLY if AR-2 and DR-2/DR-3 are satisfied.

F) Other escalation

- Route to Product Owner; only resolvable if it does not violate Strategy/Quality/Lifecycle constraints.

---

### Escalation Mutation Rule (Hard Gate)

If resolving an escalation modifies:

- assumptions (timebox/capacity), OR
- any tracked stage artifact (Stage 2/3/4), OR
- escalations content (including Deferred blocks execution toggles), OR
- decision records created/changed,
then:

1. Update `state.json` fingerprints/assumptions
2. Execute RESUME PRECHECK invalidation map
3. Do not proceed until required invalidated steps are re-run

---

### Escalation → State update rules

After processing escalations, update state.json:

- open_escalations = [list of ESC IDs still Open]
- deferred_escalations = [list of ESC IDs Deferred]
- accepted_risk_escalations = [list of ESC IDs Accepted Risk]
- deferred_execution_blockers = [list of Deferred ESC IDs where Blocks execution = Yes]
- artifacts.escalations = present

If any Open escalations remain:

- status = Blocked
- HALT

If no Open escalations remain:

- Resume execution at the first step whose artifact status is not pass (or warn where permitted).

---

# Steps (Implementation Notes)

All steps remain as defined in v1.6:

- STEP 1: stage1_readiness.md
- STEP 2: stage2_scope_extraction.md
- STEP 3: stage3_execution_plan.md
- STEP 3.5: stage3_5_model_integrity.md
- STEP 4: stage4_backlog_slice.md + update backlog slice
- STEP 4.5: stage4_5_capacity_check.md
- STEP 5: roadmap annotation (optional)
- STEP 5.5: stage5_5_cross_stage_integrity.md
- STEP 5.7: stage5_7_decision_record_integrity.md (conditional)
- STEP 6: issue artifacts (optional)
- STEP 7: cycle_summary.md
- STEP 8: lessons_learnt.md

Hard requirement for mutation safety:

- At the start of the run after STEP 0, execute RESUME PRECHECK.
- After any escalation mutation, execute RESUME PRECHECK.

---

# Publish Gate (Hard Constraint)

## Publish Gate — Deferred Execution Blockers

The run may be marked Published only if:

- open_escalations is empty, AND
- every Deferred escalation has `Blocks execution: No`

If any Deferred escalation has `Blocks execution: Yes`:

- status MUST be Blocked (or remain non-Published)
- publish_eligible = false
- HALT (do not mark Published)

When Publish Gate passes:

- publish_eligible = true
Otherwise:
- publish_eligible = false

---

## Completion Condition (Run Success)

The run is incomplete unless:

- cycle folder exists at `claude/cycles/<cycle_id>/`
- `state.json` exists and reflects the latest statuses, including mutation_seq, fingerprints, and publish_eligible
- required stage files exist and are compliant for this run
- if auto-escalate=true and blockers occurred, escalations.md exists
- Publish Gate passes

On success, update state.json:

- status = Published
- last_transition_utc = now
- publish_eligible = true
- open_escalations = []
