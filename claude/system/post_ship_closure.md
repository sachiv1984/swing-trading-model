**Owner:** Head of Specs Team
**Status:** Active
**Version:** 2.27
**Last Updated:** 2026-08-16
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

**Output suppression (clean runs):** On a clean run with no flags, advisories, corrections, or outstanding actions, suppress intermediate step output — surface only the §7 Closure Confirmation and the Advisory Summary block at the end. When a flag, advisory, or correction occurs, output it inline at the step where it arises.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

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

→ Apply `claude/system/shared/governance_preamble.md §Write-Scope`. Phase-specific permitted paths:
- `docs/product/changelog.md` (append new version entry)
- `claude/roadmap/current_roadmap.md` (status update, version headers, ✅ Complete annotation with ship date and `cycle_id`, release summary table update — all per STEP 2)
- `claude/backlog/backlog.md` (mark shipped items complete; add missing Phase 4 items; no other changes)
- Scope document at `docs/product/scope/scope--{id}-{slug}.md` (status → Superseded only)
- Decisions record at `docs/product/decisions/{id}-{slug}.md` (status → Superseded only)
- Canonical spec files (deviation note compliance fixes only — missing required fields per §3 Known Deviation Standard; no other spec edits permitted; the document owner must be notified of any fields added to their spec by this routine — record in closure record §6)
- `claude/cycles/<cycle_id>/closure_escalations.md` (create if escalations raised during closure — format per `shared_standards.md §4`; ID prefix `ESC-CLOSE-YYYYMMDD-nn`)
  - **State-pointer sync (mandatory, closes AUD-2026-08-03-001 / AUD-2026-08-08-003):** Whenever an entry is appended to `closure_escalations.md`, in the same STEP 8 write also set `.claude_current_state.json.open_escalations.<ESC-ID> = {"summary": "<one-line>", "owner": "<role>", "sla_due_utc": "<timestamp>"}`. When that escalation's `Disposition` is later set to `Resolved` (in this file or a future session that resolves it), remove the corresponding key from `open_escalations` in the same write. This is the only path outside Sprint Execution that raises escalations against the global state pointer's gate condition — Release Planning, Sprint Planning, and Roadmap Rebalance all read this field and must see real data.
- `docs/System_status_report.md` (reconciliation only — correct stale notes)
- `docs/operations/validation_system.md` (reconciliation only — correct stale notes)
- `docs/specs/Specs_Index.md` (mark resolved items; add new gaps identified during delivery)
- Templates and prompt files where a lessons learnt action specifies an immediate fix (version bump required)
- `claude/cycles/<cycle_id>/lessons_learnt_closure.md` (create via STEP 8.5)
- `claude/cycles/<cycle_id>/closure_record.md` (create at close)
- `claude/cycles/<cycle_id>/closure_state.json` (create at STEP 0; update at batch checkpoints)
- `.claude_current_state.json` (status update only)

Sealed files — must not modify: `claude/cycles/<cycle_id>/verification_report.md`, `claude/cycles/<cycle_id>/sprint_close.md`, `claude/cycles/<cycle_id>/execution_state.json`, `claude/cycles/<cycle_id>/stage4_backlog_slice.md`, `claude/cycles/<cycle_id>/amendments/*/amended_backlog_slice.md`, `claude/cycles/<cycle_id>/sprint_backlog.md`, `claude/cycles/<cycle_id>/lessons_learnt.md`, `claude/cycles/<cycle_id>/lessons_learnt_cycle.md`, `claude/strategy/strategy_rules.md`, any governance document not listed above.

---

## 6. Required Authority Roles

→ Apply `claude/system/shared/governance_preamble.md §Agent-Integrity`. Required roles:
- PMO Lead
- Product Owner
- Head of Specs Team

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

**Branch Safety Check (Hard Gate):**

Run: `git branch --show-current`

If the result is NOT `main`: halt immediately. Output:

> HALT — post-ship closure artefacts must be committed to `main`. Current branch is `<branch_name>`. Checkout `main` (`git checkout main && git pull`) and re-invoke `run post-ship`.

If the result is `main`: proceed.

Purpose: fail fast before any writes begin.

Shared standards (escalation format, halt report format, identifier conventions): `claude/system/shared_standards.md`.

**Read in parallel:** Issue all reads for -1.1 through -1.4 simultaneously — they have no inter-dependencies.

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

