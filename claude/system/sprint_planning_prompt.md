**Owner:** Head of Specs Team
**Status:** Active
**Version:** 3.17
**Last Updated:** 2026-08-21 (lifecycle audit AUD-2026-08-21, action-all-audit-points session — STEP 3.1 pre-seal stale-feature-target check, D1-tracked STALE since v8.7 Phase 3); prior — 2026-08-06; prior history retained — see prior entries in version control.
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Sprint Planning Engine — Governance Prompt

(Backlog-Driven, Capacity-Confirmed, Criteria-Gated, Sign-Off-Sealed)

---

## 1. Purpose

Convert a release-planned backlog slice into a time-boxed, executable sprint by:
- Confirming available capacity against the backlog slice
- Defining a sprint goal owned by the Product Owner
- Selecting and confirming the sprint scope within capacity
- Verifying every entering item has defined acceptance criteria and an explicit owner
- Resolving cross-item dependencies and sequencing
- Producing a signed-off sprint backlog that Phase 3 can execute without ambiguity

This routine does **NOT**:
- Add, remove, or reprioritise items in the global backlog
- Alter the release plan or re-scope the release
- Begin any execution work
- Make strategy or architecture decisions

Sprint Planning is the bridge between a Published release plan and an executable sprint. Its outputs are hard gate inputs to Phase 3.

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
plan sprint [--cycle "<cycle_id>"] [--mode "strict|standard"] [--dry-run]
```

Rules:
- Invocation must start with `plan sprint` (case-insensitive match allowed).
- `--cycle` optional: if omitted, load `active_cycle` from `.claude_current_state.json`. If absent or ambiguous, halt.
- `--mode` optional:
  - `strict`: halt on any missing acceptance criteria, unclear owner, or unresolved dependency
  - `standard` (default): proceed with flags on minor gaps; still halt on hard gates
- `--dry-run` optional: read all inputs and produce a planning preview without writing any artefacts or updating state. The pip-audit scan (STEP -1.8) still runs — it is a read-only operation.

If invocation is not exact, do not run. Treat as conversational.

Apply the Lifecycle Guard (valid from-states: `Design_Gate_Passed`; or `Release_Planning_Complete` when design gate is not required for this cycle) per `claude/system/shared_standards.md §10` before executing any step.

**Amendment_In_Progress guard (Hard Gate):** Before proceeding, check `.claude_current_state.json` status. If status = `Amendment_In_Progress`: halt immediately. Sprint Planning may not proceed while an amendment is active. Seal or withdraw the amendment before issuing `plan sprint`. Output halt report per `shared_standards.md §5`.

**Who issues this command:** The PMO Lead persona, after Phase 1B has reached `Published` status and the Design Gate has passed (`design_gate_status = Passed`).

**Tool call budget:** This routine typically requires 10–20 tool calls. Proceed through steps without requesting confirmation unless a hard gate fires.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

Shared standards (escalation format, halt report format, identifier conventions, resumability): `claude/system/shared_standards.md`.

---

## 4. Required Authority Roles

→ Apply `claude/system/shared/governance_preamble.md §Agent-Integrity`. Required roles:
- Product Owner
- Head of Specs Team
- PMO Lead
- Director of Quality
- FinOps & Resource Architect

---

## 5. Source-of-Truth Planning Inputs

| Input | Location | Required |
|-------|----------|---------|
| Global state pointer | `.claude_current_state.json` | Hard gate |
| Release plan state | `claude/cycles/<cycle_id>/state.json` | Hard gate |
| Backlog slice | See note below — may be amended | Hard gate |
| Committed backlog | `claude/backlog/backlog.md` | Required |
| Execution plan (EPICs) | `claude/cycles/<cycle_id>/release_plan.md ## Execution Plan` (schema v2 — v2.11+) or `claude/cycles/<cycle_id>/stage3_execution_plan.md` (pre-v2.11) | Required |
| Capacity check | `claude/cycles/<cycle_id>/stage4_5_capacity_check.md` | Required |
| Cycle summary | `claude/cycles/<cycle_id>/cycle_summary.md` | Required |
| Workforce capacity | `claude/roadmap/workforce_capacity.md` | Required (if present) |

**Backlog slice source-of-truth rule:** At STEP -1, check `.claude_current_state.json` for `amended_backlog_slice_path`. If this field is present and non-empty, that file is the authoritative backlog slice for this sprint — use it in place of `stage4_backlog_slice.md` throughout. If absent or empty, use `stage4_backlog_slice.md`. Never plan from `stage4_backlog_slice.md` if an amendment has sealed.

---

## 6. Write Scope Restriction (Hard Gate)

→ Apply `claude/system/shared/governance_preamble.md §Write-Scope`. Phase-specific permitted paths:
- `claude/cycles/<cycle_id>/sprint_goal.md` (create)
- `claude/cycles/<cycle_id>/sprint_backlog.md` (create)
- `claude/cycles/<cycle_id>/sprint_backlog_index.json` (create alongside sprint_backlog.md — STEP 6)
- `claude/cycles/<cycle_id>/sprint_capacity.md` (create)
- `claude/cycles/<cycle_id>/sprint_planning_notes.md` (create — dependency map and sequencing rationale)
- `claude/cycles/<cycle_id>/sprint_escalations.md` (create if escalations raised during planning)
- `.claude_current_state.json` (status update only — STEP 7)

