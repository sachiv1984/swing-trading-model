Owner: Head of Specs Team
Status: Active
Version: 1.5
Last Updated: 2026-03-02
Lifecycle Guide: claude/charter/document_lifecycle_guide.md
Team Charter: claude/charter/team_charter.md
---

# Claude Governance Prompt — Release Planning Engine (Cycle-Based, Reusable, Escalation-Aware, State-Driven)

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
- If the cycle folder exists but `state.json` is missing, rebuild state from artefacts present, write state.json, then continue.
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
  - last transition timestamp
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
  "last_transition_utc": "<ISO-8601 UTC>",
  "open_escalations": [],
  "deferred_escalations": [],
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
If the run manifest cannot be written in a lifecycle-compliant way: halt immediately. If `state.json` cannot be created/updated: halt immediately.

Update state:

-   `status = Initialized`
-   `artifacts.run_manifest = present`

* * * * *

RESUME RULE (State-Driven Execution)
------------------------------------

If `state.json` exists:

-   Continue from the first step whose artifact status is `not_started` or `fail` or `blocked`,
-   BUT do not rerun steps marked `pass` unless required by a downstream invalidation.

If status is `Blocked`:

-   Invoke Escalation Handling Subroutine first.
-   If all required escalations are resolved/deferred/accepted-risk per rules, resume from the appropriate next step.

If `state.json` is missing but artifacts exist:

Rebuild state from artifacts:

-   mark as `pass` any stage file present that satisfies the step's requirements
-   otherwise mark as `not_started`

Write `state.json` and continue.

* * * * *

ESCALATION HANDLING SUBROUTINE --- Callable (Delegated Authority)
===============================================================

Trigger
-------

Invoke this subroutine whenever any step produces ⛔ Blockers AND `--auto-escalate=true`, OR when state is `Blocked`.

Create or append:

-   `claude/cycles/<cycle_id>/escalations.md`

### Escalations file rules

-   Location is always within the cycle folder: `claude/cycles/<cycle_id>/escalations.md`

-   Append-only within the cycle (do not edit previous entries)

-   Start the file with a minimal header block suitable for a cycle-local planning artefact:

    -   Owner: PMO Lead
    -   Class: Planning Document (Class 4)
    -   Status: Active
    -   Last Updated: `<date>`

Where:

-   `<release>` = value of `--version` (e.g., v1.7)
-   `<cycle_id>` = `{date}__release-{release}`
-   `<esc_id>` = escalation ID (`ESC-YYYYMMDD-nn`)

### Each escalation entry must include

-   Escalation ID: `ESC-YYYYMMDD-nn`
-   Raised by step: e.g., `STEP 3.5`
-   Trigger type: `Lifecycle | Strategy | Quality | Workforce | Schedule/Delivery | Other`
-   Owning authority role
-   Unblock criteria + required evidence
-   SLA due-by (default if not specified below)
-   Disposition: `Open | Resolved | Accepted Risk | Deferred`
-   Resolution summary + evidence links (required when closing)

### Default SLAs (unless a step specifies otherwise)

-   Lifecycle / Process Integrity: 24 hours
-   Strategy boundary (§13): 72 hours
-   Quality: before execution begins
-   Workforce: next planning checkpoint
-   Schedule/Delivery: next planning checkpoint

When `escalations.md` is created, update state:

-   `artifacts.escalations = present`

* * * * *

Accepted Risk Governance Constraint (Hard Gate)
-----------------------------------------------

"Accepted Risk" is an irreversible decision and is permitted only under strict rules.

### AR-1: Non-acceptable domains (may NEVER be Accepted Risk)

The following trigger types may not be marked "Accepted Risk" under any circumstances:

-   Strategy
-   Quality
-   Lifecycle

If an escalation is in one of these domains, valid dispositions are:

-   Open (until resolved), or
-   Deferred (only with a named trigger and next action)

Any attempt to mark these as "Accepted Risk" is a governance violation:

