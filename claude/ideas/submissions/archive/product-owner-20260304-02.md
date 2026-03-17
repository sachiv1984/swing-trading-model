**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Rejected
**Submitted by:** Product Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-product-owner-20260304-02

---

# Idea: Portfolio Benchmark Comparison

## 1. Problem Statement

The user has no way to evaluate whether the momentum strategy is outperforming passive market exposure. Absolute returns are reported but there is no benchmark to contextualise them. Without a benchmark, a 12% annual return looks good in isolation but might be underperforming the FTSE 100 by 3 percentage points. The absence of benchmark comparison makes it impossible to assess the strategy's value versus a passive alternative, which is the fundamental question every active trader should be able to answer.

## 2. Strategic Alignment

Section reference: §2 — Strategy intent (non-negotiable)

Alignment rationale: The strategy is designed to "capture medium- to long-term momentum trends" and defend profits asymmetrically. These claims can only be validated if the user can compare strategy returns to a passive benchmark over the same period. Adding benchmark comparison directly supports evaluating whether the strategy intent is being realised in practice, without changing any trading rules.

## 3. Proposed Solution

Allow the user to select a benchmark index (FTSE 100, S&P 500) from a settings option. Display benchmark total return alongside portfolio return for the same time period in the analytics section. Show a benchmark-adjusted return (portfolio return minus benchmark return) as a headline metric. No changes to position entry, stop calculation, or exit rules are required.

## 4. Expected Value

Enables the user to answer "is this strategy beating the market?" quantitatively. The benchmark-adjusted return metric directly measures strategy value. If the strategy underperforms, the user can take action; if it outperforms, the user has evidence that the approach is working. This is a Tier 1 decision-support metric that currently does not exist in the system.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires a data source for benchmark index returns (e.g., a market data API or manually maintained index values). No changes to core trading logic required.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: The benchmark display is purely additive; removing it leaves all existing functionality unchanged.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Soon — worth debating in the next 2–3 cycles

Reasoning: High strategic value but requires a market data source dependency that should be designed carefully. Worth prioritising soon given its importance to strategy evaluation.

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
