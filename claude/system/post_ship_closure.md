**Owner:** Head of Specs Team
**Status:** Active
**Version:** 2.0
**Last Updated:** 2026-03-16
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md
**Process Reference:** docs/team_skills/pmo/processess/post-ship_closure.md (v2.0)

---

# Post-Ship Closure Engine — Governance Prompt

(Evidence-Driven, Document-Sweeping, Lessons-Applying, Cycle-Sealing)

---

## 1. Purpose

Close all planning, operational, and governance documents for a completed release cycle, apply lessons learnt, and confirm the cycle is fully sealed before the next one opens.

This engine:
- Verifies Phase 4 completion and confirmed verification status
- Writes the changelog entry for the shipped release
- Updates the roadmap, backlog, scope, and decisions documents to reflect the shipped state
- Confirms canonical spec deviation entries are compliant
- Reconciles operational and index documents
- Reviews all lessons learnt records and applies immediate process improvement actions
- Produces a `lessons_learnt_closure.md` record via `lessons_learnt_prompt.md §3.5`
- Produces a closure record and communicates completion to the Product Owner and Head of Specs Team
- Updates global state to confirm the cycle is fully sealed

This routine does **NOT**:
- Re-run or re-evaluate Phase 4 verification
- Rebalance the roadmap or reprioritise the backlog
- Override QA or Product Owner sign-offs
- Open the next planning cycle (that is the Product Owner's decision after this routine confirms closure)

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
run post-ship [--cycle "<cycle_id>"] [--mode "strict|standard"] [--dry-run]
```

Rules:
- `--cycle` optional: if omitted, load `active_cycle` from `.claude_current_state.json`. If absent, halt.
- `--mode` optional:
  - `strict`: halt on any missing document, incomplete field, or unresolved action item
  - `standard` (default): proceed with flags on minor gaps; still halt on hard gates
- `--dry-run` optional: read all inputs and produce a full closure plan — listing every write that would be made, every step outcome, and any flags — without making any writes, state updates, or commits. Dry-run output is the deliverable; the routine ends after producing it.
- Invocation must start with `run post-ship` (case-insensitive match allowed)

If invocation is not exact, do not run. Treat as conversational.

Apply the Lifecycle Guard (valid from-states: `Verified`, `Verified_with_deviations`) per `claude/system/shared_standards.md §10` before executing any step.

**Who issues this command:** The PMO Lead persona, immediately after Phase 4 completes with a passing status.

**Tool call budget:** This routine typically requires 15–35 tool calls. Proceed through steps without asking for confirmation unless a hard gate fires.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Binding governance stack (precedence order):

1. `claude/charter/team_charter.md`
2. `claude/charter/document_lifecycle_guide.md`
3. `claude/strategy/strategy_rules.md`
4. Role charters in `claude/agents/`

This routine may not override any of the above.

---

## 4. Source-of-Truth Closure Inputs

| Input | Location | Required |
|-------|----------|---------|
| Closure state | `claude/cycles/<cycle_id>/closure_state.json` | Created at STEP 0; read on resume |
| Global state | `.claude_current_state.json` | Hard gate |
| Verification report | `claude/cycles/<cycle_id>/verification_report.md` | Hard gate |
| Sprint close record | `claude/cycles/<cycle_id>/sprint_close.md` | Hard gate |
| Execution state (sealed) | `claude/cycles/<cycle_id>/execution_state.json` | Hard gate |
| Backlog slice (sealed) | See note below — may be amended | Hard gate |
| Release Planning lessons | `claude/cycles/<cycle_id>/lessons_learnt.md` | Required |
| Sprint Execution + Verification + Amendment lessons | `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` | Required (Phase 3 and Phase 4 sections; Amendment sections if any) — replaces standalone `lessons_learnt_execution.md` and `lessons_learnt_verification.md` |
| QA evidence logs | `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (one per merged EPIC) | Required |
| System status report | `docs/System_status_report.md` | Required |
| Roadmap | `claude/roadmap/current_roadmap.md` | Required |
| Backlog | `claude/backlog/backlog.md` | Required |
| Changelog | `docs/product/changelog.md` | Required (create if absent) |
| Canonical specs | Paths from `spec_references` in `execution_state.json` | Required (deviation check) |
| Specs Index | `docs/specs/Specs_Index.md` | Required |

**Backlog slice source-of-truth rule:** At STEP 0, check `.claude_current_state.json` for `amended_backlog_slice_path`. If present and non-empty, that file is the authoritative backlog slice — use it throughout in place of `stage4_backlog_slice.md`. Cross-reference against `execution_state.json.backlog_slice_source` to confirm both pointers agree. If they disagree: flag to the PMO Lead before proceeding. If `amended_backlog_slice_path` is absent or empty, use `stage4_backlog_slice.md`.

---

## 5. Write Scope Restriction (Hard Gate)

**Dry-run exception:** If `--dry-run` is active, none of the permitted writes below may be made. The routine produces a closure plan only.

During this routine you may write only to:

- `docs/product/changelog.md` (append new version entry)
- `claude/roadmap/current_roadmap.md` (status update, version headers, ✅ Complete annotation with ship date and `cycle_id`, release summary table update — all per STEP 2)
- `claude/backlog/backlog.md` (mark shipped items complete; add missing Phase 4 items; no other changes)
- Scope document at `docs/product/scope/scope--{id}-{slug}.md` (status → Superseded only)
- Decisions record at `docs/product/decisions/{id}-{slug}.md` (status → Superseded only)
- Canonical spec files (deviation note compliance fixes only — missing required fields per §3 Known Deviation Standard; no other spec edits permitted; the document owner must be notified of any fields added to their spec by this routine — record in closure record §6)
- `claude/cycles/<cycle_id>/closure_escalations.md` (create if escalations raised during closure — format per `shared_standards.md §4`; ID prefix `ESC-CLOSE-YYYYMMDD-nn`)
- `docs/System_status_report.md` (reconciliation only — correct stale notes)
- `docs/operations/validation_system.md` (reconciliation only — correct stale notes)
- `docs/specs/Specs_Index.md` (mark resolved items; add new gaps identified during delivery)
- Templates and prompt files where a lessons learnt action specifies an immediate fix (version bump required)
- `claude/cycles/<cycle_id>/lessons_learnt_closure.md` (create via STEP 8.5)
- `claude/cycles/<cycle_id>/closure_record.md` (create at close)
- `claude/cycles/<cycle_id>/closure_state.json` (create at STEP 0; update at each step completion)
- `.claude_current_state.json` (status update only)

You must **not** modify:
- `claude/cycles/<cycle_id>/verification_report.md` (sealed)
- `claude/cycles/<cycle_id>/sprint_close.md` (sealed)
- `claude/cycles/<cycle_id>/execution_state.json` (sealed)
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed)
- `claude/cycles/<cycle_id>/amendments/*/amended_backlog_slice.md` (sealed)
- `claude/cycles/<cycle_id>/sprint_backlog.md` (sealed)
- `claude/cycles/<cycle_id>/lessons_learnt.md` (read-only — do not edit, only apply)
- `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (read-only — do not edit, only apply; replaces `lessons_learnt_execution.md` and `lessons_learnt_verification.md`)
- `claude/strategy/strategy_rules.md`
- Any governance document not listed in the permitted write scope above

Violation → halt.

---

## 6. Required Authority Roles

Minimum required roles for this routine:

- PMO Lead
- Product Owner
- Head of Specs Team

Verify: each role has an agent file in `claude/agents/` containing `**Role:** <Role Name>`. If any required role is missing or malformed: halt.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

Purpose: fail fast before any writes begin.

Shared standards (escalation format, halt report format, identifier conventions): `claude/system/shared_standards.md`.

### -1.1 Status Check

Read `.claude_current_state.json`:
- `status` must be `Verified` or `Verified_with_deviations`
- `next_cycle_unblocked` must be `true`
- If `status` is anything else: halt — Phase 4 has not completed. Phase 4 must reach a passing status before post-ship closure can run.

### -1.2 Execution State Sealed

Read `claude/cycles/<cycle_id>/execution_state.json`:
- `sealed` must be `true`
- If not sealed: halt — the execution record is not closed.

### -1.2A Sprint Close Readiness Statement (Hard Gate)

Read `claude/cycles/<cycle_id>/sprint_close.md`:
- Locate the **Verification readiness statement** (required field per execution_prompt.md §5.3).
- All three readiness fields must be `Yes`:
  - `All spec references populated: Yes`
  - `All deviations filed: Yes`
  - `QA evidence logs complete: Yes`
- If any field is `No` or absent: halt — the sprint is not ready for post-ship closure. Surface the failing field(s) to the PMO Lead and request resolution before re-invoking.

### -1.3 Verification Report Present and Signed

Read `claude/cycles/<cycle_id>/verification_report.md`:
- Confirm `§9 Sign-off Block` is present
- Confirm `Signed off by: Director of Quality` with a date
- Confirm `Accepted by: Product Owner` with a date
- If either sign-off is blank: halt — verification is not complete.

### -1.4 Required Files Present

Verify all files in Section 4 exist (backlog slice subject to the source-of-truth rule resolved in STEP 0). If any are missing: halt and report exactly which.

### -1.5 Required Authority Roles Exist

Verify agent files per Section 6. If any missing: halt.

### -1.6 Write Permission Test

If `--dry-run` is NOT active: create a temporary marker file in `claude/cycles/<cycle_id>/` and confirm it can be written. Remove it. If write fails: halt.

If `--dry-run` is active: skip this check.

---

## STEP 0 — Load Release Context

**Closure state (first action — before any other reads):**

Read `claude/cycles/<cycle_id>/closure_state.json` if it exists:
- If it exists and `status = Closed`: this cycle is already closed — halt with message "Cycle already closed."
- If it exists and `status = In_Progress`: this is a resume. Skip all steps whose `steps.*` value is `pass`. Resume from the first `not_started` or `fail` step.
- If it does not exist: create it now with the schema below (fresh run).

```json
{
  "cycle_id": "<cycle_id>",
  "release": "<vX.Y>",
  "status": "In_Progress",
  "mode": "strict|standard",
  "dry_run": false,
  "started_utc": "<ISO-8601 UTC>",
  "last_updated_utc": "<ISO-8601 UTC>",
  "steps": {
    "preflight": "pass",
    "step_0_context": "not_started",
    "step_1_changelog": "not_started",
    "step_2_roadmap": "not_started",
    "step_3_backlog": "not_started",
    "step_4_scope_decisions": "not_started",
    "step_5_deviation_compliance": "not_started",
    "step_6_operational_docs": "not_started",
    "step_7_specs_index": "not_started",
    "step_8_lessons_learnt": "not_started",
    "step_8_5_lessons_closure": "not_started",
    "step_9_closure_record": "not_started",
    "step_10_global_state": "not_started",
    "step_11_manage_roadmap": "not_started",
    "step_12_groom_backlog": "not_started",
    "step_13_commit": "not_started"
  },
  "closure_status": null
}
```

If `closure_state.json` cannot be written: halt immediately.

**Backlog slice resolution (second action):** Check `.claude_current_state.json` for `amended_backlog_slice_path`:
- If present and non-empty: this is the authoritative backlog slice for this run. Verify the file exists — if not, halt.
- If absent or empty: `stage4_backlog_slice.md` is the authoritative slice.

Cross-reference the identified path against `execution_state.json.backlog_slice_source`. If they disagree: flag to PMO Lead before proceeding. Record the authoritative path as `backlog_slice_source` in the closure record §1.

Extract from the verified inputs (read targets — load only the specified sections, not the full document):

1. From `verification_report.md` — **read: `§1 verification_status` and `§4 deviation register` only.** Extract: release version (`vX.Y`), verification status (`Verified` / `Verified_with_deviations`), deviation register, QA summary.
2. From `execution_state.json` — **read: `epics` outcome map only** (not full state schema). Extract: merged EPICs (with EPIC IDs and descriptions), all ST items with `spec_references`, `deviations_filed` flags, returned-to-backlog items, `backlog_slice_source`.
3. From `sprint_close.md` — **read: verification readiness statement and deviations list only** (not full narrative sections). Extract: sprint goal, deviations filed list, outstanding delegated items, verification readiness statement.
4. From `current_roadmap.md`: the roadmap item ID and feature name for this release.
5. From `backlog.md`: identify all items with this `cycle_id` added by Phase 4 (returned items, P2/P3 deviation items, test scenario gap items) — these must all be present before STEP 3 can pass.

Confirm: release version, feature name, `cycle_id`, ship date (use today if not recorded elsewhere), and Product Owner sign-off date are all resolvable. If any cannot be determined: halt in `strict` mode; flag and proceed with `[UNKNOWN]` placeholder in `standard` mode.

Update `closure_state.json`: `steps.step_0_context = pass`, `last_updated_utc = <now>`

**If `--dry-run` is active:** After completing context load, produce the full closure plan (listing every step, every write that would be made, every flag) and end the routine. Do not proceed to STEP 1.

---

## STEP 1 — Changelog Entry (Hard Gate)

Write a new versioned entry to `docs/product/changelog.md`.

### 1.1 Entry Structure (Required)

```markdown
## v<X.Y> — <feature name> — <ship date>
Cycle: <cycle_id>
Verified: <Verified | Verified_with_deviations>
Verification report: claude/cycles/<cycle_id>/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-xx | <description> | <spec file#section(s)> |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-ref | P1/P2/P3 | <one line> | PO / PO + DoQ |

