Owner: Head of Specs Team
Status: Active
Version: 1.1
Last Updated: 2026-03-02
Lifecycle Guide: claude/charter/document_lifecycle_guide.md (v2.4)
Team Charter: claude/charter/team_charter.md (v1.1)
---

# Claude Governance Prompt — Release Planning Engine (Cycle-Based, Reusable, Escalation-Aware)

## Purpose
Translate an already-approved roadmap release (e.g., v1.7, v1.8) into an execution-ready plan:
- Sequencing, dependencies, acceptance gates, verification approach
- A release backlog slice (without reprioritising the global backlog)
- Optional GitHub issue plan (or issue import text)

This routine is NOT a roadmap rebalance. It may NOT add/replace/defer/kill initiatives or alter strategy boundaries. Those remain reserved for the Roadmap Rebalance Engine. 
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
  - `strict`: halt on any missing prerequisite or unclear scope
  - `standard`: proceed with explicit assumptions and flags
- `--issues` optional:
  - `none`: do not generate issue artifacts
  - `import`: create `issue_import.md` only
  - `gh`: attempt to create GitHub issues via `gh` CLI; if unavailable, fall back to `import`
- `--auto-escalate` optional:
  - `true` (default): system creates, routes, and attempts to resolve escalations using delegated authority.
  - `false`: system records blockers only and halts without attempting resolution.

If invocation is not exact, do not run. Treat as conversational.
---

## Canonical Governance Sources (Non-Negotiable)
Binding governance stack:
- claude/charter/team_charter.md (role authority, conflict rules)
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
- Facilitator
- Challenger

If any required role is missing or malformed (agent file absent or missing the required `**Role:** <Role Name>` line), halt.
---

