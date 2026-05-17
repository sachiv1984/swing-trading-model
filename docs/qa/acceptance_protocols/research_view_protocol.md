**Owner:** Director of Quality
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-05-16
**Story:** ST-10 (EPIC-03, v3.3) — BLG-QA-15
**Cross-reference:** `docs/qa/test_scenarios/research_view_scenarios.md`
**Spec ref:** `docs/specs/frontend/pages/research_view.md`
**Playwright tests:** `tests/e2e/pre-trade-research.spec.js`
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Acceptance Test Protocol — Research View (PT-02)

This document maps each observable acceptance criterion for the PT-02 Research View to its test method: Playwright automated coverage or human staging sign-off.

---

## 1. PT-02 Observable Acceptance Criteria

### AC-RV-01 — Page renders with ticker in title

| AC | Page header shows "{TICKER} — Research" |
|----|----------------------------------------|
| Test scenario | SC-RES-01 |
| Coverage | **Playwright** — `pre-trade-research.spec.js SC-RES-01` |
| Status | Covered |

---

### AC-RV-02 — Price and signal region renders

| AC | Price, ATR, signal badge visible when data available |
|----|-----------------------------------------------------|
| Test scenario | SC-RES-02, SC-RV-01, SC-RV-04 |
| Coverage | **Playwright** — `SC-RES-02` + signal panel tests |
| Status | Covered |

---

### AC-RV-03 — Signal badge reflects API status

| AC | Signal badge: Active (green), Watch (amber), no signal placeholder |
|----|-------------------------------------------------------------------|
| Test scenario | SC-RES-03 |
| Coverage | **Playwright** — `SC-RES-03` |
| Status | Covered |

---

### AC-RV-04 — Price change indicator shows direction

| AC | Price change shows + or − with appropriate colour |
|----|--------------------------------------------------|
| Test scenario | SC-RV-02 |
| Coverage | **Playwright** — `SC-RES-04` |
| Status | Covered |

---

### AC-RV-05 — Regime badge renders for each state

| AC | Regime badge: Risk On / Risk Off / Mixed with correct colours |
|----|--------------------------------------------------------------|
| Test scenario | SC-RV-05 |
| Coverage | **Playwright** — `SC-RV-05` |
| Status | Playwright coverage authored — run against staging |

---

### AC-RV-06 — Source attribution displayed per section

| AC | Each data section shows muted source attribution text |
|----|------------------------------------------------------|
| Test scenario | SC-RV-07, SC-RV-08, SC-RV-09 |
| Coverage | **Human staging sign-off** — visual check required |
| Sign-off criteria | "Source: Yahoo Finance" visible in price panel; "Screener" attribution visible in signal panel; screener panel shows run timestamp |
| Status | Pending — sign-off required before v3.3 delivery verification |

---

### AC-RV-07 — Trade plan panel shows plan when exists

| AC | Active plan card rendered with stop, R/R notes, read-only checklist |
|----|-------------------------------------------------------------------|
| Test scenario | SC-RES-07 |
| Coverage | **Playwright** — `SC-RES-07` |
| Status | Covered |

---

### AC-RV-08 — Trade plan CTA shown when no plan

| AC | "Create Trade Plan" button navigates to `/trade-plans/new?ticker={ticker}` |
|----|--------------------------------------------------------------------------|
| Test scenario | SC-RES-08 |
| Coverage | **Playwright** — `SC-RES-08` |
| Status | Covered |

---

### AC-RV-09 — News headlines render

| AC | Up to 5 headlines with source and relative time |
|----|------------------------------------------------|
| Test scenario | SC-RV-10 |
| Coverage | **Playwright** — `SC-RES-09` |
| Status | Covered |

---

### AC-RV-10 — News empty state

| AC | "No recent news" when news_headlines is empty |
|----|-----------------------------------------------|
| Test scenario | SC-RV-11 |
| Coverage | **Playwright** — `SC-RES-10` |
| Status | Covered |

---

### AC-RV-11 — Full-page error and Retry

| AC | Full-page error with Retry when endpoint fails |
|----|-----------------------------------------------|
| Test scenario | SC-RV-15, SC-RV-16 |
| Coverage | **Playwright** — `SC-RES-11` |
| Status | Covered |

---

### AC-RV-12 — Freshness indicator after 5 minutes

| AC | Stale indicator appears after 5 min; refresh re-fetches |
|----|--------------------------------------------------------|
| Test scenario | SC-RV-13, SC-RV-14 |
| Coverage | **Human staging sign-off** — timer-based behaviour; Playwright timer mocking not yet standardised in this project |
| Sign-off criteria | Open research page; wait 6 minutes; confirm amber indicator appears; click refresh; confirm API re-called |
| Status | Pending — sign-off required before v3.3 delivery verification |

---

### AC-RV-13 — Partial null fields degrade gracefully

| AC | Each null field shows its specific placeholder; no crash |
|----|--------------------------------------------------------|
| Test scenario | SC-RV-17, SC-RV-18, SC-RV-19 |
| Coverage | **Playwright** — `SC-RV-18` and `SC-RV-19` in `pre-trade-research.spec.js` |
| Status | Covered — SC-RV-18 and SC-RV-19 added (ST-06, EPIC-03, v3.6; closes BLG-FE-32) |

---

## 2. Freshness Indicator Acceptance Threshold

- **Threshold:** 5 minutes (300 seconds) of inactivity without re-fetch
- **Display trigger:** Timer starts on page load completion (API response received)
- **Reset trigger:** Any successful re-fetch resets the timer
- **Pass criteria for staging sign-off:** Indicator appears within 30 seconds of the 5-minute threshold (i.e. between 5:00 and 5:30 after load)

---

## 3. Source Attribution Acceptance Criteria (Staging)

For staging sign-off (AC-RV-06):

1. Navigate to `/research/AAPL`
2. Locate price panel → confirm "Yahoo Finance" text is visible in muted style beneath price
3. Locate signal panel → confirm "Screener" attribution is visible
4. Locate screener panel → confirm a run timestamp is displayed
5. Verify no section shows "Source: Unknown" or similar fallback
6. Record pass/fail in QA evidence log

---

## 4. Error State Test Scenarios Enumerated

| Error scenario | Test method | Scenario ID |
|----------------|------------|-------------|
| API 500 (full failure) | Playwright network intercept | SC-RV-15 |
| Retry after error | Playwright | SC-RV-16 |
| Price null only | Playwright | SC-RV-17 |
| Regime null only | Playwright | SC-RV-18 |
| All fields null (degraded) | Playwright | SC-RV-19 |
| News service unavailable | Playwright | SC-RV-12 |
| Ticker not in screener | Playwright | `pre-trade-research.spec.js` screener null |

---

## 5. Sign-off Requirements

Before v3.3 delivery verification:
- [ ] Playwright coverage: all "Covered" rows above pass in CI
- [ ] Human staging: AC-RV-06 (source attribution) signed off
- [ ] Human staging: AC-RV-12 (freshness indicator) signed off
- [x] SC-RV-18/SC-RV-19 Playwright coverage added (ST-06, EPIC-03, v3.6)

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-05-16 | ST-06 (EPIC-03, v3.6): AC-RV-13 status updated to Covered — SC-RV-18 and SC-RV-19 Playwright scenarios added; §5 sign-off checklist updated; closes BLG-FE-32. |
| 1.0 | 2026-05-10 | Initial creation — ST-10 (EPIC-03, v3.3). All PT-02 observable ACs mapped to Playwright or human staging sign-off. |
