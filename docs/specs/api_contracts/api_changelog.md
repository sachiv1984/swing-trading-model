**Owner:** API Contracts & Documentation Owner
**Class:** Class 2
**Status:** Canonical
**Version:** 1.9.0
**Last Updated:** 2026-08-18 (ST-07, EPIC-02, v8.9, BLG-FEAT-89 — v8.9.0 entry: 3 new Backtest Rule Change endpoints); prior — 2026-08-17 (ST-26, BLG-SPEC-118, EPIC-06, v8.8 — backfilled the v7.9–v8.4 gap: 2 new-endpoint entries added); prior — 2026-07-27 (v7.8.0 entry)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# API Changelog

## v8.9.0 (2026-08-18 — Release v8.9)

### strategy_benchmark_endpoints.md — v1.2 (NEW)

**EPIC:** EPIC-02
**ST:** ST-07

| Change | Details |
|--------|---------|
| New endpoint: POST /strategy/backtest-rule-change/run | Runs a candidate `strategy_rules.md` parameter change against a bounded historical window (first 20 active `ticker_universe` tickers, trailing 4 years), entirely in-app, and compares it against the live rule set over the identical universe/window (BLG-FEAT-89). Persists the run for audit. |
| New endpoint: GET /strategy/backtest-rule-change/runs | Run history, most recent first (AC-03). |
| New endpoint: GET /strategy/backtest-rule-change/runs/{run_id} | Re-view a prior run's stored output without re-running (AC-03). |

## v8.5.0 (2026-08-10 — Release v8.5)

### screener_api_contract.md — v1.3 (UPDATED)

**EPIC:** EPIC-06
**ST:** ST-21

| Change | Details |
|--------|---------|
| New endpoint: GET /screener/regime-distribution | Returns the aggregate risk-on/risk-off market regime distribution over screener run history for a rolling 30d/60d/all window (BLG-FEAT-29). Sourced from `screener_runs.regime_us`/`regime_uk` (one row per run), not `screener_results` (one row per ticker). |

**Note (this entry, corrected by ST-26/EPIC-06/v8.8, BLG-SPEC-118):** this changelog had not been updated between `v7.8.0` and this entry — the `v7.9`–`v8.4` gap flagged here has since been backfilled below (`v8.2.0`, `v7.9.0`), based on a full re-derivation of every `docs/specs/api_contracts/*.md` Changelog table entry dated within that window, not just the products changelog's higher-level "Spec sections updated" column (which cites section references, not necessarily new-endpoint additions — cross-checking against the actual contract file text caught one false positive, `PATCH /watchlist/{entry_id}`, cited in `v7.9`'s product changelog row but confirmed pre-existing since `v5.3`).

## v8.2.0 (2026-08-05 — Release v8.2)

### reports_endpoints.md — v0.11 (NEW)

**EPIC:** EPIC-01
**ST:** ST-01

| Change | Details |
|--------|---------|
| New endpoint: GET /reports/reconciliation | P&L / tax record reconciliation report (BLG-FEAT-88) — compares the Tax Year report's system-computed realised P&L total against an independently re-derived export-side sum for the same tax year, and surfaces a pass/fail match indicator to the user. |

## v7.9.0 (2026-07-28 — Release v7.9)

### portfolio_endpoints.md — v2.5.0 (NEW)

**EPIC:** EPIC-02
**ST:** ST-02

| Change | Details |
|--------|---------|
| New endpoint: GET /portfolio/sector-regime-trend | Weekly-bucketed sector concentration + regime status trend (BLG-FEAT-67), backed by a new `sector_regime_history` table (going-forward capture only — no prior historical sector/regime data existed to aggregate). |

**Note (this entry):** the remaining 5 releases in the backfilled `v7.9`–`v8.4` window — `v7.10`, `v8.0`, `v8.1`, `v8.3`, `v8.4` — shipped no new endpoints (confirmed via a full scan of every contract file's own Changelog table for entries dated within each release's ship window; all changes in that period were field additions to existing endpoints, response-example corrections, or documentation backfill of already-shipped-but-undocumented routes — e.g. `v8.4`'s `GET /test/quick-health`/`POST /test/rate-limit-scenarios`, which `health_endpoints.md`'s own changelog states "both routes existed in `backend/routers/test.py` but were undocumented," not newly shipped). No entries added for those 5 releases — an empty release is not silently missing, it is confirmed empty.

## v7.8.0 (2026-07-27 — Release v7.8)

### changelog_endpoints.md — v1.0 (NEW)

