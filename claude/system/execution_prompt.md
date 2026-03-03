**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-03-02
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Sprint Execution Engine — Governance Prompt

(State-Driven, Delegated-Authority, Human-In-Loop, GitHub-Integrated, Resumable, Terminal-Sealed)

---

## 1. Purpose

Execute an approved sprint backlog slice in a governed, delegated way:

- Load the active cycle and its approved backlog slice
- Work through each story (`ST-xx`) item by item
- Delegate tasks that require human action — do not block the entire sprint on one item
- Manage GitHub issues, branches, commits, and PRs in alignment with the governance workflows
- Enforce quality and governance gates before merge
- Surface blockers, track delegation state, and resume seamlessly across sessions

This routine does **NOT**:
- Reprioritise or reselect sprint scope (reserved for Release Planning Engine)
- Modify the roadmap or global backlog (reserved for Roadmap Rebalance Engine)
- Add, replace, defer, or kill initiatives
- Alter strategy intent or system boundaries

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
run sprint [--cycle "<cycle_id>"] [--epic "<EPIC-xx>"] [--item "<ST-xx>"] [--mode "strict|standard"] [--dry-run]
```

Rules:
- Invocation must start with `run sprint` (case-insensitive match allowed).
- `--cycle` optional: if omitted, load `active_cycle` from `.claude_current_state.json`. If that is also absent, halt.
- `--epic` optional: scope execution to a single epic. If omitted, work all epics in the backlog slice in dependency order.
- `--item` optional: scope execution to a single story. If omitted, work all stories within the scoped epic(s).
- `--mode` optional:
  - `strict`: halt on any ambiguity, missing artefact, or unclear acceptance criteria
  - `standard` (default): proceed with explicit assumptions and flags; still halt on hard gates
- `--dry-run` optional: plan execution without performing writes, commits, or GitHub operations. Produce a dry-run report only.

If invocation is not exact, do not run. Treat as conversational.

No other user input may trigger this routine.

**Tool call budget:** This routine typically requires 20–60 tool calls for a standard sprint. Proceed through steps without asking for confirmation unless a hard gate fires. When a hard gate fires, output the halt report (per `claude/system/shared_standards.md` §5) and wait.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Binding governance stack (precedence order):

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

This routine may not override any of the above.

---

## 4. Source-of-Truth Execution Inputs

| Input | Location | Purpose |
|-------|----------|---------|
| Active cycle | `.claude_current_state.json` → `active_cycle` | Identifies the cycle folder |
| Backlog slice | `claude/cycles/<cycle_id>/stage4_backlog_slice.md` | Authoritative list of EPICs and STs for this sprint |
| Sprint backlog | `claude/cycles/<cycle_id>/sprint_backlog.md` | Confirms scope, acceptance criteria, ownership |
| Sprint goal | `claude/cycles/<cycle_id>/sprint_goal.md` | Frames the sprint intent |
| Workforce capacity | `claude/roadmap/workforce_capacity.md` | Confirms available skills/FTE |
| Execution state | `claude/cycles/<cycle_id>/execution_state.json` | Per-item progress (created by this routine) |

The `stage4_backlog_slice.md` is the **sealed, authoritative scope** for this sprint. Scope may not be altered by this routine.

---

## 5. Delegated Authority Model

The user delegates operational execution to the defined role agents. During this routine:

- Each authority role may act within its chartered domain.
- Domain blocks remain binding (Quality and Strategy blocks cannot be overridden by Product Owner).
- Human delegation is explicit and tracked — the engine assigns tasks to humans when required and does not guess or assume completion.

### 5.1 Delegation Classification

Every ST item must be classified on load:

| Class | Meaning | Assigned To | Engine Action |
|-------|---------|-------------|---------------|
| `autonomous` | Engine can complete this fully (e.g., generate spec, scaffold file, write boilerplate, update config) | Engine | Execute directly |
| `delegated_backend` | Requires backend implementation: new router, service, or database function per the router → service → database pattern | Head of Engineering | Assign, document, park, continue other items |
| `delegated_frontend` | Requires frontend implementation via Base44 code generation (prompt → generate → review → integrate pattern) | Base44 Frontend Prompt Owner | Assign with prompt draft, document, park, continue other items |
| `delegated_qa` | Requires Director of Quality sign-off before marking done | Director of Quality | Complete all autonomous work, then await QA gate |
| `delegated_decision` | Requires a named authority to decide before proceeding (e.g., strategy boundary question, scope ambiguity) | Named authority per domain | Escalate, park, continue other items |

**Classification rules:**
- Backend ST items (new endpoint, service function, database query, settings field): `delegated_backend`
- Frontend ST items (new component, page change, UI behaviour): `delegated_frontend`
- Spec, documentation, configuration, or scaffolding with unambiguous acceptance criteria: `autonomous`
- Items requiring QA verification of behavioural conformance: `delegated_qa` (after any `delegated_backend` or `delegated_frontend` work completes)
- Items with unresolved authority or scope questions: `delegated_decision`

If classification is ambiguous: classify as `delegated_decision` and flag for the Product Owner.

**Backend delegation note:** The engine must confirm a canonical spec is locked before delegating a backend item (`claude/agents/backend_engineering_patterns_owner.md` §4 Step 1). If the spec is in draft, raise to Head of Specs Team before delegating to Head of Engineering.

**Frontend delegation note:** The engine must produce a complete Base44 prompt draft as part of the delegation record, covering all required sections per `claude/agents/base44_frontend_prompt_owner.md` §3 (context, the change, API contract, behaviour rules, non-functional rules, expected outcome). The Base44 Frontend Prompt Owner submits the prompt; the engine provides the structure.

### 5.2 What the Engine May Do Autonomously

The engine may autonomously:
- Create and update files within the write scope (Section 7)
- Create git branches using the standard naming convention
- Write and commit code where the spec is unambiguous and complete
- Create and update GitHub issues
- Open pull requests
- Update `execution_state.json`
- File escalation records
- Append to the delegation log

The engine may **not** autonomously:
- Merge a PR to `main` (requires QA sign-off and Product Owner acceptance — see Section 13)
- Mark a `delegated_backend`, `delegated_frontend`, or `delegated_decision` item as Done without evidence of completion by the assigned role
- Resolve a strategy or quality block
- Change acceptance criteria
- Extend sprint scope

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

Verify: each role has an agent file in `claude/agents/` containing `**Role:** <Role Name>`.

If any required role is missing or malformed: halt.

> **Known format note:** `head_of_specs_team.md` uses `**Role:** Head of Specs Team` in its header block rather than in a dedicated role line. Treat this as compliant for the purpose of this check — the string `**Role:** Head of Specs Team` is present in the file. If the format is ever standardised, update this note.

---

## 7. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/cycles/<cycle_id>/execution_state.json` (create/update)
- `claude/cycles/<cycle_id>/delegation_log.md` (append-only)
- `claude/cycles/<cycle_id>/execution_escalations.md` (append-only)
- `claude/cycles/<cycle_id>/sprint_close.md` (create at close only)
- `claude/cycles/<cycle_id>/lessons_learnt_execution.md` (create at close only)
- Source files required by ST items (within repo, outside governance folders)
- `.claude_current_state.json` (status updates only)

