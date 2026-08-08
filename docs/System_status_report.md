**Owner:** Director of Quality
**Class:** Living Document (Class 3)
**Status:** Active
**Version:** 4.25
**Last Updated:** 2026-08-08 (sprint close 2026-08-07__release-v8.4); prior — 2026-08-07 (delivery verification 2026-08-05__release-v8.3 — status line updated Sprint_Complete → Verified); prior — 2026-08-07 (sprint close 2026-08-05__release-v8.3); prior history retained — see prior entries in version control.
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

## Sprint: 2026-08-07__release-v8.4
**Date:** 2026-08-08
**Status:** Sprint_Complete — pending verification

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Avg P&L/Trade column added to the Monthly P&L Report table (client-derived, colour-matched to Realised P&L, "—" for zero-trade months); tax-year CSV export gains a `trade_origin` (`Signal`/`Manual`) column derived from `trade_plans.signal_id`, replacing the originally-asked-for but unbuildable price-alert linkage | `docs/specs/frontend/pages/reports.md#Monthly Financial Table`; `docs/specs/api_contracts/reports_endpoints.md#Known Deviations` | `DEV-REPORTS-ST01-02` (P3, `BLG-FE-144`); Known Deviation re: `trade_origin` scope (`BLG-FEAT-78`) |
| EPIC-02 | `openapi.yaml` structural defect fixed (~23 endpoints moved from `components:` to `paths:`, drift detection now 0 findings); 6 API contract docs corrected for stale/missing example fields; auth-header documentation gaps closed; `data_model.md` backfilled for 4 undocumented tables; new formal schema-versioning doc for trade_plan/position tables | `docs/reference/openapi.yaml`; `docs/specs/api_contracts/{settings,position,health,watchlist}_endpoints.md`; `docs/specs/data_model.md`; `docs/specs/schema_versioning_trade_plan_position.md` | None |
| EPIC-03 | Functional index on `trade_plans(UPPER(ticker))`; 429/backoff handling added to Alpaca paper-sync close/positions endpoints; AI model+version provenance logging on stored thesis text (backend capability; frontend wiring tracked as `BLG-FE-143`); mutation/audit-trail log for post-entry trade plan edits; auto-generated data dictionary script from live schema | `docs/specs/data_model.md`; `backend/services/alpaca_paper_sync_service.py`; `backend/database.py`; `scripts/generate_data_dictionary.py` | None |
| EPIC-04 | 8 `cn()`-has-no-tailwind-merge Dialog className-override defects fixed across 6 files; 13 dark-only-token gaps in inline form-validation error text closed; `WatchlistModal.js` ESLint-clean (24→0 problems); CSP `script-src 'unsafe-inline'` removed entirely (content-hash replacement), `style-src 'unsafe-inline'` narrowly retained and justified | `docs/ops/dialog_classname_override_audit_2026-08-07.md`; `docs/ops/csp_unsafe_inline_audit_2026-08-08.md` | None |
| EPIC-05 | SI-05 weekly digest delivery fix confirmed live in production (Telegram receipt verified); API performance baseline endpoint-coverage drift closed (16 endpoints re-derived and measured); `POST /digest/si05/send` added to the baseline; CI runner cache warm-up cutting pytest job time ~22–51%; database storage-growth cost trend tracking (live-queried baseline snapshot); AI API cost model for Arc 4 journal intelligence features | `docs/ops/si05_digest_delivery_root_cause_2026-08-05.md`; `docs/ops/api_performance_baseline.md`; `docs/ops/cloud_infra_spend_by_epic.md`; `docs/operations/arc4_ai_cost_model.md` | None |
| EPIC-06 | Fixed wrong patch target in a pre-existing test; regression baseline backfilled with 24 undocumented Playwright spec files (86 files/732 scenarios verified); recurring CSV export content regression check added; signal correctness fix impact measurement completed (zero impact found, 0 of 300 pre-fix signals affected) | `tests/test_api_contracts.py`; `docs/qa/regression_test_suite_baseline.md`; `.github/workflows/csv-export-content-regression-check.yml`; `docs/ops/blg_be_40_impact_measurement_findings_2026-08-08.md` | None |
| EPIC-07 | Canonical, scripted gate-detection procedure for Release Planning's ungated-candidate scan (replaces prose guidance); cross-EPIC merge conflict runbook dry-run completed | `claude/system/release_planning_prompt.md#1.3a`; `scripts/scan_backlog_gate_conditions.py`; `docs/ops/cross_epic_merge_runbook_dry_run_2026-08-08.md` | None |

### Capabilities deferred or returned

None — all 31 ST items reached `merged` status this sprint.

### Verification inputs ready

- QA evidence logs: `qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-07.md`
- Deviations filed: `DEV-REPORTS-ST01-02` (P3, `reports.md`, `BLG-FE-144`); Known Deviation re: `trade_origin` scope reinterpretation (`reports_endpoints.md`, `BLG-FEAT-78`)
- Test scenarios referenced: `tests/e2e/monthly-pnl-avg-per-trade.spec.js`; `tests/test_trade_origin_query.py`; `tests/test_reports_integration.py`; `tests/test_trade_plans_ticker_index.py`; `tests/test_alpaca_paper_sync_close_positions_backoff.py`; `tests/test_trade_plan_thesis_provenance.py`; `tests/test_trade_plan_audit_log.py`; `tests/test_generate_data_dictionary.py`; `tests/e2e/dialog-classname-override-fixes.spec.js`; `tests/e2e/form-validation-error-color-fixes.spec.js`; `tests/e2e/watchlist.spec.js`; `tests/test_api_contracts.py`; `tests/test_reports_integration.py`; `tests/test_monthly_pnl_cost_basis.py`

---

## Sprint: 2026-08-05__release-v8.3
**Date:** 2026-08-07
**Status:** Verified — 2026-08-07

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | SI-05 weekly Telegram digest pipeline root-caused and fixed, with new delivery-failure alerting; staging/production API key distinctness check made recurring; Gemini API key rotation runbook | `docs/ops/si05_digest_delivery_root_cause_2026-08-05.md`; `scripts/check_si05_digest_staleness.py`; `scripts/check_api_key_cross_environment.py`; `docs/security/api_key_security_register.md#3. Anthropic API Key` | None |
| EPIC-02 | Database index audit for Arc 4 cross-table queries; Alpaca API rate-limit backoff audit; canonical `position_state` enum registry shared frontend/backend; remaining routers conformed to the canonical error envelope; Yahoo Finance regime-check retry/backoff; idempotent Alpaca paper-trading order-sync retry | `docs/ops/db_index_audit_arc4_2026-08-06.md`; `docs/ops/alpaca_backoff_audit_2026-08-06.md`; `docs/specs/position_lifecycle_states_registry.md`; `docs/specs/api_contracts/conventions.md#13. Error Response Standard (Canonical)`; `backend/utils/retry.py`; `backend/services/alpaca_paper_sync_service.py` | None |
| EPIC-03 | `ComplianceRecheckModal.js` migrated onto the shared `Dialog` primitive; new shared `ConfirmationModal.js` (confirm/cancel + optional undo-window variant); unified loading-skeleton pattern (`DataState.js`); standard Base44 theme-compliance prompt section; shared `AiDisclaimer.js` component extraction | `docs/specs/frontend/design_system.md#Confirmation Modal (with optional undo window)`; `docs/design/2026-08-05__release-v8.3/shared-confirmation-modal-undo-window/decision_record.md`; `docs/design/2026-08-05__release-v8.3/loading-skeleton-pattern/decision_record.md`; `docs/specs/frontend/base44_prompt_template_library.md#11`; `claude/backlog/backlog.md#BLG-FE-81` | None — a real-CI focus-restoration defect (`SC-CR-11`) was found and fixed post-PR-open, not shipped; see `sprint_close.md` Process Notes |
| EPIC-04 | Baseline Playwright coverage for Watchlist.js; OpenAPI 3-way drift gate false-negative sweep; DoQ sign-off staleness pre-merge lint; OpenAPI response-example drift spot-check; API endpoint deprecation-window policy; canonical form-validation error-message pattern spec | `tests/e2e/watchlist.spec.js`; `scripts/openapi_3way_drift_sweep.py`; `scripts/check_doq_signoff_staleness.py`; `docs/ops/openapi_response_example_spot_check_2026-08-06.md`; `docs/specs/api_contracts/conventions.md#14`; `docs/specs/frontend/design_system.md#Error States` | None — a real-CI self-referential lint false positive (ST-18) was found and fixed post-PR-open, not shipped; see `sprint_close.md` Process Notes |
| EPIC-05 | Terminal-state guard correction in release planning; formal §13 semi-annual boundary re-attestation cadence; SI-02 trade-count gate threshold calibration review; `prompt_change_log.md` ordering fix; cross-role workload balance check | `claude/system/release_planning_prompt.md#Terminal State Guard — Published Is Immutable (Hard Gate)`; `claude/strategy/strategy_rules.md#13.5`; `docs/product/decisions/si02_trade_count_gate_calibration_review_2026-08-06.md`; `claude/system/sprint_planning_prompt.md#7`; `claude/system/roadmap_prompt.md#7.2` | None |
| EPIC-06 | Monthly P&L Report format review — 3-month usage retrospective; Avg P&L/Trade column recommendation accepted for a future story (`BLG-FE-141`, `v8.4`) | `docs/product/decisions/monthly_pnl_format_review_2026-08-06.md` | None |

### Capabilities deferred or returned

None — all 27 ST items reached `merged` status this sprint.

### Verification inputs ready

- QA evidence logs: `qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-06.md`
- Deviations filed: None
- Test scenarios referenced: `tests/e2e/watchlist.spec.js`; `tests/e2e/compliance-recheck.spec.js` (SC-CR-01–11); `tests/e2e/epic03-v34-frontend.spec.js`; `tests/e2e/epic02-v62-ai-briefing-chat.spec.js`; `tests/test_doq_signoff_staleness_check.py`

---

## Sprint: 2026-08-04__release-v8.2
**Date:** 2026-08-05
**Status:** Verified — 2026-08-05

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | P&L/tax reconciliation report; Compliance Recheck Modal all-pass state; RFJ event colour palette refinement; Trade Plan focus indicator contrast fix; behavioural-drift insufficient_data streak metric | `docs/specs/api_contracts/reports_endpoints.md#GET /reports/reconciliation`; `docs/specs/frontend/pages/reports.md#Reconciliation Report`; `docs/specs/frontend/pages/positions.md#Compliance Recheck Panel (Modal)`; `docs/specs/frontend/design_system.md#Focus indicator contrast`; `docs/specs/metrics/si02_drift_score.md#3.5 Insufficient-Data Streak` | None |
| EPIC-02 | Staging and production rotated to distinct, independently-revocable API keys (live-verified); staging frontend's stale Render branch config fixed (was silently redeploying a 7-week-old frozen commit); staging backend's ~7-week silent auto-deploy webhook failure diagnosed (self-recovered, root mechanism documented as unresolvable beyond the observed pattern); recurring hourly staging-deploy-drift-check.yml added and live-verified post-merge | `docs/security/api_key_security_register.md#6. Application X-API-Key`; `scripts/check_staging_deploy_drift.py`; `.github/workflows/staging-deploy-drift-check.yml` | None |
| EPIC-03 | 11-item governance-process integrity cluster: SI-05 effectiveness review (PAUSE decision — digest delivery gap since 2026-06-17, confirmed by Product Owner attestation); velocity metrics audit; Arc 5 formula gap-check; rebalance-skip advisory fix; AI vendor ToS/DPA review; governance-bypass tracker; idea-intake retrospective; SI-02 credential-fallback standing decision; §13 boundary pre-check at design gate; header-history retention convention; governance_sync.yml delegation-commit fix | `claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md#30-Day Review — 2026-08-04`; `claude/system/post_ship_closure.md#Rebalance Cadence Check`; `claude/system/design_gate_prompt.md#STEP 1`; `claude/system/shared_standards.md#§16.14` | None |
| EPIC-04 | Quarterly dependency-upgrade cadence documented; Playwright CI browser-binary caching (measured, modest real improvement); automated commit-message format lint pre-commit hook | `docs/ops/dependency_upgrade_cadence.md`; `.github/workflows/playwright.yml`; `.githooks/commit-msg` | None |
| EPIC-05 | AST-derived drift test for SystemStatus.js endpoint-count fallback; 13 missing sprint-planning changelog versions reconstructed from git history; dead-code duplicate route removed from backend/main.py; motion/timing-sensitive interaction classification added to the design gate | `claude/cycles/2026-08-04__release-v8.2/stage4_backlog_slice.md#ST-22..ST-25`; `claude/system/design_gate_prompt.md#§6` | None |

### Capabilities deferred or returned

None — all 25 items in the authoritative backlog slice shipped this sprint.

### Verification inputs ready
- QA evidence logs: `qa_evidence_EPIC-01.md`, `qa_evidence_EPIC-02.md`, `qa_evidence_EPIC-03.md`, `qa_evidence_EPIC-04.md`, `qa_evidence_EPIC-05.md`
- Deviations filed: None
- Test scenarios referenced: `tests/test_reports_integration.py`; `tests/test_behavioural_drift_service.py`; `tests/e2e/reports-reconciliation.spec.js`; `tests/e2e/compliance-recheck.spec.js`; `tests/e2e/red-flag-journal.spec.js`; `tests/e2e/trade-plan.spec.js`; `tests/e2e/reports-si02-gate-status.spec.js`; `tests/e2e/system-status.spec.js`; `tests/test_staging_deploy_drift.py`; `tests/test_system_status_endpoint_count.py`; `.githooks/test_commit_msg.sh`

---

## Sprint: 2026-08-03__release-v8.1
**Date:** 2026-08-03
**Status:** Verified — 2026-08-03

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Trade Plan tag-suggestion buttons switched from `onMouseDown` to `onClick` — keyboard-operable | `docs/specs/frontend/components/journal_components.md#4` | None |
| EPIC-02 | Recurring production Supabase `pg_dump` backup (`.github/workflows/production-db-backup.yml`, daily) with automated restore-dry-run verification job into a disposable Postgres container | `docs/ops/database_backup_disaster_recovery_runbook.md#3.4` | None |
| EPIC-03 | Governance hardening bundle: perennial gated-item sunset criteria; Product Value Ratio escalation path; minimum capacity buffer floor advisory; technical debt registry; skill-silo mitigation rotation; automated PII-field scan gate for new endpoints; governed carry-forward write path | `claude/system/release_planning_prompt.md#1.4a.1, #STEP 3`; `claude/system/roadmap_prompt.md#2.4`; `claude/system/sprint_planning_prompt.md#1.5`; `claude/backlog/technical_debt_registry.md`; `scripts/check_pii_field_patterns.py`; `claude/system/shared_standards.md#17` | None |
| EPIC-04 | Custom price alert staging delivery confirmed live (Telegram); recurring endpoint test coverage audit script; cross-cycle DEV-* deviation consolidation review; Playwright shard balance audit | staging-only (BLG-QA-115); `scripts/audit_endpoint_test_coverage.py`; `claude/system/sprint_planning_prompt.md#STEP -1`; `docs/governance/deviation_consolidation_review_2026-08-03.md`; `claude/system/post_ship_closure.md#STEP 5.1`; `docs/ops/ci_pipeline_baseline.md#7` | None |
| EPIC-05 | SI-02 Gate Status Condition 2/3 thresholds formally decided and codified (Condition 2 unchanged ≥20 linked trades; Condition 3 changed to ≥0.50 adherence rate); §13 continuity note for v6.9 on-demand recheck; SI-02 condition-3 sufficient-data threshold cross-referenced to its existing definition | `docs/specs/frontend/pages/reports.md#SI-02 Gate Status`; `docs/specs/Specs_Index.md#6.6`; `claude/strategy/strategy_rules.md#13.4`; `docs/specs/metrics/si02_drift_score.md#2` | None |
| EPIC-06 | Cursor-based (keyset) pagination pattern added as shared backend utility, adopted opt-in on `GET /trade-plans`; `trade_plans.position_id` historical backfill scoping document | `docs/specs/api_contracts/backend_engineering_patterns.md#Cursor-based pagination pattern for list endpoints`; `docs/specs/trade_plans_position_id_backfill_scoping.md` | None |
| EPIC-07 | Per-EPIC `execution_state.json` files (Option 1) — each EPIC branch now owns its own state file exclusively, eliminating the cross-EPIC merge-conflict structural issue; cycle-level summary regenerated via `generate_execution_summary.py` | `claude/system/shared_standards.md#12` | None |

### Capabilities deferred or returned

None — all 19 stories (ST-01 through ST-19) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: `qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-07.md` (all 7 present, all sign-off blocks non-blank, dated 2026-08-03)
- Deviations filed: None
- Test scenarios referenced: `tests/e2e/reports-si02-gate-status.spec.js` (SC-SI02-07, SC-SI02-08 added); `tests/test_pagination.py`; `scripts/audit_endpoint_test_coverage.py`

---

## Sprint: 2026-07-30__release-v8.0
**Date:** 2026-07-31
**Status:** Verified_with_deviations — 2026-07-31

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | `strategy_version_at_entry` field on trade_plans/positions; FX handling reviewed post-DS-05 (no amendment needed); 3 FX conversion audit-trail gaps found and fixed (`fx_rate_used` missing from `POST /portfolio/position`, `GET /portfolio/prospective-heat`, pre-entry-validation cash-constraint check) | `docs/specs/data_model.md#DS-11`; `docs/product/decisions/ds05-fx-handling-review--2026-07-30.md`; `docs/product/decisions/fx-audit-trail-completeness-check--2026-07-30.md`; `docs/specs/api_contracts/portfolio_endpoints.md#POST /portfolio/position (v2.6.0)` | None |
| EPIC-02 | 17 implicit-HTTP-200 raw-exception-text error paths fixed in `backend/main.py`; new AI-endpoint security review checklist wired into the design gate; Trade Plan pre-entry checklist keyboard-reachability fix; Abandon modal focus-trap/restoration fix; production `request.client.host` proxy behaviour verified (no collapse); `.gitleaks.toml` allowlist schema bug fixed | `docs/specs/api_contracts/conventions.md#13`; `docs/specs/security/ai_endpoint_security_checklist.md`; `docs/design/2026-07-30__release-v8.0/entry-checklist-keyboard-accessibility/decision_record.md`; `docs/design/2026-07-30__release-v8.0/abandon-modal-focus-trap/decision_record.md`; `docs/security/rate_limit_audit_2026-07-29.md` v1.1; `.gitleaks.toml` | None |
| EPIC-03 | Playwright §18 anti-pattern sweep (networkidle/route-ordering fixes); smoke/critical/regression test-tagging convention wired into CI; synthetic trade-history data generator for gated-feature testing | `claude/system/shared_standards.md#18`; `docs/team_skills/quality/playwright_patterns.md#6 (v1.1)`; `backend/test_data/generate_synthetic_trade_history.py` | None |
| EPIC-04 | Render health-check Telegram alerting on sustained 5xx spikes (live-fire verified); repo secrets configured; real staging rollback drill executed; production Build Filters audited (no gap found); database backup/DR runbook drafted, production Supabase tier confirmed (Free — backup gap flagged) | `.github/workflows/health-check-alert.yml`; `docs/operations/render_rollback_runbook.md#Execution History (v1.2)`; `docs/ops/render_build_deploy_path_filter_audit.md`; `docs/ops/database_backup_disaster_recovery_runbook.md` | None |
| EPIC-05 | 3 new reusable Base44 prompt fragments (loading-skeleton patterns) extracted into the template library | `docs/specs/frontend/base44_prompt_template_library.md (v1.4)` | None |
| EPIC-06 | Cross-EPIC `execution_state.json` merge-conflict structural fix designed and signed off (per-EPIC state files, Option 1) — implementation deferred to a follow-up story at next sprint planning | `claude/cycles/2026-07-30__release-v8.0/execution_escalations.md#ESC-EXEC-20260731-01` | None (design decision + sign-off complete; implementation intentionally sequenced to next cycle boundary per Head of Specs Team guidance) |

### Capabilities deferred or returned

None — all 19 stories (ST-01 through ST-19) delivered within the sprint. ST-19's implementation (per-EPIC state files mechanism) is deferred to a new follow-up story at next sprint planning per the design decision recorded in `ESC-EXEC-20260731-01`; this is a sequencing decision, not a returned item.

### Verification inputs ready

- QA evidence logs: `qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-06.md` (all 6 present, all sign-off blocks non-blank)
- Deviations filed: None
- Test scenarios referenced: `tests/test_strategy_version_at_entry.py`; `tests/test_fx_audit_trail_completeness.py`; `tests/test_st04_implicit_200_error_paths_fixed.py`; `tests/e2e/entry-checklist.spec.js`; `tests/e2e/epic03-v34-frontend.spec.js`; `tests/test_synthetic_trade_history_generator.py`

---

## Sprint: 2026-07-28__release-v7.10
**Date:** 2026-07-30
**Status:** Verified — 2026-07-30

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Silent HTTP-200 error masking fixed in `portfolio_risk.py`; external-provider backoff audit extended (Yahoo Finance, Gemini, Claude); idempotency-key pattern established for state-mutating POST endpoints; deprecated table read-path audited and dead code removed | `docs/ops/backoff_audit_2026-07-29.md`; `docs/specs/api_contracts/backend_engineering_patterns.md#Idempotency-key pattern for state-mutating POST endpoints`; `docs/ops/deprecated_table_read_audit_2026-07-29.md`; `docs/specs/data_model.md#Deprecated Tables` | None |
| EPIC-02 | Secrets-scanning pre-commit/CI gate added (gitleaks); AI rate-limit bypass and public-endpoint rate-limit audits completed; raw exception text removed from 27 API error responses | `.githooks/pre-commit`; `.gitleaks.toml`; `docs/ops/ai_rate_limit_bypass_audit_2026-07-29.md`; `docs/security/rate_limit_audit_2026-07-29.md` | None |
| EPIC-03 | Playwright E2E now serves a production build instead of the CRA dev server; Red Flag Journal auth regression coverage added; endpoint test-suite coverage audit (7 new registrations); consumer-driven contract-drift check tooling added | `docs/ops/e2e_production_build_migration_2026-07-29.md`; `docs/ops/endpoint_test_coverage_audit_2026-07-29.md`; `docs/ops/consumer_contract_check_2026-07-29.md`; `scripts/check_consumer_contract_drift.js` | None |
| EPIC-04 | Corrected `position_endpoints.md` response-envelope claim and undocumented lifecycle fields; corrected `trade_endpoints.md` JSON example; confirmed OpenAPI heading-drift CI linter already live | `docs/specs/api_contracts/position_endpoints.md#GET /positions`; `docs/specs/api_contracts/trade_endpoints.md#GET /trades`; `scripts/lint_api_contract_headings.py` | None |
| EPIC-05 | `calendar.js` rewritten against current react-day-picker API; `SystemStatus.js` categorizeEndpoint() branch-coverage bug fixed; `StrategyBenchmark.js` header consolidated onto shared `PageHeader`; keyboard-navigation & focus-order audit completed | `docs/specs/frontend/pages/strategy_benchmark.md#2. Page Header`; `docs/ops/keyboard_navigation_audit_2026-07-29.md` | None |
| EPIC-06 | Recent-rebalance recency advisory added to roadmap engine STEP -1; 2 backlog items (design-gate state-sync, same-day rebalance collision handling) confirmed pre-met from prior-sprint fixes | `claude/system/roadmap_prompt.md#STEP -1.5.5 — Recent-Rebalance Recency Advisory`; `claude/system/design_gate_prompt.md#STEP 5 — Update Global State`; `claude/system/roadmap_prompt.md#6. Completion Event Definition (Run Precondition)` | None |

### Capabilities deferred or returned

None — all 23 stories (ST-01 through ST-23) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: `qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-06.md` (all 6 present, all sign-off blocks non-blank)
- Deviations filed: None
- Test scenarios referenced: `tests/test_portfolio_risk_error_handling.py`; `tests/test_idempotency_util.py`; `tests/test_idempotency_endpoints.py`; `tests/test_secrets_scanning_hook.py`; `tests/test_ai_rate_limit_bypass.py`; `tests/test_main_500_no_raw_exception_text.py`; `tests/test_red_flag_journal.py`; `tests/e2e/system-status.spec.js`; `tests/e2e/strategy-benchmark.spec.js`; `tests/e2e/heading-light-theme-contrast.spec.js`

---

