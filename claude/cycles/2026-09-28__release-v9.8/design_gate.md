**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-28
**Cycle:** 2026-09-28__release-v9.8

# Design Gate Record — 2026-09-28__release-v9.8

## Gate Status: PASSED

Completed: 2026-09-28
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Migrate remaining `toFixed`/`toLocaleString` call sites to the shared formatting helper | Design Required | Slice flags `design_gate_required: true` (BLG-FE-184); extends already-approved formatting/exact-zero-colour convention to remaining sites — no new design work | `docs/design/2026-09-28__release-v9.8/shared-formatting-helper-migration/decision_record.md` | N/A — canonical convention lives in `design_system.md` §Number and Currency Formatting (outside `docs/specs/frontend/pages/`), unchanged | ✅ Cleared | Head of UX & Design |
| ST-02 | Drive Screener/Watchlist table body cells from the shared column definitions | Design Required | Slice flags `design_gate_required: true` (BLG-FE-185); single-source-of-truth architecture note, no visual change | `docs/design/2026-09-28__release-v9.8/screener-watchlist-shared-column-definitions/decision_record.md` | `screener_results.md` v1.8; `watchlist.md` v0.9 | ✅ Cleared | Head of UX & Design |
| ST-03 | Tax Year restated-months notice links to a Monthly view that actually shows the counted months | Design Required | Slice flags `design_gate_required: true` (BLG-FE-190); genuine interaction-flow gap (link unscoped by year) — new Tax Year filter on Monthly tab | `docs/design/2026-09-28__release-v9.8/tax-year-restated-notice-year-scoped-link/decision_record.md` | `reports.md` v0.20 | ✅ Cleared | Head of UX & Design |
| ST-04 | SystemStatus.js `categorizeEndpoint()` has no case for `/replay` | Design Required | Slice flags `design_gate_required: true` (BLG-FE-191); new dashboard category label | `docs/design/2026-09-28__release-v9.8/system-status-replay-categorisation/decision_record.md` | `system_status.md` v1.2 | ✅ Cleared | Head of UX & Design |
| ST-05 | Responsive-table behaviour spec for Positions, TradeHistory and TradePlans | Design Pre-Approved | Spec-authoring only — documents existing shipped behaviour, no UI change | N/A | `positions.md` v2.9 / `trade_history.md` v1.13 / `trade_plan.md` v1.16 (locked reference; this story authors new spec sections within them) | ✅ Cleared | Head of UX & Design |
| ST-06 | Canonical keyboard-shortcut inventory spec | Design Pre-Approved | Spec-authoring only, no UI change | N/A | New standalone doc — no existing page spec affected | ✅ Cleared | Head of UX & Design |
| ST-07 | Remaining ad hoc `timeout=`/retry call sites | Design Not Applicable | Backend-only, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Extend float→Decimal fee-rounding audit to tax-year statements | Design Not Applicable | Backend calculation only, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Golden-fixture CI regression for AI prompt templates | Design Not Applicable | CI/test tooling, no UI. §13 pre-check: not applicable — no AI-calling endpoint introduced or extended, only test coverage of existing templates | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | E2E test for JSON root logger | Design Not Applicable | CI/test tooling, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Playwright duration-assertion coverage for toast timing | Design Not Applicable | Test coverage only, no new UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Regression coverage for motion-timing values | Design Not Applicable | Test coverage only, no new UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Escaped-defect and follow-on-ratio tracking | Design Not Applicable | Governance metrics, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | DoQ checklist addendum for AI-touching stories | Design Not Applicable | Process/governance document, no UI. §13 pre-check: not applicable | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | Mutation-testing pilot on sizing calculator and stop ratchet | Design Not Applicable | Backend test tooling, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Enable Playwright trace/screenshot retain-on-failure | Design Not Applicable | CI tooling config, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Staging-redeploy verification check | Design Not Applicable | Infra/ops, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Pre-approved staging-DB query pattern allow-list | Design Not Applicable | Ops documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Harden non-registry dependency guard | Design Not Applicable | CI/security tooling, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Document idempotency/double-submit behaviour for mutating endpoints | Design Not Applicable | API contract documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Error-payload examples for 10 most-called endpoints | Design Not Applicable | API contract documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | Field-level openapi.yaml authoring pass for 20 thin schemas | Design Not Applicable | API contract documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Response schemas for POST/DELETE trade-plans endpoints | Design Not Applicable | API contract documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | Document `trade_plans` CHECK constraint / DS-04 | Design Not Applicable | Data model documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | `oneOf` modelling for `OperationalHealthResponse.ai_journal` | Design Not Applicable | API schema documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | screener_results.md column list omits Earnings column | Design Pre-Approved | Documentation catch-up to already-shipped UI (`SCREENER_COLUMNS`); no UI change | N/A | `screener_results.md` v1.8 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-27 | trade_reflection.md missing-value glyph and shared-helper formatting | Design Required | Visible glyph/content correction + formatting-source consolidation | `docs/design/2026-09-28__release-v9.8/trade-reflection-em-dash-consistency/decision_record.md` | `trade_reflection.md` v0.3 | ✅ Cleared | Head of UX & Design |
| ST-28 | sprint_velocity_trend_chart.md trend sentence correction | Design Not Applicable | Internal governance document (metrics narrative), not product UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 | Reconcile IT-06 §13 review with shipped Alpaca sync behaviour | Design Not Applicable | Compliance/governance reconciliation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 | Bake accessible-name/heading-order rules into Base44 prompt template | Design Not Applicable | Prompt-template governance artefact guiding future page generation, not a direct product UI change this cycle. §13 pre-check: not applicable — no new AI call, tunes an existing generation prompt's content | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 | PVR/Skill-Silo measurement package | Design Not Applicable | Governance metrics, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 | Delivery-flow metrics (lead time, ready-pool runway) | Design Not Applicable | Governance metrics, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 | Persist STEP 7.2 role-share tallies as structured history | Design Not Applicable | Governance tooling, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 | JSON Schema for `.claude_current_state.json` | Design Not Applicable | Governance tooling, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 | Size grep-and-fix-everywhere/verify-live-environment story classes higher | Design Not Applicable | Governance process calibration note, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 | strategy_rules.md §13.5 roster missing PO-05 row | Design Not Applicable | Governance document correction, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 | governance_sync.yml phased-story issue auto-close gap | Design Not Applicable | CI/governance tooling, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-38 | Scheduled trigger for 90-day post-ship AI feature usage review | Design Not Applicable | Governance process/scheduling, no UI. §13 pre-check: not applicable — a review-scheduling mechanism, not an AI call | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 | PO-04 needs its own §13 boundary review as a trackable item | Design Not Applicable | Governance tracking item, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items (if any)

