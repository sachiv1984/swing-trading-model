**Owner:** Head of Specs Team
**Status:** Active
**Version:** 3.15
**Last Updated:** 2026-05-06
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

Apply the Lifecycle Guard (valid from-states: `Sprint_Planning_Complete`; `Executing` on resume) per `claude/system/shared_standards.md §10` before executing any step.

No other user input may trigger this routine.

**Tool call budget:** This routine typically requires 20–60 tool calls for a standard sprint. Proceed through steps without asking for confirmation unless a hard gate fires. When a hard gate fires, output the halt report (per `claude/system/shared_standards.md` §5) and wait.

### execution_state.json Ownership (Multi-EPIC Sprints)

When a sprint has more than one EPIC branch executing in parallel, a single EPIC branch is designated the **execution_state.json owner** at sprint planning time. This is the first EPIC branch in execution order (Sprint 1 primary EPIC, or the first in dependency order). All other EPIC branches **must check for the existence of `execution_state.json` before creating their own version**. If the file already exists, continue from the existing file — do not overwrite. If the file does not exist, the current branch is the first to execute; create it.

**Merge order advisory:** If a `execution_state.json` conflict arises when merging multiple EPIC branches, `CLAUDE.md §8` (Cross-EPIC Merge Conflict Resolution) governs resolution. The rule of thumb: accept story completion data (status: done, commit_sha, acceptance_verified) from the branch; never revert a story from `done` → `blocked`; take the union of completed items.

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
| Backlog slice | See note below — may be amended | Authoritative list of EPICs and STs for this sprint |
| Sprint backlog | `claude/cycles/<cycle_id>/sprint_backlog.md` | Confirms scope, acceptance criteria, ownership |
| Sprint goal | `claude/cycles/<cycle_id>/sprint_goal.md` | Frames the sprint intent |
| Workforce capacity | `claude/roadmap/workforce_capacity.md` | Confirms available skills/FTE |
| Execution state | `claude/cycles/<cycle_id>/execution_state.json` | Per-item progress (created by this routine) |

**Backlog slice source-of-truth rule:** At STEP -1, check `.claude_current_state.json` for `amended_backlog_slice_path`. If this field is present and non-empty, that file is the authoritative backlog slice for this sprint — use it in place of `stage4_backlog_slice.md` throughout. If absent or empty, use `stage4_backlog_slice.md`. Never execute from `stage4_backlog_slice.md` if an amendment has sealed. The authoritative slice is sealed — this engine may not modify it.

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
| `delegated_frontend` | Requires frontend implementation — engine-autonomous (preferred) or via external frontend owner if engine cannot complete | Frontend Specifications & UX Owner | Default to autonomous; only delegate if engine-incapable |
| `delegated_qa` | Requires Director of Quality sign-off before marking done | Director of Quality | Complete all autonomous work, then await QA gate |
| `delegated_decision` | Requires a named authority to decide before proceeding (e.g., strategy boundary question, scope ambiguity) | Named authority per domain | Escalate, park, continue other items |

**Classification rules:**
- Backend ST items (new endpoint, service function, database query, settings field): `delegated_backend`
- Frontend ST items (new component, page change, UI behaviour): `autonomous` if the engine can implement against the spec; `delegated_frontend` only if external frontend ownership is genuinely required (LL-v2.3-CL-01)
- Spec, documentation, configuration, or scaffolding with unambiguous acceptance criteria: `autonomous`
- Items requiring QA verification of behavioural conformance: `delegated_qa` (after any `delegated_backend` or `delegated_frontend` work completes)
- Items with unresolved authority or scope questions: `delegated_decision`
- **Autonomous candidate pattern (LL-v1.10-P3-3):** If the item description is "refactor component X to call backend endpoint Y" with no UX change, and the API method already exists client-side (e.g. in `api.js`), classify as `autonomous` — this is a pure data-fetching swap with no delegation risk. Confirm with Product Owner if scope ambiguity exists.

If classification is ambiguous: classify as `delegated_decision` and flag for the Product Owner.

**Backend delegation note:** The engine must confirm a canonical spec is locked before delegating a backend item (`claude/agents/backend_engineering_patterns_owner.md` §4 Step 1). If the spec is in draft, raise to Head of Specs Team before delegating to Head of Engineering.

**Frontend delegation note (LL-v2.3-CL-01 — autonomous model default from 2026-03-26):** Frontend stories default to `autonomous` engine delivery. Classify as `delegated_frontend` only if the story genuinely cannot be completed by the engine. In that case, the delegation record must include: context, change required, API contract reference, behaviour rules, non-functional rules, and expected outcome.

**Mid-sprint reclassification (LL-v2.3-EX-02):** If a story's classification changes after a delegation record has already been created (e.g., `delegated_frontend` → `autonomous` because the frontend delivery model changed, or `delegated_backend` → `autonomous` because spec ambiguity was resolved), update the delegation log entry **immediately**:
- Set the entry's `Status` to `Cancelled` with a note stating the reclassification reason and new classification (e.g., "Reclassified to autonomous — frontend delivery model switched to engine per Product Owner authority 2026-03-26").
- Update `execution_state.json` classification for the item.
- Do **not** wait until STEP 5.0 to record this — in-flight updates prevent bulk rework at sprint close (same principle as LL-v2.2-EX-01).
- If a new delegation record is created for the same item under the new classification, cross-reference the cancelled entry.

### 5.3 Agent-Mediated Sign-Off

When an ST item's seal condition or acceptance criteria require sign-off from a named role, the engine must attempt agent-mediated sign-off before surfacing to the user.

**Protocol:**

1. Identify the required role from the seal condition in `sprint_backlog.md`.
2. Locate the agent file: `claude/agents/<role_slug>.md` (e.g. "Head of Specs Team" → `head_of_specs_team.md`).
3. If the agent file exists: invoke a general-purpose subagent with the role's charter and the artefact(s) to review. The subagent evaluates against the role's §5 (quality bar) and any domain-specific standards in the charter.
4. The subagent returns: `Approved` or `Blocked` + findings list.
5. If `Approved`: record sign-off in `execution_state.json` `sign_off_record` for the item; proceed.
6. If `Blocked`: apply the findings in-session, re-invoke the sign-off agent. Maximum 2 retries.
7. If still `Blocked` after 2 retries, or if no agent file exists: surface to the user as a `delegated_decision` block with the outstanding findings listed explicitly.

**Always-human gates (never agent-mediated):**
- Product Owner — sprint scope, goal, and acceptance of sprint close are always human decisions.
- Merge gate — QA sign-off and Product Owner acceptance on PRs are always human.

**Agent-mediated sign-off is appropriate for:**
- Spec sign-offs: Head of Specs Team, API Contracts & Documentation Owner, Data Model & Domain Schema Owner
- Architecture sign-offs where the ADR is already written and the review is against documented criteria
- Any named authority with an agent file where the decision is reviewable against criteria in the role charter

**Sign-off record schema** (added to `execution_state.json` per-story):

```json
"sign_off_record": {
  "required_by": "Head of Specs Team",
  "method": "agent_mediated",
  "status": "cleared",
  "findings_applied": ["list of findings addressed"],
  "cleared_utc": "ISO-8601"
}
```

`method` is `"agent_mediated"` when this protocol ran, or `"human"` when surfaced to and resolved by the user.

---

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
- `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (one per EPIC, created at EPIC completion)
- `claude/cycles/<cycle_id>/sprint_close.md` (create at close only)
- `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (append-only — Phase 3 section; create if absent)
- Source files required by ST items (within repo, outside governance folders)
- Canonical spec files (deviation documentation only — §9 Known Deviation Standard; no other spec edits permitted)
- `.claude_current_state.json` (status updates only)

