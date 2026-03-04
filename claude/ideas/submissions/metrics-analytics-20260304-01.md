**Owner:** Metrics Definitions & Analytics Canonical Owner
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Metrics Definitions & Analytics Canonical Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-metrics-analytics-20260304-01

---

# Idea: R-Multiple Distribution Report

## 1. Problem Statement

The current analytics section shows aggregate metrics — total P&L, overall Sharpe ratio, win rate — but not the distribution of individual trade outcomes in R-Multiple terms. The user cannot see whether they are running winners long enough (positive R-Multiple tail), cutting losers too late (large negative R-Multiple outliers), or whether the distribution is symmetric. The aggregate Sharpe ratio answers "is the strategy producing risk-adjusted returns?" but not "is the asymmetric risk design working as intended?" — which requires a distributional view. This is a missing analytical signal.

## 2. Strategic Alignment

Section reference: §2 — Strategy intent ("enforce asymmetric risk: losses are tolerated; gains are defended")

Alignment rationale: The R-Multiple distribution is the direct measurement of whether the strategy's asymmetric risk intent is being achieved in practice. A distribution that shows many large positive R-Multiples (winners run long) and small negative R-Multiples (losers cut relatively quickly relative to initial risk) validates the design. A distribution that shows the opposite reveals a problem with strategy execution. This is the metric most directly tied to the core strategy intent.

## 3. Proposed Solution

Add `GET /analytics/r-multiple-distribution` returning a histogram of R-Multiple outcomes for all closed trades, bucketed by range (< −3, −3 to −1, −1 to 0, 0 to 1, 1 to 3, > 3). Display as a bar chart in the analytics UI alongside the existing aggregate metrics. Include summary statistics: median R-Multiple, 25th and 75th percentile, and count per bucket. R-Multiple is already a defined critical metric in the analytics spec; this is a distributional view of an existing metric.

## 4. Expected Value

Directly measures whether the asymmetric risk design intent is being achieved. Actionable: if the distribution reveals systematic early winners or late losers, the user can adjust their exit behaviour. Fills a gap in the analytics coverage that the aggregate Sharpe ratio cannot fill. Expected to be in the top three most-reviewed analytics views once available.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires the R-Multiple calculation to be implemented consistently in the backend (it may already exist in analytics_service.py — needs verification). No strategy rule changes required.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: Adding an analytics endpoint is purely additive; removing it reverts to current state.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: This is the most direct measurement of whether the core strategy intent is working. It should have been in the system from the beginning.

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
