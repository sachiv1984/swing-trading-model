**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-21
**Cycle:** 2026-08-21__release-v9.0

# Design Gate Record — 2026-08-21__release-v9.0

## Gate Status: PASSED

Completed: 2026-08-21
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

27 of 27 items cleared — 0 Design Required, 3 Design Pre-Approved via explicit Product Owner downgrade (ST-03, ST-07, ST-10; default per §6 for each was Design Required), 5 further Design Pre-Approved without downgrade (backend/data fixes behind unchanged existing UI), 19 Design Not Applicable. No blocked items. `sprint_planning_pre_condition` is met.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Fix nightly backtest rebalance-date computation | Design Pre-Approved | Backend calculation-path fix; corrects the trade dates populating the existing backtest display, no new component/layout/interaction — same pattern as v8.9 ST-01/ST-02 | N/A | `docs/specs/frontend/pages/strategy_benchmark.md` v0.7 (locked, unchanged) | ✅ Cleared | Head of UX & Design |
| ST-02 | Configure root/app logging to reach Render's captured logs | Design Not Applicable | Ops/logging configuration only, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | Decide "linked journal entries" data source for the AI Post-Trade Debrief | Design Pre-Approved (PO-confirmed downgrade) | Backend data-source decision behind the existing Post-Trade Debrief free-text panel (`trade_history.md` §Post-Trade Debrief); any chosen source (`red_flag_events`, entry/exit notes, or both) renders as text within the existing panel — no new component/layout. §13 pre-check: covering review exists — `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (its Condition 2 sourcing discipline is explicitly extended to this change per BLG-BE-108's own scope note). Default per §6 is Design Required ("new data displayed") — Product Owner explicitly accepted the lower classification. | N/A | `docs/specs/frontend/pages/trade_history.md` v1.12 (locked; re-open only if implementation adds a new visible field/label, not just backing text) | ✅ Cleared | Product Owner (downgrade), Head of UX & Design |
| ST-04 | Fix debrief-generation prompt's unverifiable cross-trade pattern language | Design Pre-Approved | Backend prompt/verification-logic fix to the same existing Post-Trade Debrief panel; no UI change. §13 pre-check: covering review exists — `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (its Condition 9 numeric cross-check is the mechanism this story adjusts). | N/A | `docs/specs/frontend/pages/trade_history.md` v1.12 (locked, unchanged) | ✅ Cleared | Head of UX & Design |
| ST-05 | Consolidate backtest_rule_service.py with production_strategy.py | Design Not Applicable | Pure internal code consolidation; regression-verified to produce identical historical results, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Audit and backfill open positions against breakeven-floor stop invariant | Design Pre-Approved | DB audit/correction via the existing floored-calculation path; corrects values populating existing `positions.md` stop tiles, no new component/layout/interaction — same pattern as v8.9 ST-01/ST-02 | N/A | `docs/specs/frontend/pages/positions.md` v2.8 (locked, unchanged) | ✅ Cleared | Head of UX & Design |
| ST-07 | Decide/apply treatment for `trade_plans.setup_type="Other"` | Design Pre-Approved (PO-confirmed downgrade) | Direct continuation of v8.9 ST-13's identical decision item (same setup_type conflation), previously downgraded on the same rationale: any chosen treatment affects `win_rate_by_setup_type` backend query logic only, reusing existing form-validation patterns, introducing no new component. | N/A | No frontend spec change anticipated; re-open if implementation surfaces a UI-visible change | ✅ Cleared | Product Owner (downgrade), Head of UX & Design |
| ST-08 | Add a lock around `ensure_trade_plans_table()`'s memoization flag | Design Not Applicable | Backend concurrency fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Down-migration rollback verification tests | Design Not Applicable | DB migration testing, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Close What-If Sizing Preview FX-rate reproducibility gap (US-market) | Design Pre-Approved (PO-confirmed downgrade) | Either scope outcome reuses an existing pattern: (a) an FX-rate override field mirroring the field already established in `TradeEntry.js`'s `PositionSizingWidget` verbatim, introducing no new interaction pattern; or (b) a spec-wording-only fix with no UI change at all. Default per §6 is Design Required — Product Owner explicitly accepted the lower classification given the reuse-only nature of both possible outcomes. | N/A | `docs/specs/frontend/pages/trade_plan.md` v1.9 §5d.3 (re-open only if the chosen field placement/labelling deviates from the existing `PositionSizingWidget` pattern) | ✅ Cleared | Product Owner (downgrade), Head of UX & Design |
| ST-11 | Playwright coverage for UK-market position on `current_trailing_stop_native` | Design Not Applicable | Test coverage for existing rendering, no product/UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Production database backup/restore drill | Design Not Applicable | Ops procedure/drill, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Automated staging smoke test on deploy/merge | Design Not Applicable | CI/CD, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Staging environment drift detector | Design Not Applicable | CI/CD/ops, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | Confirm production `PUBLIC_URL` is set in the Render dashboard | Design Not Applicable | Ops config confirmation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | CI safeguard for `PUBLIC_URL`/asset-path regressions on GitHub Pages deploy | Design Not Applicable | CI/CD, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Arc 5 QA protocol | Design Not Applicable | Test protocol documentation + Playwright coverage of an existing flow, no new UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Visual regression baseline snapshots | Design Not Applicable | Test-infrastructure baseline capture of existing components, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | R-multiple calculation regression test | Design Not Applicable | Test-only, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Playwright coverage gap audit for `Arc5ComplianceSection` | Design Not Applicable | Audit + backlog filing only, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Standalone axe-core accessibility CI scan | Design Not Applicable | CI/CD, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | Publish backend test coverage report to PR comments | Design Not Applicable | CI/CD, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Backend service-layer boundary review | Design Not Applicable | Internal backend refactor review, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | Database connection pool tuning review | Design Not Applicable | Infra tuning, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | Render hosting tier review | Design Not Applicable | Ops/cost review, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | Render hosting cost trend dashboard | Design Not Applicable | Internal FinOps reporting artefact (Owner: FinOps & Resource Architect); not a product-frontend page, no end-user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Quarterly dependency minor-version upgrade cadence policy | Design Not Applicable | Process policy + dependency version bumps, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items

