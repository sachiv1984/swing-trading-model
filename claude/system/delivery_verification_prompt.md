**Owner:** Director of Quality
**Status:** Active
**Version:** 1.9
**Last Updated:** 2026-04-11
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
- Confirms outstanding delegated items and deferred execution blockers are dispositioned
- Identifies test scenario gaps and commissions the QA & Testing Owner to fill them
- Produces a `verification_report.md` with a definitive status
- Updates global state to unlock (or block) the next planning cycle

This routine does **NOT**:
- Re-execute or re-test work (that is the Director of Quality's domain)
- Reprioritise the backlog or roadmap
- Override QA sign-offs already given
- Alter canonical specs (read-only except where `docs/System_status_report.md` is updated)

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

**Who issues this command:** The PMO Lead persona, after the Director of Quality has confirmed (via QA evidence sign-offs on `qa_evidence_EPIC-xx.md`) that the sprint evidence is ready for verification. The readiness gate (STEP -1) will fail fast if it is not.

If invocation is not exact, do not run. Treat as conversational.

Apply the Lifecycle Guard (valid from-states: `Sprint_Complete`) per `claude/system/shared_standards.md §10` before executing any step.

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
| Backlog slice (sealed) | See note below — may be amended | Hard gate |
| Sprint backlog (sealed) | `claude/cycles/<cycle_id>/sprint_backlog.md` | Hard gate |
| QA evidence logs | `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (one per merged EPIC) | Hard gate |
| System status report | `docs/System_status_report.md` | Required |
| Canonical specs | Paths from `spec_references` in `execution_state.json` | Required |
| Test scenarios | Paths from `test_scenarios` per EPIC in `execution_state.json` | Required (may be empty) |
| Backlog | `claude/backlog/backlog.md` | Required for traceability check |
| Release plan state | `claude/cycles/<cycle_id>/state.json` | Required (deferred execution blockers) |

**Backlog slice source-of-truth rule:** At STEP -1, check `.claude_current_state.json` for `amended_backlog_slice_path`. If present and non-empty, that file is the authoritative backlog slice — use it throughout in place of `stage4_backlog_slice.md`. Cross-reference against `execution_state.json.backlog_slice_source` to confirm both pointers agree. If they disagree: flag to the PMO Lead before proceeding. If `amended_backlog_slice_path` is absent or empty, use `stage4_backlog_slice.md`.

---

## 5. Write Scope Restriction

During this routine you may write only to:

- `claude/cycles/<cycle_id>/verification_report.md` (create)
- `claude/cycles/<cycle_id>/verification_escalations.md` (create or append — hard gate blockers only)
- `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (append-only — Phase 4 section; create if absent)
- `docs/System_status_report.md` (update — reconciliation only)
- `claude/backlog/backlog.md` (append-only — outstanding items and test scenario gaps only)
- `.claude_current_state.json` (status update only)

You must **not** modify:
- `claude/cycles/<cycle_id>/execution_state.json` (sealed)
- `claude/cycles/<cycle_id>/sprint_close.md` (sealed)
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed)
- `claude/cycles/<cycle_id>/amendments/*/amended_backlog_slice.md` (sealed)
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

## ESCALATION SUBROUTINE (Callable)

Trigger: whenever a hard gate produces a blocker that cannot be resolved within this run (e.g. a P0 deviation with an unreachable owner, a missing QA sign-off that requires human action before the report can seal).

Create or append to: `claude/cycles/<cycle_id>/verification_escalations.md`

Use escalation format per `claude/system/shared_standards.md` §4. ID prefix: `ESC-VER-YYYYMMDD-nn`.

Record: blocking condition, owning authority, resolution path, SLA.

After filing: update `verification_report.md` §8 (Open Items) with a reference to the escalation record.

This subroutine does not change the verification status — a P0 that is escalated is still a P0. The escalation tracks progress toward resolution; only resolution itself changes the status.

---

## STEP -1 — Preflight Gate (Hard Gate)

