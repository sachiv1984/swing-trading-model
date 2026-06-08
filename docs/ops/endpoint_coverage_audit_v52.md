**Owner:** Head of Engineering; API Contracts & Documentation Owner
**Class:** Governance Document (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-08
**Cycle:** 2026-06-08__release-v5.2 (ST-12, BLG-GOV-100)

---

# Backend Endpoint Documentation Coverage Audit — Post-v5.1

## Purpose

Post-v5.1 audit of all endpoints defined in `backend/routers/` — verifying each has:
- (a) an entry in `docs/reference/openapi.yaml`
- (b) an entry in `backend/routers/test.py`
- (c) a `## METHOD /path` level-2 heading in a file in `docs/specs/api_contracts/`

---

## Audit Scope

**Files scanned:** All `*.py` files in `backend/routers/` (excluding `test.py` itself)
**Decorators enumerated:** `@router.get`, `@router.post`, `@router.put`, `@router.delete`
**Audit date:** 2026-06-08

---

## Route Inventory (47 endpoints)

| # | Method | Path | Router file |
|---|--------|------|-------------|
| 1 | POST | /ai/journal-summary | ai.py |
| 2 | GET | /ai/journal-summary/history | ai.py |
| 3 | POST | /ai/check-daily-cost | ai.py |
| 4 | GET | /ai/claude-audit-log | ai.py |
| 5 | GET | /alerts/rules | alerts.py |
| 6 | POST | /alerts/rules | alerts.py |
| 7 | DELETE | /alerts/rules/{rule_id} | alerts.py |
| 8 | POST | /alerts/evaluate | alerts.py |
| 9 | GET | /alerts/history | alerts.py |
| 10 | GET | /notifications | alerts.py |
| 11 | POST | /notifications/mark-all-read | alerts.py |
| 12 | GET | /notifications/preferences | alerts.py |
| 13 | GET | /analytics/metrics | analytics.py |
| 14 | GET | /analytics/cohort | analytics.py |
| 15 | GET | /analytics/r-multiple-distribution | analytics.py |
| 16 | GET | /analytics/compliance-metrics | analytics.py |
| 17 | GET | /analytics/market-correlation | analytics.py |
| 18 | GET | /analytics/arc5-compliance | analytics.py |
| 19 | GET | /analytics/behavioural-drift | analytics.py |
| 20 | GET | /digest/weekly | digest.py |
| 21 | POST | /digest/si05/send | digest.py |
| 22 | GET | /earnings/{ticker} | earnings.py |
| 23 | GET | /news/{ticker} | news.py |
| 24 | GET | /portfolio/paper-positions | paper_trading.py |
| 25 | GET | /trades/{trade_id}/plan-vs-reality | plan_vs_reality.py |
| 26 | GET | /portfolio/drawdown-status | portfolio_risk.py |
| 27 | GET | /portfolio/concentration-status | portfolio_risk.py |
| 28 | POST | /portfolio/size | portfolio_size.py |
| 29 | GET | /portfolio/pre-entry-validation | pre_entry_validation.py |
| 30 | GET | /portfolio/prospective-heat | prospective_heat.py |
| 31 | GET | /portfolio/red-flag-journal | red_flag_journal.py |
| 32 | GET | /research/{ticker} | research.py |
| 33 | GET | /screener/results | screener.py |
| 34 | POST | /screener/run | screener.py |
| 35 | GET | /ticker-universe | ticker_universe.py |
| 36 | POST | /ticker-universe | ticker_universe.py |
| 37 | DELETE | /ticker-universe/{ticker} | ticker_universe.py |
| 38 | POST | /trade-plans | trade_plans.py |
| 39 | GET | /trade-plans | trade_plans.py |
| 40 | GET | /trade-plans/by-position/{position_id} | trade_plans.py |
| 41 | GET | /trade-plans/{plan_id} | trade_plans.py |
| 42 | PUT | /trade-plans/{plan_id} | trade_plans.py |
| 43 | DELETE | /trade-plans/{plan_id} | trade_plans.py |
| 44 | POST | /trade-plans/generate-plan | trade_plans.py |
| 45 | POST | /trade-plans/{plan_id}/generate-thesis | trade_plans.py |
| 46 | GET | /trades/export/csv | trades_export.py |
| 47 | POST | /validate/calculations | validation.py |
| 48 | GET | /watchlist | watchlist.py |
| 49 | POST | /watchlist | watchlist.py |
| 50 | DELETE | /watchlist/{entry_id} | watchlist.py |

**Total: 50 endpoints** across 20 router files.

---

## Coverage Check Results

### Legend
- ✅ COVERED — entry present
- ❌ MISSING — entry absent
- ⚠️ DUPLICATE — documented in multiple files (not a gap; noted for awareness)

| # | Path | openapi.yaml | test.py | api_contracts |
|---|------|---|---|---|
| 1 | POST /ai/journal-summary | ✅ | ✅ | ✅ ai_endpoints.md |
| 2 | GET /ai/journal-summary/history | ❌ MISSING | ✅ | ❌ MISSING |
| 3 | POST /ai/check-daily-cost | ✅ | ✅ | ✅ ai_endpoints.md |
| 4 | GET /ai/claude-audit-log | ✅ | ✅ | ✅ ai_endpoints.md |
| 5 | GET /alerts/rules | ✅ | ✅ | ✅ alerts_endpoints.md |
| 6 | POST /alerts/rules | ✅ | ✅ | ✅ alerts_endpoints.md |
| 7 | DELETE /alerts/rules/{rule_id} | ✅ | ✅ | ✅ alerts_endpoints.md |
| 8 | POST /alerts/evaluate | ✅ | ✅ | ✅ alerts_endpoints.md |
| 9 | GET /alerts/history | ✅ | ✅ | ✅ alerts_endpoints.md |
| 10 | GET /notifications | ✅ | ✅ | ✅ alerts_endpoints.md |
| 11 | POST /notifications/mark-all-read | ✅ | ✅ | ✅ alerts_endpoints.md |
| 12 | GET /notifications/preferences | ✅ | ✅ | ✅ alerts_endpoints.md |
| 13 | GET /analytics/metrics | ✅ | ✅ | ✅ analytics_endpoints.md |
| 14 | GET /analytics/cohort | ✅ | ✅ | ✅ analytics_endpoints.md |
| 15 | GET /analytics/r-multiple-distribution | ✅ | ✅ | ✅ analytics_endpoints.md |
| 16 | GET /analytics/compliance-metrics | ❌ MISSING | ✅ | ❌ MISSING |
| 17 | GET /analytics/market-correlation | ✅ | ✅ | ✅ analytics_endpoints.md |
| 18 | GET /analytics/arc5-compliance | ✅ | ✅ | ✅ arc5_compliance_analytics.md |
| 19 | GET /analytics/behavioural-drift | ✅ | ✅ | ✅ behavioural_drift_contract.md |
| 20 | GET /digest/weekly | ✅ | ✅ | ✅ digest_endpoints.md |
| 21 | POST /digest/si05/send | ✅ | ✅ | ✅ digest_endpoints.md |
| 22 | GET /earnings/{ticker} | ✅ | ✅ | ✅ earnings_endpoints.md |
| 23 | GET /news/{ticker} | ❌ MISSING | ✅ | ❌ MISSING |
| 24 | GET /portfolio/paper-positions | ✅ | ✅ | ✅ portfolio_endpoints.md |
| 25 | GET /trades/{trade_id}/plan-vs-reality | ✅ | ✅ | ✅ trade_endpoints.md |
| 26 | GET /portfolio/drawdown-status | ✅ | ✅ | ✅ portfolio_endpoints.md |
| 27 | GET /portfolio/concentration-status | ✅ | ✅ | ✅ portfolio_endpoints.md |
| 28 | POST /portfolio/size | ✅ | ✅ | ✅ portfolio_endpoints.md |
| 29 | GET /portfolio/pre-entry-validation | ✅ | ✅ | ✅ portfolio_endpoints.md ⚠️ pre_entry_validation.md |
| 30 | GET /portfolio/prospective-heat | ✅ | ✅ | ✅ portfolio_endpoints.md |
| 31 | GET /portfolio/red-flag-journal | ✅ | ✅ | ✅ portfolio_endpoints.md ⚠️ red_flag_journal.md |
| 32 | GET /research/{ticker} | ✅ | ✅ | ✅ pre_trade_research_endpoints.md ⚠️ research_endpoint.md |
| 33 | GET /screener/results | ✅ | ✅ | ✅ screener_api_contract.md |
| 34 | POST /screener/run | ✅ | ✅ | ✅ screener_api_contract.md |
| 35 | GET /ticker-universe | ✅ | ✅ | ✅ ticker_universe_api_contract.md |
| 36 | POST /ticker-universe | ✅ | ✅ | ✅ ticker_universe_api_contract.md |
| 37 | DELETE /ticker-universe/{ticker} | ✅ | ✅ | ✅ ticker_universe_api_contract.md |
| 38 | POST /trade-plans | ✅ | ✅ | ✅ trade_plan_endpoints.md |
| 39 | GET /trade-plans | ✅ | ✅ | ✅ trade_plan_endpoints.md |
| 40 | GET /trade-plans/by-position/{position_id} | ✅ | ✅ | ✅ trade_plan_endpoints.md |
| 41 | GET /trade-plans/{plan_id} | ✅ | ✅ | ✅ trade_plan_endpoints.md |
| 42 | PUT /trade-plans/{plan_id} | ✅ | ✅ | ✅ trade_plan_endpoints.md |
| 43 | DELETE /trade-plans/{plan_id} | ✅ | ✅ | ✅ trade_plan_endpoints.md |
| 44 | POST /trade-plans/generate-plan | ✅ | ✅ | ✅ trade_plan_endpoints.md |
| 45 | POST /trade-plans/{plan_id}/generate-thesis | ✅ | ✅ | ✅ trade_plan_endpoints.md |
| 46 | GET /trades/export/csv | ✅ | ✅ | ✅ trade_endpoints.md |
| 47 | POST /validate/calculations | ✅ | ✅ | ✅ analytics_endpoints.md |
| 48 | GET /watchlist | ❌ MISSING | ❌ MISSING | ❌ MISSING |
| 49 | POST /watchlist | ❌ MISSING | ❌ MISSING | ❌ MISSING |
| 50 | DELETE /watchlist/{entry_id} | ❌ MISSING | ❌ MISSING | ❌ MISSING |

---

## Gap Summary

### Contract Document Gaps (BLG-SPEC items required)

| Route | Gap type | BLG-SPEC filed |
|---|---|---|
| GET /ai/journal-summary/history | Missing from ai_endpoints.md + openapi.yaml | BLG-SPEC-49 |
| GET /analytics/compliance-metrics | Missing from analytics_endpoints.md + openapi.yaml | BLG-SPEC-50 |
| GET /news/{ticker} | No contract document; missing from openapi.yaml | BLG-SPEC-51 |
| GET /watchlist | No contract document; missing from openapi.yaml + test.py | BLG-SPEC-52 |
| POST /watchlist | No contract document; missing from openapi.yaml + test.py | BLG-SPEC-52 |
| DELETE /watchlist/{entry_id} | No contract document; missing from openapi.yaml + test.py | BLG-SPEC-52 |

### openapi.yaml-only Gaps

Routes missing from openapi.yaml:
- GET /ai/journal-summary/history (covered in BLG-SPEC-49)
- GET /analytics/compliance-metrics (covered in BLG-SPEC-50)
- GET /news/{ticker} (covered in BLG-SPEC-51)
- GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id} (covered in BLG-SPEC-52)

