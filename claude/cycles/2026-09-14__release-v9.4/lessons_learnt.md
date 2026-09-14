Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-14

---

# Lessons Learnt — Release Planning 2026-09-14__release-v9.4

## Friction Items

**Friction Item 1 — the SLA-breach carry-forward gate (`AUD-2026-09-14-001`) worked exactly as designed, on its very first live trigger.** This session's first invocation of `plan release --version "v9.4"` halted cleanly at STEP -1.6 on `ESC-EXEC-20260910-01` (~26h past SLA, carried unresolved through v9.3's entire Delivery Verification and Post-Ship Closure). The gate was added specifically because that exact escalation had slipped through every prior checkpoint unhalted. Confirms the gap identified in `AUD-2026-09-14-001` is now closed at the one checkpoint that reliably runs before a new cycle opens. No further action needed — noted here as a closed-loop verification, per the same Carry-Forward mechanism pattern used at Post-Ship Closure.

**Friction Item 2 — the design-gate-triggering scan (§1.3/STEP 4.1) initially undercounted by one item, self-caught before publication.** While drafting `run_manifest.md`, the first pass of the observable-UI scan flagged only `BLG-FE-174` and `BLG-FEAT-95` (both explicitly requiring "Playwright coverage/staging sign-off" in their own AC text). `BLG-AI-05` (an in-app disclosure/badge component "applied to the daily-briefing surface") was missed on the first pass because its own AC text names no test/staging method at all — only "documented in a canonical frontend spec" — which reads more like a spec-debt item than a UI-shipping item until the Problem/Scope text is read closely ("Design a small, reusable disclosure/badge component... Apply to the existing AI-surfaced screens"). This is a new failure mode not previously catalogued: an item whose *type* label reads as spec/governance work but whose *scope* text describes shipping a new visible UI element. **Recommendation:** `release_planning_prompt.md` §1.3/STEP 4.1's design-gate scan should explicitly instruct scanning each candidate's `**Scope**` text for UI-shipping verbs ("apply to," "add to the," "component," "badge," "banner") in addition to its `**Acceptance Criteria**`, not rely on AC text alone — an item can ship a visible element while phrasing its own AC in spec-only terms. Caught and corrected within this same session before publication; no incorrect gate value shipped. Recorded as advisory for the next `release_planning_prompt.md` revision touching §1.3/STEP 4.1 — not applied inline this cycle, consistent with the standing "genuine design/wording change needs Head of Specs Team review" distinction from v9.3's own Friction Item 1 disposition.

**Friction Item 3 — the largest ready pool on record (74 items / ~65.05 days) is a direct, mechanical consequence of the prior rebalance's idea-intake window landing almost entirely ungated.** `IW-20260914-01` promoted 42 items directly to backlog with `Provisional-Target: TBD` and no gate conditions (per that rebalance's own STEP 4 disposition — "no hard gate on any item, all ungated and ready"). This is not itself a process gap — the rebalance behaved as designed — but it does mean the ready pool has now more than doubled in one cycle (61→74 items, 41.0→65.05 days) purely from one idea-intake window's output composition, not from any change in delivery rate. Worth a standing watch-item: if idea-intake windows continue landing this ungated-heavy, the ready pool will keep outpacing sprint capacity by a widening margin each cycle (this cycle left 46 items/~37.5 days unselected, up from 34/~13.1 at v9.3), and the case for either raising the capacity ceiling again or introducing a secondary prioritisation pass within the P3 tier (sub-tiering, as `2026-07-06__scheduled`'s Skill-Silo note once speculated) gets stronger each time. Not actioned this cycle — flagged for the next rebalance's own backlog-health review.

## Prompt Change Classification

No process patches proposed this cycle. Friction Item 2's recommendation is deferred to a future `release_planning_prompt.md` revision (Head of Specs Team review needed for exact scan-instruction wording), consistent with how v9.3's own Friction Item 1 (over-capacity selection method codification) was handled.

```yaml
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-09-14__release-v9.4",
  "phase": "Release",
  "filed_utc": "2026-09-14T13:15:00Z",
  "friction_item_count": 3,
  "action_now_count": 0,
  "deferred_count": 1,
  "status": "Active"
}
```
