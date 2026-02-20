# Testing Guide

**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.1
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.1 | Added Section — Observation-to-Backlog Pathway. Defines the formal process from OBS- raise through to Product Owner disposition and BLG- assignment. Fixes gap identified in 3.2 post-delivery assessment (Gap 7.1). Updated header from `Type: PMO Process Template` to `Class: Canonical (Class 1)` following lifecycle guide v2.2 formalisation of PMO process templates as Class 1. |
| 1.0 | Initial version. |

---

## Purpose

This guide answers three questions that must never be ambiguous on any feature:

1. Who writes the test scenarios?
2. When are they written?
3. What format do they follow?

It also clarifies what the QA Lead does with those scenarios during verification, and what a good verification pass looks like in practice.

This guide is mandatory reading before Phase 5 (verification) begins on any feature. The PMO Lead is responsible for ensuring the QA Lead has read it.

---

## The Two Distinct QA Roles

There are two separate roles involved in quality on every feature. Confusing them is a common source of friction.

**QA & Testing Owner** — writes the test scenarios before implementation begins. Works from the canonical specs and scope document. Produces structured, reusable test scenario documents. This is a specification-time activity, not a post-implementation activity.

**QA Lead** — executes the test scenarios after implementation is complete. Works from the test scenario document written by the QA & Testing Owner. Records results, raises defects, and produces the verification report. This is a delivery-time activity.

One role defines what to test and how. The other executes it. They are not interchangeable.

---

## When Test Scenarios Are Written

Test scenarios must be written **during Phase 4** — after QA sign-off on the specs, and before implementation is declared open.

They must not be written during verification. By the time the QA Lead is executing tests, the scenarios should already exist as a structured document. Asking the QA Lead to both figure out what to test and execute the tests at the same time is the root cause of unclear, inconsistent, or missed coverage.

```
Phase 3: QA Review Gate → specs confirmed testable
         ↓
Phase 4: Scope Document + TEST SCENARIOS AUTHORED ← this is when it happens
         ↓
Implementation Open → Head of Engineering starts building
         ↓
Phase 5: QA Lead executes test scenarios against the built system
```

---

## Who Writes the Test Scenarios

**The QA & Testing Owner writes the test scenarios.**

They derive them directly from the canonical specifications confirmed during the QA review gate. The scope document acceptance criteria section is the starting point — the test scenarios give each criterion a concrete, step-by-step execution procedure.

The QA & Testing Owner does not write test scenarios from memory, from the roadmap description, or from conversations. They write them from the specs. If a criterion cannot be derived from the specs, that is a spec gap — escalate to the relevant spec owner before writing the scenario.

**The QA Lead does not write test scenarios.** They execute them. If the QA Lead arrives at Phase 5 and there is no test scenario document, that is a process failure — escalate immediately to the PMO Lead.

---

## Test Scenario Document Format

One test scenario document per feature. Filed at:
`docs/testing/{roadmap-item-id}-{feature-slug}-test-scenarios.md`

### Document header

```markdown
# Test Scenarios — {Feature Name}

**Owner:** QA & Testing Owner
**Class:** Supporting Document
**Status:** Active
**Version:** 1.0
**Last Updated:** {date}
**Derived from:** {list of canonical spec documents with versions}
**For verification by:** QA Lead
```

### Scenario structure

Each scenario follows this format:

```markdown
## {ID} — {Short name}

**Acceptance criterion:** {The criterion from the scope document this scenario covers}
**Derived from:** {Spec document and section}
**Type:** Backend / Frontend / Settings / Integration

**Setup:**
{Any state or preconditions required before executing this scenario}

**Steps:**
1. {Numbered, concrete steps — specific values, not vague descriptions}
2. ...

**Expected result:**
{Exact expected outcome — specific field values, messages, HTTP codes, UI states}

**Notes:**
{Any execution gotchas, environment requirements, or known constraints}
```

### Grouping

Group scenarios in the same order as the acceptance criteria in the scope document:

- Backend scenarios first (API calls, direct endpoint tests)
- Frontend scenarios second (widget states, form interactions, page behaviour)
- Settings scenarios third (if applicable)
- Edge cases and error states last

### Coverage rules

- Every acceptance criterion in the scope document must have at least one scenario
- Every reason code / error state must have its own scenario
- Cross-navigation state scenarios must be included for any component with user-editable state (see `pre_alignment_run.md §Phase 3`)
- Backend scenarios should include both happy path and all documented failure modes

---

## What the QA Lead Does With Test Scenarios

The QA Lead receives the test scenario document before Phase 5 begins. They do not modify it — if a scenario is wrong or unclear, they flag it to the QA & Testing Owner for correction before starting execution.

During verification, the QA Lead:

1. Executes each scenario in order
2. Records the actual result against the expected result
3. Marks each scenario ✅ Pass, ❌ Fail, or ⏭ Deferred (with reason)
4. For any Fail: raises a defect with severity, root cause hypothesis, and steps to reproduce
5. Populates the verification report as they go — not after all scenarios are complete

