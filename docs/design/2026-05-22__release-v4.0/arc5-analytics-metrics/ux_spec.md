**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Approved
**Version:** 1.0
**Cycle:** 2026-05-22__release-v4.0
**Approved by:** Head of UX & Design + Product Owner, 2026-05-23
**Stories:** ST-02 (BLG-FEAT-37), ST-04 (BLG-FEAT-39)

---

# UX Spec — Arc 5 Signal Compliance Metrics

## Scope

This spec covers the frontend display of two new Arc 5 compliance metrics:

- **ST-02:** Red flag event frequency (events_per_week, override_rate, top_rule_breach)
- **ST-04:** Trade plan adherence rate (trade_plan_adherence_rate)

## Placement

New §19 section on the Performance Analytics page (`/analytics`), appended after §18 (Market Correlation). Title: **"Arc 5 Signal Compliance"**.

## Layout

Four stat cards in a horizontal row (responsive: stacks on narrow viewports). Same visual treatment as §17 (Discipline & Compliance) stat cards.

| Card | Metric | Source Field | Format |
|------|--------|-------------|--------|
| Red Flag Events/Week | events_per_week | `events_per_week` | integer; sub-label: "rolling 7 days" |
| Override Rate | override_rate | `override_rate` | percentage, 1dp; sub-label: "overrides / validation attempts" |
| Top Rule Breach | event_type_distribution (most frequent) | `top_rule_breach` | text label (e.g. "regime_gate"); sub-label: "most frequent event type" |
| Trade Plan Adherence | trade_plan_adherence_rate | `trade_plan_adherence_rate` | percentage, 1dp; sub-label: "trades with plan / total closed trades" |

## API Source

`GET /analytics/arc5-compliance` — new endpoint, returning:
```json
{
  "events_per_week": <int>,
  "override_rate": <float>,
  "top_rule_breach": <str | null>,
  "trade_plan_adherence_rate": <float | null>
}
```

Period: fixed rolling 7-day for events_per_week/override_rate/top_rule_breach; all-time for trade_plan_adherence_rate.

## States

- **Loading:** skeleton cards (same as §17)
- **Loaded:** cards rendered
- **Insufficient data:** individual card shows "–" with tooltip "Insufficient data" when source field is null or zero denominator
- **Error:** section-level error card

## Hard Rules

- All values backend-computed. No client-side derivation.
- Section renders regardless of trade count (shows "–" when insufficient data).
- `top_rule_breach` null → card shows "–" with tooltip "No events in period".
