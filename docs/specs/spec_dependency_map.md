# Spec Dependency Map

**Owner:** Head of Specs Team
**Class:** Class 2 Supporting Reference
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-15
**Lifecycle Guide:** `claude/charter/document_lifecycle_guide.md`

> **Point-in-time reference — last updated 2026-04-15.**
> Accuracy is not guaranteed after spec creation or revision without a manual update of this document.
> When a canonical spec is added or materially revised, the author should check whether this map requires an update.
> In case of conflict between this map and the referenced specs themselves, the referenced specs prevail.

---

## Purpose

This document maps the known cross-spec dependencies across all canonical and supporting specifications in the system. It answers:

- "If I change spec X, which other specs may be affected?"
- "Before I can safely modify spec Y, which upstream specs must I understand?"
- "Which spec is the authority for a given concept?"

This map supplements but does not supersede `docs/specs/Specs_Index.md`, which is the authoritative conflict-resolution document.

---

## How to Read This Map

Each section lists a canonical or supporting spec, identifies what it **depends on** (upstream), and what **depends on it** (downstream / consumers).

**Dependency types used:**

| Symbol | Meaning |
|--------|---------|
| `→ [spec]` | This spec references [spec] for canonical definitions |
| `← [spec]` | [spec] references this spec |
| `∅` | No known cross-spec dependencies |

---

## Tier 1 — Foundation Specs (no upstream dependencies)

These specs define canonical rules that others reference but do not themselves depend on other product specs.

### `claude/strategy/strategy_rules.md`

**Domain:** Strategy & Risk
**Owner:** Strategy Rules & System Intent Owner
**Depends on:** ∅ (governance source — top of hierarchy)
**Consumed by:**
- `docs/specs/api_contracts/portfolio_endpoints.md` → §4.1 position sizing rules, §4.1.4 validity rules
- `docs/specs/api_contracts/position_endpoints.md` → stop calculation rules, risk percent rules
- `docs/specs/api_contracts/conventions.md` → stop rules referenced in multi-currency section
- `docs/specs/api_contracts/market_endpoints.md` → market regime interpretation

**Change impact:** Any change to `strategy_rules.md` may invalidate documented validation rules, business logic descriptions, and acceptance criteria in all four consumers listed above.

---

### `docs/specs/data_model.md`

**Domain:** Data Model & Domain Schema
**Owner:** Data Model & Domain Schema Owner
**Depends on:** ∅
**Consumed by:**
- `docs/specs/api_contracts/signal_endpoints.md` → §7 signals table schema (UNIQUE constraint, field semantics)
- `docs/specs/api_contracts/trade_endpoints.md` → `trade_reflections` table schema (§7, data_model v1.8)
- `docs/specs/api_contracts/position_endpoints.md` → position field meanings, currency semantics
- `docs/specs/api_contracts/portfolio_endpoints.md` → portfolio field meanings, drawdown calculation
- `docs/specs/data_model/settings_model.md` → supplementary (settings field definitions extend data_model)

**Change impact:** Schema changes in `data_model.md` (column renames, type changes, new constraints) require review of all consumer endpoint specs and potential migration scripts.

---

### `docs/specs/metrics_definitions.md`

**Domain:** Metrics & Analytics
**Owner:** Metrics Definitions & Analytics Canonical Owner
**Depends on:** ∅
**Consumed by:**
- `docs/specs/api_contracts/analytics_endpoints.md` → Sharpe, drawdown, profit factor, cohort metrics formulas
- `docs/specs/api_contracts/portfolio_endpoints.md` → current_drawdown_percent canonical formula
- `docs/specs/api_contracts/reports_endpoints.md` → tax-year P&L calculation methodology

**Change impact:** Formula changes in `metrics_definitions.md` require immediate review of all three consumers — any changed formula may produce different numeric results in existing API responses.

---

### `docs/specs/api_contracts/conventions.md`

**Domain:** API Contracts
**Owner:** API Contracts & Documentation Owner
**Depends on:** `strategy_rules.md` (stop rules in multi-currency section)
**Consumed by:** All `*_endpoints.md` files in `docs/specs/api_contracts/`

**Note:** Every endpoint spec declares: *"Global response envelopes, error shape, defaults, and conventions are defined in **conventions.md** and apply unless explicitly stated otherwise."* This is the broadest dependency in the system — a breaking change to `conventions.md` affects every endpoint contract.

**Change impact:** Changes to the standard success/error envelope, idempotency semantics, HTTP status codes, or §13 Error Response Standard affect all endpoint specs simultaneously. Changes to `conventions.md` must trigger a full review sweep of all `*_endpoints.md` files.

