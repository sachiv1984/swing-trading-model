**Owner:** Financial Reporting & Records Owner
**Class:** Planning Document (Class 4)
**Status:** Rejected
**Submitted by:** Financial Reporting & Records Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-financial-reporting-20260304-01

---

# Idea: UK Tax Year Performance Summary Endpoint

## 1. Problem Statement

An active trader in the UK must report realised capital gains and losses in their annual self-assessment tax return. The current system provides cumulative P&L and trade history but does not support a tax-year-aligned summary (UK tax year runs April 6 to April 5, not calendar year). A user wishing to complete their tax return must manually extract and aggregate their closed trades by UK tax year from the trade history — a process that is error-prone and time-consuming. Given that the system's purpose is to support the user's trading activity, tax reporting is a direct downstream obligation of using the system.

## 2. Strategic Alignment

Section reference: §3 — Human-in-the-loop execution model; §2 — Strategy intent ("medium- to long-term momentum trends")

Alignment rationale: The strategy is a real trading system with real financial consequences. The financial reporting obligations that arise from the system's outputs — specifically UK capital gains tax on realised positions — are a direct product outcome. Supporting tax year reporting is not a peripheral feature; it is part of the complete value delivery of a trading support system.

## 3. Proposed Solution

Add `GET /analytics/tax-year-summary?year=YYYY` returning: total realised gains (closed trades where exit_price > entry_price), total realised losses (closed trades where exit_price < entry_price), net realised P&L in GBP, total fees paid, and net P&L after fees — all scoped to the UK tax year specified (April 6 YYYY to April 5 YYYY+1). Display in the analytics section with a tax year selector. Include a note that the output is for reference only and the user should verify with their accountant.

## 4. Expected Value

Saves the user 2–4 hours of manual calculation per tax year. Reduces the risk of tax reporting errors caused by manual aggregation. Provides a machine-readable summary that can be used directly in tax preparation. Value grows linearly with the number of trades per year.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires the existing trade history data (already stored with exit_date). UK tax year date logic is straightforward. GBP-normalised P&L must be used (already implemented for closed trades).

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: An analytics endpoint is additive; removing it reverts to current state.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: The UK tax year ends April 5. Users preparing their self-assessment return in the coming months would benefit immediately. Time-sensitive relative to the tax calendar.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | ❌ Rejected |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | N/A — not advanced to STEP 5 debate |
| Outcome date | N/A |
| Notes | |
