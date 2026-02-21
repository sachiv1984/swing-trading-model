# Pre-Alignment Run

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 2.0
**Last Updated:** 2026-02-21

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 2.0 | 2026-02-21 | Full rewrite. Introduced formal state machine. PMO Lead must explicitly declare current STATE at all times. Gate checkboxes replaced with Gate Validation Format requiring evidence reference, owner confirmation, and PMO validation for each item. Global Invariants defined and enforced. Phase Gate Document introduced as live tracking artefact. Defect handling separated into `defect_run.md`. |
| 1.0 | 2026-02-19 | Initial version |

---

## Purpose

This template governs delivery of a **feature** from readiness audit through to implementation open. It is the PMO Lead's operating playbook — followed identically for every feature, every time.

For **defects and bug fixes**, use `defect_run.md` instead.

The central discipline of this process is the **state machine**. The feature is always in exactly one state. The PMO Lead must always know what that state is, declare it explicitly, and only advance to the next state when all gate conditions are satisfied with written evidence.

---

## Global Invariants

These rules apply in every state, without exception. They are not guidelines — they are invariants. Any violation must be surfaced immediately to the Product Owner.

| # | Invariant |
|---|-----------|
| **GI-1** | There is always exactly one next action per owner. No owner may have zero actions (they are idle, which is a process risk) or two actions (ambiguity about priority). |
| **GI-2** | Every action must have a named deadline. "ASAP" is not a deadline. |
| **GI-3** | No gate passes without written evidence. A verbal confirmation, a message saying "done", or a commit notification without content confirmation does not constitute evidence. |
| **GI-4** | The Phase Gate Document is updated within 15 minutes of any state change. |
| **GI-5** | No ambiguity may survive a phase transition. If a question is unresolved when a state change is requested, the state does not change. |

---

## State Machine

```
READINESS_AUDIT
      ↓  [Gate R]
AWAITING_MEETING
      ↓  [Gate 0]
PRE_ALIGNMENT_MEETING
      ↓  [Gate 1]
SPEC_DELIVERY
      ↓  [Gate 2]
QA_REVIEW
      ↓  [Gate 3]
SCOPE_DOCUMENT
      ↓  [Gate 4]
IMPLEMENTATION_OPEN
      ↓  [Gate 5]
CLOSED
```

A state may only change if **all gate conditions are satisfied and validated** per the Gate Validation Format below.

When a state changes, the PMO Lead must:
1. Update the Phase Gate Document (within 15 minutes — GI-4)
2. Communicate next actions to all owners (one action per owner — GI-1)
3. Log the state transition in the Phase Gate Document

---

## Gate Validation Format

This format is mandatory for every gate item in every state. Checkboxes alone are insufficient — each gate item must have explicit written evidence, owner confirmation, and PMO validation before it can be marked passed.

```
### Gate Item: [description of what must be true]

- Evidence: [commit hash, document path + version, test result URL, or written statement]
- Owner confirmation: [Yes / No] — [Owner role name], [date]
- PMO validation: [Pass / Fail] — [PMO Lead], [date]
```

A gate item is **Pass** only when:
- Evidence exists and is specific (not "it's done")
- The owner whose work is being validated has explicitly confirmed it
- The PMO Lead has reviewed the evidence and agrees it satisfies the gate condition

A gate item is **Fail** if any of the three are absent, incomplete, or inconsistent with the gate condition.

The gate as a whole **passes** only when every individual gate item is **Pass**.

---

## Phase Gate Document

The PMO Lead creates and maintains a **Phase Gate Document** for every feature, filed at:

`docs/product/phase_gates/{id}-{slug}-phase-gate.md`

This document is the live record of the feature's state, all gate validations, and all state transitions. It is updated within 15 minutes of any state change (GI-4).

See `phase_gate_document.md` for the template.

---

## STATE: READINESS_AUDIT

### Entry condition
Product Owner has nominated a roadmap item for pre-alignment.

### PMO Lead actions
Run the readiness audit per `pre_alignment_readiness.md`. Produce a readiness report with a Go / No-Go recommendation.

