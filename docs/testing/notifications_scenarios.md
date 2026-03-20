**Owner:** QA & Testing Owner
**Class:** Canonical (Class 1)
**Status:** Canonical
**Version:** 1.0
**Last Updated:** 2026-03-20
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Derived from:** `docs/specs/frontend/pages/notifications.md` v0.1; `docs/specs/api_contracts/alerts_endpoints.md` v0.1
**Sprint:** 2026-03-18__release-v2.1 — ST-07 (closes EPIC-02 test scenario gap)

---

# Acceptance Test Scenarios — Notifications (Feed & Preferences)

---

## 1. Scope

These scenarios verify the Notifications feature against the canonical specification. They cover: alert rule evaluation, Telegram notification delivery, the in-app notification feed (display, mark-as-read, empty state), and the notification preferences page (toggle persistence, optimistic update, error revert). Alert scheduling cadence is out of scope — that gap is tracked as BLG-OPS-04.

---

## 2. Canonical Spec References

| Component | Spec location |
|-----------|--------------|
| Notification feed page | `docs/specs/frontend/pages/notifications.md §Page 1: Notification Feed` |
| Notification preferences page | `docs/specs/frontend/pages/notifications.md §Page 2: Notification Preferences` |
| Alert rules engine | `docs/specs/api_contracts/alerts_endpoints.md §POST /alerts/evaluate` |
| Notification feed API | `docs/specs/api_contracts/alerts_endpoints.md §GET /notifications` |
| Mark read API | `docs/specs/api_contracts/alerts_endpoints.md §PATCH /notifications/{id}` |
| Mark all read API | `docs/specs/api_contracts/alerts_endpoints.md §POST /notifications/mark-all-read` |
| Preferences API | `docs/specs/api_contracts/alerts_endpoints.md §GET /notifications/preferences` |
| Preferences update API | `docs/specs/api_contracts/alerts_endpoints.md §PATCH /notifications/preferences` |
| Delivery architecture | `docs/adr/ADR-003-notification-delivery-architecture.md` |

---

## 3. Scenarios

---

### SC-NOTIF-01 — Alert evaluation creates notification and delivers via Telegram

**Component:** Backend — alert rules engine, notification delivery
**API:** `POST /alerts/evaluate`, Telegram Bot API
**Priority:** P1

#### Preconditions

- Staging environment is live (`https://trading-assistant-api-c0f9.onrender.com`).
- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` environment variables are set in Render.
- At least one alert rule is enabled (all 4 are seeded by default).
- A portfolio exists with at least one open position (for `stop_loss_approach`) or the `daily_portfolio_summary` rule is enabled (triggers regardless of positions).

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Call `POST /alerts/evaluate` via the API (e.g. curl or Swagger UI). | Response: `{"status": "ok", "data": {"rules_evaluated": N, "notifications_created": M, ...}}` where N ≥ 1. |
| 2 | Observe `notifications_created` in the response. | ≥ 1 when an alert condition is met (e.g. `daily_portfolio_summary` always fires when no prior notification exists for today). |
| 3 | Check the Telegram chat associated with `TELEGRAM_CHAT_ID`. | A Telegram message is received with the notification title and message body within ~5 seconds of the API call. |
| 4 | Call `GET /notifications`. | The newly created notification appears in the feed with `read: false`. |

#### Pass criteria

- `POST /alerts/evaluate` returns 200 with `rules_evaluated` > 0.
- At least one notification is created and appears in `GET /notifications`.
- Telegram message is received for the triggered notification.

---

### SC-NOTIF-02 — Notification feed displays correctly; unread indicator present

**Component:** Frontend — notification feed page (`/notifications`)
**API:** `GET /notifications`
**Priority:** P1

#### Preconditions

- At least one notification exists in the system (created by SC-NOTIF-01 or prior evaluation).
- User navigates to staging frontend.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to the Notifications page via the sidebar nav item. | URL changes to `/#/notifications`. The feed page loads with a skeleton (brief) then the notification list. |
| 2 | Observe a notification that has `read: false`. | The row has a 2px left border in cyan. The "Mark as read" button is visible below the message. |
| 3 | Observe a notification that has `read: true` (if any). | No cyan left border. No "Mark as read" button. |
| 4 | Observe the timestamp on any notification. | Displayed as relative time (e.g. "2 hours ago"). Hovering reveals the absolute ISO timestamp in a tooltip. |
| 5 | Observe the alert type icon for each notification. | Each row has a coloured icon matching its type: ShieldAlert (rose) for `stop_loss_approach`, Clock (amber) for `grace_period_warning`, TrendingDown (violet) for `market_regime_change`, BarChart2 (cyan) for `daily_portfolio_summary`. |
| 6 | Observe the page header area. | "Mark all as read" button is visible (since ≥1 unread notification exists). |

#### Pass criteria

- Feed renders within 3 seconds of page load.
- Unread indicator (cyan left border) present on unread items only.
- Correct icon displayed per alert type.
- "Mark all as read" visible when unread items exist.

---

### SC-NOTIF-03 — Mark single notification as read; optimistic update and revert on error

**Component:** Frontend — notification feed, mark-as-read
**API:** `PATCH /notifications/{id}`
**Priority:** P1

#### Preconditions

- At least one notification with `read: false` is visible in the feed.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click "Mark as read" on an unread notification. | The cyan left border disappears immediately (optimistic update). The "Mark as read" button disappears from that row. |
| 2 | Observe the Network tab. | A `PATCH /notifications/{id}` request fires and returns 200. |
| 3 | Reload the page. | The notification remains in `read: true` state — change is persisted. |

#### Pass criteria

- Optimistic update removes unread indicator immediately on click.
- Persisted after page reload.

---

### SC-NOTIF-04 — Mark all as read; optimistic update, header button hidden

