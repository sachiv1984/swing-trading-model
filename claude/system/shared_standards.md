**Owner:** Head of Specs Team
**Status:** Active
**Version:** 3.27
**Last Updated:** 2026-08-10

# Shared Standards — All Governed Routines

This file defines standards that apply across all five governance prompts. Each prompt references this file rather than repeating these definitions. When a prompt says "per shared_standards", read this file.

---

## 1. Governance Stack (Precedence Order)

All governed routines operate under this binding stack:

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

No routine, user instruction, or delivery pressure may override the above.

---

## 2. Hard Gate Semantics

A **hard gate** is a condition that must be satisfied before execution may continue. When a hard gate fails:

1. Stop execution immediately
2. Output the halt report (§5 below)
3. Update state to `Blocked` before halting (do not halt without writing state)
4. Wait for user — do not attempt to self-resolve

A hard gate may only be cleared by the relevant domain authority. The Facilitator may not waive a hard gate.

---

## 3. Identifier Standards

| Type | Format | Required at |
|------|--------|-------------|
| Scope items | `S2-01`, `S2-02` | Stage 2 (Release Planning) |
| Epics | `EPIC-01`, `EPIC-02` | Stage 3 (Release Planning) |
| Stories | `ST-01`, `ST-02` | Sprint Backlog |
| Tasks | `TASK-01` | Sprint Backlog (optional) |
| Risks | `RISK-01`, `RISK-02` | Stage 3 (Release Planning) |
| Escalations (Release Planning) | `ESC-YYYYMMDD-nn` | Escalations file |
| Escalations (Sprint Execution) | `ESC-EXEC-YYYYMMDD-nn` | Execution escalations file |
| Escalations (Delivery Verification) | `ESC-VERIF-YYYYMMDD-nn` | Verification escalations file |
| Escalations (Post-Ship Closure) | `ESC-CLOSE-YYYYMMDD-nn` | Closure record |
| Delegation records | `DEL-YYYYMMDD-nn` | Delegation log |

IDs must be stable — never renumber existing IDs. Missing IDs on required fields is a Process Integrity failure that halts execution.

---

## 4. Escalation Record Format

Used in:
- `claude/cycles/<cycle_id>/escalations.md` (Release Planning)
- `claude/cycles/<cycle_id>/execution_escalations.md` (Sprint Execution)
- `claude/cycles/<cycle_id>/verification_escalations.md` (Delivery Verification)
- `claude/cycles/<cycle_id>/closure_escalations.md` (Post-Ship Closure)

These files are **append-only**. Never edit a previous entry.

### Header (create on first write)

```
Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
```

### Entry format

```
## <ESC-ID>

- **Raised at:** <ISO-8601 UTC>
- **Routine:** <Roadmap Rebalance | Release Planning | Sprint Execution | Delivery Verification | Post-Ship Closure>
- **Cycle ID:** <cycle_id>
- **Step:** <step number or name>
- **ST/EPIC item:** <if applicable>
- **Trigger type:** Lifecycle | Strategy | Quality | Workforce | GitHub | Human-Delegation | Other
- **Blocking statement:** <one paragraph, precise and factual>
- **Owning authority:** <role>
- **Unblock criteria:** <what must be true to resume>
- **SLA due-by:** <date/time>
- **Blocks execution:** Yes | No
- **Disposition:** Open | Resolved | Accepted Risk | Deferred
- **Resolution summary:** <complete when closing; include evidence links>
```

### Escalation SLAs

| Trigger Type | SLA | Can Be Accepted Risk? |
|-------------|-----|-----------------------|
| Lifecycle / Process Integrity | 24 hours | **Never** |
| Strategy boundary | 72 hours | **Never** |
| Quality | Before execution | **Never** |
| Workforce / Capacity | Next planning checkpoint | Yes — Product Owner only |
| Schedule / Delivery | Next planning checkpoint | Yes — Product Owner only |

Strategy, Quality, and Lifecycle escalations may never be marked Accepted Risk. Attempting to do so is a governance violation requiring a routine halt.

### SLA Breach Rule (IMP-40)

Any escalation open for 72 hours without resolution triggers a mandatory `BLOCKED_SLA_BREACH` notice. On the next invocation after the 72-hour threshold is crossed:

- The engine writes a `BLOCKED_SLA_BREACH` notice to the active cycle escalations file (same §5 halt report format, gate name: `SLA_BREACH`).
- The engine sets `blocked_sla_breached = true` in `.claude_current_state.json`.
- The engine halts — no step may proceed until the breach is resolved by the owning authority named in the escalation record.

The 72-hour clock applies regardless of escalation trigger type (overrides the type-specific SLA in the table above). The owning authority must either resolve the escalation or formally accept risk (where permitted) before the engine may resume.

---

## 5. Standard Halt Report Format

When a hard gate fires or a blocking condition is encountered, output exactly this structure:

```
🛑 HALT — <Gate Name>

Routine:     <Roadmap Rebalance | Release Planning | Sprint Execution | Delivery Verification | Post-Ship Closure>
Cycle:       <cycle_id>
Step:        <step number>
Gate:        <gate name>

What failed:
  <specific condition that failed — one sentence per failed item>

Evidence found:
  <what was checked and what was found — be specific, not generic>

Evidence missing:
  <what would be needed to pass this gate>

State written:
  <confirm state file updated to Blocked, or explain why not>

To resume:
  <exact command to re-invoke once the condition is resolved>
  e.g.: run sprint --cycle "2026-03-02__release-v1.7"
```

Do not halt with a terse message. Always output the full halt report so the user knows exactly what is needed.

---

## 6. GitHub CLI Commands (Standard Operations)

Use `gh` CLI for all GitHub operations. Do not use the GitHub API directly.

### Issue operations

```bash
# Create issue (body content per claude/system/gh_issue_template.md)
gh issue create \
  --title "[ST-xx] <title>" \
  --body "<populated gh_issue_template.md>" \
  --label "sprint" --label "EPIC-xx"

# Update issue to in-progress
gh issue edit <number> --add-label "in-progress"

# View issue (to check if it exists)
gh issue list --search "[ST-xx]" --json number,title,state
```

**Issue body format:** Use `claude/system/gh_issue_template.md` as the body template. Variable mapping:
- `{{ID}}` → EPIC-xx (the parent epic)
- `{{ST_ID}}` → ST-xx (the story)
- `{{TITLE}}` → story title from `sprint_backlog.md`
- `{{CYCLE_ID}}` → active cycle_id from `.claude_current_state.json`
- `{{PARENT_EPIC}}` → EPIC-xx
- `{{OBJECTIVE_TEXT}}`, `{{AC_1}}` etc. → from acceptance criteria in `sprint_backlog.md`

**Do not manually close issues** that will be closed by `governance_sync.yml` on push. Issues are auto-closed by CI when a commit with `[EPIC-xx][ST-xx]` format is pushed to an `exec/**` branch.

**Delegation-record commits do not auto-close (ST-18, EPIC-03, v8.2, BLG-GOV-285):** A commit that only records a delegation (e.g. a `delegation_log.md` update) still carries the mandatory `[EPIC-xx][ST-xx]` tag per the commit-format rule, but is not a completion commit. `governance_sync.yml` cross-checks the story's actual status in `execution_state` (per-EPIC files per §12.1, or the legacy single `execution_state.json` for older cycles) before closing — an issue is only auto-closed when the story's recorded status is `done` or `merged`. If the story's status cannot be determined (no `execution_state` found for the active cycle — e.g. a commit unrelated to sprint execution, or a cycle predating this check), the workflow falls back to closing unconditionally, preserving prior behaviour. This closes a false-positive that recurred twice before the fix (`v8.0` EPIC-02/ST-08, issue #1148; `v8.1` EPIC-02/ST-02, issue #1169 — both required a manual reopen). No new commit-message marker convention was introduced — the fix reads ground truth from `execution_state` rather than relying on commit authors to remember a new tag.

### PR operations

```bash
# Create PR
gh pr create \
  --title "[EPIC-xx] <epic description>" \
  --body "<body per prompt spec>" \
  --base main \
  --head exec/<cycle_id>/EPIC-xx

# Check PR status
gh pr view <number> --json state,reviews,statusCheckRollup

# List open PRs for this cycle
gh pr list --search "exec/<cycle_id>" --json number,title,state
```

