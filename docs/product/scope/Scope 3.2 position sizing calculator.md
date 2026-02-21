# Scope Document — Position Sizing Calculator

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Last Updated:** 2026-02-21
**Roadmap item:** 3.2
**Target release:** v1.6
**Superseded by:** `docs/product/changelog.md` — v1.6 entry (shipped 2026-02-20, Director of Quality sign-off)

> ⚠️ **Standing Notice:** This document describes delivery intent and summarises canonical spec decisions for the purposes of implementation. All authoritative rules, formulas, field definitions, and constraints live in the canonical specifications listed in Section 2. In any conflict between this document and those specs, the canonical specs prevail. This document must not be cited as canonical intent.

> **Lifecycle note:** This scope document is superseded. The feature shipped in v1.6 (Director of Quality sign-off 2026-02-20). Verification report: `docs/product/verification/3.2-position-sizing-calculator-verification.md` (v1.4). For the delivery record, see `docs/product/changelog.md` v1.6 entry. The canonical specifications listed in Section 2 remain authoritative and current.

---

## 1. What This Is

The Position Sizing Calculator is an always-visible widget embedded in the Trade Entry form. It calculates the suggested share quantity for a prospective position based on the user's risk percentage and the trade's stop distance. It auto-fills the Shares field when the result is valid and cash is sufficient. It is decision support — it does not block form submission in any state.

This is a daily-use feature. Every time the user enters a trade, the calculator is in front of them. The quality bar for this feature is therefore high: the widget must be fast, quiet, and correct.

---

## 2. Canonical Specifications (Implementation Source of Truth)

Engineering must implement against these documents. This scope document summarises; the specs govern.

| Spec | What it owns |
|------|--------------|
| `docs/specs/strategy_rules.md §4.1` (v1.3) | All calculation rules, validity conditions, rounding, FX handling, cash constraint logic |
| `docs/specs/api_contracts/portfolio_endpoints.md` (v1.8.0) | `POST /portfolio/size` — full request/response contract, all three response shapes, reason codes, error codes |
| `docs/specs/frontend/components/position_form.md` (v1.2) | Widget placement, all eight widget states, auto-fill behaviour, debounce, "Use suggested shares" affordance, form submission non-blocking rule, network failure behaviour, accessibility |
| `docs/specs/frontend/pages/settings.md` (v1.1) | `default_risk_percent` field in Strategy Parameters section — UI presentation, helper text, constraints |
| `docs/specs/api_contracts/settings_endpoints.md` (v1.8.0) | `default_risk_percent` field constraints for `GET /settings` and `PUT /settings` |
| `docs/specs/data_model.md` (v1.7) | `settings.default_risk_percent` — column definition, constraint, migration script |
| `docs/reference/openapi.yaml` (v1.8.0) | Supporting reference — `POST /portfolio/size` path, `SizePositionRequest`, `PositionSizeResponse` schemas |

---

## 3. Scope

### 3.1 In scope

**Backend**

- Implement `POST /portfolio/size` endpoint per `portfolio_endpoints.md`
- All calculation logic must be server-side and authoritative — no client-side calculation of sizing values
- Apply the migration script from `data_model.md §Migration v1.6 → v1.7` to add `default_risk_percent` to the `settings` table
- `GET /settings` and `PUT /settings` must expose and accept `default_risk_percent`

**Frontend**

- Implement the Position Sizing Calculator widget in the Trade Entry form per `position_form.md §Position Sizing Calculator`
- Read `settings.default_risk_percent` on form load to pre-populate the Risk % field
- Implement all eight widget states per spec (idle, loading, valid auto-fill, valid with existing shares, insufficient cash, invalid input, invalid system, post-submit reset)
- Add `default_risk_percent` field to the Settings page Strategy Parameters section per `settings.md`

### 3.2 Out of scope

- Any modification to stop logic, trailing stop behaviour, or exit rules
- Any modification to the position creation flow (`POST /portfolio/position`) — the widget feeds into the Shares field, but the form submission itself is unchanged
- Fractional share sizing in signal generation — signals remain whole-shares only; this is a separate flow
- Portfolio Heat Gauge integration — that is roadmap item 3.4 and depends on separate spec work