### Gate R — READINESS_AUDIT → AWAITING_MEETING

Each item must be validated using the Gate Validation Format.

**Gate R.1 — Data model readiness confirmed**
All fields the feature reads or writes exist in `data_model.md`, or pre-designed with type, constraint, default, and migration strategy documented.

**Gate R.2 — Settings field dependency checked**
If the feature touches the settings table in any way: all required fields confirmed in `data_model.md` and `settings_endpoints.md`, and `settings.md` is current.

**Gate R.3 — API contract readiness confirmed**
All required endpoints are documented in `api_contracts/`, or the API Contracts owner has been briefed with sufficient context.

**Gate R.4 — Frontend spec readiness confirmed**
Relevant component or page spec is current, or significant UX decisions have been pre-resolved.

**Gate R.5 — Strategy rules readiness confirmed**
If the feature touches calculations or lifecycle rules: the relevant section of `strategy_rules.md` is current.

**Gate R.6 — Effort estimate reviewed**
Roadmap effort estimate accounts for all of: backend, migration, API contract, frontend spec, settings changes, and QA review. Revised if audit changed the scope picture.

**Gate R.7 — Decisions inventory produced**
Preliminary decisions list exists and will serve as the meeting agenda.

**On Gate R pass:** State transitions to `AWAITING_MEETING`. Pre-alignment meeting is scheduled.

---

## STATE: AWAITING_MEETING

### Entry condition
Gate R passed. Meeting not yet held.

### PMO Lead actions
- Schedule the pre-alignment meeting with all required attendees
- Distribute the preliminary decisions list as the agenda
- Confirm all required roles are available

### Gate 0 — AWAITING_MEETING → PRE_ALIGNMENT_MEETING

**Gate 0.1 — All required attendees confirmed**
Required attendees: Product Owner, Head of Specs Team, API Contracts owner. Additional roles as required by feature domain (Strategy Rules owner, Data Model owner, Frontend Spec owner, Head of UX & Design, QA & Testing Owner advisory).

**Gate 0.2 — Decisions list distributed**
Preliminary decisions list sent to all attendees before the meeting.

**On Gate 0 pass:** State transitions to `PRE_ALIGNMENT_MEETING`.

---

## STATE: PRE_ALIGNMENT_MEETING

### Entry condition
Gate 0 passed. Meeting is open.

### Goal
Close all open decisions. No decisions may remain open at the end of the meeting.

### PMO Lead actions during the meeting
- Open with the preliminary decisions list
- Ensure each decision is resolved to a named, unambiguous conclusion
- Capture exact wording of each decision — not a summary
- Flag any decision that cannot be closed and assign an owner and deadline
- Do not close the meeting until all decisions are either resolved or explicitly deferred with a named owner

### Product Owner actions during or immediately after the meeting
- Author the decisions record
- Commit decisions record to `docs/product/decisions/{id}-{slug}.md` before Phase 2 work begins

### Gate 1 — PRE_ALIGNMENT_MEETING → SPEC_DELIVERY

**Gate 1.1 — All decisions closed or explicitly deferred**
Every item on the preliminary decisions list has either a resolution or a named owner and deadline. No open questions remain.

**Gate 1.2 — Decisions record committed**
Decisions record committed to `docs/product/decisions/{id}-{slug}.md`. Evidence: commit hash.

**Gate 1.3 — Action list produced**
Full action list exists with: owner, dependency, and deadline for every action. PMO Lead has identified the critical path.

**Gate 1.4 — Critical path communicated**
All owners have been notified of their first action and its deadline.

**On Gate 1 pass:** State transitions to `SPEC_DELIVERY`. PMO Lead produces the Phase Gate Document action table.

---

## STATE: SPEC_DELIVERY

### Entry condition
Gate 1 passed. Decisions record committed. All owners notified.

### Goal
All canonical spec updates are produced, reviewed, and committed. Every owner works against the locked decisions record.

### Parallel work rules