### -1.4/-1.5/-1.6 Common Preflight — Required Files, Roles, and Write Test
Apply `claude/system/shared/preflight_common.md` (all three sub-checks) with:
- required_files: per Section 4 (backlog slice subject to the source-of-truth rule resolved in STEP 0)
- required_roles: per Section 6
- write_test_path: claude/cycles/\<cycle_id\>/.write_test (mark `--dry-run: skip` if `--dry-run` is active)

---

## STEP 0 — Load Release Context

**Closure state (first action — before any other reads):**

Read `claude/cycles/<cycle_id>/closure_state.json` if it exists:
- If it exists and `status = Closed`: this cycle is already closed — halt with message "Cycle already closed."
- If it exists and `status = In_Progress`: this is a resume. Skip all steps whose `steps.*` value is `pass`. Resume from the first `not_started` or `fail` step.
- If it does not exist: create it now with these fields: `cycle_id`, `release`, `status="In_Progress"`, `mode`, `dry_run=false`, `started_utc` and `last_updated_utc` (ISO-8601 UTC), a `steps` map with `preflight="pass"` and all remaining steps (`step_0_context` through `step_13_commit`) set to `"not_started"`, and `closure_status: null`.

If `closure_state.json` cannot be written: halt immediately.

**Backlog slice resolution (second action):** Check `.claude_current_state.json` for `amended_backlog_slice_path`:
- If present and non-empty: this is the authoritative backlog slice for this run. Verify the file exists — if not, halt.
- If absent or empty: `stage4_backlog_slice.md` is the authoritative slice.

Cross-reference the identified path against `execution_state.json.backlog_slice_source`. If they disagree: flag to PMO Lead before proceeding. Record the authoritative path as `backlog_slice_source` in the closure record §1.

**Read in parallel:** Issue all five reads below simultaneously.

Extract from the verified inputs (load only the specified sections, not full documents):

1. From `verification_report.md` — **read: `§1 verification_status` and `§4 deviation register` only.** Extract: release version (`vX.Y`), verification status (`Verified` / `Verified_with_deviations`), deviation register, QA summary.
2. From `execution_state.json` — **read: `epics` outcome map only** (not full state schema). Extract: merged EPICs (with EPIC IDs and descriptions), all ST items with `spec_references`, `deviations_filed` flags, returned-to-backlog items, `backlog_slice_source`.
3. From `sprint_close.md` — **read: verification readiness statement and deviations list only** (not full narrative sections). Extract: sprint goal, deviations filed list, outstanding delegated items, verification readiness statement.
4. From `current_roadmap.md` — **read: the release summary table and the entry matching this release only.** Extract: roadmap item ID and feature name.
5. From `backlog.md` — **read: items tagged with this `cycle_id` only.** Identify all items added by Phase 4 (returned items, P2/P3 deviation items, test scenario gap items) — these must all be present before STEP 3 can pass.

Confirm: release version, feature name, `cycle_id`, ship date (use today if not recorded elsewhere), and Product Owner sign-off date are all resolvable. If any cannot be determined: halt in `strict` mode; flag and proceed with `[UNKNOWN]` placeholder in `standard` mode.

**Audit Cadence Check (advisory — non-blocking):**
Read `completed_cycle_count` and `last_audit_cycle_count` (nullable) from `.claude_current_state.json`.
AUDIT DUE fires if **either** condition is true:
- `completed_cycle_count % 3 == 0` (modulo cadence check), **OR**
- `last_audit_cycle_count` is non-null AND `(completed_cycle_count - last_audit_cycle_count) >= 4` (gap-based fallback; catches missed audits when the modulo condition was suppressed or skipped)

If either condition fires: record for the Advisory Summary block — "⚠ AUDIT DUE — completed_cycle_count = N (last_audit_cycle_count = M). Run `run audit` before next Phase 1B opens."
If `last_audit_cycle_count` is null: evaluate only the modulo condition; the gap check is skipped (null = no baseline recorded yet; field is set by `run audit` after each successful audit).
This check is non-blocking — post-ship closure proceeds regardless.

