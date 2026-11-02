**Owner:** PMO Lead; Challenger
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-11-02 (created — ST-53, EPIC-07, v9.14, BLG-GOV-189)
**Cycle:** 2026-10-29__release-v9.14 (EPIC-07, ST-53)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Governance Overhead Audit — Last 10 Release Cycles (v9.4 to v9.13)

## Question

How much of the team's planned effort and repository activity goes to PMO, spec and governance work, compared with the stories it ships? `BLG-GOV-189` asks for a retrospective estimate over the last 10 release cycles, using each cycle's run manifest and sprint backlog as the proxy, so the next roadmap rebalance can judge whether governance cost is proportionate.

## Method

No cycle records actual hours per story, so this is an estimate from three proxies. Each one can be re-run from the repository.

1. **Planned effort by story class.** For each of the 10 completed release cycles (`2026-09-14__release-v9.4` to `2026-10-16__release-v9.13`), every story with status `done` or `merged` in that cycle's `execution_state.json` is counted as shipped. Its effort is its `**Estimated effort:**` line in the cycle's `sprint_backlog.md`, weighted with `metrics_definitions.md` Appendix F's normalisation table (`scripts/compute_effort_weighted_pvr.py` `parse_effort_weight()`). Its class comes from the `**Source:**` item in the cycle's `stage4_backlog_slice.md`: `BLG-GOV-*` and `BLG-SPEC-*` count as **governance/spec**; every other namespace (`BLG-FE`, `BLG-BE`, `BLG-FEAT`, `BLG-OPS`, `BLG-QA`, `BLG-TECH`, `BLG-AI`, `BLG-SEC`, …) counts as **product/engineering**.
2. **Repository activity by kind.** Non-merge commits on `main` between consecutive cycle start dates (from each cycle folder's date, up to the v9.14 start, 2026-10-29) are split three ways: **code-touching** (any file under `src/`, `backend/`, `tests/`, `scripts/`, `.github/` or `public/`); **spec-only** (otherwise any file under `docs/` outside `docs/governance/`); **process-only** (everything else: `claude/`, `docs/governance/`, `CLAUDE.md`, `.claude/`). Process-only commits are the run manifests, state files, QA evidence, merge-gate records, escalations and prompt edits that each routine writes.
3. **Governance prompt churn.** Rows in `claude/system/prompt_change_log.md` dated inside each window.

Run manifests were read for session timing, but `shared_standards.md` §22 wall-clock logging covers only some routines in some cycles (see `metrics_definitions.md` Appendix F's governance-cycle wall-clock metric), so it is not used as a measure here.

## Results

### Shipped stories and planned effort

| Cycle | Gov/spec stories | Product/eng stories | Gov/spec days | Product/eng days | Gov/spec share of days |
|-------|-----------------:|--------------------:|--------------:|-----------------:|-----------------------:|
| v9.4 | 6 | 22 | 1.95 | 22.60 | 8% |
| v9.5 | 18 | 25 | 12.15 | 17.20 | 41% |
| v9.6 | 11 | 21 | 8.90 | 19.35 | 32% |
| v9.7 | 8 | 20 (+3 unclassified) | 4.85 | 11.15 | 30% |
| v9.8 | 20 | 19 | 11.55 | 16.45 | 41% |
| v9.9 | 16 | 19 | 11.45 | 16.40 | 41% |
| v9.10 | 7 | 14 | 5.00 | 22.90 | 18% |
| v9.11 | 10 | 33 | 5.45 | 22.52 | 19% |
| v9.12 | 14 | 34 | 7.60 | 20.35 | 27% |
| v9.13 | 10 | 30 | 4.80 | 23.20 | 17% |
| **Total** | **120** | **237** (+3) | **73.70** | **192.12** | **28%** |

v9.7's three unclassified stories had no `**Source:**` line or effort entry and are left out of the day totals.

### Repository activity

| Window start | Process-only commits | Spec-only commits | Code-touching commits | All | Prompt change-log rows |
|--------------|---------------------:|------------------:|----------------------:|----:|-----------------------:|
| 2026-09-14 (v9.4) | 24 | 14 | 6 | 44 | 12 |
| 2026-09-15 (v9.5) | 94 | 41 | 27 | 162 | 33 |
| 2026-09-21 (v9.6) | 39 | 9 | 21 | 69 | 10 |
| 2026-09-23 (v9.7) | 84 | 26 | 22 | 132 | 14 |
| 2026-09-28 (v9.8) | 53 | 13 | 15 | 81 | 10 |
| 2026-09-30 (v9.9) | 86 | 21 | 29 | 136 | 24 |
| 2026-10-06 (v9.10) | 46 | 20 | 23 | 89 | 21 |
| 2026-10-08 (v9.11) | 29 | 15 | 34 | 78 | 20 |
| 2026-10-12 (v9.12) | 112 | 32 | 43 | 187 | 30 |
| 2026-10-16 (v9.13) | 61 | 13 | 35 | 109 | 15 |
| **Total** | **628 (58%)** | **204 (19%)** | **255 (23%)** | **1,087** | **189** |

## Findings

1. **Planned governance/spec work is about a quarter of delivery effort.** Over 10 cycles, 120 of 357 classified shipped stories (34%) and 73.7 of 265.8 planned days (28%) came from `BLG-GOV`/`BLG-SPEC` items. It swings widely, from 8% (v9.4) to 41% (v9.5, v9.8, v9.9), and has been lower since v9.10 (17–27%).
2. **Process activity outweighs the stories behind it.** 58% of all commits change only process files, about 1.7 per shipped story (628 over 360), compared with 0.7 code-touching commits per shipped story. Most of these commits are ceremony around stories (state persistence, QA evidence, merge-gate records, escalation mirrors, lessons learnt) rather than governance stories themselves. This cost is not counted in any sprint's capacity.
3. **The governance prompts change about 19 times per cycle.** 189 prompt change-log rows in 10 cycles, about 19 per cycle. Each row triggers the CLAUDE.md §6 checklist (four files per bump), so prompt churn compounds the process-commit count.
4. **Lower governance share has not cut process volume.** v9.13 had the lowest gov/spec share of days (17%) but still 61 process-only commits, against 35 code-touching. The ceremony scales with the number of stories and EPICs, not with how much of the plan is governance work.

## Limits of this estimate

- Planned effort is not actual effort. Estimates are sprint-planning values, not timesheets.
- A commit count is not effort. One process commit can be a one-line state write; one code commit can be a day's work. The commit split shows where activity goes, not how long it takes.
- Classifying by source namespace puts a `BLG-GOV` item that ships a script (for example v9.14's ST-44) under governance, and a `BLG-QA` item that only edits a test plan under product/engineering.
- Wall-clock session time is recorded too sparsely to use.

## Carry-Forward to the Next Roadmap Rebalance

This audit is an input to the next `run roadmap`. It is linked there through this cycle's closure (`2026-10-29__release-v9.14`) as a carry-forward, not by a write to `claude/roadmap/*`. Suggested questions for that rebalance:
- Should sprint capacity reserve explicit time for per-story ceremony (finding 2), rather than leaving it uncounted?
- Can routine records that are always written together (state persistence, merge-gate record, escalation mirror) be combined into fewer commits or generated by script?
- Is ~19 prompt edits per cycle (finding 3) a sign that prompts should change in batches, for example only at post-ship closure?

## Challenger Note

**Challenger — 2026-11-02** (Sprint Execution Engine, agent-mediated in that role per `execution_prompt.md` §5.3). The strongest claim here, finding 2, rests on commit counts, which overstate small writes. Even so, process-only commits outnumber code-touching ones in 9 of 10 windows, and that is robust to the weighting. Finding 1's 28% is a floor for governance cost, not an estimate of it, because the ceremony in finding 2 sits outside every story's estimate. The audit should not be read as saying that governance work is waste. It shows that the cost is real, is mostly unbudgeted, and has not fallen as the governance share of the plan has fallen.
