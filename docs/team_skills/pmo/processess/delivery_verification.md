# Delivery Verification

**Owner:** PMO Lead
**Type:** PMO Process Template
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-19

---

## Purpose

This template governs the post-implementation verification phase — the work that happens after engineering has built the feature and before the feature is declared shipped. It defines what the QA Lead verifies, what evidence is required, how defects are handled, and what sign-off looks like.

This is the counterpart to `pre_alignment_run.md`. Where that template ends at "implementation open", this one begins.

The PMO Lead follows this template for every feature. A feature is not shipped until this process is complete.

---

## Where This Sits in the Delivery Lifecycle

```
Pre-Alignment Run (pre_alignment_run.md)
        ↓
        Implementation Open
        ↓
        Engineering builds the feature
        ↓
Delivery Verification (this template)
        ↓
        Feature Shipped
        ↓
Lessons Learnt (lessons_learnt.md)
```

The PMO Lead triggers this template when the Head of Engineering confirms implementation is complete and the feature is ready for verification.

---

## Inputs Required

Before verification begins, confirm all of the following are available:

- [ ] Head of Engineering has confirmed implementation is complete
- [ ] The feature is deployed to the verification environment and accessible
- [ ] The scope document is available at `docs/product/scope/scope--{id}-{slug}.md`
- [ ] The acceptance criteria from the scope document (Section 6) have been reviewed by the QA Lead
- [ ] The QA Lead has confirmed they have enough context to begin — if not, the PMO Lead arranges a brief handoff with the Head of Engineering

If any input is missing, the PMO Lead does not start the clock on verification. The feature sits at "implementation complete, not yet verified."

---

## Phase Overview

```
Phase 1: Verification Execution (QA Lead)
        ↓
Phase 2: Defect Resolution (Engineering + QA Lead)
        ↓
Phase 3: Sign-off (Director of Quality → PMO Lead)
        ↓
        Feature Declared Shipped
```

---

## Phase 1 — Verification Execution

### Goal

The QA Lead executes against every acceptance criterion in the scope document and produces a written verification report. The report is the evidence that the feature behaves as specified. It is not a summary — every criterion must have a recorded outcome.

### Who executes

The QA Lead executes verification. The Head of Engineering does not verify their own work. The PMO Lead does not verify. The QA Lead is the independent executor.

### What the QA Lead tests

The QA Lead works through the acceptance criteria in the scope document Section 6, structured as:

**Backend criteria** — verified via direct API calls (using the application, a test client, or curl). Each criterion must be confirmed against the actual response, not inferred from the frontend behaviour.

**Frontend criteria** — verified by interacting with the live feature in the verification environment. Each widget state, auto-fill behaviour, error condition, and edge case listed in the acceptance criteria must be exercised.

**Regression check** — the QA Lead confirms that existing functionality touched by this feature has not regressed. For 3.2 this means: the Trade Entry form still submits correctly without using the widget; existing positions and settings are unaffected.

### What the QA Lead produces

A verification report filed at:

`docs/product/verification/{id}-{slug}-verification.md`

The report must follow this structure:

```markdown
# Verification Report — {Feature Name}

**Feature:** {roadmap item id} — {feature name}
**Scope document:** docs/product/scope/scope--{id}-{slug}.md
**Verified by:** QA Lead
**Verification environment:** {environment name or URL}
**Date started:** {date}
**Date completed:** {date}

## Verdict
{Pass | Pass with minor observations | Fail — defects raised}

## Acceptance Criteria Results

### Backend

| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| B1 | {criterion text} | ✅ Pass / ❌ Fail / ⚠️ Partial | {evidence or defect ref} |
| B2 | ... | | |

### Frontend

| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| F1 | {criterion text} | ✅ Pass / ❌ Fail / ⚠️ Partial | {evidence or defect ref} |
| F2 | ... | | |

### Regression

| Area | Result | Notes |
|------|--------|-------|
| {existing functionality} | ✅ No regression / ❌ Regression found | {detail} |

## Defects Raised
{List of defects with severity and reference. None if clean pass.}

## Observations
{Optional: anything noted that is not a defect but worth flagging — UX inconsistencies,
performance concerns, minor deviations that are within acceptable tolerance.}
```

### Gate: Phase 1 → Phase 2 (or Phase 3 if clean)

- [ ] Verification report completed and filed
- [ ] Every acceptance criterion has a recorded result — no gaps
- [ ] If all criteria pass: proceed directly to Phase 3
- [ ] If any criteria fail: proceed to Phase 2

---

## Phase 2 — Defect Resolution

### When this phase runs

Only when Phase 1 produced one or more failing criteria. If verification is a clean pass, skip directly to Phase 3.

### Defect severity classification

The QA Lead classifies every defect before handing to engineering:

| Severity | Definition | Blocks shipping? |
|----------|-----------|-----------------|
| **Critical** | Feature does not behave as specified in a way that affects correctness, data integrity, or financial accuracy | Yes — must be resolved before shipping |
| **High** | Feature behaviour deviates from spec in a user-visible way that affects core workflow | Yes — must be resolved before shipping |
| **Medium** | Feature behaviour deviates from spec in a minor user-visible way that does not affect core workflow | At Director of Quality discretion |
| **Low** | Cosmetic or observational — does not affect behaviour | No — logged for future attention |

