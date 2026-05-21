**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 5)
**Status:** Approved
**Version:** 1.0
**Date:** 2026-05-21
**Approved by:** Product Owner — 2026-05-21
**Cycle:** 2026-05-21__release-v3.9
**Story:** ST-04 (EPIC-01)

---

# UX Spec — Degraded Run Warning Banner (ST-04)

## Purpose

When a screener run completes with >20% of tickers failing OHLCV fetch, the results are potentially incomplete. A visible warning banner alerts the user before they act on the results.

## Trigger Condition

Display this banner when `GET /screener/results` response contains `degraded_run: true`.

Do not display when `degraded_run: false` or when `degraded_run` is absent.

## Placement

- Position: below the page header, above the data freshness indicator (§6) and results table
- Full-width banner spanning the content area
- Dismissed (hidden) immediately when the user triggers a new run (`POST /screener/run`)

## Banner Design

| Attribute | Specification |
|-----------|---------------|
| Background | Amber/yellow warning tone (consistent with existing warning states, e.g. stale data badge in §7) |
| Icon | ⚠ warning icon, left-aligned |
| Text | "Results may be incomplete — {N}% of tickers failed data fetch" where {N} = `Math.round(failure_rate * 100)` |
| Dismiss | No dismiss button — banner persists while degraded run is the latest result |

## §13 Compliance

Display-only. No automated decisions. Purely informational about data availability.

## Playwright Test Scenarios

- **SC-SCR-DEG-01**: `degraded_run: true` in mocked API response → banner visible with correct percentage text
- **SC-SCR-DEG-02**: `degraded_run: false` in mocked API response → banner absent