**First action:** Read `claude/cycles/<cycle_id>/execution_state.json`. Confirm `sealed = true`. If not sealed: halt — the sprint execution record is not closed. **Resolution path:** Issue `run sprint --cycle <cycle_id>` — if all EPICs are already merged (all `pr_status = merged` in `execution_state.json`), the execution engine will detect this and execute STEP 5 (Sprint Close) directly, sealing the record and setting status to `Sprint_Complete`. Once sealed, re-invoke `run delivery verification --cycle <cycle_id>`.

Shared standards (escalation format, halt report format, gh CLI commands, identifier conventions): `claude/system/shared_standards.md`.

### -1.1 Status Check

Read `.claude_current_state.json`:
- `status` must be `Sprint_Complete`.
- If `status` is `Executing` or `Blocked`: halt — sprint is not closed. **Resolution path:** Issue `run sprint --cycle <cycle_id>`. If all EPICs are already merged, the execution engine will detect this and execute STEP 5 (Sprint Close) directly, sealing the record. Once `Sprint_Complete`, re-invoke `run delivery verification --cycle <cycle_id>`.
- If `status` is `Verified` or `Not_Verified`: confirm with the user whether they are re-running verification for this cycle. If yes: proceed. If a prior `verification_report.md` exists, archive it by appending `_prev_<timestamp>` to the filename before creating a new one.

Check `amended_backlog_slice_path`:
- If present and non-empty: record this as the authoritative backlog slice path for this run. Verify the file exists — if not, halt and report.
- If absent or empty: `stage4_backlog_slice.md` is the authoritative slice.

Cross-reference the identified authoritative path against `execution_state.json.backlog_slice_source`. If they disagree: flag to PMO Lead before proceeding. Do not silently verify against a mismatched scope.

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

Sign-off check (STRUCTURAL — two-tier, AUD-2026-04-11-005):
- **TIER 1 — BLANK:** If `Signed off by:` field is empty or "pending" → HALT. List exactly which EPICs are affected. Do not proceed until Director of Quality signs.
- **TIER 2 — WRONG AUTHORITY:** If sign-off is present but the signer is not Director of Quality → FLAG (do not halt). Require Director of Quality to provide a counter-sign note in that EPIC's `qa_evidence_EPIC-xx.md` before proceeding to STEP 1. Record the mismatch in `run_manifest` as a compliance advisory.

If any merged EPIC is missing its qa_evidence log entirely: halt (Tier 1 applies). Verification cannot proceed without signed QA evidence for every merged EPIC.

### -1.4 Required Files Present

Verify all files in Section 4 exist. If any are missing: halt and report exactly which.

---

## STEP 1 — Scope Traceability (Hard Gate)

Purpose: confirm every item that was in scope has a traceable outcome.

For every ST item in the authoritative backlog slice (identified in STEP -1.1):

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
   - **P0:** Hard block. Set `verification_status = Not_Verified`. File an escalation record in `verification_escalations.md` (ESC-VER subroutine). Do not proceed to STEP 8 signing until resolved. No acceptance path exists.
   - **P1:** Hard block. Require documented acceptance from Product Owner AND Director of Quality in `verification_report.md` §4 to proceed.
   - **P2:** Hard block. Require documented acceptance with confirmed backlog item. If backlog item is missing: add it now (permitted write).
   - **P3:** Record in report. Confirm backlog item exists (add if missing). Verification proceeds as `Verified_with_deviations`.
4. For any item where `deviations_filed = false` in `execution_state.json` (deviation check was not completed): flag as traceability gap. Surface to Director of Quality.

**Output — Deviation register** (in `verification_report.md` §4):

| Deviation Ref | ST Item | Priority | Description | Disposition | Backlog Item |
|---------------|---------|----------|-------------|-------------|-------------|
| DEV-ref | ST-xx | P0–P3 | <one line> | Blocks / Accepted / Recorded | BL-ref |

