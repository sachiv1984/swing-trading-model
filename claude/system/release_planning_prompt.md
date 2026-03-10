**Owner:** Head of Specs Team
**Status:** Active
**Version:** 2.16
**Last Updated:** 2026-03-10
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Release Planning Engine — Governance Prompt

(Cycle-Based, Reusable, Escalation-Aware, State-Driven, Mutation-Safe, Concurrency-Safe, Terminal-Sealed, Assumption-Frozen, Tamper-Evident)

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
Binding governance stack:
- claude/charter/team_charter.md (role authority, conflict rules, escalation + accepted risk constraints)
- claude/charter/document_lifecycle_guide.md (lifecycle rules)
- claude/strategy/strategy_rules.md (system intent, boundaries)

This routine may not override any of the above.

---

## 5. Source-of-Truth Planning Inputs
Authoritative planning inputs:
- claude/roadmap/current_roadmap.md
- claude/backlog/backlog.md
- docs/specs/* (canonical specs as needed for readiness checks)
- docs/reference/openapi.yaml (supporting reference; align when needed)

---

## 6. Agent Integrity (Required Roles)
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

## 7. Write Scope Restriction (Hard Gate)
During this routine you may write only to:
- claude/cycles/<cycle_id>/*
- claude/backlog/backlog.md (release slice only; no global reprioritisation)
- claude/roadmap/current_roadmap.md (ONLY to add execution notes/links under the existing release section; no scope change)
- docs/product/scope/* (scope document created at STEP 2)
- docs/product/decisions/* (decisions record created at STEP 3; also when required to resolve an escalation under the rules below; must be lifecycle-compliant)
- claude/scoring/* (only if explicitly requested by Product Owner for sequencing support)

You must not modify:
- source code
- claude/strategy/strategy_rules.md
- claude/roadmap/initiative_register.md
- claude/roadmap/decision_log.md (reserved for irreversible roadmap decisions in rebalance)
- any doc outside allowed scope

Violation → halt.

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

## 11. Canonicalization Rules (Hashing — Hard Requirement)
For markdown planning artefacts:
1. Normalize line endings to LF (`\n`)
2. Strip trailing whitespace on each line
3. Collapse runs of >2 blank lines to exactly 2
4. Trim leading/trailing blank lines
5. Do NOT reorder or otherwise transform content
6. Front matter (YAML or HTML comment headers) is included in the hash — do not strip it

Hash method: SHA-256

Filesystem timestamps are forbidden.

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

### -1.1 Required Files Present
Verify these exist:
- claude/charter/team_charter.md
- claude/charter/document_lifecycle_guide.md
- claude/strategy/strategy_rules.md
- claude/roadmap/current_roadmap.md
- claude/backlog/backlog.md

If any are missing: halt and report exactly which.

**Issue creation prerequisite (IMP-48):** If `--issues gh` or `--issues import` is specified: verify `claude/system/gh_issue_template.md` exists. If missing: halt — "gh_issue_template.md not found — issue creation will fail."

### -1.2 Verify Release Exists on the Roadmap
Open `claude/roadmap/current_roadmap.md` and confirm the requested `--version` exists as a planned release section.
- If not found: halt (this routine cannot invent new releases).

### -1.3 Required Authority Roles Exist (Agent Integrity)
Verify agent files exist under `claude/agents/` for the minimum required roles listed above and contain the correct `**Role:**` line.

If any missing/malformed: halt.

### -1.4 Write Permission Test (Non-Destructive)
Create `claude/cycles/<cycle_id>/.write_test` and confirm it can be written. Remove it immediately. If write fails: halt. If the file is not removed here (e.g. due to an unexpected error), STEP 0 must clean it up before proceeding — do not leave `.write_test` files in cycle folders.

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

---

## STEP 0 — Create Run Manifest + Initialize State (Hard Requirement; must be first write)

**Cleanup:** If `claude/cycles/<cycle_id>/.write_test` exists (left from STEP -1.4 on a previous interrupted run), delete it now before proceeding.

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

### state.json schema (minimum required keys)
```json
{
  "cycle_id": "<cycle_id>",
  "release": "<vX.Y>",
  "date": "YYYY-MM-DD",
  "mode": "strict|standard",
  "issues_mode": "none|import|gh",
  "auto_escalate": true,
  "prompt_schema_version": "v2",
  "status": "Initialized",
  "publish_eligible": false,
  "last_transition_utc": "<ISO-8601 UTC>",

  "sealed": {
    "sealed_utc": "",
    "sealed_hashes": {
      "release_plan": "",
      "stage4_backlog_slice": "",
      "escalations": ""
    },
    "sealed_assumptions": {
      "timebox": "",
      "capacity": ""
    },
    "state_snapshot_hash": ""
  },

  "drift_detected": false,
  "drift_notes": [],

  "mutation_seq": 0,
  "assumptions": {
    "timebox": "<text or empty>",
    "capacity": "<text or empty>"
  },

  "artifact_hashes": {
    "method": "sha256",
    "canonicalization": "md-v1",
    "tracked_set": [
      "release_plan",
      "stage4_backlog_slice",
      "escalations"
    ],
    "release_plan": "<sha256 or empty>",
    "stage4_backlog_slice": "<sha256 or empty>",
    "escalations": "<sha256 or empty>"
  },

  "locks": {
    "backlog_lock": {
      "required": true,
      "lock_file": "claude/backlog/.lock",
      "owned": false,
      "owner_cycle_id": "",
      "owner_release": "",
      "acquired_utc": "",
      "txn_file": "claude/cycles/<cycle_id>/backlog_txn.json",
      "txn_id": "",
      "txn_state": "none|prepared|committed",
      "marker": "RP:<release>:<cycle_id>",
      "status": "not_checked|acquired|blocked|released|stale_detected"
    },
    "roadmap_lock": {
      "required": false,
      "lock_file": "claude/roadmap/.lock",
      "owned": false,
      "owner_cycle_id": "",
      "owner_release": "",
      "acquired_utc": "",
      "txn_file": "claude/cycles/<cycle_id>/roadmap_txn.json",
      "txn_id": "",
      "txn_state": "none|prepared|committed",
      "marker": "RA:<release>:<cycle_id>",
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

  "design_gate_status": "not_started|passed|bypassed",
  "amended_backlog_slice_path": "",

  "artifacts": {
    "run_manifest": "present|missing",
    "backlog_lock": "not_checked|acquired|blocked|released|stale_detected",
    "backlog_txn": "not_started|prepared|committed",
    "roadmap_lock": "not_checked|acquired|blocked|released|stale_detected",
    "roadmap_txn": "not_started|prepared|committed",

    "stage1_readiness": "not_started|pass|fail|blocked",
    "stage2_scope_extraction": "not_started|pass|fail|blocked",
    "stage2_scope_document": "not_started|present|missing",
    "stage3_execution_plan": "not_started|pass|fail|blocked",
    "stage3_decisions_record": "not_started|present|missing",
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

**Notes on reserved fields:**
- `design_gate_status`: written by the Design Gate Engine (Phase 1.5) after this cycle publishes. Reserved here so Phase 1.5 and Phase 2 can read it from a known location. This engine initialises it to `not_started` and does not modify it further.
- `amended_backlog_slice_path`: written by the Amendment Cycle Engine if an amendment is sealed after this cycle publishes. Reserved here. This engine initialises it to empty string and does not modify it further.

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
- Continue from the first step whose artifact status is `not_started` or `fail` or `blocked`,
- BUT do not rerun steps marked `pass` unless required by invalidation (see RESUME PRECHECK).

If status is `Blocked`:
- Invoke Escalation Handling Subroutine first.
- If all required escalations are resolved/deferred/accepted-risk per rules, resume from the appropriate next step.

If `state.json` is missing but artifacts exist:
- Rebuild state from artifacts:
  - mark as `pass` any stage file present that satisfies the step's requirements
  - otherwise mark as `not_started`
- Write `state.json` and continue.

---

## RESUME PRECHECK — Mutation Detection & Invalidation (Hard Gate)
### Terminal State Guard — Published Is Immutable (Hard Gate)
If `state.json.status == "Published"`:
- Treat the cycle folder as **sealed**.
- Do NOT run invalidation.
- Do NOT re-run any steps.
- Do NOT modify any stage artefacts in this cycle.
- Do NOT append to or modify `escalations.md`.
- Do NOT change assumptions (timebox/capacity).
- Do NOT acquire locks (backlog/roadmap) or perform lock/txn steps.

#### Artifact Hash Freeze Rule (Hard Gate)
If `status == Published`:
- `state.json.artifact_hashes.*` must not change.
- Any recomputed hash that differs from `state.json.sealed.sealed_hashes.*` triggers drift detection.
- `state.json.artifact_hashes.*` must remain aligned with `state.json.sealed.sealed_hashes.*`.

### Sealed Hash Authority Rule (Hard Gate)

If status == Published:

- sealed.sealed_hashes.* is the single source of truth.
- artifact_hashes.* must equal sealed.sealed_hashes.*.
- If artifact_hashes differs from sealed_hashes:
  - Treat as drift.
  - Do NOT attempt to reconcile.

#### State File Immutability Rule (Hard Gate)
If `status == Published`:
- `state.json` may not be modified except for:
  - `drift_detected`
  - `drift_notes`
- Any other modification constitutes drift.
- open_escalations must not change
- deferred_escalations must not change
- accepted_risk_escalations must not change
- deferred_execution_blockers must not change

Perform drift detection only (see Drift Detection).

If drift found: HALT with instruction:
- "Published cycle has drift. Do not modify this cycle. Create a new amendment cycle and reference this published cycle_id."

If no drift found: HALT with message:
- "Cycle is Published and sealed. No further action permitted in this cycle."

### Purpose
Prevent stale "pass" stamps after any mutation to assumptions or tracked artifacts. Execute:
- at the start of any run after STEP 0, and
- immediately after resolving any escalation that changes assumptions or artifacts.

### Tracked items
- release_plan.md (consolidated intermediate artefact — covers Scope, Execution Plan, and Integrity Validation content)
- stage4_backlog_slice.md
- escalations.md
- assumptions: timebox, capacity

### Detection
1. Recompute current hashes for tracked items (canonicalization rules apply).
2. Compare to `state.json.artifact_hashes` and `state.json.assumptions`.
3. If any differ, record a mutation:
   - mutation_seq += 1
   - append to `mutations[]`: timestamp, changed_keys, reason
   - update hashes and assumptions in state.json.

### Invalidation map
If a tracked item changes, invalidate dependent steps by setting their artifact status to `not_started` and recording them in `invalidated_steps[]`.

Rules:
- If release_plan.md (## Scope section) changed → invalidate: STEP 3, STEP 3.5, STEP 4, STEP 5.5
- If release_plan.md (## Execution Plan section) changed → invalidate: STEP 3.5, STEP 4, STEP 5.5
- If stage4_backlog_slice changed → invalidate: STEP 5.5
- If escalations changed in a way that adds/removes decision records or Accepted Risk → invalidate: STEP 5.7 and Publish Gate evaluation

Safety policy (required):
- Always re-run STEP 4.5 after any resume where:
  - timebox changed OR capacity changed OR STEP 4.5 previously failed/blocked, OR
  - any workforce escalation was opened/resolved in this cycle.

Implementation: set `artifacts.stage4_5_capacity_check = not_started` and `attributes.capacity_feasible = not_started`.

Efficiency policy (required):
- Re-run STEP 5.5 only if Stage 2/3/4 changed (hash-based).

Resume position:
- Resume from the earliest invalidated step (lowest numbered step). If no invalidations exist: continue normal resume rule.

---

### Shared Write Recovery — Backlog (Hard Gate)
If `claude/backlog/.lock` exists OR `artifacts.backlog_lock` in state.json is `acquired`:
1. Read `claude/backlog/.lock` and determine `owner_cycle_id`.
2. If `owner_cycle_id != <cycle_id>`:
   - Record a blocker (Lifecycle / Process Integrity; owner: PMO Lead)
   - HALT (strict lock; no override; no auto-delete)
3. If `owner_cycle_id == <cycle_id>`:
   - Perform backlog STEP 4 recovery.

Backlog recovery procedure:
A) Marker value: `RP:<release>:<cycle_id>`
B) Check backlog contains:
- `<!-- release-plan-marker: RP:<release>:<cycle_id> -->`
C) If marker present:
- Ensure `backlog_txn.json` exists and committed (create/upgrade if needed).
- Update state.json:
  - artifacts.stage4_backlog_slice = pass
  - attributes.backlog_committed = true
  - artifacts.backlog_txn = committed
  - locks.backlog_lock.txn_state = committed
- Remove `claude/backlog/.lock`, update:
  - artifacts.backlog_lock = released
  - locks.backlog_lock.status = released
  - locks.backlog_lock.owned = false
- Continue.
D) If marker absent:
- Treat STEP 4 as incomplete:
  - artifacts.stage4_backlog_slice = not_started
  - artifacts.backlog_txn = prepared (create txn file if missing)
  - locks.backlog_lock.txn_state = prepared
- Resume at STEP 4.

If lock removal fails: record blocker and HALT.

---

### Shared Write Recovery — Roadmap (Hard Gate)
If `claude/roadmap/.lock` exists OR `artifacts.roadmap_lock` in state.json is `acquired`:
1. Read `claude/roadmap/.lock` and determine `owner_cycle_id`.
2. If `owner_cycle_id != <cycle_id>`:
   - Record a blocker (Lifecycle / Process Integrity; owner: PMO Lead)
   - HALT (strict lock; no override; no auto-delete)
3. If `owner_cycle_id == <cycle_id>`:
   - Perform roadmap STEP 5 recovery.

Roadmap recovery procedure:
A) Marker value: `RA:<release>:<cycle_id>`
B) Check roadmap contains:
- `<!-- roadmap-annotation-marker: RA:<release>:<cycle_id> -->`
C) If marker present:
- Ensure `roadmap_txn.json` exists and committed (create/upgrade if needed).
- Update state.json:
  - artifacts.roadmap_txn = committed
  - locks.roadmap_lock.txn_state = committed
- Remove `claude/roadmap/.lock`, update:
  - artifacts.roadmap_lock = released
  - locks.roadmap_lock.status = released
  - locks.roadmap_lock.owned = false
- Continue.
D) If marker absent:
- Treat STEP 5 annotation as incomplete:
  - artifacts.roadmap_txn = prepared (create txn file if missing)
  - locks.roadmap_lock.txn_state = prepared
- Resume at STEP 4.95 / STEP 5.

If lock removal fails: record blocker and HALT.

---

## Drift Detection
Trigger: only when `status == Published`.

**Schema version rule:** Drift detection uses the keys present in `state.sealed.sealed_hashes` for that cycle — not a fixed key list. Do not assume keys; read the `tracked_set` from `artifact_hashes.tracked_set`.

| `prompt_schema_version` | `tracked_set` keys in `sealed_hashes` |
|------------------------|---------------------------------------|
| `v2` (prompt ≥ v2.11) | `release_plan`, `stage4_backlog_slice`, `escalations` |
| `v1` or absent (prompt ≤ v2.10) | `stage2_scope_extraction`, `stage3_execution_plan`, `stage4_backlog_slice`, `escalations` |

Never compare `sealed_hashes` keys across schema versions. Each cycle is self-contained.

Recompute and compare:
- sealed_hashes (tracked planning artifacts — per schema version above)
- sealed_assumptions (timebox/capacity)
- state_snapshot_hash

If mismatch:
- state.drift_detected = true
- Append drift_notes:
  - timestamp
  - changed component
  - old value
  - new value
- HALT with instruction:
  - "Published cycle has drift. Create amendment cycle."

No repair allowed in published cycle.

---

## ESCALATION HANDLING SUBROUTINE — Callable (Delegated Authority)
Trigger:
- Invoke whenever any step produces ⛔ Blockers AND `--auto-escalate=true`, OR when `status=Blocked`.

Create or append:
- `claude/cycles/<cycle_id>/escalations.md`

Escalations file rules:
- Location is always within the cycle folder.
- Append-only within the cycle (do not edit previous entries).
- Start with header:
  - Owner: PMO Lead
  - Class: Planning Document (Class 4)
  - Status: Active
  - Last Updated: <date>

**Escalation entry format, SLAs, append-only rule, and Accepted Risk constraints:** follow `claude/system/shared_standards.md §4` exactly.

Engine-specific rules (additional to shared_standards.md §4):

When escalations.md is created:
- artifacts.escalations = present

### Escalation Freeze Rule
If status == Published:
- escalations.md becomes read-only
- Any modification (including append) → HALT

### Deferred Governance Constraint (Hard Gate)
- Only owning authority may mark Deferred (by domain).
- Deferred requires trigger and Blocks execution field.
- No auto-carry; must be re-acknowledged next cycle.
- Deferred does not bypass Strategy/Quality/Lifecycle blocks; publish depends on publish gate.

### Decision Record Controls (Minimal Anti-Drift Set)
- Typed decisions only: AR or SRB.
- Naming:
  - AR: docs/product/decisions/AR-<release>-<cycle_id>-<esc_id>.md
  - SRB: docs/product/decisions/SRB-<release>-<cycle_id>-<esc_id>.md
- Mandatory template: header + required sections; missing field → HALT.

### Escalation Mutation Rule (Hard Gate)
If resolving an escalation modifies assumptions or Stage 2/3/4 artifacts or decision records:
- Update hashes/assumptions in state.json
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

*Trigger: LL-v1.9-01 — lessons_learnt.md cycle 2026-03-06__release-v1.9. Implemented 2026-03-10.*

Update state.json:

- artifacts.stage1_readiness = pass|fail|blocked

---

## STEP 2 — Scope Extraction (No Scope Changes Allowed)

Write: `## Scope` section in `release_plan.md` (S2 IDs required)

**Scope document (required output):**

Create: `docs/product/scope/scope--{cycle_id}-{slug}.md`

Where `{slug}` is a short lowercase hyphenated name derived from the release feature name (e.g. `scope--2026-03-04__release-v1.8-risk-dashboard.md`).

Minimum required content:

```markdown
Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: vX.Y
Cycle: <cycle_id>
Last Updated: <date>

## Release Scope — vX.Y <Feature Name>

### Items in scope
| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-xx | ... |

### Items explicitly deferred
| Item | Reason | Target |
|------|--------|--------|
| ...  | ...    | ...    |

*(If nothing deferred: "None")*

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: <cycle_id>
```

This document is the authoritative scope record for Post-Ship Closure Step 4 supersession. If this document is not created here, the post-ship closure engine will flag it as missing.

Update state.json:

- artifacts.stage2_scope_extraction = pass|fail|blocked
- artifacts.stage2_scope_document = present|missing

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

**Decisions record (required output):**

Create: `docs/product/decisions/decisions--{cycle_id}.md`

This document is the authoritative planning decisions record for this release. It is superseded at Post-Ship Closure. If not created here, the post-ship closure engine will flag it as missing.

Minimum required content:

```markdown
Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: vX.Y
Cycle: <cycle_id>
Last Updated: <date>

## Planning Decisions — vX.Y <Feature Name>

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ...      | ...       | ...     | ...  |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| ...      | ...       | ...     | ...  |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| ...    | ...         | ...       | ...         | ...       |

*(Populate from any Accepted Risk escalations in this cycle. If none: "None")*

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: <cycle_id>
```

Update state.json:

- artifacts.stage3_execution_plan = pass|fail|blocked
- artifacts.stage3_decisions_record = present|missing
- attributes.plan_structured = true on pass
- status = Planning when Stage 3 exists (pass)

---

## STEP 3.5 — Local Model Integrity Check (Conditional Gate)

Classification: Conditional Gate (halts only if escalation remains Open / blocking)

Write: `## Integrity Validation — 3.5 Local Model Integrity` subsection in `release_plan.md`

Update state.json:

- artifacts.stage3_5_model_integrity = pass|fail|blocked
- attributes.plan_executable = true on pass

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

1. If `claude/backlog/.lock` does NOT exist:

   - Create it with deterministic contents:
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
     - locks.backlog_lock.marker = `RP:<release>:<cycle_id>`
     - artifacts.backlog_lock = "acquired"

2. If `claude/backlog/.lock` exists:

   - Read `owner_cycle_id` from lock file contents.
   - If `owner_cycle_id == <cycle_id>`:
     - Treat as re-entrant: proceed.
     - artifacts.backlog_lock = "acquired"
   - If `owner_cycle_id != <cycle_id>`:
     - Record a ⛔ Blocker (Lifecycle / Process Integrity; owning authority: PMO Lead)
     - Unblock criteria: "Backlog lock must be manually released or declared stale under protocol"
     - Evidence: include lock file contents
     - If `--auto-escalate=true`: invoke Escalation Handling Subroutine.
     - Update `state.json`:
       - locks.backlog_lock.owned = false
       - locks.backlog_lock.owner_cycle_id = `<value from lock file>`
       - locks.backlog_lock.owner_release = `<value from lock file, if present>`
       - locks.backlog_lock.status = "blocked"
       - artifacts.backlog_lock = "blocked"
     - HALT.

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

Schema:
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

One entry per ST item in `stage4_backlog_slice.md`. The `cycle:<cycle_id>` label is the idempotency key for GitHub issue creation (§10.2).

Update state.json (Step 4 outcome):

- artifacts.stage4_backlog_slice = pass|fail|blocked
- artifacts.stage4_issue_manifest = pass|fail|blocked
- attributes.backlog_committed = true on pass
- status = Committed on pass

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

### When outcome is WARN — Phasing Recommendation (Required)

When `artifacts.stage4_5_capacity_check = warn` (total estimated effort exceeds available capacity but the release is not infeasible), the `## Capacity Check` section of `release_plan.md` **must** include a `### Phasing Recommendation` subsection. This subsection must:

1. State the estimated total effort (mid-point hours) and available capacity (hours).
2. Propose a concrete phasing approach for sprint planning — for example:
   - `Phase 1 (Sprint 1): EPIC-xx, EPIC-yy — estimated N hrs (within capacity)`
   - `Phase 2 (Sprint 2): EPIC-aa, EPIC-bb — estimated M hrs (within capacity)`
3. Note the ordering rationale (dependencies, risk, user value).

This makes the WARN actionable: sprint planning can adopt the phasing recommendation directly rather than discovering over-allocation at sprint planning time.

*Trigger: LL-v1.9-02 — lessons_learnt.md cycle 2026-03-06__release-v1.9. Implemented 2026-03-10.*

Update state.json:

- artifacts.stage4_5_capacity_check = pass|warn|fail|blocked
- attributes.capacity_feasible = pass|warn|fail|blocked

*(NOTE: this step is forced to rerun by RESUME PRECHECK per safety policy)*

---

## STEP 5 — Roadmap Annotation

Purpose: Record that planning is underway for this release by adding execution notes to the roadmap entry. This does not change scope, priority, or strategy — it adds a link to the cycle folder and current status.

Write: Update `claude/roadmap/current_roadmap.md` — under the existing release section only.

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

Update state.json:

- artifacts.roadmap_txn = committed (on success)
- locks.roadmap_lock.status = released (on success)

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

## STEP 5.5 — Cross-Stage Integrity Validation (Hard Gate)

Write: `## Integrity Validation — 5.5 Cross-Stage Integrity` subsection in `release_plan.md`

Update state.json:

- artifacts.stage5_5_cross_stage_integrity = pass|fail|blocked
- attributes.cross_stage_integrity = pass|fail|blocked

*(NOTE: rerun only if Stage 2/3/4 changed, hash-based)*

---

## STEP 5.7 — Decision Record Integrity Validation (Hard Gate)

Write: `## Integrity Validation — 5.7 Decision Record Integrity` subsection in `release_plan.md` (only if triggered)

Update state.json:

- artifacts.stage5_7_decision_record_integrity = pass|fail|blocked|not_applicable
- attributes.decisions_validated = pass|fail|not_applicable|blocked

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

*Trigger: LL-v1.9-03 — lessons_learnt.md cycle 2026-03-06__release-v1.9. Implemented 2026-03-10.*

**Intermediate global state sync (required before writing cycle_summary.md):**

Before writing `cycle_summary.md`, update `.claude_current_state.json` to reflect the current in-progress state. This is a pre-publish sync — it does not mark the cycle Published. Its purpose is to ensure the global state pointer reflects the active cycle if the session is interrupted before STEP 9.

Update `.claude_current_state.json`:
- active_cycle = `<cycle_id>`
- status = current macro-state (e.g., `Validated` — not `Published`)
- backlog_slice_path = `claude/cycles/<cycle_id>/stage4_backlog_slice.md`
- last_sync_utc = current timestamp

STEP 9 (Global State Synchronization) is the terminal sync and is the only step that sets status = `Published`. Do not set Published here.

---

## STEP 8 — Lessons Learnt

Write: `lessons_learnt.md`

---

## STEP 9 — Global State Synchronization (Hard Requirement — Terminal)

Purpose: Final update of the root-level state pointer to reflect that this cycle is Published and sealed. This is the only step that sets `status = Published` in `.claude_current_state.json`. STEP 7's intermediate sync must have run first.

Execution Rules:
1. Verify STEP 7 intermediate sync has completed (backlog_slice_path and active_cycle are already set).
2. Update the root-level file `.claude_current_state.json`:
   - active_cycle: `<cycle_id>` (confirm — already set at STEP 7)
   - status: `Published`
   - backlog_slice_path: `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (confirm)
   - last_sync_utc: current timestamp
3. If the file does not exist, create it using the standard schema.

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

# Publish Gate (Hard Constraint)
The run may be marked Validated/Published only if ALL of the following are true:

- `open_escalations` is empty, AND
- every Deferred escalation has `Blocks execution: No`, AND
- `deferred_execution_blockers` is empty (any deferred escalation with `Blocks execution: Yes` prevents publish), AND
- `artifacts.stage4_5_capacity_check` is `pass` OR `warn` (warn allowed only if mode=standard), AND
- `artifacts.stage5_5_cross_stage_integrity` is `pass`, AND
- `artifacts.stage5_7_decision_record_integrity` is `pass` OR `not_applicable`, AND
- `artifacts.stage1_readiness` = `pass`, AND
- `artifacts.stage3_5_model_integrity` = `pass`, AND
- `attributes.plan_structured` = `true`, AND
- `attributes.plan_executable` = `true`, AND
- `attributes.backlog_committed` = `true`

If `deferred_execution_blockers` is non-empty:
- status MUST be `Blocked` (or remain non-Published)
- publish_eligible = false
- HALT (do not mark Published)

If Publish Gate passes:
- status = `Validated`
- publish_eligible = true

Else:
- publish_eligible = false

---

# Pre-Seal Revalidation (Hard Gate)
Before executing **Publish Sealing**:

1. Re-run **RESUME PRECHECK — Mutation Detection & Invalidation**.
2. If any tracked artifact or assumption changed since Publish Gate evaluation:
   - Invalidate Publish Gate.
   - Set `publish_eligible = false`.
   - Resume from the earliest invalidated step.
   - **HALT** (sealing may not proceed).
3. Sealing may only proceed if **no invalidations** occur during this check.

### Final Publish Preconditions (Hard Gate)

Before Publish Sealing:

- locks.backlog_lock.status must be "released"
- locks.roadmap_lock.status must be "released" OR "not_checked"
- locks.*.owned must be false
- locks.*.txn_state must be "committed" OR "none"

If any lock remains acquired, prepared, or blocked:
- HALT.

---

# Publish Sealing
Before setting `status = Published`:

## 18.1 Recompute Canonical Hashes
Recompute canonicalized SHA-256 hashes for (prompt schema v2 tracked set):
- release_plan.md
- stage4_backlog_slice.md
- escalations.md

If escalations.md does not exist:
- Treat its canonical hash as SHA-256 of empty string.
- Write that value into sealed.sealed_hashes.escalations.

If any of the required tracked artifacts are missing at sealing time:
- release_plan.md
- stage4_backlog_slice.md

Then:
- HALT.
- status remains Validated.

Write them into:
- state.sealed.sealed_hashes

## 18.2 Seal Assumptions
Capture:

```json
{
  "timebox": "<assumptions.timebox>",
  "capacity": "<assumptions.capacity>"
}
```

Write into:
- state.sealed.sealed_assumptions

These become immutable.

## 18.3 Seal Canonical State Snapshot (Tamper-Evident)
Create canonical JSON excluding:
- last_transition_utc
- Drift flags
- locks.*
- Dynamic artefact lock states

Include:
- cycle_id
- release
- date
- mode
- assumptions
- artifact_hashes
- mutation_seq
- escalation lists
- attributes
- sealed_hashes
- sealed_assumptions

Canonicalize key order.

Hash using SHA-256.

Write into:
- state.sealed.state_snapshot_hash

## 18.4 Finalize Seal
Set:
- sealed_utc = now (UTC)
- drift_detected = false
- drift_notes = []

## 18.5 Final Transition
After successful sealing:
- status = "Published"
- last_transition_utc = now
- publish_eligible = true

It is forbidden to mark Published before sealing completes.

If sealing fails → halt and remain Validated.

---

# State Integrity Rule
If:
- status == Published
- Sealed fields missing OR
- state_snapshot_hash mismatch

Treat as drift.

Do NOT repair.

Require amendment cycle.

---

# Completion Condition
Run is complete only if ALL of the following are true:
- Cycle folder exists
- state.json valid and status = Published
- publish_eligible = true
- cycle_summary.md exists
- lessons_learnt.md exists
- No open escalations (open_escalations is empty)
- deferred_execution_blockers is empty
- locks.backlog_lock.status = "released"
- locks.roadmap_lock.status = "released" OR "not_checked"
- docs/product/scope/scope--{cycle_id}-{slug}.md exists
- docs/product/decisions/decisions--{cycle_id}.md exists

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.16 | 2026-03-10 | IMP-48: STEP -1.1 — conditional `gh_issue_template.md` existence check added; halt if missing when `--issues gh` or `--issues import` specified. IMP-24: STEP 4 — `stage4_issue_manifest.json` produced alongside `stage4_backlog_slice.md`; schema `[{id, title, epic, description, ac_summary, labels, assignee}]`; `cycle:<cycle_id>` label is idempotency key; `artifacts.stage4_issue_manifest` added to state.json schema. §10.2 updated — consumes `stage4_issue_manifest.json` (not markdown parsing); idempotency check added (IMP-35 gap 4); `cycle:<cycle_id>` label check-before-create; creation procedure uses manifest fields. |
| 2.15 | 2026-03-10 | IMP-46: §10.1 — EPIC description source for issue import corrected from `release_plan.md ## Execution Plan` to `stage4_backlog_slice.md` (canonical scope record). IMP-47: STEP -1.4 — write permission test temp file renamed to `.write_test`; must be removed immediately; STEP 0 cleanup obligation added. |
| 2.14 | 2026-03-10 | LL-v1.9-01: Added STEP 1.1 Backlog Age Advisory — scans backlog for spec/documentation debt items aged 2+ cycles without story assignment; emits advisory warning and recommendation to promote to sprint stories. LL-v1.9-02: Added STEP 4.5 Phasing Recommendation — when capacity check outcome is WARN, a `### Phasing Recommendation` subsection is now required in `release_plan.md §Capacity Check`; lists concrete phase 1/phase 2 EPIC groupings with effort estimates and ordering rationale. LL-v1.9-03: Added STEP 7 Pre-sprint Planning Required Decisions — when any High-priority risk carries "must resolve before sprint planning seal" disposition, a `## Pre-sprint Planning Required Decisions` checklist section is required in `cycle_summary.md` for Sprint Planning Engine consumption. All three triggered by lessons_learnt.md 2026-03-06__release-v1.9 per closure_record §6 Actions #3–5. |
| 2.13 | 2026-03-08 | IMP-05: Added STEP -1.5 advisory — reads prior cycle `lessons_learnt_closure.md`, checks all `action-now` items appear in `prompt_change_log.md`; warns if missing. IMP-06: Added STEP -1.6 hard gate — `post_ship_complete = true` and `next_cycle_unblocked = true` both required in `.claude_current_state.json` before new release cycle may open; exception for first cycle. IMP-07: Removed inline escalation entry format, SLA table, and Accepted Risk constraint from ESCALATION HANDLING SUBROUTINE; replaced with reference to `shared_standards.md §4`; retained engine-specific rules (Freeze Rule, Deferred constraint, Decision Record Controls, Mutation Rule, State update rules). IMP-08: Added compact table format requirement to STEP 3 `## Execution Plan` section; full acceptance criteria belong exclusively in `stage4_backlog_slice.md`; target <200 lines for full `release_plan.md`. IMP-10: Added STEP -1.7 advisory — checks that each governed prompt's current version appears in `prompt_change_log.md`; warns if missing. |
| 2.12 | 2026-03-07 | IMP-03: Added `prompt_schema_version: "v2"` to state.json schema template. Fixed §18.1 tracked artifact list — updated from old stage file names (`stage2_scope_extraction.md`, `stage3_execution_plan.md`) to `release_plan.md` (schema v2). Added schema version migration table to Drift Detection section — documents that drift detection uses keys from `tracked_set` for the cycle's schema version; never compares across versions. |
| 2.11 | 2026-03-07 | Intermediate Release Planning artefacts collapsed into `release_plan.md`. Steps 1, 2, 3, 3.5, 4.5, 5.5, 5.7 now write sections into a single consolidated file instead of separate stage files. Final outputs retained separately: scope document, decisions record, stage4_backlog_slice.md. Tracked set in state.json schema updated from `[stage2_scope_extraction, stage3_execution_plan, stage4_backlog_slice, escalations]` to `[release_plan, stage4_backlog_slice, escalations]`. |
| 2.10 | 2026-03-07 | Added Lifecycle Guard (valid from-states: `Closed`) per `shared_standards.md §10`. |
| 2.9 | 2026-03-07 | Fixed STEP 3.9 lock acquisition — removed malformed XML-like template placeholders; replaced with plain text field descriptions. Wrote STEP 5 body — was postcondition-only; added full purpose, annotation content template, lock/transaction procedure, and idempotency rule. Clarified STEP 7 vs STEP 9 state sync — renamed STEP 7.1 as "Intermediate global state sync", added explicit note that only STEP 9 sets Published, added STEP 9 precondition to verify STEP 7 ran first. Fixed scope document supersession note — removed pre-populated TBD fields that implied known values at planning time; replaced with explicit [TBD] placeholders and "do not populate at planning time" instruction. Added decisions record creation to STEP 3 — new required output `docs/product/decisions/decisions--{cycle_id}.md` with minimum content template and supersession note. Fixed deferred_execution_blockers — added to Publish Gate as a blocking condition; added to Completion Condition. Added design_gate_status and amended_backlog_slice_path to state.json schema as reserved fields with ownership notes. Added §10.1 issue_import.md format specification. Added canonicalization rule for front matter (rule 6). Updated Write Scope Restriction (§7) to include docs/product/scope/* and docs/product/decisions/* for planning-time document creation. Updated STEP 10 commit to include scope and decisions record files. Updated Completion Condition to include lock state verification and presence checks for scope and decisions documents. |
| 2.8 | 2026-03-06 | Prior version. |