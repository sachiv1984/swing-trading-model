**Owner:** Head of UX & Design
**Cycle:** 2026-09-14__release-v9.4
**Story:** ST-17 (BLG-FR-03, EPIC-04)
**Status:** Approved

# Decision Record — Carried-Forward-Loss Field on the Tax-Year P&L Statement

## Context

UK capital-gains tax rules allow a net loss in one tax year to be carried forward and offset against gains in a future year. `reports.md`'s Tax Year P&L Summary Bar (§Summary Bar) currently shows only the selected year's own `total_realised_pnl` — it has no field representing a loss carried in from a prior year, nor any mechanism for computing one (no cross-year aggregation exists anywhere in the current API surface).

## Decision

1. **Placement:** a new row in the Summary Bar, directly below `total_realised_pnl` — **"Carried Forward Loss"** — shown only when the value is non-zero (a year with no carried-forward loss shows nothing extra, not a `£0.00` row, consistent with the existing Avg P&L/Trade "—" zero-trade convention).
2. **Status this iteration: Design Only — Implementation Pending**, per the same convention already used for §Arc 5 Compliance Summary and §Gross vs Net Comparison (`reports.md` v0.8 precedent). No backend field currently computes a cross-year carried-forward figure, and none is added this cycle — ST-17 is a frontend/spec story with no corresponding backend AC. This satisfies the story's AC alternative ("explicit informational-only status stated for this iteration") rather than the "calculation behaviour documented" branch, since there is no live calculation to document yet.
3. **Field mapping (locked, ready to implement):** `carried_forward_loss_gbp` (new field on the `summary` object in `GET /reports/tax-year`'s response) — computed as the prior tax year's `total_realised_pnl` if negative, else `0`/absent; does not itself compound across more than one prior year in this initial design (multi-year carry-forward chaining is out of scope, flagged as a future extension if a user need surfaces).
4. **Display:** red text (loss convention, matching `total_realised_pnl`'s existing red-for-negative rule), preceded by a muted label "Carried forward from `<prior_tax_year_label>`" for traceability.
5. **Disclaimer interaction:** the existing page disclaimer ("This report is provided for user reference only... seek qualified tax advice") already covers this figure — no separate disclaimer needed, but the field's tooltip/caption should state it is an estimate pending user confirmation against their own HMRC records, since carried-forward loss rules have UK tax-specific eligibility conditions this system does not evaluate.

## Rationale

Follows the existing "Design Only" precedent exactly (`reports.md` v0.8) rather than inventing a new spec-authoring convention — a reader of the spec already knows how to interpret that status marker. Locks the field mapping now so implementation, if scheduled, does not require a second design pass.

## Sign-off

Head of UX & Design: Approved, 2026-09-14.
Financial Reporting & Records Owner: Approved, 2026-09-14.
Product Owner: Approved, 2026-09-14.
