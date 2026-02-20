# Pre-Alignment Run

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.1 | Added PMO Lead next steps communication requirement at every phase gate — the PMO Lead must proactively tell all stakeholders what comes next, who acts, and when, without waiting to be asked. Added cross-navigation persistence check to Phase 3 QA gate. Added Phase Gate Document requirement — PMO Lead must update the phase gate document at every gate transition. Both changes follow 3.2 lessons learnt. |
| 1.0 | Initial version. |

---

## Purpose

This template governs the pre-alignment process from the moment the meeting opens to the moment implementation is declared open. It defines the phases, the gates between them, what runs in parallel, and what the done criteria are at each stage.

The PMO Lead follows this template for every feature. The process is the same each time — only the feature-specific content changes.

---

## PMO Lead Communication Standard (Non-Negotiable)

**The PMO Lead does not wait to be asked what comes next.**

At every phase gate, and at every significant status change within a phase, the PMO Lead proactively communicates to all relevant stakeholders:

- What just closed or was confirmed
- What the current phase is
- Who has the next action
- What they need to do
- When it needs to be done by
- What is blocked and why

This is not a reporting function — it is an active orchestration function. If a stakeholder is asking "what do I do next?" or "what's happening?", the PMO Lead has already failed this standard.

The **Phase Gate Document** (see `processes/templates/phase_gate_template.md`) is the primary tool for this. It is updated at every gate transition and shared with all stakeholders. It is not optional.

---

## Phase Overview

```
Phase 0: Readiness Audit
        ↓
Phase 1: Pre-Alignment Meeting
        ↓
Phase 2: Parallel Spec Delivery
        ↓
Phase 3: QA Review Gate
        ↓
Phase 4: Scope Document
        ↓
        Implementation Open
        ↓
Phase 5: Verification & Shipping Closure
```

No phase may begin before the previous phase's gate is passed. Within Phase 2, parallel work is permitted — the rules for what can run in parallel are defined below.

---

## Phase 0 — Readiness Audit

### Goal
Confirm the feature is ready to enter pre-alignment. Surface all gaps before the meeting is scheduled.

### PMO Lead runs
- `processes/pre_alignment_readiness.md` — full checklist
- Produces a readiness report with Go / No-Go recommendation

### Gate: Phase 0 → Phase 1

- [ ] Readiness audit complete
- [ ] All gaps remediated or explicitly accepted with rationale recorded
- [ ] Effort estimate reviewed and revised if audit changed scope picture
- [ ] Preliminary decisions list produced (agenda for the meeting)

**PMO Lead next steps communication (on gate pass):**
Notify all required meeting attendees: the feature is ready for pre-alignment, the meeting is being scheduled, share the preliminary decisions list so attendees can prepare. Confirm attendance before sending invitations.

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
- [ ] Phase Gate Document updated to Phase 2

**PMO Lead next steps communication (on gate pass):**
Immediately after the meeting, send all spec owners: their specific action, what it is blocked on (if anything), what unblocks them, and the target date. Send the updated Phase Gate Document. Do not wait for owners to ask — they should receive their action before they leave the meeting or within the hour.

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

**The PMO Lead tracks these dependencies actively.** When a blocker is resolved, the PMO Lead notifies the downstream owner immediately — not when they next check in, but as soon as the blocker clears.

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
- [ ] Phase Gate Document updated to Phase 3

**PMO Lead next steps communication (on gate pass):**
Notify QA owner that the gate is open and the QA review can begin. Provide links to every committed spec document they need to review. State the expected review timeline. Notify all other stakeholders that Phase 2 is complete and QA review is in progress.

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

### Cross-navigation persistence check (added v1.1)

For any feature that includes a frontend component with user-editable state:

- [ ] Does the spec explicitly address what happens to that state when the user navigates away from the page and returns?
- [ ] If the spec requires state to persist across navigation: is the persistence mechanism specified (sessionStorage, React Context, lifted state)?
- [ ] Is there an acceptance criterion that explicitly tests navigation-away and return with the state preserved?

If any of the above are missing, the QA review must return Conditional Pass with this as a blocking item for the Frontend Spec owner to resolve before the gate passes.

> **Why this check exists:** During 3.2 verification, DEF-006 was raised because Risk % reset to the settings default after navigation — the spec said "retains last-used session value" but the implementation used component-local state with no persistence. This class of bug only surfaces under navigation conditions that are easy to miss in development. An explicit QA gate check before implementation prevents it.

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
- [ ] Phase Gate Document updated to Phase 4

**PMO Lead next steps communication (on gate pass):**
Notify the Product Owner that QA sign-off is confirmed and the scope document can now be authored. Provide the QA verdict reference. State the expected turnaround for the scope document. Notify the Head of Engineering that implementation is approaching — they should expect the scope document and implementation open declaration shortly.

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
- [ ] Phase Gate Document updated to Implementation Open

**PMO Lead next steps communication (on gate pass):**
Notify Head of Engineering with: implementation is open, scope document location, all canonical specs locked (list them), any questions about spec intent go to the relevant spec owner not back through pre-alignment. Also notify QA Lead: implementation has started, test scenarios should be authored now against the scope document — see `processes/testing_guide.md` for who does what and when.

---

## Phase 5 — Verification & Shipping Closure

### Goal
QA Lead executes all test scenarios and verifies all acceptance criteria. All defects are resolved. Director of Quality signs off. PMO Lead actions shipping closure.

### PMO Lead role in this phase

The PMO Lead does not own verification — that is the QA Lead and Director of Quality. The PMO Lead owns:

- Knowing the current state at all times
- Communicating status and blockers to the Product Owner
- Coordinating defect resolution between QA Lead and Head of Engineering
- Actioning shipping closure once final sign-off is confirmed

### Shipping closure checklist (PMO Lead)

Once Director of Quality final sign-off is confirmed:

- [ ] Add version entry to `docs/product/changelog.md`
- [ ] Update roadmap: feature status → ✅ Complete (shipped vX.X), current version bumped
- [ ] Update scope document: status → Superseded, reference to changelog entry
- [ ] Update decisions record: status → Superseded, reference to canonical documents produced
- [ ] Notify Head of Engineering: shipping closure confirmed, next feature approaching
- [ ] Schedule lessons learnt review per `processes/lessons_learnt.md`
- [ ] Phase Gate Document updated to Shipped

**PMO Lead next steps communication (on shipping closure):**
Notify all stakeholders: the feature is shipped, changelog entry is filed, planning documents are superseded. State what the next feature entering pre-alignment is and the target readiness audit date.

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
| Stakeholders asking "what's next?" | PMO Lead not communicating proactively | Update Phase Gate Document at every gate; send next steps without waiting to be asked |
| Scope discovery in the meeting | Effort estimate changes mid-meeting | Run the readiness audit first — especially settings field dependency check |
| Stale patch | Spec file updated but contains old text | Patch verification step |
| `openapi.yaml` not updated in same PR | Drift between contract and reference | Enforce as blocking in Phase 2 gate |
| QA gate skipped | Scope document written before QA review | PMO Lead enforces gate sequence |
| Decisions not fully closed | Engineers encounter ambiguity | Do not close Phase 1 until all decisions are resolved |
| Cross-navigation state not specced | Session persistence bug found in verification | Cross-navigation persistence check in Phase 3 QA gate |
| Test scenarios unclear | QA Lead unsure what to do or who writes scripts | See `processes/testing_guide.md` — this is a mandatory read before Phase 5 begins |
