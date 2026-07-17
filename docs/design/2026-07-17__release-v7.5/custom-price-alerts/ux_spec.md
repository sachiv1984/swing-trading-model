**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-17
**Approved by:** Product Owner — 2026-07-17
**Story:** ST-02 — User-created price-alert data model, UI, and delivery integration (EPIC-02, BLG-FE-116)
**Depends on:** `docs/specs/blg_fe_116_pre_implementation_readiness_pass.md` — this artefact assumes that readiness pass's `price_alerts` schema, evaluation-pipeline integration, and §13 pre-check (PASS) as its technical baseline
**Cycle:** 2026-07-17__release-v7.5

---

# UX Specification — Custom Price Alerts

## 1. Context

`notifications.md` already documents four fixed, singleton alert types (Stop Loss Approach, Grace Period Warning, Market Regime Change, Daily Portfolio Summary) evaluated nightly and configured via the existing Alert Rule Thresholds section. Custom price alerts are structurally different — a user may define an arbitrary number of ticker/condition/threshold alerts, unconstrained by open positions (per readiness pass AC-01, backed by a new `price_alerts` table, not the singleton `alert_rules` table). This spec adds the create/view/edit/delete UI for that new surface, reusing the existing Notifications section's layout conventions.

## 2. Decision

### 2.1 Placement

A new third section on `/notifications/preferences`, below the existing "Alert Thresholds" section (which remains unchanged — it governs only the four fixed types): **"Custom Price Alerts"**.

### 2.2 Custom Price Alerts List

For each configured `price_alerts` row, a row showing:

| Element | Source | Format |
|---------|--------|--------|
| Ticker | `ticker` | Uppercase |
| Condition | `condition` + `threshold_price` | `"Above $150.00"` / `"Below £42.10"` (native currency inferred from ticker's market) |
| Status | `active` | "Active" (green) if `active = true`; "Triggered" (grey) if `active = false` and `triggered_at` set |
| Actions | — | "Delete" icon (trash), right-aligned |

**Sort:** most recently created first (`created_at` descending).

**Empty state:** icon (bell with plus, shared with the existing Alert Rules empty-state icon per `notifications.md` §Section 2), heading **"No custom price alerts."**, body `"Create an alert to be notified when a ticker crosses a price you choose."`, CTA **"Add price alert"**.

### 2.3 Create Alert Form

Triggered by **"Add price alert"** button (header of the Custom Price Alerts section, always visible — not only in the empty state).

Appears inline (expand row), consistent with the existing Alert Rule Create/Edit form pattern:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Ticker symbol | Text | Yes | Alphanumeric, 1–10 chars, uppercase-enforced on input — same validation as the Watchlist "Add Ticker" ticker field (`watchlist.md`) |
| Condition | Radio: Above / Below | Yes | — |
| Threshold price | Numeric | Yes | Positive decimal, > 0 |

**Submit:** `POST /price-alerts` (per readiness pass AC-08 pre-staged shape). On success: form collapses, new row appears at top of list. On error: inline error above the submit button: `"Failed to create price alert. Please try again."`

**Per-portfolio cap (readiness pass AC-03):** if the create call returns a `400` for exceeding the active-alert cap, show inline error: `"You've reached the maximum number of active price alerts."` — cap value itself is a backend/implementation-time decision, not fixed here.

### 2.4 Delete

Clicking the row's Delete icon shows an inline confirmation (matching the Watchlist "Remove from Watchlist" inline-confirmation pattern, not a separate modal):

> `"Delete price alert for {TICKER}?"`
- **"Delete"** (destructive) — calls `DELETE /price-alerts/{id}`; removes row from list.
- **"Cancel"** — dismisses; row remains.

### 2.5 Triggered Alerts

A triggered alert (`active = false`, `triggered_at` set) remains visible in the list with "Triggered" status until the user deletes it — it is not auto-removed, so the user can see what fired. The corresponding notification appears in the existing Notification Feed (`alert_type: 'custom_price_alert'`) per readiness pass AC-01/AC-02, using the same feed row layout as the four existing alert types — no new feed-row variant needed. Feed title format: `"Price Alert — {TICKER} {above/below} {threshold}"`.

## 3. §13 Compliance

Per readiness pass AC-05 (PASS): this feature only writes a `notifications` row and deactivates the alert — identical in kind to the existing `stop_loss_approach`/`grace_period_warning` notification-only alert types. No order placement, no position mutation, no automated execution. The user must manually act on any alert (e.g. open `TradeEntry.js`). Advisory only.

## 4. States

| State | Behaviour |
|-------|-----------|
| No alerts configured | Empty state (§2.2) |
| Alerts configured | List rendered, sorted newest-first |
| Create form open | Inline expand below "Add price alert" |
| Create — validation error | Inline error below the offending field |
| Create — cap exceeded | Inline error per §2.3 |
| Alert triggered | Row shows "Triggered" status; feed entry created |
| Delete — confirming | Inline confirmation shown |

## 5. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-17
- **Product Owner:** Approved — 2026-07-17