Must not modify: `claude/cycles/<cycle_id>/stage4_backlog_slice.md` (sealed), `claude/cycles/<cycle_id>/amendments/*/amended_backlog_slice.md` (sealed), `claude/cycles/<cycle_id>/state.json` (owned by Release Planning engine), `claude/backlog/backlog.md` (no grooming during sprint planning), `claude/roadmap/current_roadmap.md`, any canonical spec, strategy, or governance document.

---

## 7. Acceptance Criteria Standard (Hard Requirement)

Every item entering the sprint backlog must have acceptance criteria defined before the sprint may be sealed. Acceptance criteria must be structured as:

| Field | Requirement |
|-------|-------------|
| Technical | What must be built or changed — observable behaviour |
| Quality | What QA must verify — specific test scenarios |
| Security | Any security check required (may be "N/A — no security surface changed" if justified) |
| Verification | How the Director of Quality will confirm this item is done |

**Staging-only evidence designation (LL-v3.9-P3-2):** When writing ACs for stories with network-dependent verification conditions (e.g. live external API integrations, behaviour under real network failure modes), flag any AC that cannot be verified by unit or integration test in CI with `[staging-only evidence]`. This designation signals: (a) CI cannot verify this AC, (b) evidence must come from a human staging run, and (c) if staging sign-off is deferred to post-merge, a backlog item must be filed before the PR opens (per CLAUDE.md §2). Applying this flag at planning time prevents surprise P3 notations at execution and pre-stages the backlog filing before the sprint starts.

If any required field is absent:
- In `strict` mode: halt — the item cannot enter the sprint.
- In `standard` mode: flag the gap, add a placeholder marked `[AC REQUIRED]`, and record as an outstanding action. The sprint cannot be sealed until all `[AC REQUIRED]` placeholders are resolved.

**The sprint backlog may not be signed off while any item has an unresolved `[AC REQUIRED]` placeholder.**

---

## 8. Capacity Standard

Confirmed against: available FTE (`workforce_capacity.md` + `stage4_5_capacity_check.md`), sprint duration (working days), skill requirements per EPIC.

Over-allocation: scope must not exceed confirmed capacity. If over-allocated:
- `strict`: halt — require Product Owner to remove items.
- `standard`: flag, surface to Product Owner for explicit acceptance; record decision; sprint cannot seal until resolved.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

Fail fast before any planning work begins. All hard gates must pass before STEP 0.

### Hard Gates (halt immediately on failure)

**1. Global state & amendment slice** — read `.claude_current_state.json`:
- `status` must be `Published`, `Validated`, or `Committed`. Halt if `Sprint_Planning_Complete` (already planned — do not re-plan without explicit PO instruction), `Blocked` (resolve release planning escalations first), or any pre-`Committed` state (Phase 1B not complete).
- `amended_backlog_slice_path`: if present and non-empty, note the path and verify the file exists (halt if missing) — this file is the authoritative backlog slice for the cycle (see §5). If absent or empty, use `stage4_backlog_slice.md`.

**2. Release plan sealed** — read `claude/cycles/<cycle_id>/state.json`:
- `status = Published`, `publish_eligible = true`, `open_escalations` empty.
- `deferred_execution_blockers`: if non-empty — `strict` halt; `standard` record each in `sprint_escalations.md` as a named risk; PO must accept each explicitly before sprint seals.

**3. Design gate** — read `design_gate_required` from `state.json` (`attributes.design_gate_required`) OR `.claude_current_state.json` (`design_gate_required`); fall back to checking `design_gate_status` if neither field is set (pre-v2.38 release planning artefact):

- **If `design_gate_required = false` (or `not_required`):** Skip this gate check. Log: "Design gate: Not Required for this cycle — check skipped." Proceed to check 4.
- **If `design_gate_required = true` (or absent / field not initialised — treat absent as true for safety):** Apply the full design gate hard gate below.

Design gate hard gate (fires when `design_gate_required = true`):
- Read `design_gate_status` from `state.json`:
  - `Passed` → proceed normally; log "Design gate: Passed ✅".
  - `not_started`, `Blocked`, or absent → halt (absent = process deviation — Release Planning Engine STEP 4.1 should have initialised this field).
  - Exception: if every sprint item is confirmed `Design Not Applicable` by the Head of UX & Design, recorded in `state.json` or escalations, the PMO Lead may proceed with a recorded deviation.
- **Bypass audit (IMP-04, Hard Gate):** If entered from `Release_Planning_Complete` (design gate was skipped entirely): read `design_gate_bypass_authority` and `design_gate_bypass_reason` from `.claude_current_state.json`. If either is absent or empty — `strict` halt; `standard` surface + block seal until present. Per IMP-30: `design_gate_bypass_authority` must contain both `"Head of UX & Design + Product Owner"` — a single role is non-compliant. If entered from `Design_Gate_Passed`: skip bypass audit.

