Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-24

# QA Evidence — EPIC-06 Market-Data Reliability and CI

**EPIC:** EPIC-06 — Market-Data Reliability and CI
**Cycle:** 2026-11-18__release-v9.18
**Branch:** `exec/2026-11-18__release-v9.18/EPIC-06`

The consolidation block and sign-off are added when every story is done (STEP 3.2.A).

## ST-33 — Show "earnings unknown" when an earnings or gap-risk lookup fails

### Decisions (Product Owner, in session, 2026-11-24)

1. **Retry rule:** an `unavailable` answer is held 60 seconds in the session cache, then the next render retries; it is never cached for the session. Asked because the high code review found no backoff anywhere, so every remount re-sent every failed lookup while Yahoo throttled. Option chosen: "Hold 60s, then retry".
2. **Expanded-row wording:** the Positions expanded row shows "Unknown" after its "Earnings" label; the Alerts cell and Grid view card keep "Earnings: unknown". Option chosen: "'Unknown' in the row".

### DEV-EPIC06-ST33-01
**Priority:** P3
**Story:** ST-33
**AC:** "An `unavailable` answer is retried on the next render rather than cached for the session"
**Expected:** the next render retries (`positions.md` §Earnings Unknown, `screener_results.md` §4, `watchlist.md` §Earnings Cell)
**Actual:** the answer is held 60 seconds, then the first render after that retries; never cached for the session (`src/lib/earningsDataStatus.js` `createAnswerCache`)
**Impact:** a recovered Yahoo shows within 60 seconds rather than at the next render. Prevents the 2026-11-09 burst pattern during throttling.
**Backlog action:** Accepted as-is (Product Owner ruling 2026-11-24); Known Deviation recorded in the three page specs

### DEV-EPIC06-ST33-02
**Priority:** P3
**Story:** ST-33
**AC:** design record §4 / `positions.md` §Earnings Unknown, expanded row "Earnings: unknown"
**Expected:** "Earnings: unknown" in the expanded row
**Actual:** "Unknown" after the row's existing "Earnings" label
**Impact:** wording only; avoids "Earnings  Earnings: unknown"
**Backlog action:** Accepted as-is (Product Owner ruling 2026-11-24); Known Deviation recorded in `positions.md`

---