-   Immediately set disposition back to Open
-   Record a note in the escalation entry: "Accepted Risk not permitted for this domain"
-   HALT

### AR-2: Acceptable domains (permitted only with constraints)

Only these trigger types may be marked "Accepted Risk":

-   Workforce
-   Schedule/Delivery

And only by:

-   Product Owner (accepting authority)

* * * * *

Decision Record Controls (Minimal Anti-Drift Set)
-------------------------------------------------

### DR-1: Typed decision records only (Release Planning)

Decision records created by this routine are restricted to exactly two types:

-   `AR` = Accepted Risk (Workforce or Schedule/Delivery only)
-   `SRB` = Strategy Rules Boundary confirmation ("boundaries unchanged")

No other decision record types may be created in Release Planning. If needed, halt.

### DR-2: Naming convention (required; Option 2)

-   Accepted Risk: `docs/product/decisions/AR-<release>-<cycle_id>-<esc_id>.md`
-   Strategy Boundary confirmation: `docs/product/decisions/SRB-<release>-<cycle_id>-<esc_id>.md`

### DR-3: Mandatory template (hard requirement)

Any decision record created MUST follow this exact template.

#### Header (required)

-   Owner: Product Owner
-   Class: Planning Document (Class 4)
-   Status: Active
-   Last Updated: `<date>`
-   Decision Type: `AR | SRB`
-   Decision ID: `<matches filename exactly, including AR-/SRB- prefix>`
-   Related Escalation: `<esc-yyyymmdd-nn>`
-   Related Cycle: `<cycle_id>`
-   Applies To Release: `<vX.Y>`
-   Time Boundary: `This release only`

#### Body sections (required)

-   Decision
-   Context
-   Risk / Impact
-   Guardrails (Non-Negotiable)
    -   Strategy boundaries unchanged: Yes/No (explain)
    -   Quality gates not bypassed: Yes/No (explain)
    -   Lifecycle compliance maintained: Yes/No (explain)
    -   No scope change inside Release Planning: Yes/No (explain)
-   Evidence
-   Follow-up

If any required header field or section is missing:

-   The decision record is non-compliant
-   The escalation may not be closed as Accepted Risk / Resolved-via-Decision
-   HALT

* * * * *

Resolution loop behaviour (delegated authority)
-----------------------------------------------

For each Open escalation:

Switch to the owning authority agent perspective and attempt resolution within allowed write scope.

### A) Lifecycle / Process Integrity (Head of Specs Team)

-   If resolvable via local artefact remediation (IDs missing, mapping lines missing, acceptance criteria missing, missing risk links): fix the artefacts inside the cycle folder (and permitted files) and mark Resolved.
-   If it requires scope change or writes outside allowed scope: keep Open and HALT.

### B) Strategy (§13 / boundaries) (Strategy Rules & System Intent Owner)

-   If resolvable by creating a decision record confirming "boundaries unchanged" WITHOUT editing `strategy_rules.md`, create:
    -   `docs/product/decisions/SRB-<release>-<cycle_id>-<esc_id>.md`
    -   using the mandatory template and mark Resolved with evidence link.
-   If it requires changing `strategy_rules.md`: keep Open and HALT (out of scope).

### C) Quality (Director of Quality)

-   If resolvable by clarifying acceptance gates and verification criteria inside planning artefacts: update stage1/stage3 and mark Resolved.
-   If it requires evidence not present (re-testing, missing specs, missing datasets): keep Open and HALT.

### D) Workforce (FinOps & Resource Architect)

-   If resolvable by sequencing/timebox/capacity assumptions without changing scope: update stage3 plan and mark Resolved.
-   If it requires scope change or displacement: keep Open and HALT (requires Roadmap Rebalance Engine).

### E) Schedule/Delivery (Product Owner)

-   If resolvable by sequencing adjustments, explicit timeboxing, or adding non-scope-changing guardrails: update stage3/stage4 notes and mark Resolved.
-   If the only path is to knowingly accept schedule risk without affecting Strategy/Quality/Lifecycle: may mark Accepted Risk ONLY if AR-2 and DR-2/DR-3 are satisfied.

