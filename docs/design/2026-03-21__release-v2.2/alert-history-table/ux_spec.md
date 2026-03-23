**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner
**Approved date:** 2026-03-22
**Cycle:** 2026-03-21__release-v2.2
**Items:** ST-05
**Frontend spec target:** docs/specs/frontend/pages/notifications.md (update to v0.2)

---

# UX Spec — Alert History Table (ST-05)

## 1. Purpose & User Goal

Users need observability into when and why alert rules fired (or did not fire), so they can understand system behaviour and validate that alerts are working as expected. This is not a notification feed (which shows triggered user-facing notifications); it is an evaluation audit log.

**User goal:** Review a chronological log of every alert rule evaluation, see which fired and which did not, and filter by rule type to investigate specific behaviour.

---

## 2. Scope

This spec covers:
- The Alert History page/view (accessible from the Notifications section)
- The evaluation record table: fields, sort, filter
- Empty, loading, and error states

It does not cover:
- The Notification Feed (existing, covered in notifications.md v0.1)
- Notification Preferences (existing, covered in notifications.md v0.1)
- Alert rule creation/editing (ST-04)

---

## 3. Navigation & Placement

### 3.1 Route

`/notifications/history` (new route; added as a third tab in the Notifications sub-navigation)

### 3.2 Sub-Navigation

The Notifications section sub-nav is extended:

| Tab | Route | Default active? |
|-----|-------|-----------------|
| Feed | `/notifications` | Yes (unchanged) |
| Preferences | `/notifications/preferences` | No (unchanged) |
| **History** | `/notifications/history` | No (new) |

### 3.3 Page Header
- H1: **"Alert History"**
- Subtitle: `"A log of every alert rule evaluation by the system."`

---

## 4. Alert History Table

### 4.1 API Reference
- **Endpoint:** `GET /alerts/history`
- **Query parameters:** `last_n_days` or `last_n_records` (as defined by ST-03 spec output)
- **Canonical contract:** `docs/specs/api_contracts/alerts_endpoints.md`

### 4.2 Table Columns

| Column | Source field | Format |
|--------|-------------|--------|
| Date / Time | `evaluation_timestamp` | `YYYY-MM-DD HH:mm` (local time); full ISO on hover |
| Alert Type | `rule_type` | Human-readable label (see mapping below) |
| Symbol | `symbol` | Uppercase ticker, or `—` if rule is not symbol-specific |
| Triggered | `triggered` | Boolean → "Yes" (amber/orange badge) / "No" (neutral grey badge) |
| Notified | `notification_sent` | Boolean → "Yes" (green badge) / "No" (neutral grey badge) |
| Values | `values_compared` | Compact key-value summary, e.g. `"stop: $42.10, price: $43.50, gap: 3.3%"` — truncated to fit; full detail on row expand or tooltip |

**Rule type display labels:**

| API value | Display label |
|-----------|--------------|
| `stop_loss_approach` | Stop Loss Approach |
| `grace_period_warning` | Grace Period Warning |
| `market_regime_change` | Market Regime Change |
| `daily_portfolio_summary` | Daily Portfolio Summary |
| Unknown | Raw value (fallback) |

### 4.3 Default Sort

Newest first (descending `evaluation_timestamp`). This is the default and cannot be removed.

### 4.4 User-Controllable Sort

Sortable columns: **Date / Time** only (ascending or descending). Click column header to toggle. Active sort direction indicated by an up/down arrow icon.

### 4.5 Filter

A **rule type filter** appears above the table (right-aligned or inline with the table header):

```
Label: "Filter by type:"
Control: Dropdown / select
Options: All types (default) | Stop Loss Approach | Grace Period Warning | Market Regime Change | Daily Portfolio Summary
```

- Selecting a type filters the visible rows client-side (if data is fully loaded) or sends a query parameter to the API.
- Active filter is reflected in the dropdown selection.
- Reset to "All types" clears the filter.

### 4.6 Pagination / Load Window

- Default view: last 30 days (or last 200 records — whichever is smaller; driven by query param from API)
- A **"Load more"** button at the bottom of the table fetches the next page/window.
- No infinite scroll.

---

## 5. Row Expand (Values Detail)

The `values_compared` column is truncated in the table view. Clicking a row expands it inline to show the full `values_compared` map as a key: value list (no modal).

Expanded row:
```
▼ stop_loss_approach — AAPL — 2026-03-21 16:30
  stop_price:   $42.10
  current_price: $43.50
  gap_pct:       3.3%
  threshold_pct: 5.0%
  triggered:     Yes
  notification_sent: Yes
```

Click again to collapse.

---

## 6. States

### 6.1 Loading State
Skeleton rows (5 rows at standard table-row height) while data loads.

### 6.2 Empty State — No Records
```
Icon: Clock with magnifying glass (or similar)
Heading: "No alert history yet."
Body: "Alert evaluations will appear here once the system has run."
```

### 6.3 Empty State — Filter Applied, No Matches
```
Body: "No evaluations found for the selected alert type."
Link: "Clear filter" (resets to All types)
```

### 6.4 Error State
Full-width error panel: `"Unable to load alert history. Please refresh."`

---

## 7. UX Decisions Recorded

| Decision | Rationale |
|----------|-----------|
| New "History" tab in Notifications sub-nav | Alert history is evaluation observability; it belongs near notifications but is distinct from the user-facing notification feed |
| Triggered and Notified as separate columns | A rule can trigger (condition met) without sending a notification (e.g. if notification preference is off). Keeping both columns makes the distinction explicit and observable. |
| Values truncated inline, expanded on row click | Keeps table scannable; full field detail is available on demand without a modal |
| Filter by rule type (client or server-side) | Most useful dimension for diagnosing specific alert behaviour |
| Newest-first default sort | Users investigating recent behaviour should see the most recent evaluations first |
| 30-day / 200-record default window | Balances observability with performance; `load more` handles longer histories |
| No delete/archive | History is an audit log; users should not be able to remove evaluation records |
