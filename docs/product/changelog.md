# Product Changelog — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-03 (post-ship closure 2026-08-21__release-v9.0 — v9.0 entry added); prior — 2026-08-21 (post-ship closure 2026-08-17__release-v8.9 — v8.9 entry added); prior — 2026-08-17 (post-ship closure 2026-08-14__release-v8.8 — v8.8 entry added); prior history retained — see prior entries in version control

> This document is a human-maintained record of what was shipped in each product version and when. It records delivery milestones and notable decisions. It is not an immutable system record — for point-in-time system status reports, see `docs/operations/status_reports/`.

> **Authoring convention — `User Impact` column (added v8.8, ST-13, BLG-FE-161):** each `### Changes shipped` table row carries a `User Impact` cell in addition to `Description`. Write `User Impact` only for EPICs that changed something a user can see, click, or notice the effect of — one to two sentences, present tense (or implied second person), no ticket IDs, no implementation nouns (endpoint/table/component names). Leave it `—` for backend/infra/governance/test-coverage rows with no user-facing effect. `Description` is retained unchanged as the engineering record — it is not replaced. `GET /changelog/latest` sources the in-app "What's New" panel from `User Impact` only; rows with a blank/`—` cell are excluded from that feed entirely (`docs/specs/api_contracts/changelog_endpoints.md`).

---

## v9.0 — AI Debrief/Backtest Follow-Through, Risk-Data Integrity & Operational Resilience — 2026-09-03
Cycle: 2026-08-21__release-v9.0
Verified: Verified
Verification report: claude/cycles/2026-08-21__release-v9.0/verification_report.md

### Changes shipped
| EPIC | Description | User Impact | Spec sections updated |
|------|-------------|-------------|----------------------|
| EPIC-01 | AI Post-Trade Debrief & Backtest Correctness Follow-Through — fixed a nightly backtest rebalance-date computation bug that included the current in-progress month in rebalance-date lists, skewing recent backtest performance figures; configured root/app logging so `logger.info()` calls actually reach Render's captured production logs; decided the data source for the AI Post-Trade Debrief's "linked journal entries" and fixed the debrief-generation prompt's unverifiable cross-trade pattern language flagged by §13 compliance review; consolidated `backtest_rule_service.py`'s ported algorithm functions with `production_strategy.py` into a single canonical `strategy_engine.py`, with byte-identical parity tests against both pre-consolidation implementations. | Nightly backtest results (visible on the Strategy Benchmark page) no longer include the current in-progress month in rebalance-date calculations, so recent performance figures are more accurate. AI-generated post-trade debriefs no longer make cross-trade pattern claims they can't actually verify from your own trade history. | `docs/ops/api_performance_baseline.md#36.7`; `docs/specs/api_contracts/trade_endpoints.md`; `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md#Condition 1`; `backend/services/strategy_engine.py` |
| EPIC-02 | Live Risk-Management & Trade-Plan Data-Integrity Closure — audited all open positions against the breakeven-floor stop invariant (0 violations found; nightly `analyze_positions()` recompute confirmed to have kept every position correctly floored since the underlying v6.x fix); decided and applied treatment for the `trade_plans.setup_type='Other'` conflation; added a lock around `ensure_trade_plans_table()`'s memoization flag to close a startup race condition; added down-migration rollback verification tests for the 5 most recent schema migrations; closed the What-If Sizing Preview FX-rate reproducibility gap for US-market trade plans; added Playwright coverage for UK-market position `current_trailing_stop_native` display. | The What-If Sizing Preview on the trade-plan form now gives you the same risk numbers every time for a US-market plan, instead of a value that could shift between page loads. A full audit confirmed every open position's stop-loss is correctly locked in once a trade turns profitable — no live positions needed correction. | `backend/services/position_service.py`; `docs/product/decisions/setup-type-other-conflation-decision--2026-08-21.md`; `docs/specs/api_contracts/trade_plan_endpoints.md`; `docs/specs/frontend/pages/trade_plan.md#5d.2`/`#5d.3`; `docs/ops/database_migration_governance.md` |
| EPIC-03 | Operational Resilience & Deploy-Path Safeguards — production database backup/restore drill executed (confirmed pre-met on `main`); automated staging smoke test wired into deploy/merge CI; staging environment drift detector added to catch build/deploy path filter divergence; confirmed production `PUBLIC_URL` is actually set in the Render dashboard; added a CI safeguard against future `PUBLIC_URL`/asset-path regressions on the GitHub Pages deploy. | — | `docs/ops/database_backup_disaster_recovery_runbook.md`; `.github/workflows/production-db-backup.yml`; `scripts/staging_smoke_test.py`; `scripts/wait_for_staging_deploy_live.py`; `.github/workflows/staging-deploy.yml`; `docs/ops/render_build_deploy_path_filter_audit.md`; `scripts/check_deploy_path_filter_drift.py`; `docs/ops/test_environment_parity_check_2026-08-16.md`; `.github/workflows/deploy.yml` |
| EPIC-04 | QA Coverage & Process Hardening — defined the Arc 5 QA protocol; added visual regression baseline snapshots for contrast-sensitive and chart-heavy components; added the R-multiple calculation regression test against the canonical server-side formula; audited Playwright coverage gaps for `Arc5ComplianceSection` (3 gaps found, filed as backlog items); added a standalone axe-core accessibility CI scan (5 accessibility gaps found, filed as backlog items); published backend test coverage reports to PR comments. | — | `docs/qa/arc5_qa_protocol.md`; `docs/specs/metrics_definitions.md#R-Multiple (Canonical Server-Side)`; `docs/qa/arc5_coverage_audit.md`; `tests/e2e/accessibility-axe-scan.spec.js`; `scripts/generate_backend_coverage_report.py`; `.github/workflows/backend-coverage-report.yml` |
| EPIC-05 | Backend Architecture & Cost/Capacity Hygiene — backend service-layer boundary review (raw SQL still present in `analytics.py`/`digest.py`, deferred fix filed); database connection pool tuning review; Render hosting tier review; Render hosting cost trend dashboard produced; quarterly dependency minor-version upgrade cadence policy defined (a reproducible npm production-build regression found during the review, filed as tech debt). | — | `docs/ops/backend_service_layer_boundary_review_2026-08-21.md`; `docs/ops/database_connection_pool_tuning_review_2026-08-21.md`; `docs/ops/render_starter_tier_headroom_reassessment_2026-08-13.md`; `docs/ops/render_hosting_tier_review_2026-08-21.md`; `docs/ops/render_hosting_cost_trend_dashboard_2026-08-21.md`; `docs/ops/quarterly_dependency_upgrade_cadence_policy.md` |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] [U] Fix nightly backtest rebalance-date computation to exclude the current in-progress month
- [ST-02] [D] Configure root/app logging so `logger.info()` calls actually reach Render's captured logs
- [ST-03] [D] Decide "linked journal entries" data source for the AI Post-Trade Debrief
- [ST-04] [D] Fix debrief-generation prompt's unverifiable cross-trade pattern language
- [ST-05] [D] Consolidate `backtest_rule_service.py`'s ported algorithm functions with `production_strategy.py`
- [ST-06] [D] Audit and backfill open positions against the breakeven-floor stop invariant
- [ST-07] [D] Decide and apply treatment for `trade_plans.setup_type='Other'` conflation
- [ST-08] [D] Add a lock around `ensure_trade_plans_table()`'s memoization flag
- [ST-09] [D] Add down-migration rollback verification tests for the 5 most recent schema migrations
- [ST-10] [U] Close the What-If Sizing Preview FX-rate reproducibility gap for US-market plans
- [ST-11] [D] Add Playwright coverage for UK-market position on `current_trailing_stop_native`
- [ST-12] [D] Production database backup/restore drill
- [ST-13] [D] Automated staging smoke test on deploy/merge
- [ST-14] [D] Staging environment drift detector
- [ST-15] [D] Confirm production `PUBLIC_URL` is actually set in the Render dashboard
- [ST-16] [D] Add CI safeguard to catch future `PUBLIC_URL`/asset-path regressions on GitHub Pages deploy
- [ST-17] [D] Arc 5 QA protocol
- [ST-18] [D] Visual regression baseline snapshots (contrast-sensitive + chart-heavy components)
- [ST-19] [D] R-multiple calculation regression test
- [ST-20] [D] Playwright coverage gap audit for `Arc5ComplianceSection`
- [ST-21] [D] Standalone axe-core accessibility CI scan
- [ST-22] [D] Publish backend test coverage report to PR comments
- [ST-23] [D] Backend service-layer boundary review
- [ST-24] [D] Database connection pool tuning review
- [ST-25] [D] Render hosting tier review
- [ST-26] [D] Render hosting cost trend dashboard
- [ST-27] [D] Quarterly dependency minor-version upgrade cadence policy

Sign-off: Product Owner — 2026-09-03
QA sign-off: Director of Quality — 2026-09-03

---

## v8.9 — Live Risk-Management Correctness & Trade Intelligence Expansion — 2026-08-21
Cycle: 2026-08-17__release-v8.9
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-08-17__release-v8.9/verification_report.md

### Changes shipped
| EPIC | Description | User Impact | Spec sections updated |
|------|-------------|-------------|----------------------|
| EPIC-01 | Live risk-management correctness — confirmed and regression-tested that the breakeven-floor trailing-stop calculation already governs both live production stop-writing paths (the divergent, unfloored `position_manager.py` inline calc confirmed off the live path); fixed a currency-basis mismatch where `current_trailing_stop`/`stop_price` rendered GBP-converted values with the native currency symbol for US-market positions; added a `trailing_stop_action_rate` validation-tolerances spec entry | Your trailing stop on a profitable position now reliably locks in gains instead of risking a freeze at a stale, wide entry-time value. For US-market positions, the stop price shown next to your position now matches the currency you're actually trading in, instead of silently mixing a GBP-converted number with a dollar sign. | `backend/utils/calculations.py#calculate_trailing_stop`; `docs/specs/api_contracts/position_endpoints.md#Field notes`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`; `docs/specs/metrics_definitions.md#Trailing Stop Action Rate` |
| EPIC-02 | Trade sizing & post-trade intelligence — §13 system boundary review and nine binding conditions cleared for AI-generated content; sector/correlation-aware position sizing that reduces or flags new position sizes against existing open-position concentration; pre-commit "what-if" sizing/risk simulator on the trade-plan form; automated AI post-trade debrief generated on demand for closed trades; in-app backtesting engine for candidate strategy rule changes | New trade-plan sizing now accounts for how concentrated your open positions already are in the same sector, and tells you when a size was reduced or flagged for that reason. The trade-plan form shows a live preview of position size, risk, and portfolio heat impact before you save. Closed trades can now get an AI-generated debrief on demand, and you can backtest a candidate strategy-rule change against historical data right from the Strategy Benchmark page. | `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`; `docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md`; `backend/services/concentration_service.py`; `docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md`; `docs/specs/frontend/pages/trade_plan.md#5d`; `docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md`; `docs/specs/frontend/pages/strategy_benchmark.md#7.6`; `docs/specs/data_model.md#DS-16`; `docs/specs/api_contracts/trade_endpoints.md#GET /trades/{trade_id}/debrief`; `docs/specs/frontend/pages/trade_history.md#Post-Trade Debrief` |
| EPIC-03 | Backend reliability & performance — root-caused and fixed `GET /trade-plans/tags` ~10s p50 latency (per-request DDL call site, fixed via process-global memoization); verified the SI-05 digest-timing log line via a real post-merge invocation (surfaced a pre-existing production logging-configuration gap, tracked separately, adopted an interim GitHub Actions timing-proxy in the meantime); wrapped audit-trail writes in the same transaction as their primary state update; confirmed and removed dead code in `trade_csv_service.py` | — | `docs/ops/db_index_audit_arc4_2026-08-06.md`; `docs/specs/data_model.md#DS-13`; `docs/specs/api_contracts/trade_endpoints.md`; `docs/ops/api_performance_baseline.md#36.5` |
| EPIC-04 | Test coverage & QA hardening — test coverage for `screener_refresh`/`risk_off_alerts` job-registration wiring; decided and applied a server-side default for `trade_plans.setup_type`; direct unit tests for `cash_service`, `compliance_service`, `news_service`, `validation_service`; Playwright coverage for `WhatsNewCard`'s changelog `User Impact` rendering | — | `backend/routers/screener.py`; `backend/main.py#risk_off_alerts_endpoint`; `docs/specs/api_contracts/trade_plan_endpoints.md#Request Body Fields`; `docs/ops/backend_service_layer_test_coverage_report_2026-08-16.md`; `tests/e2e/whats-new-panel.spec.js`; `docs/specs/frontend/pages/dashboard.md#§6A` |
| EPIC-05 | Operations & spec currency — local dev venv version-pin enforcement documentation and production `PUBLIC_URL` parity confirmation; archived `window_summary_IW-*.md` files older than 90 days; documented `screener_refresh` and `risk_off_alerts` jobs in `health_endpoints.md` | — | `docs/ops/test_environment_parity_check_2026-08-16.md#§2.1`; `claude/backlog/backlog.md#BLG-OPS-113`; `docs/specs/api_contracts/health_endpoints.md#GET /health/scheduler` |
| EPIC-06 | Governance process debt closure — fixed `post_ship_closure.md` to actually write `last_post_ship_cycle`/`last_post_ship_utc`; root-caused and corrected `execution_state.json` timestamp drift from actual git commit dates; wired the Displacement Debt Register into `roadmap_prompt.md` STEP 8 (file-creation half still outstanding, carried forward via `ESC-EXEC-20260818-02`); defined a pruning rule for stale `RA:` roadmap-annotation markers older than 3 releases | — | `claude/system/post_ship_closure.md#STEP 10`; `claude/schemas/state_field_owners.json`; `claude/system/execution_prompt.md#3.1`; `claude/system/roadmap_prompt.md#STEP 8`; `claude/system/roadmap_management_prompt.md#STEP 5.2` |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-EPIC01-ST02-01 | P0 (as filed) | Trail Stop tile rendered GBP-converted `current_trailing_stop`/`stop_price` with the native currency symbol for US-market positions (pre-existing since v6.2) | Recorded — Resolved same-story |
| DEV-v8.9-ST05-02 | P2 (as filed) | §5d.3 "R at Risk" shipped with no FX conversion for any market, contradicting its own wording | Recorded — Resolved same-story |
| DEV-v8.9-ST05-01 | P3 | §5d.1 presence-gate wording self-contradictory as literally written | Recorded — Resolved same-story |
| DEV-EPIC03-ST09-01 | P3 | Render production log's SI-05 digest-timing line genuinely absent — root cause: no root logging configuration on the production uvicorn process (pre-existing platform gap, not a regression from this cycle) | Open — Accepted per P3 policy; `BLG-BE-107` filed |

### Tech backlog items shipped
- [ST-01] [U] Fix nightly trailing-stop ratchet to apply breakeven floor for profitable positions
- [ST-02] [U] Fix currency basis of `current_trailing_stop`/`stop_price` for US-market positions
- [ST-03] [D] Add `trailing_stop_action_rate` spec entry with validation tolerances
- [ST-04] [U] Correlation/sector-concentration-aware position sizing
- [ST-05] [U] Pre-commit "what-if" sizing/risk simulator on the trade-plan form
- [ST-06] [U] Automated AI post-trade debrief
- [ST-07] [U] In-app backtesting engine for strategy rule changes
- [ST-08] [D] Investigate `GET /trade-plans/tags` ~10s p50 latency
- [ST-09] [D] Verify ST-11 duration logging against a real post-merge invocation
- [ST-10] [D] Wrap audit-trail writes in the same transaction as the primary state update
- [ST-11] [D] Confirm `trade_csv_service.py::build_trade_history_csv` is dead code and remove
- [ST-12] [D] Add test coverage for `screener_refresh`/`risk_off_alerts` job-registration wiring
- [ST-13] [D] Decide and apply treatment for `trade_plans.setup_type` with no default/required guarantee
- [ST-14] [D] Add direct unit tests for `cash_service`, `compliance_service`, `news_service`, `validation_service`
- [ST-15] [D] Add Playwright coverage for `WhatsNewCard`'s changelog User Impact rendering
- [ST-16] [D] Local dev venv version-pin enforcement; confirm `PUBLIC_URL` parity on production
- [ST-17] [D] Archive `window_summary_IW-*.md` files older than 90 days
- [ST-18] [D] Document `screener_refresh` and `risk_off_alerts` jobs in `health_endpoints.md`
- [ST-19] [G] Fix `post_ship_closure.md` to actually write `last_post_ship_cycle`/`last_post_ship_utc`
- [ST-20] [G] Root-cause and correct `execution_state.json` timestamp drift from actual git commit dates
- [ST-21] [G] Physically place the Displacement Debt Register and wire it into `roadmap_prompt.md` STEP 8
- [ST-22] [G] Define a pruning rule for stale `RA:` roadmap-annotation markers older than 3 releases
- [ST-23] [G] §13 System Boundary Review: Automated AI Post-Trade Debrief (Sprint-Planning-added gate story)

Sign-off: Product Owner — 2026-08-21
QA sign-off: Director of Quality — 2026-08-21

---

## v8.8 — Live Data-Integrity, Backend Hardening & Debt Closure — 2026-08-17
Cycle: 2026-08-14__release-v8.8
Verified: Verified
Verification report: claude/cycles/2026-08-14__release-v8.8/verification_report.md

### Changes shipped
| EPIC | Description | User Impact | Spec sections updated |
|------|-------------|-------------|----------------------|
| EPIC-01 | Live data-integrity & scheduled job coverage — nightly overnight screener-refresh workflow; nightly risk-off-alerts workflow (closes permanently-stuck RISK OFF badge); nightly backtest import failure investigated and fixed; 3 remaining endpoints added to `api_performance_baseline.md` | Screener results and the RISK OFF regime badge on Positions now refresh automatically overnight instead of going stale — what you see reflects current market conditions, not a stale snapshot from days earlier. The Strategy Benchmark page's "data as of" freshness line also populates correctly again. | `.github/workflows/screener-refresh.yml`; `.github/workflows/risk-off-alerts.yml`; `docs/specs/api_contracts/health_endpoints.md#GET /health/scheduler`; `docs/ops/api_performance_baseline.md#39.1`, `#39.2`, `#39.3` |
| EPIC-02 | Backend hardening & data model gaps — consolidated two divergent `check_market_regime()` implementations; position lifecycle state-transition history table; `price_alerts`-to-trade provenance linkage; `si05_digest_log.telegram_message_id` now populated on send; duration logging around the SI-05 Telegram send call; Pre-Trade Research View query-latency budget review | — | `backend/utils/pricing.py`; `docs/specs/data_model.md#DS-13`, `#DS-14`, `#DS-15`; `docs/specs/api_contracts/trade_plan_endpoints.md#POST /trade-plans`; `docs/specs/api_contracts/alerts_endpoints.md#GET /notifications`; `docs/ops/api_performance_baseline.md#36` |
| EPIC-03 | Frontend UX & dead-code cleanup — "What's New" panel now writes user-facing benefit copy instead of raw engineering notes; Research page trade plan status badge readable labels for 3 of 6 statuses; Ticker Universe page search/sector/industry filtering; `PositionEntryModal.js` dead-code status resolved; Playwright coverage added for remaining Card/secondary-variant component call sites | The in-app "What's New" panel now describes releases in plain, benefit-focused language. Trade plan status badges on the Research page show readable labels instead of raw snake_case text. The Ticker Universe page can now be filtered by search term, sector, and industry. | `docs/specs/frontend/pages/dashboard.md#6A`; `docs/specs/api_contracts/changelog_endpoints.md#GET /changelog/latest`; `docs/specs/frontend/pages/research_view.md#4.7`; `docs/specs/frontend/pages/ticker_universe.md#10`; `docs/specs/frontend/design_system.md#Modal / Dialog Theming` |
| EPIC-04 | Quality & test-coverage debt — Arc 6 prerequisite field-population completeness audit; consolidated backend service-layer test-coverage report; test-environment parity check (local/CI/staging config drift); `backend/routers/test.py` completeness re-audit | — | `docs/ops/arc6_prerequisite_field_population_audit_2026-08-16.md`; `docs/ops/backend_service_layer_test_coverage_report_2026-08-16.md`; `docs/ops/test_environment_parity_check_2026-08-16.md`; `docs/ops/endpoint_test_coverage_audit_2026-08-16.md` |
| EPIC-05 | Security hardening — system/user role separation added to Claude thesis-generation prompts; dependency license compliance scan; baseline npm audit HIGH/CRITICAL findings review (react-scripts toolchain); Telegram Bot Token added to `api_key_rotation_policy.md` scope | — | `tests/test_gemini_prompt_injection_resistance.py`; `docs/security/dependency_license_compliance_scan_2026-08-16.md`; `docs/security/npm_audit_baseline_review_2026-08-16.md`; `docs/ops/api_key_rotation_policy.md` |
| EPIC-06 | API & spec debt closure — backfilled `api_changelog.md` entries for v7.9–v8.4 endpoint additions; corrected `trade_plan.md` §5.1's stale "Risk/Reward Notes" field anchor | — | `docs/product/api_changelog.md#v8.2.0`, `#v7.9.0`; `docs/specs/frontend/pages/trade_plan.md#Changelog` |
| EPIC-07 | Governance correctness fixes — corrected `CLAUDE.md` §8's commit message template to match the enforced commit-format hook; assigned `.claude_current_state.json`'s `prior_cycle` field a sole owning engine (Post-Ship Closure STEP 10) | — | N/A — governance prompt files, not canonical specs |

### Deviations accepted
None — no deviations filed this sprint (0 P0–P3 spec deviations; see `verification_report.md §4`).

### Tech backlog items shipped
- [ST-01] [U] Scheduled overnight screener refresh workflow
- [ST-02] [U] Scheduled nightly risk-off-alerts workflow (fixes permanently-stuck RISK OFF badge)
- [ST-03] [U] Investigate nightly backtest import failure (Strategy Benchmark "data as of" line)
- [ST-04] [D] Add `GET /v1beta1/news` to `api_performance_baseline.md`
- [ST-05] [D] Add `GET /trade-plans/tags` to `api_performance_baseline.md`
- [ST-06] [D] Live timing measurement for `GET /analytics/strategy-version-comparison`
- [ST-07] [D] Consolidate two divergent `check_market_regime()` implementations
- [ST-08] [D] Position lifecycle state-transition history table
- [ST-09] [D] Link `price_alerts` to the trade they trigger
- [ST-10] [D] Populate `si05_digest_log.telegram_message_id` on successful send
- [ST-11] [D] Duration logging around `POST /digest/si05/send`'s Telegram send call
- [ST-12] [D] Pre-Trade Research View query-latency budget review
- [ST-13] [U] "What's New" panel surfaces user-facing benefit statements, not raw engineering copy
- [ST-14] [U] Research page trade plan status badge: fix raw snake_case for 3 of 6 statuses
- [ST-15] [U] Ticker Universe page filtering by search, sector, and industry
- [ST-16] [D] Resolve `PositionEntryModal.js` dead-code/unreachable-mount-point status
- [ST-17] [D] Playwright coverage for Card/secondary-variant components with a live call site
- [ST-18] [D] Field-population completeness audit for Arc 6 prerequisite fields
- [ST-19] [D] Consolidated backend service-layer test-coverage report
- [ST-20] [D] Test-environment parity check — local vs CI vs staging config drift
- [ST-21] [D] `backend/routers/test.py` completeness re-audit
- [ST-22] [D] System/user role separation for Claude thesis-generation prompts
- [ST-23] [D] Dependency license compliance scan
- [ST-24] [D] Review baseline npm audit HIGH/CRITICAL findings (react-scripts toolchain)
- [ST-25] [D] Add Telegram Bot Token to `api_key_rotation_policy.md` scope
- [ST-26] [D] Backfill `api_changelog.md` entries for v7.9–v8.4 endpoint additions
- [ST-27] [D] Correct `trade_plan.md` §5.1's stale "Risk/Reward Notes" field anchor
- [ST-28] [G] Correct `CLAUDE.md` §8's commit message template to match the enforced commit-format hook
- [ST-29] [G] Assign an owning engine for `.claude_current_state.json`'s `prior_cycle` field

Sign-off: Product Owner — 2026-08-17
QA sign-off: Director of Quality — 2026-08-17

---

## v8.7 — User Features, Data-Integrity Closure & Cross-Domain Hardening — 2026-08-13
Cycle: 2026-08-12__release-v8.7
Verified: Verified
Verification report: claude/cycles/2026-08-12__release-v8.7/verification_report.md

### Changes shipped
| EPIC | Description | User Impact | Spec sections updated |
|------|-------------|-------------|----------------------|
| EPIC-01 | User-facing features & theme-consistency completion — thesis pre-mortem/invalidation-condition capture at trade-plan entry; trade-plan-link outcome consumption at position entry; `isAiDraft` flag persisted for AI-origin display badges; SI-02 Gate Status and Unrealised P&L cards (Reports.js) light/dark theme fixed; 4 hardcoded dark-only modals converted to theme-aware tokens | Trade plans now let you record what would invalidate your thesis right when you write it — not just when you're reviewing later. Opening a new position also confirms straight away whether it's linked to an existing trade plan. | `docs/specs/frontend/pages/trade_plan.md#5.1`, `#10.5`, `#10.6`; `docs/specs/api_contracts/trade_plan_endpoints.md`; `docs/specs/data_model.md`; `docs/specs/frontend/design_system.md#Card Hierarchy`, `#Modal / Dialog Theming` |
| EPIC-02 | Trade-plan data-integrity closure — staging verification of v8.6's (`BLG-BE-91`/ST-03) trade-plan-linkage enforcement and legacy orphaned-row audit against the new `CHECK` constraint | — | `docs/specs/data_model.md#DS-12` |
| EPIC-03 | Frontend correctness & test-coverage carryover — Playwright coverage for remaining shadcn token call-site families; end-to-end integration assertion for tax-year boundary trade rows | — | `tests/e2e/shadcn-token-remaining-families.spec.js`; `tests/test_tax_year_boundary_completeness.py` |
| EPIC-04 | Backend reliability hardening — `BLG-BE-57` retry/backoff audit pattern extended to Gemini API call sites; N+1 query audit across trade/position list endpoints; SI-04 strategy-version-comparison schema requirements pre-design | — | `tests/test_gemini_claude_retry_backoff.py`; `tests/test_position_lifecycle_n_plus_1_fix.py`; `docs/design/2026-07-21__release-v7.7/si04-strategy-version-comparison/data_model_pre_design.md` |
| EPIC-05 | Security hardening — prompt-injection resistance test for the Gemini thesis-generation endpoint; rate-limit audit on unauthenticated/low-auth endpoints | — | `tests/test_gemini_prompt_injection_resistance.py`; `docs/security/rate_limit_audit_2026-08-13.md` |
| EPIC-06 | Operations & QA-tooling closure — Render Starter-tier headroom reassessment; Render dashboard-only build/deploy path filter canonical documentation; substring-match false-negative fix in `check_api_performance_baseline_drift.py` | — | `docs/ops/render_starter_tier_headroom_reassessment_2026-08-13.md`; `docs/ops/render_build_deploy_path_filter_audit.md`; `tests/test_api_performance_baseline_drift_check.py` |
| EPIC-07 | Governance & cross-domain hardening — CLAUDE.md §8 shared-JSON-field schema-drift check for sibling EPIC branches; Roadmap Unlock Tracker (consolidated view of all gated features/conditions); §13 policy determination on preview analytics vs deterministic/non-predictive boundary; canonical gated `DataState` variant and visual/interaction spec | — | `CLAUDE.md`; `docs/product/roadmap_unlock_tracker.md`; `docs/product/decisions/decisions--2026-08-12__release-v8.7--confidence-interval-preview-analytics-section13-policy.md`; `docs/specs/frontend/design_system.md` |

### Deviations accepted
None — no deviations filed this sprint (0 P0–P3 spec deviations; see `verification_report.md §4`).

### Tech backlog items shipped
- [ST-01] [U] Thesis pre-mortem / invalidation-condition capture at trade-plan entry
- [ST-02] [U] Consume `trade_plan_linked`/`trade_plan_id` in the position-entry flow
- [ST-03] [U] Persist `isAiDraft` flag on `trade_plans` for AI-origin display badges
- [ST-04] [U] SI-02 Gate Status section (Reports.js) light/dark theme fix
- [ST-05] [U] Unrealised P&L card (Reports.js) light/dark theme fix
- [ST-06] [U] Convert 4 hardcoded dark-only modals to theme-aware tokens
- [ST-07] [D] Staging verification of v8.6's trade-plan-linkage enforcement + legacy orphaned-row audit
- [ST-08] [D] Playwright coverage for the remaining shadcn token call-site families
- [ST-09] [D] End-to-end integration assertion for tax-year boundary trade rows
- [ST-10] [D] Extend the `BLG-BE-57` retry/backoff audit pattern to Gemini API call sites
- [ST-11] [D] N+1 query audit across trade/position list endpoints
- [ST-12] [P] SI-04 strategy-version-comparison schema requirements pre-design
- [ST-13] [D] Prompt-injection resistance test for the Gemini thesis-generation endpoint
- [ST-14] [D] Rate-limit audit on unauthenticated/low-auth endpoints
- [ST-15] [D] Render Starter-tier headroom reassessment
- [ST-16] [D] Render dashboard-only build/deploy path filter — canonical documentation
- [ST-17] [D] Fix substring-match false negatives in `check_api_performance_baseline_drift.py`
- [ST-18] [G] CLAUDE.md §8 rule for shared JSON schema drift mid-sprint between sibling EPIC branches
- [ST-19] [G] Roadmap Unlock Tracker — consolidated view of all gated features and their conditions
- [ST-20] [G] §13 policy question: preview analytics vs deterministic/non-predictive boundary
- [ST-21] [P] Canonical gated `DataState` variant and visual/interaction spec

Sign-off: Product Owner — 2026-08-13
QA sign-off: Director of Quality — 2026-08-13

---

## v8.6 — User Features, Data-Integrity Foundation & Correctness Carryover — 2026-08-12
Cycle: 2026-08-11__release-v8.6
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-08-11__release-v8.6/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | User-facing product features — trade-plan completion-rate tracking on Analytics; AI-assisted setup thesis digest (thesis + risk factors + trade-plan link) surfaced at order placement | `docs/specs/frontend/pages/analytics.md#21`; `docs/specs/frontend/pages/trade_plan.md#10.5` |
| EPIC-02 | Trade-plan data-integrity foundation — trade-plan-to-position linkage enforced at position entry; DB-level `CHECK` constraint (`trade_plans_active_requires_position_check`, `NOT VALID`, going-forward only) plus router-level 400 guards against orphaned `trade_plans` rows | `docs/specs/frontend/pages/trade_plan.md#10`; `docs/specs/data_model.md#DS-12`; `docs/specs/api_contracts/portfolio_endpoints.md`; `docs/specs/api_contracts/trade_plan_endpoints.md` |
| EPIC-03 | Frontend design consistency & correctness carryover — 9 remaining shadcn design tokens registered in `tailwind.config.js`; Playwright coverage for remaining `-muted`/`-muted-foreground` call sites (incl. a real false-negative correction on `SavedFiltersControl.js`); 6 secondary-text token drift instances fixed against the v6.7 canonical token; modal/dialog light-theme support design decision recorded; `Layout.js` dark-class sync switched to `useLayoutEffect`; nav group/page counts corrected against live `NAV_GROUPS` in both the exploration doc and `navigation.md`; `CohortAnalysis.js` backend-endpoint migration deviation record closed (fix had already shipped) | `tailwind.config.js`; `tests/e2e/analytics-mobile-responsive.spec.js`; `tests/e2e/watchlist.spec.js`; `tests/e2e/saved-filters-calendar-view.spec.js`; `docs/specs/frontend/design_system.md#Color Usage`; `docs/design/2026-08-11__release-v8.6/modal-light-theme-support/decision_record.md`; `docs/specs/frontend/design_system.md#Modal / Dialog Theming`; `src/Layout.js`; `docs/specs/frontend/pages/navigation.md#Group Structure`; `docs/specs/frontend/pages/analytics.md#15` |
| EPIC-04 | Financial-correctness & QA-coverage carryover — `get_regime_distribution`'s dead NULL-exclusion docstring corrected to describe the real risk-off-default behaviour; multi-currency cost-basis rounding audit found and fixed a real partial-exit proportional-allocation drift bug in `exit_position()` (caught by a second, independently-scoped review pass); closed-trade export completeness confirmed against tax-year boundary edge cases; `check_dependency_vuln_rescan.py` no longer silently treats a failed audit tool as zero findings | `tests/test_screener_batch_service.py`; `docs/specs/data_model.md`; `docs/product/decisions/multi-currency-cost-basis-rounding-audit--2026-08-12.md`; `tests/test_tax_year_boundary_completeness.py`; `.github/workflows/dependency-vuln-rescan.yml`; `scripts/check_dependency_vuln_rescan.py` |
| EPIC-05 | QA test-coverage debt closure — endpoint-level regression test for `GET /analytics/tag-performance`'s `ensure_trade_plans_table` call; Playwright coverage for `setNarrativeField` AI-draft-badge clearing on the 3 remaining narrative fields; unit tests for `check_dependency_vuln_rescan.py`; documented the one-directional limitation of `test_alerts_service.py`'s `sys.modules` restore fixture | `tests/test_tag_performance_ensure_table_call.py`; `tests/e2e/trade-plan.spec.js`; `tests/test_check_dependency_vuln_rescan.py`; `tests/test_alerts_service.py` |
| EPIC-06 | Operations & governance debt closure — `api-key-cross-environment-check.yml` alert-step grep aligned with the skip-guard's `::error::` prefix; CVE-2026-4539 ignore rationale cross-referenced in `dependency-vuln-rescan.yml`; post-merge run of `dependency-vuln-rescan.yml` confirmed successful via manual dispatch; retroactive deviation record filed for the dark-mode/Radix-portal `Layout.js` fix; `shared_standards_changelog.md` missing v3.27 entry backfilled; `execution_state.json`'s `deviations_filed` field semantics formally documented; two stale-annotation escalations (`BLG-FE-146`/`BLG-FE-139`, `BLG-GOV-288`) resolved as moot | `.github/workflows/api-key-cross-environment-check.yml`; `.github/workflows/dependency-vuln-rescan.yml`; `docs/specs/frontend/pages/navigation.md#Known Deviations`; `claude/system/changelogs/shared_standards_changelog.md`; `claude/system/schemas/execution_state_schema.json`; `claude/system/shared_standards.md#16.15`; `claude/system/templates/qa_evidence_template.md` |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-v8.6-ST02-01 | P3 | "AI draft" badge omitted from the Setup Thesis Digest panel — `isAiDraft` is ephemeral client-only form state, never persisted to `trade_plans` (`BLG-BE-95` filed for the persistence follow-up) | PO (agent-mediated) |
| DEV-NAV-ST06-01 | P1 | Dark theme not applying inside Radix-portaled dialogs app-wide — retroactive record; fix already shipped in the same v8.5 commit (`41619410`) that discovered it | Recorded — Resolved |
| DEV-EPIC02-ST03-01 | P2 | `CohortAnalysis.js` used client-side cohort computation instead of `GET /analytics/cohort` — fix had already shipped 2026-03-16 (`af22ea6e`); this cycle closed the stale tracking record only | Recorded — Resolved |

### Tech backlog items shipped
- [ST-01] [U] Trade plan completion rate tracking (Analytics)
- [ST-02] [U] AI-assisted setup thesis digest at order placement
- [ST-03] [D] Enforce trade-plan linkage at position entry + DB-level safeguard against orphaned `trade_plans` rows
- [ST-04] [U] Register remaining unregistered shadcn design tokens in `tailwind.config.js`
- [ST-05] [D] Playwright coverage for the remaining `-muted`/`-muted-foreground` call sites left untested by v8.5/ST-06
- [ST-06] [U] Fix 6 drift instances against the v6.7 canonical secondary-text token
- [ST-07] [P] Design decision: should modals/dialogs support light theme? (decision only; implementation follow-up filed as `BLG-FE-156`)
- [ST-08] [D] Switch `Layout.js`'s dark-class `document.documentElement` sync to `useLayoutEffect`
- [ST-09] [D] Correct `st15_nav_bar_redesign_exploration.md`'s nav group/page counts against live `NAV_GROUPS`
- [ST-10] [D] Migrate `CohortAnalysis.js` from client-side computation to `GET /analytics/cohort` — closed stale deviation record
- [ST-11] [D] `get_regime_distribution`'s NULL-exclusion documented behaviour is dead code
- [ST-12] [D] Multi-currency cost-basis rounding consistency check — real rounding-drift bug found and fixed
- [ST-13] [D] Closed-trade export completeness check against tax-year boundary edge cases
- [ST-14] [D] `check_dependency_vuln_rescan.py` silently treats a failed audit tool as "zero findings" — fixed
- [ST-15] [D] Endpoint-level regression test for `GET /analytics/tag-performance`'s `ensure_trade_plans_table` call
- [ST-16] [D] Playwright coverage for `setNarrativeField` AI-draft-badge clearing on the 3 non-`setup_thesis` fields
- [ST-17] [D] Unit tests for `scripts/check_dependency_vuln_rescan.py`
- [ST-18] [D] Document one-directional limitation of `test_alerts_service.py`'s `sys.modules` restore fixture
- [ST-19] [D] Align `api-key-cross-environment-check.yml`'s alert-step grep with the skip-guard's `::error::` prefix
- [ST-20] [D] Document CVE-2026-4539 ignore rationale in `dependency-vuln-rescan.yml`
- [ST-21] [D] Confirm `dependency-vuln-rescan.yml` runs successfully post-merge
- [ST-22] [G] File retroactive DEV record for the dark-mode/Radix-portal `Layout.js` fix
- [ST-23] [G] `shared_standards_changelog.md` missing v3.27 entry — backfilled
- [ST-24] [G] `execution_state.json`'s `deviations_filed` field is used as "check performed" not literally "filed" — documented
- [ST-25] [G] Annotate `BLG-FE-146`/`BLG-FE-139` with 2026-08-10 trigger-condition re-check — resolved as moot
- [ST-26] [G] Correct `BLG-GOV-288`'s Acceptance Criteria text — resolved as moot

Sign-off: Product Owner — 2026-08-12
QA sign-off: Director of Quality — 2026-08-12

---

## v8.5 — Frontend Correctness, Design Consistency & Security Hardening — 2026-08-10
Cycle: 2026-08-08__release-v8.5
Verified: Verified
Verification report: claude/cycles/2026-08-08__release-v8.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Production correctness fixes — `GET /analytics/tag-performance` 500 on staging (missing `trade_tags` table ensure); confirmed and hardened `api-key-cross-environment-check.yml` (real gap: unhandled probe timeout masquerading as a cross-wired-keys false alarm) | `docs/specs/api_contracts/analytics_endpoints.md`; `docs/security/api_key_security_register.md`; `.github/workflows/api-key-cross-environment-check.yml` |
| EPIC-02 | Security hardening — security-fix false-positive rate assessment (0% measured); new monthly dependency-vulnerability re-scan cadence (pip-audit + npm audit); Application X-API-Key rotation runbook | `st03_sec02_false_positive_rate_assessment.md`; `.github/workflows/dependency-vuln-rescan.yml`; `scripts/check_dependency_vuln_rescan.py`; `docs/ops/api_key_rotation_policy.md` |
| EPIC-03 | Frontend correctness fixes — registered `muted`/`muted-foreground` design tokens in `tailwind.config.js`; frontend wiring for `trade_plans.thesis_model_version`/`thesis_prompt_version` on save; exact-zero P&L colour convention reconciled between Monthly P&L and Tax Year tables. Systemic fix found and applied at the root: the app-wide `dark` theme class was never applied to `document.documentElement`, so every Radix Dialog-based component (14+ consumers) was always rendered in light-theme CSS scope regardless of the user's actual theme (`src/Layout.js`) | `tailwind.config.js`; `docs/specs/api_contracts/trade_plan_endpoints.md`; `docs/design/2026-08-08__release-v8.5/exact-zero-pnl-colour-convention/decision_record.md`; `docs/specs/frontend/pages/reports.md` |
| EPIC-04 | Design-system & contrast consistency audit — v6.7 secondary-text token drift audit (6 instances found, follow-up filed); empty-state microcopy consistency pass (trailing-period fix on 2 pages); theme-toggle persistence confirmed correct, flash-on-load defect fixed; mobile-responsive audit for PerformanceAnalytics (4 drift instances fixed); dark/light contrast audit follow-up; ad hoc component inventory for shared design-system extraction candidates | `st09_secondary_text_token_audit_findings.md`; `docs/design/2026-08-08__release-v8.5/empty-state-microcopy-pattern/decision_record.md`; `docs/specs/frontend/design_system.md`; `docs/specs/frontend/pages/analytics.md`; `st13_dark_light_contrast_audit_followup.md`; `st14_ad_hoc_component_inventory.md` |
| EPIC-05 | Frontend UX review & documentation — nav bar redesign exploration (no redesign warranted at current scale); SI-05 Telegram digest user journey map refreshed (found stale, 2 friction items already resolved); reusable empty-state component spec added to the Base44 prompt template library; Reports page information hierarchy review (2 follow-ups filed); `ChartStyle`/`calendar.js` consumer checks confirmed both remain unused, no action needed | `st15_nav_bar_redesign_exploration.md`; `docs/ux/si05_user_journey_map.md`; `docs/specs/frontend/base44_prompt_template_library.md#12. Template: Standard Full-Page/Section Empty-State (Non-Card Context)`; `st18_reports_page_information_hierarchy_review.md`; `st19_st20_chart_calendar_consumer_check.md` |
| EPIC-06 | Analytics & governance process fixes — new `GET /screener/regime-distribution` endpoint and Regime History panel; Product Value Ratio historical trend chart (structured record, backfilled DL-057–077); Release Planning `sprint_sealed` reset-on-publish fix; `CLAUDE.md` §8 sibling-vs-sibling union clause for cross-EPIC array-field merges; fixed unrestored `sys.modules` stubbing in `test_alerts_service.py` (cross-file test pollution) | `docs/specs/api_contracts/screener_api_contract.md#GET /screener/regime-distribution`; `claude/roadmap/product_value_ratio_history.md`; `claude/system/release_planning_prompt.md#STEP 7`; `CLAUDE.md#8. Cross-EPIC Merge Conflict Resolution`; `tests/test_alerts_service.py` |

### Deviations accepted
None — zero deviations filed this sprint (all six `qa_evidence_EPIC-xx.md` logs record "Known deviations filed: None"). ST-08 resolved a deviation opened in a prior cycle (`DEV-REPORTS-ST01-02`) rather than filing a new one.

### Tech backlog items shipped
- [ST-01] [D] Fix `GET /analytics/tag-performance` 500 on staging (missing `trade_tags` column ensure)
- [ST-02] [D] Confirm `api-key-cross-environment-check.yml` is genuinely running, not silently skipping — hardened a real probe-timeout/false-alarm gap found live
- [ST-03] [D] Security fix false-positive rate assessment (BLG-SEC-02) — 0% measured
- [ST-04] [D] Recurring dependency vulnerability re-scan cadence (consolidated pip-audit + npm audit)
- [ST-05] [D] API key rotation runbook (Application X-API-Key)
- [ST-06] [U] Register `muted`/`muted-foreground` design tokens in `tailwind.config.js` — also surfaced and fixed the app-wide dark-mode-portal CSS scoping bug
- [ST-07] [D] Frontend wiring to populate `trade_plans.thesis_model_version`/`thesis_prompt_version` on save
- [ST-08] [U] Reconcile Monthly P&L vs Tax Year table's exact-zero P&L colour convention
- [ST-09] [D] Design token audit: v6.7 contrast fix consistency (6 drift instances found, follow-up filed)
- [ST-10] [U] Empty-state illustration/microcopy consistency pass
- [ST-11] [U] Confirm theme-toggle persistence across sessions — fixed flash-on-load defect
- [ST-12] [U] Mobile responsive audit for PerformanceAnalytics page (4 drift instances fixed)
- [ST-13] [D] Dark/light theme contrast audit follow-up
- [ST-14] [D] Ad hoc component inventory: candidates for shared design-system extraction
- [ST-15] [D] Nav bar redesign exploration — no redesign warranted
- [ST-16] [D] User journey map: SI-05 Telegram digest to app action — refreshed, found stale
- [ST-17] [P] Reusable empty-state component spec for Base44 prompts
- [ST-18] [D] Reports page information hierarchy review — 2 follow-ups filed
- [ST-19] [D] Rework ChartStyle `style-src 'unsafe-inline'` dependency — trigger condition unmet, no consumer
- [ST-20] [D] Playwright/staging visual verification of `calendar.js` — trigger condition unmet, no consumer
- [ST-21] [U] Regime distribution metric over screener history — new endpoint + Regime History panel
- [ST-22] [G] Product Value Ratio historical trend chart (internal governance tooling)
- [ST-23] [G] Release Planning `sprint_sealed` reset-on-publish fix
- [ST-24] [G] `CLAUDE.md` §8 sibling-vs-sibling union clause for `execution_state.json` array fields
- [ST-25] [D] Fix unrestored `sys.modules` stubbing in `test_alerts_service.py` (cross-file test pollution)

Sign-off: Product Owner — 2026-08-10
QA sign-off: Director of Quality — 2026-08-10

---

## v8.4 — User-Facing Reporting & Full-Capacity Debt Clearance — 2026-08-08
Cycle: 2026-08-07__release-v8.4
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-08-07__release-v8.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | User-facing reporting enhancements — Avg P&L/Trade column on Monthly P&L Report; trade-tag/trigger-source (`trade_origin`) column on tax-year P&L CSV export | `docs/specs/frontend/pages/reports.md`; `docs/specs/api_contracts/reports_endpoints.md` |
| EPIC-02 | API contract & spec debt closure — openapi.yaml structural defect (~23 endpoints mis-nested under `components:`), 4 stale contract examples, security-scheme documentation completeness, data model backfill for 4 tables, formal schema-versioning doc | `docs/reference/openapi.yaml`; `docs/specs/api_contracts/settings_endpoints.md`, `position_endpoints.md`, `health_endpoints.md`, `watchlist_endpoints.md`, `conventions.md`; `docs/specs/data_model.md`; `docs/specs/schema_versioning_trade_plan_position.md` |
| EPIC-03 | Backend engineering hardening — trade_plans ticker functional index, Alpaca paper-sync 429/backoff handling, AI provenance logging, trade plan mutation/audit-trail log, auto-generated data dictionary | `docs/specs/api_contracts/trade_plan_endpoints.md`; `docs/specs/data_model.md` |
| EPIC-04 | Frontend code health, accessibility & security — Dialog/DialogTitle className-override audit, remaining dark-only-token form-validation colour gaps, WatchlistModal.js ESLint cleanup, CSP `unsafe-inline` removal for script-src/style-src | `docs/ops/dialog_classname_override_audit_2026-08-07.md`; `docs/ops/csp_unsafe_inline_audit_2026-08-08.md` |
| EPIC-05 | Operational reliability & cost monitoring — SI-05 weekly digest staging verification, api_performance_baseline.md endpoint coverage drift closure (19 endpoints + SI-05 send route), CI runner cache warm-up, DB storage growth cost trend tracking, Arc 4 AI API cost model | `docs/ops/api_performance_baseline.md`; `docs/operations/arc4_ai_cost_model.md`; `docs/ops/cloud_infra_spend_by_epic.md`; `docs/ops/si05_digest_delivery_root_cause_2026-08-05.md` |
| EPIC-06 | QA & test infrastructure hardening — fixed wrong patch target in portfolio history test, regression baseline backfill (24 undocumented Playwright specs, v6.0–v7.3), recurring CSV export content regression check, signal correctness fix impact measurement | `docs/qa/regression_test_suite_baseline.md`; `docs/ops/blg_be_40_impact_measurement_findings_2026-08-08.md` |
| EPIC-07 | Governance process integrity — canonical scripted gate-detection procedure for Release Planning's ungated-candidate scan; cross-EPIC merge conflict runbook dry run | `claude/system/release_planning_prompt.md`; `docs/ops/cross_epic_merge_runbook_dry_run_2026-08-08.md` |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| `DEV-REPORTS-ST01-02` | P3 | Monthly Financial Table's zero-P&L colour rule (grey/neutral) differs from the Tax Year Trades Table's (red-for-zero) — pre-existing spec-wording inaccuracy surfaced during ST-01's own review, corrected in `reports.md` v0.15; cross-table convergence not decided | PO (recorded; no acceptance action required — P3, backlog item `BLG-FE-144` filed) |
| — (Known Deviation, no DEV-ID) | Informational (scope reinterpretation, not a defect) | `trade_origin` (`Signal`/`Manual`, derived from `trade_plans.signal_id`) shipped in place of the originally-asked-for alert-triggered/manual distinction on the tax-year CSV export — no schema linkage exists between `price_alerts` and any trade/position row | PO — direct decision via `ESC-EXEC-20260807-01`, Option (a) |

### Tech backlog items shipped
- [ST-01] [U] Add Avg P&L/Trade column to Monthly P&L Report table
- [ST-31] [U] Trade-tag/trigger-source column on tax-year P&L CSV export — shipped as `trade_origin` (Signal/Manual)
- [ST-02] [D] Fix openapi.yaml structural defect (~23 endpoints nested inside `components:`)
- [ST-03] [D] settings_endpoints.md GET /settings example missing created_at/updated_at
- [ST-04] [D] position_endpoints.md GET /positions example missing 5 live fields
- [ST-05] [D] health_endpoints.md GET /health example missing external_apis/ai_journal
- [ST-06] [D] watchlist_endpoints.md GET /watchlist illustrative example is stale
- [ST-07] [D] OpenAPI security-scheme & auth-header documentation completeness check
- [ST-08] [D] Backfill missing data_model.md sections for 4 undocumented tables
- [ST-09] [D] Formal schema-versioning doc for trade_plan/position tables
- [ST-10] [D] Add functional index on trade_plans(UPPER(ticker))
- [ST-11] [D] Add 429/backoff handling to Alpaca paper-sync close/positions endpoints
- [ST-12] [D] Log AI model+version provenance on stored thesis/summary text
- [ST-13] [D] Mutation/audit-trail log for trade plan edits post-entry
- [ST-14] [D] Auto-generated data dictionary from live schema
- [ST-15] [D] Audit Dialog/DialogTitle className-override sites for the cn()-has-no-tailwind-merge defect class
- [ST-16] [D] Close remaining dark-only-token gaps in inline form-validation error text
- [ST-17] [D] WatchlistModal.js fails ESLint (24 problems) — same patterns fixed in Watchlist.js
- [ST-18] [D] CSP allows 'unsafe-inline' for script-src and style-src
- [ST-19] [D] Staging verification required for SI-05 weekly digest fix
- [ST-20] [D] Endpoint coverage drift: 19 endpoints missing from api_performance_baseline.md
- [ST-21] [D] Add POST /digest/si05/send to api_performance_baseline.md
- [ST-22] [D] CI runner cache warm-up for backend/.venv to cut pytest job time
- [ST-23] [D] Database storage growth cost trend tracking (Postgres/Supabase)
- [ST-24] [D] AI API cost model for Arc 4 journal intelligence features
- [ST-25] [D] Fix wrong patch target in test_get_portfolio_history_returns_ok
- [ST-26] [D] Backfill regression baseline with 24 undocumented Playwright spec files (v6.0-v7.3)
- [ST-27] [D] Recurring CSV export content regression check
- [ST-28] [D] Signal correctness fix impact measurement
- [ST-29] [G] Canonical, scripted gate-detection procedure for Release Planning's ungated-candidate scan
- [ST-30] [G] Dry-run the cross-EPIC merge conflict runbook

Sign-off: Product Owner — 2026-08-08
QA sign-off: Director of Quality — 2026-08-08

---

## v8.3 — Operational Reliability & Governance Debt Clearance — 2026-08-07
Cycle: 2026-08-05__release-v8.3
Verified: Verified
Verification report: claude/cycles/2026-08-05__release-v8.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Root-caused and fixed the SI-05 weekly Telegram digest delivery pipeline (no automated trigger had ever been committed for `POST /digest/si05/send`) and added delivery-failure alerting; added a recurring check confirming staging/production API keys remain cross-environment-distinct; added a Gemini API key rotation runbook | `docs/specs/api_contracts/digest_endpoints.md#POST /digest/si05/send`; `docs/security/api_key_security_register.md#3. Anthropic API Key` |
| EPIC-02 | Database index audit for Arc 4 cross-table queries; Alpaca API rate-limit backoff audit; canonical `position_state` enum registry shared frontend/backend; remaining routers conformed to the canonical error envelope + status codes; retry/backoff added for Yahoo Finance regime-check call sites; idempotent retry added for Alpaca paper-trading order sync | `docs/specs/position_lifecycle_states_registry.md`; `docs/specs/api_contracts/conventions.md#13. Error Response Standard (Canonical)`; `docs/specs/api_contracts/backend_engineering_patterns.md#Error-response envelope conformance` |
| EPIC-03 | Migrated `ComplianceRecheckModal.js` onto the shared Dialog primitive; extracted a shared modal-confirmation component (configurable message, optional undo-window countdown); documented a unified loading-skeleton pattern for async-loading cards; added a standard Base44 prompt section for dark/light theme compliance; extracted a single shared `AiDisclaimer` component | `docs/specs/frontend/design_system.md#Confirmation Modal (with optional undo window)`; `docs/specs/frontend/design_system.md#Data States`; `docs/specs/frontend/base44_prompt_template_library.md#11. Template: Standard Theme-Compliance Section (Generation-Time)` |
| EPIC-04 | Added baseline Playwright coverage for `Watchlist.js`; documented and ran the first quarterly OpenAPI 3-way drift sweep (zero drift found); added a pre-merge lint catching stale DoQ sign-off Pending rows; performed an OpenAPI response-example drift spot-check; added an API endpoint deprecation-window policy; added a canonical form-validation error-message pattern spec | `docs/specs/api_contracts/conventions.md#14. API Endpoint Deprecation-Window Policy`; `docs/specs/frontend/design_system.md#Error States` |
| EPIC-05 | Removed the RESUME PRECHECK mutation-detection block from `release_planning_prompt.md` (Terminal State Guard and State File Immutability Rule retained); added a formal semi-annual §13 boundary re-attestation cadence; reviewed the SI-02 11-linked-trade-plan gate threshold (conclusion: still appropriate); fixed `prompt_change_log.md`'s mixed prepend/append ordering that broke gap detection; defined a cross-role workload balance check surfaced at roadmap rebalance | `claude/system/release_planning_prompt.md#Terminal State Guard — Published Is Immutable (Hard Gate)`; `claude/strategy/strategy_rules.md#13.5 Semi-Annual Boundary Re-Attestation Cadence`; `claude/system/shared_standards.md#11.1 STEP -1.7-Class Prompt Change Log Gap Detection`; `claude/system/roadmap_prompt.md#7.2 Cross-Role Workload Balance Check` |
| EPIC-06 | Monthly P&L report format review — 3-month usage retrospective (gate cleared 2026-08-05); conclusion recorded, no format changes warranted this cycle | `docs/product/decisions/monthly_pnl_format_review_2026-08-06.md` |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] [D] BLG-OPS-129: Investigate and fix the SI-05 weekly Telegram digest delivery pipeline
- [ST-02] [D] BLG-OPS-130: Add delivery-failure alerting for the SI-05 weekly digest
- [ST-03] [D] BLG-OPS-131: Recurring check confirming staging/production API keys remain distinct
- [ST-04] [D] BLG-SEC-17: Gemini API key rotation runbook
- [ST-05] [D] BLG-BE-37: Database index audit for Arc 4 cross-table queries
- [ST-06] [D] BLG-BE-57: Alpaca API rate-limit backoff audit
- [ST-07] [D] BLG-BE-67: Canonical enum registry for `position_state` values shared frontend/backend
- [ST-08] [D] BLG-BE-69: Conform remaining routers to canonical error envelope + status codes
- [ST-09] [D] BLG-BE-79: Retry/backoff for Yahoo Finance regime-check call sites
- [ST-10] [D] BLG-BE-80: Idempotent retry for Alpaca paper-trading order sync
- [ST-11] [D] BLG-FE-103: Migrate `ComplianceRecheckModal.js` onto the shared Dialog primitive
- [ST-12] [D] BLG-FE-121: Extract a shared modal-confirmation component
- [ST-13] [D] BLG-FE-126: Unified loading-skeleton pattern for async-loading cards
- [ST-14] [D] BLG-FE-132: Standard Base44 prompt section for dark/light theme compliance
- [ST-15] [D] BLG-FE-81: AI disclaimer component extraction
- [ST-16] [D] BLG-QA-86: Add baseline Playwright coverage for `Watchlist.js`
- [ST-17] [D] BLG-QA-94: OpenAPI drift gate false-negative sweep
- [ST-18] [D] BLG-QA-98: DoQ sign-off staleness pre-merge lint
- [ST-19] [D] BLG-SPEC-88: OpenAPI response-example drift spot-check
- [ST-20] [D] BLG-SPEC-96: API endpoint deprecation-window policy
- [ST-21] [D] BLG-SPEC-108: Canonical form validation error-message pattern spec
- [ST-22] [G] BLG-GOV-124: SC-02 — remove RESUME PRECHECK mutation detection block from `release_planning_prompt.md`
- [ST-23] [G] BLG-GOV-204: Formal §13 boundary re-attestation cadence
- [ST-24] [G] BLG-GOV-237: SI-02 trade-count gate threshold calibration review
- [ST-25] [G] BLG-GOV-257: `prompt_change_log.md` mixed prepend/append ordering gap-detection fix
- [ST-26] [G] BLG-GOV-270: Cross-role workload balance check
- [ST-27] [P] BLG-FEAT-45: Monthly P&L report format review — 3-month usage retrospective

Sign-off: Product Owner — 2026-08-07
QA sign-off: Director of Quality — 2026-08-07

---

## v8.2 — User-Feature Push (continued) & Full-Capacity Debt Clearance — 2026-08-05
Cycle: 2026-08-04__release-v8.2
Verified: Verified
Verification report: claude/cycles/2026-08-04__release-v8.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Added a P&L/tax record reconciliation report (system totals vs individual trade export); confirmed/specified the Compliance Recheck Modal's all-rules-pass empty state; refined RFJ event-type colour palette so `checklist_skipped`/`drawdown_prompt_dismissed`/`stop_prompt_dismissed` are perceptually distinct including under `light-daltonized`; migrated Trade Plan native form fields to the shared `focus-visible:ring-*` pattern; added a streak-length metric for the behavioural-drift endpoint's `insufficient_data` readings | `docs/specs/api_contracts/reports_endpoints.md#GET /reports/reconciliation`; `docs/specs/frontend/pages/reports.md#Reconciliation Report`; `docs/specs/frontend/pages/positions.md#Compliance Recheck Panel (Modal)`; `docs/design/2026-06-19__release-v6.0/rfj-design-review/review.md#3`; `docs/specs/frontend/design_system.md#Focus indicator contrast`; `docs/specs/metrics/si02_drift_score.md#3.5 Insufficient-Data Streak`; `docs/specs/api_contracts/behavioural_drift_contract.md#Insufficient-Data Response Shape` |
| EPIC-02 | Provisioned a distinct, independently-revocable API key for staging (live-rotated, old shared key confirmed no longer valid against production); diagnosed the silent GitHub↔Render auto-deploy webhook staleness pattern and fixed the actively-broken stale-branch config on the staging frontend, with a recurring deploy-drift detection check added | `docs/security/api_key_security_register.md#6. Application X-API-Key`; `claude/backlog/backlog.md#BLG-OPS-128` |
| EPIC-03 | 11-item governance-process integrity cluster: SI-05 Phase 1 30-day effectiveness review (PAUSE, re-evaluate 2026-10-03); `velocity_metrics.md` row-count audit (parity confirmed); Arc 5 composite formula confirmed to already account for v6.9 recheck events; rebalance-skip advisory now verifies the next release is actually scoped before recommending skip; AI vendor (Gemini/Anthropic) ToS & DPA review; direct-write/governance-bypass pattern tracker; idea-intake backlog-overlap check effectiveness retrospective; SI-02 production credential provisioning standing-behaviour decision; mandatory §13 boundary pre-check at design gate for AI-calling proposals; `Last Updated` header-history retention convention codified; `governance_sync.yml` auto-close regex no longer closes issues on delegation-record-only commits | `claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md#30-Day Review — 2026-08-04`; `claude/cycles/velocity_metrics.md#Row-Count Audit`; `docs/specs/metrics_definitions.md#v6.9 On-Demand Compliance Recheck — Confirmed No Formula Gap`; `claude/system/post_ship_closure.md#Rebalance Cadence Check`; `docs/specs/security/ai_vendor_tos_dpa_review.md`; `claude/roadmap/governance_bypass_log.md`; `docs/governance/idea_intake_overlap_check_retrospective_2026-08-04.md`; `claude/system/roadmap_prompt.md#STEP 2.3`; `claude/system/design_gate_prompt.md#STEP 1`; `claude/system/shared_standards.md#§16.14`; `.github/workflows/governance_sync.yml` |
| EPIC-04 | Documented a quarterly dependency-upgrade cadence for `backend/requirements.txt`; tuned CI caching (dependency install, browser binaries) for the Playwright job; added an automated pre-commit hook linting the `[EPIC-xx][ST-xx]` commit-message format | `docs/ops/dependency_upgrade_cadence.md`; `.github/workflows/playwright.yml`; `.github/workflows/smoke-tests.yml`; `.githooks/commit-msg`; `.githooks/test_commit_msg.sh` |
| EPIC-05 | Added a snapshot test asserting `SystemStatus.js`'s hardcoded fallback counts against an AST-derived endpoint-test count; reconstructed 13 undocumented `sprint_planning_changelog.md` versions (v3.1–v3.13); removed a dead-code duplicate `POST /test/endpoints` handler in `backend/main.py`; added a motion/timing-sensitive chart-interaction checklist item to the design gate | `claude/cycles/2026-08-04__release-v8.2/stage4_backlog_slice.md#ST-22`; `claude/cycles/2026-08-04__release-v8.2/stage4_backlog_slice.md#ST-23`; `claude/cycles/2026-08-04__release-v8.2/stage4_backlog_slice.md#ST-24`; `claude/system/design_gate_prompt.md#STEP 1 — Classify Each Item` |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] [U] BLG-FEAT-88: P&L / tax record reconciliation report (system totals vs individual trade export)
- [ST-02] [U] BLG-FE-105: Compliance Recheck Modal all-pass empty-state design
- [ST-03] [U] BLG-FE-67: RFJ event type colour palette refinement
- [ST-04] [U] BLG-FE-138: Trade Plan native form fields focus indicator fix
- [ST-05] [U] BLG-FEAT-86: Drift-detection metric for the behavioural-drift endpoint's `insufficient_data` streak
- [ST-06] [D] BLG-SEC-27: Distinct API key for the staging environment
- [ST-07] [D] BLG-OPS-128: Detect silent staging deploy staleness
- [ST-08] [G] BLG-GOV-160: File SI-05 Phase 1 30-day effectiveness review record
- [ST-09] [G] BLG-GOV-213: `velocity_metrics.md` row-count audit
- [ST-10] [G] BLG-GOV-214: Confirm Arc 5 composite formula accounts for v6.9 recheck events
- [ST-11] [G] BLG-GOV-218: Rebalance-skip advisory verifies next release is actually scoped
- [ST-12] [G] BLG-GOV-265: AI vendor Terms-of-Service & data-processing review
- [ST-13] [G] BLG-GOV-269: Direct-write / governance-bypass pattern tracker
- [ST-14] [G] BLG-GOV-278: Idea-intake backlog-overlap check effectiveness retrospective
- [ST-15] [G] BLG-GOV-279: SI-02 production credential provisioning decision
- [ST-16] [G] BLG-GOV-281: Mandatory §13 boundary pre-check at design gate
- [ST-17] [G] BLG-GOV-283: `Last Updated` header-history retention convention
- [ST-18] [G] BLG-GOV-285: `governance_sync.yml` delegation-commit auto-close fix
- [ST-19] [D] BLG-OPS-116: Quarterly dependency-upgrade cadence
- [ST-20] [D] BLG-OPS-118: CI cache tuning to reduce Playwright suite runtime
- [ST-21] [D] BLG-OPS-125: Automated commit-message format lint
- [ST-22] [D] BLG-QA-126: Snapshot test for `SystemStatus.js` hardcoded fallback counts
- [ST-23] [D] BLG-SPEC-110: Reconstruct 13 undocumented versions in `sprint_planning_changelog.md`
- [ST-24] [D] BLG-BE-81: Remove dead-code duplicate `POST /test/endpoints` handler
- [ST-25] [G] BLG-FE-131: Design-gate checklist addendum for motion/timing-sensitive chart interactions

Sign-off: Product Owner — 2026-08-05
QA sign-off: Director of Quality — 2026-08-05

---

## v8.1 — User-Feature Push & Governance Debt Clearance — 2026-08-03
Cycle: 2026-08-03__release-v8.1
Verified: Verified
Verification report: claude/cycles/2026-08-03__release-v8.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Fixed Trade Plan tag-suggestion buttons to be keyboard-operable (`onMouseDown` → `onClick`) | `docs/specs/frontend/components/journal_components.md#4` |
| EPIC-02 | Established a recurring manual `pg_dump` backup schedule for production Supabase, with dry-run restore verification | `docs/ops/database_backup_disaster_recovery_runbook.md#3.4` |
| EPIC-03 | Formal sunset criteria for perennially-returning gated backlog items; escalation path for Product Value Ratio's persistent Advisory tier; minimum capacity buffer floor recommendation for sprint planning; consolidated technical debt registry; skill-silo mitigation via execution-heavy story rotation; automated PII scan gate for new backend endpoints; governed write path for unversioned Now-horizon carry-forward headings | `claude/system/release_planning_prompt.md#1.4a.1`; `claude/system/roadmap_prompt.md#2.4`; `claude/system/sprint_planning_prompt.md#1.5`; `claude/backlog/technical_debt_registry.md`; `claude/system/release_planning_prompt.md#STEP 3`; `scripts/check_pii_field_patterns.py`; `.github/workflows/quality_gate.yml`; `claude/system/shared_standards.md#17` |
| EPIC-04 | Staging-verified custom price alert live delivery; recurring pre-sprint-planning endpoint test coverage audit; cross-EPIC deviation (DEV-*) consolidation review across cycles; post-parallelization Playwright shard balance audit | `scripts/audit_endpoint_test_coverage.py`; `claude/system/sprint_planning_prompt.md#STEP -1`; `docs/governance/deviation_consolidation_review_2026-08-03.md`; `claude/system/post_ship_closure.md#STEP 5.1`; `docs/ops/ci_pipeline_baseline.md#7` |
| EPIC-05 | Revisited and formally defined SI-02 Gate Status condition-2/3 thresholds (including sufficient-data threshold); added explicit §13 continuity note for v6.9 on-demand recheck | `docs/specs/frontend/pages/reports.md#SI-02 Gate Status`; `claude/strategy/strategy_rules.md#13.4`; `docs/specs/metrics/si02_drift_score.md#2`; `claude/roadmap/current_roadmap.md` |
| EPIC-06 | Standardised cursor-based pagination pattern across list endpoints (consolidated); scoped `trade_plans.position_id` historical backfill design | `docs/specs/api_contracts/backend_engineering_patterns.md#Cursor-based pagination pattern for list endpoints`; `docs/specs/trade_plans_position_id_backfill_scoping.md` |
| EPIC-07 | Implemented per-EPIC `execution_state.json` files (Option 1), resolving the recurring cross-EPIC merge-conflict pattern designed in v8.0 | `claude/system/shared_standards.md#12` |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] [U] Trade Plan tag-suggestion buttons use `onMouseDown`, not keyboard-operable — fixed to `onClick`, keyboard-navigable per spec
- [ST-02] [D] Recurring manual `pg_dump` backup schedule for production Supabase
- [ST-03] [G] Formal sunset criteria for perennially-returning gated backlog items
- [ST-04] [G] Escalation path for Product Value Ratio's persistent Advisory tier
- [ST-05] [G] Minimum capacity buffer floor recommendation for sprint planning
- [ST-06] [G] Technical debt registry (consolidated cross-cycle view)
- [ST-07] [G] Skill-Silo mitigation: rotate execution-heavy story assignment pattern
- [ST-08] [D] Automated PII scan gate for new backend endpoints
- [ST-09] [G] Governed write path for a non-empty, unversioned Now-horizon carry-forward
- [ST-10] [D] Staging sign-off: custom price alert live delivery firing
- [ST-11] [D] Recurring pre-sprint-planning endpoint test coverage audit
- [ST-12] [G] Cross-EPIC deviation (DEV-*) consolidation review across cycles
- [ST-13] [D] Post-parallelization Playwright shard balance audit
- [ST-14] [D] Revisit SI-02 Gate Status Condition 2/3 threshold definitions
- [ST-15] [D] Explicit §13 continuity note for v6.9 on-demand recheck
- [ST-16] [D] Formally define SI-02 condition-3 sufficient data threshold
- [ST-17] [D] Standardise pagination pattern across list endpoints (consolidated)
- [ST-18] [P] `trade_plans.position_id` historical backfill design
- [ST-19] [G] Implement per-EPIC `execution_state.json` files (Option 1)

Sign-off: Product Owner — 2026-08-03
QA sign-off: Director of Quality — 2026-08-03

---

## v8.0 — Data Integrity, Security Follow-Through & Operational Hardening — 2026-07-31
Cycle: 2026-07-30__release-v8.0
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-07-30__release-v8.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Added `strategy_version_at_entry` to `trade_plans`/`positions`; reviewed FX handling post-DS-05 US market source change (no amendment needed); audited and closed 3 FX conversion audit-trail gaps (`fx_rate_used` missing from `POST /portfolio/position`, `GET /portfolio/prospective-heat`, and pre-entry cash-constraint validation) | `docs/specs/data_model.md#DS-11`; `docs/product/decisions/ds05-fx-handling-review--2026-07-30.md`; `docs/product/decisions/fx-audit-trail-completeness-check--2026-07-30.md`; `docs/specs/api_contracts/portfolio_endpoints.md#POST /portfolio/position` |
| EPIC-02 | Fixed 17 implicit-HTTP-200 error paths in `backend/main.py` (raw exception text no longer leaked); added a mandatory AI-endpoint security review checklist to the design gate; fixed keyboard reachability on the Trade Plan pre-entry checklist; fixed the Abandon modal's missing focus trap/restoration; verified `request.client.host` is not collapsed behind Render's proxy (no code change needed); fixed an invalid `.gitleaks.toml` global `[[allowlists]]` schema (3 real false-positive findings suppressed) | `docs/specs/api_contracts/conventions.md#13. Error Response Standard (Canonical)`; `docs/specs/security/ai_endpoint_security_checklist.md`; `claude/system/design_gate_prompt.md#2.2`; `docs/design/2026-07-30__release-v8.0/entry-checklist-keyboard-accessibility/decision_record.md`; `docs/design/2026-07-30__release-v8.0/abandon-modal-focus-trap/decision_record.md`; `claude/cycles/2026-07-30__release-v8.0/release_plan.md#RISK-02`; `.gitleaks.toml` |
| EPIC-03 | Swept `tests/e2e/` for §18 anti-patterns (3 `networkidle` instances, 1 route-ordering bug fixed); established a smoke/critical/regression Playwright test-tagging convention and wired `@smoke` into CI; built a synthetic trade-history generator for gated-feature testing | `claude/system/shared_standards.md#18. Playwright Test Authoring Standard`; `docs/team_skills/quality/playwright_patterns.md#6. Test Tagging Convention (v1.1)`; `backend/test_data/generate_synthetic_trade_history.py` |
| EPIC-04 | Built and live-fire verified Render health-check-to-Telegram alerting on sustained 5xx spikes; configured Telegram repo secrets; executed a real staging rollback drill (one runbook procedure correction applied); audited the production Render dashboard-only build/deploy path filter (no gap found); drafted a database backup/DR runbook and confirmed production Supabase tier (Free — no automated backups/PITR, gap flagged) | `.github/workflows/health-check-alert.yml`; `docs/operations/render_rollback_runbook.md#Execution History`; `docs/ops/render_build_deploy_path_filter_audit.md`; `docs/ops/database_backup_disaster_recovery_runbook.md` |
| EPIC-05 | Extracted 3 new reusable Base44 prompt fragments from existing loading-skeleton precedent | `docs/specs/frontend/base44_prompt_template_library.md (v1.4)` |
| EPIC-06 | Designed and signed off a structural fix for the recurring cross-EPIC `execution_state.json` merge-conflict pattern (per-EPIC state files, Option 1) — implementation deliberately deferred to a clean cycle boundary | `claude/cycles/2026-07-30__release-v8.0/execution_escalations.md#ESC-EXEC-20260731-01` |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|--------------|-------------|
| DEV-VER-2026-07-31-01 | P2 | ST-19's AC required the cross-EPIC `execution_state.json` merge-conflict structural fix to be designed AND implemented this sprint; only the design decision was completed, implementation deliberately deferred to a follow-up story (`BLG-GOV-284`) per Head of Specs Team guidance on clean cycle boundaries | PO + DoQ |

### Tech backlog items shipped
- [ST-01] [D] BLG-SPEC-78: `strategy_version_at_entry` field on `trade_plans`/`positions`
- [ST-02] [D] BLG-SPEC-79: FX handling review post-DS-05 US market source change
- [ST-03] [D] BLG-SPEC-107: FX conversion audit trail completeness check (§4.1.5 effective-rate logging)
- [ST-04] [D] BLG-SEC-25: Raw exception text leaked in implicit-HTTP-200 error paths in `backend/main.py`
- [ST-05] [G] BLG-SEC-23: Mandatory security review checklist for new AI-calling endpoints
- [ST-06] [U] BLG-FE-135: Trade Plan pre-entry checklist items unreachable by keyboard
- [ST-07] [U] BLG-FE-136: Trade Plan "Abandon" modal has no focus trap or restoration
- [ST-08] [D] BLG-SEC-24: Verify `request.client.host` reflects true client IP behind Render's proxy
- [ST-09] [D] BLG-SEC-26: `.gitleaks.toml`'s global `[[allowlists]]` blocks use an invalid schema
- [ST-10] [D] BLG-QA-97: Retroactive Playwright §18 anti-pattern sweep (consolidated)
- [ST-11] [D] BLG-QA-120: Test-tagging convention (smoke/regression/critical) for selective CI runs
- [ST-12] [D] BLG-QA-121: Synthetic trade-history data generator for gated-feature testing
- [ST-13] [D] BLG-OPS-114: Render service health-check alerting to Telegram on 5xx spike
- [ST-14] [D] BLG-OPS-115: Configure `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` as GitHub Actions repo secrets
- [ST-15] [D] BLG-OPS-109: Confirm Render rollback runbook has real execution history
- [ST-16] [D] BLG-OPS-124: Render dashboard-only build/deploy path filter audit
- [ST-17] [D] BLG-OPS-126: Backup & disaster recovery runbook for production database
- [ST-18] [P] BLG-FE-124: Reusable Base44 prompt fragment library for common layouts
- [ST-19] [G] BLG-GOV-263: Structural fix for recurring cross-EPIC `execution_state.json` merge-conflict pattern (design only — implementation follow-up: `BLG-GOV-284`)

Sign-off: Product Owner — 2026-07-31
QA sign-off: Director of Quality — 2026-07-31

---

## v7.10 — Reliability, Security & Contract Hardening — 2026-07-30
Cycle: 2026-07-28__release-v7.10
Verified: Verified
Verification report: claude/cycles/2026-07-28__release-v7.10/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Fixed silent HTTP-200 error masking in `portfolio_risk.py`; extended retry/backoff audit to Yahoo Finance, Gemini, and Claude call sites; established and applied an idempotency-key pattern to state-mutating POST endpoints; audited deprecated-table read paths and removed dead code | `docs/specs/api_contracts/backend_engineering_patterns.md#Idempotency-key pattern for state-mutating POST endpoints`; `docs/specs/data_model.md#Deprecated Tables`; `docs/ops/backoff_audit_2026-07-29.md`; `docs/ops/deprecated_table_read_audit_2026-07-29.md` |
| EPIC-02 | Added a local secrets-scanning pre-commit gate (gitleaks); audited AI rate-limit bypass and public-endpoint rate-limiting posture; removed raw exception text from 27 API error responses | `.githooks/pre-commit`; `.gitleaks.toml`; `docs/ops/ai_rate_limit_bypass_audit_2026-07-29.md`; `docs/security/rate_limit_audit_2026-07-29.md` |
| EPIC-03 | Migrated Playwright E2E `webServer` to a production build; added Red Flag Journal auth regression coverage; audited endpoint test-suite coverage against all `backend/routers/` files; added consumer-driven contract-drift check tooling | `docs/ops/e2e_production_build_migration_2026-07-29.md`; `docs/ops/endpoint_test_coverage_audit_2026-07-29.md`; `docs/ops/consumer_contract_check_2026-07-29.md` |
| EPIC-04 | Corrected three API contract drift issues (`GET /positions` envelope claim, undocumented lifecycle fields; `GET /trades` JSON example completeness); confirmed the OpenAPI heading-drift CI linter already live from v7.8 | `docs/specs/api_contracts/position_endpoints.md#GET /positions`; `docs/specs/api_contracts/trade_endpoints.md#GET /trades` |
| EPIC-05 | Rewrote `calendar.js` against the current `react-day-picker` v9+ API; fixed a `SystemStatus.js` endpoint-categorization branch gap; consolidated `StrategyBenchmark.js`'s page header onto the shared `PageHeader` component; completed a keyboard-navigation and focus-order audit | `docs/specs/frontend/pages/strategy_benchmark.md#2. Page Header`; `docs/ops/keyboard_navigation_audit_2026-07-29.md` |
| EPIC-06 | Confirmed two governance process fixes (design-gate state-pointer sync; same-day rebalance collision handling) already live from prior-sprint work; added a recent-rebalance recency advisory to the roadmap engine | `claude/system/design_gate_prompt.md#STEP 5 — Update Global State`; `claude/system/roadmap_prompt.md#STEP -1.5.5 — Recent-Rebalance Recency Advisory` |

### Deviations accepted
None. Every `done` ST item's deviation check (STEP 3.1.A.10) resulted in "no deviation" (see `sprint_close.md` "Deviations Filed This Sprint").

### Tech backlog items shipped
- [ST-01] [D] BLG-BE-68: Fixed errors masked as HTTP 200 in `portfolio_risk.py`
- [ST-02] [D] BLG-BE-75: Extended Alpaca backoff audit to Yahoo Finance, Gemini, and Claude call sites
- [ST-03] [D] BLG-BE-76: Idempotency-key pattern for state-mutating POST endpoints
- [ST-04] [D] BLG-BE-41: Deprecated table read-path audit
- [ST-05] [D] BLG-SEC-22: Secrets-scanning pre-commit/CI gate (gitleaks)
- [ST-06] [D] BLG-SEC-09: AI rate-limit bypass test
- [ST-07] [D] BLG-SEC-18: Rate-limit audit on public-facing endpoints
- [ST-08] [D] BLG-SEC-13: Raw exception text removed from API error responses
- [ST-09] [D] BLG-QA-127: Playwright E2E now serves a production build instead of the CRA dev server
- [ST-10] [D] BLG-QA-96: Red Flag Journal auth regression test
- [ST-11] [D] BLG-QA-133: Endpoint test suite coverage audit against all backend/routers/ files
- [ST-12] [D] BLG-QA-128: Consumer-driven contract check — frontend API calls vs documented contracts
- [ST-13] [D] BLG-SPEC-102: position_endpoints.md envelope claim corrected to match live GET /positions behaviour
- [ST-14] [D] BLG-SPEC-103: GET /positions undocumented lifecycle fields added to spec
- [ST-15] [D] BLG-SPEC-104: trade_endpoints.md JSON example completed with omitted fields
- [ST-16] [G] BLG-GOV-243: OpenAPI contract linter in CI for heading-level drift (pre-met, confirmed live from v7.8)
- [ST-17] [P] BLG-FE-122: Rewrote calendar.js against the react-day-picker v9+ API ahead of its future EPIC-05 consumer
- [ST-18] [D] BLG-FE-123: SystemStatus.js categorizeEndpoint() missing branches fixed
- [ST-19] [U] BLG-FE-106: Consolidated StrategyBenchmark.js page header onto shared PageHeader component
- [ST-20] [D] BLG-FE-134: Keyboard navigation & focus-order audit
- [ST-21] [G] BLG-GOV-256: design_gate_prompt.md state-pointer sync (pre-met, confirmed live from prior sprint)
- [ST-22] [G] BLG-GOV-216: Recent-rebalance recency advisory at roadmap STEP -1
- [ST-23] [G] BLG-GOV-207: Same-day scheduled-rebalance cycle_id collision handling (pre-met, confirmed live from prior sprint)

Sign-off: Product Owner — 2026-07-30
QA sign-off: Director of Quality — 2026-07-30

---

## v7.9 — Capacity-Fill & Engineering Hardening — 2026-07-28
Cycle: 2026-07-27__release-v7.9
Verified: Verified
Verification report: claude/cycles/2026-07-27__release-v7.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Staleness tracking and Keep/Remove review action added to Watchlist | `docs/specs/frontend/pages/watchlist.md#Staleness Indicator`; `docs/specs/api_contracts/watchlist_endpoints.md#PATCH /watchlist/{entry_id}` |
| EPIC-02 | Sector concentration / regime exposure trend chart added to Risk Dashboard | `docs/specs/frontend/pages/risk_dashboard.md#8b. Component: Sector & Regime Exposure Trend`; `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/sector-regime-trend` |
| EPIC-03 | Canonical trade_plan↔position linkage schema documented in data_model.md | `docs/specs/data_model.md#Trade Plan to Position Linkage` |
| EPIC-04 | Cost-basis method disclosure/reconciliation column added to Monthly P&L CSV export | `backend/services/reports_service.py` |
| EPIC-05 | Trailing-stop rule explainer tooltip added to position/trade view | `docs/specs/frontend/pages/positions.md#Trailing Stop Column` |
| EPIC-06 | Audit-log entries added for manual position edits (who, when, before/after) | `backend/database.py`; `backend/services/position_service.py`; `docs/specs/data_model.md#Migration from v2.16 to v2.17` |
| EPIC-07 | Permanent data-integrity smoke test added to the nightly backtest CI job | `scripts/backtest_data_integrity_smoke_test.py`; `.github/workflows/backtest.yml` |
| EPIC-08 | Read-only staging/scoped-production credential provisioned and documented | `docs/security/api_key_security_register.md#6. Application X-API-Key` |
| EPIC-09 | Common regression smoke-test tag/suite defined for EPIC-branch merges | `tests/e2e/smoke-critical-paths.spec.js` |
| EPIC-10 | Pre-commit hook added blocking commits with unregistered new routes | `scripts/check_router_test_registration.py`; `.githooks/pre-commit` |
| EPIC-11 | Chart-specific contrast checklist item added to design_system.md Accessibility section | `docs/specs/frontend/design_system.md` |
| EPIC-12 | EPIC-level cost tags added to cloud resources; per-EPIC spend summary produced | `docs/ops/cloud_infra_spend_by_epic.md` |
| EPIC-13 | Dark-mode AC checklist item added to the Base44 prompt template | `docs/specs/frontend/base44_prompt_template_library.md#4. Template: Dual-Theme Verification Call-Out` |
| EPIC-14 | Rolling log of named displacement candidates and their disposition defined | `claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md#Displacement Debt Register — Design` |
| EPIC-15 | Refresh cadence defined for Grid View visual-regression baselines | `docs/testing/visual_regression_baseline_cadence.md` |

### Deviations accepted
None. Every `done` ST item's deviation check found no divergence between implementation and canonical spec (see `sprint_close.md` "Deviations Filed This Sprint").

### Tech backlog items shipped
- [ST-01] [U] BLG-FEAT-66: Watchlist staleness/decay review — Keep/Remove action
- [ST-02] [U] BLG-FEAT-67: Historical sector/regime exposure trend chart on Risk Dashboard
- [ST-03] [D] BLG-SPEC-105: Canonical trade_plan↔position linkage schema documentation
- [ST-04] [U] BLG-FEAT-85: Cost-basis method disclosure column on Monthly P&L CSV export
- [ST-05] [U] BLG-FEAT-87: Trailing-stop rule explainer tooltip
- [ST-06] [D] BLG-BE-73: Audit-log entries for manual position edits
- [ST-07] [D] BLG-BE-74: Permanent data-integrity smoke test in nightly backtest CI
- [ST-08] [D] BLG-OPS-121: Read-only staging/scoped-production credential provisioning
- [ST-09] [D] BLG-QA-124: Common regression smoke-test tag/suite for EPIC-branch merges
- [ST-10] [D] BLG-QA-125: Pre-commit hook blocking unregistered new routes
- [ST-11] [G] BLG-FE-130: Chart-specific contrast checklist item in design_system.md
- [ST-12] [D] BLG-OPS-120: EPIC-level cost tags and per-EPIC spend summary
- [ST-13] [G] BLG-FE-129: Dark-mode AC checklist item in Base44 prompt template
- [ST-14] [G] BLG-GOV-258: Rolling log of displacement candidates and disposition
- [ST-15] [D] BLG-QA-123: Refresh cadence for Grid View visual-regression baselines

Sign-off: Product Owner — 2026-07-28
QA sign-off: Director of Quality — 2026-07-28

---

## v7.8 — Release Visibility & Engineering Hardening — 2026-07-27
Cycle: 2026-07-24__release-v7.8
Verified: Verified
Verification report: claude/cycles/2026-07-24__release-v7.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | In-app "what's new" panel sourced server-side from changelog.md, with truncation/empty/error/loading states | `docs/specs/frontend/pages/dashboard.md#6A`; `docs/specs/api_contracts/changelog_endpoints.md`; `docs/specs/frontend/design_system.md` |
| EPIC-02 | Telegram digest of shipped changelog entries sent automatically on post-ship closure (STEP 1.5) | `claude/system/post_ship_closure.md#STEP 1.5`; `backend/services/changelog_digest_service.py` |
| EPIC-03 | Contrast/focus-state accessibility pass on v7.7 notification UX — nav alert-count badge contrast fix | `docs/design/2026-07-24__release-v7.8/notification-accessibility-audit/decision_record.md` |
| EPIC-04 | Consolidated dark-mode contrast audit across all 23 shipped pages — PageHeader title-gradient via-stop fix | `docs/design/2026-07-24__release-v7.8/base44-dark-mode-contrast-audit/decision_record.md`; `docs/specs/frontend/design_system.md` |
| EPIC-05 | Monthly realized P&L CSV export alongside existing tax-year export | `docs/specs/api_contracts/reports_endpoints.md#CSV Export`; `docs/specs/frontend/pages/reports.md` |
| EPIC-06 | Per-cycle AI spend trend chart added to AI Usage & Costs view | `docs/specs/frontend/pages/settings.md#6a`; `docs/specs/api_contracts/ai_endpoints.md#GET /ai/spend-trend` |
| EPIC-07 | Rotation-and-audit schedule defined for all 5 external API key types | `docs/ops/api_key_rotation_and_audit_schedule.md` |
| EPIC-08 | Endpoint rate-limit audit across all 128 live endpoints — 4 previously-unlimited endpoints remediated | `docs/security/rate_limit_audit_2026-07-26.md` |
| EPIC-09 | Shared retry/backoff decorator extracted and migrated to highest-traffic external call site (Yahoo price fetch) | `backend/utils/retry.py` |
| EPIC-10 | Flaky-test quarantine mechanism defined and CI-enforced | `docs/testing/flaky_test_quarantine_process.md` |
| EPIC-11 | Pilot contract tests added for 3 highest-traffic endpoints (positions, trades, portfolio) | `docs/testing/pilot_contract_test_approach.md`; `docs/specs/api_contracts/position_endpoints.md`; `docs/specs/api_contracts/trade_endpoints.md`; `docs/specs/api_contracts/portfolio_endpoints.md` |
| EPIC-12 | CI lint step added for API contract `##` heading-level compliance | `.github/workflows/openapi-drift.yml`; `scripts/lint_api_contract_headings.py` |

### Deviations accepted
None. Every `done` ST item's deviation check found no divergence between implementation and canonical spec (see `sprint_close.md` "Deviations Filed This Sprint").

### Tech backlog items shipped
- [ST-01] [U] BLG-FE-128: In-app "what's new" panel for most recent release
- [ST-02] [G] BLG-FEAT-84: Automated Telegram changelog digest after each release
- [ST-03] [U] BLG-FE-127: Accessibility pass on v7.7 notification UX components
- [ST-04] [U] BLG-FE-125: Dark-mode contrast audit across Base44-generated pages
- [ST-05] [U] BLG-FEAT-81: Monthly realized P&L CSV export
- [ST-06] [U] BLG-FEAT-82: AI usage spend trend dashboard (Gemini/Claude, per release cycle)
- [ST-07] [D] BLG-SEC-20: Scheduled rotation-and-audit cadence for third-party API keys
- [ST-08] [D] BLG-SEC-21: Rate-limiting review of public-facing endpoints
- [ST-09] [D] BLG-BE-71: Shared retry/backoff decorator for external data calls
- [ST-10] [D] BLG-QA-117: Flaky-test quarantine process for the Playwright suite
- [ST-11] [D] BLG-QA-119: Contract tests for highest-traffic frontend/backend endpoints
- [ST-12] [D] BLG-OPS-117: Automated lint check for API contract `##` heading level

Sign-off: Product Owner — 2026-07-27
QA sign-off: Director of Quality — 2026-07-27

---

## v7.7 — Strategy Intelligence Surfacing & Notification UX — 2026-07-24
Cycle: 2026-07-21__release-v7.7
Verified: Verified
Verification report: claude/cycles/2026-07-21__release-v7.7/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-04 strategy-version performance comparison view — win rate/average R/compliance rate before vs. after a `strategy_rules.md` version change, date-range attribution via the spec's own Change Log | `docs/specs/frontend/pages/strategy_benchmark.md`; `docs/design/2026-07-21__release-v7.7/si04-strategy-version-comparison/ux_spec.md`; `docs/specs/api_contracts/strategy_version_comparison_contract.md` |
| EPIC-02 | Remove nav duplication and unify digest/notification concepts — dedup nav entries, Weekly Digest grouping, alert-count deep-links to the alert feed | `docs/specs/frontend/pages/navigation.md`; `docs/specs/frontend/pages/notifications.md`; `docs/specs/frontend/pages/weekly_digest.md`; `docs/specs/api_contracts/alerts_endpoints.md` |
| EPIC-03 | Staging check and fix AiDailyBriefing light-theme contrast — light-mode class pairs added, re-verified in both themes | `docs/specs/frontend/pages/dashboard.md`; `docs/design/2026-07-21__release-v7.7/ai-daily-briefing-light-theme/ux_spec.md` |
| EPIC-04 | Shared "standing alert" component distinct from transient toast — enabler for alert-style UI across the app | `docs/design/2026-07-21__release-v7.7/standing-alert-component/ux_spec.md`; `docs/specs/frontend/design_system.md` |
| EPIC-05 | SI-02 nudge feasibility investigation — reviewed whether an in-app nudge would accelerate the SI-02 trade-count gate; recommendation-only, no shipped UI | `docs/product/decisions/si02-nudge-feasibility-assessment.md` |
| EPIC-06 | Response validation added to `daily-snapshot.yml` curl calls — `--fail`/`--show-error` scoped to the 3 business curl calls | `.github/workflows/daily-snapshot.yml` |
| EPIC-07 | Retroactive §13 determinism/automation compliance review against shipped PT-04 (Setup Quality Score) — PASS, deterministic/read-only/display-only confirmed | `docs/product/decisions/decisions--2026-07-21__release-v7.7--PT-04-section13-review.md`; `docs/specs/api_contracts/trade_plan_endpoints.md`; `claude/strategy/strategy_rules.md` |
| EPIC-08 | Automated regression test for numpy-scalar handling in `create_rebalance_exit_signal` — falsifiability independently confirmed; cross-file pytest test-isolation bug found and fixed during implementation | `tests/test_rebalance_exit_signal_numpy_regression.py` |
| EPIC-09 | Nightly backtest job double-run/retry idempotency audit — no correctness gap found (full-replace transaction already retry-safe); concurrency guard added to `backtest.yml` as defense-in-depth | `docs/product/decisions/decisions--2026-07-21__release-v7.7--nightly-backtest-idempotency-audit.md`; `.github/workflows/backtest.yml`; `backend/database.py` |
| EPIC-10 | Monitoring/alerting for nightly backtest failures or anomalies — Telegram alert step with graceful degradation pending repo-secrets configuration | `.github/workflows/backtest.yml` |
| EPIC-11 | CI lint gate comparing router-decorator count against the `SystemStatus.js` fallback — corrected a pre-existing drift (fallback 103 → AST-verified 99 post-merge) | `.github/workflows/quality_gate.yml` |

### Deviations accepted
None. Every `done` ST item's deviation check found no divergence between implementation and canonical spec (see `sprint_close.md` "Deviations Filed This Sprint").

### Tech backlog items shipped
- [ST-01] [U] BLG-FEAT-75: SI-04 strategy-version performance comparison view
- [ST-02] [U] BLG-FE-114: Consolidate notification/digest surfaces
- [ST-03] [U] BLG-FE-113: Confirm/fix AiDailyBriefing light-theme rendering
- [ST-04] [U] BLG-FE-120: Shared toast/notification primitive for alert-style UI
- [ST-05] [P] BLG-FEAT-80: Investigate a UX nudge to accelerate the SI-02 trade-count gate
- [ST-06] [D] BLG-OPS-108: Add response validation to daily-snapshot.yml curl calls
- [ST-07] [D] BLG-GOV-28: PT-04 §13 compliance review (retroactive)
- [ST-08] [D] BLG-QA-104: numpy-scalar regression coverage for create_rebalance_exit_signal
- [ST-09] [D] BLG-BE-63: Nightly backtest job idempotency check
- [ST-10] [D] BLG-OPS-110: Nightly backtest job monitoring/alerting
- [ST-11] [D] BLG-QA-102: Automate endpoint-count drift check (CLAUDE.md §2)

Sign-off: Product Owner — 2026-07-24
QA sign-off: Director of Quality — 2026-07-24

---

## v7.6 — PDF / Print-Friendly Export — 2026-07-20
Cycle: 2026-07-20__release-v7.6
Verified: Verified
Verification report: claude/cycles/2026-07-20__release-v7.6/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Print/PDF export action for WeeklyDigest and TradePlan — client-side `window.print()` + global print stylesheet | `docs/specs/frontend/pages/weekly_digest.md`#4; `docs/specs/frontend/pages/trade_plan.md`#7c |
| EPIC-02 | Regression suite baseline update for BLG-FE-115–119 interaction surfaces | `docs/qa/regression_test_suite_baseline.md`#Part 2 |
| EPIC-03 | Reconcile realised P&L export against trade_plan closes — structural closure-state reconciliation | `docs/specs/pnl_export_reconciliation.md` |
| EPIC-04 | Standardise error-response envelope across all routers — audit of 79 endpoints, non-conformance findings filed | `docs/specs/api_contracts/backend_engineering_patterns.md`#Error-response envelope conformance |
| EPIC-05 | Shared mock payload fixture library derived from `openapi.yaml` | `tests/e2e/fixtures/api-mocks.js` |
| EPIC-06 | Audit nightly batch jobs for idempotency risk — 4 jobs confirmed idempotent | `docs/specs/nightly_batch_idempotency_audit.md` |
| EPIC-07 | Claude API monthly cost summary — reframed from a two-provider (Gemini + Claude) premise to single-provider after the original premise was found factually incorrect | `docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md`#7; `docs/specs/frontend/pages/settings.md`#6; `docs/specs/api_contracts/ai_endpoints.md`#GET /ai/monthly-cost |
| EPIC-08 | Standing regression suite for ticker/market input sanitisation, consolidating BLG-SEC-01/02 coverage | `tests/test_ticker_market_sanitization_regression.py` |

### Deviations accepted
None. (EPIC-07's UX spec premise correction is documented as a design-artefact addendum, not a code-vs-spec deviation — see `docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md` v1.1 §7.)

### Tech backlog items shipped
- [ST-01] [U] BLG-FE-119: Print/PDF export action for WeeklyDigest and TradePlan
- [ST-02] [D] BLG-QA-112: Regression suite baseline update for BLG-FE-115–119 interaction surfaces
- [ST-03] [D] BLG-FEAT-79: Reconcile realised P&L export against trade_plan closes
- [ST-04] [D] BLG-BE-65: Standardise error-response envelope across all routers
- [ST-05] [D] BLG-QA-114: Shared mock payload fixture library from openapi.yaml
- [ST-06] [D] BLG-BE-62: Audit nightly batch jobs for idempotency risk
- [ST-07] [U] BLG-FEAT-77: Claude API monthly cost summary (single-provider reframe)
- [ST-08] [D] BLG-QA-69: Standing regression suite for ticker/market input sanitisation

Sign-off: Product Owner — 2026-07-20
QA sign-off: Director of Quality — 2026-07-20

---

## v7.5 — UI Feature Expansion Continuation — 2026-07-20
Cycle: 2026-07-17__release-v7.5
Verified: Verified
Verification report: claude/cycles/2026-07-17__release-v7.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Global Cmd/Ctrl-K command palette — cross-page ticker/entity search and page navigation, wired to the existing shadcn `Command` primitive | `docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md`; `docs/specs/frontend/pages/navigation.md` |
| EPIC-02 | User-defined custom price alerts — data model, UI, and delivery integration via the existing notification channel | `docs/design/2026-07-17__release-v7.5/custom-price-alerts/ux_spec.md`; `docs/specs/frontend/pages/notifications.md`; `docs/specs/api_contracts/alerts_endpoints.md`; `docs/specs/data_model.md` |
| EPIC-03 | Bulk actions toolbar — multi-select and bulk tag/archive/remove on Watchlist and Trade Plans | `docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md`; `docs/specs/frontend/pages/watchlist.md`; `docs/specs/frontend/pages/trade_plan.md`; `docs/specs/api_contracts/watchlist_endpoints.md`; `docs/specs/api_contracts/trade_plan_endpoints.md` |
| EPIC-04 | Named saved filter presets and a calendar view on Trade History | `docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md`; `docs/specs/frontend/pages/trade_history.md`; `docs/specs/api_contracts/saved_filters_endpoints.md`; `docs/specs/api_contracts/reports_endpoints.md` |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] [U] BLG-FE-115: Global command palette / cross-page search
- [ST-02] [U] BLG-FE-116: User-defined custom price alerts
- [ST-03] [U] BLG-FE-117: Bulk actions on list/table views
- [ST-04] [U] BLG-FE-118: Saved filter views and calendar view

Sign-off: Product Owner — 2026-07-20
QA sign-off: Director of Quality — 2026-07-20

---

## v7.4 — UI Feature Expansion Readiness Pass — 2026-07-17
Cycle: 2026-07-17__release-v7.4
Verified: Verified
Verification report: claude/cycles/2026-07-17__release-v7.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Consolidated v7.4 UI-feature readiness pass — dependency pre-flight (`cmdk`, `react-day-picker` added to `package.json`), UX specs for the saved-filters empty state and bulk-actions confirmation/undo-window modal, command-palette keyboard-navigation design review, Playwright visual-regression baseline scope, command-palette analytics event schema, regression-suite CI tagging scheme. Readiness pass only — no shippable UI this release. | `docs/specs/blg_spec_95_v7_4_ui_readiness_pass.md` |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] [P] BLG-SPEC-95: v7.4 UI-heavy release readiness bundle (dependency pre-flight, UX specs, design review, Playwright/analytics/regression-tag coverage for BLG-FE-115/116/117/118)

Sign-off: Product Owner — 2026-07-17
QA sign-off: Director of Quality — 2026-07-17

---

## v7.3 — Dashboard/Trade-Plan/Navigation UX Continuation — 2026-07-16
Cycle: 2026-07-16__release-v7.3
Verified: Verified
Verification report: claude/cycles/2026-07-16__release-v7.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Trade-plan-to-execution linkage UX ("Start Trade from Plan"); dashboard empty/first-run state coverage; dashboard briefing visual hierarchy — all three carried forward from v7.2 | `src/pages/TradePlan.js`, `src/pages/TradePlans.js`, `src/pages/TradeEntry.js`, `src/pages/DashboardHome.js`, `src/pages/Watchlist.js` |
| EPIC-02 | Command Palette (`BLG-FE-115`) pre-implementation spec, prompt template & discoverability/adoption pass — searchable entity index scope, keyboard interaction contract, Base44 prompt template, discoverability plan, adoption metrics; flagged `cmdk` missing from `package.json` | `docs/specs/blg_fe_115_pre_implementation_readiness_pass.md`; `docs/specs/frontend/base44_prompt_template_library.md` |
| EPIC-03 | Custom Price Alerts (`BLG-FE-116`) pre-implementation readiness pass — new `price_alerts` schema designed; evaluation extension to existing alert-evaluation cron; **§13 pre-check PASSED** (RISK-03 cleared) | `docs/specs/blg_fe_116_pre_implementation_readiness_pass.md` |
| EPIC-04 | Bulk Actions (`BLG-FE-117`) pre-implementation readiness pass — per-entity batch-mutation endpoint pattern designed with explicit partial-failure response shape; Base44 prompt template added; **§13 pre-check PASSED** (RISK-04 cleared) | `docs/specs/blg_fe_117_pre_implementation_readiness_pass.md`; `docs/specs/frontend/base44_prompt_template_library.md` |
| EPIC-05 | Saved Filters & Calendar View (`BLG-FE-118`) pre-implementation spec pass — dedicated `saved_filters` table decided over JSON-column-on-settings; calendar view spec authored reusing `GET /reports/monthly-pnl`'s date-grouping logic; flagged `react-day-picker` missing from `package.json` | `docs/specs/blg_fe_118_pre_implementation_readiness_pass.md` |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] [U] BLG-FE-109: Trade-plan-to-execution linkage UX ("Start Trade from Plan")
- [ST-02] [U] BLG-FE-110: Dashboard empty/first-run state coverage
- [ST-03] [U] BLG-FE-111: Dashboard briefing visual hierarchy
- [ST-04] [P] BLG-SPEC-91: Command Palette (`BLG-FE-115`) pre-implementation readiness pass
- [ST-05] [P] BLG-SPEC-92: Custom Price Alerts (`BLG-FE-116`) pre-implementation readiness pass
- [ST-06] [P] BLG-SPEC-93: Bulk Actions (`BLG-FE-117`) pre-implementation readiness pass
- [ST-07] [P] BLG-SPEC-94: Saved Filters & Calendar View (`BLG-FE-118`) pre-implementation spec pass

Sign-off: Product Owner — 2026-07-16
QA sign-off: Director of Quality — 2026-07-16

---

## v7.2 — Dashboard & Trade-Plan UX Hardening — 2026-07-15
Cycle: 2026-07-15__release-v7.2
Verified: Verified
Verification report: claude/cycles/2026-07-15__release-v7.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Mobile responsiveness baseline assessment — severity-ranked findings report covering positions, screener, trade plan form, trade entry, and Red Flag Journal; Arc 5 gate explicitly noted as not-yet-met, proceeding on recorded Product Owner priority override | `docs/specs/frontend/mobile_responsiveness_baseline_assessment_v7.2.md` |
| EPIC-02 | `BLG-FE-109` ("Start Trade from Plan") pre-implementation readiness pass — contract pre-stage, data model, auth boundary, §13 boundary, `TradeEntry.js` validation-risk, and SI-02 metric review, clearing the way for `BLG-FE-109` to enter sprint planning | `docs/specs/blg_fe_109_pre_implementation_readiness_pass.md` |
| EPIC-03 | `BLG-FE-110`/`BLG-FE-111` pre-implementation spec & instrumentation pass — `DataState` empty-state pattern and dashboard card-hierarchy treatment formalised in `design_system.md`, new Base44 prompt template library added | `docs/specs/blg_fe_110_111_pre_implementation_spec_instrumentation_pass.md`; `docs/specs/frontend/design_system.md` (v1.0→v1.1); `docs/specs/frontend/base44_prompt_template_library.md` (new) |
| EPIC-04 | Notification/digest surface consolidation review — audit of `Notifications.js`, `NotificationsHistory.js`, `NotificationPreferences.js`, `WeeklyDigest.js` navigation/content overlap; consolidation recommended, implementation scoped as a follow-up | `docs/specs/frontend/notification_surface_consolidation_review_v7.2.md` |
| EPIC-05 | Combined design review + shared Playwright suite plan for `BLG-FE-109/110/111/112` — one design review session and one shared spec file (`tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js`, named not yet populated) instead of four independent passes | `docs/specs/frontend/blg_qa_111_combined_design_review_shared_playwright_plan.md` |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] [D] BLG-FE-55: Mobile responsiveness baseline assessment
- [ST-02] [P] BLG-SPEC-89: `BLG-FE-109` pre-implementation readiness pass
- [ST-04] [P] BLG-SPEC-90: `BLG-FE-110`/`BLG-FE-111` pre-implementation spec & instrumentation pass
- [ST-07] [D] BLG-FE-112: Notification/digest surface consolidation review
- [ST-08] [P] BLG-QA-111: Combined design review + shared Playwright suite plan

Sign-off: Product Owner — 2026-07-15
QA sign-off: Director of Quality — 2026-07-15

---

## v7.1 — Nightly Backtest Data Integrity — 2026-07-14
Cycle: 2026-07-14__release-v7.1
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-07-14__release-v7.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Nightly backtest data-integrity fixes: ticker eligibility now gated on `ticker_universe.created_at` (point-in-time integrity — a newly-added ticker can no longer retroactively change historical trade selection/sizing); `total_pnl_gbp` night-to-night non-reproducibility addressed by wiring the existing drift-check output into an actual alert (threshold £50, distinct exit code, greppable log line) | `production_strategy.py`; `import_backtest.py`; `tests/test_production_strategy.py` (spec_reference_not_applicable — bug fixes, no prior canonical spec) |
| EPIC-02 | Table View RISK OFF badge brought into spec compliance (`#1E40AF`, "RISK OFF" label, icon removed), closing a v7.0 carryover deviation | `docs/specs/frontend/pages/positions.md#Alerts Column`; `#Known Deviations` |
| EPIC-03 | v7.0 post-ship hardening pass: position review-cadence nudge IDOR fix + NULL/backfill verification (backend), frontend/QA polish confirmed pre-met; realized/unrealized P&L split spec, metrics, and reconciliation hardening; tax-year P&L CSV export spec and test hardening | `docs/specs/frontend/pages/positions.md#Last Reviewed Column`; `#Position Lifecycle State Badge`; `docs/specs/metrics_definitions.md#Realized / Unrealized P&L Split`; `docs/specs/frontend/pages/reports.md#Unrealised P&L Card`; `#Known Deviations`; `docs/reference/openapi.yaml`; `docs/specs/api_contracts/reports_endpoints.md#Response (200 — CSV, format=csv)`; `docs/specs/api_contracts/backend_engineering_patterns.md#CSV/export response-body pattern`; `docs/testing/tax_year_csv_export_scenarios.md` |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-REPORTS-ST06-01 | P3 | Reports' `estimated_unrealised_pnl` reads a nightly-job snapshot of `positions.pnl` while the Positions page computes live, causing the two pages to show different unrealised figures at the same moment (verified: −£126.25 vs −£115.06, £11.19 gap). Documentation/verification scope only; not fixed in this story. Target resolution: TBD (BLG-SPEC-87). | PO |

*(1 P2 deviation, DEV-EPIC01-ST05-01, carried from v7.0 was resolved and closed this sprint by ST-03 — not a fresh acceptance.)*

### Tech backlog items shipped
- [ST-01] [D] BLG-BE-59: Gate nightly backtest ticker eligibility on `ticker_universe.created_at`
- [ST-02] [D] BLG-BE-60: Fix nightly backtest `total_pnl_gbp` non-reproducibility
- [ST-03] [U] BLG-FE-107: Table View RISK OFF badge colour/label spec compliance
- [ST-04] [D] BLG-BE-61: Position review-cadence nudge — backend/data-integrity hardening pass
- [ST-05] [D] BLG-QA-106: Position review-cadence nudge — frontend/QA polish pass (pre-met)
- [ST-06] [D] BLG-SPEC-83: Realized/unrealized P&L split — spec & metrics hardening pass
- [ST-07] [D] BLG-SPEC-84: Tax-year P&L CSV export — spec & test hardening pass

Sign-off: Product Owner — 2026-07-14
QA sign-off: Director of Quality — 2026-07-14

---

## v7.0 — Positions Grid View Parity, Carryover Fixes & Feature Enhancements — 2026-07-13
Cycle: 2026-07-12__release-v7.0
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-07-12__release-v7.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Positions Grid View Parity: RISK OFF badge and trailing-stop value + breach indicator brought to parity with Table View in `PositionCard.js`; GAP RISK/RISK OFF combined-badge stacking confirmed visually distinguishable; dedicated Grid View badge-parity Playwright coverage (9 scenarios); Grid View badge-placement subsection added to canonical spec | `docs/specs/frontend/pages/positions.md#Alerts Column`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`; `docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md`; `tests/e2e/epic01-v70-grid-badge-parity.spec.js` |
| EPIC-02 | v6.9 Carryover Fixes & Reconciliation: Reports.js Tax Year P&L tab spec reconciled to actual behaviour; `trailing_stop_action_rate` metric instrumentation wired into `GET /positions/{id}/stop-trail`; Dashboard/StrategyBenchmark light-theme heading contrast fixed; Positions Table View breach badge brought into spec colour/label compliance; Gate Progress Indicator copy divergence resolved; `GET /ai/claude-audit-log` endpoint/date-range filters added; Sector Concentration heat map now joins `ticker_universe` instead of showing positions as "Unclassified" | `docs/specs/frontend/pages/reports.md`; `docs/specs/metrics_definitions.md#Trailing Stop Action Rate`; `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`; `docs/specs/frontend/pages/dashboard.md#6`; `docs/specs/api_contracts/ai_endpoints.md`; `docs/specs/frontend/pages/risk_dashboard.md#8a. Component: Sector Concentration Heat Map` |
| EPIC-03 | User-Facing Feature Enhancements: tax-year P&L CSV export (fixed pre-existing button-order spec deviation in the process); realized vs. unrealized gain distinction in Monthly P&L view; position review-cadence nudge (`last_reviewed_at` tracking + `PATCH /positions/{id}/mark-reviewed`) | `docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md`; `docs/specs/frontend/pages/reports.md`; `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`; `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md`; `docs/specs/frontend/pages/positions.md#Last Reviewed Column` |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-EPIC01-ST05-01 | P2 | Positions Table View RISK OFF badge colour/label diverges from canonical spec (`#1E40AF`/"RISK OFF" specified; amber/"Risk-Off" shipped) — pre-existing since v6.2, unrelated to this sprint's changes. Target resolution: v7.1 (BLG-FE-107). | PO + DoQ |

### Tech backlog items shipped
- [ST-01] [D] BLG-SPEC-80: `positions.md` Grid View badge placement subsection
- [ST-02] [U] BLG-FE-102: Positions Grid View missing RISK OFF badge
- [ST-03] [U] BLG-FE-97: Positions Grid View missing trailing-stop value and breach indicator
- [ST-04] [D] BLG-QA-95: Positions Grid View badge parity Playwright coverage
- [ST-05] [D] BLG-FE-104: GAP RISK / RISK OFF combined-badge visual differentiation review
- [ST-06] [D] BLG-SPEC-71: Reports.js Tax Year P&L tab spec reconciliation
- [ST-07] [D] BLG-BE-50: Instrument trailing-stop recommendation capture for `trailing_stop_action_rate` metric
- [ST-08] [U] BLG-FE-95: Dashboard/StrategyBenchmark page-title light-theme contrast gap
- [ST-09] [U] BLG-FE-96: Positions Table View breach badge does not match approved spec colour/label
- [ST-10] [D] BLG-SPEC-73: Gate Progress Indicator copy divergence
- [ST-11] [D] BLG-BE-51: Add endpoint and date-range filters to `GET /ai/claude-audit-log`
- [ST-12] [U] BLG-BE-38: Sector Concentration: join `ticker_universe` for sector data
- [ST-13] [U] BLG-FEAT-69: Tax-year P&L CSV export
- [ST-14] [U] BLG-FEAT-70: Realized vs. unrealized gain distinction in monthly P&L
- [ST-15] [U] BLG-FEAT-68: Position review cadence nudge

Sign-off: Product Owner — 2026-07-13
QA sign-off: Director of Quality — 2026-07-13

---

## v6.9 — On-Demand Compliance Recheck & Overnight Gap Risk Flag — 2026-07-10
Cycle: 2026-07-10__release-v6.9
Verified: Verified
Verification report: claude/cycles/2026-07-10__release-v6.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | On-demand pre-entry (SI-01) compliance recheck for open positions — `GET /positions/{position_id}/compliance-recheck` re-applies the existing 5 SI-01 rule checks against current position state; `ComplianceRecheckModal.js` on Positions Table View Actions column and Position Card Grid View footer (BLG-FEAT-64, mandatory Product Value Alert pull-forward) | `docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md`; `docs/specs/frontend/pages/positions.md#Compliance Recheck Panel`; `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/compliance-recheck` |
| EPIC-02 | Overnight/weekend gap risk flag for open positions — `GET /positions/{position_id}/gap-risk` combines the earnings calendar with historical OHLCV gap statistics; new GAP RISK badge in a new Alerts table column (which also now correctly hosts the pre-existing RISK OFF badge, resolving a since-v6.2 documented-but-unbuilt gap) and near the ticker in Grid View (BLG-FEAT-65, mandatory Product Value Alert pull-forward) | `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md`; `docs/specs/frontend/pages/positions.md#Gap Risk Badge`; `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk` |

### Deviations accepted
None — no deviations filed this sprint. Two pre-authorised implementation notes (not deviations) are recorded in `verification_report.md §4`: ST-02's dedicated gap-risk endpoint (pre-authorised by story notes) and ST-01's sector-concentration formula adaptation to exclude the rechecked position from its own baseline sum.

### Tech backlog items shipped
- [ST-01] [U] BLG-FEAT-64: On-demand pre-entry rule recheck for open positions — mandatory Product Value Alert pull-forward
- [ST-02] [U] BLG-FEAT-65: Overnight/weekend gap risk flag for open positions — mandatory Product Value Alert pull-forward

Sign-off: Product Owner — 2026-07-10
QA sign-off: Director of Quality — 2026-07-10

---

## v6.8 — Production Correctness, Value Pull-Forward & Debt Clearance — 2026-07-09
Cycle: 2026-07-08__release-v6.8
Verified: Verified
Verification report: claude/cycles/2026-07-08__release-v6.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Production Correctness, Security & Infrastructure: `trade_plans.position_id` linkage bug root-caused (workflow gap, not a code defect) and forward-fixed via backend auto-link in `add_position()` — no historical backfill (BLG-BE-46); SQL injection defense-in-depth — `SIGNAL_UPDATABLE_COLUMNS` allowlist added to `database.update_signal()` plus `PATCH /signals/{id}` pre-validation (BLG-SEC-08); manual security review of all 300 production signal records for anomalous ticker/market values — PASS, no anomalies found (BLG-SEC-07); application `X-API-Key` formally registered in the security register, closing a 2-cycle-recurring credential gap and enabling direct production reads for governed routines (BLG-OPS-99) | `docs/security/signal_anomaly_review_2026-07-09.md`; `docs/security/api_key_security_register.md#6-application-x-api-key` |
| EPIC-02 | Product Value Pull-Forward (mandatory): trade tagging and tag-based performance filtering — `trade_tags` on `trade_plans`, Tag Editor on `TradePlan.js`, `GET /analytics/tag-performance`, `TradePlanTagFilter.js` on `PerformanceAnalytics.js` (BLG-FEAT-52); SI-02 gate visibility indicator — collapsible "SI-02 Gate Status" section on `Reports.js` Tax Year P&L tab showing total vs linked closed-trade counts and 3 MET/NOT MET gate condition badges, sourced live from `GET /trades`, `GET /trade-plans`, `GET /analytics/arc5-compliance` (BLG-FEAT-71) | `docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md`; `docs/specs/frontend/pages/trade_plan.md#5c`; `docs/specs/frontend/pages/analytics.md#14a`; `docs/specs/api_contracts/trade_plan_endpoints.md`; `docs/specs/api_contracts/analytics_endpoints.md`; `docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md`; `docs/specs/frontend/pages/reports.md#SI-02 Gate Status` |
| EPIC-03 | Spec & Governance Debt Clearance: dashboard visual hierarchy review (no discrepancy found, contrast follow-up BLG-FE-95 filed; BLG-SPEC-58); R-multiple cross-currency normalization spec — confirmed dimensionless by construction, no FX conversion required (BLG-SPEC-59); trailing stop visual indicator spec reconciliation — 2 implementation-vs-spec deviations found and filed as BLG-FE-96/97 (BLG-SPEC-60); trailing stop effectiveness metric definition — `trailing_stop_action_rate`, instrumentation follow-up filed BLG-BE-50 (BLG-SPEC-61); 11 of 12 dark Playwright spec files fixed (`route.fallback()` ordering fix, mock/URL corrections), 1 file deleted as architecturally incompatible, 2 genuine production bugs found and fixed along the way — `sonner` Toaster never mounted app-wide, `Arc5ComplianceSection.js` heading mismatch (BLG-QA-64); CI inline OpenAPI drift detection job added to `quality_gate.yml` (BLG-GOV-134); Anthropic API token usage/cost logging confirmed already shipped, pre-met (BLG-OPS-74); `Watchlist.js` decomposed to ESLint compliance — 3 hooks + 6 components, zero functional change (BLG-FE-77); v5.1–v5.4 endpoint baseline extension confirmed already closed, pre-met (BLG-OPS-61); Playwright test authoring standard extracted from `execution_prompt.md` to `shared_standards.md` §18 (BLG-GOV-123); system threat model document produced, 2 new gaps filed (BLG-SEC-12/13), Telegram credential added to security register (BLG-OPS-71) | `docs/specs/qa/dashboard_visual_hierarchy_review_v6.8.md`; `docs/specs/metrics_definitions.md#Cross-Currency Normalization`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`; `docs/specs/qa/trailing_stop_visual_indicator_review_v6.8.md`; `docs/specs/metrics_definitions.md#Trailing Stop Action Rate`; `playwright.config.js`; `.github/workflows/quality_gate.yml#api_baseline_drift`; `docs/specs/api_contracts/ai_endpoints.md#GET /ai/claude-audit-log`; `src/pages/Watchlist.js`; `docs/ops/api_performance_baseline.md` §17, §19; `claude/system/shared_standards.md#18`; `docs/security/threat_model.md` |

### Deviations accepted
None — all 17 ST items met their acceptance criteria without divergence from canonical spec intent. 10 follow-up backlog items were filed for pre-existing or descoped gaps found along the way (see `verification_report.md §4`).

### Tech backlog items shipped
- [ST-01] [D] BLG-BE-46: `trade_plans.position_id` never populated in production — root cause = workflow gap, forward-fixed via backend auto-link, no historical backfill
- [ST-02] [D] BLG-SEC-08: Unvalidated dict keys used as SQL column names in `database.update_signal()` — allowlist defense added
- [ST-03] [D] BLG-SEC-07: Manual review of existing signals for anomalous ticker/market values — PASS, no anomalies found
- [ST-04] [D] BLG-OPS-99: Application X-API-Key formally registered in security register — closes 2-cycle-recurring credential gap
- [ST-05] [U] BLG-FEAT-52: Trade tagging and tag-based performance filtering — mandatory Product Value Alert pull-forward
- [ST-06] [U] BLG-FEAT-71: SI-02 gate visibility indicator, Reports page — mandatory Product Value Alert pull-forward
- [ST-07] [D] BLG-SPEC-58: Dashboard homepage visual hierarchy review post-v6.2 — no discrepancy found, contrast follow-up filed
- [ST-08] [D] BLG-SPEC-59: R-multiple cross-currency normalization specification
- [ST-09] [D] BLG-SPEC-60: Trailing stop visual indicator frontend specification — reconciliation review, 2 deviations found and filed
- [ST-10] [D] BLG-SPEC-61: Trailing stop effectiveness metric definition
- [ST-11] [D] BLG-QA-64: Fix 12 dark spec files surfaced by Playwright glob discovery — 2 production bugs found and fixed
- [ST-12] [G] BLG-GOV-134: CI inline OpenAPI drift detection for `api_performance_baseline.md`
- [ST-13] [D] BLG-OPS-74: Log Anthropic API token usage and cost per morning briefing call (pre-met)
- [ST-14] [D] BLG-FE-77: Refactor `Watchlist.js` to ESLint compliance
- [ST-15] [D] BLG-OPS-61: v5.1–v5.4 endpoint baseline extension (pre-met)
- [ST-16] [G] BLG-GOV-123: Extract Playwright test standard from `execution_prompt.md` to `shared_standards.md`
- [ST-17] [D] BLG-OPS-71: System threat model document

Sign-off: Product Owner — 2026-07-09
QA sign-off: Director of Quality — 2026-07-09

---

## v6.7 — Contrast Remediation & Governance Hardening — 2026-07-08
Cycle: 2026-07-06__release-v6.7
Verified: Verified
Verification report: claude/cycles/2026-07-06__release-v6.7/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | UX & Accessibility Contrast Remediation: systematic dark-theme secondary-text contrast fix — bare `text-slate-500`→`text-slate-400` across 226 in-scope instances (59 files) + 4 `src/Layout.js` instances found at DoQ review, 33 icon-only instances correctly excluded (BLG-FE-87); light-theme companion pairing — `text-slate-600 dark:text-slate-400` added to 697 in-scope bare `text-slate-400` instances (101 files), plus 1 broken pre-existing pairing fixed and the Dashboard Advisory Label exception applied (BLG-FE-88); canonical secondary-text design token locked into `design_system.md` (BLG-FE-89) | `docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md`; `docs/specs/frontend/pages/positions.md` v2.0; `docs/specs/frontend/pages/dashboard.md` v2.6; `docs/specs/frontend/pages/reflections.md` v0.2; `docs/specs/frontend/design_system.md` v1.0 |
| EPIC-02 | Governance Process Hardening — full AUD-2026-07-06 follow-through: `.claude/skills/` write-scope authority granted to Head of Specs Team + commit-check diff-verification patch applied, closing the 3-cycle-carried `ESC-CLOSE-20260706-01` escalation (BLG-GOV-167); Canonical Append-Only Verification Procedure extracted and applied to all 4 append-only governance logs (`execution_escalations.md`, `verification_escalations.md`, `delegation_log.md`, plus the existing `decision_log.md` pattern) (BLG-GOV-168); `audit.py` SLA block updated to require same-session commit of audit reports (BLG-GOV-169); Delivery Verification STEP 6 status-line update documented as expected, routine behaviour (BLG-GOV-170) | `claude/system/shared_standards.md`; `.claude/skills/commit-check/SKILL.md`; `claude/system/prompt_change_log.md`; `claude/system/release_planning_prompt.md`; `claude/system/execution_prompt.md`; `claude/system/delivery_verification_prompt.md`; `claude/audit.py`; `claude/system/OPERATIONAL_GUIDE.md` |

### Deviations accepted
None — all 7 ST items met their acceptance criteria without divergence from canonical specs.

### Tech backlog items shipped
- [ST-01] [U] BLG-FE-87: Dark-theme secondary-text contrast fix — 226+4 instances remediated to WCAG-AA (5.71:1), Playwright coverage added
- [ST-02] [U] BLG-FE-88: Light-theme secondary-text contrast fix — 697 instances paired to WCAG-AA (6.92:1), Playwright coverage extended
- [ST-03] [D] BLG-FE-89: Shared secondary-text design token — canonical token locked into `design_system.md`, closing the third recurrence of this defect class
- [ST-04] [G] BLG-GOV-167: `.claude/skills/` write-scope authority + commit-check diff-verification patch — closes 3-cycle-carried escalation
- [ST-05] [G] BLG-GOV-168: Structural guard extended to 4 append-only governance logs
- [ST-06] [G] BLG-GOV-169: `audit.py` same-session commit SLA
- [ST-07] [G] BLG-GOV-170: Delivery Verification STEP 6 status-line documentation

Sign-off: Product Owner — 2026-07-08
QA sign-off: Director of Quality — 2026-07-08

---

## v6.6 — UX & QA Debt Clearance — 2026-07-06
Cycle: 2026-07-04__release-v6.6
Verified: Verified
Verification report: claude/cycles/2026-07-04__release-v6.6/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | UX & Accessibility Debt: systematic class-based WCAG-AA contrast audit across `text-slate-400/500` secondary-text usages app-wide (764 instances, 102 files) — findings-only (Design Not Applicable), 3 follow-up items filed (BLG-FE-87 P1, BLG-FE-88 P2, BLG-FE-89 P3) (BLG-FE-82); Red Flag Journal filter state (event type, ticker, since-date) now persists across reload via a versioned localStorage envelope, with graceful stale/corrupt-state recovery (BLG-FE-40) | `claude/cycles/2026-07-04__release-v6.6/contrast_audit_findings.md`; `src/pages/RedFlagJournal.js`; `tests/e2e/red-flag-journal-filter-persistence.spec.js`; `docs/specs/frontend/pages/red_flag_journal.md#Filter Controls` |
| EPIC-02 | QA & Test Infrastructure Debt: all 10 true backlog-ID collisions renumbered with traceability notes, 0 IDs reused; `backlog_management_prompt.md` STEP 4.5 fixed to stop false-flagging compliant §6.1 stub+verbatim archive pairs as duplicates (BLG-QA-72); hand-maintained `_DB_STUB_FUNCTIONS` test-stub list replaced with an AST scan of `backend/` imports (excluding vendored/`.venv` paths), retiring the corresponding CLAUDE.md manual-sync rule (BLG-QA-73) | `claude/backlog/backlog.md`; `claude/backlog/backlog_archive.md`; `claude/system/backlog_management_prompt.md#STEP 4.5 — ID Uniqueness Scan`; `tests/conftest.py` |

### Deviations accepted
None — no spec deviations filed this sprint. One partial-AC outcome (ST-03/AC-03 — 5 of 15 flagged ID groups left unresolved pending Product Owner disposition) is a documented governance-correct boundary, not a deviation; tracked via `BLG-QA-74`.

### Tech backlog items shipped
- [ST-01] [D] BLG-FE-82: Colour contrast audit sweep — systematic WCAG-AA audit app-wide; findings-only (no in-story fix, preserves Design Not Applicable classification); 3 follow-up items filed
- [ST-02] [U] BLG-FE-40: Red Flag Journal filter state persistence — filter state now survives reload via versioned localStorage envelope, with graceful stale-state clearing
- [ST-03] [D] BLG-QA-72: Audit colliding backlog IDs — 10 true collisions renumbered with traceability notes; `backlog_management_prompt.md` STEP 4.5 scan-logic fix
- [ST-04] [D] BLG-QA-73: `database.py` / `_DB_STUB_FUNCTIONS` manual-sync risk — replaced with automated AST-scan derivation; CLAUDE.md rule retired

Sign-off: Product Owner — 2026-07-06
QA sign-off: Director of Quality — 2026-07-06

---

## v6.5 — Audit Debt Clearance, Backlog Debt Clearance & AI Thesis Feedback Loop — 2026-07-03
Cycle: 2026-07-02__release-v6.5
Verified: Verified
Verification report: claude/cycles/2026-07-02__release-v6.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | AUD-2026-07-01 governance/lifecycle debt clearance: `audit.py` config block (PRIOR_AUDIT_ID/PRIOR_AUDIT_OPEN_ITEMS/PRIOR_SCORES/COMPLETED_CYCLES) brought in sync with `.claude_current_state.json` (BLG-GOV-157); README.md hygiene sweep — all 13 governed routines listed, broken §2 path corrected, staleness refreshed, `pmo_lead.md` header bolded (BLG-GOV-158); OPERATIONAL_GUIDE/prompt version-sync drift resolved — header/§14/Change Log consistency, §14 Roadmap Rebalance Prompt row, Metrics owner role name (BLG-GOV-159) | CLAUDE.md#Governance Non-Negotiables; claude/audit.py#FRICTION_LOAD; claude/README.md#4. Organisational Routines; claude/README.md#2. Governing Authorities; claude/system/OPERATIONAL_GUIDE.md#14. Governance Table; claude/agents/metrics_definitions_analytics_owner.md |
| EPIC-02 | Backlog debt clearance: v6.4's `GET /strategy/benchmark/open-positions` endpoint registered in `api_performance_baseline.md` with live production measurement, p50=524.5ms/p95=600.0ms (BLG-OPS-83); Playwright coverage added for Strategy Benchmark Panel 0 (Open Positions) rendering, Market-filter interaction, and API-error state (TEST-GAP-EPIC-03-v64); 3-cycle-stagnant `signals_scenarios.md` review against the v6.0 risk-based sizing model completed — zero stale scenarios found (BLG-QA-61) | docs/ops/api_performance_baseline.md#24; docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md; tests/e2e/strategy-benchmark.spec.js; docs/testing/signals_scenarios.md |
| EPIC-03 | Claude thesis generation user feedback mechanism — thumbs-up/down control gated on `isClaudeDraft`, persisted to `trade_plans.thesis_feedback` (BLG-FE-46); Claude thesis adoption rate metric defined, joined against `gemini_audit_log.plan_id` (BLG-FEAT-41) | docs/design/2026-07-02__release-v6.5/thesis-feedback-mechanism/ux_spec.md; docs/specs/data_model.md#DS-09; tests/e2e/trade-plan.spec.js; docs/specs/metrics_definitions.md#Thesis Adoption Rate |

### Deviations accepted
None — no spec deviations this sprint (2 non-binding implementation notes recorded, not deviations: ST-07's `trade_plans.thesis_feedback` persistence location and ST-08's `gemini_audit_log.plan_id` join-key correction, both against the ux_spec.md's non-binding suggestions).

### Tech backlog items shipped
- [ST-01] BLG-GOV-157: Lifecycle/prompt/state wording and consistency fixes — `audit.py` config block synced to current audit/open-item counts
- [ST-02] BLG-GOV-158: README.md document hygiene sweep — governed routines list, broken path, staleness, header bolding
- [ST-03] BLG-GOV-159: OPERATIONAL_GUIDE/prompt version-sync drift — header/§14/Change Log consistency, Metrics owner role name
- [ST-04] BLG-OPS-83: Add v6.4 endpoint to `api_performance_baseline.md` — live 5-warm-sample production measurement
- [ST-05] TEST-GAP-EPIC-03-v64: Playwright coverage for Strategy Benchmark Panel 0 rendering
- [ST-06] BLG-QA-61: Review `signals_scenarios.md` against ST-01 signal sizing model changes — resolves 3-cycle carry-forward (v6.2→v6.3→v6.4)
- [ST-07] BLG-FE-46: Claude thesis generation user feedback mechanism
- [ST-08] BLG-FEAT-41: Claude thesis adoption rate metric

Sign-off: Product Owner — 2026-07-03
QA sign-off: Director of Quality — 2026-07-03

---

## v6.4 — Audit Remediation, Security Hardening & Strategy Benchmark Enhancement — 2026-07-02
Cycle: 2026-07-02__release-v6.4
Verified: Verified
Verification report: claude/cycles/2026-07-02__release-v6.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Production correctness fix + AI security hardening: signal generation now reads `ticker_universe` instead of the deprecated `tickers` table (BLG-BE-40, P1 fast-track); `context_opts.ticker` sanitised before system prompt injection, including a trailing-newline regex bypass closed during sign-off (BLG-SEC-01); ticker/market strings validated at all 3 signal write paths, including a second write path (`database.update_signal()`) discovered during sign-off review (BLG-SEC-02) | docs/specs/api_contracts/signal_endpoints.md#POST /signals/generate; docs/specs/api_contracts/ticker_universe_api_contract.md; docs/specs/security/ai_injection_risk_assessment.md; docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat |
| EPIC-02 | AUD-2026-07-01 lifecycle-audit remediation: governance version-sync drift corrected (BLG-GOV-150); document hygiene cleanup (BLG-GOV-151); structural reliability gaps closed, including the 2-cycle-carried FI-P4-01/DF-10 `spec_references` convention and FI-P3-02 staging-AC wording ambiguity, plus FI-P3-01 Base44 advisory (BLG-GOV-152); audit/governance process fixes — design gate bypass dual-authority rule, `run audit` dry-run table entry, FRICTION_LOAD formula wording, `scored_initiatives.md` naming (BLG-GOV-153) | claude/system/OPERATIONAL_GUIDE.md; claude/system/roadmap_prompt.md; claude/agents/metrics_definitions_analytics_owner.md; claude/README.md; claude/system/shared_standards.md; claude/system/execution_prompt.md; CLAUDE.md; claude/system/amendment_cycle_prompt.md; claude/agents/base44_frontend_prompt_owner.md; claude/charter/team_charter.md; claude/audit.py |
| EPIC-03 | Strategy Benchmark Open Positions panel + UX/QA polish: Panel 0 (Open Positions) added to Strategy Benchmark page, showing unrealized P&L for open backtest positions (BLG-FEAT-54 — Skill-Silo pull-forward); AI daily briefing and chat widget disclaimer contrast fixed to meet WCAG AA (BLG-UX-01/02); v6.3 endpoints added to API performance baseline, measured against production after staging returned 404 (BLG-OPS-82); Playwright coverage added for AI journal summary error states and the full Strategy Benchmark page — nav, filters, toggle modes, badge colours (TEST-GAP-EPIC-01, TEST-GAP-EPIC-03) | docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md; docs/specs/frontend/pages/strategy_benchmark.md; docs/specs/api_contracts/strategy_benchmark_endpoints.md; docs/reference/openapi.yaml; docs/specs/qa/ai_disclaimer_visibility_assessment.md; docs/ops/api_performance_baseline.md |

### Deviations accepted
None — no spec deviations this sprint.

### Tech backlog items shipped
- [ST-01] BLG-BE-40: Signal generation reads deprecated `tickers` table instead of `ticker_universe` — switched to `ticker_universe_service.get_all_tickers(active_only=True)`
- [ST-02] BLG-SEC-01: Sanitise `context_opts.ticker` before system prompt injection — HTTP 422 on newline/injection characters; trailing-newline regex bypass closed at sign-off
- [ST-03] BLG-SEC-02: Validate ticker/market strings at signal write time — all 3 signal write paths sanitised, including `update_signal()` discovered during review
- [ST-04] BLG-GOV-150: Fix governance version-sync drift — OPERATIONAL_GUIDE.md self-desync, stale §14 roadmap version, metrics owner role-name drift
- [ST-05] BLG-GOV-151: Document hygiene cleanup — README coverage/staleness/broken path, Class 6 header format, agent header bolding
- [ST-06] BLG-GOV-152: Close structural reliability gaps — append-only guard parity, FI-P4-01/DF-10 spec_references convention, FI-P3-02 staging AC protocol, FI-P3-01 Base44 advisory, amendment_lessons sunset contradiction
- [ST-07] BLG-GOV-153: Audit & governance process fixes — design gate bypass authority, run audit dry-run entry, friction_load formula wording, scored_initiatives naming
- [ST-08] BLG-FEAT-54: Add Open Positions panel to Strategy Benchmark page — `backtest_open_positions` table, one-line summary + per-position table
- [ST-09] BLG-UX-01: Improve AI daily briefing disclaimer text contrast — text-slate-500 → text-slate-300
- [ST-10] BLG-UX-02: Improve AI chat widget footer disclaimer contrast and add test coverage — text-slate-600 → text-slate-400; data-testid + Playwright assertion
- [ST-11] BLG-OPS-82: Add v6.3 endpoints to `api_performance_baseline.md` — 3 GET endpoints measured against production
- [ST-12] TEST-GAP-EPIC-01: Playwright coverage for ST-01 observable UI ACs — AI journal summary error states on Trade History tab
- [ST-13] TEST-GAP-EPIC-03: Playwright scenario coverage for Strategy Benchmark page — nav, filters, Panel 1 placeholder, toggle modes/badge colours

Sign-off: Product Owner — 2026-07-02
QA sign-off: Director of Quality — 2026-07-02

---

## v6.3 — Strategy Benchmark, AI Security & Quality Infrastructure — 2026-06-30
Cycle: 2026-06-26__release-v6.3
Verified: Verified
Verification report: claude/cycles/2026-06-26__release-v6.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | AI Security & Quality Hardening: AI journal summary fixed (data.message stored and displayed; logger.error added to ai_service.py); R-multiple display fixed on Reflection page (field name correction base44Client.js net_r_multiple → r_multiple; N/A display for no-stop trades); per-endpoint rate limiting hardened (POST /ai/daily-briefing 10 req/min/IP; POST /ai/chat 30 req/min/IP; 429+Retry-After); AI response injection risk assessment (5 inputs assessed, 3 accepted, 2 open — BLG-SEC-01/02 filed); AI disclaimer visibility assessment (§13 amber badge PASS; WCAG contrast gaps filed BLG-UX-01/02); API contract review checklist (11-item checklist authored, both AI endpoints ALL PASS) | docs/specs/api_contracts/ai_endpoints.md v1.5; docs/specs/security/ai_injection_risk_assessment.md; docs/specs/qa/ai_disclaimer_visibility_assessment.md; docs/specs/api_contracts/ai_advisory_contract_checklist.md |
| EPIC-02 | Test Infrastructure & Quality Coverage: 21 nightly computation CI simulation tests passing (7 trailing stop, 5 rebalance exit, 9 inv-vol sizing); strategy signal regression test specification authored (scenario coverage, float tolerance, fixture maintenance procedure); 8 AI chat response schema validation tests passing; §13 boundary test suite (11 scenarios across D1–D4 dimensions for both AI advisory endpoints) | tests/test_nightly_computations.py; tests/fixtures/nightly_portfolio_state.json; docs/specs/qa/strategy_signal_regression_spec.md; tests/test_ai_chat_schema.py; docs/specs/qa/ai_s13_boundary_test_suite.md |
| EPIC-03 | Strategy Benchmark & UX Enhancement: Strategy Benchmark page live (DB schema backtest_trades + backtest_yearly_performance; POST /strategy/benchmark/import + GET summary + GET trades; import_backtest.py companion script; full page with 3 panels, sticky filters, toggle modes, exit reason badges); Morning briefing progressive disclosure (3 collapsible sections, localStorage persistence, SC-PD Playwright coverage); GET /health/scheduler endpoint (architecture review + 3-job tracking); live AI endpoint latency baseline (daily-briefing p50=10,296ms p95=11,152ms; chat p50=6,258ms p95=7,035ms); Render deployment rollback runbook | docs/specs/api_contracts/strategy_benchmark_endpoints.md; src/pages/StrategyBenchmark.js; docs/reference/openapi.yaml v3.7.0; docs/specs/api_contracts/health_endpoints.md v1.3; docs/ops/api_performance_baseline.md §22.3; docs/operations/render_rollback_runbook.md |

### Deviations accepted
None — no spec deviations this sprint.

### Tech backlog items shipped
- [ST-01] BLG-BE-39: AI journal summary fixed — data.message surfaced to user on Trade History tab; logger.error added to ai_service.py
- [ST-02] BLG-FE-79: R-multiple display fixed on Reflection page — field name correction + N/A handling for no-stop trades
- [ST-03] BLG-OPS-81: AI endpoint per-endpoint rate limiting — 10 req/min/IP (daily-briefing), 30 req/min/IP (chat); 429+Retry-After
- [ST-04] BLG-GOV-146: AI response injection risk assessment — threat model, 5 inputs assessed, BLG-SEC-01/02 filed
- [ST-05] BLG-GOV-147: AI disclaimer visibility assessment — §13 amber badge PASS; contrast gaps BLG-UX-01/02 filed
- [ST-06] BLG-GOV-148: API contract review checklist — 11-item checklist, both AI endpoints ALL PASS
- [ST-07] BLG-QA-65: Nightly stop computation CI simulation tests — 21 tests (7 TS, 5 RX, 9 IV) all passing
- [ST-08] BLG-QA-66: Strategy signal regression test specification — scenario coverage, tolerance, fixture procedure
- [ST-09] BLG-QA-67: AI chat response schema validation tests — 8 tests, schema + advisory-only constraints
- [ST-10] BLG-QA-68: §13 boundary test suite — 11 scenarios across both AI advisory endpoints
- [ST-11] BLG-FEAT-53: Strategy Benchmark page — 3 endpoints, 2 DB tables, import script, full page (3 panels)
- [ST-12] BLG-FE-80: Morning briefing progressive disclosure — 3 collapsible sections, localStorage, Playwright
- [ST-13] BLG-OPS-79: GET /health/scheduler — architecture review + 3-job tracking; test.py updated
- [ST-14] BLG-OPS-78: AI endpoint live latency baseline — daily-briefing p50/p95, chat p50/p95 measured
- [ST-15] BLG-OPS-80: Render deployment rollback runbook — steps, decision matrix, Infrastructure Owner sign-off

Sign-off: Product Owner (agent-mediated — sachiv.patel@hotmail.co.uk) — 2026-06-30
QA sign-off: Director of Quality (agent-mediated) — 2026-06-30

---

## v6.2 — Production Strategy Parity & AI Intelligence — 2026-06-25
Cycle: 2026-06-24__release-v6.2
Verified: Verified
Verification report: claude/cycles/2026-06-24__release-v6.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Production strategy parity cluster: nightly trailing stop computation with profit-lock ratchet (INITIAL_ATR_MULT=5, PROFIT_ATR_MULT=2, ATR_PERIOD=14); month-end rebalance exit signal generation (exit_rebalance status, last-trading-day detection, teal badge); inverse-volatility position sizing for signal-driven entries (weight_i = 1/ATR_i, [5–20%] cash constraints, re-normalised); risk-off exit alerts for open positions (SPY/FTSE MA200 regime check, per-market isolation) | docs/specs/api_contracts/position_endpoints.md#GET /positions; docs/specs/api_contracts/signal_endpoints.md#GET /signals; docs/specs/api_contracts/signal_endpoints.md#POST /signals/generate; docs/specs/frontend/pages/positions.md |
| EPIC-02 | AI intelligence layer: POST /ai/daily-briefing (portfolio/signals/trailing-stops/regime/rebalance context assembly, claude-sonnet-4-6, advisory-only §13 SRB-v1.7 PASS); AiDailyBriefing.js dashboard card (summary, action list, Regenerate button, timestamp); POST /ai/chat (stateless conversational advisor grounded in live portfolio state); AiChatWidget.js on Positions page (canonical) and Signals page (stretch goal); advisory: true enforced in all AI responses | docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing; docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat; docs/specs/frontend/pages/dashboard.md; docs/specs/frontend/pages/positions.md |
| EPIC-03 | Governance & QA debt: execution_prompt.md v3.47→v3.48 (BLG-GOV-135 autonomous class hard gate — blocks when src/components/** or src/pages/** modified; BLG-GOV-136 test_scenarios path validation advisory); api_performance_baseline.md v2.5→v2.6 §21 (GET /portfolio/sector-weights p50=287ms p95=356ms; GET /trade-plans/setup-quality-score p50=464ms p95=516ms — 20 live production samples; BLG-OPS-75); Playwright spec auto-registration via glob pattern (playwright.config.js testDir — BLG-QA-62; 12 dark specs excluded via testIgnore, BLG-QA-64 filed) | claude/system/execution_prompt.md v3.48; docs/ops/api_performance_baseline.md v2.6; playwright.config.js; tests/e2e/ |

### Deviations accepted
None — no spec deviations this sprint.

### Tech backlog items shipped
- [ST-10] BLG-GOV-135: execution_prompt autonomous class hard gate — v3.48 criterion blocks autonomous sign-off when any story modifies src/components/** or src/pages/**
- [ST-11] BLG-GOV-136: execution_prompt test_scenarios path validation advisory — CI/test files only; docs/testing/ paths flagged as evidence artefacts, not scenario files
- [ST-12] BLG-OPS-75: api_performance_baseline.md §21 — GET /portfolio/sector-weights and GET /trade-plans/setup-quality-score measured (20 live production samples each; p95 flag noted for setup-quality-score)
- [ST-13] BLG-QA-62: Playwright spec auto-registration via glob pattern — eliminates manual registration step; 12 pre-existing dark specs excluded via testIgnore (BLG-QA-64 filed for resolution)

Sign-off: Product Owner (agent-mediated — sachiv.patel@hotmail.co.uk) — 2026-06-25
QA sign-off: Director of Quality (agent-mediated) — 2026-06-25

---

## v6.1 — Governance Correctness, CI Quality & User Value Foundation — 2026-06-23
Cycle: 2026-06-22__release-v6.1
Verified: Verified
Verification report: claude/cycles/2026-06-22__release-v6.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance prompt correctness: release_planning_prompt.md STEP 4.1 added design gate detection and `design_gate_required` flag; sprint_planning_prompt.md enforces design gate as hard gate at STEP -1 preflight; governance overhead ceiling proposal produced (G+D+P% metric, 5-cycle baseline=86.0%) | claude/system/release_planning_prompt.md; claude/system/sprint_planning_prompt.md; docs/product/decisions/gov_overhead_ceiling_proposal_v6.1.md |
| EPIC-02 | CI quality hygiene: morning-briefing.spec.js and screener-quality.spec.js registered in playwright.yml (23→25 spec files); PATCH /trades/{id}/costs baseline entry added to api_performance_baseline.md v2.4→v2.5 | .github/workflows/playwright.yml; docs/ops/api_performance_baseline.md |
| EPIC-03 | User value features: portfolio sector heat-map (SectorHeatMap.js on RiskDashboard, GET /portfolio/sector-weights endpoint, amber alert ≥40%); trade gate proximity indicator (GateProgressStrip.js on DashboardHome, {N}/20 trades progress, Gate cleared ✓ state) | docs/design/2026-06-22__release-v6.1/sector-heatmap/ux_spec.md; docs/design/2026-06-22__release-v6.1/gate-proximity-indicator/ux_spec.md; docs/specs/api_contracts/portfolio_endpoints.md |
| EPIC-04 | Setup Quality Score (PT-04, gate cleared): GET /trade-plans/setup-quality-score backend endpoint (gate enforcement, 3 unit test cases); SetupQualityScorePanel frontend in Research.js and TradePlan.js; SC-SQS-01..06 Playwright tests | docs/specs/api_contracts/trade_plan_endpoints.md; docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md |

### Deviations accepted
None — no spec deviations this sprint.

### Tech backlog items shipped
- [ST-01] BLG-GOV-132: Release planning design gate required flag — STEP 4.1 detection + design_gate_required field
- [ST-02] BLG-GOV-133: Sprint planning design gate hard gate at preflight — STEP -1.3 halt when gate not passed
- [ST-03] BLG-GOV-131: Governance overhead ceiling metric — proposal doc + G+D+P% baseline at 86.0%
- [ST-04] BLG-QA-60: Playwright CI registration gap — morning-briefing.spec.js + screener-quality.spec.js registered
- [ST-05] BLG-OPS-73: api_performance_baseline.md PATCH /trades/{id}/costs baseline entry added
- [ST-06] BLG-FE-76: Portfolio sector heat-map — SectorHeatMap.js + GET /portfolio/sector-weights
- [ST-07] BLG-FE-78: Trade gate proximity indicator — GateProgressStrip.js on DashboardHome
- [ST-08/09] BLG-FEAT-25: Setup Quality Score — backend engine + frontend display (PT-04 conditional, gate cleared)

Sign-off: Product Owner — 2026-06-23
QA sign-off: Director of Quality — 2026-06-23

---

## v6.0 — Signal Correctness, User Intelligence & SI-05 Effectiveness — 2026-06-22
Cycle: 2026-06-19__release-v6.0
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-06-19__release-v6.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | P0 correctness fast-track: aligned signal_service suggested_shares to risk-based sizing model per strategy_rules.md §4.1 — cash-allocation model removed; size_position() now canonical for suggested_shares | claude/strategy/strategy_rules.md#4.1; docs/specs/api_contracts/signal_endpoints.md |
| EPIC-02 | Trader's Morning Briefing dashboard (ST-02): frontend composition from 5 existing live endpoints; net-of-costs performance tracking (ST-03): additive trade_costs column + backend net-of-costs calculation + frontend net cost/R display | docs/specs/api_contracts/grace_period_alert_endpoint.md; docs/specs/api_contracts/position_endpoints.md; docs/specs/api_contracts/red_flag_journal.md; docs/specs/api_contracts/earnings_endpoints.md; docs/specs/api_contracts/analytics_endpoints.md; docs/specs/api_contracts/trade_endpoints.md; docs/specs/data_model.md |
| EPIC-03 | Screener data quality telemetry (ST-04): ScreenerQualityPanel with data source, freshness, and degradation indicator; screener_api_contract.md updated to v1.2; openapi.yaml updated. SI-05 deep link AC-04 staging confirmation (ST-05): digest received 2026-06-17 post-FRONTEND_URL; both deep links verified by I&O Owner | docs/specs/api_contracts/screener_api_contract.md; docs/specs/api_contracts/digest_endpoints.md |
| EPIC-04 | RFJ design review pre-brief (ST-06) and visual design review (ST-07): brief and review artefacts delivered; 2 P3 backlog items filed (BLG-FE-66, BLG-FE-67). SI-05 digest cadence review (ST-08): weekly cadence maintained; reassess 2026-07-04. SI-05 actionability metrics (ST-09): 4 metrics defined (ATCR, RFAR, DDCR, EPAR). SI-05 Phase 2 activation scope (ST-10): DEFER — review date revised to 2026-08-04. SI-05 p99 latency baseline review (ST-11): PASS WITH DEVIATION; functional evidence satisfactory | docs/design/2026-06-19__release-v6.0/rfj-design-review/brief.md; docs/design/2026-06-19__release-v6.0/rfj-design-review/review.md; docs/product/decisions/si05-digest-cadence-review--2026-06-22.md; docs/product/decisions/si05-actionability-metrics-definition.md; docs/product/decisions/si05-phase2-activation-decision--2026-06-22.md; docs/testing/staging_latency_review_ST-11.md |

### Deviations accepted
2 minor P3 process deviations for ST-11 — see verification_report.md §4 (ST-11-DEV-1: 16-day vs 4-week measurement window; ST-11-DEV-2: AC-02 N/A — no BLG-OPS-54 baseline; both accepted under PO gate override 2026-06-20).

### Tech backlog items shipped
- [ST-01] BLG-BE-36: Align signal_service suggested_shares to risk-based sizing model — P0 correctness fix; size_position() per §4.1 now canonical
- [ST-02] BLG-FEAT-46: Trader's Morning Briefing dashboard — morning summary view from 5 live endpoints with Playwright coverage (11 scenarios)
- [ST-03] BLG-FEAT-20: Net-of-costs performance tracking — additive trade_costs fields + frontend net-of-costs display; 5 Playwright scenarios
- [ST-04] BLG-FEAT-47: Screener data quality telemetry — ScreenerQualityPanel; screener contract v1.2; 5 Playwright scenarios
- [ST-05] BLG-OPS-70: SI-05 deep link AC-04 staging confirmation — digest received 2026-06-17; both deep links verified by I&O Owner
- [ST-06] BLG-FE-64: RFJ design review pre-brief — brief.md authored; scope for ST-07 defined; HoUX&D sign-off
- [ST-07] BLG-FE-41: Red Flag Journal visual design review — Accept/Refine verdict; BLG-FE-66 + BLG-FE-67 filed; HoUX&D sign-off
- [ST-08] BLG-GOV-112: SI-05 digest weekly cadence review — weekly cadence maintained; reassess 2026-07-04
- [ST-09] BLG-GOV-115: SI-05 digest actionability metric definition — 4 metrics (ATCR, RFAR, DDCR, EPAR) defined; feeds BLG-GOV-112 and BLG-GOV-96
- [ST-10] BLG-GOV-130: SI-05 Phase 2 activation decision scope — DEFER; revised review date 2026-08-04; BLG-GOV-121 §13 pre-clearance action raised
- [ST-11] BLG-OPS-59: SI-05 service production p99 latency baseline review — PASS WITH DEVIATION; BLG-OPS-54 scope revised to Render internal log approach

Sign-off: Product Owner — 2026-06-22
QA sign-off: Director of Quality — 2026-06-22

---

## v5.9 — RFJ UX Pre-work, SI-05 Effectiveness Review & Governance Simplification — 2026-06-18
Cycle: 2026-06-17__release-v5.9
Verified: Verified
Verification report: claude/cycles/2026-06-17__release-v5.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | 5 governance simplification stories (SC-03–SC-07): consolidated spec_references policy sub-variants in execution_prompt.md; removed STEP 8.6–8.7 fatigue detection guardrail from roadmap_prompt.md; removed dead-load advisory steps from release_planning_prompt.md; made Playwright selector check conditional on DOM changes in execution_prompt.md; compressed Advisory Summary Block format docs in post_ship_closure.md | claude/system/execution_prompt.md, claude/system/roadmap_prompt.md, claude/system/release_planning_prompt.md, claude/system/post_ship_closure.md |
| EPIC-02 | 6 QA/audit/UX stories: Yahoo Finance backoff path integration test stub (ST-06); DoQ sign-off date compliance audit v3.7–v3.9 (ST-07); QA evidence file format audit v3.7–v4.0 (ST-08); agent idea participation tracking summary (ST-09); formal regression test suite baseline document (ST-10); pre-entry panel warning/fail count badge when collapsed — Playwright coverage SC-PEP-BADGE-01a/01b/02 (ST-11) | tests/test_screener_data_service.py, claude/cycles/2026-06-17__release-v5.9/advisory_doq_audit_v37_v39.md, claude/cycles/2026-06-17__release-v5.9/advisory_qa_format_audit_v37_v40.md, claude/cycles/2026-06-17__release-v5.9/advisory_agent_idea_participation.md, docs/qa/regression_test_suite_baseline.md, src/pages/TradePlan.js, tests/e2e/pre-entry-panel-badge.spec.js |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] BLG-GOV-125: SC-03 spec_references policy sub-variants consolidated in execution_prompt.md
- [ST-02] BLG-GOV-126: SC-04 fatigue detection guardrail (STEP 8.6–8.7) removed from roadmap_prompt.md
- [ST-03] BLG-GOV-127: SC-05 dead-load advisory steps removed from release_planning_prompt.md
- [ST-04] BLG-GOV-128: SC-06 Playwright selector check made conditional on DOM changes in execution_prompt.md
- [ST-05] BLG-GOV-129: SC-07 Advisory Summary Block format docs compressed in post_ship_closure.md
- [ST-06] BLG-QA-24: Yahoo Finance backoff path integration test stub added (test_yahoo_backoff_path_401_sleep_once_then_200)
- [ST-07] BLG-GOV-38: DoQ sign-off date compliance audit (v3.7–v3.9) — advisory_doq_audit_v37_v39.md
- [ST-08] BLG-QA-34: QA evidence file format audit (v3.7–v4.0) — advisory_qa_format_audit_v37_v40.md
- [ST-09] BLG-GOV-53: Agent idea participation tracking summary — advisory_agent_idea_participation.md
- [ST-10] BLG-QA-50: Formal regression test suite baseline document — docs/qa/regression_test_suite_baseline.md
- [ST-11] BLG-FE-57: Pre-entry panel warning/fail count badge when collapsed — TradePlan.js + Playwright SC-PEP-BADGE-01a/01b/02

### Items returned to backlog
None — all 11 stories shipped.

Sign-off: Product Owner — 2026-06-18
QA sign-off: Director of Quality — 2026-06-18

---

## v5.8 — RFJ UX Design Completion, SI-05 Effectiveness Review & Production Hardening — 2026-06-17
Cycle: 2026-06-17__release-v5.8
Verified: Verified
Verification report: claude/cycles/2026-06-17__release-v5.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | FRONTEND_URL production env var configured on Render backend (trading-assistant-api-c0f9.onrender.com) — restores SI-05 deep-link functionality in production; deployment runbook v0.3 updated (§6.1 env var table); AC-04 staging-only deep link confirmation deferred to BLG-OPS-70 | docs/ops/production_deployment_runbook.md#6.1 |
| EPIC-01 | Governance model complexity assessment produced (GCA-2026-06-17; docs/governance/governance_complexity_assessment_2026-06-17.md); 7 simplification candidates enumerated (BLG-GOV-123–129); hypothesis test: complexity IS a secondary contributing factor (not root cause); Director of HR + PMO Lead + Head of Specs Team sign-off | docs/governance/governance_complexity_assessment_2026-06-17.md |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-03] BLG-GOV-101: FRONTEND_URL production env var — SI-05 deep-link production support restored (AC-04 staging-only evidence deferred to BLG-OPS-70)
- [ST-04] BLG-GOV-101: Governance complexity assessment — GCA-2026-06-17 produced; 7 simplification candidates BLG-GOV-123–129 filed

### Items returned to backlog
- ST-01 (BLG-FE-64): RFJ design review pre-brief — gate 2026-06-21 not yet reached (5th deferral); BLG-FE-64 updated
- ST-02 (BLG-FE-41): Red Flag Journal visual design review — depends on ST-01; gate 2026-06-21 not reached; BLG-FE-41 updated
- ST-05 (BLG-GOV-112): SI-05 digest weekly cadence review — Sprint 2 gate 2026-07-04 not reached; BLG-GOV-112 updated
- ST-06 (BLG-GOV-115): SI-05 digest actionability metric definition — gate 2026-07-04 not reached; BLG-GOV-115 updated
- ST-07 (BLG-OPS-59): SI-05 service production p99 latency baseline review — gate 2026-07-04 not reached; BLG-OPS-59 updated

Sign-off: Product Owner — 2026-06-17
QA sign-off: Director of Quality — 2026-06-17

---

## v5.7 — Staging Verification Completion, SI-05 Effectiveness Review & Engineering/Governance Patches — 2026-06-17
Cycle: 2026-06-16__release-v5.7
Verified: Verified
Verification report: claude/cycles/2026-06-16__release-v5.7/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Production latency staging verifications: concentration-status p95=755ms ✓, red-flag-journal p95=872ms ✓, behavioural-drift p95=677ms (cached) ✓, research view p95=105ms ✓ (all BLG-OPS-66–69 closed); SI-05 deep links mobile Telegram staging run confirmed working after two in-sprint bug fixes (BLG-FE-75 closed); Arc 5 Playwright coverage gaps closed: SC-SI-01d (all-pass state), SC-RFJ-04 (pagination), SC-ARC5-05 (compliance trend values) | docs/ops/api_performance_baseline.md; tests/e2e/si01-si03-integration.spec.js; tests/e2e/red-flag-journal.spec.js; tests/e2e/arc5-compliance-section.spec.js |
| EPIC-02 | Lazy-import pattern documented in backend_engineering_patterns.md v1.0→v1.1 (BLG-BE-36 closed); dual sign-off class pattern confirmed present in execution_prompt.md §5.3 at v3.42 (BLG-GOV-123 closed; LL-v5.6-DV-03 carry-forward resolved) | docs/specs/api_contracts/backend_engineering_patterns.md; claude/system/execution_prompt.md |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] BLG-OPS-66: Staging verification — concentration-status p95 — p95=755ms confirmed, FX cache fix effective
- [ST-02] BLG-OPS-67: Staging verification — red-flag-journal p95 — p95=872ms confirmed, schema-once fix effective
- [ST-03] BLG-OPS-68: Staging verification — behavioural-drift p95 + cache — p95=677ms cached, cache hit rate ≥50% inferred
- [ST-04] BLG-OPS-69: Staging verification — research view p95 + cache — p95=105ms, cache hit rate ≥90%, mechanism confirmed
- [ST-05] BLG-FE-75: Staging verification — SI-05 deep links on mobile Telegram — two in-sprint fixes, both links confirmed
- [ST-06] BLG-QA-56: SI-01 all-pass state Playwright scenario (SC-SI-01d added)
- [ST-07] BLG-QA-57: SI-03 RFJ pagination Playwright scenario (SC-RFJ-04 added)
- [ST-08] BLG-QA-58: Arc 5 compliance trend Playwright scenario (SC-ARC5-05 added)
- [ST-10] BLG-BE-36: Lazy-import pattern documentation — backend_engineering_patterns.md v1.1
- [ST-11] BLG-GOV-123: Dual sign-off class pattern confirmed in execution_prompt.md — LL-v5.6-DV-03 closed

Sign-off: Product Owner (agent-mediated) — 2026-06-17
QA sign-off: Director of Quality (agent-mediated) — 2026-06-17

---

## v5.6 — Research Performance, SI-05 UX Improvements & Governance Patches — 2026-06-16
Cycle: 2026-06-16__release-v5.6
Verified: Verified
Verification report: claude/cycles/2026-06-16__release-v5.6/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-03 | PT-04 trade count gate re-verification (13/20 closed trades — gate NOT MET, 7 more required; trajectory accelerating); Arc 5 QA completion criteria defined (BLG-QA-26 gate condition updated; SI-05 Phase 2/SI-04 excluded); Arc 5 test scenario completeness assessment (3 P3 Playwright gaps filed as BLG-QA-56/57/58); Anthropic API cost 14-cycle trend analysis (est. $0.05–$0.15/month; stable) | claude/roadmap/current_roadmap.md#PT-04; docs/qa/arc5_qa_completion_criteria.md; docs/qa/arc5_test_coverage_assessment.md; docs/ops/anthropic_api_cost_trend_2026.md |
| EPIC-01 | SI-05 digest UX: deep links added to Risk Dashboard and Red Flag Journal screens (FRONTEND_URL env var); N/A pass rate reason clarified with distinct messages for no_events vs data_unavailable | backend/services/si05_digest_service.py |
| EPIC-02 | Performance latency hardening: 5-min TTL FX rate cache for GET /portfolio/concentration-status; process-lifetime schema-once guard for GET /portfolio/red-flag-journal; schema-once guard + 15-min TTL result cache for GET /analytics/behavioural-drift; 15-min per-ticker TTL cache + screener invalidation for GET /research/{ticker} | backend/utils/pricing.py; backend/routers/red_flag_journal.py; backend/routers/analytics.py; backend/routers/research.py; backend/routers/screener.py |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-08] PT-04 trade count gate re-verification — BLG-GOV-106 closed
- [ST-09] Arc 5 QA completion criteria definition — BLG-QA-45 closed
- [ST-10] Arc 5 test scenario completeness assessment — BLG-QA-49 closed
- [ST-11] Anthropic API cost 14-cycle trend analysis — BLG-OPS-65 closed
- [ST-01] Add deep links from SI-05 digest to relevant app screens — BLG-FE-73 closed
- [ST-02] Clarify N/A pass rate reason in SI-05 digest — BLG-FE-74 closed
- [ST-04] Investigate GET /portfolio/concentration-status high latency — BLG-OPS-62 closed
- [ST-05] Investigate GET /portfolio/red-flag-journal high latency — BLG-OPS-63 closed
- [ST-06] Investigate GET /analytics/behavioural-drift high latency — BLG-OPS-64 closed
- [ST-07] Research data caching layer — BLG-OPS-22 closed

### Items returned to backlog
- [ST-03] BLG-FE-64: RFJ visual design review pre-brief — gate 2026-06-21 not met (SI-03 Red Flag Journal live ≥30 days); BLG-FE-64 remains open (eligible from 2026-06-21)

Sign-off: Product Owner — 2026-06-16
QA sign-off: Director of Quality — 2026-06-16

---

## v5.5 — SI-05 Effectiveness Review, Governance Hardening & UX Debt Clearance — 2026-06-16
Cycle: 2026-06-10__release-v5.5
Verified: Verified
Verification report: claude/cycles/2026-06-10__release-v5.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance patches: sprint_planning_prompt.md within-sprint date gate advisory (ST-01); execution_prompt.md pr_status read-after-open improvement with mandatory persist-before-halt gate (ST-02 / LL-v5.5-EX-02); qa_evidence commit discipline advisory (ST-03) | claude/system/sprint_planning_prompt.md; claude/system/execution_prompt.md |
| EPIC-02 | Trade count gate-monitoring view: GET /portfolio/gate-metrics backend endpoint + SI-05 data density progress line in Telegram digest | docs/ops/api_performance_baseline.md; claude/cycles/2026-06-10__release-v5.5/stage4_backlog_slice.md |
| EPIC-03 | API performance baseline complete: 18 endpoints measured across v2.8–v5.4; formal regression test suite baseline document produced (387 scenarios, 66 endpoints, 41 e2e specs); SI-05 user journey map authored with 2 friction findings | docs/ops/api_performance_baseline.md; docs/qa/regression_test_suite_baseline.md; docs/ux/si05_user_journey_map.md |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] sprint_planning_prompt.md within-sprint date gate advisory — BLG-GOV-116 closed
- [ST-02] execution_prompt.md pr_status read-after-open improvement — BLG-GOV-117 closed
- [ST-03] qa_evidence commit discipline advisory in execution_prompt.md — BLG-GOV-118 closed
- [ST-04] Trade count gate-monitoring view (backend) — BLG-BE-34 closed
- [ST-05] Trade data density progress tracker (frontend display) — BLG-GOV-120 closed
- [ST-06] v2.8–v4.6 endpoint performance baseline re-run (24 endpoints) — BLG-OPS-13 closed
- [ST-07] v5.1–v5.4 endpoint baseline extension — BLG-OPS-61 closed
- [ST-08] POST /digest/si05/send to api_performance_baseline.md — BLG-OPS-54 closed
- [ST-09] Formal regression test suite baseline document — BLG-QA-50 closed
- [ST-10] User journey map: SI-05 Telegram digest to app action — BLG-FE-65 closed

### Items returned to backlog
- [ST-11] Red Flag Journal visual design review pre-brief — gate 2026-06-21 not met; BLG-FE-64 remains open (eligible from 2026-06-21)
- [ST-12] SI-05 p99 production latency baseline review — gate 2026-07-04 not met; BLG-OPS-59 remains open
- [ST-13] SI-05 digest weekly cadence review — gate 2026-07-04 not met; BLG-GOV-112 remains open
- [ST-14] SI-05 digest actionability metric definition — gate 2026-07-04 not met; BLG-GOV-115 remains open

Sign-off: Product Owner — 2026-06-16
QA sign-off: Director of Quality — 2026-06-16

---

## v5.4 — Ops Monitoring, UX Debt Clearance & Governance Patches — 2026-06-10
Cycle: 2026-06-09__release-v5.4
Verified: Verified
Verification report: claude/cycles/2026-06-09__release-v5.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Add v5.3 new endpoints to api_performance_baseline.md — 5 endpoint rows with live Render measurements (GET /ai/journal-summary/history, GET /news/AAPL, GET /watchlist) | docs/ops/api_performance_baseline.md#17. v5.3 New Endpoints |
| EPIC-02 | Pre-entry panel: separate warn/fail override acknowledgement flow — UX spec document produced | docs/product/ux/pre_entry_override_ux_spec.md |
| EPIC-03 | SI-05 Phase 2 activation criteria definition — governance doc produced, PO-approved | docs/governance/si05_phase2_activation_criteria.md |

### Deviations accepted
None.

### Tech backlog items shipped
- [ST-01] Add v5.3 new endpoints to api_performance_baseline.md — BLG-OPS-60 closed
- [ST-04] SI-05 Phase 2 activation criteria definition — BLG-GOV-92 closed

### Items returned to backlog
- [ST-03] RFJ visual design review pre-brief — returned; date gate (SI-03 live ≥30 days; 2026-06-21) not met; BLG-FE-64 remains open

Sign-off: Product Owner — 2026-06-10
QA sign-off: Director of Quality — 2026-06-10

---

## v5.3 — Spec Debt, Security Hardening & Ops Governance — 2026-06-09
Cycle: 2026-06-08__release-v5.3
Verified: Verified
Verification report: claude/cycles/2026-06-08__release-v5.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | API contract spec debt resolution: BLG-SPEC-53 — contract gap resolution plan; BLG-SPEC-54 — openapi.yaml completeness audit (50 routes); BLG-QA-51 — QA acceptance criteria template for SPEC-49–52; BLG-SPEC-49 — GET /ai/journal-summary/history contract; BLG-SPEC-50 — GET /analytics/compliance-metrics contract; BLG-SPEC-51 — GET /news/{ticker} contract; BLG-SPEC-52 — Watchlist endpoint contracts + test.py. All 6 known API contract gaps closed. | docs/specs/api_contracts/ai_endpoints.md; docs/specs/api_contracts/analytics_endpoints.md; docs/specs/api_contracts/news_endpoints.md; docs/specs/api_contracts/watchlist_endpoints.md; docs/reference/openapi.yaml; docs/qa/endpoint_contract_qa_criteria_template.md |
| EPIC-02 | Security hardening: BLG-BE-35 — POST /digest/si05/send API key authentication implemented; BLG-OPS-57 — SI-05 Telegram delivery failure alerting; BLG-OPS-58 — CI secret scanning gate (gitleaks). | docs/specs/api_contracts/digest_endpoints.md; docs/operations/deployment_runbook.md; .github/workflows/secret-scanning.yml; .gitleaks.toml |
| EPIC-03 | Governance patches and AI policy: LL-v5.2-P4-01 — qa_evidence_template.md signer format note; LL-v5.2-P4-02 — execution_prompt.md STEP 5.3A SSR sub-step; BLG-GOV-107 — SI-02 frontend activation criteria precision; BLG-GOV-108 — AI model pin update policy; BLG-GOV-109 — AI audit log retention policy; BLG-GOV-110 — Arc 4 trade_plan data completeness audit; BLG-GOV-104 — strategy_rules.md §11 parameter validation; BLG-GOV-113 — SI-05 effectiveness review protocol; BLG-GOV-114 — si05_digest_log schema validation. | claude/system/templates/qa_evidence_template.md; claude/system/execution_prompt.md; claude/roadmap/current_roadmap.md; docs/governance/ai_model_version_pinning_policy.md; docs/governance/ai_audit_log_retention_policy.md; docs/governance/arc4_trade_plan_data_completeness_audit.md; docs/governance/strategy_parameter_validation_v53.md; docs/governance/si05_effectiveness_review_protocol.md; docs/governance/si05_digest_log_schema_validation.md |
| EPIC-04 | QA coverage and UX review: BLG-QA-52 — Tax year P&L boundary edge case validation (6 test scenarios); BLG-QA-53 — SI-05 digest Playwright E2E coverage (4 scenarios); BLG-QA-54 — Playwright coverage matrix update post-v5.2; BLG-FE-66 — Red Flag Journal post-launch UX review; BLG-FE-67 — BLG-FE-64 visual design review scope definition. | tests/test_tax_year_pnl_boundary.py; tests/e2e/si05-digest-delivery.spec.js; docs/qa/playwright_coverage_matrix.md; docs/governance/rfj_ux_review_v53.md; docs/governance/blg_fe_64_scope_definition.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-SPEC-53 — API contract gap resolution plan
- [ST-02] BLG-SPEC-54 — openapi.yaml completeness audit
- [ST-03] BLG-QA-51 — QA acceptance criteria for SPEC-49–52
- [ST-04] BLG-SPEC-49 — GET /ai/journal-summary/history contract
- [ST-05] BLG-SPEC-50 — GET /analytics/compliance-metrics contract
- [ST-06] BLG-SPEC-51 — GET /news/{ticker} contract
- [ST-07] BLG-SPEC-52 — Watchlist endpoint contracts + test.py
- [ST-08] BLG-BE-35 — POST /digest/si05/send API key authentication
- [ST-09] BLG-OPS-57 — SI-05 Telegram delivery failure alerting
- [ST-10] BLG-OPS-58 — CI secret scanning gate
- [ST-11] LL-v5.2-P4-01 — qa_evidence_template.md signer format note
- [ST-12] LL-v5.2-P4-02 — execution_prompt.md STEP 5.3A SSR sub-step
- [ST-13] BLG-GOV-107 — SI-02 frontend activation criteria precision (roadmap annotation)
- [ST-14] BLG-GOV-108 — AI model pin update policy
- [ST-15] BLG-GOV-109 — AI audit log retention policy
- [ST-16] BLG-GOV-110 — Arc 4 trade_plan data completeness audit
- [ST-17] BLG-GOV-104 — strategy_rules.md §11 parameter validation
- [ST-18] BLG-QA-52 — Tax year P&L boundary edge case validation
- [ST-19] BLG-QA-53 — SI-05 digest Playwright E2E coverage
- [ST-20] BLG-QA-54 — Playwright coverage matrix update post-v5.2
- [ST-21] BLG-FE-66 — Red Flag Journal post-launch UX review
- [ST-22] BLG-FE-67 — BLG-FE-64 visual design review scope definition
- [ST-23] BLG-GOV-113 — SI-05 effectiveness review protocol
- [ST-24] BLG-GOV-114 — si05_digest_log schema validation

Sign-off: Product Owner — 2026-06-09
QA sign-off: Director of Quality — 2026-06-09

---

## v5.2 — Governance Debt, SI-05 Ops & Spec Compliance — 2026-06-08
Cycle: 2026-06-08__release-v5.2
Verified: Verified
Verification report: claude/cycles/2026-06-08__release-v5.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance patches: OA-01 — release_planning_prompt.md v2.33→v2.34 §-1.2 STEP 8.1 Option(b) path added; OA-02 — execution_prompt.md v3.36→v3.37 §3.1.A step 2c test-authoring spec_references guidance; BLG-SPEC-47 resolved — DEV-v51-EPIC01-01 closed, Option(a) pass_rate computation documented, si05-telegram-message-format-spec.md updated; BLG-SPEC-48 — digest_endpoints.md v0.2→v0.3 authentication requirements section added. | claude/system/release_planning_prompt.md v2.34; claude/system/execution_prompt.md v3.37; docs/specs/api_contracts/digest_endpoints.md v0.3; docs/product/decisions/si05-telegram-message-format-spec.md |
| EPIC-02 | SI-05 operational hardening: BLG-BE-32 — Telegram retry (max 2 retries, 30s/60s backoff; ERROR logging; 3 new unit tests; injectable sleep for CI); BLG-BE-33 — si05_digest_log table (schema: id, sent_at, status, event_count, telegram_message_id, error_message, created_at; CREATE TABLE IF NOT EXISTS guard; log rows on both paths; registered in main.py on_startup()); BLG-OPS-55 — production deployment runbook §6 (SI-05 env vars, cron schedule, failure detection, health check; v0.1→v0.2); BLG-OPS-56 — SI-05 health check procedure (3 check options; escalation path; weekly cadence). | backend/services/si05_digest_service.py; docs/specs/api_contracts/digest_endpoints.md; docs/ops/production_deployment_runbook.md v0.2; docs/ops/si05_health_check_procedure.md |
| EPIC-03 | Security reviews: BLG-GOV-97 — Claude API model deprecation check (PASS; claude-haiku-4-5-20251001 current; next review 2026-09-08); BLG-GOV-98 — Telegram bot token minimal-permission review (PASS with recommendation: send-only confirmed; BotFather manual check recommended); BLG-GOV-99 — digest endpoint authentication review (GAP_FOUND: POST /digest/si05/send unauthenticated; BLG-BE-35 P2 filed); BLG-GOV-100 — backend endpoint coverage audit (50 routes enumerated; 6 contract gaps; BLG-SPEC-49/50/51/52 filed). | docs/governance/ai_model_deprecation_check_v52.md; docs/security/security_register.md; docs/ops/endpoint_coverage_audit_v52.md |
| EPIC-04 | QA governance: BLG-QA-46 — SI-05 edge case gap analysis + 2 new tests (connection failure, message truncation; 26 tests total passing); BLG-QA-47 + BLG-GOV-94 — SI-05 Phase 1 acceptance test protocol + delivery verification protocol docs; BLG-QA-48 — regression baseline refresh (POST /digest/si05/send in test.py confirmed; 5 Playwright scenarios confirmed; BLG-QA-50 formal baseline doc filed); BLG-GOV-96 — SI-05 effectiveness measurement criteria (3 criteria; 30-day review 2026-07-04). | tests/test_si05_digest_service.py; backend/routers/test.py; docs/qa/si05_edge_case_gap_analysis.md; docs/qa/si05_acceptance_test_protocol.md; docs/qa/si05_delivery_verification_protocol.md; docs/qa/regression_baseline_refresh_v51.md; claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] OA-01 — release_planning_prompt.md §-1.2 STEP 8.1 Option(b) accommodation patch (v2.33→v2.34)
- [ST-02] OA-02 — execution_prompt.md §3.1.A test-authoring spec_references guidance (v3.36→v3.37)
- [ST-03] BLG-SPEC-47 — SI-05 pass_rate computation aligned with BLG-GOV-86 §5.2; DEV-v51-EPIC01-01 resolved
- [ST-04] BLG-SPEC-48 — POST /digest/si05/send API contract gap check and authoring (digest_endpoints.md v0.3)
- [ST-05] BLG-BE-32 — SI-05 Telegram delivery retry and failure handling (30s/60s backoff; ERROR logging; unit tests)
- [ST-06] BLG-BE-33 — SI-05 digest delivery log table (si05_digest_log) — Data Model Owner sign-off
- [ST-07] BLG-OPS-55 — Deployment runbook update for SI-05 operational environment (v0.1→v0.2)
- [ST-08] BLG-OPS-56 — SI-05 service scheduled run health check procedure
- [ST-09] BLG-GOV-97 — Claude API model deprecation compliance check (PASS; next review 2026-09-08)
- [ST-10] BLG-GOV-98 — Telegram bot token minimal-permission security review (PASS with recommendation)
- [ST-11] BLG-GOV-99 — SI-05 digest endpoint authentication review (GAP_FOUND: BLG-BE-35 P2 filed)
- [ST-12] BLG-GOV-100 — Backend endpoint documentation coverage audit post-v5.1 (50 routes; 6 gaps filed)
- [ST-13] BLG-QA-46 — SI-05 digest service edge case test gap analysis (2 new tests; 26 total passing)
- [ST-14] BLG-QA-47 + BLG-GOV-94 — SI-05 Phase 1 acceptance test protocol and delivery verification protocol
- [ST-15] BLG-QA-48 — Regression test suite baseline refresh post-v5.1
- [ST-16] BLG-GOV-96 — SI-05 Phase 1 effectiveness measurement criteria (30-day review 2026-07-04)

Sign-off: Product Owner — 2026-06-08
QA sign-off: Director of Quality — 2026-06-08

---

## v5.1 — SI-05 Phase 1 & Governance Debt — 2026-06-04
Cycle: 2026-06-21__release-v5.1
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-06-21__release-v5.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-05 Phase 1 — Weekly Strategy Integrity Digest via Telegram. BLG-GOV-67 delivered: `backend/services/si05_digest_service.py`; `POST /digest/si05/send` endpoint (openapi.yaml updated); 21 unit tests; SI-05 financial reporting scope verified as OUT OF SCOPE for Phase 1 (BLG-SPEC-45 resolved). | docs/product/decisions/si05-telegram-message-format-spec.md (Known Deviations section added); docs/specs/api_contracts/arc5_compliance_analytics.md; docs/specs/api_contracts/digest_endpoints.md |
| EPIC-02 | Governance patch — `delivery_verification_prompt.md` §-1.3 Tier 2: explicit acceptance of agent-mediated signer format added (v2.9→v3.0). Resolves v5.0 Phase 4 Tier 2 advisory (LL-RP-v5.0-D-2). | claude/system/delivery_verification_prompt.md v3.0 |
| EPIC-03 | QA & documentation debt: BLG-FE-61 — SignalCard `allocation_insufficient` badge Playwright E2E coverage (5 scenarios, SC-SIG-AI-01/02/03); BLG-QA-43 — `compliance_summary` field population validation by code review; BLG-GOV-89 — staged verification sprint protocol document v1.0. | docs/operations/staged_verification_sprint_protocol.md v1.0; docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl |

### Deviations accepted
1 minor deviation — see verification_report.md

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-v51-EPIC01-01 | P3 | `pass_rate` computation uses volume-weighted overall rate instead of mean-of-per-rule-rates per BLG-GOV-86 §5.2; `digest_endpoints.md` v0.2 documents "Overall pass/total ratio" creating spec-to-spec inconsistency with BLG-GOV-86 §5.2. BLG-SPEC-47 filed for resolution before next SI-05 feature increment. | PO |

### Tech backlog items shipped
- [ST-01] BLG-GOV-67 — SI-05 Phase 1 backend service + Telegram weekly digest implementation
- [ST-02] BLG-SPEC-45 — SI-05 financial reporting scope verification (confirmed OUT OF SCOPE for Phase 1)
- [ST-03] LL-RP-v5.0-D-2 — delivery_verification_prompt.md §-1.3 Tier 2 agent-mediated signer format acceptance (v2.9→v3.0)
- [ST-04] BLG-FE-61 — SignalCard allocation_insufficient badge Playwright E2E coverage (5 scenarios)
- [ST-05] BLG-QA-43 — compliance_summary field population validation
- [ST-06] BLG-GOV-89 — Staged verification sprint protocol document v1.0

Sign-off: Product Owner — 2026-06-21
QA sign-off: Director of Quality — 2026-06-21

---

## v5.0 — Governance Hardening, Product Correctness & SI-05 Pre-work — 2026-06-03
Cycle: 2026-06-03__release-v5.0
Verified: Verified
Verification report: claude/cycles/2026-06-03__release-v5.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance Document Patches — prompt_change_log.md verified complete (all 7 BLG-GOV-79 entries confirmed present; AUD-001 gap closed); 5 non-standard agent file headers corrected (ATX heading; trailing backslash removed): ai_compliance_governance_officer.md, cybersecurity_trust_lead.md, director_of_hr.md, financial_reporting_records_owner.md, finops_resource_architect.md; PR template updated with explicit "Product Owner Acceptance (Hard Gate)" section + GitHub Approve instruction (v1.2→v1.3) | claude/system/prompt_change_log.md; claude/agents/ (5 files); .github/pull_request_template.md |
| EPIC-02 | Governance Engine Structural Fixes — execution_prompt.md STEP 8 structural governance file edit check added (git-diff scan replaces operator memory; v3.35→v3.36; root-cause fix for BLG-GOV-79/80 pattern); post-ship audit advisory strengthened (dual-condition: % 3 == 0 OR gap ≥ 4, null-safe); last_audit_cycle_count field added to .claude_current_state.json and lifecycle_schema.json; post_ship_closure.md v2.12→v2.13 | claude/system/execution_prompt.md v3.36; docs/reference/OPERATIONAL_GUIDE.md; claude/system/post_ship_closure.md v2.13; claude/system/schemas/lifecycle_schema.json |
| EPIC-03 | Product Correctness Fixes & Ops Verification — allocation_insufficient signal status: new backend status value + reason field when price_gbp > allocation_gbp; frontend SignalCard orange "Cannot Size" badge + reason inline; openapi.yaml, test.py, SC-SS-01b updated; pre-entry regime gate fix: shared 5-min cache in check_market_regime() eliminates independent yf.download (all callers share one result per window); unit tests covering cache hit/miss added; Anthropic SDK (0.40.0 → 0.105.2) staging verification complete | docs/specs/api_contracts/signal_endpoints.md; docs/specs/api_contracts/pre_entry_validation.md; docs/specs/api_contracts/ai_thesis_generation.md; docs/specs/api_contracts/ai_endpoints.md |
| EPIC-04 | SI-05 Phase 1 Pre-work Documentation Suite — SI-05 notification channel trade-off doc + PO decision (Telegram confirmed); SI-05 Telegram message format spec v1.0 (section structure, data bindings GET /analytics/arc5-compliance, character budget ~265/4096, failure modes); SI-02 re-entry trigger criteria (hard gate ≥20 closed trades, soft advisory ≥3 months, PMO check from v5.1); SI-04 §13 binding conditions formal decisions document (all 6 conditions; Strategy Rules & System Intent Owner sign-off); SI-02 drift summary feasibility assessment (feasible with conditions; 3 UX risks + mitigations) | docs/product/decisions/si05-notification-channel-tradeoff.md; docs/product/decisions/si05-telegram-message-format-spec.md; docs/product/decisions/si02-reentry-trigger-criteria.md; docs/product/decisions/decisions--2026-06-03__release-v5.0--SI-04-binding-conditions.md; docs/product/decisions/si02-drift-summary-feasibility-assessment.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-79 — prompt_change_log.md: all 7 missing entries verified present (AUD-001 closed)
- [ST-02] BLG-GOV-81 — 5 agent file header corrections (ATX heading; no trailing backslash)
- [ST-03] BLG-GOV-83 — PR template: PO acceptance = GitHub Approve instruction added
- [ST-04] BLG-GOV-80 — execution_prompt.md STEP 8 structural governance check (v3.35→v3.36)
- [ST-05] BLG-GOV-82 — post-ship audit advisory dual-condition + last_audit_cycle_count schema (v2.12→v2.13)
- [ST-06] BLG-FEAT-43 — allocation_insufficient signal status + reason field + frontend badge (openapi.yaml + test.py updated)
- [ST-07] BLG-BE-25 — pre-entry regime gate fix: shared market status cache (5-min TTL; unit tests added)
- [ST-08] BLG-OPS-52 — Anthropic SDK 0.40.0 → 0.105.2 staging verification (POST /generate-thesis + POST /ai/check-daily-cost confirmed)
- [ST-09] BLG-FE-60 — SI-05 notification channel trade-off + PO decision (Telegram confirmed)
- [ST-10] BLG-GOV-86 — SI-05 Telegram message format specification v1.0
- [ST-11] BLG-GOV-87 — SI-02 re-entry trigger criteria definition
- [ST-12] BLG-GOV-88 — SI-04 §13 binding conditions formal decisions document
- [ST-13] BLG-BE-26 — SI-02 drift summary feasibility assessment

Sign-off: Product Owner — 2026-06-03
QA sign-off: Sprint Execution Engine (autonomous class) — 2026-06-03

---

## v4.9 — Security/CI Hardening & SI-05 Phase 1 — 2026-06-02
Cycle: 2026-06-02__release-v4.9
Verified: Verified
Verification report: claude/cycles/2026-06-02__release-v4.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Security & Dependency Hardening — 21 npm HIGH CVEs cleared via npm audit fix + overrides; 6 moderate remain (CRA chain, non-production) (ST-01); Anthropic Python SDK upgraded 0.40.0 → 0.105.2; Messages API changelog reviewed, no breaking changes; AC-04 staging validation deferred post-merge per BLG-OPS-52 (ST-02) | docs/security/security_register.md (Audit 001; Upgrade 001) |
| EPIC-02 | CI/QA Infrastructure Strengthening — Real Postgres service container (postgres:15) wired to Phase B CI; DATABASE_URL injected; 13 pre-existing Phase B test isolation failures surfaced and fixed; Phase A unaffected (ST-03); Schema lifecycle column smoke tests created in tests/test_schema.py: assert positions table has position_state, state_entered_at, state_history; skips in Phase A (stub), passes in Phase B (ST-04) | .github/workflows/ci-tests.yml; tests/test_schema.py |
| EPIC-03 | Governance Debt Clearance — roadmap_prompt.md STEP 8.1 converted from advisory-only to soft gate requiring explicit PO decision when Now horizon empty; both options documented with example formats (add section now / defer with rationale); OPERATIONAL_GUIDE.md v4.25→v4.26 (ST-05) | claude/system/roadmap_prompt.md v6.8; claude/system/OPERATIONAL_GUIDE.md v4.26; claude/system/prompt_change_log.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-OPS-49 — npm devDependency HIGH CVE remediation (21 HIGH CVEs cleared; docs/security/security_register.md Audit 001)
- [ST-02] BLG-OPS-50 — Anthropic SDK upgrade 0.40.0 → 0.105.2 (docs/security/security_register.md Upgrade 001; AC-04 staging deferred: BLG-OPS-52)
- [ST-03] BLG-QA-40 — Wire Phase B CI with real Postgres service (.github/workflows/ci-tests.yml; 13 pre-existing failures fixed)
- [ST-04] BLG-QA-41 — Schema smoke test: lifecycle columns on positions table (tests/test_schema.py)
- [ST-05] BLG-GOV-78 — roadmap_prompt.md STEP 8.1 gate strengthening (v6.7→v6.8; OPERATIONAL_GUIDE.md v4.25→v4.26)

Sign-off: Product Owner — 2026-06-02
QA sign-off: Director of Quality — 2026-06-02

---

## v4.8 — Governance Hardening, Ops/Security Debt & SI-05 Phase 1 — 2026-06-02
Cycle: 2026-06-01__release-v4.8
Verified: Verified
Verification report: claude/cycles/2026-06-01__release-v4.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance & Compliance Hardening — §14 self-metadata Version corrected 4.20→4.24; §13 and §14 entries for all 7 Class 6 prompts verified present (ST-01); agent charter **Role:** header format verified compliant across all 23 agent files — pre-met in v4.5 EPIC-02 ST-05 (ST-02); all 3 v4.4 deferred patches confirmed resolved in v4.5 — AUD-2026-05-30-006 gap formally closed (ST-03). Sprint close governance patch: execution_prompt.md v3.34→v3.35 (LL-v4.8-EX-01 — commit SHA record immediately after push). | claude/system/OPERATIONAL_GUIDE.md v4.25; claude/system/prompt_change_log.md; claude/system/execution_prompt.md v3.35 |
| EPIC-02 | Operations, Security & QA Debt — Build minutes monitoring policy created (docs/operations/build_minutes_monitoring_policy.md v1.0): monthly allocation 400 min, 80% threshold, billing reset, double-capacity assessment (ST-04); dependency audit complete (docs/security/security_register.md v1.0): pip clean, 45 npm vulns (21 HIGH devDep); BLG-OPS-49/50 filed (ST-05); coverage matrix updated with compliance_summary regression point; GET /reports/monthly-pnl v0.6 contract verified (ST-06); SI-04 strategy version comparison endpoint contract pre-authored (docs/specs/api_contracts/strategy_version_comparison_contract.md v0.1.0; placeholder in openapi.yaml — ST-07). | docs/operations/build_minutes_monitoring_policy.md v1.0; docs/security/security_register.md v1.0; docs/qa/playwright_coverage_matrix.md v1.1; docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl (v0.6 confirmed); docs/specs/api_contracts/strategy_version_comparison_contract.md v0.1.0; docs/reference/openapi.yaml |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-69: §13 register completion — OPERATIONAL_GUIDE.md §14 updated; all 7 Class 6 prompts verified in §13 and §14
- [ST-02] BLG-GOV-70: Agent charter header compliance remediation — pre-met in v4.5; verified resolved across all 23 agent files
- [ST-03] BLG-GOV-72: AUD-2026-05-30-006 gap resolution verification — all 3 v4.4 deferred patches confirmed resolved in v4.5; gap formally closed
- [ST-04] BLG-OPS-46: Build minutes monitoring policy — docs/operations/build_minutes_monitoring_policy.md v1.0 created
- [ST-05] BLG-OPS-47: Dependency audit post-v4.7 — docs/security/security_register.md v1.0; BLG-OPS-49/50 filed
- [ST-06] BLG-QA-39: Coverage matrix update and v4.7 contract verification — docs/qa/playwright_coverage_matrix.md v1.1; GET /reports/monthly-pnl v0.6 verified
- [ST-07] BLG-SPEC-43: SI-04 strategy version comparison endpoint contract — strategy_version_comparison_contract.md v0.1.0 created; placeholder in openapi.yaml

Sign-off: Product Owner (agent-mediated) — 2026-06-02
QA sign-off: Director of Quality (agent-mediated) — 2026-06-02

---

## v4.7 — Arc 5 Completion Pre-work, Staged Verifications & Aged Backlog Clearance — 2026-06-01
Cycle: 2026-05-31__release-v4.7
Verified: Verified
Verification report: claude/cycles/2026-05-31__release-v4.7/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-04 §13 Formal Pre-Assessment — §13 review applied; determination PASS; 6 binding conditions documented; Arc 5 completion path cleared (ST-01) | docs/product/decisions/si04_section13_preassessment.md (new) |
| EPIC-02 | Arc 5 Compliance Score in Monthly P&L Report — compliance_summary field (validation_pass_rate, override_count, red_flag_events_count, most_frequent_rule_breach) added to GET /reports/monthly-pnl; field renamed strategy_compliance → compliance_summary; 2 unit tests + SC-REP-05a/05b Playwright scenarios (ST-03) | docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl (v0.6); docs/reference/openapi.yaml |
| EPIC-03 | Staging Verifications & Ops Housekeeping — RENDER_STAGING_DEPLOY_HOOK confirmed; code-change deploy and docs-only filter verified (ST-04); all 5 DS-07 SI-02 columns and 3 indexes confirmed on staging (ST-05); severity column, default assignment, backfill confirmed (ST-06); Render 7-day log retention documented; database audit tables confirmed durable (ST-07) | docs/ops/staging_deploy_verification.md; docs/ops/ds07_migration_staging_verification.md; docs/ops/severity_field_staging_verification.md; docs/specs/data_model.md; docs/ops/render_log_retention_policy.md |
| EPIC-04 | Cost & UX Assessments — no Anthropic API tier upgrade required; $5/month trigger threshold defined (ST-08); PreEntryValidationPanel UX reviewed; 3 improvement candidates ranked; BLG-FE-56/57/58 filed (ST-09) | docs/ops/anthropic_api_tier_assessment.md; docs/product/ux/pre_entry_panel_ux_assessment.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] SI-04 §13 Formal Pre-Assessment (BLG-GOV-62) — §13 gate PASS; Arc 5 SI-04 sprint planning now unblocked
- [ST-03] Arc 5 Compliance Score in Monthly P&L (BLG-FEAT-38) — additive compliance_summary section in monthly P&L report; aged 3+ cycles
- [ST-04] Staging Deploy Live Verification (BLG-OPS-28) — Render staging deploy workflow confirmed end-to-end; aged 4+ cycles
- [ST-05] DS-07 Migration Staging Verification (BLG-OPS-44) — v4.6 staging debt closed; all SI-02 schema changes confirmed on staging
- [ST-06] Severity Field Staging Verification (BLG-OPS-45) — v4.6 staging debt closed; severity column confirmed with correct backfill
- [ST-07] Render Log Retention Policy (BLG-OPS-31) — policy documented; database tables sufficient; no additional archiving required
- [ST-08] Anthropic API Tier Cost Assessment (BLG-OPS-37) — cost threshold defined; free tier adequate at current usage
- [ST-09] Pre-Entry Validation Panel UX Assessment (BLG-FE-49) — 3 UX improvement candidates filed as BLG-FE-56/57/58

Sign-off: Product Owner — 2026-06-01
QA sign-off: Director of Quality — 2026-06-01

---

## v4.6 — SI-02 Behavioural Drift Detection & Arc 5 Completion — 2026-05-31
Cycle: 2026-05-30__release-v4.6
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-30__release-v4.6/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | SI-02 Behavioural Drift Detection (Backend) — DS-07 data migration adding 5 SI-02 columns to trade_plans (ST-01); POST /trade-plans updated to capture 5 new SI-02 fields at plan creation (ST-02); 4-metric behavioural drift service (entry_timing_drift, sizing_adherence, consecutive_loss_sizing, regime_context; 90-day window; green/amber/red bands; §13 binding conditions enforced; ST-03); GET /analytics/behavioural-drift endpoint, openapi.yaml, and API contract (60 total endpoints; ST-04); 35-case SI-02 unit test suite (ST-05). | docs/specs/data_model/si02_data_schema.md; docs/specs/metrics/si02_drift_score.md; docs/specs/api_contracts/behavioural_drift_contract.md; docs/reference/openapi.yaml |
| EPIC-03 | Arc 5 Enablers & Gate-Cleared Items — red_flag_events severity field added (backfill + filter support; AC-08 Data Model sign-off accepted at EPIC level; ST-09); Arc 5 hosting cost projection assessment (current Render Starter tier adequate; no upgrade required at <50 trades; ST-10); Arc 5 nav cohesion review (maintain current structure; no changes recommended; ST-11); Red Flag Journal design review scope document (gate: 2026-06-21; ST-12). | docs/specs/api_contracts/portfolio_endpoints.md; docs/reference/openapi.yaml; docs/ops/arc5_hosting_cost_projection.md; docs/specs/frontend/arc5_nav_cohesion_review_v4.6.md; docs/specs/fe/rfj_design_review_scope.md |
| EPIC-04 | Governance, Spec Debt & OA Resolution — System_status_report.md v4.4 stale status correction (OA-01; ST-14); release_planning_prompt.md v2.33 gate scan + data density checkpoint (BLG-GOV-32/43; ST-15); closed trade count audit confirming data density gate NOT MET — 6 closed trades, 0 linked trade_plans (gate ≥20; EPIC-02 deferred 6th time; BLG-GOV-33; ST-16); Arc 4 data density risk trajectory assessment — Option A selected, gate dates ~Nov 2026 (SI-02), ~Sep 2026 (PT-04), ~Jun 2027 (PT-04 full; BLG-GOV-34; ST-17); Arc 6 Monte Carlo §13 pre-assessment — PASS with 10 binding conditions (BLG-GOV-45; ST-18); trade plan schema audit — 25 fields, 0 orphaned, 3 P3 process gaps (BLG-GOV-52; ST-19); sprint close automation investigation — workflow functioning as designed, no fix required (BLG-GOV-41; ST-20); external API integration spec template created (BLG-SPEC-32; ST-21); roadmap_prompt.md v6.7 next_release advisory added (OA-02; ST-22). | claude/system/release_planning_prompt.md v2.33; claude/system/roadmap_prompt.md v6.7; docs/product/decisions/arc4_data_density_trajectory_v4.6.md; docs/product/decisions/arc6_ps03_section13_preassessment.md; docs/specs/data_model/trade_plan_schema_audit_v4.6.md; docs/ops/sprint_close_reminder_investigation_v4.6.md; docs/specs/api_contracts/_external_api_template.md |

### Deviations accepted
2 minor deviations — see verification_report.md

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-DV4.6-01 | P3 | DS-07 migration staging verification pending — 5 SI-02 columns and 3 indexes not yet verified in staging environment; code-review verified; idempotent migration | DoQ + PO |
| DEV-DV4.6-02 | P3 | red_flag_events severity field staging ACs (AC-01/02/03) and AC-08 Data Model sign-off pending; code-review verified; idempotent migration pattern | DoQ + PO |

### Tech backlog items shipped
- [ST-15] BLG-GOV-32 + BLG-GOV-43: release_planning_prompt.md gate scan + data density checkpoint
- [ST-16] BLG-GOV-33: closed trade count audit (PT-04 + SI-02 data density gate)
- [ST-17] BLG-GOV-34: Arc 4 data density risk trajectory assessment
- [ST-18] BLG-GOV-45: Arc 6 Monte Carlo §13 pre-assessment
- [ST-19] BLG-GOV-52: trade plan schema field count gate check
- [ST-20] BLG-GOV-41: sprint close automation failure investigation
- [ST-21] BLG-SPEC-32: external API integration spec template
- [ST-09] BLG-BE-16: red_flag_events severity field
- [ST-10] BLG-OPS-40: Arc 5 hosting cost projection assessment
- [ST-11] BLG-FE-42: Arc 5 nav cohesion review
- [ST-12] BLG-FE-47: Red Flag Journal design review scope document

Sign-off: Product Owner — 2026-05-31
QA sign-off: Director of Quality — 2026-05-31

---

## v4.5 — Governance Prompt Hardening, Audit Debt & SI-02 Spec Pre-Planning — 2026-05-30
Cycle: 2026-05-30__release-v4.5
Verified: Verified
Verification report: claude/cycles/2026-05-30__release-v4.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance Prompt Patches — execution_prompt.md v3.34: two-phase DEL terminal-status write (sign_off_cleared at sign-off, commit_sha at push; ST-01); explicit pr_status sync in STEP 3.2.B after PR open + EPIC.status done→merged rule (ST-02); LL-v4.5-EX-01 verification-class sub-criterion for pre-planning sprints (ST-03); LL-v4.5-EX-02 spec_references policy for doc-creation stories (ST-04). All four v4.4 outstanding actions resolved. | claude/system/execution_prompt.md v3.34 |
| EPIC-02 | Agent Role Header Standardization — 5 agent files updated from `**Owner:**` to `**Role:**` format: api_contracts_documentation_owner.md, backend_engineering_patterns_owner.md, data_model_domain_schema_owner.md, frontend_specs_ux_documentation_owner.md, metrics_definitions_analytics_owner.md (AUD-2026-05-30-005 Tier 2 audit debt cleared; ST-05) | claude/agents/ — 5 agent files |
| EPIC-03 | SI-02 Spec Pre-Sprint — §13 formal boundary review (PASS; 9 binding conditions documented; ST-06); drift detection score metric definition (4 metrics; 90-day window; green/amber/red bands; SI-05 integration; ST-07); data schema pre-definition (5 new trade_plans columns; DS-07 migration script; ST-08). SI-02 sprint planning now unblocked. | docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md; docs/specs/metrics/si02_drift_score.md; docs/specs/data_model/si02_data_schema.md; docs/specs/si02_gap_analysis.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-75: execution_prompt.md two-phase DEL terminal-status write
- [ST-02] BLG-GOV-76: execution_prompt.md STEP 3.2.B pr_status sync after PR open
- [ST-03] BLG-GOV-77: execution_prompt.md verification-class sub-criterion for pre-planning sprints
- [ST-04] BLG-GOV-70: execution_prompt.md spec_references policy for documentation-creation stories
- [ST-05] AUD-2026-05-30-005: Agent file role header standardization (5 files)
- [ST-06] BLG-GOV-39: SI-02 §13 formal boundary review
- [ST-07] BLG-SPEC-41: SI-02 drift score metric definition
- [ST-08] BLG-SPEC-37: SI-02 data schema pre-definition

Sign-off: Product Owner — 2026-05-30
QA sign-off: Director of Quality — 2026-05-30

---

## v4.4 — Governance Patches, SI-02 Pre-Planning Sprint & Ops Hardening — 2026-05-30
Cycle: 2026-05-29__release-v4.4
Verified: Verified
Verification report: claude/cycles/2026-05-29__release-v4.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance Prompt Patches — roadmap_prompt.md v6.6 (STEP 8.1 empty-Now-horizon advisory; ST-01); sprint_planning_prompt.md v3.8 (frontend classification fast-path for React-only stories; ST-02); execution_prompt.md v3.33 (auto-set deviations_filed on delegation clearance; ST-03); qa_evidence_template.md v1.4 (delegated_qa DoQ sign-off both format variants; ST-04); release_planning_prompt.md v2.32 (STEP 7 RESUME PRECHECK note; ST-05) | claude/system/roadmap_prompt.md v6.6; claude/system/sprint_planning_prompt.md v3.8; claude/system/execution_prompt.md v3.33; claude/system/templates/qa_evidence_template.md v1.4; claude/system/release_planning_prompt.md v2.32 |
| EPIC-04 | Ops Documentation Hardening — OPERATIONAL_GUIDE.md v4.19 §7.9 "Staging URL Disambiguation" subsection added (frontend SPA URL vs backend API URL distinction; health check guidance updated; ST-13) | claude/system/OPERATIONAL_GUIDE.md v4.19 §7.9 |
| EPIC-02 | SI-02 Backend Pre-Planning — drift detection query pre-design + HBE sign-off (ST-06); Arc 5 backend architecture review + ADR-001 cached-synchronous Option B recommendation (ST-07); query index pre-assessment with 3 migration-candidate indexes (ST-08); background job ADR-SI02-001 cached-synchronous selected, no worker/Redis/Celery on Render (ST-09) | docs/specs/si02/si02_query_predesign.md; docs/specs/si02/arc5_backend_architecture_review.md; docs/specs/si02/si02_index_preassessment.md; docs/specs/si02/si02_background_job_adr.md |
| EPIC-03 | SI-02 Frontend & QA Pre-Planning — drift detection result component pre-design (Option B percentage-deviation display, 4 component states; ST-10); interaction spec (5 states, non-dismissable, 13 Playwright DFT IDs; ST-11); Playwright scenario pre-design DFT-01–DFT-13 + 4 staging-only scenarios S-STG-01–S-STG-04 (ST-12) | docs/specs/si02/si02_fe_component_predesign.md; docs/specs/si02/si02_fe_interaction_spec.md; docs/qa/si02_playwright_predesign.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-71: roadmap_prompt.md STEP 8.1 advisory for empty Now horizon after Extended-tier rebalance
- [ST-02] BLG-GOV-72: sprint_planning_prompt.md frontend classification fast-path for React-only stories
- [ST-03] BLG-GOV-73: execution_prompt.md auto-set deviations_filed on delegation sign-off clearance
- [ST-04] BLG-GOV-69 + BLG-GOV-74: qa_evidence_template.md DoQ sign-off format for delegated_qa EPICs (both format variants)
- [ST-05] Release planning STEP 7 RESUME PRECHECK patch (v4.3 LL-2 carry-forward)
- [ST-06] BLG-BE-17: SI-02 drift detection query pre-design
- [ST-07] BLG-BE-18: Arc 5 backend architecture review for SI query patterns
- [ST-08] BLG-BE-23: SI-02 query index pre-assessment
- [ST-09] BLG-BE-20: SI-02 background job architecture design
- [ST-10] BLG-FE-52: SI-02 drift detection result component pre-design
- [ST-11] BLG-FE-53: SI-02 drift detection interaction spec
- [ST-12] BLG-QA-31: SI-02 Playwright scenario pre-design (DFT-01–DFT-13)
- [ST-13] BLG-OPS-43: Staging URL disambiguation in OPERATIONAL_GUIDE §7

Sign-off: Product Owner — 2026-05-30
QA sign-off: Director of Quality — 2026-05-30

---

## v4.3 — Governance Consolidation, QA Debt Clearance & Ops Hardening — 2026-05-29
Cycle: 2026-05-29__release-v4.3
Verified: Verified
Verification report: claude/cycles/2026-05-29__release-v4.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | v4.2 Governance Patch Resolution — execution_prompt.md v3.31→v3.32 (STEP 3.2.A qa_signed_off advisory; STEP 5.3/8 branch safety hard gate); qa_evidence_template.md v1.2→v1.3 (1:1 AC mapping advisory); OPERATIONAL_GUIDE.md v4.12→v4.13 (§7.8 staging-only AC pre-designation reference table); AI feature inventory document v1.0 (3 features with §13 compliance status) (ST-01–05) | claude/system/execution_prompt.md v3.32; claude/system/templates/qa_evidence_template.md v1.3; claude/system/OPERATIONAL_GUIDE.md v4.13; docs/ai/ai_feature_inventory.md |
| EPIC-04 | Frontend Fixes & Arc 5 P&L Section — pre-entry check entry price bug fix (PreEntryValidationPanel entryPrice/stopPrice props + URL params; SC-TP-21); Claude thesis generation UI copy audit (HAS_GEMINI→HAS_AI, isGeminiLoading→isAiLoading; SC-TP-22); Arc 5 compliance score in monthly P&L report (backend get_arc5_compliance_summary() + monthly-pnl strategy_compliance field; frontend Strategy Compliance section with 4 metric cards; SC-REP-05a/05b) (ST-16–18) | docs/specs/api_contracts/pre_entry_validation.md; docs/specs/frontend/pages/trade_plan.md; docs/specs/frontend/pages/reports.md; docs/specs/api_contracts/reports_endpoints.md v0.5; docs/specs/api_contracts/arc5_compliance_analytics.md |
| EPIC-03 | Ops & Security Documentation Hardening — API key rotation policy v1.0 + external API key security register v1.0 (5 credentials, 8-step staging-first procedure); staging environment parity audit v4.3 (env vars, DB schema, 4 endpoint health checks); claude-audit-log performance baseline §16 (p50=2,541ms, p95=2,858ms; BLG-OPS-42 closed); ANTHROPIC_API_KEY added to staging permanently (ST-13–15) | docs/ops/api_key_rotation_policy.md; docs/security/api_key_security_register.md; docs/ops/staging_parity_report_v4.3.md; docs/ops/api_performance_baseline.md v2.0 §16 |
| EPIC-02 | QA Debt Clearance — Playwright E2E for Arc5ComplianceSection (4 tests: SC-ARC5-01/02/03/04); Arc 5 E2E integration test spec v1.0 (20 scenarios); CI pipeline baseline v1.0 (p50=444s; BLG-QA-27 gate cleared); Playwright coverage matrix v1.0 (39 spec files) + Arc 5 coverage audit v1.0 (18 scenarios, 100% coverage); staging verifications: Claude thesis (AC-01/02/03 pass), ticker validation (HTTP 422 confirmed), Claude API cost alert (Telegram received) (ST-06–12) | docs/qa/arc5_e2e_integration_test_spec.md; docs/ops/ci_pipeline_baseline.md; docs/qa/playwright_coverage_matrix.md; docs/qa/arc5_coverage_audit.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] OA-1 (v4.2): execution_prompt.md STEP 3.2.A qa_signed_off advisory patch
- [ST-02] OA-2 (v4.2): execution_prompt.md STEP 5.3/STEP 8 sprint close branch safety hard gate
- [ST-03] OA-3 (v4.2): qa_evidence_template.md AC mapping 1:1 advisory
- [ST-04] BLG-GOV-42: staging-only AC pre-designation reference table
- [ST-05] BLG-GOV-47: AI feature inventory document
- [ST-06] BLG-QA-29: staging verification — Claude thesis generation
- [ST-07] BLG-QA-30: staging verification — ticker validation Yahoo Finance rejection path
- [ST-08] BLG-QA-35: staging verification — Claude API daily cost threshold alert
- [ST-09] BLG-QA-28: Playwright E2E coverage for Arc5ComplianceSection
- [ST-10] BLG-QA-36: Arc 5 end-to-end integration test specification
- [ST-11] BLG-QA-38: CI pipeline execution time baseline measurement
- [ST-12] BLG-QA-32 + BLG-QA-33: Playwright scenario coverage matrix + Arc 5 coverage audit
- [ST-13] BLG-OPS-33: staging environment parity audit
- [ST-14] BLG-OPS-42: claude-audit-log performance baseline (GET /ai/claude-audit-log)
- [ST-15] BLG-GOV-36 + BLG-GOV-50: API key rotation policy + external API key security register
- [ST-16] BLG-FE-50: pre-entry check entry price bug fix
- [ST-17] BLG-FE-51: Claude thesis generation UI copy audit (Gemini→AI variable rename)
- [ST-18] BLG-FE-38: Arc 5 compliance score in monthly P&L report

Sign-off: Product Owner — 2026-05-29
QA sign-off: Director of Quality — 2026-05-29

---

## v4.2 — Claude API Governance, SI-02 Pre-Work Readiness & Spec Debt — 2026-05-29
Cycle: 2026-05-27__release-v4.2
Verified: Verified
Verification report: claude/cycles/2026-05-27__release-v4.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Claude API Compliance & Security — Anthropic API accountability formally assigned (AI Compliance Officer charter §4.1 updated); ANTHROPIC_API_KEY security posture confirmed (docs/security/anthropic_api_key_scope_review.md, 3 sign-offs); model version pinning policy created (docs/governance/ai_model_version_pinning_policy.md v1.0; env-var override removed from ai_service.py); Claude API log hygiene policy produced and activated (docs/ops/claude_api_log_hygiene_policy.md v1.0; Render log inspection confirmed clean) (ST-01/02/03) | docs/security/anthropic_api_key_scope_review.md; claude/agents/ai_compliance_governance_officer.md; docs/governance/ai_model_version_pinning_policy.md; backend/services/ai_service.py; docs/ops/claude_api_log_hygiene_policy.md |
| EPIC-02 | Operational Monitoring & Baselines — POST /ai/check-daily-cost baseline added (p50=205ms, p95=518ms; 5 staging samples); Claude API first monthly cost review produced ($0.007387/6 calls; monthly cadence + $5/month alert threshold defined); Claude API thesis generation latency baseline established (p50=3,560ms, p95=3,923ms; 10 warm production samples; regression threshold 2× baseline) (ST-04/05/06) | docs/ops/api_performance_baseline.md v1.6→v1.7; docs/ops/claude_cost_review_2026-05.md |
| EPIC-03 | Gemini→Claude Spec Debt Clearance — claude_audit_log table + ensure/create/query functions in database.py; GET /ai/claude-audit-log endpoint; ai_endpoints.md v1.2; gemini_thesis_generation.md renamed to ai_thesis_generation.md v2.1.0 (Claude API token fields added); gemini_thesis_generation.md superseded; openapi.yaml updated; Claude API Playwright mock strategy document produced; prompt caching assessment: DEFER (prefix <1,024 tokens; <10 calls/day) (ST-07/08/09/10) | docs/specs/api_contracts/ai_endpoints.md v1.2; docs/specs/api_contracts/ai_thesis_generation.md v2.1.0; docs/specs/api_contracts/gemini_thesis_generation.md (Superseded); docs/reference/openapi.yaml; backend/database.py; backend/routers/ai.py; docs/team_skills/quality/claude_api_playwright_mock_strategy.md; docs/governance/claude_prompt_caching_assessment.md |
| EPIC-04 | SI-02/SI-04 Pre-Planning — si02_prerequisites_checklist.md v1.0 (13 items: 4 Complete, 1 gate-conditional, 8 Open); si04_scope_definition.md v1.0 (5 metrics, date-range versioning, comparison UI concept); v4.1 staging deviation trend review (IMPROVED: v4.1=2 vs v4.0=4); backlog namespace audit (287 BLG IDs, 0 collisions) (ST-11/12/13) | docs/governance/si02_prerequisites_checklist.md; docs/governance/si04_scope_definition.md; docs/governance/v41_staging_deviation_review.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-GOV-66 + BLG-GOV-65: Anthropic API accountability assignment + API key security review
- [ST-02] BLG-GOV-64: Anthropic model version pinning policy
- [ST-03] BLG-OPS-38: Claude API log hygiene policy
- [ST-04] BLG-OPS-35: API performance baseline — POST /ai/check-daily-cost (OA-3 resolution)
- [ST-05] BLG-OPS-36: Claude API first monthly cost review
- [ST-06] BLG-OPS-39: Claude API thesis generation latency baseline
- [ST-07] BLG-GOV-63: Claude API audit trail implementation
- [ST-08] BLG-SPEC-42: AI thesis API contract update for Claude
- [ST-09] BLG-QA-37: Claude API Playwright mock strategy
- [ST-10] BLG-BE-22: Claude API prompt caching assessment (deferred)
- [ST-11] BLG-GOV-60: SI-02 sprint planning prerequisites checklist
- [ST-12] BLG-GOV-57: SI-04 strategy version comparison pre-planning
- [ST-13] BLG-GOV-61 + BLG-GOV-59: v4.1 staging sign-off review + backlog namespace audit

Sign-off: Product Owner — 2026-05-29
QA sign-off: Director of Quality — 2026-05-29

---

## v4.1 — Governance Hardening, Spec Debt, Arc 5 Compliance + SI-02 Pre-Planning — 2026-05-27
Cycle: 2026-05-26__release-v4.1
Verified: Verified
Verification report: claude/cycles/2026-05-26__release-v4.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Governance prompt hardening — execution_prompt.md v3.27→v3.28 (merge-gate re-invocation HARD GATE after every EPIC merge; OA-01 resolved); sprint_planning_prompt.md v3.6→v3.7 (mandatory staging-only AC check at STEP 6.2 sign-off gate; OA-02 resolved); shared_standards.md v3.3→v3.4 (sprint_backlog.md template [REQUIRED] enforcement); delivery_verification_prompt.md v2.5→v2.6 (STEP -1.3A PR Number Recovery; OA-04 resolved) (ST-01/02/03) | claude/system/execution_prompt.md; claude/system/sprint_planning_prompt.md; claude/system/shared_standards.md; claude/system/delivery_verification_prompt.md |
| EPIC-02 | API contract spec debt clearance — four undocumented v3.8/v3.9/v4.0 endpoints verified and formally contracted: red_flag_journal.md v1.0.0 (SI-03), pre_entry_validation.md v1.0.0 (SI-01), arc5_compliance_analytics.md v1.0.0 (Arc 5), gemini_thesis_generation.md v2.0.0 (AI thesis); all openapi.yaml entries confirmed (ST-04/05/06/07) | docs/specs/api_contracts/red_flag_journal.md; docs/specs/api_contracts/pre_entry_validation.md; docs/specs/api_contracts/arc5_compliance_analytics.md; docs/specs/api_contracts/gemini_thesis_generation.md; docs/reference/openapi.yaml |
| EPIC-03 | Arc 5 P&L integration + Claude API cost alerting + frontend spec — metrics_definitions.md v1.10→v1.11 (Arc 5 composite score formula); reports.md v0.2→v0.3 (Arc 5 Compliance Summary section); POST /ai/check-daily-cost endpoint with Telegram alert ($1.00 default threshold) + 5 unit tests; research_view.md v1.1→v1.2 (signal_type Setup Type field + 4 Playwright tests); arc5_compliance_section.md v1.0 created (ST-08/09/10) | docs/specs/metrics_definitions.md; docs/specs/frontend/pages/reports.md; docs/specs/api_contracts/ai_endpoints.md v1.1; docs/specs/frontend/pages/research_view.md; docs/specs/frontend/components/arc5_compliance_section.md; docs/reference/openapi.yaml |
| EPIC-04 | SI-02 pre-planning + security review + operational reviews — si02_gap_analysis.md (5 gaps enumerated); section13_criteria.md, data_prerequisite_audit.md (gate NOT met: <20 closed trades), query_performance_assessment.md; ANTHROPIC_API_KEY scope review + credential inventory v1.1; delivery_verification_prompt.md v2.6→v2.7 (STEP 9.0 artefact presence check); OPERATIONAL_GUIDE.md v4.05→v4.06; api_performance_baseline.md v1.4→v1.5; gemini_cost_tracking.md v1.1→v1.2; pnl_attribution_gate_check.md v1.0 (ST-12/13/14/15) | docs/specs/si02_gap_analysis.md; docs/specs/si02/section13_criteria.md; docs/specs/si02/data_prerequisite_audit.md; docs/specs/si02/query_performance_assessment.md; docs/security/anthropic_api_key_scope_review.md; docs/ops/external_api_credential_inventory.md v1.1; claude/system/delivery_verification_prompt.md; docs/ops/api_performance_baseline.md; docs/ops/gemini_cost_tracking.md; docs/ops/pnl_attribution_gate_check.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] OA-01 (2nd-recurrence): execution_prompt.md merge-gate re-invocation as hard gate
- [ST-02] OA-02 (2nd-recurrence): sprint_planning_prompt.md staging-only AC designation at planning
- [ST-03] OA-04: delivery_verification_prompt.md PR number null guard (STEP -1.3A)
- [ST-04] BLG-SPEC-33: SI-03 Red Flag Journal API contract document
- [ST-05] BLG-SPEC-34: SI-01 Pre-Entry Validation API contract document
- [ST-06] BLG-SPEC-40: Arc 5 analytics endpoint API contract
- [ST-07] BLG-SPEC-38: AI thesis endpoint API contract (Claude API)
- [ST-08] BLG-FEAT-40 + BLG-FEAT-42: Arc 5 compliance metrics P&L integration (composite score formula + Reports page section)
- [ST-09] BLG-OPS-34: Claude API daily cost threshold alert via Telegram
- [ST-10] BLG-FE-44 + BLG-FE-48: Research view signal_type field + Arc5ComplianceSection component spec
- [ST-12] BLG-SPEC-39: SI-02 data model gap analysis
- [ST-13] BLG-GOV-44 + BLG-GOV-46 + BLG-GOV-51: SI-02 pre-planning (§13 criteria + data audit + query performance)
- [ST-14] BLG-GOV-49 + BLG-GOV-54 + BLG-GOV-56: Security review (ANTHROPIC_API_KEY) + SI-05 annotation + delivery_verification_prompt.md STEP 9.0
- [ST-15] BLG-OPS-29 + BLG-OPS-30 + BLG-OPS-32: API performance baseline v1.5 + first Claude usage review + P&L attribution gate check

Sign-off: Product Owner — 2026-05-27
QA sign-off: Director of Quality — 2026-05-27

---

## v4.0 — Arc 5 Analytics Foundation + Spec Closure + Gemini Compliance — 2026-05-25
Cycle: 2026-05-22__release-v4.0
Verified: Verified
Verification report: claude/cycles/2026-05-22__release-v4.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Arc 5 compliance analytics — GET /analytics/arc5-compliance delivering validation_pass_rate_by_rule, events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate; pre_entry_validation_log table; Arc5ComplianceSection.js frontend on PerformanceAnalytics §19; SI-01→SI-03 Playwright integration suite (8 scenarios) (ST-01/02/03/04) | docs/specs/api_contracts/analytics_endpoints.md v2.2.0; docs/specs/metrics_definitions.md#Arc 5 Compliance Metrics; docs/design/2026-05-22__release-v4.0/arc5-analytics-metrics/ux_spec.md; docs/reference/openapi.yaml |
| EPIC-02 | Ticker Quality & Security — live Yahoo Finance symbol validation at POST /ticker-universe (HTTP 422 on unknown symbol; SKIP_TICKER_VALIDATION CI bypass); red flag endpoint auth/PII security review (PASS); starlette CVE remediation (starlette==1.0.1; PYSEC-2026-161 closed) (ST-05/06/13) | docs/specs/api_contracts/ticker_universe_api_contract.md v1.2; docs/specs/api_contracts/red_flag_journal.md; backend/requirements.txt |
| EPIC-03 | AI Governance & CI/CD — Gemini Flash base wiring (POST /trade-plans/{plan_id}/generate-thesis; "Improve with AI" button on TradePlan edit); gemini_audit_log table (fire-and-forget, 90-day retention); token/cost tracking ($0.075/$0.30 per M tokens; 800k alert threshold); CI/CD staging auto-deploy (.github/workflows/staging-deploy.yml with path filter) (ST-07/08/09/12) | docs/specs/api_contracts/trade_plan_endpoints.md v0.3; docs/ops/gemini_cost_tracking.md; backend/routers/test.py (60→61) |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-FEAT-36: SI-01 validation pass/fail rate by rule — backend metric endpoint
- [ST-02] BLG-FEAT-37: Red flag event frequency metric — backend + frontend
- [ST-03] BLG-QA-25: E2E Playwright test — SI-01→SI-03 integration path
- [ST-04] BLG-FEAT-39: Trade plan adherence rate metric — backend + frontend
- [ST-05] BLG-BE-15: Validate ticker symbol on add
- [ST-06] BLG-GOV-37: Red flag endpoint auth and PII review
- [ST-07] BLG-GOV-35: Gemini audit trail — log AI thesis generation calls
- [ST-08] BLG-OPS-26: Gemini cost tracking — token usage and cost per call
- [ST-09] BLG-OPS-27: CI/CD automated staging re-deploy on main merge
- [ST-12] BLG-BE-19: Gemini Flash base wiring (hard-prerequisite; AMD-20260523-01)
- [ST-13] CVE PYSEC-2026-161: Starlette security upgrade to ≥1.0.1 (emergency; AMD-20260523-01)

Sign-off: Product Owner — 2026-05-25
QA sign-off: Director of Quality — 2026-05-25

---

## v3.9 — Screener Quality & Reliability + Arc 5 Red Flag Journal + Governance Patches — 2026-05-22
Cycle: 2026-05-21__release-v3.9
Verified: Verified
Verification report: claude/cycles/2026-05-21__release-v3.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Screener Data Quality & Reliability: Yahoo Finance crumb/401 retry with exponential backoff+jitter (ST-01); sector/industry fields restored to screener results (ST-02); invalid ticker DAY removed with startup deactivation (ST-03); degraded-run warning banner when >20% fetch failures (ST-04) | backend/services/screener_data_service.py; backend/services/screener_batch_service.py; docs/specs/frontend/pages/screener_results.md; docs/specs/api_contracts/screener_api_contract.md v1.1; docs/reference/openapi.yaml |
| EPIC-02 | Ticker Universe Enhancements: .L suffix stripped from display labels while preserving API requests (ST-05); company_name column added with CSV backfill and management page display (ST-06) | docs/specs/frontend/pages/ticker_universe.md; docs/specs/api_contracts/ticker_universe_api_contract.md |
| EPIC-03 | Arc 5 Red Flag Journal (SI-03): red_flag_events table; GET /portfolio/red-flag-journal endpoint (paginated, filterable by event_type/ticker/since); SI-01 override event write path; RedFlagJournal.js frontend with filters, pagination, empty state, Trading nav link (ST-07/08) | docs/specs/api_contracts/portfolio_endpoints.md v2.3; docs/specs/frontend/pages/red_flag_journal.md; docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md; docs/reference/openapi.yaml; backend/routers/test.py (59→60) |
| EPIC-04 | Governance Patches — all 5 v3.8 carry-forward items resolved: execution_prompt.md v3.26 (test_scenarios scope rule + createPageUrl delegation note); sprint_planning_prompt.md v3.4 (deferred_at_planning state); release_planning_prompt.md v2.31 + delivery_verification_prompt.md v2.5 (--dry-run support); PR template v1.2 (QA evidence pre-merge checklist) (ST-09/10/11/12) | claude/system/execution_prompt.md v3.26; claude/system/sprint_planning_prompt.md v3.4; claude/system/release_planning_prompt.md v2.31; claude/system/delivery_verification_prompt.md v2.5; .github/pull_request_template.md v1.2 |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01] BLG-TECH-10: Fix Yahoo Finance crumb/401 rate-limiting in screener batch
- [ST-02] BLG-BE-10: Fix sector/industry data dropped in screener batch
- [ST-03] BLG-BE-11: Remove DAY from ticker universe (invalid Yahoo Finance symbol)
- [ST-04] BLG-FE-38: Add degraded-run warning to screener when OHLCV failure rate exceeds 20%
- [ST-05] BLG-FE-37: Strip .L suffix from Ticker Universe page display labels
- [ST-06] BLG-BE-12: Add company_name column to ticker universe
- [ST-11] BLG-GOV-25: Add --dry-run support to plan release and run delivery verification engines

Sign-off: Product Owner — 2026-05-22
QA sign-off: Director of Quality — 2026-05-22

---

## v3.8 — Arc 5 Strategy Integrity Foundation + Trade Plan Form Enhancements + Ticker Universe Management — 2026-05-20
Cycle: 2026-05-19__release-v3.8
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-19__release-v3.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-04 | Ticker Universe Management Page (ST-09): TickerUniverse.js page with add/toggle/delete/filter; `public.tickers` startup sync retired; `ticker_universe` is sole authoritative source. Governance Debt Clearance (ST-10): gh_issue_template.md added to §14; DoQ enforcement via PR template; OPERATIONAL_GUIDE.md v3.90→v3.92. | docs/specs/api_contracts/ticker_universe_api_contract.md; claude/system/OPERATIONAL_GUIDE.md#§14 |
| EPIC-03 | Setup Type Classification Field (ST-06): `setup_type` dropdown on trade plan form, 6 options, persisted. News Context Panel (ST-07): collapsible Alpaca news panel on trade plan form, localStorage-persisted collapse state. AI-Assisted Thesis Generation (ST-08): "Generate thesis" template engine + "Improve with AI" (Gemini-gated). | docs/specs/api_contracts/trade_plan_endpoints.md; docs/specs/frontend/pages/trade_plan.md |
| EPIC-01 | §13 Review Gate for SI-01 (ST-01): 8 binding conditions documented; Category A + B checks authorised. SI-01 Backend (ST-02): `strategy_rules.md` v1.4 §4.2; `GET /portfolio/pre-entry-validation`; 17 unit tests; conftest.py stubs (BLG-QA-20 resolved). SI-01 Frontend (ST-03): PreEntryValidationPanel with override acknowledgement checkbox on trade plan form; SC-TP-17–20 Playwright pass. | docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/pre-entry-validation; docs/specs/frontend/pages/trade_plan.md; docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md |

### Deviations accepted
| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-EPIC04-ST09-01 | P3 | createPageUrl map missing TickerUniverse entry at time of EPIC-04 PR merge — resolved in same release (fix commit 75b7eda4, PR #456) | PO + DoQ |

### Tech backlog items shipped
- [ST-09] BLG-FEAT-22: Ticker Universe Management page
- [ST-10] BLG-GOV-24 + DoQ OA: Governance debt clearance (gh_issue_template.md §14 + PR template enforcement)
- [ST-06] BLG-FEAT-23: Setup type classification field on trade plans
- [ST-07] BLG-FE-36: News context panel on trade plan form
- [ST-08] BLG-FEAT-24: AI-assisted setup thesis generation

Sign-off: Product Owner — 2026-05-20
QA sign-off: Director of Quality — 2026-05-20

---

## v3.7 — Signal-to-Watchlist Workflow + Arc 2 Completion + Governance Hardening — 2026-05-18
Cycle: 2026-05-18__release-v3.7
Verified: Verified
Verification report: claude/cycles/2026-05-18__release-v3.7/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Signal-to-Watchlist Workflow (S2-01): `watchlisted` status added to signals table CHECK constraint; `PATCH /signals/{id}` accepts `status: "watchlisted"`; `SignalCard.js` primary CTA replaced with "Add to Watchlist" with watchlisted state badge; `SignalContextPanel.js` read-only signal context panel in trade plan form with entry_rationale + confirmation_criteria pre-population; 7 Playwright scenarios SC-SIG-WL-01/02/03 (signals-add-to-watchlist.spec.js) + SC-TP-SIG-01/02/03/04 (trade-plan-signal-context.spec.js) | docs/specs/api_contracts/signal_endpoints.md v1.2; docs/specs/data_model.md v2.8; docs/specs/frontend/pages/signals.md; docs/specs/frontend/pages/trade_plan.md; docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md |
| EPIC-03 | Governance hardening patches (S2-03): execution_prompt.md v3.23→v3.24 (deviations_filed atomic write, backlog verify guidance, spec_references path verify guidance); qa_evidence_template.md v1.0→v1.1 (BLG-GOV-19 criterion 3 fail-path); retroactive prompt_change_log.md entries for v3.18–v3.22 gap | claude/system/execution_prompt.md; claude/system/templates/qa_evidence_template.md |
| EPIC-04 | Tech debt clearance (S2-04): BLG-QA-20 database stub conftest consolidation (session-scoped `types.ModuleType("database")` stub in tests/conftest.py; CLAUDE.md §2 updated); BLG-OPS-16 pycache git hygiene (git rm -r --cached + .gitignore); BLG-FE-35 Research page typography staging sign-off (SC-RV-TYP-01 Playwright regression); BLG-GOV-23 scored_initiatives.md Arc 3–6 comprehensive refresh (OA-RP-05 resolved) | docs/frontend/design_system.md; claude/scoring/scored_initiatives.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-09] BLG-QA-20: Database stub conftest consolidation
- [ST-10] BLG-OPS-16 + BLG-FE-35: Pycache git hygiene + Research page typography staging sign-off
- [ST-11] BLG-GOV-23: scored_initiatives.md Arc 3–6 comprehensive refresh (resolves OA-RP-05)

Sign-off: Product Owner — 2026-05-18
QA sign-off: Director of Quality — 2026-05-18

---

## v3.6 — Arc 4 Data Integrity + Research Debt Clearance + Governance Patches — 2026-05-17
Cycle: 2026-05-16__release-v3.6
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-16__release-v3.6/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Arc 4 Data Integrity (S2-01): `planned_entry_price` column added to trade_history (nullable; ALTER TABLE IF NOT EXISTS); `exit_position()` captures signal's current_price at entry; `_compute_entry_delta_pct()` calculates (actual−planned)/planned×100; `PlanVsReality` component updated to display entry_delta_pct with emerald (favorable) / rose (unfavorable) colouring; null → 'data not available for historical trades'; 9 Playwright scenarios (SC-PVR-03a/b, SC-PVR-04a/b, SC-PVR-05a/b/c) | docs/specs/arc4/arc4_data_requirements.md §3.1; docs/specs/frontend/pages/trade_history.md §Expandable Journal Row — Plan vs Reality; openapi.yaml (planned_entry_price field added to TradeHistoryResponse) |
| EPIC-03 | Research QA/Spec/UX Debt (S2-03): SC-RV-18 and SC-RV-19 Playwright tests added (RESEARCH_REGIME_NULL, RESEARCH_ALL_NULL payloads); research_endpoint.md v1.2 §Error Responses updated; `_get_price_data()` returns `_YF_UNAVAILABLE`/`_TICKER_NOT_FOUND` sentinels → HTTP 503/404; partial failures still 200+nulls; Research.js error state shows specific messages; regime lozenge `whitespace-nowrap` fix (BLG-FE-26 wrapping bug) | docs/specs/api_contracts/research_endpoint.md v1.2; docs/qa/test_scenarios/research_view_scenarios.md v1.1; openapi.yaml (404/503 responses added); docs/frontend/design_system.md |
| EPIC-04 | Governance Patches (S2-04): execution_prompt.md v3.21→v3.22 — §13 gate story pattern formalised (LL-v3.5-SP-01); metadata + sprint_close + Phase 3 deferred patches applied; retroactive prompt_change_log.md entries for v3.18–v3.22 gap; OA-RP-01–04 resolved | claude/system/execution_prompt.md v3.22; OPERATIONAL_GUIDE.md §8+§14; claude/system/prompt_change_log.md |

### Deviations accepted
1 minor P3 deviation: ST-08 AC-02 — research page regime lozenge human staging sign-off deferred; backlog item BLG-FE-33 filed

### Tech backlog items shipped
- [ST-06] BLG-FE-32 + TEST-GAP-EPIC-03-v33: SC-RV-18 and SC-RV-19 Playwright coverage
- [ST-07] BLG-SPEC-27: Research endpoint HTTP 404/503 error code differentiation
- [ST-08] BLG-FE-26: Research page regime lozenge wrapping fix
- [ST-09] Governance: execution_prompt.md §13 gate story pattern formalisation + retroactive changelog entries (OA-RP-01–04)
- [ST-10] Governance: execution_prompt.md metadata + sprint_close + Phase 3 patches

### Deferred
- EPIC-02 (PT-04 Arc 2 Quality Score) — deferred to v3.7; PT-04 gate condition (≥20 closed trades) unconfirmed at sprint planning

Sign-off: Product Owner — 2026-05-17
QA sign-off: Director of Quality — 2026-05-17

---

## v3.5 — Arc 3 Completion + Arc 4 Foundation — 2026-05-15
Cycle: 2026-05-15__release-v3.5
Verified: Verified
Verification report: claude/cycles/2026-05-15__release-v3.5/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Arc 3 Completion — IT-06 Alpaca Paper Trading: §13 compliance review (PASS; four binding conditions documented); backend sync service `alpaca_paper_sync_service.py` + `GET /portfolio/paper-positions` endpoint (best-effort US market position mirroring); `PaperAccountPanel` frontend component on Positions page; 5 Playwright scenarios (SC-PA-01a/b/c, SC-PA-02a/b) | claude/strategy/strategy_rules.md#§13; docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md; docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/paper-positions; docs/ux_specs/paper-trading/ux_spec.md |
| EPIC-02 | Arc 4 Foundation — Arc 4 data requirements capture (`docs/product/arc4_data_requirements.md` v1.0, PO + HoUX sign-off); PO-01 Plan vs Reality backend calculation service + `GET /trades/{id}/plan-vs-reality` endpoint + `plan_vs_reality` JSONB field migration; `PlanVsReality` frontend component in TradeHistoryTable; 5 Playwright scenarios (SC-PVR-01a/b/c, SC-PVR-02a/b) | docs/specs/api_contracts/trade_endpoints.md#GET /trades/{trade_id}/plan-vs-reality; docs/data_model.md#trade_history; docs/data_model.md#trade_plans; docs/ux_specs/plan-vs-reality/ux_spec.md |
| EPIC-03 | Spec & QA Debt: BLG-SPEC-29 grace-period-alert ux_spec.md §5 sessionStorage correction; BLG-SPEC-30 stop-management-workflow ux_spec.md §4.4 PATCH correction; BLG-SPEC-31 React Query v5 onSuccess scan (1 fix applied TradePlan.js; SC-TP-08 Playwright 9/9); BLG-QA-19 research view regression protocol v1.0 | docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md; docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md; docs/qa/acceptance_protocols/research_view_regression_protocol.md |
| EPIC-04 | Governance Patches: BLG-GOV-22 sprint_planning_prompt.md v3.1 (shared execution_state.json ownership rule + multi-EPIC merge guidance); execution_prompt.md v3.20 (intent-check advisory, Known Deviations sync advisory, backlog ID uniqueness check, sprint_close readiness consistency rule, BLG ID completeness check) | claude/system/sprint_planning_prompt.md; claude/system/execution_prompt.md |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-07] BLG-SPEC-29: Correct grace-period-alert ux_spec.md §5 dismiss storage to sessionStorage
- [ST-08] BLG-SPEC-30: Correct stop-management-workflow ux_spec.md §4.4 stop-update HTTP verb to PATCH
- [ST-09] BLG-SPEC-31: React Query v5 onSuccess codebase scan and fix (TradePlan.js)
- [ST-10] BLG-QA-19: Research view regression test protocol
- [ST-04] BLG-GOV-21: Arc 4 data requirements capture
- [ST-11] BLG-GOV-22: sprint_planning_prompt.md shared ownership patch

Sign-off: Product Owner — 2026-05-15
QA sign-off: Director of Quality — 2026-05-15

---

## v3.4 — Arc 3 In-Trade Risk Management (continued) — 2026-05-14
Cycle: 2026-05-14__release-v3.4
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-14__release-v3.4/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Arc 3 Frontend Completion (IT-01/02/03): LifecycleBadge component on positions page (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN states) with arc3_lifecycle_display feature flag guard; GracePeriodAlertZone with sessionStorage dismiss; TrailStopModal with PATCH /positions/{id} stop update. 10/10 Playwright scenarios pass | docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md; docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md; docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md |
| EPIC-02 | Arc 3 Risk Prompts (IT-04/05): GET /portfolio/drawdown-status backend (drawdown % from peak, threshold breach, open positions by state); DrawdownReviewPrompt component (§13 display-only, session-scoped dismiss); GET /portfolio/concentration-status backend (per-position/sector heat); ConcentrationLimitsWarning component (DS-03 graceful degradation). 10/10 Playwright scenarios pass | docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md; docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md; docs/reference/openapi.yaml |
| EPIC-03 | Frontend Quick Wins: Research page UK suffix strip (BLG-FE-23); negative/zero earnings days display (BLG-FE-24); Signals page defaults to most recent day (BLG-FE-25); Watchlist research status indicator (BLG-FE-29); Trade plan status badges + abandonment UI (BLG-FE-30 + BLG-FEAT-21 frontend). 16/16 Playwright scenarios pass | docs/specs/frontend/pages/trade_plan.md#9 |
| EPIC-04 | Spec & QA Debt: Research view component library (BLG-FE-31); Screener morning routine UX spec (BLG-FE-22); trade_plan.md §6.2 entry checklist field references updated (BLG-SPEC-28); AI journal review cadence (BLG-AI-03); Screener accuracy test protocol (BLG-QA-18) | docs/frontend/component_library_research_view.md; docs/specs/frontend/pages/screener_morning_routine.md; docs/specs/frontend/pages/trade_plan.md#§6.2; docs/testing/screener_accuracy_protocol.md |

### Deviations accepted
4 minor P3 deviations — see verification_report.md §4 for full detail:
- EPIC-01/DEV-v3.4-01 [ST-02, P3]: sessionStorage used instead of localStorage for grace period dismiss — matches "same browser session" AC. Target: v3.5 (BLG-SPEC-29).
- EPIC-01/DEV-v3.4-02 [ST-03, P3]: PATCH /positions/{id} used instead of PUT for stop update — correct HTTP verb. Target: v3.5 (BLG-SPEC-30).
- EPIC-03/DEV-v3.4-01 [ST-10, P3]: React Query v5 removed onSuccess from useQuery — isAbandoned derived from query data. Codebase scan pending (BLG-SPEC-31).
- EPIC-02/DEV-v3.4-01 [ST-05, P3]: useState in-memory dismiss — spec §6 explicitly specifies in-memory state. Self-resolving.

### Tech backlog items shipped
- [ST-11] Research view component library (BLG-FE-31) — PT-02 component catalogue
- [ST-12] Screener morning routine UX spec (BLG-FE-22) — Arc 1→Arc 2 workflow spec
- [ST-13] trade_plan.md §6.2 spec update (BLG-SPEC-28) + AI journal review cadence (BLG-AI-03)
- [ST-14] Screener accuracy test protocol (BLG-QA-18) — §11 filter accuracy protocol
- [ST-07] Research page UK suffix strip (BLG-FE-23) + negative earnings days (BLG-FE-24)
- [ST-08] Signals page default to most recent day (BLG-FE-25)
- [ST-09] Watchlist research status indicator (BLG-FE-29)
- [ST-10] Trade plan status badges (BLG-FE-30) + abandonment UI (BLG-FEAT-21 frontend)

Sign-off: Product Owner — 2026-05-14
QA sign-off: Director of Quality — 2026-05-14

---

## v3.3 — Arc 3 In-Trade Risk Management — 2026-05-13
Cycle: 2026-05-09__release-v3.3
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-05-09__release-v3.3/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | IT-01 Position Lifecycle Manager (backend + state machine): DS-05 positions table lifecycle fields (position_state, state_entered_at, days_in_state) and direct SQL migration; position_lifecycle_service.py state machine (5 states: NEW → GRACE → LOSING/PROFITABLE → EXIT); GET /positions enriched with lifecycle fields; POST /positions/{id}/refresh-state endpoint; arc3_lifecycle_display feature flag. Frontend state display (ST-03) deferred to v3.4 | docs/specs/data_model.md#DS-05; backend/services/position_lifecycle_service.py; docs/reference/openapi.yaml |
| EPIC-02 | IT-02 Grace Period Decision Support (backend): GET /positions/grace-period-alerts endpoint — positions in grace period expiring within N days with trade plan join and §13-compliant display recommendation. IT-03 Stop Management Workflow (backend): GET /positions/{id}/stop-trail endpoint — ATR trail calculation, R-denominated recommendation, §13 display-only. Frontend alert card (ST-05) and trail stop panel (ST-07) deferred to v3.4 | docs/specs/api_contracts/grace_period_alert_endpoint.md; docs/reference/openapi.yaml |
| EPIC-03 | PT-02 research API contract (BLG-SPEC-25) and data source provenance spec (BLG-SPEC-26). Research view canonical spec (BLG-SPEC-24) and UX spec (BLG-FE-28). Test scenario library (BLG-QA-17): 19 scenarios SC-RV-01–19. Acceptance test protocol (BLG-QA-15). Entry checklist Playwright E2E tests (BLG-QA-14): entry-checklist.spec.js covering SC-CL-01–07. Research endpoint integration tests (BLG-QA-16), latency baseline (BLG-OPS-15), trade plan sensitivity classification (BLG-SEC-06), field extension governance policy (BLG-GOV-20) | docs/specs/api_contracts/research_endpoint.md; docs/specs/frontend/pages/research_view.md; docs/design/2026-05-09__release-v3.3/research-view/ux_spec.md; docs/qa/test_scenarios/research_view_scenarios.md; docs/qa/acceptance_protocols/research_view_protocol.md; tests/e2e/entry-checklist.spec.js; docs/ops/api_performance_baseline.md#section-11; docs/specs/security/trade_plan_data_sensitivity.md; docs/governance/trade_plan_field_extension_policy.md |
| EPIC-04 | Governance patches: execution_prompt.md v3.16→v3.17 (OA-01/CF-01 sealed-file check, OA-02/CF-02 mock payload advisory); sprint_planning_prompt.md v2.7→v2.8 (OA-05 design gate before sprint planning check); backlog_management_prompt.md v1.5→v1.6 + backlog_deferral_policy.md (OA-03/CF-03 3-cycle deferral policy). PT-05 §13 compliance review (BLG-GOV-19). Feature flag infrastructure (BLG-FEAT-13): is_flag_enabled() utility, FEATURE_FLAGS env var, arc3_lifecycle_display POC. Trade plan abandonment backend (BLG-FEAT-21 partial): DS-06 abandonment_reason column migration, PUT /trade-plans/{id} abandonment guard. Frontend status badges (ST-17 sub-deliverables: BLG-FE-30/23/24/25/29) deferred to v3.4 | claude/system/execution_prompt.md v3.17; claude/system/sprint_planning_prompt.md v2.8; claude/system/backlog_management_prompt.md v1.6; docs/governance/backlog_deferral_policy.md; docs/specs/compliance/pt05_entry_checklist_s13_review.md; docs/specs/platform/feature_flags.md; backend/utils/feature_flags.py; docs/specs/data_model.md#DS-06 |

### Deviations accepted
4 minor P3 deviations — see verification_report.md §4 for full detail:
- DEV-v33-01 [ST-01, P3]: AC specified Alembic migration; implementation used project-standard direct SQL. Target: v3.4.
- DEV-v33-02 [ST-08, P3]: AC specified 404/503/429 error codes; implementation returns 200 with null sub-fields on source failure. Known limitation documented in research_endpoint.md §Error Responses. Target: v3.4. (Reclassified P2→P3 by Director of Quality 2026-05-13.)
- DEV-v33-03 [ST-11, P3]: Spec references stop_level/risk_reward_notes for pre-population; implementation uses early_exit_conditions/r_target. Tests cover actual behaviour. Target: v3.4.
- DEV-v33-04 [ST-16, P3]: QA evidence reclassification note in qa_evidence_EPIC-04.md. Target: v3.4.

### Tech backlog items shipped
- [ST-08] Research API contract (BLG-SPEC-25) + data source provenance spec (BLG-SPEC-26)
- [ST-09] Canonical research view spec (BLG-SPEC-24) + UX spec (BLG-FE-28)
- [ST-10] Research view test scenario library (BLG-QA-17) + acceptance test protocol (BLG-QA-15)
- [ST-11] Entry checklist Playwright E2E tests (BLG-QA-14)
- [ST-12] Research endpoint integration tests (BLG-QA-16) + latency baseline (BLG-OPS-15) + trade plan sensitivity classification (BLG-SEC-06) + field extension governance (BLG-GOV-20)
- [ST-15] PT-05 §13 compliance review (BLG-GOV-19)
- [ST-16] Feature flag rollout infrastructure (BLG-FEAT-13)
- [ST-17] Trade plan abandonment backend (BLG-FEAT-21 — backend only; frontend sub-deliverables deferred to v3.4)

Sign-off: Product Owner — 2026-05-13
QA sign-off: Director of Quality — 2026-05-13

---

## v3.2 — Arc 2 Pre-Trade Research & Planning — 2026-05-08
Cycle: 2026-05-05__release-v3.2
Verified: Verified
Verification report: claude/cycles/2026-05-05__release-v3.2/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Pre-Trade Research View (PT-02 + PT-03): Research page at /research/{ticker}, ticker fundamentals, momentum signal, prospective heat at entry, trade plan panel, news headlines, screener/watchlist nav integration | docs/specs/frontend/pages/research.md; docs/specs/api_contracts/pre_trade_research_endpoints.md |
| EPIC-02 | Pre-Trade Entry Checklist (PT-05): Checklist component in Trade Plan form, 4 default items, toggle/persist, pre-population from plan data, research view link | docs/specs/frontend/pages/trade_plan.md#Entry Checklist |
| EPIC-03 | Governance & process hardening (OA-02–OA-05): sprint_planning_prompt.md STEP 0 main-branch check, execution_prompt.md STEP 5.1 deviations_filed enforcement, §3.1.A test_scenarios advisory, Playwright waitFor standard. Test scenario registrations: SC-TP-01–07 (trade plan), SC-EARN-01–09 (earnings), SC-UK-01–04 (UK screener) | claude/system/sprint_planning_prompt.md; claude/system/execution_prompt.md; tests/e2e/ |
| EPIC-04 | Documentation & security backlog clearance: React component inventory, design system doc, Alpaca credential audit/rotation policy, external API dependency risk register, cycle artefact inventory review | docs/specs/frontend/component_inventory.md; docs/specs/frontend/design_system.md; docs/ops/alpaca_key_rotation_policy.md; docs/ops/external_api_dependency_register.md; claude/system/OPERATIONAL_GUIDE.md §16 |

### Deviations accepted
None — zero spec deviations filed this sprint.

### Tech backlog items shipped
- [ST-13] React component inventory (BLG-FE-16)
- [ST-14] Design system document (BLG-FE-21)
- [ST-15] Alpaca credential audit and rotation policy (BLG-SEC-05)
- [ST-16] External API dependency risk register (BLG-GOV-18)
- [ST-17] Cycle artefact inventory and maintenance review (BLG-GOV-11)

Sign-off: Product Owner — 2026-05-07
QA sign-off: Director of Quality — 2026-05-07

---

## v3.1 — Arc 2 Trade Plan Foundation — 2026-05-05
Cycle: 2026-04-29__release-v3.1
Verified: Verified
Verification report: claude/cycles/2026-04-29__release-v3.1/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | PT-01 Trade Plan Object: data model schema (trade_plans table + 3 indexes; data_model.md v2.5), 6-endpoint CRUD API (POST /trade-plans, GET /trade-plans/{id}, PUT /trade-plans/{id}, DELETE /trade-plans/{id}, GET /trade-plans/by-position/{position_id}, GET /trade-plans/by-ticker/{ticker}), frontend creation/edit/view form and plan-exists banner; test.py 43 entries | docs/specs/data_model.md#Trade Plan; docs/specs/api_contracts/trade_plan_endpoints.md v0.1 |
| EPIC-02 | PT-02 Pre-Trade Research View (backend only): GET /research/{ticker} aggregation endpoint (signal, regime, sector, screener, earnings — all null-safe); pre_trade_research_endpoints.md v0.1; test.py 49 entries. Frontend deferred to v3.2 | docs/specs/api_contracts/pre_trade_research_endpoints.md v0.1 |
| EPIC-03 | DS-04 Earnings Calendar: GET /earnings/{ticker} backend + openapi.yaml; EarningsBadge on screener/watchlist/positions (⚠ proximity warning ≤5 days). BLG-FE-20 UK screener fix: stripUkSuffix helper for display and watchlist POST. BLG-QA-10/11: screener_accuracy_protocol.md + screener_scenarios.md (10 scenarios SCN-01–10). E2E: earnings-calendar.spec.js (SC-EARN-01–09), screener-uk-suffix.spec.js (SC-UK-01–04) | docs/specs/api_contracts/earnings_endpoints.md v0.1; docs/specs/screener_results_schema.md; docs/qa/screener_accuracy_protocol.md; docs/qa/screener_scenarios.md |
| EPIC-04 | BLG-FEAT-19 Monthly P&L report: GET /reports/monthly-pnl endpoint + MonthlyPnlTable in Reports.js. BLG-SEC-03/04+BLG-GOV-17: alpaca_key_rotation_policy.md, external_api_credential_inventory.md, external_api_dependency_register.md. CF-01/CF-02: execution_prompt.md v3.11→v3.13 (reclassification backfill instruction + STEP 8.5 output target fix) | docs/specs/api_contracts/reports_endpoints.md; docs/ops/; claude/system/execution_prompt.md v3.13 |

### Deviations accepted
None

### Tech backlog items shipped
- [ST-01–03] PT-01 — Trade Plan Object (full): data model, backend CRUD, frontend creation/edit/view flow
- [ST-04–05] PT-02 — Pre-Trade Research View (backend): aggregation endpoint (frontend deferred v3.2)
- [ST-06] BLG-FE-20 — UK screener ticker display fix and watchlist POST correction
- [ST-07–08] DS-04 — Earnings Calendar (backend + frontend EarningsBadge)
- [ST-09] BLG-QA-11 — Screener accuracy test protocol
- [ST-10] BLG-QA-10 — Screener scenario test data library (10 scenarios)
- [ST-11] BLG-FEAT-19 — Monthly P&L summary report
- [ST-12] BLG-SEC-03/04 + BLG-GOV-17 — External API security policy docs and dependency risk register
- [ST-13] CF-01 — execution_prompt.md §3.1.A reclassification backfill instruction (v3.11→v3.12)
- [ST-14] CF-02 — execution_prompt.md STEP 8.5 output target fix (v3.12→v3.13)

Sign-off: Product Owner — 2026-05-05
QA sign-off: Director of Quality — 2026-05-05

---

## v3.0 — Arc 1 Screener Engine & Results Page — 2026-04-27
Cycle: 2026-04-25__release-v3.0
Verified: Verified
Verification report: claude/cycles/2026-04-25__release-v3.0/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Screener Engine Backend — ticker universe data model + endpoints (ST-01); OHLCV data pipeline service with Alpaca primary / Yahoo Finance fallback (ST-02); ATR + regime detection + signal scoring engine (ST-03); screener batch engine + API endpoints `/screener/run` and `/screener/results` (ST-04) | docs/specs/api_contracts/ticker_universe_api_contract.md; docs/specs/api_contracts/alpaca_integration_contract.md; docs/specs/screener_results_schema.md; docs/specs/api_contracts/screener_api_contract.md; docs/reference/openapi.yaml |
| EPIC-02 | Screener Frontend — results page with sort/filter/regime badge/freshness/skeleton/empty/error states (ST-05); watchlist promotion inline popover + POST /watchlist integration (ST-06); news panel attachment with badge + inline expand/collapse (ST-07); keyboard shortcuts n/w/r + sidebar hints (ST-11, cross-EPIC) | docs/specs/frontend/pages/screener_results.md |
| EPIC-03 | Operations, Observability & Test Quality — external API health check extension (Alpaca + Yahoo Finance in GET /health) (ST-08); AI journal monitoring metrics (usage_rate, error_rate, p95_latency_ms in GET /health) (ST-09); AI audit service unit tests 12 tests (ST-10) | docs/specs/api_contracts/health_endpoints.md |
| EPIC-04 | Technical Debt & Governance — execution_prompt.md §2 deferred patch (ST-12); execution_prompt.md §3.1.A deferred patch (ST-13); prompt_change_log.md retrospective entries (ST-14); consecutive losing streak metric in metrics_definitions.md (ST-15); AI journal model version contract (ST-16) | claude/system/execution_prompt.md; claude/system/prompt_change_log.md; docs/specs/metrics_definitions.md; docs/specs/ai_journal_model_contract.md |

### Deviations accepted
None. DEV-01 (P3 — screener results news panel deferred from v2.9) resolved this sprint by ST-07 delivery.

### Tech backlog items shipped
- [ST-01] BLG-DS-01/ticker-universe: Ticker universe data model + CRUD endpoints + DB table
- [ST-02] BLG-DS-02/ohlcv-pipeline: OHLCV data pipeline with Alpaca primary + Yahoo Finance fallback
- [ST-03] BLG-DS-03/screener-engine: ATR Wilder 14-period + regime detection + composite signal score (RSI+MACD+volume)
- [ST-04] BLG-DS-04/screener-api: Screener batch run engine + POST /screener/run + GET /screener/results
- [ST-05] BLG-FE-19/screener-page: Screener results page (React, HashRouter, DataState, RegimeBadge, filters)
- [ST-06] BLG-FE-20/watchlist-promo: Watchlist promotion inline popover flow
- [ST-07] BLG-FE-18/news-panel: Screener news panel — resolves DEV-01 from v2.9
- [ST-08] BLG-OPS-12/health-ext: External API health check extension (Alpaca + Yahoo Finance)
- [ST-09] BLG-OPS-13/ai-metrics: AI journal monitoring metrics in GET /health
- [ST-10] BLG-QA-10/ai-audit-tests: AI audit service unit tests (12 tests)
- [ST-11] BLG-FE-21/keyboard-shortcuts: Keyboard shortcuts (cross-EPIC: n/w/r + sidebar hints)
- [ST-12] PATCH-EP-§2: execution_prompt.md §2 deferred patch from v2.9
- [ST-13] PATCH-EP-§3.1.A: execution_prompt.md §3.1.A deferred patch from v2.9
- [ST-14] PATCH-PCL: prompt_change_log.md retrospective entries from v2.9
- [ST-15] BLG-FEAT-13/streak-metric: Consecutive losing streak metric + GET /analytics/streak-metric
- [ST-16] BLG-AI-02/model-contract: AI journal model version contract spec

Sign-off: Product Owner (agent-mediated) — 2026-04-27
QA sign-off: Director of Quality (agent-mediated) — 2026-04-27

---

## v2.9 — Arc 1 Foundation: Stock Discovery & Screening Spec & Infrastructure — 2026-04-24
Cycle: 2026-04-22__release-v2.9
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-04-22__release-v2.9/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-03 | Arc 1 Governance & QA Foundation — §13 review record for DS-06 (BLG-GOV-16 gate cleared); external API mock harness for CI (tests/mock_harness/, 7 smoke tests pass); screener test data library (12 scenarios, 10+ synthetic tickers) | claude/strategy/strategy_rules.md#§13 |
| EPIC-01 | Arc 1 Specification Foundation — screener results schema spec (Class 2); Alpaca API integration contract (Class 2, RISK-01 gate cleared); screener internal API contract (Class 2, openapi.yaml updated); screener results page UX spec (DS-02 implementation deferred to v3.0) | docs/specs/data_model/screener_results_schema.md; docs/specs/api_contracts/alpaca_integration_contract.md; docs/specs/api_contracts/screener_api_contract.md; docs/specs/frontend/pages/screener_results.md; docs/reference/openapi.yaml |
| EPIC-04 | Governance Debt & Quick Wins — execution_prompt.md §3.2 governance patches (v3.8→v3.10); SystemStatus.js /ai prefix fix; AI Journal summary audit log (ai_audit_log table + GET /ai/journal-summary/history); AI Journal test scenario coverage (4 scenarios in ai_scenarios.md) | claude/system/execution_prompt.md v3.10; src/pages/SystemStatus.js; docs/specs/api_contracts/ai_endpoints.md; docs/testing/ai_scenarios.md |
| EPIC-02 | Arc 1 Implementation Start — sector & industry classification (DS-03: sector_service.py, position enrichment, 9 unit tests); Alpaca US market data integration (DS-05: alpaca_service.py, US→Alpaca/UK→Yahoo routing, 10 integration tests); Alpaca news panel (DS-06: news_service.py, GET /news/{ticker}, Watchlist.js news panel; screener results page attachment deferred to v3.0 — DEV-01 P3) | docs/specs/data_model.md; docs/specs/api_contracts/alpaca_integration_contract.md |

### Deviations accepted
1 minor P3 deviation — see verification_report.md §4 for full detail. Backlog item filed: BLG-FE-18 (screener results news panel wiring, v3.0).

### Tech backlog items shipped
- [ST-01] BLG-SPEC-21: Screener results schema spec — screener_results_schema.md created; registered in Specs_Index.md §3.4b
- [ST-02] BLG-SPEC-22: Alpaca API integration contract — alpaca_integration_contract.md created; RISK-01 gate cleared
- [ST-03] BLG-SPEC-23: Screener internal API contract — screener_api_contract.md created; openapi.yaml updated
- [ST-04] BLG-FE-17: Screener results page UX spec — screener_results.md created
- [ST-08] BLG-GOV-16: §13 review record for DS-06 (Alpaca News Panel) — gate cleared
- [ST-09] BLG-QA-08: External API mock harness for CI — tests/mock_harness/; 7 smoke tests pass
- [ST-10] BLG-QA-09: Screener test data library — 12 scenarios, 10+ synthetic tickers
- [ST-11] BLG-GOV-14: execution_prompt.md §3.2 governance patches — reclassification counter-sign rule + EPIC-level consolidation note (v3.8→v3.9)
- [ST-12] BLG-GOV-15: execution_prompt.md STEP 5.1.B advisory — System_status_report capability cross-check added (v3.9→v3.10)
- [ST-13] BLG-FE-15: SystemStatus.js /ai prefix fix — /ai case added to categorizeEndpoint()
- [ST-14] BLG-AI-01: AI Journal summary audit log — ai_audit_log table, log_ai_summary_run integration, GET /ai/journal-summary/history endpoint
- [ST-15] TEST-GAP-EPIC-04: AI Journal test scenario coverage — docs/testing/ai_scenarios.md (4 scenarios)

Sign-off: Product Owner — 2026-04-24
QA sign-off: Director of Quality — 2026-04-24

---

## v2.8 — Frontend Completion, Test Quality & AI Journal Feature — 2026-04-20
Cycle: 2026-04-17__release-v2.8
Verified: Verified
Verification report: claude/cycles/2026-04-17__release-v2.8/verification_report.md

### Changes shipped
| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Market Correlation View — MarketCorrelationSection.js on Analytics page; per-position Pearson correlation with severity badges (high=Rose-500, moderate=Amber-500, low=Emerald-500); portfolio weighted average; nulls sort to bottom | docs/specs/api_contracts/analytics_endpoints.md v2.1.0; docs/specs/frontend/pages/analytics.md v1.7; docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md |
| EPIC-02 | Market Correlation Endpoint Scenarios — SC-CORR-01–04 added to docs/testing/analytics_scenarios.md v1.1 | docs/specs/api_contracts/analytics_endpoints.md v2.1.0 |
| EPIC-02 | Supplementary Indicator Field Scenarios — SC-SIG-IND-01–02 added to docs/testing/signals_scenarios.md v1.1 | docs/specs/api_contracts/signal_endpoints.md v1.1 |
| EPIC-03 | DoQ Date Field Reminder Patch — execution_prompt.md §3.2.A explicit Date: field pre-condition at PR open | claude/system/execution_prompt.md v3.7 |
| EPIC-03 | Sprint Close Terminology Clarification — execution_prompt.md §5.3 Deviations filed clarified: spec deviations only | claude/system/execution_prompt.md v3.8 |
| EPIC-03 | Backlog Archive Deduplication — 64 duplicate entries removed; 83 unique IDs retained | claude/backlog/backlog_archive.md |
| EPIC-04 | AI Journal Summary Backend — POST /ai/journal-summary; Anthropic API (claude-haiku-4-5-20251001); graceful LLM failure (HTTP 200 summary:null); display-only; SRB-v1.7 compliant | docs/specs/api_contracts/ai_endpoints.md v1.0; docs/reference/openapi.yaml v2.7.0 |
| EPIC-04 | AI Journal Summary Frontend — AI summary section in TradeHistory.js; collapsed by default; non-dismissible disclaimer; Strategy Rules owner sign-off 2026-04-18 confirming SRB-v1.7 | docs/specs/frontend/pages/trade_history.md v1.7; docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md |

### Deviations accepted
None

### Tech backlog items shipped
- [BLG-FE-14] Market Correlation frontend view — deferred from v2.7 AC-6
- [BLG-QA-13] Test scenario coverage (SC-CORR, SC-SIG-IND) — v2.7 gap closure
- [BLG-GOV-13] Backlog archive deduplication — ID uniqueness compliance
- [BLG-FEAT-16] AI Journal Summarisation — first AI feature (Arc 4 foundation)

Sign-off: Product Owner — 2026-04-20
QA sign-off: Director of Quality — 2026-04-20

---

## v2.7 — Performance, Governance Hardening & Market Intelligence — 2026-04-16

Cycle: 2026-04-13__release-v2.7
Verified: Verified
Verification report: claude/cycles/2026-04-13__release-v2.7/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Supabase Supavisor connection pooling enabled (staging + production); `get_portfolio_summary()` refactored to single DB connection — GET /portfolio p50 = 234ms | `docs/ops/api_performance_baseline.md` v1.2; `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio` |
| EPIC-02 | QA sign-off gate before PR (§3.2.B); autonomous DoQ sign-off class for code-review-only EPICs (§3.2.A); governance_sync.yml push-to-main trigger | `claude/system/execution_prompt.md` v3.6; `claude/system/delivery_verification_prompt.md` v2.0 |
| EPIC-03 | Playwright LIFO route ordering fix (30/30 pass across 4 spec files); System Status Playwright spec authored (16/16 pass, 28-endpoint mock, category routing verified) | `tests/e2e/system-status.spec.js`; all 4 existing e2e spec files patched |
| EPIC-04 | `GET /analytics/market-correlation` backend endpoint (Pearson, 252-day lookback, 8h cache, SPY/FTSE benchmark); four supplementary indicator fields on `POST /signals/generate` (display-only, §13 COMPLIANT) | `docs/specs/api_contracts/analytics_endpoints.md` v2.1.0; `docs/specs/api_contracts/signal_endpoints.md` v1.1; `docs/reference/openapi.yaml` v2.6.0 |
| EPIC-05 | Spec Dependency Map (`docs/specs/spec_dependency_map.md` v1.0); Governance Health Score (OPERATIONAL_GUIDE.md §15 + roadmap_prompt.md STEP -1.7, advisory) | `docs/specs/spec_dependency_map.md` v1.0; `claude/system/OPERATIONAL_GUIDE.md` v3.59 |

### Deviations accepted

None — no P0–P3 spec deviations filed this sprint. AC-6 (market correlation frontend rendering) is an in-spec deferred AC, not a deviation.

### Tech backlog items shipped

- [ST-01] Enable Supabase Supavisor connection pooling — BLG-OPS-14; DEL-20260414-01 unblocked 2026-04-16
- [ST-02] Refactor get_portfolio_summary() to use a single DB connection — BLG-BE-07-FIX
- [ST-03] Require QA evidence sign-off block complete before PR — BLG-GOV-18
- [ST-04] Define formal autonomous DoQ sign-off class — BLG-GOV-19
- [ST-05] Extend governance_sync.yml to push-to-main — BLG-GOV-16
- [ST-06] Fix Playwright page.route() intercepts — BLG-QA-11 (Playwright fix)
- [ST-07] System Status Playwright spec — BLG-QA-12
- [ST-08] Market Correlation Analysis — BLG-FEAT-17
- [ST-09] Add supplementary indicator fields — BLG-BE-10
- [ST-10] Spec Dependency Map — BLG-SPEC-D17
- [ST-11] Governance Health Score — BLG-GOV-14

Sign-off: Product Owner — 2026-04-16
QA sign-off: Director of Quality — 2026-04-16

---

## v2.5 — Integration Baseline, Quick Wins & Governance Debt — 2026-04-10

Cycle: 2026-04-05__release-v2.5
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-04-05__release-v2.5/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | System Status reliability: auth forwarding fixed in POST /test/endpoints (API key forwarded to all internal calls); endpoint test list synced to 26 endpoints (matches openapi.yaml); Alerts, Notifications, Digest categories added to SystemStatus.js categorisation | backend/services/health_service.py; backend/routers/test.py; src/pages/SystemStatus.js |
| EPIC-02 | Backend integration documentation: Reports page and Signals page integration status mapped (gaps, SDK usage, follow-up items); GET /notifications/preferences outlier latency fixed (redundant ensure_alerts_tables() removed); GET /portfolio architectural constraint documented; Supavisor pooling recommendation filed | docs/ops/reports_integration_review.md; docs/ops/signals_integration_review.md; docs/ops/api_performance_baseline.md v1.1; backend/services/alerts_service.py |
| EPIC-03 | Frontend & operations quick wins: GitHub Actions curl calls hardened with --max-time 120; Avg Slippage StatsCard gradient deviation DEV-ST14-01 closed; Fee Drag % metric delivered end-to-end (backend fee_drag_pct + avg_fee_drag_pct, API contract v2.2.0, openapi.yaml v2.5.0, Trade History table amber column + sortable, Avg Fee Drag StatsCard); DataTable.js TableHead onClick bug fixed | docs/specs/api_contracts/trade_endpoints.md v2.2.0; docs/specs/metrics_definitions.md v1.9.0; docs/reference/openapi.yaml v2.5.0; src/pages/TradeHistory.js; src/components/trades/TradeHistoryTable.js; src/components/ui/DataTable.js; docs/testing/slippage_scenarios.md v1.2 |
| EPIC-04 | Governance hardening: execution_prompt.md STEP 8 governance file edit check (CF-2); delivery_verification_prompt.md pre-seal Date gate (CF-2); governance_sync.yml batch push fix (git log range, all commit messages parsed); backlog entry placement rule formalised; test scenarios SC-ATR-01, SC-DEDUP-01/02, SC-STOP-01 created | claude/system/execution_prompt.md v3.1; claude/system/delivery_verification_prompt.md v1.8; .github/workflows/governance_sync.yml; docs/testing/atr_scenarios.md; docs/testing/dedup_scenarios.md; docs/testing/stop_price_scenarios.md |

### Deviations accepted

4 minor P3 deviations — see verification_report.md §4 for full detail. Backlog items filed: BLG-FE-11 (card layout), BLG-FE-12 (header styling), BLG-FE-13 (flexible sort), BLG-BE-07-FIX (portfolio connection refactor).

No P1/P2 deviations. DataTable.js TableHead onClick (P2) fixed in-sprint before merge.

### Tech backlog items shipped

- [ST-01] BLG-OPS-12: Fix auth forwarding in POST /test/endpoints
- [ST-02] BLG-OPS-13: Sync endpoint test list with openapi.yaml
- [ST-03] BLG-FE-07: Fix System Status endpoint categorisation for v2.3/v2.4 routes
- [ST-04] BLG-BE-08: Review and document Reports page backend integration
- [ST-05] BLG-BE-09: Review and document Signals page backend integration
- [ST-06] BLG-BE-07: Investigate high external baseline latency on DB-backed endpoints
- [ST-07] BLG-OPS-11: Add --max-time to GitHub Actions curl calls
- [ST-08] DEV-ST14-01 closure: Fix Avg Slippage StatsCard gradient rendering (documentation close)
- [ST-09] BLG-FEAT-15: Fee drag metric on Trade History (backend + API + frontend)
- [ST-10] BLG-GOV-12: Fix governance_sync.yml batch push issue closure
- [ST-11] BLG-GOV-13: Formalise backlog entry placement standard
- [ST-12] BLG-GOV-11 (CF-2): Apply v2.4 deferred governance prompt patches
- [ST-13] TEST-GAP-EPIC-01: Create test scenarios for EPIC-01 correctness fixes

Sign-off: Product Owner — 2026-04-10
QA sign-off: Director of Quality — 2026-04-10

---

## v2.4 — Correctness, Insight & Governance Hardening — 2026-04-03

Cycle: 2026-03-31__release-v2.4
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-31__release-v2.4/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Backend correctness fixes: ATR pence→GBP conversion for all .L tickers (always-on, no guard); notification dispatch deduplication (rule_id + trading_day); initial stop price exposed on analytics trade endpoint (stop_price field join) | backend/utils/pricing.py; docs/specs/api_contracts/alerts_endpoints.md §4; docs/specs/api_contracts/analytics_endpoints.md §trades_for_charts |
| EPIC-02 | Frontend & UX: P&L (GBP) absolute value column restored to Positions Table View; user-facing error message mapping layer (HTTP status + error code → readable message) | docs/specs/frontend/pages/positions.md; src/lib/apiError.js |
| EPIC-03 | Spec debt: portfolios and trade_history table schemas in data_model.md reconciled against live Supabase DB (8 divergences corrected on trade_history; initial_cash and created_at confirmed correct on portfolios) | docs/specs/data_model.md#portfolios; docs/specs/data_model.md#trade_history |
| EPIC-04 | Weekly trading digest: new GET /digest/weekly endpoint returning 7-day P&L, alert activity, compliance score trend, staleness summary; WeeklyDigest.js frontend component | backend/routers/digest.py; docs/specs/api_contracts/digest_endpoints.md; docs/reference/openapi.yaml; src/pages/WeeklyDigest.js |
| EPIC-05 | Operational readiness: Render hosting tier reviewed and documented (free tier sufficient — decision record filed); API endpoint performance baseline documented (all endpoints, p50/p95); slippage tracking test scenario file (SC-SLIP-01 through SC-SLIP-06); cycle velocity metric defined and backfilled 6 cycles | docs/ops/api_performance_baseline.md; docs/testing/slippage_scenarios.md; claude/cycles/velocity_metrics.md; claude/system/roadmap_prompt.md (velocity section) |
| EPIC-06 | Governance engine maintenance: execution_prompt.md action-now patches (second recurrences LL-v2.2-EX-01/02/04); delivery_verification_prompt.md deviation compliance check patch (LL-v2.3-CL-03); execution_prompt.md delegation model update + delegation log line count check; release planning cycle artefact sealing simplified (SHA-256 hash verification removed, sealed: true flag retained) | claude/system/execution_prompt.md; claude/system/delivery_verification_prompt.md; claude/system/release_planning_prompt.md |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-EPIC02-ST05-03 | P2 | Missing P&L (GBP) column on Positions page (accepted v2.3; **resolved this sprint by ST-04**) | PO + DoQ (v2.3); resolved v2.4 |
| DEV-ST14-01 | P3 | Avg Slippage StatsCard renders without gradient background (cosmetic, pre-existing). BLG-FE-08 filed. | DoQ 2026-03-20 (pre-accepted) |

### Tech backlog items shipped

- [ST-01] BLG-BE-05: Fix ATR pence→GBP conversion for all UK (.L) tickers
- [ST-02] BLG-BE-06: Alert evaluation notification dispatch deduplication
- [ST-03] BLG-BE-04: Expose initial stop price (stop_price) on analytics trade endpoint
- [ST-04] BLG-FE-06: Fix missing P&L (GBP) column on Positions page
- [ST-05] BLG-FE-03: User-facing error message mapping layer
- [ST-06] BLG-SPEC-D15: Reconcile portfolios table schema in data_model.md
- [ST-07] BLG-SPEC-D16: Reconcile trade_history table schema in data_model.md
- [ST-08/09] BLG-FEAT-14: Weekly trading review digest (backend endpoint + frontend component)
- [ST-10] BLG-OPS-10: Render hosting tier review and decision record
- [ST-11] BLG-OPS-05: API endpoint performance baseline document
- [ST-12] TEST-GAP-EPIC-05-SLIP: Slippage tracking test scenario file
- [ST-13] BLG-GOV-09: Cycle velocity metric defined and backfilled
- [ST-17] BLG-GOV-03: Release planning cycle artefact sealing simplified (SHA-256 removed)
- [ST-14/15/16] Governance carry-forward patches: execution_prompt.md + delivery_verification_prompt.md action-now items (LL-v2.2-EX-01/02/04, LL-v2.3-CL-02/03)

Sign-off: Product Owner — 2026-04-03
QA sign-off: Director of Quality — 2026-04-03

---

## v2.3 — Quality Automation & User Insight — 2026-03-30

Cycle: 2026-03-24__release-v2.3
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-24__release-v2.3/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | StrategyCompliancePanel (display-only; per-position stop compliance, stop age, size compliance; collapsible; auto-expands on violation); MetricsStalenessIndicator (data-freshness badge, staleness age, per-metric tooltip) | docs/specs/frontend/pages/positions.md#Strategy Compliance Panel; docs/specs/frontend/pages/analytics.md#Metrics Staleness Indicator; docs/specs/api_contracts/position_endpoints.md#GET /positions/compliance |
| EPIC-02 | UnderwaterChart zoom/pan; MonthlyHeatmap tile drill-down modal (per-trade table, R-Multiple, exit reason); R-Multiple Distribution histogram; critical-path smoke tests (3 paths, CI advisory); staging data reset script; test data seed scripts | docs/testing/chart_interactivity_scenarios.md |
| EPIC-03 | GET /health/database endpoint (DB size monitor, Telegram alert); health_endpoints.md v1.2; system health check playbook (3 failure modes); DEV-HEALTH-001 closed | docs/specs/api_contracts/health_endpoints.md v1.2 |
| EPIC-04 | Alert notification badge on Alerts nav item; Alert Thresholds empty state CTA form (closes DEV-EPIC02-ST04-01); loading state standardisation (5 pages); collapsible sidebar navigation groups (4 groups, sessionStorage persist, badge integration) | docs/specs/frontend/pages/notifications.md; docs/specs/frontend/patterns/loading_states.md; docs/specs/frontend/pages/navigation.md |
| EPIC-05 | Backend branch discipline invariant (execution_prompt.md §13); canonical test execution report template; integration test coverage CI report | claude/system/execution_prompt.md; docs/testing/test_execution_report_template.md; docs/reference/openapi.yaml |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-EPIC02-ST05-03 | P2 | P&L (GBP) column absent on Positions page — % uplift shown, absolute £ not rendered. BLG-FE-06 filed. | PO + DoQ |
| V-CHART-05a/b/c | P2 | R-Multiple chart visual AC staging-blocked by BLG-BE-04 (stop_price absent from /trades API). BLG-BE-04 existing item. | PO + DoQ |

### Tech backlog items shipped

- [ST-03] BLG-OPS-08: Staging data reset script
- [ST-04] BLG-QA-06: Test data seed script library
- [ST-05] BLG-QA-05: Critical-path smoke test (Playwright, advisory-only CI)
- [ST-14] BLG-GOV-07: Backend branch discipline invariant in execution_prompt.md §13
- [ST-15] BLG-QA-03: Canonical test execution report template
- [ST-16] BLG-QA-04: Integration test coverage CI report

Sign-off: Product Owner — 2026-03-30
QA sign-off: Director of Quality — 2026-03-30

---

## v2.2 — Security, Alert Maturity & Quality — 2026-03-24

Cycle: 2026-03-21__release-v2.2
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-21__release-v2.2/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | X-API-Key authentication middleware (all non-health endpoints); Content Security Policy meta tag | docs/specs/api_contracts/conventions.md §1 v1.1; public/index.html |
| EPIC-02 | Alert scheduling design (trigger mechanism, cooldown, cron); Alert Threshold Customisation UI (inline edit/validation); Alert History Table (evaluation log + backend: alert_evaluations table, GET /alerts/history, GitHub Actions cron) | docs/specs/api_contracts/alerts_endpoints.md v0.3; docs/specs/frontend/pages/notifications.md v0.2 §2 + §Page 3; docs/product/decisions/decisions--2026-03-21__release-v2.2.md §ST-03 |
| EPIC-03 | CSV export function name bug fix; Slippage StatsCard gradient key fix; Operational health check endpoint (db status, last evaluation timestamps) | docs/specs/api_contracts/trade_endpoints.md; docs/specs/frontend/pages/trade_history.md; docs/specs/api_contracts/health_endpoints.md |
| EPIC-04 | Notification scenario execution (SC-NOTIF-01–08, 9 Playwright tests); Watchlist test scenarios (SC-WATCH-01–06); Test automation readiness assessment; Spec-to-test traceability matrix (54 ACs, 22 TEST-GAP entries) | docs/testing/notifications_scenarios.md; docs/testing/watchlist_scenarios.md; docs/testing/test_automation_readiness.md; docs/testing/spec_to_test_traceability_matrix.md |
| EPIC-05 | Provisional-Target field at backlog promotion; scored_initiatives.md effort band handoff for release planning; Structured lessons learnt carry-forward block across all engines | claude/system/roadmap_prompt.md v4.5; claude/system/release_planning_prompt.md v2.24; claude/system/sprint_planning_prompt.md v2.3; claude/system/post_ship_closure.md v2.1; claude/system/shared_standards.md v2.7; claude/system/lessons_learnt_prompt.md v1.8 |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-HEALTH-001 | P2 | GET /health implementation schema differs from spec v1.0 — more informative schema; BLG-SPEC-D14 created for spec update | PO + DoQ 2026-03-24 |
| DEV-EPIC02-ST05-02 | P2 | ST-05 backend commits landed on main rather than EPIC-02 branch — process deviation, no functional impact; BLG-GOV-07 created | PO + DoQ 2026-03-24 |

2 minor deviations (P3/observation): DEV-EPIC02-ST04-01 (missing CTA in empty state — BLG-FE-04 created), DEV-EPIC02-ST05-01 (React fragment key — observation only). See verification_report.md.

### Tech backlog items shipped

- [ST-01] API Key Authentication for Render Deployment (BLG-SEC-01)
- [ST-02] Content Security Policy Headers (BLG-SEC-02)
- [ST-03] Alert Scheduling Design (BLG-OPS-04)
- [ST-04] Alert Threshold Customisation (BLG-FEAT-10)
- [ST-05] Alert History Table (BLG-FEAT-12)
- [ST-06] Fix CSV Export Import Bug (BLG-BE-03)
- [ST-07] Fix Slippage StatsCard Gradient Key (BLG-FE-01)
- [ST-08] Health Check Endpoint (BLG-OPS-06)
- [ST-09] Execute Notification Scenarios on Staging (TEST-GAP-EPIC-02)
- [ST-10] Create Watchlist Test Scenarios (TEST-GAP-EPIC-03)
- [ST-11] Test Automation Readiness Assessment (BLG-QA-02)
- [ST-12] Spec-to-Test Traceability Matrix (BLG-SPEC-T01)
- [ST-13] Roadmap Engine: Provisional-Target Field (BLG-GOV-04)
- [ST-14] Release Planning: Load scored_initiatives.md (BLG-GOV-05)
- [ST-15] Structured Lessons Learnt Carry-Forward Block (BLG-GOV-06)

Sign-off: Product Owner — 2026-03-24
QA sign-off: Director of Quality — 2026-03-24

---

## v2.1 — Alerts, Watchlists & Enhancements — 2026-03-21

Cycle: 2026-03-18__release-v2.1
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-18__release-v2.1/verification_report.md

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Async notification delivery ADR — architecture decision: FastAPI BackgroundTasks (no Redis/Celery) | docs/adr/ADR-003-notification-delivery-architecture.md |
| EPIC-02 | Alerts & Notifications full stack — rules engine (4 alert types), Telegram delivery, notification preferences UI, in-app notification feed, QA scenarios | docs/specs/api_contracts/alerts_endpoints.md, docs/specs/frontend/pages/notifications.md, docs/testing/notifications_scenarios.md |
| EPIC-03 | Watchlist monitoring — spec, backend (4 endpoints, signal status join-on-read), frontend (add/edit/delete/Add-to-Position) | docs/specs/api_contracts/watchlist_endpoints.md, docs/specs/frontend/pages/watchlist.md |
| EPIC-04 | Chart interactivity — tooltips, zoom/pan, heatmap drill-down (all 16 SC-CHART-IX sub-scenarios verified) | docs/specs/frontend/pages/analytics.md |
| EPIC-05 | Tax Year P&L PDF + CSV exports; slippage tracking (fill price, slippage %, avg slippage); Render PR preview environments | docs/specs/api_contracts/reports_endpoints.md, docs/specs/frontend/pages/trade_history.md |
| EPIC-06 | Spec debt cleared — lifecycle headers, spec coverage inventory, chart QA scenarios, zero cross-EPIC process violations | docs/specs/spec_coverage_inventory.md, docs/testing/chart_interactivity_scenarios.md, docs/testing/reports_scenarios.md, docs/testing/signals_scenarios.md |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-ST04-01 | P2 | Notification delivery via Telegram instead of email — Gmail SMTP and Brevo blocked/unavailable on Render free tier | PO + DoQ 2026-03-20 |
| EPIC-03 cherry-pick | P2 | EPIC-03 delivered via cherry-pick to main (not branch PR) — branch divergence would have reverted EPIC-02/05/06 work | PO + DoQ 2026-03-21 |

1 minor deviation (P3): DEV-ST14-01 — StatsCard cosmetic null-state colour. See verification_report.md.

### Tech backlog items shipped

- [ST-12] Tax Year P&L PDF Export (BLG-FR-01)
- [ST-13] Tax Year P&L CSV Export (BLG-FR-02)
- [ST-14] Slippage Tracking (BLG-FEAT-03)
- [ST-15] Render PR Preview Environments (BLG-OPS-03)
- [ST-16] Bulk lifecycle header remediation (BLG-SPEC-D12)
- [ST-17] Spec maintenance batch (BLG-SPEC-D13, BLG-SPEC-G6, BLG-SPEC-D10, BLG-SPEC-D11)
- [ST-18] Missing test scenario documents (TEST-GAP-SIG-01, TEST-GAP-TAX-01)
- [ST-19] Cross-EPIC process compliance check (BLG-PROC-01)

Sign-off: Product Owner — 2026-03-21
QA sign-off: Director of Quality — 2026-03-21

---

## v2.0 — Reporting & Alerts — 2026-03-17

Cycle: 2026-03-17__release-v2.0
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-17__release-v2.0/verification_report.md

Fixes the P1 portfolio response defect (BLG-BE-01), delivers the UK tax-year P&L report endpoint and frontend view, and exposes the signal exposure controls (`top_n` and `lookback_days`) — making all three production-ready in a single sprint. Prospective heat endpoint (BLG-BE-02) shipped as stretch. EPIC-03 (Alerts & Notifications) deferred to v2.1 pending BLG-TECH-08 (async notification architecture ADR).

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-04 | Portfolio fix + prospective heat: `GET /portfolio` extended with 4 missing fields (`initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value`) — P1 BLG-BE-01 resolved. `GET /portfolio/prospective-heat` spec authored and implemented (ST-13 stretch — BLG-BE-02 closed). Tax-year P&L spec pre-completed (ST-03). | `docs/specs/api_contracts/portfolio_endpoints.md v2.0.0`; `docs/specs/api_contracts/reports_endpoints.md v0.1`; `docs/testing/v1.7-qa-scenario-gaps.md — GAP-03 PASS` |
| EPIC-01 | Signal Exposure Enhancement: signals page frontend spec authored; `top_n` and `lookback_days` controls implemented with 500ms debounce, invalid-input reset, and empty-state handling. | `docs/specs/frontend/pages/signals.md v0.1`; `docs/specs/api_contracts/signal_endpoints.md` |
| EPIC-02 | Tax-Year P&L Statement: `GET /reports/tax-year` endpoint implemented with UK 6 April tax-year boundary logic; frontend report view with year selector, P&L summary bar, trades table, disclaimer banner. Post-merge P1 hotfix bb66b69 (base44.baseUrl undefined on production — resolved same day). | `docs/specs/api_contracts/reports_endpoints.md v0.1`; `docs/specs/frontend/pages/reports.md v0.1` |
| EPIC-05 | Documentation & Standards Pack: Production Deployment Runbook; Positions Table Data Dictionary; Database Migration Governance Standard; Spec Coverage Inventory (38 documents, 7 actions); CohortAnalysis backend regression scenarios (stretch — ST-20). | `docs/ops/production_deployment_runbook.md`; `docs/specs/data_model_positions_dictionary.md`; `docs/ops/database_migration_governance.md`; `docs/specs/spec_coverage_inventory.md`; `docs/testing/analytics_scenarios.md v1.0` |
| EPIC-06 | Governance Tooling (parallel track): `roadmap_prompt.md` v3.0→v4.0 — all stage file references replaced with `cycle_record.md` sections for all tiers. `idea_intake_prompt.md` v1.3→v2.0 — per-file model replaced with `ideas_register.md`; 44 ideas migrated. | `claude/system/roadmap_prompt.md v4.0`; `claude/system/idea_intake_prompt.md v2.0`; `claude/ideas/ideas_register.md` |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| — | — | No deviations accepted. DEV-v2.0-02 (P1, base44.baseUrl) resolved by hotfix bb66b69 before verification — not an open deviation. 1 minor P3 deviation (DEV-v2.0-01 — ST-20 cross-branch process commit, CLAUDE.md §2 patch applied, BLG-PROC-01 filed). See verification_report.md §4. | — |

### Tech backlog items shipped

- [BLG-BE-01 / ST-12] GET /portfolio missing 4 fields (P1) — `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value` added; GAP-03 passes; 10/10 integration tests pass
- [BLG-BE-02 / ST-13] GET /portfolio/prospective-heat spec and implementation — endpoint specified and implemented; `@unittest.skip` removed; tests pass
- [BLG-OPS-02 / ST-14] Production Deployment Runbook — `docs/ops/production_deployment_runbook.md` created
- [BLG-DATA-01 / ST-15] Positions Table Data Dictionary — `docs/specs/data_model_positions_dictionary.md` created
- [BLG-TECH-07 / ST-16] Database Migration Governance Standard — `docs/ops/database_migration_governance.md` created
- [BLG-NEW-13 / ST-17] Spec Coverage Inventory — `docs/specs/spec_coverage_inventory.md` v1.0; 38 documents audited; 7 actions identified
- [BLG-GOV-01 / ST-18] Roadmap stage document consolidation — `roadmap_prompt.md` v4.0; all tiers use `cycle_record.md` sections
- [BLG-GOV-02 / ST-19] Ideas register — `idea_intake_prompt.md` v2.0; `ideas_register.md` created; 44 ideas migrated; 45 prior submissions archived

### Deferred items

- EPIC-03 (3.5 Alerts & Notifications — ST-06–ST-10) deferred to v2.1. No async notification infrastructure present. BLG-TECH-08 (ADR) required before v2.1 sprint planning may seal.

Sign-off: Product Owner — 2026-03-17
QA sign-off: Director of Quality — 2026-03-17

---

## v1.10 — Operations & Quality Foundation — 2026-03-16

Cycle: 2026-03-15__release-v1.10
Verified: Verified_with_deviations
Verification report: claude/cycles/2026-03-15__release-v1.10/verification_report.md

Establishes staging as the canonical pre-merge QA environment, closes the CohortAnalysis architecture violation carried since v1.9, delivers FastAPI TestClient integration tests for portfolio endpoints with a CI merge gate, and formally closes the v1.7 QA scenario gaps (BLG-QA-01) — executing 4 scenarios against staging. Resolves prior P2 deviation DEV-EPIC02-ST03-01.

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Development Environment Foundation: staging environment provisioned (Render Blueprint — API + Static Site + Supabase staging project); CI/CD auto-deploy from `main` via Render native auto-deploy; QA sign-off governance updated — `OPERATIONAL_GUIDE.md` v3.19 now mandates staging URL as canonical pre-merge QA environment | `claude/system/OPERATIONAL_GUIDE.md` v3.18→v3.19 |
| EPIC-02 | Analytics Architecture Correctness: `CohortAnalysis.js` refactored to call `GET /analytics/cohort` via `useQuery` + `api.analytics.cohort(period)`; `buildCohorts()`, `getPeriodLabel()`, `getPeriodKey()` removed; `trades` prop removed from call site; resolves analytics.md §15 hard rule and closes DEV-EPIC02-ST03-01 (P2, carried since v1.9) | `docs/specs/frontend/pages/analytics.md` §15; `docs/specs/api_contracts/analytics_endpoints.md` #GET /analytics/cohort |
| EPIC-03 | QA Infrastructure & Coverage: 15 FastAPI TestClient integration tests for `GET /portfolio` (response shape, GBP conversion, portfolio heat, grace period/display_status); `.github/workflows/integration-tests.yml` CI step blocks merge on failure; 4 v1.7 scenario gaps (GAP-01–GAP-04) authored and executed in `docs/testing/v1.7-qa-scenario-gaps.md`; BLG-QA-01 closed; TEST-GAP-EPIC-06 retired | `docs/specs/api_contracts/portfolio_endpoints.md`; `docs/testing/v1.7-qa-scenario-gaps.md` (new) |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| 1 minor deviation (DEV-ST05-01) | P3 | `GET /portfolio/prospective-heat` endpoint not defined in `portfolio_endpoints.md` and not implemented in backend — TestClient tests skipped with `@unittest.skip`; BLG-BE-02 filed for v2.0 — see verification_report.md §4 | PO — 2026-03-16 |

**Prior-cycle deviation resolved this sprint:**
- DEV-EPIC02-ST03-01 (P2, v1.9 Sprint 2) — CohortAnalysis client-side cohort computation — resolved by ST-04 (EPIC-02).

### Tech backlog items shipped

- [BLG-OPS-01 / ST-01] Provision staging environment infrastructure — Render Blueprint (Web Service + Static Site); Supabase staging project; staging live at https://trading-assistant-staging.onrender.com and https://trading-assistant-api-staging.onrender.com
- [BLG-OPS-01 / ST-02] Configure CI/CD auto-deploy to staging — Render native auto-deploy from `main`; deploy time ~2–5 min; no manual intervention required
- [ST-03] Update QA sign-off governance process — `OPERATIONAL_GUIDE.md` v3.19; staging URL referenced in §8.2 and §8.5; LL-01 governance gap closed
- [ST-04] Refactor CohortAnalysis.js to use backend endpoint — architecture violation closed; DEV-EPIC02-ST03-01 (P2) resolved
- [ST-05] FastAPI TestClient integration tests for portfolio endpoints — 15 tests; `tests/test_portfolio_integration.py`; all CI checks green
- [ST-06] Add integration test CI step — `.github/workflows/integration-tests.yml`; PR #72 CI check visible and named
- [BLG-QA-01 / ST-07] Author v1.7 missing QA test scenarios — 4 scenarios (GAP-01–GAP-04) in `docs/testing/v1.7-qa-scenario-gaps.md`; GAP-01 PASS, GAP-02 PASS, GAP-03 FAIL (BLG-BE-01 P1 filed — see Known Issues), GAP-04 BLOCKED (no closed trades in staging — deferred)

### Known issues carried forward

- **BLG-BE-01 (P1):** `GET /portfolio` response missing 4 required fields (`initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value`) per `portfolio_endpoints.md` v1.9.0. Discovered via GAP-03 staging execution. Targeted for v1.11.
- **GAP-04** (staging data gap): scenario valid but not executable — no closed trades in staging environment. Deferred.

Sign-off: Product Owner — 2026-03-16
QA sign-off: Director of Quality — 2026-03-16

---

## v1.9 — Risk Dashboard Fixes & Foundation — Sprint 1 of 2 (March 2026)

**Shipped:** 2026-03-09
**Cycle:** 2026-03-06__release-v1.9
**Verified:** Verified
**Verification report:** `claude/cycles/2026-03-06__release-v1.9/verification_report.md`
**Director of Quality sign-off:** 2026-03-09
**Product Owner acceptance:** 2026-03-09
**Sprint:** 1 of 2 — Sprint 2 (user-facing features) pending execution

Resolves all 10 Risk Dashboard deviations carried from v1.8, establishes reproducible Playwright test infrastructure that closes the v1.8 scenario coverage gap, and completes the full documentation hygiene backlog. User-facing features (Structured Trade Reflection Template, Compliance Metrics, Cohort Analysis, Dashboard Homepage, R-Multiple Distribution) are deferred to Sprint 2.

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-04 | Risk Dashboard: all 10 v1.8 deviations resolved — error states (HeatGauge, DrawdownSummary, GracePeriodPanel, PositionRiskTable, ProspectiveHeatPanel), sort direction (ascending), Stop Price column, Days in Grace column, GRACE badge colour (blue), GBP value at risk in HeatGauge, threshold label badge, US position GBP conversion for entry price and current stop | `docs/specs/frontend/pages/risk_dashboard.md` v0.1.7→v0.1.8 |
| EPIC-05 (partial) | QA infrastructure: Playwright canonical test scenario library Phase 1 (17 Risk Dashboard scenarios automated, CI gate); Service Layer Test Coverage Standard authored and enforced via pytest-cov in CI | `docs/testing/risk_dashboard_scenarios.md` v1.0→v1.1; `docs/specs/backend_engineering_patterns.md` |
| EPIC-06 | Documentation hygiene: Canonical Terms Glossary; AI-Assisted Workflow Governance Policy; `GET /market/status` endpoint spec; `settings_model.md` canonical spec; Error Response Standard in `conventions.md §13`; API Contracts README updated to v1.9.0; `GET /positions/search/tags` documented; `System_status_report.md` lifecycle header added; broken cross-references to `document_lifecycle_guide.md` fixed; `structured_logging_standards.md` registered in Specs Index; ADR-002 relocated; `validation_system.md` owner field corrected | Multiple spec documents (see Tech Backlog below) |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| — | — | No deviations accepted this sprint — all 10 inherited v1.8 Risk Dashboard deviations resolved | — |

### Tech backlog items shipped

- [BLG-RD-01 / EPIC-04] Entity store fallback masks API error states — all 5 Risk Dashboard components now render independent error states; entity fallback suppresses positionError correctly
- [BLG-RD-02 / EPIC-04] GracePeriodPanel empty vs error state — distinct error card rendered on API failure
- [BLG-RD-03 / EPIC-04] PositionRiskTable sort direction — corrected to ascending (most at risk first)
- [BLG-RD-04 / EPIC-04] Stop Price column absent — Stop Price column added to PositionRiskTable (GBP, 2 dp)
- [BLG-RD-05 / EPIC-04] GRACE badge colour amber — corrected to blue per spec §6.3
- [BLG-RD-06 / EPIC-04] GBP value at risk absent from HeatGauge — SVG text added below gauge percentage
- [BLG-RD-07 / EPIC-04] Days in Grace column absent — `holding_days` column added to GracePeriodPanel
- [BLG-RD-09 / EPIC-04] ProspectiveHeatPanel threshold label absent — threshold label badge added
- [BLG-RD-10 / EPIC-04] US entry prices in USD — `portfolio_service.py` now converts `entry_price` to GBP for US positions using `stored_fx_rate`; 5 new golden output vectors (FX-01–FX-05)
- [BLG-RD-11 / EPIC-04] `current_stop` in USD for US positions — `portfolio_service.py` converts `current_stop` to GBP for US positions; Stop Distance % now uses matching currencies
- [BLG-NEW-10 Phase 1 / ST-11] Canonical Test Scenario Library Phase 1 — Playwright mock layer; 17 Risk Dashboard scenarios automated; CI gate `.github/workflows/playwright.yml`; mock data in `tests/e2e/mocks/portfolio-mock-data.js`
- [BLG-NEW-12 / ST-13] Service Layer Test Coverage Standard — coverage threshold enforced via pytest-cov in CI; standard documented in `docs/specs/backend_engineering_patterns.md`
- [BLG-NEW-04 / ST-15] AI-Assisted Workflow Governance Policy — policy document filed in `docs/governance/`
- [BLG-NEW-11 / ST-14] Canonical Terms Glossary — `docs/reference/glossary.md` Class 2 Supporting v1.1; minimum terms defined with canonical source links; registered in Specs Index §3.6
- [BLG-SPEC-D3 / ST-16] `GET /market/status` endpoint documented — `docs/specs/api_contracts/market_endpoints.md` Class 1 Canonical v0.1; openapi.yaml updated; registered in Specs Index §3.4
- [BLG-SPEC-G1 / ST-17] `settings_model.md` created — `docs/specs/data_model/settings_model.md` Class 1 Canonical v0.1; registered in Specs Index §3.2
- [BLG-SPEC-G2 / ST-18] Error Response Standard defined — `docs/specs/api_contracts/conventions.md` §13 added (canonical error envelope, HTTP status mapping)
- [BLG-SPEC-D1, D4, D8, D9, G3, G4, G5 / ST-19] Remaining SPEC debt batch resolved — API Contracts README v1.9.0; `GET /positions/search/tags` documented; `System_status_report.md` lifecycle header added; cross-references fixed; `structured_logging_standards.md` registered in Specs Index §3.5b; ADR-002 relocated to `docs/product/decisions/`; `validation_system.md` owner field corrected to named role

### Sprint 2 — pending

| Item | Description | EPIC |
|------|-------------|------|
| ST-01 | Structured Trade Reflection Template | EPIC-01 |
| ST-02 | Basic Compliance Metrics (pre-work gate for ST-01) | EPIC-01 |
| ST-03 | Cohort Analysis | EPIC-02 |
| ST-04 | Dashboard Homepage / Session Summary | EPIC-03 |
| ST-05 | R-Multiple Distribution Report | EPIC-02 |
| ST-12 | Canonical Test Scenario Library Phase 2 (feature scenarios for Sprint 2 deliveries) | EPIC-05 |

Sign-off: Product Owner — 2026-03-09
QA sign-off: Director of Quality — 2026-03-09

---

## v1.8 — Risk Dashboard (March 2026)

**Shipped:** 2026-03-06
**Cycle:** 2026-03-04__release-v1.8
**Verified:** Verified_with_deviations
**Verification report:** `claude/cycles/2026-03-04__release-v1.8/verification_report.md`
**Director of Quality sign-off:** 2026-03-06
**Product Owner acceptance:** 2026-03-06

Full Risk Dashboard page giving the trader daily visibility into portfolio heat, drawdown, grace period status, and per-position risk. Simultaneously established automated correctness gates and closed highest-priority spec and governance debt from v1.7.

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | Risk Dashboard page: portfolio heat gauge (colour-coded thresholds), current drawdown summary, grace period status panel, per-position risk table, prospective heat indicator | `docs/specs/frontend/pages/risk_dashboard.md` v0.1.0–v0.1.6; `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio`; `docs/specs/metrics_definitions.md#Portfolio Heat` |
| EPIC-02 | CI Quality Gates: golden output regression (5 PS + 7 SL vectors, 30 tests), backtest vs live stop reconciliation, pip-audit CVE scanning (high/critical threshold), OpenAPI drift detection | `claude/strategy/strategy_rules.md`; `docs/reference/openapi.yaml` |
| EPIC-03 | Settings spec correction: PUT /settings replaced with PATCH /settings/{settings_id} and POST /settings; openapi.yaml updated to v1.9.0 | `docs/specs/api_contracts/settings_endpoints.md` v1.1.0; `docs/reference/openapi.yaml` v1.9.0 |
| EPIC-04 | Unavailability failure mode policy; running API changelog | `docs/ops/unavailability_policy.md` v1.0.0 (new); `docs/specs/api_contracts/api_changelog.md` v1.0.0 (new) |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| DEV-ST03-01 | P2 | Entity store fallback activates on `GET /portfolio` failure; error states not displayed when fallback data is available (§8) | PO — 2026-03-05 |
| DEV-ST03-03 | P2 | PositionRiskTable sorted descending by stop distance; spec §6.4 requires ascending | PO — 2026-03-05 |
| DEV-ST03-04 | P2 | Stop Price column absent from PositionRiskTable; spec §6.2 requires `current_stop` (GBP, 2 dp) | PO — 2026-03-05 |
| DEV-ST03-08 | P2 | Drawdown reads from `GET /portfolio`; spec §4.1 states `GET /analytics/metrics` — Head of Specs Team to verify | PO — 2026-03-05 |
| DEV-ST03-11 | P2 | US position entry prices display in native USD instead of GBP per spec §6.2 | PO — 2026-03-05 |
| DEV-ST03-12 | P2 | `current_stop` returned in USD for US positions; Stop Distance % derivation mixes currencies per spec §6.2 | PO — 2026-03-05 |
| P3 deviations | P3 | 5 minor deviations (DEV-ST03-02, DEV-ST03-05, DEV-ST03-06, DEV-ST03-07, DEV-ST03-09) — see `verification_report.md §4` | PO — 2026-03-05 |

All deviations accepted for v1.8; v1.9 resolution targets. Full register: `docs/specs/frontend/pages/risk_dashboard.md §11`.

### Tech backlog items shipped

- [BLG-NEW-01 / ST-05] Golden Output Regression Baseline — `tests/golden_outputs.json` created (5 PS + 7 SL vectors); CI workflow golden-outputs.yml added; 30 tests pass
- [BLG-NEW-02 / ST-06] Backtest vs Live Stop Reconciliation — stop formula reconciled against all 7 golden SL inputs; synthetic divergence detection confirmed sensitive
- [BLG-NEW-03 / ST-11] Unavailability Failure Mode Documentation — `docs/ops/unavailability_policy.md` created at v1.0.0
- [BLG-NEW-05 / ST-07] Dependency Vulnerability Scanning — `pip-audit` CI gate; high/critical CVEs block merge; requests package upgraded (pre-existing CVE resolved)
- [BLG-NEW-07 / ST-12] Running API Changelog — `docs/specs/api_contracts/api_changelog.md` created at v1.0.0; registered in Specs_Index.md §3.4
- [BLG-NEW-08 / ST-08] Automated OpenAPI Drift Detection — regex-based CI drift check; KNOWN_GAPS config supports managed transitions
- [BLG-SPEC-D2 / ST-09] Settings endpoint method drift resolved — `settings_endpoints.md` v1.1.0; PUT removed, PATCH/POST documented
- [BLG-SPEC-D7 / ST-10] openapi.yaml updated to v1.9.0 — PositionSummary, ValidationResponse, TradeHistory, Settings paths all aligned

### Test coverage gap

- [TEST-GAP-EPIC-01] 17/27 Risk Dashboard scenarios not executable — test infrastructure gap (no data injection mechanism). QA & Testing Owner to deliver seeded test environment before next sprint on Risk Dashboard spec sections. See `verification_report.md §6`.

Sign-off: Product Owner — 2026-03-06
QA sign-off: Director of Quality — 2026-03-06

---

## v1.7 — Foundation & Governance (March 2026)

**Shipped:** 2026-03-03
**Cycle:** 2026-03-02__release-v1.7
**Verified:** Verified
**Verification report:** `claude/cycles/2026-03-02__release-v1.7/verification_report.md`
**Director of Quality sign-off:** 2026-03-03
**Product Owner acceptance:** 2026-03-03

Non-user-facing governance and specification foundation release. Unlocks v1.8 pre-alignment (EPIC-03), v2.0 pre-alignment (EPIC-04, EPIC-05), and §13-gated features (EPIC-02).

### Changes shipped

| EPIC | Description | Spec sections updated |
|------|-------------|----------------------|
| EPIC-01 | CI/CD merge gate: `.github/workflows/validate-analytics.yml` — triggers on PR/push to main/develop; calls `POST /validate/calculations`; blocks merge on `critical_failed > 0`; posts severity breakdown as PR comment | `docs/specs/api_contracts/analytics_endpoints.md#POST /validate/calculations` |
| EPIC-02 | §13 Strategy Boundary Review: three features reviewed (Signal Params: COMPLIANT, AI Journal: CONDITIONALLY COMPLIANT, New Indicators: COMPLIANT if canonical). §13-gated features cleared to proceed | `claude/strategy/strategy_rules.md`; `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md` |
| EPIC-03 | Portfolio Heat metrics canonicalised: Position Risk (GBP-adjusted, FX-handled), Portfolio Heat (sum of Position Risks as % of portfolio value), explicit display thresholds with colour bands | `docs/specs/metrics_definitions.md` v1.5.8 → v1.6.0 |
| EPIC-04 | Structured Logging Standards: Class 1 Canonical Specification created — log levels (ERROR/WARNING/INFO/DEBUG), JSON log format (required + optional fields), correlation ID scheme (UUID v4, HTTP header propagation), async observability approach | `docs/specs/structured_logging_standards.md` v0.1.0 (new) |
| EPIC-05 | API Versioning Decision Record: URL path versioning deferred to first breaking change; 60-day deprecation notice; webhooks versioned from inception; existing endpoints grandfather-exempted | `docs/product/decisions/api-versioning-v1.7.md` |
| EPIC-06 | Spec Debt Resolution: `analytics_endpoints.md` v1.9.0 (14 validated metrics incl. `sharpe_ratio_trade_method`, OBS-01 resolved); `portfolio_endpoints.md` v1.9.0 (corrected to match live API, OBS-QWB-R1-01 resolved); `trade_endpoints.md` v1.9.0 (`holding_days` added, OBS-QWB-R3-01 resolved); `trade_service.py` updated | `docs/specs/api_contracts/analytics_endpoints.md` v1.8.1 → v1.9.0; `docs/specs/api_contracts/portfolio_endpoints.md` v1.8.2 → v1.9.0; `docs/specs/api_contracts/trade_endpoints.md` v1.8.4 → v1.9.0 |

### Deviations accepted

| Ref | Priority | Description | Accepted by |
|-----|----------|-------------|-------------|
| — | — | No deviations filed this sprint | — |

### Tech backlog items shipped

- [BLG-TECH-04] CI/CD GitHub Actions Validation Workflow — validate-analytics.yml workflow merged; merge gate live on main/develop
- [BLG-TECH-06] Canonicalise `sharpe_ratio_trade_method` — 14th validated metric added to analytics_endpoints.md v1.9.0; OBS-01 resolved
- [BLG-TECH-08] Align portfolio_endpoints.md positions summary — spec corrected to match live API (option a chosen); OBS-QWB-R1-01 resolved
- [BLG-TECH-09] Add `holding_days` to GET /trades — backend fix applied (option b chosen); OBS-QWB-R3-01 resolved

### Hard gates cleared by this release

| Gate | Cleared by |
|------|-----------|
| v1.8 pre-alignment | EPIC-03 — `metrics_definitions.md` v1.6.0 |
| v2.0 pre-alignment (logging) | EPIC-04 — `structured_logging_standards.md` Class 1 |
| v2.0 pre-alignment (API versioning) | EPIC-05 — `api-versioning-v1.7.md` |
| §13-gated features | EPIC-02 — SRB decision record filed |

### Test coverage gap

- [TEST-GAP-EPIC-06] 4 new scenarios required: `validate-analytics-14-metrics`, `validate-analytics-critical-count`, `portfolio-positions-field-alignment`, `trades-holding-days-present`. QA & Testing Owner to deliver before next sprint on analytics, portfolio, or trade endpoint domains. See `verification_report.md §6`.

Sign-off: Product Owner — 2026-03-03
QA sign-off: Director of Quality — 2026-03-03

---

## v1.6.1 — Quick Wins Bundle (March 2026)

**Shipped:** 2026-03-01
**Director of Quality sign-off:** 2026-03-01
**Verification report:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0
**Scope document:** `docs/product/scope/scope--QWB-quick-wins-bundle.md` (Superseded)

Six self-contained user-facing improvements. No new pages. No data model migrations.

---

### BLG-FEAT-01 — Current Drawdown Widget ✅ Complete

**Backend**
- `GET /portfolio` extended with two always-present fields: `current_drawdown_percent` (float, ≤ 0.0) and `peak_portfolio_value` (float, GBP)
- Calculated server-side: `(peak − current) / peak × 100`. Peak = `MAX(portfolio_history.total_value)` all-time. Both default to `0.0` when no `portfolio_history` exists
- Spec: `portfolio_endpoints.md` v1.8.2

**Frontend — Dashboard**
- Current Drawdown Widget added as fifth card in stats row
- Three display states: in-drawdown (% + peak equity + days underwater + progress bar), at-peak ("New Peak!"), no-history
- Progress bar sourced from `max_drawdown.percent` via `GET /analytics/metrics`. `days_underwater` sourced from `advanced_metrics.days_underwater` — no fallback calculation
- Spec: `dashboard.md` v1.1

---

### BLG-FEAT-02 — R-Multiple Column in Trade History ✅ Complete

**Frontend — Trade History**
- R-multiple column added to trade history table
- Frontend-only calculation: `R = (exit_price − entry_price) / (entry_price − stop_price)`. Source: `trades_for_charts` from `GET /analytics/metrics`, joined by trade `id`
- Display: signed, 2dp, R suffix (e.g. `+2.31R`, `−0.54R`). Em dash when `stop_price` absent or denominator is zero
- Column sortable; em-dash rows sort to end
- Spec: `trade_history.md` v1.1, `metrics_definitions.md` v1.5.8

---

### BLG-FEAT-04 — Best / Worst Trades Widget ✅ Complete

**Frontend — Performance Analytics**
- Best/Worst Trades component added below Top Performers on Performance Analytics page
- Two panels: top 3 and bottom 3 closed trades by R-multiple. Trades without `stop_price` excluded from ranking
- Partial panels when fewer than 3 qualifying trades; empty state when none
- Card content: ticker, R-multiple, P&L (GBP), exit date, exit reason
- Spec: `analytics.md` v1.2

---

### BLG-FEAT-05 — Win Rate by Month Chart ✅ Complete

**Frontend — Performance Analytics**
- Win Rate by Month bar chart added below Best/Worst Trades
- Source: `monthly_data` from `GET /analytics/metrics`
- Y-axis fixed 0–100. Bars green when `win_rate > 50%`, red at or below 50%. Dashed reference line at 50%
- Tooltip shows month, win rate %, and `trade_count`
- Returns null (no render) when `monthly_data` is empty
- Spec: `analytics.md` v1.2

---

### BLG-FEAT-06 — Grace Period Indicator ✅ Complete

**Backend**
- `GET /positions` extended with `grace_days_remaining` (integer | null) on every position object. Always present
- Formula: `max(0, 10 − holding_days)` when `grace_period = true`; `null` when `grace_period = false`. On day 10, `grace_period` becomes `false` → field returns `null`, not `0`
- Spec: `position_endpoints.md` v1.8.3

**Frontend — Positions**
- Grace Days Remaining column added to open positions table
- Display: `"Day {holding_days + 1} of 10"` when in grace; dash (`—`) when `null`
- Spec: `positions.md` v1.2

---

### BLG-FEAT-07 — CSV Export of Trade History ✅ Complete

**Backend**
- New endpoint: `GET /trades/export/csv`
- `Content-Type: text/csv`, `Content-Disposition: attachment; filename="trade_history.csv"`
- 14 columns: `ticker, market, entry_date, exit_date, shares, entry_price, exit_price, pnl, pnl_pct, holding_days, exit_reason, tags, entry_note, exit_note`
- Null fields → empty string. Tags array → semicolon-separated string. Empty history → header row only (HTTP 200)
- Spec: `trade_endpoints.md` v1.8.4

**Frontend — Trade History**
- CSV Export button added to Trade History page; triggers browser-native download
- Spec: `trade_history.md` v1.1

---

### Canonical Specs Updated

| Spec | Version | Change |
|------|---------|--------|
| `docs/specs/metrics_definitions.md` | v1.5.8 | New section: Current Drawdown |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.8.2 | New fields: `current_drawdown_percent`, `peak_portfolio_value` |
| `docs/specs/api_contracts/position_endpoints.md` | v1.8.3 | New field: `grace_days_remaining`; A-QA-05 day-10 contradiction corrected |
| `docs/specs/api_contracts/trade_endpoints.md` | v1.8.4 | New endpoint: `GET /trades/export/csv` |
| `docs/specs/frontend/pages/dashboard.md` | v1.1 | Current Drawdown Widget added |
| `docs/specs/frontend/pages/trade_history.md` | v1.1 | R-Multiple column + CSV Export button added |
| `docs/specs/frontend/pages/analytics.md` | v1.2 | Best/Worst Trades (§11) + Win Rate by Month (§12) added |
| `docs/specs/frontend/pages/positions.md` | v1.2 | Grace Days Remaining column added |
| `docs/specs/api_dependencies.md` | v1.2 | New dependencies added |

---

### Verification Summary

- **Scenarios:** 47 total — 45 pass, 2 deferred (F-17: data prerequisite; F-27: environment state), 0 fail
- **Defects:** 0 raised at any severity
- **Observations:** 2 pre-existing issues raised for backlog (BLG-TECH-08, BLG-TECH-09)
- **Sign-off:** Director of Quality, 2026-03-01. Verdict: Pass with logged deferrals

---

## v1.6 — Position Sizing Calculator (February 2026)

### Position Sizing Calculator ✅ Complete

**Sign-off:** Director of Quality, 2026-02-20
**Verification report:** `docs/product/verification/3.2-position-sizing-calculator-verification.md` (v1.4)

**Backend**
- `POST /portfolio/size` endpoint — calculates suggested share quantity for a prospective new position. Idempotent. No state mutation. Returns three distinct response shapes: valid result, insufficient cash (with `max_affordable_shares` always present), and invalid inputs (with machine-readable `reason` code)
- `default_risk_percent` field added to `settings` table — supports widget pre-population. Database migration applied; all existing rows default to `1.00`
- `GET /settings` and `PUT /settings` updated to expose and accept `default_risk_percent`

**Frontend**
- Position Sizing Calculator widget — always visible in Trade Entry form, directly above the Shares field
- Risk % field pre-populated from `settings.default_risk_percent` on form load
- Eight widget states implemented: idle, loading, valid auto-fill, valid with existing shares, insufficient cash, invalid input, invalid system, post-submit reset
- Auto-fills Shares field when result is valid and field is empty; "Use suggested shares" affordance shown when Shares already populated
- Debounced API call (300ms) on input change — does not block form submission in any state
- `default_risk_percent` field added to Settings page — Strategy Parameters section

**Canonical specifications updated**
- `strategy_rules.md` v1.3 — §4.1 sizing calculator rules
- `portfolio_endpoints.md` v1.8.0 — `POST /portfolio/size` contract
- `settings_endpoints.md` v1.8.0 — `default_risk_percent` field
- `data_model.md` v1.7 — settings column and migration script
- `position_form.md` v1.2 — widget spec and all eight states
- `settings.md` v1.1 — Strategy Parameters section
- `openapi.yaml` v1.8.0 — aligned with above contract changes

---

### BLG-TECH-01 — Sharpe Variance + Capital Efficiency Fix ✅ Complete

**Closed:** 2026-02-21
**Canonical Owner sign-off:** 2026-02-21
**Validation result:** 13/13 pass at 2026-02-21T00:24:41Z

This item was the v1.6 quality gate. v1.6 did not ship until these fixes were verified.

- `_calculate_sharpe()` updated to use sample variance (÷ n−1) for both portfolio-based and trade-based Sharpe methods
- Capital efficiency updated to use `Mean(total_cost)` in GBP from `trade_history` — eliminates USD/GBP mixing for portfolios with both markets
- `validation_data.py` expected values updated: `capital_efficiency` 0.17 → 0.22; `total_cost` fields added
- Validation metric count increased from 12 to 13 (capital efficiency added as explicitly validated metric)
- `metrics_definitions.md` v1.5.7 — Appendix E Backlog Items 1 and 2 marked resolved with closure detail
- `analytics_endpoints.md` v1.8.1 — resolved known limitations removed; severity contract added (A5/A6 actions completed alongside this closure)

---

## v1.5 — Performance Analytics (February 2026)

### Performance Analytics Page ✅ Complete

**Backend**
- Unified analytics endpoint: `GET /analytics/metrics?period=` (six period options: last 7 days, last month, last quarter, last year, YTD, all time)
- All metrics computed server-side from `trade_history` and `portfolio_history`; frontend performs no calculations
- Period filtering on both trade exit date and portfolio snapshot date
- `has_enough_data` gate: configurable minimum trade threshold (default 10, set via Settings)
- `POST /validate/calculations` endpoint: smoke-tests all metric calculations against a known 5-trade validation dataset with per-metric tolerance checks and CSV export

**Metrics delivered**
- Executive: Sharpe ratio (portfolio-based when 30+ snapshots available, trade-based fallback), max drawdown (percent, amount, date), recovery factor, expectancy per trade, profit factor, risk/reward ratio
- Advanced: win streak, loss streak, average hold time for winners vs losers, trade frequency (per week), capital efficiency, days underwater, portfolio peak equity
- Market comparison: win rate, total P&L, average win/loss, best and worst performer — UK and US independently
- Exit reason analysis: count, win rate, total P&L, average P&L, percentage of trades — per exit reason
- Monthly performance: P&L, trade count, win rate, cumulative — last 12 months
- Day of week: average P&L and trade count per weekday
- Holding period buckets: 1–5, 6–10, 11–20, 21–30, 31+ days — average P&L, count, win rate
- Top 5 winners and top 5 losers by P&L
- Consistency metrics: consecutive profitable months, current streak, win rate standard deviation, P&L standard deviation
- R-multiple analysis and tag performance derived from `trades_for_charts`

**Frontend**
- 12-component page render: executive summary cards, key insights, advanced metrics grid, monthly heatmap, underwater equity chart, market comparison, exit reason table, time-based charts, R-multiple analysis, top performers, consistency metrics, strategy tag performance
- Period selector drives single re-fetch of unified endpoint
- Loading, error, and not-enough-data states
- Key insights: up to 5 generated observations from metric values (Sharpe quality, hold time discipline check, profit factor commentary, expectancy edge, risk/reward)
- PDF export: print-optimised HTML report covering executive summary, key insights, and advanced metrics table
- snake_case → camelCase transformation on API response
- System Status page updated: analytics and validation endpoints categorised and included in automated endpoint testing suite

---

## v1.4 — Trade Journal & Notes System (February 2026)

### Trade Journal & Notes System ✅ Complete

- Entry notes when creating positions (500 character limit)
- Exit notes when closing positions (500 character limit)
- Tag system for categorising trades, with autocomplete from existing tags
- Tag validation: lowercase, hyphens only, up to 10 tags per position
- Tag filtering in trade history (OR logic)
- Expandable trade rows showing full journal entries
- Journal view mode in Positions page
- Visual entry/exit note cards with colour-coded headers
- Strategy tag pills with gradient styling
- Database schema updates: `entry_note`, `exit_note`, `tags` fields on positions and trade history
- GIN indexes on tags fields for fast filtering
- Backend endpoints: updateNote, updateTags, getTags

---

## v1.3 — System Health & Monitoring (February 2026)

- Health check endpoint (`GET /health`) for load balancers
- Detailed system status (`GET /health/detailed`)
- Automated endpoint testing (`POST /test/endpoints`) — 11 endpoints at launch
- Frontend status dashboard page with real-time monitoring
- Component-level health checks: Database, Yahoo Finance, Services, Config
- One-click endpoint testing with pass/fail results
- Auto-refresh at 5-second intervals
- Response time tracking
- 100% test pass rate at launch
