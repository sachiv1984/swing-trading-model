**Owner:** Head of UX & Design
**Class:** Planning Document (Class 4)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-15
**Story:** ST-07 (BLG-FE-112, EPIC-04, v7.2)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Notification/Digest Surface Consolidation Review

## 1. Purpose

Audit navigation entry points, usage patterns, and content overlap across the four notification/digest surfaces (`Notifications.js`, `NotificationsHistory.js`, `NotificationPreferences.js`, `WeeklyDigest.js`) and produce findings/recommendations. **Implementation of any consolidation recommendation is explicitly out of scope for this item (AC-03)** — this is an audit only.

## 2. Method

Static-code review: `src/Layout.js` nav structure, each of the four pages' data source and content, and `docs/specs/frontend/pages/notifications.md`.

## 3. Navigation Entry Points (AC-01)

| Nav Group | Item | Icon | Routes to |
|---|---|---|---|
| Tools | "Alerts" (badged with unread count) | `Bell` | `/notifications` |
| System | "Notifications" | `Bell` | `/notifications` |
| Analytics | "Weekly Digest" | `CalendarDays` | `/WeeklyDigest` |

`NotificationPreferences` and `NotificationsHistory` have **no standalone sidebar entry** — both are reachable only via `NotificationTabBar`'s "Preferences"/"History" tabs from within `/notifications`. This is correct and not flagged as an issue (they are sub-views of one feature, not independent destinations).

**Finding 1 — duplicate sidebar entries for the same page.** "Alerts" (Tools group) and "Notifications" (System group) are two separate `NAV_GROUPS` entries (`src/Layout.js` lines ~79 and ~88) that both route to the identical page (`page: "notifications"`). Only "Alerts" carries the unread-count badge (`alertBadge: true`). A user has two different, differently-labelled ways to reach the same screen from two unrelated nav sections, with no indication they're the same destination until clicked.

**Finding 2 — Weekly Digest sits in a disconnected nav group.** "Weekly Digest" lives in "Analytics", structurally separate from "Alerts"/"Notifications" in "Tools"/"System", despite being conceptually a notification/reporting surface (see Finding 4 below for the deeper content-level version of this).

## 4. Content Overlap (AC-01, AC-02)

**Finding 3 — Weekly Digest surfaces alert aggregates with no link back to the alerts themselves.** `WeeklyDigest.js` renders `alerts_fired_7d` and `alerts_dismissed_7d` as raw counts (`GET /digest/weekly`). A user seeing "12 Alerts Fired (7d)" has no way to jump from that number to the actual list of alerts in `/notifications` or `/notifications/history` — the two surfaces show related data with zero cross-navigation.

**Finding 4 — two independent "digest" concepts exist with no shared design language.** `NotificationPreferences.js` defines a `daily_portfolio_summary` alert type ("Receive a daily digest of portfolio status") — when enabled, this fires as an individual notification event delivered through the same feed as `stop_loss_approach`/`grace_period_warning`/`market_regime_change`, and appears as a row type in `NotificationsHistory.js` (`TYPE_LABELS.daily_portfolio_summary`). This is functionally a "digest" — but it is architecturally and terminologically disconnected from `WeeklyDigest.js`, which is:
- A different cadence (daily vs weekly)
- A dedicated standalone page, not a feed entry
- Backed by an entirely separate endpoint (`GET /digest/weekly` vs the notifications feed's own endpoint)
- Not configurable via `NotificationPreferences.js` at all — there is no on/off toggle for the weekly digest anywhere in the four surfaces reviewed

A user trying to answer "how do I get a summary of my portfolio" has to independently discover two unrelated mechanisms (a notification preference toggle, and a separate page under a different nav group) that use the word "digest"/"summary" in overlapping but not identical ways, with no in-app text connecting them.

## 5. Redundancy Summary

| Redundancy | Severity | Type |
|---|---|---|
| Duplicate "Alerts"/"Notifications" nav entries → same page | Moderate | Navigation |
| Weekly Digest nav-grouped away from Alerts/Notifications | Low | Navigation / discoverability |
| No cross-link between Weekly Digest's alert counts and the alert feed | Moderate | Content |
| Two disconnected "digest" concepts (daily portfolio summary notification vs weekly digest page) | Moderate–High | Conceptual / IA |

## 6. Recommendation (AC-02)

Consolidate to a single mental model: one "Notifications & Digests" surface. Concretely (for a future story to scope, not actioned here):
1. Remove one of the two duplicate nav entries (keep the badged "Alerts" entry; drop the unbadged "Notifications" duplicate, or merge them into one entry that carries the badge regardless of nav group).
2. Move "Weekly Digest" into the same nav group as "Alerts"/"Notifications" (or add a tab for it on the existing `NotificationTabBar`, alongside Feed/Preferences/History), so all notification-adjacent surfaces are discoverable from one place.
3. Add a visible link from `WeeklyDigest.js`'s alert-count rows to the filtered notification history for that period.
4. Either fold "Daily Portfolio Summary" into the same page/concept as "Weekly Digest" (configurable cadence: daily or weekly), or rename one of the two to avoid the shared "digest/summary" terminology implying they're related when they're currently unconnected.

## 7. Follow-Up (AC-03)

Per this item's own scope boundary, no implementation is performed here. This audit recommends consolidation (§6) — per AC-03, a follow-up backlog item (`BLG-FE`-class) should be filed for the future consolidation work, scoped as a `delegated_frontend` story with its own design-gate pass (given the nav/IA change touches multiple pages and a shared component).

**Filing deferred outside this routine's write scope.** `execution_prompt.md §7` restricts this routine's writes to `claude/backlog/backlog.md` to the STEP 5.2 `returned_to_backlog` note only — a new BLG item filing is a different action and is out of scope here. This report itself is the durable record of the recommendation; the item should be filed at the next `groom backlog` pass, at sprint close by the Product Owner directly, or by re-invoking `/backlog-add` outside this execution run, using this report (§3–§6) as source content.

## 8. Known Deviations

None. This is a net-new audit artefact.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-07-15 | 1.0 | Initial consolidation review (ST-07, EPIC-04, v7.2) |
