**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-07 (created — v9.1 ST-27, BLG-GOV-238)

---

# Governed-vs-Ad-Hoc Backlog Scope Visibility Tally

## Purpose

BLG-GOV-238: three independent idea submissions flagged the same pattern — 5 P1 items were added to `backlog.md` outside a governed cycle in one session, with no lightweight tracking of governed-cycle-added vs. ad-hoc session-added items per release, and no visibility into whether ad-hoc additions are displacing gated/scored capacity. This document scopes a lightweight tally mechanism and records the first data point.

## Mechanism

**Definitions:**
- **Governed-cycle addition:** an item that entered `backlog.md` via the governed idea-intake → rebalance → release-planning pipeline (i.e., it was present in a `stage4_backlog_slice.md` for some cycle, or its `Source:` line names an idea-intake window / scheduled rebalance).
- **Ad-hoc addition:** an item added directly to `backlog.md` mid-cycle, outside that pipeline — the narrow exception `execution_prompt.md` §7 grants Sprint Execution (new-item-addition only, for a genuinely out-of-scope finding surfaced while working a different in-scope item). Every such item's `Source:` line names the discovering ST/EPIC and date, per that write-scope rule — this is what makes the tally mechanically countable rather than requiring manual judgement per item.

**Per-cycle tally (recorded once per release cycle, appended below as a new dated row set):**
1. Count of items in that cycle's `stage4_backlog_slice.md` (= governed-cycle additions committed to that cycle).
2. Count of ad-hoc items whose `Source:` line names that cycle's `cycle_id` and an ST/EPIC discovery context (= ad-hoc additions surfaced during that cycle's own execution).
3. Ratio: ad-hoc ÷ governed, as a lightweight "displacement pressure" signal — a rising ratio across consecutive cycles would indicate ad-hoc discoveries are consuming a growing share of scope relative to what governed planning committed to, worth escalating to Release Planning if it becomes a sustained trend.

**Where recorded:** this document (not `run_manifest.md` or `cycle_summary.md`, both Release Planning artefacts outside Sprint Execution's write scope per `execution_prompt.md` §7) — a standalone, append-only tracker any engine or Product Owner can read without needing write access to a different phase's artefacts. `PMO Lead`/`FinOps & Resource Architect` are named readers/owners per BLG-GOV-238's own scope.

**Known limitation (disclosed, not smoothed over):** an ad-hoc item's `Source:` line is only visible in `backlog.md` once the branch that added it has merged to `main`. A count taken from a branch mid-sprint (as this first data point is) will under-count ad-hoc items still sitting on an unmerged sibling branch. The first data point below states which branches were merged at count time and names the one known-but-not-yet-visible item explicitly, rather than presenting a branch-local count as a complete cycle total.

## First Data Point — `2026-09-03__release-v9.1`

**Recorded:** 2026-09-07, from the `exec/2026-09-03__release-v9.1/EPIC-04` branch, with EPIC-01 and EPIC-02 already merged to `main`; EPIC-03's PR (#1537) open but not yet merged; EPIC-05 not yet started.

| Metric | Count | Detail |
|--------|-------|--------|
| Governed-cycle additions | 41 | Full `stage4_backlog_slice.md` scope for this cycle |
| Ad-hoc additions (visible on this branch) | 6 | `BLG-FE-170`, `BLG-QA-157`, `BLG-SPEC-134`, `BLG-FE-171` (EPIC-01 dual PR review, merged); `BLG-TECH-19`, `BLG-OPS-149` (EPIC-02/ST-08, merged) |
| Ad-hoc additions (known, not yet branch-visible) | 2 | `BLG-FE-172` (EPIC-03/ST-13, on the still-open PR #1537 branch); `BLG-OPS-150` (EPIC-04/ST-23, this same branch/session, added after this count was taken — see note) |
| **Total ad-hoc, this cycle so far (best current knowledge)** | **8** | 6 branch-visible + 2 known-pending |
| Ratio (ad-hoc ÷ governed) | 8 ÷ 41 ≈ **0.195** | Using the best-current-knowledge total of 8 |

**Note on `BLG-OPS-150`:** filed by this same ST-27 session's sibling story (ST-23, committed just before this one) — included in the "known, not yet branch-visible" row for completeness since it genuinely exists in this cycle's history, even though a literal git-branch-state snapshot taken at this exact moment would show it as already on this branch (both ST-23 and ST-27 are EPIC-04 stories on the same branch). Listed there rather than in the "visible" row only to keep the row's stated cutoff point unambiguous relative to when the count was actually taken (before ST-23's own commit landed) — a future reader re-deriving this count from `git log` will see 7 branch-visible-at-EPIC-04-completion, not 6; both readings agree once EPIC-03 also merges.

**This cycle is not yet closed** — EPIC-03 and EPIC-05 remain in progress. This data point will be superseded by a final count at this cycle's own sprint close, once all 5 EPIC branches have merged and every ad-hoc addition (if any more are found in EPIC-05) is visible on `main`. Recording an interim, branch-scoped count now — rather than waiting — satisfies BLG-GOV-238's "first data point recorded... where determinable" AC without claiming a false completeness this mid-cycle snapshot cannot have.

## Recommendation

Re-run this tally at each cycle's Sprint Close (STEP 5.3) or Post-Ship Closure, appending a new row set below rather than overwriting this one. After 3-4 cycles of data, the ratio trend becomes meaningful; a single cycle's reading (0.195 here) is not yet a basis for any conclusion about displacement pressure — it establishes the baseline this mechanism exists to build.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, PMO Lead role — §5.3)
- Date: 2026-09-07
- Comments: Tally mechanism scoped (definitions, counting method, ratio, storage location chosen to respect Sprint Execution's actual write scope). First data point recorded for the current cycle (v9.1) rather than v7.1, per the AC's own "v7.1/this cycle where determinable" flexibility — v9.1 is fully within this session's direct knowledge, whereas reconstructing v7.1's governed/ad-hoc split from historical records alone would require re-deriving context this session does not have first-hand. A genuine cross-branch visibility limitation was found and disclosed (2 ad-hoc items exist but are not yet visible from this branch) rather than presented as a complete count. Satisfies BLG-GOV-238's AC.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-07 | Initial creation — v9.1 ST-27, BLG-GOV-238. Mechanism scoped; first data point recorded for `2026-09-03__release-v9.1` (interim, mid-cycle). |
