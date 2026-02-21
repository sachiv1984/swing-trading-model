# Defect Run

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-21

---

## Purpose

This template governs delivery of a **defect or bug fix** from report through to closure. It is the defect-specific equivalent of `pre_alignment_run.md`.

For **features**, use `pre_alignment_run.md` instead.

A defect is any observed behaviour that deviates from what a canonical specification says should happen. The canonical spec is always the reference — if the spec and the behaviour disagree, the spec wins. If the spec is wrong, the spec must be corrected first.

The same Global Invariants and Gate Validation Format that govern features govern defects without exception.

---

## Global Invariants

These rules apply in every state, without exception.

| # | Invariant |
|---|-----------|
| **GI-1** | There is always exactly one next action per owner. |
| **GI-2** | Every action must have a named deadline. |
| **GI-3** | No gate passes without written evidence. |
| **GI-4** | The Phase Gate Document is updated within 15 minutes of any state change. |
| **GI-5** | No ambiguity may survive a phase transition. |

---

## Defect State Machine

```
TRIAGE
  ↓  [Gate T]
ROOT_CAUSE
  ↓  [Gate RC]
FIX_SCOPE
  ↓  [Gate FS]
IMPLEMENTATION
  ↓  [Gate I]
VERIFICATION
  ↓  [Gate V]
CLOSED
```

A state may only change if all gate conditions are satisfied and validated per the Gate Validation Format.

When a state changes, the PMO Lead must:
1. Update the Phase Gate Document (within 15 minutes — GI-4)
2. Communicate next actions to all owners (one action per owner — GI-1)
3. Log the state transition in the Phase Gate Document

---

## Gate Validation Format

Mandatory for every gate item. A checkbox alone is not sufficient.

```
### Gate Item: [description]

- Evidence: [specific reference — commit hash, doc path, written statement, test result]
- Owner confirmation: [Yes / No] — [Owner role], [date]
- PMO validation: [Pass / Fail] — PMO Lead, [date]
```

A gate item is **Pass** only when all three components are present, consistent, and explicitly confirmed.

---

## Phase Gate Document

The PMO Lead creates one Phase Gate Document per defect, filed at:

`docs/product/phase_gates/defect-{id}-{slug}-phase-gate.md`

Use the template in `phase_gate_document.md`, adapted for the defect state machine below.

---

## Defect Severity Tiers

Defect severity determines the maximum time allowed in each state before escalation.

| Severity | Definition | Max time in TRIAGE | Max time in ROOT_CAUSE | Fix target |
|----------|------------|-------------------|----------------------|------------|
| **Critical** | Incorrect data shown to user; canonical formula violated; security or data loss risk | 2 hours | 4 hours | Current release or hotfix |
| **High** | Feature behaves incorrectly against spec; user workflow broken | 24 hours | 48 hours | Current or next release |
| **Medium** | Spec deviation with acceptable workaround | 48 hours | 72 hours | Next release |
| **Low** | Minor display or cosmetic deviation | 1 week | 1 week | Backlog |

The severity tier is assigned in TRIAGE and may only be changed by the Product Owner with written rationale.

---

## STATE: TRIAGE

### Entry condition
Defect has been reported. Report includes: observed behaviour, expected behaviour (with canonical spec reference), and steps to reproduce.

### PMO Lead actions
- Open a Phase Gate Document for the defect
- Assign triage to the Product Owner + QA & Testing Owner
- Apply escalation timer per severity tier

### Gate T — TRIAGE → ROOT_CAUSE

**Gate T.1 — Defect confirmed against canonical spec**
The expected behaviour has been identified in a canonical specification (not tribal knowledge or assumption). If no canonical spec covers the behaviour, the spec must be authored before the defect can advance.