### F) Other escalation

-   Route to Product Owner; only resolvable if it does not violate Strategy/Quality/Lifecycle constraints.

* * * * *

Applying "Accepted Risk" (Mechanics)
------------------------------------

If an escalation is proposed to be marked "Accepted Risk":

1.  Validate trigger type is Workforce or Schedule/Delivery (AR-2). If not, apply AR-1.
2.  Validate accepting authority is Product Owner (AR-2). If not, HALT.
3.  Create the mandatory AR decision record at:
    -   `docs/product/decisions/AR-<release>-<cycle_id>-<esc_id>.md`
    -   using DR-3 template.
4.  Update the escalation entry:
    -   Disposition: Accepted Risk
    -   Link to decision record
    -   Time Boundary: This release only

If any step above cannot be satisfied: HALT.

### Escalation → State update rules

After processing escalations, update `state.json`:

-   `open_escalations = [list of ESC IDs still Open]`
-   `deferred_escalations = [list of ESC IDs Deferred]`
-   `accepted_risk_escalations = [list of ESC IDs Accepted Risk]`
-   `artifacts.escalations = present`

If any Open escalations remain:

-   `status = Blocked`
-   HALT

If no Open escalations remain:

-   Resume execution at the first step whose artifact status is not `pass` (or `warn` where permitted).

* * * * *

STEP 1 --- Release Readiness Validation
=====================================

Authorities: Product Owner + Strategy Rules & System Intent Owner + Head of Specs Team + Director of Quality

Create:

-   `claude/cycles/<cycle_id>/stage1_readiness.md`

Validate:

-   Strategy boundary safety:
    -   Confirm nothing in this release violates strategy intent or §13 boundaries.
    -   If a boundary decision/confirmation is required (per roadmap gating), record as blocker.
-   Spec readiness:
    -   Identify which canonical specs must exist/lock before implementation.
    -   If missing and `mode=strict`: record blocker(s).
    -   If missing and `mode=standard`: record "Spec TODO list" and mark as "Implementation may not start until complete".
-   Quality readiness:
    -   Define release-level acceptance gates (what "ready to ship" means).
-   Dependency readiness:
    -   Confirm prerequisite roadmap items for the release are complete/closed as required.
    -   If not, record as blocker or constraint.

### Output format

-   ✅ Ready items
-   ⚠ Risks
-   ⛔ Blockers (must name owning role + unblock criteria + evidence required)

If ⛔ Blockers exist:

-   Apply Global Rule --- Blockers Must Route

Update `state.json`:

-   `artifacts.stage1_readiness = pass|fail|blocked`
-   If pass: `status = ReadinessValidated`

* * * * *

STEP 2 --- Scope Extraction (No Scope Changes Allowed)
====================================================

Authorities: Product Owner + Head of Specs Team

Create:

-   `claude/cycles/<cycle_id>/stage2_scope_extraction.md`

Rules:

-   Extract only what is already stated under the target release in `claude/roadmap/current_roadmap.md`.
-   You may clarify wording but may not add features or expand scope.

Output MUST include:

-   A list of scope items with IDs:

    -   `S2-01: ...`
    -   `S2-02: ...`
-   A "Scope-to-Epic Mapping Table (seed)" section:

    -   `S2-01 -> (to be mapped in Stage 3)`
    -   `S2-02 -> (to be mapped in Stage 3)`

If IDs are missing or the output cannot be represented as S2 items:

-   Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
-   Apply Global Rule --- Blockers Must Route

Update `state.json`:

-   `artifacts.stage2_scope_extraction = pass|fail|blocked`
-   If pass: `status = ScopeLocked`

* * * * *

STEP 3 --- Execution Plan (Sequencing + Work Breakdown)
=====================================================

Authorities: Product Owner (sequencing), Director of Quality (verification gates), Head of Specs Team (spec governance), Infrastructure & Ops (operational considerations)

Create:

