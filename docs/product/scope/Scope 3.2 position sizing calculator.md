# Scope Document — Position Sizing Calculator

**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-02-20
**Roadmap item:** 3.2
**Target release:** v1.6

> ⚠️ **Standing Notice:** This document describes delivery intent and summarises canonical spec decisions for the purposes of implementation. All authoritative rules, formulas, field definitions, and constraints live in the canonical specifications listed in Section 2. In any conflict between this document and those specs, the canonical specs prevail. This document must not be cited as canonical intent.

> **Verification status (updated 2026-02-20):** Implementation verified. Director of Quality sign-off granted 2026-02-19 (v1.1) and re-verification pass signed off 2026-02-20 (v1.2). Shipping closure pending resolution of DEF-006 (Low — Risk % session persistence) and execution of F15 (deferred — database access constraint). Full verification record: `docs/product/verification/3.2-position-sizing-calculator-verification.md`.

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

Full spec in `position_form.md §Position Sizing Calculator`. Key rules:

- Always visible — no toggle, no activation required
- Risk % pre-populated from `settings.default_risk_percent` on form load
- Recalculates 300ms after user stops typing in Entry Price, Stop Price, FX Rate, or Risk %
- Auto-fills Shares when `valid: true` and `cash_sufficient: true` and Shares field is empty
- Does not overwrite Shares if user has manually entered a value — shows "Use suggested shares" button instead
- Does not auto-fill when `cash_sufficient: false` — shows `max_affordable_shares` as informational text only
- Does not block form submission in any state
- On network failure: shows `—`, no error message, retries on next keystroke
- After successful form submission: resets to idle; Risk % retains last-used value (not reset to settings default)

---

## 7. Settings Change

`default_risk_percent` is a new field on the `settings` table and the Settings page.

- Type: `DECIMAL(4,2)`, constraint `> 0 AND <= 100`, default `1.00`
- Migration is safe: `NOT NULL DEFAULT 1.00` — existing rows receive `1.00` automatically, no backfill needed
- On the Settings page it sits in the Strategy Parameters section with helper text: *"Pre-filled in the Position Sizing Calculator on trade entry. This is your default — you can override it per trade."*
- It is a user preference, not an enforced limit. The widget allows any valid risk % to be typed per trade.

---

## 8. Acceptance Criteria

Derived from `portfolio_endpoints.md` and `position_form.md` per QA review (A10, 2026-02-19).

**Backend — `POST /portfolio/size`**

- Given valid inputs with `stop_price < entry_price` and sufficient cash: returns `valid: true`, `cash_sufficient: true`, `suggested_shares` floored to 4dp, all output fields present
- Given valid inputs with `stop_price < entry_price` and insufficient cash: returns `valid: true`, `cash_sufficient: false`, `max_affordable_shares` present and populated
- Given `risk_percent = 0`: returns `valid: false`, `reason: INVALID_RISK_PERCENT`
- Given `stop_price >= entry_price`: returns `valid: false`, `reason: INVALID_STOP_DISTANCE`
- Given `entry_price = 0`: returns `valid: false`, `reason: INVALID_ENTRY_PRICE`
- Given `stop_price = 0`: returns `valid: false`, `reason: INVALID_STOP_PRICE`
- Given no portfolio history snapshot exists: returns `valid: false`, `reason: NO_PORTFOLIO_VALUE_SNAPSHOT`
- Missing required field (`entry_price`, `stop_price`, or `risk_percent`): returns HTTP 400
- Invalid `market` value: returns HTTP 400
- `fx_rate_used` is `1.0` for UK positions and the applied rate for US positions
- No state mutation — portfolio cash, positions, and history rows are unchanged after any call

**Backend — `default_risk_percent` settings field**

- `GET /settings` response includes `default_risk_percent`
- `PUT /settings` with `default_risk_percent: 0` returns HTTP 422
- `PUT /settings` with `default_risk_percent: -1` returns HTTP 422
- `PUT /settings` with `default_risk_percent: 101` returns HTTP 422
- `PUT /settings` with a valid value persists and is returned on subsequent `GET`

**Frontend — Widget**

- Widget is visible on Trade Entry form load without any user action
- Risk % field pre-populates from `settings.default_risk_percent`
- No API call is made when Entry Price or Stop Price is empty
- Loading state is shown during debounce and API round-trip
- When Shares is empty and result is valid with sufficient cash: Shares auto-fills
- When Shares already has a value: "Use suggested shares" button appears; clicking it fills Shares
- `INVALID_STOP_DISTANCE` → amber message "Stop price must be below entry price"
- `INVALID_RISK_PERCENT` → amber message "Risk % must be greater than zero"
- `INVALID_ENTRY_PRICE` → amber message "Enter a valid entry price above zero"
- `INVALID_STOP_PRICE` → amber message "Enter a valid stop price above zero"
- `cash_sufficient: false` → muted grey informational display with `max_affordable_shares`
- `NO_PORTFOLIO_VALUE_SNAPSHOT` → muted grey message
- Network failure → dashes shown, form remains submittable
- Form submits regardless of widget state
- Post-submit: widget resets; Risk % retains last-used session value

**Frontend — Settings page**

- `default_risk_percent` field present in Strategy Parameters section
- Saving `0` is rejected with a visible error message
- Saving a negative value is rejected with a visible error message
- Saving a valid value persists and pre-populates widget on next Trade Entry load

---

## 9. Effort Estimate

**2–3 days.** Revised from the original roadmap estimate of 1–2 days to account for the expanded scope confirmed during pre-alignment (migration, settings endpoint update, settings page UI update, and spec updates across four documents — all now complete).

The canonical specs are locked. The pre-implementation spec phase is done. Engineering is clear to begin.

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
