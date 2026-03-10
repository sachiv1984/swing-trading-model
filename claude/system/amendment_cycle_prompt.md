**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.3
**Last Updated:** 2026-03-10
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Amendment Cycle Engine — Governance Prompt

(Emergency-Only, Backlog-Scoped, Authority-Ratified, Original-Sealed)

---

## 1. Purpose

Amend a published release plan's backlog slice in response to an emergency that makes the sealed plan unexecutable or unsafe to execute as-is.

This engine exists because the Release Planning engine's published state is immutable — once `state.json.status = Published`, no artefact in that cycle may be modified. When a genuine emergency forces a backlog change after publication, this engine creates a controlled, authority-ratified amendment record in a sub-folder of the original cycle, and produces a replacement backlog slice that Sprint Planning will use instead of the original.

This routine does **NOT**:
- Rebalance the roadmap or alter strategy boundaries
- Amend acceptance criteria, EPIC structure, capacity assumptions, or timebox
- Create a new release version or a new roadmap item
- Replace the Release Planning engine for routine scope changes — routine changes do not qualify
- Operate during or after Phase 2 (sprint sealed) — once `sprint_sealed = true`, scope is owned by the execution engine

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
amend cycle --cycle "<original_cycle_id>" --reason "<emergency-fix|hard-blocker>" [--mode "strict|standard"]
```

Rules:
- Invocation must start with `amend cycle` (case-insensitive match allowed).
- `--cycle` is required. Must reference an existing cycle with `state.json.status = Published`.
- `--reason` is required. Must be one of:
  - `emergency-fix` — security patch, regulatory requirement, or critical production issue that must be addressed in this sprint
  - `hard-blocker` — a planned item is confirmed undeliverable and must be replaced or removed
- `--mode` optional:
  - `strict`: halt on any missing evidence, incomplete rationale, or unresolved authority confirmation
  - `standard` (default): proceed with flags on minor gaps; still halt on hard gates
- If invocation is not exact, do not run. Treat as conversational.

Apply the Lifecycle Guard (valid from-states: `Sprint_Planning_Complete` with `sprint_sealed = false`) per `claude/system/shared_standards.md §10` before executing any step.

**Who issues this command:** The PMO Lead persona, after Phase 1B has published and before `sprint_sealed = true`.

**Hard gate on timing:** Read `.claude_current_state.json` before proceeding. If `sprint_sealed = true`: halt immediately — amendments are not permitted after Phase 2 seals. Scope changes during or after execution are handled by the execution engine's escalation model.

---

## 3. Amendment Classification and Authority

The `--reason` flag determines which authorities must ratify the amendment. Both must confirm before the amendment can be sealed.

| Reason | Ratifying Authorities | PMO Lead Role |
|--------|-----------------------|---------------|
| `emergency-fix` | Product Owner + Director of Quality | Coordinates; no unilateral decision |
| `hard-blocker` | Product Owner + Head of Specs Team | Coordinates; no unilateral decision |

**PMO Lead may never self-ratify an amendment.** An amendment without both required authority confirmations is not valid and may not be sealed.

---

## 4. What an Amendment May Change

An amendment may only modify the **backlog slice** — specifically:

| Permitted | Notes |
|-----------|-------|
| Add an ST item | Must fit within original confirmed capacity; must reference an existing EPIC or a new emergency EPIC (see §4.1) |
| Remove an ST item | Must record reason and confirm no downstream dependency is broken |
| Replace an ST item | Treated as one remove + one add; both must be ratified |

An amendment may **not** change:
- Acceptance criteria for existing items (use the execution engine's escalation model)
- EPIC structure or EPIC-to-scope mappings (these are sealed in `release_plan.md ## Execution Plan` for schema v2 cycles; in `stage3_execution_plan.md` for pre-v2.11 cycles)
- Capacity assumptions or timebox (these are sealed in `stage4_5_capacity_check.md`)
- `stage2_scope_extraction.md`, `stage3_execution_plan.md`, or any other sealed stage artefact
- The original `state.json` or any artefact in `claude/cycles/<original_cycle_id>/`

### 4.1 Emergency EPIC Rule