-   `claude/cycles/<cycle_id>/stage3_execution_plan.md`

Must include:

-   Workstreams (backend, frontend, docs/governance, CI/CD)
-   Epics → Stories → Tasks breakdown
-   Dependencies between items
-   Delivery sequencing (Week 1/Week 2 or Sprint days) based on timebox/capacity if provided
-   Risk register (top 5) with mitigations and owners

### Epic format (hard requirement)

For each epic:

-   `EPIC-xx: <title>`
-   `Maps to: S2-yy, S2-zz`
-   `Acceptance Criteria:` (bullets)
-   `Verification Approach:` (bullets)
-   `Definition of Done:` (bullets)
-   `Stories/Tasks:` (optional IDs `ST-xx` / `TASK-xx`)

### Risk format (hard requirement)

For each risk:

-   `RISK-xx: <risk title>`
-   `Relates to: EPIC-xx OR Release-level`
-   `Mitigation:` (bullets)
-   `Owner: <role>`

If EPIC IDs, S2 mappings, or required epic sections are missing:

-   Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
-   Apply Global Rule --- Blockers Must Route

Update `state.json`:

-   `artifacts.stage3_execution_plan = pass|fail|blocked`
-   If pass: `status = PlanDrafted`

* * * * *

STEP 3.5 --- Local Model Integrity Check (Soft Gate)
==================================================

Authority: Head of Specs Team (process integrity), Director of Quality (gate completeness)

Create:

-   `claude/cycles/<cycle_id>/stage3_5_model_integrity.md`

Purpose:

-   Validate that the Stage 3 execution model is internally executable before committing it to the backlog slice.

Checks (local only --- does not require Stage 4):

-   Epic completeness:
    -   Every `EPIC-xx` includes Acceptance Criteria, Verification Approach, and Definition of Done.
-   Risk alignment:
    -   Every `RISK-xx` has `Relates to: EPIC-xx` OR `Release-level`.
-   Basic mapping presence:
    -   Every `EPIC-xx` contains a `Maps to:` line with at least one `S2-xx`.

Outcomes:

-   PASS: record "PASS" and list epic IDs validated.
-   FAIL (remediable without scope change):
    -   Update `stage3_execution_plan.md` to add the missing sections/lines.
    -   Re-run checks and record "PASS after remediation".
-   FAIL (not remediable without scope change or requires missing external info):
    -   Record ⛔ Blocker(s) (Lifecycle / Process Integrity; owner: Head of Specs Team)
    -   Apply Global Rule --- Blockers Must Route
    -   Halt if escalation remains Open.

Update `state.json`:

-   `artifacts.stage3_5_model_integrity = pass|fail|blocked`
-   If pass: `status = PlanExecutable`

* * * * *

STEP 4 --- Backlog Slice (Release Section Only; No Global Reprioritisation)
=========================================================================

Authorities: Product Owner + PMO Lead (process) + Head of Specs Team (no grooming)

Create:

-   `claude/cycles/<cycle_id>/stage4_backlog_slice.md`

Then update:

-   `claude/backlog/backlog.md`

### Rules for backlog update

-   Do NOT reprioritise global backlog.
-   Only add a clearly marked section:
    -   `Release Plan: <version> (Prepared <date>)`
-   Within that section, list epics by EPIC ID exactly (no free-text epics), with links to cycle docs.
-   Stage 4 slice MUST NOT introduce any EPIC IDs that are not present in Stage 3.
-   Do not rewrite existing backlog items; you may add one-line status notes:
    -   `Planned for vX.Y --- see cycle <cycle_id>`

If any backlog change beyond the release slice is required:

-   Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
-   Apply Global Rule --- Blockers Must Route

Update `state.json`:

-   `artifacts.stage4_backlog_slice = pass|fail|blocked`
-   If pass: `status = Committed`

* * * * *

STEP 4.5 --- Capacity Feasibility Sense Check (Soft Gate)
=======================================================

Primary Authority: FinOps & Resource Architect Process Authority: Head of Specs Team