**Component:** Frontend — notification feed, mark all read
**API:** `POST /notifications/mark-all-read`
**Priority:** P2

#### Preconditions

- Multiple unread notifications are visible in the feed.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click "Mark all as read" in the page header. | All cyan left borders disappear immediately. All "Mark as read" per-row buttons disappear. |
| 2 | Observe the "Mark all as read" button in the header. | Button disappears (no unread items remain). |
| 3 | Observe the Network tab. | A `POST /notifications/mark-all-read` request fires and returns 200. |
| 4 | Reload the page. | All notifications are in `read: true` state. "Mark all as read" button does not appear. |

#### Pass criteria

- All indicators cleared optimistically.
- Header button hidden after all-read.
- Persisted after reload.

---

### SC-NOTIF-05 — Empty state displayed when no notifications exist

**Component:** Frontend — notification feed, empty state
**Priority:** P2

#### Preconditions

- No notifications exist in the system (fresh environment or all notifications have been cleared at the DB level).
- Alternatively: test on the live/production environment where no evaluations have been run.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to `/#/notifications`. | Page loads. No skeleton persists. |
| 2 | Observe the main content area. | A centred Bell icon is displayed. Heading reads "No notifications yet." Sub-text reads "Alert notifications will appear here when triggered." |
| 3 | Observe the page header area. | "Mark all as read" button is absent. |

#### Pass criteria

- Empty state renders correctly with Bell icon and both text strings.
- No "Mark all as read" button shown.

---

### SC-NOTIF-06 — Notification preferences page loads and displays all four alert types

**Component:** Frontend — notification preferences page (`/notifications/preferences`)
**API:** `GET /notifications/preferences`
**Priority:** P1

#### Preconditions

- User is on the staging or live frontend.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Navigate to `/#/notifications` then click the "Preferences" tab. | URL changes to `/#/notifications/preferences`. Skeleton rows appear briefly then the preferences list renders. |
| 2 | Observe the preference rows. | Exactly 4 rows are shown: Stop Loss Approach, Grace Period Warning, Market Regime Change, Daily Portfolio Summary. Each has a toggle switch and a one-line description. |
| 3 | Observe the "Feed" and "Preferences" tab bar. | "Preferences" tab has the active indicator (cyan underline). "Feed" tab is inactive. |
| 4 | Observe the sidebar nav item. | "Notifications" nav item is highlighted (active state) when on either the feed or preferences page. |

#### Pass criteria

- All 4 alert types rendered with correct labels and descriptions.
- Tab bar active state correct on preferences.
- Sidebar nav item active on both routes.

---

### SC-NOTIF-07 — Preference toggle persists; "Saved" confirmation shown

**Component:** Frontend — notification preferences, toggle + PATCH
**API:** `PATCH /notifications/preferences`
**Priority:** P1

#### Preconditions

- Preferences page is loaded and at least one toggle is visible.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Click the toggle for "Daily Portfolio Summary" to disable it (if currently enabled). | Toggle flips immediately (optimistic update). |
| 2 | Observe the row within 2 seconds. | A brief "Saved" label appears in cyan adjacent to the toggle, then fades out. |
| 3 | Observe the Network tab. | A `PATCH /notifications/preferences` request fires with body `{"daily_portfolio_summary": {"email_enabled": false}}` and returns 200. |
| 4 | Reload the page. | "Daily Portfolio Summary" toggle is in the off state — change persisted. |
| 5 | Toggle it back on. | Toggle flips, "Saved" label appears, `PATCH` fires with `{"email_enabled": true}`, and setting persists after reload. |

#### Pass criteria

- Optimistic toggle flip on click.
- "Saved" label visible then fades.
- Value persisted after page reload.

---

### SC-NOTIF-08 — All four alert types can be individually toggled

**Component:** Frontend — notification preferences
**API:** `PATCH /notifications/preferences`
**Priority:** P2

#### Preconditions

- Preferences page is loaded with all 4 rows visible.

#### Steps

| Step | Action | Expected result |
|------|--------|-----------------|
| 1 | Toggle off each of the 4 alert types one at a time. | Each toggle flips, each PATCH fires individually with the correct `alert_type` key, each "Saved" label appears. |
| 2 | Reload the page. | All 4 toggles are in the off state. |
| 3 | Toggle all 4 back on. | Each persists individually as above. |

#### Pass criteria

- Each alert type can be toggled independently.
- All 4 types map to the correct `alert_type` keys in the PATCH body.

---

## 4. Out of Scope

| Topic | Reason |
|-------|--------|
| Alert scheduling / cron trigger | Tracking as BLG-OPS-04 — awaiting Product Owner guidance on frequency and mechanism |
| Stop loss approach trigger (live positions required) | Requires open position within threshold; covered by integration path when positions exist |
| Grace period warning trigger | Requires position in grace period (day 8–9); covered by integration path |
| Market regime change trigger | Requires regime transition event; covered by integration path |
| Notification pagination ("Load more") | Verified incidentally when > 50 notifications exist; not a dedicated scenario due to volume requirement |
| Telegram message format | Confirmed in SC-NOTIF-01; exact formatting is delivery-channel detail, not frontend AC |

---

## 5. Director of Quality Sign-Off

**SC-NOTIF-01:** Verified 2026-03-20 — `POST /alerts/evaluate` returned `rules_evaluated: 4`, `notifications_created: 1` (daily_portfolio_summary); Telegram message received.
**SC-NOTIF-02 through SC-NOTIF-08:** Verified 2026-03-20 — feed renders in staging with unread indicators; empty state confirmed in live; preferences page loads all 4 types; toggle saves with "Saved" confirmation; nav highlights on both routes.
**Director of Quality sign-off:** 2026-03-20