### test.py-only Gaps

Routes missing from test.py:
- GET /watchlist (covered in BLG-SPEC-52)
- POST /watchlist (covered in BLG-SPEC-52)
- DELETE /watchlist/{entry_id} (covered in BLG-SPEC-52)

### Duplicate Coverage Notes (not gaps — informational)

| Route | Files |
|---|---|
| GET /portfolio/pre-entry-validation | portfolio_endpoints.md AND pre_entry_validation.md |
| GET /portfolio/red-flag-journal | portfolio_endpoints.md AND red_flag_journal.md |
| GET /research/{ticker} | pre_trade_research_endpoints.md AND research_endpoint.md |
| POST /trade-plans/generate-plan | ai_thesis_generation.md AND gemini_thesis_generation.md AND trade_plan_endpoints.md |

---

## Coverage Score

| Category | Total routes | Covered | Gap | Coverage % |
|---|---|---|---|---|
| openapi.yaml | 50 | 44 | 6 | 88% |
| test.py | 50 | 47 | 3 | 94% |
| api_contracts | 50 | 44 | 6 | 88% |

---

## BLG-SPEC Items Filed

- **BLG-SPEC-49** — Author GET /ai/journal-summary/history contract and openapi.yaml entry
- **BLG-SPEC-50** — Author GET /analytics/compliance-metrics contract and openapi.yaml entry
- **BLG-SPEC-51** — Author GET /news/{ticker} contract and openapi.yaml entry
- **BLG-SPEC-52** — Author watchlist endpoint contracts (GET/POST/DELETE) + openapi.yaml + test.py entries

**Note:** POST /digest/si05/send (ST-04 BLG-SPEC-48) was confirmed covered by this audit — contract at digest_endpoints.md, openapi.yaml entry present, test.py entry present. ST-04 can proceed directly to verification.

---

## Sign-Off

**Head of Engineering:** Sprint Execution Engine (autonomous class), 2026-06-08
**API Contracts & Documentation Owner:** Sprint Execution Engine (autonomous class), 2026-06-08
