Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Complete
Last Updated: 2026-08-21
Cycle: 2026-08-21__release-v9.0

# Lessons Learnt — Release Planning 2026-08-21__release-v9.0

## Carry-Forward

Items: 3 — `2026-08-17__release-v8.9`'s own `lessons_learnt_closure.md` `## Carry-Forward` section was checked at STEP -1.5/STEP 0 of this run. All 3 items are informational/advisory for other engines (Roadmap Rebalance, Post-Ship Closure) — none required action within this Release Planning run's write scope. Noted for awareness: 2 Phase-4-originated deferred patches (`ESC-CLOSE-20260821-01`/`-02`, SLA 2026-08-24) are outstanding and outside this routine's write scope to resolve.

## Observations From This Run

- **The "no ready U-item" finding recurred, this time explicitly, not silently.** Neither `BLG-FEAT-73` nor `BLG-FEAT-74` (the only two P1 build-and-ship candidates) cleared their pre-conditions, and the nearest P2 feature candidate (`BLG-FEAT-92`) was blocked on the same unresolved `BLG-FEAT-30` reconciliation as last cycle. This release therefore leads with correctness/follow-through scope rather than new feature scope — flagged explicitly in `release_plan.md`/`cycle_summary.md` rather than left implicit, per the Skill-Silo mitigation rotation guideline's spirit (`release_planning_prompt.md` §3).
- **`BLG-FEAT-92`'s reconciliation gap is now a 2-cycle-recurring pattern, not a one-off.** It was shortlisted and dropped at `2026-08-17__release-v8.9` for the same unresolved dependency on gated `BLG-FEAT-30`, and again this cycle with no change in status. Per the same reasoning that motivates the Perennial-Return Check (§1.4a) for gate-conditional items, a same-shaped pattern is emerging for this item even though it is not formally gate-conditional itself (its blocker is a reconciliation decision, not a data-availability gate). Worth a deliberate PO/Head of Specs Team disposition before a 3rd consecutive silent re-shortlist — recorded here as an advisory precedent, not a formal escalation (no existing rule requires one for this shape of recurrence).
- **A content-level gate with no formal `Gate criteria:` field recurred as a scan-blind-spot instance (BLG-OPS-48 pattern).** `BLG-FEAT-73` and `BLG-FEAT-74` both state real, unmet pre-conditions in prose (`Provisional-Target`/`Type` fields) but carry no formal Gate field, so `scripts/scan_backlog_gate_conditions.py`'s structural scan does not flag them — both required manual exclusion. This is the same data-quality pattern the script's own docstring already names; recorded here as a second live instance to strengthen the case for a `groom backlog` pass adding formal Gate fields to both items.
- **Horizon-signalled (`Provisional-Target: v9.0`) items again ran well short of eventual scope.** 4 items carried the explicit v9.0 signal at scoping time; eventual scope was 27 items. Same observation as `v8.9`'s own lessons learnt regarding `Provisional-Target` density not being a reliable predictor of eventual release size — recorded again as a second data point.

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-21__release-v9.0",
  "phase": "Release",
  "filed_utc": "2026-08-21T00:00:00Z",
  "friction_item_count": 0,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
