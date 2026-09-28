# system_status.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Class 1
**Status:** Canonical
**Version:** 1.2
**Last Updated:** 2026-09-28 (v9.8 design gate — ST-04/BLG-FE-191: new §Endpoint Test Category Labels documenting the endpoint-test-grid categorisation scheme, including the new Replay category); prior — 2026-03-18 (initial spec).
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
| Analytics | `/analytics` | `BarChart3` | violet |
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
| Replay | `/replay` | `RefreshCw` | pink |
| Core | `/health`, exact `GET /`, `/changelog` | `Server` | blue |
| Other | anything else | `HelpCircle` | slate |

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
