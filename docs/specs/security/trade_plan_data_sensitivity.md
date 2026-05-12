**Owner:** Cybersecurity & Trust Lead
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-10
**Story:** ST-12 (EPIC-03, v3.3) — BLG-SEC-06
**Sign-off:** Cybersecurity & Trust Lead: Accepted — 2026-05-10 (agent-mediated, v3.3 design gate)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Trade Plan Data Sensitivity Classification

This document classifies all fields in the `trade_plans` table by sensitivity level and specifies access control principles per level. Referenced by Arc 3/4 features that expose trade plan data.

---

## 1. Field Classification

### 1.1 Public Fields

Fields that are safe to expose in any authenticated API response, search results, or aggregated displays.

| Field | Classification | Rationale |
|-------|---------------|-----------|
| `id` | Public | UUID — no information leakage |
| `ticker` | Public | Ticker symbol is public market data |
| `market` | Public | `US`/`UK` market designation — non-sensitive |
| `status` | Public | Plan status (`draft`, `active`, `closed`, `abandoned`) — display metadata only |
| `created_at` | Public | Creation timestamp — metadata |
| `updated_at` | Public | Update timestamp — metadata |

### 1.2 Internal Fields

Fields containing operational metadata that should be returned only to authenticated users with portfolio access but are not considered sensitive trading IP.

| Field | Classification | Rationale |
|-------|---------------|-----------|
| `position_id` | Internal | FK to position — portfolio reference; not sensitive in isolation |
| `portfolio_id` | Internal | FK to portfolio — must be scoped per authenticated user |
| `checklist_completed` | Internal | Operational status flag |
| `checklist_items` | Internal | Array of checklist booleans — operational state, not trading strategy |

### 1.3 Private Fields

Fields that contain the trader's proprietary strategy, entry logic, and risk management parameters. These represent the trader's intellectual property and must not be exposed in any non-scoped context.

| Field | Classification | Rationale |
|-------|---------------|-----------|
| `setup_thesis` | Private | Trading thesis — proprietary strategy IP |
| `entry_rationale` | Private | Entry logic — proprietary |
| `r_target` | Private | Target R-multiple — position sizing strategy |
| `early_exit_conditions` | Private | Exit logic — proprietary risk management |
| `confirmation_criteria` | Private | Entry confirmation criteria — proprietary |
| `regime_context_at_entry` | Private | Market regime assessment at entry — strategy context |
| `stop_level` | Private | Stop price — active risk management parameter |
| `risk_reward_notes` | Private | R/R assessment — proprietary |
| `abandonment_reason` | Private | Reason for abandoning plan — internal decision log |

---

## 2. Access Control Principles

### 2.1 Authentication Boundary

All trade plan fields (including Public classification) require:
- Valid `X-API-Key` header (enforced by `api_key_middleware` in `backend/main.py`)
- Correct `portfolio_id` scoping (all queries filter by portfolio derived from the authenticated session)

There is no unauthenticated access to any trade plan data.

### 2.2 Per-Classification Access Rules

| Classification | Who may access | Conditions |
|---------------|----------------|-----------|
| Public | Any authenticated request | Portfolio scoping required |
| Internal | Authenticated portfolio owner only | Portfolio ID must match request context |
| Private | Authenticated portfolio owner only | Portfolio ID must match; never returned in aggregated/cross-portfolio views |

### 2.3 Arc 3/4 Feature Rules

When any Arc 3 or Arc 4 feature exposes trade plan data:

1. **Confirm portfolio scoping:** The trade plan's `portfolio_id` must match the requesting user's portfolio before any field is returned.
2. **Private field minimisation:** Only expose Private fields that are strictly necessary for the feature's function. Do not return full trade plan objects when a subset suffices.
3. **Grace period alert endpoint** (`GET /positions/grace-period-alerts`): may return `trade_plan_id`, `stop_level`, R-target from trade plan. All Private fields. Portfolio scoping is mandatory.
4. **Stop management endpoint** (`GET /positions/{id}/stop-trail`): may return `current_stop` (from position, not trade plan). If R is derived from trade plan `r_target`, portfolio scope must be verified.
5. **Research view trade plan panel**: returns full trade plan including Private fields to the authenticated user. Portfolio scoping enforced at `GET /trade-plans?ticker={ticker}`.

### 2.4 Logging

Private fields must not appear in application logs (print statements, exception tracebacks) in plain text. The existing `backend/main.py` pattern of printing position updates must not be extended to log trade plan private fields.

---

## 3. Data Model Reference

Source table: `docs/specs/data_model.md` §DS-04 (trade_plans table, v2.5+).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-05-10 | Initial creation — ST-12 (EPIC-03, v3.3). All trade_plans fields classified. Access control principles per level. Arc 3/4 feature rules. Cybersecurity & Trust Lead sign-off. |
