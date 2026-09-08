**Owner:** QA & Testing Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (created — ST-14, v9.2 EPIC-03, BLG-QA-103)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# pip-audit Trend Log

## Purpose

`BLG-QA-103`: `sprint_planning_prompt.md`'s STEP -1 Pre-Sprint Vulnerability Scan (advisory 6) runs `pip-audit -r backend/requirements.txt --format=json` every sprint planning, but until this log existed the result was recorded only in that cycle's own `sprint_planning_notes.md` — nothing tracked whether the same finding recurs, whether a "pip-audit unavailable" gap recurs, or how the dependency count is trending, across cycles.

## Convention

From `sprint_planning_prompt.md` v3.18 onward (this story), STEP -1 advisory 6 appends one row to the table below in the same sprint-planning session that runs the scan, in addition to (not instead of) the existing `sprint_planning_notes.md` note. Columns:

| Column | Meaning |
|--------|---------|
| Cycle | The `cycle_id` this scan ran under |
| Date | Date the scan was run (usually the sprint planning session date) |
| Dependencies scanned | Total resolved dependency count `pip-audit` reported against, or "—" if the tool didn't run |
| Result | `Clean`, `N finding(s)`, or `Unavailable` (tool not installed/runnable) |
| Resolution status | For a non-clean result: `Accepted risk (backlog item)`, `Resolved same cycle`, or `Open`. `—` for `Clean`/`Unavailable` |
| Notes | Anything worth carrying forward — CVE IDs, the specific unavailability cause, notable dependency-count deltas |

A recurring `Unavailable` reading (the same environment gap appearing 2+ consecutive cycles) or a finding whose `Resolution status` stays `Open` across 2+ cycles should be raised as its own backlog item by whoever notices it during a later sprint planning or `groom backlog` pass — this log's job is to make that recurrence visible, not to auto-file anything itself.

## Log

| Cycle | Date | Dependencies scanned | Result | Resolution status | Notes |
|-------|------|----------------------|--------|--------------------|-------|
| `2026-09-07__release-v9.2` | 2026-09-07 | 58 | Clean | — | — |
| `2026-09-03__release-v9.1` | 2026-09-03 | 58 | Clean | — | — |
| `2026-08-21__release-v9.0` | 2026-08-21 | 57 | Clean | — | Dependency count dropped 58→57 vs the prior two readings; not investigated as part of this backfill (no finding was associated with the drop) — noted here so a future reviewer has the data point if the count matters later. |
| `2026-08-17__release-v8.9` | 2026-08-17 | 58 | Clean | — | — |
| `2026-08-14__release-v8.8` | 2026-08-14 | — | Unavailable | — | `pip-audit` not installed in the sprint-planning environment (`command not found`). Recorded as advisory only at the time; did not recur at the next reading (`v8.9`, 5 days later, back to a clean 58-dependency scan) — a one-off environment gap, not a recurring one. |
| `2026-08-12__release-v8.7` | 2026-08-12 | — | Clean | — | Dependency count not stated in the source `sprint_planning_notes.md` entry for this cycle (named specific packages instead of a total) — recorded as "—" rather than guessing a number. |

**Backfill scope note:** the 6 rows above (`v8.7` through `v9.2`) were backfilled from each cycle's own `sprint_planning_notes.md ## Pre-Sprint Vulnerability Scan` section as part of this story (ST-14) — the AC only requires the convention to apply "from the next sprint planning onward," but a log with a single row is not yet a trend, so the most recent 6 available readings were pulled in to give this table an immediately useful starting history. Earlier cycles were not searched — no claim is made about pip-audit's history before `v8.7`.

## Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-09-08 | Sprint Execution Engine | Created (ST-14, EPIC-03, v9.2, BLG-QA-103). Convention documented; backfilled with the 6 most recent readings (`v8.7`–`v9.2`) found in each cycle's `sprint_planning_notes.md`. |
