**Owner:** Head of Specs Team
**Status:** Active
**Version:** 2.7
**Last Updated:** 2026-03-02
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
  - `import`: create `issue_import.md` only
  - `gh`: attempt to create GitHub issues via `gh` CLI; if unavailable, fall back to `import`
- `--auto-escalate` optional:
  - `true` (default): system creates, routes, and attempts to resolve escalations using delegated authority
  - `false`: system records blockers only and halts without attempting resolution

If invocation is not exact, do not run. Treat as conversational.

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

## 11. Canonicalization Rules (Hashing — Hard Requirement)
For markdown planning artefacts:
1. Normalize line endings to LF (`\n`)
2. Strip trailing whitespace on each line
3. Collapse runs of >2 blank lines to exactly 2
4. Trim leading/trailing blank lines
5. Do NOT reorder or otherwise transform content

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
- **Planning** means “Stage 3 exists and Stage 3.5 passed.”
- **Committed** means “Stage 4 passed.”
- **Validated** means “Stage 4.5 + Stage 5.5 + Stage 5.7 (if triggered) passed AND Publish Gate eligible.”
- **Published** means “Sealed snapshot recorded AND cycle summary + lessons exist AND publish gate passed.”

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
  "status": "Initialized",
  "publish_eligible": false,
  "last_transition_utc": "<ISO-8601 UTC>",

  "sealed": {
    "sealed_utc": "",
    "sealed_hashes": {
      "stage2_scope_extraction": "",
      "stage3_execution_plan": "",
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
      "stage2_scope_extraction",
      "stage3_execution_plan",
      "stage4_backlog_slice",
      "escalations"
    ],
    "stage2_scope_extraction": "<sha256 or empty>",
    "stage3_execution_plan": "<sha256 or empty>",
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

  "artifacts": {
    "run_manifest": "present|missing",
    "backlog_lock": "not_checked|acquired|blocked|released|stale_detected",
    "backlog_txn": "not_started|prepared|committed",
    "roadmap_lock": "not_checked|acquired|blocked|released|stale_detected",
    "roadmap_txn": "not_started|prepared|committed",

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
  - mark as `pass` any stage file present that satisfies the step’s requirements
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
- “Published cycle has drift. Do not modify this cycle. Create a new amendment cycle and reference this published cycle_id.”

If no drift found: HALT with message:
- “Cycle is Published and sealed. No further action permitted in this cycle.”

### Purpose
Prevent stale “pass” stamps after any mutation to assumptions or tracked artifacts. Execute:
- at the start of any run after STEP 0, and
- immediately after resolving any escalation that changes assumptions or artifacts.

### Tracked items
- stage2_scope_extraction.md
- stage3_execution_plan.md
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
- If stage2_scope_extraction changed → invalidate: STEP 3, STEP 3.5, STEP 4, STEP 5.5
- If stage3_execution_plan changed → invalidate: STEP 3.5, STEP 4, STEP 5.5
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

Recompute and compare:
- sealed_hashes (tracked planning artifacts)
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
  - “Published cycle has drift. Create amendment cycle.”

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

Each escalation entry must include:
- Escalation ID: `ESC-YYYYMMDD-nn`
- Raised by step
- Trigger type: Lifecycle | Strategy | Quality | Workforce | Schedule/Delivery | Other
- Owning authority role
- Unblock criteria + required evidence
- SLA due-by
- Disposition: Open | Resolved | Accepted Risk | Deferred
- Resolution summary + evidence links (required when closing)

Deferred must additionally include:
- Deferred by: <role>
- Deferred reason
- Next trigger:
  - Trigger type: date | event | dependency | decision
  - Trigger condition: <concrete>
  - Target date or target cycle: <value>
- Blocks execution: Yes | No
- Safe to proceed scope (required if Blocks execution = No): <what is safe to do>

Default SLAs:
- Lifecycle / Process Integrity: 24 hours
- Strategy boundary: 72 hours
- Quality: before execution begins
- Workforce: next planning checkpoint
- Schedule/Delivery: next planning checkpoint

When escalations.md is created:
- artifacts.escalations = present

### Escalation Freeze Rule
If status == Published:
- escalations.md becomes read-only
- Any modification (including append) → HALT

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
- status = Planning when Stage 3 exists (pass)

## STEP 3.5 — Local Model Integrity Check (Conditional Gate)

Classification: Conditional Gate (halts only if escalation remains Open / blocking)

Write: `stage3_5_model_integrity.md`

Update state.json:

- artifacts.stage3_5_model_integrity = pass|fail|blocked
- attributes.plan_executable = true on pass

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

- Read owner_cycle_id.
- If owner_cycle_id == `<cycle_id>`:
- Treat as re-entrant: proceed.
- artifacts.backlog_lock = "acquired"
- If owner_cycle_id != `<cycle_id>`:
- Record a ⛔ Blocker (Lifecycle / Process Integrity; owning authority: PMO Lead)
- Unblock criteria: "Backlog lock must be manually released or declared stale under protocol"
- Evidence: include lock file contents
- If `--auto-escalate=true`: invoke Escalation Handling Subroutine.
- Update `state.json`:
- locks.backlog_lock.owned = false
- locks.backlog_lock.owner_cycle_id = <from lock="" file=""></from>
- locks.backlog_lock.owner_release = <from lock="" file="" if="" present=""></from>
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

### Backlog Section Marker (Required for Idempotency)

When writing the release slice section into `claude/backlog/backlog.md`, include this HTML comment marker inside the section:

- `<!-- release-plan-marker: RP:<release>:<cycle_id> -->`

### STEP 4 Transaction — Prepare (Hard Requirement)

Create or update:

- `claude/cycles/<cycle_id>/backlog_txn.json`

Set to “prepared” BEFORE any modification to `claude/backlog/backlog.md`.

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

Update state.json (Step 4 outcome):

- artifacts.stage4_backlog_slice = pass|fail|blocked
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

## STEP 4.5 — Capacity Feasibility Sense Check (Conditional Gate)

Classification: Conditional Gate (halts only if escalation remains Open / blocking)

Write: `stage4_5_capacity_check.md`

Update state.json:

- artifacts.stage4_5_capacity_check = pass|warn|fail|blocked
- attributes.capacity_feasible = pass|warn|fail|blocked
(NOTE: this step is forced to rerun by RESUME PRECHECK per safety policy)

## STEP 5 — Roadmap Annotation (optional)

### STEP 5 Postcondition — Release Roadmap Lock (Strict)

After roadmap_txn state = committed:

- Remove `claude/roadmap/.lock`
- Update state.json:
  - locks.roadmap_lock.status = "released"
  - locks.roadmap_lock.owned = false
  - artifacts.roadmap_lock = "released"

If removal fails:
- Record blocker and HALT.

## STEP 5.5 — Cross-Stage Integrity Validation (Hard Gate)

Write: `stage5_5_cross_stage_integrity.md`

Update state.json:

- artifacts.stage5_5_cross_stage_integrity = pass|fail|blocked
- attributes.cross_stage_integrity = pass|fail|blocked
(NOTE: rerun only if Stage 2/3/4 changed, hash-based)

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
The run may be marked Validated/Published only if:
- open_escalations is empty, AND
- every Deferred escalation has `Blocks execution: No`, AND
- artifacts.stage4_5_capacity_check is pass OR warn (warn allowed only if mode=standard), AND
- artifacts.stage5_5_cross_stage_integrity is pass, AND
- artifacts.stage5_7_decision_record_integrity is pass OR not_applicable
- artifacts.stage1_readiness = pass
- artifacts.stage3_5_model_integrity = pass
- attributes.plan_structured = true
- attributes.plan_executable = true
- attributes.backlog_committed = true

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
Recompute canonicalized SHA-256 hashes for:
- stage2_scope_extraction.md
- stage3_execution_plan.md
- stage4_backlog_slice.md
- escalations.md

If escalations.md does not exist:
- Treat its canonical hash as SHA-256 of empty string.
- Write that value into sealed.sealed_hashes.escalations.

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
Run is complete only if:
- Cycle folder exists
- state.json valid
- publish_eligible = true
- status = Published
- Summary + Lessons exist
- No open escalations
