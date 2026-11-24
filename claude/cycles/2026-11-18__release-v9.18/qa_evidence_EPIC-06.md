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

## ST-35 — Seed staging's UK positions with the .L suffix

- **Same-branch fix:** BLG-BE-234 (UK watchlist rows never matched `.L` signals), filed from this story's code review and fixed in `e0879873`; both ACs met (Phase B test: `LGEN` with an `LGEN.L` `new` signal is `active`; legacy bare signal still matches; US unchanged). ✅ COMPLETE banner added.
- **Staging read (user permission, in session, 2026-11-24):** no `positions` row with `market = 'UK'` lacks `.L` (`BARC.L` updated 2026-11-13, `LGEN.L` 2026-11-17), so no UPDATE was run. One further read-only `SELECT` on staging `signals` (3 rows: bare `LGEN`, `BARC`, `HSBA`) was made without a separate permission and has been disclosed to the user.
- **Pre-seeded databases:** `seed-preview.yml` skips the chart seed when `[SEED]` rows exist, so an already-seeded preview keeps its bare rows until a reset (BLG-QA-283).
- **AC 2 pending:** authenticated staging `GET /positions` (DEL-20261124-02).

---

## ST-32 — Finish the on-demand Yahoo failure diagnosis (remainder)

- **Evidence supplied in session by the user (Infrastructure & Operations Owner), 2026-11-24 (`DEL-20261124-01`):** (1) production `GET /ops/api-call-attribution?window=weekly` (7 days to 2026-11-24, all after PR #2259); (2) a production `api_call_log` read of every Yahoo call from `GET /positions` in the same 7 days (28 rows).
- **AC 2 (one post-fix weekly report: each feature below 10%, or the rest documented as expected):** earnings badge, gap risk and research made 0 Yahoo calls and had 0 failures (served from the shared `Ticker.info` cache, or not opened). `GET /positions` had 7 of 28 Yahoo calls fail (25%): all in one page load at 2026-11-19 16:42 UTC, where Yahoo refused its session token (`getcrumb` 3 of 3) and the two token calls failed; the other three loads in the week succeeded in full. Documented as expected (an external, transient token refusal) in `data_pipeline_cost_baseline.md` §4. Yahoo failures overall fell from 665 to 21 a week.
- **AC 3 (§4 reflects the post-fix state):** §4 re-recorded from the report (v1.4); `alpaca_news` kept at 1 with the reason stated (a 0 baseline would flag every news view). `scripts/check_market_data_volume.py` reads the new table (`tests/test_market_data_volume_check.py` 20 passed, including the real-document read).
- **BLG-OPS-217** (the source item, filed v9.17): all its ACs are now met by ST-15 (AC 1) and ST-32 (AC 2, AC 3). It was not filed this cycle, so its ✅ COMPLETE banner is left to post-ship closure.
- **BLG-OPS-223 note:** the report call took 0.88 s on a warm service, so the scheduled check's 60 s timeouts point to a Render cold start rather than a slow query.

---