## Sprint: 2026-07-27__release-v7.9
**Date:** 2026-07-28
**Status:** Verified — 2026-07-28

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Watchlist staleness tracking — new "stale" indicator plus Keep/Remove review action on watchlist entries | `docs/specs/frontend/pages/watchlist.md#Staleness Indicator`; `docs/specs/api_contracts/watchlist_endpoints.md#PATCH /watchlist/{entry_id}` | None |
| EPIC-02 | Historical sector/regime exposure trend chart added to the Risk Dashboard — new `GET /portfolio/sector-regime-trend` | `docs/specs/frontend/pages/risk_dashboard.md#8b. Component: Sector & Regime Exposure Trend`; `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/sector-regime-trend` | None |
| EPIC-03 | Canonical `trade_plan`↔`position` FK linkage schema documented in `data_model.md` | `docs/specs/data_model.md#Trade Plan to Position Linkage` | None |
| EPIC-04 | Cost-basis method disclosure/reconciliation column added to the Monthly P&L CSV export | `backend/services/reports_service.py` | None |
| EPIC-05 | "Why is my stop moving" explainer tooltip added to the trailing-stop column on position/trade views | `docs/specs/frontend/pages/positions.md#Trailing Stop Column` | None |
| EPIC-06 | Audit-log entries for manual position edits (who, when, before/after) | `backend/database.py`; `backend/services/position_service.py`; `docs/specs/data_model.md#Migration from v2.16 to v2.17` | None |
| EPIC-07 | Permanent data-integrity smoke test added as a standing gate on the nightly backtest CI job | `scripts/backtest_data_integrity_smoke_test.py`; `.github/workflows/backtest.yml` | None |
| EPIC-08 | Credential-persistence gap for SI-02 gate re-checks diagnosed and resolved — register entry #6 (`RENDER_API_KEY`) confirmed already provisioned; live gate re-check performed directly against production | `docs/security/api_key_security_register.md#6. Application X-API-Key` | None |
| EPIC-09 | Shared cross-EPIC smoke-test tag/suite defined for regression coverage on EPIC-branch merges | `tests/e2e/smoke-critical-paths.spec.js` | None |
| EPIC-10 | Pre-commit hook blocking commits that add new routes without a corresponding `backend/routers/test.py` registration | `scripts/check_router_test_registration.py`; `.githooks/pre-commit` | None |
| EPIC-11 | Chart-specific WCAG contrast checklist item added to `design_system.md` Accessibility section | `docs/specs/frontend/design_system.md` | None |
| EPIC-12 | Per-EPIC cloud infrastructure spend summary — documented that Render's Blueprint spec has no native tagging mechanism; git-history-derived attribution table substituted | `docs/ops/cloud_infra_spend_by_epic.md` | None |
| EPIC-13 | Dark-mode acceptance-criteria checklist item added to the Base44 prompt template library | `docs/specs/frontend/base44_prompt_template_library.md#4. Template: Dual-Theme Verification Call-Out` | None |
| EPIC-14 | Displacement debt register designed — rolling log of named displacement candidates and their disposition (physical placement tracked via ESC-EXEC-20260727-02, outside this routine's write scope) | `claude/cycles/2026-07-27__release-v7.9/qa_evidence_EPIC-14.md#Displacement Debt Register — Design` | None |
| EPIC-15 | Refresh cadence defined for Grid View visual-regression baselines | `docs/testing/visual_regression_baseline_cadence.md` | None |

### Capabilities deferred or returned

None — all 15 stories (ST-01 through ST-15) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: `qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-15.md` (all 15 present, all sign-off blocks non-blank)
- Deviations filed: None
- Test scenarios referenced: `tests/test_position_audit_log.py`; `scripts/backtest_data_integrity_smoke_test.py`; `tests/e2e/smoke-critical-paths.spec.js`; `scripts/check_router_test_registration.py`; `tests/e2e/system-status.spec.js` (SC-SS-01b, 102-endpoint baseline)

---

## Sprint: 2026-07-24__release-v7.8
**Date:** 2026-07-27
**Status:** Verified — 2026-07-27

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | In-app "what's new" panel on the dashboard — new `GET /changelog/latest` parses `docs/product/changelog.md` server-side on every request, no hardcoded copy (BLG-FE-128) | `docs/specs/frontend/pages/dashboard.md#6A`; `docs/specs/api_contracts/changelog_endpoints.md` | None |
| EPIC-02 | Automated Telegram digest of shipped items sent on post-ship closure, reusing existing Telegram POST+JSON+retry infrastructure (BLG-FEAT-84) | `claude/system/post_ship_closure.md#STEP 1.5`; `backend/services/changelog_digest_service.py` | None |
| EPIC-03 | Notification/digest surface accessibility pass — nav alert-count badge contrast fixed (`bg-red-500`→`bg-red-600`, 3.76:1→4.83:1); focus-indicator standard confirmed trivially met | `docs/design/2026-07-24__release-v7.8/notification-accessibility-audit/decision_record.md` | None |
| EPIC-04 | Consolidated dark-mode contrast audit across all 23 shipped pages — `PageHeader.js` title gradient missing `dark:via-` stop fixed | `docs/design/2026-07-24__release-v7.8/base44-dark-mode-contrast-audit/decision_record.md`; `docs/specs/frontend/design_system.md` | None |
| EPIC-05 | Monthly realised P&L CSV export alongside the existing tax-year export — `format=csv` on `GET /reports/monthly-pnl` | `docs/specs/api_contracts/reports_endpoints.md#CSV Export`; `docs/specs/frontend/pages/reports.md` | None |
| EPIC-06 | Per-cycle AI spend trend chart on the AI Usage & Costs view — new `GET /ai/spend-trend`, bucketed from existing `claude_audit_log` data by release-cycle windows parsed from `changelog.md` | `docs/specs/frontend/pages/settings.md#6a`; `docs/specs/api_contracts/ai_endpoints.md#GET /ai/spend-trend` | None |
| EPIC-07 | Consolidated rotation-and-audit cadence for all 5 external API key types (Alpaca, Claude, Telegram, Yahoo Finance, Gemini) — new quarterly audit cadence distinct from rotation | `docs/ops/api_key_rotation_and_audit_schedule.md` | None |
| EPIC-08 | Rate-limiting audit of all 128 live endpoints — `GET /health` (60/min/IP) and 3 previously-unlimited Claude-calling endpoints (10/min/IP each) remediated; remainder explicitly accepted as risk with documented rationale | `docs/security/rate_limit_audit_2026-07-26.md` | None |
| EPIC-09 | Shared `retry_with_backoff` decorator extracted and applied to the highest-traffic external call site (Yahoo Finance price fetch, previously had zero retry logic) | `backend/utils/retry.py` | None |
| EPIC-10 | Flaky-test quarantine process defined (`test.fixme` + required `FLAKY-QUARANTINE:`/backlog-reference format), enforced by a new format-compliance test | `docs/testing/flaky_test_quarantine_process.md` | None |
| EPIC-11 | Pilot contract-schema tests for the 3 highest-traffic endpoints (`GET /positions`, `GET /trades`, `GET /portfolio`, resolved via RISK-03 escalation) — surfaced 3 real doc/reality gaps, none P0/P1 | `docs/testing/pilot_contract_test_approach.md`; `docs/specs/api_contracts/position_endpoints.md`; `docs/specs/api_contracts/trade_endpoints.md`; `docs/specs/api_contracts/portfolio_endpoints.md` | None |
| EPIC-12 | CI lint step catching the documented "###-level silent-fail" case in API contract heading depth, running ahead of the existing OpenAPI Drift Detection gate | `.github/workflows/openapi-drift.yml`; `scripts/lint_api_contract_headings.py` | None |

### Capabilities deferred or returned

None — all 12 stories (ST-01 through ST-12) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: `qa_evidence_EPIC-01.md` through `qa_evidence_EPIC-12.md` (all 12 present, all DoQ sign-off blocks non-blank)
- Deviations filed: None
- Test scenarios referenced: `tests/e2e/whats-new-panel.spec.js`; `tests/test_changelog_service.py`; `tests/test_changelog_digest_service.py`; `tests/e2e/notification-badge-contrast.spec.js`; `tests/e2e/alert-nav-badge.spec.js`; `tests/e2e/page-header-dark-gradient-contrast.spec.js`; `tests/e2e/monthly-pnl-csv-export.spec.js`; `tests/test_api_contracts.py`; `tests/e2e/ai-usage-costs.spec.js`; `tests/test_ai_spend_trend_service.py`; `tests/test_rate_limit_endpoints.py`; `tests/test_retry_backoff.py`; `tests/test_flaky_quarantine_format.py`; `tests/test_pilot_contract_schemas.py`; `tests/test_lint_api_contract_headings.py`; `tests/e2e/system-status.spec.js`

---

## Sprint: 2026-07-21__release-v7.7
**Date:** 2026-07-24
**Status:** Verified — 2026-07-24

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | SI-04 strategy-version performance comparison view — compares strategy performance across `strategy_rules.md` version boundaries via date-range attribution (`backend/strategy_version_registry.py`, no migration needed) (BLG-FEAT-75) | `docs/specs/frontend/pages/strategy_benchmark.md`; `docs/specs/api_contracts/strategy_version_comparison_contract.md` | None |
| EPIC-02 | Nav duplication removed; Weekly Digest grouped with Notifications; `GET /notifications` gains `since_days`/`read` params for digest deep-links (BLG-FE-114) | `docs/specs/frontend/pages/navigation.md`; `docs/specs/frontend/pages/notifications.md`; `docs/specs/frontend/pages/weekly_digest.md`; `docs/specs/api_contracts/alerts_endpoints.md` | None |
| EPIC-03 | AiDailyBriefing light-theme contrast defect fixed (dark card on white page) via established light/dark token pairs (BLG-FE-113) | `docs/specs/frontend/pages/dashboard.md` | None |
| EPIC-04 | Shared `StandingAlert`/`StandingAlertStack` component — persistent, manually-dismissed alert distinct from auto-dismissing toast; documented, not yet wired to a live surface this cycle (BLG-FE-120) | `docs/specs/frontend/design_system.md` | None |
| EPIC-05 | SI-02 gate-acceleration nudge feasibility investigation — root-caused zero gate movement to discoverability, not a defect; recommendation scoped for a future sprint (no implementation this cycle) | `docs/product/decisions/si02-nudge-feasibility-assessment.md` | None |
| EPIC-06 | `daily-snapshot.yml` business curl calls gain `--fail`/`--show-error` response validation (3 endpoints); health-check ping correctly kept non-fatal | `.github/workflows/daily-snapshot.yml` | None |
| EPIC-07 | Retroactive §13 compliance review of shipped PT-04 (Setup Quality Score) — PASS, deterministic/read-only/no write path, first standalone review record for this feature | `docs/product/decisions/decisions--2026-07-21__release-v7.7--PT-04-section13-review.md` | None |
| EPIC-08 | Automated regression test for numpy-scalar handling in `generate_rebalance_exit_signals` (prevents recurrence of the PR #971 defect class) | `tests/test_rebalance_exit_signal_numpy_regression.py` | None |
| EPIC-09 | Nightly backtest job double-run/retry safety audit — confirmed already retry-safe (full delete-then-reinsert atomic transaction); added a CI concurrency guard as defense-in-depth | `docs/product/decisions/decisions--2026-07-21__release-v7.7--nightly-backtest-idempotency-audit.md`; `.github/workflows/backtest.yml` | None |
| EPIC-10 | Monitoring/alerting for nightly backtest failures or drift anomalies — Telegram alert distinguishing hard failure from detected anomaly, degrades gracefully pending secrets configuration | `.github/workflows/backtest.yml` | None — BLG-OPS-115 filed for repo-secrets follow-up |
| EPIC-11 | CI gate enforcing SystemStatus.js's endpoint-count fallback stays in sync with `backend/routers/test.py`'s AST-parsed `test_cases` count — corrected a live drift found while building the gate (fallback settled at 99 after reconciling with EPIC-01's concurrent endpoint addition) | `.github/workflows/quality_gate.yml` | None |

### Capabilities deferred or returned

None — all 11 stories (ST-01 through ST-11) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md through qa_evidence_EPIC-11.md (all 11 present, all DoQ sign-off blocks non-blank)
- Deviations filed: None
- Follow-up backlog items filed this sprint (not deviations): BLG-OPS-115 (EPIC-10, Telegram repo-secrets configuration)
- Test scenarios referenced: tests/e2e/si04-version-comparison.spec.js; tests/test_strategy_version_registry.py; tests/e2e/nav-notification-digest-consolidation.spec.js; tests/e2e/alert-nav-badge.spec.js; tests/e2e/sidebar-nav-groups.spec.js; tests/test_api_contracts.py; tests/e2e/standing-alert.spec.js; tests/test_rebalance_exit_signal_numpy_regression.py; tests/e2e/system-status.spec.js

---

## Sprint: 2026-07-20__release-v7.6
**Date:** 2026-07-20
**Status:** Verified — 2026-07-20

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Print/PDF export action on WeeklyDigest and TradePlan — client-side `window.print()` + print stylesheet (BLG-FE-119) | `docs/specs/frontend/pages/weekly_digest.md`#4; `docs/specs/frontend/pages/trade_plan.md`#7c | None |
| EPIC-04 | Backend error-response envelope audit across all 23 `backend/routers/*.py` files (79 endpoints) against `conventions.md` §13; canonical envelope conformance documented (BLG-BE-65) | `docs/specs/api_contracts/backend_engineering_patterns.md`#Error-response envelope conformance | None — audit/documentation, non-conforming endpoints filed as follow-up (BLG-BE-68, BLG-BE-69) |
| EPIC-02 | Regression suite baseline updated with 5 entries for `BLG-FE-115`–`BLG-FE-119` interaction surfaces, cross-referenced against Playwright spec files (BLG-QA-112) | `docs/qa/regression_test_suite_baseline.md`#Part 2 | None — broader v6.0–v7.3 cataloguing gap flagged, filed as follow-up (BLG-QA-116) |
| EPIC-03 | P&L export ↔ trade plan closure reconciliation — structural closure-state check between `trade_history` and `trade_plans.status` (BLG-FEAT-79) | `docs/specs/pnl_export_reconciliation.md` | None — production run: 0 mismatches (20 trade_history rows, 11 trade_plans) |
| EPIC-05 | Shared OpenAPI-derived Playwright mock fixture library, covering the 9 endpoints touched by `BLG-SPEC-95`'s scope (BLG-QA-114) | `tests/e2e/fixtures/api-mocks.js`; documented in `docs/qa/playwright_coverage_matrix.md`#3A | None |
| EPIC-06 | Nightly batch-job idempotency audit — all 4 scoped jobs (position analysis, portfolio snapshot, signal generation, backtest import) confirmed idempotent via direct SQL inspection (BLG-BE-62) | `docs/specs/nightly_batch_idempotency_audit.md` | None found |
| EPIC-08 | Standing regression suite consolidating BLG-SEC-01/BLG-SEC-02 coverage across all 4 previously-vulnerable ticker/market input paths (BLG-QA-69) | `tests/test_ticker_market_sanitization_regression.py` | None |
| EPIC-07 | Claude API monthly cost summary on Settings §6 — reframed from "consolidated Gemini + Claude" after discovering no Gemini integration exists in this codebase (BLG-FEAT-77) | `docs/specs/frontend/pages/settings.md`#6; `docs/specs/api_contracts/ai_endpoints.md`#GET /ai/monthly-cost | Design-artefact deviation — original UX spec premise (two AI providers) was factually incorrect; escalated (`ESC-EXEC-20260720-01`), resolved by Product Owner as a single-provider reframe, documented as `ux_spec.md` v1.1 §7 addendum |

### Capabilities deferred or returned

None — all 8 stories (ST-01 through ST-08) delivered within the sprint. ST-07 was mid-sprint reclassified `autonomous` → `delegated_decision` → `autonomous` after its escalation resolved; no item was returned to the backlog.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md through qa_evidence_EPIC-08.md (all 8 present, all DoQ sign-off blocks non-blank — 6 autonomous-class engine sign-off, 2 agent-mediated Director of Quality role sign-off for the frontend-visible EPICs, EPIC-01 and EPIC-07)
- Deviations filed: None (code-vs-spec sense) — EPIC-07's design-artefact deviation is documented in its own UX spec addendum, not a `/dev-file` DEV-* record, per `document_lifecycle_guide.md` §9 treatment of design-artefact corrections
- Follow-up backlog items filed this sprint (not deviations — audit findings about pre-existing conditions): BLG-BE-68, BLG-BE-69 (EPIC-04 audit), BLG-QA-116 (EPIC-02 cataloguing gap)
- Escalations: ESC-EXEC-20260720-01 (EPIC-07, Quality trigger) — raised and resolved within this sprint, Disposition: Resolved
- Test scenarios referenced: tests/e2e/print-export-pdf.spec.js; tests/e2e/fixtures/api-mocks.js; tests/e2e/ai-usage-costs.spec.js; tests/test_pnl_reconciliation_service.py; tests/test_ticker_market_sanitization_regression.py; tests/test_monthly_ai_cost.py

---

## Sprint: 2026-07-17__release-v7.5
**Date:** 2026-07-20
**Status:** Verified — 2026-07-20

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Global Cmd/Ctrl-K command palette wired to the existing shadcn Command primitive, navigable to every page including query-param-based TradePlan detail routes (BLG-FE-115) | `docs/design/2026-07-17__release-v7.5/command-palette/ux_spec.md`; `docs/specs/frontend/pages/navigation.md` | None |
| EPIC-02 | User-defined custom price alerts — `price_alerts` table, GET/POST /price-alerts, DELETE /price-alerts/{id}, evaluation folded into the alert delivery pipeline, health-check surfacing (BLG-FE-116) | `docs/design/2026-07-17__release-v7.5/custom-price-alerts/ux_spec.md`; `docs/specs/frontend/pages/notifications.md`; `docs/specs/api_contracts/alerts_endpoints.md`; `docs/specs/data_model.md`#Price Alerts Table | None |
| EPIC-03 | Bulk actions toolbar (checkbox selection, inline Bulk Tag, destructive confirmation, partial-failure toast) on Watchlist and Trade Plans, 6 new batch endpoints (BLG-FE-117) | `docs/design/2026-07-17__release-v7.5/bulk-actions-toolbar/ux_spec.md`; `docs/specs/frontend/pages/watchlist.md`; `docs/specs/frontend/pages/trade_plan.md`; `docs/specs/api_contracts/watchlist_endpoints.md`; `docs/specs/api_contracts/trade_plan_endpoints.md` | None |
| EPIC-04 | Named saved filter presets and a Table/Calendar toggle view on Trade History (realised-P&L day indicators, unrealised-P&L banner, day-click date filter), plus a localStorage envelope for previously-unpersisted active-filter state (BLG-FE-118) | `docs/design/2026-07-17__release-v7.5/saved-filters-calendar-view/ux_spec.md`; `docs/specs/frontend/pages/trade_history.md`; `docs/specs/api_contracts/saved_filters_endpoints.md`; `docs/specs/api_contracts/reports_endpoints.md`; `docs/specs/data_model.md`#Saved Filters Table | None |

### Capabilities deferred or returned

None — all 4 stories (ST-01 through ST-04) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (agent-mediated Director of Quality, 2026-07-17), qa_evidence_EPIC-02.md (agent-mediated Director of Quality, 2026-07-20), qa_evidence_EPIC-03.md (agent-mediated Director of Quality, 2026-07-20), qa_evidence_EPIC-04.md (agent-mediated Director of Quality, 2026-07-20)
- Deviations filed: None
- Test scenarios referenced: tests/e2e/command-palette.spec.js (SC-CP-01..12); tests/e2e/custom-price-alerts.spec.js; tests/e2e/bulk-actions-toolbar.spec.js; tests/e2e/saved-filters-calendar-view.spec.js

---

## Sprint: 2026-07-04__release-v6.6
**Date:** 2026-07-06
**Status:** Verified — 2026-07-06

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | UX & Accessibility Debt: systematic app-wide WCAG-AA contrast audit (764 instances, 102 files) — findings-only, 3 follow-up items filed (BLG-FE-87/88/89); Red Flag Journal filter state (event type, ticker, since-date) now persists across reload via versioned localStorage envelope, with graceful stale-state recovery | `claude/cycles/2026-07-04__release-v6.6/contrast_audit_findings.md`; `src/pages/RedFlagJournal.js`; `docs/specs/frontend/pages/red_flag_journal.md#Filter Controls` | None |
| EPIC-02 | QA & Test Infrastructure Debt: 10 true backlog-ID collisions renumbered with traceability notes (BLG-QA-72); manual `_DB_STUB_FUNCTIONS` sync list replaced with an AST scan of `backend/` imports, retiring the CLAUDE.md manual-sync rule (BLG-QA-73) | `claude/backlog/backlog.md`; `claude/backlog/backlog_archive.md`; `tests/conftest.py` | None |

### Capabilities deferred or returned

None — all 4 stories (ST-01 through ST-04) delivered within the sprint. One partial AC (backlog-ID AC-03 for ST-03) is gated on a pending Product Owner decision (BLG-QA-74, duplicate archival records), not deferred work.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (agent-mediated Director of Quality, mixed-class, 2026-07-06), qa_evidence_EPIC-02.md (autonomous class, 2026-07-06)
- Deviations filed: None
- Test scenarios referenced: tests/e2e/red-flag-journal-filter-persistence.spec.js (SC-RFJ-05a, SC-RFJ-05b)

---

## Sprint: 2026-07-02__release-v6.5
**Date:** 2026-07-03
**Status:** Verified — 2026-07-03

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Audit remediation cluster: `claude/audit.py` config block (PRIOR_AUDIT_ID/PRIOR_AUDIT_OPEN_ITEMS/PRIOR_SCORES/COMPLETED_CYCLES) reconciled with AUD-2026-07-01 (BLG-GOV-157); README.md document hygiene and OPERATIONAL_GUIDE/prompt version-sync drift verified pre-met on main from v6.4 work (BLG-GOV-158, BLG-GOV-159) | `claude/audit.py`#FRICTION_LOAD; `claude/cycles/2026-06-26__release-v6.3/audit_report_AUD-2026-07-01.md`#11; `claude/README.md`; `claude/system/OPERATIONAL_GUIDE.md`#14 | None |
| EPIC-02 | Backlog debt clearance: `GET /strategy/benchmark/open-positions` added to the API performance baseline with a live production measurement (p50=524.5ms, p95=600.0ms, BLG-OPS-83); 6 new Playwright scenarios for Strategy Benchmark Panel 0 conditional rendering (TEST-GAP-EPIC-03-v64); `signals_scenarios.md` reviewed against the risk-based sizing model — no stale references found, resolving the 3-cycle BLG-QA-61 carry-forward | `docs/ops/api_performance_baseline.md`#24; `tests/e2e/strategy-benchmark.spec.js`; `docs/testing/signals_scenarios.md` | None |
| EPIC-03 | Claude thesis feedback loop: thumbs-up/down feedback control on the Trade Plan form gated on a new `isClaudeDraft` flag, persisted to `trade_plans.thesis_feedback` (BLG-FE-46); `thesis_adoption_rate` metric definition (adopted-thesis-at-entry / thesis-generated-plans) with corrected `gemini_audit_log.plan_id` join key (BLG-FEAT-41) | `docs/design/2026-07-02__release-v6.5/thesis-feedback-mechanism/ux_spec.md`; `docs/specs/data_model.md`#DS-09; `tests/e2e/trade-plan.spec.js`; `docs/specs/metrics_definitions.md`#Thesis Adoption Rate | None |

### Capabilities deferred or returned

None — all 8 stories (ST-01 through ST-08) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (autonomous class, 2026-07-03), qa_evidence_EPIC-02.md (autonomous class, 2026-07-03), qa_evidence_EPIC-03.md (agent-mediated Director of Quality role, 2026-07-03)
- Deviations filed: None
- Test scenarios referenced: tests/e2e/strategy-benchmark.spec.js (SC-SB-05..07); tests/e2e/trade-plan.spec.js (SC-TP-23a..f)

---

## Sprint: 2026-07-02__release-v6.4
**Date:** 2026-07-02
**Status:** Verified — 2026-07-02

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Production correctness fix + AI security hardening: signal generation now reads `ticker_universe` instead of the deprecated `tickers` table (BLG-BE-40); `context_opts.ticker` sanitised before system prompt injection including a trailing-newline regex bypass fix (BLG-SEC-01); ticker/market strings validated at all 3 signal write paths including a second write path (`update_signal`) discovered during sign-off (BLG-SEC-02) | docs/specs/api_contracts/signal_endpoints.md; docs/specs/api_contracts/ticker_universe_api_contract.md; docs/specs/security/ai_injection_risk_assessment.md; docs/specs/api_contracts/ai_endpoints.md | None (BLG-SEC-07, BLG-SEC-08 filed as backlog follow-ups; not spec deviations) |
| EPIC-02 | AUD-2026-07-01 lifecycle-audit remediation: governance version-sync drift corrected (BLG-GOV-150); document hygiene cleanup (BLG-GOV-151); structural reliability gaps closed (BLG-GOV-152); audit/governance process fixes (BLG-GOV-153); FI-P3-01/FI-P3-02/FI-P4-01 re-targets resolved | claude/system/OPERATIONAL_GUIDE.md; claude/system/roadmap_prompt.md; claude/README.md; claude/system/shared_standards.md; claude/system/execution_prompt.md; claude/audit.py | None |
| EPIC-03 | Strategy Benchmark Open Positions panel + UX/QA polish: Panel 0 (Open Positions) added to Strategy Benchmark page (BLG-FEAT-54); AI daily briefing and chat widget disclaimer contrast fixed to WCAG AA (BLG-UX-01/02); v6.3 endpoints added to API performance baseline (BLG-OPS-82); Playwright coverage added for AI journal summary error states and full Strategy Benchmark page nav/filters/toggle modes/badge colours (TEST-GAP-EPIC-01/TEST-GAP-EPIC-03) | docs/specs/frontend/pages/strategy_benchmark.md; docs/specs/api_contracts/strategy_benchmark_endpoints.md; docs/reference/openapi.yaml; docs/specs/qa/ai_disclaimer_visibility_assessment.md; docs/ops/api_performance_baseline.md | None |

### Capabilities deferred or returned

None — all 13 stories (ST-01 through ST-13) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (Cybersecurity & Trust Lead agent-mediated + Product Owner/Director of Quality PR acceptance), qa_evidence_EPIC-02.md (autonomous class), qa_evidence_EPIC-03.md (Head of UX & Design + Infrastructure & Operations Owner agent-mediated + QA Lead/Director of Quality/Product Owner PR review)
- Deviations filed: None (spec deviations); BLG-SEC-07, BLG-SEC-08, TEST-GAP-EPIC-03-v64 filed as backlog follow-ups
- Test scenarios referenced: tests/e2e/epic02-v62-ai-briefing-chat.spec.js; tests/e2e/trade-history-ai-journal-summary.spec.js (SC-TH-AI-01..03); tests/e2e/strategy-benchmark.spec.js (SC-SB-01..04)

---

## Sprint: 2026-06-26__release-v6.3
**Date:** 2026-06-30
**Status:** Verified — 2026-06-30

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | AI Security & Quality Hardening: AI journal summary fixed (error surfaced to user, logger.error added); R-multiple display fixed on Reflection page (field name correction base44Client.js + N/A handling); per-endpoint rate limiting hardened (POST /ai/daily-briefing 10 req/min/IP; POST /ai/chat 30 req/min/IP; 429+Retry-After); AI response injection risk assessment (5 inputs assessed, BLG-SEC-01/02 filed); AI disclaimer visibility assessment (partially compliant — BLG-UX-01/02 filed); API contract review checklist for AI advisory endpoints (11-item checklist authored, both endpoints ALL PASS) | docs/specs/api_contracts/ai_endpoints.md v1.5; docs/specs/security/ai_injection_risk_assessment.md; docs/specs/qa/ai_disclaimer_visibility_assessment.md; docs/specs/api_contracts/ai_advisory_contract_checklist.md | None (BLG-UX-01 P3, BLG-UX-02 P2, BLG-SEC-01 P2, BLG-SEC-02 P3 filed as backlog items; not spec deviations) |
| EPIC-02 | Test Infrastructure & Quality Coverage: 21 nightly computation CI simulation tests (7 trailing stop, 5 rebalance exit, 9 inv-vol) passing; strategy signal regression test specification authored; 8 AI chat response schema validation tests passing; §13 boundary test suite (11 scenarios for POST /ai/daily-briefing and POST /ai/chat) | tests/test_nightly_computations.py; tests/fixtures/nightly_portfolio_state.json; docs/specs/qa/strategy_signal_regression_spec.md; tests/test_ai_chat_schema.py; docs/specs/qa/ai_s13_boundary_test_suite.md | None |
| EPIC-03 | Strategy Benchmark & UX Enhancement: Strategy Benchmark page live (3 panels with sticky filters, toggle modes, exit reason badges; 3 backend endpoints; DB schema backtest_trades + backtest_yearly_performance; import_backtest.py script); Morning briefing progressive disclosure (3 collapsible sections with localStorage persistence; SC-PD Playwright coverage); GET /health/scheduler endpoint (architecture review + 3 job tracking); live latency baseline established (daily-briefing p50=10,296ms p95=11,152ms; chat p50=6,258ms p95=7,035ms); Render deployment rollback runbook | src/pages/StrategyBenchmark.js; docs/specs/api_contracts/strategy_benchmark_endpoints.md; docs/reference/openapi.yaml v3.7.0; docs/specs/api_contracts/health_endpoints.md v1.3; docs/ops/api_performance_baseline.md §22.3; docs/operations/render_rollback_runbook.md | None |

### Capabilities deferred or returned

None — all 15 stories (ST-01 through ST-15) delivered within the sprint. Zero items returned to backlog.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (Sprint Execution Engine + Director of Quality counter-sign 2026-06-30), qa_evidence_EPIC-02.md (Sprint Execution Engine autonomous class + Director of Quality counter-sign 2026-06-30), qa_evidence_EPIC-03.md (Sprint Execution Engine + Director of Quality counter-sign 2026-06-30)
- Deviations filed: None (spec deviations); process notes and backlog items only
- Test scenarios referenced: tests/e2e/r-multiple-reflection.spec.js (SC-RM-01..03c); tests/test_nightly_computations.py (21 tests); tests/test_ai_chat_schema.py (8 tests); tests/e2e/ai-briefing-progressive-disclosure.spec.js (SC-PD-01..07)

---

## Sprint: 2026-06-24__release-v6.2
**Date:** 2026-06-25
**Status:** Verified — 2026-06-25

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Production strategy parity cluster: nightly trailing stop computation (profit-lock logic, INITIAL_ATR_MULT=5, PROFIT_ATR_MULT=2, ATR_PERIOD=14, ratchet invariant); month-end rebalance exit signals (`exit_rebalance` status, teal badge); inverse-volatility position sizing for signal-driven entries (`weight_i = (1/ATR_i) / Σ(1/ATR_j)`, [5%–20%] cash constraints); risk-off exit alerts (SPY/FTSE MA200 regime check, US/UK isolated); trailing stop display and breach badge on portfolio positions view | docs/specs/api_contracts/position_endpoints.md#GET /positions; docs/specs/api_contracts/signal_endpoints.md#GET /signals; docs/specs/api_contracts/signal_endpoints.md#POST /signals/generate; docs/specs/frontend/pages/positions.md | None |
| EPIC-02 | AI intelligence layer: POST /ai/daily-briefing (portfolio context assembly, claude-sonnet-4-6, advisory-only per §13 SRB-v1.7 PASS); AiDailyBriefing.js dashboard card (summary, action list with type chips, Regenerate button, non-dismissible advisory label); POST /ai/chat (stateless conversational advisor, grounded in live portfolio state); AiChatWidget.js on Positions + Signals pages (collapsed pill, expanded panel, advisory footer, error state) | docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing; docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat; docs/specs/frontend/pages/dashboard.md; docs/specs/frontend/pages/positions.md | None |
| EPIC-03 | Governance patches: execution_prompt.md v3.48 (BLG-GOV-135 autonomous class hard gate — criterion 3 detection rule for src/components/\*\* or src/pages/\*\* changes; BLG-GOV-136 test_scenarios path validation advisory); API performance baseline §21 (GET /portfolio/sector-weights p50=287ms p95=356ms; GET /trade-plans/setup-quality-score p50=464ms p95=516ms; BLG-OPS-75 closed); Playwright spec auto-registration via glob pattern (playwright.config.js testDir; BLG-QA-62 closed; 12 pre-existing dark specs excluded via testIgnore, BLG-QA-64 filed) | claude/system/execution_prompt.md v3.48; docs/ops/api_performance_baseline.md v2.6 §21; playwright.config.js | None |

### Capabilities deferred or returned

None — all 13 stories (ST-01 through ST-13) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (Director of Quality, 2026-06-25), qa_evidence_EPIC-02.md (Director of Quality, 2026-06-25), qa_evidence_EPIC-03.md (Director of Quality autonomous class, 2026-06-25)
- Deviations filed: None (spec deviations); ST-04 test suite replacement documented in EPIC-01 QA evidence as implementation note (not a spec deviation)
- Test scenarios referenced: tests/e2e/epic01-v62-stops-alerts.spec.js (EPIC-01, 9 scenarios), tests/e2e/epic02-v62-ai-briefing-chat.spec.js (EPIC-02, 9 scenarios)

---

## Sprint: 2026-06-22__release-v6.1
**Date:** 2026-06-23
**Status:** Verified — 2026-06-23

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Design Gate enforcement in governance engines: release_planning_prompt.md now requires STEP 4.1 design gate check and emits advisory; sprint_planning_prompt.md enforces design gate as hard gate at preflight (STEP -1, check 3); governance overhead ceiling proposal with G+D+P% metric and 86.0% 5-cycle baseline | claude/system/release_planning_prompt.md; claude/system/sprint_planning_prompt.md; docs/product/decisions/gov_overhead_ceiling_proposal_v6.1.md | None |
| EPIC-02 | CI quality hygiene: morning-briefing.spec.js and screener-quality.spec.js registered in playwright.yml (26 total spec files); PATCH /trades/{id}/costs performance baseline documented in api_performance_baseline.md §20 | .github/workflows/playwright.yml; docs/ops/api_performance_baseline.md v2.5 | None |
| EPIC-03 | Portfolio sector heat-map: GET /portfolio/sector-weights endpoint; SectorHeatMap.js on RiskDashboard; amber alert ≥40% concentration; SC-SHM-01..04 Playwright tests. Trade gate proximity indicator: GateProgressStrip.js on DashboardHome; {N}/20 trades progress bar; Gate cleared ✓ state; SC-GP-01..04 Playwright tests | docs/design/2026-06-22__release-v6.1/sector-heatmap/ux_spec.md; docs/design/2026-06-22__release-v6.1/gate-proximity-indicator/ux_spec.md; docs/specs/api_contracts/portfolio_endpoints.md v2.4.0 | None |
| EPIC-04 | Setup Quality Score backend: GET /trade-plans/setup-quality-score; score = clamp(win_rate×0.6 + avg_pnl_pct×0.4, 0, 100); gate_not_met when <20 trades; unit tests in test_setup_quality_score.py. Frontend: SetupQualityScorePanel in Research.js + TradePlan.js; gate-not-met advisory; expand/collapse detail view; SC-SQS-01..06 Playwright tests; test.py 67→69; SystemStatus.js 68→69 | docs/specs/api_contracts/trade_plan_endpoints.md v0.5; docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md | None |

### Capabilities deferred or returned

None — all 9 stories (ST-01 through ST-09) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md (all Sprint Execution Engine autonomous class, 2026-06-23)
- Deviations filed: None (spec deviations)
- Test scenarios referenced: tests/e2e/morning-briefing.spec.js, tests/e2e/screener-quality.spec.js, tests/e2e/sector-heatmap.spec.js (SC-SHM-01..04), tests/e2e/gate-progress.spec.js (SC-GP-01..04), tests/e2e/setup-quality-score.spec.js (SC-SQS-01..06)

---

## Sprint: 2026-06-19__release-v6.0
**Date:** 2026-06-22
**Status:** Verified_with_deviations — 2026-06-22

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Signal correctness fix — signal_service.suggested_shares now uses size_position() per strategy_rules.md §4.1 canonical risk-based formula; cash-allocation model removed; tests/test_signal_sizing.py added (AC-02–05 coverage); Strategy Rules & System Intent Owner sign-off cleared via agent-mediated review | claude/strategy/strategy_rules.md#4.1; docs/specs/api_contracts/signal_endpoints.md | None |
| EPIC-02 | Trader's Morning Briefing dashboard (MorningBriefing.js + 5 sub-cards; DashboardHome.js integration; 11 Playwright scenarios covering all 5 cards, empty states, links); Net-of-costs performance tracking (PATCH /trades/{id}/costs; net_r_multiple in TradeHistoryTable.js; data_model.md DS-08; openapi.yaml + test.py + SystemStatus.js 66→67; 5 Playwright scenarios) | docs/specs/api_contracts/grace_period_alert_endpoint.md; docs/specs/api_contracts/position_endpoints.md; docs/specs/api_contracts/red_flag_journal.md; docs/specs/api_contracts/earnings_endpoints.md; docs/specs/api_contracts/analytics_endpoints.md; docs/specs/api_contracts/trade_endpoints.md; docs/specs/data_model.md | None |
| EPIC-03 | Screener data quality telemetry — ScreenerQualityPanel replaces DegradedRunBanner; new GET /screener/results fields (tickers_requested, tickers_loaded, tickers_failed, last_full_run_utc, run_quality); screener_api_contract.md v1.2; 5 Playwright scenarios (3 quality states + expandable list + stale advisory). SI-05 deep link staging confirmation — digest received 2026-06-17 post-FRONTEND_URL; both deep links confirmed by I&O Owner | docs/specs/api_contracts/screener_api_contract.md v1.2; docs/specs/api_contracts/digest_endpoints.md | None |
| EPIC-04 | RFJ design review brief (docs/design/2026-06-19__release-v6.0/rfj-design-review/brief.md; HoUX&D sign-off); RFJ visual design review — Accept verdict, no redesign, 2 P3 refinements filed (BLG-FE-66, BLG-FE-67); SI-05 digest cadence review — weekly maintained, reassessment 2026-07-04; SI-05 actionability metrics definition — 4 metrics (ATCR, RFAR, DDCR, EPAR); SI-05 Phase 2 activation decision — DEFER, revised review 2026-08-04; SI-05 p99 latency baseline review — PASS WITH DEVIATION (7 dispatches confirmed; no prior baseline) | docs/design/2026-06-19__release-v6.0/rfj-design-review/; docs/product/decisions/si05-digest-cadence-review--2026-06-22.md; docs/product/decisions/si05-actionability-metrics-definition.md; docs/product/decisions/si05-phase2-activation-decision--2026-06-22.md; docs/testing/staging_latency_review_ST-11.md | P3 (ST-11): 16-day vs 4-week measurement window; AC-02 N/A (no prior BLG-OPS-54 baseline); PO gate override 2026-06-20; BLG-OPS-54 scope revised |

### Capabilities deferred or returned

None — all 11 stories (ST-01 through ST-11) delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (Sprint Execution Engine autonomous class 2026-06-19), qa_evidence_EPIC-02.md (Director of Quality agent-mediated BLG-GOV-19 2026-06-19), qa_evidence_EPIC-03.md (Director of Quality agent-mediated BLG-GOV-19 2026-06-19 + I&O Owner addendum 2026-06-22), qa_evidence_EPIC-04.md (Director of Quality 2026-06-22; PO acceptance 2026-06-22)
- Deviations filed: None (spec deviations); ST-11 P3 process deviations in QA evidence (measurement constraints, PO gate override 2026-06-20)
- Test scenarios referenced: tests/test_signal_sizing.py (EPIC-01); tests/e2e/morning-briefing.spec.js, tests/e2e/net-r-trade-history.spec.js (EPIC-02); tests/e2e/screener-quality.spec.js (EPIC-03); delegated sign-offs (EPIC-04)

---

## Sprint: 2026-06-17__release-v5.9
**Date:** 2026-06-18
**Status:** Verified — 2026-06-18

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Governance Simplification (SC-03–SC-07): execution_prompt.md v3.42→v3.44 (spec_references policy consolidation SC-03; Playwright selector check made conditional SC-06); roadmap_prompt.md v7.1→v7.3 (fatigue guardrail removed SC-04; STEP 9 dangling ref corrected); release_planning_prompt.md v2.36→v2.37 (dead-load advisory steps removed SC-05); post_ship_closure.md v2.13→v2.14 (Advisory Summary Block compressed SC-07) | claude/system/execution_prompt.md v3.44; claude/system/roadmap_prompt.md v7.3; claude/system/release_planning_prompt.md v2.37; claude/system/post_ship_closure.md v2.14 | None |
| EPIC-02 | Yahoo Finance 401 backoff integration test stub (test_yahoo_backoff_path_401_sleep_once_then_200, mocked); DoQ sign-off date compliance audit advisory (v3.7–v3.9, 10 files, 3 findings); QA evidence format audit advisory (v3.7–v4.0, 13 files, 6 findings); Agent idea participation summary (11 closed windows, 22 eligible agents, 100% participation rate); Regression test suite baseline v1.1 (66 backend endpoints, 41 Playwright spec files); Pre-entry panel collapsed badge (warn/fail count when collapsed; additive; SC-PEP-BADGE-01a/01b/02 Playwright coverage) | tests/test_screener_data_service.py::test_yahoo_backoff_path_401_sleep_once_then_200; claude/cycles/2026-06-17__release-v5.9/advisory_doq_audit_v37_v39.md; claude/cycles/2026-06-17__release-v5.9/advisory_qa_format_audit_v37_v40.md; claude/cycles/2026-06-17__release-v5.9/advisory_agent_idea_participation.md; docs/qa/regression_test_suite_baseline.md v1.1; src/pages/TradePlan.js; tests/e2e/pre-entry-panel-badge.spec.js | None |

### Capabilities deferred or returned

None — all 11 stories completed within the sprint. 0 returned to backlog.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (Sprint Execution Engine autonomous class, 2026-06-17; Head of Specs Team agent-mediated cleared 2026-06-17T18:45:00Z), qa_evidence_EPIC-02.md (Director of Quality, 2026-06-18)
- Deviations filed: None
- Test scenarios referenced: tests/test_screener_data_service.py::test_yahoo_backoff_path_401_sleep_once_then_200 (ST-06); tests/e2e/pre-entry-panel-badge.spec.js — SC-PEP-BADGE-01a/01b/02 (ST-11)

---

## Sprint: 2026-06-10__release-v5.5
**Date:** 2026-06-15
**Status:** Sprint_Complete — pending verification

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Governance prompt hardening — sprint_planning_prompt.md date gate advisory; execution_prompt.md pr_status read-after-open + qa_evidence commit discipline | claude/system/sprint_planning_prompt.md; claude/system/execution_prompt.md | None |
| EPIC-02 | Trade count gate-monitoring endpoint (GET /portfolio/gate-metrics) + SI-05 digest data density line | stage4_backlog_slice.md#ST-04/05; backend/database.py#get_gate_metrics | None |
| EPIC-03 | API performance baseline complete (18 endpoints measured; BLG-OPS-13 closed); regression test suite baseline doc (66 endpoints, 41 e2e specs, 387 scenarios); SI-05 user journey map with 2 friction findings (BLG-FE-73/74) | docs/ops/api_performance_baseline.md§18/19; docs/qa/regression_test_suite_baseline.md; docs/ux/si05_user_journey_map.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-11 | Gate date 2026-06-21 not yet reached (SI-03 live ≥ 30 days) | BLG-FE-64 — not eligible before 2026-06-21 |
| ST-12 | Gate date 2026-07-04 not yet reached (≥ 4 weeks production) | BLG-OPS-59 — not eligible before 2026-07-04 |
| ST-13 | Gate date 2026-07-04 not yet reached (effectiveness review) | BLG-GOV-112 — not eligible before 2026-07-04 |
| ST-14 | Gate date 2026-07-04 not yet reached (BLG-GOV-113 protocol) | BLG-GOV-115 — not eligible before 2026-07-04 |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md
- Deviations filed: None
- Test scenarios referenced: tests/test_gate_metrics.py (EPIC-02); docs/qa/regression_test_suite_baseline.md (EPIC-03)

---

## Sprint: 2026-06-08__release-v5.2
**Date:** 2026-06-08
**Status:** Verified — 2026-06-08

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-03 | Claude API model deprecation compliance check — claude-haiku-4-5-20251001 confirmed current; next review 2026-09-08; AI Compliance & Governance Officer sign-off | docs/governance/ai_model_deprecation_check_v52.md | None |
| EPIC-03 | Telegram bot token minimal-permission security review — send-only confirmed from code; BotFather manual verification recommended; Cybersecurity & Trust Lead sign-off | docs/security/security_register.md (Review 002) | None |
| EPIC-03 | SI-05 digest endpoint authentication review — GAP_FOUND: POST /digest/si05/send unauthenticated; BLG-BE-35 P2 filed for fix; Cybersecurity & Trust Lead sign-off | docs/security/security_register.md (Review 003); docs/specs/api_contracts/digest_endpoints.md | None (auth gap filed as BLG-BE-35 P2; fix scoped to future sprint) |
| EPIC-03 | Backend endpoint documentation coverage audit post-v5.1 — 50 routes enumerated; 6 contract gaps found; BLG-SPEC-49/50/51/52 filed; HoE + API Contracts Owner sign-off | docs/ops/endpoint_coverage_audit_v52.md | None (contract gaps filed as BLG-SPEC-49–52) |
| EPIC-02 | SI-05 Telegram delivery retry and failure handling — 30s/60s exponential backoff; max 2 retries; ERROR logging preserved; 3 new unit tests; 24 total passing; staging retry confirmed in Render logs | backend/services/si05_digest_service.py | None |
| EPIC-02 | SI-05 digest delivery log table (si05_digest_log) — CREATE TABLE IF NOT EXISTS guard; log rows on success/failure paths; registered in main.py on_startup(); staging migration and live row confirmed | docs/specs/api_contracts/digest_endpoints.md; backend/database.py | None |
| EPIC-02 | Deployment runbook updated for SI-05 operational environment — §6 added (env vars, cron schedule, service verification, failure detection reference) | docs/ops/production_deployment_runbook.md v0.2 | None |
| EPIC-02 | SI-05 service scheduled run health check procedure v1.0 — 3 check options; escalation path; weekly cadence; responsible role | docs/ops/si05_health_check_procedure.md | None |
| EPIC-04 | SI-05 digest service edge case test gap analysis — 2 missing tests authored; 26 total tests passing; gap analysis document filed | tests/test_si05_digest_service.py; docs/qa/si05_edge_case_gap_analysis.md | None |
| EPIC-04 | SI-05 Phase 1 acceptance test protocol + delivery verification protocol (companion docs) covering v5.1 deferred ACs | docs/qa/si05_acceptance_test_protocol.md; docs/qa/si05_delivery_verification_protocol.md | None |
| EPIC-04 | Regression test suite baseline refresh post-v5.1 — POST /digest/si05/send confirmed in test.py; 5 Playwright scenarios confirmed; BLG-QA-50 filed for formal baseline doc | backend/routers/test.py; tests/e2e/signals-allocation-insufficient.spec.js | None |
| EPIC-04 | SI-05 Phase 1 effectiveness criteria — 3 criteria defined; 30-day review 2026-07-04; PO acknowledged | claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md | None |
| EPIC-01 | release_planning_prompt.md v2.34 — §-1.2 accepts STEP 8.1 Option(b) as valid gate substitute; OA-01 resolved | claude/system/release_planning_prompt.md v2.34 | None |
| EPIC-01 | execution_prompt.md v3.37 — §3.1.A step 2c: test-authoring stories set spec_references to created test file path; OA-02 resolved | claude/system/execution_prompt.md v3.37 | None |
| EPIC-01 | SI-05 pass_rate computation aligned with BLG-GOV-86 §5.2 — Option(a) volume-weighted ratio confirmed canonical; spec v1.2; DEV-v51-EPIC01-01 resolved; BLG-SPEC-47 closed | docs/product/decisions/si05-telegram-message-format-spec.md v1.2; docs/specs/api_contracts/digest_endpoints.md | None (P3 deviation resolved) |
| EPIC-01 | POST /digest/si05/send API contract gap closed — digest_endpoints.md v0.3 with auth requirements section; BLG-SPEC-48 closed | docs/specs/api_contracts/digest_endpoints.md v0.3 | None |

### Capabilities deferred or returned

None. All 16 in-scope stories completed. ST-17 (BLG-FE-64) deferred at sprint planning (gate not clear at seal) — not returned from sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (autonomous class 2026-06-08), qa_evidence_EPIC-02.md (DoQ 2026-06-08), qa_evidence_EPIC-03.md (autonomous class 2026-06-08), qa_evidence_EPIC-04.md (autonomous class 2026-06-08)
- Deviations filed: None (spec deviations); BLG-BE-35, BLG-SPEC-49–52, BLG-QA-50 filed as backlog items
- Test scenarios referenced: tests/test_si05_digest_service.py (26 unit tests)

---

## Sprint: 2026-06-21__release-v5.1
**Date:** 2026-06-21
**Status:** Verified_with_deviations — 2026-06-21

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-02 | delivery_verification_prompt.md §-1.3 Tier 2 patched — agent-mediated signer format now explicitly accepted; v2.9→v3.0; OPERATIONAL_GUIDE.md v4.30→v4.31; BLG-GOV-89 (delivery verification carry-forward) closed | claude/system/delivery_verification_prompt.md v3.0 | None |
| EPIC-03 | SignalCard allocation_insufficient badge Playwright E2E coverage — 5 scenarios (SC-SIG-AI-01/02/03) covering orange badge, reason text, visual distinction from active signals; BLG-FE-61 closed after 3 consecutive carry-forwards | tests/e2e/signals-allocation-insufficient.spec.js | None |
| EPIC-03 | compliance_summary field population validated by code review — all 5 spec fields confirmed present in `get_arc5_compliance_summary()` (`period_days`, `validation_pass_rate`, `override_count`, `red_flag_events_count`, `most_frequent_rule_breach`); staging AC-01 deferred | docs/specs/api_contracts/reports_endpoints.md#compliance_summary | None (staging AC-01 deferred) |
| EPIC-03 | Staged verification sprint protocol document v1.0 — trigger criteria, batching approach, evidence format, sprint sizing; DoQ + PMO Lead sign-off recorded | docs/operations/staged_verification_sprint_protocol.md v1.0 | None |
| EPIC-01 | BLG-SPEC-45 resolved — SI-05 financial reporting confirmed OUT OF SCOPE for Phase 1; decision document filed; FR&R Owner sign-off; BLG-SPEC-45 closed | docs/product/decisions/si05-financial-reporting-scope-decision.md v1.0 | None |
| EPIC-01 | SI-05 Phase 1 weekly Telegram digest — `POST /digest/si05/send`; `backend/services/si05_digest_service.py`; SI-01 + SI-03 data sourcing; MarkdownV2 format per BLG-GOV-86 §4; 5-rule summary line; Telegram delivery via v2.4 infrastructure; 21 unit tests; endpoint total 62; openapi.yaml + test.py + SystemStatus.js + SC-SS-01b all updated in same commit per CLAUDE.md §2 | docs/product/decisions/si05-telegram-message-format-spec.md v1.1; docs/specs/api_contracts/digest_endpoints.md v0.2; docs/reference/openapi.yaml | DEV-v51-EPIC01-01 (P3) — pass_rate computation; BLG-SPEC-47 |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-01 AC-09 — Telegram staging delivery | Staging-only AC; I&O Owner sign-off required in staged verification sprint | Staged verification sprint |
| ST-05 AC-01 — compliance_summary live data verification | Staging-only AC; I&O Owner sign-off required | Staged verification sprint |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ 2026-06-21), qa_evidence_EPIC-02.md (autonomous class 2026-06-21), qa_evidence_EPIC-03.md (DoQ 2026-06-21)
- Deviations filed: DEV-v51-EPIC01-01 (P3 — pass_rate computation method vs BLG-GOV-86 §5.2; BLG-SPEC-47)
- Test scenarios referenced: tests/e2e/signals-allocation-insufficient.spec.js (5 scenarios); tests/test_si05_digest_service.py (21 unit tests)

---

## Sprint: 2026-06-03__release-v5.0
**Date:** 2026-06-03
**Status:** Verified — 2026-06-03

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | prompt_change_log.md verified complete — all 7 BLG-GOV-79 entries confirmed present; AUD-001 gap closed | claude/system/prompt_change_log.md | None |
| EPIC-01 | Agent file headers normalised — 5 non-compliant agent files (ATX heading + Role line) corrected: ai_compliance_governance_officer.md, cybersecurity_trust_lead.md, director_of_hr.md, financial_reporting_records_owner.md, finops_resource_architect.md | claude/agents/ (5 files) | None |
| EPIC-01 | PR template PO acceptance gate — explicit "Product Owner Acceptance (Hard Gate)" section added with GitHub Approve instruction; v1.2→v1.3; BLG-GOV-83 closed | .github/pull_request_template.md | None |
| EPIC-02 | execution_prompt.md STEP 8 structural governance check — git-diff scan replaces operator memory for governance file change log entries; v3.35→v3.36; BLG-GOV-80 closed | claude/system/execution_prompt.md v3.36 | None |
| EPIC-02 | Post-ship audit advisory strengthened — dual-condition trigger (% 3 == 0 OR gap ≥ 4, null-safe); last_audit_cycle_count field added to .claude_current_state.json and lifecycle_schema.json; post_ship_closure.md v2.12→v2.13; BLG-GOV-82 closed | claude/system/post_ship_closure.md v2.13 | None |
| EPIC-03 | allocation_insufficient signal status — new backend status value + reason field; frontend SignalCard orange "Cannot Size" badge + reason inline; openapi.yaml + test.py + SC-SS-01b updated; BLG-FEAT-43 closed | docs/specs/api_contracts/signal_endpoints.md | None |
| EPIC-03 | Pre-entry regime gate fix — shared 5-min cache in check_market_regime(); eliminates independent yf.download from /portfolio/pre-entry-validation; dashboard + pre-entry + signal gen share one result per window; BLG-BE-25 closed | docs/specs/api_contracts/pre_entry_validation.md | None |
| EPIC-03 | Anthropic SDK staging verification — POST /trade-plans/{plan_id}/generate-thesis HTTP 200 + non-null thesis confirmed; POST /ai/check-daily-cost HTTP 200 + cost structure confirmed; BLG-OPS-52 closed | docs/specs/api_contracts/ai_endpoints.md | None |
| EPIC-04 | SI-05 notification channel trade-off + PO decision — Telegram confirmed as delivery channel; BLG-FE-60 closed | docs/product/decisions/si05-notification-channel-tradeoff.md | None |
| EPIC-04 | SI-05 Telegram message format spec v1.0 — section structure, data bindings (GET /analytics/arc5-compliance), character budget (~265/4096), failure modes, weekly schedule; BLG-GOV-86 closed | docs/product/decisions/si05-telegram-message-format-spec.md | None |
| EPIC-04 | SI-02 re-entry trigger criteria — hard gate (≥20 closed trades), soft advisory (≥3 months), formal PMO Lead check from v5.1/2026-09; BLG-GOV-87 closed | docs/product/decisions/si02-reentry-trigger-criteria.md | None |
| EPIC-04 | SI-04 binding conditions formal decisions — all 6 §13 binding conditions formalised; Strategy Rules & System Intent Owner sign-off; BLG-SPEC-43 cross-referenced; BLG-GOV-88 closed | docs/product/decisions/decisions--2026-06-03__release-v5.0--SI-04-binding-conditions.md | None |
| EPIC-04 | SI-02 drift summary feasibility assessment — feasible with conditions; 3 UX risks + mitigations; minimal display scope (Reports page, 3 metrics, advisory framing); PO sign-off; BLG-BE-26 closed | docs/product/decisions/si02-drift-summary-feasibility-assessment.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-14 — SI-05 Phase 1 backend + Telegram delivery (EPIC-04 conditional) | Gate: SI-01 + SI-03 live ≥ 30 days — clears 2026-06-21; conditional Sprint 2 amendment required | backlog.md |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ autonomous class, 2026-06-03), qa_evidence_EPIC-02.md (DoQ autonomous class, 2026-06-03), qa_evidence_EPIC-03.md (I&O + DoQ agent-mediated, 2026-06-03), qa_evidence_EPIC-04.md (DoQ autonomous class via LL-v4.5-EX-01, 2026-06-03)
- Deviations filed: None (spec deviations); BLG-FE-61 filed for ST-06 frontend Playwright gap (backlog only)
- Test scenarios referenced: tests/test_pre_entry_validation.py, backend/routers/test.py (EPIC-03)

---

## Sprint: 2026-06-02__release-v4.9
**Date:** 2026-06-02
**Status:** Verified — 2026-06-02

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | npm devDependency HIGH CVE remediation — 21 HIGH severity CVEs cleared via npm audit fix + overrides; 6 moderate remain (all CRA chain, non-production); security_register.md updated | docs/security/security_register.md | None |
| EPIC-01 | Anthropic SDK upgrade 0.40.0 → 0.105.2 — requirements.txt updated; 447 tests passing; Messages API changelog reviewed (no breaking changes); staging validation (AC-04) deferred post-merge per BLG-OPS-52 | docs/security/security_register.md Upgrade 001 | None |
| EPIC-02 | Real Postgres CI service wired in Phase B — postgres:15 service container; DATABASE_URL injected; 13 pre-existing Phase B test isolation failures surfaced and fixed; Phase A unaffected | .github/workflows/ci-tests.yml | None |
| EPIC-02 | Schema lifecycle column smoke tests — tests/test_schema.py: test_ensure_lifecycle_columns_creates_all_three() proves absent column is detectable; skips in Phase A (stub), passes in Phase B | tests/test_schema.py | None |
| EPIC-03 | roadmap_prompt.md STEP 8.1 gate strengthened — Now horizon empty gate fires on any rebalance (not just Extended tier); both decision options documented with example record formats; OPERATIONAL_GUIDE.md v4.25→v4.26 | claude/system/roadmap_prompt.md v6.8 | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-06 — SI-05 Phase 1 backend + Telegram delivery (EPIC-04) | Gate not met: SI-01 + SI-03 live ≥ 30 days — clears 2026-06-21 | backlog.md |
| ST-07 — SI-05 Phase 1 Playwright coverage (EPIC-04) | Same gate condition; depends on ST-06 | backlog.md |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ autonomous class, 2026-06-02), qa_evidence_EPIC-02.md (DoQ autonomous class, 2026-06-02), qa_evidence_EPIC-03.md (DoQ autonomous class, 2026-06-02)
- Deviations filed: None (spec deviations); BLG-OPS-52 filed for ST-02 AC-04 staging deferral
- Test scenarios referenced: tests/test_schema.py (Phase B schema smoke tests)