You must **not** modify:
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed)
- `claude/cycles/<cycle_id>/amendments/*/amended_backlog_slice.md` (sealed)
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
  "backlog_slice_source": "claude/cycles/<cycle_id>/stage4_backlog_slice.md | <amended path>",
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
      "qa_evidence_log": "claude/cycles/<cycle_id>/qa_evidence_EPIC-01.md",
      "test_scenarios": [],
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
          "spec_references": [],
          "deviations_filed": false,
          "last_completed_substep": null,
          "sign_off_record": null,
          "notes": ""
          // spec_references (LL-v2.2-EX-04 — second recurrence): Items that are
          // delegated_qa documentation artefacts (test scenario files, readiness
          // assessments) OR autonomous infrastructure/tooling items with no prior
          // canonical spec MAY leave spec_references empty. REQUIRED: set notes
          // field to exactly "no prior spec applicable". This phrase is the
          // exemption token — the completion condition check and delivery
          // verification MUST NOT flag spec_references:[] as a traceability gap
          // when this phrase is present in the notes field.
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

`backlog_slice_source` records the exact file path of the authoritative backlog slice used for this execution. Set at STEP 0. The Delivery Verification Engine may use this to confirm scope provenance.

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

### 10.2 Sub-Item Resume

For items with `status = in_progress` and a non-null `last_completed_substep`:
- Read `last_completed_substep` to identify the last completed sub-step within the ST item execution (e.g., `"3.1.A.commit"` for a committed autonomous item awaiting issue close verification).
- Resume from the next sub-step. Do not re-execute the substep recorded in `last_completed_substep`.
- Update `last_completed_substep` after each discrete sub-step completes, before any network or filesystem operation that could fail.

---

## 11. Delegation Log (Append-Only)

All delegated tasks must be recorded in:

`claude/cycles/<cycle_id>/delegation_log.md`

This file is append-only. Do not edit previous entries.

Schema: per `claude/system/shared_standards.md §16.3` (header format, delegation record format, compliance rules).

---

## Mandatory End-to-End Process

## STEP -1 — Preflight Gate (Hard Gate)

**First action:** Read `claude/cycles/<cycle_id>/execution_state.json` if it exists.
If it exists and `status` is not `not_started`: you are resuming — see Resumability Protocol in `claude/system/shared_standards.md` §8.
If it does not exist: this is a fresh run. Continue below.

Shared standards (escalation format, halt report format, gh CLI commands, identifier conventions): `claude/system/shared_standards.md`

Purpose: fail fast before any execution begins.

### -1.1 Required Files and Backlog Slice Source

Verify:
- `.claude_current_state.json` (and `active_cycle` is populated)
- `claude/charter/team_charter.md`
- `claude/charter/document_lifecycle_guide.md`
- `claude/strategy/strategy_rules.md`
- `claude/cycles/<cycle_id>/sprint_backlog.md`
- `claude/cycles/<cycle_id>/sprint_goal.md`

Check `amended_backlog_slice_path` in `.claude_current_state.json`:
- If present and non-empty: this is the authoritative backlog slice. Verify the file exists — if not, halt and report. Record this path for use throughout this run.
- If absent or empty: verify `claude/cycles/<cycle_id>/stage4_backlog_slice.md` exists — if not, halt and report. Record this path for use throughout this run.

**Sprint backlog index (IMP-25):** Load `claude/cycles/<cycle_id>/sprint_backlog_index.json` if it exists. When `--epic` is specified, use the index to identify which ST items belong to the scoped EPIC and their `backlog_slice_refs` — read only those items from `sprint_backlog.md` rather than the full document. If the index does not exist: fall back to reading the full `sprint_backlog.md`.

If any required file is missing: halt and report exactly which.

### -1.2 Active Cycle Status Check (Hard Gate)

Read `.claude_current_state.json`:
- `status` must be `Sprint_Planning_Complete` (fresh run) or `Executing` (resuming an in-progress sprint).
- `sprint_sealed` must be `true`.
- If `status` is `Blocked`: halt — the cycle has unresolved escalations. Resolve them before executing.
- If `status` is anything other than `Sprint_Planning_Complete` or `Executing`: halt — Sprint Planning has not completed or the cycle is in an unexpected state. Check that `plan sprint` has been completed and sealed before invoking `run sprint`.

### -1.3 Sprint Backlog Sealed (Hard Gate)

Verify `sprint_backlog.md`:
- Status field must be `Sealed`.
- Product Owner sign-off must be recorded — no `[AWAITING SIGN-OFF]` fields remaining.

If either condition fails: halt — Sprint Planning sign-off gate was not completed. Re-invoke `plan sprint` to resolve outstanding sign-off items before proceeding.

### -1.4 Backlog Slice Integrity

Verify the authoritative backlog slice file (identified in STEP -1.1):
- Contains at least one EPIC with `EPIC-xx` IDs.
- Each EPIC contains at least one story with `ST-xx` IDs.
- All IDs are unique within the slice.

If IDs are missing or duplicated: halt. Do not invent IDs.

### -1.5 Acceptance Criteria Check

Verify `sprint_backlog.md`:
- Each ST item in the sprint scope has acceptance criteria defined.

If any in-scope ST item lacks acceptance criteria:
- In `strict` mode: halt and report which items are missing criteria.
- In `standard` mode: flag as a blocker, classify the item as `delegated_decision`, and continue with remaining items.

### -1.6 Required Authority Roles Exist

Verify agent files in `claude/agents/` for all required roles (Section 6). If any missing: halt.

### -1.7 Write Permission Test

Create `claude/cycles/<cycle_id>/.write_test` and confirm it can be written. Remove it immediately. If write fails: halt. If not removed here, STEP 0 must clean it up before proceeding.

---

## STEP 0 — Initialise Execution State (Hard Requirement; first write)

**Cleanup:** If `claude/cycles/<cycle_id>/.write_test` exists (left from STEP -1.7 on a previous interrupted run), delete it now before proceeding.

Create `claude/cycles/<cycle_id>/execution_state.json` if it does not exist.

**Index-guided load (IMP-25):** If `sprint_backlog_index.json` was loaded in STEP -1.1 and `--epic` is scoped: use the index `backlog_slice_refs` for the scoped EPIC to read only the relevant AC entries from `stage4_backlog_slice.md`. Do not load the full backlog slice when the index provides the exact section anchors needed.

1. Parse the authoritative backlog slice (identified in STEP -1.1) to extract all EPIC and ST items in dependency order.
2. Record `backlog_slice_source` in `execution_state.json` — the exact file path used.
3. Cross-reference with `sprint_backlog.md` to confirm which items are in sprint scope.
4. For each ST item: classify (`autonomous` / `delegated_backend` / `delegated_frontend` / `delegated_qa` / `delegated_decision`) based on acceptance criteria and item type.
5. For each ST item: populate `spec_references` — the canonical spec file path(s) and section heading(s) this item implements:
   - `delegated_backend`: **mandatory** — must name the locked spec file and section before delegation proceeds (e.g., `["docs/specs/api_contracts/portfolio_endpoints.md#POST /portfolio/size"]`)
   - `delegated_frontend`: record the frontend spec file and page/component section (e.g., `["docs/specs/frontend/pages/positions.md#Position Entry Form"]`)
   - `autonomous`: record spec if one governs the work; leave `[]` only if purely infrastructural
   - `delegated_decision`: leave `[]` until resolved — populate when re-classified
   If a `delegated_backend` item has no lockable spec reference: classify as `delegated_decision` instead and surface to Head of Specs Team.
6. For each EPIC: check `docs/testing/` for existing test scenario files referencing the EPIC ID or any of its ST items. Record found scenario file paths in `execution_state.json` under the EPIC's `test_scenarios` field. If none found: set `test_scenarios: []`. The verification engine will use this to confirm which scenarios were run.
7. Initialise all statuses to `not_started`.
8. Set cycle-level status to `Running`.

Update `.claude_current_state.json`:
- `status` → `Executing`

`Executing` is a valid intermediate status between `Sprint_Planning_Complete` and `Sprint_Complete`. It is documented in the guide's lifecycle table and cycle trigger table. Phase 4 (`run delivery verification`) may not be invoked while status is `Executing` — Phase 3 must complete and status must reach `Sprint_Complete` first.

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