> **Backlog reference synchronisation (LL-CL-v22-01):** When a new backlog item is created for a deviation in this step (P2 requires backlog item; P3 confirms or creates one), also update the `Backlog reference:` field in the corresponding canonical spec deviation note to reference the correct backlog item ID. Do this in the same session — this prevents stale placeholder references (e.g. "to be filed at next rebalance") from persisting into post-ship closure, where they require correction at STEP 5.

> **Canonical spec Known Deviations sync (LL-v2.3-CL-03):** After confirming or creating a backlog item for any deviation (P1–P3), verify that the canonical spec named in the deviation record has a Known Deviations section with an entry for this deviation. If absent: create the section and entry in the same session using the standard fields (description, canonical requirement, priority P0–P3, target resolution release, owner, backlog reference). This prevents the post-ship closure STEP 5 from being the first gate to enforce canonical spec propagation — it happened twice (v2.2 stale backlog refs, v2.3 missing Known Deviations section).

---

## STEP 4 — Outstanding Items and Deferred Execution Blockers

### 4.1 Outstanding Items Backlog Check

Any item unresolved at sprint close must be in the backlog. This is a final sweep — not a block.

Check `sprint_close.md` for:
- Items delegated and outstanding (still in delegated state at close)
- Open escalations carried forward

For each:
1. Confirm `backlog.md` entry exists with `cycle_id` reference. If missing: add it now (permitted write).
2. Record in `verification_report.md` §5.

### 4.2 Deferred Execution Blockers Review

Read `deferred_execution_blockers` from `claude/cycles/<cycle_id>/state.json` (set by the Release Planning Engine at publish time; accepted by the Product Owner at Sprint Planning).

For each deferred execution blocker:

| Situation | Action |
|-----------|--------|
| Resolved during execution (item `done` or `merged`) | Record as resolved in `verification_report.md` §5 |
| Item `returned_to_backlog` | Confirm backlog entry references the original blocker; record as carried forward |
| Not resolved and no backlog entry | Add backlog entry now (permitted write); record as unresolved carry-forward |

If `deferred_execution_blockers` is empty or field is absent: note "No deferred execution blockers" and continue.

This step is informational — deferred execution blockers do not block verification status (the Product Owner accepted them at planning time). Their purpose here is audit closure: every blocker accepted at planning must be traceable to an outcome at verification.

### 4.3 Stale Parked Items Detection (IMP-15)

Scan the authoritative backlog slice for items with `status = parked`.

For each parked item, check whether the same item appeared as `parked` in the backlog slices from the 2 prior completed cycles (by searching for the same ST item ID in `claude/cycles/<prior_cycle_id>/stage4_backlog_slice.md` — where available).

**If an item has been `parked` in 3 or more consecutive cycle backlog slices:**
- Flag as stale parked item.
- Record in `verification_report.md §5` under sub-section "Stale Parked Items Requiring PO Disposition":
  ```
  | ST Item | Title | Parked cycles | Action required |
  |---------|-------|---------------|-----------------|
  | ST-xx | <title> | [cycle_id_1, cycle_id_2, cycle_id_3] | Mandatory PO disposition before next release plan |
  ```
- Surface to PMO Lead: these items must receive an explicit Product Owner decision (Advance, Reject, or explicitly defer with written rationale) before the next `plan release` run.

This step is detection only — it does not block verification status. Enforcement is at Post-Ship Closure STEP 3.4 and at backlog management grooming.

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

### 5.3 Test Scenario Gaps Table (IMP-14)

After producing all gap feedback records in STEP 5.2, produce a structured `test_scenario_gaps` table in `verification_report.md §6`:

```
### Test Scenario Gaps — Structured Register

| gap_id | EPIC | Description | Qualifying reason | Disposition |
|--------|------|-------------|-------------------|-------------|
| TSG-<cycle_short>-01 | EPIC-xx | <one-line gap description> | <why this qualifies: core user journey / no scenario coverage / spec section uncovered> | backlog_item_created | not_applicable | deferred |
```

