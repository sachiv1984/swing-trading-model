**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Last Updated:** 2026-07-15
**Approved by:** Product Owner — 2026-07-15
**Story:** ST-05 — Dashboard empty/first-run state coverage (BLG-FE-110)
**Depends on:** ST-04 spec & instrumentation pass (BLG-SPEC-90) — formalises the `DataState` empty-state pattern in `design_system.md`; this artefact is the concrete application to `DashboardHome.js`
**Cycle:** 2026-07-15__release-v7.2

---

# UX Specification — Dashboard Empty/First-Run State Coverage

## 1. Context

`Watchlist.js` already uses the shared `DataState` component (`src/components/ui/DataState.js`) for a properly designed empty state (icon, heading, body, CTA). `DashboardHome.js`'s five session-summary cards do not: `OpenPositionsCard` and `GracePeriodCard` render a bare muted text line when their count is zero, and `RecentActivityCard`'s zero-state (per `dashboard.md` §4 Card 5, "No recent trade activity") is likewise plain text with no icon/heading treatment. `DataState`'s `empty` branch is sized for a full-page/table context (`py-16`, `w-10 h-10` icon) — too tall for a compact card inside the 3-card/2-card grid without visibly unbalancing row height against sibling cards.

## 2. Decision

### 2.1 Component change — `DataState` compact variant

Add an optional `compact` boolean prop to `DataState` (default `false`, non-breaking — `Watchlist.js` and any other existing caller is unaffected):

| Element | Default (`compact=false`) | `compact=true` |
|---------|---------------------------|-----------------|
| Outer padding | `py-16` | `py-4` |
| Icon size | `w-10 h-10` | `w-6 h-6` |
| Gap | `gap-3` | `gap-2` |
| Heading | `text-sm font-semibold` | `text-xs font-semibold` |
| Body | `text-xs` (unchanged) | `text-xs` (unchanged) |

Loading and error branches are untouched by this change (AC-03) — `compact` only affects the `empty` branch's layout classes.

### 2.2 Cards in scope (AC-01, AC-02)

Each card's own content (inside `<DashboardCard>`, below the always-visible title label) is wrapped in `<DataState compact empty={...} emptyIcon={...} emptyHeading={...} emptyBody={...}>` around its existing non-empty JSX. `DashboardCard`'s own `isLoading`/`error` short-circuit (lines 13–24, `DashboardCard.js`) is unchanged — `DataState`'s `loading`/`error` props are left unset here, so only the `empty` branch is reachable, and AC-03 is satisfied by construction (zero lines of the loading/error path are touched).

| Card | Empty condition | Icon | Heading | Body |
|------|-----------------|------|---------|------|
| `OpenPositionsCard` | `open.length === 0` | `Inbox` | "No open positions" | "Positions you open will appear here." |
| `GracePeriodCard` | grace count `=== 0` | `ShieldCheck` | "No positions in grace" | "You'll be notified as positions approach review." |
| `RecentActivityCard` | activity list `.length === 0` | `Activity` | "No recent activity" | "Trade opens, closes, and stop updates will show up here." |

No `emptyAction` CTA on any of the three — unlike `Watchlist.js` (a page whose sole content is the empty/non-empty list), these are small cards inside a denser grid; the existing card-level click-through (whole card navigates to `/Positions` etc., per `dashboard.md` §8) already provides the next step. Adding a second CTA inside the card would compete with that.

**Icon tone note:** `GracePeriodCard`'s zero-state is a *good* outcome (nothing at risk), so `ShieldCheck` is used rather than a neutral "nothing here" icon like `Inbox` — same rationale Watchlist/Open Positions use (those zero-states are neutral/action-inviting, not reassuring).

### 2.3 Cards explicitly out of scope

| Card | Rationale |
|------|-----------|
| `PortfolioHeatCard` | 0% heat is a legitimate, meaningful value (fully deployed cash), not missing/empty data — no empty state applies |
| `SignalStatusCard` | "0 new signals today" is a valid count, not missing data — no empty state applies |
| Morning Briefing 5 sub-cards (`ScreenerHitsCard`, `ExitZoneCard`, `RedFlagsCard`, `EarningsAlertCard`, `ComplianceCard`) | Already have specced single-line empty copy (`dashboard.md` §1A) appropriate to their denser 5-across layout; promoting to the full icon+heading+body pattern would visually overweight this row relative to its "Trader's Morning Briefing" intent (glanceable, not the primary content). Not a gap — an intentional exclusion. |
| `AiDailyBriefing` | Already has a fully-designed "No briefing yet" state (`dashboard.md` §5 States table) with explanatory text and an enabled CTA — already compliant with the "not a blank card or raw zero/null value" bar. No change. |

## 3. §13 Compliance

Display-only presentational change. No new data, no automated action.

## 4. States

| State | Behaviour |
|-------|-----------|
| Loading (any in-scope card) | Unchanged — `DashboardCard`'s existing skeleton/spinner path |
| Error (any in-scope card) | Unchanged — `DashboardCard`'s existing "Unable to load" path |
| Empty, in-scope card | Compact `DataState` empty block (icon + heading + body, no CTA) |
| Non-empty, in-scope card | Existing card content, unchanged |
| Out-of-scope cards | Unchanged in all states |

## 5. Playwright / Dual-Theme Note

Per ST-04 AC-04, Base44 prompt drafts and Playwright coverage for this story must explicitly verify both light and dark theme rendering of the new compact empty-state icon/text (contrast of `text-slate-600 dark:text-slate-400` body copy against both card backgrounds). Test file: shared spec named per ST-08 (EPIC-05 combined Playwright suite plan).

## 6. Sign-off

- **Head of UX & Design:** Confirmed — 2026-07-15
- **Product Owner:** Approved — 2026-07-15