**EPIC:** EPIC-01
**ST:** ST-01

| Change | Details |
|--------|---------|
| New endpoint: GET /changelog/latest | Returns the most recent release's version label and changes-shipped descriptions, parsed server-side from docs/product/changelog.md. Backs the in-app "What's New" panel (dashboard.md §6A). `data` is null if no parseable version section exists. |

### reports_endpoints.md — v0.10 (UPDATED)

**EPIC:** EPIC-05
**ST:** ST-05

| Change | Details |
|--------|---------|
| New query param: GET /reports/monthly-pnl?format=csv | Returns a CSV file download of the month rows (Year, Month, Realised P&L (GBP), Trades) instead of JSON — mirrors the existing GET /reports/tax-year?format=csv handler. Invalid format values return 400. |

### ai_endpoints.md — v1.8 (UPDATED)

**EPIC:** EPIC-06
**ST:** ST-06

| Change | Details |
|--------|---------|
| New endpoint: GET /ai/spend-trend | Returns Claude API spend for the last 6 release cycles, oldest to newest, bucketed by date windows parsed from docs/product/changelog.md version headings. Sourced from existing claude_audit_log data. |

## v6.1.0 (2026-06-23 — Release v6.1)

### portfolio_endpoints.md — v2.4.0 (UPDATED)

**EPIC:** EPIC-03
**ST:** ST-06

| Change | Details |
|--------|---------|
| New endpoint: GET /portfolio/sector-weights | Returns open-position sector breakdown by market value: sectors array (sector_name, position_count, exposure_pct), total_positions, concentration_alert (true when ≥40% in single sector). Positions without sector field grouped as "Unclassified". Silent graceful degradation on error. |

### trade_plan_endpoints.md — v0.5 (UPDATED)

**EPIC:** EPIC-04
**ST:** ST-08

| Change | Details |
|--------|---------|
| New endpoint: GET /trade-plans/setup-quality-score | Returns 0-100 setup quality score from closed trade history. Gate: returns gate_not_met=true when <20 closed trades. Score = clamp(win_rate×0.6 + max(avg_pnl_pct,0)×0.4, 0, 100). Response includes: score, matching_trades, win_rate, average_pnl_pct, score_explanation. |

**Sign-off:** Sprint Execution Engine (autonomous class) — 2026-06-23

---

## v2.9.0 (2026-04-23 — Release v2.9)

### alpaca_integration_contract.md — v1.0 (NEW)

**EPIC:** EPIC-01 (Arc 1 Specification Foundation)
**ST:** ST-02 (BLG-SPEC-22)

| Change | Details |
|--------|---------|
| New contract: Alpaca Markets API integration | External API contract for Alpaca Data API v2. Documents GET /v2/stocks/{symbol}/bars (OHLCV bars, DS-05) and GET /v1beta1/news (news headlines, DS-06). Includes rate limits, error codes, retry strategy, and explicit fallback strategy (Yahoo Finance for OHLCV; empty panel for news). US tickers only. API version pinned. |

**Sign-off:** Sprint Execution Engine (autonomous class) — 2026-04-23

---

### screener_api_contract.md — v1.0 (NEW)

**EPIC:** EPIC-01 (Arc 1 Specification Foundation)
**ST:** ST-03 (BLG-SPEC-23)

| Change | Details |
|--------|---------|
| New endpoint: GET /screener/results | Returns screener result records from the latest (or specified) completed screener run. Offset-based pagination. Filter by market. Results ordered by signal_score descending. |
| New endpoint: POST /screener/run | Triggers an async screener run. Returns run_id (UUID) immediately. Results retrievable via GET /screener/results?run_id={run_id}. Returns 409 if a run is already in progress. |

**Sign-off:** Sprint Execution Engine (autonomous class) — 2026-04-23

---

## v2.1.2 (2026-03-20 — Release v2.1)

### trade_endpoints.md — v2.1.0

**EPIC:** EPIC-05 (Financial Reporting Exports & Enhancements)
**ST:** ST-14

| Change | Details |
|--------|---------|
| New field: `fill_price` per trade | Actual fill price in native currency. `null` for trades entered before v2.1 (Fill Price capture not yet active). Source: `positions.fill_price`. |
| New field: `slippage_pct` per trade | Computed server-side: `(fill_price − entry_price) / entry_price * 100`. Negative = favourable (filled below market). Positive = unfavourable. `null` when `fill_price` is `null`. Rounded to 2dp. |
| New field: `avg_slippage_pct` (top-level) | Portfolio average slippage across all trades with `fill_price` recorded. `null` when no trades have `fill_price`. |
| Data model gate | `fill_price` was pre-existing in `data_model.md` v1.2 (`positions` table, nullable `DECIMAL(10,4)`). Gate cleared: Data Model & Domain Schema Owner + Head of Specs Team countersigned 2026-03-20. |

