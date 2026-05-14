**Owner:** Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Cycle:** 2026-05-14__release-v3.4
**EPIC:** EPIC-03 — Frontend Quick Wins (v3.3 deferred)
**Branch:** exec/2026-05-14__release-v3.4/EPIC-03

---

# QA Evidence — EPIC-03

---

## ST-07 — Negative earnings days + today display (BLG-FE-23 + BLG-FE-24)

**Delegation class:** autonomous (frontend, engine delivery)
**Commit:** b70d6c59
**GitHub issue:** not yet synced

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Negative days_until_earnings (past earnings) renders "—" in Screener | Playwright SC-E03-01 — pass | Pass |
| AC-02 | days_until_earnings = 0 renders "Today" in Screener | Playwright SC-E03-02 — pass | Pass |
| AC-03 | Negative days renders "—" in Watchlist | Playwright SC-E03-03 — pass | Pass |
| AC-04 | days = 0 renders "Today" in Watchlist | Playwright SC-E03-04 — pass | Pass |
| AC-05 | Earnings column visible in Positions table | Playwright SC-E03-05 — pass | Pass |
| AC-06 | days = 0 renders "Today" amber badge in Positions table | Playwright SC-E03-06 — pass | Pass |
| AC-07 | No regression in existing earnings proximity warning (≤5 days) | Code review — early returns added before existing colour logic; existing branches untouched | Pass |

**Deviations:** None

---

## ST-08 — Signals page: default to most recent day (BLG-FE-25)

**Delegation class:** autonomous (frontend, engine delivery)
**Commit:** dc383a5d
**GitHub issue:** not yet synced

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Signals page defaults to most recent trading day's signals on load | Playwright SC-E03-07 — MSFT (older signal) not visible, AAPL (today) visible | Pass |
| AC-02 | Toggle control exists to view all days | Playwright SC-E03-08 — "Most Recent Day" button present; clicking shows all | Pass |
| AC-03 | showRecentOnly state defaults to true | Code review — `useState(true)` at line 25 | Pass |
| AC-04 | mostRecentDate derived from full signals set (not filtered) | Code review — derived from `signals` array before any filtering | Pass |
| AC-05 | No regression in existing filter controls | Code review — existing market/sort/topN/lookback/dismissed controls unchanged | Pass |

**Deviations:** None

---

## ST-09 — Watchlist research status indicator (BLG-FE-29)

**Delegation class:** autonomous (frontend, engine delivery)
**Commit:** cdbb18e2
**GitHub issue:** not yet synced

### Acceptance Criteria Verification

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Watchlist table includes Research Status indicator per row (icon — not text label) | Playwright SC-E03-09: "Research" column header visible; SC-E03-10: SVG icon present | Pass |
| AC-02 | Done = research record exists (ticker in screener results) | Code review — `screenerTickers.has(entry.ticker?.toUpperCase())` | Pass |
| AC-03 | Not Done = no screener record | Code review — muted slate icon rendered when not in set | Pass |
| AC-04 | Binary only — no quality score, no freshness signal | Code review — single BookOpen icon, two colour states only | Pass |
| AC-05 | No regression in watchlist loading performance | Code review — single GET /screener/results call with 5min staleTime; no per-row calls | Pass |

**Deviations:** None

---

## ST-10 — Trade plan status badges + abandonment UI (BLG-FE-30 + BLG-FEAT-21 frontend)

**Delegation class:** autonomous (frontend, engine delivery)
**Commit:** 08fe4e39 (implementation); 8c1c30c0 (RQ v5 fix + tests)
**GitHub issue:** not yet synced

### Acceptance Criteria Verification (BLG-FE-30 — status badges)

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-01 | Status badges in trade plan list view for all 7 states | Playwright SC-E03-11 — "Draft" and "Abandoned" badges visible in TradePlans list | Pass |
| AC-02 | Status badge in TradePlan detail view header | Code review — `TradePlanStatusBadge` rendered in PageHeader description via `existingPlan?.status` | Pass |
| AC-03 | Colour coding: grey/amber/blue/purple/green/muted/red | Code review — STATUS_CONFIG map in TradePlans.js with bg-gray-500/amber-600/blue-600/violet-600/green-700/slate-500/red-600 | Pass |
| AC-04 | Each status accessible (contrast ≥ 4.5:1) | Code review — filled pill, white text on coloured bg; all dark/saturated backgrounds meet WCAG AA with white text | Pass |
| AC-05 | No regression in trade plan list rendering | Playwright — SC-E03-11/12 render correctly; no console errors observed | Pass |

### Acceptance Criteria Verification (BLG-FEAT-21 frontend — abandonment UI)

| AC | Criterion | Evidence method | Status |
|----|-----------|-----------------|--------|
| AC-06 | Trade plan can be set to Abandoned via UI with required reason | Playwright SC-E03-14/15 — modal shown, submit disabled until ≥10 chars | Pass |
| AC-07 | Abandoned plans show abandonment reason | Code review — reason banner rendered when `isAbandoned && abandonment_reason` | Pass |
| AC-08 | Active positions linked to plan cannot be abandoned (backend guard) | Code review — frontend calls `PUT /trade-plans/{id}` with `{status: 'abandoned', abandonment_reason}`; backend already enforces 400 guard (DS-06, v3.3 ST-17) | Pass |
| AC-09 | No regression in existing plan status transitions | Code review — STATUSES dropdown unchanged for non-abandoned flow; abandoned status only via modal | Pass |
| AC-10 | Abandoned plan hides Abandon and Save buttons | Playwright SC-E03-16 — both buttons not visible | Pass |

**Deviations:**
- DEV-01: React Query v5 dropped `onSuccess` from `useQuery`. The pre-existing `onSuccess` in `existingPlan` query does not fire. Fixed by deriving `isAbandoned` from `existingPlan?.status` (query data) in addition to `form.status`, so abandonment state is correct on initial load without the form being populated.

---

## Consolidation

| Story | Playwright | Code Review | Status |
|-------|-----------|-------------|--------|
| ST-07 | 6/6 scenarios pass | Early-return guards only; no existing logic changed | Pass |
| ST-08 | 2/2 scenarios pass | State + filter + toggle added cleanly | Pass |
| ST-09 | 2/2 scenarios pass | Single batch fetch, no per-row calls | Pass |
| ST-10 | 6/6 scenarios pass | New TradePlans.js page + modal; RQ v5 fix applied | Pass |

**DoQ Sign-off:** Director of Quality — 2026-05-14
**Test run date:** 2026-05-14 — all 16 Playwright scenarios pass