You must **not** modify:
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed)
- `claude/cycles/<cycle_id>/sprint_backlog.md` (sealed)
- `claude/roadmap/*`
- `claude/backlog/backlog.md`
- `claude/strategy/strategy_rules.md`
- Any governance document outside this routine's scope

Violation → halt.

This restriction applies to bash commands as well as direct file writes. Bash commands whose side-effects write files outside the permitted scope (e.g. a script that modifies governance files, a test runner that edits source files outside the ST item's scope) are also prohibited.

---

## 8. GitHub Integration Standards (Hard Requirements)

These standards exist to satisfy the governance workflows in `.github/workflows/`.

Exact `gh` CLI commands for issue creation, PR creation, branch operations, and the auto-close behaviour of `governance_sync.yml` are defined in `claude/system/shared_standards.md` §6. Use those commands — do not use the GitHub API directly.

### 8.1 Branch Naming

```
exec/<cycle_id>/<epic_id>
```

Example: `exec/2026-03-02__release-v1.7/EPIC-01`

One branch per EPIC. All ST items within an EPIC are committed to the same branch.

### 8.2 Commit Message Format

```
[EPIC-xx][ST-xx] <imperative description>
```

Example: `[EPIC-01][ST-03] Add portfolio variance endpoint`

This format is required by `governance_sync.yml` to:
- Parse the EPIC and ST IDs
- Close the corresponding GitHub issue automatically on push

Every commit to an `exec/**` branch must follow this format. Commits without the prefix are non-compliant.

### 8.3 Issue Lifecycle

| State | Trigger | Who |
|-------|---------|-----|
| `Open` | Created at Phase 1B (`sync gh`) or at STEP 0 of this routine if missing | Engine |
| `In Progress` | Engine assigns itself (or human) and updates the issue | Engine |
| `Closed` | Commit pushed to `exec/**` branch with `[EPIC-xx][ST-xx]` prefix → `governance_sync.yml` closes automatically | CI/CD |

If a GitHub issue does not exist for an ST item at invocation: create it before beginning work on that item.

### 8.4 Pull Request Requirements

One PR per EPIC branch → `main`.

PR title must satisfy `quality_gate.yml`:

```
[EPIC-xx] <description of epic outcome>
```

Example: `[EPIC-01] Portfolio analytics foundation`

PR body must include:
- Sprint goal reference
- List of ST items in this PR with status
- Acceptance criteria summary
- QA sign-off reference (required before merge is permitted)
- Link to `execution_state.json` for this cycle

PRs may not be merged until the merge gate (Section 13) passes.

---

## 9. Execution State (Required)

All per-item progress is recorded in:

`claude/cycles/<cycle_id>/execution_state.json`

### 9.1 Schema

```json
{
  "cycle_id": "<cycle_id>",
  "sprint_goal": "<text>",
  "invoked_utc": "<ISO-8601>",
  "mode": "strict|standard",
  "status": "Running|Blocked|Completed|Sealed",
  "last_updated_utc": "<ISO-8601>",

  "epics": {
    "EPIC-01": {
      "status": "not_started|in_progress|blocked|done|merged",
      "branch": "exec/<cycle_id>/EPIC-01",
      "pr_number": null,
      "pr_status": "none|open|approved|merged",
      "qa_signed_off": false,
      "stories": {
        "ST-01": {
          "title": "<text>",
          "classification": "autonomous|delegated_backend|delegated_frontend|delegated_qa|delegated_decision",
          "status": "not_started|in_progress|blocked_backend|blocked_frontend|blocked_qa|blocked_decision|done|merged",
          "assigned_to": "engine|human|qa|<role>",
          "github_issue": null,
          "branch": "exec/<cycle_id>/EPIC-01",
          "commit_sha": null,
          "delegation_record_id": null,
          "blocked_since_utc": null,
          "unblock_criteria": null,
          "completed_utc": null,
          "acceptance_verified": false,
          "notes": ""
        }
      }
    }
  },

  "blocked_items": [],
  "delegated_items": [],
  "completed_items": [],
  "open_escalations": [],

  "merge_gate": {
    "epics_merged": [],
    "epics_pending": [],
    "all_merged": false
  },

  "sealed": false,
  "sealed_utc": null
}
```

### 9.2 State Update Rule (Hard Requirement)

`execution_state.json` must be updated:
- After every ST item status change
- After every GitHub operation (branch create, commit, issue update, PR open)
- After every delegation record is created
- After every escalation is filed
- Before and after the merge gate runs

If the state file cannot be updated: halt.

---

## 10. Resumability (State-Driven Execution)

This routine is fully resumable across sessions.

On invocation:
1. Load `.claude_current_state.json` to identify `active_cycle`.
2. Check for `claude/cycles/<cycle_id>/execution_state.json`.
3. If it exists: resume from the first item whose status is `not_started`, `in_progress`, or `blocked_*` (after re-evaluating whether blocks are cleared).
4. If it does not exist: initialise from the backlog slice (STEP 0).
5. Never re-execute items already marked `done` or `merged`.

### 10.1 Block Re-Evaluation on Resume

On every resume, for each item in `blocked_items`:
- Re-check the unblock criteria.
- If the criteria are now met (e.g., human has pushed a commit, QA has signed off): transition the item to `in_progress` and continue.
- If not met: keep blocked and report status to the user.

---

## 11. Delegation Log (Append-Only)

All delegated tasks must be recorded in:

`claude/cycles/<cycle_id>/delegation_log.md`

This file is append-only. Do not edit previous entries.

### 11.1 Header (create on first write)

```
Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
```

### 11.2 Delegation Record Format

Each entry must include:

```
## DEL-<YYYYMMDD>-<nn>

- **ST Item:** ST-xx — <title>
- **EPIC:** EPIC-xx
- **Classification:** delegated_backend | delegated_frontend | delegated_qa | delegated_decision
- **Assigned to:** Head of Engineering | Base44 Frontend Prompt Owner | Director of Quality | <named role>
- **GitHub Issue:** #<number>
- **Branch:** exec/<cycle_id>/EPIC-xx
- **Delegated at:** <ISO-8601 UTC>
- **What is needed:** <specific, actionable description — not generic>
- **Spec reference:** <path to locked canonical spec that governs this item>  [backend/frontend items only]
- **Base44 prompt draft:** <attached or linked>  [delegated_frontend items only]
- **Unblock criteria:** <what must be true / what evidence is required>
- **Commit format required:** `[EPIC-xx][ST-xx] <description>` pushed to `exec/<cycle_id>/EPIC-xx`
- **Status:** Pending | In Progress | Unblocked | Cancelled
```

The "What is needed" field must be specific enough that the assignee can act without further clarification. Vague delegations are non-compliant.

For `delegated_backend` items: "What is needed" must reference the specific layer(s) required (router / service / database) and the canonical spec section that governs the behaviour.

For `delegated_frontend` items: the Base44 prompt draft field is mandatory. An incomplete prompt is non-compliant — it must cover all six required sections (context, change, API contract, behaviour rules, non-functional rules, expected outcome).

---

## Mandatory End-to-End Process

## STEP -1 — Preflight Gate (Hard Gate)

**First action:** Read `claude/cycles/<cycle_id>/execution_state.json` if it exists.
If it exists and `status` is not `not_started`: you are resuming — see Resumability Protocol in `claude/system/shared_standards.md` §8.
If it does not exist: this is a fresh run. Continue below.

Shared standards (escalation format, halt report format, gh CLI commands, identifier conventions): `claude/system/shared_standards.md`

Purpose: fail fast before any execution begins.

### -1.1 Required Files Present

Verify:
- `.claude_current_state.json` (and `active_cycle` is populated)
- `claude/charter/team_charter.md`
- `claude/charter/document_lifecycle_guide.md`
- `claude/strategy/strategy_rules.md`
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md`
- `claude/cycles/<cycle_id>/sprint_backlog.md`
- `claude/cycles/<cycle_id>/sprint_goal.md`

If any are missing: halt and report exactly which.

### -1.2 Active Cycle Status Check

Read `.claude_current_state.json`:
- `status` must be `Committed` or `Validated` or `Published` (i.e., the release plan is complete).
- If `status` is `Blocked`: halt — the release cycle has unresolved escalations. Resolve them via the Release Planning Engine before executing.
- If `status` is `Initialized` or `Planning`: halt — the release plan is not yet complete.

### -1.3 Backlog Slice Integrity

Verify `stage4_backlog_slice.md`:
- Contains at least one EPIC with `EPIC-xx` IDs.
- Each EPIC contains at least one story with `ST-xx` IDs.
- All IDs are unique within the slice.

If IDs are missing or duplicated: halt. Do not invent IDs.

### -1.4 Sprint Backlog Acceptance Criteria Check

Verify `sprint_backlog.md`:
- Product Owner sign-off is recorded.
- Each ST item in the sprint scope has acceptance criteria defined.

If any in-scope ST item lacks acceptance criteria:
- In `strict` mode: halt and report which items are missing criteria.
- In `standard` mode: flag as a blocker, classify the item as `delegated_decision`, and continue with remaining items.

### -1.5 Required Authority Roles Exist

Verify agent files in `claude/agents/` for all required roles (Section 6). If any missing: halt.

### -1.6 Write Permission Test

Create a temporary marker file in `claude/cycles/<cycle_id>/` and confirm it can be written. Remove it. If write fails: halt.

---

## STEP 0 — Initialise Execution State (Hard Requirement; first write)

Create `claude/cycles/<cycle_id>/execution_state.json` if it does not exist.

1. Parse `stage4_backlog_slice.md` to extract all EPIC and ST items in dependency order.
2. Cross-reference with `sprint_backlog.md` to confirm which items are in sprint scope.
3. For each ST item: classify (`autonomous` / `delegated_backend` / `delegated_frontend` / `delegated_qa` / `delegated_decision`) based on acceptance criteria and item type.
4. Initialise all statuses to `not_started`.
5. Set cycle-level status to `Running`.

Update `.claude_current_state.json`:
- `status` → `Executing` (new state; does not affect Release Planning Engine semantics)

If execution_state.json already exists: resume (do not reinitialise). Perform STEP 0 only for items with status `not_started`.

---

## STEP 1 — GitHub Issue Preflight

For each ST item in the sprint scope:

1. Check `execution_state.json` for `github_issue` value.
2. If `null` or absent: search GitHub for an existing issue matching the ST ID and title.
3. If found: record the issue number in `execution_state.json`.
4. If not found: create the issue with:
   - Title: `[ST-xx] <title>`
   - Body: acceptance criteria from `sprint_backlog.md`, epic reference, sprint goal
   - Label: `sprint`, `EPIC-xx`
5. Update `execution_state.json` with all issue numbers.

Do not create duplicate issues. Check before creating.

---

## STEP 2 — Branch Preflight

For each EPIC in scope:

1. Check whether branch `exec/<cycle_id>/EPIC-xx` exists (local or remote).
2. If it does not exist: create it from the current `main`.
3. If it exists: verify it is based on `main` (or the declared base branch). If it has diverged: flag as a blocker, record in escalations, halt this EPIC (continue other EPICs).
4. Record branch name in `execution_state.json`.

---

## STEP 3 — Execution Loop (Per EPIC, Per ST Item)

Work through EPICs in dependency order. Within each EPIC, work through ST items in dependency order.

### 3.1 For each ST item

#### 3.1.A If `autonomous`:

1. Execute the work defined in the acceptance criteria.
2. Commit to the EPIC branch with format: `[EPIC-xx][ST-xx] <imperative description>`
3. Push to `exec/<cycle_id>/EPIC-xx`.
4. `governance_sync.yml` will close the GitHub issue automatically on push.
5. Verify issue is closed (re-check after push).
6. Mark item `done` in `execution_state.json`.
7. Set `acceptance_verified = true` once acceptance criteria are confirmed met.
8. Set `commit_sha` to the pushed commit.

#### 3.1.B If `delegated_backend` or `delegated_frontend`:

1. Create or update the GitHub issue to `In Progress` with delegation note.
2. Create a delegation record in `delegation_log.md` (Section 11).
   - For `delegated_backend`: include spec reference and required layer(s) (router / service / database).
   - For `delegated_frontend`: include the complete Base44 prompt draft (all six sections).
3. Set item status to `blocked_backend` or `blocked_frontend` in `execution_state.json`.
4. Record `delegation_record_id` and `unblock_criteria` in the item.
5. Surface the delegation to the assigned role with:
   - Exactly what is needed (with spec reference or Base44 prompt draft)
   - The branch to commit to
   - The required commit format: `[EPIC-xx][ST-xx] <description>`
   - The issue number
6. **Continue to the next ST item.** Do not stall.

**Unblock detection (on resume):**
- Check whether a commit matching `[EPIC-xx][ST-xx]` has been pushed to the branch since delegation.
- If yes: transition item to `done`, verify acceptance criteria, update state.
- If no: keep blocked and report status to user.

#### 3.1.C If `delegated_qa`:

1. Complete all autonomous work for the item.
2. Commit and push per 3.1.A.
3. Set item status to `blocked_qa`.
4. Create a delegation record: QA sign-off required.
5. Surface to Director of Quality:
   - What was built
   - The acceptance criteria to verify
   - The commit SHA
   - How to signal sign-off (comment on PR / issue)
6. Continue to next item.

**Unblock detection:** Check PR or issue for QA sign-off comment. If present and from Director of Quality: transition to `done`, set `qa_signed_off = true`.

#### 3.1.D If `delegated_decision`:

1. Create an escalation record in `execution_escalations.md`.
2. Set item status to `blocked_decision`.
3. Surface to the owning authority:
   - The decision required
   - The unblock criteria
   - The SLA (default: 24 hours for lifecycle; 72 hours for strategy)
4. Continue to next item.

**Unblock detection:** Check escalation record for Resolved or Accepted Risk disposition. If resolved: re-classify item and resume.

### 3.2 EPIC Completion

An EPIC is `done` (not yet `merged`) when all of its ST items are `done`.

When an EPIC is done:
1. Open a pull request: `exec/<cycle_id>/EPIC-xx` → `main`
2. PR title: `[EPIC-xx] <epic description>`
3. PR body: per Section 8.4
4. Update `execution_state.json`: EPIC `pr_status` = `open`, `pr_number` = PR number.
5. Do not merge. The merge gate (STEP 4) governs this.

---

## STEP 4 — Merge Gate (Hard Gate, Per EPIC)

A PR may only be merged when **all** of the following are true:

| Condition | Required State |
|-----------|---------------|
| All ST items in EPIC | `done` (not `blocked_*`) |
| Acceptance criteria | verified for all ST items |
| QA sign-off | present on PR (comment from Director of Quality) |
| Product Owner acceptance | recorded (comment on PR or in `sprint_backlog.md`) |
| `quality_gate.yml` CI | passed (PR title has `[EPIC-xx]`, all checks green) |
| No open escalations | for items in this EPIC |

If all conditions pass:
1. Merge the PR (squash or merge as configured).
2. Update `execution_state.json`: EPIC `pr_status` = `merged`, `status` = `merged`.
3. Update `merge_gate.epics_merged`.

If any condition fails: do not merge. Record which condition is unmet. If QA or Product Owner has not responded within their SLA: file an escalation record.

**The engine may not self-approve a merge.** QA sign-off and Product Owner acceptance are always required and must come from the relevant authority.

---

## ESCALATION HANDLING SUBROUTINE (Callable)

Trigger: whenever a step produces a blocker that cannot be resolved autonomously.

Create or append to: `claude/cycles/<cycle_id>/execution_escalations.md`

Escalation entry format, SLAs, append-only rule, and Accepted Risk constraints: `claude/system/shared_standards.md` §4.
Use `ESC-EXEC-YYYYMMDD-nn` as the ID prefix (to distinguish from Release Planning escalations which use `ESC-YYYYMMDD-nn`).

After processing escalations: update `execution_state.json.open_escalations`.

If any escalations remain `Open` with `Blocks execution: Yes`: set cycle status to `Blocked` and output the halt report per `claude/system/shared_standards.md` §5.

---

## STEP 5 — Sprint Close (All EPICs Merged)

Trigger: all EPICs in `execution_state.json.merge_gate.epics_pending` are empty (all merged).

### 5.1 Acceptance Summary

For each ST item: confirm `acceptance_verified = true`. If any are false and the item is `merged`: this is a quality gap — file an escalation.

### 5.2 Items Returned to Backlog

Any ST item that is `blocked_backend`, `blocked_frontend`, or `blocked_decision` at sprint close and will not be completed in this sprint:
- Set status to `returned_to_backlog`.
- Note must be added to `claude/backlog/backlog.md` (one line, referencing this cycle_id and the reason).
- This is the only permitted write to `backlog.md` in this routine.

### 5.3 Sprint Close Record

Create: `claude/cycles/<cycle_id>/sprint_close.md`

Must include:
- Sprint goal
- Items Done (with commit SHAs)
- Items Returned to Backlog (with reason)
- Items Delegated and outstanding (with delegation record IDs)
- QA sign-offs received
- Open escalations (if any)
- Net outcome vs sprint goal

### 5.4 Lessons Learnt

Create: `claude/cycles/<cycle_id>/lessons_learnt_execution.md`

Record:
- Delegation patterns (what kept needing humans that could be improved)
- GitHub integration friction
- Acceptance criteria gaps
- Governance process friction
- Immediate improvements that can be actioned now (if any, apply and record what changed)

Do not re-litigate scope decisions. Record only what improves the process.

---

## STEP 6 — Global State Update (Hard Requirement)

After sprint close:

Update `.claude_current_state.json`:
- `status` → `Sprint_Complete`
- `last_sync_utc` → now

If all roadmap items for this release are complete:
- Flag `release_complete: true` in `.claude_current_state.json`.
- Surface to Product Owner: the release is ready for Phase 1 (Roadmap Rebalance) or direct Phase 1B (next release planning).

---

## STEP 7 — Seal Execution Record (Hard Gate)

Once sprint close and global state update are complete:

1. Set `execution_state.json.sealed = true`, `sealed_utc = now`.
2. Set `execution_state.json.status = Sealed`.
3. No further modifications to `execution_state.json` are permitted.
4. No further modifications to `delegation_log.md` or `execution_escalations.md` are permitted.

**Terminal state rule:** Once sealed, the execution record is immutable. Any correction or amendment requires a new execution cycle referencing this `cycle_id`.

---

## STEP 8 — Commit & Push Cycle Artefacts

Stage and commit all cycle artefacts created or modified by this routine:

```
git add claude/cycles/<cycle_id>/execution_state.json
git add claude/cycles/<cycle_id>/delegation_log.md
git add claude/cycles/<cycle_id>/execution_escalations.md  (if created)
git add claude/cycles/<cycle_id>/sprint_close.md
git add claude/cycles/<cycle_id>/lessons_learnt_execution.md
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Sprint execution closed: <cycle_id>"
git push origin <current-branch>
```

If git operations are unavailable: output the exact files to stage and the commit message. Mark as "Ready to commit."

---

## 12. Completion Condition

The run is complete only if:

- `execution_state.json.status = Sealed`
- All in-scope ST items have a recorded outcome (`done`, `merged`, or `returned_to_backlog`)
- `sprint_close.md` exists and is lifecycle-compliant
- `lessons_learnt_execution.md` exists
- `.claude_current_state.json` updated to `Sprint_Complete`
- No open escalations with `Blocks execution: Yes`
- STEP 8 commit complete (or commit manifest produced)

---

## 13. Governance Invariants

- **No autonomous merge.** The engine never merges without QA sign-off and Product Owner acceptance.
- **No scope change.** The backlog slice is sealed. The engine executes what is there.
- **No strategy boundary decisions.** The Strategy Rules owner decides; the engine surfaces and parks.
- **Delegation is explicit and tracked.** No silent assumptions about human completion.
- **Commit format is non-negotiable.** `[EPIC-xx][ST-xx]` prefix on every commit to `exec/**`. `governance_sync.yml` depends on it.
- **PR title is non-negotiable.** `[EPIC-xx]` in title. `quality_gate.yml` blocks merge without it.
- **Every block is recorded.** Nothing is silently skipped. Blocked items are documented in `execution_state.json` and surfaced to the user.
- **Delivery pressure does not override quality gates.** Director of Quality sign-off is required on every EPIC before merge, regardless of timeline.