1. Execute the work defined in the acceptance criteria. **Test scenarios advisory (ST-13):** When tests are created as part of this work, populate `test_scenarios` in `execution_state.json` for the parent EPIC with the test file paths (e.g. `tests/test_screener_service.py`). This is non-blocking — story execution does not halt if the field is not updated immediately — but it must be populated before the EPIC-level QA evidence log is created at STEP 3.2.A.
2. Confirm `spec_references` is populated in `execution_state.json` for this item. If empty and a spec exists: populate now before proceeding.
3. Commit to the EPIC branch with format: `[EPIC-xx][ST-xx] <imperative description>`
4. Push to `exec/<cycle_id>/EPIC-xx`.
5. `governance_sync.yml` will close the GitHub issue automatically on push.
6. Verify issue is closed (re-check after push).
7. Mark item `done` in `execution_state.json`.
8. Set `acceptance_verified = true` once acceptance criteria are confirmed met.
9. Set `commit_sha` to the pushed commit.
10. Deviation check: compare implementation against canonical spec.
    - If no deviation: set `deviations_filed = true` (meaning "deviation check completed; none found").
    - If a deviation exists: document it in the canonical spec per `claude/charter/document_lifecycle_guide.md` §9 (description, canonical requirement, priority P0–P3, target resolution release, owner, backlog reference). Set `deviations_filed = true` once filed. A P0 deviation blocks the merge gate — escalate immediately.
    - **Deviation type distinction (LL-v1.10-P4-2):** If the deviation is "endpoint/feature absent from spec" (the spec does not define this thing at all), file in `qa_evidence_EPIC-xx.md` and backlog only — the canonical spec is not the right home for an absence note. If the deviation is "implementation differs from what the spec requires" (the spec defines it, but the implementation diverges), file in the canonical spec as above.

11. **Sign-off gate:** If the item's seal condition in `sprint_backlog.md` names a required sign-off role: invoke agent-mediated sign-off per §5.3. Do not mark `acceptance_verified = true` until `sign_off_record.status = "cleared"`. Record outcome in `sign_off_record` in `execution_state.json`.

12. **Post-story test files check (OA-04 / ST-09):** If this story created any new test files (in `tests/` or `tests/e2e/`), populate `test_scenarios` in `execution_state.json` for the parent EPIC with those file paths **now**, before advancing to the next story. Do not defer this step to STEP 3.2.A.

13. **Cross-spec selector check (LL-v3.2-P3-02):** If this story modifies, replaces, removes, or renames a DOM element (e.g. changes a component, removes a checkbox, renames a form field), scan all existing Playwright spec files in `tests/e2e/` for selectors targeting that element (by ID, data-testid, role, or class name). If any stale selectors are found, update them in the same commit before pushing. This prevents CI failures in unrelated test files caused by UI changes in this story.

**Pre-met path (LL-v2.4-P4-02):** If an item's acceptance criteria were satisfied by work completed in a prior sprint (item classified `pre-met` or notes field records `AC pre-met on main`):
- Verify by code review / prompt review that all AC items are still met on `main`.
- Mark `status = done`, `acceptance_verified = true`, note the prior commit SHA where the work was done.
- **A `qa_evidence_EPIC-xx.md` entry is still required.** Create or append an entry recording: what the pre-met item covers, how verification was conducted (code review / prompt review), and DoQ sign-off. Pre-met does not mean unverified — the QA evidence log must document the pre-met verification explicitly.
- Deviation check applies: if the prior implementation diverges from the current sprint's spec, file a deviation.

**Reclassification backfill (CF-01):** If a story is reclassified from `delegated_frontend` to `autonomous` mid-sprint (per LL-v2.3-EX-02), the accepting engine must backfill `test_scenarios` in `execution_state.json` at the time of reclassification. `test_scenarios` must be populated with the test file paths (or set to `"pending — QA & Testing Owner to author before next sprint on this domain"` if no test files exist yet) before the story's QA evidence log entry is written. Do not proceed to STEP 3.2.A for the parent EPIC until `test_scenarios` is populated for all reclassified stories in that EPIC.

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
  - Confirm `spec_references` is populated (fill now if missing — ask the assignee which spec section was implemented).
  - Check for deviations: if implementation diverges from the spec, file the deviation in the canonical spec before setting `deviations_filed = true`.
  - **HARD GATE (LL-v2.2-EX-01 — second recurrence): Update the delegation log entry** (per `shared_standards.md §16.3`) — set status to `Unblocked` and note the commit SHA **in the same step as setting item status to `done` in `execution_state.json`.** These two writes are atomic. Do not advance to the next ST item until both are recorded. Batching delegation log updates to STEP 5.0 is a process violation — prior advisory language was applied twice and proven insufficient.
- If no: keep blocked and report status to user.

#### 3.1.C If `delegated_qa`:

1. Complete all autonomous work for the item.
2. Confirm `spec_references` is populated. Populate now if missing.
3. Commit and push per 3.1.A steps 3–9 (deviation check applies here too).
4. Set item status to `blocked_qa`.
5. Create `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` if it does not already exist (use the header and structure defined in Section 3.2.A). Then append an entry for this ST item:
   - ST item ID and title
   - Spec references (from `spec_references` field)
   - Acceptance criteria (from `sprint_backlog.md`)
   - Commit SHA
   - What was built (one paragraph)
   - Test scenarios to execute: list any from `execution_state.json.epics.EPIC-xx.test_scenarios`; if none, derive from spec + acceptance criteria
   - Open section for QA findings (Director of Quality fills this)
   - Open section for disposition (Pass / Pass with notes / Fail)
   - **Pending implementation note (LL-v2.2-EX-05):** If a test gap is identified in this delegated_qa item and the corresponding implementation story (e.g. the backend endpoint being tested) is not yet `done`, note "pending ST-xx completion" in the test scenarios field rather than flagging as a P1 gap. A test gap against an undelivered feature is expected — it is not a deviation; it becomes actionable once the implementation story ships.
6. Surface to Director of Quality:
   - Link to `qa_evidence_EPIC-xx.md`
   - The specific section for this ST item
   - How to signal sign-off (complete the disposition section + comment on PR)
7. Continue to next item.

**Unblock detection:** Check `qa_evidence_EPIC-xx.md` for completed disposition section AND PR comment from Director of Quality. If both present: transition to `done`, set `qa_signed_off = true` on the EPIC.

#### 3.1.D If `delegated_decision`:

1. Create an escalation record in `execution_escalations.md`.
2. Set item status to `blocked_decision`.
3. Surface to the owning authority:
   - The decision required
   - The unblock criteria
   - The SLA (default: 24 hours for lifecycle; 72 hours for strategy)
4. Continue to next item.

**SLA breach tracking:** Per `claude/system/shared_standards.md §16.4`.

**Unblock detection:** Check escalation record for Resolved or Accepted Risk disposition. If resolved: re-classify item and resume. **HARD GATE (LL-v2.4-EX-01 — third recurrence): Update the delegation log entry** (per `shared_standards.md §16.3`) — set status to `Unblocked` and note the commit SHA in the same step as setting item status to `done` in `execution_state.json`. These two writes are atomic. Do not advance to the next ST item until both are recorded. This gate applies to `delegated_decision` items just as it does to `delegated_backend` and `delegated_frontend`.

### 3.2 EPIC Completion

An EPIC is `done` (not yet `merged`) when all of its ST items are `done`.

When an EPIC is done:

**3.2.A — Consolidate QA Evidence Log (required before PR)**

`claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` should already exist with per-ST-item entries from STEP 3.1.C. If it does not exist (e.g., all items were `autonomous` or `delegated_backend`/`delegated_frontend` with no explicit `delegated_qa` items): create it now using the structure below.

Add or complete the **EPIC-level consolidation block** at the end of the file:

```
Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
```

The consolidation block must include:

**EPIC:** EPIC-xx — <title>
**Cycle:** <cycle_id>
**Sprint goal:** <text>
**Test scenarios used:** <list paths from `test_scenarios` field, or "Derived from spec + AC">

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-xx | <spec file#section> | <one line> | <criteria text> | Pass / Fail | None / DEV-ref |

*(Reconcile any partial per-item entries from STEP 3.1.C into this table. Do not duplicate — one row per ST item.)*

**QA test coverage:**
- Scenarios run: <list scenario file names, or "manual acceptance review">
- Regression areas checked: <list affected spec domains>
- Known deviations filed: <list deviation refs or "None">