---

## 4. Calculation Summary

The canonical rules are in `strategy_rules.md §4.1`. For orientation:

```
RiskAmount      = PortfolioValue × RiskPercent
StopDistance    = EntryPrice − StopPrice
RawShares       = RiskAmount / StopDistance
SuggestedShares = floor(RawShares, 4dp)
EstimatedCost   = (SuggestedShares × EntryPrice) + EstimatedFees
```

`PortfolioValue` is `latest portfolio_history.total_value` — not available cash. Available cash is the feasibility gate, not the risk basis. This distinction is important.

All prices are in native currency (USD for US, GBP for UK). Portfolio value and cash are always GBP. FX conversion is required for US positions.

---

## 5. API Endpoint

`POST /portfolio/size` — full contract in `portfolio_endpoints.md`.

Three response shapes:

| Condition | `valid` | `cash_sufficient` | Key fields |
|-----------|---------|-------------------|------------|
| Valid, can afford | `true` | `true` | `suggested_shares`, `risk_amount`, `estimated_cost`, `available_cash`, `fx_rate_used` |
| Valid, cannot afford | `true` | `false` | All of the above + `max_affordable_shares` (always present) |
| Invalid inputs | `false` | — | `reason` (machine-readable code), `reason_detail` (log use only) |

Business rule failures (`INVALID_STOP_DISTANCE` etc.) return HTTP 200 with `valid: false`. Missing required fields return HTTP 400. The distinction matters for frontend error handling.

---

## 6. Widget Behaviour Summary

Full spec in `position_form.md §Position Sizing Calculator`.

Eight states: idle → loading → valid (auto-fill or with existing shares) → insufficient cash → invalid input → invalid system → post-submit reset.

The widget never blocks form submission.

---

## 7. Settings Page Change

`default_risk_percent` field added to Strategy Parameters section. Full spec in `settings.md`.

Helper text: "Pre-filled in the Position Sizing Calculator on trade entry. This is your default — you can override it per trade."

Constraint: > 0 and ≤ 100. Zero or negative values rejected with HTTP 400.

---

## 8. Acceptance Criteria

Full criteria in the verification report: `docs/product/verification/3.2-position-sizing-calculator-verification.md` (v1.4).

---

## 9. Effort Estimate

**2–3 days.** Revised from the original roadmap estimate of 1–2 days to account for the expanded scope confirmed during pre-alignment (migration, settings endpoint update, settings page UI update, and spec updates across four documents — all now complete).

---

## 10. Pre-Implementation Checklist

All items confirmed complete before this document was written:

- [x] Calculation rules canonical in `strategy_rules.md §4.1` (v1.3)
- [x] API contract authored in `portfolio_endpoints.md` (v1.8.0)
- [x] `openapi.yaml` updated (v1.8.0)
- [x] `data_model.md` updated with migration (v1.7)
- [x] `settings_endpoints.md` updated with `default_risk_percent`
- [x] `position_form.md` updated with full widget spec (v1.2)
- [x] `settings.md` updated with `default_risk_percent` field (v1.1)
- [x] `api_dependencies.md` updated with `POST /portfolio/size` (v1.1)
- [x] Roadmap updated with revised effort and scope note
- [x] Decisions record authored (`docs/product/decisions/3.2-position-sizing-calculator.md`)
- [x] QA review complete — acceptance criteria confirmed derivable (A10, 2026-02-19)

---

## 11. Out of Scope Confirmation

The following were explicitly considered and excluded:

| Item | Decision |
|------|----------|
| Toggle activation model | Rejected — Decision 3. Always visible. |
| Client-side sizing calculation | Rejected — backend is authoritative for all financial calculations |
| Blocking form submission on invalid widget state | Rejected — Decision 6. Widget is decision support, not a gate |
| Fractional shares in signal generation | Out of scope — separate flow, whole-shares only |
| Portfolio Heat Gauge integration | Deferred — roadmap 3.4, separate spec phase required |
| User-configurable risk limit (hard cap) | Out of scope — `default_risk_percent` is a preference default, not an enforced limit |