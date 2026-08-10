**Owner:** Head of Specs Team
**Status:** Active
**Version:** 2.49
**Last Updated:** 2026-08-10
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Release Planning Engine — Governance Prompt

(Cycle-Based, Reusable, Escalation-Aware, State-Driven, Mutation-Safe, Concurrency-Safe, Terminal-Sealed, Assumption-Frozen)

## 1. Purpose
Translate an already-approved roadmap release (e.g., v1.7, v1.8) into an execution-ready plan:
- Sequencing, dependencies, acceptance gates, verification approach
- A release backlog slice (without reprioritising the global backlog)
- Optional GitHub issue plan (or issue import text)

This routine is **NOT** a roadmap rebalance. It may **NOT** add/replace/defer/kill initiatives or alter strategy boundaries. Those remain reserved for the Roadmap Rebalance Engine.

---

## 2. Delegated Authority Model (User Delegation)
The user delegates operational decision-making to the defined role agents. During this routine:
- Each authority role may decide within its chartered domain.
- Domain blocks remain binding (Quality and Strategy blocks cannot be overridden by Product Owner).
- If an escalation requires information that is not present in-repo and cannot be inferred safely, the routine must record the escalation and halt.

Non-decision roles (Facilitator, Challenger) have no decision authority. They enforce process and demand clarity only.

---

## 3. Invocation Rule (Hard Gate)
This routine executes ONLY when the user issues the explicit command:

```
plan release --version "<vX.Y>" [--date "YYYY-MM-DD"] [--timebox "<text>"] [--capacity "<text>"] [--mode "<strict|standard>"] [--issues "<none|import|gh>"] [--auto-escalate "<true|false>"]
```

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
  - `import`: create `issue_import.md` in `claude/cycles/<cycle_id>/issue_import.md` — see §10.1
  - `gh`: attempt to create GitHub issues via `gh` CLI; if unavailable, fall back to `import`
- `--auto-escalate` optional:
  - `true` (default): system creates, routes, and attempts to resolve escalations using delegated authority
  - `false`: system records blockers only and halts without attempting resolution

If invocation is not exact, do not run. Treat as conversational.

Apply the Lifecycle Guard (valid from-states: `Closed`) per `claude/system/shared_standards.md §10` before executing any step.

---

## 4. Canonical Governance Sources (Non-Negotiable)

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

---