**Disposition values:**
- `backlog_item_created` — a `TEST-GAP-EPIC-xx` backlog item has been added to `backlog.md` (link the item ID).
- `not_applicable` — gap does not cover a core user journey; no backlog item required (record rationale).
- `deferred` — gap is acknowledged but backlog item creation deferred to a named future release (record rationale and target release).

**Phase 4 exit criterion:** All identified test scenario gaps must have a disposition recorded in this table before `verification_report.md` may be sealed. A row with no disposition is an open item that blocks STEP 8.5.

If no test scenario gaps were identified this run: record "No test scenario gaps identified" in `verification_report.md §6` and mark the table as N/A.

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
Backlog slice source: <file path used — original or amended>
Verification run: <ISO-8601 UTC>
```

**§2 — Traceability Matrix** — from STEP 1. Full table + flag counts.

**§3 — QA Evidence Summary** — from STEP 2. Per EPIC: pass/fail summary, sign-off confirmed, notes surfaced.

**§4 — Deviation Register** — from STEP 3. Full table. Hard blocks section. Acceptance records section (for any P1/P2 accepted: who accepted, when, rationale).

**§5 — Outstanding Items and Deferred Execution Blockers** — from STEP 4. Two sub-sections: (a) outstanding items carried to backlog (item, reason, backlog entry ref); (b) deferred execution blocker dispositions (blocker description, original acceptance, outcome).

**§6 — Test Coverage Assessment** — from STEP 5. Per EPIC: scenario status. Full gap feedback records. Backlog items added.

**§7 — System Status Confirmation** — from STEP 6. Confirmed / corrected / created. Any corrections listed.

**§8 — Open Items** *(only if `Not_Verified`)* — every condition that must be resolved before re-running. Each: description, owner, resolution path. Reference any `verification_escalations.md` entries by ID.

**§9 — Sign-off Block**

```
## Director of Quality Sign-off

- [ ] Traceability complete (or gaps documented with rationale)
- [ ] QA evidence reviewed and accepted
- [ ] Deviation register reviewed; all P0/P1/P2 dispositions confirmed
- [ ] Test coverage gaps actioned (backlog items created)
- [ ] System status report confirmed accurate
- [ ] Deferred execution blockers dispositioned

Signed off by: Director of Quality
Date:
Comments:

## Product Owner Acceptance

- [ ] Outstanding items confirmed in backlog
- [ ] P1/P2 deviation acceptances confirmed (if any)
- [ ] Deferred execution blocker outcomes acknowledged
- [ ] Next cycle cleared to open

Accepted by: Product Owner
Date:
Comments:
```

**Pre-seal gate (LL-v2.4-DV-01):** Before proceeding to STEP 8.5, read the §9 sign-off block in `verification_report.md`. Verify that:
- Director of Quality `Date:` field is non-blank.
- Product Owner `Date:` field is non-blank.

If either `Date:` field is blank: do not proceed to STEP 8.5. Surface to the relevant authority (Director of Quality or Product Owner) with the current `verification_report.md` §9 block and request that the Date field be completed. Do not seal `verification_report.md` until both Date fields are filled. Once both are non-blank: continue to STEP 8.5.

---

## STEP 8.5 — Lessons Learnt (Phase 4 Append)

Invoke: `claude/system/lessons_learnt_prompt.md` (§3.4 — Delivery Verification Phase 4 Append)

Output path: `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (Phase 4 section append — create file if absent)

The shared prompt governs the structured table block format (§4.2), idempotency guard, action rules, and completion conditions. Phase 4 friction areas to focus on: gate sequencing, deviation severity call consistency, test scenario coverage gaps, sign-off coordination friction.

**Idempotency guard (built into `lessons_learnt_prompt.md §3.4`):** Pre-write check for `## Phase 4 — <cycle_id>` header in `lessons_learnt_cycle.md`. If present: skip append.

