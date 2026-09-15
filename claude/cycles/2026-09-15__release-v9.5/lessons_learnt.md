Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-15

---

# Lessons Learnt — Release Planning 2026-09-15__release-v9.5

## Friction Items

**Friction Item 1 — `BLG-SPEC-56`/`BLG-SPEC-57`/`BLG-QA-59` had been excluded from the ready pool for two consecutive cycles (v9.3, v9.4) on a rationale that does not actually apply to them.** Both prior cycles' `run_manifest.md`s grouped these 3 items together with the genuinely gate-blocked `BLG-FEAT-73`/`74`/`76` under a single "data-quality-flagged, treat as not-ready" umbrella, because all 6 shared the same scripted-scan symptom (embedded gate-like free text in `Provisional-Target`, no formal `Gate` field). On direct re-read this session, the 3 SPEC/QA items' own text ("pre-work before PO-02 gate ~2026-10") and `Type` fields ("Spec / Pre-authoring", "Quality Assurance / Pre-design") describe work explicitly meant to be done *ahead of* the PO-02 gate, not work blocked *by* it — the opposite of `BLG-FEAT-73`/`74`/`76`, which each state in their own body text that they may not enter sprint planning yet. The scripted scan's own docstring is explicit that a data-quality warning "does not mark the item gated." Re-included this session (`ST-15`, `ST-23`, `ST-24`) — 2 prior cycles' worth of legitimately-doable pre-work went unscoped as a result of the grouping. **Recommendation:** `release_planning_prompt.md` §1.3a's data-quality-warning handling should note explicitly that a warning is not itself exclusionary — each flagged item's own text must still be read individually before deciding ready/not-ready, rather than treating the whole warning list as a single disposition. Deferred to a future Head of Specs Team-reviewed revision, consistent with how v9.4's own Friction Item 2 (design-gate scan wording) was handled — not applied inline this cycle.

**Friction Item 2 — the first-ever ready P1 items exposed a gap in §1.4c's literal wording.** §1.4c's canonical selection method opens with "P2-first" because every prior cycle's ready pool held 0 P1 items (confirmed at each rebalance's own Production Correctness Fast-Track). This cycle's ready pool held 2 genuine ungated P1 items (`BLG-BE-117`, `BLG-OPS-160`). This session applied the evident intended ordering — P1 ahead of P2 — as a reading of the rule's *purpose* (seat the highest-priority ready work first) rather than its literal text, which does not mention P1 at all. No incorrect scope selection resulted, but a future session could reasonably read §1.4c literally and seat a P1 item behind P2 items, which would be a worse outcome. **Recommendation:** amend §1.4c step 1 to "P1-then-P2-first" (or equivalent) so the rule's text matches its evident intent without requiring re-derivation each time a ready P1 item appears. Deferred to a future Head of Specs Team-reviewed revision — not applied inline this cycle.

**Friction Item 3 — the ready pool tightened sharply from v9.4's 74 items/~65 days to this cycle's 62 items/~44 days**, purely from v9.4's own scope having consumed 28 of those items. Capacity fill landed at 27.99 days, the tightest full-capacity fit yet (0.01 days under the exact ceiling) — a function of the item mix available, not a deliberate precision target. Worth a standing watch, per v9.4's own Friction Item 3: if future idea-intake windows continue landing mostly ungated, the ready pool will refill faster than it can be watched to zero, and the case for a secondary P3-tier prioritisation pass (raised at `2026-07-06__scheduled`) remains open. Not actioned this cycle.

## Prompt Change Classification

No process patches proposed this cycle. Friction Items 1 and 2's recommendations are deferred to a future `release_planning_prompt.md` revision (Head of Specs Team review needed for exact wording), consistent with how v9.4's own Friction Item 2 was handled.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-15__release-v9.5",
  "phase": "Release",
  "filed_utc": "2026-09-15T15:30:00Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 2,
  "status": "Active"
}
```
