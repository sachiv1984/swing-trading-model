**Owner:** Director of Quality
**Class:** Living Document (Class 3)
**Status:** Active
**Version:** 2.4
**Last Updated:** 2026-05-06
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

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
