# Frontend Specification — Trade Reflection Template

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Canonical Specification (Class 1)
**Status:** Canonical
**Version:** 0.1
**Last Updated:** 2026-03-06
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Release:** v1.9
**EPIC:** EPIC-01
**Design Source:** docs/design/2026-03-06__release-v1.9/trade-reflection/ux_spec.md
**Confirmed by:** Head of Specs Team — 2026-03-06

---

## 1. Purpose

A structured post-trade reflection form presented when a position is closed. Pre-populated with trade record data. Prompts the user with five structured reflection questions to encourage disciplined learning.

**Design principles:**
- No AI; fully deterministic and testable
- Submission is optional — skip at any time
- Reflection data is stored server-side, linked to the trade record

---

## 2. Trigger

The reflection modal opens automatically when a trade close is confirmed by the user (i.e., after the position exit is recorded server-side and the success response is received).

**Trigger location:** Trade close confirmation response — anywhere in the application where a position can be exited (Trade History, Risk Dashboard, Positions page).

---

## 3. Component Structure

**Type:** Modal overlay (not a separate page navigation)

**Route:** None — modal overlays the current page

---

## 4. Pre-Populated Trade Summary (Read-Only Section)

Displayed at the top of the modal. All fields are read-only, sourced from the trade close API response.

| Field | Source | Format |
|-------|--------|--------|
| Ticker | `trade.ticker` | String, bold |
| Entry Price | `trade.entry_price` | GBP, 2dp |
| Exit Price | `trade.exit_price` | GBP, 2dp |
| Hold Time | `trade.holding_days` | "N days" |
| R-Multiple | `trade.r_multiple` | Signed, 2dp, "R" suffix — from backend |
| Exit Reason | `trade.exit_reason` | STOP / MANUAL / REGIME |
| Exit State | `trade.exit_state` | GRACE / LOSING / PROFITABLE |
| Exit Date | `trade.exit_date` | ISO date, formatted DD Mon YYYY |

**Hard rule:** All 8 fields are backend-sourced. None are computed on the frontend. If a field is null (e.g., r_multiple not computable), display "–".

---

## 5. Reflection Questions (Editable Section)

Five structured fields presented below the trade summary. Each field is a textarea with a short prompt label.

| Field ID | Prompt label | Max length |
|----------|-------------|-----------|
| `trade_rationale` | "Why did you enter this trade? What was the setup?" | 500 chars |
| `what_worked` | "What did the trade do well? Was the setup validated?" | 500 chars |
| `what_didnt_work` | "What went wrong or was unexpected?" | 500 chars |
| `discipline_assessment` | "Did you follow your rules? Any impulse decisions?" | 500 chars |
| `key_takeaway` | "One lesson from this trade." | 500 chars |

All fields optional. Character count displayed beneath each textarea.

---

## 6. Actions

| Action | Behaviour |
|--------|-----------|
| Skip | Dismiss modal without saving. Trade close already complete. No reflection stored. |
| Save Reflection | POST reflection payload to backend. Close modal on success. Show success toast. |

**Submit behaviour:** Permitted with any subset of fields completed, including all empty. Backend stores whatever is provided.

---

## 7. API

**Endpoint:** `POST /trades/{trade_id}/reflection`

**Request body:**
```json
{
  "trade_rationale": "string | null",
  "what_worked": "string | null",
  "what_didnt_work": "string | null",
  "discipline_assessment": "string | null",
  "key_takeaway": "string | null"
}
```

**Response:** `200 OK` on success. On error: display inline error message; re-enable submit button.

This endpoint must be documented in `docs/specs/api_contracts/trade_endpoints.md` before implementation.

---

## 8. States

| State | Behaviour |
|-------|-----------|
| Modal open | Trade summary pre-populated (read-only); reflection fields empty |
| Saving | Submit button shows loading indicator; all fields and Skip disabled |
| Save error | Inline error message below submit button; fields and Skip re-enabled; user may retry or skip |
| Save success | Modal closes; brief toast notification "Reflection saved" (2 seconds) |

---

## 9. Accessibility

- Modal has a descriptive `aria-label`: "Trade Reflection — {ticker}"
- Focus trap within modal while open
- Skip button is always reachable by keyboard

---

## 10. Data Model Requirement

Reflection responses require a storage table linked to the trade record. The Data Model & Domain Schema Owner must define the `trade_reflections` schema in `docs/specs/data_model.md` before backend implementation. Minimum fields: `trade_id`, `trade_rationale`, `what_worked`, `what_didnt_work`, `discipline_assessment`, `key_takeaway`, `created_at`.

---

## 11. Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-03-06 | Initial spec — v1.9 EPIC-01 ST-02. |