**Rebalance Cadence Check (advisory — non-blocking):**
Read `completed_cycle_count` and `next_release` from `.claude_current_state.json` (already loaded above).
If `completed_cycle_count % 2 == 0` (i.e., even): record for the Advisory Summary block — "⚠ REBALANCE DUE — completed_cycle_count = N (even). Run `run roadmap --reason scheduled` before next `plan release`."
If `completed_cycle_count % 2 == 1` (i.e., odd):
  Read `claude/roadmap/current_roadmap.md` §1's "Next planned release" line — parse its version and Status field.
  - **If `next_release` is `[TBD]` or empty** (no version decided yet): the skip advisory's "proceed directly to `plan release v<next_release>`" instruction is not actionable — a scoping decision is still needed. Record instead: "⚠ REBALANCE SKIP WITHHELD — completed_cycle_count = N (odd), but `next_release` is `[TBD]`/unscoped. A rebalance or scoping decision is needed before `plan release` can proceed — recommend `run roadmap --reason scheduled` despite the odd cadence."
  - **If `current_roadmap.md` §1's "Next planned release" version matches `next_release` AND its Status is not `[TBD]`** (e.g. already `Planning`, `Committed`, or `✅ Complete` — meaning `plan release` has already run, or is already running, for that version): the next release is already-consumed, not a genuinely fresh scoping opportunity. Record instead: "⚠ REBALANCE SKIP WITHHELD — completed_cycle_count = N (odd), but v<next_release> is already scoped (current_roadmap.md §1 Status: <Status>) — the unconditional skip advisory is stale for an already-planned release. Verify scope is still current before proceeding; no rebalance action needed if release planning already completed for this version."
  - **Otherwise** (a genuinely fresh, unconsumed `next_release` with no existing Option(a)/Option(b) scoping decision yet): record the standard advisory unchanged — "✅ REBALANCE SKIP — completed_cycle_count = N (odd). Proceed directly to `plan release v<next_release>` — no rebalance required this cycle."
Rationale: rebalances run every 2nd cycle to reduce governance overhead and increase throughput. The PO may override and run a rebalance on any cycle — this advisory is guidance, not a gate. The `[TBD]`/already-consumed checks (v8.2, ST-11, EPIC-03, BLG-GOV-218) prevent the advisory from recommending an already-completed or not-yet-possible next action.

**If `--dry-run` is active:** After completing context load, produce the full closure plan (listing every step, every write that would be made, every flag) and end the routine. Do not proceed to STEP 1.

**Batch checkpoint 1:** Update `closure_state.json` after STEP 1 completes (see below).

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
| EPIC | Description | User Impact | Spec sections updated |
|------|-------------|-------------|----------------------|
| EPIC-xx | <description> | <user-benefit copy, or `—` if no user-facing change> | <spec file#section(s)> |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-ref | P1/P2/P3 | <one line> | PO / PO + DoQ |

*(If no deviations accepted: "None")*

### Tech backlog items shipped
- [ST-xx] [U|G|D|P] <title> — <one line description>

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
- **Each `Tech backlog items shipped` line must carry a `[U|G|D|P]` classification tag** immediately after the story ID, per `roadmap_prompt.md` STEP 2.4's schema: `U` = user-facing feature or visible UX improvement; `G` = governance/prompt/process work; `D` = debt clearance (spec, QA, ops baseline, audit, security hardening, backend correctness fix with no direct visible surface); `P` = pre-work for a future feature (pre-design/pre-planning/pre-spec). Assign the tag using the story's own backlog item content — do not defer this to a later reconstruction. This removes the reconstruction-variance risk documented in `2026-07-02__scheduled` lessons learnt Friction Item 3, where `roadmap_prompt.md` STEP 2.4 had to re-derive U/G/D/P per story from changelog prose each time it ran, producing different splits for the same cycle across sessions.
- **Each `Changes shipped` row's `User Impact` cell must be populated at authoring time, not deferred (ST-13, BLG-FE-161, v8.8):** write one to two sentences of curated, present-tense, user-benefit copy for any EPIC that changed something a user can see, click, or notice the effect of — no ticket IDs, no implementation nouns (endpoint/table/component names). Leave the cell `—` for EPICs with no user-facing effect (backend/infra/governance/test-coverage-only work). `Description` is unaffected and remains the full engineering record — `User Impact` is additive, not a replacement. `GET /changelog/latest` sources the in-app "What's New" panel from this column only, excluding blank/`—` rows entirely (`docs/specs/api_contracts/changelog_endpoints.md`) — an entry written without this column populated leaves the panel showing "Nothing to show" for the whole release. See `docs/product/changelog.md`'s own authoring convention note for the full rule.
- Update `Last Updated` on `docs/product/changelog.md` to today's date.

**Failure condition:** If `docs/product/changelog.md` does not exist: create it with a standard header (Owner: PMO Lead, Class: Operational Record, Status: Active) and then add the entry. A ship without a changelog entry is not recorded — this is a hard gate.

**Batch checkpoint 1 — update `closure_state.json`:** Set `steps.step_0_context = pass`, `steps.step_1_changelog = pass`, `last_updated_utc = <now>`.