None.

## Notes

- **§6 Motion/timing check:** none of the 39 items touch an existing motion/timing parameter (easing, duration, debounce/throttle, delay-before-show) — ST-11 and ST-12 (EPIC-03) *add test coverage* for already-shipped timing values (ST-42/ST-41 precedent) without changing any parameter, so the "always Design Required" motion/timing rule does not apply to them.
- **§13 AI-boundary pre-check (STEP 1):** reviewed all 39 items for AI-provider-calling introductions or extensions. None found. ST-09, ST-14, ST-30 and ST-38 are AI-adjacent (test coverage of prompt templates, a DoQ process addendum, a page-generation prompt template edit, and a usage-review scheduling mechanism respectively) but none introduces or extends an actual call to an AI/inference service — flagged individually above, no `§13 PRE-CHECK REQUIRED` gate fired.
- **Post-Gate-Correction Addendum (§4.1):** not used this cycle — no correction to the sealed `stage4_backlog_slice.md` was surfaced by this gate's classification or design work. `stage4_backlog_slice_addendum.md` was not created.
- **Design Required items (5 total — ST-01, ST-02, ST-03, ST-04, ST-27):** all had no pre-existing cycle-specific design artefact, so Head of UX & Design produced new decision records under `docs/design/2026-09-28__release-v9.8/` per STEP 2.2; Product Owner approved each per STEP 2.3; Frontend Specifications & UX Documentation Owner updated the corresponding `docs/specs/frontend/pages/*.md` spec(s) per STEP 3; Head of Specs Team confirmed lifecycle compliance (version bump, Last Updated field capped at current + 2 prior per CLAUDE.md §2, Design Source cross-reference) on each: `screener_results.md` (1.7→1.8), `watchlist.md` (0.8→0.9), `reports.md` (0.19→0.20), `system_status.md` (1.1→1.2), `trade_reflection.md` (0.2→0.3).
- **ST-01's frontend-spec disposition** is the one departure from "every Design Required item gets a `docs/specs/frontend/pages/` edit": its canonical contract lives entirely in `design_system.md` (outside this routine's page-spec write scope) and is unchanged by the migration, so there is no page-spec wording to update — recorded as N/A rather than forced into an unrelated page spec. Same disposition precedent as `reports.md` v0.9 ("existing artefact reviewed and confirmed current — no new design work required").
- **ST-05/ST-06/ST-26 (Design Pre-Approved):** per §6, spec-authoring/spec-catch-up items with no UI change require no Head of UX & Design artefact; the current spec version is recorded in the Frontend Spec column as Sprint Planning's locked reference, per STEP 1's instruction for this classification.
