Owner: Head of Specs Team
Status: Active
Version: 1.0
Last Updated: 2026-03-02
Lifecycle Guide: claude/charter/document_lifecycle_guide.md (v2.4)
Team Charter: claude/charter/team_charter.md (v1.1)
---

# Claude Governance Prompt — Release Planning Engine (Cycle-Based, Reusable)

## Purpose (What this routine is for)
Translate an already-approved roadmap release (e.g., v1.7, v1.8) into an execution-ready plan:
- Sequencing, dependencies, acceptance gates, verification approach
- A release backlog slice (without reprioritising the global backlog)
- Optional GitHub issue plan (or issue import text)

This routine is **not** a roadmap rebalance. It may **not** add/replace/defer/kill initiatives or alter strategy boundaries. (Those are reserved for the Roadmap Rebalance Engine.) 

---

## Invocation Rule (Hard Gate)
This routine executes ONLY when the user issues the explicit command:

plan release --version "<vX.Y>" [--date "YYYY-MM-DD"] [--timebox "<text>"] [--capacity "<text>"] [--mode "<strict|standard>"] [--issues "<none|import|gh>"]

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
You must treat the following as authoritative planning inputs:
- claude/roadmap/current_roadmap.md
- claude/backlog/backlog.md
- docs/specs/* (ly allowed by the relevant governance prompt constraints. 

---

## Agent-Based Delegation Model enforce process and demand clarity only. 

### Minimum required roles for this routine
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
- claude/backlog/backlog.md  (release slice only; no reprioritisation outside release)
- claude/roadmap/current_roadmap.md (ONLY to add execution notes/links under the existing release section; no scope change)
- claude/scoring/* (only if explicitly requested by Product Owner for sequencing support)
- claude/ideas/* (not used by default in this routine)

You must not modify:
- source code
- strategy_rules.md
- initiative_register.md
- decision_log.md (reserved for irreversible roadmap decisions in rebalance)
- any doc outside allowed scope

Violation → halt. 

---

## Cycle Folder (Required)
Define:
- date = `--date` or today (YYYY-MM-DD)
- release = `--version` (e.g., v1.7)
- cycle_id = `{date}__release-{release}`  (example: `2026-03-02__release-v1.7`)
Create:
- `claude/cycles/<cycle_id>/`

This routine must always produce a cycle folder with a run manifest and stage outputs.

---

# Mandatory End-to-End Process (Single Run)

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

If all checks pass, proceed.

---

## STEP 0 — Create Run Manifest (Hard Requirement; must be first write)
Create:
- `claude/cycles/<cycle_id>/run_manifest.md`

Class: Operational Record (Class 3)
Owner: Infrastructure & Operations Owner
Status: Filed

Use this header (required fields):
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

If the run manifest cannot be written in a lifecycle-compliant way: halt immediately.

---

## STEP 1 — Release Readiness Validation
Authorities: Product Owner + Strategy Rules & System Intent Owner + Head of Specs Team + Director of Quality

Create:
- `stage1_readiness.md`

Validate:
1) Strategy boundary safety:
   - Confirm nothing in this release violates strategy intent or §13 boundaries.
   - If a boundary decision is required (per roadmap gating), record it as a **blocker** (this routine may not resolve it).
2) Spec readiness:
   - Identify which canonical specs must exist/lock before implementation (metrics definitions, API contracts, data model, frontend page specs).
   - If missing and mode=strict: halt with blockers.
   - If missing and mode=standard: proceed with a “Spec TODO list” and flag as “Implementation may not start until complete”.
3) Quality readiness:
   - Define release-level acceptance gates (what “ready to ship” means for this release).
4) Dependency readiness:
   - Confirm prerequisite roadmap items for the release are marked complete in the roadmap narrative.
   - If not, treat as a blocker or scope constraint.

Output format:
- ✅ Ready items
- ⚠ Risks
- ⛔ Blockers (must name owning role)

---

## STEP 2 — Scope Extraction (No Scope Changes Allowed)
Authorities: Product Owner + Head of Specs Team (governance)

Create:
- `stage2_scope_extraction.md`

Rules:
- Extract only what is already stated under the target release in `current_roadmap.md`.
- You may clarify wording but may not add features or expand scope.
- Any ambiguity must be turned into:
  - a clarifying question, or
  - an assumption (mode=standard only), or
  - a blocker (mode=strict)

Output:
- Scope bullets (exactly as extracted)
- Explicit out-of-scope for this release (as stated or implied)
- Required gates and prerequisites (as stated)

---

## STEP 3 — Execution Plan (Sequencing + Work Breakdown)
Authorities: Product Owner (sequencing), Director of Quality (verification gates), Head of Specs Team (spec governance), Infrastructure & Ops (operational considerations)

Create:
- `stage3_execution_plan.md`

Must include:
- Workstreams (e.g., backend, frontend, docs/governance, CI/CD)
- Epics → Stories → Tasks breakdown
- Dependencies between items
- Verification notes per epic (tests, validations, QA sign-off)
- Definition of Done per epic
- Delivery sequencing (Week 1/Week 2 or Sprint days) based on timebox/capacity if provided
- Risk register (top 5) with mitigations and owners

Hard rule:
- No epic without acceptance criteria and verification approach.

---

## STEP 4 — Backlog Slice (Reconciliation Only)
Authorities: Product Owner + PMO Lead (process), Head of Specs Team (no grooming)

Create:
- `stage4_backlog_slice.md`

Then update:
- `claude/backlog/backlog.md` (allowed write scope)

Rules for backlog update:
- Do NOT reprioritise global backlog.
- Only add a clearly marked section:
  - “Release Plan: <version> (Prepared <date>)”
- Within that section, list:
  - the selected epics/stories with references to stage3_execution_plan anchors
  - links to relevant specs and cycle docs
- Do not rewrite existing backlog items; you may add one-line status notes such as:
  - “Planned for v1.7 — see cycle <cycle_id>”

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
Authority: PMO Lead (process), Product Owner (content)

Create one of:
- `issue_import.md` (always if --issues=import OR gh fails)
- If --issues=gh:
  - attempt to create issues via `gh` CLI
  - if `gh auth status` fails: fall back to issue_import.md

Issue requirements:
- One epic issue per epic
- Child issues for stories
- Include:
  - acceptance criteria
  - verification notes
  - links to cycle docs
- Labels (suggested):
  - release:<version>
  - area:backend / area:frontend / area:docs
  - type:feature / type:tech-debt / type:chore

---

## STEP 7 — Cycle Summary (Required)
Authority: Facilitator (process summary)

Create:
- `cycle_summary.md`

Must include:
- Release version planned
- Blockers (if any) and owning roles
- Final scoped epics count
- Key risks and mitigations
- Files produced in this cycle folder
- If issues created/import produced, note where

---

## STEP 8 — Lessons Learnt Stub (Required)
Authority: PMO Lead

Create:
- `lessons_learnt.md` (stub; to be filled post-release)

Structure:
- What went well in planning
- What was unclear / caused delay
- Governance improvements suggested (prompt updates, templates, checks)

---

## Completion Condition (Run Success)
The run is incomplete unless:
- A cycle folder exists at `claude/cycles/<cycle_id>/`
- `run_manifest.md`, `stage1_readiness.md`, `stage2_scope_extraction.md`,
  `stage3_execution_plan.md`, `stage4_backlog_slice.md`, `cycle_summary.md`,
  and `lessons_learnt.md` exist and are lifecycle compliant
- If backlog updates were made, they are release-slice only (no reprioritisation)
- No prohibited files were edited

If you cannot reach this state: report the precise blocking rule and halt.
