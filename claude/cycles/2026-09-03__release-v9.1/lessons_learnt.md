Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Complete
Last Updated: 2026-09-03
Cycle: 2026-09-03__release-v9.1

# Lessons Learnt — Release Planning 2026-09-03__release-v9.1

## Carry-Forward

Items: 3 — `2026-08-21__release-v9.0`'s own `lessons_learnt_closure.md` `## Carry-Forward` section was checked at STEP -1.5/STEP 0 of this run. Items 1 and 2 (deviation-labelled-field drift, TSG full-document-sweep gap) were both already structurally fixed same-day (2026-09-03) before this session began — confirmed via `prompt_change_log.md`. Item 3 (deferred-patch backlog needing its own periodic clearance pass) is informational and moot given items 1/2's same-day resolution. None required action within this Release Planning run's write scope.

## Observations From This Run

- **The `BLG-FEAT-92`/`BLG-FEAT-30` reconciliation gap, recurring silently for 2 consecutive cycles (v8.9, v9.0), was resolved this session rather than shortlisted-and-dropped a 3rd time.** `2026-08-21__release-v9.0`'s own lessons learnt (as `2026-08-17__release-v8.9`'s before it) explicitly flagged this as "worth a deliberate PO/Head of Specs Team disposition before a 3rd consecutive silent re-shortlist." This session made that disposition: `BLG-FEAT-92` is now formally a `BLG-FEAT-30` sub-scope inheriting its gate, closing the ambiguity rather than perpetuating it. Recorded here as confirmation that a flagged pattern was actually acted on, for future sessions to verify against if the item resurfaces.
- **This is the first v8.5+ release cycle with no live-production-bug or `Provisional-Target`-signalled anchor scope at all.** v9.0 led with 4 PR-review-surfaced items; v8.9 led with 2 live P0 bugs; this cycle had neither — scope is entirely backlog-driven hygiene/debt-clearance, assembled from 5 independently-curated themes. Worth watching whether this reflects a genuinely quieter production/spec surface after 6 consecutive full-capacity releases, or whether backlog curation without any anchor signal is systematically under-surfacing real correctness issues that simply haven't been found yet (as opposed to not existing).
- **3 outstanding passed-`Provisional-Target` items were cleared in the same session that found them.** `backlog_health_20260903.md` (filed at v9.0's own post-ship closure, same day) flagged `BLG-GOV-74`, `BLG-SPEC-132`, and `BLG-GOV-311` as needing a Product Owner decision. All 3 were resolved here — by direct scheduling rather than further re-defer — within 1 day of being flagged, the fastest turnaround of this pattern observed to date.
- **Governance/spec-process debt (EPIC-04 + EPIC-05) accounts for 23 of 41 items (56%) but only 14.4 of 27.5 estimated days (52%)** — a large item count skewed toward small (XS/S) effort, consistent with the backlog's own composition this cycle (many TBD-provisional-target governance-hygiene items filed across recent cycles' PR reviews and closures, none yet cleared). Worth noting for the next Skill-Silo Alert reading: this release's own EPIC composition leans governance/debt-heavy by item count, even though no single EPIC dominates by effort.

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-03__release-v9.1",
  "phase": "Release",
  "filed_utc": "2026-09-03T00:00:00Z",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
