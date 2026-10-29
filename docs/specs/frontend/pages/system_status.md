# system_status.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 1.4
**Last Updated:** 2026-10-29 (v9.14 design gate — ST-28/BLG-FE-217: `/reports` endpoints group under Analytics; the Replay row corrected to the shipped Analytics mapping); prior — 2026-10-16 (v9.13 design gate — ST-10/BLG-SPEC-188: new §Stop Freshness Panel); prior — 2026-09-28 (v9.8 design gate — ST-04/BLG-FE-191: new §Endpoint Test Category Labels documenting the endpoint-test-grid categorisation scheme, including the new Replay category); prior history retained — see prior entries in version control
**Design Source (v1.3 stop freshness):** docs/design/2026-10-16__release-v9.13/stop-freshness-status/decision_record.md
**Design Source (v1.2 endpoint category labels):** docs/design/2026-09-28__release-v9.8/system-status-replay-categorisation/decision_record.md
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

## Purpose & User Goals
The System Status page provides users with visibility into the health of the application’s data sources and operational processes.  
Its goal is to increase user confidence by clearly showing whether the system is functioning normally and whether key services (such as data fetching, pricing, analysis, or settings) are operating correctly.

Users should be able to:
- Confirm that the application is connected and working  
- Understand whether any data source is delayed, stale, or unavailable  
- Recognize whether their actions (position entry, exit, cash management) might be impacted  
- Access relevant troubleshooting steps  

---

## Layout Structure

### Header (global)
- App name/logo  
- Navigation  
- Theme toggle  

### Main Content

#### System Health Overview
A high‑level indicator showing:
- Overall system status (e.g., “All Systems Operational”, “Degraded”, “Service Disruption”)  
- Timestamp of last successful check  

#### Individual Service Cards
Each card displays the health of a specific system:

- **Portfolio Service**  
  - Retrieves portfolio summary and historical values  
  - Shows last update time  

- **Positions Service**  
  - Fetches live position data including prices, stops, tags, notes  
  - Indicates if any values are delayed or could not refresh  

- **Trades Service**  
  - Provides closed‑trade history and journal records  
  - Shows whether trade data is complete  

- **Market Data Service**  
  - Provides price updates, ATR values, and FX rates  
  - Indicates when market data is stale  
  - Highlights if risk regime data is out of date  

- **Settings Service**  
  - Manages strategy and fee configurations  
  - Confirms ability to read and write settings  

- **Journal & Tag Service**  
  - Validates that note updates and tag autocomplete are available  

Each card includes:
- Service name  
- Status indicator (e.g., OK, Delayed, Unavailable)  
- Description of any detected issues  
- Last successful update timestamp  

---

## Stop Freshness Panel (v1.3 — ST-10, BLG-SPEC-188)

**Design source:** `docs/design/2026-10-16__release-v9.13/stop-freshness-status/decision_record.md`

A full-width card placed after Component Health Checks and before Endpoint Tests. It reports how recently open-position stops were recalculated (§7.1), using the metric defined in `metrics_definitions.md`. The figures come from the backend, not computed in the browser.

| Element | Display | `data-testid` |
|---------|---------|---------------|
| Heading | "Stop Freshness" | — |
| Median age | "Median stop age" + value | `stop-freshness-median` |
| Maximum age | "Oldest stop" + value + " · {TICKER}"; `title` holds the exact timestamp | `stop-freshness-max` |
| Coverage | "{k} of {n} open positions" (`k` = positions with a `stop_calculated_at`) | `stop-freshness-coverage` |
| Never recalculated | "{m} never recalculated", only when `m > 0` | `stop-freshness-never` |
| As-of | "As of {local time}" (muted) | — |

- **Age format:** hours with one decimal below 48 h ("18.4 h"), otherwise days and hours ("3 d 6 h").
- NULL `stop_calculated_at` positions are excluded from the median and maximum and counted as never recalculated.
- **Neutral display:** no status colour or threshold in v1.3.
- **States:** no open positions shows "No open positions." (muted). Source unavailable shows "Stop freshness unavailable." (muted, `stop-freshness-unavailable`) and leaves the rest of the page unaffected. Loading shows a single-line `Skeleton`.
- **Tokens:** card `bg-white dark:bg-slate-800/50 border-slate-200 dark:border-slate-700/50`; values `text-slate-900 dark:text-white`; labels `text-slate-600 dark:text-slate-400` (`design_system.md` §Light-Theme Colour Tokens).