**Sign-off:** Data Model & Domain Schema Owner + Head of Specs Team (gate) — 2026-03-20

---


## v2.1.1 (2026-03-20 — Release v2.1)

### reports_endpoints.md — v0.3

**EPIC:** EPIC-05 (Financial Reporting Exports & Enhancements)
**ST:** ST-13

| Change | Details |
|--------|---------|
| New format: `GET /reports/tax-year?format=csv` | CSV download of tax-year P&L report. `Content-Type: text/csv`. `Content-Disposition: attachment; filename="tax-year-{year}-pnl.csv"`. |
| CSV structure | 5-row metadata block (Tax Year, Generated At, Total Realised P&L, Total Closed Trades, Win Rate %), blank row, 17-column trades table with human-readable headers. |
| Column headers | Trade ID, Ticker, Market, Entry Date, Exit Date, Holding Days, Entry Price (Native), Exit Price (Native), Entry FX Rate (GBP/USD), Exit FX Rate (GBP/USD), Shares, Total Cost (GBP), Exit Proceeds (GBP), Realised P&L (GBP), P&L %, Currency, Tags. |
| `format` validation tightened | Unknown `format` values now return `400 — "format must be one of: pdf, csv"`. Previously unspecified. |
| No schema migration | Pure format conversion of existing endpoint data. |

**Sign-off:** Head of Engineering (implementation) — 2026-03-20

---

## v2.1.0 (2026-03-20 — Release v2.1)

### alerts_endpoints.md — v0.1 (new file)

**EPIC:** EPIC-02 (Alerts & Notifications)
**ST:** ST-02
**ADR:** ADR-003 (FastAPI BackgroundTasks delivery architecture)

| Change | Details |
|--------|---------|
| New endpoint: `GET /alerts/rules` | List alert rules for portfolio. Seeds 4 defaults on first call. Returns array with `id`, `type`, `enabled`, `threshold_percent`. |
| New endpoint: `POST /alerts/rules` | Create alert rule (used to restore after deletion). Returns `400` if type already exists. |
| New endpoint: `PATCH /alerts/rules/{rule_id}` | Update rule `enabled` or `threshold_percent`. |
| New endpoint: `DELETE /alerts/rules/{rule_id}` | Delete alert rule. Standard DELETE envelope. |
| New endpoint: `POST /alerts/evaluate` | Evaluate all enabled rules against current portfolio state. Enqueues email delivery as FastAPI BackgroundTask. Returns `notifications_created`, `delivery_tasks_enqueued`, `redelivery_tasks_enqueued`. |
| New endpoint: `GET /notifications` | Notification feed, newest first. Page-based pagination (50/page). Returns `notifications[]`, `total`, `page`, `per_page`, `has_more`. |
| New endpoint: `PATCH /notifications/{id}` | Mark one notification as read. Idempotent. |
| New endpoint: `POST /notifications/mark-all-read` | Mark all unread as read. Returns `marked_read_count`. |
| New endpoint: `GET /notifications/preferences` | Per-type email preferences. Seeds defaults on first call. |
| New endpoint: `PATCH /notifications/preferences` | Update preferences for one or more alert types. Map body: `{ alert_type_key: { email_enabled: bool } }`. |
| Architecture | Delivery via FastAPI `BackgroundTasks` — no Redis/Celery. Retry: re-enqueue on next evaluation if `delivered = false` and `delivery_attempts < 3`. |

**Data model:** `data_model.md` v1.9 — 3 new tables: `alert_rules`, `notifications` (with delivery tracking), `notification_preferences`.

**Sign-off:** Head of Specs Team — 2026-03-20

---


## v2.0.0 (2026-03-17 — Release v2.0)

### reports_endpoints.md — v0.1 (new file)

**EPIC:** EPIC-02 (4.1b Tax-Year P&L)
**ST:** ST-03

