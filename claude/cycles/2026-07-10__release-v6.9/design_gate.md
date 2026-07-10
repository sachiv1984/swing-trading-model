**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-10
**Cycle:** 2026-07-10__release-v6.9

# Design Gate Record — 2026-07-10__release-v6.9

## Gate Status: PASSED

Completed: 2026-07-10
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | On-demand pre-entry rule recheck for open positions (BLG-FEAT-64) | Design Required | New user-facing action ("Recheck Compliance") and modal panel on the Positions page; AC-02 is explicitly a visual-rendering AC requiring the same visual pattern as `PreEntryValidationPanel`. | `docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md` v1.0 | `docs/specs/frontend/pages/positions.md` v2.1 | ✅ Cleared | Head of UX & Design |
| ST-02 | Overnight/weekend gap risk flag for open positions (BLG-FEAT-65) | Design Required | New user-facing alert badge and tooltip on the Positions page Alerts column; AC-02/AC-03 are explicitly visual-rendering/interaction-timing ACs. | `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md` v1.0 | `docs/specs/frontend/pages/positions.md` v2.1 | ✅ Cleared | Head of UX & Design |

## Blocked Items (if any)

None.

## Notes

- Both items in this release's scope are the mandatory Product Value Alert pull-forward anchors (BLG-FEAT-64, BLG-FEAT-65) named at roadmap rebalance `2026-07-10__scheduled`; `cycle_summary.md` RISK-02 flagged both as carrying observable UI acceptance criteria requiring this gate before Sprint Planning may seal.
- No existing design artefacts were found for either item (`docs/design/`, `docs/specs/frontend/pages/positions.md` searched) — both required new artefacts (STEP 2.2).
- ST-01 reuses the existing `PreEntryValidationPanel` visual pattern (5 SI-01 rule keys, pass/warn/fail badge palette, override checkbox) per AC-02's explicit instruction — no new colour or component pattern introduced. Positioned as a modal, distinct from the panel's original inline placement on the Trade Plan form, since this is a per-position on-demand check on the Positions page rather than a pre-entry gate on the Trade Plan form.
- ST-02 reuses and extends the existing Alerts column (introduced v6.2 — ST-05, `risk_off_exit`) rather than introducing a new column — the v6.2 design already anticipated multiple stacked alert types in the same cell. New badge colour amber-600 (`#D97706`) confirmed distinct from all existing Positions page badge colours (trail-stop breach orange `#EA580C`, RISK OFF blue-800 `#1E40AF`, lifecycle-state palette).
- Both stories' AC-04 (§13 sign-off by Strategy Rules & System Intent Owner) is a Sprint Execution deliverable, not a Design Gate deliverable — both artefacts document the §13 compliance rationale (no new automation/prediction surface) to support that later sign-off, consistent with `cycle_summary.md` RISK-01/RISK-03 (expected fast pass, SI-01 precedent).
- No disagreements between Product Owner and Head of UX & Design were raised on either item's classification.

## Design-Required Items — Detail

### ST-01
- **2.1/2.2:** No existing artefact; new artefact produced — `docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md` v1.0
- **2.3:** Product Owner approved 2026-07-10
- **3:** `positions.md` v2.0→v2.1 (new "Compliance Recheck Panel" §, Actions column entry added, Grid View quick-links updated). Head of Specs Team confirmed lifecycle compliance (Class 1, version incremented, Last Updated set).

### ST-02
- **2.1/2.2:** No existing artefact; new artefact produced — `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md` v1.0
- **2.3:** Product Owner approved 2026-07-10
- **3:** `positions.md` v2.0→v2.1 (new "Gap Risk Badge" § under existing Alerts Column, Grid View badge list updated). Head of Specs Team confirmed lifecycle compliance (Class 1, version incremented, Last Updated set).
