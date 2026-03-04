**Owner:** Strategy Rules & System Intent Owner
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Strategy Rules & System Intent Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-strategy-owner-20260304-02

---

# Idea: ATR Parameter Sensitivity Analysis

## 1. Problem Statement

The current production ATR period (14 days) and ATR multipliers (5× for losing positions, 2× for profitable positions) are documented in §11 as "current production configuration" but there is no evidence in any document that these values were selected through analysis rather than convention. If they are conventional defaults, every stop calculated by the system may be suboptimally calibrated. Section 12.3 requires that any parameter change "state the rationale and expected impact" — but the same requirement should apply to the original choice of parameters. The rationale for the current values is missing.

## 2. Strategic Alignment

Section reference: §12 — Parameter governance; §12.3 — Change control requirements ("any parameter change must: state the rationale and expected impact")

Alignment rationale: The strategy document is explicit that parameters "describe how the strategy currently expresses its intent." Intent cannot be expressed correctly by parameters chosen without analysis. Performing a one-time sensitivity analysis directly satisfies the spirit of §12.3 for the existing parameter values — providing the evidence that should have accompanied the original parameter selection.

## 3. Proposed Solution

Commission a one-time analytical study using all historical closed trades: rerun each closed trade with ATR periods of 10, 14, and 21 days and with multiplier variants (initial: 3×, 5×, 7×; profit: 1.5×, 2×, 3×). Report the delta in total P&L, win rate, average holding days, and average R-Multiple for each variant. Document the findings as a strategy decision record regardless of whether parameters change. If the analysis confirms 14 days and the current multipliers are optimal, that evidence becomes the rationale. If not, the Strategy Owner proposes a change through the §12.3 process.

## 4. Expected Value

Either validates the current parameters with evidence (eliminating a latent governance gap) or identifies better parameters with quantitative backing. Either outcome satisfies §12.3's rationale requirement. If even one multiplier is shown to improve the Sharpe ratio by ≥5%, the financial value of the change across the strategy lifetime far exceeds the analysis cost.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires access to all historical closed trade data and a backtest runner that can apply alternative parameters. The analysis should be implemented in a standalone script, not as a production feature.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: The sensitivity analysis produces a document and optionally a parameter change proposal. Both are reversible.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Soon — worth debating in the next 2–3 cycles

Reasoning: High analytical value, but should not block delivery work. The right timing is when the system has at least 50 closed trades to provide a meaningful statistical sample.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | |
| Classification date | |
| Classified by | Product Owner |
| STEP 5 outcome | |
| Outcome date | |
| Notes | |