**QA sign-off block:** (Director of Quality completes this)
> **Authoring note (LL-v1.10-P4-1):** When completing the sign-off block, update all AC table rows from "Pending"/"Awaiting QA" to "Pass" or "Pass with notes" in the same edit. Sign-off block and AC table must be consistent — leaving rows as "Pending" after signing off creates a documentation inconsistency.
> **Date field requirement (LL-v2.3-EX-01 / ST-04):** The `Date:` field must be non-blank before the PR can be opened (§3.2.B pre-condition, BLG-GOV-18) and before the merge gate runs. A sign-off block with a blank Date: field is incomplete — the PR will be blocked from opening, and Sprint Close STEP 5.1 (LL-v2.0-P4-1) will also block. Fill in the date when signing off, not at sprint close.
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object **(LL-v2.0-P3-4)**
- Signed off by: Director of Quality
- Date: <fill in — must be non-blank (LL-v2.3-EX-01)>
- Comments:

This file is the evidence backing `qa_signed_off = true` in `execution_state.json`. A PR comment alone is not sufficient — this file must exist and the sign-off block must be complete before the merge gate runs.

**Frontend testing gate (LL-v3.1-EX-01 — hard gate):**

Before signing off any EPIC that introduces frontend-visible changes, verify for each observable AC (visible rendering, element presence/absence, colour, interaction, timing):

1. **Check Playwright coverage:** Is there a Playwright test in `tests/e2e/` that exercises this AC? If yes: record the test file and scenario ID in the DoQ comments.
2. **If no Playwright test:** Has a human staging run been performed? If yes: record the staging run date in the DoQ sign-off block.
3. **If neither:** The AC must be noted in the sign-off comments as "code review only — backlog item required". File a backlog item (via `/backlog-add`) for the Playwright test before opening the PR. This is a **hard gate**: the PR may not be opened with observable AC marked "code review only" unless the backlog item reference is recorded in the sign-off comments.

The autonomous class sign-off (BLG-GOV-19) is unavailable for any EPIC with frontend-visible changes — criterion 3 (no frontend-visible change) will not be met.

**Autonomous DoQ sign-off class (BLG-GOV-19):**

When all four of the following qualifying criteria are met, the engine may apply an autonomous DoQ sign-off without Director of Quality review. This class is defined to avoid unnecessary delegation blocks on pure governance or spec documentation EPICs where no behavioural verification is possible.

**Qualifying criteria:**
1. All stories in the EPIC have `delegation_class: autonomous`
2. All AC is verifiable by code review alone — no observable UI behaviour, no staging run required, and no live system interaction
3. No frontend-visible change is introduced by this EPIC
4. Engine signer field is populated as "Sprint Execution Engine (autonomous class)"

When all criteria are met, populate the sign-off block as follows:

```
**Autonomous class eligibility check (BLG-GOV-19):**
- [ ] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓ / ✗
- [ ] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓ / ✗
- [ ] Criterion 3: No frontend-visible change — confirm no React page or UI component was created or modified (check src/pages/ and src/components/) — ✓ / ✗
- [ ] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓ / ✗

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: <today's date — must be non-blank>
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable, no frontend changes, engine signer populated).
```

If any criterion is not met, the autonomous class does not apply — the sign-off block must be completed by the Director of Quality. An EPIC signed off under the autonomous class is still subject to the STEP 4 merge gate; the Director of Quality may review and override at any time before merge.

**Reclassification counter-sign rule (BLG-GOV-14 / LL-v2.3-EX-02):** When a story was originally classified `delegated_frontend` and has been reclassified to `autonomous` per LL-v2.3-EX-02, but the EPIC as a whole introduces frontend-visible changes (UI rendering, interaction behaviour, or page routing), the autonomous class sign-off is insufficient for that EPIC. Director of Quality counter-sign is required at STEP 5 sprint close, in addition to the engine sign-off. Record the counter-sign as a second sign-off block in `qa_evidence_EPIC-xx.md` and confirm in `sprint_close.md`.

**EPIC-level consolidation note (BLG-GOV-14):** When story-level sign-offs within the EPIC involve domain-specific authorities (e.g. Strategy Rules & System Intent Owner, Security Officer, Compliance), the EPIC-level DoQ consolidation block in `qa_evidence_EPIC-xx.md` must explicitly list those story-level authority sign-offs and confirm they are cleared. A domain-authority sign-off at story level does not substitute for the EPIC-level DoQ consolidation block — both are required.

**3.2.B — Open PR**

**Pre-condition (BLG-GOV-18):** Do not open the PR until the DoQ sign-off block in `qa_evidence_EPIC-xx.md` has a non-blank `Date:` field. A blank Date means sign-off is incomplete. The merge gate (STEP 4) also enforces this, but checking here prevents opening a PR that will immediately be blocked — which creates unnecessary review noise. If the Date field is blank: complete the sign-off first, then proceed.

1. Open a pull request: `exec/<cycle_id>/EPIC-xx` → `main`
2. PR title: `[EPIC-xx] <epic description>`
3. PR body: per Section 8.4 — include link to `qa_evidence_EPIC-xx.md`
4. Update `execution_state.json`: EPIC `pr_status` = `open`, `pr_number` = PR number.
5. Do not merge. The merge gate (STEP 4) governs this.

---

## STEP 4 — Merge Gate (Hard Gate, Per EPIC)

A PR may only be merged when **all** of the following are true:

| Condition | Required State |
|-----------|---------------|
| All ST items in EPIC | `done` (not `blocked_*`) |
| Acceptance criteria | verified for all ST items |
| `spec_references` | populated for all `done` ST items |
| `qa_evidence_EPIC-xx.md` | exists; all ST item disposition sections completed by Director of Quality |
| QA sign-off | comment from Director of Quality on PR referencing qa_evidence log |
| Product Owner acceptance | recorded (comment on PR or in `sprint_backlog.md`) |
| `quality_gate.yml` CI | passed (PR title has `[EPIC-xx]`, all checks green) |
| No open escalations | for items in this EPIC |
| No unresolved P0 deviations | all `deviations_filed = true`; no P0 deviations open in referenced specs |

If all conditions pass:
1. Merge the PR (squash or merge as configured).
2. Update `execution_state.json`: EPIC `pr_status` = `merged`, `status` = `merged`.
3. Update `merge_gate.epics_merged`.
4. **Output the following user-facing re-invocation reminder:**

> ✅ EPIC-xx merged. **Re-invoke `run sprint --cycle <cycle_id>` now — required after every EPIC merge, including the final one.** If this is the final EPIC, the engine detects `merge_gate.all_merged = true` and executes STEP 5 (Sprint Close) directly, producing `sprint_close.md` and sealing `execution_state.json`. Do not proceed to `run delivery verification` without doing this first.

> **⚠ HARD GATE (LL-v2.2-EX-02 / BLG-GOV-17 — third recurrence):** When `merge_gate.all_merged = true`, STEP 5 (Sprint Close) **must execute in the same session without exception.** Do not output anything to the user after the merge gate confirmation block without first entering STEP 5. If a session ends after the final merge but before STEP 5, re-invoke `run sprint --cycle <cycle_id>` immediately on resume — the engine detects `all_merged = true` and executes STEP 5 directly. Advisory language was applied twice; this is now a hard gate. **A GitHub Actions workflow (`.github/workflows/sprint_close_reminder.yml`) also posts a mandatory PR comment on every EPIC merge — a third recurrence mandated this automation (BLG-GOV-17).**

If any condition fails: do not merge. Record which condition is unmet. If QA or Product Owner has not responded within their SLA: file an escalation record.

**The engine may not self-approve a merge.** QA sign-off and Product Owner acceptance are always required and must come from the relevant authority.

> **Rationale for re-invocation reminder (lessons learnt — 2026-03-04__release-v1.8 / EX-LL Friction Item 4):** A session ended after recording EPIC-02 QA sign-off but before the PR merge was reported. The user then merged the PR on GitHub without re-invoking `run sprint`. `sprint_close.md` was never created, `execution_state.json` remained unsealed, and `run delivery verification` failed preflight. The reminder makes the re-invocation requirement visible at the moment the user receives merge gate output.

