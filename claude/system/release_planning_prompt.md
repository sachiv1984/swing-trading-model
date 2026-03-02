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
