**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.5
**Last Updated:** 2026-07-27
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Design Gate Engine — Governance Prompt

(UX/Design Review Between Release Planning and Sprint Planning)

---

## 1. Purpose

This engine runs between Release Planning (Phase 1B) and Sprint Planning (Phase 2). It classifies each sprint item by design requirement, routes items needing UX work through a structured review, and produces a gate record that Sprint Planning uses as a pre-condition. It does not change sprint scope, author canonical specifications, or replace Sprint Planning — it gates it.

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues:

```
run design-gate --cycle "<cycle_id>" [--dry-run]
```

Rules:
- Invocation must start with `run design-gate` (case-insensitive).
- `--cycle` is required and must match an active cycle in `claude/cycles/`.
- `--dry-run`: produces the classification table and gap list without writing any files, updating state, or gating Sprint Planning. Run exits after STEP 1 — no gate record, no state update, no commit.
- If invocation is not exact, do not run. Treat as conversational.

Apply the Lifecycle Guard (valid from-states: `Release_Planning_Complete`) per `claude/system/shared_standards.md §10` before executing any step.

**Pre-condition (Hard Gate):** Phase 1B must be complete and `sprint_sealed = false`. If Sprint Planning is already sealed, flag as process deviation — this engine may not run.

**Who issues this command:** PMO Lead, after Release Planning Publish Gate is passed and before issuing `plan sprint`.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

---

## 4. Required Roles

| Role | Function |
|------|----------|
| Head of UX & Design | Reviews and approves design artefacts; classifies design requirement per item |
| Product Owner | Confirms design-not-applicable classifications for borderline items; approves all design artefacts |
| Frontend Specs & UX Documentation Owner | Updates `docs/specs/frontend/pages/` based on approved designs |
| Head of Specs Team | Confirms frontend spec versions are updated and compliant |
| PMO Lead | Runs the engine; records outcomes; updates global state |
| Facilitator | Enforces gate; blocks Sprint Planning if gate not cleared |

---

## 5. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/cycles/<cycle_id>/design_gate.md` (create)
- `claude/cycles/<cycle_id>/state.json` (additive write only — do not overwrite unrelated fields)
- `docs/specs/frontend/pages/` (Head of Specs Team and Frontend Specs owner only)
- `.claude_current_state.json` (additive write only, restricted to `design_gate_status`, `design_gate_record`, `design_gate_completed_utc` — STEP 5 mirror write; no other field in this file may be touched — BLG-GOV-190)

You must **not** modify `claude/cycles/<cycle_id>/stage4_backlog_slice.md`, any roadmap or backlog document, or any canonical spec beyond approved frontend spec updates. Violation → halt.

**`--dry-run`:** no files written, no state updated.

---

## 6. Design Requirement Classification

| Classification | Criteria |
|----------------|----------|
| **Design Required** | User-facing UI change (new component, modified layout, new page, changed interaction flow, new data displayed) |
| **Design Pre-Approved** | Purely backend/infrastructure/spec debt with no UI change; or frontend spec already updated in a prior cycle and confirmed unchanged |
| **Design Not Applicable** | Purely technical (CI/CD, database migration, logging, observability) with no user-visible effect |

**Default:** When in doubt, classify as Design Required. Head of UX & Design may downgrade with explicit confirmation.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

Verify all of the following are present and valid:

- `claude/charter/team_charter.md`
- `claude/charter/document_lifecycle_guide.md`
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md`
- `claude/cycles/<cycle_id>/state.json` with `sprint_sealed = false`
- Agent files: `claude/agents/head_of_ux_&_design.md` (or equivalent), `claude/agents/frontend_specs_ux_documentation_owner.md`

Check `design_gate_status` in `state.json`:
- `not_started` (default set by Release Planning Engine at STEP 0): proceed normally
- `Passed`: already cleared — confirm with PMO Lead before re-running
- `Blocked`: prior run left items unresolved — proceed to clear blocked items
- Field absent or other value: treat as `not_started`

If `sprint_sealed = true`: halt. Design gate was bypassed. Record as process deviation in escalations.

**`--dry-run`:** preflight runs normally. If preflight fails, report and stop.

---

## STEP 0 — Load Sprint Backlog Slice

Load `claude/cycles/<cycle_id>/stage4_backlog_slice.md`. Extract all sprint items.

---

## STEP 1 — Classify Each Item

For each item, apply §6 classification rules. Present to Head of UX & Design for confirmation.

Produce classification table:

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|

For disagreements between Product Owner and Head of UX & Design: default to **Design Required** unless Product Owner explicitly accepts a lower classification. Record the decision.

For items classified **Design Pre-Approved**: record the current spec version in the Frontend Spec column — Sprint Planning uses this as the locked spec reference. No further step required for these items.

**`--dry-run` exit:** output the classification table and any identified gaps (items with no existing artefact, likely blockers). Stop here.

---

## STEP 2 — Design Required Items: Artefact Review

For each item classified as **Design Required**:

### 2.1 Check for existing design artefacts

- If yes: Head of UX & Design reviews and confirms artefact is current and approved
- If no: proceed to STEP 2.2

### 2.2 Design work (if needed)

Head of UX & Design produces:
- Wireframe or interaction specification (filed at `docs/design/<cycle_id>/<item-slug>/`)
- UX decision record covering layout, states, interactions, edge cases

Constraints:
- Must not contradict `strategy_rules.md §13`
- Analytics/metrics features must align with canonical metric definitions
- These artefacts become authoritative for STEP 3 spec updates

### 2.3 Product Owner approval

Product Owner reviews and approves all artefacts before STEP 3. One item may not block others.

---

## STEP 3 — Frontend Spec Updates

For each **Design Required** item (approved artefacts in hand):

Frontend Specs & UX Documentation Owner updates the relevant `docs/specs/frontend/pages/*.md` spec. Head of Specs Team confirms lifecycle compliance (correct class, version increment, Last Updated).

**Hard rule:** No Design Required item may proceed to Sprint Planning until its frontend spec is updated and confirmed compliant.

Record updated spec path and version in the Classification Summary table.

---

## STEP 4 — Produce Design Gate Record

Write: `claude/cycles/<cycle_id>/design_gate.md`

```markdown
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** <date>
**Cycle:** <cycle_id>

# Design Gate Record — <cycle_id>

## Gate Status: PASSED | BLOCKED

Completed: <date>
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| <id> | <title> | Design Required | <rationale> | `docs/design/...` | `docs/specs/frontend/pages/x.md` vX.Y | ✅ Cleared | Head of UX & Design |
| <id> | <title> | Design Not Applicable | <rationale> | N/A | N/A | ✅ Cleared | Head of UX & Design |
| <id> | <title> | Design Required | <rationale> | PENDING | Not updated | ❌ Blocked | — |

## Blocked Items (if any)

| Item ID | Blocker | Owner | Required by |
|---------|---------|-------|-------------|
| <id> | Frontend spec not updated | Frontend Specs owner | Before plan sprint |

## Notes

<Any process notes, disagreements, or escalations>
```

**Gate status rules:**
- **PASSED**: all Design Required items have approved artefacts and updated specs; all items classified
- **BLOCKED**: one or more Design Required items have no approved artefact or unupdated spec

---

## STEP 5 — Update Global State

Update `claude/cycles/<cycle_id>/state.json` — additive write only:

```json
{
  "design_gate_status": "Passed | Blocked",
  "design_gate_completed_utc": "<ISO-8601>",
  "design_gate_record": "claude/cycles/<cycle_id>/design_gate.md",
  "sprint_planning_pre_condition": "design_gate_status == Passed"
}
```

**State lifecycle for `design_gate_status`:**
- `not_started` → set by Release Planning Engine at STEP 0
- `Blocked` → set here if one or more items unresolved
- `Passed` → set here when all Design Required items cleared; unlocks Sprint Planning

If **Blocked**: do not set `sprint_planning_pre_condition` to true; record blocked items in `claude/cycles/<cycle_id>/escalations.md`.

**Root state pointer mirror (BLG-GOV-190 — additive only):** Immediately after the cycle-level `state.json` write above, mirror the same three values into `.claude_current_state.json`:

```json
{
  "design_gate_status": "Passed | Blocked",
  "design_gate_record": "claude/cycles/<cycle_id>/design_gate.md",
  "design_gate_completed_utc": "<ISO-8601>"
}
```

Do not touch any other field in `.claude_current_state.json` (in particular, do not set `status`, `design_gate_bypass_authority`, or `design_gate_bypass_reason` here — those remain outside this routine's write scope). This closes the drift where the cycle-level gate record showed `Passed` but the root pointer read by CLAUDE.md §0 kept reporting `not_started` indefinitely.

---

## STEP 6 — Commit

**Skip if `--dry-run`.**

```
git add claude/cycles/<cycle_id>/design_gate.md
git add claude/cycles/<cycle_id>/state.json
git add .claude_current_state.json
git add docs/design/<cycle_id>/
git add docs/specs/frontend/pages/  (only files updated this run)
git commit -m "[GOVERNANCE] Design gate: <cycle_id> — <n> items cleared, <n> blocked"
git push origin <current-branch>
```

If git operations unavailable: output exact files and commit message. Mark as "Ready to commit."

**Governance file edit check:** Before committing, if any §6-governed file (per OPERATIONAL_GUIDE.md §14) was modified — including frontend spec files updated in STEP 3 — append one entry per file to `claude/system/prompt_change_log.md`: `| date | filename | vOLD→vNEW | summary | authority |`.

---

## 7. Completion Condition

The run is complete when:

- All items classified
- All Design Required items have approved artefacts and updated specs, or recorded as blocked
- Design gate record written
- Global state updated (`design_gate_status = Passed | Blocked`) in both the cycle-level `state.json` and, additively, in `.claude_current_state.json` (BLG-GOV-190)
- Commit complete (or commit manifest produced)

**`--dry-run`:** classification table produced, gap summary output. No files written. Run complete.

Sprint Planning (`plan sprint`) may only be issued when `design_gate_status = Passed`.

---

## Change Log

See: [`claude/system/changelogs/design_gate_changelog.md`](changelogs/design_gate_changelog.md)
