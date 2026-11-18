**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-18__release-v9.18
**Stories:** ST-12 (BLG-UX-19) — EPIC-02

# Decision Record — Trade Plan Checklist: System Checks as Status, Judgement as Ticks

## 1. Scope of this record

ST-12 splits the Trade Plan Pre-Trade Checklist (`trade_plan.md` §6, `EntryChecklist.js`) into items the system already knows (status) and items only the trader can judge (ticks). Design direction: re-review §13.2 (aviation Do-Confirm checklists), §14.4 "Commit form" template.

Spec impact: `trade_plan.md` v1.29 → v1.30 (§6 rewritten; §13 note amended).

## 2. Data-source and premise check

- **Premise false: "Position size within heat limits".** `strategy_rules.md` (v1.27) sets no portfolio heat limit. The five pre-entry checks (`GET /portfolio/pre-entry-validation`, `portfolio_endpoints.md`) are `regime_gate`, `cash_constraint`, `sector_concentration`, `earnings_proximity` and `sizing_validity`; none tests heat. The What-If preview's `heat_impact_percent` is a value with no limit to test against.
- **Product Owner decision (the user, in session, 2026-11-18):** the item becomes **"Position size checks"**, an automatic status taken from the three size-related pre-entry checks: Cash Constraint (§4.2.4), Sector Concentration (§4.2.2) and Sizing Validity (§4.2.5). No new rule.
- **"Stop level defined"** reads the form's Stop Level field (`planned_stop_price`, `trade_plan.md` §5.1, positive decimal, native currency). Today CHK-03 is pre-ticked from `early_exit_conditions`, a text field; the new status reads the stop itself.
- **§13 note is now stale.** `trade_plan.md` §6 says "No automated condition evaluation … is generated" (`pt05_entry_checklist_s13_review.md`). After ST-12 two items show a deterministic evaluation. They reuse checks already reviewed under SI-01 (the §4.2 rules) and a form field, are advisory (§4.2.6) and gate nothing, so no new §13 review is needed. But the PT-05 review's statement must be amended in ST-12 and confirmed (dated) by the Strategy Rules & System Intent Owner before the build (addendum).

## 3. What the user sees

The section keeps its header "Pre-Trade Checklist" and splits into two groups:

**Checked by the system** (`data-testid="checklist-system"`), no checkboxes:

| Item | Status rule | Text |
|------|-------------|------|
| Position size checks | From the Pre-Entry Validation result: worst status of `cash_constraint`, `sector_concentration`, `sizing_validity` (fail > warn > pass; `skipped` ignored) | pass → "✓ Pass"; warn → "! Warning — see Pre-Entry Checks"; fail → "✗ Fail — see Pre-Entry Checks"; no result yet (shares not entered, loading, error, or all three skipped) → "Not checked yet" (muted) |
| Stop level defined | Stop Level field holds a positive number | "✓ Set: {stop} {currency}" / "✗ Not set" |

- Status colours: `text-app-positive` / `text-app-warning` / `text-app-negative`, and the glyph and word always appear with the colour (colour is never the only signal).
- Each row is plain text with `role="status"`-free markup (no live region, to avoid announcing every keystroke); the row's accessible text is its visible text. It cannot be focused or ticked.
- The status follows the inputs as they change (it reads the same panel result the form already holds, `PreEntryValidationPanel` → snapshot, and the live Stop Level value).

**Your judgement** (`data-testid="checklist-human"`), tickable as today (`role="checkbox"`, Space/Enter, v1.3 keyboard rules unchanged):

- Strategy signal confirmed
- Pre-trade research reviewed

The counter becomes "{n} / 2 confirmed" (human items only); "All complete" becomes "Both confirmed".

**Pause point unchanged:** the pre-entry acknowledgement (§5e) stays the one deliberate pause before "Create Position". The checklist never disables Save (§4.2.6).

**Pre-population:** "Pre-trade research reviewed" keeps its `r_target` pre-tick. CHK-03's `early_exit_conditions` pre-tick is retired with the tick.

**Read-only (detail view):** both groups render; system items show the status computed from the plan's stored `pre_entry_validation_snapshot` and stored Stop Level, with the caption "As checked when the plan was saved, {d MMM HH:mm}". A plan with no snapshot shows "Not checked when saved" for Position size checks.

## 4. Stored data compatibility

- The `checklist` array keeps four entries with the existing ids (`signal_confirmed`, `heat_limit_checked`, `stop_defined`, `research_reviewed`), so old readers see the same shape.
- On save, `heat_limit_checked.checked` = (Position size checks status is pass) and `stop_defined.checked` = (stop set), each with `"auto": true`. Human items save their tick as today.
- On load, saved `checked` values for the two system items are ignored for display (status is recomputed) but not deleted; human items load their saved ticks. Worked example: a v1.29 plan saved with all four ticked, no snapshot, Stop Level 142 → human items ticked; Position size checks "Not checked yet" (form) / "Not checked when saved" (detail); Stop level "✓ Set: 142.00 USD".
- ST-12 greps every reader of `checklist` (first-time-right check 17) — e.g. any analytics or completion count that treats four ticks as "complete" — and runs the legacy-row example through each.

## 5. Worked examples (form)

| Shares | Stop Level | Panel result (cash / sector / sizing) | Position size checks | Stop level defined |
|--------|------------|----------------------------------------|----------------------|--------------------|
| empty | empty | no result | Not checked yet | ✗ Not set |
| 10 | empty | pass / pass / skipped | ✓ Pass | ✗ Not set |
| 10 | 0 | pass / pass / fail | ✗ Fail — see Pre-Entry Checks | ✗ Not set |
| 10 | 142 | fail (cash) / pass / pass | ✗ Fail — see Pre-Entry Checks | ✓ Set: 142.00 USD |
| 10 | 142 | pass / warn / pass | ! Warning — see Pre-Entry Checks | ✓ Set: 142.00 USD |
| 10 | 142 | panel error | Not checked yet | ✓ Set: 142.00 USD |

Market UK: the stop shows in GBP per the existing `currencyForMarket` rule. The checks' input change matrix (ticker, market, shares, stop) is the panel's own; the status re-reads the panel result after each refetch.

## 6. Approvals

- Head of UX & Design: approved (agent-mediated, Design Gate Engine), 2026-11-18.
- Product Owner: approved (the user, in session, 2026-11-18); "Position size checks" chosen by the Product Owner.
- Before build: Strategy Rules & System Intent Owner confirms the amended §13 note (addendum).