---

## Sprint: 2026-06-01__release-v4.8
**Date:** 2026-06-01
**Status:** Verified — 2026-06-02

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | §13 OPERATIONAL_GUIDE Artefact Register — all 7 Class 6 governance prompts verified present in §13 and §14; §14 self-metadata Version corrected 4.20→4.24; sprint_planning_prompt.md v3.6→v3.8 prompt_change_log entries appended (OA clearance) | `claude/system/OPERATIONAL_GUIDE.md` v4.24 | None |
| EPIC-01 | Agent charter header compliance — all 23 agent files verified compliant with `**Role:**` header format; 5 non-compliant files fixed in v4.5 (BLG-GOV-70 pre-met) | `claude/agents/` (23 files, compliance verified) | None |
| EPIC-01 | AUD-2026-05-30-006 gap closed — 3 deferred v4.4 patches (DEL two-phase write, PR status sync, BLG-GOV-19 verification-class sub-criterion) confirmed resolved in v4.5 execution_prompt.md v3.33→v3.34 | `claude/cycles/2026-05-29__release-v4.4/lessons_learnt_closure.md` | None |
| EPIC-02 | Build minutes monitoring policy v1.0 — monthly allocation 400 min, 80% threshold 320 min, billing reset 1st of month, double-capacity assessment (upgrade recommended for v4.9) | `docs/operations/build_minutes_monitoring_policy.md` | None |
| EPIC-02 | Security register v1.0 — pip-audit clean, npm audit 45 vulns (0 critical, 21 HIGH all devDep react-scripts chain), Anthropic SDK 0.40.0→0.105.2 available; BLG-OPS-49 (P1) and BLG-OPS-50 (P2) filed | `docs/security/security_register.md` | None |
| EPIC-02 | Coverage matrix v1.1 — v4.3–v4.7 sections added, compliance_summary regression point (SC-REP-05 reference); GET /reports/monthly-pnl v0.6 contract verified in reports_endpoints.md | `docs/qa/playwright_coverage_matrix.md` | None |
| EPIC-02 | SI-04 strategy version comparison endpoint contract v0.1.0 — GET /analytics/strategy-version-comparison pre-sprint spec; query params, response schema, error cases, 6 §13 binding conditions documented; openapi.yaml placeholder added | `docs/specs/api_contracts/strategy_version_comparison_contract.md` | None |
| Sprint Close | execution_prompt.md v3.35 — STEP 3.1.A step 4a added (LL-v4.8-EX-01): commit SHA record immediately after push; resolves first recurrence of null commit_sha pattern | `claude/system/execution_prompt.md` v3.35 | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-08 (EPIC-03) — SI-05 Phase 1 implementation (BLG-GOV-67) | Gate NOT MET at sprint planning seal: SI-01 + SI-03 live ≥ 30 days clears 2026-06-21; to be scoped in v4.9 | backlog.md |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ autonomous class, 2026-06-01), qa_evidence_EPIC-02.md (DoQ autonomous class, 2026-06-01)
- Deviations filed: None (spec deviations); BLG-OPS-49 (P1 npm HIGH devDep) and BLG-OPS-50 (P2 Anthropic SDK upgrade) filed as security audit findings
- Test scenarios referenced: None — all stories documentation/policy/contract creation only

---

## Sprint: 2026-05-31__release-v4.7
**Date:** 2026-06-01
**Status:** Verified — 2026-06-01

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-03 | Staging deploy live verification: RENDER_STAGING_DEPLOY_HOOK confirmed, code-change deploy trigger verified, docs-only path filter confirmed (BLG-OPS-28 closed) | docs/ops/staging_deploy_verification.md | None |
| EPIC-03 | DS-07 migration staging verification: all 5 SI-02 columns (signal_id, risk_percent_used, portfolio_value_at_entry, pre_entry_validation_snapshot, effective_settings_snapshot) and 3 indexes confirmed on staging (BLG-OPS-44 closed) | docs/ops/ds07_migration_staging_verification.md | None |
| EPIC-03 | Severity field staging verification: severity column, default assignment rule, and backfill (0 nulls) confirmed on staging (BLG-OPS-45 closed) | docs/ops/severity_field_staging_verification.md | None |
| EPIC-03 | Render log retention policy: 7-day platform retention documented; claude_audit_log and red_flag_events confirmed durable; decision: no additional archiving required (BLG-OPS-31 closed) | docs/ops/render_log_retention_policy.md | None |
| EPIC-04 | Anthropic API tier cost assessment: current usage below upgrade threshold; $5/month trigger defined for model review (BLG-OPS-37 closed) | docs/ops/anthropic_api_tier_assessment.md | None |
| EPIC-04 | Pre-entry validation panel UX assessment: 3 improvement candidates ranked by effort/value; no implementation committed; BLG-FE-56/57/58 filed (BLG-FE-49 closed) | docs/product/ux/pre_entry_panel_ux_assessment.md | None |
| EPIC-02 | Arc 5 compliance_summary field in GET /reports/monthly-pnl: adds validation_pass_rate, override_count, red_flag_events_count, most_frequent_rule_breach; null when data unavailable; 2 unit tests + SC-REP-05 Playwright coverage; openapi.yaml updated (BLG-FEAT-38 closed) | docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl v0.6; docs/reference/openapi.yaml | None |
| EPIC-01 | SI-04 §13 formal pre-assessment: determination PASS; 6 binding conditions documented; Arc 5 completion planning path clear (BLG-GOV-62 closed) | docs/product/decisions/si04_section13_preassessment.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-02 — SI-05 Phase 1 Implementation | Gate: SI-01 + SI-03 live ≥30 days (clears 2026-06-21); deferred at planning | BLG-GOV-67 |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ autonomous class 2026-05-31), qa_evidence_EPIC-02.md (Director of Quality agent-mediated 2026-05-31), qa_evidence_EPIC-03.md (DoQ autonomous class 2026-05-31), qa_evidence_EPIC-04.md (DoQ autonomous class 2026-05-31)
- Deviations filed: None
- Test scenarios referenced: tests/test_api_contracts.py (TestReportsEndpoints), tests/e2e/reports-performance-tab.spec.js (SC-REP-05a, SC-REP-05b)

---

## Sprint: 2026-05-30__release-v4.5
**Date:** 2026-05-30
**Status:** Verified — 2026-05-30

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-02 | Agent header standardization: **Role:** format applied to 5 agent files (api_contracts_documentation_owner.md, backend_engineering_patterns_owner.md, data_model_domain_schema_owner.md, frontend_specs_ux_documentation_owner.md, metrics_definitions_analytics_owner.md) | claude/agents/ — 5 files | None |
| EPIC-01 | execution_prompt.md v3.34: four v4.4 OA patches — (1) DEL terminal-status two-phase write LL-v3.9 (ST-01); (2) pr_status sync after PR open LL-v4.5-ST02 (ST-02); (3) verification-class sub-criterion LL-v4.5-EX-01 for pre-planning sprints (ST-03); (4) spec_references policy LL-v4.5-EX-02 for doc-creation stories (ST-04) | claude/system/execution_prompt.md v3.34 | None |
| EPIC-03 | SI-02 spec pre-sprint completion: (ST-06) §13 boundary review — PASS, 9 binding conditions; (ST-07) drift score metric definition — 4 metrics, 90-day window, green/amber/red thresholds, SI-05 integration; (ST-08) data schema pre-definition — 5 fields identified, DS-07 migration script, gap analysis with dispositions | docs/product/decisions/decisions--2026-05-30__release-v4.5--SI-02-section13-review.md; docs/specs/metrics/si02_drift_score.md; docs/specs/data_model/si02_data_schema.md | None |

### Capabilities deferred or returned

None. All 8 stories completed. 0 returned to backlog.

### Verification inputs ready
- QA evidence logs: qa_evidence_EPIC-01.md (autonomous class 2026-05-30), qa_evidence_EPIC-02.md (autonomous class 2026-05-30), qa_evidence_EPIC-03.md (autonomous class + DoQ counter-sign 2026-05-30)
- Deviations filed: None
- Test scenarios referenced: None (governance + spec-only sprint — document inspection verification; no code/automated tests)

---

