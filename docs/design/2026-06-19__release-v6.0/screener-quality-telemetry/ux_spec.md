**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-19
**Approved by:** Product Owner — 2026-06-19
**Cycle:** 2026-06-19__release-v6.0
**Story:** ST-04 (EPIC-03)

---

# UX Spec — Screener Data Quality Telemetry (ST-04)

## Purpose

Replace the prior single-condition degraded-run banner (v3.9 design) with a structured run quality panel that covers three distinct states: FULL, DEGRADED, and FAILED. Users can now see the loaded ratio, which tickers failed, and how fresh the results are — rather than a generic warning.

## Supersedes

`docs/design/2026-05-21__release-v3.9/degraded-run-banner/ux_spec.md` — deprecated. The old `degraded_run: boolean` banner is replaced entirely by this panel.

## Data Source

`GET /screener/results` response envelope gains new fields (v6.0 API contract update):

| Field | Type | Description |
|-------|------|-------------|
| `tickers_requested` | int | Number of tickers in universe queried |
| `tickers_loaded` | int | Number that returned valid OHLCV data |
| `tickers_failed` | string[] | Ticker symbols that failed data fetch |
| `last_full_run_utc` | ISO 8601 | Timestamp of last run where tickers_loaded = tickers_requested |
| `run_quality` | enum | `FULL` \| `DEGRADED` \| `FAILED` |

---

## Placement

- Position: below the page header, above the data freshness indicator and results table (same position as the prior banner)
- Full-width panel spanning the content area

---

## Panel States

### FULL State

| Attribute | Specification |
|-----------|---------------|
| Badge | Green badge — "✓ FULL" |
| Content | Loaded ratio: "{tickers_loaded} / {tickers_requested}" |
| Message | None (clean pass state) |
| Stale advisory | If `last_full_run_utc` > 24h ago: amber sub-line "Last full run: {N} hours ago" appended below loaded ratio |

### DEGRADED State

| Attribute | Specification |
|-----------|---------------|
| Badge | Amber badge — "⚠ DEGRADED" |
| Content | Loaded ratio: "{tickers_loaded} / {tickers_requested}" |
| Message | "Results may be incomplete — {N} tickers failed to load" where N = `tickers_failed.length` |
| Expandable | Chevron button "Show failed tickers ▾"; expands to show `tickers_failed` as a comma-separated list (or pill chips if ≤ 20; plain text wrapped if > 20) |
| Stale advisory | As per FULL state — shown when `last_full_run_utc` > 24h ago |

### FAILED State

| Attribute | Specification |
|-----------|---------------|
| Badge | Red badge — "✗ FAILED" |
| Content | "Screener run failed — no results available" |
| Retry prompt | "Retry Run" button (secondary style); fires `POST /screener/run`; shows spinner while running |
| Failed ticker list | Not shown (run did not produce output) |

---

## Stale Advisory (Cross-State)

When `last_full_run_utc` is older than 24 hours (checked at render time):
- Display amber sub-line: "Last full run: {N} hours ago" (integer hours, rounded down)
- Stale advisory is independent of `run_quality` — a FULL state result can still be stale if the last successful run was > 24h ago

---

## Transition Behaviour

- Panel updates in place when a new screener run is triggered and completes
- DEGRADED failed ticker list collapses when a new run starts (chevron resets to closed)
- FAILED retry button returns to its default state after run completes (success or failure triggers a full panel re-render)

---

## §13 Compliance

Display-only quality telemetry. No automated decisions. No AI-generated content. Fully compliant with strategy_rules.md §13.

## Playwright Test Scenarios

- **SC-SQT-01a**: `run_quality: FULL` → green "✓ FULL" badge and loaded ratio visible; no stale advisory when `last_full_run_utc` < 24h
- **SC-SQT-01b**: `run_quality: FULL` + `last_full_run_utc` > 24h → stale advisory "Last full run: N hours ago" visible
- **SC-SQT-01c**: `run_quality: DEGRADED` → amber "⚠ DEGRADED" badge, loaded ratio, failure message with correct N, and "Show failed tickers" toggle visible
- **SC-SQT-01d**: DEGRADED: expand failed tickers → list of ticker symbols visible; collapse → list hidden
- **SC-SQT-01e**: `run_quality: FAILED` → red "✗ FAILED" badge, failure message, and "Retry Run" button visible; no loaded ratio or ticker list
- **SC-SQT-01f**: Prior `degraded_run: boolean` banner is absent (backwards-compat check: old response without new fields falls back gracefully or shows FAILED state)