## 5. Source-of-Truth Planning Inputs
Authoritative planning inputs:
- claude/roadmap/current_roadmap.md
- claude/backlog/backlog.md
- docs/specs/* (canonical specs as needed for readiness checks)
- docs/reference/openapi.yaml (supporting reference; align when needed)

---

## 6. Agent Integrity (Required Roles)
→ Apply `claude/system/shared/governance_preamble.md §Agent-Integrity`. Required roles:
- Product Owner
- Head of Specs Team
- PMO Lead
- Director of Quality
- Infrastructure & Operations Owner
- Strategy Rules & System Intent Owner
- FinOps & Resource Architect
- Facilitator
- Challenger

---

## 7. Write Scope Restriction (Hard Gate)
→ Apply `claude/system/shared/governance_preamble.md §Write-Scope`. Phase-specific permitted paths:
- `claude/cycles/<cycle_id>/*`
- `claude/backlog/backlog.md` (release slice only; no global reprioritisation)
- `claude/roadmap/current_roadmap.md` (ONLY to add execution notes/links under the existing release section; no scope change)
- `docs/product/scope/*` (scope document created at STEP 2)
- `docs/product/decisions/*` (decisions record created at STEP 3; also when required to resolve an escalation; must be lifecycle-compliant)
- `claude/scoring/*` (only if explicitly requested by Product Owner for sequencing support)

Must not modify: source code, `claude/strategy/strategy_rules.md`, `claude/roadmap/initiative_register.md`, `claude/roadmap/decision_log.md` (reserved for irreversible roadmap decisions in rebalance), any doc outside allowed scope.

---

## 8. Authoritative Source Model
The cycle folder:

`claude/cycles/<cycle_id>/`

is the authoritative historical planning record.

Shared files (backlog.md, roadmap.md) are operational mirrors only.

Post-publish modifications to shared files do NOT alter the sealed record.

Amendments require a new cycle.

---

## 9. Identifier Standards (Hard Requirement)
To enable deterministic cross-stage integrity checks, all stage artefacts MUST use stable IDs.

### 9.1 ID Formats
- Stage 2 scope items: `S2-01`, `S2-02`, ...
- Stage 3 epics: `EPIC-01`, `EPIC-02`, ...
- Stage 3 stories/tasks (optional but recommended): `ST-01`, `TASK-01`, ...
- Risks: `RISK-01`, `RISK-02`, ...
- Escalations: `ESC-YYYYMMDD-nn`

### 9.2 Mapping Rules
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

## 10. Cycle Folder + State (Required)
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

## 10.1 Issue Import Format (`--issues import`)
When `--issues import` (or `gh` fallback) is specified, write:

`claude/cycles/<cycle_id>/issue_import.md`

Minimum required content per issue:

```markdown
## [EPIC-xx] <Epic Title>

**Labels:** epic, release-vX.Y
**Milestone:** vX.Y
**Assignee:** (unassigned)

<Epic description from stage3_execution_plan.md>

---

## [ST-xx] <Story Title>

**Labels:** story, release-vX.Y
**Milestone:** vX.Y
**Parent epic:** EPIC-xx
**Assignee:** (unassigned)

<Story description and acceptance criteria summary>
```

One entry per EPIC-xx and ST-xx in `stage4_backlog_slice.md`, in backlog order. This file is the authoritative import source if `gh` CLI is unavailable or falls back.

For EPIC descriptions, source from `stage4_backlog_slice.md` (the EPIC header and description there are the authoritative issue import source, as the backlog slice is the canonical scope record for Sprint Planning).

---

## 11. Sealing Mechanism

Per-artefact SHA-256 hash computation has been removed (ST-17, v2.4). Sealing uses `sealed: true` flag as the sole sealing mechanism. `state_snapshot_hash` is retained as a single lightweight tamper indicator — record the git commit SHA at publish time. Filesystem timestamps are forbidden.

`git diff main` is the authoritative drift detection method for Published cycles.

---

## 12. State Machine Model (Reduced Macro-States)
### 12.1 Canonical macro-states
- `Initialized` — run manifest + state created
- `Planning` — plan being constructed and internally executable
- `Committed` — backlog slice committed (release slice written)
- `Validated` — feasibility + integrity + decisions validated + publish gate eligible
- `Published` — sealed; cycle summary + lessons filed; publish gate passed
- `Blocked` — one or more Open escalations exist; publish gate cannot pass; strict locks block progress; or terminal publish guard halts further action

### 12.2 State semantics (no overlap)
- **Planning** means "Stage 3 exists and Stage 3.5 passed."
- **Committed** means "Stage 4 passed."
- **Validated** means "Stage 4.5 + Stage 5.5 + Stage 5.7 (if triggered) passed AND Publish Gate eligible."
- **Published** means "Sealed snapshot recorded AND cycle summary + lessons exist AND publish gate passed."

---

# Mandatory End-to-End Process (Single Run)

## 13. Gate Semantics (Definitions)
**Hard Gate:** Any FAIL halts immediately (no continuation).

**Conditional Gate:** FAIL may be remediated or escalated; the run halts only if the resulting escalation remains Open or blocks publishing/execution.

**Advisory Check:** WARN-only; never creates blockers; never escalates; never halts.

### 13.1 Global Rule — Blockers Must Route
If any step produces one or more ⛔ Blockers:
- If `--auto-escalate=true`: invoke the **ESCALATION HANDLING SUBROUTINE** immediately after that step.
- If `--auto-escalate=false`: record blockers in the step output and **HALT**.

### 13.2 Global Rule — State Must Be Updated
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

**Dry-run detection (BLG-GOV-25 / ST-11):** If `--dry-run` is specified in the invocation, execute this step and scope extraction only (sub-checks -1.1 through -1.5), then output the dry-run report below and exit without making any file writes, git commits, or state updates.

**Dry-run report format:**
```
DRY-RUN: plan release --version <vX.Y>
Preflight: PASS / FAIL (list any missing files or role gaps)
Roadmap item: <item-id> — <item-name>
Artefacts that would be created:
  - claude/cycles/<cycle_id>/release_plan.md
  - claude/cycles/<cycle_id>/stage4_backlog_slice.md
  - claude/cycles/<cycle_id>/stage4_issue_manifest.json
  - claude/cycles/<cycle_id>/design_gate.md (if design required)
  - .claude_current_state.json (status → Release_Plan_Published)
Estimated scope: <N> EPICs, <M> stories (based on roadmap item backlog slice)
No files written — re-invoke without --dry-run to execute.
```

### -1.1 Common Preflight — Required Files Present
Apply `claude/system/shared/preflight_common.md` (sub-check 1 only) with:
- required_files:
  - claude/charter/team_charter.md
  - claude/charter/document_lifecycle_guide.md
  - claude/strategy/strategy_rules.md
  - claude/roadmap/current_roadmap.md
  - claude/backlog/backlog.md

**Issue creation prerequisite (IMP-48):** If `--issues gh` or `--issues import` is specified: verify `claude/system/gh_issue_template.md` exists. If missing: halt — "gh_issue_template.md not found — issue creation will fail."

### -1.2 Verify Release Exists on the Roadmap
Open `claude/roadmap/current_roadmap.md` and confirm the requested `--version` exists as a planned release section.
- If found: proceed.
- If not found: check whether a documented STEP 8.1 Option(b) decision exists for the most recent rebalance. Read the most recent rebalance cycle's `run_manifest.md` (or `cycle_summary.md`) for a `PO decision (STEP 8.1): Option (b) — defer` record.
  - If Option(b) record found: proceed. A documented Option(b) decision from the prior rebalance is equivalent to a formal planned release section for this gate. Record in the run manifest: "§-1.2 cleared via STEP 8.1 Option(b) decision from [rebalance cycle]."
  - If neither a planned release section nor an Option(b) record exists: halt — this routine cannot invent new releases. Either add the release to the roadmap via `run roadmap` (Option(a)) or record an Option(b) decision before invoking release planning.

### -1.3/-1.4 Common Preflight — Roles and Write Test
Apply `claude/system/shared/preflight_common.md` (sub-checks 2 and 3) with:
- required_roles: per Section 6 (Agent Integrity)
- write_test_path: claude/cycles/\<cycle_id\>/.write_test

### -1.5 Prior Cycle Lessons Learnt Closure Check (Advisory — not a hard gate)

Read `.claude_current_state.json` → `prior_cycle`. If `prior_cycle` is set, check:

1. Does `claude/cycles/<prior_cycle>/lessons_learnt_closure.md` exist?
2. If yes: extract all items marked `action: now` (or equivalent `action-now` marker).
3. For each action-now item: verify an entry exists in `claude/system/prompt_change_log.md` referencing that item (by description or IMP reference).

**If any action-now items have no corresponding `prompt_change_log.md` entry:**
- Warn: "⚠ Advisory: [N] action-now item(s) from prior cycle lessons learnt have no matching change log entry." List each missing item.
- Record as an outstanding action in the run manifest.
- **Do not halt.** This is advisory — the release may proceed.

If `prior_cycle` is absent or `lessons_learnt_closure.md` does not exist: skip silently (first cycle or prior cycle pre-dates this check).

### -1.6 Post-Ship Precondition Check (Hard Gate)

Read `.claude_current_state.json`:

- `post_ship_complete` must be `true`. If absent or `false`: halt — prior cycle Post-Ship Closure has not completed. The next release cycle may not open until the prior cycle is fully closed. Run `run post-ship` first.
- `next_cycle_unblocked` must be `true`. If absent or `false`: halt — the prior cycle's Delivery Verification did not set the cycle-unlock flag. This indicates an incomplete or bypassed verification. Resolve the prior cycle's verification state before opening a new release cycle.

This check adds a second layer of safety beyond the lifecycle status guard (`status = Closed`): it ensures that `status = Closed` was set via the legitimate post-ship path, not via a partial write or session crash.

**Exception:** If this is the very first cycle in this repository (no `prior_cycle` field in `.claude_current_state.json`), skip this check.

### -1.7 Prompt Change Log Integrity Check (Advisory — not a hard gate)

Per `shared_standards.md §11`, verify that each governed prompt's current version appears in `claude/system/prompt_change_log.md`:

- For each Class 6 prompt listed in `shared_standards.md §11`: read its `**Version:**` header field.
- Check that the change log contains at least one row with that prompt filename and version.

**If any prompt version is not recorded:**
- Warn: "⚠ Advisory: [prompt name] v[X.Y] has no change log entry." List each missing entry.
- Record as an outstanding action in the run manifest.
- **Do not halt.**

### -1.8 Amendment In Progress Guard (Hard Gate — IMP-11)

Read `.claude_current_state.json` → `status`.

If `status = Amendment_In_Progress`: halt immediately. Output halt report per `claude/system/shared_standards.md §5` (gate: `Amendment_In_Progress`). Resolution: (1) Seal the amendment — re-invoke `amend cycle` until `amendment_state.json.status = Sealed`; (2) or withdraw the amendment and restore the prior state; (3) then re-invoke `plan release --version "<vX.Y>"`. This guard is mode-independent. `--mode standard` does not relax it.

### -1.9 Stale Backlog Lock Preflight Check (Advisory — IMP-16)

Check whether `claude/backlog/.lock` exists before the routine begins. An existing lock from a prior cycle is a signal that a previous Release Planning or Amendment Cycle run did not release the lock cleanly.

**If `claude/backlog/.lock` exists and `owner_cycle_id` ≠ `<this cycle_id>`:**

1. Read the lock file — record `owner_cycle_id`, `acquired_utc`, `acquired_by`.
2. Determine staleness:
   - **Stale condition:** owning cycle is in `Closed` or `post_ship_complete = true` state in `.claude_current_state.json`, **or** `acquired_utc` is more than 72 hours prior to now with no recorded active session.
3. **If stale:**
   - Set `locks.backlog_lock.status = "stale_detected"` in this cycle's `state.json` (if it exists).
   - Surface to PMO Lead: "⚠ Stale backlog lock detected from cycle `<owner_cycle_id>` — acquired `<acquired_utc>`. Owning cycle appears closed. PMO Lead must confirm staleness evidence and manually remove `claude/backlog/.lock` before backlog write steps can proceed."
   - Record the stale detection in this cycle's escalation log (`escalations.md`) as a Lifecycle trigger (advisory — not a hard block at this stage, becomes a hard gate at STEP 4 Precondition).
   - Do not delete the lock automatically.
4. **If not stale (active owning cycle):**
   - Surface to PMO Lead: "⚠ Backlog lock held by active cycle `<owner_cycle_id>`. This cycle will block at STEP 4 unless the lock is released before then."
   - Do not halt here — STEP 4 Precondition will enforce the hard gate.

Reference: `claude/charter/team_charter.md` §6 Shared Write Concurrency Constraint.

---

## STEP 0 — Create Run Manifest + Initialize State (Hard Requirement; must be first write)

**Root `sprint_sealed` reset (ST-23, BLG-GOV-288, v8.5):** This step initialises the *cycle-level* `claude/cycles/<cycle_id>/state.json` only — it never touches the root `.claude_current_state.json` (confirmed: no root-file write exists anywhere in this section). The root pointer's `sprint_sealed` field is reset to `false` for the new cycle at STEP 7's intermediate sync instead, atomically with `active_cycle` switching over — the same single-write-site pattern already used for `design_gate_status` (see STEP 7 for the actual write and full rationale). Noted here because the originating backlog item (`BLG-GOV-288`) named this step; the technically correct write site, matching existing precedent, is STEP 7.

**Cleanup:** If `claude/cycles/<cycle_id>/.write_test` exists (left from STEP -1.4 on a previous interrupted run), delete it now before proceeding.

**Carry-Forward Advisory (ST-15 — per `shared_standards.md §16.8`):**
Before creating the run manifest, check the most recently completed cycle's `lessons_learnt_closure.md` for a `## Carry-Forward` section. "Most recently completed" = highest YYYY-MM-DD cycle ID with `post_ship_complete = true` in `.claude_current_state.json`. If the section is present and non-empty: surface each item as an advisory in session output; record in `run_manifest.md` as "Carry-forward items reviewed: N items from cycle `<cycle_id>`." If absent or zero rows: record "No carry-forward items from prior cycle `<cycle_id>`." Do not halt — advisory only.

**scored_initiatives.md Load (ST-14 — per `shared_standards.md §16.7`):**
Load `claude/scoring/scored_initiatives.md` if it exists. Extract `Effort Band` values for initiatives matching the current release scope items. Record in `run_manifest.md` as "scored_initiatives.md: N matching items with effort band / not present or no matching items." This is a read-only load — no write to `claude/scoring/*` at this step.

Create:
- `claude/cycles/<cycle_id>/run_manifest.md`

Class: Operational Record (Class 3)

Owner: Infrastructure & Operations Owner

Status: Filed

Header (required fields):
- Owner: Infrastructure & Operations Documentation Owner
- Status: Operational Record
- Deployment Version: N/A
- Report Date: <date>
- Environment: Governance
- Generated By: Claude Code (Release Planning Engine)
- Filed: <date filed>

Then create or update:
- `claude/cycles/<cycle_id>/state.json`

### state.json initialization

Initialize per `claude/system/schemas/release_state_schema.json`. Set the following fields from invocation parameters:
- `cycle_id`, `release`, `date`, `mode`, `issues_mode`, `auto_escalate`
- `status = "Initialized"`, `publish_eligible = false`, `last_transition_utc = <now UTC>`
- `assumptions.timebox`, `assumptions.capacity` from invocation (or empty)
- `locks.backlog_lock.marker = "RP:<release>:<cycle_id>"`
- `locks.roadmap_lock.marker = "RA:<release>:<cycle_id>"`
- `artifacts.run_manifest = "present"`
- All other fields at their schema defaults.

Reserved fields `design_gate_status` and `amended_backlog_slice_path` are initialized to schema defaults only — see `_notes` in the schema file.

If the run manifest cannot be written in a lifecycle-compliant way: halt immediately.

If `state.json` cannot be created/updated: halt immediately.

Update state:
- status = `Initialized`
- artifacts.run_manifest = `present`
- assumptions.timebox = value from invocation (or empty)
- assumptions.capacity = value from invocation (or empty)
- locks.backlog_lock.marker = `RP:<release>:<cycle_id>`
- locks.roadmap_lock.marker = `RA:<release>:<cycle_id>`

---

## RESUME RULE (State-Driven Execution)
If `state.json` exists:
- Continue from the first step whose artifact status is `not_started` or `fail` or `blocked`.
- Do not rerun steps marked `pass`.

If status is `Blocked`:
- Invoke Escalation Handling Subroutine first.
- If all required escalations are resolved/deferred/accepted-risk per rules, resume from the appropriate next step.

If `state.json` is missing but artifacts exist:
- Rebuild state from artifacts:
  - mark as `pass` any stage file present that satisfies the step's requirements
  - otherwise mark as `not_started`
- Write `state.json` and continue.

---

## Terminal State Guard — Published Is Immutable (Hard Gate)

**(Extracted from the former RESUME PRECHECK block, ST-22, BLG-GOV-124, EPIC-05, v8.3 — the mutation-detection/invalidation-map machinery that block also contained was removed; see `sprint_planning_notes.md`-equivalent rationale in `prompt_change_log.md`. This gate and the State File Immutability Rule below it are unaffected by that removal and continue to apply on every resume, per the RESUME RULE above.)**

If `state.json.status == "Published"`:
- Treat the cycle folder as **sealed**.
- Do NOT re-run any steps.
- Do NOT modify any stage artefacts in this cycle.
- Do NOT append to or modify `escalations.md`.
- Do NOT change assumptions (timebox/capacity).
- Do NOT acquire locks (backlog/roadmap) or perform lock/txn steps.

### State File Immutability Rule (Hard Gate)
If `status == Published`:
- `state.json` may not be modified.
- open_escalations must not change
- deferred_escalations must not change
- accepted_risk_escalations must not change
- deferred_execution_blockers must not change

Drift detection: use `git diff main` to verify no files in the cycle folder have been modified after the publish commit.

If drift found: HALT with instruction:
- "Published cycle has drift. Do not modify this cycle. Create a new amendment cycle and reference this published cycle_id."

If no drift found: HALT with message:
- "Cycle is Published and sealed. No further action permitted in this cycle."

---

### Shared Write Recovery (Hard Gate)

Apply `claude/system/shared/lock_recovery_procedure.md` for each resource that has a lock or acquired state:

**Backlog recovery:** `{resource: backlog, lock_file: claude/backlog/.lock, marker_value: RP:<release>:<cycle_id>, marker_key: release-plan-marker, txn_file: claude/cycles/<cycle_id>/backlog_txn.json, artifact_key: backlog_lock, resume_step: STEP 4}`

**Roadmap recovery:** `{resource: roadmap, lock_file: claude/roadmap/.lock, marker_value: RA:<release>:<cycle_id>, marker_key: roadmap-annotation-marker, txn_file: claude/cycles/<cycle_id>/roadmap_txn.json, artifact_key: roadmap_lock, resume_step: STEP 4.95/5}`

---

## Drift Detection
Trigger: only when `status == Published`.

Per-artefact hash comparison removed (ST-17, v2.4). Drift detection for Published cycles uses `git diff main` — any modified files in the cycle folder after the publish commit constitute drift.

If drift found:
- HALT with instruction: "Published cycle has drift. Create amendment cycle."

No repair allowed in published cycle.

---

## ESCALATION HANDLING SUBROUTINE — Callable (Delegated Authority)

Full procedure: `claude/system/shared/escalation_subroutine.md`.

**Trigger:** Any step produces ⛔ Blockers AND `--auto-escalate=true`, OR `status=Blocked`.

**Engine-specific additions (beyond shared subroutine):**
- ESC entries in `escalations.md` store decision/status only. Full risk context lives in `release_plan.md §Execution Plan` via the `escalation_ref` field on each RISK-ID row.
- When escalations.md is created: `artifacts.escalations = present`.
- Escalation Freeze Rule: If `status == Published`, `escalations.md` becomes read-only — any append → HALT.
- **Structural append-verification (BLG-GOV-168):** Apply the Structural Append-Verification Procedure per `shared_standards.md §7.1` at every append to `escalations.md` (count before/after, confirm exactly +1, confirm no prior entry text changed — halt on either failure).

---

# Steps

## STEP 1 — Release Readiness Validation

Write: `## Readiness` section in `release_plan.md` (create the file if this is the first step; append the section if resuming)

### 1.1 Backlog Age Advisory (Advisory — not a hard gate)

After writing the Readiness section, scan `claude/backlog/backlog.md` for spec/documentation debt items (items classified as spec debt, documentation debt, or equivalent) that appear in the active backlog slice for this release.

For each such item, check how many prior release cycles it has appeared in without receiving a story assignment (i.e., no `ST-xx` in the sprint_backlog of any prior cycle). A cycle count of ≥ 2 without a story assignment triggers a warning.

**If any spec/documentation debt item has been in the backlog for 2+ cycles without a story assignment:**
- Warn: "⚠ Advisory: [N] spec/documentation debt item(s) aged 2+ cycles without story assignment: [list items]."
- Recommendation: These items should be promoted to sprint stories (assigned an `ST-xx` ID and added to `stage4_backlog_slice.md`) if the release scope permits. Items not assigned a story ID will not enter sprint planning.
- Record as an advisory note in the run manifest.
- **Do not halt.** This is advisory only — the release may proceed.

If no such items are found, or backlog cannot be dated reliably: skip silently.

### 1.2 Provisional-Target Advisory (Advisory — not a hard gate)

After writing the Readiness section, scan backlog candidates for this release for the `**Provisional-Target:**` field (per `shared_standards.md §16.6`).

- Count items with `Provisional-Target: v<current_release>` (horizon-planned for this release).
- Count items with `Provisional-Target: TBD`, `Provisional-Target: Unscheduled`, or field absent.
- Emit advisory: "ℹ N item(s) carry `Provisional-Target: <current_release>` — horizon-planned for this release. M item(s) have no matching Provisional-Target signal."
- Record as an advisory note in the run manifest.
- **Do not halt.** Scope selection authority remains at STEP 2.

### 1.3 Design-Gate Language Scan (Advisory)

Scan scope candidates for design-gate language ("design decision required", "pending design", "requires UX decision"). Flag items as "Design dependency detected — surface at Pre-sprint Required Decisions checklist." Non-blocking.

### 1.3a Gate-Detection Procedure (Mandatory, Scripted)

Before running the Perennial-Return Check (§1.4a) or any other step that reasons about "conditional or gate-blocked" candidate items, run the canonical scripted gate-detection procedure:

```
python3 scripts/scan_backlog_gate_conditions.py
```

This replaces ad hoc reading of each candidate's fields, which produced 3 self-caught scan misses across 3 consecutive Release Planning cycles (`v8.0`, `v8.1`, `v8.2` — see `BLG-GOV-286`) plus a 4th failure mode self-caught while building this fix (`v8.4`): a missing `---` separator between two adjacent backlog entries let one item's body text bleed into the next item's field scan.

**What the script does (see the script's own docstring for full detail):**
1. Splits `claude/backlog/backlog.md` into item blocks using the next `### BLG-` (or `### TEST-GAP-`) heading as the boundary — **never** the `---` separator, which is not 100% consistently present (structurally eliminates the missing-separator failure mode rather than merely detecting it).
2. For each item, checks for a gate condition across every observed field-name variant, in order: `**Gate criteria:**`, `**Gate:**`, `**Gate date:**`.
3. If none of those fields are present, checks whether `**Provisional-Target:**` contains gate-like free text (e.g. "gated", "no earlier than", "conditional", "pending") with no formal Gate field backing it — this is flagged as a **data-quality warning**, not treated as gated, since the canonical fix is adding a proper Gate field to that item (the `BLG-OPS-48` pattern that caused 2 of the 3 original misses).

**Use the script's output** — the gated-item list and any data-quality warnings — as the input to §1.4a's "check each conditional or gate-blocked candidate item" step, rather than re-deriving the list by eye. Record the gated-item count and any data-quality warnings found in `run_manifest.md`.

**Not a hard gate:** the script always exits 0 — it is a scan/report tool, not a CI gate. A data-quality warning does not block release planning; it is a flag for a future `groom backlog` pass to correct the source item's fields.

### 1.4a Perennial-Return Check (Advisory — triggers PO active disposition)

Before finalising the scope candidate list, check each conditional or gate-blocked candidate item (per §1.3a's scripted scan output):

1. Does this item appear in the prior cycle's `stage4_backlog_slice.md` with status `returned_to_backlog`, `deferred`, or equivalent? If yes, increment a consecutive-return counter.
2. If returned in **2 or more consecutive prior cycles** (including the current cycle): surface to Product Owner as "⚠ Perennial-Return Item — returned N consecutive cycles."
3. PO must make an **explicit active disposition**:
   - (a) Keep as conditional — provide updated gate evidence or a revised gate date that differs from prior cycles
   - (b) Remove from horizon — park in backlog until gate permanently cleared
   - (c) Resolve directly this cycle — promote to firm scope and complete it now, for low-effort items where the cheapest fix is closure rather than further deferral or parking
4. Silent re-entry (no active PO disposition when N ≥ 2) is **not permitted**. Record PO decision in `run_manifest.md`.

This check is advisory-only — it does not halt execution. It prevents backlog churn on items that recurrently fail to execute due to unchanged gate conditions.

### 1.4a.1 Sunset Criteria (Mandatory — supersedes indefinite Option (a) re-parking)

The Perennial-Return Check above is advisory at every threshold: the PO may choose Option (a) "keep conditional" indefinitely, cycle after cycle, with no upper bound. This subsection adds a hard ceiling so a perennially-returning item cannot occupy conditional/gated status forever without ever forcing a real disposition.

1. **Sunset trigger:** When an item has received Option (a) "keep as conditional" **4 consecutive times** (i.e., the Perennial-Return Check has fired and the PO chose (a) on 4 consecutive cycles, counting from the cycle the check first fired — not from the item's original filing), the disposition escalates from advisory to **mandatory**.
2. **Mandatory choice at the sunset trigger:** The PO must choose Option (b) "Remove from horizon — park until gate permanently cleared" (a formal Kill-from-active-consideration, not silent continuation), **unless** the PO documents a *materially new* gate-clearance path that did not exist at any prior disposition. "Materially new" means: a concrete, named forthcoming event or change (not "more data will accrue naturally" restated) together with a specific date or trigger by which it is expected to resolve the gate.
3. **Recording:** Record the sunset-trigger disposition (forced (b), or the materially-new path accepted in lieu) in `run_manifest.md`, same as any Perennial-Return Check disposition.
4. **Rationale:** 4 was chosen as double the 2-cycle advisory trigger — giving the PO two additional full cycles of visibility past the first advisory flag before a forced disposition, while still guaranteeing the item cannot coast on option (a) indefinitely. This closes the gap where a P1-priority item can sit "conditional" at zero delivery cost release after release without ever crossing a threshold that forces a genuine kill-or-fix decision.

**Retroactive assessment (2026-08-03, ST-03, BLG-GOV-280):** Applied against `BLG-FEAT-73` and `BLG-FEAT-74`, the two items the Perennial-Return Check has actively flagged. Counting from the cycle the check first fired for each item:
- `BLG-FEAT-73` (SI-02 frontend build): flagged at `2026-07-30__release-v8.0` (1st) and `2026-08-03__release-v8.1` (2nd, current) — Option (a) both times. **2 of 4** consecutive (a) dispositions elapsed. Below the sunset trigger; no forced (b) required yet.
- `BLG-FEAT-74` (PO-05 Lightweight Replay Mode): same two flagged cycles, same count — **2 of 4** elapsed. Below the sunset trigger.
- Neither item is currently subject to a forced Option (b). Both remain correctly on Option (a) under existing PO dispositions. This assessment is a status check, not a new disposition — the PO's existing conditional-keep dispositions for both items stand unchanged. If either item receives a 3rd and 4th consecutive Option (a) at the next two rebalances with no materially new gate-clearance path, the sunset trigger becomes mandatory at that point.

---

### 1.4b Within-Sprint Date Gate Classification (Mandatory)

Before finalising sprint capacity and scope classification, identify any candidate item where the gate condition's earliest clearing date falls **within the planned sprint execution window** (i.e., between sprint start and planned sprint close):

1. **Definition — within-sprint date gate:** A gate condition whose clearing date is a specific calendar date that falls on or after sprint start AND on or before the planned sprint close.
2. **Mandatory classification rule:** Any item with a within-sprint date gate **must** be classified as **conditional** in the release plan and sprint backlog. It may **not** be classified as firm capacity, regardless of how likely the gate is to clear.
3. **Promotion path:** The item may be promoted from conditional → firm only when the gate owner **explicitly confirms** the gate condition has been met (dated confirmation recorded in `run_manifest.md` or sprint planning artefact).
4. **Record:** For each within-sprint date gate item, record in the run manifest: item ID, gate condition, gate clearing date, and "classified: conditional."

**Rationale (why mandatory):** This rule was filed as advisory (LL-P3-03-v55, v5.5 post-ship) and elevated to mandatory after the pattern recurred across five consecutive releases: v5.4 ST-03, v5.5 ST-11–14, v5.6 ST-03, v5.7 ST-09/ST-12–14, v5.8 ST-01/ST-02 — all returned to backlog at sprint close because a within-sprint date gate was not met. Items classified as firm with a within-sprint date gate predictably return to backlog. This rule eliminates the source of that return pattern. Applied action-now: rebalance 2026-06-17__scheduled (LL-P3-03-v55/LL-P4-01-v55 overdue).

**Violation:** A firm-classified item returned to backlog at sprint close due to a within-sprint date gate is a P2 process deviation and must be filed as a BLG-GOV deviation record for the next delivery verification cycle. Recurrence across two sprints escalates to Head of Specs Team.

---

### 1.4 Gate-Condition Proximity Scan (Advisory — not a hard gate)

After the design-gate scan, scan all gate-conditional backlog items in `claude/backlog/backlog.md` for items where the gate condition is likely to clear within 30–60 days given current trajectory. Output a gate proximity table in the run manifest.

**Gate proximity table format:**

`| Item | Gate condition | Current trajectory | Projected clear date |`

For items without a calculable trajectory: record "trajectory unknown" in the Current trajectory column.

**Arc 4 data density sub-check (mandatory within STEP 1.4):**

Check the following current data density metrics (query from production or estimate from trade frequency signals in the run manifest):
- Current closed trade count and monthly rate (relevant to PO-04 gate: 50+ trades with plans)
- AI journal entry count and monthly generation rate (relevant to PO-02 gate: 6+ months AI journals)
- Trade plan creation rate (plans/month; relevant to SI-02 gate: 20+ trades with plans)

Surface projection: estimated gate-clearing dates for:
- PO-02 (6+ months AI journal entries): `[current_count] entries at [rate]/month → projected [date]`
- PO-04 (50+ trades with plans): `[current_count] at [rate]/month → projected [date]`
- SI-02 (20+ trades with plans): `[current_count] at [rate]/month → projected [date]` — Product Owner to confirm or update

Record projected dates in the gate proximity table. If data is unavailable: record "data not available — Product Owner to surface at readiness review."

**Do not halt.** This is advisory only — the release may proceed regardless of proximity table results.

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass|fail|blocked
```

---

## STEP 2 — Scope Extraction (No Scope Changes Allowed)

Write: `## Scope` section in `release_plan.md` (S2 IDs required)

**Scope document (required output):**

Create: `docs/product/scope/scope--{cycle_id}-{slug}.md` per `claude/system/templates/scope_document_template.md`.

Populate: `Release`, `Cycle`, `Last Updated`, `Items in scope` table (S2-IDs required), `Items explicitly deferred`. Leave `Supersession note` section unpopulated (completed at Post-Ship Closure).

This document is the authoritative scope record for Post-Ship Closure Step 4 supersession. If not created here, the post-ship closure engine will flag it as missing.

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass|fail|blocked
artifacts.stage2_scope_document: present|missing
```

---

## STEP 3 — Execution Plan + Decisions Record

Write: `## Execution Plan` section in `release_plan.md` (EPIC IDs + Maps to + RISK IDs required)

**Format constraint (IMP-08 — token efficiency):** The `## Execution Plan` section must use a compact table format rather than narrative prose. Full acceptance criteria belong exclusively in `stage4_backlog_slice.md`. Target: the complete `release_plan.md` should remain under 200 lines.

Required table format for each EPIC:

```
| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02 | <role> | RISK-01 | After EPIC-02 |
```

If an EPIC has significant sequencing rationale or dependency notes that cannot fit in the table, append a brief note (2–3 lines maximum) below the table row, prefixed with the EPIC-ID. Full dependency maps belong in `sprint_planning_notes.md`.

**Skill-Silo mitigation — execution-heavy assignment rotation (advisory, added v2.46 — ST-07, BLG-GOV-246):** `roadmap_prompt.md` §7.1's Skill-Silo Alert fires when the rolling 3-cycle governance/debt story share exceeds 40%, and its "Mandatory pull-forward on sustained failure" clause forces at least 2 build-and-ship U-items once the alert has worsened or held for 3+ consecutive readings. This guideline adds a lighter-weight, earlier-acting companion at the *scoping* stage rather than waiting for the 3-reading mandatory trigger: as a soft target, aim for **at least 1 in every 3 release cycles** to lead its `## Execution Plan` EPIC table with execution-heavy (build-and-ship U-shaped) scope by default, rather than governance/debt-heavy scope. This is a rotation heuristic, not a hard gate — it does not block STEP 3 from passing. **Trigger condition:** this guideline is explicitly tied to the same STEP 7.1 Skill-Silo Alert reading — when the most recent rebalance reported the alert as fired (>40%) or worsening, weight the next release's EPIC table selection toward execution-heavy scope as this cycle's "1 in 3" rotation slot, rather than treating rotation as an independent unscheduled preference. Owner: Director of HR (rotation-pattern fairness across the release cadence is an HR-domain concern, distinct from PMO Lead's capacity-sequencing ownership of the table itself).

**Risk register format (required alongside EPIC table):**

After the EPIC table, write a `### Risk Register Summary` subsection. Each RISK-ID referenced in the EPIC table must appear as a row:

```
| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | <description> | High/Medium/Low | <mitigation action> | null |
| RISK-02 | EPIC-01 | <description> | Low | <mitigation action> | ESC-YYYYMMDD-nn |
```

`escalation_ref`: set to `null` if no escalation has been raised for this risk. Set to the ESC-id if an escalation was raised. This keeps ESC entries lean — they store decision/status only; the full risk context lives here via the back-link.

**Decisions record (required output):**

Create: `docs/product/decisions/decisions--{cycle_id}.md` per `claude/system/templates/decisions_record_template.md`.

Populate: `Release`, `Cycle`, `Last Updated`, scope decisions, sequencing decisions, accepted risks (from any Accepted Risk escalations in this cycle; "None" if none). Leave `Supersession note` unpopulated (completed at Post-Ship Closure).

This document is the authoritative planning decisions record for this release. If not created here, the post-ship closure engine will flag it as missing.

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass|fail|blocked
artifacts.stage3_decisions_record: present|missing
attributes.plan_structured: true          # on pass
status: Planning                           # when Stage 3 passes
```

---

## STEP 3.5 — Local Model Integrity Check (Conditional Gate)

Classification: Conditional Gate (halts only if escalation remains Open / blocking)

Write: `## Integrity Validation — 3.5 Local Model Integrity` subsection in `release_plan.md`

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass|fail|blocked
attributes.plan_executable: true   # on pass
```

---

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

1. If `claude/backlog/.lock` does NOT exist: create with contents `{cycle_id, release, acquired_utc, acquired_by: "Release Planning Engine"}`.

```yaml
# state.json update — lock acquired:
locks.backlog_lock: { owned: true, owner_cycle_id: <cycle_id>, owner_release: <release>,
  acquired_utc: <ISO-8601 UTC>, status: acquired, marker: "RP:<release>:<cycle_id>" }
artifacts.backlog_lock: acquired
```

2. If `claude/backlog/.lock` exists:
   - Read `owner_cycle_id`. If `== <cycle_id>`: re-entrant — proceed (`artifacts.backlog_lock = acquired`).
   - If `!= <cycle_id>`: record ⛔ Blocker (PMO Lead; unblock: "manually release or declare stale"), include lock contents as evidence. If `--auto-escalate=true`: invoke Escalation Handling Subroutine.

```yaml
# state.json update — lock blocked:
locks.backlog_lock: { owned: false, owner_cycle_id: <from lock file>,
  owner_release: <from lock file>, status: blocked }
artifacts.backlog_lock: blocked
# → HALT
```

Stale protocol (detect only; do not clear):

- If lock appears stale based on timestamp threshold defined by PMO Lead, you may:
  - set locks.backlog_lock.status = "stale_detected"
  - set artifacts.backlog_lock = "stale_detected"
  - create a blocker requiring manual stale resolution
- You may not delete or overwrite the lock automatically.

---

## STEP 4 — Backlog Slice (commitment)

Write: `stage4_backlog_slice.md` + update backlog slice section

### STEP 4 Precondition — Backlog Lock Required (Hard Gate)

Before writing to `claude/backlog/backlog.md`:

- Verify `claude/backlog/.lock` exists AND contains owner_cycle_id == `<cycle_id>`.
If not true:
- Record a ⛔ Blocker (Lifecycle / Process Integrity; owner: PMO Lead)
- Invoke escalation subroutine if auto-escalate=true
- HALT

### Backlog Section Marker (Required for Idempotency)

When writing the release slice section into `claude/backlog/backlog.md`, include this HTML comment marker inside the section:

- `<!-- release-plan-marker: RP:<release>:<cycle_id> -->`

### STEP 4 Transaction — Prepare (Hard Requirement)

Create or update:

- `claude/cycles/<cycle_id>/backlog_txn.json`

Set to "prepared" BEFORE any modification to `claude/backlog/backlog.md`.

Minimum required fields:

- cycle_id: `<cycle_id>`
- release: `<release>`
- txn_id: `BLTX-<YYYYMMDD>-<nn>`
- state: `prepared`
- prepared_utc: `<ISO-8601 UTC>`
- marker: `RP:<release>:<cycle_id>`
- target_file: `claude/backlog/backlog.md`

Update `state.json`:

- locks.backlog_lock.txn_state = "prepared"
- artifacts.backlog_txn = "prepared"

### STEP 4 Idempotency Rule (Hard Requirement)

Before inserting/appending the release slice section:

- Search backlog for marker:
- `<!-- release-plan-marker: RP:<release>:<cycle_id> -->`

If marker is found:

- Do NOT write the section again.
- Treat backlog update as already completed for this cycle.
- Proceed to Transaction Commit + Lock Release.

If marker is not found:

- Write the release slice section once, including the marker.

### STEP 4 Transaction — Commit (Hard Requirement)

After backlog write completes successfully (or marker already present):

- Update `claude/cycles/<cycle_id>/backlog_txn.json`:
  - state: `committed`
  - committed_utc: `<ISO-8601 UTC>`

Update `state.json`:

- locks.backlog_lock.txn_state = "committed"
- artifacts.backlog_txn = "committed"

**Issue Manifest (IMP-24):** After `stage4_backlog_slice.md` is written, also produce:

`claude/cycles/<cycle_id>/stage4_issue_manifest.json`

Schema: see `claude/system/shared_standards.md §16.2`.

One entry per ST item in `stage4_backlog_slice.md`. The `cycle:<cycle_id>` label is the idempotency key for GitHub issue creation (§10.2).

```yaml
# state.json update (STEP 4 outcome):
artifacts.stage4_backlog_slice: pass|fail|blocked
artifacts.stage4_issue_manifest: pass|fail|blocked
attributes.backlog_committed: true          # on pass
attributes.design_gate_required: true|false # set in STEP 4.1 below
status: Committed                           # on pass
```

### STEP 4.1 — Design Gate Classification (Required — same session as STEP 4)

After writing `stage4_backlog_slice.md`, scan all ST items for UI-facing scope:

**Classification rule:**
- `design_gate_required = true` if ANY item has delegation class `delegated_frontend` OR is `autonomous` with at least one observable UI acceptance criterion (visible rendering, element presence/absence, colour, interaction, timing)
- `design_gate_required = false` if all items are backend, spec/documentation, CI/infrastructure, or autonomous with no observable UI ACs

**Required output:**
- If `design_gate_required = true`: output `⚠ DESIGN GATE REQUIRED before plan sprint — N items classified as UI-facing. Run: run design-gate --cycle <cycle_id>`
- If `design_gate_required = false`: output `Design Gate: Not Required — proceed directly to plan sprint`

**Required state updates (same session — Hard Requirement):**
```yaml
# state.json:
attributes.design_gate_required: true|false
```

If `design_gate_required = false`: set `design_gate_status = "not_required"` in `state.json` (via `attributes.design_gate_status`, mirrored to `.claude_current_state.json` at STEP 7 as below).

**Note (LP-01 fix, v2.41 — resolves 2-cycle recurrence):** Do **not** write `design_gate_required`/`design_gate_status` to `.claude_current_state.json` here. Writing it at STEP 4.1 — before `active_cycle` has been advanced to this cycle at STEP 7 — creates a transient window where `.claude_current_state.json` carries this cycle's design-gate fields while `active_cycle` still points at the just-closed prior cycle, overwriting that cycle's own completed design-gate record. `.claude_current_state.json` is updated for this field once only, atomically with `active_cycle`, at STEP 7's intermediate sync (see STEP 7).

### STEP 4 Postcondition — Release Backlog Lock (Strict)

After successfully completing STEP 4 (txn committed):

- Remove `claude/backlog/.lock`
- Update `state.json`:
  - locks.backlog_lock.status = "released"
  - locks.backlog_lock.owned = false
  - artifacts.backlog_lock = "released"

If the environment does not permit removing the lock file:

- Record a blocker and HALT (lock cannot be left ambiguous).

---

## STEP 4.5 — Capacity Feasibility Sense Check (Conditional Gate)

Classification: Conditional Gate (halts only if escalation remains Open / blocking)

Write: `## Capacity Check` section in `release_plan.md`

**Effort Band Lookup (ST-14 — per `shared_standards.md §16.7`):**
For each EPIC in scope, apply the three-tier resolution rule before deriving effort estimates:
1. If a pre-assigned `Effort Band` was loaded from `scored_initiatives.md` at STEP 0 for this EPIC: use it as the primary sizing input; note "from scored_initiatives.md".
2. If the initiative has a row in `scored_initiatives.md` but no `Effort Band` value: emit advisory "⚠ [N] EPIC(s) have no effort band in scored_initiatives.md — falling back to inline estimate." Use STEP 4 estimate.
3. If no matching row in `scored_initiatives.md`: use STEP 4 estimate; no advisory required.

### When outcome is WARN — Phasing Recommendation (Required)

When `artifacts.stage4_5_capacity_check = warn` (total estimated effort exceeds available capacity but the release is not infeasible), the `## Capacity Check` section of `release_plan.md` **must** include a `### Phasing Recommendation` subsection. This subsection must:

1. State the estimated total effort (mid-point hours) and available capacity (hours).
2. Propose a concrete phasing approach for sprint planning — for example:
   - `Phase 1 (Sprint 1): EPIC-xx, EPIC-yy — estimated N hrs (within capacity)`
   - `Phase 2 (Sprint 2): EPIC-aa, EPIC-bb — estimated M hrs (within capacity)`
3. Note the ordering rationale (dependencies, risk, user value).

This makes the WARN actionable: sprint planning can adopt the phasing recommendation directly rather than discovering over-allocation at sprint planning time.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass|warn|fail|blocked
attributes.capacity_feasible: pass|warn|fail|blocked
```

---

## STEP 5 — Roadmap Annotation

Purpose: Record that planning is underway for this release by adding execution notes to the roadmap entry. This does not change scope, priority, or strategy — it adds a link to the cycle folder and current status.

Write: Update `claude/roadmap/current_roadmap.md` — under the existing release section only. If no formal `## vX.Y` roadmap section exists for this release (e.g. an Option (b)-deferred release with no dedicated section yet), annotate the `**Next planned release:**` line in §1 (Current Version) instead.

Required annotation content (append under the release section heading; do not modify any other content):

```markdown
<!-- roadmap-annotation-marker: RA:<release>:<cycle_id> -->

**Execution notes (added by Release Planning Engine):**
- Cycle: <cycle_id>
- Plan published: <date>
- Cycle folder: claude/cycles/<cycle_id>/
- Backlog slice: claude/cycles/<cycle_id>/stage4_backlog_slice.md
- Status at annotation: <macro-state at time of annotation>
```

Lock and transaction procedure:

1. Acquire `claude/roadmap/.lock` with marker `RA:<release>:<cycle_id>` (same rules as backlog lock — halt if held by different cycle_id; re-entrant if same).
2. Create or update `claude/cycles/<cycle_id>/roadmap_txn.json` — set state = "prepared" before writing.
3. Write the annotation (idempotent — check for existing marker before writing; do not write twice).
4. Update roadmap_txn.json: state = "committed".
5. Release lock (see postcondition below).

```yaml
# state.json update (STEP 5):
artifacts.roadmap_txn: committed            # on success
locks.roadmap_lock.status: released         # on success
```

### STEP 5 Postcondition — Release Roadmap Lock (Strict)

After roadmap_txn state = committed:

- Remove `claude/roadmap/.lock`
- Update state.json:
  - locks.roadmap_lock.status = "released"
  - locks.roadmap_lock.owned = false
  - artifacts.roadmap_lock = "released"

If removal fails:
- Record blocker and HALT.

---

## STEP 5.5 — Integrity Validation (Hard Gate)

Run both integrity checks and write results as subsections of `release_plan.md`:

**5.5 Cross-Stage Integrity:** Verify all S2 IDs map to EPICs, all EPIC IDs in backlog slice match stage3, all RISK IDs in EPIC table appear in Risk Register, no orphaned references.

**5.7 Decision Record Integrity** (SC-05 — run only when `artifacts.escalations = present` in state.json; skip if no escalations were raised): Verify `decisions--{cycle_id}.md` is present, all AR/SRB records referenced in escalations exist at their declared paths, all mandatory template fields are populated.

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass|fail|blocked
artifacts.stage5_7_decision_record_integrity: pass|fail|blocked|not_applicable
attributes.cross_stage_integrity: pass|fail|blocked
attributes.decisions_validated: pass|fail|not_applicable|blocked
```

*(NOTE: rerun only if Stage 2/3/4 artefacts changed)*

---

## STEP 7 — Cycle Summary

Write: `cycle_summary.md`

### Pre-sprint Planning Required Decisions (Conditional — include when applicable)

Before writing `cycle_summary.md`, review all risks in `release_plan.md §Execution Plan` (STEP 3 output). For any risk classified as **High priority** with a disposition of "must resolve before sprint planning seal" (or equivalent — the risk explicitly blocks sprint planning):

Include a `## Pre-sprint Planning Required Decisions` section in `cycle_summary.md` with a checklist entry for each such risk. Format:

```markdown
## Pre-sprint Planning Required Decisions

The following High-priority decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-xx] <Risk title> — <Required decision / resolution path> — Owner: <role>
```

If no High-priority risks have a "must resolve before sprint planning seal" disposition: omit this section (do not write an empty section).

This checklist is designed to be consumed by the Sprint Planning Engine at its preflight step — making explicit what must be decided before the sprint plan can be sealed.

**Intermediate global state sync (required before writing cycle_summary.md):**

> **Resume check (unrelated to the former RESUME PRECHECK mutation-detection block, removed ST-22/v8.3):** If the session was resumed via context compaction and STEP 7 has completed without the intermediate sync being performed, execute the intermediate sync immediately before proceeding to STEP 8. Do not proceed to STEP 8 with stale `.claude_current_state.json` state from the prior cycle.

Before writing `cycle_summary.md`, update `.claude_current_state.json` to reflect the current in-progress state. This is a pre-publish sync — it does not mark the cycle Published. Its purpose is to ensure the global state pointer reflects the active cycle if the session is interrupted before STEP 9.

```yaml
# .claude_current_state.json intermediate sync (STEP 7 — pre-publish only):
active_cycle: <cycle_id>
status: <current macro-state>       # e.g. Validated — NOT Published
backlog_slice_path: claude/cycles/<cycle_id>/stage4_backlog_slice.md
design_gate_required: true|false          # LP-01 fix, v2.41 — carried from state.json attributes.design_gate_required (set at STEP 4.1); written here, atomically with active_cycle, not at STEP 4.1
design_gate_status: "not_started"|"not_required"   # LP-01 fix, v2.41 — "not_started" if design_gate_required=true and not yet run, else "not_required"
sprint_sealed: false          # ST-23 fix, v2.49, BLG-GOV-288 — reset here, atomically with active_cycle switching to the new cycle_id, same pattern as design_gate_status above. sprint_sealed is owned and set true only by sprint_planning_prompt.md's own seal for THIS cycle — nothing else may ever write true here. Without this reset, the field carries a stale true from the prior cycle's seal into the new cycle's pre-planning window (observed live at the 2026-08-07__release-v8.4 design gate: root sprint_sealed read true, carried from v8.3, while the v8.4 cycle-level state.json correctly had no sprint_sealed key at all).
last_sync_utc: <ISO-8601 UTC now>
```

STEP 9 (Global State Synchronization) is the terminal sync and is the only step that sets status = `Published`. Do not set Published here.

**`cycle_summary.md` header must include `design_gate_required` status line (AC-05):** When writing `cycle_summary.md`, include the following line in its header metadata block:

```
Design Gate Required: true | false | not_required
```

Source: `attributes.design_gate_required` from `state.json` (set in STEP 4.1). Use `not_required` if the field is absent (prior-cycle artefact without STEP 4.1 classification).

---

## STEP 8 — Lessons Learnt

Write: `lessons_learnt.md`

The lessons learnt file must end with an `// ARTEFACT_STATUS` JSON terminal block. Schema: per `claude/system/roadmap_prompt.md` §11 — use `"phase": "Release"`.

---

## STEP 9 — Global State Synchronization (Hard Requirement — Terminal)

Purpose: Final update of the root-level state pointer to reflect that this cycle's release plan is published and sealed. This is the only step that sets `status = Release_Planning_Complete` in `.claude_current_state.json`. STEP 7's intermediate sync must have run first.

Note: "Published" is the release plan's own cycle-level `state.json.status` value (see §6B.6 Publish Gate) — it is distinct from the root-level `.claude_current_state.json.status` field written here, which must use the canonical `lifecycle_schema.json` state-enum value `Release_Planning_Complete`, not `Published` or `Validated`. Per `shared_standards.md` §10.6, `lifecycle_schema.json` prevails on any conflict between the two vocabularies.

**`next_release` ownership (OA-1, post-ship closure `2026-07-24__release-v7.8`):** This step is the sole authoritative writer of `.claude_current_state.json.next_release`. It was found 4 releases stale (stamped from a prior cycle) at the start of the v7.8 Release Planning session because no engine explicitly owned the field's upkeep — `roadmap_prompt.md` STEP 8 only ever writes it advisorily (best-effort pre-fill, skipped entirely on a no-change rebalance with no determinable next release label), and nothing else in the observed chain (`plan release`, post-ship closure) wrote it at all. STEP 9 below now writes it unconditionally, from this invocation's own `--version` argument, every time Release Planning seals — this is the authoritative source, not `roadmap_prompt.md`'s advisory pre-fill, which remains useful only as an early best-guess signal before this step next runs.

Execution Rules:
1. Verify STEP 7 intermediate sync has completed (backlog_slice_path and active_cycle are already set).
2. If `.claude_current_state.json` does not exist, create it using the standard schema.
3. Terminal state update:

```yaml
# .claude_current_state.json terminal update (STEP 9 — sets Release_Planning_Complete):
active_cycle: <cycle_id>            # confirm — already set at STEP 7
status: Release_Planning_Complete
backlog_slice_path: claude/cycles/<cycle_id>/stage4_backlog_slice.md   # confirm
next_release: <--version argument, e.g. v7.8>   # authoritative write — this step owns this field (OA-1)
last_sync_utc: <ISO-8601 UTC now>
```

---

## STEP 10 — Stage, Commit & Push (Delegated Publication)
Purpose: Publish the sealed cycle and updated state to the remote repository.

### 10.1 Issue Import Generation (`--issues import` or `gh` fallback)
If `--issues import` was specified, or `gh` is unavailable and fallback applies:
- Write `claude/cycles/<cycle_id>/issue_import.md` per the format specified in §10.1 of this document.
- Update state.json: artifacts.issue_import = present.

### 10.2 GitHub Issue Automation (`--issues gh`)
If `--issues gh` was specified and `gh` CLI is available:

**Source:** Consume `claude/cycles/<cycle_id>/stage4_issue_manifest.json` (produced at STEP 4). Do not parse `stage4_backlog_slice.md` directly — the manifest is the authoritative structured source for issue creation (IMP-24).

**Idempotency check (IMP-35 gap 4):** Before creating any issue, check whether a GitHub issue already exists for this ST item in this cycle by searching for the label `cycle:<cycle_id>` combined with the ST-id in the title. Use:
```bash
gh issue list --search "[ST-xx] label:cycle:<cycle_id>" --json number,title,state
```
- If a matching issue exists: update labels/body if changed; do not create a duplicate.
- If no matching issue exists: create.

**Creation procedure:** For each entry in `stage4_issue_manifest.json`:
1. Write the issue body to a temporary file: `.gh_issue_body.tmp` (use `gh_issue_template.md` populated with manifest fields).
2. Execute: `gh issue create --title "[ST-xx] <title>" --body-file .gh_issue_body.tmp --label "sprint" --label "EPIC-xx" --label "cycle:<cycle_id>"`
3. Delete the temporary file.

Note: Temporary file avoids shell errors from backticks or special characters in markdown bodies.

### 10.3 Commit
Execution Commands:
1. `git add .claude_current_state.json`
2. `git add claude/cycles/<cycle_id>/*`
3. `git add claude/backlog/backlog.md`
4. `git add docs/product/scope/scope--{cycle_id}-{slug}.md`
5. `git add docs/product/decisions/decisions--{cycle_id}.md`
6. `git commit -m "[GOVERNANCE] Published Release Plan <cycle_id>"`
7. `git push origin <current-branch>`

---

# Publish Gate, Sealing, and Completion

Full procedure: `claude/system/shared/publish_gate.md`.

**Engine-specific Publish Gate conditions (all must be true):**
- `open_escalations` is empty
- Every Deferred escalation has `Blocks execution: No`; `deferred_execution_blockers` is empty
- `artifacts.stage4_5_capacity_check` is `pass` OR `warn` (warn allowed in `standard` mode only)
- `artifacts.stage5_5_cross_stage_integrity` is `pass`
- `artifacts.stage5_7_decision_record_integrity` is `pass` OR `not_applicable`
- `artifacts.stage1_readiness`, `stage3_5_model_integrity` are `pass`
- `attributes.plan_structured`, `plan_executable`, `backlog_committed` are `true`

If gate passes: `status = Validated`, `publish_eligible = true`. If `deferred_execution_blockers` non-empty: `status = Blocked`, HALT.

**Engine-specific Completion Condition** (all must be true in addition to shared publish gate completion):
- `docs/product/scope/scope--{cycle_id}-{slug}.md` exists
- `docs/product/decisions/decisions--{cycle_id}.md` exists
- `locks.backlog_lock.status = "released"`
- `locks.roadmap_lock.status = "released"` OR `"not_checked"`

---

## Change Log

See: [`claude/system/changelogs/release_planning_changelog.md`](changelogs/release_planning_changelog.md)
