**Owner:** Metrics Definitions & Analytics Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-11 (roadmap rebalance 2026-08-11__scheduled — appended row for DL-078, refreshed sparkline); prior — 2026-08-10 (ST-22, EPIC-06, v8.5 — created, backfilled from decision_log.md prose DL-057 through DL-077)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Created by:** ST-22 (BLG-FEAT-72, EPIC-06, v8.5)

---

# Product Value Ratio History

## Purpose

`roadmap_prompt.md` STEP 2.4 computes a rolling `user_value_ratio` (U ÷ total stories, last 5 cycles) at every roadmap rebalance and records it in that cycle's `run_manifest.md`. Historically, `run_manifest.md` is cycle-scoped and gets superseded each rebalance — the only durable record of the ratio's *trajectory* across cycles was prose embedded in `decision_log.md`'s `**Rationale:**` field (e.g. `"Product Value Ratio: 0.37 (Advisory, improving from 0.209)"`), which had to be re-read and re-derived by eye each time someone wanted to see the trend, and did not consistently carry the full `U/G/D/P` breakdown.

This file is the structured, durable record going forward: one row per rebalance with a PVR reading, appended by `roadmap_prompt.md` STEP 2.4 in the same run that writes `run_manifest.md`. `decision_log.md`'s prose sentence remains the historical narrative record (unchanged), but this file — not prose re-reading — is now the source for trend/sustained-tier checks (e.g. the 3-consecutive-Advisory-readings mandatory-pull-forward rule).

## Sparkline (all readings, chronological, ▁=0.110 min · █=0.42 max recorded)

```
▇▇▆▆▅▄▂▂▆▆▅▇██▇▁
```

## History

| Cycle | Date | Ratio | Tier | U | G | D | P | Total | Window | Decision Log Ref |
|-------|------|-------|------|---|---|---|---|-------|--------|-------------------|
| 2026-06-26__scheduled | 2026-06-26 | 0.37 | Advisory | — | — | — | — | — | IW-20260626-01 (breakdown not recorded in decision_log.md prose this cycle) | DL-057 |
| 2026-07-01__scheduled | 2026-07-01 | 0.36 | Advisory | 21 | 15 | 21 | 2 | 59 | — | DL-058 |
| 2026-07-02__scheduled | 2026-07-02 | 0.344 | Advisory | 21 | 15 | 23 | 2 | 61 | IW-20260702-01 | DL-059 |
| 2026-07-03__scheduled | 2026-07-03 | 0.328 | Advisory | 19 | 15 | 24 | 0 | 58 | v6.1–v6.5 | DL-060 |
| 2026-07-06__scheduled | 2026-07-06 | 0.302 | Advisory | 16 | 12 | 25 | 0 | 53 | v6.2–v6.6 | DL-061 |
| 2026-07-08__scheduled | 2026-07-08 | 0.26 | 🔴 Alert (first time below 0.30 floor) | 12 | 14 | 21 | 0 | 47 | v6.3–v6.7 | DL-062 |
| 2026-07-10__scheduled | 2026-07-10 | 0.18 | 🔴 Alert | 9 | 16 | 24 | 0 | 49 | v6.4-window | DL-063 |
| 2026-07-12__scheduled | 2026-07-12 | 0.21 | 🔴 Alert | 8 | 9 | 21 | 0 | 38 | v6.5–v6.9 | DL-064 |
| 2026-07-13__scheduled | 2026-07-13 | 0.33 | Advisory | 15 | 6 | 24 | 0 | 45 | v6.6-window | DL-065 |
| 2026-07-15__scheduled | 2026-07-15 | 0.31 | Advisory | 15 | 6 | 27 | 0 | 48 | v6.7-window | DL-066 |
| 2026-07-16__scheduled | 2026-07-16 | 0.28 | 🔴 Alert | 13 | 2 | 28 | 3 | 46 | rolling | DL-067 |
| 2026-07-17__scheduled | 2026-07-17 | 0.39 | Advisory | 14 | 0 | 15 | 7 | 36 | v6.9-window | DL-070 |
| 2026-07-24__scheduled | 2026-07-24 | 0.42 | Advisory (improved from 0.39) | — | — | — | — | — | — (breakdown not recorded in decision_log.md prose this cycle) | DL-075 |
| 2026-07-27__scheduled | 2026-07-27 | 0.42 | Advisory (unchanged tier) | — | — | — | — | — | v7.4-v7.8 (breakdown not recorded in decision_log.md prose this cycle) | DL-076 |
| 2026-07-28__scheduled | 2026-07-28 | 0.38 | Advisory (down from 0.42) | — | — | — | — | — | v7.5-v7.9 (breakdown not recorded in decision_log.md prose this cycle) | DL-077 |
| 2026-08-11__scheduled | 2026-08-11 | 0.110 | 🔴 Alert (first time below 0.30 floor since 2026-07-12) | 14 | 30 | 80 | 3 | 127 | v8.1-v8.5 | DL-078 |

**Consecutive Advisory-tier streak (broken 2026-08-11):** The prior 3-reading Advisory streak (2026-07-24, 2026-07-27, 2026-07-28) ended this reading — not because it improved to Healthy, but because it dropped through Advisory straight into 🔴 Alert. Per `roadmap_prompt.md` STEP 2.4's Alert-tier rule (stronger than the sustained-Advisory clause), this reading independently mandates a pull-forward with explicit PO written response — see `cycle_record.md` 2026-08-11__scheduled STEP 2.4/STEP 7.1 for the combined response (this reading's root cause is the same one driving the concurrent Skill-Silo mandatory-pull-forward trigger).

**Most recent scheduled rebalance:** 2026-08-11__scheduled — this history is current as of that run.

## Backfill Method

Rows above were extracted from `decision_log.md`'s `**Rationale:**` prose field for each `DL-xxx` entry mentioning "Product Value Ratio", via a one-time regex extraction pass (`Product Value Ratio\s*(?:moved to)?\s*:?\s*\**\s*([\d.]+)` for the ratio, `U=(\d+)[,\s]*G=(\d+)[,\s]*D=(\d+)[,\s]*P=(\d+)` for the breakdown where present). `DL-068`, `DL-069`, `DL-071`–`DL-074` were checked and confirmed to be non-rebalance decisions (e.g. a release-planning gap resolution) with no PVR reading to backfill — not a gap in the extraction. Rows without a `U/G/D/P` breakdown reflect decision_log.md entries that recorded the ratio and tier but not the full classification table that cycle — exactly the durability gap this file exists to close going forward.

## Maintenance

`roadmap_prompt.md` STEP 2.4 appends one new row to this table (and refreshes the sparkline) at the end of every rebalance that computes a PVR reading, in the same commit as `run_manifest.md`. This file is append-plus-sparkline-refresh — do not edit historical rows.
