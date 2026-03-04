**Owner:** Financial Reporting & Records Owner
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Financial Reporting & Records Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-financial-reporting-20260304-02

---

# Idea: Explicit Realised vs Unrealised P&L Labelling

## 1. Problem Statement

The current analytics section aggregates P&L across open and closed positions without consistently distinguishing realised P&L (from closed trades — a taxable event in the UK) from unrealised P&L (from open positions — not a taxable event). A user reviewing their "total P&L" may conflate the two, leading to incorrect tax reporting assumptions or incorrect assessments of how much profit has actually been locked in. This is not a display convenience issue — misclassifying unrealised gains as realised gains can cause tax over-reporting, and the reverse can cause under-reporting.

## 2. Strategic Alignment

Section reference: metrics_definitions.md (v1.6.0) — Portfolio Risk Metrics, P&L definitions; §10 — Risk management summary ("currency-aware P&L; cash-flow-adjusted performance tracking")

Alignment rationale: The metrics specification defines P&L but does not explicitly require the realised/unrealised distinction to be surfaced in the user interface. This is a financial reporting governance gap: the system's P&L reporting does not meet the standard required for a user to use the figures for tax purposes without manual reclassification. Financial reporting integrity requires the distinction to be explicit.

## 3. Proposed Solution

Update all P&L displays in the analytics and portfolio sections to carry an explicit label: "Realised P&L (closed trades)" and "Unrealised P&L (open positions)" and "Total P&L." Ensure the API responses (`GET /analytics/*`, `GET /portfolio/summary`) include separate `realised_pnl` and `unrealised_pnl` fields rather than only a combined total. Update the metrics_definitions.md to add the realised/unrealised distinction as a required metric tier.

## 4. Expected Value

Eliminates user confusion between taxable and non-taxable gains. Enables accurate tax reporting directly from system output. Reduces the risk of material tax reporting errors. Required as a prerequisite for the tax year summary endpoint (submitted separately).

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires metrics_definitions.md update (Class 1 canonical change) and API contract updates for affected endpoints. Frontend label changes. All changes must be coordinated through the Head of Specs Team.

## 6. Reversibility

- [x] Mostly reversible — minor rework required

Reasoning: The API field additions are backward-compatible (new fields alongside existing total); removing them requires a deprecation cycle per the API versioning policy.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Should be implemented before the tax year summary endpoint to ensure the underlying P&L data is correctly classified. The two ideas are sequential dependencies.

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
