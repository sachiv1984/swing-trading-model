**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Advancing
**Submitted by:** Director of Quality
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-director-of-quality-20260304-02

---

# Idea: Golden Output Regression Baseline for CI

## 1. Problem Statement

The current CI gate (`POST /validate/calculations`, EPIC-01) checks that `critical_failed > 0` blocks the merge. This is a pass/fail gate on calculation existence and non-crash behaviour — it does not verify that specific calculations return the correct numeric values. A change that silently alters the trailing stop formula from `CurrentPrice - (2 × ATR)` to `CurrentPrice - (2.1 × ATR)` would pass the current CI gate. This is a category of regression that the current quality system cannot detect.

## 2. Strategic Alignment

Section reference: §11 — Current production parameters ("must be consistent across production backtests, live system logic, and reported performance metrics")

Alignment rationale: The strategy defines exact parameter values and calculation rules. Any implementation that produces numerically different results is wrong by the strategy spec's own authority statement. A golden output regression baseline is the implementation of this requirement in the CI pipeline: it makes the spec's numeric constraints machine-enforceable, not just human-reviewable.

## 3. Proposed Solution

Define a set of deterministic golden test cases: known inputs (entry_price, ATR, risk_percent, etc.) with expected output values derived directly from the canonical strategy spec. Store these in `tests/golden_outputs.json`. Add a CI step that calls the backend with each golden input and asserts the output matches to the required precision. Any numeric divergence from the golden values fails the build. The golden outputs file is treated as a canonical artefact and updated only via a spec-linked PR.

## 4. Expected Value

Catches calculation regressions that the current critical_failed gate misses. Measurable as: number of silent calculation regressions caught per quarter (target: catch 100% of numeric deviations from spec, versus current ~0%). Prevents the class of defect most dangerous in a trading system — a calculation that is wrong but does not crash.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires careful derivation of golden values from canonical specs (not from current implementation — the implementation may already be wrong). Requires agreement on precision tolerances (e.g., 4 decimal places for share counts).

## 6. Reversibility

- [x] Mostly reversible — minor rework required

Reasoning: If golden values are defined incorrectly, they must be revised — but this is a spec clarification exercise, not a destructive change.

## 7. What Would You Stop?

I would stop adding new CI steps that are not spec-grounded. The golden output baseline is the right next step for CI quality before expanding test coverage to new areas.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: This closes the most dangerous gap in the current quality system — numeric correctness — and is a natural progression from the v1.7 CI gate work.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | ✅ Advancing |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | ✅ Advance — promoted to backlog (scope: stop/sizing calcs only) |
| Outcome date | 2026-03-04 |
| Notes | |
