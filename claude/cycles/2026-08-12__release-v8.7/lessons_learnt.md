Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Filed
Last Updated: 2026-08-12

---

# Lessons Learnt — Release Planning 2026-08-12__release-v8.7

## Friction Items

None. Preflight, gate-detection, and integrity steps all passed cleanly on the first pass. `scored_initiatives.md` was empty (0 active initiatives) — falls back to inline estimates by design, not a friction item.

## Carry-Forward

Items: 2 (from `2026-08-11__release-v8.6`'s own `lessons_learnt_closure.md`, reviewed at STEP 0 of this run, out of this routine's write scope):

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `check_api_performance_baseline_drift.py`'s substring-matching false-negative fix carried 3 consecutive cycles (v8.4→v8.5→v8.6) unapplied; explicit recommendation to file a dedicated sprint story. | **Actioned this cycle** — `BLG-OPS-142` included in scope (EPIC-06/ST-17), closing the carry-forward. | Release Planning (this cycle) |
| 2 | `reports.md` cross-cycle deviation register concentration signal unchanged; 3rd deviation consolidation review not yet due (2 of 3 cycles since 2026-08-08). | No action needed this cycle; re-check due at the 3rd cycle. | Delivery Verification / Post-Ship |

## Observations From This Run

- The ungated `BLG-FEAT-*`/`BLG-FE-*` pool grew from 2 items (v8.6) to 6 items (`BLG-FEAT-84`, `BLG-FE-151`, `BLG-FE-152`, `BLG-FE-156`, `BLG-FE-157`, `BLG-FE-158`) this cycle — a modest but real widening, consistent with v8.6's own observation that `BLG-BE-91`'s trade-plan-linkage enforcement would be "the most direct lever available to widen this pool." `BLG-FE-158` (surfacing the linkage outcome to the user) is a direct second-order product of that same v8.6 fix, filed by an agent-mediated PO review of the resulting PR — worth noting as a concrete example of the lever paying off within one cycle, not just a hoped-for future effect.
- Running `scripts/scan_backlog_gate_conditions.py` before scope selection (rather than after, as an afterthought check) made the "user features first" directive directly actionable: the full ungated FEAT/FE candidate set (6 items) was known before any other category was considered, avoiding the risk of anchoring on debt/process items and only checking user-facing candidates afterward.
- `BLG-BE-96`'s "do not defer further" Product Owner risk-acceptance condition is the first instance this cycle-chain of a release-planning-time item carrying a binding non-deferral instruction from a prior cycle's PR review (rather than from a rebalance or gate). Worth watching whether this becomes a recurring pattern requiring its own tracked field (distinct from `Provisional-Target`) — not yet common enough to warrant a schema change.

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-12__release-v8.7",
  "phase": "Release",
  "filed_utc": "2026-08-12T16:30:00Z",
  "friction_item_count": 0,
  "action_now_count": 1,
  "deferred_count": 1,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