### Branch operations

```bash
# Create EPIC branch from main
git checkout main && git pull
git checkout -b exec/<cycle_id>/EPIC-xx
git push -u origin exec/<cycle_id>/EPIC-xx

# Check if branch exists remotely
git ls-remote --heads origin exec/<cycle_id>/EPIC-xx
```

### 6.1 CI Failure Diagnosis and Workflow-Authoring Guidance (lessons-learnt deferred patches, `2026-08-05__release-v8.3` Phase 3 friction items 3–4, resolved 2026-08-07)

**Infra-outage vs real-failure classification:** Before treating a red CI check as a code regression, run `python3 scripts/check_ci_infra_outage.py --run <run-id>` (or `--pr <pr-number>` to list runs first). It scans job logs for known GitHub-side infrastructure-failure signature strings (`"Failed to resolve action download info"`, `"Error: Service Unavailable"` at the action-setup phase, and cancelled-with-no-`startedAt` queue-timeout patterns) and reports a classification per job — `infra_outage`, `real_failure_candidate`, or `inconclusive`. It also detects the "stuck rerun" symptom: `gh run rerun` returning `"workflow file may be broken"` while the run itself is still `queued`/`in_progress` is an outage symptom, not a real workflow-syntax problem — do not edit the workflow file in response to that message alone. This is a read-only diagnostic; it never retries or reruns anything itself. Extend `INFRA_SIGNATURES` in the script only when a new pattern is confirmed against a real, `githubstatus.com`-documented incident — do not add speculative signatures.

**Safe retry when a rerun attempt is stuck:** If `gh run rerun` on an already-attempted run reports the stuck-rerun symptom above, do not keep retrying the same run. Push an empty retrigger commit on the affected branch (`git commit --allow-empty -m "[EPIC-xx] Retrigger CI after GitHub Actions outage"`) to obtain a clean run on a fresh SHA instead of continuing to fight the stuck run-side state.

**`pipefail`/`tee` exit-code capture:** GitHub Actions `run:` steps default to `bash -e {0}` (errexit only) unless `shell: bash` is explicitly declared on the step or job — this silently defeats the common `cmd | tee output.log; echo $?` pattern for capturing a piped command's real exit code, since without `pipefail` the pipeline's exit status is that of the *last* command (`tee`, which almost always succeeds) rather than `cmd`. Any new workflow step that pipes a command through `tee`, `grep`, or similar for log capture while still needing the original command's exit code must either: (a) declare `shell: bash` on the step so `set -o pipefail` conventions apply consistently, or (b) capture the exit code explicitly via `${PIPESTATUS[0]}` (bash) immediately after the pipeline, not via a bare trailing `echo $?`. Check this whenever authoring or reviewing a new `.github/workflows/*.yml` step that pipes command output.

---

## 7. Append-Only File Rule

The following files are append-only within their cycle. Never edit a previous entry:

- `claude/cycles/<cycle_id>/escalations.md`
- `claude/cycles/<cycle_id>/execution_escalations.md`
- `claude/cycles/<cycle_id>/verification_escalations.md`
- `claude/cycles/<cycle_id>/delegation_log.md`
- `claude/roadmap/decision_log.md`

If a correction is needed to a previous entry, append a correction note referencing the original entry ID. Do not overwrite.

### 7.1 Structural Append-Verification Procedure (canonical, reusable — BLG-GOV-168)

`claude/roadmap/decision_log.md` has a confirmed structural guard (`roadmap_prompt.md` STEP 9). The procedure below generalises that guard into a single reusable block. Every engine that appends to one of the four files in the table must apply this exact procedure at its write step — do not restate or paraphrase it inline; reference this section.

**Procedure:**
1. **Before write:** count existing entries in the target file (count occurrences of the file's entry-header pattern, e.g. via `grep -c '^## ESC-EXEC-'`).
2. **Perform the append.**
3. **After write:** re-count entries using the same pattern.
4. **Verify:**
   - New count = old count + 1 exactly (not zero — a silent no-op; not more than one — an unintended double-append).
   - No existing entry's text changed (diff the file's pre-write content against post-write, excluding the newly appended entry — confirm every prior line is byte-identical).
5. **If either check fails:** halt. Do not proceed past a failed structural verification. Report which check failed (count mismatch vs. altered prior entry) in the halt report.

**Applies to:**

| File | Entry header pattern | Owning engine |
|------|----------------------|----------------|
| `claude/cycles/<cycle_id>/escalations.md` | `^## ESC-` | `release_planning_prompt.md` |
| `claude/cycles/<cycle_id>/execution_escalations.md` | `^## ESC-EXEC-` | `execution_prompt.md` |
| `claude/cycles/<cycle_id>/verification_escalations.md` | `^## ESC-VERIF-` | `delivery_verification_prompt.md` |
| `claude/cycles/<cycle_id>/delegation_log.md` | `^## DEL-` | `execution_prompt.md` |
| `claude/roadmap/decision_log.md` | `^## DEC-` (or equivalent decision entry marker) | `roadmap_prompt.md` (existing guard — reference model for this procedure) |

Each owning engine's write step for its file(s) above must state: "Apply the Structural Append-Verification Procedure per `shared_standards.md §7.1`" at the point of append — not a re-description of the steps.

---

## 8. Resumability Protocol

Every governed routine is resumable. On every invocation:

1. **First action:** Read the relevant state file (`state.json`, `execution_state.json`, or `.claude_current_state.json` for post-ship)
2. If the file exists and status is not `not_started` or `Initialized`: you are resuming
3. Skip all completed steps (any step whose output artefact exists and is valid)
4. Re-evaluate all `blocked_*` items: check whether their unblock criteria are now met
5. Resume from the first incomplete or newly unblocked item
6. Never re-execute a step that already produced a valid output

If the state file does not exist: this is a fresh run. Proceed from STEP -1.

**Post-Ship Closure resumability:** The closure engine maintains `claude/cycles/<cycle_id>/closure_state.json`. On re-invocation, STEP 0 reads this file: if `status = Closed`, the cycle is already closed (halt); if `status = In_Progress`, resume from the first step with value `not_started` or `fail`; if the file does not exist, this is a fresh run. This follows the same resumability model as the execution and release planning engines.

---

## 9. Lifecycle Compliance Quick Reference

Every governed artefact must have a complete header. Minimum required fields by class:

| Class | Required Fields |
|-------|----------------|
| Class 1 (Canonical) | Owner, Status: Canonical, Version, Last Updated |
| Class 3 (Operational Record) | Owner, Status: Operational Record, Report Date, Filed |
| Class 4 (Planning Document) | Owner, Class: Planning Document (Class 4), Status, Last Updated |
| Class 6 (Governance Prompt) | Owner, Status: Active, Version, Last Updated |

A document without a complete header is non-compliant and must not be relied upon. Non-compliant documents discovered during a routine: apply header remediation (headers only) and continue.

