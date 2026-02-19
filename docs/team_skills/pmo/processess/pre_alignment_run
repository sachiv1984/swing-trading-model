# Pre-Alignment Run

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-19

---

## Purpose

This template governs the pre-alignment process from the moment the meeting opens to the moment implementation is declared open. It defines the phases, the gates between them, what runs in parallel, and what the done criteria are at each stage.

The PMO Lead follows this template for every feature. The process is the same each time — only the feature-specific content changes.

---

## Phase Overview

```
Phase 1: Pre-Alignment Meeting
        ↓
Phase 2: Parallel Spec Delivery
        ↓
Phase 3: QA Review Gate
        ↓
Phase 4: Scope Document
        ↓
        Implementation Open
```

No phase may begin before the previous phase's gate is passed. Within Phase 2, parallel work is permitted — the rules for what can run in parallel are defined below.

---

## Phase 1 — Pre-Alignment Meeting

### Goal
Close all open decisions. No decisions may remain open at the end of the meeting.

### Required attendees
- Product Owner (decisions authority, decisions record owner)
- Head of Specs Team (governance and cross-spec alignment)
- Strategy Rules owner (if the feature touches calculations, rules, or lifecycle behaviour)
- Data Model owner (if the feature touches schema or fields)
- API Contracts owner (always — every feature touches at least one endpoint)
- Frontend Spec owner (if the feature has a UI surface)
- Head of UX & Design (if new interaction patterns or widget states are involved)
- QA & Testing Owner (to confirm acceptance criteria will be derivable — advisory role only at this stage)

Roles not listed above attend only if the feature requires their domain.

### During the meeting

The PMO Lead:
- Opens with the preliminary decisions list from the readiness audit
- Ensures each decision is resolved to a named, unambiguous conclusion
- Captures the exact wording of each decision — not a summary
- Flags any decision that cannot be closed in the meeting and assigns an owner and deadline
- Does not close the meeting until all decisions have either been resolved or explicitly deferred with an owner

The Product Owner:
- Authors the decisions record during or immediately after the meeting
- Decisions record is committed to `docs/product/decisions/` before Phase 2 spec work begins

### Gate: Phase 1 → Phase 2

- [ ] All decisions closed (or deferred with named owner and deadline)
- [ ] Decisions record committed to `docs/product/decisions/{item-id}-{feature-slug}.md`
- [ ] Action list produced with owners, dependencies, and blockers identified
- [ ] Critical path communicated to all owners

---

## Phase 2 — Parallel Spec Delivery

### Goal
All canonical spec updates are produced, reviewed, and committed. Every owner produces their deliverable against the locked decisions record.

### Parallel work rules

The following work streams are independent and may run simultaneously once Phase 1 is complete:

| Work stream | Owner | Dependency |
|-------------|-------|------------|
| API contract authoring | API Contracts owner | Decisions record |
| `openapi.yaml` update | API Contracts owner | API contract (same action) |
| Data model update + migration | Data Model owner | Decisions record |
| Strategy rules update (if needed) | Strategy Rules owner | Decisions record |
| Roadmap update | Product Owner | Decisions record |
| UX design (if needed) | Head of UX & Design | Decisions record |

The following work streams have dependencies and must wait:

| Work stream | Owner | Blocked on |
|-------------|-------|------------|
| Component spec update (e.g. `position_form.md`) | Frontend Spec owner | API contract committed + UX design complete |
| Settings page spec update | Frontend Spec owner | Data model update committed |
| `api_dependencies.md` update | Frontend Spec owner | API contract committed |

**The PMO Lead tracks these dependencies actively.** When a blocker is resolved, the PMO Lead notifies the downstream owner immediately.

### openapi.yaml rule

Every PR that includes an API contract change must also include the `openapi.yaml` update in the same commit. The PMO Lead flags this as a blocking requirement — it is not optional per governance rules. The action is not marked complete until both files are committed together.

### Patch verification rule

When a spec patch is produced and committed, the owner must confirm the specific text that changed in the committed file — not just that the file was updated. The PMO Lead does not mark the action complete on the basis of a commit notification alone.

### Action tracking format

The PMO Lead maintains an action table throughout Phase 2:

| # | Action | Owner | Status | Blocked on |
|---|--------|-------|--------|------------|
| A1 | API contract | API Contracts owner | ✅ Complete | — |
| A2 | `openapi.yaml` | API Contracts owner | ✅ Complete | A1 |
| A3 | Data model | Data Model owner | ✅ Complete | — |
| A4 | Strategy rules patch | Strategy Rules owner | ✅ Complete | — |
| A5 | UX design | Head of UX & Design | ✅ Complete | — |
| A6 | Component spec | Frontend Spec owner | 🟢 In progress | A1, A5 |
| A7 | Settings spec | Frontend Spec owner | 🟢 In progress | A3 |
| A8 | API dependencies | Frontend Spec owner | 🟢 In progress | A1 |
| A9 | Roadmap update | Product Owner | ✅ Complete | — |
| A10 | QA review | QA owner | ⛔ Blocked | A6 |
| A11 | Scope document | Product Owner | ⛔ Blocked | A10 |

### Gate: Phase 2 → Phase 3

- [ ] All spec actions confirmed complete and committed
- [ ] `openapi.yaml` committed in the same PR as the API contract
- [ ] Patch verification confirmed for any patched files
- [ ] No open actions remaining in the spec delivery phase

---

## Phase 3 — QA Review Gate

### Goal
The QA owner confirms that acceptance criteria are fully derivable from the committed canonical specs. This is a review, not a testing activity — no code exists yet.

### What the QA owner reviews

- The API contract for the new or modified endpoint(s)
- The frontend component spec (if applicable)
- Cross-references these against the decisions record and strategy rules

### What the QA owner produces

- A written review verdict: **Pass**, **Conditional Pass**, or **Fail**
- For Conditional Pass: a list of specific issues that must be resolved, with the blocking item clearly identified
- For Fail: a list of all issues preventing acceptance criteria from being derived

### Conditional Pass handling

If the QA review returns Conditional Pass:
- Each issue is assigned to the relevant spec owner
- The spec owner resolves the issue and commits the fix
- The QA owner confirms the fix before the gate is passed
- The PMO Lead does not advance to Phase 4 until confirmation is received

### Gate: Phase 3 → Phase 4

- [ ] QA review verdict recorded as Pass or Conditional Pass resolved
- [ ] No outstanding spec issues from the QA review
- [ ] QA owner has confirmed sign-off explicitly

---

## Phase 4 — Scope Document

### Goal
The Product Owner authors the scope document using `processes/feature_scope_document.md`. This is the final artefact before implementation opens.

### What the scope document must contain

See `processes/feature_scope_document.md` for the full template. At minimum:

- Reference to all locked canonical specs (with versions)
- Calculation summary (for features involving business logic)
- Acceptance criteria derived from the QA review
- Pre-implementation checklist (all actions confirmed complete)
- Effort estimate (revised if scope changed during pre-alignment)
- Out of scope confirmation

### Committed location

`docs/product/scope/scope--{roadmap-item-id}-{feature-slug}.md`

### Gate: Phase 4 → Implementation Open

- [ ] Scope document committed to `docs/product/scope/`
- [ ] Scope document has compliant Class 4 header
- [ ] Roadmap entry updated with locked canonical spec references
- [ ] Implementation declared open by Product Owner

---

## Declaring Implementation Open

When all Phase 4 gates are passed, the PMO Lead communicates to the Head of Engineering:

- Implementation is open for `{feature name}`
- Scope document location: `docs/product/scope/scope--{id}-{slug}.md`
- All canonical specs are locked — engineering builds against these
- Any questions about spec intent go to the relevant spec owner, not back through pre-alignment

---

## Common Failure Modes

| Failure | Symptom | Prevention |
|---------|---------|------------|
| Scope discovery in the meeting | Effort estimate changes mid-meeting | Run the readiness audit first |
| Stale patch | Spec file updated but contains old text | Patch verification step |
| `openapi.yaml` not updated in same PR | Drift between contract and reference | Enforce as blocking in Phase 2 gate |
| QA gate skipped | Scope document written before QA review | PMO Lead enforces gate sequence |
| Decisions not fully closed | Engineers encounter ambiguity | Do not close Phase 1 until all decisions are resolved |