| Change | Details |
|--------|---------|
| New endpoint: `GET /reports/tax-year` | Tax-year P&L statement for UK tax years. Attribution by `exit_date`. `year` query parameter = start year of UK tax year (e.g. `year=2025` = 6 Apr 2025 to 5 Apr 2026). |
| Response shape | Top-level: `tax_year_start`, `tax_year_end`, `tax_year_label`, `generated_at`. Summary: `total_realised_pnl`, `total_gross_profit`, `total_gross_loss`, `win_count`, `loss_count`, `win_rate`, `estimated_unrealised_pnl`, `unrealised_note`. Trades array: full per-trade breakdown including FX rates, GBP costs/proceeds, tags. |
| Validation | Future year returns 400. Absent or non-integer `year` returns 400. Empty tax year returns 200 with zero summary and empty trades array. |
| Scope | UK-based accounts only (6 April to 5 April boundary). Not a substitute for qualified tax advice. |

**Sign-off:** Head of Specs Team + Financial Reporting & Records Owner — 2026-03-17

---

## Purpose

This document is the running changelog for all API contract versions. It must be updated alongside every contract version bump.

**Maintenance obligation:** Whenever an `*_endpoints.md` contract file is incremented (major or minor version), a corresponding entry must be added here. This document is the single place to trace what changed between API versions.

---

## v1.9.0 (2026-03-05 — Release v1.8)

### analytics_endpoints.md — v1.9.0

**EPIC:** EPIC-06 (Release v1.7) — Spec Debt
**ST:** ST-06 (v1.7)

| Change | Details |
|--------|---------|
| Added `sharpe_ratio_trade_method` as 14th validated metric | `POST /validate/calculations` now validates 14 metrics total. `sharpe_ratio_trade_method` is severity `critical`. The method field on the Sharpe result distinguishes `portfolio`, `trade`, or `insufficient_data` calculation paths. |
| Total metric count | `summary.total: 14` (was 13). Severity distribution: critical: 4, high: 3, medium: 6, low: 1. |

### portfolio_endpoints.md — v1.9.0

**EPIC:** EPIC-06 (Release v1.7) — Spec Debt
**ST:** ST-07 (v1.7)

| Change | Details |
|--------|---------|
| Spec corrected to match live API | Position summary objects in `GET /portfolio` confirmed to include: `current_value`, `current_stop`, `pnl_pct`, `fx_rate`, `live_fx_rate`. Field `pnl_pct` is the canonical field name for position P&L percentage (not `pnl_percent` — that appears in trade history only for backward compatibility). |

### trade_endpoints.md — v1.9.0

**EPIC:** EPIC-06 (Release v1.7) — Spec Debt
**ST:** ST-08 (v1.7)

| Change | Details |
|--------|---------|
| Added `holding_days` to changelog | `GET /trades` trade objects include `holding_days` (integer, calendar days from `entry_date` to `exit_date` inclusive). Field was present in the implementation and added to the spec changelog. |

---

## v1.9.0 — settings_endpoints.md (2026-03-05 — Release v1.8)

**EPIC:** EPIC-03 (Release v1.8) — API & Spec Debt
**ST:** ST-09 (v1.8)

| Change | Details |
|--------|---------|
| Replaced `PUT /settings` with `PATCH /settings/{settings_id}` and `POST /settings` | The live backend implementation uses `PATCH /settings/{settings_id}` for updating an existing settings record and `POST /settings` for creating a new one. The spec previously documented `PUT /settings` which was never the live behaviour. ESC-20260304-01 option (a) — spec updated to follow implementation. |
| Added lifecycle header | `settings_endpoints.md` now has a canonical lifecycle header. Version incremented to 1.1.0. |

---

## v1.8.1 (prior to Release v1.8)

### openapi.yaml — v1.8.1

**EPIC:** BLG-TECH-02 (pre-v1.8 technical debt)

| Change | Details |
|--------|---------|
| Added severity model to ValidationResponse | Each `POST /validate/calculations` result now includes a `severity` field (critical \| high \| medium \| low). Summary includes `by_severity` breakdown. |

---

## v1.8.0 (Release v1.7 — prior history)

### settings_endpoints.md — v1.8.0 (approximate)

| Change | Details |
|--------|---------|
| Added `default_risk_percent` field | `GET /settings` response includes `default_risk_percent` (float, > 0, ≤ 100). Used to pre-populate the Position Sizing Calculator widget. Default: `1.00`. |

---

## Maintenance Notes

- This changelog covers contract versions from v1.8.0 onward. Earlier history was not captured in this document.
- For pre-v1.8.0 changes, refer to individual `*_endpoints.md` file history.
- All future API contract version bumps must include an entry here before the PR is merged.

---

## Change Log (this document)

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-03-05 | Initial version. Backfilled v1.9.0 changes from EPIC-06 (v1.7) and EPIC-03 (v1.8). ST-12, S2-08. |