The following work streams may run simultaneously:

| Work stream | Owner | Dependency |
|-------------|-------|------------|
| API contract authoring | API Contracts owner | Decisions record |
| `openapi.yaml` update | API Contracts owner | API contract (same action — same PR) |
| Data model update + migration | Data Model owner | Decisions record |
| Strategy rules update (if needed) | Strategy Rules owner | Decisions record |
| Roadmap update | Product Owner | Decisions record |
| UX design (if needed) | Head of UX & Design | Decisions record |

The following must wait:

| Work stream | Owner | Blocked on |
|-------------|-------|------------|
| Component spec update | Frontend Spec owner | API contract committed + UX design complete |
| Settings page spec update | Frontend Spec owner | Data model update committed |
| `api_dependencies.md` update | Frontend Spec owner | API contract committed |
| QA review | QA & Testing Owner | All spec actions complete |
| Scope document | Product Owner | QA sign-off |

### Invariant enforcement in this state

**GI-1 enforcement:** The PMO Lead maintains one active action per owner at all times. When an owner completes their action, the PMO Lead immediately identifies and communicates their next action (or declares them idle if none remains).

**GI-2 enforcement:** Every action in the tracking table has a deadline. The PMO Lead flags any action without a deadline as a process violation.

**GI-3 enforcement — openapi.yaml rule:** Every PR that includes an API contract change must include the `openapi.yaml` update in the same commit. The action is not marked complete until both files are confirmed committed together.

**GI-3 enforcement — patch verification rule:** When a spec file is updated, the owner must confirm the specific content change — not just that the file was saved. The PMO Lead does not mark an action complete on the basis of a commit notification alone.

### Action tracking format

| # | Action | Owner | Deadline | Status | Blocked on | Evidence |
|---|--------|-------|----------|--------|------------|---------|
| A1 | {action} | {role} | {date} | ⛔ Blocked / 🟡 Not started / 🟢 In progress / ✅ Complete | {dependency} | {commit / doc} |

### Gate 2 — SPEC_DELIVERY → QA_REVIEW

Each item must be validated using the Gate Validation Format.

**Gate 2.1 — All spec actions confirmed complete**
Every action in the tracking table shows ✅ Complete. No in-progress or blocked actions remain.

**Gate 2.2 — openapi.yaml committed in same PR as API contract**
Evidence: single commit hash containing both files.

**Gate 2.3 — Patch verification confirmed for all patched files**
For each file that was patched (not freshly authored): the specific changed text has been confirmed by the owner.

**Gate 2.4 — No open decisions**
No questions have surfaced during spec delivery that remain unresolved. If any new decision arose during this state, it must have been resolved and appended to the decisions record before this gate is attempted.

**On Gate 2 pass:** State transitions to `QA_REVIEW`. QA & Testing Owner is notified with a complete list of committed specs to review.

---

## STATE: QA_REVIEW

### Entry condition
Gate 2 passed. All specs committed. QA owner notified.

### Goal
QA owner confirms that acceptance criteria are fully derivable from the committed canonical specs. This is a spec review — no code exists yet.

### QA owner produces
- A written verdict: **Pass**, **Conditional Pass**, or **Fail**
- For Conditional Pass: specific list of issues, each with the blocking item identified
- For Fail: complete list of issues preventing acceptance criteria derivation

### Conditional Pass handling
Each issue assigned to relevant spec owner with a deadline. Spec owner commits fix. QA owner explicitly confirms fix. PMO Lead does not advance until confirmation is received in writing.

### Gate 3 — QA_REVIEW → SCOPE_DOCUMENT

**Gate 3.1 — QA verdict recorded as Pass**
Written verdict from QA & Testing Owner on record. Evidence: written confirmation with date.

**Gate 3.2 — All Conditional Pass issues resolved (if applicable)**
For each issue raised: spec owner confirmation of fix committed + QA owner explicit confirmation of resolution. Evidence: both confirmations on record.

**Gate 3.3 — No outstanding spec questions**
QA review raised no unresolved questions about canonical spec content.

