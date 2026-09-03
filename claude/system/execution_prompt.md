**Owner:** Head of Specs Team
**Status:** Active
**Version:** 3.71
**Last Updated:** 2026-09-03 (post-ship closure 2026-08-21__release-v9.0 outstanding actions, Head of Specs Team direct action — STEP 3.1.A step 10a gains a same-step self-verification read-back after the deviations_filed write (LL-v9.0-P3-01) and a resolving-commit deviation-closure discipline requirement (LL-v9.0-P4-01, BLG-GOV-315); STEP 3.1.A step 12's roll-up backstop gains a qa_evidence cross-check extension (LL-v9.0-P4-02)); prior — 2026-08-21 (lifecycle audit AUD-2026-08-21, action-all-audit-points session — STEP 5.1 item-count reconciliation check; STEP 5.3 escalation cross-reference check; §3.2.B multi-sprint EPIC 2nd-PR convention; STEP 0 test_scenarios array-only prohibition; STEP 4 merge_gate mid-session re-sync); prior history retained — see prior entries in version control.
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

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

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
- **Infra/ops verification pattern (LL-v8.0-P3-01):** Infrastructure/operations verification or configuration task requiring live external dashboard/production access the engine cannot perform (e.g. Render/Supabase dashboard reads, GitHub repo secret configuration) → `delegated_backend`, regardless of whether any code is written. This sub-pattern was missing at `2026-07-30__release-v8.0`, causing 6 of 19 stories (32% of scope) to be initially recorded as stale `autonomous` at STEP 0, requiring mid-execution correction.

**§13 gate story pattern (LL-v3.5-SP-01):** When an arc feature requires a strategy or compliance review gate (referenced as a "§13 review" in the OPERATIONAL_GUIDE), scope the review as a Sprint 1 story with `classification: delegated_decision`, gating all implementation stories (backend, frontend) to Sprint 2. The Sprint 1 gate story must reach `status: done` before Sprint 2 implementation stories begin execution. If the gate story is not resolved by end of Sprint 1: surface as an escalation and defer implementation stories to the next cycle. This pattern was validated in v3.5 ST-01 (IT-06 Arc 3 integration — §13 gate cleared before Arc 3 backend implementation).

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
5. If `Approved`: record sign-off in `execution_state.json` `sign_off_record` for the item; proceed. **BLG-GOV-73 — Deviations_filed auto-set on clearance:** When setting `sign_off_record.status = "cleared"` for a delegated story (any delegation class), if no DEV-* deviation record was filed for that story, also set `deviations_filed = true` in the same operation. Condition: delegated story + sign-off cleared + no DEV-* record filed → `deviations_filed = true`. This prevents the batch-correction pattern at sprint close for cleared delegated stories.
6. If `Blocked`: apply the findings in-session, re-invoke the sign-off agent. Maximum 2 retries.
7. If still `Blocked` after 2 retries, or if no agent file exists: surface to the user as a `delegated_decision` block with the outstanding findings listed explicitly.

**Quantitative/"already verified" claim second-pass requirement (LL-v8.6-P3-01):** When an agent-mediated sign-off's own comments assert an independent quantitative re-verification (e.g. "re-verified the bound and found it conservative," "independently confirmed the count," "re-checked and it is correct") rather than a plain pass/fail against a documented criterion, that assertion must itself be evidenced in the sign-off comments — cite the actual calculation, count, or check performed, not just the conclusion. If it cannot be evidenced inline, do not rely on the first-pass sign-off alone: a second, differently-scoped review pass must confirm the specific quantitative claim before the item is marked cleared. Confirmed live at `2026-08-11__release-v8.6`: 3 separate stories (ST-03/EPIC-02, ST-11+ST-12/EPIC-04, ST-24/EPIC-06) each had a first-pass "already verified"-class claim that was factually wrong, caught only by a second, independently-requested review pass — the ST-12 case shipped a real, unbounded cost-basis-drift bug into the PR because the first pass's "independently re-verified, conservative" claim was itself unsubstantiated.

**Infrastructure co-sign class (LL-v5.6-DV-03):** For backend-only EPICs, a valid DoQ sign-off may take the co-sign form: `"Infrastructure & Operations Owner + Director of Quality: Confirmed — [N] stories, YYYY-MM-DD"`. This dual-domain co-sign is accepted by delivery_verification_prompt.md §-1.3 Tier 2 as equivalent to agent-mediated sign-off with named domain role. When using this format, record `"method": "infrastructure_co_sign"` in `sign_off_record` in `execution_state.json` for the EPIC.

**Always-human gates (never agent-mediated):**
- Product Owner — sprint scope, goal, and acceptance of sprint close are always human decisions.
- Merge gate — QA sign-off and Product Owner acceptance on PRs are always human.

**Agent-mediated sign-off is appropriate for:**
- Spec sign-offs: Head of Specs Team, API Contracts & Documentation Owner, Data Model & Domain Schema Owner
- Architecture sign-offs where the ADR is already written and the review is against documented criteria
- Any named authority with an agent file where the decision is reviewable against criteria in the role charter

**Agent-mediated PR review comment labeling convention (OA-6 ruling, post-ship closure 2026-07-24__release-v7.8 — carried unruled from v7.7):** An agent may draft and post PR review comments evaluating a PR against a named role's quality bar — including Product Owner or Director of Quality — since this is permitted, not disallowed: it surfaces the same findings a human reviewer would otherwise have to derive from scratch, and does not by itself satisfy either always-human gate above. The following are mandatory whenever this is done:
- The comment must **never** be labeled as if authored by the human role itself (e.g. never `Product Owner: Approved` or `Director of Quality: Confirmed` verbatim) — that phrasing is indistinguishable from an actual human sign-off to a future reader, CI script, or another agent.
- The comment must be explicitly labeled as agent-mediated and reviewing *on behalf of* the named role, e.g. `**[Agent-mediated review — on behalf of Product Owner, pending human confirmation]**`.
- Any sign-off field the comment references (in `qa_evidence_EPIC-xx.md`, `sign_off_record`, or the PR merge-gate checklist) must remain blank until the actual human authority completes it. An agent-mediated PR review comment never itself satisfies the "QA sign-off" or "Product Owner acceptance" merge-gate conditions (Section 13 / CLAUDE.md §2) — those remain always-human regardless of any agent-drafted commentary.

This codifies, as a standing rule, the ad hoc labeling convention already used successfully in the v7.8 cycle (agent-mediated, blank sign-off fields left for human completion) rather than leaving it a per-cycle judgment call carried unruled between cycles.

**Sign-off record schema** (added to `execution_state.json` per-story) — see `shared_standards.md` §16.13 (canonical definition, moved out of this file at AUD-2026-07-20-004; not duplicated here).

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

→ Apply `claude/system/shared/governance_preamble.md §Agent-Integrity`. Required roles:
- Product Owner
- Head of Specs Team
- PMO Lead
- Director of Quality
- Infrastructure & Operations Owner
- Strategy Rules & System Intent Owner
- FinOps & Resource Architect
- Facilitator

Phase-specific note: `head_of_specs_team.md` uses `**Role:** Head of Specs Team` in its header block rather than a dedicated role line — treat as compliant (string is present in the file).

---

## 7. Write Scope Restriction (Hard Gate)

→ Apply `claude/system/shared/governance_preamble.md §Write-Scope`. Phase-specific permitted paths:
- `claude/cycles/<cycle_id>/execution_state.json` (create/update)
- `claude/cycles/<cycle_id>/delegation_log.md` (append-only)
- `claude/cycles/<cycle_id>/execution_escalations.md` (append-only)
- `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (one per EPIC, created at EPIC completion)
- `claude/cycles/<cycle_id>/sprint_close.md` (create at close only)
- `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (append-only — Phase 3 section; create if absent)
- Source files required by ST items (within repo, outside governance folders)
- Canonical spec files (deviation documentation only — §9 Known Deviation Standard; no other spec edits permitted)
- `.claude_current_state.json` (status updates only)
- `claude/backlog/backlog.md` — **new-item addition only**, and only for a genuinely out-of-scope finding surfaced mid-sprint (a defect, gap, or follow-up discovered while working an ST item that is not itself in the current sprint's scope). Permitted: appending a new `### BLG-xx` item under its correct §1–§8 type section, per the Placement Rule at the top of `backlog.md`. Not permitted: editing any existing item's content, priority, status, or `Provisional-Target`; touching the Release Slice / capacity tables; anything that amounts to a scope or re-prioritisation decision. Every item added this way must carry a `**Source:**` line naming the discovering ST/EPIC and today's date, so post-ship closure and `groom backlog` can trace it back to this cycle. This exception formalises a practice already in continuous use across `v8.1`–`v8.3` (see `prompt_change_log.md` this entry) — it does not expand what may be *decided*, only where a *finding* may be recorded.

Must not modify: `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed), `claude/cycles/<cycle_id>/amendments/*/amended_backlog_slice.md` (sealed), `claude/cycles/<cycle_id>/sprint_backlog.md` (sealed), `claude/roadmap/*`, `claude/backlog/backlog.md` (beyond the narrow new-item-addition exception above), `claude/strategy/strategy_rules.md`, any governance document outside this routine's scope.

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

Schema: `claude/system/schemas/execution_state_schema.json` — read this file when creating `execution_state.json`. `backlog_slice_source` records the exact authoritative backlog slice path used; set at STEP 0 (used by Delivery Verification to confirm scope provenance). `spec_references` exemption: when `spec_reference_not_applicable: true` (with `spec_reference_not_applicable_reason` populated — see STEP 3.1.A Case E), `spec_references: []` must NOT be flagged as a traceability gap by completion condition checks or delivery verification. Legacy records written before this field existed may instead carry `notes` containing exactly `"no prior spec applicable"` — Delivery Verification honours both forms.

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
0. **(LL-v7.2-P3-01)** Run `git fetch origin` and compare local `main` to `origin/main` before trusting any local state file — see STEP -1's Session-start divergence check. Do not wait for STEP 4's merge-gate resume-sync (LL-v3.9-P3-1) to catch a session that starts behind origin.
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

**Structural append-verification (BLG-GOV-168):** Apply the Structural Append-Verification Procedure per `shared_standards.md §7.1` at every append (count before/after, confirm exactly +1, confirm no prior entry text changed — halt on either failure).

---

## Mandatory End-to-End Process

## STEP -1 — Preflight Gate (Hard Gate)

**Session-start divergence check (required, generalises LL-v3.9-P3-1 — LL-v7.2-P3-01):** Before reading or trusting any local state file, run `git fetch origin` then compare local `main` to `origin/main` (e.g. `git rev-list --left-right --count main...origin/main`). If local `main` is behind `origin/main`, run `git checkout main && git pull` (only if currently on `main` with no uncommitted changes) before proceeding. A session that starts significantly behind origin risks re-deriving `execution_state.json` state and GitHub issues that already exist upstream (duplicate STEP 0 re-initialisation, duplicate issue creation) — this check must run before the "First action" read below, not only at STEP 4's merge-gate resume-sync, which fires too late to prevent the duplication.

**First action:** Read `claude/cycles/<cycle_id>/execution_state.json` if it exists.
If it exists and `status` is not `not_started`: you are resuming — see Resumability Protocol in `claude/system/shared_standards.md` §8.
If it does not exist: this is a fresh run. Continue below.

Shared standards (escalation format, halt report format, gh CLI commands, identifier conventions): `claude/system/shared_standards.md`

Purpose: fail fast before any execution begins.

### -1.1 Common Preflight — Required Files Present
Apply `claude/system/shared/preflight_common.md` (sub-check 1 only) with:
- required_files:
  - .claude_current_state.json (and `active_cycle` populated)
  - claude/charter/team_charter.md
  - claude/charter/document_lifecycle_guide.md
  - claude/strategy/strategy_rules.md
  - claude/cycles/\<cycle_id\>/sprint_backlog.md
  - claude/cycles/\<cycle_id\>/sprint_goal.md

Check `amended_backlog_slice_path` in `.claude_current_state.json`:
- If present and non-empty: this is the authoritative backlog slice. Verify the file exists — if not, halt and report. Record this path for use throughout this run.
- If absent or empty: verify `claude/cycles/<cycle_id>/stage4_backlog_slice.md` exists — if not, halt and report. Record this path for use throughout this run.

**Sprint backlog index (IMP-25):** Load `claude/cycles/<cycle_id>/sprint_backlog_index.json` if it exists. When `--epic` is specified, use the index to identify which ST items belong to the scoped EPIC and their `backlog_slice_refs` — read only those items from `sprint_backlog.md` rather than the full document. If the index does not exist: fall back to reading the full `sprint_backlog.md`.

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

### -1.6/-1.7 Common Preflight — Roles and Write Test
Apply `claude/system/shared/preflight_common.md` (sub-checks 2 and 3) with:
- required_roles: per Section 6 (Agent Integrity)
- write_test_path: claude/cycles/\<cycle_id\>/.write_test

---

## STEP 0 — Initialise Execution State (Hard Requirement; first write)

**Cleanup:** If `claude/cycles/<cycle_id>/.write_test` exists (left from STEP -1.7 on a previous interrupted run), delete it now before proceeding.

**Sealed-file integrity check (OA-01/CF-01 — Hard Gate):** At each EPIC session start, run:

```
git diff --name-only HEAD
git diff --name-only --cached
```

Check the output against sealed files for this cycle:
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md`
- `claude/cycles/<cycle_id>/release_plan.md`
- `claude/cycles/<cycle_id>/state.json`
- Any amended backlog slice at `amended_backlog_slice_path` if present

If any sealed file appears in the diff output (staged or unstaged):

```
[HALT] Sealed file modified: {filename}. Do not modify sealed artefacts. Revert changes before proceeding.
```

This is a hard gate — no bypass. Revert the change and re-run STEP 0.

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
6. For each EPIC: check `tests/` and `tests/e2e/` for existing runnable test script files that exercise acceptance criteria for this EPIC's stories. Record found paths in `execution_state.json` EPIC `test_scenarios` field. If none: set `test_scenarios: []` — **always a bare empty array, never a descriptive string** (AUD-2026-08-21-009). Any manual-review rationale (e.g. "no application test suite affected — governance-only change") belongs in the `qa_evidence_EPIC-xx.md` "Test scenarios used" prose field instead, never smuggled into this JSON array. **Advisory (BLG-GOV-136):** `docs/testing/` paths are QA evidence artefacts (scenario description documents), not runnable test files — do not record `docs/testing/` paths in `test_scenarios`.

```yaml
# execution_state.json initial schema (∀ ST item at STEP 0):
epics.<EPIC-xx>.stories.<ST-xx>:
  status: not_started
  classification: autonomous|delegated_backend|delegated_frontend|delegated_qa|delegated_decision
  spec_references: []          # populate per rule above; [] only if purely infrastructural
  spec_reference_not_applicable: false          # set true only per STEP 3.1.A Case E (no governing spec, no new artefact)
  spec_reference_not_applicable_reason: null    # required one-line reason when spec_reference_not_applicable is true
  github_issue: null           # filled at STEP 1
  branch: null                 # filled at STEP 2
  deviations_filed: false
  acceptance_verified: false
  commit_sha: null
epics.<EPIC-xx>.test_scenarios: []   # populate with runnable test file paths from tests/ or tests/e2e/ only
execution_state.status: Running
backlog_slice_source: <authoritative slice path>

# global state update:
.claude_current_state.json.status: Executing
```

`Executing` is a valid intermediate status between `Sprint_Planning_Complete` and `Sprint_Complete`. It is documented in the guide's lifecycle table and cycle trigger table. Phase 4 (`run delivery verification`) may not be invoked while status is `Executing` — Phase 3 must complete and status must reach `Sprint_Complete` first.

If execution_state.json already exists: resume (do not reinitialise). Perform STEP 0 only for items with status `not_started`.

---

## STEP 1 — GitHub Issue Preflight

Issues are created by `sync gh` at the end of sprint planning (CLAUDE.md §4). This step verifies they exist and records their numbers.

For each ST item in the sprint scope:

1. Check `execution_state.json` for `github_issue` value.
2. If `null` or absent: search GitHub for an existing issue matching the ST ID and title.
3. If found: record the issue number in `execution_state.json`.
4. If not found: note as a process gap (`sync gh` was not run at planning seal), then create a minimal issue — Title: `[ST-xx] <title>`, Labels: `EPIC-xx` — and record the number. Do not halt.
5. Update `execution_state.json` with all issue numbers.

Before creating an issue for any story, run:
```
gh issue list --search "[ST-xx]" --state open --json number,title
```
replacing `ST-xx` with the actual story ID. If a matching open issue is returned: record the issue number in `execution_state.json` and skip `gh issue create`. Do not create duplicate issues.

---

## STEP 2 — Branch Preflight

For each EPIC in scope:

1. Check whether branch `exec/<cycle_id>/EPIC-xx` exists (local or remote).
2. If it does not exist: create it from the current `main`.
3. If it exists: verify it is based on `main` (or the declared base branch). If it has diverged: flag as a blocker, record in escalations, halt this EPIC (continue other EPICs).
4. Record branch name in `execution_state.json`.

---

## STEP 3 — Execution Loop (Per EPIC, Per ST Item)

```yaml
# commit format (mandatory ∀ commits on exec/** branches):
"[EPIC-xx][ST-xx] <imperative description>"
# two stories in one commit: "[EPIC-xx][ST-xx][ST-yy] <description>"
# governance_sync.yml parses this to close GitHub issues automatically
```

Work through EPICs in dependency order. Within each EPIC, work through ST items in dependency order.

### 3.1 For each ST item

#### 3.1.A If `autonomous`:

1. Execute the work defined in the acceptance criteria. **Test scenarios advisory (ST-13):** When tests are created as part of this work, populate `test_scenarios` in `execution_state.json` for the parent EPIC with the test file paths (e.g. `tests/test_screener_service.py`). This is non-blocking — story execution does not halt if the field is not updated immediately — but it must be populated before the EPIC-level QA evidence log is created at STEP 3.2.A. **Scoping rule (AUD-2026-05-21-003):** Only list spec files that contain at least one scenario directly exercising an acceptance criterion for this EPIC. Do not list shared utilities or spec files from other EPICs whose tests happen to run in the same suite.
2. **Spec_references policy (SC-03):** Populate `spec_references` in `execution_state.json` using this 4-case lookup:

   | Case | Story type | Rule |
   |------|-----------|------|
   | A — Path verify | Any story | Verify each path exists on disk (file read or ls) before recording. Non-existent paths cause false traceability — record only resolving paths. (LL-v3.7-EX-03) |
   | B — Documentation-creation | Primary deliverable IS a new/updated spec or doc artefact (API contract, metrics definition, schema spec) | Set `spec_references` to the created/updated artefact path — the artefact IS the governing spec. Also record path in `delivery_note` field. `spec_references = []` is non-compliant. (LL-v4.5-EX-02) |
   | C — Test-authoring | Sole deliverable is a new test file; no prior canonical spec governs the work | Set `spec_references` to the created test file path. Do not leave empty with `notes: "no prior spec applicable"` — the file IS a traceable artefact. (OA-02) |
   | D — CI/infrastructure | Sole deliverable is a CI/pipeline/tooling config change (e.g. `playwright.config.js`, workflow YAML) with no prior canonical spec | Set `spec_references` to the primary file changed — it is the de facto spec reference. (FI-P4-01 / DF-10) |
   | E — No governing spec exists | Bug/correctness fix (backend or otherwise) with no prior canonical spec to cite and no new artefact created that would itself serve as one — e.g. a data-integrity or security fix verified only against its own stated acceptance criteria and a regression test | Set `spec_references: []`, `spec_reference_not_applicable: true`, and `spec_reference_not_applicable_reason` to a one-line rationale (e.g. `"bug fix, no prior canonical spec — verified via tests/test_x.py"`). This structured pair is the required signal — do not rely on freeform `notes` text alone. (Added v3.55, lessons_learnt_closure.md v6.8 Phase 4 friction item — replaces the undocumented `notes: "no prior spec applicable"` convention with a field Delivery Verification can check directly instead of re-deriving rationale from prose each time.) |

   If none of the above cases apply and a governing spec exists: set `spec_references` to that spec path. `spec_references = []` should not occur for any story type covered by Cases A–E above.

3. Commit to the EPIC branch (format: see STEP 3 header schema).

> **API performance baseline advisory (AUD-2026-06-22-006):** If this commit adds a new entry to `docs/reference/openapi.yaml`, also add a corresponding row to `docs/ops/api_performance_baseline.md` in the same commit. **Note (v6.9 post-ship closure correction):** this is enforced by a hard CI gate — "API Performance Baseline Drift Detection (ST-12)" in `.github/workflows/quality_gate.yml` — not merely an advisory; omission blocks the PR outright rather than being caught at post-ship STEP 6. Applies to any story that adds a `## METHOD /path` heading to a file in `docs/specs/api_contracts/`.

> **AST-derivable hardcoded constant re-derivation check (structural fix, OA-5 post-ship closure 2026-07-24__release-v7.8):** If this commit hardcodes a literal count/total/constant that mirrors a value also mechanically derivable from a script or AST scan of the codebase (e.g. `src/pages/SystemStatus.js`'s `Tests {totalTests || 'N'} endpoints` fallback count per CLAUDE.md §2, or any similar count-of-X literal kept in sync with a source of truth it summarises), do not assume the value carried over from this branch's cut-from-main baseline is still correct — re-derive it fresh (re-run the script/count against the current codebase) immediately before this commit, and again immediately before opening the PR if `main` has moved since. This class of constant produced an undetected `git merge` collision in two consecutive cycles (v7.7, and v7.8 EPIC-01/EPIC-06 — identical shape) because two independently-cut branches each hardcoded the same wrong value against different baselines: the literal text matched, so `git merge` saw no conflict even though the value was wrong on both branches relative to the post-merge state. A stale-but-matching literal is invisible to `git merge`; only re-derivation catches it.

4. Push to `exec/<cycle_id>/EPIC-xx`.
4a. **Commit SHA record (LL-v4.8-EX-01):** Immediately after push, run `git rev-parse HEAD` to obtain the pushed commit SHA. Write it to `execution_state.json` for this ST item: `epics.<EPIC-xx>.stories.<ST-xx>.commit_sha`. For batch commits covering multiple stories, write the same SHA to all covered story entries. Do not defer this write to sprint close — an unrecorded SHA cannot be recovered if the branch advances before seal.
4b. **`completed_utc` derivation (BLG-GOV-309, ST-20, v8.9):** In the same step as 4a, derive `completed_utc` from the pushed commit's own authored timestamp — run `git log -1 --format=%aI <sha>` (the SHA from 4a) and write that value, not an approximated or narrated wall-clock estimate. This field was previously undocumented anywhere in this prompt (no schema definition, no derivation rule existed for it or for `blocked_since_utc`), which is the root cause of the ~5-6 hour drift found between recorded `completed_utc` values and commits' actual `authoredDate` (BLG-GOV-309, found via `gh pr view`'s commit data on EPIC-06's stories, `2026-08-14__release-v8.8`). For batch commits covering multiple stories, the same authored timestamp applies to all covered story entries, same as the SHA.
5. `governance_sync.yml` closes the GitHub issue automatically on push.
6. Verify issue is closed (re-check after push).

```yaml
# state update after push:
epics.<EPIC-xx>.stories.<ST-xx>:
  status: done
  commit_sha: <pushed sha>
  completed_utc: <commit's own %aI authored timestamp — see 4b, not an estimate>
  acceptance_verified: true   # set once AC confirmed met
```
10. Deviation check: compare implementation against canonical spec.
    - If no deviation: set `deviations_filed = true` (meaning "deviation check completed; none found").
    - If a deviation exists: document it in the canonical spec per `claude/charter/document_lifecycle_guide.md` §9 (description, canonical requirement, priority P0–P3, target resolution release, owner, backlog reference). Set `deviations_filed = true` once filed. A P0 deviation blocks the merge gate — escalate immediately.
    - **Deviation type distinction (LL-v1.10-P4-2):** If the deviation is "endpoint/feature absent from spec" (the spec does not define this thing at all), file in `qa_evidence_EPIC-xx.md` and backlog only — the canonical spec is not the right home for an absence note. If the deviation is "implementation differs from what the spec requires" (the spec defines it, but the implementation diverges), file in the canonical spec as above.
    - **Intent check advisory (LL-v3.4-P3-03):** Before filing a deviation, verify implementation matches spec *intent*, not just literal draft wording. If spec and implementation agree on intent, record as an implementation note in `execution_state.json` notes only — do not file a deviation.
    - **Known Deviations section advisory (LL-v3.4-P3-04):** When filing a deviation in the canonical spec, also add a `## Known Deviations` section to that spec in the same commit if one does not already exist. This makes the deviation traceable directly from the spec and reduces Phase 4 verification overhead.

10a. **Deviations_filed atomic write (LL-v3.7-EX-01):** Immediately after step 10 deviation check: write `deviations_filed: true` to `execution_state.json` for this ST item. Do not defer this write to a later step or to sprint close.
    - **Same-step self-verification read-back (LL-v9.0-P3-01):** Immediately after making the write above, re-read `execution_state.json`'s `deviations_filed` field for this ST item back and confirm it now reads `true` before advancing to step 11. This converts the "do not defer this write" instruction from memory-dependent to mechanically-checkable — mirroring the structural append-verification pattern already used elsewhere (`shared_standards.md §7.1`). Added after 12 of 27 stories at `2026-08-21__release-v9.0` reached STEP 5.1 still carrying `deviations_filed: false` despite the underlying deviation check having genuinely been completed — a pure write-timing miss caught only by STEP 5.1's own batch backstop, not by this step itself.

    - **Resolving-commit deviation-closure discipline (LL-v9.0-P4-01, BLG-GOV-315):** If this story's work closes the root cause of a *pre-existing*, already-filed deviation (`DEV-*`, filed by a different story or a prior cycle — not one being newly filed by this step's own deviation check), the same commit must also update that deviation's own labelled Known Deviation fields (at minimum: Target resolution release / Status) in its canonical spec or supporting-document entry — not just add narrative evidence elsewhere in the document. Confirmed 3 times across 4 cross-cycle deviation consolidation reviews (`docs/governance/deviation_consolidation_review_*.md`) that a deviation resolved via a later, different story's own evidence does not automatically propagate back to its own tracking fields, because no prior step re-visited a pre-existing deviation's fields when a later story closes its root cause.

10b. **Backlog verify guidance (LL-v3.7-EX-02):** When filing a mandatory backlog item for a deferred staging AC (per `LL-v3.1-EX-01` or CLAUDE.md §2 frontend testing gate), verify the item appears in `claude/backlog/backlog.md` before closing the story (file read or grep check). A backlog item that was not persisted does not satisfy the gate.

11. **Sign-off gate:** If the item's seal condition in `sprint_backlog.md` names a required sign-off role: invoke agent-mediated sign-off per §5.3. Do not mark `acceptance_verified = true` until `sign_off_record.status = "cleared"`. Record outcome in `sign_off_record` in `execution_state.json`.

12. **Post-story test files check (OA-04 / ST-09):** If this story created any new test files (in `tests/` or `tests/e2e/`), populate `test_scenarios` in `execution_state.json` for the parent EPIC with those file paths **now**, before advancing to the next story. Do not defer this step to STEP 3.2.A. Only include spec files containing scenarios that exercise this EPIC's acceptance criteria — do not add cross-EPIC spec files.
    - **Roll-up backstop (LL-v8.4-P4-01):** Before sealing the EPIC (STEP 3.2.A), cross-check the EPIC-level `test_scenarios` array against the union of all its stories' own `spec_references` entries that are test files (`tests/` or `tests/e2e/` paths). If any such file is present in a story's `spec_references` but absent from the EPIC-level `test_scenarios` array, add it — do not leave `test_scenarios: []` at the EPIC level when a story's own `spec_references` already lists real, run test files. This catches the case where step 12 above was skipped for an individual story but the file was still correctly recorded at story level (found `2026-08-07__release-v8.4`, EPIC-01 — real Playwright/pytest coverage existed and was cited in `qa_evidence_EPIC-01.md`, but the EPIC-level rollup was never populated).
      - **Re-trigger on post-seal edits (LL-v8.4-P4-01a, applied v8.6 after 1 cycle carried):** If a story's `spec_references` is edited *after* this roll-up check has already run once (e.g. during in-EPIC DoQ remediation, after the initial EPIC seal), re-run the cross-check before the EPIC's own DoQ sign-off completes — do not rely on the single initial-seal pass alone. Confirmed gap: `2026-08-11__release-v8.6` EPIC-03's `test_scenarios` array omitted `tests/e2e/saved-filters-calendar-view.spec.js`, added to ST-05's own `spec_references` only during a mid-EPIC remediation pass that ran after the initial roll-up check.
      - **qa_evidence cross-check extension (LL-v9.0-P4-02):** The roll-up backstop above only cross-checks stories' own `spec_references`. This misses test files that were genuinely authored and run for an EPIC's stories but never entered into any story's `spec_references` (e.g. ops/infra-class stories that use `spec_reference_not_applicable` or list only supporting-doc references). Before EPIC seal, also cross-check the EPIC-level `test_scenarios` array against the "Test scenarios used" / "Scenarios run" line in that EPIC's own `qa_evidence_EPIC-xx.md` — if a real test file is named there but absent from `execution_state.json`'s `test_scenarios` array, add it. Confirmed gap: `2026-08-21__release-v9.0` EPIC-03's `test_scenarios` field was left as `[]` despite `qa_evidence_EPIC-03.md` itself listing 3 real, run test files (`tests/test_deploy_path_filter_drift_check.py`, `tests/test_staging_smoke_test.py`, `tests/test_wait_for_staging_deploy_live.py`) — a metadata-completeness gap, not a coverage gap, but one requiring cross-referencing two documents to catch at verification time instead of being visible from `execution_state.json` alone.

13. **Cross-spec selector check (LL-v3.2-P3-02, SC-06):** Skip this check for governance-only and backend-only stories — no DOM changes are possible. For stories that **do** modify, replace, remove, or rename a DOM element (e.g. changes a component, removes a checkbox, renames a form field): scan all existing Playwright spec files in `tests/e2e/` for selectors targeting that element (by ID, data-testid, role, or class name). If stale selectors are found, update them in the same commit before pushing. Frontend EPICs retain the full scan requirement with no exceptions.

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
   - For `delegated_frontend`: include the complete Base44 prompt draft (all six sections). **New page route (AUD-2026-05-21-005):** If the story creates a new frontend page (new route), the delegation spec must additionally require: (a) `createPageUrl` map update in `pages.config.js` with the new route entry; (b) nav/sidebar registration if applicable. Explicitly state the target map key and value in the spec.
3. Set item status to `blocked_backend` or `blocked_frontend` in `execution_state.json`. **`blocked_since_utc` derivation (BLG-GOV-309, ST-20, v8.9):** In the same write, record `blocked_since_utc` as the real current wall-clock time at the moment of this write — obtain it via a shell timestamp command (e.g. `date -u +%Y-%m-%dT%H:%M:%SZ`), not an approximated or narrated value. Unlike `completed_utc` (step 4b below, derived from a commit's own authored timestamp), there is no commit to anchor to at blocking time — this field's correctness depends on reading the actual current time at the moment of the write, not estimating it.
4. Record `delegation_record_id` and `unblock_criteria` in the item.
5. Surface the delegation to the assigned role with:
   - Exactly what is needed (with spec reference or Base44 prompt draft)
   - The branch to commit to
   - The required commit format: `[EPIC-xx][ST-xx] <description>`
   - The issue number
6. **Continue to the next ST item.** Do not stall.

**In-session credential/action provisioning (LL-v8.2-P3-04):** Steps 1–6 above describe the standard park-and-wait flow, where a human completes the blocking action in a *separate* session and the engine detects it on resume. A distinct sub-path applies when the human instead supplies the missing credential, dashboard action, or other blocking input **directly within the current session** (e.g. the user pastes a rotated API key, confirms a Render/Supabase dashboard change was made live, or grants a one-off access token mid-conversation):
- Create the `delegation_log.md` entry **at the moment the need is identified** (step 2 above), even though it may be unblocked seconds later — do not wait to see whether the human responds in-session before writing it, and do not write it retroactively at sprint close. An entry created after the fact cannot be trusted to capture the actual blocking window.
- The moment the human provides the input in-session: immediately re-run the **Unblock detection** logic below rather than treating step 6's "continue to the next ST item" as a multi-session parking instruction — there is no need to move on and re-check later if the unblock condition is already satisfied in this same turn.
- Record the delegation log entry's terminal `Unblocked` state with an explicit note: `"Unblocked in-session — <what was supplied>, <who supplied it>, same session as delegation"` — this distinguishes it from a genuine cross-session delegation for anyone reading the log later.
- All other requirements (spec_references, deviation check, sign-off gate) still apply once the item is unblocked — in-session provisioning shortens the *wait*, not the *verification*.
- **Commit-SHA write reminder (LL-v8.4-P3-01):** Once the item is unblocked and its commit is pushed, step 4a's commit-SHA record (`LL-v4.8-EX-01`) still applies — write `commit_sha` to `execution_state.json` immediately after push, same as the standard flow. This sub-path's own step list ends at "re-run Unblock detection"; it does not itself repeat the SHA-write rule, which made it easy to complete the in-session unblock and mark the item `done` without the SHA ever being recorded (found `2026-08-07__release-v8.4`, 3 items: ST-20/ST-21/ST-23 — all corrected same-session, see `lessons_learnt_cycle.md` Phase 3).

**Unblock detection (on resume):**
- Check whether a commit matching `[EPIC-xx][ST-xx]` has been pushed to the branch since delegation.
- If yes: transition item to `done`, verify acceptance criteria, update state.
  - Confirm `spec_references` is populated (fill now if missing — ask the assignee which spec section was implemented).
  - Check for deviations: if implementation diverges from the spec, file the deviation in the canonical spec before setting `deviations_filed = true`.
  - **HARD GATE: Update the delegation log entry** (per `shared_standards.md §16.3`) — two-phase write: **(a) sign-off step:** set DEL record `status = "sign_off_cleared"` when sign-off is confirmed; **(b) push step:** set DEL record `commit_sha` when the commit SHA is recorded. Both sub-steps must complete before setting the DEL entry to terminal state `Unblocked`. Set item `status = done` in `execution_state.json` atomically with the `Unblocked` write. Do not advance to the next ST item until the delegation log entry is at terminal state `Unblocked` and execution_state item is `done`.
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
2. Set item status to `blocked_decision`. Record `blocked_since_utc` per the same real-wall-clock-time rule as §3.1.B step 3 above (BLG-GOV-309, ST-20, v8.9).
3. Surface to the owning authority:
   - The decision required
   - The unblock criteria
   - The SLA (default: 24 hours for lifecycle; 72 hours for strategy)
4. Continue to next item.

**SLA breach tracking:** Per `claude/system/shared_standards.md §16.4`.

**Unblock detection:** Check escalation record for Resolved or Accepted Risk disposition. If resolved: re-classify item and resume. **HARD GATE: Update the delegation log entry** (per `shared_standards.md §16.3`) — two-phase write: **(a) sign-off step:** set DEL record `status = "sign_off_cleared"` when the escalation disposition is resolved; **(b) push step:** set DEL record `commit_sha` when the commit SHA is recorded. Set item `status = done` in `execution_state.json` atomically with the terminal `Unblocked` write. Do not advance to the next ST item until both are recorded.

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

The consolidation block must include: EPIC, Cycle, Sprint goal, Test scenarios used, a row per ST item (Spec Reference / What was built / AC / Result / Deviations), QA test coverage (scenarios run, regression areas, deviations), and the sign-off block. **Template: `claude/system/templates/qa_evidence_template.md`** — read this file to get the exact header, consolidation block format, and sign-off block template. Key rule: the sign-off block `Date:` field must be non-blank before the PR can be opened (§3.2.B pre-condition) and before the merge gate runs.

**Multi-sprint EPIC second-PR convention (AUD-2026-08-21-005):** If an EPIC's original PR has already merged and a later gated Sprint-2 (or subsequent) story requires a new PR against the same EPIC, do not overwrite the EPIC's existing `pr_number`/`pr_status` fields in `execution_state.json`. Instead, add a sub-object `epics.<EPIC-xx>.additional_prs: [{label, pr_number, pr_status, status}]` recording the new PR separately, preserving the original Sprint 1 PR record intact.

**Governance self-consistency check at OPERATIONAL_GUIDE.md version bump (LL-v8.5-P3-01, applied v8.6 after 2 cycles carried unapplied):** If any story in this EPIC bumped `OPERATIONAL_GUIDE.md`'s version (i.e. CLAUDE.md §6's Governance File Edit Checklist fired for this EPIC), run the `governance-drift` skill's Step 1b self-consistency check (3-way match: document header / §14 self-row / Change Log top row) before completing this EPIC's DoQ sign-off. If `SELF-DRIFT` is found: fix per the skill's own Step 5 before proceeding to §3.2.B. This closes the gap between "a check exists" (the skill) and "the check is mandatorily run at the moment it matters" — deferred at `2026-08-08__release-v8.5` Phase 3 lessons learnt, carried forward without a `prompt_change_log.md` entry for 2 consecutive cycles, applied now per `lessons_learnt_prompt.md` §3.7's recurrence-escalation rule rather than deferred a 3rd time.

**Hard requirement (OA-1/ST-01, elevated from advisory — DF-02, v6.3 Phase 3 LL, applied v6.4 post-ship closure):** After completing DoQ sign-off and committing `qa_evidence_EPIC-xx.md`, update `execution_state.json` `qa_signed_off: true` in the same commit. The STEP 4 merge gate table's `qa_signed_off = true (execution_state.json)` row enforces this — the merge gate blocks if the flag is unset, even if the qa_evidence log and PR comment are both present.

This file is the evidence backing `qa_signed_off = true` in `execution_state.json`. A PR comment alone is not sufficient — this file must exist and the sign-off block must be complete before the merge gate runs.

**Frontend testing gate (LL-v3.1-EX-01 — hard gate):**

Before signing off any EPIC that introduces frontend-visible changes, verify for each observable AC (visible rendering, element presence/absence, colour, interaction, timing):

1. **Check Playwright coverage:** Is there a Playwright test in `tests/e2e/` that exercises this AC? If yes: record the test file and scenario ID in the DoQ comments.
2. **If no Playwright test:** Has a human staging run been performed? If yes: record the staging run date in the DoQ sign-off block.
3. **If neither:** The AC must be noted in the sign-off comments as "code review only — backlog item required". File a backlog item (via `/backlog-add`) for the Playwright test before opening the PR. This is a **hard gate**: the PR may not be opened with observable AC marked "code review only" unless the backlog item reference is recorded in the sign-off comments.

The autonomous class sign-off (BLG-GOV-19) is unavailable for any EPIC with frontend-visible changes — criterion 3 (no frontend-visible change) will not be met.

**Environment-parity sub-clause for focus/interaction-timing ACs (LL-v8.3-P3-02):** A sandboxed or local pre-merge review pass is not a fully reliable predictor of real-CI Playwright outcomes for focus-restoration, focus-trap, and other interaction-timing behaviour specifically — confirmed at `2026-08-05__release-v8.3` ST-11, where a `Dialog.Content` focus-restoration assumption (Radix does not fall back to restoring `document.activeElement` without an explicit `onCloseAutoFocus` handler) passed sandboxed review but failed real GitHub Actions CI. For any AC in this sub-class (focus moves on open/close, keyboard-trap boundaries, debounce/throttle-gated interactions, animation-completion-gated state changes): step 1's "Check Playwright coverage" is not satisfied by a locally-authored-and-reviewed test alone — record in the DoQ sign-off comments that the specific scenario was **observed passing in a real GitHub Actions CI run** (not merely "coverage exists"), citing the run URL or commit SHA. If the PR has not yet had a real CI run at sign-off time, note this explicitly as a pending confirmation and re-check before merge — do not treat sandboxed-pass as sufficient for this AC sub-class specifically.

**Autonomous DoQ sign-off class (BLG-GOV-19):**

When all four of the following qualifying criteria are met, the engine may apply an autonomous DoQ sign-off without Director of Quality review. This class is defined to avoid unnecessary delegation blocks on pure governance or spec documentation EPICs where no behavioural verification is possible.

**Qualifying criteria:**
1. All stories in the EPIC have `delegation_class: autonomous`. **Verification-class sub-criterion (LL-v4.5-EX-01 — pre-planning sprint pattern):** Criterion 1 may be satisfied when all stories' VERIFICATION is by document inspection only (regardless of EXECUTION class), provided criteria 2–4 are also met. Applies when: the EPIC's primary deliverable is a governance or spec document; no observable UI behaviour, staging run, or live system interaction is required. Does not apply to EPICs with `delegated_backend` execution where the deliverable is a running system component.
2. All AC is verifiable by code review alone — no observable UI behaviour, no staging run required, and no live system interaction
3. No frontend-visible change is introduced by this EPIC — **detection rule (BLG-GOV-135):** if any story in this EPIC creates or modifies a file under `src/components/**` or `src/pages/**`, this criterion is automatically unmet and the autonomous class path is unavailable, regardless of Playwright test coverage
4. Engine signer field is populated as "Sprint Execution Engine (autonomous class)"

When all criteria are met, populate the sign-off block using the **BLG-GOV-19 template in `claude/system/templates/qa_evidence_template.md`**.

If any criterion is not met, the autonomous class does not apply — the sign-off block must be completed by the Director of Quality. An EPIC signed off under the autonomous class is still subject to the STEP 4 merge gate; the Director of Quality may review and override at any time before merge.

**Reclassification counter-sign rule (BLG-GOV-14 / LL-v2.3-EX-02):** When a story was originally classified `delegated_frontend` and has been reclassified to `autonomous` per LL-v2.3-EX-02, but the EPIC as a whole introduces frontend-visible changes (UI rendering, interaction behaviour, or page routing), the autonomous class sign-off is insufficient for that EPIC. Director of Quality counter-sign is required at STEP 5 sprint close, in addition to the engine sign-off. Record the counter-sign as a second sign-off block in `qa_evidence_EPIC-xx.md` and confirm in `sprint_close.md`.

**EPIC-level consolidation note (BLG-GOV-14):** When story-level sign-offs within the EPIC involve domain-specific authorities (e.g. Strategy Rules & System Intent Owner, Security Officer, Compliance), the EPIC-level DoQ consolidation block in `qa_evidence_EPIC-xx.md` must explicitly list those story-level authority sign-offs and confirm they are cleared. A domain-authority sign-off at story level does not substitute for the EPIC-level DoQ consolidation block — both are required.

**3.2.B — Open PR**

**Pre-condition (BLG-GOV-18):** Do not open the PR until the DoQ sign-off block in `qa_evidence_EPIC-xx.md` has a non-blank `Date:` field. A blank Date means sign-off is incomplete. The merge gate (STEP 4) also enforces this, but checking here prevents opening a PR that will immediately be blocked — which creates unnecessary review noise. If the Date field is blank: complete the sign-off first, then proceed.

**qa_evidence commit advisory (BLG-GOV-118):** Before running `gh pr create`, verify that `qa_evidence_EPIC-xx.md` is committed to the EPIC branch. Run `git status --short` and confirm the file is not listed as untracked or modified. An uncommitted `qa_evidence_EPIC-xx.md` is invisible to reviewers and CI, and will not satisfy the merge gate evidence requirement. Commit it now if it exists only as an untracked or modified file.

**API performance baseline pre-PR check (LL-v7.6-P3-01, enforced as script step OA-2 v3.60):** Before running `gh pr create`, run `python3 scripts/check_api_performance_baseline_drift.py` (the same check `quality_gate.yml`'s "API Performance Baseline Drift Detection (ST-12)" CI job runs). This is a hard pre-PR gate, not an advisory — if the script exits non-zero, add a registration entry for each endpoint it lists now, following the most recent `## N. vX.Y Endpoint Registration` section's pattern (read one for the exact format — endpoint profile table, characteristics, Infrastructure & Operations Owner sign-off block), then re-run the script until it exits 0, before opening the PR. Do not run an ad hoc `grep` instead of the script — the prose-advisory form of this check (a per-path manual grep) failed to prevent the same class of miss twice (v7.6/EPIC-07, v7.8/EPIC-06) because it relied on the agent remembering to run it correctly on every new path under multi-file endpoint-addition load; the script removes that judgment call by checking every `openapi.yaml` endpoint in one deterministic pass with a hard exit code.

1. Open a pull request: `exec/<cycle_id>/EPIC-xx` → `main`
2. PR title: `[EPIC-xx] <epic description>`
3. PR body: per Section 8.4 — include link to `qa_evidence_EPIC-xx.md`
4. Update `execution_state.json`: EPIC `pr_status` = `open`, `pr_number` = PR number.
5. Run `gh pr view <pr_number> --json state,mergeStateStatus` immediately and sync `pr_status` in `execution_state.json` to the actual current state. **EPIC.status sync rule:** If `state = "MERGED"` (PR was already merged before the engine recorded it), update `EPIC.status` from `"done"` to `"merged"` in `execution_state.json` in the same write.
6. Do not merge autonomously. The merge gate (STEP 4) governs this.

---

## STEP 4 — Merge Gate (Hard Gate, Per EPIC)

> **On session resume — merge gate state sync (required, LL-v3.9-P3-1):** When invoking `run sprint` in a fresh session, `execution_state.json.merge_gate.epics_merged` may be stale if one or more EPICs were merged via GitHub between sessions. **Branch check before syncing (LL-v6.4-P3-01):** Run `git branch --show-current` before performing the sync write. If the result is not `main`, run `git checkout main && git pull` first — a fresh session can resume on any `exec/**` branch, and the sync write below must land on `main`, not on whatever branch happened to be checked out (a write orphaned on a stale exec branch has to be redone against main's post-merge file). Before evaluating any EPIC's merge gate conditions, run `gh pr view <pr_number> --json mergedAt,mergeStateStatus` for every EPIC in `merge_gate.epics_pending`. If `mergedAt` is non-null, that EPIC is already merged — add it to `merge_gate.epics_merged`, remove it from `merge_gate.epics_pending`, and set the EPIC's `pr_status = "merged"` in `execution_state.json`. If `epics_pending` is now empty after the sync, proceed directly to STEP 5 (Sprint Close) — do not re-evaluate merge gate conditions for already-merged EPICs.
>
> **Mid-session re-sync on every "PR merged" report (AUD-2026-08-21-010):** The check above fires at session-start/resume, but a single continuous session that merges multiple sibling PRs in sequence (e.g. a cross-EPIC conflict-resolution pass, CLAUDE.md §8) can go stale *between* those merges too — nothing previously re-fired this check mid-session. Whenever the user reports a PR merged at any point during an active session, re-run this same sync (branch check + `gh pr view ... --json mergedAt,mergeStateStatus` for the merged EPIC) immediately, before proceeding to the next EPIC in queue — do not wait for the next full session start to catch the staleness.
>
> **Orphaned post-merge commit check (LL-v6.8-P3-01):** The sync above only covers `execution_state.json`'s own merge_gate fields. Separately, for every EPIC now confirmed merged, run `git fetch origin` then `git log origin/main..origin/exec/<cycle_id>/<epic_id> --oneline`. Any commit listed was made *after* that EPIC's PR merged and is orphaned — it never entered `main` via the PR merge diff. For each orphaned commit: inspect its content (`git show <sha> --stat`); if it modifies a shared governance file (e.g. `claude/backlog/backlog.md`, `execution_state.json`, `claude/system/*`) with content not already present on `main`, reconcile it onto `main` now (apply the equivalent change directly, or cherry-pick if clean) and commit with message `[EPIC-xx] Reconcile orphaned post-merge commit <sha> onto main`. If the content is already present on `main` in equivalent or superseding form, no action is needed beyond noting the redundancy. Record every check performed (reconciled or redundant) in `execution_state.json`'s `process_notes` array (create if absent) — this check runs per-EPIC at merge-gate resume, before `sprint_close.md` exists; STEP 5.3 rolls `process_notes` up into the sprint close record's Process Notes section. This check exists because STEP 4's post-merge hard-gate halt does not itself prevent a session from continuing to commit governance-file changes (e.g. mid-session backlog filings) to an EPIC branch after that branch's PR has already merged — any such commit is stranded unless explicitly reconciled. **Note (LL-v6.8-P3-02):** the "If all conditions pass" flow below now checks out `main` before its own state-sync and governance-file commits (step 3a0), so this scan should find nothing to reconcile from that flow going forward — it remains active only as a safety net for commits made outside it.

A PR may only be merged when **all** of the following are true:

| Condition | Required State |
|-----------|---------------|
| All ST items in EPIC | `done` (not `blocked_*`) |
| Acceptance criteria | verified for all ST items |
| `spec_references` | populated for all `done` ST items |
| `qa_evidence_EPIC-xx.md` | exists; all ST item disposition sections completed by Director of Quality |
| QA sign-off | comment from Director of Quality on PR referencing qa_evidence log |
| `qa_signed_off = true` (execution_state.json) | flag set in the same commit as the qa_evidence sign-off block (DF-02, v6.3 Phase 3 LL) — a PR comment alone does not satisfy this row |
| Product Owner acceptance | recorded (comment on PR or in `sprint_backlog.md`) |
| `quality_gate.yml` CI | passed (PR title has `[EPIC-xx]`, all checks green) |
| No open escalations | for items in this EPIC |
| No unresolved P0 deviations | all `deviations_filed = true`; no P0 deviations open in referenced specs |

If all conditions pass:
1. Merge the PR (squash or merge as configured).
2. Update `execution_state.json`: EPIC `pr_status` = `merged`, `status` = `merged`.
3. Update `merge_gate.epics_merged`.
3a0. **Branch checkout before state-sync commits (LL-v6.8-P3-02 — supersedes committing to the EPIC branch post-merge):** Immediately run `git checkout main && git pull origin main` (same branch-check pattern used at session resume, above). Steps 3a and 3b below commit onto `main`, not the just-merged `exec/<cycle_id>/<epic_id>` branch. Committing to that branch after its own PR has merged produces an orphaned commit that never reaches `main` via the merge diff — this was LL-v6.8-P3-01's root cause (all three EPIC branches in the v6.8 cycle received post-merge commits stranded on the now-inert branch, one of which required manual reconciliation at the next `run sprint` resume). The "Orphaned post-merge commit check (LL-v6.8-P3-01)" note above remains active as a secondary safety net (e.g. for commits made outside this flow), but this fix removes the routine cause of it firing.
3a. **Persist state before halt (LL-v5.5-EX-02 — third recurrence: v5.3/v5.4/v5.5):** Immediately commit `execution_state.json` on `main` NOW — before outputting the halt message. An uncommitted state write is lost if the session ends, requiring stale-state correction on the next resume. Run: `git add claude/cycles/<cycle_id>/execution_state.json && git commit -m "[EPIC-xx] Persist merged state before session close" && git push origin main`. This is a hard requirement; the halt message must not be the last action in the session if execution_state.json is unstaged.
3b. **Pre-halt governance commit (AUD-2026-06-22-002):** Before outputting the halt message, run:
```
git status --short
```
If any tracked governance files are modified or unstaged — in particular `claude/backlog/backlog.md`, `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md`, or any other `claude/` file written during this EPIC's execution — stage and commit them now on `main` (per 3a0 above):
```
git add claude/backlog/backlog.md claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md
git commit -m "[EPIC-xx] Commit governance file updates before merge halt"
git push origin main
```
Do not leave governance files unstaged. An unstaged backlog.md or qa_evidence file at session close requires `git stash` on next resume and risks stash-pop conflicts. This step fires after step 3a (execution_state.json persist) and before the halt output.

3c. **Proactive sibling-branch `execution_state.json` sync (structural fix, OA-4 post-ship closure 2026-07-24__release-v7.8):** For every EPIC branch still in `merge_gate.epics_pending` after this merge, propagate this merge's `execution_state.json` change to that branch now, instead of letting every pending branch accumulate an independently-diverging copy until its own eventual merge gate:
```
git checkout exec/<cycle_id>/<epic_id>
git merge main --no-commit --no-edit
```
If `execution_state.json` conflicts, resolve per CLAUDE.md §8's rules (accept story completion data from the branch; never revert `done` → `blocked`; take the union of completed items across both sides; take the branch's blocked/delegated lists). Commit as `[EPIC-xx] Sync execution_state.json from main post-merge` and push, then `git checkout main` before continuing. This runs once per remaining pending branch, per merge event.

This step exists because a per-branch resolve deferred to each branch's own merge gate compounds: the conflict recurred 2 consecutive cycles with cost scaling up each time (10/11 branches at v7.7, 11/12 at v7.8) rather than down, because the prior cycle's identical deferred fix (v7.7 lessons learnt) was never applied. Resolving the shared-file drift incrementally, right after each merge, keeps each individual resolve small instead of letting it compound into a full-cycle scramble across every remaining branch at once.

4. **[HARD GATE — HALT after every EPIC merge (OA-01, v4.1 ST-01)]** Output the block below and **stop immediately**. Do not proceed to the next EPIC, do not continue the execution loop, do not execute STEP 5 in this invocation. The engine resumes only when the user explicitly re-invokes `run sprint`:

> ✅ EPIC-xx merged. **HARD GATE: Re-invoke `run sprint --cycle <cycle_id>` now.** The engine halts after every EPIC merge and may not auto-advance to the next EPIC or STEP 5. If this is the final EPIC, re-invocation detects `merge_gate.all_merged = true` and executes STEP 5 (Sprint Close) directly, producing `sprint_close.md` and sealing `execution_state.json`. Do not proceed to `run delivery verification` without this re-invocation.

> **⚠ ENFORCEMENT:** `.github/workflows/sprint_close_reminder.yml` posts a PR comment on every EPIC merge as a backup reminder. The halt is absolute — STEP 5 must execute in the re-invocation session, not this one. Any output after this block (other than the halt marker) is a process violation.

If any condition fails: do not merge. Record which condition is unmet. If QA or Product Owner has not responded within their SLA: file an escalation record.

**The engine may not self-approve a merge.** QA sign-off and Product Owner acceptance are always required and must come from the relevant authority.

> **Session-close advisory (AUD-2026-06-10-002, superseded by step 3b for governance files):** Step 3b above now enforces a mandatory pre-halt commit of governance files (backlog.md, qa_evidence). This advisory remains active for any non-governance working-tree changes not covered by step 3b (e.g. source code edits left open). If `git status --short` shows any remaining changes after step 3b: commit or stash before closing. (Root cause: v5.3 + v5.4 + v5.5 + v6.0 recurrence of stash-at-branch-switch pattern — AUD-2026-06-22-002.)

> **Merge order note (LL-v2.0-P3-5):** If more than one EPIC branch modifies a shared governance file (e.g. `execution_state.json`, `.claude_current_state.json`, `backlog.md`, `delegation_log.md`), establish a merge order at the start of STEP 3. Later EPIC branches **must rebase onto `main`** after the first EPIC merges — before running their final QA review and opening a PR. This prevents merge conflicts at the merge gate and avoids the need to rebase mid-merge-sequence.
>
> **Async-merge sibling notification (v7.3 Phase 3 friction, applied AUD-2026-07-20-003, closes a 3-cycle-overdue deferred patch):** When all sibling EPIC PRs in a cycle are opened before any of them has merged, the engine cannot proactively rebase at PR-open time — the "first EPIC merges" precondition above hasn't happened yet. `.github/workflows/sprint_close_reminder.yml` now posts a "rebase recommended" comment on every other open sibling PR in the same cycle when one EPIC PR merges, giving a concrete signal to act on at the next `run sprint` invocation instead of waiting for a failed merge attempt.

---

## ESCALATION HANDLING SUBROUTINE (Callable)

Trigger: whenever a step produces a blocker that cannot be resolved autonomously.

Create or append to: `claude/cycles/<cycle_id>/execution_escalations.md`

Escalation entry format, SLAs, append-only rule, and Accepted Risk constraints: `claude/system/shared_standards.md` §4.
Use `ESC-EXEC-YYYYMMDD-nn` as the ID prefix (to distinguish from Release Planning escalations which use `ESC-YYYYMMDD-nn`).

**Structural append-verification (BLG-GOV-168):** Apply the Structural Append-Verification Procedure per `shared_standards.md §7.1` at every append (count before/after, confirm exactly +1, confirm no prior entry text changed — halt on either failure).

After processing escalations: update `execution_state.json.open_escalations`.

If any escalations remain `Open` with `Blocks execution: Yes`: set cycle status to `Blocked` and output the halt report per `claude/system/shared_standards.md` §5.

---

## STEP 5 — Sprint Close (All EPICs Merged)

Trigger: all EPICs in `execution_state.json.merge_gate.epics_pending` are empty (all merged).

**Branch ordering gate (LL-v5.5-EX-01 — third recurrence: v5.3/v5.4/v5.5):** Before ANY write in STEP 5 (including STEP 5.2 backlog returns and STEP 5.1 state updates), run `git branch --show-current`. If the result is NOT `main`, switch to main NOW — before writing anything. Do not write backlog.md, execution_state.json, sprint_close.md, lessons_learnt_cycle.md, or System_status_report.md while on an exec/ branch. The STEP 5.3 branch advisory exists but fires too late (after STEP 5.2 backlog writes). This gate fires first.

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

### 5.0A — pr_status Pre-Seal Sync (STRUCTURAL — AUD-2026-04-11-003 + AUD-2026-05-27-002)

Before writing `Sprint_Complete`, sync `pr_number` and `pr_status` in `execution_state.json` for every EPIC in `merge_gate.epics_merged`:

```
for each EPIC in merge_gate.epics_merged:

  # Step 1 — Recover null pr_number (AUD-2026-05-27-002)
  if EPIC.pr_number is null or 0:
    run: gh pr list --search "[EPIC-xx]" --state merged --json number,title,mergedAt
         (substitute actual EPIC identifier, e.g. "[EPIC-03]")
    if a matching PR is found:
      set execution_state.json EPIC.pr_number = <recovered number>
      log: "pr_number recovered via gh pr list search (was null)"
    else:
      set execution_state.json EPIC.pr_number = "not_found"
      log process gap in sprint_close.md: "EPIC-xx: no merged PR found at seal time"
      # do not halt — continue to Step 2

  # Step 2 — Sync pr_status (AUD-2026-04-11-003)
  if EPIC.pr_number is not null and not "not_found":
    run: gh pr view <pr_number> --json state
    if state == "MERGED": set execution_state.json EPIC.pr_status = "merged"
  else:
    set execution_state.json EPIC.pr_status = "not_created"
```

This step is idempotent — re-running does not alter already-correct values. Do not proceed to STEP 5.1 until all EPICs in `epics_merged` have `pr_status = "merged"` or `"not_created"`. This prevents misleading `"open"` or `"none"` values in sealed artefacts visible at delivery verification.

### 5.1 Acceptance Summary

For each ST item: confirm `acceptance_verified = true`. If any are false and the item is `merged`: this is a quality gap — file an escalation.

**Item-count reconciliation check (AUD-2026-08-21-004):** Before proceeding, count the total ST items declared across the full `sprint_backlog.md` (including any gated/Sprint-2 sections), using the Product Owner Sign-Off section's own "Scope confirmed" count as the authoritative total. Compare against the count of story entries actually present in `execution_state.json`. If they do not match: halt and flag Sprint Close — do not write `Sprint_Complete` until every declared item (including gated items not yet unblocked) has a corresponding `execution_state.json` entry or an explicit "not yet unblocked, gated on <ST-xx>" note.

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

Note (AUD-2026-05-27-003): `returned_to_backlog` is also a valid **in-flight** status transition for PO-authorized deferrals — it does not require waiting until sprint close. When the Product Owner authorizes a mid-sprint deferral, apply `returned_to_backlog` immediately, update the delegation log entry to `Cancelled` if applicable, and record the deferral rationale in execution_state.json notes. The sprint close record should reference the earlier in-flight deferral.

### 5.3 Sprint Close Record

> **Branch advisory (OA-2/ST-02):** Sprint close artefacts (`sprint_close.md`, `lessons_learnt_cycle.md`, `execution_state.json` seal write, `docs/System_status_report.md`) must be committed to `main`. Verify you are on `main` before writing these files. STEP 8 enforces this with a hard gate — flagging here prevents artefact rework if you discover the wrong branch after writing.

Create: `claude/cycles/<cycle_id>/sprint_close.md`

Must include:
- Sprint goal
- Items Done (with commit SHAs and spec references)
- Items Returned to Backlog (with reason)
- Items Delegated and outstanding (with delegation record IDs)
- QA evidence logs produced (list: `qa_evidence_EPIC-xx.md` per EPIC)
- Process notes (roll up `execution_state.json.process_notes`, if any — orphaned post-merge commit checks per LL-v6.8-P3-01)
- Deviations filed this sprint (list: spec file, deviation ref, priority — or "None") — **spec deviations only** (implementation diverges from what the spec requires; filed via `/dev-file`). Process notations, execution observations, and deferred items belong in `execution_state.json` notes column or `execution_escalations.md`, not this register.
  - **Deviation severity consistency check (LL-v3.3-CF-01):** Before writing this section, verify deviation priorities here match the DoQ assessment in `qa_evidence_EPIC-xx.md` sign-off blocks. If they diverge, correct one or both documents before closing. Severity must be consistent between `sprint_close.md` and the QA evidence.
  - **Backlog ID completeness check (LL-v3.3-CF-02):** Every deviation listed as "backlog item filed" must include the BLG ID in the table row. A "backlog item filed" note without a BLG ID is incomplete — query `backlog.md` for the assigned ID and record it before writing `sprint_close.md`.
- Open escalations (if any). **Backlog cross-reference check (AUD-2026-08-21-006):** for every ST item closing with an open, carried-forward escalation, confirm the escalation's originating backlog item (via its `Source:` field in `sprint_backlog.md`) already references the current `cycle_id` and the escalation ID before this record is sealed — backfill if missing.
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

**Sub-step — cycle_id section check (LL-v5.2-P4-02):** Before writing the section below, check whether `docs/System_status_report.md` already contains a `## Sprint: <cycle_id>` heading for the current cycle_id. If it does not exist: create it now using the template below. If it already exists (e.g. from a prior partial sprint close attempt): update it in-place — do not create a duplicate section. This check prevents duplicate sprint sections and ensures the SSR has a section for every cycle before the file is committed.

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

**Immediate staging (LL-v5.9-P4-01):** After writing or updating `docs/System_status_report.md`, run:
```
git add docs/System_status_report.md
```
This ensures the SSR update is staged before any branch switch. Do not wait for the STEP 8 commit block — stage it now.

**Write verification (AUD-2026-06-22-001):** Immediately after the `git add` above, confirm the new section actually exists in the file:
```
grep -c "Sprint: <cycle_id>" docs/System_status_report.md
```
If the count is 0, the write step did not execute. Re-run the SSR section write now — do not proceed to STEP 5.4 until `grep` returns ≥ 1. The `git add` instruction above can only stage a write that happened; this verification detects a silent skip.

### 5.4 Lessons Learnt

Invoke: `claude/system/lessons_learnt_prompt.md` (§3.3 — Sprint Execution Phase 3 Append)

Output path: `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (Phase 3 section append — create file if absent)

> **Header when creating (AUD-2026-05-13-002):** If creating the file, use exactly: `Owner: PMO Lead` / `Class: Operational Record (Class 3)` / `Status: Active` / `Last Updated: <date>` / `Cycle: <cycle_id>`. Do NOT use `Planning Document (Class 4)` — that class applies to QA evidence and planning artefacts, not operational records.

> **Output target (CF-02):** Output target is `lessons_learnt_cycle.md` — do **NOT** append to `lessons_learnt.md` (that is the Release Planning artefact, written by the roadmap and post-ship engines). Create `lessons_learnt_cycle.md` if absent. Writing to the wrong file silently corrupts the Release Planning artefact and prevents Phase 5 from reading the correct lessons.

The shared prompt governs the structured table block format (§4.2), idempotency guard, action rules, and completion conditions. The execution-specific friction areas to focus on:
- Delegation patterns (which classification kept needing humans — could any become autonomous?)
- GitHub integration friction (CI behaviour, issue/PR lifecycle)
- Acceptance criteria gaps (items that lacked criteria and had to be parked as `delegated_decision`)
- Governance process friction (gates that fired unexpectedly, SLA misses)

The prompt's §6.2 rule applies: if any friction can be resolved by updating a template or prompt during this run, apply it immediately and record it.

**Idempotency guard (IMP-35 gap 2 — now active):** Before appending, check for existing section header `## Phase 3 — <cycle_id>` in `lessons_learnt_cycle.md`. If present: skip append (already complete for this cycle).

**Backlog ID pre-assignment check (LL-v3.4-P3-05):** Before filing new backlog IDs in the lessons_learnt Phase 3 section, verify each proposed BLG ID is unoccupied in `claude/backlog/backlog.md`. Query existing IDs before assigning. A duplicate BLG ID causes reference conflicts at subsequent sprint planning and grooming cycles.

---

## STEP 6 — Global State Update (Hard Requirement)

> **LL-v2.1-P4-3 guard:** Before setting `status → Sprint_Complete` in `.claude_current_state.json`, confirm that STEP 7 (Seal Execution Record) will execute in the same session. Do not emit `Sprint_Complete` if `execution_state.json.sealed` is still `false`. The delivery verification preflight hard-gates on `sealed: true` — an unsealed execution record will block Phase 4.

After sprint close:

```yaml
# global state update (.claude_current_state.json):
status: Sprint_Complete
last_sync_utc: <ISO-8601 UTC now>
blocked_sla_breached: true   # only if any execution_escalations.md entry open ≥72h; else omit
release_complete: true       # only if all roadmap items for this release complete; else omit
```

If `release_complete: true`: surface to Product Owner — release ready for Phase 1 or direct Phase 1B.

---

## STEP 7 — Seal Execution Record (Hard Gate)

Once sprint close and global state update are complete:

**Pre-seal check — `completed_items` cross-EPIC union (LL-v7.10-P4-01):**
Before writing `sealed: true`, verify the top-level `completed_items` array in `execution_state.json` is the union of every `done`/`merged` story ID across **all** EPICs in `epics_merged` — not just the first-merged EPIC's items (matching the union rule in `shared_standards.md §12` Rule 2 / `CLAUDE.md §8`). If the array is missing any `done`/`merged` story from a merged EPIC, correct it now before sealing. This does not gate the seal (the per-story `epics.<EPIC-xx>.stories.<ST-xx>.status` fields remain the traceability source of truth), but an incomplete summary array must not be sealed uncorrected.

**Pre-seal check — delegation_log.md integrity (LL-v2.3-CL-02):**
Before sealing, verify `delegation_log.md` line count is consistent with delegation activity:
1. Count `delegated_items` entries in `execution_state.json`.
2. If `delegated_items` is non-empty: confirm `delegation_log.md` has substantially more than 5 lines (a header-only or near-empty file after a sprint with delegation records indicates a staging error — as occurred in v2.3 sprint close commit `a12233f`).
3. If line count is suspiciously low (fewer than 10 lines with non-empty `delegated_items`): halt, surface the discrepancy, and re-read `delegation_log.md` before proceeding. Do not seal an incomplete delegation log.

```yaml
# seal write (execution_state.json):
sealed: true
sealed_utc: <ISO-8601 UTC now>
status: Sealed
```

After seal: `execution_state.json`, `delegation_log.md`, and `execution_escalations.md` are immutable. Any correction requires a new execution cycle referencing this `cycle_id`.

---

## STEP 8 — Commit & Push Cycle Artefacts

**Branch Safety Check (Hard Gate — OA-2/ST-02):**

Run: `git branch --show-current`

If the result is NOT `main`: halt immediately. Output:

> HALT — sprint close artefacts must be committed to `main`. Current branch is `<branch_name>`. Run `git checkout main && git pull` and re-invoke `run sprint --cycle <cycle_id>` to complete STEP 8.

If the result is `main`: proceed.

**Governance file edit check (ST-12 / CF-2 → BLG-GOV-80 STRUCTURAL):** Before committing, run the following scan:

```bash
git diff --name-only HEAD | grep -E '^(claude/system/|claude/charter/|claude/agents/)' || true
git diff --name-only --cached | grep -E '^(claude/system/|claude/charter/|claude/agents/)' || true
```

For each file path returned by the above commands:
1. Check whether `claude/system/prompt_change_log.md` already contains an entry for this file at the correct version transition (the version that was just modified in this run).
2. If the entry is **missing**: append it now using the format `| date | filename | vOLD→vNEW | summary | authority |` — do not proceed to the STEP 8 commit until all missing entries are appended.
3. If the entry is **already present**: no action needed for that file.

This check is STRUCTURAL — it runs against the actual git diff, not relying on operator memory. It applies to any governance file modified during this sprint execution run, including changes made as part of ST item execution (e.g. deferred prompt patches applied mid-sprint). If `git diff` returns no governance-path files, this check passes immediately with no entries to append.

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
- All `done` ST items have `spec_references` populated — exemption: items with `spec_reference_not_applicable: true` (LL-v2.2-EX-04; structured field per STEP 3.1.A Case E, added v3.55) are exempt and must **not** be flagged as traceability gaps. Legacy records predating this field are exempt if `notes` contains "no prior spec applicable".
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

→ Apply `claude/system/shared/governance_preamble.md §Invariants` (system-wide) and `claude/system/invariants.md`. Phase-specific additions:

**Ambiguity definition:** An item is *ambiguous* when its acceptance criteria, EPIC assignment, spec reference, or delegation classification cannot be determined without an authority decision. Ambiguous items must be classified `delegated_decision` and escalated — never silently assumed or guessed. This applies in both `strict` and `standard` modes.

- **Gate evidence requirement.** Any hard gate status change in `current_roadmap.md` (marking a gate as "complete") must reference the evidence artefact that cleared it (PoG Gate ID, decision record path, or verifiable session output reference). No artefact → gate stays "pending"; record in escalations.md.
- **No scope change.** The backlog slice is sealed. The engine executes what is there.
- **No strategy boundary decisions.** The Strategy Rules owner decides; the engine surfaces and parks.
- **Delegation is explicit and tracked.** No silent assumptions about human completion.
- **Director of Quality sign-off is required on every EPIC before merge**, regardless of timeline.
- **Backend commits for delegated_frontend items must land on the EPIC branch.** Backend commits tightly coupled to a `delegated_frontend` story must be committed to that story's EPIC branch, not directly to `main`, unless the PMO Lead explicitly authorises a direct-to-main path in writing. Violation must be documented in the QA evidence log. Reference: DEV-EPIC02-ST05-02 (LL-v2.2-EX-03).

---

## 14. Playwright Test Authoring Standard

Moved to `claude/system/shared_standards.md §18` (BLG-GOV-123, v6.8 ST-16). Apply that standard whenever this routine writes or updates Playwright tests.

---

## Change Log

See: [`claude/system/changelogs/execution_prompt_changelog.md`](changelogs/execution_prompt_changelog.md)
