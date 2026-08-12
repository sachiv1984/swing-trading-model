**Owner:** Head of Specs Team
**Status:** Active
**Version:** 3.8
**Last Updated:** 2026-08-12
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

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

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

→ Apply `claude/system/shared/governance_preamble.md §Write-Scope`. Phase-specific permitted paths:
- `claude/cycles/<cycle_id>/verification_report.md` (create)
- `claude/cycles/<cycle_id>/verification_escalations.md` (create or append — hard gate blockers only)
- `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` (append-only — Phase 4 section; create if absent)
- `docs/System_status_report.md` (update — reconciliation only)
- `claude/backlog/backlog.md` (append-only — outstanding items and test scenario gaps only)
- `.claude_current_state.json` (status update only)

Must not modify: `claude/cycles/<cycle_id>/execution_state.json` (sealed), `claude/cycles/<cycle_id>/sprint_close.md` (sealed), `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed), `claude/cycles/<cycle_id>/amendments/*/amended_backlog_slice.md` (sealed), `claude/cycles/<cycle_id>/sprint_backlog.md` (sealed), `claude/cycles/<cycle_id>/qa_evidence_EPIC-xx.md` (owned by Director of Quality), any canonical spec file, `claude/roadmap/*`, `claude/strategy/strategy_rules.md`.

---

## 6. Required Authority Roles

→ Apply `claude/system/shared/governance_preamble.md §Agent-Integrity`. Required roles:
- Director of Quality
- Product Owner
- PMO Lead
- QA & Testing Owner

---

## 7. Deviation Severity Policy (Hard Gates)

| Priority | Meaning | Verification impact |
|----------|---------|-------------------|
| P0 | System-breaking, data loss, or security issue | **Hard block.** Verification cannot pass. Must be resolved before any status except `Not_Verified` is assigned. No acceptance path. |
| P1 | Material functional deviation — feature does not meet spec | **Hard block.** Verification cannot pass unless Product Owner AND Director of Quality both explicitly accept with documented rationale recorded in `verification_report.md`. |
| P2 | Partial implementation — core behaviour present but incomplete | **Hard block.** Verification cannot pass unless explicitly accepted with documented rationale, AND a backlog item is confirmed for the remainder. |
| P3 | Minor deviation — cosmetic, edge case, or non-critical gap | Record in report. Create backlog item. Verification proceeds as `Verified_with_deviations`. |

**Any open item that is not a filed deviation** (returned item, flagged gap, unresolved escalation) must have a `backlog.md` entry before the verification report is sealed. Verification does not block on these items — but they must be traceable.

**Resolved-deviation carve-out (LL-v8.6-P4-03, added v3.8):** The P0–P3 hard-block/documented-acceptance requirements above apply only to deviations that are **open** at the time of this sprint's own delivery. A deviation record filed this sprint with `Status: Resolved` — i.e. a retroactive record of a defect already fully fixed (in this cycle or a prior one), filed for traceability rather than to flag a current gap — is entered in the Deviation Register (STEP 3 output) for traceability but does **not** trigger the severity policy's hard-block or PO+DoQ acceptance-recording requirement, regardless of its priority field. Confirm the canonical spec's own Known Deviations entry states `RESOLVED` (or equivalent) with a resolution narrative before applying this carve-out — an entry merely *labelled* P1 with no resolution evidence still hard-blocks per the table above. This closes an interpretive gap first found at `2026-08-11__release-v8.6` (`DEV-NAV-ST06-01`, a retroactively-filed P1 record for an already-shipped v8.5 fix, required the verifying engine to infer this exemption rather than read it directly from this policy).

---

## Mandatory End-to-End Process

---

ESCALATION: Create/append `verification_escalations.md`. Use ESC-VER-YYYYMMDD-nn prefix per `shared_standards.md §4`. Record: blocking condition, owning authority, resolution path, SLA. Reference from `verification_report.md §8`. Escalation does not change verification status — only resolution does. **Structural append-verification (BLG-GOV-168):** Apply the Structural Append-Verification Procedure per `shared_standards.md §7.1` at every append (count before/after, confirm exactly +1, confirm no prior entry text changed — halt on either failure).

---

## STEP -1 — Preflight Gate (Hard Gate)

**Branch Safety Check (Hard Gate):**

Run: `git branch --show-current`

If the result is NOT `main`: halt immediately. Output:

> HALT — delivery verification artefacts must be committed to `main`. Current branch is `<branch_name>`. Checkout `main` (`git checkout main && git pull`) and re-invoke `run delivery verification`.

If the result is `main`: proceed.

**Dry-run detection (BLG-GOV-25 / ST-11):** If `--dry-run` is specified in the invocation, read the required files (execution_state.json, sprint_close.md, qa_evidence files), then output the dry-run report below and exit without writing any verification report, updating `.claude_current_state.json`, or making any git commits.

**Dry-run report format:**
```
DRY-RUN: run delivery verification --cycle <cycle_id>
Precondition check: status must be Sprint_Complete — PASS / FAIL
Checks that would run:
  STEP -1: Sprint close readiness statement verification
  STEP 1:  Scope completeness — all ST items from backlog slice traced to execution_state.json
  STEP 2:  QA evidence completeness — qa_evidence_EPIC-xx.md exists per EPIC, sign-off dates non-blank
  STEP 3:  PR merge state — all EPIC PRs merged to main
  STEP 4:  Backlog traceability — filed deviations have BLG IDs; source items archived or updated
  STEP 5:  Test scenario coverage — Playwright tests referenced in qa_evidence match tests/e2e/
  STEP 6:  Spec/contract drift — openapi.yaml in sync with canonical contracts
  STEP 7:  Commit format compliance — all exec/* commits have [EPIC-xx][ST-xx] prefix
  STEP 8:  Verification report written, .claude_current_state.json updated → Verified/Not_Verified
Artefacts that would be created:
  - claude/cycles/<cycle_id>/verification_report.md
  - .claude_current_state.json (status → Verified or Not_Verified)
No files written — re-invoke without --dry-run to execute.
```

**First action:** Read `claude/cycles/<cycle_id>/execution_state.json`. Confirm `sealed = true`. If not sealed: halt — the sprint execution record is not closed. **Resolution path:** Issue `run sprint --cycle <cycle_id>` — if all EPICs are already merged (all `pr_status = merged` in `execution_state.json`), the execution engine will detect this and execute STEP 5 (Sprint Close) directly, sealing the record and setting status to `Sprint_Complete`. Once sealed, re-invoke `run delivery verification --cycle <cycle_id>`.

**Parallel reads:** Read `execution_state.json`, `sprint_close.md`, and all `qa_evidence_EPIC-xx.md` files in parallel.

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
- **TIER 2 — WRONG AUTHORITY:** If sign-off is present but the signer is neither Director of Quality nor "Sprint Execution Engine (autonomous class)" nor a recognised agent-mediated format nor a recognised named domain-authority format (see below) → FLAG (do not halt). Require Director of Quality to provide a counter-sign note in that EPIC's `qa_evidence_EPIC-xx.md` before proceeding to STEP 1. Record the mismatch in `run_manifest` as a compliance advisory.
  - **Autonomous class exception (BLG-GOV-19):** If the signer is "Sprint Execution Engine (autonomous class)", verify that all four qualifying criteria defined in `execution_prompt.md §3.2.A` (Autonomous DoQ sign-off class) are met for this EPIC: (1) all stories autonomous, (2) all AC code-review-verifiable with no UI/staging requirement, (3) no frontend-visible change, (4) engine signer field populated. If all four are met: treat as compliant — do not apply Tier 2 treatment. If any criterion is not met: apply Tier 2 treatment and require Director of Quality counter-sign.
  - **Agent-mediated class exception (ST-03, v5.1):** `"Sprint Execution Engine (agent-mediated, <Role Name> role — §X.Y)"` is accepted for mixed-class EPICs as equivalent to agent-mediated sign-off with named role. If the signer field matches this pattern (role name and section reference both present, referencing `execution_prompt.md §5.3` agent-mediated sign-off protocol), treat as compliant — do not apply Tier 2 treatment. Example of compliant format: `"Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)"`. If the format is incomplete (missing role name or section reference): apply Tier 2 treatment and require Director of Quality counter-sign.
  - **Named domain-authority class exception (ESC-CLOSE-20260731-01):** A signer naming a specific human or agent-mediated domain-authority role (e.g. `Infrastructure & Operations Owner`, `Head of Engineering`, `Head of Specs Team`) — including compound forms such as `<Role A> ..., with <Role B> concurrence` or execution_prompt.md's Infrastructure co-sign format `<Role A> + Director of Quality: Confirmed — [N] stories, YYYY-MM-DD` — is accepted as compliant, provided the EPIC contains no `autonomous`-class story. Autonomous-class stories always require one of the literal Director of Quality, autonomous-class, or agent-mediated paths above regardless of this exception. If the EPIC contains any autonomous-class story and the signer only matches this domain-authority pattern: apply Tier 2 treatment and require Director of Quality counter-sign.

If any merged EPIC is missing its qa_evidence log entirely: halt (Tier 1 applies). Verification cannot proceed without signed QA evidence for every merged EPIC.

### -1.3A — PR Number Recovery (OA-04)

Before proceeding, verify that every EPIC in `execution_state.json.merge_gate.epics_merged` has a non-null `pr_number`. If any EPIC has `pr_number = null` or `pr_number = 0`:

1. Recover via: `gh pr view exec/<cycle_id>/EPIC-xx --json number,state,mergedAt`
2. If a merged PR is found: record the `number` for that EPIC — set `pr_number = <recovered_number>` and confirm `pr_status = "merged"` if `mergedAt` is non-null. **Write target (LL-v8.1-P4-01):** under the per-EPIC execution state mechanism (`shared_standards.md §12.1`), `execution_state.json` is a computed, regenerate-on-read summary — do not hand-write into it. Write the recovered fields into the owning `claude/cycles/<cycle_id>/execution_state/EPIC-xx.json` file instead, then regenerate `execution_state.json` via `claude/system/scripts/generate_execution_summary.py <cycle_id>` before continuing. If the cycle predates the per-EPIC mechanism (no `execution_state/` directory present — legacy shared-file cycle), write directly into `execution_state.json` as before.
3. If no PR is found for an EPIC branch: flag as a process gap (sprint close executed without a PR) — record in `verification_report.md §8` and continue.

**Why this step exists:** During v4.0 delivery verification, `pr_number = null` in `execution_state.json` caused downstream steps to fail when attempting `gh pr view <pr_number>`. This guard recovers the PR number from GitHub before any PR-dependent check proceeds (OA-04, v4.1 ST-03).

### -1.4 Common Preflight — Required Files Present
Apply `claude/system/shared/preflight_common.md` (sub-check 1 only) with:
- required_files: per Section 4

---

## STEP 1 — Scope Traceability (Hard Gate)

Purpose: confirm every item that was in scope has a traceable outcome.

For every ST item in the authoritative backlog slice (identified in STEP -1.1):

1. Locate its record in `execution_state.json`.
2. Check status — must be `done`, `merged`, or `returned_to_backlog`.
   - If any item has no record, or has status `not_started` / `in_progress` / `blocked_*` without a `returned_to_backlog` disposition: traceability gap — halt in `strict` mode; flag and continue in `standard` mode.
3. For `done` / `merged` items: confirm `spec_references` is non-empty.
   - If `spec_references = []`: check `spec_reference_not_applicable`. If `true` (per `execution_prompt.md` STEP 3.1.A Case E — a structured field, added v3.55): this is exempt, not a gap — record it in the traceability matrix as `spec_reference_not_applicable` with the story's `spec_reference_not_applicable_reason` as the rationale, and do **not** count it toward the `Traceability gaps` flag count. Legacy records predating this field are exempt on the same terms if `notes` contains exactly "no prior spec applicable".
   - If `spec_references = []` and neither exemption applies: flag as traceability gap. Cannot verify against spec with no reference.
4. For `returned_to_backlog` items: confirm a corresponding entry exists in `claude/backlog/backlog.md` referencing this `cycle_id`.
   - If the backlog entry is missing: **add it now** (permitted write):
     ```
     - [ST-xx] <title> — returned from <cycle_id>: <reason>. See sprint_close.md.
     ```
   - Record the addition in `verification_report.md`.

**Output — Traceability matrix** (in `verification_report.md` §2):

| ST Item | Title | Outcome | Spec Reference | Backlog Entry |
|---------|-------|---------|---------------|---------------|
| ST-xx | <title> | done/merged/returned | <spec#section or "none filed" or "spec_reference_not_applicable: <reason>"> | N/A / ✓ / ⚠ added |

Flag counts: `Traceability gaps: N | Items returned: N | Backlog entries added this run: N`

---

## STEP 2 — QA Evidence Review

For each merged EPIC, read `qa_evidence_EPIC-xx.md`:

### 2.1 Per-Item Review

For each ST item row in the evidence table:
- `Result` must be `Pass`, `Pass with notes`, or `Staging-deferred (per CLAUDE.md §2 / shared_standards.md §16.11)`.
- `Staging-deferred (per CLAUDE.md §2 / shared_standards.md §16.11)` is valid only when a backlog item for the deferred staging sign-off was filed pre-PR (confirm the backlog reference is present and traceable). It is not a blocking `Fail` when that condition holds.
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

**Skip this step if the authoritative backlog slice contains zero items with `status = parked`.**

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

**Algorithm replacement advisory (AUD-2026-06-22-007):** For any story that replaces a core algorithm, model, or scoring function: cross-check that every file listed in `test_scenarios` for that story was either (a) confirmed run in `qa_evidence_EPIC-xx.md` "Scenarios run" field, or (b) explicitly declared superseded in the DoQ sign-off block with a note naming the replacement test file. A purpose-built unit test for a new algorithm does not automatically satisfy domain-level scenario coverage from a prior scenario file — both must be addressed or the prior file must be retired with a note. If neither condition is met, flag as a coverage gap and produce a TSG entry in STEP 5.3.

### 5.2 Feedback to QA & Testing Owner

**Short-circuit:** If `test_scenarios = []` AND the EPIC has no frontend-visible AC (autonomous/governance/backend-only class): record disposition as `not_applicable` in the TSG table (STEP 5.3) and skip the feedback record block for that EPIC.

For each EPIC with a genuine coverage gap (not short-circuited above), produce a structured feedback record:

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
- `not_applicable` — gap does not cover a core user journey or EPIC is autonomous/backend-only class; no backlog item required (record rationale).
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

**Status-line update (expected step, BLG-GOV-170):** As part of this reconciliation, update the section's `**Status:**` line from `Sprint_Complete — pending verification` (written by `execution_prompt.md` STEP 5.3A) to `Verified — <date>` or `Verified_with_deviations — <date>` — whichever matches the STEP 7 outcome for this cycle, using the date this verification run completes. This is expected, routine behaviour on every verification run, not a new or unusual finding — do not log it as friction in `lessons_learnt_cycle.md`.

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

**§3 — QA Evidence Summary** — from STEP 2. Use table format:

| EPIC | Items | Pass | Fail | Sign-off | Notes |
|------|-------|------|------|----------|-------|
| EPIC-xx | N | N | 0 | ✓ DoQ YYYY-MM-DD | — |

**§4 — Deviation Register** — from STEP 3. Full table. Hard blocks section. Acceptance records section (for any P1/P2 accepted: who accepted, when, rationale).

**§5 — Outstanding Items and Deferred Execution Blockers** — from STEP 4. Use table format:

| Item | Type | Outcome | Backlog ref |
|------|------|---------|-------------|

Two sub-sections: (a) outstanding items carried to backlog; (b) deferred execution blocker dispositions.

**§6 — Test Coverage Assessment** — from STEP 5. Per EPIC: scenario status and TSG table. If all EPICs are `not_applicable`: record "No test scenario gaps identified — all EPICs autonomous/governance/backend-only class" and omit feedback record blocks.

**§7 — System Status Confirmation** — from STEP 6. Confirmed / corrected / created. Any corrections listed.

**§8 — Open Items** *(only if `Not_Verified`)* — every condition that must be resolved before re-running. Each: description, owner, resolution path. Reference any `verification_escalations.md` entries by ID. Omit this section entirely when status is `Verified` or `Verified_with_deviations`.

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

### STEP 9.0 — Artefact Presence Pre-Check

**Artefact existence precondition:** Before updating `.claude_current_state.json`, verify the following cycle artefacts exist on disk:

| Artefact | Path | Class | Required? |
|----------|------|-------|-----------|
| Verification report | `claude/cycles/<cycle_id>/verification_report.md` | Class 3 (Operational Record) | ✅ Required |
| Sprint close record | `claude/cycles/<cycle_id>/sprint_close.md` | Class 3 (Operational Record) | ✅ Required |
| Lessons learnt (Phase 4 section) | `claude/cycles/<cycle_id>/lessons_learnt_cycle.md` | Class 3 (Operational Record) | ✅ Required |
| QA evidence logs | `claude/cycles/<cycle_id>/qa_evidence_EPIC-*.md` (one per merged EPIC) | Class 4 (Planning Document) | ⚠️ Advisory |

**If a Required artefact is absent:** Do not proceed to the state update. Create or complete the missing artefact (STEP 8 for verification_report, STEP 8.5 for lessons_learnt, execution engine STEP 5.3 for sprint_close), then return to this step.

**If an Advisory artefact is absent:** Record a governance warning in the verification report §8 and continue. Do not halt.

**Soft halt condition:** If a Required Class-3 Operational Record cannot be completed in this session (e.g. Director of Quality sign-off unavailable), record the absence as an open escalation in `verification_escalations.md` and output:
> ⚠️ Artefact presence pre-check: `<filename>` missing. Governance warning recorded. State update proceeding with `next_cycle_unblocked: false` until resolved.

---

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

The run is complete when: `verification_report.md` has all required sections (§8 only if `Not_Verified`), `.claude_current_state.json` is updated with verification outcome and `next_cycle_unblocked` flag, STEP 10 commit is done, and every open item from STEPS 1–6 has a recorded disposition (returned items in backlog, P2/P3 deviations in backlog, test gaps in TSG table, deferred blockers in §5, system status report confirmed accurate).

---

## 9. Governance Invariants

→ Apply `claude/system/shared/governance_preamble.md §Invariants` (system-wide). Phase-specific additions:
- **No autonomous verification.** The engine assembles evidence and produces the report. The Director of Quality and Product Owner sign off. The engine does not self-certify.
- **No cycle unlocking without passing status.** `next_cycle_unblocked = true` is only set when status is `Verified` or `Verified_with_deviations`. Never when `Not_Verified`.
- **P0 deviations have no acceptance path.** They must be resolved. The engine will never record a P0 deviation as accepted — only the resolution of the underlying issue unlocks verification.

---

## Change Log

See: [`claude/system/changelogs/delivery_verification_changelog.md`](changelogs/delivery_verification_changelog.md)