**On Gate 3 pass:** State transitions to `SCOPE_DOCUMENT`. Product Owner is notified to begin the scope document.

---

## STATE: SCOPE_DOCUMENT

### Entry condition
Gate 3 passed. QA sign-off confirmed.

### Goal
Product Owner authors the scope document per `feature_scope_document.md`. This is the final artefact before implementation opens.

### Gate 4 — SCOPE_DOCUMENT → IMPLEMENTATION_OPEN

**Gate 4.1 — Scope document committed to correct location**
`docs/product/scope/scope--{id}-{slug}.md`. Evidence: commit hash.

**Gate 4.2 — Scope document has compliant Class 4 header**
Owner, Class, Status (Active), Last Updated, Roadmap item, Target release all present. Evidence: confirmed by PMO Lead review.

**Gate 4.3 — All canonical specs listed with version numbers**
Section 2 of scope document lists every spec with its locked version. Evidence: PMO Lead spot-check of spec section.

**Gate 4.4 — Pre-implementation checklist complete**
All items checked. No unchecked items. Evidence: PMO Lead review of checklist section.

**Gate 4.5 — Roadmap entry updated**
Roadmap entry references locked canonical spec versions. Evidence: commit hash.

**On Gate 4 pass:** State transitions to `IMPLEMENTATION_OPEN`. Head of Engineering notified.

---

## STATE: IMPLEMENTATION_OPEN

### Entry condition
Gate 4 passed. Scope document committed. Engineering notified.

### PMO Lead actions
- Communicate to Head of Engineering: implementation is open, scope document location, all specs locked
- Monitor for any spec questions from engineering — these go to the relevant spec owner, not back through pre-alignment
- Trigger post-ship closure process (`post_ship_closure.md`) when Product Owner confirms ship sign-off

### Gate 5 — IMPLEMENTATION_OPEN → CLOSED

**Gate 5.1 — Ship sign-off confirmed**
Product Owner (or Director of Quality) has confirmed ship sign-off. Evidence: written confirmation with date.

**Gate 5.2 — Post-ship closure complete**
All items in `post_ship_closure.md` checklist confirmed complete. Evidence: PMO Lead confirmation.

**Gate 5.3 — Lessons learnt filed**
Record filed at `docs/product/lessons_learnt/{id}-{slug}-lessons.md`. Evidence: file path.

**On Gate 5 pass:** State transitions to `CLOSED`.

---

## STATE: CLOSED

The feature is fully delivered and all documentation is closed. No further PMO actions required unless a defect is raised against this feature, in which case `defect_run.md` governs.

---

## State Transition Log Format

Every state transition is logged in the Phase Gate Document:

```
## State Transition Log

| # | From | To | Date | Time | Declared by | Gate passed |
|---|------|----|------|------|-------------|-------------|
| 1 | READINESS_AUDIT | AWAITING_MEETING | 2026-02-19 | 14:30 | PMO Lead | Gate R |
| 2 | AWAITING_MEETING | PRE_ALIGNMENT_MEETING | 2026-02-19 | 16:00 | PMO Lead | Gate 0 |
```

---

## Common Failure Modes

| Failure | Symptom | Rule violated | Prevention |
|---------|---------|---------------|------------|
| Gate advanced without evidence | Owner said "done" but no commit | GI-3 | Gate Validation Format enforced for every item |
| Two actions assigned to one owner | Owner unsure what to do first | GI-1 | PMO Lead maintains one-action-per-owner at all times |
| Deadline missing from action | Action drifts without pressure | GI-2 | PMO Lead flags any deadline-free action at creation |
| Phase Gate Document not updated | State change happened but not recorded | GI-4 | 15-minute rule — PMO Lead has no other priority at point of state change |
| Ambiguity survives phase transition | Engineers encounter open questions | GI-5 | Gate 1.1 and 2.4 enforce decision closure |
| openapi.yaml in separate commit | Drift between contract and reference | GI-3 | Gate 2.2 blocks on evidence of same-PR commit |