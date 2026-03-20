**Owner:** API Contracts & Documentation Owner
**Class:** Class 2
**Status:** Canonical
**Version:** 1.2.0
**Last Updated:** 2026-03-18
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# API Changelog

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