None.

## Notes

- **§13 pre-check scope:** Every item was checked against the mandatory §13 boundary pre-check (STEP 1). ST-03 and ST-04 both touch the existing AI Post-Trade Debrief feature (v8.9 ST-06, BLG-FEAT-90) and are covered by its existing §13 review — `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (CONDITIONAL, 9 binding conditions) — neither introduces a *new* AI-provider call, so no fresh §13 review is required; paths recorded in the Rationale column per STEP 1. No other item in this cycle's scope introduces or extends a call to an AI/LLM provider.
- **Downgrade decisions (§6/STEP 1 disagreement-resolution rule):** ST-03, ST-07, and ST-10 each default to Design Required under §6's literal criteria ("new data displayed" / new form field) but were explicitly downgraded to Design Pre-Approved by Product Owner, each on documented reuse-of-existing-pattern grounds (see rationale column). ST-07 is a direct continuation of v8.9 ST-13, which received the identical downgrade on the identical rationale. As with that precedent, if any of these three items' implementation surfaces a genuinely new UI element not covered by the stated reuse rationale, it must be returned to this gate before merge rather than shipped under this classification.
- **Motion/timing-sensitive interactions (§6):** No item in this cycle's scope touches animation easing/duration, debounce/throttle intervals, or delay-before-show thresholds. The rule does not apply this cycle.
- **Frontend specs:** No spec file required an update this cycle — every item touching a spec-covered surface (ST-01, ST-03, ST-04, ST-06, ST-10) is a backend/data-source change behind an already-current spec (`strategy_benchmark.md` v0.7, `trade_history.md` v1.12, `positions.md` v2.8, `trade_plan.md` v1.9), confirmed unchanged and locked as the Sprint Planning reference. STEP 3 (Frontend Spec Updates) was not required.
- **No design artefacts produced this cycle:** all 27 items cleared as Design Pre-Approved or Design Not Applicable; none required STEP 2 (Design Required artefact review). `docs/design/2026-08-21__release-v9.0/` was not created.
