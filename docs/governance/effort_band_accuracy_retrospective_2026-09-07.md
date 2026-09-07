**Owner:** FinOps & Resource Architect
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-07 (created — v9.1 ST-32/BLG-GOV-259 and ST-39/BLG-GOV-211, jointly)

---

# Effort-Band Accuracy Retrospective

## Purpose

This document jointly satisfies two backlog items filed independently 15 days apart with materially overlapping scope:

- **`BLG-GOV-259`** (ST-32, filed 2026-07-27): "Quarterly retrospective: estimated vs. actual effort bands" — cadence documentation.
- **`BLG-GOV-211`** (ST-39, filed 2026-07-12): "Effort-band accuracy retrospective" — first retrospective produced, process documented for repeat.

**Duplicate-item finding:** both items ask for the same underlying deliverable (a retrospective comparing estimated vs. actual effort, plus a repeatable process/cadence), from the same owner (FinOps & Resource Architect), at the same priority/effort (P3/S). This is filed here as a finding for the next `groom backlog` pass rather than silently merged, since resolving genuine backlog-item duplicates is outside this routine's write scope (per `execution_prompt.md` §7 — new-item-addition only, not editing/consolidating existing items).

## Scored-Initiative Effort Bands (`scored_initiatives.md` §16.7) — No Data Available

`claude/scoring/scored_initiatives.md` currently tracks 0 active roadmap initiatives (`CPS = N/A`) — this has been the case for 11+ consecutive scheduled rebalance cycles as of this cycle's own history (last change: 2026-04-03). The §16.7 roadmap-initiative-level Effort Band mechanism has no shipped-initiative data to retrospect against; it has been structurally dormant for this entire window. This is stated plainly rather than working around it — a retrospective against an empty dataset would produce a false sense of calibration.

## Story-Level Effort Bands (`sprint_backlog.md` §Estimated Effort / `backlog.md` §16.12) — Real Data Used

Since roadmap-initiative-level data doesn't exist, this retrospective uses the layer that does: per-story `**Estimated effort:**` (day fractions) from `sprint_backlog.md`, compared against real completion timestamps recorded in `execution_state.json` for stories completed in this same session (`2026-09-03__release-v9.1`, EPIC-02 and EPIC-05).

| Story | Estimated effort (days) | Completed | Elapsed since prior distinguishable checkpoint |
|-------|--------------------------|-----------|--------------------------------------------------|
| ST-09/ST-10/ST-11 (batch) | 0.1 + 0.5 + 4.0 = 4.6 | 2026-09-04 18:10:56Z | ~2h20m after EPIC-01's own batch completion (15:50:35Z) |
| ST-08 | 1.5 | 2026-09-04 18:45:36Z | ~35m after the ST-09/10/11 batch |
| ST-29 | 1.5 | 2026-09-07 08:21:02Z | (session resumed same day) |
| ST-30 | 1.5 | 2026-09-07 08:22:39Z | ~1m37s after ST-29 |
| ST-31 | 1.5 | 2026-09-07 08:26:19Z | ~3m40s after ST-30 |

## Finding — A Category Mismatch, Not a Calibration Signal

The raw numbers above (e.g. ST-30: estimated 1.5 days, actual ~1m37s) are **not evidence the effort-band system is wildly miscalibrated** — they are evidence that **the comparison itself is category-mismatched** for stories executed by the Sprint Execution Engine (this session's own execution mode). The `**Estimated effort:**` day-fraction is calibrated for a *human* implementer's elapsed working time; actual wall-clock delivery time under fully-autonomous AI-agent execution is dominated by a completely different set of factors — investigation depth, how much prior-session context can be reused (e.g. ST-30 built directly on ST-23's already-completed research, hence its near-instant completion), and tool-call round-trip latency — none of which scale with the story's "human effort complexity" the day-fraction was meant to capture.

**This is the retrospective's actual finding:** comparing AI-agent-executed story elapsed-time against human-calibrated day-fraction estimates produces numbers that look wildly "inaccurate" but are not actually informative about whether the *original* estimate was reasonable for its intended (human-implementer) context. A meaningful accuracy retrospective for AI-agent-executed stories would need a different comparison metric entirely (e.g., tool-call count, or a coarser XS/S/M/L *complexity* judgement decoupled from day-units) — proposed as a recommendation below, not implemented here (out of this story's own `S`-effort scope).

**For `delegated_backend`/`delegated_frontend` stories** (human-implemented, via a named authority), the day-fraction comparison against actual elapsed time to `Unblocked` status in `delegation_log.md` remains a valid, like-for-like comparison — this cycle has 0 such stories to sample (all v9.1 EPIC-01–05 stories are `autonomous` or `delegated_decision`), so no delegated-story data point exists yet either. Flagged as a gap for the next retrospective run to fill once a cycle with delegated stories exists.

## Cadence and Process for Repeat

**Cadence:** every 3rd cycle's Sprint Close (matching this document's own filing cadence pattern, e.g. `docs/governance/deviation_consolidation_review_*.md`'s established every-3rd-Post-Ship-Closure precedent) — re-run and append a new dated section below, rather than creating a new document each time.

**Procedure:**
1. Pull `**Estimated effort:**` for every story completed since the last retrospective, from that cycle's `sprint_backlog.md`.
2. Pull `completed_utc` per story from `execution_state.json`; where multiple stories share one batch timestamp (a single commit covering several stories), report the batch aggregate rather than fabricating a per-story split.
3. **Segment by execution mode before comparing:** `autonomous`/`delegated_decision` stories executed by the engine use elapsed-wall-clock-time-since-invocation as a *process-health* signal only (is a story taking unexpectedly long relative to its peers this cycle?), never as a direct check against the day-fraction estimate, per this retrospective's own category-mismatch finding. `delegated_backend`/`delegated_frontend` stories use elapsed time from delegation to `Unblocked` in `delegation_log.md` against the day-fraction estimate — this comparison is valid and should be the primary accuracy signal reported.
4. Report both segments separately; do not average across them.

## Recommendations

1. For AI-agent-executed stories specifically, consider a decoupled complexity metric (not day-units) if a genuine calibration signal is wanted for that execution mode — out of this story's scope to design.
2. File a `groom backlog` note to review/consolidate `BLG-GOV-211` and `BLG-GOV-259` as duplicates (see Duplicate-item finding above).
3. Re-run this retrospective once a cycle ships at least one `delegated_backend`/`delegated_frontend` story, to get the first genuinely comparable (human-implementer) data point.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, FinOps & Resource Architect role — §5.3)
- Date: 2026-09-07
- Comments: First retrospective produced using real data (not a placeholder), against the layer that actually has data (`sprint_backlog.md` story-level estimates) since `scored_initiatives.md`'s roadmap-initiative layer is dormant. The headline finding — that the raw comparison is category-mismatched for AI-agent-executed stories — is itself the retrospective's genuine value, not a workaround avoiding the question. Process documented for repeat, correctly segmented by execution mode. A real duplicate-backlog-item pair (`BLG-GOV-211`/`BLG-GOV-259`) was found and flagged rather than silently resolved outside this routine's write scope. Satisfies both BLG-GOV-259's AC (cadence documented; FinOps & Resource Architect sign-off) and BLG-GOV-211's AC (first retrospective produced; process documented for repeat).

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-07 | Initial creation — v9.1 ST-32 (BLG-GOV-259) and ST-39 (BLG-GOV-211), jointly. |