Create:

-   `claude/cycles/<cycle_id>/stage4_5_capacity_check.md`

Purpose:

-   Perform a lightweight feasibility sanity check to ensure the planned release is not obviously undeliverable given the declared timebox and capacity.
-   This step does NOT reprioritise work, does NOT resize scope, and does NOT perform estimation.
-   It answers one question only: "Is this plan clearly infeasible as written?"

Inputs:

-   `stage3_execution_plan.md`
-   `stage4_backlog_slice.md`
-   Invocation parameters: `--timebox`, `--capacity`

Checks:

-   Order-of-magnitude fit
-   Critical-path plausibility
-   Capacity assumption consistency

Outcomes:

-   PASS:
    -   Record "PASS" with short justification.
-   WARN (allowed only if `mode=standard`):
    -   Borderline feasibility; record "WARN" with explicit risks and ensure the risk is reflected in Stage 3 risk register.
-   FAIL:
    -   Record "FAIL" with evidence.
    -   Create ⛔ Blocker(s) with:
        -   Trigger type: Workforce
        -   Owning authority: FinOps & Resource Architect
        -   Unblock criteria:
            -   Clarified or adjusted timebox, OR
            -   Clarified or adjusted capacity assumption, OR
            -   Deferral to Roadmap Rebalance Engine
    -   Apply Global Rule --- Blockers Must Route
    -   HALT if escalation remains Open.

Hard rules:

-   This step may NOT reduce scope.
-   This step may NOT introduce new work.
-   This step may NOT override strategy or quality gates.

Update `state.json`:

-   `artifacts.stage4_5_capacity_check = pass|warn|fail|blocked`
-   If pass or warn (where allowed): `status = Feasible`
-   If fail/blocked: `status = Blocked`

* * * * *

STEP 5 --- Roadmap Annotation (Optional, Non-Decision Notes Only)
===============================================================

Authority: Product Owner

Update `claude/roadmap/current_roadmap.md` ONLY to:

-   add links to the cycle folder under the relevant release section, and/or
-   add a short "Execution Notes" subsection that does not change scope, status, or priority.

If an edit would change scope/priority:

-   Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
-   Apply Global Rule --- Blockers Must Route

(No state change required; this step is optional.)

* * * * *

STEP 5.5 --- Cross-Stage Integrity Validation (Hard Gate)
=======================================================

Authority: Head of Specs Team (governance integrity)

Create:

-   `claude/cycles/<cycle_id>/stage5_5_cross_stage_integrity.md`

Purpose:

-   Enforce cross-stage consistency so the release plan is coherent, traceable, and executable.
-   This is a HARD GATE. Any failure must halt.

Validation Inputs:

-   `stage2_scope_extraction.md`
-   `stage3_execution_plan.md`
-   `stage4_backlog_slice.md`
-   `stage1_readiness.md` (for blockers/assumptions alignment)

Checks (must all pass; ID-based):

-   Scope preservation (no dropped scope)
-   No new scope (no scope creep)
-   Epic completeness (cross-stage invariant)
-   Commitment integrity (plan → slice)
-   Risk alignment (no orphan risks; no implicit scope creep)

Failure behaviour (mandatory):

-   Write FAIL report with evidence (exact IDs and where mismatches occur)
-   Record ⛔ Blocker(s) (Lifecycle / Process Integrity; owner: Head of Specs Team)
-   Apply Global Rule --- Blockers Must Route
-   HALT regardless of mode if any escalation remains Open

Update `state.json`:

-   `artifacts.stage5_5_cross_stage_integrity = pass|fail|blocked`
-   If pass: `status = IntegrityPassed`

* * * * *

STEP 5.7 --- Decision Record Integrity Validation (Hard Gate)
===========================================================

Authority: Head of Specs Team (governance integrity)

Create:

-   `claude/cycles/<cycle_id>/stage5_7_decision_record_integrity.md`

Trigger:

Run this step only if either:

