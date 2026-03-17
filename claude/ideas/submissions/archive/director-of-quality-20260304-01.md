**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Parked-cycle-3
**Park Rationale (cycle 2026-03-17__item-v1.10):** v2.0 capacity committed to core initiatives (4.1b Tax-Year P\&L, 4.3 Signal Exposure); Head of Specs Team capacity committed to BLG-GOV-01 and BLG-GOV-02. Will surface as stale next cycle — Product Owner written disposition required.
**Submitted by:** Director of Quality
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-director-of-quality-20260304-01

---

# Idea: Spec-to-Test Traceability Matrix

## 1. Problem Statement

There is no systematic mapping between canonical spec sections and the test cases that validate them. When a spec changes, it is unknown which tests are affected. When a test fails, it is unclear which canonical behaviour it is verifying. The v1.7 EPIC-06 work added spec debt across three endpoint specs — but there is no check that the corrected spec sections are now covered by tests. This is a quality governance gap: we cannot claim spec-defined behaviour is tested without being able to trace which test covers which spec section.

## 2. Strategic Alignment

Section reference: Director of Quality §4.1 — "ensure traceability between specifications and validation artifacts"

Alignment rationale: The Director of Quality's core mandate is to ensure what is specified is testable and what is built is verifiable. A traceability matrix is the structural implementation of this mandate. Without it, the claim that the system behaves as canonically specified cannot be demonstrated — it can only be asserted.

## 3. Proposed Solution

Create `docs/team_skills/quality/spec_traceability_matrix.md` — a Class 2 supporting document mapping each canonical spec section (strategy_rules.md, metrics_definitions.md, all endpoint specs) to the test file and test function that validates it. Maintained by the QA & Testing Owner as part of every spec change PR — no spec section changes without a corresponding matrix update. Gaps (sections with no mapped test) are flagged as unverified and treated as quality risk items.

## 4. Expected Value

Makes test coverage of canonical behaviour visible and auditable. Enables regression risk assessment when specs change: "this section has no test — any change here is unverified risk." Target: 100% of critical spec sections (stopping logic, sizing calculator, grace period) have at least one mapped test within two cycles of adoption.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires initial population by reviewing all existing tests and mapping them to spec sections. Ongoing maintenance requires discipline in the PR review process.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: The matrix is a reference document; removing it does not affect system behaviour or test execution.

## 7. What Would You Stop?

If this is prioritised, I would defer adding new test scenarios until the existing tests are mapped. Building a matrix for an unknown corpus of tests first, then extending from a known baseline, is more efficient.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: The v1.7 CI gate (EPIC-01) validates that calculations don't critically fail but does not verify specific values — the traceability matrix is the next maturity step for the quality programme.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | 🅿 Parked |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | N/A — not advanced to STEP 5 debate |
| Outcome date | N/A |
| Notes | |