If an `emergency-fix` amendment adds an item that does not map to any existing EPIC, a new emergency EPIC may be created **only** if:
- The Director of Quality confirms the item cannot be subordinated to an existing EPIC without distorting its scope
- The new EPIC is assigned an `EPIC-xx` ID continuing the existing sequence
- The new EPIC is recorded in the amendment artefacts only — it does not modify the release plan Execution Plan section or any sealed cycle artefact
- Its addition is explicitly noted in the amendment ratification record as an out-of-band EPIC

---

## 5. Canonical Governance Sources (Non-Negotiable)

Binding governance stack (precedence order):

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

This routine may not override any of the above.

Shared standards: `claude/system/shared_standards.md`.

---

## 6. Required Authority Roles

Minimum required roles for this routine:

- PMO Lead
- Product Owner
- Head of Specs Team
- Director of Quality

Verify: each role has an agent file in `claude/agents/` containing `**Role:** <Role Name>`. If any missing: halt.

---

## 7. Amendment Folder Structure (Hard Requirement)

All amendment artefacts live inside the original cycle folder:

```
claude/cycles/<original_cycle_id>/
  amendments/
    <amendment_id>/
      amendment_manifest.md
      amendment_state.json
      amendment_ratification.md
      amended_backlog_slice.md
      amendment_lessons.md        (produced at seal)
```

Amendment ID format: `AMD-<YYYYMMDD>-<nn>` (e.g., `AMD-20260303-01`)

The `amendments/` folder and the `<amendment_id>/` sub-folder are created by this engine on first write. Nothing in `claude/cycles/<original_cycle_id>/` outside the `amendments/` sub-folder may be touched.

---

## 8. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/` (all amendment artefacts)
- `claude/backlog/backlog.md` (update the release slice to reflect the amendment — same lock/transaction protocol as Phase 1B; see §9)
- `.claude_current_state.json` (amendment pointer and status update — STEP 7 only)

You must **not** modify:
- Any artefact in `claude/cycles/<original_cycle_id>/` outside the `amendments/` sub-folder
- `claude/cycles/<original_cycle_id>/state.json` (sealed)
- `claude/cycles/<original_cycle_id>/stage4_backlog_slice.md` (sealed)
- Any stage artefact (`stage*.md`) from the original cycle
- `claude/roadmap/current_roadmap.md`
- `claude/strategy/strategy_rules.md`
- Any canonical spec or governance document

Violation → halt.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

### -1.1 Timing Gate

**Atomicity guard — lock acquisition (Hard Gate):** Before reading `sprint_sealed`, acquire `claude/backlog/.lock`:

- If `claude/backlog/.lock` exists and is **not** owned by this amendment (marker `AMEND-CHECK:<original_cycle_id>`): halt — do not auto-delete. Another operation is modifying the backlog. Report the lock contents and wait for manual resolution.
- If the lock does not exist: create it with marker `AMEND-CHECK:<original_cycle_id>` and `acquired_utc`. This prevents a concurrent Sprint Planning seal from writing `sprint_sealed = true` between this check and the first amendment write.
- Release this lock at **STEP 2.5** (before human ratification begins — STEP 2.5 is the procedural release step). Re-acquire at STEP 5.1 when the backlog write begins. On any halt path before STEP 2.5: release the lock before halting.

Read `.claude_current_state.json`:
- `sprint_sealed` must be absent or `false`
- If `sprint_sealed = true`: halt immediately — the sprint is sealed; amendments are not permitted. Scope changes after Phase 2 are handled by the execution escalation model (`run sprint`). Release the lock before halting.
- `active_cycle` must match `--cycle` argument (or be set to it)

### -1.2 Original Cycle Sealed

Read `claude/cycles/<original_cycle_id>/state.json`:
- `status` must be `Published`
- `publish_eligible` must be `true`
- If not: halt — you cannot amend an unpublished cycle. If the cycle is still in planning, fix it via the release planning engine directly.

### -1.3 No Active Amendment

Check `claude/cycles/<original_cycle_id>/amendments/` for any existing amendment with `amendment_state.json.status` not equal to `Sealed` or `Withdrawn`.
- If one exists: halt — only one active amendment per cycle at a time. Seal or withdraw the existing amendment before opening a new one.

### -1.4 Required Files Present

