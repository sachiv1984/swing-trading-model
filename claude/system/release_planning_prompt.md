Owner: Head of Specs Team
Status: Active
Version: 1.3
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
- docs/product/decisions/* (ONLY when required to resolve an escalation; must be lifecycle-compliant decision record)
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

### Global Rule — Blockers Must Route
If any step produces one or more ⛔ Blockers:
- If `--auto-escalate=true`: invoke the **ESCALATION HANDLING SUBROUTINE** immediately after that step.
- If `--auto-escalate=false`: record blockers in the step output and **HALT**.

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

## ESCALATION HANDLING SUBROUTINE — Callable (Delegated Authority)
Trigger:
- Invoke this subroutine whenever any step produces ⛔ Blockers AND `--auto-escalate=true`.

Create or append:
- `claude/cycles/<cycle_id>/escalations.md`

Escalations file rules:
- Location is always within the cycle folder: `claude/cycles/<cycle_id>/escalations.md`
- Append-only within the cycle (do not edit previous entries)
- Start the file with a minimal header block suitable for a cycle-local planning artefact:

Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>

Each escalation entry must include:
- Escalation ID: `ESC-YYYYMMDD-nn`
- Raised by step: e.g., `STEP 3.5`
- Trigger type: Lifecycle | Strategy | Quality | Workforce | Other
- Owning authority role
- Unblock criteria + required evidence
- SLA due-by (default if not specified below)
- Disposition: Open | Resolved | Accepted Risk | Deferred
- Resolution summary + evidence links (required when closing)

Default SLAs (unless a step specifies otherwise):
- Lifecycle / Process Integrity: 24 hours
- Strategy boundary (§13): 72 hours
- Quality: before execution begins (cannot be waived here)
- Workforce: next planning checkpoint (cannot be overridden)

Resolution loop behaviour (delegated authority):
For each Open escalation:
- Switch to the owning authority agent perspective and attempt resolution within allowed write scope.

A) Lifecycle / Process Integrity (Head of Specs Team):
- If resolvable via local artefact remediation (IDs missing, mapping lines missing, acceptance criteria missing, missing risk links): fix the artefacts **inside the cycle folder** (and permitted files) and mark Resolved.
- If it requires scope change or writes outside allowed scope: keep Open and HALT.

B) Strategy (§13 / boundaries) (Strategy Rules & System Intent Owner):
- If resolvable by creating a decision record that confirms “boundaries unchanged” WITHOUT editing `strategy_rules.md`, create it under `docs/product/decisions/` and mark Resolved with evidence.
- If it requires changing `strategy_rules.md`: keep Open and HALT (out of scope).

C) Quality (Director of Quality):
- If resolvable by clarifying acceptance gates and verification criteria inside planning artefacts: update stage1/stage3 and mark Resolved.
- If it requires evidence not present (re-testing, missing specs, missing datasets): keep Open and HALT.

D) Workforce (FinOps & Resource Architect):
- If resolvable by sequencing/timebox/capacity assumptions without changing scope: update stage3 plan and mark Resolved.
- If it requires scope change or displacement: keep Open and HALT (requires Roadmap Rebalance Engine).

E) Other escalation:
- Route to Product Owner; only resolvable if it does not violate domain blocks.

Hard rule:
- If any escalation remains Open after attempted resolution:
  - If escalation type is Strategy, Quality, or Lifecycle → HALT regardless of mode
  - Otherwise:
    - mode=strict → HALT
    - mode=standard → HALT unless the missing info is purely clerical and can be authored deterministically from existing repo context

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
- ⛔ Blockers (must name owning role + unblock criteria + evidence required)

If ⛔ Blockers exist:
- Apply Global Rule — Blockers Must Route

---

## STEP 2 — Scope Extraction (No Scope Changes Allowed)
Authorities: Product Owner + Head of Specs Team

Create:
- `claude/cycles/<cycle_id>/stage2_scope_extraction.md`

Rules:
- Extract only what is already stated under the target release in `claude/roadmap/current_roadmap.md`.
- You may clarify wording but may not add features or expand scope.
- Output MUST include a list of scope items with IDs:
  - `S2-01: ...`
  - `S2-02: ...`
- Output MUST include a “Scope-to-Epic Mapping Table (seed)” section:
  - `S2-01 -> (to be mapped in Stage 3)`
  - `S2-02 -> (to be mapped in Stage 3)`

If IDs are missing or the output cannot be represented as S2 items:
- Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
- Apply Global Rule — Blockers Must Route

---

## STEP 3 — Execution Plan (Sequencing + Work Breakdown)
Authorities: Product Owner (sequencing), Director of Quality (verification gates), Head of Specs Team (spec governance), Infrastructure & Ops (operational considerations)

Create:
- `claude/cycles/<cycle_id>/stage3_execution_plan.md`

Must include:
- Workstreams (backend, frontend, docs/governance, CI/CD)
- Epics → Stories → Tasks breakdown
- Dependencies between items
- Delivery sequencing (Week 1/Week 2 or Sprint days) based on timebox/capacity if provided
- Risk register (top 5) with mitigations and owners

Epic format (hard requirement):
For each epic:
- `EPIC-xx: <title>`
  - Maps to: `S2-yy, S2-zz`
  - Acceptance Criteria: (bullets)
  - Verification Approach: (bullets)
  - Definition of Done: (bullets)
  - Stories/Tasks: (optional IDs ST-xx / TASK-xx)

Risk format (hard requirement):
- `RISK-xx: <risk title>`
  - Relates to: `EPIC-xx` OR `Release-level`
  - Mitigation: (bullets)
  - Owner: <role>

If EPIC IDs, S2 mappings, or required epic sections are missing:
- Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
- Apply Global Rule — Blockers Must Route

---

## STEP 3.5 — Local Model Integrity Check (Soft Gate)
Authority: Head of Specs Team (process integrity), Director of Quality (gate completeness)

Create:
- `claude/cycles/<cycle_id>/stage3_5_model_integrity.md`

Purpose:
- Validate that the Stage 3 execution model is internally executable before committing it to the backlog slice.

Checks (local only — does not require Stage 4):
1) Epic completeness:
   - Every `EPIC-xx` includes Acceptance Criteria, Verification Approach, and Definition of Done.
2) Risk alignment:
   - Every `RISK-xx` has `Relates to: EPIC-xx` OR `Release-level`.
3) Basic mapping presence:
   - Every `EPIC-xx` contains a `Maps to:` line with at least one `S2-xx`.

Outcomes:
- PASS: record “PASS” and list epic IDs validated.
- FAIL (remediable without scope change):
  - Update `stage3_execution_plan.md` to add the missing sections/lines.
  - Re-run checks and record “PASS after remediation”.
- FAIL (not remediable without scope change or requires missing external info):
  - Record ⛔ Blocker(s) (Lifecycle / Process Integrity; owner: Head of Specs Team)
  - Apply Global Rule — Blockers Must Route
  - Halt if escalation remains Open.

---

## STEP 4 — Backlog Slice (Release Section Only; No Global Reprioritisation)
Authorities: Product Owner + PMO Lead (process) + Head of Specs Team (no grooming)

Create:
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md`

Then update:
- `claude/backlog/backlog.md`

Rules for backlog update:
- Do NOT reprioritise global backlog.
- Only add a clearly marked section:
  - “Release Plan: <version> (Prepared <date>)”
- Within that section, list epics **by EPIC ID** exactly (no free-text epics), with links to cycle docs.
- Stage 4 slice MUST NOT introduce any EPIC IDs that are not present in Stage 3.
- Do not rewrite existing backlog items; you may add one-line status notes:
  - “Planned for vX.Y — see cycle <cycle_id>”

If any backlog change beyond the release slice is required:
- Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
- Apply Global Rule — Blockers Must Route

## STEP 4.5 — Capacity Feasibility Sense Check (Soft Gate)
Primary Authority: FinOps & Resource Architect  
Process Authority: Head of Specs Team

Create:
- `claude/cycles/<cycle_id>/stage4_5_capacity_check.md`

Purpose:
- Perform a lightweight feasibility sanity check to ensure the planned release is not obviously undeliverable given the declared timebox and capacity.
- This step does NOT reprioritise work, does NOT resize scope, and does NOT perform estimation.
- It answers one question only: “Is this plan clearly infeasible as written?”

Inputs:
- `stage3_execution_plan.md`
- `stage4_backlog_slice.md`
- Invocation parameters:
  - `--timebox`
  - `--capacity`

Checks:

1) Order-of-magnitude fit
   - Given the number of EPIC-xx items, their described effort signals (e.g. “multi-day”, “requires spec + verification”), and the declared timebox/capacity:
     - Is the plan obviously too large?
   - Example FAIL conditions:
     - Multiple non-trivial epics in a very short timebox with low capacity
     - No slack or buffer implied anywhere in the plan

2) Critical-path plausibility
   - Identify the longest dependency chain across EPIC-xx items.
   - Determine whether that chain plausibly fits inside the declared timebox.
   - If the critical path alone clearly exceeds the timebox → FAIL.

3) Capacity assumption consistency
   - Check whether the execution plan respects the declared capacity model.
   - Example FAIL conditions:
     - Capacity declared as “solo-dev evenings” but plan assumes parallel backend/frontend execution
     - Capacity declared as part-time but sequencing assumes full-time throughput

Outcomes:

- PASS:
  - Record “PASS” with a short justification in `stage4_5_capacity_check.md`.
  - Proceed to STEP 5.

- WARN (allowed only if `mode=standard`):
  - Borderline feasibility (tight fit, no slack).
  - Record “WARN” with explicit risks.
  - Proceed, but ensure the risk is also reflected in the Stage 3 risk register.

- FAIL:
  - Plan is clearly infeasible and cannot be corrected by resequencing alone.
  - Record “FAIL” with evidence in `stage4_5_capacity_check.md`.
  - Create ⛔ Blocker(s) with:
    - Trigger type: Workforce
    - Owning authority: FinOps & Resource Architect
    - Unblock criteria:
      - Clarified or adjusted timebox, OR
      - Clarified or adjusted capacity assumption, OR
      - Deferral to Roadmap Rebalance Engine
  - Apply Global Rule — Blockers Must Route.
  - HALT if escalation remains Open.

Hard rules:
- This step may NOT reduce scope.
- This step may NOT introduce new work.
- This step may NOT override strategy or quality gates.

---

## STEP 5 — Roadmap Annotation (Optional, Non-Decision Notes Only)
Authority: Product Owner

Update `claude/roadmap/current_roadmap.md` ONLY to:
- add links to the cycle folder under the relevant release section, and/or
- add a short “Execution Notes” subsection that does not change scope, status, or priority.

If an edit would change scope/priority:
- Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: Head of Specs Team)
- Apply Global Rule — Blockers Must Route

---

## STEP 5.5 — Cross-Stage Integrity Validation (Hard Gate)
Authority: Head of Specs Team (governance integrity)

Create:
- `claude/cycles/<cycle_id>/stage5_5_cross_stage_integrity.md`

Purpose:
- Enforce cross-stage consistency so the release plan is coherent, traceable, and executable.
- This is a HARD GATE. Any failure must halt.

Validation Inputs:
- stage2_scope_extraction.md
- stage3_execution_plan.md
- stage4_backlog_slice.md
- stage1_readiness.md (for blockers/assumptions alignment)

Checks (must all pass; ID-based):
1) Scope preservation (no dropped scope):
   - Every `S2-xx` in Stage 2 must be referenced by at least one `EPIC-xx` “Maps to:” line in Stage 3.
2) No new scope (no scope creep):
   - Every `EPIC-xx` in Stage 3 must map back to at least one `S2-xx` in Stage 2.
3) Epic completeness (cross-stage invariant):
   - Every `EPIC-xx` has Acceptance Criteria + Verification Approach + Definition of Done.
4) Commitment integrity (plan → slice):
   - Every `EPIC-xx` in Stage 3 appears in Stage 4 slice.
   - Stage 4 slice contains no unknown `EPIC-xx` IDs.
5) Risk alignment:
   - Every `RISK-xx` relates to at least one `EPIC-xx` OR is explicitly `Release-level`.
   - Risk mitigations must not imply new work not represented in epics/tasks (implicit scope creep).

Failure behaviour (mandatory):
- Write a FAIL report including:
  - Each failed check
  - Evidence (exact IDs and where they mismatch)
- Record ⛔ Blocker(s) (Lifecycle / Process Integrity; owner: Head of Specs Team)
- Apply Global Rule — Blockers Must Route
- HALT regardless of mode if any escalation remains Open

---

## STEP 6 — Issue Artifacts (Optional; depends on --issues)
Authority: PMO Lead (process), Product Owner (content)

Create one of:
- `claude/cycles/<cycle_id>/issue_import.md` (always if --issues=import OR gh fails)
- If --issues=gh:
  - attempt to create issues via `gh` CLI
  - if `gh auth status` fails: fall back to `issue_import.md`

Issue requirements:
- One epic issue per epic (EPIC IDs)
- Child issues for stories (if you created ST/TASK IDs)
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
- `claude/cycles/<cycle_id>/cycle_summary.md`

Must include:
- Release version planned
- Escalations raised + disposition (IDs)
- Remaining blockers (if any) and owning roles
- Final scoped epics count
- Key risks and mitigations
- Files produced in this cycle folder
- If issues created/import produced, note where

---

## STEP 8 — Lessons Learnt Stub (Required)
Authority: PMO Lead

Create:
- `claude/cycles/<cycle_id>/lessons_learnt.md` (stub; to be filled post-release)

Structure:
- What went well in planning
- What was unclear / caused delay
- Governance improvements suggested (prompt updates, templates, checks)

---

## Completion Condition (Run Success)
The run is incomplete unless:
- A cycle folder exists at `claude/cycles/<cycle_id>/`
- The following files exist and are lifecycle compliant:
  - run_manifest.md
  - stage1_readiness.md
  - stage2_scope_extraction.md
  - stage3_execution_plan.md
  - stage3_5_model_integrity.md
  - stage4_backlog_slice.md
  - stage5_5_cross_stage_integrity.md
  - cycle_summary.md
  - lessons_learnt.md
- If any blockers occurred and `--auto-escalate=true`, `escalations.md` exists and contains entries
- No prohibited files were edited

If you cannot reach this state: report the precise blocking rule and halt.