## Sprint: 2026-05-29__release-v4.4
**Date:** 2026-05-30
**Status:** Verified — 2026-05-29

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | roadmap_prompt.md v6.6: STEP 8.1 advisory for empty Now horizon no-change path (BLG-GOV-71) | claude/system/roadmap_prompt.md v6.6 | None |
| EPIC-01 | sprint_planning_prompt.md v3.8: frontend classification fast-path (3 conditions for autonomous default) (BLG-GOV-72) | claude/system/sprint_planning_prompt.md v3.8 | None |
| EPIC-01 | execution_prompt.md v3.33: auto-set deviations_filed=true on delegation clearance with no DEV-* record (BLG-GOV-73) | claude/system/execution_prompt.md v3.33 | None |
| EPIC-01 | qa_evidence_template.md v1.4: delegated_qa sign-off format — individual + aggregate variants documented (BLG-GOV-69 + BLG-GOV-74) | claude/system/templates/qa_evidence_template.md v1.4 | None |
| EPIC-01 | release_planning_prompt.md v2.32: STEP 7 RESUME PRECHECK note added (v4.3 LL-2 carry-forward) | claude/system/release_planning_prompt.md v2.32 | None |
| EPIC-04 | OPERATIONAL_GUIDE.md v4.19: §7.9 Staging URL Disambiguation subsection — frontend SPA vs backend API hostname distinction, health check guidance (BLG-OPS-43) | claude/system/OPERATIONAL_GUIDE.md v4.19 §7.9 | None |
| EPIC-02 | SI-02 query pre-design: 11 available fields, 6 required gaps, 5 SQL patterns (win_rate_by_setup_type, win_rate_by_regime_at_entry, entry_timing_drift, sizing_adherence, consecutive_loss_context), 3 missing fields for DS-07 (BLG-BE-17) | docs/specs/si02/si02_query_predesign.md | None |
| EPIC-02 | Arc 5 backend architecture review: cached-synchronous pattern recommended (Option B, 8h TTL); ADR-001 filed; async/background approach rejected for Render constraints (BLG-BE-18) | docs/specs/si02/arc5_backend_architecture_review.md | None |
| EPIC-02 | SI-02 query index pre-assessment: 3 indexes identified (idx_trade_plans_signal P1, idx_trade_history_exit/entry_date P2); CREATE INDEX CONCURRENTLY migration plan (BLG-BE-23) | docs/specs/si02/si02_index_preassessment.md | None |
| EPIC-02 | SI-02 background job ADR (ADR-SI02-001): cached-synchronous selected; Render Cron (B1) and APScheduler (B2) rejected; event-triggered (C) rejected under §13 no-side-effects constraint; upgrade path at 150 trades documented (BLG-BE-20) | docs/specs/si02/si02_background_job_adr.md | None |
| EPIC-03 | SI-02 FE component pre-design: Option B (percentage deviation display) selected; data contract — API response shape + 4 component states (loading/insufficient_data/no_drift/drift_detected); props interface for DriftAnalysisPanel + DriftMetricCard (BLG-FE-52) | docs/specs/si02/si02_fe_component_predesign.md | None |
| EPIC-03 | SI-02 FE interaction spec: 5 observable states, non-dismissable + session-collapse model, no drill-down MVP, severity thresholds (ok/approaching/breached hard-coded), ARIA spec, 13 Playwright DFT IDs (DFT-01–DFT-13) (BLG-FE-53) | docs/specs/si02/si02_fe_interaction_spec.md | None |
| EPIC-03 | SI-02 Playwright scenario pre-design: DFT-01–DFT-13 with mock setup + assertion detail; 4 staging-only scenarios (S-STG-01–S-STG-04); mock shape consistent with component pre-design §6.1 API contract; waitFor standard confirmed (BLG-QA-31) | docs/qa/si02_playwright_predesign.md | None |

### Capabilities deferred or returned

None. All 13 stories completed. 0 returned to backlog.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (autonomous class 2026-05-29), qa_evidence_EPIC-02.md (autonomous class 2026-05-30), qa_evidence_EPIC-03.md (autonomous class with note 2026-05-29), qa_evidence_EPIC-04.md (autonomous class 2026-05-29)
- Deviations filed: None
- Test scenarios referenced: None (pre-planning sprint — no code/automated tests; Playwright pre-design DFT-01–DFT-13 authored for SI-02 implementation sprint use)

---

## Sprint: 2026-05-29__release-v4.3
**Date:** 2026-05-29
**Status:** Verified — 2026-05-29

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Governance patches (v4.2 OA resolution): execution_prompt.md v3.31→v3.32 (STEP 3.2.A qa_signed_off advisory + STEP 5.3/8 branch safety gate); qa_evidence_template.md v1.2→v1.3 (1:1 AC mapping advisory); OPERATIONAL_GUIDE.md v4.12→v4.13 (§7.8 staging-only AC pre-designation reference table) | claude/system/execution_prompt.md v3.32; claude/system/templates/qa_evidence_template.md v1.3; claude/system/OPERATIONAL_GUIDE.md v4.13 | None |
| EPIC-01 | AI feature inventory document v1.0: 3 AI features documented (Claude thesis generation, daily cost check, future Arc 6 AI signal scoring); §13 compliance status per feature | docs/ai/ai_feature_inventory.md | None |
| EPIC-04 | Pre-entry check entry price bug fix: PreEntryValidationPanel now correctly receives and propagates entryPrice/stopPrice as props and URL params; SC-TP-21 Playwright test added | docs/specs/api_contracts/pre_entry_validation.md; docs/specs/frontend/pages/trade_plan.md | None |
| EPIC-04 | Claude thesis generation UI copy audit: HAS_GEMINI→HAS_AI, isGeminiLoading→isAiLoading renames; provider-agnostic copy confirmed; SC-TP-22 Playwright test added | docs/specs/frontend/pages/trade_plan.md | None |
| EPIC-04 | Arc 5 compliance score in monthly P&L report: backend get_arc5_compliance_summary() + monthly-pnl strategy_compliance field; frontend Strategy Compliance section with 4 metric cards; SC-REP-05a/05b Playwright tests | docs/specs/frontend/pages/reports.md; docs/specs/api_contracts/reports_endpoints.md v0.5 | None |
| EPIC-03 | API key rotation policy v1.1 + external API key security register v1.2: 5 credentials documented (Alpaca key/secret, ANTHROPIC_API_KEY, News API, Supabase DB); staging-first 8-step rotation procedure; next rotation due 2026-08-25 for ANTHROPIC_API_KEY | docs/ops/api_key_rotation_policy.md v1.1; docs/security/api_key_security_register.md v1.2 | None |
| EPIC-03 | Staging parity report v4.3: all 3 ACs pass — env vars, DB schema, endpoint health checks; env var naming corrected (APCA_* convention); ANTHROPIC_API_KEY added to staging permanently | docs/ops/staging_parity_report_v4.3.md | None |
| EPIC-03 | claude-audit-log performance baseline §16: p50=2,541ms, p95=2,858ms (7 samples, backend API URL); flagged above 500ms threshold — Render starter-tier staging; BLG-OPS-42 closed | docs/ops/api_performance_baseline.md v2.0 §16 | None |
| EPIC-02 | Playwright E2E coverage for Arc5ComplianceSection: 4 tests (SC-ARC5-01/02/03/04) covering heading, stat cards, loading skeleton, error state | tests/e2e/arc5-compliance-section.spec.js | None |
| EPIC-02 | Arc 5 E2E integration test specification v1.0: 20 scenarios (16 Playwright, 4 manual); SI-01→SI-03 data flow; override chain scenarios | docs/qa/arc5_e2e_integration_test_spec.md | None |
| EPIC-02 | CI pipeline baseline documentation v1.0: p50=444s (7.4 min); BLG-QA-27 gate cleared (5 min floor confirmed) | docs/ops/ci_pipeline_baseline.md | None |
| EPIC-02 | Playwright coverage matrix v1.0 + Arc 5 coverage audit v1.0: 39 spec files mapped; 3 zero-coverage features identified; 18 Arc 5 scenarios, 100% Playwright coverage | docs/qa/playwright_coverage_matrix.md; docs/qa/arc5_coverage_audit.md | None |
| EPIC-02 | Staging verifications — Claude thesis generation (AC-01/02/03 pass); ticker validation rejection path (HTTP 422 confirmed); Claude API daily cost alert end-to-end (Telegram received) | claude/cycles/2026-05-29__release-v4.3/qa_evidence_EPIC-02.md | None |

### Capabilities deferred or returned

None. All 18 stories completed and merged.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ 2026-05-29), qa_evidence_EPIC-02.md (DoQ 2026-05-29), qa_evidence_EPIC-03.md (DoQ 2026-05-29), qa_evidence_EPIC-04.md (DoQ 2026-05-29)
- Deviations filed: None
- Test scenarios referenced: tests/e2e/arc5-compliance-section.spec.js; tests/e2e/trade-plan.spec.js; tests/e2e/reports-performance-tab.spec.js

---

## Sprint: 2026-05-27__release-v4.2
**Date:** 2026-05-28
**Status:** Verified — 2026-05-29

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Anthropic API accountability: AI Compliance Officer charter updated with Anthropic API coverage (§4.1); ANTHROPIC_API_KEY security review document v1.0 with tri-authority sign-off | docs/security/anthropic_api_key_scope_review.md; claude/agents/ai_compliance_governance_officer.md | None |
| EPIC-01 | Model version pinning policy v1.0: ai_service.py pinned to MODEL_VERSION=claude-sonnet-4-6; env-var override removed | docs/governance/ai_model_version_pinning_policy.md | None |
| EPIC-01 | Claude API log hygiene policy v1.0: Render logs confirmed clean (ANTHROPIC_API_KEY absent, prompt text absent); log level + retention policy defined | docs/ops/claude_api_log_hygiene_policy.md | None |
| EPIC-02 | API performance baseline update: POST /ai/check-daily-cost baseline added — p50=205ms, p95=518ms | docs/ops/api_performance_baseline.md §14 | None |
| EPIC-02 | First monthly Claude API cost review: 6 calls, $0.007387; monthly cadence (first Thursday) + $5.00/month threshold | docs/ops/claude_cost_review_2026-05.md | None |
| EPIC-02 | Thesis generation latency baseline: p50=3,560ms, p95=3,923ms (10 prod samples); regression threshold p95 > 7,846ms | docs/ops/api_performance_baseline.md §15 | None |
| EPIC-03 | Claude API audit trail: claude_audit_log table + ensure/create/query functions in database.py; GET /ai/claude-audit-log route; 59 total endpoints | docs/specs/api_contracts/ai_endpoints.md v1.2; docs/reference/openapi.yaml | None |
| EPIC-03 | Gemini→Claude spec debt cleared: gemini_thesis_generation.md superseded; ai_thesis_generation.md v2.1.0 canonical; openapi.yaml drift gate PASSED (83/83) | docs/specs/api_contracts/ai_thesis_generation.md v2.1.0 | None |
| EPIC-03 | Claude API Playwright mock strategy v1.0: intercept patterns for 3 Claude-backed endpoints; LIFO alignment; CI guarantee | docs/team_skills/quality/claude_api_playwright_mock_strategy.md | None |
| EPIC-03 | Prompt caching assessment: DEFERRED — gate criteria: ≥1,024-token prefix AND ≥10 calls/day required | docs/governance/claude_prompt_caching_assessment.md | None |
| EPIC-04 | SI-02 sprint planning prerequisites checklist v1.0: 13 items (4 Complete, 1 gate-conditional, 8 Open); integrated at sprint planning STEP -1 | docs/governance/si02_prerequisites_checklist.md | None |
| EPIC-04 | SI-04 scope definition v1.0: date-range versioning, 5 deterministic metrics, two-column comparison UI concept; §13 gate BLG-GOV-62 before sprint planning | docs/governance/si04_scope_definition.md | None |
| EPIC-04 | v4.1 staging sign-off review: deviation trend IMPROVED (v4.1=2 vs v4.0=4); backlog namespace audit 287 BLG IDs, 0 collisions | docs/governance/v41_staging_deviation_review.md | None |

### Capabilities deferred or returned

None. All 13 stories completed and merged.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ 2026-05-28), qa_evidence_EPIC-02.md (DoQ 2026-05-28), qa_evidence_EPIC-03.md (DoQ 2026-05-28), qa_evidence_EPIC-04.md (DoQ 2026-05-28)
- Deviations filed: None
- Test scenarios referenced: None (governance/documentation/ops scope — no new test files)

---

## Sprint: 2026-05-21__release-v3.9
**Date:** 2026-05-22
**Status:** Verified — 2026-05-22

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Screener Data Quality & Reliability: Yahoo Finance 401/crumb retry with exponential backoff+jitter (ST-01); sector/industry fields restored to screener results (ST-02); invalid ticker DAY removed + startup deactivation (ST-03); degraded-run banner (>20% fetch failures → amber warning with failure_rate) in Screener page (ST-04). 7 unit tests; SC-SCR-DEG-01/02 Playwright pass. | backend/services/screener_data_service.py; backend/services/screener_batch_service.py; docs/specs/frontend/pages/screener_results.md; docs/specs/api_contracts/screener_api_contract.md v1.1; openapi.yaml updated | P3 process notation: ST-01 AC-04 integration test deferred to post-merge staging (BLG-QA-24) |
| EPIC-02 | Ticker Universe Enhancements: .L suffix stripped from display labels while preserving API requests (ST-05); company_name column added to ticker_universe table with CSV backfill + management page display as 2nd column (ST-06). SC-TU-DISP-01, SC-TU-COMP-01 Playwright pass. | docs/specs/frontend/pages/ticker_universe.md; docs/specs/api_contracts/ticker_universe_api_contract.md | None |
| EPIC-03 | Arc 5 Red Flag Journal (SI-03): red_flag_events table (id, event_type, ticker, position_id, context, created_at); GET /portfolio/red-flag-journal endpoint (paginated, filterable by event_type/ticker/since); SI-01 pre_entry_override event write on acknowledgement; RedFlagJournal.js frontend with filters, pagination, empty state; Trading nav link. Endpoint total: 60. SC-RFJ-01/02/03 Playwright pass. | docs/specs/api_contracts/portfolio_endpoints.md v2.3; docs/specs/frontend/pages/red_flag_journal.md; docs/design/2026-05-21__release-v3.9/red-flag-journal/ux_spec.md; openapi.yaml; backend/routers/test.py (59→60) | None |
| EPIC-04 | Governance Patches (v3.8 carry-forward, all 5 resolved): execution_prompt.md v3.26 (test_scenarios scope rule + createPageUrl delegation note); sprint_planning_prompt.md v3.4 (deferred_at_planning state); release_planning_prompt.md v2.31 + delivery_verification_prompt.md v2.5 (--dry-run support); PR template v1.2 (QA evidence pre-merge checklist). | claude/system/execution_prompt.md; claude/system/sprint_planning_prompt.md; claude/system/release_planning_prompt.md; claude/system/delivery_verification_prompt.md; .github/pull_request_template.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-13/ST-14 (PT-04 Setup Quality Score) | Gate condition not met: <20 closed trades (PO confirmed 2026-05-22); EPIC-05 deferred at planning | BLG-FEAT-25 |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ 2026-05-22), qa_evidence_EPIC-02.md (DoQ 2026-05-22), qa_evidence_EPIC-03.md (DoQ 2026-05-22, autonomous class), qa_evidence_EPIC-04.md (DoQ 2026-05-22, autonomous class)
- Deviations filed: None (BLG-QA-24 is a process notation, not a spec deviation)
- Test scenarios referenced: tests/test_screener_data_service.py, tests/test_screener_batch_service.py, tests/test_red_flag_journal.py; E2E: tests/e2e/screener.spec.js (SC-SCR-DEG-01/02), tests/e2e/ticker-universe.spec.js (SC-TU-DISP-01, SC-TU-COMP-01), tests/e2e/red-flag-journal.spec.js (SC-RFJ-01/02/03)

---