Verify all of the following exist:
- `claude/cycles/<original_cycle_id>/state.json`
- `claude/cycles/<original_cycle_id>/stage4_backlog_slice.md`
- `claude/cycles/<original_cycle_id>/release_plan.md` (schema v2 — `release_planning_prompt.md` v2.11+; `state.json` `prompt_schema_version = "v2"`) **or** `claude/cycles/<original_cycle_id>/stage3_execution_plan.md` (pre-v2.11 cycles only). Check `state.json` to determine which applies; the Execution Plan section in `release_plan.md` is the schema v2 equivalent.
- `claude/cycles/<original_cycle_id>/stage4_5_capacity_check.md` (pre-v2.11) or `release_plan.md ## Capacity Check` section (schema v2)
- `claude/backlog/backlog.md`
- `claude/system/shared_standards.md`

If any missing: halt and report exactly which.

### -1.5 Required Authority Roles Exist

Verify agent files per Section 6. If any missing: halt.

### -1.6 Write Permission Test

Create a temporary marker file in `claude/cycles/<original_cycle_id>/amendments/` and confirm it can be written. Remove it. If write fails: halt.

---

## STEP 0 — Create Amendment Manifest and Initialise State

### 0.1 Define Amendment ID

```
amendment_id = AMD-<YYYYMMDD>-<nn>
```

Where `nn` is the next sequential amendment number for this cycle (start at `01`; increment if prior sealed/withdrawn amendments exist).

### 0.2 Create Amendment Folder

Create: `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/`

### 0.3 Create Amendment Manifest

Create: `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/amendment_manifest.md`

```markdown
**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** <date>
**Amendment ID:** <amendment_id>
**Original Cycle:** <original_cycle_id>
**Release:** <vX.Y from original state.json>
**Amendment Reason:** emergency-fix | hard-blocker
**Raised by:** PMO Lead
**Raised at:** <ISO-8601 UTC>
**Required ratifying authorities:** <Product Owner + Director of Quality | Product Owner + Head of Specs Team>
**Ratification status:** Pending
```

### 0.4 Initialise Amendment State

Create: `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/amendment_state.json`

```json
{
  "amendment_id": "<amendment_id>",
  "original_cycle_id": "<original_cycle_id>",
  "release": "<vX.Y>",
  "reason": "emergency-fix | hard-blocker",
  "status": "Initialized",
  "ratification_status": "Pending",
  "ratified_by": [],
  "ratified_at": [],
  "changes": [],
  "backlog_lock_status": "not_checked",
  "sealed_utc": "",
  "last_updated_utc": "<ISO-8601 UTC>"
}
```

Update `.claude_current_state.json`:
```json
{
  "active_amendment": "<amendment_id>",
  "amendment_status": "In_Progress",
  "last_sync_utc": "<ISO-8601 UTC>"
}
```

---

## STEP 1 — Emergency Evidence Gate (Hard Gate)

Before any backlog changes are proposed, the PMO Lead must provide evidence that the amendment qualifies.

### For `emergency-fix`:

Required evidence (all must be present):
- **Nature of the emergency:** security patch / regulatory requirement / critical production issue
- **External reference:** CVE ID, regulatory notice reference, incident ticket, or equivalent
- **Why this sprint:** explanation of why the fix cannot wait for the next planned sprint
- **Director of Quality assessment:** confirmation that the fix is within QA's ability to verify within this sprint's capacity

If any evidence is missing:
- In `strict` mode: halt — the amendment cannot proceed without complete evidence.
- In `standard` mode: flag each missing item as `[EVIDENCE REQUIRED]`. The amendment cannot be ratified until all `[EVIDENCE REQUIRED]` items are resolved.

### For `hard-blocker`:

Required evidence (all must be present):
- **Blocked item reference:** EPIC ID and ST item ID(s) that are confirmed undeliverable
- **Blocker description:** what specifically makes delivery impossible (technical constraint, dependency failure, resource loss, etc.)
- **Discovery date:** when the blocker was confirmed
- **Head of Specs Team assessment:** confirmation that the blocker cannot be resolved within the sprint and that a replacement item (if proposed) is within scope

If any evidence is missing: same flag behaviour as above.

Record evidence in `amendment_manifest.md` under a new section `## Emergency Evidence`.

---

## STEP 2 — Proposed Changes

