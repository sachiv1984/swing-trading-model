# system_status.md

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