## Sprint: 2026-05-19__release-v3.8
**Date:** 2026-05-20
**Status:** Verified_with_deviations — 2026-05-20

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-04 | Governance Debt Clearance: `gh_issue_template.md` added to OPERATIONAL_GUIDE §14; DoQ sign-off date enforcement via PR template. Ticker Universe Management Page: TickerUniverse.js live with add/toggle/filter CRUD; `public.tickers` startup sync removed; `ticker_universe` is sole authoritative source for screener and signal generation. 15 Playwright scenarios (SC-TU-01 through SC-TU-06). | claude/system/OPERATIONAL_GUIDE.md §14; docs/specs/api_contracts/ticker_universe_api_contract.md | P3 DEV-EPIC04-ST09-01 (createPageUrl map, resolved in PR #456) |
| EPIC-03 | Trade Plan Form Enhancements: Setup Type dropdown (6 options, pre-selects Momentum Continuation from signal); collapsible News Context Panel (US tickers; Alpaca headlines; localStorage state); AI-Assisted Thesis Generation (Phase 1 template engine; AI draft badge; Gemini hidden when no key). SC-TP-09 through SC-TP-16 pass. | docs/specs/api_contracts/trade_plan_endpoints.md; docs/specs/frontend/pages/trade_plan.md | None |
| EPIC-01 | Arc 5 Strategy Integrity Foundation — SI-01 Pre-Entry Rule Validation: §13 gate PASS with 8 binding conditions; `GET /portfolio/pre-entry-validation` endpoint (5 advisory checks: regime gate, sizing validity, cash constraint, sector concentration, earnings proximity); PreEntryValidationPanel in TradePlan.js (collapsible, non-blocking, override acknowledgement checkbox, pre_entry_override_acknowledged persisted); strategy_rules.md v1.4 §4.2 formalised; 17 backend unit tests; SC-TP-17 through SC-TP-20 pass. Endpoint total: 59. Also includes fix for TickerUniverse nav routing (DEV-EPIC04-ST09-01). | docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/pre-entry-validation; claude/strategy/strategy_rules.md#§4.2; docs/specs/frontend/pages/trade_plan.md; docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-04/ST-05 (PT-04 Setup Quality Score) | Gate condition not met: < 20 closed trades (PO confirmed 2026-05-19); EPIC-02 removed from sprint at planning | Parked in backlog (< 20 trades gate) |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-04.md (DoQ sign-off 2026-05-20), qa_evidence_EPIC-03.md (DoQ sign-off 2026-05-20), qa_evidence_EPIC-01.md (DoQ sign-off 2026-05-20)
- Deviations filed: DEV-EPIC04-ST09-01 (P3 — createPageUrl map, resolved — fix merged PR #456)
- Test scenarios referenced: tests/e2e/ticker-universe.spec.js (SC-TU-01–06), tests/e2e/trade-plan.spec.js (SC-TP-09–20), backend/routers/pre_entry_validation.py (17 unit tests)

---

## Sprint: 2026-05-18__release-v3.7
**Date:** 2026-05-18
**Status:** Verified — 2026-05-18

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-04 | Technical Debt Clearance: database stub conftest consolidation (BLG-QA-20); pycache untracked from git (BLG-OPS-16); Research page typography staging sign-off + Playwright SC-RV-TYP-01 regression (BLG-FE-35); scored_initiatives.md Arc 3–6 comprehensive refresh — IT-01–06, PO-01–05, SI-01–05, PS-01–05 scored (BLG-GOV-23, resolves OA-RP-05). | tests/conftest.py; docs/frontend/design_system.md; claude/scoring/scored_initiatives.md | None |
| EPIC-03 | Governance Prompt Hardening: execution_prompt.md v3.23→v3.24 (deviations_filed atomic write LL-v3.7-EX-01, backlog verify guidance LL-v3.7-EX-02, spec_references path verify LL-v3.7-EX-03); qa_evidence_template.md v1.0→v1.1 (BLG-GOV-19 criterion 3 fail-path advisory). | claude/system/execution_prompt.md v3.24; claude/system/templates/qa_evidence_template.md v1.1 | None |
| EPIC-01 | Signal-to-Watchlist Workflow: `PATCH /signals/{id}` accepts `status=watchlisted`; `watchlisted` field on signals list response; `SignalCard.js` Add to Watchlist CTA + watchlisted state; `SignalContextPanel.js` read-only panel in trade plan form with `entry_rationale`+`confirmation_criteria` pre-population. Playwright E2E: SC-SIG-WL-01/02/03 + SC-TP-SIG-01/02/03/04 (7 scenarios). openapi.yaml + test.py + SystemStatus (57→58 endpoints). data_model.md v2.8. | docs/specs/api_contracts/signal_endpoints.md; docs/specs/frontend/pages/signals.md; docs/design/2026-05-18__release-v3.7/signal-context-panel/ux_spec.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| EPIC-02 (ST-04/05/06 — PT-04 Setup Quality Score) | Gate condition not met: < 20 closed trades (PO confirmed 2026-05-18) | Deferred to v3.8 |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-04.md (DoQ signed 2026-05-18), qa_evidence_EPIC-03.md (autonomous class 2026-05-18), qa_evidence_EPIC-01.md (DoQ signed 2026-05-18)
- Deviations filed: None (zero P0/P1/P2/P3)
- Test scenarios referenced: docs/testing/signals_scenarios.md v1.2 (SC-SIG-WL-01/02/03); docs/testing/watchlist_scenarios.md v1.1 (SC-TP-SIG-01/02/03/04)

---

## Sprint: 2026-05-15__release-v3.5
**Date:** 2026-05-15
**Status:** Verified — 2026-05-15

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-04 | Governance Patches: sprint_planning_prompt.md v3.1 (shared execution_state.json ownership rule + merge order section); execution_prompt.md v3.20 (deviation intent-check advisory, Known Deviations sync advisory, backlog ID uniqueness check, CF-01/CF-02 deviation severity and backlog ID completeness checks). BLG-GOV-22 closed. | claude/system/sprint_planning_prompt.md v3.1; claude/system/execution_prompt.md v3.20 | None |
| EPIC-03 | Spec & QA Debt: grace-period-alert ux_spec.md v1.1 (§5 sessionStorage corrected, dismiss-on-tab-close noted); stop-management-workflow ux_spec.md v1.1 (§4.4 PATCH corrected); React Query v5 onSuccess fix in TradePlan.js (SC-TP-08 Playwright 9/9 pass); Research View Regression Test Protocol v1.0 (SC-RES-01–13 canonical). BLG-SPEC-29/30/31 and BLG-QA-19 closed. | docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md; docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md; docs/qa/acceptance_protocols/research_view_regression_protocol.md | None |
| EPIC-01 | Arc 3 Completion — IT-06 Alpaca Paper Trading: §13 compliance review (PASS determination, 4 binding conditions); `backend/services/alpaca_paper_sync_service.py` + `GET /portfolio/paper-positions`; `PaperAccountPanel` component on Positions page. Playwright E2E: SC-PA-01/02 (5/5 pass). openapi.yaml + test.py + SystemStatus.js (55→57 total endpoints) updated. | docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/paper-positions; docs/ux_specs/paper-trading/ux_spec.md; docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md | None |
| EPIC-02 | Arc 4 Foundation — PO-01 Plan vs Reality: Arc 4 data requirements capture (arc4_data_requirements.md v1.0, PO + HoUX sign-off); `plan_vs_reality` JSONB column on trade_history; `planned_stop_price` on trade_plans; `backend/services/plan_vs_reality_service.py` + `GET /trades/{trade_id}/plan-vs-reality`; `PlanVsReality` component in TradeHistoryTable. Playwright E2E: SC-PVR-01/02 (5/5 pass). openapi.yaml + test.py + SystemStatus.js updated. | docs/specs/api_contracts/trade_endpoints.md#GET /trades/{trade_id}/plan-vs-reality; docs/ux_specs/plan-vs-reality/ux_spec.md; docs/data_model.md; docs/product/arc4_data_requirements.md | None (entry_delta_pct null pending Arc 4 planned_entry_price snapshot — not a deviation per arc4_data_requirements.md §3.1) |

### Capabilities deferred or returned

None. All 13 sprint items completed and merged.

### Verification inputs

- QA evidence logs: qa_evidence_EPIC-04.md (autonomous class), qa_evidence_EPIC-03.md, qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md — all signed 2026-05-15
- Deviations filed: None (zero P0/P1/P2/P3)
- Test scenarios: 10 Playwright scenarios across EPIC-01 (5) and EPIC-02 (5) — 10/10 pass; EPIC-03 SC-TP-08 (9/9 pass); EPIC-04 not applicable (governance)

---

## Sprint: 2026-05-14__release-v3.4
**Date:** 2026-05-14
**Status:** Verified_with_deviations — 2026-05-14

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Arc 3 Frontend Completion: LifecycleBadge component (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN states) with arc3_lifecycle_display feature flag guard; GracePeriodAlertZone with sessionStorage dismiss (§13 display-only); TrailStopModal with PATCH /positions/{id} stop update (§13 guided confirmation required). 10/10 Playwright scenarios (SC-LS-01–04, SC-GP-01–03, SC-TS-01–03) pass. | docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md; docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md; docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md | P3: sessionStorage vs localStorage (DEV-v3.4-01); P3: PATCH vs PUT stop update (DEV-v3.4-02) |
| EPIC-02 | Arc 3 Risk Prompts: GET /portfolio/drawdown-status backend (drawdown % from peak, threshold breach, lifecycle state counts); DrawdownReviewPrompt component (session-scoped dismiss, §13 display-only); GET /portfolio/concentration-status backend (per-position/sector heat %); ConcentrationLimitsWarning component (DS-03 graceful degradation, §13 display-only). 10/10 Playwright scenarios (SC-DD-01–05, SC-CC-01–05) pass. test.py 53→55. | docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md; docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md; docs/reference/openapi.yaml | P3: useState in-memory dismiss — self-resolving (spec §6 spec-compliant) |
| EPIC-03 | Frontend Quick Wins: Research page UK suffix strip (BLG-FE-23); negative/zero earnings days display `—`/`Today` (BLG-FE-24); Signals page defaults to most recent trading day (BLG-FE-25); Watchlist binary research status indicator (BLG-FE-29); Trade plan 7-state colour-coded status badges + abandonment UI with reason field (BLG-FE-30 + BLG-FEAT-21 frontend). 16/16 Playwright scenarios pass. | docs/specs/frontend/pages/trade_plan.md#9 | P3: RQ v5 onSuccess removal — isAbandoned derived from query data (DEV-v3.4-01) |
| EPIC-04 | Spec & QA Debt: Research view component library (docs/frontend/component_library_research_view.md); Screener morning routine UX spec (docs/specs/frontend/pages/screener_morning_routine.md); trade_plan.md §6.2 pre-population fields corrected (BLG-SPEC-28); AI journal review cadence defined (BLG-AI-03); Screener accuracy test protocol (docs/testing/screener_accuracy_protocol.md, BLG-QA-18). | docs/frontend/component_library_research_view.md; docs/specs/frontend/pages/trade_plan.md#§6.2 | None |

### Capabilities deferred or returned

None. All 14 sprint items completed and merged.

### Verification inputs

- QA evidence logs: qa_evidence_EPIC-01.md through qa_evidence_EPIC-04.md — all DoQ signed 2026-05-14
- Deviations filed: 4 P3 (no P0/P1/P2)
- Test scenarios: 36 Playwright scenarios across EPIC-01/02/03 — 36/36 pass; EPIC-04 not applicable (documentation)

---

## Sprint: 2026-05-09__release-v3.3
**Date:** 2026-05-12
**Status:** Verified — 2026-05-13

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Position Lifecycle State Machine: DS-05 data migration (position_state, state_entered_at, state_history columns on positions table); compute_position_state() service (GRACE/PROFITABLE/LOSING/EXIT ZONE/UNKNOWN); GET /positions enriched with lifecycle fields; POST /positions/{id}/refresh-state; 22 unit tests. Feature flag (arc3_lifecycle_display) ready. | docs/specs/data_model.md#DS-05; backend/services/position_lifecycle_service.py | P3: Alembic migration AC vs direct SQL implementation |
| EPIC-02 | Arc 3 Decision Support Backends: GET /positions/grace-period-alerts (grace period counting with graceful fallback); GET /positions/{id}/stop-trail (ATR trail calculation, R-term output). Both endpoints §13 display-only — no automated action. | docs/reference/openapi.yaml#grace-period-alerts; docs/reference/openapi.yaml#stop-trail | None |
| EPIC-03 | Research View Spec & QA Closure: research_endpoint.md API contract; research_view_provenance.md data provenance spec; research_view.md canonical frontend spec; research-view UX spec; 19 research view + 7 entry checklist test scenarios; acceptance test protocol; entry checklist Playwright E2E tests (SC-CL-01–07); research endpoint latency baseline (p50 2500–4000ms); trade plan data sensitivity classification; field extension governance policy. | docs/specs/api_contracts/research_endpoint.md; docs/specs/frontend/pages/research_view.md; tests/e2e/entry-checklist.spec.js | P2: error codes (404/503/429 not returned; always 200 with null sub-fields); P3: entry checklist field name divergence |
| EPIC-04 | Governance Patches: execution_prompt.md v3.17 (sealed-file integrity check STEP 0, mock payload advisory §14); sprint_planning_prompt.md v2.8 (design gate pre-planning check); backlog_management_prompt.md v1.6 (3-cycle deferral policy); backlog_deferral_policy.md created; PT-05 §13 compliance review; feature flag infrastructure (is_flag_enabled(), FEATURE_FLAGS env var, feature_flags.json, startup logging); DS-06 migration (abandonment_reason column on trade_plans); PUT /trade-plans/{id} abandonment guard. | claude/system/execution_prompt.md v3.17; docs/specs/platform/feature_flags.md; docs/specs/data_model.md#DS-06 | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-03 — Position lifecycle state badge (frontend) | delegated_frontend — not completed in sprint | Returned to backlog — next frontend sprint window |
| ST-05 — Grace Period alert card (frontend) | delegated_frontend — not completed in sprint | Returned to backlog — next frontend sprint window |
| ST-07 — Trail Stop panel (frontend) | delegated_frontend — not completed in sprint | Returned to backlog — next frontend sprint window |
| ST-17 — Trade plan status badges + 5 frontend quick wins | delegated_frontend — backend done, frontend deferred | BLG-FE-30, BLG-FE-23, BLG-FE-24, BLG-FE-25, BLG-FE-29 in backlog |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md
- Deviations filed: P3 (ST-01 Alembic vs direct SQL), P2 (ST-08 error codes), P3 (ST-11 field name divergence), P3 (ST-16 reclassification note)
- Test scenarios referenced: tests/e2e/entry-checklist.spec.js (SC-CL-01–07); research view scenarios SC-RV-01–19 (manual/staging)

---

## Sprint: 2026-05-05__release-v3.2
**Date:** 2026-05-06
**Status:** Sprint_Complete — 2026-05-06

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | PT-02 Pre-Trade Research View (frontend): `Research.js` page with price & signal data, prospective heat at entry, trade plan context panel (EntryChecklist read-only, R Target, Edit plan link), recent news headlines; navigation entry points from Screener (`/research/{ticker}` link) and Watchlist (Research button); `GET /portfolio/prospective-heat` wired to prospective heat panel (PT-03). | `docs/specs/frontend/pages/research.md`; `docs/specs/api_contracts/pre_trade_research_endpoints.md` | None |
| EPIC-02 | PT-05 Pre-Trade Entry Checklist: `EntryChecklist` component with 4 default items (signal confirmed, heat limit, stop defined, research reviewed); integrated into TradePlan form (editable, saves via PUT /trade-plans/{id}); read-only display in Research view trade plan panel. Pre-population logic: early_exit_conditions → stop_defined, r_target → research_reviewed. "Review research" link to /research/{ticker}. Observable ACs: code review only — BLG-QA-14 filed (Playwright target v3.3). | `docs/specs/frontend/pages/trade_plan.md#Entry Checklist` | None |
| EPIC-03 | Governance hardening: sprint_planning_prompt.md v2.6 (STEP 0 main-branch verification — OA-02); execution_prompt.md v3.14 (STEP 5.1 deviations_filed enforcement — OA-03; §3.1.A post-story test_scenarios advisory — OA-04; §14 Playwright waitFor standard — OA-05). Playwright test coverage: `tests/e2e/trade-plan.spec.js` SC-TP-01–07 (8 tests, TEST-GAP-EPIC-01 closed); `tests/e2e/earnings-calendar.spec.js` SC-EARN-01–09 (9 tests); `tests/e2e/screener-uk-suffix.spec.js` SC-UK-01–04 (4 tests, TEST-GAP-EPIC-03 closed). | `claude/system/sprint_planning_prompt.md` v2.6; `claude/system/execution_prompt.md` v3.14; `tests/e2e/` | None |
| EPIC-04 | Documentation and security: React component inventory (`docs/specs/frontend/component_inventory.md` — BLG-FE-16); Design system document (`docs/specs/frontend/design_system.md` — BLG-FE-21); Alpaca credential audit and rotation policy (`docs/ops/alpaca_key_rotation_policy.md` — BLG-SEC-05); External API dependency risk register (`docs/ops/external_api_dependency_register.md` — BLG-GOV-18); Cycle artefact inventory review (OPERATIONAL_GUIDE §16 updated — BLG-GOV-11). | `docs/specs/frontend/`; `docs/ops/`; `claude/system/OPERATIONAL_GUIDE.md` §16 | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| BLG-QA-14 — Playwright E2E for entry checklist (PT-05) | Frontend testing gate (LL-v3.1-EX-01): code-review-only AC; BLG-QA-14 filed | v3.3 |

### Verification inputs ready

| Input | Status |
|-------|--------|
| All 4 EPICs merged to main | ✅ PRs #345, #347, #346, #348 |
| QA evidence sign-off | ✅ All 4 EPIC QA evidence files signed off (Director of Quality, 2026-05-06) |
| Delivery verification | ✅ Verified 2026-05-07 |

---

## Sprint: 2026-04-29__release-v3.1
**Date:** 2026-05-05
**Status:** Verified — 2026-05-05

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | PT-01 Trade Plan Object: data model schema (trade_plans table DDL + 3 indexes), 6-endpoint CRUD API, frontend creation/edit/view form; `data_model.md` v2.4→v2.5; `trade_plan_endpoints.md` v0.1; `openapi.yaml` +7 paths; 3 test.py entries (43 total) | `docs/specs/data_model.md#Trade Plan`; `docs/specs/api_contracts/trade_plan_endpoints.md` | None |
| EPIC-02 | PT-02 Pre-Trade Research View (backend): `pre_trade_research_endpoints.md` v0.1 spec (`GET /research/{ticker}` aggregating signal, regime, sector, screener, earnings — all sub-sources null-safe); `backend/routers/research.py`; `openapi.yaml` +1 path; test.py 49 total | `docs/specs/api_contracts/pre_trade_research_endpoints.md` | None |
| EPIC-03 | DS-04 Earnings Calendar: `earnings_endpoints.md` v0.1 (`GET /earnings/{ticker}` via yfinance); `earnings_service.py`; `useEarnings` hook; EarningsBadge on screener, watchlist, positions (⚠ proximity warning ≤5 days); `openapi.yaml` +1 path. BLG-FE-20 UK screener fix: `stripUkSuffix` helper applied to display column and watchlist POST. BLG-QA-10/11: `screener_accuracy_protocol.md` + `screener_scenarios.md` (10 scenarios SCN-01–10). Playwright: `earnings-calendar.spec.js` (SC-EARN-01–09), `screener-uk-suffix.spec.js` (SC-UK-01–04) | `docs/specs/api_contracts/earnings_endpoints.md`; `docs/specs/screener_results_schema.md`; `docs/qa/screener_accuracy_protocol.md`; `docs/qa/screener_scenarios.md` | None |
| EPIC-04 | BLG-FEAT-19 Monthly P&L report: `GET /reports/monthly-pnl` + `MonthlyPnlTable` in Reports.js (3rd tab). BLG-SEC-03/04/GOV-17: `alpaca_key_rotation_policy.md`, `external_api_credential_inventory.md`, `external_api_dependency_register.md`. CF-01/CF-02: `execution_prompt.md` v3.11→v3.13 (reclassification backfill + output target notes) | `docs/specs/api_contracts/reports_endpoints.md`; `docs/ops/`; `claude/system/execution_prompt.md` v3.13 | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| PT-02 frontend (Pre-Trade Research View UI) | Design gate required; deferred to v3.2 per release plan | v3.2 |
| PT-03 (Trade Plan linking from journal) | Gated on PT-01 delivery + design gate | v3.2 |
| PT-05 (Trade Plan analytics) | Gated on volume (20+ trades) | v3.2+ |

### Verification inputs ready

| Input | Status |
|-------|--------|
| All 4 EPICs merged to main | ✅ PRs #323–#326 |
| QA evidence sign-off | ✅ All 4 EPIC QA evidence files signed off (Director of Quality, 2026-04-30) |
| Delivery verification | ✅ Verified 2026-05-05 |

## Sprint: 2026-04-25__release-v3.0
**Date:** 2026-04-27
**Status:** Verified — 2026-04-27

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | DS-01 screener engine: ticker universe data model + 3 endpoints; OHLCV data pipeline (Alpaca US + Yahoo Finance UK/fallback, GBp→GBP conversion); ATR + regime detection + signal scoring (Wilder's 14-period ATR, RSI+MACD+volume, 4-gate pipeline); batch engine + GET /screener/results + POST /screener/run | `docs/specs/api_contracts/ticker_universe_api_contract.md`; `docs/specs/api_contracts/screener_api_contract.md`; `docs/specs/screener_results_schema.md`; `backend/services/` | None |
| EPIC-02 | DS-02 screener results page (sort/filter/regime badges/freshness); DS-07 watchlist promotion flow (inline WatchlistPopover, POST /watchlist, 409 handled); BLG-FE-18 news panel attachment (GET /news/{ticker}, display-only per BLG-GOV-16 §13) | `docs/specs/frontend/pages/screener_results.md`; `src/pages/Screener.js` | DEV-01: ST-11 keyboard shortcuts cross-EPIC committed on EPIC-02 branch (co-delivered with Screener nav in Layout.js); documented in both EPIC QA evidence |
| EPIC-03 | BLG-OPS-12 external API health check (Alpaca + Yahoo Finance in GET /health); BLG-OPS-14 AI journal monitoring metrics (usage_rate, error_rate, p95_latency_ms in GET /health); TEST-GAP-ST14 AI audit service unit tests (12 tests); BLG-FE-19 keyboard shortcuts ('n','w','r' — cross-EPIC, delivered on EPIC-02 branch) | `docs/specs/api_contracts/health_endpoints.md`; `backend/services/health_service.py`; `tests/test_ai_audit_service.py` | None (ST-11 deviation attributed to EPIC-02) |
| EPIC-04 | execution_prompt.md §2 + §3.1.A deferred patches (v3.11); prompt_change_log.md retrospective scan (no gaps found); BLG-FEAT-18 consecutive losing streak metric (analytics compute + metrics_definitions.md v1.10.0); BLG-AI-02 model version contract for AI journal (Class 2 canonical spec, claude-haiku-4-5-20251001) | `claude/system/execution_prompt.md` v3.11; `docs/specs/metrics_definitions.md` v1.10.0; `docs/specs/ai_journal_model_contract.md` | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| DS-04 Earnings Calendar | No spec; independent of screener; M effort | v3.1 |
| BLG-FEAT-13 Feature Flags | P3, M effort; lower priority than Arc 1 | v3.1 |
| BLG-FEAT-19 Monthly P&L Summary | Arc 2 reporting scope | v3.1 |
| BLG-FE-16 React Component Inventory | P3, M effort; capacity constraint | v3.1 |

### Verification inputs ready

| Input | Status |
|-------|--------|
| All 4 EPICs merged to main | ✅ PRs #301–#304 |
| QA evidence sign-off | ✅ All 4 EPIC QA evidence files signed off |
| Delivery verification | ✅ Verified 2026-04-27 |

---

## Sprint: 2026-04-22__release-v2.9
**Date:** 2026-04-24
**Status:** Verified_with_deviations — 2026-04-24

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-03 | §13 review record for DS-06 news panel (BLG-GOV-16 gate cleared); external API mock harness for CI (Alpaca + Yahoo Finance intercepts, 7 smoke tests); screener test data library (12 scenarios, 10+ synthetic tickers) | `docs/product/decisions/sec13_review_DS-06_alpaca_news_panel.md`; `tests/mock_harness/`; `tests/mock_harness/fixtures/` | None |
| EPIC-01 | Screener results schema spec (BLG-SPEC-21); Alpaca integration contract (BLG-SPEC-22); screener internal API contract (BLG-SPEC-23); screener results page UX spec (BLG-FE-17) — all four Arc 1 specification artefacts; DS-01 screener engine unblocked for v3.0 | `docs/specs/screener_results_schema.md`; `docs/specs/api_contracts/alpaca_integration_contract.md`; `docs/specs/api_contracts/screener_api_contract.md`; `docs/specs/frontend/pages/screener_results.md` | None |
| EPIC-04 | execution_prompt.md v3.10: BLG-GOV-14 reclassification counter-sign rule + EPIC-level consolidation note (§3.2.A); BLG-GOV-15 STEP 5.1.B System Status Report integrity advisory; SystemStatus.js /ai prefix categorisation fix; AI audit log (`ai_audit_log` table, SHA-256 hashing, `GET /ai/journal-summary/history`); AI test scenario coverage (4 scenarios) | `claude/system/execution_prompt.md` v3.10; `src/pages/SystemStatus.js`; `backend/services/ai_audit_service.py`; `docs/testing/ai_scenarios.md` | None |
| EPIC-02 | DS-03 sector & industry classification (virtual fields on positions, Yahoo Finance enrichment, 9 unit tests); DS-05 Alpaca US market data integration (OHLCV v2, Yahoo Finance fallback, 10 integration tests); DS-06 Alpaca news panel (display-only per BLG-GOV-16 §13, watchlist toggle, UK tickers excluded) | `backend/services/sector_service.py`; `backend/services/alpaca_service.py`; `backend/services/news_service.py`; `backend/routers/news.py`; `src/pages/Watchlist.js` | DEV-01: DS-06 news panel on screener results page deferred to v3.0 (DS-02 implementation prerequisite not yet built) |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| DS-06 screener results page news panel (ST-07 AC-1 partial) | DS-02 (screener results page) deferred to v3.0; backend endpoint available | v3.0 (DS-02) |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-03.md, qa_evidence_EPIC-01.md, qa_evidence_EPIC-04.md, qa_evidence_EPIC-02.md — all DoQ sign-off complete
- Deviations filed: DEV-01 (P3 — DS-06 screener results page deferred; scope constraint, not defect)
- Test scenarios referenced: `tests/test_api_mock_harness.py` (7 smoke), `tests/test_sector_service.py` (9 unit), `tests/test_alpaca_integration.py` (10 integration), `docs/testing/ai_scenarios.md` (4 scenarios)
- v3.0 prerequisites: all 10 Arc 1 prerequisites delivered and merged

---

## Sprint: 2026-04-13__release-v2.7
**Date:** 2026-04-16
**Status:** Verified — Shipped 2026-04-16

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Supabase Supavisor connection pooling enabled on staging and production (p50 GET /portfolio = 234ms); `get_portfolio_summary()` refactored to single DB connection per request | `docs/ops/api_performance_baseline.md` v1.2; `docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio` | None |
| EPIC-02 | QA evidence sign-off gate added to execution engine (§3.2.B); autonomous DoQ sign-off class defined for code-review-only EPICs (§3.2.A); governance_sync.yml extended to trigger on push to main | `claude/system/execution_prompt.md` v3.6; `claude/system/delivery_verification_prompt.md` v2.0; `.github/workflows/governance_sync.yml` | None |
| EPIC-03 | Playwright LIFO route ordering bug fixed across 4 spec files (30/30 tests pass); System Status Playwright spec authored (16/16 tests pass; 28-endpoint mock; Alerts/Notifications/Digest category routing verified) | `tests/e2e/reports-performance-tab.spec.js`; `tests/e2e/slippage-tracking.spec.js`; `tests/e2e/fee-drag-trade-history.spec.js`; `tests/e2e/signals-cash-balance.spec.js`; `tests/e2e/system-status.spec.js` | None |
| EPIC-04 | `GET /analytics/market-correlation` backend endpoint (Pearson correlation, 252-day lookback, 8h cache, SPY/FTSE benchmark, graceful Yahoo Finance fallback); four supplementary indicator fields added to `POST /signals/generate` (`relative_strength_pct`, `week52_high_proximity_pct`, `avg_daily_volume_20d`, `price_vs_50d_ma`) | `docs/specs/api_contracts/analytics_endpoints.md` v2.1.0; `docs/specs/api_contracts/signal_endpoints.md` v1.1; `docs/reference/openapi.yaml` v2.6.0 | AC-6 (market correlation frontend rendering) deferred to future frontend story — backend contract fully specified |
| EPIC-05 | Spec Dependency Map created (`docs/specs/spec_dependency_map.md` v1.0, four-tier structure, Head of Specs Team sign-off); Governance Health Score added to OPERATIONAL_GUIDE.md §15 and roadmap_prompt.md STEP -1.7 (advisory only) | `docs/specs/spec_dependency_map.md` v1.0; `claude/system/OPERATIONAL_GUIDE.md` §15; `claude/system/roadmap_prompt.md` v4.9 | None |

### Capabilities deferred

None. All 11 stories completed. AC-6 (frontend rendering for market correlation) is an in-spec deferred AC, not a returned story.

### QA summary

- QA evidence logs: qa_evidence_EPIC-01.md through qa_evidence_EPIC-05.md — all signed off
- Deviations filed: none (process notations in sprint_close.md are autonomous-class sign-off records, not spec deviations)
- Velocity: 11/11 (1.00); 6-cycle rolling average: 0.99

---

## Sprint: 2026-04-05__release-v2.5
**Date:** 2026-04-10
**Status:** Verified_with_deviations — Shipped 2026-04-10

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | System Status auth forwarding fixed (POST /test/endpoints now forwards X-API-Key); endpoint test list synced to 26 endpoints (openapi.yaml parity); Alerts, Notifications, Digest endpoint categories added to UI | backend/services/health_service.py; backend/routers/test.py; src/pages/SystemStatus.js | None |
| EPIC-02 | Reports and Signals page backend integration documented (gaps GAP-R01/R02, GAP-S01–S03 identified, backlog items filed); GET /notifications/preferences outlier latency fixed (redundant ensure_alerts_tables() removed); GET /portfolio architectural constraint documented; Supavisor recommendation filed | docs/ops/reports_integration_review.md; docs/ops/signals_integration_review.md; docs/ops/api_performance_baseline.md v1.1; backend/services/alerts_service.py | None |
| EPIC-03 | GitHub Actions curl calls hardened with --max-time 120 (alert-evaluation.yml, daily-snapshot.yml); Avg Slippage StatsCard gradient fix closure documented; Fee Drag % metric end-to-end: backend (fee_drag_pct, avg_fee_drag_pct), API contract (v2.2.0), openapi.yaml (v2.5.0), Trade History table (amber column, sortable), StatsCard (Avg Fee Drag); DataTable.js TableHead onClick bug fixed | .github/workflows/alert-evaluation.yml; .github/workflows/daily-snapshot.yml; docs/testing/slippage_scenarios.md v1.2; docs/specs/api_contracts/trade_endpoints.md v2.2.0; docs/reference/openapi.yaml v2.5.0; docs/specs/metrics_definitions.md v1.9.0; src/pages/TradeHistory.js; src/components/trades/TradeHistoryTable.js; src/components/ui/DataTable.js | P3 UX observations: BLG-FE-11/12/13 filed |
| EPIC-04 | Governance prompt patches CF-2: execution_prompt.md STEP 8 edit check, delivery_verification_prompt.md pre-seal Date gate (both v-bumped); governance_sync.yml batch push fix (git log range); backlog placement rule formalised; test scenarios SC-ATR-01, SC-DEDUP-01/02, SC-STOP-01 filed | claude/system/execution_prompt.md v3.1; claude/system/delivery_verification_prompt.md v1.8; .github/workflows/governance_sync.yml; docs/testing/atr_scenarios.md; docs/testing/dedup_scenarios.md; docs/testing/stop_price_scenarios.md | P3: ST-10 live multi-commit test deferred to next push |

### Capabilities deferred or returned

None. All 13 planned stories delivered (velocity 1.00).

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md
- Deviations filed: DataTable.js TableHead onClick (P2, fixed); BLG-FE-11/12/13 (P3 UX); ST-10 live test deferred (P3)
- Test scenarios referenced: docs/testing/slippage_scenarios.md, docs/testing/atr_scenarios.md, docs/testing/dedup_scenarios.md, docs/testing/stop_price_scenarios.md

---

## Sprint: 2026-03-31__release-v2.4
**Date:** 2026-04-03
**Status:** Verified_with_deviations — post-ship closure complete 2026-04-03

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | ATR pence→GBP conversion fix for UK (.L) tickers (always-on, guard removed); notification dispatch deduplication for all four alert types (calendar-day dedup, logged); initial stop price exposed on analytics trade endpoint via positions LEFT JOIN | backend/utils/pricing.py; backend/services/alerts_service.py; docs/specs/api_contracts/alerts_endpoints.md v0.4 | None |
| EPIC-02 | P&L (GBP) column added to Positions table (separate from P&L % column, colour-coded); user-facing error message mapping layer (friendlyErrorMessage utility, HTTP 400/404/500 mapped to readable messages) | src/pages/Positions.js; src/lib/apiError.js | Resolves DEV-EPIC02-ST05-03 (P2) |
| EPIC-03 | portfolios and trade_history table schemas reconciled against actual Supabase DB (direct DB confirmation); 13 divergences corrected across both tables; data_model.md v2.0→v2.3 | docs/specs/data_model.md v2.3 | None |
| EPIC-04 | GET /digest/weekly backend endpoint (7-day realised P&L, unrealised delta, alerts, compliance, staleness); WeeklyDigest frontend page (DataTable, null handling, nav registered); digest_endpoints.md v0.1; openapi.yaml v2.4.0 | docs/specs/api_contracts/digest_endpoints.md v0.1; src/pages/WeeklyDigest.js; tests/e2e/weekly-digest.spec.js | None |
| EPIC-05 | Render hosting tier decision record (free tier sufficient; GitHub Actions <1% utilisation); API endpoint performance baseline (21 GET endpoints measured, p50/p95 documented; Supabase free tier overhead identified; 4 backlog items filed); slippage tracking test scenario file (SC-SLIP-01–04, Playwright spec, manual runbook); cycle velocity metric defined and backfilled 6 cycles | claude/cycles/2026-03-31__release-v2.4/render_tier_decision_ST10.md; docs/ops/api_performance_baseline.md v1.0; docs/testing/slippage_scenarios.md; claude/cycles/velocity_metrics.md | DEV-ST14-01 (P3 cosmetic, pre-accepted) |
| EPIC-06 | Action-now execution_prompt.md patches (LL-v2.2-EX-01/02/04 — second recurrences resolved); delivery_verification_prompt.md deviation compliance sync; execution_prompt.md delegation model update + delegation log line count check; release planning artefact sealing simplified (SHA-256 hashes removed) | claude/system/execution_prompt.md v2.9; claude/system/delivery_verification_prompt.md v1.7; claude/system/release_planning_prompt.md | None |

### Capabilities deferred or returned

None. All 17 planned stories delivered (velocity 1.00).

### Known issues at close (backlog items filed)

| ID | Title | Priority |
|----|-------|----------|
| BLG-OPS-11 | Add --max-time 120 to GitHub Actions cron curl calls | P4 |
| BLG-OPS-12 | Fix auth forwarding in POST /test/endpoints internal calls | P2 |
| BLG-OPS-13 | Keep endpoint test list in sync with openapi.yaml | P3 |
| BLG-BE-07 | Investigate high external baseline latency on DB-backed endpoints | P2 |
| BLG-FE-07 | Fix System Status endpoint categorisation for v2.3/v2.4 routes | P4 |
| BLG-GOV-10 | Fix governance_sync.yml batch push (closes only last commit's issue) | P2 |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md through qa_evidence_EPIC-06.md — all signed off (EPIC-01/02/05 DoQ 2026-04-03; EPIC-03 HoE + DoQ 2026-04-02/03; EPIC-04 QA Lead + DoQ 2026-04-01/03; EPIC-06 DoQ 2026-04-03 — filed at delivery verification preflight)
- Deviations filed: DEV-EPIC02-ST05-03 resolved by ST-04; DEV-ST14-01 (P3 cosmetic, pre-accepted)
- Test scenarios referenced: tests/e2e/weekly-digest.spec.js (SC-DIG-01–05); tests/e2e/slippage-tracking.spec.js (SC-SLIP-02a–02d, 03a–03b, 04a–04b); docs/testing/slippage_manual_runbook.md (SC-SLIP-01)
- Delegation log: all 3 entries terminal (Unblocked — DEL-20260401-01/02/03)
- Performance baseline: docs/ops/api_performance_baseline.md v1.0 — 21 GET endpoints measured

---

## Sprint: 2026-03-24__release-v2.3
**Date:** 2026-03-30
**Status:** Verified_with_deviations — post-ship closure complete 2026-03-30

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | StrategyCompliancePanel (display-only, per-position stop/size compliance, collapsible, auto-expands on violation); MetricsStalenessIndicator (data-freshness badge, staleness age, per-metric tooltip) | docs/specs/frontend/components/strategy_compliance_panel.md; docs/specs/frontend/components/metrics_staleness_indicator.md | None |
| EPIC-02 | UnderwaterChart zoom/pan (wheel zoom, drag pan, reset); MonthlyHeatmap tile drill-down modal (per-trade table, R-multiple, exit reason); R-Multiple Distribution histogram | docs/specs/frontend/pages/analytics.md §3, §4, §5 | None material; Playwright selector fragility fixes post-merge (CI only, no functional regression) |
| EPIC-03 | GET /health/database endpoint (DB size monitor, Telegram alert at threshold); health_endpoints.md v1.2; health_check_playbook.md (3 failure modes) | docs/specs/api_contracts/health_endpoints.md v1.2 | DEV-HEALTH-001 (P2, closed) |
| EPIC-04 | Sidebar navigation groups + collapsible sections; responsive layout improvements; lucide-react icon polish; nav keyboard accessibility | docs/specs/frontend/pages/layout.md | None |
| EPIC-05 | Monthly performance calendar widget; lessons learnt carry-forward; backlog slice health gate (BLG-HEALTH-01–03) | claude/system/ prompt updates | None; ST-17 (engine prompt compression) returned to backlog |

### Capabilities deferred or returned

| Item | Backlog entry | Reason |
|------|--------------|--------|
| ST-17 — Engine prompt compression | BLG-GOV-08 | Stretch goal; Sprint 3 capacity exhausted. Returned to backlog at P3. |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md through qa_evidence_EPIC-05.md — all signed off
- Deviations filed: none new this sprint (DEV-HEALTH-001 closed in EPIC-03)
- Test scenarios referenced: tests/e2e/chart-interactivity.spec.js (SC-CHART-IX-01a–06b); tests/e2e/ staleness indicator scenarios (SC-STALE-01–05)
- Delegation log: all 13 entries terminal (1 Unblocked, 12 Cancelled per 2026-03-26 autonomous reclassification)

---

## Sprint: 2026-03-21__release-v2.2
**Date:** 2026-03-24
**Status:** Verified_with_deviations — post-ship closure in progress

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | X-API-Key authentication middleware (all endpoints except GET /health); Content Security Policy meta tag | docs/specs/api_contracts/conventions.md §1 v1.1; public/index.html CSP | None / CSP no prior spec (absence note only) |
| EPIC-02 | Alert Scheduling design decisions (trigger mechanism, cooldown, data source, cron mechanism); Alert Threshold Customisation UI (inline edit, validation, PATCH /alerts/rules/{rule_id}); Alert History Table (evaluation log, sort, filter, row-expand, load-more); backend alert_evaluations table + GET /alerts/history + GitHub Actions cron | docs/specs/frontend/pages/notifications.md §2 + §Page 3; docs/specs/api_contracts/alerts_endpoints.md v0.3; docs/product/decisions/decisions--2026-03-21__release-v2.2.md §ST-03 | DEV-EPIC02-ST04-01 (P3), DEV-EPIC02-ST05-01 (obs), DEV-EPIC02-ST05-02 (P2) |
| EPIC-03 | CSV export function name bug fix (get_all_trade_history → get_all_closed_trades_for_csv_export); Slippage StatsCard gradient key fix (cyan → violet); Operational health check endpoint (db check, last_alert_evaluation, last_market_status_check) | docs/specs/api_contracts/trade_endpoints.md#GET /trades/export/csv; docs/specs/frontend/pages/trade_history.md#Avg Slippage StatsCard; docs/specs/api_contracts/health_endpoints.md#GET /health | DEV-HEALTH-001 (P2) |
| EPIC-04 | Notification scenario execution (SC-NOTIF-01–08, 9 Playwright tests pass); Watchlist test scenarios created (SC-WATCH-01–06); Test automation readiness assessment (4-phase plan aligned to BLG-QA-01); Spec-to-test traceability matrix (54 ACs, 22 TEST-GAP entries) | docs/testing/notifications_scenarios.md; docs/testing/watchlist_scenarios.md; docs/testing/test_automation_readiness.md; docs/testing/spec_to_test_traceability_matrix.md | TEST-GAP-007 (P1, HoST v2.3 action) |
| EPIC-05 | Provisional-Target field at backlog promotion (roadmap STEP 9 + §16.6); scored_initiatives.md effort band handoff for release planning (STEP 0 + STEP 4.5 + §16.7); structured lessons learnt carry-forward block in all engines (§16.8, post_ship STEP 8.5, engine STEP 0 advisories) | claude/system/roadmap_prompt.md v4.5; claude/system/release_planning_prompt.md v2.24; claude/system/sprint_planning_prompt.md v2.3; claude/system/post_ship_closure.md v2.1; claude/system/shared_standards.md v2.7; claude/system/lessons_learnt_prompt.md v1.8 | None |

### Capabilities deferred or returned

None — all 15 sprint items delivered.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md, qa_evidence_EPIC-05.md
- Deviations filed: DEV-EPIC02-ST04-01 (P3), DEV-EPIC02-ST05-02 (P2), DEV-HEALTH-001 (P2), TEST-GAP-007 (P1)
- Test scenarios referenced: docs/testing/notifications_scenarios.md (SC-NOTIF-01–08), docs/testing/watchlist_scenarios.md (SC-WATCH-01–06)

---

## Sprint: 2026-03-18__release-v2.1
**Date:** 2026-03-21
**Status:** Verified_with_deviations — cycle closed 2026-03-21

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Async notification delivery ADR | docs/adr/ADR-003 | None |
| EPIC-02 | Alerts & Notifications — full stack (rules engine, Telegram delivery, preferences UI, notification feed) | docs/specs/api_contracts/alerts_endpoints.md, docs/specs/frontend/pages/notifications.md | DEV-ST04-01: Telegram delivery (email blocked on Render free tier) |
| EPIC-03 | Watchlist monitoring — spec, backend, frontend | docs/specs/api_contracts/watchlist_endpoints.md, docs/specs/frontend/pages/watchlist.md | Branch deviation (cherry-pick) |
| EPIC-04 | Chart interactivity — tooltips, zoom/pan, heatmap drill-down | docs/specs/frontend/pages/analytics.md | None |
| EPIC-05 | Tax Year P&L PDF + CSV exports; slippage tracking; Render PR preview environments | docs/specs/api_contracts/reports_endpoints.md, docs/specs/frontend/pages/trade_history.md | DEV-ST14-01: cosmetic null-state colour (P3) |
| EPIC-06 | Spec debt cleared; spec coverage inventory; chart QA scenarios; zero cross-EPIC process violations | docs/specs/spec_coverage_inventory.md, docs/testing/chart_interactivity_scenarios.md | None |

### Capabilities deferred or returned

None — all 19 sprint items delivered.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md, qa_evidence_EPIC-05.md, qa_evidence_EPIC-06.md
- Deviations filed: DEV-ST04-01 (P2), DEV-ST14-01 (P3)
- Test scenarios referenced: docs/testing/notifications_scenarios.md, docs/testing/chart_interactivity_scenarios.md

---

# System Status Verification Report

**Date:** February 14, 2026
**Environment:** Production (Render + GitHub Pages)

---

## ✅ Health Check Results

### Overall Status: **HEALTHY** ✅
```json
{
  "status": "healthy",
  "version": "1.4.0",
  "responseTime": 855.98ms
}
```

### Component Health

| Component | Status | Details |
|-----------|--------|---------|
| Database | ✅ Healthy | PostgreSQL connected, portfolio exists, journal tables present |
| Yahoo Finance | ✅ Healthy | External API accessible, FX rate: 1.3642 |
| Services | ✅ Healthy | All 5 modules loaded and operational |
| Config | ✅ Healthy | Settings table exists and loaded |

---

## ✅ Endpoint Test Results

### Summary: **100% PASS RATE** 🎉

```
Total Tests: 12  (Updated: +1 new endpoints)
Passed: 12 ✅
Failed: 0
Errors: 0
Success Rate: 100.0%
```

### Detailed Results

| Endpoint | Status | Response Time | Notes |
|----------|--------|---------------|-------|
| GET / | ✅ Pass | 255ms | Fast |
| GET /health | ✅ Pass | 262ms | Fast |
| GET /settings | ✅ Pass | 516ms | Normal |
| GET /positions | ✅ Pass | 3,566ms | Expected (Yahoo API calls) |
| GET /portfolio | ✅ Pass | 4,371ms | Expected (Yahoo API calls) |
| GET /trades | ✅ Pass | 587ms | Normal |
| GET /cash/transactions | ✅ Pass | 598ms | Normal |
| GET /cash/summary | ✅ Pass | 602ms | Normal |
| GET /signals | ✅ Pass | 632ms | Normal |
| GET /market/status | ✅ Pass | 1,522ms | Normal (3 Yahoo API calls) |
| GET /portfolio/history | ✅ Pass | 569ms | Normal |
| **GET /positions/tags** | ✅ **Pass** | **543ms** | **NEW v1.4** |


---

## 📊 Performance Analysis

### Fast Endpoints (< 700ms)
All database-only endpoints perform excellently:
- Settings, trades, cash, signals, tags: 500-650ms
- Root and health: 250-300ms

### Slower Endpoints (1-5s) - **EXPECTED**
These endpoints make external API calls to Yahoo Finance:

**GET /positions (3.6s):**
- Fetches live prices for all open positions
- Multiple Yahoo Finance API calls
- Rate limiting delays (300ms between calls)
- **This is by design** to prevent IP bans

**GET /portfolio (4.4s):**
- Fetches live prices for all positions
- Comprehensive portfolio calculation
- Same Yahoo Finance rate limiting

**GET /market/status (1.5s):**
- Fetches SPY price + 200-day MA
- Fetches FTSE price + 200-day MA
- Fetches live GBP/USD FX rate
- **Total: 3 external API calls**

### ⚡ Potential Optimizations (Optional)

**Cache Implementation (Not Required, Just Optional):**
- Add 5-minute cache for live prices
- Would reduce /positions from 3.6s → ~500ms
- Trade-off: Slightly stale prices vs speed
- **Recommendation:** Leave as-is for MVP, prices are more important than speed

---

## 🎯 System Capabilities Verified

### ✅ Core Features Working
- Portfolio management
- Position tracking with live prices
- Multi-currency support (USD/GBP)
- Cash transaction tracking
- Trade history recording
- Market regime monitoring
- Signal generation
- Settings management

### ✅ Trade Journal Features (NEW v1.4)
- Entry notes (500 char limit)
- Exit notes (500 char limit)
- Tag system (max 10 tags per position)
- Tag autocomplete
- Tag filtering in trade history
- Expandable journal rows
- Notes preserved in trade history

### ✅ Infrastructure Working
- Database connectivity
- External API integration (Yahoo Finance)
- Service layer architecture
- Error handling
- CORS configuration
- Production deployment

### ✅ Monitoring Working
- Health checks operational
- Automated endpoint testing
- Component-level diagnostics
- Real-time status dashboard
- Response time tracking

---

## 📋 Post-Deployment Checklist

### Backend Verification
- [x] All endpoints return 200 OK
- [x] Database queries executing correctly
- [x] External API calls working (Yahoo Finance)
- [x] Service modules loaded
- [x] Error handling in place
- [x] CORS configured for GitHub Pages
- [x] Journal endpoints operational (v1.4)
- [x] Tag validation working (v1.4)

### Frontend Verification
- [x] Status page loads
- [x] Health check displays correctly
- [x] Endpoint tests run successfully
- [x] Auto-refresh working
- [x] Component details expandable
- [x] Environment variable loaded correctly
- [x] Journal UI components rendering (v1.4)
- [x] Tag filtering working (v1.4)

### Data Integrity
- [x] Portfolio data accessible
- [x] Positions retrievable
- [x] Cash transactions recorded
- [x] Trade history available
- [x] Settings loaded
- [x] Signals retrievable
- [x] Journal notes persist (v1.4)
- [x] Tags stored correctly (v1.4)

---

## 🚀 Deployment Status

### Production URLs
- **Frontend:** https://sachiv1984.github.io/swing-trading-model
- **Backend:** https://trading-assistant-api-c0f9.onrender.com

### Environment
- Frontend: GitHub Pages (Static Hosting)
- Backend: Render (Cloud Platform)
- Database: PostgreSQL (Render Managed)
- Architecture: React SPA + FastAPI + PostgreSQL

### Version Info
- Backend Version: 1.4.0
- Frontend Version: 1.4
- Health API: ✅ Operational
- Test API: ✅ Operational
- Journal API: ✅ Operational (v1.4)

---

## 🎓 Lessons from Test Results

### What We Learned

**1. External API Calls Are Slow (Expected)**
- Yahoo Finance calls take 1-5 seconds
- This is normal and by design
- Rate limiting prevents IP bans
- Trade-off: Accuracy > Speed

**2. Database Operations Are Fast**
- All DB queries < 700ms
- PostgreSQL performing well
- Indexes working correctly
- GIN indexes optimize tag queries (v1.4)

**3. System Architecture Is Sound**
- All components healthy
- No service failures
- Clean separation of concerns
- Error handling working

**4. Production Deployment Successful**
- Frontend serving from GitHub Pages
- Backend running on Render
- CORS configured correctly
- Environment variables loaded

**5. Journal System Performance (NEW v1.4)**
- Tag queries very fast (~5ms with GIN index)
- Notes stored efficiently in TEXT fields
- Tag autocomplete responsive
- No performance impact on main queries

---

## 🎉 Summary

**Overall Assessment:** EXCELLENT ✅

The system is:
- ✅ Fully operational
- ✅ All endpoints working
- ✅ 100% test pass rate
- ✅ Production-ready
- ✅ Well-architected
- ✅ Properly monitored
- ✅ **Trade Journal fully integrated (v1.4)**

**Confidence Level:** 10/10

The system is ready for:
- Production use
- Feature development
- Performance monitoring
- User onboarding
- **Trading journal workflows (v1.4)**

---

## 🆕 New Features in v1.4

### Trade Journal & Notes System
**Implemented:** February 14, 2026

**Features:**
- ✅ Entry notes when creating positions (500 char limit)
- ✅ Exit notes when closing positions (500 char limit)
- ✅ Tag system for categorizing trades
- ✅ Tag autocomplete from existing tags
- ✅ Tag filtering in trade history (OR logic)
- ✅ Expandable journal rows in trade history
- ✅ Full-width responsive journal cards
- ✅ Color-coded sections (Entry/Exit/Tags)
- ✅ Journal view mode in Positions page

**Backend:**
- ✅ 3 new API endpoints (note, tags, getTags)
- ✅ PostgreSQL TEXT[] array for tags
- ✅ GIN indexes for fast tag queries
- ✅ Tag validation (lowercase, hyphens only)
- ✅ Character limit validation (500 chars)

**Frontend:**
- ✅ Entry note text area in position form
- ✅ Exit note text area in exit modal
- ✅ Tag input with autocomplete
- ✅ Tag filter dropdown (multi-select)
- ✅ Expandable trade rows
- ✅ Journal view component
- ✅ Beautiful visual design

**Database:**
- ✅ positions.entry_note (TEXT)
- ✅ positions.exit_note (TEXT)
- ✅ positions.tags (TEXT[])
- ✅ trade_history.entry_note (TEXT)
- ✅ trade_history.exit_note (TEXT)
- ✅ trade_history.tags (TEXT[])
- ✅ GIN indexes on tags fields

---

## 📈 Feature Progression

### v1.0 (Initial MVP)
- ✅ Portfolio management
- ✅ Position tracking
- ✅ Grace period (10 days)
- ✅ ATR-based stops
- ✅ Fractional shares

### v1.1 (Cash Management)
- ✅ Deposit/withdrawal tracking
- ✅ Accurate P&L calculation
- ✅ Portfolio history snapshots
- ✅ Multi-currency support

### v1.2 (Exit Flexibility)
- ✅ Partial exits
- ✅ Custom exit dates
- ✅ User-provided exit prices
- ✅ User-provided FX rates

### v1.3 (System Health)
- ✅ Health check endpoints
- ✅ Detailed system status
- ✅ Automated endpoint testing
- ✅ Status dashboard page

### v1.4 (Trade Journal) ⭐ CURRENT
- ✅ Entry and exit notes
- ✅ Tag system with validation
- ✅ Tag filtering
- ✅ Expandable journal rows
- ✅ Journal view mode
- ✅ Complete documentation

---

## 🔮 Next Steps

### Recommended v1.5 Features
1. **Performance Analytics** - Win rate by tag, monthly returns
2. **Alerts & Notifications** - Email/SMS for stop hits
3. **Export & Reporting** - CSV/PDF export for taxes

### Infrastructure Improvements
- Consider caching for live prices (optional)
- Add full-text search in notes (future)
- Implement note edit history (future)
- Add tag analytics dashboard (future)

---

**Report Generated:** February 14, 2026
**Generated By:** System Health Check v1.4
**Next Review:** Weekly or after major deployments

**Document maintained by:** Development Team
**Status:** Current and Complete ✅

---

## Sprint: 2026-03-15__release-v1.10
**Date:** 2026-03-16
**Status:** Verified_with_deviations — Director of Quality sign-off 2026-03-16; Product Owner acceptance 2026-03-16

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Staging environment — Render Blueprint (Web Service + Static Site) + Supabase staging project; frontend at https://trading-assistant-staging.onrender.com, API at https://trading-assistant-api-staging.onrender.com; CI/CD auto-deploy from main via Render Blueprint; OPERATIONAL_GUIDE.md v3.19 — staging URL as canonical pre-merge QA environment (§8.2 + §8.5) | stage4_backlog_slice.md#ST-01, #ST-02, #ST-03; claude/system/OPERATIONAL_GUIDE.md §8.2, §8.5 | None |
| EPIC-02 | CohortAnalysis architecture correction — CohortAnalysis.js refactored from client-side buildCohorts() to useQuery + api.analytics.cohort(period); PerformanceAnalytics.js call-site updated; DEV-EPIC02-ST03-01 (P2, v1.9 Sprint 2) closed | docs/specs/frontend/pages/analytics.md §15; docs/specs/api_contracts/analytics_endpoints.md#GET /analytics/cohort | None (prior P2 resolved) |
| EPIC-03 | QA infrastructure — tests/test_portfolio_integration.py (15 FastAPI TestClient tests for GET /portfolio: shape, GBP conversion, heat, grace period); .github/workflows/integration-tests.yml (CI gate blocks merge on test failure); docs/testing/v1.7-qa-scenario-gaps.md (4 QA scenarios GAP-01 through GAP-04 closing TEST-GAP-EPIC-06 / BLG-QA-01) | docs/specs/api_contracts/portfolio_endpoints.md; docs/testing/v1.7-qa-scenario-gaps.md | DEV-ST05-01 (P3 — GET /portfolio/prospective-heat tests skipped; endpoint not in spec) |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| — | All 7 stories delivered | N/A |

### Known findings from this sprint

| Finding | Priority | Backlog item |
|---------|----------|-------------|
| GET /portfolio missing `initial_value`, `net_deposits`, `current_drawdown_percent`, `peak_portfolio_value` — spec since v1.8.2 but absent from API response | P1 | BLG-BE-01 (v1.11) |
| GAP-04 (holding_days on GET /trades) could not be verified on staging — no closed trades in staging environment | Informational | Scenario retained in docs/testing/v1.7-qa-scenario-gaps.md |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md
- Deviations filed: DEV-ST05-01 (P3, qa_evidence_EPIC-03.md — prospective-heat endpoint absent from spec; BLG-BE-02 filed); DEV-EPIC02-ST03-01 (P2, analytics.md v1.4) — resolved this sprint by ST-04
- Test scenarios referenced: docs/testing/v1.7-qa-scenario-gaps.md (4 new scenarios)

---

## Sprint: 2026-03-06__release-v1.9 (Sprint 1 of 2)
**Date:** 2026-03-09
**Status:** Verified — 2026-03-09

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-04 | Risk Dashboard defect resolution — US currency conversion (entry_price, current_stop → GBP); all 5 components render independent error states; PositionRiskTable ascending sort + Stop Price column; GracePeriodPanel Days in Grace column; ProspectiveHeatPanel threshold label; HeatGauge GBP at risk text; GRACE badge blue | risk_dashboard.md §3.2, §3.4, §4.1, §4.3, §5.2, §5.5, §6.2–6.5, §7.5–7.6; portfolio_endpoints.md | None (11 prior DEV-ST03-xx resolved) |
| EPIC-05 | Canonical test scenario library — 17 Playwright acceptance tests with mock layer, no live backend required; CI gate (playwright.yml); Service layer test coverage standard — 18 unit tests (grace_service 100%, drawdown_service 100%), 80% threshold CI gate (service-coverage.yml); backend_engineering_patterns_owner.md §11 | docs/testing/risk_dashboard_scenarios.md v1.1; backend_engineering_patterns_owner.md v1.1 | None |
| EPIC-06 | Documentation hygiene — Canonical Terms Glossary (glossary.md v1.1); AI-Assisted Workflow Governance Policy (ai_workflow_policy.md); GET /market/status documented (market_endpoints.md v0.1); settings_model.md v0.1; Error Response Standard (conventions.md §13); 7 BLG spec debt items resolved | docs/reference/glossary.md; docs/governance/ai_workflow_policy.md; docs/specs/api_contracts/market_endpoints.md; docs/specs/data_model/settings_model.md; docs/specs/api_contracts/conventions.md §13 | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-01, ST-02, ST-03, ST-04, ST-05, ST-12 | Deferred to Sprint 2 (Product Owner decision — phased approach) | sprint_backlog.md §Sprint 2 deferred items |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-04.md, qa_evidence_EPIC-05.md, qa_evidence_EPIC-06.md
- Deviations filed: None new — 11 prior deviations resolved (DEV-ST03-01 through DEV-ST03-12 minus DEV-ST03-08 resolved at ST-06)
- Test scenarios referenced: docs/testing/risk_dashboard_scenarios.md v1.1 (EPIC-04 and EPIC-05; 17/27 automated via Playwright mock layer)

---

## Sprint: 2026-03-04__release-v1.8
**Date:** 2026-03-06
**Status:** Verified_with_deviations — Director of Quality sign-off 2026-03-06; Product Owner acceptance 2026-03-06

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Risk Dashboard page — portfolio heat gauge, drawdown summary, grace period panel, per-position risk table, prospective heat panel | docs/specs/frontend/pages/risk_dashboard.md; docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio; docs/specs/metrics_definitions.md#Portfolio Heat | DEV-ST03-01 through DEV-ST03-12 (all accepted P2/P3; see risk_dashboard.md §11) |
| EPIC-02 | CI Quality Gates — golden output regression (5 PS + 7 SL vectors), backtest vs live stop reconciliation, pip-audit CVE scanning, OpenAPI drift detection | claude/strategy/strategy_rules.md; docs/reference/openapi.yaml | None |
| EPIC-03 | Settings spec correction (PATCH/POST replaces PUT); openapi.yaml updated to v1.9.0 | docs/specs/api_contracts/settings_endpoints.md; docs/reference/openapi.yaml | None |
| EPIC-04 | Unavailability failure mode policy; running API changelog | docs/ops/unavailability_policy.md; docs/specs/api_contracts/api_changelog.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| (none) | All 12 ST items completed within sprint | N/A |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md
- Deviations filed: DEV-ST03-01 through DEV-ST03-12 (docs/specs/frontend/pages/risk_dashboard.md §11)
- Test scenarios referenced: docs/testing/risk_dashboard_scenarios.md (EPIC-01; 10/27 executable in v1.8 environment)

---

## Sprint: 2026-03-02__release-v1.7
**Date:** 2026-03-02
**Status:** Verified — Director of Quality sign-off 2026-03-03; Product Owner acceptance 2026-03-03

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | CI/CD merge gate — validate-analytics.yml workflow triggers on PR/push; blocks merge on critical_failed > 0; calls POST /validate/calculations | docs/specs/api_contracts/analytics_endpoints.md#POST /validate/calculations | None |
| EPIC-02 | §13 Strategy Boundary Review complete — Signal Params COMPLIANT, AI Journal CONDITIONALLY COMPLIANT, New Indicators COMPLIANT if canonical; §13-gated features cleared to proceed | docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md; claude/strategy/strategy_rules.md | None |
| EPIC-03 | Canonical Portfolio Heat metrics defined — Position Risk (GBP-adjusted), Portfolio Heat formula, explicit display thresholds added to metrics_definitions.md v1.6.0 | docs/specs/metrics_definitions.md#Portfolio Risk Metrics | None |
| EPIC-04 | Structured Logging Standards — Class 1 Canonical Specification created covering log levels, JSON format, correlation IDs, async observability | docs/specs/structured_logging_standards.md | None |
| EPIC-05 | API Versioning Decision Record — URL path versioning deferred to first breaking change, 60-day deprecation, webhooks versioned from inception, existing endpoints grandfather-exempted | docs/product/decisions/api-versioning-v1.7.md | None |
| EPIC-06 | Spec Debt Resolution — analytics_endpoints.md v1.9.0 (14 validated metrics incl. sharpe_ratio_trade_method); portfolio_endpoints.md v1.9.0 (corrected to match live API); trade_endpoints.md v1.9.0 (holding_days added); trade_service.py updated | docs/specs/api_contracts/analytics_endpoints.md; docs/specs/api_contracts/portfolio_endpoints.md; docs/specs/api_contracts/trade_endpoints.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| (none) | All 30 tasks completed within sprint | N/A |

### Hard Gates Cleared

| Gate | Cleared By |
|------|-----------|
| v1.8 pre-alignment | EPIC-03 — metrics_definitions.md v1.6.0 |
| v2.0 pre-alignment (logging) | EPIC-04 — structured_logging_standards.md Class 1 |
| v2.0 pre-alignment (API versioning) | EPIC-05 — api-versioning-v1.7.md |
| §13-gated features | EPIC-02 — SRB decision record |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md, qa_evidence_EPIC-05.md, qa_evidence_EPIC-06.md
- Deviations filed: None
- Test scenarios referenced: docs/testing/QWB-quick-wins-bundle-test-scenarios.md (EPIC-06)

---

## Sprint: 2026-03-06__release-v1.9 Sprint 2
**Date:** 2026-03-13
**Status:** Verified_with_deviations — Director of Quality sign-off 2026-03-13; Product Owner acceptance 2026-03-13

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Compliance Metrics: journal_completion_rate, stop_exit_rate, avg_position_size_pct — backend endpoint GET /analytics/compliance-metrics + DisciplineComplianceSection.js §17 analytics panel | docs/specs/metrics_definitions.md#Discipline & Compliance Metrics; docs/specs/frontend/pages/analytics.md#§17 | None |
| EPIC-01 | Trade Reflection: POST-trade structured reflection modal (5 prompts, 500-char limit), GET/POST /trades/{id}/reflection, TradeReflection.js browsing page | docs/specs/frontend/pages/trade_reflection.md; docs/specs/api_contracts/trade_endpoints.md#reflection; docs/specs/data_model.md#v1.8 | None |
| EPIC-02 | Cohort Analysis: GET /analytics/cohort?period={month\|quarter\|year}, CohortAnalysis.js §15 with period toggle and table | docs/specs/metrics_definitions.md#Cohort Metrics; docs/specs/frontend/pages/analytics.md#§15 | DEV-EPIC02-ST03-01 (P2 — client-side cohort computation; v1.10 fix: BLG-TECH-06) |
| EPIC-02 | R-Multiple Distribution: GET /analytics/r-multiple-distribution, 7-bucket chart + 4 stat cards, hard rule: no client-side R computation | docs/specs/metrics_definitions.md#R-Multiple (Canonical Server-Side); docs/specs/frontend/pages/analytics.md#§16 | None |
| EPIC-03 | Dashboard Homepage: root `/` landing page with 5 independent data cards (Open Positions, Portfolio Heat, Grace Period, Market Signals, Recent Activity) | docs/specs/frontend/pages/dashboard.md v2.0 | DEV-EPIC03-ST05-01 (P3 — hidden full-page retry overlay; v1.10 enhancement) |
| EPIC-05 | Canonical Test Scenario Library Phase 2: 25 scenarios for v1.9 features (SC-CM-01–04, SC-TR-01–07, SC-CA-01–04, SC-RM-01–04, SC-DH-01–10) in risk_dashboard_scenarios.md v1.3 | docs/testing/risk_dashboard_scenarios.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| (none) | All 6 Sprint 2 items completed and merged | N/A |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-05-sprint2.md
- Deviations filed: DEV-EPIC02-ST03-01 (P2, analytics.md v1.4); DEV-EPIC03-ST05-01 (P3, dashboard.md)
- Test scenarios referenced: docs/testing/risk_dashboard_scenarios.md v1.3 (25 scenarios)

---

## Sprint: 2026-03-17__release-v2.0
**Date:** 2026-03-17
**Status:** Verified_with_deviations — Post-ship closure complete 2026-03-17

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-04 | P1 fix: GET /portfolio — 4 missing fields (initial_value, net_deposits, current_drawdown_percent, peak_portfolio_value); empty-positions early-return path fixed | docs/specs/api_contracts/portfolio_endpoints.md v2.0.0; docs/testing/v1.7-qa-scenario-gaps.md GAP-03 | None |
| EPIC-04 | GET /portfolio/prospective-heat — stretch: prospective risk preview for entry sizing (ticker, shares, entry_price, stop_price → heat_pct, position_risk_gbp, within_limit) | docs/specs/api_contracts/portfolio_endpoints.md v2.0.0 §GET /portfolio/prospective-heat | None |
| EPIC-01 | Signals page spec + top_n / lookback_days controls with 500ms debounce re-fetch | docs/specs/frontend/pages/signals.md v0.1; docs/specs/api_contracts/signal_endpoints.md | None |
| EPIC-02 | GET /reports/tax-year endpoint — UK tax-year (6 Apr–5 Apr) P&L summary: 29 integration tests pass | docs/specs/api_contracts/reports_endpoints.md v0.1; docs/specs/data_model.md §3 | None |
| EPIC-02 | Tax Year P&L Report frontend view — Reports page tab, year selector, summary cards (Total P&L, Realised Trades, Win Rate, Best/Worst Trade) | docs/specs/frontend/pages/reports.md v0.1 | P1 hotfix bb66b69: base44.baseUrl undefined on production — fixed post-merge |
| EPIC-05 | Production Deployment Runbook, Positions Table Data Dictionary, Database Migration Governance Standard, Spec Coverage Inventory — operational and governance documentation | docs/ops/production_deployment_runbook.md; docs/specs/data_model_positions_dictionary.md; docs/ops/database_migration_governance.md; docs/specs/spec_coverage_inventory.md | None |
| EPIC-05 | CohortAnalysis backend integration regression scenarios (stretch) — 3 backend scenarios (SC-CA-BACKEND-01–03) | docs/testing/analytics_scenarios.md v1.0 | P3 cross-branch: committed on EPIC-04 branch |
| EPIC-06 | Roadmap stage document consolidation — roadmap_prompt.md v4.0 (cycle_record.md pattern all tiers) | claude/system/roadmap_prompt.md v4.0; OPERATIONAL_GUIDE.md v3.24 | None |
| EPIC-06 | Ideas register migration — idea_intake_prompt.md v2.0, ideas_register.md (44 ideas migrated from per-file model) | claude/system/idea_intake_prompt.md v2.0; claude/ideas/ideas_register.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-06 through ST-10 (EPIC-03 — notification delivery) | No async notification infrastructure; BLG-TECH-08 prerequisite required before v2.1 sprint planning | BLG-TECH-08 (v2.1 prerequisite) |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-04.md, qa_evidence_EPIC-05.md, qa_evidence_EPIC-06.md (all DoQ sign-off 2026-03-17)
- Deviations filed: ST-20 cross-branch commit P3 (content correct); base44.baseUrl P1 production defect (fixed bb66b69 2026-03-17)
- Post-merge hotfix: bb66b69 — base44.baseUrl undefined on production (src/api/base44Client.js)
- Test scenarios referenced: docs/testing/analytics_scenarios.md v1.0 (3 scenarios, ST-20); test_reports_integration.py (29 tests, ST-04)

---

## Sprint: 2026-04-17__release-v2.8
**Date:** 2026-04-20
**Status:** Verified — 2026-04-20

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Market Correlation View — MarketCorrelationSection.js on Analytics page; severity-coloured table (high=Rose-500, moderate=Amber-500, low=Emerald-500, null=Slate-500); sort descending; nulls to bottom | docs/specs/api_contracts/analytics_endpoints.md v2.1.0; docs/specs/frontend/pages/analytics.md v1.7; docs/design/2026-04-17__release-v2.8/market-correlation/ux_spec.md | None |
| EPIC-02 | Market Correlation Endpoint Scenarios — 4 new test scenarios (SC-CORR-01–04) in analytics_scenarios.md | docs/specs/api_contracts/analytics_endpoints.md v2.1.0 | None |
| EPIC-02 | Supplementary Indicator Field Scenarios — 2 new test scenarios (SC-SIG-IND-01–02) in signals_scenarios.md | docs/specs/api_contracts/signal_endpoints.md v1.1 | None |
| EPIC-03 | DoQ Date Field Reminder Patch — execution_prompt.md §3.2.A updated; Date: field non-blank requirement enforced at sign-off | claude/system/execution_prompt.md v3.7 | None |
| EPIC-03 | Sprint Close Terminology Clarification — sprint_close template terminology aligned | claude/system/execution_prompt.md §5.3 | None |
| EPIC-03 | Backlog Archive Deduplication — 531 lines → clean archive; duplicate IDs removed (most recent retained) | claude/backlog/backlog_archive.md | None |
| EPIC-04 | AI Journal Summary Backend — POST /ai/journal-summary; Anthropic API (claude-haiku-4-5-20251001); display-only; SRB-v1.7 compliant | docs/specs/api_contracts/ai_endpoints.md v1.0; docs/reference/openapi.yaml v2.7.0 | None |
| EPIC-04 | AI Journal Summary Frontend — AI summary section in TradeHistory.js; collapsed by default; non-dismissible disclaimer; Strategy Rules owner sign-off 2026-04-18 | docs/specs/frontend/pages/trade_history.md v1.7; docs/design/2026-04-17__release-v2.8/ai-journal-summary/ux_spec.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| (none) | All 8 sprint items completed and merged | N/A |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md
- Deviations filed: None
- Test scenarios referenced: docs/testing/analytics_scenarios.md (SC-CORR-01–04); docs/testing/signals_scenarios.md (SC-SIG-IND-01–02); tests/e2e/market-correlation.spec.js (SC-CORR-FE-01–08 Playwright, 8/8 green CI run 24656513015)

---

## Sprint: 2026-04-25__release-v3.0
**Date:** 2026-04-27
**Status:** Verified — 2026-04-27

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Ticker Universe Data Model + Endpoints — ticker_universe table, seed data (200 US + 50 UK tickers), GET /ticker-universe, GET /ticker-universe/{ticker}, POST /ticker-universe | docs/specs/api_contracts/ticker_universe_api_contract.md | None |
| EPIC-01 | OHLCV Data Pipeline Service — Alpaca (US) + Yahoo Finance (UK, GBp→GBP conversion) price fetching, OHLCV storage | docs/specs/api_contracts/alpaca_integration_contract.md, docs/specs/screener_results_schema.md | None |
| EPIC-01 | ATR + Regime Detection + Signal Scoring Engine — Wilder 14-period ATR, RSI+MACD+volume signal score (0–1), regime gate | docs/specs/screener_results_schema.md | None |
| EPIC-01 | Screener Batch Engine + API Endpoints — POST /screener/run, GET /screener/results, screener_results table, concurrency guard | docs/specs/api_contracts/screener_api_contract.md | None |
| EPIC-02 | Screener Results Page — sort/filter/regime badges/freshness/skeleton/error; market + regime + sector filters; Screener nav item | docs/specs/frontend/pages/screener_results.md | DEV-01 resolved (news panel now live) |
| EPIC-02 | Watchlist Promotion Flow — inline WatchlistPopover, POST /watchlist, 409 already-in-watchlist handling | docs/specs/frontend/pages/screener_results.md#watchlist-promotion | None |
| EPIC-02 | Screener News Panel — news count badge, GET /news/{ticker}, inline expandable panel (display-only, BLG-FE-18) | docs/specs/frontend/pages/screener_results.md#news-panel | None |
| EPIC-02 | Keyboard Shortcuts — n (new position), w (add to watchlist), r (refresh); per-page sidebar kbd hints | docs/specs/frontend/pages/screener_results.md#keyboard-shortcuts | Cross-EPIC: ST-11 committed on EPIC-02 branch |
| EPIC-03 | External API Health Extension — GET /health external_apis section (alpaca, yahoo_finance); cache-based, non-blocking | docs/specs/api_contracts/health_endpoints.md | None |
| EPIC-03 | AI Journal Monitoring Metrics — GET /health ai_journal section (usage_rate, error_rate, p95_latency_ms) from ai_audit_log | docs/specs/api_contracts/health_endpoints.md | None |
| EPIC-03 | AI Audit Service Unit Tests — 12 unit tests for ensure_ai_audit_table, log_ai_summary_run, query_audit_log | (test quality story) | None |
| EPIC-04 | execution_prompt.md §2 + §3.1.A Deferred Patches — pre-seal gate + advisory instruction fixes | claude/system/execution_prompt.md | None |
| EPIC-04 | Consecutive Losing Streak Metric — 7 unit tests; metrics_definitions.md updated v1.9→v1.10 | docs/specs/metrics_definitions.md | None |
| EPIC-04 | AI Journal Model Version Contract — Class 2 canonical spec; claude-haiku-4-5-20251001 pinned | docs/specs/ai_journal_model_contract.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| (none) | All 16 sprint items completed and merged | N/A |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md
- Deviations filed: DEV-01 (screener_results.md) resolved this sprint by ST-07; no new spec deviations
- Test scenarios referenced: tests/test_ticker_universe.py, tests/test_screener_data_service.py, tests/test_screener_engine.py, tests/test_screener_batch_service.py, tests/test_streak_metric.py, tests/test_health_extensions.py, tests/test_ai_audit_service.py; E2E: tests/e2e/screener.spec.js (SC-SCR-01–18), tests/e2e/keyboard-shortcuts.spec.js, tests/e2e/visual-snapshots.spec.js (VS-01–12), tests/e2e/positions-pnl-columns.spec.js (V-PATH2-01–04)

---

## Sprint: 2026-05-14__release-v3.4
**Date:** 2026-05-14
**Status:** Verified_with_deviations — 2026-05-14

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-04 | Research view component library — catalogue of PT-02 research view UI components with EPIC-01 reuse candidates noted | docs/frontend/component_library_research_view.md | None |
| EPIC-04 | Screener morning routine UX spec — step-by-step pre-market workflow for screener use | docs/specs/frontend/pages/screener_morning_routine.md | None |
| EPIC-04 | trade_plan.md §6.2 spec update — CHK-03/CHK-04 field names corrected; AI journal review cadence doc created | docs/specs/frontend/pages/trade_plan.md#§6.2; docs/specs/compliance/ai_journal_review_cadence.md | None |
| EPIC-04 | Screener accuracy test protocol — formal accuracy test process doc (Owner: Director of Quality) | docs/testing/screener_accuracy_protocol.md | None |
| EPIC-03 | Research page UK suffix strip + negative earnings days (BLG-FE-23/24) — .L stripped from display; "Today" label + negative days shown | (frontend only) | None |
| EPIC-03 | Signals page default to most recent day (BLG-FE-25) — auto-selects latest signal date on load | (frontend only) | None |
| EPIC-03 | Watchlist research status indicator (BLG-FE-29) — badge shows research freshness per watchlist row | (frontend only) | None |
| EPIC-03 | Trade plan status badges + abandonment UI (BLG-FE-30/BLG-FEAT-21) — active/draft/abandoned badges; abandon action in plan view | docs/specs/frontend/pages/trade_plan.md#9 | DEV-01 (RQ v5 onSuccess removed) |
| EPIC-01 | Position lifecycle state badge (IT-01) — LifecycleBadge in Positions table; GRACE/LOSING/PROFITABLE/EXIT ZONE states | docs/design/2026-05-09__release-v3.3/position-lifecycle-display/ux_spec.md | None |
| EPIC-01 | Grace Period Decision Support (IT-02) — GracePeriodAlertZone on Positions page; sessionStorage dismiss; §13 display-only | docs/design/2026-05-09__release-v3.3/grace-period-alert/ux_spec.md | DEV-01 (sessionStorage) |
| EPIC-01 | Stop Management Workflow (IT-03) — TrailStopModal with stop-trail data; PATCH /positions/{id} update | docs/design/2026-05-09__release-v3.3/stop-management-workflow/ux_spec.md | DEV-02 (PATCH) |
| EPIC-02 | Drawdown-Triggered Review Prompt backend (IT-04) — GET /portfolio/drawdown-status; 30-day peak; regime label; lifecycle state counts | docs/reference/openapi.yaml#/portfolio/drawdown-status; docs/specs/api_contracts/portfolio_endpoints.md | None |
| EPIC-02 | Drawdown-Triggered Review Prompt frontend (IT-04) — DrawdownReviewPrompt card on Positions page; amber warning; in-memory dismiss | docs/design/2026-05-14__release-v3.4/drawdown-review-prompt/ux_spec.md | DEV-01 (useState dismiss) |
| EPIC-02 | Position Concentration Limits backend + frontend (IT-05) — GET /portfolio/concentration-status; ConcentrationLimitsWarning with position/sector breach detail | docs/design/2026-05-14__release-v3.4/concentration-limits-warning/ux_spec.md; docs/specs/api_contracts/portfolio_endpoints.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| (none) | All 14 sprint items completed and merged | N/A |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-04.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md (all DoQ sign-off 2026-05-14)
- Deviations filed: DEV-01/DEV-02 in EPIC-01 (sessionStorage, PATCH stop update); DEV-01 in EPIC-03 (RQ v5); DEV-01 in EPIC-02 (useState dismiss) — all P3
- Test scenarios referenced: tests/e2e/epic01-v34-lifecycle.spec.js (10 scenarios); tests/e2e/epic02-v34-risk-prompts.spec.js (10 scenarios); tests/e2e/epic03-v34-frontend.spec.js (16 scenarios)

---

## Sprint: 2026-05-22__release-v4.0
**Date:** 2026-05-25
**Status:** Verified — post-ship closure complete 2026-05-25

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Arc 5 compliance analytics endpoint — GET /analytics/arc5-compliance returning validation_pass_rate_by_rule, events_per_week, override_rate, top_rule_breach, trade_plan_adherence_rate; pre_entry_validation_log table | docs/specs/api_contracts/analytics_endpoints.md v2.2.0; docs/specs/metrics_definitions.md#Arc 5 Compliance Metrics | None |
| EPIC-01 | Arc5ComplianceSection.js — "Red Flag Events/Week", "Override Rate", "Trade Plan Adherence", "Top Rule Breach" stat cards on PerformanceAnalytics page (§19) | docs/design/2026-05-22__release-v4.0/arc5-analytics-metrics/ux_spec.md | Staging-only: observable rendering deferred → BLG-QA-28 |
| EPIC-01 | SI-01→SI-03 Playwright integration test — tests/e2e/si01-si03-integration.spec.js (8 scenarios: SC-SI-01a/b/c, SC-SI-03a/b/c, SC-SI-PATH-01/02) | docs/specs/api_contracts/portfolio_endpoints.md#GET /portfolio/pre-entry-validation; docs/specs/api_contracts/red_flag_journal.md | None |
| EPIC-02 | Ticker symbol validation at POST /ticker-universe — live Yahoo Finance lookup gate; HTTP 422 on invalid/unknown symbol; SKIP_TICKER_VALIDATION bypass for CI | docs/specs/api_contracts/ticker_universe_api_contract.md v1.2 | Staging-only: live rejection path deferred → BLG-QA-30 |
| EPIC-02 | Red flag journal security review — PASS (auth, PII, SQL injection, response leakage); review doc filed | docs/specs/api_contracts/red_flag_journal.md | None |
| EPIC-02 | Starlette CVE remediation — starlette==1.0.1 (from 0.49.1); remediates PYSEC-2026-161 auth bypass | backend/requirements.txt | None |
| EPIC-03 | Gemini Flash base wiring — POST /trade-plans/{plan_id}/generate-thesis; backend/services/gemini_service.py; "Improve with AI" button on TradePlan edit page | docs/specs/api_contracts/trade_plan_endpoints.md v0.3 | Staging-only: live API key + frontend staging deferred → BLG-QA-29 |
| EPIC-03 | Gemini audit trail — gemini_audit_log table; fire-and-forget write per thesis generation; 90-day retention | docs/specs/api_contracts/trade_plan_endpoints.md | None |
| EPIC-03 | Gemini cost tracking — prompt/completion/total tokens logged; estimated_cost_usd per call; 800k token/month alert threshold documented | docs/ops/gemini_cost_tracking.md | None |
| EPIC-03 | CI/CD staging auto-deploy — .github/workflows/staging-deploy.yml with path filter (src/**, backend/**, public/**, package.json, requirements.txt) | docs/ops/staging_deploy_notes.md | Staging-only: live Render deploy hook verification deferred → BLG-OPS-28 |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-10 — PT-04 Quality Score backend | Gate not met: <20 closed trades (PO confirmed 2026-05-23) | BLG-FEAT-25 |
| ST-11 — PT-04 Quality Score frontend | Gate not met: <20 closed trades (PO confirmed 2026-05-23) | BLG-FEAT-25 |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ 2026-05-24), qa_evidence_EPIC-02.md (DoQ 2026-05-24), qa_evidence_EPIC-03.md (DoQ 2026-05-25)
- Deviations filed: None (spec deviations); 4 staging-only ACs deferred to backlog (BLG-QA-28/29/30, BLG-OPS-28)
- Test scenarios referenced: docs/testing/analytics_scenarios.md; tests/e2e/si01-si03-integration.spec.js (8 scenarios)

---

## Sprint: 2026-05-26__release-v4.1
**Date:** 2026-05-27
**Status:** Verified — 2026-05-27

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | execution_prompt.md v3.28: HARD GATE added after every EPIC merge (OA-01 resolved — 2nd-recurrence escalation) | claude/system/execution_prompt.md | None |
| EPIC-01 | sprint_planning_prompt.md v3.7 + shared_standards.md v3.4: staging-only AC designation mandatory at planning (OA-02 resolved — 2nd-recurrence escalation) | claude/system/sprint_planning_prompt.md, claude/system/shared_standards.md | None |
| EPIC-01 | delivery_verification_prompt.md v2.6: STEP -1.3A PR Number Recovery — recovers pr_number from gh CLI when null/0 (OA-04 resolved) | claude/system/delivery_verification_prompt.md | None |
| EPIC-02 | API contracts verified: GET /portfolio/red-flag-journal (BLG-SPEC-33), GET /portfolio/pre-entry-validation (BLG-SPEC-34), GET /analytics/arc5-compliance (BLG-SPEC-40) — all pre-met in main, verified by code review | docs/specs/api_contracts/red_flag_journal.md, pre_entry_validation.md, arc5_compliance_analytics.md; docs/reference/openapi.yaml | None |
| EPIC-03 | POST /trade-plans/{plan_id}/generate-thesis API contract verified (BLG-SPEC-38 — Claude Haiku 4.5); openapi.yaml confirmed at lines 3751 + 3815 | docs/specs/api_contracts/gemini_thesis_generation.md v2.0.0; docs/reference/openapi.yaml | None |
| EPIC-03 | Arc 5 Compliance Composite Score formula: metrics_definitions.md v1.11.0 (4-term weighted formula, severity mapping); reports.md v0.3 (Arc 5 Compliance Summary section, collapsible, data from GET /analytics/arc5-compliance) | docs/specs/metrics_definitions.md, docs/specs/frontend/pages/reports.md | None |
| EPIC-03 | POST /ai/check-daily-cost — Claude API daily cost threshold alert via Telegram; AI_DAILY_COST_THRESHOLD configurable env var (default $1.00/day); 5 unit tests; endpoint total 58 | docs/specs/api_contracts/ai_endpoints.md v1.1; docs/reference/openapi.yaml | AC-05 staging deferred → BLG-QA-35 |
| EPIC-03 | Research view: Setup Type field (signal_type) in signal panel; 4 Playwright tests (SC-ST-01 through SC-ST-04); arc5_compliance_section.md spec created | docs/specs/frontend/pages/research_view.md v1.2; docs/specs/frontend/components/arc5_compliance_section.md | None |
| EPIC-04 | SI-02 data model gap analysis: 5 gaps enumerated (type, source, migration complexity); gap analysis at docs/specs/si02_gap_analysis.md | docs/specs/data_model.md; docs/specs/si02_gap_analysis.md | None |
| EPIC-04 | SI-02 pre-planning: §13 criteria doc, data prerequisite audit, query performance assessment; gate NOT met (< 20 closed trades) — sprint planning for SI-02 still pending gate | docs/specs/si02/section13_criteria.md, data_prerequisite_audit.md, query_performance_assessment.md | None |
| EPIC-04 | Security: ANTHROPIC_API_KEY scope review; credential inventory v1.1; GEMINI_API_KEY disposition recorded; delivery_verification_prompt.md v2.7 STEP 9.0 artefact presence check | docs/security/anthropic_api_key_scope_review.md; docs/ops/external_api_credential_inventory.md | None |
| EPIC-04 | Operational reviews: api_performance_baseline.md v1.5 (arc5-compliance + thesis endpoints); gemini_cost_tracking.md v1.2 (first Claude usage review); pnl_attribution_gate_check.md v1.0 | docs/ops/api_performance_baseline.md, gemini_cost_tracking.md, pnl_attribution_gate_check.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-11 ACs 02–04 — staging verification for Arc5ComplianceSection, AI thesis, ticker validation, deploy hook | Staging-only ACs; PO discretionary deferral authority (sprint_backlog.md) | BLG-QA-28, BLG-QA-29, BLG-QA-30, BLG-OPS-28 |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ autonomous class), qa_evidence_EPIC-02.md (DoQ autonomous class), qa_evidence_EPIC-03.md (DoQ 2026-05-27), qa_evidence_EPIC-04.md (DoQ autonomous class)
- Deviations filed: None (spec deviations)
- Test scenarios referenced: tests/e2e/research-view-signal-type.spec.js (4 scenarios), tests/e2e/arc5-compliance-section.spec.js (4 scenarios), tests/test_daily_cost_alert.py (5 unit tests)

---

## Sprint: 2026-05-30__release-v4.6
**Date:** 2026-05-31
**Status:** Verified_with_deviations — 2026-05-31

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | DS-07 data migration: 5 new SI-02 columns added to trade_plans (signal_id, risk_percent_used, portfolio_value_at_entry, effective_settings_snapshot, pre_entry_validation_snapshot) | docs/specs/data_model/si02_data_schema.md | None |
| EPIC-01 | POST /trade-plans: captures 5 new SI-02 fields at plan creation (2 from backend, 3 from frontend) | docs/specs/data_model/si02_data_schema.md | None |
| EPIC-01 | SI-02 behavioural drift detection service: 4 metrics (entry_timing_drift, sizing_adherence, consecutive_loss_sizing, regime_context), 90-day window, §13 binding conditions enforced | docs/specs/metrics/si02_drift_score.md | P3: ST-01 AC-05 staging verification pending (BLG-OPS-44) |
| EPIC-01 | GET /analytics/behavioural-drift endpoint: full 4-metric response, openapi.yaml updated, API contract created; endpoint total 60; SC-SS-01b updated | docs/specs/api_contracts/behavioural_drift_contract.md; docs/reference/openapi.yaml | None |
| EPIC-01 | SI-02 unit test suite: 35 test cases covering all 4 metrics, threshold bands, §13 compliance, deviation_pct formula; conftest.py _DB_STUB_FUNCTIONS updated | docs/specs/metrics/si02_drift_score.md | None |
| EPIC-03 | red_flag_events.severity column: added to DB, backfill logic, create/filter endpoint updated; portfolio_endpoints.md + openapi.yaml updated | docs/specs/api_contracts/portfolio_endpoints.md; docs/reference/openapi.yaml | P3: ST-09 AC-01/02/03 staging verification pending (BLG-OPS-45) |
| EPIC-03 | Arc 5 hosting cost projection: current Render Starter tier adequate; no upgrade required at < 50 trades | docs/ops/arc5_hosting_cost_projection.md | None |
| EPIC-03 | Arc 5 nav cohesion review: current structure maintained (1-click depth, Trading/Analytics split correct); no structural changes | docs/specs/frontend/arc5_nav_cohesion_review_v4.6.md | None |
| EPIC-03 | Red Flag Journal design review scope: in-scope items documented; gate date 2026-06-21 | docs/specs/fe/rfj_design_review_scope.md | None |
| EPIC-04 | System_status_report.md v4.4 status corrected (OA-01) | docs/System_status_report.md | None |
| EPIC-04 | release_planning_prompt.md v2.33: STEP 1.4 Gate-Condition Proximity Scan + data density checkpoint (BLG-GOV-32/43) | claude/system/release_planning_prompt.md | None |
| EPIC-04 | BLG-GOV-33 closed trade count audit: Q1=6 closed trades, Q2=0 with linked trade_plans; SI-02 gate NOT MET; EPIC-02 deferred (6th deferral); BLG-FEAT-25 updated | — (audit result in QA evidence) | None |
| EPIC-04 | Arc 4 data density trajectory assessed: Option A (proceed); SI-02 gate ~Nov 2026; PT-04 full ~Jun 2027 | docs/product/decisions/arc4_data_density_trajectory_v4.6.md | None |
| EPIC-04 | Arc 6 Monte Carlo §13 pre-assessment: PASS; 10 binding conditions; Arc 6 planning unlocked | docs/product/decisions/arc6_ps03_section13_preassessment.md | None |
| EPIC-04 | Trade plan schema audit: 25 fields enumerated post-DS-07; 0 orphaned fields; 3 P3 process gaps noted | docs/specs/data_model/trade_plan_schema_audit_v4.6.md | None |
| EPIC-04 | Sprint close automation investigation: no failure; observer effect root cause (BLG-GOV-41 resolved) | docs/ops/sprint_close_reminder_investigation_v4.6.md | None |
| EPIC-04 | External API integration spec template: 7-section structure (BLG-SPEC-32) | docs/specs/api_contracts/_external_api_template.md | None |
| EPIC-04 | roadmap_prompt.md v6.7: STEP 12.1 next_release advisory after DL decision (OA-02) | claude/system/roadmap_prompt.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| EPIC-02: ST-06/07/08 — BehaviouralDriftPanel + integration + Playwright | Data density gate NOT MET (0 linked trade_plans vs ≥20); deferred at planning, confirmed at close | BLG-FEAT-25 (6th deferral) |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (DoQ autonomous class, 35 unit tests), qa_evidence_EPIC-03.md (Director of Quality 2026-05-30), qa_evidence_EPIC-04.md (DoQ autonomous class)
- Deviations filed: None
- Test scenarios referenced: tests/test_behavioural_drift_service.py (35 cases), tests/test_red_flag_journal.py

---

## Sprint: 2026-06-08__release-v5.2
**Date:** 2026-06-08
**Status:** Verified — 2026-06-08

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-03 | BLG-GOV-97: Claude API model deprecation compliance check — claude-haiku-4-5-20251001 confirmed current; next review 2026-09-08 | docs/governance/ai_model_deprecation_check_v52.md | None |
| EPIC-03 | BLG-GOV-98: Telegram bot token minimal-permission security review — send-only confirmed; BotFather manual check recommended | docs/security/security_register.md (Review 002) | None |
| EPIC-03 | BLG-GOV-99: SI-05 digest endpoint authentication review — auth gap found; BLG-BE-35 P2 filed for fix | docs/security/security_register.md (Review 003); docs/specs/api_contracts/digest_endpoints.md | None (gap filed as BLG-BE-35) |
| EPIC-03 | BLG-GOV-100: Backend endpoint coverage audit — 50 routes; 6 contract gaps; BLG-SPEC-49/50/51/52 filed | docs/ops/endpoint_coverage_audit_v52.md | None (gaps filed as BLG-SPEC backlog items) |
| EPIC-02 | BLG-BE-32: SI-05 Telegram delivery retry — max 2 retries, 30s/60s backoff; ERROR logging confirmed; 3 unit tests added (24 total) | backend/services/si05_digest_service.py | None |
| EPIC-02 | BLG-BE-33: SI-05 digest delivery log table (si05_digest_log) — CREATE TABLE IF NOT EXISTS; log writes on success and failure paths; staging DB confirmed | backend/database.py; backend/main.py; docs/specs/api_contracts/digest_endpoints.md | None |
| EPIC-02 | BLG-OPS-55: Deployment runbook updated v0.1→v0.2 — §6 covers SI-05 env vars, cron schedule, failure detection | docs/ops/production_deployment_runbook.md | None |
| EPIC-02 | BLG-OPS-56: SI-05 health check procedure v1.0 — 3 check options (log table, Render logs, Telegram); escalation path defined | docs/ops/si05_health_check_procedure.md | None |
| EPIC-04 | BLG-QA-46: SI-05 edge case gap analysis — 2 missing tests authored (Telegram API failure, message truncation); 26 tests total | tests/test_si05_digest_service.py; docs/qa/si05_edge_case_gap_analysis.md | None |
| EPIC-04 | BLG-QA-47 + BLG-GOV-94: SI-05 acceptance test protocol + delivery verification protocol — covers v5.1 deferred ACs | docs/qa/si05_acceptance_test_protocol.md; docs/qa/si05_delivery_verification_protocol.md | None |
| EPIC-04 | BLG-QA-48: Regression test suite baseline refresh — test.py and Playwright confirmed current; BLG-QA-50 filed for formal baseline doc | backend/routers/test.py; docs/qa/regression_baseline_refresh_v51.md | None |
| EPIC-04 | BLG-GOV-96: SI-05 effectiveness criteria — 3 criteria defined; 30-day review 2026-07-04 | claude/cycles/2026-06-08__release-v5.2/si05_effectiveness_criteria.md | None |
| EPIC-01 | OA-01 resolved: release_planning_prompt.md v2.33→v2.34 — §-1.2 Option(b) path added | claude/system/release_planning_prompt.md | None |
| EPIC-01 | OA-02 resolved: execution_prompt.md v3.36→v3.37 — §3.1.A step 2c test-authoring spec_references guidance added | claude/system/execution_prompt.md | None |
| EPIC-01 | BLG-SPEC-47 resolved: si05-telegram-message-format-spec.md v1.1→v1.2 — Option(a) pass_rate computation accepted; DEV-v51-EPIC01-01 closed | docs/product/decisions/si05-telegram-message-format-spec.md | None |
| EPIC-01 | BLG-SPEC-48 resolved: digest_endpoints.md v0.2→v0.3 — POST /digest/si05/send auth requirements section added | docs/specs/api_contracts/digest_endpoints.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-17 (BLG-FE-64) | Gate: SI-03 Red Flag Journal live ≥ 30 days — not clear at sprint planning seal (2026-06-08); gate clears 2026-06-21 | backlog.md (deferred at planning, never entered sprint) |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-03.md (autonomous class, 2026-06-08), qa_evidence_EPIC-02.md (Director of Quality, 2026-06-08), qa_evidence_EPIC-04.md (autonomous class, 2026-06-08), qa_evidence_EPIC-01.md (autonomous class, 2026-06-08)
- Deviations filed: None
- Test scenarios referenced: tests/test_si05_digest_service.py (26 unit tests)

---

## Sprint: 2026-06-08__release-v5.3
**Date:** 2026-06-09
**Status:** Verified — 2026-06-09

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-02 | BLG-BE-35: POST /digest/si05/send API key authentication — Depends injection pattern; 401 on missing/invalid key | docs/specs/api_contracts/digest_endpoints.md | None |
| EPIC-02 | BLG-OPS-57: SI-05 Telegram delivery failure alerting — ERROR-level log after retry exhaustion; deployment runbook updated | docs/operations/deployment_runbook.md | None |
| EPIC-02 | BLG-OPS-58: CI secret scanning gate — gitleaks workflow with allowlist for test fixtures; blocks PRs on leaked secrets | .github/workflows/secret-scanning.yml; .gitleaks.toml | None |
| EPIC-01 | BLG-SPEC-53: API contract gap resolution plan — 6 gaps scoped; resolution order documented | claude/cycles/2026-06-08__release-v5.3/api_contract_gap_resolution_plan.md | None |
| EPIC-01 | BLG-SPEC-54: openapi.yaml completeness audit — all 50 routes checked; 6 gaps confirmed and added | docs/reference/openapi.yaml | None |
| EPIC-01 | BLG-QA-51: QA acceptance criteria template for endpoint contracts — reusable template for future gap stories | docs/qa/endpoint_contract_qa_criteria_template.md | None |
| EPIC-01 | BLG-SPEC-49: GET /ai/journal-summary/history contract added to ai_endpoints.md + openapi.yaml | docs/specs/api_contracts/ai_endpoints.md | None |
| EPIC-01 | BLG-SPEC-50: GET /analytics/compliance-metrics contract added to analytics_endpoints.md + openapi.yaml | docs/specs/api_contracts/analytics_endpoints.md | None |
| EPIC-01 | BLG-SPEC-51: GET /news/{ticker} contract — new news_endpoints.md created + openapi.yaml | docs/specs/api_contracts/news_endpoints.md | None |
| EPIC-01 | BLG-SPEC-52: GET/POST/DELETE /watchlist contracts — watchlist_endpoints.md + openapi.yaml + test.py updated; SystemStatus.js + SC-SS-01b updated | docs/specs/api_contracts/watchlist_endpoints.md; docs/reference/openapi.yaml; backend/routers/test.py | None |
| EPIC-03 | LL-v5.2-P4-01: qa_evidence_template.md signer format note clarified — engine signer field format documented | claude/system/templates/qa_evidence_template.md v3.9→v4.0 | None |
| EPIC-03 | LL-v5.2-P4-02: execution_prompt.md STEP 5.3A SSR sub-step added — duplicate section prevention guard | claude/system/execution_prompt.md v3.37→v3.38 | None |
| EPIC-03 | BLG-GOV-107: SI-02 frontend activation criteria precision — 3 specific checkable gate conditions in current_roadmap.md | claude/roadmap/current_roadmap.md | None |
| EPIC-03 | BLG-GOV-108: AI model pin update policy — 30-day deprecation notice timeline; CI model-pin drift check | docs/governance/ai_model_version_pinning_policy.md | None |
| EPIC-03 | BLG-GOV-109: AI audit log retention policy — 12-month retention; cleanup mechanism defined; aligned with Supabase | docs/governance/ai_audit_log_retention_policy.md | None |
| EPIC-03 | BLG-GOV-110: Arc 4 trade_plan data completeness audit — per-field null% for 5 fields; gap assessment complete | docs/governance/arc4_trade_plan_data_completeness_audit.md | None |
| EPIC-03 | BLG-GOV-104: strategy_rules.md §11 parameter validation — 6 closed trades insufficient data; parameters unchanged; rationale documented | docs/governance/strategy_parameter_validation_v53.md | None |
| EPIC-03 | BLG-GOV-113: SI-05 effectiveness review protocol — participants, evidence sources, output format, decision authority by 2026-07-01 | docs/governance/si05_effectiveness_review_protocol.md | None |
| EPIC-03 | BLG-GOV-114: si05_digest_log schema validation — send_at, status, recipient, content_hash fields confirmed PASS | docs/governance/si05_digest_log_schema_validation.md | None |
| EPIC-04 | BLG-QA-52: Tax year P&L boundary edge case validation — UK Apr 6 boundary; straddle and edge scenarios covered | tests/test_tax_year_pnl_boundary.py | None |
| EPIC-04 | BLG-QA-53: SI-05 digest Playwright E2E coverage — 3 scenarios (happy path, empty red flag, compliance score); Telegram mocked | tests/e2e/si05-digest-delivery.spec.js | None |
| EPIC-04 | BLG-QA-54: Playwright coverage matrix updated post-v5.2 — all new v5.3 scenarios counted | docs/qa/playwright_coverage_matrix.md | None |
| EPIC-04 | BLG-FE-66: Red Flag Journal post-launch UX review — friction points documented; BLG-FE-68+ filed where needed | docs/governance/rfj_ux_review_v53.md | None |
| EPIC-04 | BLG-FE-67: BLG-FE-64 visual design review scope definition — distinct from BLG-FE-66; gate date 2026-06-21 | docs/governance/blg_fe_64_scope_definition.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-25 — BLG-FE-64 (conditional) | Gate date 2026-06-21 not reached at planning time; add via amendment cycle if gate clears | backlog.md |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-02.md (autonomous class, 2026-06-09), qa_evidence_EPIC-01.md (autonomous class, 2026-06-09), qa_evidence_EPIC-03.md (autonomous class, 2026-06-09), qa_evidence_EPIC-04.md (autonomous class, 2026-06-09)
- Deviations filed: None
- Test scenarios referenced: tests/test_tax_year_pnl_boundary.py, tests/e2e/si05-digest-delivery.spec.js, tests/test_api_contracts.py (EPIC-01/02)

## Sprint: 2026-06-09__release-v5.4
**Date:** 2026-06-10
**Status:** Verified — 2026-06-10

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | v5.3 endpoint performance baselines — 5 new endpoints added to api_performance_baseline.md with live measurements | docs/ops/api_performance_baseline.md#17. v5.3 New Endpoints | None |
| EPIC-02 | Pre-entry panel UX spec — warn/fail override acknowledgement flows separated; fail requires deliberate modal confirmation | docs/product/ux/pre_entry_override_ux_spec.md | None |
| EPIC-03 | SI-05 Phase 2 activation criteria — formal document defining hard gate, quality gate, and Phase 1 effectiveness gate for Phase 2 go/no-go | docs/governance/si05_phase2_activation_criteria.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-03 — RFJ visual design review pre-brief | Date gate not met (SI-03 live ≥30 days; 2026-06-21); PO-authorised sprint close | BLG-FE-64 (backlog.md) |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (autonomous class, 2026-06-10), qa_evidence_EPIC-02.md (autonomous class, 2026-06-10), qa_evidence_EPIC-03.md (autonomous class, 2026-06-10)
- Deviations filed: None
- Test scenarios referenced: None (all stories produced specification/governance documents; no executable test scenarios)

## Sprint: 2026-06-16__release-v5.6
**Date:** 2026-06-16
**Status:** Sprint_Complete — pending verification

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-03 | PT-04 trade count gate re-verification (13/20 trades; gate NOT MET; trajectory updated) + Arc 5 QA completion criteria doc + Arc 5 test coverage assessment + Anthropic API cost 14-cycle trend analysis | claude/roadmap/current_roadmap.md#PT-04; docs/qa/arc5_qa_completion_criteria.md; docs/qa/arc5_test_coverage_assessment.md; docs/ops/anthropic_api_cost_trend_2026.md | None |
| EPIC-01 | SI-05 digest deep links (Risk Dashboard + Red Flag Journal) + N/A pass-rate reason clarification (distinct messages: no_events vs data_unavailable); 13 new unit tests | backend/services/si05_digest_service.py | None |
| EPIC-02 | Performance hardening: 5-min FX rate TTL cache (concentration-status); schema-once guards for red-flag-journal + behavioural-drift; 15-min per-ticker research TTL cache with screener invalidation + hit/miss logging | backend/utils/pricing.py; backend/routers/red_flag_journal.py; backend/routers/analytics.py; backend/routers/research.py; backend/routers/screener.py | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-03 — BLG-FE-64: RFJ design review pre-brief | Gate 2026-06-21 not cleared at planning (SI-03 live ≥30 days) | BLG-FE-64 (backlog.md) |
| ST-04/05/06/07 — Production latency re-measurement | Staging-only ACs: production deployment required | BLG-OPS-66/67/68/69 (backlog.md) |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-03.md (agent-mediated, 2026-06-16), qa_evidence_EPIC-01.md (agent-mediated, 2026-06-16), qa_evidence_EPIC-02.md (agent-mediated, 2026-06-16)
- Deviations filed: None
- Test scenarios referenced: tests/test_si05_digest_service.py (33 tests; 13 new for EPIC-01)

## Sprint: 2026-06-16__release-v5.7
**Date:** 2026-06-17
**Status:** Verified — 2026-06-17

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Production latency verifications (ST-01–04): concentration-status p95=755ms, red-flag-journal p95=872ms, behavioural-drift p95(cached)=677ms, research-view p95=105ms — all within targets; SI-05 deep link mobile fix (ST-05): MarkdownV2 + HashRouter /#/ bugs fixed, both Telegram deep links confirmed working; Arc 5 Playwright coverage (ST-06–08): SC-SI-01d, SC-RFJ-04, SC-ARC5-05 added | stage4_backlog_slice.md#ST-01–05; tests/e2e/si01-si03-integration.spec.js; tests/e2e/red-flag-journal.spec.js; tests/e2e/arc5-compliance-section.spec.js | None |
| EPIC-02 | Lazy-import pattern documentation in backend engineering guide (ST-10); execution_prompt §5.3 dual sign-off pattern confirmed (ST-11) | docs/specs/api_contracts/backend_engineering_patterns.md; claude/system/execution_prompt.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-09 — BLG-FE-64: RFJ design review pre-brief | Gate 2026-06-21 not cleared (SI-03 live <30 days); 4th deferral | BLG-FE-64 (backlog.md) |
| ST-12 — BLG-GOV-112: SI-05 cadence review | EPIC-03 Sprint 2 conditional — gate 2026-07-04 not reached | BLG-GOV-112 (backlog.md) |
| ST-13 — BLG-GOV-115: SI-05 actionability metrics | EPIC-03 Sprint 2 conditional — gate 2026-07-04 not reached | BLG-GOV-115 (backlog.md) |
| ST-14 — BLG-OPS-59: SI-05 p99 latency baseline | EPIC-03 Sprint 2 conditional — gate 2026-07-04 not reached | BLG-OPS-59 (backlog.md) |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (I&O co-sign + Head of UX & Design, 2026-06-17), qa_evidence_EPIC-02.md (autonomous class, 2026-06-17)
- Deviations filed: None
- Test scenarios referenced: tests/e2e/si01-si03-integration.spec.js, tests/e2e/red-flag-journal.spec.js, tests/e2e/arc5-compliance-section.spec.js

## Sprint: 2026-06-17__release-v5.8
**Date:** 2026-06-17
**Status:** Sprint_Complete — pending verification

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | FRONTEND_URL production env var configured (ST-03): SI-05 digest deep-link support restored in production backend; deployment runbook v0.3 updated. Governance complexity assessment (ST-04): GCA-2026-06-17 produced covering all 6 governance engines; 7 simplification candidates filed (BLG-GOV-123–129) | docs/ops/production_deployment_runbook.md#6.1; docs/governance/governance_complexity_assessment_2026-06-17.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-01 — RFJ design review pre-brief | Gate 2026-06-21 not yet reached; PO-authorised deferral (5th) | BLG-FE-64 |
| ST-02 — RFJ visual design review | Depends on ST-01; gate 2026-06-21 not reached | BLG-FE-41 |
| ST-05 — SI-05 cadence review | Sprint 2 gate 2026-07-04 not reached | BLG-GOV-112 |
| ST-06 — SI-05 actionability metric definition | Sprint 2 gate 2026-07-04 not reached | BLG-GOV-115 |
| ST-07 — SI-05 p99 latency baseline review | Sprint 2 gate 2026-07-04 not reached | BLG-OPS-59 |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (Director of Quality, 2026-06-17)
- Deviations filed: None
- Test scenarios referenced: None (all deliverables are documentation and operational artefacts)

## Sprint: 2026-06-17__release-v5.9
**Date:** 2026-06-18
**Status:** Sprint_Complete — pending verification

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Governance simplification SC-03–SC-07: execution_prompt.md v3.44 (spec_references 3-case lookup consolidated; Playwright selector check conditional on DOM changes); roadmap_prompt.md v7.3 (STEPs 8.6/8.7 fatigue guardrail removed; convergence bias coverage added to Challenger); release_planning_prompt.md v2.37 (STEP 5.7 conditional on escalations; STEP 1.3 reduced to advisory note); post_ship_closure.md v2.14 (Advisory Summary Block format docs compressed to 3 lines) | claude/system/execution_prompt.md v3.44; claude/system/roadmap_prompt.md v7.3; claude/system/release_planning_prompt.md v2.37; claude/system/post_ship_closure.md v2.14 | None |
| EPIC-02 | Yahoo Finance 401 backoff path integration test (ST-06); DoQ sign-off date audit v3.7–v3.9 advisory (ST-07, 10 files reviewed, 3 findings); QA evidence format audit v3.7–v4.0 advisory (ST-08, 13 files, 6 findings); agent idea participation summary (ST-09, 11 windows, 100% participation rate across 22 eligible agents); regression test baseline v1.1 refresh (ST-10, 66 endpoints, 41 Playwright specs); pre-entry panel collapsed badge showing warn/fail count with Playwright tests SC-PEP-BADGE-01a/01b/02 (ST-11) | tests/test_screener_data_service.py; docs/qa/regression_test_suite_baseline.md v1.1; src/pages/TradePlan.js; tests/e2e/pre-entry-panel-badge.spec.js | None |

### Capabilities deferred or returned

None — all 11 stories delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (autonomous class, 2026-06-17), qa_evidence_EPIC-02.md (Director of Quality, 2026-06-18)
- Deviations filed: None
- Test scenarios referenced: tests/test_screener_data_service.py::test_yahoo_backoff_path_401_sleep_once_then_200 (ST-06); tests/e2e/pre-entry-panel-badge.spec.js SC-PEP-BADGE-01a/01b/02 (ST-11)

## Sprint: 2026-06-19__release-v6.0
**Date:** 2026-06-22
**Status:** Sprint_Complete — pending verification

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | P0 signal correctness fix: signal_service.suggested_shares now calls size_position() per strategy_rules.md §4.1 canonical risk-based sizing formula; cash-allocation model removed | docs/specs/api_contracts/signal_endpoints.md; claude/strategy/strategy_rules.md#4.1 | None |
| EPIC-02 | Trader's Morning Briefing dashboard (ST-02): frontend composition from 5 live endpoints (grace-period-alerts, positions, red-flag-journal, earnings, arc5-compliance); Playwright coverage in tests/e2e/morning-briefing.spec.js. Net-of-costs performance tracking (ST-03): optional commission/spread/slippage fields on trade records; net R-multiple calculation; trade history display updated | docs/specs/api_contracts/trade_endpoints.md; docs/specs/data_model.md | None |
| EPIC-03 | Screener data quality telemetry (ST-04): screener results enriched with data_source, data_freshness_utc, degraded_run indicator; ScreenerQualityPanel component; screener contract updated to v1.2; Playwright coverage in tests/e2e/screener-quality.spec.js. SI-05 deep link AC-04 staging confirmation (ST-05): both deep links verified by I&O Owner post-FRONTEND_URL | docs/specs/api_contracts/screener_api_contract.md v1.2; docs/specs/api_contracts/digest_endpoints.md | None |
| EPIC-04 | RFJ design review pre-brief (ST-06) and visual design review (ST-07): HoUX&D Accept/Refine decisions; BLG-FE-66/67 filed. SI-05 effectiveness reviews: cadence maintained weekly (ST-08); 4 actionability metrics defined ATCR/RFAR/DDCR/EPAR (ST-09); Phase 2 DEFERRED to 2026-08-04 (ST-10); p99 latency baseline established at 16-day mark with PASS WITH DEVIATION (ST-11) | docs/design/2026-06-19__release-v6.0/rfj-design-review/; docs/product/decisions/si05-*; docs/testing/staging_latency_review_ST-11.md | P3 (ST-11): 16-day measurement window; AC-02 N/A — no prior baseline |

### Capabilities deferred or returned

None — all 11 stories delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (agent-mediated, 2026-06-19), qa_evidence_EPIC-02.md (Director of Quality, 2026-06-19), qa_evidence_EPIC-03.md (Director of Quality + I&O staging, 2026-06-22), qa_evidence_EPIC-04.md (autonomous class, 2026-06-22)
- Deviations filed: None (P3 process deviations for ST-11 documented in qa_evidence_EPIC-04.md only)
- Test scenarios referenced: tests/e2e/morning-briefing.spec.js (ST-02 AC-09); tests/e2e/screener-quality.spec.js (ST-04 AC-07)

## Sprint: 2026-06-26__release-v6.3
**Date:** 2026-06-30
**Status:** Sprint_Complete — pending verification

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Production correctness & AI security hardening: AI journal summary fix (ST-01); R-multiple display fix via net_r_multiple field mapping (ST-02); per-endpoint rate limiting for /ai/daily-briefing (10 req/min) and /ai/chat (30 req/min) with 429+Retry-After (ST-03); AI response injection risk assessment — 5 inputs assessed, 2 open risks filed (ST-04); advisory disclaimer visibility assessment — partially compliant, remediation items BLG-UX-01/02 filed (ST-05); §13 API contract review checklist authored and applied to both AI endpoints (ST-06) | docs/specs/api_contracts/ai_endpoints.md v1.5; docs/specs/security/ai_injection_risk_assessment.md; docs/specs/qa/ai_disclaimer_visibility_assessment.md; docs/specs/api_contracts/ai_advisory_contract_checklist.md; docs/reference/openapi.yaml v3.5.0 | BLG-UX-01 (P3), BLG-UX-02 (P2): disclaimer contrast below WCAG AA — backlog items filed, §13 core intent met |
| EPIC-02 | Strategy computation CI + advisory contract quality: 21 nightly computation tests covering trailing stop (7), rebalance exit (5), inv-vol sizing (9) (ST-07); strategy signal regression test specification — TS/RX/IV scenarios, float tolerance, fixture maintenance procedure (ST-08); 8 AI chat schema validation tests — schema conformance + advisory-only constraint tests (ST-09); 11 §13 boundary scenarios for both AI advisory endpoints + compliance matrix + template for future AI endpoints (ST-10) | tests/test_nightly_computations.py; tests/fixtures/nightly_portfolio_state.json; docs/specs/qa/strategy_signal_regression_spec.md; tests/test_ai_chat_schema.py; docs/specs/qa/ai_s13_boundary_test_suite.md | None |
| EPIC-03 | Strategy Benchmark page + UX enhancement: full Strategy Benchmark page with 3 backend endpoints (POST /strategy/benchmark/import, GET /strategy/benchmark/summary, GET /strategy/benchmark/trades), DB schema (backtest_trades, backtest_yearly_performance), import_backtest.py companion script, 3-panel page with sticky filters, toggle modes, exit reason badges (ST-11); Morning Briefing progressive disclosure with 3 collapsible sections, localStorage persistence, Playwright coverage SC-PD-01 through SC-PD-07 (ST-12); GET /health/scheduler endpoint tracking 3 scheduler jobs in-memory (ST-13); live latency baseline: daily-briefing p50=10,296ms p95=11,152ms; chat p50=6,258ms p95=7,035ms (ST-14); Render rollback runbook with decision matrix + step-by-step procedure (ST-15) | docs/specs/api_contracts/strategy_benchmark_endpoints.md; docs/reference/openapi.yaml v3.7.0; src/pages/StrategyBenchmark.js; docs/frontend/prompts/ai-briefing-progressive-disclosure-v1.md; tests/e2e/ai-briefing-progressive-disclosure.spec.js; docs/specs/api_contracts/health_endpoints.md v1.3; docs/ops/api_performance_baseline.md §22.3; docs/operations/render_rollback_runbook.md | None |

### Capabilities deferred or returned

None — all 15 stories delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (agent-mediated, 2026-06-30), qa_evidence_EPIC-02.md (agent-mediated, 2026-06-30), qa_evidence_EPIC-03.md (agent-mediated, 2026-06-30)
- Deviations filed: None (P3 spec deviations); BLG-UX-01 (P3) and BLG-UX-02 (P2) filed as backlog items for disclaimer contrast
- Test scenarios referenced: tests/e2e/r-multiple-reflection.spec.js SC-RM-01..03c (ST-02); tests/test_nightly_computations.py (ST-07); tests/test_ai_chat_schema.py (ST-09); tests/e2e/ai-briefing-progressive-disclosure.spec.js SC-PD-01..07 (ST-12)

## Sprint: 2026-07-06__release-v6.7
**Date:** 2026-07-08
**Status:** Verified — 2026-07-08

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-02 | Governance process hardening (AUD-2026-07-06 follow-through): `.claude/skills/` write-scope authority provision + commit-check diff-verification patch, closing the 3-cycle-carried write-scope escalation (ST-04); canonical Structural Append-Verification Procedure applied to all 4 append-only governance logs (ST-05); `audit.py` same-session commit SLA requirement (ST-06); Delivery Verification STEP 6 status-line documentation (ST-07) | `shared_standards.md` §17, §7.1; `.claude/skills/commit-check/SKILL.md`; `claude/audit.py`; `delivery_verification_prompt.md` STEP 6 | None |
| EPIC-01 | UX & Accessibility contrast remediation: app-wide dark-theme secondary-text fix (226 instances, 59 files) (ST-01); light-theme companion pairing (697 instances, 101 files), including a `src/Layout.js` app-shell gap found and fixed at DoQ review (ST-02); canonical `text-slate-600 dark:text-slate-400` secondary-text token locked into `design_system.md` (ST-03) | `docs/design/2026-07-06__release-v6.7/secondary-text-contrast/ux_spec.md`; `docs/specs/frontend/pages/positions.md` v2.0; `dashboard.md` v2.6; `reflections.md` v0.2; `docs/specs/frontend/design_system.md` v1.0 | None |

### Capabilities deferred or returned

None — all 7 stories delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-02.md (autonomous class, 2026-07-06), qa_evidence_EPIC-01.md (agent-mediated, Director of Quality role, 2026-07-08)
- Deviations filed: None
- Test scenarios referenced: tests/e2e/secondary-text-contrast.spec.js SC-CTR-01a/01b/02a/02b (ST-01/ST-02)

## Sprint: 2026-07-08__release-v6.8
**Date:** 2026-07-09
**Status:** Verified — 2026-07-09

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Production correctness & security hardening: `trade_plans.position_id` linkage bug root-caused and forward-fixed via backend auto-link in `add_position()` (ST-01, BLG-BE-46); SQL column allowlist added to `database.update_signal()` closing an injection-shaped vulnerability (ST-02, BLG-SEC-08); manual anomaly review of all 300 production signal records, no anomalies found (ST-03, BLG-SEC-07); application X-API-Key formally registered in the security register, enabling direct gate-condition verification (ST-04, BLG-OPS-99) | `docs/security/signal_anomaly_review_2026-07-09.md`; `docs/security/api_key_security_register.md#6-application-x-api-key` | None |
| EPIC-02 | Mandatory Product Value Alert pull-forwards: trade-plan tagging with tag-based performance filtering on Analytics, independent of position/journal tags (ST-05, BLG-FEAT-52); collapsible SI-02 Gate Status section on Reports page showing live total/linked closed-trade counts and 3 gate condition badges (ST-06, BLG-FEAT-71) | `docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md`; `trade_plan.md` §5c; `analytics.md` §14a; `trade_plan_endpoints.md`; `analytics_endpoints.md`; `docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md`; `reports.md` §SI-02 Gate Status | None |
| EPIC-03 | Spec & governance debt clearance: dashboard visual hierarchy review (ST-07, BLG-SPEC-58); R-multiple cross-currency normalization spec (ST-08, BLG-SPEC-59); trailing stop visual indicator spec (ST-09, BLG-SPEC-60) and effectiveness metric definition (ST-10, BLG-SPEC-61); 12 dark Playwright spec files fixed via route-ordering/locator corrections (ST-11, BLG-QA-64); CI inline OpenAPI-vs-baseline drift detection (ST-12, BLG-GOV-134); Anthropic API token usage/cost logging verified pre-met (ST-13, BLG-OPS-74); `Watchlist.js` decomposed into hooks + presentational components for ESLint compliance (ST-14, BLG-FE-77); v5.1–v5.4 endpoint baseline extension verified pre-met (ST-15, BLG-OPS-61); Playwright Test Authoring Standard extracted to `shared_standards.md` §18 (ST-16, BLG-GOV-123); system threat model document (ST-17, BLG-OPS-71) | `docs/specs/qa/dashboard_visual_hierarchy_review_v6.8.md`; `metrics_definitions.md`; `positions.md#Trailing Stop Column`; `docs/specs/qa/trailing_stop_visual_indicator_review_v6.8.md`; `playwright.config.js`; `.github/workflows/quality_gate.yml#api_baseline_drift`; `ai_endpoints.md#GET /ai/claude-audit-log`; `src/pages/Watchlist.js`; `api_performance_baseline.md` §17/§19; `shared_standards.md#18`; `docs/security/threat_model.md` | None |

### Capabilities deferred or returned

None — all 17 stories delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (agent-mediated, 2026-07-09), qa_evidence_EPIC-02.md (agent-mediated, 2026-07-09), qa_evidence_EPIC-03.md (agent-mediated across multiple domain authorities, 2026-07-09)
- Deviations filed: None (2 backlog items filed as follow-up: BLG-SPEC-71, BLG-SPEC-72, plus BLG-FE-95, BLG-BE-50)
- Test scenarios referenced: tests/test_position_trade_plan_link.py; tests/test_signal_write_sanitization.py; tests/e2e/trade-plan.spec.js SC-TP-24-27; tests/e2e/trade-plan-tag-filter.spec.js SC-TPTF-01-05; tests/e2e/reports-si02-gate-status.spec.js SC-SI02-01-06; tests/e2e/arc5-compliance-section.spec.js; tests/e2e/entry-checklist.spec.js; tests/e2e/gate-progress.spec.js; tests/e2e/paper-account.spec.js; tests/e2e/plan-vs-reality.spec.js; tests/e2e/pre-entry-panel-badge.spec.js; tests/e2e/red-flag-journal.spec.js; tests/e2e/sector-heatmap.spec.js; tests/e2e/si01-si03-integration.spec.js; tests/e2e/signals-add-to-watchlist.spec.js; tests/e2e/signals-allocation-insufficient.spec.js

## Sprint: 2026-07-10__release-v6.9
**Date:** 2026-07-10
**Status:** Verified — 2026-07-10

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | On-demand SI-01 compliance recheck for open positions: `GET /positions/{position_id}/compliance-recheck` re-applies the 5 existing SI-01 pre-entry deterministic rule checks against a position's current state (regime, cash, sector, earnings, sizing) rather than its entry-time snapshot; `ComplianceRecheckModal.js` reuses the `PreEntryValidationPanel` pass/warn/fail visual pattern, wired into a new "Recheck Compliance" action in the Positions Table View Actions column and Grid View card footer (ST-01, BLG-FEAT-64) | `docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md`; `docs/specs/frontend/pages/positions.md#Compliance Recheck Panel`; `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/compliance-recheck` | None |
| EPIC-02 | Overnight/weekend gap risk flag for open positions: `GET /positions/{position_id}/gap-risk` combines the DS-04 earnings calendar with historical OHLCV gap statistics to flag earnings-before-next-session and Friday-close weekend-hold positions; new "Alerts" Table View column (completing the column documented since v6.2 ST-05 but never built as a separate column — RISK OFF badge relocated into it, GAP RISK badge added, stacked); Grid View GAP RISK badge near ticker (ST-02, BLG-FEAT-65) | `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md`; `docs/specs/frontend/pages/positions.md#Gap Risk Badge`; `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk` | None |

### Capabilities deferred or returned

None — both named mandatory Product Value Alert pull-forwards were delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (agent-mediated: Strategy Rules & System Intent Owner §13 AC-04, Director of Quality EPIC consolidation, 2026-07-10), qa_evidence_EPIC-02.md (agent-mediated: Strategy Rules & System Intent Owner §13 AC-04, Director of Quality EPIC consolidation, 2026-07-10)
- Deviations filed: None
- Test scenarios referenced: tests/test_compliance_recheck.py; tests/e2e/compliance-recheck.spec.js SC-CR-01–08; tests/test_gap_risk.py; tests/e2e/gap-risk-flag.spec.js SC-GR-01–08

## Sprint: 2026-07-12__release-v7.0
**Date:** 2026-07-13
**Status:** Verified_with_deviations — 2026-07-13

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Positions Grid View/Table View badge parity: RISK OFF badge added to Grid View cards (deep blue #1E40AF), trailing-stop value + breach indicator (icon-only) added to Grid View, combined GAP RISK/RISK OFF stacking confirmed distinguishable in both views (ST-01–ST-05, BLG-SPEC-80/BLG-FE-102/BLG-FE-97/BLG-QA-95/BLG-FE-104) | `docs/specs/frontend/pages/positions.md#Alerts Column`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`; `docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md` | DEV-EPIC01-ST05-01 (P2 — Table View RISK OFF badge colour/label pre-existing spec deviation, unrelated to this sprint; BLG-FE-107, target v7.1) |
| EPIC-02 | v6.9 carryover reconciliation and fixes: Tax Year P&L tab spec reconciled to shipped behaviour, Table View breach badge brought into spec colour/label compliance, Gate Progress Indicator copy reconciled, Dashboard/StrategyBenchmark light-theme heading contrast fixed, `trailing_stop_action_rate` metric capture instrumented, `GET /ai/claude-audit-log` gained endpoint/date-range filters, Sector Concentration heat map now joins `ticker_universe` for real sector data instead of stale/missing values (ST-06–ST-12) | `docs/specs/frontend/pages/reports.md`; `docs/specs/metrics_definitions.md#Trailing Stop Action Rate`; `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column`; `docs/specs/frontend/pages/dashboard.md#6`; `docs/specs/api_contracts/ai_endpoints.md`; `docs/specs/frontend/pages/risk_dashboard.md#8a. Component: Sector Concentration Heat Map` | None |
| EPIC-03 | New reporting and position-review features: tax-year P&L CSV export (button order fixed to match spec, Playwright coverage added), realized vs. unrealized gain split in Monthly P&L view, position review-cadence nudge (`last_reviewed_at` tracking + `PATCH /positions/{id}/mark-reviewed`) (ST-13–ST-15, BLG-FEAT-69/BLG-FEAT-70/BLG-FEAT-68) | `docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md`; `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`; `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md`; `docs/specs/frontend/pages/reports.md`; `docs/specs/frontend/pages/positions.md#Last Reviewed Column` | None |

### Capabilities deferred or returned

None — all 15 sealed backlog-slice items were delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (Director of Quality, 2026-07-13), qa_evidence_EPIC-02.md (Director of Quality, 2026-07-13), qa_evidence_EPIC-03.md (Director of Quality, 2026-07-13)
- Deviations filed: DEV-EPIC01-ST05-01 (P2, BLG-FE-107, target v7.1)
- Test scenarios referenced: tests/e2e/epic01-v70-grid-badge-parity.spec.js SC-GVP-01–09; tests/e2e/heading-light-theme-contrast.spec.js; tests/test_portfolio_risk_sector.py; tests/test_claude_audit_log_filters.py; tests/test_trailing_stop_recommendation_log.py; tests/e2e/tax-year-csv-export.spec.js; tests/e2e/monthly-pnl-realized-unrealized.spec.js; tests/e2e/position-review-cadence-nudge.spec.js; tests/test_mark_position_reviewed.py

## Sprint: 2026-07-14__release-v7.1
**Date:** 2026-07-14
**Status:** Verified_with_deviations — 2026-07-14

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Nightly backtest data-integrity fixes: ticker eligibility now gated on `ticker_universe.created_at` closing a look-ahead-bias bug (ST-01, BLG-BE-59); `total_pnl_gbp` non-reproducibility root-caused to external yfinance historical-price revisions, guarded via a new drift-check alert (`import_backtest.check_drift_alert`, £50 threshold, distinct exit code, greppable log line) rather than eliminated at the source (ST-02, BLG-BE-60) | spec_reference_not_applicable — bug fixes, no prior canonical spec; verified via `tests/test_production_strategy.py` (`TestComputeSignalsCreatedAtGating`, `TestBacktestDeterminism`, `TestDriftAlert`) | None |
| EPIC-02 | Table View RISK OFF badge brought into spec compliance: `#1E40AF` colour, "RISK OFF" label, no icon — matches Grid View, closing a v7.0 carryover deviation (ST-03, BLG-FE-107) | `docs/specs/frontend/pages/positions.md#Alerts Column`; `#Known Deviations` | None — closed DEV-EPIC01-ST05-01 (v2.3→v2.4) |
| EPIC-03 | v7.0 post-ship hardening pass across 4 features: position review-cadence nudge IDOR fix (PATCH /positions/{id}/mark-reviewed now routes through ownership check) plus NULL/backfill and lifecycle-state confirmation (ST-04); review-cadence frontend re-verified pre-met, no code changes (ST-05); realized/unrealized P&L split ownership/rounding/reconciliation rules documented and production-verified, surfacing a new P3 data-freshness deviation (ST-06, DEV-REPORTS-ST06-01, BLG-SPEC-87); tax-year CSV export Content-Type/auth/versioning documented with 11 new content-asserting tests and a new scenario doc (ST-07) | `backend/services/position_service.py#mark_position_reviewed()`; `docs/specs/frontend/pages/positions.md#Last Reviewed Column`, `#Position Lifecycle State Badge`; `docs/specs/metrics_definitions.md#Realized / Unrealized P&L Split`; `docs/specs/frontend/pages/reports.md#Unrealised P&L Card`, `#Known Deviations`; `docs/reference/openapi.yaml`; `docs/specs/api_contracts/reports_endpoints.md#Response (200 — CSV, format=csv)`; `docs/specs/api_contracts/backend_engineering_patterns.md#CSV/export response-body pattern`; `docs/testing/tax_year_csv_export_scenarios.md` | DEV-REPORTS-ST06-01 (P3, BLG-SPEC-87, target TBD) |

### Capabilities deferred or returned

None — all 7 sealed backlog-slice items were delivered within the sprint.

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (agent-mediated, 2026-07-14), qa_evidence_EPIC-02.md (agent-mediated, 2026-07-14), qa_evidence_EPIC-03.md (autonomous class, BLG-GOV-19, 2026-07-14)
- Deviations filed: DEV-REPORTS-ST06-01 (P3, BLG-SPEC-87) — new; DEV-EPIC01-ST05-01 (P2, BLG-FE-107) — closed this sprint
- Test scenarios referenced: tests/test_production_strategy.py; tests/e2e/epic01-v62-stops-alerts.spec.js SC-RO-02; tests/e2e/epic01-v70-grid-badge-parity.spec.js SC-GVP-02; tests/e2e/gap-risk-flag.spec.js; tests/test_mark_position_reviewed.py; tests/e2e/position-review-cadence-nudge.spec.js SC-RCN-01–07; tests/e2e/monthly-pnl-realized-unrealized.spec.js; tests/test_reports_integration.py::TestTaxYearCsvExport

## Sprint: 2026-07-15__release-v7.2
**Date:** 2026-07-15
**Status:** Verified — 2026-07-15

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Mobile responsiveness baseline assessment across positions/screener/trade plan form/trade entry/Red Flag Journal (ST-01); Arc 5 gate confirmed not-met, proceeding on recorded PO priority override | docs/specs/frontend/mobile_responsiveness_baseline_assessment_v7.2.md | None |
| EPIC-02 | Trade-plan-linkage pre-implementation readiness pass (ST-02, BLG-FE-109) — schema gap, contract pre-stage, prefill pattern, auth/S13 boundary, regression risk, and SI-02 scope all confirmed ahead of ST-03 implementation | docs/specs/blg_fe_109_pre_implementation_readiness_pass.md | None |
| EPIC-03 | Dashboard-UX readiness/spec & instrumentation pass (ST-04, BLG-FE-110/111) — design_system.md v1.0→v1.1 and new base44_prompt_template_library.md formalise the event/instrumentation contract ahead of ST-05/ST-06 implementation | docs/specs/blg_fe_110_111_pre_implementation_spec_instrumentation_pass.md; docs/specs/frontend/design_system.md; docs/specs/frontend/base44_prompt_template_library.md | None |
| EPIC-04 | Notification/digest surface consolidation review (ST-07) — 4 findings documented (duplicate nav entries, disconnected nav grouping, no digest/alert cross-link, two disconnected "digest" concepts); consolidation recommendation deferred to next groom-backlog pass | docs/specs/frontend/notification_surface_consolidation_review_v7.2.md | None |
| EPIC-05 | Combined design-review + shared-Playwright-suite plan (ST-08) — confirms design_gate.md's combined pass and names the shared spec file (tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js) for ST-03/ST-05/ST-06 | docs/specs/frontend/blg_qa_111_combined_design_review_shared_playwright_plan.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-03, ST-05, ST-06 | Implementation stories gated on this sprint's readiness passes (ST-02/ST-04) — now unblocked, ready for next sprint planning | n/a — carried in stage4_backlog_slice.md sequencing constraint, not a backlog return |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md, qa_evidence_EPIC-02.md, qa_evidence_EPIC-03.md, qa_evidence_EPIC-04.md, qa_evidence_EPIC-05.md (all autonomous class, BLG-GOV-19, 2026-07-15)
- Deviations filed: None
- Test scenarios referenced: None — all five deliverables are readiness/audit/planning documentation artefacts; no runnable test files added this sprint

## Sprint: 2026-07-16__release-v7.3
**Date:** 2026-07-16
**Status:** Verified — 2026-07-16

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Trade-plan-to-execution linkage UX "Start Trade from Plan" (ST-01, BLG-FE-109); dashboard empty/first-run state coverage (ST-02); dashboard briefing visual hierarchy (ST-03) — all three carried forward from v7.2 | src/pages/TradePlan.js, src/pages/TradePlans.js, src/pages/TradeEntry.js, src/pages/DashboardHome.js, src/pages/Watchlist.js | None |
| EPIC-02 | Command Palette (BLG-FE-115) pre-implementation readiness pass (ST-04) — searchable entity index scope, keyboard interaction contract, Base44 prompt template, discoverability plan, adoption metrics, and confirmed no new API surface; flagged `cmdk` package missing from `package.json` as an implementation-time blocker | docs/specs/blg_fe_115_pre_implementation_readiness_pass.md; docs/specs/frontend/base44_prompt_template_library.md | None |
| EPIC-03 | Custom Price Alerts (BLG-FE-116) pre-implementation readiness pass (ST-05) — new `price_alerts` schema designed (existing `alert_rules` is singleton-per-type, cannot represent per-ticker alerts); evaluation extension to existing `POST /alerts/evaluate` cron and `GET /health/scheduler` designed; **§13 pre-check PASSED** (RISK-03 cleared) | docs/specs/blg_fe_116_pre_implementation_readiness_pass.md | None |
| EPIC-04 | Bulk Actions (BLG-FE-117) pre-implementation readiness pass (ST-06) — per-entity batch-mutation endpoint pattern designed with explicit partial-failure response shape (no prior batch-write pattern existed); Base44 prompt template added; **§13 pre-check PASSED** (RISK-04 cleared) | docs/specs/blg_fe_117_pre_implementation_readiness_pass.md; docs/specs/frontend/base44_prompt_template_library.md | None |
| EPIC-05 | Saved Filters & Calendar View (BLG-FE-118) pre-implementation spec pass (ST-07) — dedicated `saved_filters` table decided over JSON-column-on-settings (RISK-05 schema decision recorded with rationale); calendar view spec authored reusing `GET /reports/monthly-pnl`'s date-grouping logic; flagged `react-day-picker` package missing from `package.json` | docs/specs/blg_fe_118_pre_implementation_readiness_pass.md | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| `BLG-FE-115/116/117/118` | Implementation of the four readiness-passed features themselves remains out of this sprint's scope — now unblocked for v7.4 release planning per the PO anchor-scope decision (`2026-07-16__scheduled`, DL-067) | n/a — carried in stage4_backlog_slice.md#Deferred-Items sequencing constraint, not a backlog return |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md through qa_evidence_EPIC-05.md (EPIC-02 through EPIC-05 all autonomous class, BLG-GOV-19, 2026-07-16)
- Deviations filed: None
- Test scenarios referenced: None — all five deliverables this sprint are UI implementation (EPIC-01, carried from v7.2 with its own Playwright coverage) or readiness/spec documentation artefacts (EPIC-02 through EPIC-05); no new runnable test files added by EPIC-02–05

## Sprint: 2026-07-17__release-v7.4
**Date:** 2026-07-17
**Status:** Verified — 2026-07-17

### Capabilities now live (merged this sprint)

| EPIC | Capability | Spec sections implemented | Deviations |
|------|-----------|--------------------------|------------|
| EPIC-01 | Consolidated v7.4 UI-feature readiness pass (ST-01) — dependency pre-flight (`cmdk`, `react-day-picker` added to `package.json`), UX specs for saved-filters empty state and bulk-actions confirmation/undo-window modal, command-palette keyboard-navigation design review, Playwright visual-regression baseline scope, command-palette analytics event schema, regression-suite CI tagging scheme. Readiness pass only — no shippable UI. | `docs/specs/blg_spec_95_v7_4_ui_readiness_pass.md` | None |

### Capabilities deferred or returned

| ST Item | Reason | Backlog reference |
|---------|--------|-------------------|
| ST-02 (BLG-FE-115, command palette) | Removed from scope by `AMD-20260717-01` — Design Gate BLOCKED, no approved design-review artefact | backlog.md |
| ST-03 (BLG-FE-116, price alerts) | Removed from scope by `AMD-20260717-01` — Design Gate BLOCKED, no design artefact scheduled anywhere in v7.4 plan | backlog.md |
| ST-04 (BLG-FE-117, bulk actions) | Removed from scope by `AMD-20260717-01` — Design Gate BLOCKED, no UX spec for confirmation/undo-window modal | backlog.md |
| ST-05 (BLG-FE-118, saved filters/calendar) | Removed from scope by `AMD-20260717-01` — Design Gate BLOCKED, no UX spec for empty state / no calendar-view design review | backlog.md |

### Verification inputs ready

- QA evidence logs: qa_evidence_EPIC-01.md (autonomous class, BLG-GOV-19, 2026-07-17)
- Deviations filed: None (one forward-looking backlog item filed: BLG-FE-122 — react-day-picker v8→v9 API break in `calendar.js`, pre-implementation finding for future EPIC-05)
- Test scenarios referenced: None — sole deliverable is a readiness/spec documentation artefact; no runnable test files added this sprint