The PMO Lead proposes the specific backlog changes required by the emergency. Each proposed change must be stated as one of:

- **Add:** EPIC reference, ST item ID (continuing existing sequence), title, one-line description, estimated effort, dependency notes
- **Remove:** ST item ID, reason, confirmation that no other in-scope item depends on it
- **Replace:** treated as one Remove + one Add (both must be fully specified)

For each proposed change, record in `amendment_manifest.md` under `## Proposed Changes`:

```markdown
### Change <n>

Type: Add | Remove | Replace
Item: <ST-xx — title>
EPIC: <EPIC-xx>
Reason: <one paragraph — direct reference to emergency evidence>
Effort delta: <+N | -N | 0 capacity units>
Dependency impact: <none | list affected items>
Ratification required from: <Product Owner + Director of Quality | Product Owner + Head of Specs Team>
```

### 2.1 Capacity Check

Calculate the net effort delta of all proposed changes against the confirmed capacity from `stage4_5_capacity_check.md`.

If net effort delta > 0 (adding more work than removing):
- In `strict` mode: halt — the amendment may not increase total sprint effort above the confirmed capacity ceiling.
- In `standard` mode: flag the over-allocation and require explicit Product Owner acceptance as part of ratification. Record the delta clearly.

If net effort delta ≤ 0: proceed.

### 2.2 Dependency Integrity

For each proposed removal: confirm no remaining in-scope item has a declared dependency on the removed item. If a dependency exists:
- The dependent item must also be removed or its dependency must be explicitly resolved
- Record the resolution in the change record

For each proposed addition: identify any items the new item depends on and confirm they are either already in scope or the dependency is explicitly noted as external.

---

## STEP 2.5 — Release Backlog Lock Before Ratification (Hard Requirement)

**Release the backlog lock NOW** — before human ratification begins (STEP 3). Ratification is a human coordination step that may take hours or days. The lock must not be held across it.

Release `claude/backlog/.lock` (if owned by this amendment):
- Delete the lock file.
- Update `amendment_state.json`: `backlog_lock_status = "released_before_ratification"`.

**Lock re-acquisition at STEP 5.1:** When ratification is confirmed and backlog update begins, re-acquire the lock per STEP 5.1 protocol.

**If the lock cannot be released:** halt and report. Do not proceed to STEP 3 while the lock is held.

---

## STEP 3 — Authority Ratification (Hard Gate)

The amendment may not proceed to backlog update until both required authorities have explicitly confirmed.

### 3.1 Ratification Record

Create: `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/amendment_ratification.md`

```markdown
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Amendment ID:** <amendment_id>
**Original Cycle:** <original_cycle_id>

## Ratification Checklist

### Required Authority 1: <Product Owner>

- [ ] Emergency evidence reviewed and accepted
- [ ] Proposed changes reviewed and accepted
- [ ] Capacity impact accepted (if over-allocation flagged)
- [ ] Confirmed: this amendment is necessary and proportionate

Confirmed by: Product Owner
Date: [AWAITING CONFIRMATION]

### Required Authority 2: <Director of Quality | Head of Specs Team>

- [ ] Emergency evidence reviewed and accepted
- [ ] Proposed changes reviewed from domain perspective
- [ ] Domain-specific concerns: <none | list>
- [ ] Confirmed: this amendment is safe to proceed from <Quality | Specs> perspective

Confirmed by: <Director of Quality | Head of Specs Team>
Date: [AWAITING CONFIRMATION]

## Ratification Status

Overall: Pending | Ratified | Rejected
```

### 3.2 Ratification Gate

Both `[AWAITING CONFIRMATION]` fields must be replaced with explicit authority confirmations and dates before the amendment may be sealed. If either authority rejects:
- Record the rejection reason in the ratification record
- Set `amendment_state.json.status = Withdrawn`
- Update `.claude_current_state.json`: `active_amendment = null`, `amendment_status = Withdrawn`
- Halt — the original sealed backlog slice remains in effect

If both confirm:
- Update `amendment_state.json`:
  - `ratification_status = Ratified`
  - `ratified_by = [<authority 1>, <authority 2>]`
  - `ratified_at = [<date>, <date>]`
  - `status = Ratified`

---

## STEP 4 — Produce Amended Backlog Slice

Create: `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/amended_backlog_slice.md`