The QA Lead does not improvise additional tests. If they find a behaviour that seems wrong but is not covered by a scenario, they flag it as an observation and escalate to the QA & Testing Owner to decide whether a new scenario is needed.

---

## Deferred Scenarios

Some scenarios cannot be executed in the standard verification environment — typically those requiring specific database states, network failure simulation, or environment conditions that cannot be reproduced without special access.

When a scenario must be deferred:

- Mark it ⏭ Deferred in the verification report with the reason
- Record what is needed to execute it
- The PMO Lead tracks deferred scenarios as open items — they must be completed before shipping closure
- Deferred scenarios are never dropped — they are completed in a subsequent pass once the environment condition is available

---

## Defect Severity Definitions

Used by the QA Lead when raising defects in the verification report.

| Severity | Definition | Examples |
|----------|------------|---------|
| **Critical** | Feature is broken or unsafe. Cannot ship. | Wrong calculation result, data corruption, form submits incorrect data |
| **High** | Core acceptance criterion fails. Blocks shipping without resolution. | Required UI state not rendering, API returns wrong response code, required field not saved |
| **Medium** | Acceptance criterion fails but a workaround exists, or behaviour is clearly wrong but not data-affecting | Message not displayed, state resets unexpectedly, wrong styling on error state |
| **Low** | Minor deviation from spec. Does not affect correctness. | Cosmetic wording difference, sub-optimal UX that still functions, non-blocking performance issue |

**Observations (OBS)** are not defects — they are things noticed during verification that are not covered by an acceptance criterion and are flagged for Product Owner awareness. The Product Owner decides whether to raise an observation as a defect or log it as a backlog item.

---

## Environment Requirements

The QA Lead should confirm the following before starting verification:

- [ ] Feature is deployed to the verification environment
- [ ] Verification environment has a known, stable dataset (or the QA Lead knows the current state)
- [ ] Any database-level scenarios requiring direct access have been arranged (coordinate with Head of Engineering)
- [ ] The test scenario document version matches the scope document version being verified

If any of the above are not in place, do not start verification. Notify the PMO Lead.

---

## Observation-to-Backlog Pathway

An observation (OBS-) is something noticed during verification that is not a defect against a canonical acceptance criterion but is notable enough to flag — a UX concern, an unexpected behaviour, a performance signal, or a potential improvement. Observations are not defects and do not block shipping unless the Director of Quality determines the observation reveals an undocumented behavioural gap that should have been an acceptance criterion.

**Step 1 — QA Lead raises the observation in the verification report.**

Format:
```
ID:           OBS-{NNN}
Title:        One sentence describing what was noticed
Observed:     What the QA Lead saw
Why notable:  Why this is worth flagging — not a complaint, a specific concern
Spec ref:     If there is a related spec section, reference it. If there isn't, note that.
```

**Step 2 — QA Lead flags all open observations to the PMO Lead at the end of each verification pass.**

Observations are not silently dropped. The PMO Lead tracks them in the Phase Gate Document alongside defects.

**Step 3 — PMO Lead reviews all observations with the Product Owner at shipping closure.**

For each observation, the Product Owner decides one of three dispositions:

| Disposition | What it means | What happens |
|-------------|---------------|--------------|
| **Raise as backlog item** | Worth addressing in a future release | PMO Lead assigns a BLG- reference and adds it to `docs/product/backlog.md` with the observation as context. Observation record updated with BLG- reference. |
| **Address now** | Significant enough to fix before shipping | Treated as a defect from this point — assigned severity, raised to Head of Engineering, re-verified before closure. Director of Quality notified. |
| **Close — not significant** | Not worth further action | Observation record updated with `Disposition: Closed — {reason}`. No further action. |

**Step 4 — Every observation has a recorded disposition before the verification report is Filed.**

The verification report cannot move to Filed status with any observation in an undisposed state. The PMO Lead confirms all observations are disposed before requesting Director of Quality final sign-off.

---

## Quick Reference: Who Does What

| Activity | Owner | When |
|----------|-------|------|
| Confirm specs are testable | QA & Testing Owner | Phase 3 (QA Review Gate) |
| Write test scenario document | QA & Testing Owner | Phase 4 (after QA sign-off) |
| Execute test scenarios | QA Lead | Phase 5 (after implementation complete) |
| Record results and raise defects | QA Lead | Phase 5 |
| Raise observations | QA Lead | Phase 5 (as noticed) |
| Produce verification report | QA Lead | Phase 5 |
| Review observations with Product Owner | PMO Lead | Phase 5 (at shipping closure) |
| Dispose observations (raise, address, or close) | Product Owner | Phase 5 (at shipping closure) |
| Sign off on verification report | Director of Quality | Phase 5 (after all observations disposed) |
| Resolve defects | Head of Engineering | Phase 5 (as raised) |
| Re-verify fixed defects | QA Lead | Phase 5 (after fix deployed) |
| Confirm shipping closure | PMO Lead | After Director of Quality final sign-off |