*(If no deviations accepted: "None")*

### Tech backlog items shipped
- [ST-xx] <title> — <one line description>

*(If none: "None")*

Sign-off: Product Owner — <date>
QA sign-off: Director of Quality — <date>
```

### 1.2 Entry Rules

- One entry per release version. Do not create duplicate entries.
- All merged EPICs must appear with their EPIC ID and at least one spec section reference.
- All accepted P1/P2 deviations from the deviation register must appear.
- P3 deviations need not appear individually — they may be summarised as "N minor deviations — see verification_report.md".
- Tech backlog items that shipped alongside the primary feature must appear as a distinct sub-section.
- Update `Last Updated` on `docs/product/changelog.md` to today's date.

**Failure condition:** If `docs/product/changelog.md` does not exist: create it with a standard header (Owner: PMO Lead, Class: Operational Record, Status: Active) and then add the entry. A ship without a changelog entry is not recorded — this is a hard gate.

Update `closure_state.json`: `steps.step_1_changelog = pass`, `last_updated_utc = <now>`

---

## STEP 2 — Roadmap Update

Update `claude/roadmap/current_roadmap.md`:

1. Locate the roadmap entry for this release (match by version label or feature name from STEP 0).
2. Mark it **✅ Complete** with the ship date and `cycle_id` reference.
3. Update the "Current Version" header to the shipped version.
4. Update the "Next planned release" header to the next version (if known; leave as `[TBD]` if not).
5. If the release contained P0/P1 quality gate items (confirmed in `verification_report.md`): mark those complete within their roadmap section.
6. Update the release summary table if present.
7. Update `Last Updated` to today's date.

**Failure condition (hard gate in `strict` mode; flag in `standard`):** Roadmap entry still shows Planned or In Progress after this step. Stale roadmap status will cause Phase 1 (Roadmap Rebalance) to misread the current state.

Update `closure_state.json`: `steps.step_2_roadmap = pass`, `last_updated_utc = <now>`

---

## STEP 3 — Backlog Reconciliation (Hard Gate)

Update `claude/backlog/backlog.md`. All reconciliation is performed against the authoritative backlog slice identified in STEP 0.

### 3.1 Mark shipped items complete

For every ST item in `execution_state.json` with status `done` or `merged`:
- Locate the corresponding entry in `backlog.md`.
- Mark it **✅ COMPLETE** with closure date and `cycle_id` reference.
- If the item is not in `backlog.md`: record the gap in the closure record (permitted to add a note; do not silently skip).

### 3.2 Confirm Phase 4 additions are present

Cross-reference against items added by the Phase 4 engine:
- Returned-to-backlog items (from `sprint_close.md` "Items Returned to Backlog" section)
- P2/P3 deviation items (from `verification_report.md §4`)
- Test scenario gap items (from `verification_report.md §6`)

For each: confirm a `backlog.md` entry exists with the `cycle_id` reference. If any are missing: **add them now** (permitted write). Record each addition in the closure record.

### 3.3 Confirm next-release items are tagged

Items in `backlog.md` that have been assigned to the next release (per sprint close or verification report): confirm they have a target release note. Flag any that are missing one.

Update `Last Updated` on `backlog.md` to today's date.

### 3.4 Stale Parked Items Disposition Check (IMP-15)

Identify all items in `backlog.md` marked `parked` that carry a `cycle_id` reference from 3 or more completed cycles (i.e. the item was parked in this cycle's authoritative backlog slice, and also appeared as parked in the 2 prior completed cycles' backlog slices).

For each stale parked item identified:
1. Record in the closure record §6 Outstanding Actions:
   ```
   Outstanding action: [ST-xx / BLG-xx] "<title>" has been parked for 3+ consecutive cycles.
   PMO Lead must obtain explicit Product Owner disposition (Advance, Reject, or explicit re-park
   with written rationale) before the next release plan opens.
   Owner: PMO Lead / Product Owner
   Deadline: Before `plan release` for next cycle
   ```
2. Add a note to `backlog.md` on the parked item: `[STALE — PO disposition required before next release plan]`.
3. Do not remove or resolve the item here — disposition is a Product Owner decision.

If no stale parked items are found: note "No stale parked items" in the closure record and continue.

**Failure condition:** Any shipped item still shown as open after this step. Any Phase 4 addition unaccounted for. Any item in the authoritative backlog slice with no traceable outcome in `backlog.md`.

Update `closure_state.json`: `steps.step_3_backlog = pass`, `last_updated_utc = <now>`

---

## STEP 4 — Scope and Decisions Documents

### 4.1 Scope document

Locate: `docs/product/scope/scope--{id}-{slug}.md` (derive the ID and slug from the roadmap item).

Update:
- Status: `Active` → `Superseded`
- Add supersession note:
  ```
  Superseded by: v<X.Y> ship — <ship date>
  Changelog: docs/product/changelog.md#v<X.Y>
  Verification report: claude/cycles/<cycle_id>/verification_report.md
  Cycle: <cycle_id>
  ```
- Update `Last Updated` to today's date.

**Failure condition:** Scope document still Active after ship. Per lifecycle guide §4: scope documents must be updated to Superseded when the feature ships.

If the scope document cannot be located: flag in `strict` mode (halt); flag and continue in `standard` mode — record in closure record as an outstanding action for the PMO Lead to resolve manually.

### 4.2 Decisions record

Locate: `docs/product/decisions/{id}-{slug}.md`

Update:
- Status: `Active` → `Superseded`
- Add supersession note referencing changelog entry and `cycle_id`
- Update `Last Updated` to today's date.

**Note on Accepted Risk decision records:** `AR-<release>-<cycle_id>-<esc_id>.md` files are Operational Records (Class 3) — they are permanent and must **not** be marked Superseded. Confirm they are filed and linked from the changelog entry.

If the decisions record cannot be located: same flag behaviour as scope document.

**N/A condition:** If no decisions document exists for this release AND no decisions with options analysis or accepted risk were made this cycle, mark STEP 4.2 as N/A — no decision record required. Document the rationale in the closure record (§6 Outstanding Actions or §5 Lessons Learnt Action Summary as appropriate). Do not flag as a missing artefact in this case.

Update `closure_state.json`: `steps.step_4_scope_decisions = pass | not_applicable`, `last_updated_utc = <now>`

---

## STEP 5 — Canonical Spec Deviation Compliance Check

For each deviation listed in `sprint_close.md` "Deviations filed this sprint":

1. Locate the deviation entry in the referenced canonical spec file (filed there during Phase 3 execution per §3.1.A step 10 of the execution prompt).
2. Confirm the entry contains all required fields per §3 Known Deviation Standard:
   - Description
   - Canonical requirement
   - Priority (P0–P3)
   - Target resolution release
   - Owner
   - Backlog reference
3. If any required field is missing:
   - In `strict` mode: halt and list exactly which fields are missing for which deviations.
   - In `standard` mode: add the missing fields now (permitted write — deviation compliance only) and record the correction in the closure record.
4. Confirm P3 deviations have corresponding backlog items (from STEP 3.2 check). If missing: add now.
5. Confirm accepted P1/P2 deviations appear in the changelog entry (STEP 1). If not: add them now.

**Failure condition (hard gate):** Any deviation entry in a canonical spec missing required fields after this step. Non-compliant deviation notes render the spec non-compliant.

Update `closure_state.json`: `steps.step_5_deviation_compliance = pass`, `last_updated_utc = <now>`

---

## STEP 6 — Operational Documents Reconciliation

For each of the following documents, read the current content and check for stale references to this release's features:

- `docs/System_status_report.md` — confirmed current by Phase 4, but verify the section for this `cycle_id` reflects the final verified status (not "pending verification"). Correct if needed.
- `docs/operations/validation_system.md` — check metric counts, expected values, and example outputs. Update any entries that reference "planned" or "backlog" behaviour that has now shipped.

If other operational documents are referenced in `execution_state.json` spec references: check those too for stale notes.

Update `Last Updated` on any document that is modified.

Record all corrections in the closure record. If a document is outside the write scope (e.g. a Class 1 spec that is not being corrected for deviation compliance): flag for the document owner rather than editing.

Update `closure_state.json`: `steps.step_6_operational_docs = pass | not_applicable`, `last_updated_utc = <now>`

---

## STEP 7 — Specs Index Review

Read `docs/specs/Specs_Index.md`:

### 7.1 Resolve closed items

For each item in Section 6 (Pending Spec Work) and Section 7 (Open Compliance Issues):
- Cross-reference against this delivery: did any shipped ST items or deviation filings resolve a listed item?
- If yes: mark it resolved with date and `cycle_id`.

### 7.2 Add new gaps

From `verification_report.md §6` (Test Coverage Assessment) and `qa_evidence_EPIC-xx.md` notes: identify any new spec gaps or compliance issues surfaced during this delivery that are not yet in the Specs Index.
- Add each as a new entry in the appropriate section.

Update `Last Updated` on `docs/specs/Specs_Index.md` to today's date if any changes were made.

Update `closure_state.json`: `steps.step_7_specs_index = pass`, `last_updated_utc = <now>`

---

## STEP 8 — Lessons Learnt Review and Application

Read all available lessons learnt records for this cycle — **read action item sections only (not full prose)**:

| Record | Location | Read target |
|--------|----------|-------------|
| Release Planning lessons | `claude/cycles/<cycle_id>/lessons_learnt.md` | Action items section / classification table only |
| Sprint Execution + Verification + Amendment lessons | `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` | All phase sections (Phase 3, Phase 4, and any Amendment sections) — structured table read (`lessons_learnt_prompt.md §4.2` format) |

For each action item in all records, classify it:

| Class | Criteria | Action |
|-------|----------|--------|
| `immediate` | Can be resolved by updating a template, prompt, or process document right now | Apply now; bump version of the modified document; record in closure record |
| `deferred` | Requires changes that depend on the next cycle's context, or needs more than one session to implement | Record in closure record with owner and target cycle |
| `decision_required` | Requires a named authority to decide (e.g. authority boundary change, strategy question, new role) | Surface to the relevant owner with a clear decision question and 72-hour deadline; record in closure record |

**Immediate action rule:** If a lessons learnt action specifies updating a template or prompt and that update can be made without ambiguity, make it now within the permitted write scope. Do not defer what can be done immediately.

**Filing without reviewing is equivalent to skipping.** Every action item must have a recorded disposition (`immediate`, `deferred`, or `decision_required`) in the closure record. Blank or unreviewed items are non-compliant.

Produce a consolidated action summary:
- Immediate actions applied: `N` (list each: document updated, version bumped)
- Deferred to next cycle: `N` (list each: action, owner, target cycle)
- Escalated for decision: `N` (list each: question, owner, 72-hour deadline from today)

Update `closure_state.json`: `steps.step_8_lessons_learnt = pass`, `last_updated_utc = <now>`

---

## STEP 8.5 — Produce Lessons Learnt Closure Record

Invoke `lessons_learnt_prompt.md §3.5` using the consolidated action summary produced in STEP 8 as input.

> **Note (sequencing):** `closure_record.md` is produced in STEP 9 — it does not yet exist at the time STEP 8.5 executes. The input to `lessons_learnt_prompt.md §3.5` is the STEP 8 consolidated action summary (immediate actions applied, deferred items list, and any escalations). The §6 Outstanding Actions table in `closure_record.md` is derived from the same deferred items list. Do not wait for `closure_record.md` before producing `lessons_learnt_closure.md`.

The lessons learnt prompt will create: `claude/cycles/<cycle_id>/lessons_learnt_closure.md`

This record covers:
- Closure-phase observations (document gaps surfaced, deviation compliance corrections, spec index gaps added)
- The consolidated action summary from STEP 8 (all three records reviewed, classified, and applied)
- Any process improvements applied immediately during this run (with document refs and version bumps)
- Carry-forward items for the next cycle

Do not proceed to STEP 9 until `lessons_learnt_closure.md` exists and is non-empty. If the lessons learnt prompt cannot be invoked: produce the file directly using the structure from `lessons_learnt_prompt.md §3.5`, record the deviation in the closure record §6.

Update `closure_state.json`: `steps.step_8_5_lessons_closure = pass`, `last_updated_utc = <now>`

---

## STEP 9 — Produce Closure Record

Create: `claude/cycles/<cycle_id>/closure_record.md`

Lifecycle header:
```
Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: <date>
Cycle: <cycle_id>
```

Body (seven sections in order):

**§1 — Closure Status**
```
Status: Closed | Closed_with_actions
Release: v<X.Y> — <feature name>
Ship date: <date>
Cycle: <cycle_id>
Verification status: <Verified | Verified_with_deviations>
Backlog slice source: <file path used — original or amended>
Closure run: <ISO-8601 UTC>
```

**§2 — Documents Updated** — for each step, confirm status:

| Step | Document | Action Taken | Status |
|------|----------|--------------|--------|
| 1 | docs/product/changelog.md | Entry written for v<X.Y> | ✅ |
| 2 | claude/roadmap/current_roadmap.md | Marked ✅ Complete; version headers updated | ✅ |
| 3 | claude/backlog/backlog.md | N items marked COMPLETE; N Phase 4 additions confirmed | ✅ |
| 4 | Scope document | Status → Superseded | ✅ / ⚠ not found |
| 5 | Decisions record | Status → Superseded | ✅ / ⚠ not found / N/A |
| 6 | Canonical specs | N deviations checked; N fields corrected | ✅ |
| 7 | Operational docs | N corrections made | ✅ / N/A |
| 8 | Specs Index | N items resolved; N gaps added | ✅ |
| 8.5 | lessons_learnt_closure.md | Created via lessons_learnt_prompt.md §3.5 | ✅ |

**§3 — Backlog Additions This Run** — any items added to `backlog.md` by this routine (Phase 4 items that were missing, new gaps). List each with backlog ref.

**§4 — Deviation Compliance Summary** — list of deviations checked, any fields corrected, all now compliant: Yes / No (with detail if No).

**§5 — Lessons Learnt Action Summary** — from STEP 8. Full three-way breakdown (immediate / deferred / decision_required) with detail per item. References all records reviewed (Release Planning, Execution, Verification).

**§6 — Outstanding Actions** — any items that could not be completed by this routine (e.g. scope document not found, document owner unresponsive, lessons_learnt_prompt.md could not be invoked). Required table format:

| # | Description | Owner | Deadline | Escalation path | Resolution |
|---|-------------|-------|----------|-----------------|------------|
| 1 | \<description\> | \<role\> | \<date or "Before next cycle"\> | \<escalation path\> | *(complete when resolved)* |

If there are no outstanding actions: write "None — all steps completed."

**§7 — Closure Confirmation**
```
Post-ship closure complete — <cycle_id> — <date>
Release: v<X.Y> — <feature name>
Verification status: <Verified | Verified_with_deviations>
Lessons learnt applied: <N immediate> | <N deferred> | <N escalated>
Outstanding actions carried forward: <list or "none">
Next cycle may now open.
```

Update `closure_state.json`: `steps.step_9_closure_record = pass`, `last_updated_utc = <now>`

---

## STEP 10 — Global State Update (Hard Requirement)

Update `.claude_current_state.json`:

```json
{
  "status": "Closed",
  "closure_record": "claude/cycles/<cycle_id>/closure_record.md",
  "closure_status": "Closed | Closed_with_actions",
  "post_ship_complete": true,
  "completed_cycle_count": "<prior value + 1>",
  "last_sync_utc": "<now>"
}
```

**`completed_cycle_count` rule:** Read the current value from `.claude_current_state.json`. If absent, treat as `0`. Write the value incremented by 1. This counter tracks the total number of fully closed cycles for meta-review cadence tracking (Phase 1 STEP 11 triggers meta-review every third completed cycle).

Surface §7 Closure Confirmation to the user for communication to the Product Owner and Head of Specs Team.

If any outstanding actions remain in §6: set `closure_status = Closed_with_actions`. The next cycle may still open — outstanding actions do not block it unless a hard gate condition is unmet.

Update `closure_state.json`:
```json
{
  "steps": { "step_10_global_state": "pass" },
  "status": "Closed",
  "closure_status": "Closed | Closed_with_actions",
  "last_updated_utc": "<now>"
}
```

---

## STEP 11 — Roadmap Document Management (Mandatory)

Invoke `claude/system/roadmap_management_prompt.md` inline.
Pass through `--dry-run` if `run post-ship` was invoked with `--dry-run`.
Output: manage_roadmap run log at `claude/cycles/<cycle_id>/manage_roadmap_<YYYYMMDD>.md`.
On completion: confirm `last_manage_roadmap_utc` written to `.claude_current_state.json`.
Update `closure_state.json`: `{"step_11_manage_roadmap": "complete", "last_updated_utc": "<now>"}`.

## STEP 12 — Backlog Document Management (Mandatory)

Invoke `claude/system/backlog_management_prompt.md` inline.
Pass through `--dry-run` if `run post-ship` was invoked with `--dry-run`.
Output: backlog health report at `claude/backlog/backlog_health_<YYYYMMDD>.md`.
On completion: confirm `last_groom_backlog_utc` written to `.claude_current_state.json`.
Update `closure_state.json`: `{"step_12_groom_backlog": "complete", "last_updated_utc": "<now>"}`.

---

## STEP 13 — Commit

**Push-before-pull rule (required):** Do NOT perform a `git pull` or `git merge` from the remote branch before pushing. Push local governance commits first. If the push is rejected due to divergent history, investigate the cause — do not run `git pull` automatically, as a remote merge commit may overwrite or reorder governance commits. Resolve divergence manually with PMO Lead approval before retrying the push.

Commit all artefacts created or modified by this routine:

```
git add docs/product/changelog.md
git add claude/roadmap/current_roadmap.md
git add claude/backlog/backlog.md
git add docs/product/scope/scope--*.md       (if modified)
git add docs/product/decisions/*.md          (if modified)
git add docs/System_status_report.md         (if modified)
git add docs/operations/validation_system.md (if modified)
git add docs/specs/Specs_Index.md            (if modified)
git add <any template or prompt files updated by lessons learnt actions>
git add claude/cycles/<cycle_id>/lessons_learnt_closure.md
git add claude/cycles/<cycle_id>/closure_record.md
git add claude/cycles/<cycle_id>/closure_state.json
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Post-ship closure complete: <cycle_id> — v<X.Y>"
git push origin <current-branch>
```

If git operations are unavailable: output the exact files to stage and the commit message. Mark as "Ready to commit."

Update `closure_state.json`: `steps.step_13_commit = pass`, `last_updated_utc = <now>`

---

## 7. Completion Condition

The run is complete only if:

- `closure_record.md` exists with all 7 sections
- `lessons_learnt_closure.md` exists and follows the structure from `lessons_learnt_prompt.md §3.5`
- Changelog entry written and complete for this release version
- Roadmap entry marked ✅ Complete
- All shipped backlog items marked COMPLETE; all Phase 4 additions confirmed present; authoritative backlog slice (original or amended) fully reconciled
- Scope and decisions documents marked Superseded (or outstanding action filed if not found)
- All deviation entries in canonical specs have required fields
- Operational documents reconciled
- Specs Index reviewed and updated
- All lessons learnt records reviewed; every action item has a disposition
- `.claude_current_state.json` updated with `post_ship_complete = true` and `status = Closed`
- STEP 13 commit complete (or commit manifest produced)

**Dry-run:** Run is complete when the closure plan is produced after STEP 0. No files written, no state updated, no commit.

---

## 8. Closure Status Values

| Status | Meaning | Next cycle? |
|--------|---------|-------------|
| `Closed` | All steps complete; no outstanding actions | Open immediately |
| `Closed_with_actions` | All steps complete; minor outstanding actions carried forward (e.g. scope doc not found, deferred lessons learnt items) | Open — outstanding actions tracked in closure record |

There is no `Failed` state for post-ship closure. If a hard gate fires before completion, the routine halts and reports. Re-issue `run post-ship --cycle "<cycle_id>"` once the condition is resolved — the engine resumes from the first incomplete step.

---

## 9. Governance Invariants

- **No re-verification.** This engine reads sealed Phase 4 artefacts. It does not re-assess what passed or failed.
- **No scope revision.** The execution state is sealed. The engine records what shipped; it does not alter it.
- **Write scope is strictly bounded.** Status updates, changelog entries, and deviation compliance fixes only. No content changes to specs, strategies, or canonical documents beyond the permitted scope.
- **Lessons learnt must be reviewed, not just filed.** Every action item requires a disposition. Deferred is acceptable; unreviewed is not.
- **Immediate lessons learnt actions are non-deferrable.** If an action can be applied now (template fix, prompt correction), it must be. Do not defer what can be done immediately.
- **Outstanding actions do not block the next cycle** — but they must be recorded and owned. Nothing is silently dropped.
- **Delivery pressure does not override closure steps.** The changelog, roadmap, and backlog must be updated before the next cycle opens, regardless of timeline.
- **Dry-run produces no side effects.** No files written, no state changed, no commit made. The closure plan is the sole output.
- **Amendment slice supersedes original.** If `amended_backlog_slice_path` is set, backlog reconciliation (STEP 3) runs against that file. Reconciling against the original slice when an amendment has sealed is a process integrity failure.

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.0 | 2026-03-16 | Post-ship closure v1.10 deferred patch applied. STEP 8.5: sequencing clarification note added — `closure_record.md` is produced in STEP 9 and is not available at STEP 8.5 execution time; `lessons_learnt_closure.md` must be produced from STEP 8 consolidated action summary context; §6 Outstanding Actions in `closure_record.md` is derived from the same deferred items list. Prevents incorrect sequencing where STEP 8.5 waits for STEP 9 output. |
| 1.9 | 2026-03-14 | AUD-2026-03-13-004: STEP 11 (Roadmap Document Management — mandatory) and STEP 12 (Backlog Document Management — mandatory) added. Both invoke their respective management prompts inline and pass through --dry-run. Closes Phase 1M skip gap — manage roadmap + groom backlog now run every cycle regardless of whether Phase 1 was executed. Former STEP 11 (Commit) renumbered STEP 13. closure_state.json schema updated: step_11_manage_roadmap, step_12_groom_backlog, step_13_commit. |
| 1.8 | 2026-03-11 | IMP-15: STEP 3.4 added — stale parked items disposition check; identifies `backlog.md` items parked in 3+ consecutive completed cycles; records mandatory PO disposition requirement in closure record §6 Outstanding Actions; adds `[STALE — PO disposition required]` note to backlog item; does not resolve item. |
| 1.7 | 2026-03-10 | IMP-54: §4 Source-of-Truth inputs — `lessons_learnt_execution.md` and `lessons_learnt_verification.md` rows replaced with single `lessons_learnt_cycle.md` row (Phase 3 + Phase 4 + Amendment sections). §5 must-not-modify — `lessons_learnt_execution.md` and `lessons_learnt_verification.md` lines replaced with `lessons_learnt_cycle.md` (read-only). STEP 8 lessons learnt table — two rows replaced with single `lessons_learnt_cycle.md` row (all phase sections, structured table read). |
| 1.6 | 2026-03-10 | IMP-27: STEP 0 — field-level read targets added for `verification_report.md` (§1 verification_status + §4 deviation register only), `execution_state.json` (epics outcome map only), `sprint_close.md` (verification readiness statement + deviations list only). STEP 8 — `lessons_learnt` files: read action items section / classification table only (not full prose). |
| 1.5 | 2026-03-10 | IMP-42: STEP -1.2A added — sprint_close.md verification readiness statement check (all three `Yes` fields required before proceeding). IMP-34: §5 Write Scope — `current_roadmap.md` entry expanded to list all STEP 2 write actions; canonical spec entry updated to add document owner notification requirement; `closure_escalations.md` added as permitted write. IMP-50: `closure_escalations.md` added to §5 write scope (escalations during closure use this file, not `closure_record.md §6`). IMP-59: STEP 10 — `completed_cycle_count` increment added to global state write; rule documented (default 0 if absent; used for meta-review cadence tracking). IMP-12: STEP 9 §6 Outstanding Actions template — required table format added with named columns (Description, Owner, Deadline, Escalation path, Resolution); "None" path documented. |
| 1.4 | 2026-03-07 | **IMP-01 — closure_state.json for reliable resumability.** Added `closure_state.json` to §4 Source-of-Truth inputs and §5 Write Scope. Added full STEP 0 initialization/resume logic with JSON schema (fresh run creates file; resume skips completed steps; already-Closed halts). Added `closure_state.json` update lines at the end of STEP 0 through STEP 11 (each step writes its completion flag and `last_updated_utc`). STEP 11 commit list: `closure_state.json` added. `next_cycle_unblocked` guard noted in STEP 10. Consistent with resumability model used by execution and release planning engines. |
| 1.3 | 2026-03-07 | **Lifecycle Guard added.** Apply Lifecycle Guard per `shared_standards.md §10` (valid from-states: `Verified`, `Verified_with_deviations`) at §2 Invocation Rule. |
| 1.2 | 2026-03-07 | **`amended_backlog_slice_path` handling added.** §4 backlog slice source-of-truth rule added. §5 must-not-modify: amended backlog slice added. STEP 0: `amended_backlog_slice_path` read from `.claude_current_state.json` as first action; cross-referenced against `execution_state.json.backlog_slice_source`; disagreement flagged before proceeding; authoritative path recorded in closure record §1. STEP 3 intro updated: reconciliation runs against the authoritative slice. STEP 3.3 failure condition expanded. `closure_record.md` §1 template: `Backlog slice source` field added. §9 invariant added. **`lessons_learnt_closure.md` creation formalised (STEP 8.5, new).** STEP 8.5 added: invokes `lessons_learnt_prompt.md §3.5` using STEP 8 consolidated action summary as input; produces `claude/cycles/<cycle_id>/lessons_learnt_closure.md`; hard gate before STEP 9. §5 write scope: `lessons_learnt_closure.md` creation entry updated to reference STEP 8.5 explicitly. §7 completion condition: `lessons_learnt_closure.md` condition updated to reference `lessons_learnt_prompt.md §3.5` structure. §9 closure record §2 table: STEP 8.5 row added. §6 outstanding actions: `lessons_learnt_prompt.md` invocation failure added as example. STEP 11 commit: order corrected (`lessons_learnt_closure.md` before `closure_record.md`). §1 Purpose updated to name STEP 8.5 explicitly. **Dry-run enforcement added throughout.** §2: dry-run definition tightened — closure plan is the deliverable; routine ends after producing it. §5: dry-run exception block added at top (no writes permitted). STEP -1.6: write permission test skipped in dry-run. STEP 0: dry-run exits here after producing closure plan. §7 completion condition: dry-run completion defined. §9 invariant added. |
| 1.1 | 2026-03-06 | Added `decisions_record` N/A condition (STEP 4.2). Added push-before-pull rule (STEP 11). Clarified AR record exemption from Superseded status. |
| 1.0 | 2026-03-03 | Initial version. |