### 4.1 Structure

The amended backlog slice is a **complete replacement** for `stage4_backlog_slice.md` — it is not a diff. It must contain:
- All items from the original `stage4_backlog_slice.md` that are not removed by this amendment
- All new items added by this amendment
- A header block identifying it as an amendment and referencing the original

```markdown
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Cycle:** <original_cycle_id>
**Amendment:** <amendment_id>
**Supersedes:** claude/cycles/<original_cycle_id>/stage4_backlog_slice.md (for sprint planning purposes)
**Ratified:** <date> by Product Owner and <Director of Quality | Head of Specs Team>

> This amended backlog slice supersedes the original stage4_backlog_slice.md for the purposes
> of Sprint Planning. The original sealed artefact is unchanged and remains the historical record
> of the published release plan.

## Amendment Summary

| Change | Item | Type | Reason |
|--------|------|------|--------|
| Added | ST-xx — <title> | emergency-fix | hard-blocker | <one line> |
| Removed | ST-xx — <title> | emergency-fix | hard-blocker | <one line> |

---

<Full backlog slice content — all EPICs and ST items in original sequence,
 with amendments applied. Removed items replaced by a struck note:
 "~~ST-xx — <title>~~ — Removed by <amendment_id>: <one line reason>"
 Added items marked: "[ADDED by <amendment_id>]">
```

### 4.2 ID Continuity

New ST items must use IDs continuing from the highest existing ST-xx in the original backlog slice. Do not reuse or renumber existing IDs.

---

## STEP 5 — Backlog Update (Concurrency-Safe)

Update `claude/backlog/backlog.md` to reflect the amendment, using the same lock/transaction protocol as Phase 1B (per `release_planning_prompt.md` §STEP 3.9 and §STEP 4).

### 5.1 Lock Acquisition

- Lock marker: `AMD:<release>:<original_cycle_id>:<amendment_id>`
- Lock file: `claude/backlog/.lock`
- If the lock file exists and is not owned by this amendment: halt — no auto-deletion.
- Create lock file, then proceed.

### 5.2 Transaction

- Create: `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/backlog_txn.json`
- Set `state: prepared` before any write to `backlog.md`
- Apply changes (add/remove items in the release slice section)
- The idempotency marker for this amendment: `<!-- amendment-marker: AMD:<release>:<original_cycle_id>:<amendment_id> -->`
- Set `state: committed` after successful write
- Release the lock

If any step fails: halt, preserve lock state, report precisely. Do not leave `backlog.md` in a partial state.

### 5.3 Backlog Write Rules

- Locate the release slice section in `backlog.md` (identified by the original `<!-- release-plan-marker: RP:<release>:<original_cycle_id> -->`)
- Apply only the changes specified in the ratified amendment
- Do not modify any items outside the release slice section
- Do not reformat or reprioritise any other section

---

## STEP 6 — Seal Amendment

Update `amendment_state.json`:

```json
{
  "status": "Sealed",
  "sealed_utc": "<ISO-8601 UTC>"
}
```

Update `amendment_manifest.md` status: `Active` → `Sealed`.

Update `amendment_ratification.md` ratification status: `Pending` → `Ratified`.

---

## STEP 7 — Global State Update (Hard Requirement)

Update `.claude_current_state.json`:

```json
{
  "active_amendment": "<amendment_id>",
  "amendment_status": "Sealed",
  "amended_backlog_slice_path": "claude/cycles/<original_cycle_id>/amendments/<amendment_id>/amended_backlog_slice.md",
  "amendment_sealed_utc": "<ISO-8601 UTC>",
  "last_sync_utc": "<ISO-8601 UTC>"
}
```

**Sprint Planning engine behaviour after amendment:** When `plan sprint` reads `.claude_current_state.json` and finds `amended_backlog_slice_path` set, it must use the amended backlog slice as its source of truth instead of `stage4_backlog_slice.md`. This pointer is the mechanism by which the amendment takes effect.

---

## STEP 8 — Amendment Lessons

Invoke `claude/system/lessons_learnt_prompt.md` (§3 — use the closest applicable routine inputs from the amendment manifest and ratification record).

Output: `claude/cycles/<original_cycle_id>/amendments/<amendment_id>/amendment_lessons.md`