-   Any escalation disposition is "Accepted Risk", OR
-   Any escalation was resolved via a decision record (e.g., SRB boundary confirmation)

Checks (must all pass):

-   A decision record exists for each such escalation:
    -   Accepted Risk → `docs/product/decisions/AR-<release>-<cycle_id>-<esc_id>.md`
    -   Strategy boundary confirmation → `docs/product/decisions/SRB-<release>-<cycle_id>-<esc_id>.md`
-   Each decision record is typed correctly:
    -   Only Decision Type AR or SRB allowed
    -   Filename prefix matches Decision Type
    -   Decision ID matches filename exactly (including prefix)
-   Required header fields present:
    -   Owner, Class, Status, Last Updated
    -   Decision Type, Decision ID
    -   Related Escalation, Related Cycle
    -   Applies To Release
    -   Time Boundary ("This release only")
-   Required body sections present:
    -   Decision
    -   Context
    -   Risk / Impact
    -   Guardrails (Non-Negotiable)
    -   Evidence
    -   Follow-up

Failure behaviour:

-   Write FAIL with evidence
-   Record ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
-   Apply Global Rule --- Blockers Must Route
-   HALT

Pass behaviour:

-   Write PASS and list validated decision record filenames.

Update `state.json`:

-   `artifacts.stage5_7_decision_record_integrity = pass|fail|blocked|not_applicable`
-   If not triggered: set to `not_applicable`
-   If pass or not_applicable: `status = DecisionsValidated`

* * * * *

STEP 6 --- Issue Artifacts (Optional; depends on --issues)
========================================================

Authority: PMO Lead (process), Product Owner (content)

Create one of:

-   `claude/cycles/<cycle_id>/issue_import.md` (always if `--issues=import` OR `gh` fails)

If `--issues=gh`:

-   attempt to create issues via `gh` CLI
-   if `gh auth status` fails: fall back to `issue_import.md`

(No state change required; optional.)

* * * * *

STEP 7 --- Cycle Summary (Required)
=================================

Authority: Facilitator (process summary)

Create:

-   `claude/cycles/<cycle_id>/cycle_summary.md`

Must include:

-   Release version planned
-   Escalations raised + disposition (IDs)
-   Remaining blockers (if any) and owning roles
-   Any Accepted Risk entries must include:
    -   escalation ID
    -   decision record link
    -   time boundary (this release only)
-   Final scoped epics count
-   Key risks and mitigations
-   Files produced in this cycle folder
-   If issues created/import produced, note where

Update `state.json`:

-   `artifacts.cycle_summary = present`

* * * * *

STEP 8 --- Lessons Learnt Stub (Required)
=======================================

Authority: PMO Lead

Create:

-   `claude/cycles/<cycle_id>/lessons_learnt.md` (stub; to be filled post-release)

Update `state.json`:

-   `artifacts.lessons_learnt = present`

* * * * *

Completion Condition (Run Success)
----------------------------------

The run is incomplete unless:

-   A cycle folder exists at `claude/cycles/<cycle_id>/`
-   `state.json` exists and reflects the latest statuses
-   The following files exist and are lifecycle compliant:
    -   `run_manifest.md`
    -   `stage1_readiness.md`
    -   `stage2_scope_extraction.md`
    -   `stage3_execution_plan.md`
    -   `stage3_5_model_integrity.md`
    -   `stage4_backlog_slice.md`
    -   `stage4_5_capacity_check.md`
    -   `stage5_5_cross_stage_integrity.md`
    -   `stage5_7_decision_record_integrity.md` (only required if triggered per STEP 5.7; otherwise state must mark `not_applicable`)
    -   `cycle_summary.md`
    -   `lessons_learnt.md`
-   If any blockers occurred and `--auto-escalate=true`, `escalations.md` exists and contains entries
-   No prohibited files were edited

If you cannot reach this state: report the precise blocking rule and halt.

On success, update `state.json`:

-   `status = Published`
-   `last_transition_utc = now`
-   `artifacts.*` reflect final status
-   `open_escalations = []`