**4. Files, roles & write access** (may be checked in parallel):
- Authoritative backlog slice contains ≥1 EPIC with ≥1 ST item; halt if absent or empty.
- All required files in §5 exist; halt and report exactly which are missing.
- All authority role agent files in §4 present; halt if any missing.
- `claude/system/lessons_learnt_prompt.md` exists; halt if missing.
- Write test: create and delete `claude/cycles/<cycle_id>/.write_test`; halt if write fails. If not cleaned up here (e.g. due to an unexpected error), STEP 0 must remove it.

### Advisory Checks (non-blocking — record findings in sprint_planning_notes.md)

**5. Pre-sprint required decisions** — read `cycle_summary.md ## Pre-sprint Planning Required Decisions` (if section exists):
- For each listed decision: confirm resolved (recorded answer, decision log reference, or authority sign-off).
- Unresolved decisions: `strict` halt — output list per `shared_standards.md §5`, do not proceed until resolved; `standard` record as `Blocker? Yes` OA in `sprint_planning_notes.md`; sign-off gate (STEP 6.2) blocked until resolved.
- No section or all resolved: proceed.

**6. Vulnerability scan** — run `pip-audit -r backend/requirements.txt --format=json` (runs in `--dry-run` mode too — read-only):
- High/critical CVEs: record each in sprint planning notes; PO and Head of Engineering must accept each as a documented risk (with backlog item) before seal.
- Clean: note "pre-sprint pip-audit: clean".
- Unavailable: flag; recommend installation before sprint execution.
- Advisory — does not block sprint planning.