Record:
- What caused the emergency that forced the amendment
- Whether the amendment process was proportionate and efficient
- Any process improvements for earlier detection of hard blockers or emergencies
- Any improvements to the release planning engine's readiness checks that could catch this class of issue earlier

---

## STEP 9 — Commit

```
git add claude/cycles/<original_cycle_id>/amendments/<amendment_id>/
git add claude/backlog/backlog.md
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Amendment sealed: <amendment_id> on <original_cycle_id> — <reason>"
git push origin <current-branch>
```

If git operations unavailable: output exact files to stage and commit message. Mark as "Ready to commit."

---

## 9. Completion Condition

The run is complete only if:

- `amendment_manifest.md` exists and status = `Sealed`
- `amendment_ratification.md` exists with both authority confirmations recorded
- `amended_backlog_slice.md` exists as a complete replacement slice
- `amendment_state.json` status = `Sealed`
- `backlog.md` updated with amendment marker present
- Backlog lock released
- `amendment_lessons.md` filed
- `.claude_current_state.json` updated with `amended_backlog_slice_path` and `amendment_status = Sealed`
- STEP 9 commit complete (or commit manifest produced)

---

## 10. Withdrawal

If an amendment is opened but the emergency is resolved before ratification, or if either ratifying authority rejects:

- Set `amendment_state.json.status = Withdrawn`
- Record reason in `amendment_manifest.md`
- Update `.claude_current_state.json`: `active_amendment = null`, `amendment_status = Withdrawn`, `amended_backlog_slice_path` — remove or set to null
- The original `stage4_backlog_slice.md` remains the active source of truth
- Do not delete the amendment folder — it is a permanent governance record

---

## 11. Governance Invariants

- **Emergency only.** Routine scope changes, priority changes, and "nice to have" additions do not qualify. If it could wait for the next sprint, it waits.
- **Original cycle is immutable.** No amendment touches any artefact in `claude/cycles/<original_cycle_id>/` outside the `amendments/` sub-folder.
- **Two-authority ratification is non-negotiable.** PMO Lead coordinates; PMO Lead never self-approves.
- **Backlog slice only.** Acceptance criteria, EPIC structure, capacity, and timebox are not amendable. Use the execution escalation model for those.
- **One active amendment at a time.** Seal or withdraw before opening another.
- **Capacity ceiling holds.** An amendment may not increase total sprint effort above the confirmed capacity ceiling without explicit Product Owner acceptance recorded in the ratification record.
- **Sprint Planning uses the amended slice.** Once sealed, `amended_backlog_slice_path` in `.claude_current_state.json` is the source of truth for Phase 2. The original slice remains the historical record.
- **Delivery pressure never qualifies as an emergency.** Wanting to add a feature because a deadline moved is not an emergency. A CVE or a confirmed undeliverable item is.
- **`sprint_sealed` check is atomic.** The backlog lock must be acquired before reading `sprint_sealed`. Do not check `sprint_sealed` without the lock — concurrent Sprint Planning seal would invalidate the result.
- **Lock release before ratification is required.** The backlog lock is released at STEP 2.5 before human ratification begins. It is re-acquired at STEP 5.1 when the backlog write runs. Never hold the lock across a human confirmation step — ratification may take hours or days.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.3 | 2026-03-10 | IMP-49: STEP -1.4 — `stage3_execution_plan.md` replaced with `release_plan.md` (schema v2 detection via `state.json.prompt_schema_version`); backward compatibility note for pre-v2.11 cycles. §4 and §4.1 references updated to match. IMP-51: STEP 2.5 added — explicit procedural step to release backlog lock before STEP 3 human ratification begins; lock re-acquired at STEP 5.1. STEP -1.1 parenthetical updated to reference STEP 2.5. Governance invariant added. |
| 1.2 | 2026-03-08 | IMP-09: Added atomicity guard to STEP -1.1 — backlog lock acquired with marker `AMEND-CHECK:<cycle_id>` before `sprint_sealed` is read; lock released after STEP 5 or on any halt. Governance invariant added. |
| 1.1 | 2026-03-07 | Added Lifecycle Guard (valid from-states: `Sprint_Planning_Complete` with `sprint_sealed = false`). |
| 1.0 | 2026-03-07 | Initial version. |