> **Merge order note (LL-v2.0-P3-5):** If more than one EPIC branch modifies a shared governance file (e.g. `execution_state.json`, `.claude_current_state.json`, `backlog.md`, `delegation_log.md`), establish a merge order at the start of STEP 3. Later EPIC branches **must rebase onto `main`** after the first EPIC merges — before running their final QA review and opening a PR. This prevents merge conflicts at the merge gate and avoids the need to rebase mid-merge-sequence.

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

### 5.0 Delegation Log Outcome Check (Required before Sprint_Complete)

Before writing `Sprint_Complete`, verify `claude/cycles/<cycle_id>/delegation_log.md`:
- Every delegation entry (`DEL-YYYYMMDD-nn`) must have `Status` set to `Unblocked`, `Cancelled`, or an equivalent terminal state.
- Entries still showing `Pending` or `In Progress` indicate delegated items with unrecorded outcomes.

For each entry still `Pending` or `In Progress`:
- Check `execution_state.json` for the item's current status.
- If the item is `done` or `merged`: update the delegation log entry status to `Unblocked` (noting the commit SHA).
- If the item is `returned_to_backlog`: update the delegation log entry status to `Cancelled` (noting the backlog return reason).
- If the item is still blocked: record the outcome as `In Progress — carried to post-sprint` with a note.

**Hard gate:** Do not proceed to STEP 5.0A if any delegation log entry has an unrecorded outcome for an item that reached a terminal sprint state. The sprint close record must faithfully account for every delegated item.

### 5.0A — pr_status Pre-Seal Sync (STRUCTURAL — AUD-2026-04-11-003)

Before writing `Sprint_Complete`, sync `pr_status` in `execution_state.json` for every EPIC in `merge_gate.epics_merged`:

```
for each EPIC in merge_gate.epics_merged:
  run: gh pr view <pr_number> --json state
  if state == "MERGED": set execution_state.json EPIC.pr_status = "merged"
  if pr_number is null or 0: set pr_status = "not_created" (do not halt)
```

This step is idempotent — re-running does not alter an already-correct value. Do not proceed to STEP 5.1 until all EPICs in `epics_merged` have `pr_status = "merged"` or `"not_created"`. This prevents misleading `"open"` or `"none"` values in sealed artefacts visible at delivery verification.

### 5.1 Acceptance Summary

For each ST item: confirm `acceptance_verified = true`. If any are false and the item is `merged`: this is a quality gap — file an escalation.

**Deviations filed enforcement check (OA-03 / ST-08):** For each ST item with `status: done`, verify `deviations_filed = true`:
- If `deviations_filed = false` and no deviation record exists in the spec or `qa_evidence_EPIC-xx.md`: set `deviations_filed = true` and append a log note to `execution_state.json` notes field: `"No spec deviation found — deviations_filed corrected at sprint close"`.
- If `deviations_filed = false` and a deviation record **does** exist (deviation was filed but the flag was not set): surface as a process warning and do not auto-correct — requires human review to confirm the deviation record is complete before setting the flag.
- If `deviations_filed = true`: no action needed.

**QA Evidence File Existence Check (LL-v2.4-P4-01 — second recurrence):** Before checking sign-off dates, verify that `qa_evidence_EPIC-xx.md` **exists** for every EPIC in `merge_gate.epics_merged`. A missing QA evidence file is a hard gate — create it immediately using §3.2.A, complete the verification (including pre-met items and autonomous items), obtain DoQ sign-off, then continue. Do not proceed to STEP 5.2 until all qa_evidence files exist. A file created here at sprint close is acceptable; a file missing at Phase 4 (delivery verification) preflight is a recurrent process failure that this gate must prevent.

**QA Evidence Persistence Check (LL-v2.0-P4-1):** For each EPIC with `qa_signed_off: true` in `execution_state.json`, read the corresponding `qa_evidence_EPIC-xx.md` file and confirm the sign-off block `Date:` field is non-blank. If blank: the sign-off was not persisted during sprint execution — re-apply the sign-off block immediately (Director of Quality authority required). Do not proceed to STEP 5.3 until all sign-off blocks are confirmed non-blank.

**STEP 5.1.B — System Status Report Integrity Advisory (BLG-GOV-15):** Before writing Sprint_Complete, open `docs/System_status_report.md` and verify that all SC-* scenario count cells reflect the actual scenario count after this sprint's additions. If scenario count cells were set at sprint planning and not updated post-execution (e.g. new test data library fixtures were added), correct those cells now. Also verify that the execution_prompt.md version reference in the System Status Report matches the actual current version of `claude/system/execution_prompt.md`. Record any corrections made (or confirm no correction was needed) in `sprint_close.md` under a "System Status Report corrections" note. This advisory is non-blocking — corrections are made in-place; the sprint does not halt if cells were stale.

**Unpushed-Commit Check (ST-12 / CF-1):** Before closing the sprint, verify that all commits on the exec branch have been pushed to origin. Run:

```
git log --not origin/<branch> --oneline
```

If any unpushed commits are listed: output their SHAs and subjects. If any unpushed commit includes a `qa_evidence_EPIC-xx.md` file (check via `git show <sha> --name-only`), this is a **soft gate** — you must push those commits before sprint close proceeds. Push the branch (`git push origin <branch>`) and confirm the list is empty before continuing to STEP 5.2.

### 5.2 Items Returned to Backlog

Any ST item that is `blocked_backend`, `blocked_frontend`, or `blocked_decision` at sprint close and will not be completed in this sprint:
- Set status to `returned_to_backlog`.
- Note must be added to `claude/backlog/backlog.md` (one line, referencing this cycle_id and the reason).
- This is the only permitted write to `backlog.md` in this routine.

### 5.3 Sprint Close Record

Create: `claude/cycles/<cycle_id>/sprint_close.md`

Must include:
- Sprint goal
- Items Done (with commit SHAs and spec references)
- Items Returned to Backlog (with reason)
- Items Delegated and outstanding (with delegation record IDs)
- QA evidence logs produced (list: `qa_evidence_EPIC-xx.md` per EPIC)
- Deviations filed this sprint (list: spec file, deviation ref, priority — or "None") — **spec deviations only** (implementation diverges from what the spec requires; filed via `/dev-file`). Process notations, execution observations, and deferred items belong in `execution_state.json` notes column or `execution_escalations.md`, not this register.
- Open escalations (if any)
- Net outcome vs sprint goal
- **Verification readiness statement** (STRUCTURAL — AUD-2026-04-11-004): Write the following block verbatim in `sprint_close.md`. Each field must be `Yes` before writing — resolve any `No` items first. The Delivery Verification Engine reads this block at STEP -1.2; an absent or malformed block causes a preflight failure.

  ```
  ## Verification Readiness Statement
  | Field | Status |
  |-------|--------|
  | All spec references populated in execution_state.json | Yes |
  | All P1–P3 deviations filed and backlog references updated | Yes |
  | QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
  ```

  Do not write `No` in any field. If a field cannot be `Yes`, resolve the gap first, then write the block.

### 5.3A System Status Report Update (required)

Update or create: `docs/System_status_report.md`

This is the living record of what is deployed and verified. The Delivery Verification Engine reads it to confirm what the system can do vs what the verification report will check.

For this sprint, add or update a section:

```
## Sprint: <cycle_id>
**Date:** <sprint close date>
**Status:** Sprint_Complete — pending verification

### Capabilities now live (merged this sprint)
| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-xx | <description> | <spec file#section(s)> | None / <ref> |

### Capabilities deferred or returned
| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-xx | <reason> | backlog.md |

### Verification inputs ready
- QA evidence logs: <list qa_evidence_EPIC-xx.md files>
- Deviations filed: <list or None>
- Test scenarios referenced: <list or None>
```

If `docs/System_status_report.md` does not exist: create it with this sprint's section as the initial content. Use lifecycle header (Owner: Director of Quality, Class: Living Document, Status: Active).

### 5.4 Lessons Learnt

Invoke: `claude/system/lessons_learnt_prompt.md` (§3.3 — Sprint Execution Phase 3 Append)

