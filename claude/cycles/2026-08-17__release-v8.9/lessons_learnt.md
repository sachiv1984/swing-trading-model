Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Complete
Last Updated: 2026-08-17
Cycle: 2026-08-17__release-v8.9

# Lessons Learnt — Release Planning 2026-08-17__release-v8.9

## Carry-Forward

Items: 0 — `2026-08-14__release-v8.8`'s own `lessons_learnt_closure.md` was checked at STEP -1.5/STEP 0 of this run; all 6 listed items are "Deferred to next cycle" (not `action_now`), so none required action within this Release Planning run. 2 of those deferred items (CI-green per-fix restatement clarification; canonical Sandbox Access Constraint block) have now carried one full cycle transition without a `prompt_change_log.md` entry — flagged in `run_manifest.md` per the originating carry-forward note's own threshold instruction, but actioning them requires write access to `execution_prompt.md`/`shared_standards.md`, outside this routine's write scope.

## Observations From This Run

- **The prior cycle's own recommendation was validated and applied.** `2026-08-14__release-v8.8`'s `lessons_learnt.md` recommended surfacing the widen-vs-tight sizing decision explicitly to the Product Owner whenever `plan release` runs without a `--capacity` directive and the `Provisional-Target`-tagged pool alone leaves significant headroom — exactly this cycle's situation (2 P0 items, ~2.25 days, vs. the confirmed ~24–28 day band). Applied here via an explicit 3-option question (tight / widen / moderate) rather than defaulting silently. This recommendation is also independently tracked as a deferred `release_planning_prompt.md` patch in `2026-08-14__release-v8.8`'s `lessons_learnt_closure.md` (item 5) — this run's real-world application is evidence the pattern is sound and worth formalising in the prompt itself when that patch is next actioned.
- **A brand-new P0 pair arrived mid-cycle from a live production investigation, not from the governed idea-intake pipeline.** Both `BLG-BE-102` and `BLG-BE-103` were filed the same day as this planning session, sourced from a user directly investigating a real position's stop-loss discrepancy rather than from `run ideas`/rebalance. This is a healthy signal that the backlog's direct-filing path works for urgent production-correctness findings, but it also means this cycle's `Provisional-Target: v8.9`-tagged pool (2 items) was far smaller than the eventual scope (22 items) — a reminder that `Provisional-Target` tagging density at scoping time is not a reliable predictor of eventual release size when live-investigation findings can override the tagged pool entirely.
- **A shortlisted P2 item was excluded on its own stated precondition, not a Release Planning judgment call.** `BLG-FEAT-92` passed the gate-detection scan as ungated, but its own item text names an unresolved scope-overlap dependency on the gated `BLG-FEAT-30` requiring explicit PO/Head of Specs Team reconciliation before it may enter sprint planning. This routine correctly deferred to that stated precondition rather than picking an interpretation unilaterally — worth noting as the right pattern for any future item that names its own pre-entry reconciliation requirement in-text.
- **The ungated P1/P2 pool remains structurally thin outside live-investigation findings.** Excluding the 2 P0 items, only 7 ungated P1/P2 items existed at scoping time (1 closed/stale, 6 live, all filed the same session as the P0s) — consistent with `v8.8`'s closure-time observation that this pool is "nearly exhausted." The next release's P1/P2 scope will again depend almost entirely on newly-filed items or gate-clearance events; flagged again for the next scheduled rebalance as a persisting scoping-input signal.

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-17__release-v8.9",
  "phase": "Release",
  "filed_utc": "2026-08-17T14:20:00Z",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
