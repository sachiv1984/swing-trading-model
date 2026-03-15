**Owner:** Backend Engineering Patterns Owner
**Class:** Planning Document (Class 4)
**Status:** Promoted-Added
**Submitted by:** Backend Engineering Patterns Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-backend-engineering-20260304-01

---

# Idea: Service Layer Test Coverage Standard

## 1. Problem Statement

There is no minimum test coverage requirement for the backend service layer. The service layer contains all business logic and all canonical calculations — including stop calculation, position sizing, P&L computation, and Sharpe ratio. If these functions lack deterministic unit tests, refactoring is dangerous, and a regression may not be caught until a user notices incorrect output. The current CI gate verifies that the validation endpoint does not critically fail; it does not verify that individual service functions produce the correct results for known inputs.

## 2. Strategic Alignment

Section reference: Backend Engineering Patterns §8 — Canonical Spec Alignment ("if the implementation would produce a different result from what the canonical spec defines, the implementation is wrong")

Alignment rationale: Service layer tests are the implementation-level enforcement of the canonical spec alignment requirement. Without them, spec alignment is verified only at the HTTP integration level (the current CI gate) — not at the calculation level. A minimum coverage standard closes this gap by requiring that every service function has at least one test verifying it against the canonical spec.

## 3. Proposed Solution

Define a minimum 80% line coverage requirement for all files in `backend/services/`. Add `pytest --cov=backend/services --cov-fail-under=80` to the CI pipeline. The 80% threshold is the gate; any PR that reduces coverage below 80% is blocked from merging. Document the standard in `backend_engineering_patterns.md` as a new §11. The standard is reviewed and may be raised in future cycles as coverage matures.

## 4. Expected Value

Catches calculation regressions before deployment. Provides a measurable, auditable coverage baseline. Target: every critical calculation function (stop calculation, sizing, P&L, Sharpe) has a dedicated test suite by the time coverage reaches 80%. Expected to reveal currently untested service functions whose absence of tests represents undetected risk.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires an initial audit of current coverage to determine the gap between current state and 80%. Some new tests will need to be written; the effort depends on the gap size.

## 6. Reversibility

- [x] Mostly reversible — minor rework required

Reasoning: Removing the coverage gate is trivial; removing the tests that were written to meet the gate is low-effort. No architectural lock-in.

## 7. What Would You Stop?

No view — leave to debate. This is a quality infrastructure investment, not a product feature.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: The golden output regression baseline idea (submitted by the Director of Quality) and this idea are complementary — one sets numeric golden outputs, the other ensures service functions are tested. Both should be done together.

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
