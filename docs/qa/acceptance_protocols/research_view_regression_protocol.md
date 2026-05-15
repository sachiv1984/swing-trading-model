**Owner:** QA Lead
**Class:** Supporting Document (Class 2)
**Status:** Draft — Awaiting QA Lead Sign-off
**Version:** 0.1
**Last Updated:** 2026-05-15
**Story:** ST-10 (EPIC-03, v3.5) — BLG-QA-19
**Cross-reference:** `docs/qa/acceptance_protocols/research_view_protocol.md`
**API contract:** `docs/specs/api_contracts/research_endpoint.md`
**Playwright tests:** `tests/e2e/pre-trade-research.spec.js`
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Regression Test Protocol — Research View

This protocol defines the canonical set of tests that MUST pass after any modification to the `/research/{ticker}` endpoint (`backend/routers/research.py`) or any research view component (`src/pages/Research.js`, `src/components/research/`).

Any sprint story touching these files must run this protocol and record results in the sprint's QA evidence log before the PR opens.

---

## 1. Trigger Conditions

Run this protocol when ANY of the following change:

| Change type | Examples |
|-------------|---------|
| Research endpoint response schema | Adding/removing/renaming fields in `GET /research/{ticker}` |
| Research backend logic | `backend/routers/research.py`, research service layer |
| Research frontend page | `src/pages/Research.js` |
| Research view components | Any component in `src/components/research/` |
| Research view data additions | IT-series stories adding fields to the research view |

---

## 2. Mandatory Playwright Suite

All tests in this section MUST pass in CI before the PR opens.

### 2.1 PT-02 Base View (Core Research Display)

| Scenario ID | Test | File | Must pass |
|-------------|------|------|-----------|
| SC-RES-01 | Page header shows "{TICKER} — Research" | `pre-trade-research.spec.js` | Yes |
| SC-RES-02 | Price and signal region renders | `pre-trade-research.spec.js` | Yes |
| SC-RES-03 | Signal badge reflects API status | `pre-trade-research.spec.js` | Yes |
| SC-RES-04 | Price change indicator direction | `pre-trade-research.spec.js` | Yes |
| SC-RES-05 | Prospective heat region renders | `pre-trade-research.spec.js` | Yes |
| SC-RES-06 | Heat region degrades on partial endpoint error | `pre-trade-research.spec.js` | Yes |
| SC-RES-07 | Trade plan panel shows plan when exists | `pre-trade-research.spec.js` | Yes |
| SC-RES-08 | Trade plan CTA shown when no plan | `pre-trade-research.spec.js` | Yes |
| SC-RES-09 | News empty state | `pre-trade-research.spec.js` | Yes |
| SC-RES-10 | News empty state with no-signal data | `pre-trade-research.spec.js` | Yes |
| SC-RES-11 | Full-page error + Retry on endpoint failure | `pre-trade-research.spec.js` | Yes |
| SC-RES-12 | Research link in Screener row actions | `pre-trade-research.spec.js` | Yes |
| SC-RES-13 | Research link in Watchlist actions | `pre-trade-research.spec.js` | Yes |

### 2.2 Null / Degraded State Handling

| Scenario ID | Test | Coverage method | Must pass |
|-------------|------|----------------|-----------|
| SC-RV-18 | Regime field null — badge degrades gracefully | Playwright (filed: BLG-FE-33) | Yes — when coverage exists |
| SC-RV-19 | All research fields null — no crash | Playwright (filed: BLG-FE-33) | Yes — when coverage exists |

> **Note:** SC-RV-18 and SC-RV-19 Playwright coverage is pending (BLG-FE-33). Until that backlog item ships, human staging sign-off against these scenarios is required in the QA evidence log.

---

## 3. Human Staging Sign-off Requirements

The following scenarios require human staging sign-off (timer-based or visual behaviour not suitable for Playwright without timer mocking standardisation):

| Scenario | Sign-off criteria |
|----------|------------------|
| AC-RV-06 — Source attribution | "Source: Yahoo Finance" visible in price panel; "Screener" attribution visible in signal panel; timestamp displayed |
| AC-RV-12 — Freshness indicator | Indicator appears within 30s of 5-minute inactivity threshold; refresh re-fetches |

Record staging date and pass/fail in the sprint QA evidence log.

---

## 4. IT-Series Additions Checklist

When an IT-series story adds new fields to the research view, additionally verify:

- [ ] New field renders correctly when API returns a value
- [ ] New field degrades gracefully (shows placeholder/dash) when API returns null
- [ ] No existing SC-RES-* tests broken by the addition
- [ ] If a new Playwright scenario is added for the new field: it is listed in §2 in the next protocol update

**IT-04 (risk signal):** Risk signal badge and R-score field — covered by IT-04 story QA evidence.
**IT-05 (risk prompt display):** Risk prompt panel — covered by IT-05 story QA evidence.
**IT-06 (future):** TBD — update this protocol when IT-06 ships.

---

## 5. Pass Criteria Summary

Before opening any PR that triggers this protocol:

- [ ] All §2.1 Playwright scenarios pass in CI (`npx playwright test pre-trade-research.spec.js`)
- [ ] §2.2 scenarios: Playwright pass (or human staging sign-off if Playwright not yet available)
- [ ] §3 human staging sign-offs recorded in QA evidence log with date
- [ ] §4 IT-series checklist completed if applicable
- [ ] No pre-existing SC-RES-* tests were broken

---

## 6. Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| QA Lead | — | — | Pending |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-05-15 | Initial draft — ST-10 (EPIC-03, v3.5). Canonical regression suite from SC-RES-01 to SC-RES-13; SC-RV-18/19 gap noted; IT-series checklist added. Awaiting QA Lead sign-off. |