## Write Scope Restriction (Hard Gate)
During this routine you may write only to:
- claude/cycles/<cycle_id>/*
- claude/backlog/backlog.md  (release slice only; no global reprioritisation)
- claude/roadmap/current_roadmap.md (ONLY to add execution notes/links under the existing release section; no scope change)
- docs/product/decisions/* (ONLY when required to resolve an escalation; must be lifecycle-compliant Class 4 decision record owned by Product Owner unless the lifecycle guide requires otherwise)
- claude/scoring/* (only if explicitly requested by Product Owner for sequencing support)

You must not modify:
- source code
- claude/strategy/strategy_rules.md
- claude/roadmap/initiative_register.md
- claude/roadmap/decision_log.md (reserved for irreversible roadmap decisions in rebalance)
- any doc outside allowed scope

Violation → halt.
---

## Cycle Folder (Required)
Define:
- date = `--date` or today (YYYY-MM-DD)
- release = `--version` (e.g., v1.7)
- cycle_id = `{date}__release-{release}` (example: `2026-03-02__release-v1.7`)
Create:
- `claude/cycles/<cycle_id>/`

This routine must always produce a cycle folder with a run manifest and stage outputs.
---

# Mandatory End-to-End Process (Single Run)

## STEP -1 — Preflight Gate (Hard Gate)
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

## STEP 0 — Create Run Manifest (Hard Requirement; must be first write)
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

If the run manifest cannot be written in a lifecycle-compliant way: halt immediately.
---

## STEP 1 — Release Readiness Validation
Authorities: Product Owner + Strategy Rules & System Intent Owner + Head of Specs Team + Director of Quality

Create:
- `claude/cycles/<cycle_id>/stage1_readiness.md`

Validate:
1) Strategy boundary safety:
   - Confirm nothing in this release violates strategy intent or §13 boundaries.
   - If a boundary decision/confirmation is required (per roadmap gating), record as blocker.
2) Spec readiness:
   - Identify which canonical specs must exist/lock before implementation.
   - If missing and mode=strict: record blocker(s).
   - If missing and mode=standard: record “Spec TODO list” and mark as “Implementation may not start until complete”.
3) Quality readiness:
   - Define release-level acceptance gates (what “ready to ship” means).
4) Dependency readiness:
   - Confirm prerequisite roadmap items for the release are complete/closed as required.
   - If not, record as blocker or constraint.

Output format:
- ✅ Ready items
- ⚠ Risks
- ⛔ Blockers (must name owning role + unblock criteria)
---

## STEP 1.5 — Escalation Handling Loop (Delegated Authority)  [NEW]
Trigger:
- If any ⛔ Blockers exist in stage1_readiness.md AND `--auto-escalate=true`

Create or append:
- `claude/cycles/<cycle_id>/escalations.md`

Escalation file rules:
- Append-only within the cycle (do not edit previous entries).
- Each entry must be factual and must name:
  - Escalation ID (ESC-YYYYMMDD-nn)
  - Trigger type: Lifecycle | Strategy | Quality | Workforce | Other
  - Owning authority role
  - Unblock criteria + required evidence
  - SLA due-by (default: Lifecycle 24h; Strategy 72h; Quality before execution; Workforce next checkpoint unless prompt-specific override)
  - Disposition: Open | Resolved | Accepted Risk | Deferred

Resolution loop behaviour:
For each Open escalation, switch to the owning authority agent perspective and attempt resolution:

A) Lifecycle escalation (Head of Specs Team):
- If resolvable within allowed write scope via header-only remediation or lifecycle correction: perform the minimal compliant change and mark Resolved with evidence link.
- If resolution requires edits outside allowed scope: keep Open and halt.

B) Strategy escalation (§13 / boundaries) (Strategy Rules & System Intent Owner):
- If resolution can be achieved by a decision record (e.g., "Boundaries unchanged for <feature>") WITHOUT editing strategy_rules.md, create a lifecycle-compliant decision record under `docs/product/decisions/` and mark Resolved with link.
- If resolution requires strategy_rules.md revision: keep Open and halt (outside scope).

C) Quality escalation (Director of Quality):
- If resolution is “define/clarify acceptance gates” and no missing verification prerequisites remain, update stage1_readiness + stage3_execution_plan gates and mark Resolved.
- If resolution requires re-testing, missing specs, or evidence not available in repo: keep Open and halt.

D) Workforce escalation (FinOps & Resource Architect):
- If resolution is possible by sequencing adjustments, timebox adjustments, or clarifying capacity assumptions (without scope change), update stage3 plan and mark Resolved.
- If resolution requires changing scope or stopping work: keep Open and halt (requires Roadmap Rebalance Engine).

E) Other escalation:
- Route to Product Owner; only resolvable if it does not violate domain blocks.

Hard rule:
- If any escalation remains Open after the loop and mode=strict OR the escalation is Strategy/Quality/Lifecycle: halt and report the escalation IDs and required next action.
---

## STEP 2 — Scope Extraction (No Scope Changes Allowed)
Authorities: Product Owner + Head of Specs Team

Create:
- `claude/cycles/<cycle_id>/stage2_scope_extraction.md`

Rules:
- Extract only what is already stated under the target release in `claude/roadmap/current_roadmap.md`.
- You may clarify wording but may not add features or expand scope.
- Any ambiguity must become:
  - a clarifying question, or
  - an assumption (mode=standard only), or
  - a blocker (mode=strict), which routes to STEP 1.5 if auto-escalate is true.
---

## STEP 3 — Execution Plan (Sequencing + Work Breakdown)
Authorities: Product Owner (sequencing), Director of Quality (verification gates), Head of Specs Team (spec governance), Infrastructure & Ops (operational considerations)

Create:
- `claude/cycles/<cycle_id>/stage3_execution_plan.md`

Must include:
- Workstreams (backend, frontend, docs/governance, CI/CD)
- Epics → Stories → Tasks
- Dependencies
- Acceptance criteria + verification approach per epic
- Definition of Done per epic
- Sequencing based on timebox/capacity if provided
- Risk register (top 5) with mitigations + owners
---

## STEP 4 — Backlog Slice (Release Section Only; No Global Reprioritisation)
Authorities: Product Owner + PMO Lead + Head of Specs Team

Create:
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md`

Then update:
- `claude/backlog/backlog.md`

Rules:
- Do NOT reprioritise global backlog.
- Only add a clearly marked section:
  - “Release Plan: <version> (Prepared <date>)”
- List selected epics/stories and link to cycle docs.
- Do not rewrite existing items; only add one-line status notes:
  - “Planned for vX.Y — see cycle <cycle_id>”
If any backlog change beyond the release slice is required: halt.
---

## STEP 5 — Roadmap Annotation (Optional, Non-Decision Notes Only)
Authority: Product Owner

Update `claude/roadmap/current_roadmap.md` ONLY to:
- add links to the cycle folder under the relevant release section, and/or
- add a short “Execution Notes” subsection that does not change scope, status, or priority.

If an edit would change scope/priority: halt (requires Roadmap Rebalance Engine).
---

## STEP 6 — Issue Artifacts (Optional; depends on --issues)
Authority: PMO Lead + Product Owner

Create:
- `claude/cycles/<cycle_id>/issue_import.md` if --issues=import OR gh fails
- If --issues=gh:
  - attempt to create issues via `gh` CLI
  - if `gh auth status` fails: fall back to `issue_import.md`
---

## STEP 7 — Cycle Summary (Required)
Authority: Facilitator

Create:
- `claude/cycles/<cycle_id>/cycle_summary.md`

Must include:
- Release version planned
- Escalations raised + disposition (IDs)
- Remaining blockers (if any)
- Final scoped epics count
- Key risks and mitigations
- Files produced
---

## STEP 8 — Lessons Learnt Stub (Required)
Authority: PMO Lead

Create:
- `claude/cycles/<cycle_id>/lessons_learnt.md` (stub)
---

## Completion Condition (Run Success)
The run is incomplete unless:
- Cycle folder exists at `claude/cycles/<cycle_id>/`
- run_manifest.md, stage1_readiness.md, stage2_scope_extraction.md, stage3_execution_plan.md, stage4_backlog_slice.md, cycle_summary.md, lessons_learnt.md exist
- If blockers occurred and auto-escalate=true, escalations.md exists and contains entries
- No prohibited files were edited
If you cannot reach this state: report the precise blocking rule and halt.
