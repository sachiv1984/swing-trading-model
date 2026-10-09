**Owner:** Metrics Definitions & Analytics Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-10-09 (ST-34, EPIC-06, v9.11, BLG-GOV-355 — column note: STEP 2.4 now appends both readings; Tier is derived from the story-count Ratio only); prior — 2026-10-08 (ST-34, EPIC-06, v9.11, BLG-GOV-355 — History table gains the effort-weighted ratio, backfilled for the 5 windows computed in metrics_definitions.md Appendix F); prior — 2026-10-08 (roadmap rebalance 2026-10-08__scheduled — appended row for DL-084, refreshed sparkline (0.161, min/max unchanged)); prior history retained — see prior entries in version control
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Created by:** ST-22 (BLG-FEAT-72, EPIC-06, v8.5)

---

# Product Value Ratio History

## Purpose

`roadmap_prompt.md` STEP 2.4 computes a rolling `user_value_ratio` (U ÷ total stories, last 5 cycles) at every roadmap rebalance and records it in that cycle's `run_manifest.md`. Historically, `run_manifest.md` is cycle-scoped and gets superseded each rebalance — the only durable record of the ratio's *trajectory* across cycles was prose embedded in `decision_log.md`'s `**Rationale:**` field (e.g. `"Product Value Ratio: 0.37 (Advisory, improving from 0.209)"`), which had to be re-read and re-derived by eye each time someone wanted to see the trend, and did not consistently carry the full `U/G/D/P` breakdown.

This file is the structured, durable record going forward: one row per rebalance with a PVR reading, appended by `roadmap_prompt.md` STEP 2.4 in the same run that writes `run_manifest.md`. `decision_log.md`'s prose sentence remains the historical narrative record (unchanged), but this file — not prose re-reading — is now the source for trend/sustained-tier checks (e.g. the 3-consecutive-Advisory-readings mandatory-pull-forward rule).

## Sparkline (all readings, chronological, ▁=0.046 min · █=0.42 max recorded)

```
▇▇▇▆▆▅▄▄▆▆▅▇██▇▂▂▁▂▂▂▃
```

## History

| Cycle | Date | Ratio | Effort-weighted Ratio | Tier | U | G | D | P | Total | Window | Decision Log Ref |
|-------|------|-------|-----------------------|------|---|---|---|---|-------|--------|-------------------|
| 2026-06-26__scheduled | 2026-06-26 | 0.37 | — | Advisory | — | — | — | — | — | IW-20260626-01 (breakdown not recorded in decision_log.md prose this cycle) | DL-057 |
| 2026-07-01__scheduled | 2026-07-01 | 0.36 | — | Advisory | 21 | 15 | 21 | 2 | 59 | — | DL-058 |
| 2026-07-02__scheduled | 2026-07-02 | 0.344 | — | Advisory | 21 | 15 | 23 | 2 | 61 | IW-20260702-01 | DL-059 |
| 2026-07-03__scheduled | 2026-07-03 | 0.328 | — | Advisory | 19 | 15 | 24 | 0 | 58 | v6.1–v6.5 | DL-060 |
| 2026-07-06__scheduled | 2026-07-06 | 0.302 | — | Advisory | 16 | 12 | 25 | 0 | 53 | v6.2–v6.6 | DL-061 |
| 2026-07-08__scheduled | 2026-07-08 | 0.26 | — | 🔴 Alert (first time below 0.30 floor) | 12 | 14 | 21 | 0 | 47 | v6.3–v6.7 | DL-062 |
| 2026-07-10__scheduled | 2026-07-10 | 0.18 | — | 🔴 Alert | 9 | 16 | 24 | 0 | 49 | v6.4-window | DL-063 |
| 2026-07-12__scheduled | 2026-07-12 | 0.21 | — | 🔴 Alert | 8 | 9 | 21 | 0 | 38 | v6.5–v6.9 | DL-064 |
| 2026-07-13__scheduled | 2026-07-13 | 0.33 | — | Advisory | 15 | 6 | 24 | 0 | 45 | v6.6-window | DL-065 |
| 2026-07-15__scheduled | 2026-07-15 | 0.31 | — | Advisory | 15 | 6 | 27 | 0 | 48 | v6.7-window | DL-066 |
| 2026-07-16__scheduled | 2026-07-16 | 0.28 | — | 🔴 Alert | 13 | 2 | 28 | 3 | 46 | rolling | DL-067 |
| 2026-07-17__scheduled | 2026-07-17 | 0.39 | — | Advisory | 14 | 0 | 15 | 7 | 36 | v6.9-window | DL-070 |
| 2026-07-24__scheduled | 2026-07-24 | 0.42 | — | Advisory (improved from 0.39) | — | — | — | — | — | — (breakdown not recorded in decision_log.md prose this cycle) | DL-075 |
| 2026-07-27__scheduled | 2026-07-27 | 0.42 | — | Advisory (unchanged tier) | — | — | — | — | — | v7.4-v7.8 (breakdown not recorded in decision_log.md prose this cycle) | DL-076 |
| 2026-07-28__scheduled | 2026-07-28 | 0.38 | 0.457 | Advisory (down from 0.42) | — | — | — | — | — | v7.5-v7.9 (breakdown not recorded in decision_log.md prose this cycle) | DL-077 |
| 2026-08-11__scheduled | 2026-08-11 | 0.110 | 0.115 | 🔴 Alert (first time below 0.30 floor since 2026-07-12) | 14 | 30 | 80 | 3 | 127 | v8.1-v8.5 | DL-078 |
| 2026-09-14__scheduled | 2026-09-14 | 0.092 | 0.109 | 🔴 Alert (2nd consecutive Alert-tier reading, new low) | 16 | 48 | 110 | 0 | 174 | v8.9-v9.3 | DL-079 |
| 2026-09-19__scheduled | 2026-09-19 | 0.046 | 0.021 | 🔴 Alert (3rd consecutive Alert-tier reading, new low) | 9 | 60 | 122 | 4 | 195 | v9.1-v9.5 | DL-080 |
| 2026-09-28__scheduled | 2026-09-28 | 0.089 | 0.093 | 🔴 Alert (4th consecutive Alert-tier reading, improved from prior low) | 14 | 36 | 104 | 4 | 158 | v9.3-v9.7 | DL-081 |
| 2026-09-30__scheduled | 2026-09-30 | 0.094 | — | 🔴 Alert (5th consecutive Alert-tier reading, marginal further improvement) | 16 | 41 | 109 | 4 | 170 | v9.4-v9.8 | DL-082 |
| 2026-10-06__scheduled | 2026-10-06 | 0.096 | — | 🔴 Alert (6th consecutive Alert-tier reading, flat) | 17 | 43 | 114 | 3 | 177 | v9.5-v9.9 | DL-083 |
| 2026-10-08__scheduled | 2026-10-08 | 0.161 | — | 🔴 Alert (7th consecutive Alert-tier reading, improving) | 25 | 36 | 94 | 0 | 155 | v9.6-v9.10 | DL-084 |