- Evidence: {canonical spec reference — document path, section, version}
- Owner confirmation: [Yes/No] — {QA & Testing Owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate T.2 — Severity assigned**
Severity tier confirmed by Product Owner. Escalation timer set.

- Evidence: {written severity assignment with rationale}
- Owner confirmation: [Yes/No] — {Product Owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate T.3 — Reproduction confirmed**
Defect is reproducible. Steps to reproduce documented.

- Evidence: {reproduction steps confirmed by QA Lead or Engineering}
- Owner confirmation: [Yes/No] — {QA Lead or Head of Engineering}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate T.4 — Owner assigned**
A named engineering owner is assigned to ROOT_CAUSE investigation with a deadline.

- Evidence: {named owner + deadline}
- Owner confirmation: [Yes/No] — {Head of Engineering}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**On Gate T pass:** State transitions to `ROOT_CAUSE`.

---

## STATE: ROOT_CAUSE

### Entry condition
Gate T passed. Engineering owner assigned to investigation.

### Goal
Identify the exact root cause — the specific code, logic, or data model change required to fix the defect.

### PMO Lead actions
- One action in tracking table: "Identify root cause" — engineering owner, with deadline from severity tier
- Monitor for escalation timer breach
- If timer breaches: escalate to Head of Engineering immediately

### Gate RC — ROOT_CAUSE → FIX_SCOPE

**Gate RC.1 — Root cause identified and documented**
Engineering owner has stated the exact root cause: the file, function, or logic that produces the incorrect behaviour, and why.

- Evidence: {written root cause statement from engineering owner}
- Owner confirmation: [Yes/No] — {Engineering owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate RC.2 — Canonical spec impact assessed**
The Metrics Definitions, API Contracts, or relevant canonical spec owner has confirmed whether the fix requires any canonical spec update, or that no spec update is needed.

- Evidence: {written confirmation from relevant canonical owner: "spec update required: [yes/no], reason: [...]"}
- Owner confirmation: [Yes/No] — {relevant canonical owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate RC.3 — Regression surface identified**
Engineering owner has identified all areas of the system that could be affected by the fix.

- Evidence: {written list of affected areas or "no regression surface beyond the fix location"}
- Owner confirmation: [Yes/No] — {Engineering owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**On Gate RC pass:** State transitions to `FIX_SCOPE`.

---

## STATE: FIX_SCOPE

### Entry condition
Gate RC passed. Root cause known. Spec impact assessed.

### Goal
Define exactly what will change: code, specs, validation expected values. If spec changes are required, they must be completed and committed before implementation begins.

### Important rule — spec-first
If Gate RC.2 identified a required canonical spec update: the spec must be authored, committed, and confirmed by the spec owner before Gate FS can pass. Implementation does not begin against an unspecified fix.

### PMO Lead actions
- Produce action list: spec updates (if required), implementation action, validation update action
- One action per owner, all with deadlines

### Gate FS — FIX_SCOPE → IMPLEMENTATION

**Gate FS.1 — Fix scope documented**
A written fix scope statement exists: what changes, in which files, and what the expected post-fix behaviour is (with canonical spec reference).

- Evidence: {written fix scope — may be in Phase Gate Document or a filed note}
- Owner confirmation: [Yes/No] — {Product Owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate FS.2 — Canonical spec updates committed (if required)**
If Gate RC.2 required a spec update: the spec has been updated and committed. If no spec update was required: explicit statement to that effect.

- Evidence: {commit hash of spec update, OR "no spec update required — confirmed by [canonical owner]"}
- Owner confirmation: [Yes/No] — {relevant canonical owner or Product Owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate FS.3 — Validation expected values update scoped**
If the fix changes any metric or calculation output: the expected value update to `validation_data.py` has been scoped, with the new value independently calculated from the canonical spec (not from a re-run of the implementation).

- Evidence: {new expected value with hand-calculation method documented, OR "no validation update required — [metric] not affected"}
- Owner confirmation: [Yes/No] — {Metrics Definitions owner or Engineering}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate FS.4 — openapi.yaml update scoped (if API contract changes)**
If the fix changes any API contract: `openapi.yaml` update has been scoped alongside the contract change.

- Evidence: {"openapi.yaml update required, scoped for same PR" OR "no API contract change — confirmed by API Contracts owner"}
- Owner confirmation: [Yes/No] — {API Contracts owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**On Gate FS pass:** State transitions to `IMPLEMENTATION`.

---

## STATE: IMPLEMENTATION

### Entry condition
Gate FS passed. Fix scope locked. All required spec updates committed.

### Goal
Engineering implements the fix against the locked spec. No scope changes during this state — any scope question goes back to FIX_SCOPE.

### PMO Lead actions
- One action: "Implement fix" — engineering owner, with deadline
- If engineering raises a scope question: state reverts to FIX_SCOPE, gate revalidated
- State reversion is logged in the State Transition Log

### Gate I — IMPLEMENTATION → VERIFICATION

**Gate I.1 — Fix committed**
Fix code committed. Evidence: commit hash covering all changed files.

- Evidence: {commit hash}
- Owner confirmation: [Yes/No] — {Engineering owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate I.2 — Validation expected values updated (if required)**
If Gate FS.3 required a validation update: `validation_data.py` committed with new values, change documented with calculation method. Both the expected value and the hand-calculation method are on record.

- Evidence: {commit hash of validation_data.py, OR "not required"}
- Owner confirmation: [Yes/No] — {Engineering owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate I.3 — openapi.yaml committed in same PR as API contract (if applicable)**
If Gate FS.4 required a contract change: both files in same commit.

- Evidence: {commit hash showing both files, OR "not applicable"}
- Owner confirmation: [Yes/No] — {API Contracts owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate I.4 — Patch verification**
Engineering owner confirms the specific content changes made — not just that commits were made.

- Evidence: {for each changed file: what specifically changed}
- Owner confirmation: [Yes/No] — {Engineering owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**On Gate I pass:** State transitions to `VERIFICATION`. QA Lead notified.

---

## STATE: VERIFICATION

### Entry condition
Gate I passed. Fix implemented. QA Lead notified.

### Goal
Confirm the fix produces the expected behaviour per the canonical spec. Confirm no regressions in the areas identified in Gate RC.3.

### PMO Lead actions
- One action: "Verify fix" — QA Lead, with deadline
- If QA raises a regression: state reverts to `IMPLEMENTATION`, state reversion logged

### Gate V — VERIFICATION → CLOSED

**Gate V.1 — Defect behaviour resolved**
QA has confirmed the defect no longer reproduces and the system now behaves as the canonical spec requires.

- Evidence: {QA verification result — test method, result, date}
- Owner confirmation: [Yes/No] — {QA Lead}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate V.2 — Validation passes (if validation was updated)**
`POST /validate/calculations` returns all pass. If validation was not updated: explicit statement.

- Evidence: {validation run result with timestamp, OR "validation not affected — confirmed"}
- Owner confirmation: [Yes/No] — {QA Lead or Engineering}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate V.3 — No regressions in identified surface areas**
QA has checked all areas identified in Gate RC.3. No regressions observed.

- Evidence: {QA confirmation with method — test cases run, results}
- Owner confirmation: [Yes/No] — {QA Lead}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**Gate V.4 — Canonical Owner sign-off (P0/P1 defects only)**
For P0 and P1 defects: the owner of the canonical spec against which the defect was identified has confirmed the fix is correct.

- Evidence: {written sign-off from canonical owner, OR "P2/P3 — sign-off not required"}
- Owner confirmation: [Yes/No] — {relevant canonical owner}, {date}
- PMO validation: [Pass/Fail] — PMO Lead, {date}

**On Gate V pass:** State transitions to `CLOSED`.

---

## STATE: CLOSED

### PMO Lead actions on closure
1. File the tech backlog lessons learnt record per `tech_backlog_lessons_learnt.md` (P0 and P1 defects — mandatory; P2 and P3 at PMO Lead discretion)
2. Update `backlog.md` to mark the defect item closed with closure evidence
3. Update `changelog.md` with a defect closure entry (P0 and P1 — mandatory)
4. Update `validation_system.md` if metric counts, expected values, or severity assignments changed
5. Apply the known deviation triage rule (`document_lifecycle_guide.md §9`) to any related deviation notes in canonical specs

---

## Defect vs Feature Decision Rule

Use this template when the work item is a **deviation from canonical spec behaviour in existing code**.

Use `pre_alignment_run.md` when the work item is **new behaviour not yet defined in any canonical spec**.

If unclear: the Product Owner decides. The decision and rationale are recorded in the Phase Gate Document.

### Boundary cases

| Scenario | Template |
|----------|----------|
| Metric calculates incorrectly (BLG-TECH-01 style) | `defect_run.md` |
| New metric needs adding | `pre_alignment_run.md` |
| API returns wrong field type | `defect_run.md` |
| New endpoint needed | `pre_alignment_run.md` |
| UI displays data inconsistently with spec | `defect_run.md` |
| New UI widget needed | `pre_alignment_run.md` |
| Spec says X, code does Y | `defect_run.md` |
| Spec doesn't cover this case yet | `pre_alignment_run.md` (spec first, then possibly `defect_run.md`) |

---

## Common Failure Modes

| Failure | Symptom | Rule violated | Prevention |
|---------|---------|---------------|------------|
| Implementation before root cause confirmed | Fix solves the wrong problem | GI-5 | Gate RC must pass before FIX_SCOPE |
| Spec updated after implementation | Implementation runs ahead of spec | Spec-first rule | Gate FS.2 requires spec committed before Gate FS passes |
| Expected value derived from implementation | Validation passes incorrect fix | BLG-TECH-01 pattern | Gate FS.3 requires hand-calculated value from canonical spec |
| Regression missed | Fix introduces new defect | GI-3 | Gate V.3 requires explicit regression check against RC.3 surface |
| P0 defect in TRIAGE beyond 2 hours | Escalation timer breach | GI-2 | PMO Lead monitors timer and escalates to Head of Engineering |
| Scope creep during IMPLEMENTATION | Fix grows beyond agreed scope | GI-5 | Any scope question reverts state to FIX_SCOPE |

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-02-21 | Initial version. Created as part of PMO state-machine upgrade alongside pre_alignment_run.md v2.0 and phase_gate_document.md v1.0. Applies the same Global Invariants and Gate Validation Format as the feature process. |