---

## STEP 1.5 — Telegram Changelog Digest (ST-02, EPIC-02, v7.8, BLG-FEAT-84)

After the changelog entry (STEP 1) is written and committed to `docs/product/changelog.md`, send a Telegram digest of the release's `### Changes shipped` entries — reusing the existing Telegram notification infrastructure (POST+JSON with retry, shipped v2.4/v5.1 for the SI-05 weekly digest).

Run:

```bash
python3 scripts/send_changelog_digest.py --version "v<X.Y>"
```

substituting the actual version being shipped (e.g. `--version "v7.8"`). The script prints a result dict (`{"sent": true/false, ...}`) and always exits `0`.

**Hard rule — non-blocking:** A failed send (missing `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`, Telegram API error, network failure) must **NOT** block Post-Ship Closure. `send_changelog_digest()` (`backend/services/changelog_digest_service.py`) never raises — log the printed result and continue to STEP 2 regardless of `sent` value. Do not retry manually beyond the script's own built-in retry (2 retries, 30s/60s backoff, inherited from the SI-05 Telegram send helper) and do not treat a failed send as a reason to halt or re-run this step.

**Batch checkpoint 1.5 — update `closure_state.json`:** Set `steps.step_1_5_changelog_digest = pass` (regardless of whether the send itself succeeded — this step is "attempted", not "delivered"), `last_updated_utc = <now>`.

---

## STEP 2 — Roadmap Update

**Read target:** Read only the entry matching this release's version label or feature name and the release summary table — not the full roadmap document.

Update `claude/roadmap/current_roadmap.md`:

1. Locate the roadmap entry for this release (match by version label or feature name from STEP 0).
2. Mark it **✅ Complete** with the ship date and `cycle_id` reference.
3. Update the "Current Version" header to the shipped version.
4. Update the "Next planned release" header to the next version (if known; leave as `[TBD]` if not).
5. If the release contained P0/P1 quality gate items (confirmed in `verification_report.md`): mark those complete within their roadmap section.
6. Update the release summary table if present.
7. Update `Last Updated` to today's date.

**Note (STEP 2 / STEP 11 boundary):** Do not write a `*RA:<release> retired — see roadmap_archive.md...*` annotation line at this step, even though prior cycles' roadmap entries show one immediately adjacent to the Current Version section. That line is written by STEP 11 (`roadmap_management_prompt.md`, invoked later in this same routine) when the item is actually archived — it does not yet exist at STEP 2. Writing it here records an archival that has not happened.

**Failure condition (hard gate in `strict` mode; flag in `standard`):** Roadmap entry still shows Planned or In Progress after this step. Stale roadmap status will cause Phase 1 (Roadmap Rebalance) to misread the current state.

---

## STEP 3 — Backlog Reconciliation (Hard Gate)

**Read targets:** `backlog.md` — items tagged with this `cycle_id` plus items with status `done`/`merged` from STEP 0 extraction. `sprint_close.md` and `execution_state.json` data already extracted in STEP 0 — do not re-read.

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

**Batch checkpoint 2 — update `closure_state.json`:** Set `steps.step_2_roadmap = pass`, `steps.step_3_backlog = pass`, `steps.step_4_scope_decisions = pass | not_applicable`, `steps.step_5_deviation_compliance = pass`, `last_updated_utc = <now>`.

### STEP 5.1 — Cross-Cycle Deviation Consolidation Review (Recurring, added v2.23 — ST-12, BLG-QA-129)