**§9.1 Version/state header cross-check (meta-review pattern, `2026-07-10__scheduled` — Type A Governance Drift recurring 3+ times across 2 cycles: `scored_initiatives.md` unbounded accumulation, `OPERATIONAL_GUIDE.md` header lagging its own Change Log table on 4 occasions, a backlog gate-field-label synonym silently excluded from an automated scan; recurred a further time at AUD-2026-07-14 despite this note, root-caused to the note covering the Change Log top row but not the §14 field-table's own summary row):** Before any edit that bumps a document's own `**Version:**`/`**Last Updated:**` header field, or before any step that is documented as "overwrite" rather than "append," apply this checklist:
1. Read the document's Change Log table's top row (or full existing body) — confirm the header field is not already ahead of, or behind, what the edit assumes.
2. If the document carries its own internal self-referential summary table (e.g. `OPERATIONAL_GUIDE.md` §14's `Version` / `Last Updated` field rows) **distinct from the Change Log**, read and update that table's own `Version`/`Last Updated` row explicitly — do not assume updating the Change Log or the top header alone also updates this row; it is a separate write.
3. Do not trust a header field, a Change Log row, or an instruction's label ("overwritten each run") in isolation — cross-check all three locations (header, self-referential summary row if one exists, Change Log top row) against each other before writing, and correct any that disagree.

**Mechanical enforcement note (added v3.18, AUD-2026-07-20-001 — 3rd recurrence of this exact pattern despite the v3.10 and v3.16 prose strengthenings above):** This checklist has now failed under real load twice since it was written (`OPERATIONAL_GUIDE.md` §14's self-row drifted 3 versions behind between the v3.16 fix and AUD-2026-07-20). Any governance commit that bumps `OPERATIONAL_GUIDE.md`'s header `**Version:**` must additionally pass a mechanical check — via the repo's `commit-check` skill — comparing that value against the §14 field-table's own `| Version | X |` row before the commit lands. Do not rely on this checklist alone a fourth time.

---

## 10. Lifecycle Validation Rules (Lifecycle Guard)

All engines that write `.claude_current_state.json` status must apply this guard on every invocation, before executing any step.

### 10.1 Allowed Entry States

| Engine | Command | Valid from-states | Additional preconditions |
|--------|---------|-------------------|--------------------------|
| Release Planning | `plan release` | `Closed` | `post_ship_complete = true` **and** `next_cycle_unblocked = true` must be present in `.claude_current_state.json` (checked at STEP -1.6) |
| Design Gate | `run design-gate` | `Release_Planning_Complete` | — |
| Sprint Planning | `plan sprint` | `Release_Planning_Complete` (design N/A), `Design_Gate_Passed` | When entering from `Release_Planning_Complete`: `design_gate_bypass_authority` + `design_gate_bypass_reason` required in state (STEP -1.3) |
| Sprint Execution | `run sprint` | `Sprint_Planning_Complete`, `Executing` (resume), `Closed` (multi-sprint only: `sprint_planning.sprint2_deferred` non-empty AND `sprint_sealed = true` AND `post_ship_complete = true`) | Multi-sprint exception: `Closed` is valid only when the same `cycle_id` is being continued across sprints (Sprint N closed, Sprint N+1 resuming). See `lifecycle_schema.json` for full entry condition. |
| Delivery Verification | `run delivery verification` | `Sprint_Complete` | — |
| Post-Ship Closure | `run post-ship` | `Verified`, `Verified_with_deviations` | — |
| Amendment Cycle | `amend cycle` | `Sprint_Planning_Complete` (before sprint_sealed = true) | Acquire backlog lock before reading `sprint_sealed` (STEP -1.1) |

### 10.2 Guard Algorithm

On engine invocation:

1. Read `.claude_current_state.json` → record `current_status`
2. Check `current_status` against the engine's valid from-states (table above)
3. **If `current_status = Blocked`:** read `prior_status`. If `prior_status` is a valid from-state for this engine, proceed as if status = `prior_status`. Otherwise, halt — the block is in the wrong phase for this engine.
4. **If `current_status` is not in valid from-states and is not `Blocked`:** halt immediately with a Lifecycle hard gate (§2 + §5 format). Write `status = Blocked` and `prior_status = <current_status>` to `.claude_current_state.json` before emitting the halt report.
5. **If valid:** continue to engine steps.

### 10.3 State Write Rules

- An engine may only write a state value that is in its allowed `to` transitions (see `lifecycle_schema.json`).
- Write `status` only at the defined completion signal step. Do not set an in-progress state at an earlier step unless the transition explicitly defines an intermediate state (e.g., `Executing` is a valid in-progress write for Sprint Execution).
- Before writing `status`, confirm the value in `.claude_current_state.json` has not changed since step 1. If it has changed (concurrent write), halt with `ESC-YYYYMMDD-nn` (Lifecycle trigger) without overwriting.

### 10.4 Blocked State Protocol

When any hard gate fires during execution:

1. Set `prior_status` = current `status` value in `.claude_current_state.json`
2. Set `status` = `Blocked`
3. Write `.claude_current_state.json` — this write must complete before the halt report is emitted
4. Emit halt report (§5 format); include "State written: status = Blocked, prior_status = <value>"
5. Wait for user — do not self-resolve

To clear `Blocked`: the domain authority identified in the escalation record must resolve the block. On resolution, restore `status` from `prior_status` and clear `prior_status` to `null`.

### 10.5 Phase Skip Rule

Forward-only movement is enforced by the entry state check (§10.2). An engine that cannot pass the entry check must not execute, regardless of delivery pressure. No timeline instruction or user override may waive a Lifecycle hard gate.

### 10.6 Full State Machine Reference

`claude/system/lifecycle_schema.json` is the **machine-readable source of truth** for all valid states and transitions. The table in §10.1 is a human-readable summary; in any conflict, `lifecycle_schema.json` prevails. Every engine must read `lifecycle_schema.json` to validate transitions rather than relying solely on the §10.1 table. The schema includes: all valid states, all transitions with entry conditions and completion signals, and concurrent-write prevention rules.

---

## 11. Prompt Version Control (IMP-10)

Any increment to a governance prompt version **must** be accompanied by an entry in `claude/system/prompt_change_log.md` in the same commit.

**Rule:** A prompt whose version number is not recorded in `prompt_change_log.md` is considered non-compliant. During Release Planning STEP -1 (advisory check), the engine verifies that each governed prompt's current version appears in the change log.

**Scope:** Applies to all Class 6 Governance Prompts in `claude/system/`:

- `release_planning_prompt.md`
- `sprint_planning_prompt.md`
- `execution_prompt.md`
- `delivery_verification_prompt.md`
- `post_ship_closure.md`
- `design_gate_prompt.md`
- `amendment_cycle_prompt.md`
- `roadmap_management_prompt.md`
- `backlog_management_prompt.md`
- `roadmap_prompt.md`
- `gh_issue_template.md` (Owner: Head of Specs Team, Class: 6)

**Simultaneity rule:** A `prompt_change_log.md` entry must be created in the **same commit** as the prompt version increment it records. An entry created after the fact (in a separate commit) is non-compliant. When applying prompt patches, stage both the modified prompt file and the updated `prompt_change_log.md` in the same `git add` + `git commit` sequence.

**Enforcement:** STEP -1 of Release Planning (advisory, not hard gate) verifies the current version of each prompt appears in `prompt_change_log.md`. Missing entries are flagged as advisory warnings; the release planning engine may proceed but must record the gap as an outstanding action.

**Companion per-file changelog rule (v3.17, `2026-07-17__scheduled` Friction Item 1):** Each Class 6 prompt's standalone `claude/system/changelogs/<prompt>_changelog.md` file exists to hold "full history" for that prompt (per each such file's own stated purpose) and must be updated in the **same commit** as any version bump, alongside `prompt_change_log.md`. It is not a substitute for `prompt_change_log.md` (the canonical, cross-prompt log) but a derived per-file view — both must stay in sync. Found this cycle: `roadmap_prompt.md` had advanced to v9.1 with correct `prompt_change_log.md` and `OPERATIONAL_GUIDE.md` §14 entries, but `changelogs/roadmap_prompt_changelog.md` had fallen 3 versions behind (missing 8.9, 9.0, 9.1) because no rule named it as a required companion write. Engines applying an action-now prompt patch must update both files in the same commit going forward.

### 11.1 STEP -1.7-Class Prompt Change Log Gap Detection (date-scan method, v3.24, BLG-GOV-257)

Any STEP-numbered check across the governance prompts that needs to find "the most recently logged transition for file X" in `prompt_change_log.md` (the pattern used at Sprint Planning STEP -1.7 and equivalent hygiene advisories elsewhere) **must** use the date-scan method below, not a file-position shortcut.

**Why file position is unsafe:** `prompt_change_log.md` is not uniformly ordered. A contiguous block was written prepended-newest-first (per the v3.9→v3.10 `sprint_planning_prompt.md` fix), but it sits above an older historical backfill written in ascending chronological order that runs to the end of the file. A filename's true latest row can therefore be either the first `grep` match or one further down the file — `grep "<filename>" | head -1` silently returns a stale row whenever the true latest entry landed in the older, ascending-ordered tail. This produced a confirmed false-positive "prompt change log gap" advisory for `sprint_planning_prompt.md` during `plan sprint 2026-07-24__release-v7.8` (current v3.13; the check reported last-logged v3.12 when v3.13 was in fact already logged further down the file, at what was then line 572).

**Method:**
1. `grep "<filename>" claude/system/prompt_change_log.md` — collect **every** matching row, not just the first.
2. Parse the `Date` column (leftmost, `YYYY-MM-DD`) of each matched row.
3. Select the row with the **latest date**. If two or more rows share the same latest date, take the one with the highest `vOLD→vNEW` target version (the version after `→`).
4. Extract that row's target version and compare against the prompt's current `**Version:**` header per the calling check's own gap-reporting logic.

Do not use `head -1`, `tail`, or any other file-position-based selection — position does not correlate with recency across the whole file, only within the single prepend-ordered block at the top.

**Consumers of this method:** `sprint_planning_prompt.md` STEP -1.7 (Hygiene advisories — Prompt change log gaps). Any future STEP that performs an equivalent "most recent logged transition" lookup must cite this section rather than re-deriving its own file-position-based logic.

---

---

## 12. Parallel EPIC Branch Merge Sequencing

When multiple EPIC branches are active simultaneously in the same sprint, per-EPIC state writes must not collide. Apply the following convention.

**Rule 1 — Merge sequence:** When multiple EPIC branches are ready for merge, merge them in dependency order (logical dependencies first; alphabetical by EPIC ID if no dependencies exist). Do not merge multiple EPIC branches to main simultaneously.

**Rule 2 — Retired (ST-19, BLG-GOV-284, cycle `2026-08-03__release-v8.1`):** The prior hand-merge conflict-resolution rule ("on a merge conflict in `execution_state.json`, keep the version from the more recently-merged EPIC branch") is retired. It is structurally obsolete under the per-EPIC mechanism below — there is no longer a shared file for two branches to conflict on. Superseded by **§12.1 Per-EPIC Execution State Mechanism**.

**Rule 3 — GOVERNANCE commit after each merge:** After each EPIC branch merges to main, regenerate `execution_state.json` on main via `python3 claude/system/scripts/generate_execution_summary.py <cycle_id>` and commit the result directly as a GOVERNANCE commit, before the next EPIC branch opens a PR. This prevents the next EPIC's PR from showing a conflict on `execution_state.json` at open time — the file is regenerated fresh each time rather than hand-reconciled, so there is nothing to merge-conflict over.

**Why this matters:** Without this convention, a 4-EPIC sprint with parallel branches requires several conflict resolution rounds, each triggering a CI re-run (~3–5 minutes each). Cumulative latency: 30–60 minutes per sprint close. With this convention, conflict rounds are eliminated.

*Trigger: Friction Item 1, lessons_learnt_execution.md — cycle 2026-03-06__release-v1.9 Sprint 1. Confirmed by Head of Specs Team.*

### 12.1 Per-EPIC Execution State Mechanism (added ST-19, BLG-GOV-284, cycle `2026-08-03__release-v8.1`)

Each EPIC branch owns exactly one file, `claude/cycles/<cycle_id>/execution_state/EPIC-xx.json`, and writes only to it — never to any other EPIC's file, and never directly to the cycle-level `execution_state.json`. Schema: `claude/system/schemas/execution_state_epic_schema.json`. Cycle-level fields (`sprint_goal`, `backlog_slice_source`, `invoked_utc`, `mode`, `open_escalations`, `process_notes`, `sealed`, `sealed_utc`) live in `claude/cycles/<cycle_id>/execution_state/_cycle_meta.json`, owned by whichever EPIC is designated the structural-transition owner for that sprint (or the first EPIC to open, absent a designation).

`claude/cycles/<cycle_id>/execution_state.json` is a **computed, regenerate-on-read summary** — never hand-edited, never hand-merged. It is produced by `claude/system/scripts/generate_execution_summary.py <cycle_id>`, which reads `_cycle_meta.json` plus every `EPIC-*.json` present and unions them into the same shape the legacy shared file used, so Delivery Verification and Post-Ship Closure continue reading it unchanged. Regenerate it (Rule 3) after every EPIC merge. A git conflict on the generated file is resolved by re-running the generator on the merged `main`, not by manual reconciliation — the file has no independent authority of its own to merge.

**Adoption note:** A sprint may run a mixed transition — EPICs already executing under the legacy shared-file mechanism when this mechanism lands may complete under it; EPICs opening afterward adopt the per-EPIC mechanism. See the sprint's own `sprint_planning_notes.md §Multi-EPIC Execution Notes` for the designated cutover point, if any.

---

## 13. Dry-Run Standard

The following engines support `--dry-run`. The guarantee is identical in all cases:

**Dry-run guarantee:** No writes to any file. No state updates to `.claude_current_state.json`. No git commits. No GitHub operations (issues, PRs, branch creation). The output is a plan or preview only.

| Engine | `--dry-run` produces |
|--------|---------------------|
| `plan sprint` | Sprint planning preview — capacity, scope, AC gaps, sequencing, pip-audit result |
| `run sprint` | Dry-run execution report — item classification, delegation targets, spec references, anticipated blockers |
| `run post-ship` | Closure plan — every step listed, every write that would be made, every flag. Note: STEP 11 (`manage roadmap`) and STEP 12 (`groom backlog`) also pass through `--dry-run`. |
| `manage roadmap` | Change plan — items to retire, items to flag |
| `groom backlog` | Change plan — items to archive, items to flag |
| `run design-gate` | Design gate preview — classification table, gap list, required design artefacts; no gate record, no state write, no commit |
| `run roadmap` | Rebalance preview — capacity analysis, displacement candidates, scoring matrix, backlog impact |
| `run ideas` | Submission window summary — counts per agent, ideas available for STEP 4 |
| `run ideas housekeeping` | Housekeeping preview — terminal rows to archive, rejected-but-strong revival candidates, pipeline health advisory; no ideas_register.md writes, no archive writes |
| `plan release --dry-run` | Scope extraction preview — roadmap item, tentative EPIC/ST structure, artefacts that would be created (release_plan.md, backlog_slice, design_gate.md if required); no artefact writes, no state updates |
| `run delivery verification --dry-run` | Verification plan — list of all STEP checks with their precondition sources; no verification_report.md written, no .claude_current_state.json update |
| `amend cycle --dry-run` | Amendment preview — proposed backlog slice delta, scope changes, authority ratification requirements; no state.json writes, no slice artefact created |
| `run audit` | N/A — `claude/audit.py` is read-only by design (produces a report + a PATCH manifest for Claude Code to apply separately); no `--dry-run` flag needed, no writes occur during the audit run itself |

**Scope of read operations:** Read operations (file reads, git queries, pip-audit scans) are always permitted in dry-run mode. A dry-run that cannot read required inputs should halt with a standard halt report, not silently produce an empty plan.

**Re-invocation after dry-run:** A dry-run does not advance lifecycle state. After reviewing the dry-run output, re-invoke without `--dry-run` to execute.

---

## 14. Preflight Field Scope (IMP-22)

To reduce repeated full-file reads of `.claude_current_state.json` across consecutive engine preflights, each engine must read only the field set listed below at preflight (STEP -1 / STEP 0), unless a specific later step explicitly requires an unlisted field.

**Section-scoped read rule:** "Engines must read only the fields specified in their `shared_preflight_fields` entry from `.claude_current_state.json`, not the full file, unless a field outside the set is explicitly required by a named step."

| Engine | Minimum preflight fields |
|--------|--------------------------|
| Release Planning (`plan release`) | `status`, `active_cycle`, `prior_cycle`, `post_ship_complete`, `next_cycle_unblocked` |
| Design Gate (`run design-gate`) | `status`, `active_cycle`, `design_gate_required` |
| Sprint Planning (`plan sprint`) | `status`, `active_cycle`, `design_gate_status`, `design_gate_bypass_authority`, `design_gate_bypass_reason`, `sprint_sealed` |
| Sprint Execution (`run sprint`) | `status`, `active_cycle`, `amended_backlog_slice_path`, `sprint_sealed`, `sprint_planning` |
| Delivery Verification (`run delivery verification`) | `status`, `active_cycle`, `amended_backlog_slice_path` |
| Post-Ship Closure (`run post-ship`) | `status`, `active_cycle`, `verification_status`, `next_cycle_unblocked` |
| Amendment Cycle (`amend cycle`) | `status`, `active_cycle`, `sprint_sealed` |
| Roadmap Rebalance (`run roadmap`) | `status`, `active_cycle` |

Fields not in this list may be read when a specific named step requires them. Full-file reads remain acceptable for engines with fewer than three tool calls budgeted for state loading.

---

## 15. Spec Debt Item Lifecycle (IMP-43)

**Spec debt items** (identified by prefix `BLG-SPEC-*`) represent deviations between what was built and the canonical spec, where the spec itself must be updated to reflect the agreed authoritative requirement.

### 15.1 Creation trigger

A spec debt item is created when:
- A deviation is noted during Phase 3 execution (STEP 5.3 in `execution_prompt.md`) or Phase 4 verification (STEP 3) AND
- The resolution requires a spec update (not just a backlog implementation item)

### 15.2 Required fields

Each `BLG-SPEC-*` entry in `backlog.md` must contain:

| Field | Description |
|-------|-------------|
| `BLG-SPEC-*` ID | Stable, unique, never renumbered |
| Affected spec file | Full path to the spec file that must be updated |
| Section | The specific section or table within the spec |
| Deviation description | What the implementation does vs. what the spec says |
| Canonical requirement | The authoritative requirement as it should read after correction |
| Priority | P0–P3 (same scale as deviation register) |
| Owner | Role responsible for the spec update |
| Target release | Release in which the spec update is expected |

### 15.3 Acceptance criteria for closure

A `BLG-SPEC-*` item is closed when:
1. The affected spec file has been updated to reflect the canonical requirement
2. The update has been reviewed by the Head of Specs Team
3. The Head of Specs Team has recorded sign-off (inline comment or PR review)

### 15.4 Closing authority

**Head of Specs Team sign-off is required** to mark a `BLG-SPEC-*` item as complete. No other role may close a spec debt item.

### 15.5 Validation rule (Phase 1M — Backlog Management)

The Backlog Management Engine (`groom backlog`) validates spec debt items against their `spec_update_status`:
- `open`: spec file not yet updated — item remains in backlog
- `in_progress`: spec file update in a live PR — flag for tracking
- `review_pending`: update merged but Head of Specs Team sign-off not yet recorded — flag
- `closed`: Head of Specs Team sign-off confirmed — mark item complete and archive

---

## 16. Governed JSON Schemas

Inline JSON schemas in engine prompts must be replaced with a reference to this section.
Format for reference: "Schema: per `shared_standards.md §16.N`"

### 16.1 sprint_backlog_index.json

Produced by: `sprint_planning_prompt.md` STEP 6.1A
Consumed by: `execution_prompt.md` STEP -1.1

```json
{
  "cycle_id": "<cycle_id>",
  "generated_utc": "<ISO-8601 UTC>",
  "epics": {
    "EPIC-xx": {
      "st_items": ["ST-xx", "ST-yy"],
      "backlog_slice_refs": ["stage4_backlog_slice.md#ST-xx", "stage4_backlog_slice.md#ST-yy"]
    }
  }
}
```

### 16.2 stage4_issue_manifest.json

Produced by: `release_planning_prompt.md` STEP 4 (IMP-24)
Consumed by: `sync gh` inline handler

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

One entry per ST item in `stage4_backlog_slice.md`. The `cycle:<cycle_id>` label is the idempotency key for GitHub issue creation (CLAUDE.md §4 / `sync gh` handler).

### 16.3 Delegation Log Schema

Produced by: `execution_prompt.md` — append on every delegated item
Consumed by: `execution_prompt.md` STEP 5.0 (outcome check), `post_ship_closure.md`

**Header (create on first write):**

```
Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
```

**Delegation Record Format** (`DEL-<YYYYMMDD>-<nn>`):

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

**Compliance rules:**
- "What is needed" must be specific enough that the assignee can act without further clarification. Vague delegations are non-compliant.
- For `delegated_backend`: "What is needed" must reference the specific layer(s) required (router / service / database) and the canonical spec section.
- For `delegated_frontend`: the Base44 prompt draft field is mandatory, covering all six required sections (context, change, API contract, behaviour rules, non-functional rules, expected outcome).

### 16.4 SLA Breach Tracking (Execution Engine)

On each re-invocation of the execution engine, check all open escalation timestamps against the current time. If any escalation has been open for **72 hours or more** without resolution, the SLA Breach Rule in `shared_standards.md §4` applies:

1. Write `BLOCKED_SLA_BREACH` notice to `execution_escalations.md` (same §5 halt report format, gate name: `SLA_BREACH`).
2. Set `blocked_sla_breached = true` in `.claude_current_state.json`.
3. Halt — no step may proceed until the breach is resolved by the owning authority.

Reference: `execution_prompt.md` STEP 3.1.D (delegated_decision items) and STEP 5.1 (Sprint_Complete state write).

### 16.5 ideas_register.md Schema

**File:** `claude/ideas/ideas_register.md`
**Produced by:** `idea_intake_prompt.md` STEP 2 (append row) and STEP 4 (update row status)
**Consumed by:** `roadmap_prompt.md` STEP 4 (idea classification and document management)

**File header (create on first write):**

```markdown
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** <date>
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# Ideas Register
```

**Register table (append new rows; update existing rows in-place):**

| Idea ID | Title | Submitter | Window | Submitted At | Status | Park Count | Park Rationale | Step 4 | Step 5 |
|---------|-------|-----------|--------|--------------|--------|------------|----------------|--------|--------|

**Column definitions:**

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| Idea ID | string | Yes | Unique identifier: `IDEA-<agent-slug>-<YYYYMMDD>-<nn>` |
| Title | string | Yes | Short idea title |
| Submitter | string | Yes | Full role name of submitting agent |
| Window | string | Yes | Window ID (e.g. `IW-20260304-01`) |
| Submitted At | date | Yes | ISO date (YYYY-MM-DD) |
| Status | enum | Yes | One of: `Submitted`, `Advancing`, `Parked-cycle-<n>`, `Rejected`, `Promoted-Added`, `Promoted-Backlog`, `Promoted-Rejected`, `Withdrawn`. **`Promoted-Added` also covers a STEP 5 debate that resolves into a governance/prompt process patch rather than a roadmap/backlog addition** (e.g. `IDEA-challenger-20260702-01` at `2026-07-06__scheduled`, `IDEA-pmo-lead-20260708-02` at `2026-07-08__scheduled`) — use `Promoted-Added` with the Step 5 column noting "resolved as process patch, not a roadmap/backlog item." (Clarified v3.10 — this reuse had occurred twice without being documented, a Type B friction item.) **`Promoted-Backlog`** is a distinct terminal status, set by `roadmap_prompt.md`'s STEP 5/9 disposition table for the `📋 Backlog (gate-conditional)` Step 4 outcome — idea lifecycle complete, tracked as a gate-conditional backlog item from here, without having passed through `Advancing`/STEP 5 debate. It is functionally terminal in the same sense as `Promoted-Added` (idea → tracked backlog item) but distinguishes "advanced directly" from "sent to backlog pending a gate condition." (Formalised v3.11 — added retroactively; the status had been in continuous use by `roadmap_prompt.md` for many cycles but was never added to this enum, which `ideas_housekeeping_prompt.md §6` and this table both need to classify it correctly. Root cause: `claude/cycles/2026-07-08__release-v6.8/lessons_learnt_closure.md` Advisory Summary.) |
| Park Count | integer | Conditional | Number of consecutive cycles parked; required when Status = `Parked-cycle-<n>`; `—` otherwise |
| Park Rationale | string | Conditional | PO one-line rationale; required on every park action; `—` if never parked |
| Step 4 | string | Conditional | Product Owner classification from most recent roadmap run; `—` if no roadmap run yet |
| Step 5 | string | Conditional | Debate outcome from most recent roadmap run; `—` if not advanced to debate |

**Compliance rules:**
- Rows are append-only for new ideas; never deleted
- Status field is the only column updated after initial row creation (except Park Count, Park Rationale, Step 4, Step 5 — updated on each roadmap run)
- A park action without a written Park Rationale is treated as Reject-not-strong by the roadmap engine
- `Status: Parked-cycle-<n>` where n ≥ 3 triggers stale idea surfacing in roadmap STEP 4.5

---

## §16.6 Backlog Item Provisional-Target Field

**Used by:** Roadmap Engine (write at STEP 9), Release Planning Engine (read at STEP 1.2)

### Field syntax

```
**Provisional-Target:** v<X.Y> | TBD | Unscheduled
```

### Horizon-to-release mapping rules

| Roadmap horizon | Provisional-Target value |
|-----------------|--------------------------|
| `Now` | Next planned release label in `current_roadmap.md` Now horizon (e.g. `v2.3`) |
| `Next` | Release label in the Next horizon of `current_roadmap.md` (e.g. `v2.4`) |
| `Later` | `Unscheduled` |
| Horizon tier has no release label | `TBD` |
| Horizon structure absent from roadmap | `TBD` |

**Rules:**
- The field must be present on every newly promoted item written to `backlog.md` at STEP 9.
- `TBD` is the explicit fallback when no release label can be resolved — the field is **never blank**.
- The field is a signal, not a commitment. Release planning may include or exclude items regardless of `Provisional-Target` value; deviation requires explicit PO rationale.

---

## §16.7 scored_initiatives.md Effort Band Column and Handoff Contract

**Used by:** Roadmap Engine (write at STEP 9), Release Planning Engine (read at STEP 0 / STEP 4.5)

### Effort band column

`claude/scoring/scored_initiatives.md` must carry an `Effort Band` column for all active roadmap initiatives:

| Initiative | Strat | Fin | Risk | WF | TTV | Rev | SPS | Effort Band |
|---|---|---|---|---|---|---|---|---|
| Initiative name | ... | ... | ... | ... | ... | ... | ... | S \| M \| L \| XS |

Effort band is assigned by the Roadmap Engine at promotion time.

### Three-tier resolution rule for STEP 4.5

| Tier | Condition | Action |
|------|-----------|--------|
| 1 | Row present in `scored_initiatives.md` AND `Effort Band` value present | Use effort band as primary sizing input; note "from scored_initiatives.md" |
| 2 | Row present BUT `Effort Band` cell empty or absent | Use STEP 4 estimate; emit advisory: "⚠ [N] EPIC(s) have no effort band in scored_initiatives.md — falling back to inline estimate." |
| 3 | No matching row in `scored_initiatives.md` | Use STEP 4 estimate; no advisory required |

### Handoff contract

- The Roadmap Engine writes; the Release Planning Engine reads. No other engine writes to this field.
- The Release Planning Engine must not modify `claude/scoring/scored_initiatives.md` — STEP 0 load is read-only.
- If `scored_initiatives.md` is absent from the filesystem: record "scored_initiatives.md: not present" in the STEP 0 load summary and proceed with STEP 4 estimates only.

---

## §16.8 lessons_learnt_closure.md Carry-Forward Section Schema

**Used by:** Post-Ship Closure Engine (write at STEP 8.5), Roadmap Engine / Release Planning Engine / Sprint Planning Engine (read at STEP 0)

### Section schema

```markdown
## Carry-Forward
Items: N

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | <one-sentence observation from this cycle> | <what the engine should do differently next cycle> | Roadmap \| Release Planning \| Sprint Planning \| All |
```

**Rules:**
- Absence of the `## Carry-Forward` section OR zero rows is valid — means no carry-forwards for this cycle.
- Maximum 5 items. Fewer is better — only include items with a clear, engine-actionable implication.
- Engine values: `Roadmap`, `Release Planning`, `Sprint Planning`, `All`.
- Items must be specific and actionable — not general observations.

### STEP 0 read protocol (for Roadmap, Release Planning, Sprint Planning engines)

1. Identify the most recently completed cycle: highest YYYY-MM-DD cycle ID where `post_ship_complete = true` in `.claude_current_state.json`.
2. Read `claude/cycles/<most_recent_cycle_id>/lessons_learnt_closure.md`.
3. If `## Carry-Forward` section is present and non-empty: surface each item as an advisory in session output; record in the run manifest as "Carry-forward items reviewed: N items from cycle `<cycle_id>`."
4. If section absent or has zero rows: record "No carry-forward items from prior cycle `<cycle_id>`" in run manifest and proceed.
5. Do not halt on absence. This step is advisory only.

---

## §16.9 ideas_window.json Schema

**Produced by:** idea_intake_prompt.md (STEP 2 — window open; STEP 10 — window close)
**Consumed by:** roadmap_prompt.md (STEP -1.6 trigger check)

Required fields:
```json
{
  "window_id": "IW-YYYYMMDD-nn",
  "opened_utc": "<ISO 8601>",
  "opened_by": "<role>",
  "status": "Open | Closed",
  "eligible_agents": ["<agent_slug>", ...],
  "submissions_received": ["<IDEA-ID>", ...],
  "per_agent_submission_count": { "<agent_slug>": <int>, ... },
  "closed_utc": "<ISO 8601 | null>",
  "closed_by": "<role | null>"
}
```
`per_agent_submission_count`: computed at STEP 3 by counting IDEA IDs in `submissions_received` containing each agent slug. Required field — must be present before window closes.

---

## 16.10 sprint_planning_notes.md Schema

**Produced by:** `sprint_planning_prompt.md` STEP 5
**Consumed by:** Sprint Execution Engine (STEP 0 advisory carry-forward read)

**Document title:** `# Sprint Planning Notes — <cycle_id>`

**Header block (required):**

```
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Cycle:** <cycle_id>
```

**Required sections:**

```markdown
## Backlog Slice Source

Original / Amended — <file path used>

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-xx | <reason> | Yes / No |

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-xx | ST-yy | Internal | Resolved |

## Execution Sequence

<Ordered list of EPICs and ST items>

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-xx | EPIC-xx | Valid / Changed / Materialised |

## Pre-Sprint Vulnerability Scan

<pip-audit result: clean / findings listed / tool unavailable>

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| <action> | <role> | Yes / No |
```

**Optional sections** (include when applicable):
- `## Pre-Sprint Backlog Advisory` — unconverted "Before Sprint Planning" items (STEP -1 advisory 7)
- `## Carry-Forward Items` — from prior cycle STEP 0 advisory
- `## Capacity WARN Acknowledgement` — when capacity check outcome is `warn`

---

## 16.11 sprint_backlog.md Schema

**Produced by:** `sprint_planning_prompt.md` STEP 6
**Consumed by:** Sprint Execution Engine (STEP -1 / STEP 0 load), Post-Ship Closure Engine

**Document title:** `# Sprint Backlog — <cycle_id>`

**Header block (required):**

```
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active | Sealed
**Last Updated:** <date>
**Cycle:** <cycle_id>
**Release:** <vX.Y>
**Sprint Goal:** <goal from sprint_goal.md>
**Backlog Slice Source:** <original stage4_backlog_slice.md | amended: path>
```

**Structure:**

```markdown
## Sprint Scope

### EPIC-xx — <Epic Title>

**Maps to:** S2-xx
**Owner:** <role from execution plan>
**Estimated effort:** <N capacity units>
**Risk IDs:** RISK-xx (if applicable)
**Execution sequence:** <N>

#### ST-xx — <Story Title>

**Owner:** <role>
**Estimated effort:** <N>
**Delegation class:** autonomous | delegated_backend | delegated_frontend | delegated_qa | delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-xx`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** ST-yy (must complete first) / None

**Notes:** <any flags, deferred execution blockers, or risks>

**Staging-only ACs:** [REQUIRED] List each AC from `stage4_backlog_slice.md` that carries `[staging-only evidence]` or requires live external API calls, deploy hook verification, or staging-environment behaviour that CI cannot reproduce — e.g. "AC-02 (live API response behaviour)", "AC-05 (Telegram alert on staging)". Write `None` **only** when every AC for this story is verifiable in CI. This field is enforced at the sign-off gate: `None` when staging-only ACs exist is a seal blocker (OA-02, 2nd recurrence, v4.1 ST-02).

---

*(repeat for each ST item and EPIC)*

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | <N units> |
| Total estimated effort (in-scope) | <N units> |
| Utilisation | <N%> |
| Over-allocation | Yes (accepted by PO) / No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-xx | EPIC-xx | <reason> |

## Deferred Execution Blockers Accepted

| Blocker | Accepted by | Date |
|---------|-------------|------|
| <blocker description> | Product Owner | <date> |

*(omit section if deferred_execution_blockers was empty)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| <action> | <role> | Yes / No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** [AWAITING SIGN-OFF]
**Scope confirmed:** [AWAITING SIGN-OFF]
**Capacity confirmed:** [AWAITING SIGN-OFF]
**Deferred execution blockers accepted (if any):** [AWAITING SIGN-OFF / N/A]
**Signed off by:** Product Owner
**Date:** [AWAITING SIGN-OFF]
```

**Status transition:** `Active` → `Sealed` when sign-off gate (STEP 6.2) passes. `sprint_sealed = true` in `.claude_current_state.json` must be set concurrently. Phase 3 may not invoke while status is `Active`.

---

## §16.12 Backlog Item Effort Field — Day-Range Requirement

**Used by:** Roadmap Engine (write at STEP 4.2 and STEP 9), Backlog Management Engine (validate at STEP 1), Release Planning Engine (read at STEP 4.5 Capacity Feasibility Sense Check)

**Origin:** `2026-07-14__release-v7.1` Release Planning Friction Item 1, escalated to Head of Specs Team at that cycle's post-ship closure and resolved 2026-07-14. Root cause: items filed to `backlog.md` via `roadmap_prompt.md` STEP 4.2's `📋 Backlog (gate-conditional)` disposition path bypass STEP 6 (Scoring Matrix Overlay), which is the only place the existing `S (≤ 1 day) / M (2–5 days) / L (> 5 days)` day-range convention (§16.7) was ever documented — so STEP 4.2 items routinely landed with a bare letter and no range, forcing Release Planning's capacity check to infer ranges by analogy to unrelated items.

### Field syntax

```
**Effort:** S | M | L | XS [(<day range>)]
```

### Rule

- The day range in parentheses is **required** whenever the item's `**Provisional-Target:**` (§16.6) names a specific release (`v<X.Y>`) — this is exactly the case where a precise capacity estimate is needed.
- The day range is optional when `Provisional-Target` is `TBD` or `Unscheduled` — no near-term capacity decision depends on the estimate yet.
- Day-range bands are indicative, not binding: `XS` (<1 day), `S` (~0.5–2 days), `M` (~1–5 days), `L` (~3+ days) — authors should state their own best-fit range within or near these bands rather than treating them as hard boundaries.

### Enforcement points

- **`roadmap_prompt.md` STEP 4.2** (📋 Backlog gate-conditional disposition) and **STEP 9** (Now/Next horizon promotion): when writing a new `backlog.md` item with a `Provisional-Target` naming a specific release, the `**Effort:**` field must include a day range at time of write. Do not defer this to a later grooming pass.
- **`backlog_management_prompt.md` STEP 1**: flag (do not silently backfill) any existing item whose `Provisional-Target` names a specific release but whose `Effort` field carries a bare letter with no day range — day-range estimation requires domain judgment from the item's owner, not mechanical inference.

---

## §16.13 Sign-Off Record Schema

**Used by:** Sprint Execution Engine (written at STEP 5.2 agent-mediated sign-off protocol)

**Origin:** Moved from `execution_prompt.md` §5.1 (AUD-2026-07-20-004) — canonicalised here alongside the other governed JSON schemas rather than kept inline, per §16's own stated purpose.

**Schema** (added to `execution_state.json` per-story):

```json
"sign_off_record": {
  "required_by": "Head of Specs Team",
  "method": "agent_mediated",
  "status": "cleared",
  "findings_applied": ["list of findings addressed"],
  "cleared_utc": "ISO-8601"
}
```

`method` is `"agent_mediated"` when the agent-mediated sign-off protocol ran, or `"human"` when surfaced to and resolved by the user.

---

## §16.14 Last Updated Header-History Retention Convention (ST-17, EPIC-03, v8.2, BLG-GOV-283; scope broadened 2026-08-07, user-directed session review — CLAUDE.md §2)

**Problem:** Documents chain every prior revision into the `**Last Updated:**` header field as `<date> (<reason>); prior — <date> (<reason>); prior — <date> (<reason>); ...`, with no depth or age limit. Left unbounded, this field grows every time the document is touched, eventually dwarfing the document's actual content — `ideas_register.md`'s header reached 5 chained entries before this convention was first written (2026-08-04). The original version of this rule scoped enforcement to Class 4 Planning Documents only. A 2026-08-07 session review, prompted directly by the user, found the same unbounded-chain pattern thriving outside that scope: `claude/backlog/backlog.md`'s header chain had reached **56 entries, ~32,000 characters in one field** — despite already having been truncated once, on 2026-07-28, per this same convention (nothing re-applied the cap on subsequent touches, since `backlog.md` was never named in the original "Applies to" list). `docs/System_status_report.md` (Class 3), `docs/specs/Specs_Index.md` (Class 1), `claude/backlog/backlog_archive.md`, `claude/roadmap/roadmap_archive.md`, and `claude/ideas/ideas_register_archive.md` (all Class 4, but likewise unnamed) showed the same unbounded growth. The rule is now universal — see below.

**Rule:** A `**Last Updated:**` header chain must retain **at most the current entry plus 2 prior entries (3 total)**. When writing a new entry would make the chain exceed 3, drop all entries older than the 2 most recent prior ones, and terminate the chain with the closing note `prior history retained — see prior entries in version control` in place of the dropped entries.

**Depth threshold:** 3 (current + 2 prior). This is a fixed depth, not an age-based threshold — a document touched rarely keeps its last 3 revisions regardless of how old they are; a document touched frequently truncates aggressively. Full history remains recoverable via `git log -p -- <file>` regardless of what the header retains — the header is a quick-glance summary, not the historical record of truth.

**Applies to:** Any document, of any Class, that uses the chained `**Last Updated:**` pattern at all — not just Class 4. This is now a CLAUDE.md §2 always-active non-negotiable, not an engine-specific write step, precisely because the prior narrower scoping (naming specific files/engines) is what let the pattern go unenforced everywhere else. A document that instead uses a dedicated `## Changelog` table or companion `claude/system/changelogs/*.md` file (per §11's `prompt_change_log.md` convention and the 2026-05-09 modular prompt refactor) is not exempt because of its Class — it is exempt because that structured, append-only storage is a different field serving a different purpose, and is not at risk of header-field bloat. A document with a bare single-line `**Last Updated:** <date>` field (no chaining) is already compliant and needs no action. `docs/specs/Specs_Index.md` (Class 1, Authoritative) is chaining directly in its header with no Changelog table of its own — this is filed as a structural follow-up (see backlog) rather than fixed in place, since giving it a proper Changelog table is a bigger change than a truncation.

**Enforcement:** Applied automatically by the writing engine at the point of header update — not a separate cleanup pass. See `roadmap_prompt.md` STEP 9 and `idea_intake_prompt.md`'s equivalent write step for the applied instruction. Any other engine or ad hoc session touching a chained `**Last Updated:**` field must apply the same cap at time of write, regardless of whether that file appears in this section's examples.

---

## 17. `.claude/skills/` Write Authority (BLG-GOV-167)

No governed engine's declared Write Scope (§7 pattern, `claude/system/shared/governance_preamble.md §Write-Scope`) includes `.claude/skills/`. Skill files (`.claude/skills/**/SKILL.md`) are process tooling that sits adjacent to, but outside, the five governed routines — they are invoked directly by the user or by Claude Code's skill dispatch, not by any of the phase engines.

This left a gap: a deferred patch to `.claude/skills/commit-check/SKILL.md` (adding a diff-verification step) carried unresolved across three consecutive cycles (v6.4 → v6.5 → v6.6) because no engine's write scope covered the file, and no explicit authority was named to action it outside a governed routine.

**Provision:** The **Head of Specs Team** holds standing write authority over `.claude/skills/**`, independent of any single engine's per-run Write Scope. This authority may be exercised:
- Directly, at any time, without opening a governed cycle — skill files are process tooling, not release-scoped artefacts.
- As part of a sprint story (e.g. an EPIC-02-style governance-hardening story), in which case the story's own Write Scope entry for `claude/system/`-class files extends to cover the specific `.claude/skills/` path named in the story's acceptance criteria.

**Compliance rule:** Any commit that edits a file under `.claude/skills/` must be authored or reviewed by the Head of Specs Team (directly, or via delegated sprint-story execution under this provision). No other role may modify `.claude/skills/` content.

This closes the 3-cycle carry-forward escalation `ESC-CLOSE-20260706-01`.

**`CLAUDE.md` write authority (companion provision, added AUD-2026-07-10-001):** No governed routine's declared write scope currently includes `CLAUDE.md` itself — confirmed absent from `roadmap_prompt.md`'s write-scope text. This has left a structurally identical patch (a `CLAUDE.md` §6 Governance File Edit Checklist amendment) carried unresolved across 5 consecutive scheduled-rebalance cycles (2026-07-01 through 2026-07-10) for the same reason `.claude/skills/` was stuck before this section resolved it. The **Head of Specs Team** holds standing write authority over `CLAUDE.md`, independent of any single engine's per-run Write Scope, exercisable directly or via delegated sprint-story execution. This is not a routine invocation and does not require a `[GOVERNANCE]`-prefixed commit on its own, but any such edit must still comply with CLAUDE.md's own §6 Governance File Edit Checklist for any governance file it touches as a consequence, and should be recorded in the relevant cycle's `lessons_learnt` record once applied.

This closes the 5-cycle carry-forward `CLAUDE.md` §6 patch escalation, first raised at `2026-07-01__scheduled`.

**Now-horizon carry-forward version-label write (companion provision, added ST-09/BLG-GOV-240):** `roadmap_prompt.md` STEP 8.1 condition 1b treats a non-empty, un-versioned Now-horizon carry-forward heading in `current_roadmap.md` (e.g. "Unblocked carry-forward items (un-versioned — pending next `plan release`)") the same as an empty Now horizon, requiring a PO decision at the next rebalance. But relabeling that heading with a formal version label once Release Planning has actually adopted the carry-forward scope into a firm release previously required either waiting for a full `run roadmap` invocation, or an unauthorised out-of-band hand-edit — the same structural gap `.claude/skills/` and `CLAUDE.md` had before this section existed. The **Head of Specs Team** holds standing write authority to apply this specific, narrow edit directly — relabeling an existing un-versioned Now-horizon carry-forward heading in `current_roadmap.md` with the version label Release Planning has just confirmed for that scope — without opening a full `run roadmap` rebalance cycle. This authority extends **only** to the heading label itself and its directly adjacent version/date metadata; it does not extend to adding, removing, or reprioritising items within the section, which remains reserved to `run roadmap` / `plan release`. Record any such edit in the receiving release's `run_manifest.md` or `decisions--<cycle_id>.md` for traceability. This closes `BLG-GOV-240`.

---

## 18. Playwright Test Authoring Standard (BLG-GOV-123 — moved from `execution_prompt.md` §14)

When writing or updating Playwright tests in this project:

**Use `waitFor` patterns — not `networkidle`.**

`page.waitForLoadState('networkidle')` is unreliable on CI and is prohibited in new tests. Replace with:

- **`await expect(page.locator('selector')).toBeVisible({ timeout: N })`** — preferred; waits for a specific element that confirms the page/component has rendered.
- **`await page.waitForSelector('selector')`** — acceptable when `expect` is not available at the point of navigation.
- **`await page.waitForResponse(urlPattern)`** — when the test needs to confirm a specific API call was made.
- **`await page.waitForLoadState('domcontentloaded')`** — only in navigation helper functions where a specific element is unknown. Never in the body of a test scenario.

**Standard:**
1. Every `page.goto()` or `page.reload()` must be followed by an element-specific wait, not `networkidle`.
2. In test helper functions (e.g., `async function goto(page, hash)`), use `domcontentloaded` as the base wait only when no specific element is available.
3. `waitForLoadState('networkidle')` is never permitted in new test code. The QA Evidence sign-off block for any EPIC introducing new Playwright tests must confirm this standard was followed.

**Mock payload advisory (OA-02/CF-02):** Mock payloads must match the canonical API spec response shape. Before authoring mocks, read the relevant `openapi.yaml` path and use the documented response schema. Nested objects (e.g. `{data: {field: value}}`) must not be flattened in mocks. Mismatch = silent test failure in prod.

**Route ordering advisory (ST-11, v6.8, BLG-QA-64):** When registering multiple `page.route()` handlers for overlapping URL patterns (e.g. a generic catch-all plus a more specific handler for one path), Playwright evaluates handlers in reverse registration order (most-recently-registered first). A handler's `route.continue()` call sends the request onward to the real network — it does **not** fall through to an earlier-registered, more-specific handler. Use `route.fallback()` instead of `route.continue()` when the intent is to defer to a previously-registered handler for the same request. Register generic catch-all mocks **first**, specific mocks **last**, and use `route.fallback()` in any generic handler's non-matching branch.

---

## 19. Array Guard Standard for JSON API Response Fields

**Origin:** Recurrence escalation, first raised `2026-07-17__release-v7.5` closure, carried unresolved across 3 consecutive Post-Ship Closure cycles (v7.5 → v7.6 → v7.7) because its named target ("next roadmap review") did not occur until this cycle (`2026-07-24__scheduled` — no `run roadmap` invocation had run since `2026-07-17__scheduled`; v7.6 and v7.7 both used direct-write bypass patterns instead). Owner: Head of Engineering.

**Standard:** Any frontend code calling `.map()`, `.filter()`, `.forEach()`, or similar array methods directly on a field sourced from a JSON API response must first guard with `Array.isArray(...)` (or an equivalent explicit type check) before iterating. Do not assume an API response field is an array merely because the contract types it as one — a malformed response, a partial/error payload, or a schema drift not yet caught by the OpenAPI Drift Detection gate can deliver `null`, `undefined`, or a non-array value at runtime, and an unguarded `.map()`/`.filter()` call throws and can crash the enclosing component.

**Pattern:**
```js
// Wrong — throws if data.items is not an array
data.items.map(item => ...)

// Right
Array.isArray(data.items) ? data.items.map(item => ...) : []
```

**Enforcement:** New Playwright test coverage and code review for any story touching a `.map()`/`.filter()` call site over API response data should confirm this guard is present. Not retroactively enforced against existing code as a blanket requirement — apply at next-touch of the affected call site, or file a targeted backlog item where a specific unguarded call site is identified as high-risk.

---

## 20. Dependency Vulnerability Scan Cadence (BLG-SEC-15, ST-04, EPIC-02, v8.5)

Dependency vulnerability scanning runs on three independent, overlapping cadences — no single one alone catches every gap the others close:

| Tier | Trigger | Tool(s) | Scope | Workflow / Prompt |
|------|---------|---------|-------|--------------------|
| 1 — Per-PR gate | Every PR + push to `main`/`develop` | `pip-audit` only | `backend/requirements.txt` | `.github/workflows/vulnerability-scan.yml` — HIGH/CRITICAL **blocks merge** |
| 2 — Pre-sprint check | Every `plan sprint` invocation (including `--dry-run`) | `pip-audit` only | `backend/requirements.txt` | `sprint_planning_prompt.md` STEP -1.8 — advisory, recorded in `sprint_planning_notes.md` §Pre-Sprint Vulnerability Scan |
| 3 — Scheduled re-scan | Monthly (1st of month, 07:00 UTC) + manual `workflow_dispatch` | `pip-audit` **and** `npm audit` | `backend/requirements.txt` **and** root `package-lock.json` | `.github/workflows/dependency-vuln-rescan.yml` — non-blocking; files/updates a GitHub issue (labels `security`, `dependency-scan`) for any finding not already present in `docs/security/dependency_vuln_baseline.json` |

Tier 1 and Tier 2 never run `npm audit`, and both are gated on human/CI activity (a PR being opened, a sprint being planned) — a dependency untouched by either in a given window could carry a newly-disclosed CVE unnoticed indefinitely. Tier 3 exists specifically to close that gap: it runs on a fixed calendar schedule independent of any other activity, and it is the only tier covering the frontend (`npm audit`) dependency tree at all.

**New-vs-known dedup:** Tier 3 does not re-file an issue for every run against the same already-known findings — `docs/security/dependency_vuln_baseline.json` tracks advisory IDs already surfaced (see the file's own header comment for the baseline-vs-accepted-risk distinction). Only advisory IDs absent from that file trigger a new issue. Analysis logic: `scripts/check_dependency_vuln_rescan.py`.

**Filed-item requirement:** Any new (not-in-baseline) HIGH/CRITICAL finding from Tier 3 results in a filed GitHub issue automatically (the CI-native equivalent of a backlog item — this workflow runs unattended on a schedule and cannot itself write to `claude/backlog/backlog.md`, which is governance-write-scoped to governed routines). Cybersecurity & Trust Lead triages the issue at the next convenient session, converting it to a formal `BLG-SEC-xx` backlog item via `/backlog-add` if it isn't resolved before then.

---

## Change Log

See: [`claude/system/changelogs/shared_standards_changelog.md`](changelogs/shared_standards_changelog.md)