**7. Hygiene advisories** (both advisory only — no halt):
- **Prompt change log gaps (date-scan method, not file-position — BLG-GOV-257, v3.16):** for each Class 6 prompt file, run `grep "<filename>" claude/system/prompt_change_log.md` to collect **every** row mentioning that filename — do not take only the first match and do not assume the file's ordering (prepend-newest-first does not hold uniformly across the whole file: a contiguous prepend-ordered block sits above an older, ascending-chronological historical backfill, so a filename's true latest row can be either the first grep match or one further down). Parse the `Date` column (leftmost, `YYYY-MM-DD`) of every matched row and select the row with the **latest date** — not `head -1`, not file position. Extract the target version (the `v<X.Y>` after `→` in that row's version column). If the current `**Version:**` in the file exceeds that version: surface as "⚠ Prompt change log gap: `<filename>` current v<X.Y> — last log v<A.B>. Add a prepended row per CLAUDE.md §6." Record in `sprint_planning_notes.md`. Full method: `shared_standards.md §STEP -1.7-Class Prompt Change Log Gap Detection`.
- **"Before Sprint Planning" backlog items:** scan `claude/backlog/backlog.md` for items with `Provisional-Target: Before v<X.Y> sprint planning` where X.Y = current release. For each found: surface advisory and record under `## Pre-Sprint Backlog Advisory` in `sprint_planning_notes.md` with item IDs and titles.

**8. Recurring endpoint test coverage audit (added v3.15 — ST-11, BLG-QA-113):** Run `python3 scripts/audit_endpoint_test_coverage.py` — a full-repo backstop audit comparing every `@router.get/post/put/delete` decorator in `backend/routers/*.py` against `backend/routers/test.py`'s registered entries, complementing the pre-commit diff-only check (`scripts/check_router_test_registration.py`). Record the result in `sprint_planning_notes.md`:
- Exit 0 (clean, or all gaps are documented `KNOWN_GAPS` exclusions): record "pre-sprint endpoint coverage audit: clean."
- Exit 1 (undocumented gap found): surface as advisory, list the missing route(s); recommend filing a backlog item or adding the route to `test.py` before sprint scope is finalised. Advisory only — does not block sprint planning.

---

## STEP 0 — Load Release Context

**Branch Safety Check (Hard Gate — OA-02 / ST-07):**

Run: `git branch --show-current`

If the result is NOT `main`: halt immediately. Output:

> HALT — sprint planning artefacts must be committed to `main`. Current branch is `<branch_name>`. Checkout `main` (`git checkout main`) and re-invoke `plan sprint`.

If the result is `main`: proceed.

**Cleanup:** If `claude/cycles/<cycle_id>/.write_test` exists (left from STEP -1.8 on a previous interrupted run), delete it now before proceeding.

**Carry-Forward Advisory (ST-15 — per `shared_standards.md §16.8`):**
Before loading release context, check the most recently completed cycle's `lessons_learnt_closure.md` for a `## Carry-Forward` section. "Most recently completed" = highest YYYY-MM-DD cycle ID with `post_ship_complete = true` in `.claude_current_state.json`. If the section is present and non-empty: surface each item as an advisory in session output; record in `sprint_planning_notes.md` as "Carry-forward items reviewed: N items from cycle `<cycle_id>`." If absent or zero rows: record "No carry-forward items from prior cycle." Do not halt — advisory only.

Extract from the backlog slice and execution plan:

1. From the authoritative backlog slice (per §5 and STEP -1.1): all EPICs with their EPIC IDs, descriptions, and ST items. Note any items already marked as deferred or blocked. If an amendment file is in use, note this explicitly in the load summary.
2. From `release_plan.md ## Execution Plan` (schema v2 — v2.11+) or `stage3_execution_plan.md` (pre-v2.11): sequencing dependencies, risk IDs associated with EPICs, estimated effort per EPIC.
3. From `release_plan.md ## Capacity Check` (schema v2) or `stage4_5_capacity_check.md` (pre-v2.11): confirmed available capacity (FTE, skills, duration). If the `capacity_check` outcome field is `warn`: record the warning and require Product Owner acknowledgement before proceeding to scope selection (see STEP 0 note below).
4. From `cycle_summary.md`: the sprint goal candidate (if the release planning engine proposed one), any outstanding escalations deferred to execution.
5. From `workforce_capacity.md` (if present): skill availability constraints.

Produce a load summary confirming:
- Number of EPICs loaded
- Number of ST items loaded
- Confirmed capacity (FTE and duration)
- Backlog slice source (original or amended — name the file)
- Any deferred execution blockers from the release plan escalations file (cross-check against `deferred_execution_blockers` field verified in STEP -1.2)

**Capacity WARN acknowledgement (IMP-41):** If the capacity check outcome is `warn`, surface this to the Product Owner before proceeding. The Product Owner must explicitly acknowledge the over-capacity risk before scope selection begins. Record their acknowledgement in `sprint_planning_notes.md` and set `capacity_warn_acknowledged = true` in the STEP 7 state write. Do not silently proceed past a WARN — unacknowledged capacity risk compounds at execution.

**Phasing Recommendation as a live option (LP-14 — closes `2026-07-14__release-v7.1` post-ship closure Outstanding Action #2):** If `release_plan.md ## Capacity Check` includes a `### Phasing Recommendation` subsection (per `release_planning_prompt.md` STEP 4.5), present it to the Product Owner as an actual decision point alongside the WARN acknowledgement — not a document that was merely produced and can be waved through. The Product Owner's acknowledgement must explicitly state one of: (a) **Adopt** — scope is phased per the recommendation, sprint backlog reflects only the Phase 1 subset; (b) **Decline** — full scope proceeds in a single sprint, with rationale recorded for why the phasing was not needed despite the WARN. Record the choice and rationale in `sprint_planning_notes.md`. A capacity WARN with an unread Phasing Recommendation is not a valid acknowledgement.

---

## STEP 1 — Capacity Baseline

Write: `claude/cycles/<cycle_id>/sprint_capacity.md`

### 1.1 Capacity Inputs

Derive from `stage4_5_capacity_check.md` and `workforce_capacity.md`:

```
Sprint duration:    <N working days>
Available FTE:      <N> (<role breakdown if known>)
Total capacity:     <FTE × days = capacity units>
Skill constraints:  <list any scarce or role-locked skills>
```

### 1.2 Item Effort Mapping

For each EPIC and its ST items, record the effort estimate from `release_plan.md ## Execution Plan` (schema v2) or `stage3_execution_plan.md` (pre-v2.11). If an ST item has no effort estimate:
- In `strict` mode: halt — all items must have estimates.
- In `standard` mode: flag as `[ESTIMATE REQUIRED]` and record as an outstanding action. The sprint cannot be sealed until all estimates are present.

### 1.3 Total Effort vs Capacity

Calculate: total estimated effort across all candidate items vs confirmed capacity.

If total effort > capacity:
- Flag over-allocation with a breakdown by EPIC.
- This gap must be resolved in STEP 3 (scope selection).

### 1.4 Gate-Conditional Deferred Items

If any ST items are conditionally deferred at planning (recorded as `status: deferred_at_planning` with a `gate_condition` in `execution_state.json`), include a `## Conditional (Deferred)` section in `sprint_capacity.md` after the item effort table. For each deferred item, record: EPIC, story ID, effort band, and the gate condition string.

**Re-invocation advisory (mandatory when deferred items exist):** After the conditional table, add the following note to `sprint_capacity.md`:

> **Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle <cycle_id> --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.

Header block for `sprint_capacity.md`:
```
Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: <date>
Cycle: <cycle_id>
```

### 1.5 Minimum Capacity Buffer Floor (Advisory — added v3.14, ST-05, BLG-GOV-254)

**Recommendation:** Target scope selection at or below **95% of confirmed capacity**, leaving a standing ~5% buffer for in-sprint slippage (mid-sprint escalations, delegation round-trips, unplanned rework). This is a recommendation for STEP 3.2's Capacity Gate to reference, not a new hard gate — the existing over-allocation rule in §8 (halt in `strict`, PO-acceptance-required flag in `standard`) is unchanged and still governs actual sprint sealing.

**Rationale:** Recent cycles have run scope at up to ~110% of confirmed capacity (`workforce_capacity.md`, v7.9) with no formal floor recommendation to weigh against — each cycle's capacity discussion starts from zero rather than from an explicit "this is the buffer we're giving up" baseline. A named floor gives the Product Owner and FinOps & Resource Architect a concrete number to accept or explicitly override, rather than an open-ended "how much over is too much" judgment call each time.

**How to apply:** At STEP 3.2 (Capacity Gate), after confirming scope is within confirmed capacity, additionally compute `scope_effort ÷ confirmed_capacity`. If this ratio exceeds 0.95:
- Record the ratio in `sprint_capacity.md` alongside the effort table.
- Surface to the Product Owner as an explicit "buffer floor exceeded" note (distinct from the existing over-100%-of-capacity WARN, which is a harder breach). This is advisory — it does not block sealing, but the ratio and the PO's acknowledgement (proceed / trim scope) must be recorded.

**Sign-off:** FinOps & Resource Architect + PMO Lead (agent-mediated, §5.3) reviewed and approved this recommendation as an advisory reference for STEP 3.2, 2026-08-03.

---

## STEP 2 — Sprint Goal Definition

Write: `claude/cycles/<cycle_id>/sprint_goal.md`

### 2.1 Goal Derivation

The sprint goal is a single sentence describing the primary outcome of this sprint. It must:
- Be owned and approved by the Product Owner
- Reference the release feature or roadmap item this sprint advances
- Be concrete enough that at sprint close, it is unambiguous whether it was achieved
- Not be a list of tasks — it is an outcome statement

If `cycle_summary.md` contains a proposed sprint goal from Phase 1B: surface it as a candidate. The Product Owner must explicitly confirm or replace it.

If no candidate exists: surface the release version and feature name and ask the Product Owner to define the goal before proceeding.

**The sprint goal is a hard gate.** Sprint planning may not proceed past STEP 2 without a confirmed sprint goal.

### 2.2 Sprint Goal Record Structure

```markdown
# Sprint Goal — <cycle_id>

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Cycle:** <cycle_id>

## Goal

<One sentence — sprint outcome statement>

## Release Context

- Release: <vX.Y>
- Feature: <feature name>
- Roadmap item: <item ID and name>

## Confirmed by

Product Owner: [AWAITING SIGN-OFF]
Date: <date>
```

`[AWAITING SIGN-OFF]` must be replaced with the Product Owner's explicit confirmation before the sprint backlog can be sealed.

---

## STEP 3 — Scope Selection

### 3.1 Candidate Item Review

For each EPIC and ST item from the authoritative backlog slice, review:
- Is this item within confirmed capacity?
- Does this item have an owner (from `stage3_execution_plan.md`)?
- Does this item have acceptance criteria defined, or will they be drafted in STEP 4?
- Is this item blocked by an unresolved dependency or escalation?

Classify each item:
- `include` — within capacity, owned, can be AC-confirmed
- `defer` — over-capacity or blocked; return to backlog slice for next sprint
- `flag` — has an issue that must be resolved before it can be included (missing owner, missing estimate, deferred execution blocker)

**Pre-seal stale-feature-target check (AUD-2026-08-21-011, D1-tracked since v8.7 Phase 3):** For each candidate item, if its acceptance criteria or backlog reference names a specific roadmap item/feature as the target of new work, confirm that feature has not already shipped on `main` (grep `claude/backlog/backlog_archive.md` and recent `prompt_change_log.md`/changelog entries for the referenced ID). If already shipped with no remaining gap: classify as `flag` and surface for Product Owner review before scope is sealed, rather than including it as planned work.

**Delegation class assignment (set at planning time — §12 invariant):** For every `include` item, determine the delegation class for the sprint backlog:
- `autonomous` — fully implementable by the execution engine; no UX change; no human decision or mid-task sign-off required
- `delegated_backend` / `delegated_frontend` / `delegated_qa` / `delegated_decision` — requires human review, decision, or execution at a specific step

**LL-v1.10-P3-3 — Autonomous heuristic:** "Refactor to call existing client-side API with no UX change" = `autonomous`. Conservative `delegated_frontend` is valid but must be explicitly justified — over-classification adds unnecessary handoff.

**BLG-GOV-72 — Frontend classification fast-path (default autonomous):** The following story types default to `autonomous` unless new design decisions are required:
- (a) Prop/state threading bug fix with no UX change
- (b) Variable rename within a React component (no behaviour change)
- (c) New section or component implemented against a locked frontend spec where Playwright feasibility has been confirmed

Apply `delegated_frontend` only when the story genuinely cannot be completed by the engine (e.g., new UX design required, external stakeholder input needed, or no locked spec exists). Record the specific justification in `sprint_planning_notes.md` when overriding the default-autonomous classification.

**LL-v2.0-P4-2 — Test scenario gap:** Every `delegated_frontend` item introducing a new page or new user-facing controls (not a refactor of existing UI): set EPIC `test_scenarios = "pending — QA & Testing Owner to author before next sprint on this domain"` in `execution_state.json`; record in `sprint_planning_notes.md`.

**LL-v2.2-SP-01 — Blocked-decision design artefact:** Every `delegated_decision` item: check for HoST design session or equivalent artefact. If absent: surface "No design artefact found for [item]. A HoST design session should be scheduled before sprint start." in session output and `sprint_planning_notes.md`. Advisory only.

### 3.2 Capacity Gate

The selected `include` items must not exceed confirmed capacity.

If over-allocated after selection:
- Surface the gap to the Product Owner with a clear breakdown (which EPICs/items to remove to come within capacity).
- The Product Owner decides which items to defer. Record the decision.
- Do not proceed until either:
  - Scope is within capacity, or
  - The Product Owner has explicitly accepted the over-allocation with a recorded rationale (permitted in `standard` mode only).

### 3.3 Deferred Items

For each item classified `defer`:
- Record the reason (capacity, blocked dependency, missing prerequisite)
- Confirm it remains in `claude/backlog/backlog.md` with its current status (do not modify the backlog)
- Note it in `sprint_planning_notes.md` for carry-forward to the next sprint planning run

---

## STEP 4 — Acceptance Criteria Confirmation

For every `include` item, confirm acceptance criteria against the standard in Section 7.

### 4.1 Criteria Source

Acceptance criteria may come from:
- The authoritative backlog slice (if defined during release planning or amendment)
- `release_plan.md ## Execution Plan` (schema v2) or `stage3_execution_plan.md` (pre-v2.11) (if defined at EPIC level)
- Drafted during this step (if not yet defined)

### 4.2 Drafting Criteria

If acceptance criteria are not yet defined for an item, draft them now using the Section 7 structure. Surface the draft to the Head of Specs Team for confirmation before the item can be sealed.

The Head of Specs Team must confirm:
- Technical criteria are testable and observable
- Quality criteria name specific test scenarios (not "tested")
- Security criteria are explicitly stated or explicitly waived with justification
- Verification criteria are sufficient for the Director of Quality to sign off

### 4.3 Director of Quality Readiness Check

For each `include` EPIC, confirm with the Director of Quality that:
- The QA criteria are sufficient for them to produce `qa_evidence_EPIC-xx.md` at sprint close
- There are no known test coverage gaps that would block sign-off

If the Director of Quality flags a gap: record it as an outstanding action. In `strict` mode: the EPIC cannot enter the sprint until resolved.

---

## STEP 5 — Dependency Mapping and Sequencing

Write: `claude/cycles/<cycle_id>/sprint_planning_notes.md`

### 5.1 Dependency Identification

For each `include` EPIC and ST item:
- Identify cross-item dependencies (items that must complete before another can start)
- Identify external dependencies (delegated items, third-party blockers, infrastructure requirements)
- Identify spec dependencies (items that require a spec section to be locked before execution can begin)

### 5.2 Sequencing

Produce an execution order for EPICs and ST items that:
- Respects all identified dependencies
- Sequences spec-dependent items after their spec locks are confirmed
- Groups autonomous items before delegated items where possible (to unblock delegation early)
- Surfaces any circular dependencies as a blocking issue

If a circular dependency is detected: halt and surface to PMO Lead and Head of Specs Team.

**Multi-EPIC `execution_state.json` ownership (Required when > 1 EPIC in scope):** When a sprint has more than one EPIC branch, the execution order produced here determines ownership. Designate the first EPIC in execution order as the `execution_state.json` owner. Record this designation explicitly in `sprint_planning_notes.md` under a "Multi-EPIC Execution Notes" section. All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite. This prevents execution-state collisions that caused cross-EPIC rework in v3.3 and v3.4.

**Shared file ownership advisory (Required when > 1 EPIC in scope):** Identify any source files that multiple EPICs will modify (e.g., `Positions.js`, `openapi.yaml`, `data_model.md`). For each shared file: record in `sprint_planning_notes.md` which EPIC owns the canonical version and note that later EPICs must rebase onto `main` after earlier EPICs merge before finalising their changes to that file. This advisory must appear in the sprint backlog merge order section (see STEP 6.1).

**Planning-deferred item traceability (AUD-2026-05-21-002):** For each ST item in the authoritative backlog slice (`stage4_backlog_slice.md`) that is NOT included in the sealed sprint backlog (e.g. conditional EPICs deferred at planning, stories removed from scope), add an entry to `execution_state.json` at initialisation:
```yaml
epics.<EPIC-xx>.stories.<ST-xx>:
  status: deferred_at_planning
  gate_condition: "<reason — e.g. RISK-02 gate not confirmed, conditional EPIC deferred to next sprint>"
```
This ensures delivery verification STEP 1 can account for all slice items without a traceability gap. Record the deferral reason so sprint planning notes and future release planning can trace why the item was not executed.

### 5.3 Risk Flags

From `release_plan.md ## Execution Plan` (schema v2) or `stage3_execution_plan.md` (pre-v2.11) risk register: confirm which risk IDs are associated with `include` items. For each:
- Confirm the risk mitigation approach is still valid
- Flag any risk that has materialised since release planning (if known) as an escalation item

**Multi-vehicle fix-choice risk check (LP-14 — closes `2026-07-14__release-v7.1` post-ship closure Outstanding Action #2):** For any risk register item whose mitigation names two or more genuinely alternative fix vehicles (e.g. "(a) approach X, (b) approach Y, (c) approach Z — pick one") rather than an additive scope checklist, and whose mitigation defers the choice to execution kickoff: do not let this pass silently. Confirm at planning time whether the candidate approaches carry materially different effort estimates. If they do, and a `### Phasing Recommendation` (§ above) exists for this cycle, cross-reference it — the pessimistic-case fix vehicle may push total sprint effort past the recommendation's Phase 1 boundary. Record this cross-reference in `sprint_planning_notes.md` even if the final decision remains "resolve at kickoff" — the point is to surface the risk to capacity at planning time, not defer the sizing uncertainty invisibly to execution.

### Sprint Planning Notes Structure

Write per `claude/system/shared_standards.md §16.10` (sprint_planning_notes.md schema). Produce all required sections; include optional sections when applicable (carry-forward items, Capacity WARN acknowledgement, Pre-Sprint Backlog Advisory).

---

## STEP 6 — Sprint Backlog Production

Write: `claude/cycles/<cycle_id>/sprint_backlog.md` and `claude/cycles/<cycle_id>/sprint_backlog_index.json`

### 6.1 Sprint Backlog Structure

Write per `claude/system/shared_standards.md §16.11` (sprint_backlog.md schema).

Key constraints: ST item `Acceptance Criteria` must reference `stage4_backlog_slice.md#ST-xx` — do not duplicate the full AC table (Execution Engine reads AC directly via `spec_references`). `[AWAITING SIGN-OFF]` placeholders in the Product Owner Sign-Off section must be replaced with explicit PO confirmation and date before sealing (STEP 6.2).

**Merge order section (Required when > 1 EPIC in scope):** When the sprint has more than one EPIC, the sprint backlog must include a merge order section immediately after the Sprint Scope header. This section must state: (a) the EPIC merge sequence (e.g., EPIC-04→03→01→02), (b) the `execution_state.json` owner EPIC (designated in STEP 5.2), and (c) any shared files across EPICs with the ownership advisory from STEP 5.2. The Execution Engine relies on this to prevent execution-state collisions and to sequence branch rebases at merge time.

**Within-sprint date gate advisory (BLG-GOV-116):** For any ST item whose execution is gated on a specific date that falls within the sprint period (rather than a gate that must be confirmed before the sprint starts), add the following field to that story's entry in `sprint_backlog.md` at planning time:

```
**Status at sprint open: conditional — gate <YYYY-MM-DD>**
```

This signals to the Execution Engine that the story must not begin execution until the gate date has passed. Leave it as `**Status at sprint open: ready**` only when there is no within-sprint date gate condition. An unmarked within-sprint date gate is a silent execution blocker — the story would appear `ready` at execution time when it is not.

### 6.1A Sprint Backlog Index (Required — produce alongside sprint_backlog.md)

Write: `claude/cycles/<cycle_id>/sprint_backlog_index.json`

This index enables the Execution Engine to read only the relevant slice of `sprint_backlog.md` per EPIC, without loading the full document.

Required schema: per `claude/system/shared_standards.md §16.1`

One entry per EPIC in sprint scope. `backlog_slice_refs` lists the canonical section anchors in `stage4_backlog_slice.md` for each ST item — Execution Engine uses these to load AC without reading the full backlog slice.

### 6.2 Sign-Off Gate (Hard Gate)

The sprint backlog is not sealed until:
- All `[AWAITING SIGN-OFF]` fields are replaced with explicit Product Owner confirmation and a date
- All `[AC REQUIRED]` placeholders are resolved
- All `[ESTIMATE REQUIRED]` placeholders are resolved
- No outstanding actions are marked `Blocker? Yes`
- Sprint goal confirmed in `sprint_goal.md`
- All deferred execution blockers explicitly accepted by the Product Owner (if any were present)
- **Staging-only AC check (OA-02, 2nd recurrence — mandatory seal gate):** For each ST item in the sprint backlog, review every AC in `stage4_backlog_slice.md` for that item. If any AC carries a `[staging-only evidence]` tag (or requires live external API calls, deploy verification, or staging-environment behaviour that CI cannot reproduce), the `**Staging-only ACs:**` field for that story must list those AC IDs explicitly. Leaving the field as `None` when staging-only ACs exist is a **seal blocker**. This check prevents silent P3 deviations at execution by pre-staging backlog filing obligations before the sprint starts.

If any of the above are unresolved: the sprint backlog status remains `Active` (not `Sealed`). Phase 3 may not be invoked.

Once all conditions are met:
- Update `sprint_backlog.md` status: `Active` → `Sealed`
- Update `sprint_goal.md` to reflect confirmed sign-off

---

## STEP 7 — Global State Update (Hard Requirement)

Update `.claude_current_state.json`:

```json
{
  "status": "Sprint_Planning_Complete",
  "sprint_goal_path": "claude/cycles/<cycle_id>/sprint_goal.md",
  "sprint_backlog_path": "claude/cycles/<cycle_id>/sprint_backlog.md",
  "sprint_capacity_path": "claude/cycles/<cycle_id>/sprint_capacity.md",
  "sprint_sealed": true,
  "sprint_goal_status": "confirmed",
  "capacity_warn_acknowledged": true,
  "last_sync_utc": "<ISO-8601 UTC>"
}
```

**Field notes:**
- `sprint_goal_status`: always `"confirmed"` when the sprint is sealed (Product Owner sign-off gate passed).
- `capacity_warn_acknowledged`: set to `true` if capacity check outcome was `warn` and Product Owner explicitly acknowledged it in STEP 0; omit (or set `false`) if capacity check was `pass`.

`sprint_sealed` must only be set to `true` when the sign-off gate in STEP 6.2 has passed. If the sign-off gate has not passed:
- Set `sprint_sealed: false`
- Set `status: "Sprint_Planning_In_Progress"`
- The engine is resumable — re-invoke `plan sprint` once outstanding items are resolved

---

## STEP 8 — Commit

Commit all artefacts created by this routine:

```
git add claude/cycles/<cycle_id>/sprint_goal.md
git add claude/cycles/<cycle_id>/sprint_backlog.md
git add claude/cycles/<cycle_id>/sprint_capacity.md
git add claude/cycles/<cycle_id>/sprint_planning_notes.md
git add claude/cycles/<cycle_id>/sprint_escalations.md   (if created)
git add .claude_current_state.json
git commit -m "[GOVERNANCE] Sprint planning complete: <cycle_id>"
git push origin <current-branch>
```

If git operations are unavailable: output the exact files to stage and the commit message. Mark as "Ready to commit."

Commit may only proceed if `sprint_sealed = true`. If the sprint is not yet sealed, do not commit — the artefacts are still in progress.

After a successful push, run `sync gh` (CLAUDE.md §4) to create GitHub issues for all ST items in the sealed backlog slice with correct `v<X.Y>`, `sprint-N`, and `EPIC-xx` labels. This is the canonical point for issue creation; execution STEP 1 only verifies issues exist.

---

## 9. Escalation

If a planning blocker arises that cannot be resolved by the PMO Lead within this routine (e.g. a capacity constraint requiring a workforce decision, an acceptance criteria gap requiring a Head of Specs Team ruling, a scope conflict requiring Product Owner arbitration):

- Create or append `claude/cycles/<cycle_id>/sprint_escalations.md`
- Use escalation format per `claude/system/shared_standards.md` §4
- Escalation ID format: `ESC-PLAN-YYYYMMDD-nn`
- Record the blocking statement, owning authority, unblock criteria, and SLA
- Set `.claude_current_state.json` status to `Sprint_Planning_Blocked`
- Halt

Re-invoke `plan sprint` once the blocking condition is resolved. The engine resumes from the first incomplete step.

---

## 10. Completion Condition

The run is complete only if:

- `sprint_goal.md` exists with confirmed Product Owner sign-off
- `sprint_backlog.md` exists with status `Sealed` and Product Owner sign-off
- `sprint_capacity.md` exists with capacity baseline
- `sprint_planning_notes.md` exists with dependency map and sequencing
- No outstanding actions marked `Blocker? Yes`
- No `[AC REQUIRED]` or `[ESTIMATE REQUIRED]` placeholders unresolved
- All deferred execution blockers explicitly accepted by Product Owner (or confirmed empty)
- `.claude_current_state.json` status = `Sprint_Planning_Complete` and `sprint_sealed = true`
- STEP 8 commit complete (or commit manifest produced)

---

## 11. Resumability

On every invocation, the engine first checks:

1. Does `sprint_backlog.md` exist?
   - If yes and status is `Sealed`: sprint is already planned. Halt with confirmation message.
   - If yes and status is `Active`: resume from the first outstanding item (unresolved AC, missing sign-off, open blocker).
   - If no: fresh run, proceed from STEP -1.

2. Does `sprint_goal.md` exist?
   - If yes with sign-off: STEP 2 complete, skip.
   - If yes without sign-off: resume at STEP 2 sign-off gate.
   - If no: fresh run from STEP 2.

3. Does `sprint_capacity.md` exist?
   - If yes: STEP 1 complete, skip.
   - If no: run STEP 1.

Per `claude/system/shared_standards.md` §8 — never re-execute a step that already produced a valid output.

---

## 12. Governance Invariants

→ Apply `claude/system/shared/governance_preamble.md §Invariants` (system-wide). Phase-specific additions:
- No scope changes — backlog slice is sealed; select from it, don't alter it.
- No AC-less items — every sprint item must have confirmed acceptance criteria.
- No over-allocation without explicit PO acceptance; capacity is a hard constraint.
- PO sign-off is a hard gate — sprint may not seal without it.
- Circular dependencies always halt; sequencing is not final until all resolved.
- Delegation class set at planning time and recorded in sprint backlog for Phase 3.
- Design gate must be passed (`design_gate_status = Passed`) or Design Not Applicable fully documented for all items.
- Deferred execution blockers require explicit PO acceptance before execution begins.

*Full context: §2 (hard gates), §6 (write scope), §7 (AC standard), §8 (capacity), §10 (lifecycle guard).*

---

## Change Log

See: [`claude/system/changelogs/sprint_planning_changelog.md`](changelogs/sprint_planning_changelog.md)
