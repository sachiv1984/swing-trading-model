**Owner:** Head of UX & Design
**Status:** Approved
**Approved by:** Product Owner — 2026-03-24
**Cycle:** 2026-03-24__release-v2.3
**Story:** ST-02 (BLG-FEAT-09)

---

# UX Spec — Metrics Staleness Indicator

## Placement

Appears on two pages:
1. **Analytics page** — below the page title, above the period selector
2. **Portfolio/Positions page** — below the page title, inline with the view controls

## Display Format

Normal state (fresh data): `Data as of 14 mins ago` (grey text, small — secondary typography)

Stale state (data older than threshold): amber badge: `⚠ Data as of 3h ago — may be outdated`

Hover / tooltip on both states: absolute ISO timestamp (e.g. `Updated: 2026-03-24 09:41 UTC`)

## Staleness Threshold

Default: **4 hours**. No user-configurable threshold in v2.3 (may be a settings item in a future release).

## Relative Time Display

- < 1 min: "just now"
- 1–59 min: "N mins ago"
- 1–23 hrs: "Nh ago"
- ≥ 24 hrs: "N days ago"

## Data Source

Backend exposes `last_sync_at` (or equivalent) on the relevant API response. Frontend reads this field and computes relative time client-side. If field absent or null: omit indicator entirely (do not show "unknown").

## States

- **Absent / null:** indicator hidden
- **Fresh (< threshold):** grey text, no badge
- **Stale (≥ threshold):** amber text + ⚠ icon