**Effort-weighted Ratio column (ST-34, BLG-GOV-355, v9.11):** effort-days of U stories ÷ effort-days of U+G+D+P stories over the same window, defined in `docs/specs/metrics_definitions.md` Appendix F (PVR Measurement Package, `BLG-GOV-339`). The 5 readings shown are the backfill computed and cross-validated there (`scripts/compute_effort_weighted_pvr.py`), placed on the rows whose `Window` they cover; v7.5–v7.9 has no breakdown on its row but its story-count reading reconstructs to the recorded 0.38. "—" means not computed for that row. From `roadmap_prompt.md` v9.32 (STEP 2.4, `BLG-GOV-339` sign-off recorded 2026-10-09, `ESC-EXEC-20261008-03`), each rebalance appends both readings; coverage and any excluded stories are recorded in that rebalance's `run_manifest.md`. The 2026-09-30, 2026-10-06 and 2026-10-08 rows were not computed and stay "—". The Tier column is derived from the story-count Ratio column only; the effort-weighted reading is diagnostic and carries no tier.

**Consecutive Advisory-tier streak (broken 2026-08-11):** The prior 3-reading Advisory streak (2026-07-24, 2026-07-27, 2026-07-28) ended this reading — not because it improved to Healthy, but because it dropped through Advisory straight into 🔴 Alert. Per `roadmap_prompt.md` STEP 2.4's Alert-tier rule (stronger than the sustained-Advisory clause), this reading independently mandates a pull-forward with explicit PO written response — see `cycle_record.md` 2026-08-11__scheduled STEP 2.4/STEP 7.1 for the combined response (this reading's root cause is the same one driving the concurrent Skill-Silo mandatory-pull-forward trigger).

**2nd consecutive Alert-tier reading (2026-09-14):** The Alert first triggered at `2026-08-11__scheduled` (0.110, window v8.1-v8.5) has not recovered — this reading (0.092, window v8.9-v9.3) is lower still, a new low on record. No 5-cycle window entirely postdating `BLG-BE-91`'s v8.6 ship has completed yet (the ship sits inside this window, at v8.6, which falls just before the v8.9-v9.3 window itself — i.e. the fix's own ship cycle has already rolled out of the trailing-5 window), so this reading cannot yet reflect any correction the fix might eventually produce even once linked-trade volume accrues; see `cycle_record.md` 2026-09-14__scheduled STEP 2.4/STEP 7.1 for the full PO response (root-cause fix already funded and shipped last reading; 0 ungated build-and-ship U-item candidates found this cycle, down from 1 at the prior reading).

**3rd consecutive Alert-tier reading (2026-09-19):** 0.046 (window v9.1-v9.5, U=9/G=60/D=122/P=4 of 195) — a new low, down from 0.092. The 5 U-stories in v9.1 remain in this window but roll out at the next reading; with only `BLG-FEAT-96`/`97` (P2, committed at this rebalance) as the next release's U-items, the v9.2-v9.6 window is projected at roughly 6 U of ~182 stories ≈ 0.033, i.e. the ratio is expected to stay in Alert for at least the next 3 readings by construction. The PO response this reading is **Modify** (commit ≥2 build-and-ship U-items) rather than accept-shortfall; the measurement question — the `D` bucket is 122 of 195 stories and cannot distinguish user-protective from hygiene debt — is routed to `BLG-GOV-339`. See `cycle_record.md` 2026-09-19__scheduled STEP 2.4.

