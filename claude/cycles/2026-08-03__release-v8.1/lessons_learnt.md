Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-03
Cycle: 2026-08-03__release-v8.1

# Lessons Learnt — Release Planning — v8.1

## What worked well

- Reading each candidate item's full Problem statement (not just its gate-label text) before accepting or rejecting it caught a real substantive miss before any write: `BLG-FE-45`'s gate literally reads "v4.1 sprint planning complete" (trivially true), but its Problem text requires "knowing which Arc 6 compliance data points will be added" — Arc 6 is still unscoped, so the gate's substance is not actually met. Trusting the label alone would have incorrectly promoted the whole Arc 5 UX-prep cluster to firm/conditional scope this cycle.
- The v8.0 `stage2/decisions`/`release_plan.md` deferred-items list was consulted before finalising this cycle's exclusions, confirming the Arc 5 UX-prep cluster and `BLG-FEAT-73`/`BLG-FEAT-74` disposition is a genuine 2nd-consecutive-cycle recurrence (triggering STEP 1.4a) rather than a fresh judgment call reinvented from scratch.
- Honouring "focus on user features where possible" by naming the scarcity plainly (1 of 19 items) rather than relabeling governance/debt work as user-facing to make the instruction appear better-satisfied than the backlog allows.

## Friction Log

### Friction Item 1

**Classification:** Type C — Self-caught verification error (scan-methodology gap, not a prompt defect)

**Recurrence:** Related to, but not identical to, `2026-07-30__release-v8.0`'s Friction Item 1 (`BLG-OPS-48` gate-field-name-variant miss). Same root-cause family: no canonical, reliable method for the ungated-candidate scan.

**What happened:** An initial automated `awk`-based scan across the backlog, used to build a first-pass P1/P2 "ungated" candidate list, incorrectly reported `BLG-BE-24` and `BLG-OPS-48` as having no `**Gate criteria:**` field (both were flagged `NONE`). Both items do carry a gate field — `BLG-BE-24`'s gate is expressed via the canonical `**Gate criteria:**` string, so this was not the v8.0 field-name-variant pattern; the scan script's own line-window logic was insufficiently bounded and missed a gate field that appeared after the point the script stopped scanning within each item's block. Caught before any write: both items were re-verified by reading their full text in a second pass before being added to `release_plan.md §Scope`, and both were correctly excluded.

**Where in the routine:** STEP 2 scope extraction (candidate identification), before STEP 4 commitment.

**Root cause:** Same structural gap named at v8.0's Friction Item 1 — `release_planning_prompt.md` does not define or require a canonical, mechanically-reliable scan procedure for identifying gated vs. ungated candidates; each session re-derives its own ad hoc script or read pattern. Two sessions in a row have now produced a real (self-caught) miss from two different failure modes of that same ad hoc approach (field-name variance at v8.0; scan line-window bounds at v8.1).

**Blast radius analysis:**
- What would have propagated: had either miss gone uncaught, `BLG-BE-24` or `BLG-OPS-48` would have been committed to `stage4_backlog_slice.md`/`backlog.md` as firm scope, then surfaced as blocked/premature at Sprint Planning or Execution — the same returned-to-backlog pattern `release_planning_prompt.md §1.4b` exists to prevent for within-sprint gates (both of these are beyond-sprint gates, an even clearer miss).
- Recovery cost if uncaught: low-medium, same class as v8.0's — manual removal, capacity re-check, S2/ST re-numbering, one stage later than ideal.

**Process patch:** Not filed directly by this engine — new backlog items are outside Release Planning's write scope (`backlog.md` writes are release-slice-only per §7). This is now the 2nd consecutive cycle to produce a self-caught miss from the same underlying "no canonical scan procedure" root cause. Recorded below as a Recurrence Escalation and a Carry-Forward item, recommending the next `groom backlog` or `run roadmap` session file a `BLG-GOV-*` item: add a canonical, scripted (not ad hoc) gate-detection procedure to `release_planning_prompt.md`'s scope-selection guidance, covering all observed gate-field variants (`Gate criteria`, `Gate`, `Gate date`) and requiring a full-block scan rather than a fixed line window.

## Recurrence Escalations

**Recurrence Escalation 1:** 2nd consecutive Release Planning cycle (`v8.0`, `v8.1`) with a self-caught ungated-candidate scan miss, each from a different failure mode of the same ad hoc-scan root cause. Per the v8.0 Carry-Forward item's own stated trigger ("if a second instance ... is found, file a `BLG-GOV-*` item"), this now qualifies — flagged here since this engine cannot file the item itself (outside write scope); the next session with backlog write authority (`groom backlog`, `run roadmap`, or a direct user-directed session fix) should file it.

## Process improvements actioned this run

None (this engine's write scope does not extend to filing new backlog items or patching `release_planning_prompt.md`).

## Outstanding deferred patches

| Patch | Target | Rationale |
|-------|--------|-----------|
| File `BLG-GOV-*`: canonical, scripted gate-detection procedure for Release Planning's scope-selection scan (full-block scan, canonical field-name list: `Gate criteria`, `Gate`, `Gate date`) | Next `groom backlog` or `run roadmap` session | 2nd consecutive cycle with a related self-caught miss (Recurrence Escalation 1) |

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | The ungated-candidate scope-selection scan has now produced a self-caught miss at 2 consecutive Release Planning cycles (v8.0: gate-field-name variant; v8.1: scan line-window bounds) — both caught before a write, neither propagated. | If a 3rd instance occurs, this should be treated as a mandatory action-now patch, not a further carry-forward. | Release Planning |
| 2 | Exactly 1 of 19 scoped items this cycle was genuinely user-facing (`BLG-FE-137`), despite explicit user instruction to prioritise user features — every other `BLG-FEAT-*`/`BLG-FE-*` candidate is gate-blocked, largely on the SI-02 trade-plan-linkage data-density gate. | The next `run roadmap` rebalance should treat this cycle's Product Value Ratio reading as high-signal, and Product Owner should consider whether any near-term, ungated action could accelerate SI-02 data-density clearance rather than only re-deferring the same cluster a further cycle. | Roadmap |

// ARTEFACT_STATUS
```json
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-08-03__release-v8.1",
  "phase": "Release",
  "filed_utc": "2026-08-03T00:40:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 1,
  "escalation_count": 1,
  "overdue_patches": 0,
  "status": "Complete"
}
```