**§13:** display only.

---

## Key Components Used
- Status cards  
- Health indicator icons  
- Timestamp labels  
- Error explanation text blocks  

---

## Endpoint Test Category Labels (v1.2 — ST-04, EPIC-01, v9.8, BLG-FE-191)

**Design source:** docs/design/2026-09-28__release-v9.8/system-status-replay-categorisation/decision_record.md

The endpoint test grid (`Tests {N} endpoints`, CLAUDE.md §2) groups each tested endpoint into a category chip via `categorizeEndpoint()` (`SystemStatus.js`), most-specific-pattern-first, falling back to `Other` when nothing matches:

| Category | Match | Icon | Colour |
|----------|-------|------|--------|
| Analytics | `/analytics`, `/replay`, `/reports` *(v1.4 — ST-28, BLG-FE-217)* | `BarChart3` | violet |
| Validation | `/validate` | `Shield` | emerald |
| Alerts | `/alerts`, `/price-alerts` | `Bell` | rose |
| Notifications | `/notifications` | `BellRing` | orange |
| Digest | `/digest` | `Mail` | teal |
| Portfolio | `/position`, `/portfolio` | `Database` | green |
| Trading | `/trades`, `/saved-filters` | `Activity` | cyan |
| Cash Management | `/cash` | `Zap` | amber |
| Market Data | `/signals`, `/market` | `Globe` | indigo |
| Configuration | `/settings` | `Settings` | purple |
| AI | `/ai` | — | (no dedicated icon/colour entry; renders with `Other`'s styling under its own `"AI"` label — pre-existing gap, out of this story's scope) |
| Core | `/health`, exact `GET /`, `/changelog` | `Server` | blue |
| Other | anything else | `HelpCircle` | slate |

**v1.4 (ST-28, BLG-FE-217):** `/reports/*` endpoints group under **Analytics**, matching the app's navigation (`src/Layout.js`: Reports sits in the Analytics group) and the precedent `SystemStatus.js` set for `/replay`. The `/reports` case is checked with the other specific patterns, before Core. No `/reports/*` endpoint appears under Other. The v1.2 table's separate Replay row (`RefreshCw`, pink) is removed: the shipped code maps `/replay` to Analytics (`SystemStatus.js` `categorizeEndpoint()`, comment citing ST-04, v9.8), so the row described a category that was never rendered. Design source: no new record; the v9.8 nav-taxonomy precedent applies.

This section records the current scheme as of v9.8; it does not attempt to reconcile the rest of this page's spec (written for an earlier, higher-level health-card view) with the shipped endpoint-test-grid feature.

---

## States

### Normal Operation
- All service cards show green/healthy state  
- No warnings or delays  
- Dashboard and Positions pages expected to load normally  

### Degraded State
Possible causes:
- Delayed market data  
- Partial failure in position or trade history fetch  
- Tag service unavailable  
- Settings temporarily inaccessible  

User impact:
- Some metrics may appear stale  
- Journal changes may temporarily fail  
- Exit/entry workflows may require retries  

### Outage State
When one or more major services fail:
- Prominent message explaining which service is unavailable  
- Clear guidance on what features are impacted (e.g., “Exiting positions is currently unavailable”)  
- Retry button to attempt reconnection  

---

## Responsive Behavior
- Cards stack vertically on narrow screens  
- Health indicators shift from icon‑left to icon‑top layout on mobile  
- Long service descriptions collapse into expandable accordions for readability  
- Timestamps wrap beneath labels in small viewports  

---

## UX Notes
- Status must be readable at a glance using color, iconography, and concise language  
- Avoid technical jargon; status messages should be user‑friendly  
- Display the most recent update time clearly to reassure users about data freshness  
- When issues occur, present next steps (“Try again”, “Check internet connection”, etc.)  
- Ensure error states never block access to unrelated parts of the application  

---