---

## Tier 2 — Domain Specs (depend on Tier 1)

### `docs/specs/api_contracts/analytics_endpoints.md`

**Version:** 2.1.0 (last updated 2026-04-15)
**Depends on:**
- `conventions.md` → standard envelope, error shapes
- `metrics_definitions.md` → cohort metrics formulas (§Cohort Metrics), R-multiple formula, Sharpe, drawdown
**Consumed by:**
- `docs/specs/api_contracts/digest_endpoints.md` → metrics data used in weekly digest (metrics staleness, analytics summary)

---

### `docs/specs/api_contracts/position_endpoints.md`

**Depends on:**
- `conventions.md` → standard envelope, multi-currency/stop rules
- `data_model.md` → position field semantics, stop calculation, currency fields
- `strategy_rules.md` → risk percent rules, stop distance rules
**Consumed by:**
- `docs/specs/api_contracts/portfolio_endpoints.md` → prospective heat calculation references position sizing
- `docs/specs/api_contracts/trade_endpoints.md` → trade closure affects position lifecycle
- `docs/specs/api_contracts/cash_endpoints.md` → position entry consumes allocated cash
- `docs/specs/api_contracts/signal_endpoints.md` → `position_id` set on signal when `status = 'entered'`

---

### `docs/specs/api_contracts/portfolio_endpoints.md`

**Depends on:**
- `conventions.md` → standard envelope, multi-currency rules
- `metrics_definitions.md` → current_drawdown_percent formula
- `strategy_rules.md` → §4.1 position sizing rules, §4.1.4 validity rules
**Consumed by:**
- `docs/specs/api_contracts/cash_endpoints.md` → available_cash sourced from portfolio summary
- `docs/specs/api_contracts/analytics_endpoints.md` → portfolio value used in analytics calculations

---

### `docs/specs/api_contracts/signal_endpoints.md`

**Version:** 1.1 (last updated 2026-04-15)
**Depends on:**
- `conventions.md` → standard envelope, error shapes
- `data_model.md` → §7 signals table schema (UNIQUE constraint, `position_id`, `suggested_shares` semantics)
- `position_endpoints.md` → `position_id` link when signal `status = 'entered'`
**Consumed by:** ∅ (no known downstream spec consumers)

---

### `docs/specs/api_contracts/trade_endpoints.md`

**Depends on:**
- `conventions.md` → standard envelope, error shapes
- `data_model.md` → `trade_reflections` table schema (v1.8)
- `position_endpoints.md` → trade closing a position updates position lifecycle
**Consumed by:**
- `docs/specs/api_contracts/analytics_endpoints.md` → trade history used in R-multiple distribution, cohort analysis

---

### `docs/specs/api_contracts/cash_endpoints.md`

**Depends on:**
- `conventions.md` → standard envelope
- `portfolio_endpoints.md` → available_cash definition
- `position_endpoints.md` → position entry/exit affects cash balance
**Consumed by:**
- `docs/specs/api_contracts/signal_endpoints.md` → `available_cash` included in signal generation response

---

### `docs/specs/api_contracts/alerts_endpoints.md`

**Version:** 0.3 (last updated 2026-03-24)
**Depends on:**
- `conventions.md` → standard envelope, error shapes
**Consumed by:**
- `docs/specs/api_contracts/digest_endpoints.md` → alert activity included in weekly digest

---

### `docs/specs/api_contracts/reports_endpoints.md`

**Depends on:**
- `conventions.md` → standard envelope
- `metrics_definitions.md` → tax-year P&L calculation methodology
**Consumed by:** ∅

---

### `docs/specs/api_contracts/settings_endpoints.md`

**Depends on:**
- `conventions.md` → standard envelope
- `docs/specs/data_model/settings_model.md` → canonical field definitions, validation rules, defaults
**Consumed by:**
- `docs/specs/api_contracts/portfolio_endpoints.md` → `default_risk_percent` used for position sizing pre-population

---

### `docs/specs/api_contracts/digest_endpoints.md`

**Version:** 0.1 (created 2026-04-03)
**Depends on:**
- `conventions.md` → standard envelope
- `analytics_endpoints.md` → metrics staleness (4h threshold, `last_sync_at`)
- `alerts_endpoints.md` → alert activity summary in digest
**Consumed by:** ∅

---

### `docs/specs/api_contracts/health_endpoints.md`

**Version:** 1.2 (last updated 2026-03-30)
**Depends on:**
- `conventions.md` → standard envelope
**Consumed by:** ∅

---

### `docs/specs/api_contracts/market_endpoints.md`