**4th consecutive Alert-tier reading, but the first improvement since the Alert began (2026-09-28):** 0.089 (window v9.3-v9.7, U=14/G=36/D=104/P=4 of 158) — up from the 0.046 low, roughly double, because the prior reading's own commitment actually landed: v9.6 shipped 8 U-stories and v9.7 shipped 5 more (13 of the 14 U-stories in this window), directly reflecting the `BLG-FEAT-96`/`97`/`98` pull-forward plus v9.7's own build-and-ship EPICs. Still below the 0.30 floor, so the Alert-tier mandatory-response rule still applies; PO response **Modify** (reaffirmed) — the next `plan release` must again seat ≥1-2 build-and-ship U-items, with no specific item named yet since no release is currently being scoped (Now horizon empty). See `cycle_record.md` 2026-09-28__scheduled STEP 2.4.

**5th consecutive Alert-tier reading, marginal further improvement (2026-09-30):** 0.094 (window v9.4-v9.8, U=16/G=41/D=109/P=4 of 170) — up slightly from 0.089, effectively flat: v9.8 itself shipped only 2 U-classified stories (an all-debt-clearance release), so the window's continued slow rise is now mostly carried by v9.6/v9.7 remaining inside it rather than fresh U-item supply. Still below the 0.30 floor; PO response **Modify**, this time with a concrete, well-specified candidate named — `BLG-BE-135`/`BLG-FE-193` (ATR calculation consolidation + stop-loss transparency), filed this cycle from `IW-20260930-01`, directly answering a live user-reported trust issue. Recommended (not force-selected) for the next `plan release`'s mandatory U-item seat. See `cycle_record.md` 2026-09-30__scheduled STEP 2.4.

**6th consecutive Alert-tier reading, flat (2026-10-06):** 0.096 (window v9.5-v9.9, U=17/G=43/D=114/P=3 of 177) — effectively unchanged from 0.094. v9.9 shipped 2 U-classified stories of 35 (ST-01, `BLG-BE-135` canonical ATR/stop recalculation with timestamps; ST-35, `BLG-FE-192` zero-P&L badge tone). `BLG-FE-193`, the user-facing half of the ATR transparency pair, was not seated because its gate had not cleared at planning time. v9.4's 1 U-story rolled out of the window. PO response **Modify**, now with commitments rather than recommendations: `BLG-FE-193` (gate met — `BLG-BE-135` shipped v9.9) and `BLG-FE-198` (exit dialog pre-selects the known exit reason, new this cycle) are committed to a new `v9.10` Now-horizon section, alongside the STEP 8.0 fast-tracked `BLG-BE-138`. This cycle's full-roster idea intake also filed 4 further ungated build-and-ship candidates (`BLG-FE-196/197/199`, `BLG-FE-195` gate-conditional). See `cycle_record.md` 2026-10-06__scheduled STEP 2.4.

**7th consecutive Alert-tier reading, largest improvement since the Alert began (2026-10-08):** 0.161 (window v9.6-v9.10, U=25/G=36/D=94/P=0 of 155) — up from 0.096. v9.10 shipped 8 U-classified stories of 21 (the `BLG-FE-193`/`BLG-FE-198` commitments plus its EPIC-02 build-and-ship scope), and the all-debt v9.5 (0 U of 43) rolled out of the window. Still below the 0.30 floor; PO response **Modify** with commitments: `BLG-FE-206` and `BLG-BE-154` (both from a direct read of the Risk Dashboard in `IW-20261008-01`) are committed to a new `v9.11` Now section, alongside the STEP 8.0 fast-tracked `BLG-BE-152`. See `cycle_record.md` 2026-10-08__scheduled STEP 2.4.

**Most recent scheduled rebalance:** 2026-10-08__scheduled — this history is current as of that run.

## Backfill Method

Rows above were extracted from `decision_log.md`'s `**Rationale:**` prose field for each `DL-xxx` entry mentioning "Product Value Ratio", via a one-time regex extraction pass (`Product Value Ratio\s*(?:moved to)?\s*:?\s*\**\s*([\d.]+)` for the ratio, `U=(\d+)[,\s]*G=(\d+)[,\s]*D=(\d+)[,\s]*P=(\d+)` for the breakdown where present). `DL-068`, `DL-069`, `DL-071`–`DL-074` were checked and confirmed to be non-rebalance decisions (e.g. a release-planning gap resolution) with no PVR reading to backfill — not a gap in the extraction. Rows without a `U/G/D/P` breakdown reflect decision_log.md entries that recorded the ratio and tier but not the full classification table that cycle — exactly the durability gap this file exists to close going forward.

## Maintenance

`roadmap_prompt.md` STEP 2.4 appends one new row to this table (and refreshes the sparkline) at the end of every rebalance that computes a PVR reading, in the same commit as `run_manifest.md`. This file is append-plus-sparkline-refresh — do not edit historical rows.
