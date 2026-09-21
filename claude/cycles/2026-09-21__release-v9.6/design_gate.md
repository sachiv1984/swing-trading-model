**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-21
**Cycle:** 2026-09-21__release-v9.6

# Design Gate Record — 2026-09-21__release-v9.6

## Gate Status: PASSED

Completed: 2026-09-21
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

32 of 32 items cleared — 8 Design Required (ST-01 to ST-08, all with an approved decision record and an updated frontend spec), 1 Design Pre-Approved (ST-24), 23 Design Not Applicable. No blocked items. `sprint_planning_pre_condition` is met.

**Classification note:** the sealed slice flagged EPIC-01 (6 items) and EPIC-02 as carrying observable UI acceptance criteria (`design_gate_required: true`). STEP 1 confirmed all 8 as genuinely design-relevant: ST-01 to ST-06 (new/changed interactions and displayed data across the Trade Plans list, Screener, Watchlist, Notifications, every empty state, and three tables) and ST-07/ST-08 (new data displayed on Monthly P&L). ST-06 was classified Design Required although it reads as a "pure refactor": its AC requires "identical negative/decimal conventions" across three tables, no spec defined such a convention, and the migration visibly changes output — so the convention had to be decided at this gate, not during implementation. No item qualified under the §6 motion/timing special rule (BLG-FE-131); the 48 h in ST-04 is a business rule, not a UI motion parameter.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | 'Clone as new plan' action on the Trade Plans list | Design Required | New interaction (list-row link + detail button) and new pre-populated form flow. Slice's non-existent `planned` status corrected to `draft` (addendum). | `docs/design/2026-09-21__release-v9.6/trade-plan-clone/decision_record.md` (new) | `trade_plan.md` v1.14 → v1.15 (§2, §4.2, new §4.5, §7) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-02 | Flag stale 'planned' trade plans on the Trade Plans list | Design Required | New visual marker on the list. `planned` → the four pre-entry statuses; age from `updated_at`, `N > 14` (addendum). Reuses the Watchlist staleness visual language. | `docs/design/2026-09-21__release-v9.6/trade-plan-stale-marker/decision_record.md` (new) | `trade_plan.md` v1.15 (§4.2, new §4.6) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-03 | CSV export for Screener results and Watchlist | Design Required | New control and download interaction on two pages. Reuses Reports' "Download CSV" pattern. | `docs/design/2026-09-21__release-v9.6/screener-watchlist-csv-export/decision_record.md` (new) | `screener_results.md` v1.6 → v1.7 (§5.3); `watchlist.md` v0.7 → v0.8 (Page Header, §CSV Export) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-04 | In-app reminder to complete TradeReflection within 48 hours | Design Required | New notification type and feed row, new email-preference row, and a new re-entry path to a route-less modal. §13 pre-check: deterministic, no AI call. | `docs/design/2026-09-21__release-v9.6/reflection-reminder/decision_record.md` (new) | `notifications.md` v0.8 → v0.9 (§Reflection Reminder Row, §Email Preferences) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-05 | Name one primary next action in every empty state | Design Required | Changes the visible content of ~14 empty states; needs a defined rule, exclusion criterion and audit baseline for the AC to be measurable. | `docs/design/2026-09-21__release-v9.6/empty-state-next-action/decision_record.md` (new; holds the 20-site baseline) | `design_system.md` v1.20 → v1.21 (§Data States, Next-action rule) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-06 | Single number/currency formatting helper — three tables | Design Required | Visible-output change with no existing spec convention (found: mixed `−`/`-`, unsigned P&L cell, 1 dp vs 2 dp R, no grouping). Convention fixed here. | `docs/design/2026-09-21__release-v9.6/number-format-convention/decision_record.md` (new) | `design_system.md` v1.21 (§Consistency Rules → Number and Currency Formatting) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-07 | Audit closed-trade P&L net of fees_paid; flag NULL fees_paid in Monthly P&L | Design Required | New data displayed on Monthly P&L (aggregate notice, per-month count, mandatory basis caption). | `docs/design/2026-09-21__release-v9.6/monthly-pnl-fees-not-recorded/decision_record.md` (new) | `reports.md` v0.17 → v0.18 (§Fees-Not-Recorded Visibility) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-08 | Month-end immutable snapshot of Monthly P&L, with a restatement diff | Design Required | New marker, expandable diff row and Tax Year notice. Snapshot store scoped per month per the source item; tax-year table gets an API-supplied notice, not a second snapshot (addendum). | `docs/design/2026-09-21__release-v9.6/monthly-pnl-restatement-diff/decision_record.md` (new) | `reports.md` v0.18 (§Monthly Restatement Marker, Summary Bar notice) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-09 | calculate_trailing_stop entry-price floor divergence | Design Not Applicable | Backend stop-logic decision and golden-output test, no UI. (Live-trading-behaviour sign-off requirement is a Strategy Rules matter carried in the slice notes, not a design one.) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | list_backtest_rule_runs negative-limit validation | Design Not Applicable | Backend API param validation (400 vs 500), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | JsonLinesFormatter 500-char message truncation | Design Not Applicable | Backend log formatting, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Float-vs-Decimal money-arithmetic audit | Design Not Applicable | Backend audit and golden tests, no UI. Not the same as ST-06: this concerns computation, not display. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Shared upstream-call helper: timeout and bounded retry | Design Not Applicable | Backend/platform, no UI. §13 pre-check: wraps *existing* yfinance/Alpaca/Anthropic calls with a timeout and retry budget; introduces no new AI call, prompt or output surface, so the pre-check does not apply. Execution note: a retry budget on Anthropic calls re-issues paid inference — it must stay within the existing AI cost gating. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Dead-man's-switch alert for nightly-stop-update | Design Not Applicable | Ops alerting to the existing Telegram channel, no in-app UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | GitHub Actions secrets ownership map | Design Not Applicable | Ops documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Confirm synthetic uptime monitor live-fire and notification delivery | Design Not Applicable | Ops verification, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | CI minutes/artifact-storage visibility; explicit retention | Design Not Applicable | CI/CD configuration, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Quarterly full-suite Playwright re-run on a fresh staging seed | Design Not Applicable | QA process and cadence document plus a test run; adds no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | DoQ checklist addendum for flaky-test disposition | Design Not Applicable | QA governance document, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Standing regression check for the OpenAPI Drift Detection gate | Design Not Applicable | CI test fixtures, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | test_trade_plan_audit_log.py unrestored sys.modules swap | Design Not Applicable | Backend test-isolation fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | DS-17 unique index migration on live positions table | Design Not Applicable | Database migration and spec confirmation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | PO-05 (Lightweight Replay Mode) §13 determinism pre-clearance review | Design Not Applicable | Decision-record filing, no UI. §13 pre-check: this item **is** the §13 review for PO-05/`BLG-FEAT-74`; it introduces no AI call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | Canonical colour-blind-safe chart palette spec | Design Pre-Approved | Spec debt, documentation only — the source scope states "not a visual re-skin"; no rendered UI changes. The palette itself is the story's deliverable; Head of UX & Design approves it at QA sign-off. Any later adoption in chart components is a UI change needing its own gate pass. | N/A | `design_system.md` v1.21 (locked reference at this gate; the story adds its own version bump) | ✅ Cleared | Head of UX & Design |
| ST-25 | Lightweight ADR log for cross-cutting backend decisions | Design Not Applicable | Documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | Canonicalise the Sharpe-ratio lookback window | Design Not Applicable | Metrics-spec documentation, no UI; the follow-on code fix is separate | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Release-planning gate scan treats lapsed date gates as permanently gated | Design Not Applicable | Governance script and prompt change, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 | Re-confirm §13 boundary review cadence | Design Not Applicable | Governance decision, no UI. §13 pre-check: a cadence decision about the review process; introduces no AI call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 | Revisit sprint capacity band | Design Not Applicable | Governance/capacity document, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 | Fixed-cadence audit of every governance prompt's §14 entry | Design Not Applicable | Governance prompt change, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 | Claude model deprecation monitoring procedure | Design Not Applicable | Governance procedure document, no UI. §13 pre-check: procedure only, makes no model call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 | Sprint Velocity Trend Chart | Design Not Applicable | A generated governance artefact from `velocity_metrics.md`, per the slice's own note — not product UI. If it were instead built as an app page it would need its own gate pass. | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items

