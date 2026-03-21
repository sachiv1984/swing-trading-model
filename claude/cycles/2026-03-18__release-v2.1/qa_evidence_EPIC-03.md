# QA Evidence Log — EPIC-03 (Alerts & Watchlist)
**Cycle:** 2026-03-18__release-v2.1
**Epic:** EPIC-03

---

## ST-10 — Frontend: Watchlist UI

**Verification method:** Live staging run
**Date:** 2026-03-21
**Signed off by:** Director of Quality

### Acceptance criteria results

| # | AC | Result | Notes |
|---|----|--------|-------|
| 1 | Add ticker — modal opens, saves, appears in table | Pass | |
| 2 | Signal badge renders with correct colours | Pass | |
| 3 | Edit — click ticker, update prices, save | Pass | |
| 4 | Delete — trash icon → inline confirm → fade remove | Pass | |
| 5 | Add to Position — row fades, navigates to Trade Entry with prefill | Pass | |
| 6 | Sort order — Active → Watch → No Signal → alpha within group | Not tested | No test data with mixed signal statuses available on staging |

### DoQ sign-off

**Status: PASS (with deferred AC)**
AC-6 (sort order) deferred — logic is verified by code review (`SIGNAL_ORDER` constant, `sortEntries()` called on add/update/fetch). Full live test requires seeded watchlist data with mixed signal statuses. Filed as post-merge action: seed test data and verify sort order in a future QA session.

---