Critical and High severity defects block shipping. The feature does not move to Phase 3 until all Critical and High defects are resolved and re-verified.

### Defect handling rules

- The QA Lead documents each defect with: the criterion it violates, the observed behaviour, the expected behaviour per spec, and the severity classification.
- The defect is assigned to the Head of Engineering for resolution.
- The QA Lead does not suggest fixes — that is engineering's responsibility.
- When engineering confirms a fix is deployed, the QA Lead re-verifies the specific criterion only. A full re-run is not required unless the fix touches unrelated areas.
- The verification report is updated with the re-verification result.
- The PMO Lead tracks open defects and their resolution status. Engineering does not self-close defects — the QA Lead closes them on re-verification.

### What the QA Lead does NOT do

- The QA Lead does not reinterpret the spec to make a failing criterion pass. If observed behaviour differs from the spec and the QA Lead believes the spec may be wrong, this is escalated to the QA & Testing Owner and the relevant spec domain owner — it is not resolved informally.
- The QA Lead does not negotiate severity with engineering. Severity is a QA determination. Engineering may escalate to the Director of Quality if they disagree, but they do not override the QA Lead's classification directly.

### Gate: Phase 2 → Phase 3

- [ ] All Critical and High severity defects resolved and re-verified
- [ ] Verification report updated with re-verification results
- [ ] No open Critical or High defects remain
- [ ] Medium and Low defects logged and acknowledged (resolution deferred or scheduled)

---

## Phase 3 — Sign-off

### Who signs off

The Director of Quality reviews the completed verification report and issues formal sign-off. The Director of Quality is the accountable owner of release confidence. The PMO Lead does not sign off on quality — that boundary is non-negotiable.

### What the Director of Quality reviews

- The verification report: completeness, verdict, defect disposition
- That no Critical or High defects remain open
- That the regression check was performed
- That the QA Lead who executed is not the same person as the engineer who built the feature (independence check)

### What sign-off looks like

The Director of Quality records sign-off by replying to or annotating the verification report with:

```
Quality sign-off confirmed.
Verified by: [QA Lead name]
Reviewed by: [Director of Quality name]
Date: {date}
Verdict: {Pass | Pass with logged observations}
Feature is cleared for shipping.
```

This text is appended to the verification report document before it is treated as complete.

### If the Director of Quality does not sign off

If the Director of Quality identifies concerns with the verification report — incomplete criteria, disputed defect closures, independence breach — they return it to the QA Lead with specific issues. The PMO Lead does not override this. The feature does not ship until sign-off is granted.

### Gate: Phase 3 → Feature Declared Shipped

- [ ] Verification report complete with no open Critical or High defects
- [ ] Director of Quality sign-off recorded in the verification report
- [ ] PMO Lead notified of sign-off

---

## Declaring the Feature Shipped

When Phase 3 is complete, the PMO Lead coordinates the following closure actions:

- [ ] Roadmap entry updated to `✅ Complete (shipped {version})`
- [ ] Current version number incremented in `docs/product/roadmap.md`
- [ ] Scope document status updated to `Superseded` with reference to the shipped version
- [ ] Changelog entry added at `docs/product/changelog.md`
- [ ] Head of Engineering notified that the feature is officially shipped
- [ ] Lessons learnt review scheduled per `processes/lessons_learnt.md`

The feature is not declared shipped until all closure actions are complete. Updating the roadmap is not optional — it is part of shipping.

---

## Verification Report Filing

All verification reports are filed at:

`docs/product/verification/{id}-{slug}-verification.md`

Naming convention: `{roadmap-item-id}-{feature-slug}-verification.md`

Examples:
- `3.2-position-sizing-calculator-verification.md`
- `3.4-portfolio-heat-gauge-verification.md`

Verification reports are permanent records. They are not superseded or archived — they record what was verified, when, and by whom at the time of shipping.

---

## Common Failure Modes

| Failure | Symptom | Prevention |
|---------|---------|------------|
| Verification skipped | Feature declared shipped without a report | PMO Lead enforces gate — no sign-off, no shipped status |
| Engineering self-verifying | QA Lead bypassed | Director of Quality independence check in Phase 3 |
| Spec reinterpreted to make failing test pass | Failing criterion closed without fix | QA Lead escalates to QA & Testing Owner; does not resolve informally |
| Defect severity negotiated down | Critical becomes Medium to unblock shipping | Severity is QA Lead's determination; appeals go to Director of Quality only |
| Report filed with gaps | Some criteria have no recorded result | Gate check: every criterion must have a result before Phase 1 closes |
| Closure actions skipped | Roadmap not updated, scope doc not superseded | PMO Lead owns the closure checklist; it is part of shipping, not optional admin |

---

## Relationship to Lessons Learnt

The delivery verification phase feeds directly into the lessons learnt review. The PMO Lead should note:

- How long verification took relative to the effort estimate
- Whether any defects were Critical or High severity (indicating a pre-implementation gap)
- Whether any acceptance criteria were ambiguous or untestable (indicating a QA review gap earlier in the process)
- Whether the verification environment was available and stable when needed

These observations belong in the lessons learnt record under "What created friction."

---

## Guiding Principle

> Implementation proves intent was understood.
> Verification proves the implementation is correct.
>
> Neither replaces the other. Both are required before a feature ships.