**Version:** 0.1 (created 2026-03-08)
**Depends on:**
- `conventions.md` → standard envelope
- `strategy_rules.md` → market regime interpretation (SPY/FTSE risk-on thresholds)
**Consumed by:**
- `docs/specs/api_contracts/signal_endpoints.md` → market regime included in signal generation response

---

---

## Tier 3 — Supporting and Reference Specs

### `docs/reference/openapi.yaml`

**Class:** Supporting Reference only (must not diverge from canonical contracts)
**Depends on:** All `*_endpoints.md` files (is derived from / must track all of them)
**Consumed by:** Frontend (API client generation), CI/CD (OpenAPI drift detection gate)

**Note:** `openapi.yaml` is not canonical. Any conflict between `openapi.yaml` and a canonical `*_endpoints.md` is resolved in favour of the Markdown contract.

---

### `docs/specs/data_model/settings_model.md`

**Class:** Class 1 Canonical, v0.1 (created 2026-03-08)
**Depends on:** `data_model.md` (extends the general data model for settings domain)
**Consumed by:** `settings_endpoints.md`

---

### `docs/specs/structured_logging_standards.md`

**Class:** Class 1 Canonical, v0.1.0 (created 2026-03-02)
**Depends on:** ∅
**Consumed by:** `docs/specs/api_contracts/backend_engineering_patterns.md`

---

### `docs/specs/api_contracts/backend_engineering_patterns.md`

**Depends on:**
- `structured_logging_standards.md` → logging format and level standards
- `conventions.md` → API error patterns
**Consumed by:** (advisory — no mandatory downstream consumers; guides backend implementation practice)

---

### `docs/specs/spec_coverage_inventory.md`

**Class:** Class 3 QA/Operations
**Depends on:** All `*_endpoints.md` files (tracks coverage status per endpoint)
**Consumed by:** (informational)

---

### `docs/specs/api_contracts/api_changelog.md`

**Class:** Running changelog
**Depends on:** All `*_endpoints.md` files (records version increments)
**Consumed by:** (informational)

---

### `docs/reference/glossary.md`

**Class:** Class 2 Supporting Reference, v1.1
**Depends on:** (language only — no behavioral dependencies)
**Consumed by:** (informational — terms should align with all domain specs)

---

## Frontend Spec Dependencies

### `docs/specs/frontend/design_system.md`

**Depends on:** ∅ (base frontend spec)
**Consumed by:** All `docs/specs/frontend/pages/` and `docs/specs/frontend/components/` specs

---

### `docs/specs/frontend/settings_model.md` (frontend view)

**Depends on:** `docs/specs/data_model/settings_model.md` → canonical field definitions
**Consumed by:** Settings page and component specs

---

### `docs/specs/frontend/pages/` and `docs/specs/frontend/components/`

**Depends on:**
- `docs/specs/frontend/design_system.md` → visual and interaction standards
- Relevant `*_endpoints.md` → API contracts for data fetched/submitted
**Consumed by:** (implementation — no downstream specs)

---

## Summary Dependency Graph (High-Level)

```
strategy_rules.md
    ↓ (risk rules)
    ↓──────────────────────────────────────┐
data_model.md                              │
    ↓ (schema)                             │
metrics_definitions.md                     │
    ↓ (formulas)                           │
                                           ↓
conventions.md ──── (envelope) ──→ All *_endpoints.md files
                                           │
                    analytics_endpoints.md ←── metrics_definitions.md
                    portfolio_endpoints.md ←── metrics_definitions.md + strategy_rules.md
                    position_endpoints.md  ←── data_model.md + strategy_rules.md
                    trade_endpoints.md     ←── data_model.md + position_endpoints.md
                    signal_endpoints.md    ←── data_model.md + position_endpoints.md
                    cash_endpoints.md      ←── portfolio_endpoints.md + position_endpoints.md
                    alerts_endpoints.md    ←── (self-contained beyond conventions)
                    digest_endpoints.md    ←── analytics_endpoints.md + alerts_endpoints.md
                    reports_endpoints.md   ←── metrics_definitions.md
                    settings_endpoints.md  ←── settings_model.md
                    health_endpoints.md    ←── (self-contained beyond conventions)
                    market_endpoints.md    ←── strategy_rules.md
                                           │
                                           ↓
                    openapi.yaml ←── (derived from all *_endpoints.md — supporting reference only)
```

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-15 | Initial version (ST-10, BLG-SPEC-D17, v2.7). All known cross-spec dependencies captured at time of authoring. Head of Specs Team sign-off in qa_evidence_EPIC-05.md. |
