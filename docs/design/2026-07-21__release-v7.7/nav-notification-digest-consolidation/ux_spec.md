**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-07-21
**Cycle:** 2026-07-21__release-v7.7
**Story:** ST-02 (EPIC-02, BLG-FE-114)

---

# UX Decision Record — Nav Duplication Removal & Digest/Notification Consolidation

## 1. Audit Findings

Inspection of `src/Layout.js` `NAV_GROUPS` confirms the duplication ST-02 targets:

```
Tools  group → { name: "Alerts",        icon: Bell, page: "notifications", alertBadge: true }
System group → { name: "Notifications", icon: Bell, page: "notifications" }
```

Both items route to the same page (`notifications`), share the same icon (`Bell`), and carry no visual indication that they are the same destination — a user can plausibly not realise "Alerts" and "Notifications" are one page. This is AC1's target.

`Weekly Digest` currently lives in the **Analytics** group (`page: "WeeklyDigest"`), separate from both Alerts and Notifications — this is AC2's gap.

## 2. Decisions

### AC1 — Remove nav duplication

Remove the **"Alerts"** entry from the **Tools** group. Retain a single **"Notifications"** entry in the **System** group as the sole nav path to the notifications page. The removed entry's `alertBadge: true` behaviour (unacknowledged-count badge) moves onto the retained "Notifications" entry.

**Why keep "Notifications" over "Alerts":** `notifications.md` already documents the page's own identity as "a top-level **Notifications** nav item" with Feed/Preferences/History sub-tabs — "Alerts" was the redundant shortcut alias, not the canonical name. Removing "Alerts" instead of "Notifications" requires no rename of the page's own spec, route structure, or its four documented surfaces.

**Nav.md impact:** the existing "Alert Badge Integration" section (nav.md) ties badge propagation to the **Tools** group collapse behaviour. This moves to the **System** group (§3 below).

### AC2 — Weekly Digest same grouping as Notifications

Move **"Weekly Digest"** from the **Analytics** group to the **System** group, positioned immediately above "Notifications" (both are point-in-time/activity-summary surfaces, distinct from Analytics' drill-down/investigation surfaces).

Resulting System group order: Settings → System Status → Weekly Digest → Notifications.

**Rejected alternative:** merging Weekly Digest as a fourth sub-nav tab on the Notifications page itself. Rejected because Weekly Digest is a distinct read-only summary artefact (own API, own print/export action) rather than an alert-management surface — folding it into the Notifications tab bar would misrepresent it as an alert-type surface. Shared grouping (not shared page) satisfies the AC without that misrepresentation.

### AC3 — Weekly Digest alert-count values link to filtered notification history

`weekly_digest.md` §2 renders `Alerts Fired (7d)` and `Alerts Dismissed (7d)` as static values, sourced from `GET /digest/weekly` → `alerts_fired_7d` / `alerts_dismissed_7d`. Per `digest_endpoints.md` §Field definitions, both are counts against the `notifications` table (`created_at` / `read`), the same table backing the Notification **Feed** (`GET /notifications`) — not the separate `alerts/history` evaluation-log table behind the Alert History tab. The link target is therefore the **Feed**, not History.

**Decision:** both values become links:
- **Alerts Fired (7d)** → `/notifications?since_days=7`
- **Alerts Dismissed (7d)** → `/notifications?since_days=7&read=true`

**New requirement flagged for Sprint Execution:** the Notification Feed (`GET /notifications` / `notifications.md` Page 1) does not currently document `since_days` or `read` query-param filtering — it is an unfiltered "newest first" list. Adding these two optional filter params (client-side query-string read on mount, applied before existing pagination) is in scope for ST-02's implementation; it is a small additive filter, not a new surface, so it does not require its own design-required classification. Documented in `notifications.md` update (STEP 3).

### AC4 — "Daily Portfolio Summary" vs. "Weekly Digest"

`notifications.md` §Page 2 has a **"Daily Portfolio Summary"** notification-preference toggle (`daily_portfolio_summary` type — a push/email notification sent once daily) that is easily confused with the **Weekly Digest** page (a 7-day on-demand summary view). Same rough concept ("portfolio summary"), different cadence and delivery mechanism, different underlying system entirely.

**Decision: differentiate via copy, not merge.** Renaming or collapsing `daily_portfolio_summary` would touch the stored preference key, the notification-feed row title (`"Daily Portfolio Summary"` per §Notification List), and the History rule-type label mapping — disproportionate for what is fundamentally a naming-clarity problem, not a duplicated-surface problem (unlike AC1, these are not two paths to the same content).

Applied fix: the preference row in `notifications.md` §Page 2 gets explanatory helper text distinguishing it from the Weekly Digest page, plus a cross-link. See STEP 3 spec update for exact copy.

## 3. Nav.md Alert Badge Section

Update the "Alert Badge Integration" section: badge is now on the **Notifications** item in the **System** group; when System is collapsed, the count propagates to the System group header, mirroring the existing Tools-group propagation pattern being replaced.

## 4. Constraints

- No route changes — `/notifications`, `/notifications/preferences`, `/notifications/history`, and the Weekly Digest route are unchanged; only nav placement and cross-links change.
- No backend schema change. The two new Feed filter params operate on data already returned by `GET /notifications` (query-string driven client request, not a new field).

## 5. Approval

Product Owner: approved 2026-07-21 (copy-based differentiation for AC4 accepted over a full concept merge).
Head of UX & Design: approved 2026-07-21.
