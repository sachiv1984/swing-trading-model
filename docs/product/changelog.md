# Product Changelog — Momentum Trading Assistant

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-16

> This document is a human-maintained record of what was shipped in each product version and when. It records delivery milestones and notable decisions. It is not an immutable system record — for point-in-time system status reports, see `docs/operations/status_reports/`.

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