Unlike STEP 5 above (which only checks *this cycle's* newly-filed deviations for field completeness), this sub-step periodically consolidates `DEV-*` deviation records **across recent cycles** to surface recurring patterns a single-cycle view would miss.

**Cadence:** Run this sub-step every 3rd Post-Ship Closure invocation (tracked via `.claude_current_state.json` — add a `last_deviation_consolidation_review_utc` / `deviation_consolidation_review_cycle_count` pair analogous to the existing `run audit` 3-cycle cadence tracking). On cycles where it does not fire, log "Deviation consolidation review: not due (N of 3 cycles since last run)."

**When due:**
1. Scan canonical spec files, QA evidence logs, and verification reports for `## DEV-*` / `### DEV-*` headings (the `Known Deviations` section convention).
2. Build a consolidated register: DEV ID, spec file, priority, status, target/resolved release.
3. Check for recurring patterns: same spec file/component deviating repeatedly, same root-cause category, stale target-release dates (named target release more than 2 releases behind current), and resolution-status drift between a spec's own Known Deviations entry and any QA/test-scenario doc that separately tracked the same deviation to resolution.
4. Produce `docs/governance/deviation_consolidation_review_<date>.md` per the template in `docs/governance/deviation_consolidation_review_2026-08-03.md` (first run, ST-12).
5. Director of Quality sign-off required on the produced review.

This closes the gap the first run (2026-08-03) found directly: a deviation resolved via a QA/test-scenario doc does not automatically propagate its resolved status back to the canonical spec's own entry, because no existing step re-visits a spec's pre-existing DEV-* entries once filed.

---

## STEP 6 — Operational Documents Reconciliation

**Read targets:** `System_status_report.md` — the section for this `cycle_id` only. `validation_system.md` — metric count entries and expected-value lines only. `velocity_metrics.md` — last row only (to verify format before appending). `openapi.yaml` — path keys only (count distinct method+path combinations).

For each of the following documents, check for stale references to this release's features:

- `docs/System_status_report.md` — confirmed current by Phase 4, but verify the section for this `cycle_id` reflects the final verified status (not "pending verification"). Correct if needed.
- `docs/operations/validation_system.md` — check metric counts, expected values, and example outputs. Update any entries that reference "planned" or "backlog" behaviour that has now shipped.
- `claude/cycles/velocity_metrics.md` — append a row for this cycle. Values from `execution_state.json`: Planned = count of ST items at sprint-plan seal; Completed = count of items with `status: done` at post-ship (delegated items that were delivered count as Completed). Update the rolling 6-cycle average. Do not re-derive from cycle artefacts — always write the row here.

If other operational documents are referenced in `execution_state.json` spec references: check those too for stale notes.

### Advisory — Endpoint Coverage Drift Check

After all PRs for this cycle are merged, compare endpoint coverage between:

1. **`docs/reference/openapi.yaml`** — count all `path:` entries (each distinct HTTP method + path combination is one endpoint)
2. **`docs/ops/api_performance_baseline.md`** — count all endpoints listed in the measurement table(s)

**Path-parameter normalisation (required before diffing):** The two documents do not always use the same placeholder name for the same path parameter (e.g. `openapi.yaml` may use `{position_id}`/`{rule_id}`/`{trade_id}` while `api_performance_baseline.md` uses a generic `{id}`). Normalise both endpoint lists by replacing any `{paramName}` segment with a single generic token (e.g. `{id}`) before comparing — a literal string diff without this step produces false-positive gaps.

If openapi.yaml contains endpoints that are absent from the baseline doc (after normalisation):

- **Check for an existing open tracking item first** — grep `claude/backlog/backlog.md` for an already-open `BLG-OPS-*` item covering the same endpoint-coverage-drift gap class (e.g. a prior cycle's "N endpoints missing from api_performance_baseline.md" item) before filing a new one. If one exists and still covers the current gap: do not file a duplicate — reference the existing item in the closure record instead. **If the current normalised gap count/list has grown beyond that item's own recorded list** (new endpoints have accumulated since it was filed): do not edit the existing item's body (outside this routine's backlog write scope — mark-shipped-complete and add-missing-Phase-4-items only) — instead, note the delta explicitly in the closure record and Advisory Summary (e.g. "N endpoints missing, up from M at filing — BLG-OPS-xx's own list is stale by <count> items") so the item's owner can reconcile it at their own next review, rather than letting the tracking item silently understate the true gap.
- **Script-derived tracking-item handoff (AUD-2026-08-03-003):** When the delta rule above fires, also emit the fully re-derived current-gap endpoint list (already computed by this check's own diff) into the closure record's Advisory Summary in copy-paste-ready form, and instruct that the next engine actioning the item (or the next `groom backlog` review) apply that list verbatim rather than re-deriving the diff from scratch. This closes a 3-consecutive-cycle recurring drift pattern (`BLG-OPS-111`, v7.9→v7.10→v8.0) caused by the tracking item's list being manually maintained and only ever delta-noted, never corrected.
- Do **not** attempt to fill them in — performance re-runs require a live environment and human coordination
- Raise a backlog item (`BLG-OPS-xx`) titled "Add <N> new endpoints to api_performance_baseline.md re-run" referencing the missing paths, only if no existing open item covers the gap
- Record the gap in the closure record under §6 (Outstanding Actions)
- Record for the Advisory Summary block: "⚠ Endpoint coverage drift: N new paths not yet in api_performance_baseline.md — BLG-OPS-xx filed." (or "— already tracked by BLG-OPS-xx" if referencing an existing item)

This check is **advisory-only** — it does not block closure. If no gap exists, note "Endpoint coverage: no drift" in the closure record.

Additionally, check `src/pages/SystemStatus.js` `categorizeEndpoint()`: if any new top-level path prefix was introduced this cycle (visible in openapi.yaml) that is not handled by an existing `includes()` check, flag it as a follow-up for the frontend engineer. A new prefix will silently fall into the `'Other'` category rather than causing an error.

Update `Last Updated` on any document that is modified.

Record all corrections in the closure record. If a document is outside the write scope (e.g. a Class 1 spec that is not being corrected for deviation compliance): flag for the document owner rather than editing.

---

## STEP 7 — Specs Index Review

**Read target:** Sections 6 and 7 of `docs/specs/Specs_Index.md` only (Pending Spec Work and Open Compliance Issues).

### 7.1 Resolve closed items

For each item in Section 6 (Pending Spec Work) and Section 7 (Open Compliance Issues):
- Cross-reference against this delivery: did any shipped ST items or deviation filings resolve a listed item?
- If yes: mark it resolved with date and `cycle_id`.

### 7.2 Add new gaps

From `verification_report.md §6` (Test Coverage Assessment) and `qa_evidence_EPIC-xx.md` notes: identify any new spec gaps or compliance issues surfaced during this delivery that are not yet in the Specs Index.
- Add each as a new entry in the appropriate section.

### 7.3 TSG backlog reconciliation (AUD-2026-06-22-005)

**No fixed section number (LL-v8.4-Closure-01, self-confirmed at `2026-08-08__release-v8.5` closure):** `Specs_Index.md`'s Test Coverage Gap register is append-only and chronologically numbered — a new `## N. Test Coverage Gaps — vX.Y` section is appended each cycle one fires, so the section number drifts every cycle and no fixed number (the historical "§27" reference below is already stale) reliably names the register. Scan the full document for `**Status:** Open` fields belonging to a `TSG-*`-prefixed entry (pattern: a `### N.N TSG-<id> — <title>` heading followed by a `**Status:**` field) instead of relying on any single section number.

For each such entry found with status "Open":
1. Look up the corresponding BLG item ID cited in the entry's own `**Backlog item:**` field, in `claude/backlog/backlog.md`.
2. If the BLG item is marked COMPLETE or DONE: update the entry's status from "Open" to "RESOLVED" and record the cycle in which it was resolved.
3. If the BLG item remains open: leave the entry unchanged.

Record any corrections made in `lessons_learnt_closure.md` "What worked well" or "Friction Log" as applicable. This prevents stale "Open" TSG entries from accumulating across cycles and misleading roadmap engine STEP 0 gap-checks.

Update `Last Updated` on `docs/specs/Specs_Index.md` to today's date if any changes were made.

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

---

## STEP 8.5 — Produce Lessons Learnt Closure Record

Invoke `lessons_learnt_prompt.md §3.5` — **read: §3.5 only** — using the consolidated action summary produced in STEP 8 as input.

> **Note (sequencing):** `closure_record.md` is produced in STEP 9 — it does not yet exist at the time STEP 8.5 executes. The input to `lessons_learnt_prompt.md §3.5` is the STEP 8 consolidated action summary (immediate actions applied, deferred items list, and any escalations). The §6 Outstanding Actions table in `closure_record.md` is derived from the same deferred items list. Do not wait for `closure_record.md` before producing `lessons_learnt_closure.md`.

The lessons learnt prompt will create: `claude/cycles/<cycle_id>/lessons_learnt_closure.md`

This record covers:
- Closure-phase observations (document gaps surfaced, deviation compliance corrections, spec index gaps added)
- The consolidated action summary from STEP 8 (all three records reviewed, classified, and applied)
- Any process improvements applied immediately during this run (with document refs and version bumps)
- Carry-forward items for the next cycle

**Carry-Forward section required (ST-15 — per `shared_standards.md §16.8`):**
`lessons_learnt_closure.md` must include a `## Carry-Forward` section. The section may have zero rows if no carry-forward items are warranted — absence of rows is valid; absence of the section is not. Use the schema in `shared_standards.md §16.8`. The carry-forward write is the responsibility of the `lessons_learnt_prompt.md §3.5` invocation; if direct production is required (per the fallback note below), include the `## Carry-Forward` section with at least zero rows.

Do not proceed to STEP 9 until `lessons_learnt_closure.md` exists and is non-empty. If the lessons learnt prompt cannot be invoked: produce the file directly using the structure from `lessons_learnt_prompt.md §3.5`, record the deviation in the closure record §6.

**Batch checkpoint 2 (continued) — update `closure_state.json`:** Set `steps.step_6_operational_docs = pass | not_applicable`, `steps.step_7_specs_index = pass`, `steps.step_8_lessons_learnt = pass`, `steps.step_8_5_lessons_closure = pass`, `last_updated_utc = <now>`.

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

| Step | Document | Action | Status |
|------|----------|--------|--------|
| 1 | docs/product/changelog.md | Entry written | ✅ |
| 2 | claude/roadmap/current_roadmap.md | ✅ Complete; headers updated | ✅ |
| 3 | claude/backlog/backlog.md | N items COMPLETE; N additions confirmed | ✅ |
| 4 | Scope document | Superseded | ✅ / ⚠ not found |
| 5 | Decisions record | Superseded | ✅ / ⚠ not found / N/A |
| 6 | Canonical specs | N deviations checked; N fields corrected | ✅ |
| 7 | Operational docs | N corrections | ✅ / N/A |
| 8 | Specs Index | N resolved; N gaps added | ✅ |
| 8.5 | lessons_learnt_closure.md | Created | ✅ |

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
  "last_audit_cycle_count": "<see rule below — set if audit ran this cycle, else omit>",
  "last_sync_utc": "<now>"
}
```

**`completed_cycle_count` rule:** Read the current value from `.claude_current_state.json`. If absent, treat as `0`. Write the value incremented by 1. This counter tracks the total number of fully closed cycles for meta-review cadence tracking (Phase 1 STEP 11 triggers meta-review every third completed cycle).

**`last_audit_cycle_count` rule (BLG-GOV-82):** After writing `completed_cycle_count`, check whether `run audit` was completed during this cycle (indicator: `last_audit_utc` is later than the cycle's sprint_start date, or `last_audit_id` references an audit from this cycle). If an audit ran this cycle: write `last_audit_cycle_count = new_completed_cycle_count` (the incremented value just written). If no audit ran this cycle: leave the existing `last_audit_cycle_count` value unchanged. This field is used by STEP 0 Audit Cadence Check to detect cycles where the modulo advisory was suppressed or skipped.

**Amendment field reset rule (LL-v7.6-P4-01):** Check `active_amendment` in `.claude_current_state.json`. If non-empty, determine the cycle_id the amendment originated in (the cycle segment of `amended_backlog_slice_path`, e.g. `claude/cycles/<origin_cycle_id>/amendments/...`). If that origin cycle is not the cycle currently being closed by this run, read that origin cycle's own `closure_state.json` (or its `closure_record.md`, if present) to confirm it already reached `Closed` or `Closed_with_actions`. If confirmed closed: clear `amended_backlog_slice_path`, `amendment_sealed_utc`, `active_amendment`, and `amendment_status` to empty string/null in this same STEP 10 write. If the origin cycle is not yet closed, or cannot be confirmed closed, leave the fields unchanged and note the deferral in the closure record §6 Outstanding Actions. This prevents a stale cross-cycle amendment pointer from requiring manual dismissal at a later cycle's STEP 0 backlog-slice resolution (as happened at `2026-07-20__release-v7.6` delivery verification, where `amended_backlog_slice_path` still pointed to the already-closed `2026-07-17__release-v7.4`/`AMD-20260717-01`).

Surface §7 Closure Confirmation to the user for communication to the Product Owner and Head of Specs Team.

If any outstanding actions remain in §6: set `closure_status = Closed_with_actions`. The next cycle may still open — outstanding actions do not block it unless a hard gate condition is unmet.

---

## STEP 11 — Roadmap Document Management (Mandatory)

Invoke `claude/system/roadmap_management_prompt.md` — **read: execution steps and action checklist sections only.**
Pass through `--dry-run` if `run post-ship` was invoked with `--dry-run`.
Output: manage_roadmap run log at `claude/cycles/<cycle_id>/manage_roadmap_<YYYYMMDD>.md`.
On completion: confirm `last_manage_roadmap_utc` written to `.claude_current_state.json`.

## STEP 12 — Backlog Document Management (Mandatory)

Invoke `claude/system/backlog_management_prompt.md` — **read: execution steps and action checklist sections only.**
Pass through `--dry-run` if `run post-ship` was invoked with `--dry-run`.
Output: backlog health report at `claude/backlog/backlog_health_<YYYYMMDD>.md`.
On completion: confirm `last_groom_backlog_utc` written to `.claude_current_state.json`.

## STEP 12.5 — Ideas Housekeeping (Mandatory)

Invoke `claude/system/ideas_housekeeping_prompt.md` as a subroutine — **read: all execution steps.**
Pass through `--dry-run` if `run post-ship` was invoked with `--dry-run`.

This subroutine handles three tasks:
- **STEP 1** — Archive terminal rows from `claude/ideas/ideas_register.md` to `claude/ideas/ideas_register_archive.md`
- **STEP 2** — Review `claude/ideas/rejected_but_strong.md` revival conditions against the just-closed cycle
- **STEP 3** — Ideas pipeline health check (near-empty backlog advisory)

The subroutine returns an advisory block for inclusion in the Advisory Summary. It does not commit — STEP 13 owns the commit.

On completion: record subroutine outcome (rows archived, revival advisory, pipeline advisory) in closure_state.json `steps.step_12_5_ideas_housekeeping`.

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
git add claude/ideas/ideas_register.md
git add claude/ideas/ideas_register_archive.md   (if modified or created)
git add claude/cycles/<cycle_id>/lessons_learnt_closure.md
git add claude/cycles/<cycle_id>/closure_record.md
git add claude/cycles/<cycle_id>/closure_state.json
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Post-ship closure complete: <cycle_id> — v<X.Y>"
git push origin <current-branch>
```

If git operations are unavailable: output the exact files to stage and the commit message. Mark as "Ready to commit."

**Batch checkpoint 3 — update `closure_state.json`:** Set `steps.step_9_closure_record = pass`, `steps.step_10_global_state = pass`, `steps.step_11_manage_roadmap = complete`, `steps.step_12_groom_backlog = complete`, `steps.step_12_5_ideas_housekeeping = complete`, `steps.step_13_commit = pass`, `status = "Closed"`, `closure_status = "Closed | Closed_with_actions"`, `last_updated_utc = <now>`. Include this file in the commit above.

---

## Advisory Summary Block

After STEP 13, output a consolidated advisory block using `── Advisory Summary ──────────────────────────────────` / `[list or "None."]` / `──────────────────────────────────────────────────────` format. Sources: STEP 0 (audit/rebalance cadence), STEP 6 (endpoint drift), STEP 12.5 (pipeline health), any other non-blocking flags. If none: output "Advisory Summary: None."

---

## 7. Completion Condition

The run is complete when:

- `closure_state.json` has all steps = `pass` (or `complete` for STEPs 11/12) and `status = "Closed"`
- `closure_record.md` exists with all 7 sections and `lessons_learnt_closure.md` is non-empty
- `.claude_current_state.json` has `post_ship_complete = true` and `status = Closed`
- STEP 13 commit is complete (or commit manifest produced)

**Dry-run:** Complete when the closure plan is produced after STEP 0. No files written, no state updated, no commit.

---

## 8. Closure Status Values

| Status | Meaning | Next cycle? |
|--------|---------|-------------|
| `Closed` | All steps complete; no outstanding actions | Open immediately |
| `Closed_with_actions` | All steps complete; minor outstanding actions carried forward (e.g. scope doc not found, deferred lessons learnt items) | Open — outstanding actions tracked in closure record |

There is no `Failed` state for post-ship closure. If a hard gate fires before completion, the routine halts and reports. Re-issue `run post-ship --cycle "<cycle_id>"` once the condition is resolved — the engine resumes from the first incomplete step.

---

## 9. Governance Invariants

→ Apply `claude/system/shared/governance_preamble.md §Invariants` (system-wide). Phase-specific additions:
- **No re-verification.** This engine reads sealed Phase 4 artefacts. It does not re-assess what passed or failed.
- **No scope revision.** The execution state is sealed. The engine records what shipped; it does not alter it.
- **Lessons learnt must be reviewed, not just filed.** Every action item requires a disposition. Deferred is acceptable; unreviewed is not.
- **Immediate lessons learnt actions are non-deferrable.** If an action can be applied now (template fix, prompt correction), it must be. Do not defer what can be done immediately.
- **Outstanding actions do not block the next cycle** — but they must be recorded and owned. Nothing is silently dropped.
- **Dry-run produces no side effects.** No files written, no state changed, no commit made. The closure plan is the sole output.

---

## Change Log

See: [`claude/system/changelogs/post_ship_closure_changelog.md`](changelogs/post_ship_closure_changelog.md)