Do not proceed to STEP 9 until the Phase 4 section has been appended to `lessons_learnt_cycle.md`. If the lessons learnt prompt cannot be invoked: produce the Phase 4 section directly using the §4.2 structured table format and record the deviation in `verification_report.md §8`.

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
  "status": "Not_Verified",
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
- Reference to `verification_escalations.md` entries (if any filed this run)
- How to re-run: once conditions are met, re-issue `run delivery verification --cycle "<cycle_id>"`. The engine re-reads all inputs and re-evaluates. It does not re-process steps that were already clean.

**The next planning cycle may not open until `next_cycle_unblocked = true`.** The Roadmap Rebalance Engine and Release Planning Engine must check this flag at their preflight gates.

---

## STEP 10 — Commit

Commit all artefacts created or modified by this routine:

```
git add claude/cycles/<cycle_id>/verification_report.md
git add claude/cycles/<cycle_id>/verification_escalations.md  (if created)
git add claude/cycles/<cycle_id>/lessons_learnt_cycle.md  (if created or appended)
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

- `verification_report.md` exists with all 9 sections (§8 only if `Not_Verified`)
- Verification status is one of: `Verified`, `Verified_with_deviations`, `Not_Verified`
- Phase 4 section appended to `lessons_learnt_cycle.md` (STEP 8.5 complete)
- All `returned_to_backlog` items have confirmed backlog entries
- All P2/P3 deviations have backlog items
- All test coverage gaps have a disposition recorded in the `test_scenario_gaps` table (STEP 5.3) — `backlog_item_created`, `not_applicable`, or `deferred`
- All deferred execution blockers have a recorded disposition in `verification_report.md` §5
- `docs/System_status_report.md` confirmed accurate for this cycle
- `verification_escalations.md` filed for any hard gate blockers that required escalation (if applicable)
- `.claude_current_state.json` updated with verification outcome and `next_cycle_unblocked` flag
- STEP 10 commit complete (or commit manifest produced)

---

## 9. Governance Invariants

- **No autonomous verification.** The engine assembles evidence and produces the report. The Director of Quality and Product Owner sign off. The engine does not self-certify.
- **No cycle unlocking without passing status.** `next_cycle_unblocked = true` is only set when status is `Verified` or `Verified_with_deviations`. Never when `Not_Verified`.
- **No scope revision.** This engine reads sealed artefacts. It does not add, remove, or change what was in scope.
- **All gaps are traceable.** Nothing is silently dropped. Every outstanding item, test gap, deviation, and deferred execution blocker has a disposition before the report is sealed.
- **Re-runnable.** `Not_Verified` does not close the cycle — re-issue the command once conditions are resolved. The engine focuses only on the remaining open items.
- **P0 deviations have no acceptance path.** They must be resolved. The engine will never record a P0 deviation as accepted — only the resolution of the underlying issue unlocks verification.
- **Amendment slice supersedes original.** If `amended_backlog_slice_path` is set, scope traceability runs against that file. Verifying against the original slice when an amendment has sealed is a process integrity failure.
- **Delivery pressure does not override quality gates.** The Director of Quality and Product Owner sign off independently. Neither can unilaterally accept a P0 deviation.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.9 | 2026-04-11 | AUD-2026-04-11-005: STEP -1.3 sign-off check upgraded to two-tier STRUCTURAL check — Tier 1 (BLANK): empty or "pending" sign-off = HALT; Tier 2 (WRONG AUTHORITY): sign-off present but not Director of Quality = FLAG + require DoQ counter-sign before STEP 1 + compliance advisory in run_manifest. Resolves STALE 2-cycle deferred patch. Authority: Head of Specs Team (AUD-2026-04-11, 2026-04-11). |
| 1.8 | 2026-04-06 | ST-12 (CF-2b): Pre-seal gate added at STEP 8 — before proceeding to STEP 8.5, verify §9 DoQ Date and PO Date fields are both non-blank in verification_report.md; surface for completion if blank; do not seal until both filled. Authority: Head of Specs Team (ST-12, 2026-04-06). [Backfill entry — not present at time of apply.] |
| 1.7 | 2026-03-31 | LL-v2.3-CL-03: STEP 3 — canonical spec Known Deviations sync note added. After creating a backlog item for any P1–P3 deviation, verify the canonical spec has a Known Deviations section entry for this deviation; create if absent. Prevents post-ship closure STEP 5 from being the first propagation gate (recurred v2.2 and v2.3). Authority: Head of Specs Team (post-ship closure 2026-03-24__release-v2.3). |
| 1.6 | 2026-03-24 | LL-CL-v22-01: STEP 3 deviation register — backlog reference synchronisation note added. When a new backlog item is created for a deviation, the canonical spec deviation note `Backlog reference:` field must be updated to the new item ID in the same session. Prevents stale references at post-ship closure. Authority: Head of Specs Team (lessons learnt closure 2026-03-21__release-v2.2). |
| 1.4 | 2026-03-11 | IMP-14: STEP 5.3 added — `test_scenario_gaps` structured table in `verification_report.md §6`; fields: gap_id, EPIC, description, qualifying_reason, disposition (backlog_item_created | not_applicable | deferred); all gaps must have a disposition before report seals (Phase 4 exit criterion). §8 completion condition updated. IMP-15: STEP 4.3 added — stale parked items detection; items parked in 3+ consecutive cycle backlog slices surfaced for mandatory PO disposition; recorded in `verification_report.md §5`; detection only — does not block verification status. |
| 1.3 | 2026-03-10 | IMP-54: §5 Write Scope — `lessons_learnt_cycle.md` added (append-only, Phase 4 section; create if absent). STEP 8.5 added — lessons learnt Phase 4 append via `lessons_learnt_prompt.md §3.4`; output: `lessons_learnt_cycle.md` Phase 4 section; idempotency guard built into prompt §3.4; hard gate before STEP 9. STEP 10 commit: `lessons_learnt_cycle.md` added. §8 completion condition: Phase 4 section appended condition added. |
| 1.1 | 2026-03-07 | **`amended_backlog_slice_path` handling added.** §4 backlog slice source-of-truth rule added. STEP -1.1 extended: checks `amended_backlog_slice_path` in `.claude_current_state.json`; cross-references against `execution_state.json.backlog_slice_source`; flags disagreement before proceeding. STEP 1 updated: iterates over the authoritative slice (not hardcoded `stage4_backlog_slice.md`). §5 write scope: amended backlog slice added to must-not-modify list. `verification_report.md` §1 template: `Backlog slice source` field added. §9 invariant added. **`Verification_Failed` status corrected to `Not_Verified`.** STEP 9 `Not_Verified` path: `status` field in `.claude_current_state.json` changed from `Verification_Failed` to `Not_Verified`, consistent with guide §9.4 state machine and lifecycle table. **Deferred execution blockers acknowledged (STEP 4.2, new).** STEP 4 split into §4.1 (outstanding items, unchanged) and §4.2 (deferred execution blockers). §4.2 reads `deferred_execution_blockers` from `state.json`, dispositions each blocker, and records outcomes in `verification_report.md` §5. Informational only — does not block verification status. Sign-off blocks in `verification_report.md` §9 updated: DoQ checklist and PO checklist each add a deferred blocker acknowledgement line. §8 completion condition updated. §9 invariant updated. **Escalation subroutine added.** `verification_escalations.md` added to §5 write scope. Escalation subroutine added (callable, ID prefix `ESC-VER-YYYYMMDD-nn`). STEP 3: P0 deviation now files escalation record. STEP 9 Not_Verified path: references escalation records in halt report. STEP 10 commit: `verification_escalations.md` added. §8 completion condition updated. **Guide fix required:** §9 source prompt v1.0 → v1.1; §14 Verification Engine Source → v1.1; `Not_Verified` confirmed as the canonical status string (not `Verification_Failed`). |
| 1.0 | 2026-03-03 | Initial version. |