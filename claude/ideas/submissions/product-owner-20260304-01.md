**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Product Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-product-owner-20260304-01

---

# Idea: Weekly Performance Email Digest

## 1. Problem Statement

The system only shows real-time portfolio state when the user actively visits the dashboard. There is no push channel that keeps the user informed of performance, open stop distances, or triggered exit recommendations without requiring a login. A user who is travelling or away from their desk for several days may miss a critical exit recommendation, resulting in a position held past its stop — the exact outcome the strategy is designed to prevent.

## 2. Strategic Alignment

Section reference: §3 — Human-in-the-loop execution model

Alignment rationale: The system is designed so that exit signals require manual confirmation. For the human-in-the-loop model to work reliably, the human must be reachable. A weekly digest — and ideally a same-day notification for triggered exit recommendations — ensures the decision-support intent reaches the user even when they are not actively monitoring the dashboard. This strengthens the human-in-the-loop model rather than replacing it.

## 3. Proposed Solution

Generate a weekly email or push notification summarising: (1) current open positions with stop distances and P&L, (2) any exit recommendations triggered in the past 7 days and whether they were actioned, and (3) the weekly portfolio P&L movement. For exit recommendations, send a same-day notification rather than waiting for the weekly digest. No trade execution occurs — this is pure decision support delivered to the user's inbox.

## 4. Expected Value

Reduces the risk of missed exit recommendations from ~100% likely when the user is away to near-zero. The number of positions held past their stop due to the user not seeing the recommendation should reduce to zero in weeks where a digest is delivered. Secondary benefit: weekly performance awareness without requiring daily logins increases user engagement and strategy discipline.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires an email/notification delivery mechanism (SMTP or third-party service). No changes to strategy rules or calculation logic required.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: The feature is additive — disabling it reverts to current state with no data loss or structural change.

## 7. What Would You Stop?

No view — leave to debate. This feature is additive and low-risk; the trade-off question is about priority versus other roadmap candidates, not displacement of existing functionality.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Every day without this feature is a day when a missed exit recommendation is a latent risk — the cost of inaction is real and ongoing.

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
