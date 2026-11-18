**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-18__release-v9.18
**Stories:** ST-03 (BLG-FE-318), ST-04 (BLG-FE-228) — EPIC-01

# Decision Record — Alert Delivery Truth and Alert History Values

## 1. Scope of this record

ST-03 makes alert-delivery copy true (Telegram, not email) and shows when an alert was not sent. ST-04 fixes the Alert History compact values. Both change the Notifications pages, built ST-03 then ST-04.

Spec impact: `notifications.md` v0.11 → v0.12 (Page 2 wording, §Channel Scope, Feed row delivery line, Alert History §Values mapping).

## 2. Telegram wording (ST-03)

- Every "email" on Notification Preferences becomes "Telegram": the subtitle ("Choose which alerts are also sent to Telegram, and set custom thresholds."), the section title ("Telegram alerts", was "Email Preferences"), the toggle column ("Send to Telegram"), and the Reflection Reminder description ("Send to Telegram when a closed trade has no reflection after 48 hours").
- The `email_enabled` column and API field keep their names (no migration); `notifications.md` and the contract note that the field governs Telegram delivery.
- Backend error strings that reach the UI change too: `'email not configured'` → `'Telegram not configured'`, `'email disabled'` → `'Telegram off for this alert type'`.
- §Channel Scope: "Telegram is the only delivery channel. There is no email or SMS."

## 3. "Not sent" (ST-03)

### 3.1 Data-source check

- `notifications` stores `delivered`, `delivery_attempts`, `delivery_error`, `delivery_attempted_at` (`alerts_endpoints.md` line 32). `GET /notifications` does **not** return them today, so the Feed cannot show delivery. ST-03 adds one derived field to each `GET /notifications` item: `delivery_status` (contract and `openapi.yaml` in ST-03).
- Delivery is enqueued only when the alert type's preference is on. With it off, a generic notification is never attempted (`delivery_attempts = 0`); a Reflection Reminder is created already settled with the "disabled" error. Re-delivery retries `delivered = false`, `attempts < 3`, unread rows.

### 3.2 `delivery_status` (derived server-side)

| Stored state | `delivery_status` | Feed row shows |
|--------------|-------------------|----------------|
| `delivered = true`, no error | `sent` | nothing extra |
| preference off: `delivery_attempts = 0`, or the "disabled" error | `not_requested` | nothing extra (in-app only is what the user chose) |
| `delivered = false`, error "Telegram not configured" (after ST-03's backend change) | `not_sent` | "Not sent: Telegram not configured" |
| `delivered = false`, `delivery_attempts ≥ 3`, other error | `not_sent` | "Not sent: Telegram delivery failed" |
| `delivered = false`, `1 ≤ attempts < 3`, other error | `pending` | nothing extra (a retry is due on the next evaluation) |
| `delivered = false`, attempts 0, preference on (enqueued, not yet run) | `pending` | nothing extra |

- **Backend change:** with `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` unset, `deliver_notification` writes `delivered = FALSE`, `delivery_error = 'Telegram not configured'` (was TRUE / 'email not configured'). Re-delivery then retries it up to 3 times (each fails the same way); that is accepted, and the row is `not_sent` from the first attempt because the error names the cause.
- **Rendering:** a muted line under the notification's message, `text-xs text-app-warning`, with an `AlertTriangle` icon (`aria-hidden`), `data-testid="notification-not-sent"`. The text carries the meaning; colour is secondary.
- **Where:** the Notification Feed rows. Notification History (`alert_evaluations`) already has a "Notified" column for whether a notification was created; it does not track delivery, and is unchanged.
- **Old rows:** rows written before ST-03 as `delivered = TRUE, 'email not configured'` are not rewritten; they show nothing extra. Recorded as known history, not a deviation.

## 4. Alert History compact values (ST-04)

### 4.1 Data-source check — keys the backend writes (`alerts_service.py`)

| Rule type | `values_compared` keys written | UI expects today | Gap |
|-----------|-------------------------------|------------------|-----|
| `stop_loss_approach` | `stop_price`, `current_price`, `gap_pct`, `threshold_pct` | `current_price`, `stop_price`, `gap_pct` | None (but see §4.3 currency) |
| `grace_period_warning` | `holding_days`, `min_hold_days`, `days_remaining` | `days_remaining`, `grace_period_days` | `grace_period_days` never written |
| `market_regime_change` | the regime notification's context: `spy_risk_on`, `ftse_risk_on`; `{}` when not triggered | `regime`, `previous_regime` | Neither key written (not in the backlog item; found here) |
| `daily_portfolio_summary` | `open_positions` | `positions_count`, `total_pnl` | Neither key written |

### 4.2 Decision: align the UI to the backend keys (no backend rename)

| Rule type | Compact text |
|-----------|--------------|
| `stop_loss_approach` | "Price {current_price} · Stop {stop_price} · Gap {gap_pct}%" |
| `grace_period_warning` | "Day {holding_days} of {min_hold_days} · {days_remaining} day(s) left" |
| `market_regime_change` | "US {RISK-ON \| RISK-OFF} · UK {RISK-ON \| RISK-OFF}" from `spy_risk_on`/`ftse_risk_on` (true → RISK-ON, false → RISK-OFF, null → UNKNOWN); `{}` → "—" |
| `daily_portfolio_summary` | "{open_positions} open position(s)" |

The full key/label mapping table goes in `notifications.md` §Alert History Values; the row-expand detail uses the same labels.

### 4.3 Currency (worked example)

`formatValue` formats every `*_price` as USD. A UK stop-loss row (`BARC.L`, stop 180.00, price 182.50, both GBP per the position's native currency) shows "$182.50". The compact text must use the row's market currency. `alert_evaluations` has `symbol` but no `market`, and this gate has not confirmed whether `symbol` keeps the `.L` suffix or whether UK values are in pounds or pence. ST-04 traces the writer for both (first-time-right check 1), then derives the currency from the suffix or a position join. Before the commit it checks one real UK row (staging, with the user's permission).

## 5. Approvals

- Head of UX & Design: approved (agent-mediated, Design Gate Engine), 2026-11-18.
- Product Owner: approved (the user, in session, 2026-11-18).
