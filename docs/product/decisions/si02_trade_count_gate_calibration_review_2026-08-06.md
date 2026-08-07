**Owner:** AI Compliance & Governance Officer
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-08-06
**Cycle:** 2026-08-05__release-v8.3 (ST-24 — BLG-GOV-237)

---

# SI-02 Trade-Count Gate Threshold Calibration Review

## Purpose

`BLG-GOV-237`'s problem statement: SI-02's frontend sprint-planning gate condition (1) — "≥20 closed trades with linked `trade_plans` in production database" — has sat at 0 (of a total 11 trade-plan rows, none linked) for a near-full quarter (unchanged 2026-07-06 through 2026-07-28 across 6 live re-checks; see `current_roadmap.md`'s structured SI-02 gate field). No review has confirmed the threshold itself is still the right calibration point, versus the linkage-UX root cause `BLG-FE-109` was built to fix. This review performs that check, now that `BLG-FE-109` has shipped (v7.3, 2026-07-16 — the story's own gate condition, "review performed after BLG-FE-109 ships," is met).

**Terminology correction:** the backlog item's own title/problem text calls this "SI-02's 11-linked-trade-plan gate threshold." That phrasing conflates two different numbers. Per the actual gate definition (`current_roadmap.md`, `BLG-GOV-107`, v5.3 ST-13): the gate's threshold is **20** closed trades with linked trade plans. The **11** is the current total count of `trade_plans` rows in production (0 of which are linked) — a data point, not the threshold. This review evaluates the actual threshold (20), and separately notes the terminology issue so it isn't repeated.

## What has and hasn't changed

- **`BLG-BE-46`** (shipped v6.8, 2026-07-09): backend forward-fix — auto-links new trade plans to their resulting trade going forward. Does not backfill existing unlinked rows.
- **`BLG-FE-109`** (shipped v7.3, 2026-07-16): frontend fix — adds a "Start Trade from Plan" action, making linkage the path of least resistance rather than a manual step nobody takes. This is the root-cause fix the gate has been waiting on.
- **As of the most recent live re-check (2026-07-28, `2026-07-27__release-v7.9` sprint execution EPIC-08/ST-08):** still 0 of 11 linked. Per `current_roadmap.md`'s own note, this is expected and not a sign the fix failed: "no new trade has been opened via the shipped flow" yet — a data-timing gap (the fix affects future trade creation, and no trade plan has been created *and closed* through it since 2026-07-16), not a re-emergence of the original bug.

## Calibration assessment

**Is 20 still the right threshold?** Yes, with one caveat noted below. The threshold was set as an evidentiary bar for behavioural-drift analysis to be statistically meaningful (per `BLG-GOV-92` Phase 2 criteria) — a small-sample-size concern independent of *why* trades weren't linking. `BLG-FE-109` fixes the *linkage mechanism*, not the *trade volume* the threshold is calibrated against. Removing the linkage friction doesn't argue for a lower threshold; it argues that the threshold is now finally reachable through normal usage rather than staying permanently stuck at 0 regardless of trading activity.

**Caveat — total trade volume is still the binding constraint, not linkage.** The system has only 11 trade-plan rows total to date. Even with every future trade linking automatically, reaching 20 *linked* closed trades requires the *total* trade count to grow well past 20 (since some plans are cancelled/abandoned rather than closed as trades, per `TradePlan.js`'s Abandon flow). This is a trading-cadence question, not a linkage-UX question, and is out of this review's scope — `BLG-FE-109` cannot accelerate it. No threshold change is warranted on this basis either: a lower threshold (e.g. 10, matching SI-02's own internal `_MIN_TRADES` drift-score threshold per `docs/specs/metrics/si02_drift_score.md` §2) would weaken the evidentiary bar for frontend sprint planning specifically, which is a materially different decision (committing frontend build capacity) than the drift-score's own internal statistical-noise threshold.

**Recommendation:** Keep the threshold at 20. Re-check condition (1) at each scheduled roadmap rebalance as already practiced (no process change needed there). If the count has still not moved from 0 by the **next 2 rebalance cycles** after this review (i.e. by early October 2026, given the current ~biweekly cadence), that would indicate `BLG-FE-109`'s fix is not being exercised in practice (e.g. users still not using the "Start Trade from Plan" action) rather than a threshold-calibration problem — a UX adoption question, not answerable by lowering the gate.

## Written conclusion

The 20-closed-linked-trade threshold remains appropriate and is not changed by this review. `BLG-FE-109` addresses the linkage *mechanism*; it does not and should not change the evidentiary *bar*. The persistent 0/11 reading reflects a data-timing gap (no trade has been opened-and-closed via the new flow since shipping) combined with genuinely low total trade volume, not a miscalibrated threshold. No action required on the gate itself. Forward pointer: the next roadmap rebalance's SI-02 structured gate note (`current_roadmap.md`) should link to this review the next time that file is updated (this review does not modify `current_roadmap.md` directly — outside this routine's write scope, per `execution_prompt.md §7`).

## Known Deviations

None. This is a net-new artefact — no prior canonical spec governed this work.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-08-06 | 1.0 | Initial calibration review (ST-24, EPIC-05, v8.3, BLG-GOV-237) |
