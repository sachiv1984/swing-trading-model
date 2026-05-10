**Owner:** Head of Specs Team
**Status:** Active
**Version:** 1.3
**Last Updated:** 2026-05-09
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Team Charter:** claude/charter/team_charter.md

---

# Design Gate Engine — Governance Prompt

(UX/Design Review Between Release Planning and Sprint Planning)

---

## 1. Purpose

This engine runs between Release Planning (Phase 1B) and Sprint Planning (Phase 2). Its job is to ensure that every sprint item requiring UX/design work has approved design artefacts and updated frontend specs before Sprint Planning opens acceptance criteria.

It classifies each sprint item by design requirement, routes items that need design work through a structured review, and produces a design gate record that Sprint Planning uses as a pre-condition.

This engine does **NOT**:
- Change sprint item scope or priority — those are sealed by Release Planning
- Author canonical specifications — the Head of Specs Team and Frontend Specs & UX Documentation Owner do that
- Replace the Sprint Planning Engine — it gates it

---

## 2. Invocation Rule (Hard Gate)

This routine executes ONLY when the user issues the explicit command:

```
run design-gate --cycle "<cycle_id>" [--dry-run]
```

Rules:
- Invocation must start with `run design-gate` (case-insensitive match allowed).
- `--cycle` is required and must match an active cycle in `claude/cycles/`.
- `--dry-run`: produces the classification table and gap list without writing any files, updating global state, or gating Sprint Planning. Output ends after the classification table and blocked items summary — no gate record, no state update, no commit.
- If invocation is not exact, do not run. Treat as conversational.

Apply the Lifecycle Guard (valid from-states: `Release_Planning_Complete`) per `claude/system/shared_standards.md §10` before executing any step.

**Pre-condition (Hard Gate):** Phase 1B must be complete and `sprint_sealed = false` (Sprint Planning has not yet started). If Sprint Planning is already sealed, this engine may not run — the gate has been bypassed and must be flagged as a process deviation.

**Who issues this command:** PMO Lead, after Release Planning Publish Gate is passed and before issuing `plan sprint`.

---

## 3. Canonical Governance Sources (Non-Negotiable)

Canonical governance stack: per `claude/system/shared/governance_stack.md`. This routine may not override any entry in that stack.

---

## 4. Required Roles

| Role | Function in this engine |
|------|------------------------|
| Head of UX & Design | Reviews and approves design artefacts; classifies design requirement per item |
| Product Owner | Confirms design-not-applicable classifications for borderline items |
| Frontend Specs & UX Documentation Owner | Updates `docs/specs/frontend/pages/` based on approved designs |
| Head of Specs Team | Confirms frontend spec versions are updated and compliant |
| PMO Lead | Runs the engine; records outcomes; updates global state |
| Facilitator | Enforces gate; blocks Sprint Planning if gate is not cleared |

---

## 5. Write Scope Restriction (Hard Gate)

During this routine you may write only to:

- `claude/cycles/<cycle_id>/design_gate.md` (design gate record — create)
- `claude/cycles/<cycle_id>/state.json` (update `design_gate_status` and related fields — additive write only; do not overwrite unrelated fields)
- `docs/specs/frontend/pages/` (update frontend specs with approved design decisions — Head of Specs Team and Frontend Specs owner only, not Facilitator)

