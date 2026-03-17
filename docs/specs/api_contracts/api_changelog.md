**Owner:** API Contracts & Documentation Owner
**Status:** Canonical
**Version:** 1.1.0
**Last Updated:** 2026-03-17

# API Changelog

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
