**Owner:** Director of Quality
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-03-03
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Delivery Verification Engine — Governance Prompt

(Evidence-Driven, Gate-Enforced, Quality-Owned, Cycle-Unlocking)

---

## 1. Purpose

Verify that what was built in the completed sprint matches what was scoped, specified, and accepted.

This engine:
- Confirms every in-scope item has a traceable outcome
- Reviews QA evidence against canonical specs
- Assesses deviations and enforces resolution thresholds
- Confirms outstanding delegated items are in the backlog
- Identifies test scenario gaps and commissions the QA & Testing Owner to fill them
- Produces a `verification_report.md` with a definitive status
- Updates global state to unlock (or block) the next planning cycle

This routine does **NOT**:
- Re-execute or re-test work (that is the Director of Quality's domain)
- Reprioritise the backlog or roadmap
- Override QA sign-offs already given
- Alter canonical specs (read-only except where system_status_report.md is updated)

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
run delivery verification [--cycle "<cycle_id>"] [--mode "strict|standard"]
```

Rules:
- `--cycle` optional: if omitted, load `active_cycle` from `.claude_current_state.json`. If absent, halt.
- `--mode` optional:
  - `strict`: halt on any missing artefact, incomplete field, or ambiguous state
  - `standard` (default): proceed with flags on minor gaps; still halt on hard gates
- Invocation must start with `run delivery verification` (case-insensitive match allowed).

**Who issues this command:** The PMO Lead persona. In practice, the user running this in Claude Code is acting in the PMO Lead capacity — closing out the sprint phase before the next cycle opens. This command should be issued after the Director of Quality has confirmed (via QA evidence sign-offs on `qa_evidence_EPIC-xx.md`) that the sprint evidence is ready for verification. The readiness gate (STEP -1) will fail fast if it is not.

If invocation is not exact, do not run. Treat as conversational.

**Tool call budget:** This routine typically requires 15–40 tool calls. Proceed through steps without asking for confirmation unless a hard gate fires.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Binding governance stack (precedence order):

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

This routine may not override any of the above.

---

## 4. Source-of-Truth Verification Inputs

| Input | Location | Required |
|-------|----------|---------|
| Global state | `.claude_current_state.json` | Hard gate |
| Sprint close record | `claude/cycles/<cycle_id>/sprint_close.md` | Hard gate |
| Execution state (sealed) | `claude/cycles/<cycle_id>/execution_state.json` | Hard gate |
| Backlog slice (sealed) | `claude/cycles/<cycle_id>/stage4_backlog_slice.md` | Hard gate |
| Sprint backlog (sealed) | `claude/cycles/<cycle_id>/sprint_backlog.md` | Hard gate |
| QA evidence logs | `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (one per merged EPIC) | Hard gate |
| System status report | `docs/System_status_report.md` | Required |
| Canonical specs | Paths from `spec_references` in `execution_state.json` | Required |
| Test scenarios | Paths from `test_scenarios` per EPIC in `execution_state.json` | Required (may be empty) |
| Backlog | `claude/backlog/backlog.md` | Required for traceability check |

---

## 5. Write Scope Restriction

During this routine you may write only to:

- `claude/cycles/<cycle_id>/verification_report.md` (create)
- `docs/System_status_report.md` (update — reconciliation only)
- `claude/backlog/backlog.md` (append-only — outstanding items and test scenario gaps only)
- `.claude_current_state.json` (status update only)

You must **not** modify:
- `claude/cycles/<cycle_id>/execution_state.json` (sealed)
- `claude/cycles/<cycle_id>/sprint_close.md` (sealed)
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed)
- `claude/cycles/<cycle_id>/sprint_backlog.md` (sealed)
- `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (owned by Director of Quality)
- Any canonical spec file
- `claude/roadmap/*`
- `claude/strategy/strategy_rules.md`

Violation → halt.

---

## 6. Required Authority Roles

Minimum required roles for this routine:

- Director of Quality
- Product Owner
- PMO Lead
- QA & Testing Owner

Verify: each role has an agent file in `claude/agents/` containing `**Role:** <Role Name>`.

If any required role is missing or malformed: halt.

---

## 7. Deviation Severity Policy (Hard Gates)

| Priority | Meaning | Verification impact |
|----------|---------|-------------------|
| P0 | System-breaking, data loss, or security issue | **Hard block.** Verification cannot pass. Must be resolved before any status except `Not_Verified` is assigned. No acceptance path. |
| P1 | Material functional deviation — feature does not meet spec | **Hard block.** Verification cannot pass unless Product Owner AND Director of Quality both explicitly accept with documented rationale recorded in `verification_report.md`. |
| P2 | Partial implementation — core behaviour present but incomplete | **Hard block.** Verification cannot pass unless explicitly accepted with documented rationale, AND a backlog item is confirmed for the remainder. |
| P3 | Minor deviation — cosmetic, edge case, or non-critical gap | Record in report. Create backlog item. Verification proceeds as `Verified_with_deviations`. |

**Any open item that is not a filed deviation** (returned item, flagged gap, unresolved escalation) must have a `backlog.md` entry before the verification report is sealed. Verification does not block on these items — but they must be traceable.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

**First action:** Read `claude/cycles/<cycle_id>/execution_state.json`. Confirm `sealed = true`. If not sealed: halt — the sprint execution record is not closed. The execution engine must complete and seal before verification can run.

Shared standards (escalation format, halt report format, gh CLI commands, identifier conventions): `claude/system/shared_standards.md`.

### -1.1 Status Check

Read `.claude_current_state.json`:
- `status` must be `Sprint_Complete`.
- If `Executing` or `Blocked`: halt — sprint is not closed.
- If `Verified` or `Verification_Failed`: confirm with the user whether they are re-running verification for this cycle. If yes: proceed. If a prior `verification_report.md` exists, archive it by appending `_prev_<timestamp>` to the filename before creating a new one.

### -1.2 Sprint Close Readiness Statement

Read `sprint_close.md` — locate the **Verification readiness statement**:

```
All spec references populated: Yes/No
All deviations filed: Yes/No
QA evidence logs complete: Yes/No
```

If any field is `No`: halt. Report exactly which condition is unmet and what is needed to resolve it. Do not proceed until all three are `Yes`.

### -1.3 QA Evidence Logs Present

For each EPIC in `execution_state.json.merge_gate.epics_merged`:
- Confirm `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` exists.
- Confirm the QA sign-off block contains `Signed off by: Director of Quality` with a date.

If any merged EPIC is missing its qa_evidence log or has a blank sign-off: halt. List exactly which EPICs are affected. Verification cannot proceed without signed QA evidence for every merged EPIC.

### -1.4 Required Files Present

Verify all files in Section 4 exist. If any are missing: halt and report exactly which.

---

## STEP 1 — Scope Traceability (Hard Gate)

Purpose: confirm every item that was in scope has a traceable outcome.

For every ST item in `stage4_backlog_slice.md`:

1. Locate its record in `execution_state.json`.
2. Check status — must be `done`, `merged`, or `returned_to_backlog`.
   - If any item has no record, or has status `not_started` / `in_progress` / `blocked_*` without a `returned_to_backlog` disposition: traceability gap — halt in `strict` mode; flag and continue in `standard` mode.
3. For `done` / `merged` items: confirm `spec_references` is non-empty.
   - If `spec_references = []`: flag as traceability gap. Cannot verify against spec with no reference.
4. For `returned_to_backlog` items: confirm a corresponding entry exists in `claude/backlog/backlog.md` referencing this `cycle_id`.
   - If the backlog entry is missing: **add it now** (permitted write):
     ```
     - [ST-xx] <title> — returned from <cycle_id>: <reason>. See sprint_close.md.
     ```
   - Record the addition in `verification_report.md`.

**Output — Traceability matrix** (in `verification_report.md` §2):

| ST Item | Title | Outcome | Spec Reference | Backlog Entry |
|---------|-------|---------|---------------|---------------|
| ST-xx | <title> | done/merged/returned | <spec#section or "none filed"> | N/A / ✓ / ⚠ added |

Flag counts: `Traceability gaps: N | Items returned: N | Backlog entries added this run: N`

---

## STEP 2 — QA Evidence Review

For each merged EPIC, read `qa_evidence_EPIC-xx.md`:

### 2.1 Per-Item Review

For each ST item row in the evidence table:
- `Result` must be `Pass` or `Pass with notes`.
- If `Result = Fail`: verification blocker — record in open items. In `strict` mode: halt immediately. In `standard` mode: continue reviewing remaining EPICs; verification status cannot be `Verified` or `Verified_with_deviations` until resolved.

### 2.2 Acceptance Criteria Check

Cross-reference each ST item's acceptance criteria (from `sprint_backlog.md`) against the `Result` entry in the qa_evidence log.
- If criteria were narrowed or omitted in the evidence log without a filed deviation: flag as potential scope reduction. Surface to Director of Quality.

### 2.3 Sign-off Completeness

Confirm the QA sign-off block is complete:
- All three checkboxes marked
- `Signed off by: Director of Quality` with a date
- `Pass with notes` results have substantive comments (not blank)

---

## STEP 3 — Deviation Assessment

Read the deviation list from `sprint_close.md` ("Deviations filed this sprint").

For each deviation:

1. Locate it in the referenced canonical spec file (filed there per execution_prompt §3.1.A step 10).
2. Confirm the deviation entry contains: priority (P0–P3), description, canonical requirement, target resolution release, owner, and backlog reference.
3. Apply the severity policy (Section 7):
   - **P0:** Hard block. Set `verification_status = Not_Verified`. Do not proceed to STEP 8 signing until resolved. No acceptance path exists.
   - **P1:** Hard block. Require documented acceptance from Product Owner AND Director of Quality in `verification_report.md` §4 to proceed.
   - **P2:** Hard block. Require documented acceptance with confirmed backlog item. If backlog item is missing: add it now (permitted write).
   - **P3:** Record in report. Confirm backlog item exists (add if missing). Verification proceeds as `Verified_with_deviations`.
4. For any item where `deviations_filed = false` in `execution_state.json` (deviation check was not completed): flag as traceability gap. Surface to Director of Quality.

**Output — Deviation register** (in `verification_report.md` §4):

| Deviation Ref | ST Item | Priority | Description | Disposition | Backlog Item |
|---------------|---------|----------|-------------|-------------|-------------|
| DEV-ref | ST-xx | P0–P3 | <one line> | Blocks / Accepted / Recorded | BL-ref |

---

## STEP 4 — Outstanding Items Backlog Check

Any item unresolved at sprint close must be in the backlog. This is a final sweep — not a block.

Check `sprint_close.md` for:
- Items delegated and outstanding (still in delegated state at close)
- Open escalations carried forward

For each:
1. Confirm `backlog.md` entry exists with `cycle_id` reference. If missing: add it now (permitted write).
2. Record in `verification_report.md` §5.

---

## STEP 5 — Test Scenario Coverage Assessment

Read `execution_state.json` — for each EPIC, read the `test_scenarios` field.

### 5.1 Coverage Check

For each EPIC:
- `test_scenarios = []`: record "no scenarios available — manual acceptance review only."
- `test_scenarios` populated: cross-reference with `qa_evidence_EPIC-xx.md` "Scenarios run" field.
  - Scenarios available but not referenced as run: flag as "available but not executed."

### 5.2 Feedback to QA & Testing Owner

For each EPIC with coverage gaps, produce a structured feedback record:

```
## Test Coverage Gap — EPIC-xx: <title>

**Gap type:** No scenarios exist | Scenarios existed but not run | Partial coverage
**Spec sections covered by this EPIC:**
  - <spec file#section> (from spec_references of Done items)
**Acceptance criteria not covered by existing scenarios:**
  - <list AC items from sprint_backlog.md with no corresponding scenario>
**Recommended new scenarios:**
  - Scenario: <title> — tests: <what behaviour> — against spec: <spec#section>
  (repeat per gap)
**Action required:**
  QA & Testing Owner to create scenario file(s) in docs/testing/ covering the above,
  referencing EPIC-xx and the spec sections listed.
  Target: before next sprint that touches these spec sections.
```

Add backlog item:
```
- [TEST-GAP-EPIC-xx] Test scenario coverage gap from <cycle_id>: QA & Testing Owner to create scenarios per verification_report.md §Test Coverage. Target: pre-next sprint on this domain.
```

The engine does not create scenario files. It produces a complete specification for what needs to be created, with enough detail that the QA & Testing Owner can act without further clarification.

---

## STEP 6 — System Status Report Reconciliation

Read `docs/System_status_report.md` — locate the section for this `cycle_id`.

Verify:
- All merged EPICs appear in "Capabilities now live" with correct spec references.
- All `returned_to_backlog` items appear in "Capabilities deferred."
- P3 deviations are noted under the relevant capability row.

If any discrepancy: correct the system status report now (permitted write). Record the correction in `verification_report.md` §7.

If `docs/System_status_report.md` does not exist: create it (the execution engine should have done this — if missing, create it using the execution_prompt §5.3A template).

---

## STEP 7 — Determine Verification Status

Based on findings from STEPS 1–6:

| Condition | Status |
|-----------|--------|
| No hard blocks; no unaccepted P0/P1/P2 deviations; no QA Fail results; all traceability gaps flagged only (standard mode) | `Verified` |
| Hard blocks present but all P1/P2 deviations have documented acceptance by Product Owner + Director of Quality | `Verified_with_deviations` |
| Any P0 deviation open; any P1/P2 without documented acceptance; any QA Fail result unresolved | `Not_Verified` |

`Verified` and `Verified_with_deviations` both unlock the next cycle.  
`Not_Verified` blocks the next cycle until the engine is re-run and produces a passing status.

---

## STEP 8 — Produce Verification Report

Create: `claude/cycles/<cycle_id>/verification_report.md`

Lifecycle header:
```
Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active — Pending sign-off
Last Updated: <date>
Cycle: <cycle_id>
```

Body (nine sections in order):

**§1 — Verification Status**
```
Status: Verified | Verified_with_deviations | Not_Verified
Sprint goal: <text>
Cycle: <cycle_id>
Verification run: <ISO-8601 UTC>
```

**§2 — Traceability Matrix** — from STEP 1. Full table + flag counts.

**§3 — QA Evidence Summary** — from STEP 2. Per EPIC: pass/fail summary, sign-off confirmed, notes surfaced.

**§4 — Deviation Register** — from STEP 3. Full table. Hard blocks section. Acceptance records section (for any P1/P2 accepted: who accepted, when, rationale).

**§5 — Outstanding Items Carried to Backlog** — from STEP 4. List: item, reason, backlog entry ref.

**§6 — Test Coverage Assessment** — from STEP 5. Per EPIC: scenario status. Full gap feedback records. Backlog items added.

**§7 — System Status Confirmation** — from STEP 6. Confirmed / corrected / created. Any corrections listed.

**§8 — Open Items** *(only if `Not_Verified`)* — every condition that must be resolved before re-running. Each: description, owner, resolution path.

**§9 — Sign-off Block**

```
## Director of Quality Sign-off

- [ ] Traceability complete (or gaps documented with rationale)
- [ ] QA evidence reviewed and accepted
- [ ] Deviation register reviewed; all P0/P1/P2 dispositions confirmed
- [ ] Test coverage gaps actioned (backlog items created)
- [ ] System status report confirmed accurate

Signed off by: Director of Quality
Date:
Comments:

## Product Owner Acceptance

- [ ] Outstanding items confirmed in backlog
- [ ] P1/P2 deviation acceptances confirmed (if any)
- [ ] Next cycle cleared to open

Accepted by: Product Owner
Date:
Comments:
```

---

## STEP 9 — Global State Update (Hard Requirement)

### If status = `Verified` or `Verified_with_deviations`:

Update `.claude_current_state.json`:
```json
{
  "status": "Verified",
  "verification_report": "claude/cycles/<cycle_id>/verification_report.md",
  "verification_status": "Verified | Verified_with_deviations",
  "next_cycle_unblocked": true,
  "last_sync_utc": "<now>"
}
```

Surface to user:
> Delivery verification complete. Status: [Verified / Verified_with_deviations].
> The next planning cycle (Roadmap Rebalance or Release Planning) may now be opened.
> [N test coverage gap backlog items added — QA & Testing Owner to action before next sprint on these domains.]
> [N deviations carried to backlog at P3 / accepted at P1/P2 with documented rationale.]

### If status = `Not_Verified`:

Update `.claude_current_state.json`:
```json
{
  "status": "Verification_Failed",
  "verification_report": "claude/cycles/<cycle_id>/verification_report.md",
  "verification_status": "Not_Verified",
  "next_cycle_unblocked": false,
  "last_sync_utc": "<now>"
}
```

Output halt report per `claude/system/shared_standards.md` §5. Include:
- Which conditions are unresolved (exact list)
- Owner per condition
- Resolution path per condition
- How to re-run: once conditions are met, re-issue `run delivery verification --cycle "<cycle_id>"`. The engine re-reads all inputs and re-evaluates. It does not re-process steps that were already clean.

**The next planning cycle may not open until `next_cycle_unblocked = true`.** The Roadmap Rebalance Engine and Release Planning Engine must check this flag at their preflight gates.

---

## STEP 10 — Commit

Commit all artefacts created or modified by this routine:

```
git add claude/cycles/<cycle_id>/verification_report.md
git add docs/System_status_report.md
git add claude/backlog/backlog.md  (if modified)
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Delivery verification complete: <cycle_id> — <status>"
git push origin <current-branch>
```

If git operations are unavailable: output the exact files to stage and the commit message. Mark as "Ready to commit."

---

## 8. Completion Condition

The run is complete only if:

- `verification_report.md` exists with all 9 sections (§8 only if Not_Verified)
- Verification status is one of: `Verified`, `Verified_with_deviations`, `Not_Verified`
- All `returned_to_backlog` items have confirmed backlog entries
- All P2/P3 deviations have backlog items
- All test coverage gaps have backlog items for QA & Testing Owner
- `docs/System_status_report.md` confirmed accurate for this cycle
- `.claude_current_state.json` updated with verification outcome and `next_cycle_unblocked` flag
- STEP 10 commit complete (or commit manifest produced)

---

## 9. Governance Invariants

- **No autonomous verification.** The engine assembles evidence and produces the report. The Director of Quality and Product Owner sign off. The engine does not self-certify.
- **No cycle unlocking without passing status.** `next_cycle_unblocked = true` is only set when status is `Verified` or `Verified_with_deviations`. Never when `Not_Verified`.
- **No scope revision.** This engine reads sealed artefacts. It does not add, remove, or change what was in scope.
- **All gaps are traceable.** Nothing is silently dropped. Every outstanding item, test gap, and deviation has a backlog entry before the report is sealed.
- **Re-runnable.** `Not_Verified` does not close the cycle — re-issue the command once conditions are resolved. The engine focuses only on the remaining open items.
- **P0 deviations have no acceptance path.** They must be resolved. The engine will never record a P0 deviation as accepted — only the resolution of the underlying issue unlocks verification.
- **Delivery pressure does not override quality gates.** The Director of Quality and Product Owner sign off independently. Neither can unilaterally accept a P0 deviation.