You must **not** modify:
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md` — sprint scope is sealed
- Any roadmap or backlog document
- Any canonical spec beyond the approved frontend spec updates

Violation → halt.

**`--dry-run` write scope:** nothing. No files are written, no state is updated.

---

## 6. Design Requirement Classification

Every item in the sprint backlog slice must be classified:

| Classification | Criteria |
|----------------|----------|
| **Design Required** | Item has a user-facing UI change (new component, modified layout, new page, changed interaction flow, new data displayed) |
| **Design Pre-Approved** | Item is purely backend, infrastructure, or spec debt with no UI change; or the frontend spec for this item was already updated in a prior cycle and the design is confirmed unchanged |
| **Design Not Applicable** | Item is purely technical (CI/CD, database migration, logging, observability) with no user-visible effect |

**Default rule:** When in doubt, classify as Design Required. The Head of UX & Design may downgrade to Design Pre-Approved or Not Applicable with explicit confirmation.

---

## Mandatory End-to-End Process

---

## STEP -1 — Preflight Gate (Hard Gate)

### -1.1 Required Files Present

Verify:
- `claude/charter/team_charter.md`
- `claude/charter/document_lifecycle_guide.md`
- `claude/cycles/<cycle_id>/stage4_backlog_slice.md`
- `claude/cycles/<cycle_id>/state.json` with `sprint_sealed = false`

Check `design_gate_status` in `state.json`:
- `not_started` (default set by Release Planning Engine at STEP 0): proceed normally
- `Passed`: gate already cleared — confirm with PMO Lead before re-running; re-run is idempotent but should be intentional
- `Blocked`: prior run left items unresolved — proceed to clear blocked items
- Any other value or field absent: treat as `not_started` and proceed

If `sprint_sealed = true`: halt. Design gate was bypassed. Record as process deviation in escalations.

### -1.2 Agent Files Present

Verify agent files exist for:
- `claude/agents/head_of_ux_&_design.md` (or equivalent)
- `claude/agents/frontend_specs_ux_documentation_owner.md`

If missing: halt and report.

**`--dry-run`:** preflight runs normally. If preflight fails, report and stop — do not proceed to classification.

---

## STEP 0 — Load Sprint Backlog Slice

Load `claude/cycles/<cycle_id>/stage4_backlog_slice.md`.

Extract all sprint items (EPICs, tasks, or sprint items as defined in the backlog slice).

---

## STEP 1 — Classify Each Item

For each item in the sprint backlog slice, apply the classification rules in §6.

Present the classification to the Head of UX & Design for confirmation.

Produce classification table:

| Item ID | Title | Classification | Rationale | Confirmed by |
|---------|-------|----------------|-----------|-------------|
| EPIC-01 | CI/CD workflow | Design Not Applicable | No UI change | Head of UX & Design |
| EPIC-03 | Risk Dashboard page | Design Required | New page with multiple components | Head of UX & Design |

For any item where Product Owner or Head of UX & Design disagree on classification:
- Record the disagreement
- Default to **Design Required** unless Product Owner explicitly accepts Design Pre-Approved/Not Applicable
- Record the decision and rationale

**`--dry-run` exit point:** output the classification table and any identified gaps (items with no existing artefact, items likely to block). Stop here — do not proceed to STEP 2 or beyond.

---

## STEP 2 — Design Required Items: Artefact Review

For each item classified as **Design Required**:

### 2.1 Check for existing design artefacts

Does a wireframe, mockup, or UX decision record exist for this item?

- If yes: Head of UX & Design reviews and confirms artefact is current and approved for implementation
- If no: design work is needed — proceed to STEP 2.2

### 2.2 Design work (if needed)

For items with no existing approved artefact:

The Head of UX & Design produces:
- Wireframe or interaction specification (filed at `docs/design/<cycle_id>/<item-slug>/`)
- UX decision record covering: layout, states, interactions, edge cases

Constraints:
- Design artefacts must not contradict canonical strategy rules (`strategy_rules.md §13`)
- Design artefacts for analytics or metrics features must align with canonical metric definitions
- Design artefacts become the authoritative source for frontend spec updates in STEP 3

### 2.3 Product Owner approval

Product Owner reviews and approves all design artefacts before STEP 3 proceeds.
Approval is required for each item — one item may not block others.

---

## STEP 3 — Frontend Spec Updates

For each item classified as **Design Required** (approved artefacts in hand):

The Frontend Specs & UX Documentation Owner updates the relevant `docs/specs/frontend/pages/*.md` spec to reflect the approved design. The Head of Specs Team confirms the update is lifecycle-compliant (correct class, version increment, Last Updated).

| Item | Spec file updated | Version | Confirmed by |
|------|-------------------|---------|-------------|
| EPIC-03 | `docs/specs/frontend/pages/risk_dashboard.md` | v0.1.0 (new) | Head of Specs Team |

**Hard rule:** No item classified as Design Required may proceed to Sprint Planning until its frontend spec is updated and confirmed compliant. This is the gate.

---

## STEP 4 — Design Pre-Approved Items: Spec Version Confirmation

For each item classified as **Design Pre-Approved**:

Confirm the current version of the relevant frontend spec (if any).
Record the spec version — Sprint Planning will use this as the locked spec reference for acceptance criteria.

---

## STEP 5 — Produce Design Gate Record

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

## Item Classification Summary

| Item ID | Title | Classification | Design Artefact | Frontend Spec | Gate Status |
|---------|-------|----------------|-----------------|---------------|-------------|
| <id> | <title> | Design Required | `docs/design/...` | `docs/specs/frontend/pages/x.md` vX.Y | ✅ Cleared |
| <id> | <title> | Design Not Applicable | N/A | N/A | ✅ Cleared |
| <id> | <title> | Design Required | PENDING | Not updated | ❌ Blocked |

## Blocked Items (if any)

| Item ID | Blocker | Owner | Required by |
|---------|---------|-------|-------------|
| <id> | Frontend spec not updated | Frontend Specs owner | Before plan sprint |

## Design Artefacts Produced This Cycle

| Item | Artefact | Location | Approved by |
|------|----------|----------|-------------|
| <id> | Wireframe | `docs/design/<cycle_id>/<slug>/` | Product Owner |

## Frontend Spec Versions Locked for Sprint Planning

| Item | Spec | Version |
|------|------|---------|
| <id> | `docs/specs/frontend/pages/x.md` | vX.Y |

## Notes

<Any process notes, disagreements recorded, or escalations>
```

**Gate status rules:**
- **PASSED**: all Design Required items have approved artefacts and updated specs; all items classified
- **BLOCKED**: one or more Design Required items have no approved artefact or unupdated spec

---

## STEP 6 — Update Global State

Update `claude/cycles/<cycle_id>/state.json` — additive write only; do not overwrite unrelated fields set by other engines:

```json
{
  "design_gate_status": "Passed | Blocked",
  "design_gate_completed_utc": "<ISO-8601>",
  "design_gate_record": "claude/cycles/<cycle_id>/design_gate.md",
  "sprint_planning_pre_condition": "design_gate_status == Passed"
}
```

**State lifecycle for `design_gate_status`:**
- `not_started` — initial value set by Release Planning Engine (STEP 0); this engine reads it at preflight
- `Blocked` — set here if one or more items are unresolved
- `Passed` — set here only when all Design Required items are cleared; this is the value that unlocks Sprint Planning

If gate status is **Blocked**:
- Do not set `sprint_planning_pre_condition` to true
- Record blocked items in `claude/cycles/<cycle_id>/escalations.md`
- Sprint Planning (`plan sprint`) must not be issued until the gate is cleared

---

## STEP 7 — Commit

**Skip entirely if `--dry-run`.** Dry-run ends at STEP 1.

```
git add claude/cycles/<cycle_id>/design_gate.md
git add claude/cycles/<cycle_id>/state.json
git add docs/design/<cycle_id>/
git add docs/specs/frontend/pages/  (only files updated this run)
git commit -m "[GOVERNANCE] Design gate: <cycle_id> — <n> items cleared, <n> blocked"
git push origin <current-branch>
```

If git operations unavailable: output exact files and commit message. Mark as "Ready to commit."

**Governance file edit check (ST-13 / CF-2):** Before committing, check whether any §6-governed file (listed in `claude/system/OPERATIONAL_GUIDE.md` §14) was modified during this design gate run — including frontend spec files updated in STEP 3. If any were modified: append one entry per file to `claude/system/prompt_change_log.md` in the same session, using the format `| date | filename | vOLD→vNEW | summary | authority |`. This step must complete before the STEP 7 commit is pushed.

---

## 7. Completion Condition

The run is complete when:

- All items classified
- All Design Required items have approved artefacts and updated frontend specs, or are recorded as blocked
- Design gate record written (`claude/cycles/<cycle_id>/design_gate.md`)
- Global state updated (`design_gate_status = Passed | Blocked`)
- Commit complete (or commit manifest produced)

**`--dry-run` completion condition:** classification table produced and gap summary output. No files written, no state updated, no commit. Run is complete.

Sprint Planning (`plan sprint`) may only be issued when `design_gate_status = Passed`.

---

## 8. Governance Invariants

- **Sprint scope is sealed.** This engine may not add, remove, or reprioritise sprint items. It only gates their readiness.
- **Design Required is the default.** Ambiguous items are classified as Design Required unless explicitly downgraded by Head of UX & Design.
- **Frontend spec must be updated before the gate clears.** A design artefact without a corresponding spec update does not clear the gate.
- **Product Owner approves all design artefacts.** The Head of UX & Design produces; the Product Owner approves. These are not the same step.
- **Gate bypass is a process deviation.** If Sprint Planning is run without a passing design gate, this must be recorded in escalations and lessons learnt.
- **Dry-run is safe.** `--dry-run` never writes files, updates state, or affects Sprint Planning gating. It exits after classification.
- **State writes are additive.** STEP 6 writes only the four `design_gate_*` fields — it must not overwrite fields set by other engines (e.g. `backlog_committed`, `publish_eligible`).

---

## Change Log

See: [`claude/system/changelogs/design_gate_changelog.md`](changelogs/design_gate_changelog.md)