None.

## Notes

- **Post-gate-correction addendum:** `claude/cycles/2026-09-21__release-v9.6/stage4_backlog_slice_addendum.md` — 7 corrections (ST-01, ST-02, ST-03, ST-04, ST-05, ST-06, ST-08). Sprint Planning and Sprint Execution must read it together with the sealed slice. None changes scope, priority or effort. The most consequential: the slice names a `planned` trade-plan status in ST-01/ST-02 that does not exist anywhere in the code, data model or spec (`draft` is the entry state); and ST-08's slice title mentions a tax-year snapshot the source item never scoped.
- **§13 pre-check scope:** every item was checked (STEP 1). No item introduces or extends a call to an AI/LLM provider. AI-adjacent items — ST-13 (wraps existing Anthropic calls), ST-23 (is a §13 review), ST-28 (cadence decision), ST-31 (deprecation procedure) — are annotated individually above; ST-04 is deterministic by design. No `§13 PRE-CHECK REQUIRED` flags.
- **AI endpoint security checklist (`ai_endpoint_security_checklist.md`):** not triggered — no new AI-calling endpoint in this cycle.
- **Design artefacts produced this run (8):** under `docs/design/2026-09-21__release-v9.6/` — `trade-plan-clone`, `trade-plan-stale-marker`, `screener-watchlist-csv-export`, `reflection-reminder`, `empty-state-next-action`, `number-format-convention`, `monthly-pnl-fees-not-recorded`, `monthly-pnl-restatement-diff`.
- **Frontend specs updated (6 files):** `trade_plan.md` 1.14→1.15, `screener_results.md` 1.6→1.7, `watchlist.md` 0.7→0.8, `notifications.md` 0.8→0.9, `reports.md` 0.17→0.18, `design_system.md` 1.20→1.21. Logged in `prompt_change_log.md`.
- **Pre-existing changelog gaps (disclosed, not repaired):** the `## Changelog` tables of `trade_plan.md` (missing 1.13, 1.14), `watchlist.md` (missing 0.7) and `notifications.md` (missing 0.8) had no rows for the v9.5 ST-29/ST-30 bumps — only the header `Last Updated` was updated then. New rows were added for this gate's versions and each says so; the older rows were not fabricated.
- **Obligations passed to Sprint Execution (outside this gate's write scope):** ST-04 and ST-07/ST-08 change API responses/contracts — `docs/specs/api_contracts/`, `docs/reference/openapi.yaml` and, for any new route, `backend/routers/test.py` (with the `SystemStatus.js` fallback count and `SC-SS-01b`) in the same commit per CLAUDE.md §2. ST-08 needs a new table/migration and `data_model.md` entry (RISK-02). ST-06 will change visible strings, so existing Playwright assertions must be updated in the same commit. All 8 Design Required items carry an observable UI AC and need Playwright coverage or a dated staging run (CLAUDE.md §2).
- **Sequencing reminders (from the slice, still binding):** ST-01 → ST-02 → ST-06 all touch `TradePlans.js`; ST-06 also depends on the convention now in `design_system.md` v1.21.
- **Preflight observation:** the cycle-level `state.json` carries no `sprint_sealed` key (the root pointer has `sprint_sealed: false`). Treated as unsealed — no seal, amendment or `sprint_backlog.md` exists for this cycle.
- **Role sign-offs:** Head of UX & Design and Product Owner confirmations are agent-mediated (Sprint Execution Engine acting under those roles), consistent with the `2026-09-14__release-v9.4` and `2026-09-15__release-v9.5` gates. Three of the decisions are genuine product calls the Product Owner may wish to review before `plan sprint`: the `planned` → status mapping and `updated_at` age basis (ST-01/ST-02), the email-only/default-Off preference reading (ST-04), and the `−` minus-sign choice (ST-06).