Output path: `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (Phase 3 section append — create file if absent)

> **Output target (CF-02):** Output target is `lessons_learnt_cycle.md` — do **NOT** append to `lessons_learnt.md` (that is the Release Planning artefact, written by the roadmap and post-ship engines). Create `lessons_learnt_cycle.md` if absent. Writing to the wrong file silently corrupts the Release Planning artefact and prevents Phase 5 from reading the correct lessons.

The shared prompt governs the structured table block format (§4.2), idempotency guard, action rules, and completion conditions. The execution-specific friction areas to focus on:
- Delegation patterns (which classification kept needing humans — could any become autonomous?)
- GitHub integration friction (CI behaviour, issue/PR lifecycle)
- Acceptance criteria gaps (items that lacked criteria and had to be parked as `delegated_decision`)
- Governance process friction (gates that fired unexpectedly, SLA misses)

The prompt's §6.2 rule applies: if any friction can be resolved by updating a template or prompt during this run, apply it immediately and record it.

**Idempotency guard (IMP-35 gap 2 — now active):** Before appending, check for existing section header `## Phase 3 — <cycle_id>` in `lessons_learnt_cycle.md`. If present: skip append (already complete for this cycle).

---

## STEP 6 — Global State Update (Hard Requirement)

> **LL-v2.1-P4-3 guard:** Before setting `status → Sprint_Complete` in `.claude_current_state.json`, confirm that STEP 7 (Seal Execution Record) will execute in the same session. Do not emit `Sprint_Complete` if `execution_state.json.sealed` is still `false`. The delivery verification preflight hard-gates on `sealed: true` — an unsealed execution record will block Phase 4.

After sprint close:

Update `.claude_current_state.json`:
- `status` → `Sprint_Complete`
- `last_sync_utc` → now
- **`blocked_sla_breached`** → `true` if any entry in `execution_escalations.md` has been open for 72 hours or more without resolution (per `shared_standards.md §4` SLA Breach Rule); otherwise omit or set `false`.

If all roadmap items for this release are complete:
- Flag `release_complete: true` in `.claude_current_state.json`.
- Surface to Product Owner: the release is ready for Phase 1 (Roadmap Rebalance) or direct Phase 1B (next release planning).

---

## STEP 7 — Seal Execution Record (Hard Gate)

Once sprint close and global state update are complete:

**Pre-seal check — delegation_log.md integrity (LL-v2.3-CL-02):**
Before sealing, verify `delegation_log.md` line count is consistent with delegation activity:
1. Count `delegated_items` entries in `execution_state.json`.
2. If `delegated_items` is non-empty: confirm `delegation_log.md` has substantially more than 5 lines (a header-only or near-empty file after a sprint with delegation records indicates a staging error — as occurred in v2.3 sprint close commit `a12233f`).
3. If line count is suspiciously low (fewer than 10 lines with non-empty `delegated_items`): halt, surface the discrepancy, and re-read `delegation_log.md` before proceeding. Do not seal an incomplete delegation log.

1. Set `execution_state.json.sealed = true`, `sealed_utc = now`.
2. Set `execution_state.json.status = Sealed`.
3. No further modifications to `execution_state.json` are permitted.
4. No further modifications to `delegation_log.md` or `execution_escalations.md` are permitted.

**Terminal state rule:** Once sealed, the execution record is immutable. Any correction or amendment requires a new execution cycle referencing this `cycle_id`.

---

## STEP 8 — Commit & Push Cycle Artefacts

**Governance file edit check (ST-12 / CF-2):** Before committing, check whether any §6-governed file (listed in `claude/system/OPERATIONAL_GUIDE.md` §14) was modified during this sprint execution run — including changes applied as part of ST items (e.g. deferred prompt patches). If any were modified: append one entry per file to `claude/system/prompt_change_log.md` in the same session as the edit, using the format `| date | filename | vOLD→vNEW | summary | authority |`. This step must complete before the STEP 8 commit is pushed.

Stage and commit all cycle artefacts created or modified by this routine:

```
git add claude/cycles/<cycle_id>/execution_state.json
git add claude/cycles/<cycle_id>/delegation_log.md
git add claude/cycles/<cycle_id>/execution_escalations.md  (if created)
git add claude/cycles/<cycle_id>/qa_evidence_EPIC-*.md
git add claude/cycles/<cycle_id>/sprint_close.md
git add claude/cycles/<cycle_id>/lessons_learnt_cycle.md
git add docs/System_status_report.md
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
- All `done` ST items have `spec_references` populated — exemption: items where `notes` contains "no prior spec applicable" (LL-v2.2-EX-04) are exempt and must **not** be flagged as traceability gaps
- All `done` ST items have `deviations_filed = true`
- One `qa_evidence_EPIC-xx.md` exists per merged EPIC, with consolidation block complete
- `docs/System_status_report.md` updated with this sprint's section
- `sprint_close.md` exists, is lifecycle-compliant, and includes verification readiness statement
- `lessons_learnt_cycle.md` Phase 3 section appended (idempotency guard applied)
- `.claude_current_state.json` updated to `Sprint_Complete`
- No open escalations with `Blocks execution: Yes`
- STEP 8 commit complete (or commit manifest produced)

---

## 13. Governance Invariants

System-wide invariants: per `claude/system/invariants.md`. Execution-engine-specific invariants below.

**Ambiguity definition:** An item is *ambiguous* when its acceptance criteria, EPIC assignment, spec reference, or delegation classification cannot be determined without an authority decision. Ambiguous items must be classified `delegated_decision` and escalated — never silently assumed or guessed. This applies in both `strict` and `standard` modes. The only difference between modes is whether execution continues on other items (standard) or halts entirely (strict).

- **No autonomous merge.** The engine never merges without QA sign-off and Product Owner acceptance.
- **Gate evidence requirement.** Any hard gate status change in `current_roadmap.md` (marking a gate as "complete") must reference the evidence artefact that cleared it (PoG Gate ID, decision record path, or verifiable session output reference). A gate may not be marked complete without an evidence reference. If no artefact exists: gate remains "pending". Record in escalations.md.
- **No scope change.** The backlog slice is sealed. The engine executes what is there.
- **No strategy boundary decisions.** The Strategy Rules owner decides; the engine surfaces and parks.
- **Delegation is explicit and tracked.** No silent assumptions about human completion.
- **Commit format is non-negotiable.** `[EPIC-xx][ST-xx]` prefix on every commit to `exec/**`. `governance_sync.yml` depends on it.
- **PR title is non-negotiable.** `[EPIC-xx]` in title. `quality_gate.yml` blocks merge without it.
- **Every block is recorded.** Nothing is silently skipped. Blocked items are documented in `execution_state.json` and surfaced to the user.
- **Amendment slice supersedes original.** If `amended_backlog_slice_path` is set, it is used exclusively. Executing from the original slice when an amendment has sealed is a process integrity failure.
- **Delivery pressure does not override quality gates.** Director of Quality sign-off is required on every EPIC before merge, regardless of timeline.
- **Backend commits for delegated_frontend items must land on the EPIC branch.** Backend commits tightly coupled to a `delegated_frontend` story (e.g. new DB migration + endpoint required by the frontend) must be committed to that story's EPIC branch, not directly to `main`, unless the PMO Lead explicitly authorises a direct-to-main path in writing. Violation is a process deviation and must be documented in the QA evidence log for the affected EPIC (and any other EPIC whose merge window was impacted). Reference: DEV-EPIC02-ST05-02 (LL-v2.2-EX-03).

---

## 14. Playwright Test Authoring Standard (OA-05 / ST-10)

When writing or updating Playwright tests in this project:

**Use `waitFor` patterns — not `networkidle`.**

`page.waitForLoadState('networkidle')` is unreliable on CI and is prohibited in new tests. Replace with:

- **`await expect(page.locator('selector')).toBeVisible({ timeout: N })`** — preferred; waits for a specific element that confirms the page/component has rendered.
- **`await page.waitForSelector('selector')`** — acceptable when `expect` is not available at the point of navigation.
- **`await page.waitForResponse(urlPattern)`** — when the test needs to confirm a specific API call was made.
- **`await page.waitForLoadState('domcontentloaded')`** — only in navigation helper functions where a specific element is unknown. Never in the body of a test scenario.

**Standard:**
1. Every `page.goto()` or `page.reload()` must be followed by an element-specific wait, not `networkidle`.
2. In test helper functions (e.g. `async function goto(page, hash)`), use `domcontentloaded` as the base wait only when no specific element is available.
3. `waitForLoadState('networkidle')` is never permitted in new test code. The QA Evidence sign-off block for any EPIC introducing new Playwright tests must confirm this standard was followed.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 3.15 | 2026-05-09 | Post-ship closure v3.2 — two action-now patches applied. (LL-v3.2-P3-02) §3.1.A step 13 added — Cross-spec selector check: when a story modifies, replaces, removes, or renames a DOM element, scan all existing Playwright specs for selectors targeting that element and update stale selectors in the same commit. Prevents CI failures caused by UI changes in unrelated test files. (LL-v3.2-P4-01) §3.2.A BLG-GOV-19 autonomous class sign-off block — explicit criterion checklist added (✓ / ✗ for each of the 4 criteria); Criterion 3 includes explicit instruction to check src/pages/ and src/components/ before claiming no frontend-visible change. Makes criterion 3 a positive assertion, preventing autonomous class misapplication. Authority: Head of Specs Team (post-ship closure v3.2, 2026-05-09). |
| 3.14 | 2026-05-06 | ST-08 + ST-09 + ST-10 (EPIC-03, v3.2): Three OA patches combined. (ST-08 / OA-03) §5.1 — Deviations filed enforcement check added: for each done story, if `deviations_filed=false` and no deviation record exists, auto-correct with log note; if deviation record exists but flag false, surface process warning without auto-correct. (ST-09 / OA-04) §3.1.A step 12 — Post-story test files check added: explicit named step requiring `test_scenarios` in `execution_state.json` to be populated immediately after any story that creates test files, before advancing to next story. (ST-10 / OA-05) §14 — Playwright Test Authoring Standard added: `networkidle` prohibited in new tests; `waitFor` element-specific patterns required; `domcontentloaded` permitted in navigation helpers only; all existing `networkidle` occurrences in `tests/e2e/` replaced. Authority: Head of Specs Team (ST-08 + ST-09 + ST-10, 2026-05-06). |
| 3.13 | 2026-05-01 | §3.2.A Frontend testing gate (LL-v3.1-EX-01): hard gate added — any EPIC with frontend-visible changes must have Playwright test coverage for each observable AC, or human staging sign-off with date, before PR opens. "Code review only" without a filed backlog item blocks the PR. CLAUDE.md §2 corresponding rule updated. Also records test file paths SC-UK-01–04 (screener-uk-suffix.spec.js) and SC-EARN-01–09 (earnings-calendar.spec.js) created for ST-06 and ST-08 gaps. Authority: Head of Specs Team (2026-05-01). |
| 3.12 | 2026-04-30 | ST-13 + ST-14 (EPIC-04, v3.1): Two carry-forward patches combined. (ST-13 / CF-01) §3.1.A — Reclassification backfill instruction added: when a story is reclassified from `delegated_frontend` to `autonomous` mid-sprint, the engine must backfill `test_scenarios` in `execution_state.json` at the time of reclassification; `test_scenarios` must be populated before the story's QA evidence log entry is written. (ST-14 / CF-02) §5.4 — Output target note added: output target is `lessons_learnt_cycle.md`; explicit warning NOT to append to `lessons_learnt.md` (Release Planning artefact); prevents silent corruption of the RP artefact. Authority: Head of Specs Team (ST-13 + ST-14, 2026-04-30). |
| 3.11 | 2026-04-25 | ST-12 + ST-13 (EPIC-04, v3.0): Two deferred patches combined. (ST-12 / OA-v29-02) §2 execution_state.json ownership rule added for multi-EPIC sprints — first EPIC branch in execution order is designated owner; all others check for file existence before creating; merge conflict advisory references CLAUDE.md §8. (ST-13 / OA-v29-03) §3.1.A step 1 — test scenarios advisory added: when tests are created, populate test_scenarios in execution_state.json with test file paths; non-blocking; must be complete before STEP 3.2.A QA evidence log creation. Authority: Head of Specs Team (ST-12 + ST-13, 2026-04-25). |
| 3.8 | 2026-04-18 | ST-05 (EPIC-03, v2.8): §5.3 sprint close template — "Deviations filed" clarified: spec deviations only (implementation diverges from spec; filed via /dev-file). Process notations, execution observations, and deferred items belong in execution_state.json notes or execution_escalations.md, not the deviation register. Closes v2.7 carry-forward CF-2 (deviation register terminology confusion). Authority: Head of Specs Team (ST-05, 2026-04-18). |
| 3.7 | 2026-04-18 | ST-04 (EPIC-03, v2.8): §3.2.A Date field requirement note updated — explicitly states Date must be non-blank before PR can be opened (§3.2.B pre-condition, BLG-GOV-18) in addition to before the merge gate runs. Closes the loop between §3.2.A sign-off block authoring and §3.2.B PR-opening enforcement. Authority: Head of Specs Team (ST-04, 2026-04-18). |
| 3.4 | 2026-04-13 | BLG-GOV-17 (third recurrence — sprint close skipped): Two-pronged fix. (1) STEP 3.2.D post-merge reminder — removed conditional qualifier "if there are remaining EPICs pending"; reminder is now unconditional and explicitly calls out that re-invocation is required after the final merge, with the engine detecting `all_merged = true` and executing STEP 5 directly. (2) Created `.github/workflows/sprint_close_reminder.yml` — GitHub Actions workflow that posts a mandatory PR comment on every EPIC merge to main, firing regardless of Claude Code session state. HARD GATE blockquote updated to reference BLG-GOV-17 and the new workflow. Authority: Head of Specs Team (OA-1, BLG-GOV-17, 2026-04-13). |
| 3.3 | 2026-04-11 | AUD-2026-04-11-003 + AUD-2026-04-11-004: Two STALE/OVERDUE deferred patches applied. (AUD-003 — OVERDUE 3 cycles) STEP 5.0A added — pr_status pre-seal sync: before writing Sprint_Complete, call `gh pr view <n> --json state` for each EPIC in merge_gate.epics_merged; set pr_status="merged" if MERGED; set pr_status="not_created" if no PR number. Prevents misleading "open"/"none" values in sealed artefacts. (AUD-004 — STALE 2 cycles) STEP 5.3 Verification Readiness Statement upgraded from informal description to STRUCTURAL template — exact markdown table block provided; each field must resolve to Yes before writing; no-No rule enforced. Delivery Verification STEP -1.2 handoff gap closed. Authority: Head of Specs Team (AUD-2026-04-11, 2026-04-11). |
| 3.1 | 2026-04-06 | ST-12 (CF-2a, EPIC-04 v2.5): STEP 8 governance file edit check added — if any §6-governed file (listed in OPERATIONAL_GUIDE.md §14) was modified during sprint execution run, append one entry per file to prompt_change_log.md in same session before STEP 8 commit. Authority: Head of Specs Team (ST-12, 2026-04-06). [Backfill entry — not present at time of apply.] |
| 3.0 | 2026-04-03 | Post-ship closure v2.4 lessons learnt — three action-now patches applied. LL-v2.4-EX-01 (third recurrence): §3.1.D delegated_decision unblock detection — hard gate added to update delegation log entry to Unblocked atomically with item status=done; applies equally to delegated_decision items as to delegated_backend/frontend. LL-v2.4-P4-01 (second recurrence): STEP 5.1 — QA Evidence File Existence Check added; before sign-off date check, verify qa_evidence_EPIC-xx.md exists for every EPIC in merge_gate.epics_merged; missing file is a hard gate at sprint close. LL-v2.4-P4-02: §3.1.A pre-met path note added — pre-met items require qa_evidence_EPIC-xx.md entry with DoQ sign-off confirming verification; pre-met does not mean unverified. Authority: Head of Specs Team (post-ship closure 2026-03-31__release-v2.4). |
| 2.9 | 2026-03-31 | Post-ship closure v2.3 lessons learnt applied (deferred patches). LL-v2.3-CL-01: §5.1 delegated_frontend classification updated — Base44 model superseded; frontend stories default to autonomous engine delivery; classification rule and delegation note updated. LL-v2.2-EX-01 (second recurrence): STEP 3.1.A unblock detection upgraded from advisory to hard gate — delegation log entry must be updated atomically with item status to `done`; batching to STEP 5.0 is a process violation. LL-v2.2-EX-02 (second recurrence): STEP 4 all_merged advisory upgraded to hard gate — STEP 5 sprint close must execute in same session as final merge without exception. LL-v2.2-EX-04 (second recurrence): §9.1 spec_references comment made explicit — "no prior spec applicable" is the exemption token; completion condition updated to name the token explicitly; engine must not flag spec_references:[] as a traceability gap when token is present. LL-v2.3-CL-02: STEP 7 pre-seal check added — delegation_log.md line count verified against delegated_items count before sealing. Authority: Head of Specs Team (post-ship closure 2026-03-24__release-v2.3). |
| 2.7 | 2026-03-24 | Post-ship closure v2.2 lessons learnt applied. LL-v2.2-EX-01: STEP 3.1.B unblock detection — delegation log entry updated to `Unblocked` in-flight (not batched at STEP 5.0). LL-v2.2-EX-02: STEP 4 merge gate — advisory added: when `all_merged=true`, STEP 5 Sprint Close must execute in same session. LL-v2.2-EX-03: §13 invariants — backend branch discipline note added (delegated_frontend backend commits must land on EPIC branch). LL-v2.2-EX-04: §9.1 schema — spec_references may be empty for delegated_qa doc artefacts and autonomous infra items with no prior spec; notes field: "no prior spec applicable". LL-v2.2-EX-05: STEP 3.1.C — test gap against undelivered feature should be noted "pending ST-xx completion", not flagged P1. Authority: Head of Specs Team (post-ship closure 2026-03-21__release-v2.2). |
| 2.6 | 2026-03-21 | LL-v2.1-P4-3: STEP 6 guard note added — do not emit `Sprint_Complete` in `.claude_current_state.json` if `execution_state.json.sealed` is still `false`. Ensures STEP 7 (Seal Execution Record) executes in the same session as sprint close before the delivery verification preflight can proceed. Authority: Head of Specs Team (post-ship closure immediate action). |
| 2.5 | 2026-03-20 | §5.3 Agent-Mediated Sign-Off added — when a seal condition names a role with an agent file in `claude/agents/`, invoke a subagent acting in that role to perform the review before surfacing to the user. Always-human gates (Product Owner, merge gate) unchanged. §3.1.A step 11 added — sign-off gate check after deviation check. §9.1 schema — `sign_off_record` field added to ST item. Authority: Head of Specs Team. |
| 2.4 | 2026-03-17 | Post-ship closure v2.0 lessons learnt patches applied. LL-v2.0-P3-4: qa_evidence sign-off block template — DoQ URL construction check added (for direct URL construction not via api.* wrapper, confirm base URL variable is exposed on imported object). LL-v2.0-P3-5: STEP 4 merge gate — merge order note added for multi-EPIC sprints where >1 EPIC modifies shared governance files; later branches must rebase onto main after first EPIC merges before final QA. LL-v2.0-P4-1: STEP 5.1 — QA Evidence Persistence Check added; after qa_signed_off: true, confirm qa_evidence Date: field is non-blank; if blank, re-apply sign-off before STEP 5.3. |
| 2.3 | 2026-03-16 | AUD-2026-03-13-017: §11 delegation log schema replaced with reference to `shared_standards.md §16.3`; SLA breach tracking note in STEP 3.1.D replaced with reference to `shared_standards.md §16.4`; §13 cross-reference to `claude/system/invariants.md` added. |
| 2.2 | 2026-03-16 | LL-v1.10-P3-3: §5.1 autonomous candidate pattern note added (refactor with no UX change + existing API method → autonomous). LL-v1.10-P4-2: §3.1.A step 10 deviation type distinction added (absent from spec → qa_evidence + backlog; differs from spec → canonical spec). LL-v1.10-P4-1: qa_evidence sign-off block template authoring note added. |
| 2.1 | 2026-03-14 | AUD-2026-03-13-001 (PATCH 5): Gate evidence requirement added to §9 invariants — hard gate status changes in current_roadmap.md must reference an evidence artefact; gate remains pending without one. |
| 2.0 | 2026-03-10 | IMP-53: §7 Write Scope — `lessons_learnt_execution.md` replaced with `lessons_learnt_cycle.md` (append-only, Phase 3 section; create if absent). STEP 5.4 — invocation updated from `§3.3` to `§3.3 — Sprint Execution Phase 3 Append`; output path changed to `lessons_learnt_cycle.md`; IMP-35 gap 2 idempotency guard activated (was marked inactive until IMP-28 — now active). STEP 8 commit list: `lessons_learnt_execution.md` → `lessons_learnt_cycle.md`. §12 completion condition: `lessons_learnt_execution.md exists` → `lessons_learnt_cycle.md Phase 3 section appended`. |
| 1.9 | 2026-03-10 | IMP-25: STEP -1.1 — load `sprint_backlog_index.json` if present; when `--epic` scoped, use index `st_items` and `backlog_slice_refs` to read only the relevant EPIC slice rather than full document. STEP 0 — index-guided load note added; when index provides exact `backlog_slice_refs`, read only those AC sections from `stage4_backlog_slice.md`. Fall-back to full document read when index absent. |
| 1.8 | 2026-03-10 | IMP-40: §3.1.D SLA breach tracking note added — 72-hour breach check on each re-invocation; `blocked_sla_breached = true` written at STEP 6 if any escalation exceeds SLA; references `shared_standards.md §4` SLA Breach Rule. STEP 6 state write schema: `blocked_sla_breached` field added. IMP-35 (gap 2): STEP 5.4 — future IMP-28 idempotency guard documented (inactive until IMP-28 implemented); pre-write check for `## Phase 3 — <cycle_id>` header in `lessons_learnt_cycle.md` before appending. |
| 1.7 | 2026-03-10 | IMP-47/56: STEP -1.7 — temp file renamed to `.write_test`; STEP 0 — cleanup obligation added. IMP-44: §9.1 schema — `last_completed_substep` field added to ST item; §10.2 Sub-Item Resume rule added. IMP-20: STEP 5.0 added — delegation log outcome check (all delegation entries must have terminal status) required before Sprint_Complete is written. IMP-33: §13 Governance Invariants — "Ambiguity" definition block added. |
| 1.5 | 2026-03-07 | **Pre-condition status check corrected (STEP -1.2).** Was checking for Release Planning states (`Committed`, `Validated`, `Published`) — corrected to `Sprint_Planning_Complete` (fresh run) or `Executing` (resume); `sprint_sealed = true` added as required condition. **Sprint backlog sealed check added (STEP -1.3).** Verifies `sprint_backlog.md` status = `Sealed` and no `[AWAITING SIGN-OFF]` fields remain — was absent in prior version. **`amended_backlog_slice_path` handling added.** §4 backlog slice source-of-truth rule added. STEP -1.1 extended: checks `amended_backlog_slice_path`; if present, uses that file as the authoritative scope; records the authoritative path for use throughout the run. STEP 0 updated: parses the authoritative slice (not hardcoded `stage4_backlog_slice.md`); records `backlog_slice_source` in `execution_state.json`. §7 write scope: amended backlog slice added to must-not-modify list. §9.1 schema: `backlog_slice_source` field added. §13 invariant added. **`Executing` status documented.** STEP 0 note: `Executing` is a valid intermediate status between `Sprint_Planning_Complete` and `Sprint_Complete`; Phase 4 may not be invoked while `Executing`. Guide updated separately (§4 lifecycle table, §12 cycle trigger table, §13 artefact register). **STEP numbering adjusted:** -1.1 now includes backlog slice source check; -1.2 status check; -1.3 sprint backlog sealed (new); former -1.3/-1.4/-1.5/-1.6 renumbered to -1.4/-1.5/-1.6/-1.7. |
| 1.4 | 2026-03-06 | Prior version. |