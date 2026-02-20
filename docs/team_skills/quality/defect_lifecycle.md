# Defect Lifecycle Process

**Owner:** Director of Quality
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-02-20

---

## Change Log

| Version | Change |
|---------|--------|
| 1.0 | Initial version. Authored following 3.2 delivery — defect management was handled ad hoc during verification. Covers full defect arc from raise to close, Director of Quality sign-off process, and cross-domain escalation path. |

---

## Purpose

This document defines the authoritative process for defect management across the full delivery lifecycle. It covers:

- How defects are raised and what a defect record must contain
- Severity classification
- Assignment, resolution, and re-verification
- Closure and sign-off
- Director of Quality final sign-off criteria
- Cross-domain defect escalation

This process applies to all defects raised during Phase 5 verification. It does not govern bugs found in production — those follow the incident response process.

---

## 1. What Is a Defect

A defect is a divergence between observed system behaviour and behaviour defined in a canonical specification.

A defect is **not**:
- A question about intent (escalate to the relevant spec owner)
- A new feature request (raise as a backlog item)
- An observation — something noticed during testing that is not covered by an acceptance criterion (see Section 8)

If it is unclear whether something is a defect or an observation, the QA Lead escalates to the QA & Testing Owner. If still unclear, the Director of Quality decides.

---

## 2. Defect Severity

| Severity | Definition | Shipping impact |
|----------|------------|-----------------|
| **Critical** | Feature is broken or produces incorrect data. Cannot ship. | Blocks shipping closure until resolved and re-verified |
| **High** | Acceptance criterion fails. Core behaviour is wrong. | Blocks shipping closure until resolved and re-verified |
| **Medium** | Acceptance criterion fails but a workaround exists, or behaviour is clearly wrong but not data-affecting | Blocks shipping closure unless explicitly accepted by Director of Quality with rationale recorded |
| **Low** | Minor deviation from spec. Does not affect correctness or user trust. | Does not block. Recorded in verification report. Raised as backlog item if no immediate fix. |

Severity is assigned by the QA Lead at the point of raising. The Director of Quality may escalate severity if they disagree with the QA Lead's classification — this is recorded in the verification report with rationale.

---

## 3. Raising a Defect

The QA Lead raises defects during Phase 5 verification. Each defect must include:

```
ID:           DEF-{NNN} (sequential within the feature)
Severity:     Critical / High / Medium / Low
Title:        One sentence describing the wrong behaviour
Scenario:     Which test scenario(s) produced this defect (by scenario ID)
Steps to reproduce:
  1. {step}
  2. {step}
Expected result:   {from the test scenario or canonical spec}
Actual result:     {what was observed}
Canonical source:  {spec document and section that defines the expected behaviour}
Hypothesis:        {QA Lead's view on root cause — not authoritative, helps engineering}
Assigned to:       Head of Engineering
Raised:            {date}
Status:            Open
```

Defects are recorded in the verification report. They are not tracked in a separate tool — the verification report is the defect register for Phase 5.

---

## 4. Assignment and Resolution

**Assignment:** All defects are assigned to the Head of Engineering on raise. The Head of Engineering assigns to the relevant engineer and provides an ETA to the QA Lead and PMO Lead.

**Resolution:** Engineering fixes the defect and confirms deployment to the verification environment. The fix confirmation must include:
- What was changed
- Where (file/component)
- Why the fix addresses the root cause

Engineering does not close the defect — only the QA Lead can close it after re-verification.

**Spec implications:** If fixing the defect requires a change to a canonical specification (i.e. the spec was ambiguous or wrong, not the implementation), the spec owner must update the spec before engineering makes the fix. The Head of Engineering raises this to the relevant spec owner. The PMO Lead tracks it. The fix does not proceed until the spec patch is committed.

---

## 5. Re-verification

After engineering confirms deployment of a fix:

The QA Lead re-executes the specific scenario(s) that failed. They do not re-execute the full test suite unless the fix touched shared components that could cause regression — in which case re-execution scope is agreed with the QA & Testing Owner.

Re-verification result:
- **Pass:** QA Lead updates the defect status to Resolved in the verification report. Re-verification date and result recorded.
- **Fail:** QA Lead records the new observation, updates the defect record, and raises with the Head of Engineering again. Severity is reviewed — if the fix made things worse, severity may escalate.

---

## 6. Director of Quality Sign-Off Process

The Director of Quality signs off the verification report once all defects are resolved and the QA Lead confirms the feature is ready for shipping closure.

### What the Director of Quality reviews

Before signing off, the Director of Quality independently reviews:

1. **Acceptance criteria coverage** — every criterion in the scope document has a corresponding scenario, and all scenarios are either Pass or accounted for with a documented rationale (Deferred with completion plan, or Low severity with backlog reference)

2. **Defect resolution completeness** — all Critical and High defects are Resolved with re-verification Pass recorded. All Medium defects are either Resolved or explicitly accepted in writing with rationale. All Low defects are recorded.

3. **Observations** — all observations raised during verification are either closed (raised as backlog items, assigned BLG- reference) or addressed as defects.

4. **Verification report integrity** — the report version history reflects the actual sequence of verification activity. No scenario result has been changed without a corresponding re-verification event.

5. **Independence check** — the QA Lead who executed the scenarios did not author or modify the canonical specifications being tested.

### Sign-off criteria

The Director of Quality signs off when:
- All Critical and High defects are Resolved and re-verified
- All Medium defects are Resolved or formally accepted with rationale
- All acceptance criteria are covered by Pass scenarios
- No open items exist without a documented disposition
- The verification report reflects an accurate record of what was tested and what was found

### Withholding sign-off

If the Director of Quality is not satisfied, they document:
- Which criterion or defect is unsatisfactory
- What is required before sign-off is granted
- Whether this constitutes a shipping block or a conditional condition

This is communicated to the PMO Lead and Product Owner in writing. The PMO Lead updates the Phase Gate Document and communicates to all stakeholders.

The Director of Quality does not withhold sign-off due to delivery pressure. Independence of quality judgement is non-negotiable.

---

## 7. Cross-Domain Defect Escalation

Some defects cannot be assigned to a single canonical owner because they span multiple spec domains — for example, a defect where the API contract, the strategy rules, and the data model all have a bearing on the correct behaviour.

### Identification

A defect is cross-domain when:
- The QA Lead cannot identify a single canonical spec section that definitively resolves the defect
- Engineering's fix would require changes to two or more canonical specs simultaneously
- The Head of Specs Team determines on review that the defect exposes a gap at a domain boundary

### Process

1. The QA Lead flags the defect as cross-domain in the verification report and escalates to the Director of Quality
2. The Director of Quality convenes the relevant canonical spec owners (at minimum the two whose domains are in conflict)
3. The Head of Specs Team mediates — their role is to identify which spec owns the decision and ensure consistency, not to make the content decision themselves
4. The convened owners agree the correct behaviour and which spec(s) need updating
5. The spec patches are committed first, then engineering implements the fix against the updated specs
6. The QA Lead re-verifies against the updated canonical spec

**The Head of Specs Team has the deciding vote** if the convened owners cannot agree. This is recorded in the decisions record for the feature.

### Timeline expectation

Cross-domain defects are given priority escalation. The Head of Specs Team confirms the canonical owner within one working day of escalation. The convened owners resolve the spec question within two working days. Timeline extensions require Director of Quality approval.

---

## 8. Observations

An observation is something noticed during verification that is not covered by an acceptance criterion and is not a defect against a canonical spec — it is notable behaviour, a UX concern, a potential improvement, or a risk flag.

**Raising:** The QA Lead raises observations in the verification report under a separate Observations section using the prefix OBS-{NNN}.

**Classification:** Observations are not defects. They do not block shipping unless the Director of Quality determines the observation reveals an undocumented behavioural gap that should have been an acceptance criterion.

**Pathway to backlog:**
1. QA Lead raises the observation in the verification report with a clear description and why it is notable
2. At shipping closure, the PMO Lead reviews all observations with the Product Owner
3. Product Owner decides: raise as backlog item (BLG-FEAT- or BLG-TECH-), defer, or close as not significant
4. For any observation raised as a backlog item: the PMO Lead assigns a BLG- reference and adds it to `docs/product/backlog.md` with the observation as context
5. The observation record in the verification report is updated with the BLG- reference or closure decision

**Observations are never silently dropped.** Every observation has a recorded disposition before the verification report is filed.

---

## 9. Defect Register Format (Verification Report)

The verification report maintains two registers:

**Active defects** — shown inline within the scenario results table, with full defect records in a dedicated Defects section.

**Defect summary** — a count table at the top of the Defects section:

```
| Severity | Raised | Resolved | Accepted | Open |
|----------|--------|----------|----------|------|
| Critical | N      | N        | —        | 0    |
| High     | N      | N        | —        | 0    |
| Medium   | N      | N        | N        | 0    |
| Low      | N      | N        | —        | 0    |
```

All Open counts must be zero before Director of Quality sign-off is granted.
